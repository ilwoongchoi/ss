from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from geometry_package.absolute_constants import DELTA_T_OBS_DERIVED


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)


def load_series() -> np.ndarray:
    values: list[float] = []
    with SEIS_PATH.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                values.append(float(row["k_eff"]))
            except (TypeError, ValueError):
                continue
    x = np.asarray(values, dtype=float)
    return (x - np.mean(x)) / (np.std(x) + 1.0e-12)


def moving_average(x: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return x
    kernel = np.ones(window, dtype=float) / float(window)
    return np.convolve(x, kernel, mode="same")


def build_phase_maps(n: int, delta: float) -> list[tuple[str, np.ndarray]]:
    t = np.arange(n, dtype=float)
    t_norm = t / max(n - 1, 1)
    inv_delta = 1.0 / max(delta, 1.0e-12)

    log_num = np.log1p(delta * (n - 1) * t_norm)
    log_den = max(float(np.log1p(delta * (n - 1))), 1.0e-12)
    exp_den = max(float(np.expm1(delta)), 1.0e-12)

    return [
        ("sample_linear", 2.0 * math.pi * delta * t),
        ("norm_linear", 2.0 * math.pi * delta * t_norm),
        ("inv_delta_linear", 2.0 * math.pi * inv_delta * t_norm),
        ("one_minus_delta", 2.0 * math.pi * (1.0 - delta) * t_norm),
        ("power_delta", 2.0 * math.pi * np.power(t_norm, delta)),
        ("power_complement", 2.0 * math.pi * np.power(t_norm, 1.0 - delta)),
        ("log_delta", 2.0 * math.pi * (log_num / log_den)),
        ("exp_delta", 2.0 * math.pi * (np.expm1(delta * t_norm) / exp_den)),
    ]


def build_basis(theta: np.ndarray, delta: float) -> tuple[np.ndarray, list[str], float]:
    n = theta.size
    t_norm = np.arange(n, dtype=float) / max(n - 1, 1)
    x = np.cos(theta)
    y = np.sin(theta)
    z = delta * t_norm
    X = np.column_stack(
        [
            np.ones(n),
            x,
            y,
            z,
            x * y,
            x * z,
            y * z,
            x * x,
            y * y,
            z * z,
            x * y * z,
            x * z * z,
            y * z * z,
        ]
    )
    names = ["bias", "x", "y", "z", "xy", "xz", "yz", "x2", "y2", "z2", "xyz", "xz2", "yz2"]
    turns_total = float((theta[-1] - theta[0]) / (2.0 * math.pi)) if n > 1 else 0.0
    return X, names, turns_total


def fit_projection(y: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, float, float]:
    coeffs = np.linalg.pinv(X) @ y
    fit = X @ coeffs
    resid = y - fit
    rmse = float(np.sqrt(np.mean(resid * resid)))
    explained = 1.0 - float(np.var(resid) / max(np.var(y), 1.0e-12))
    return coeffs, rmse, explained


def top_coefficients(coeffs: np.ndarray, names: list[str], k: int = 8) -> list[dict[str, float | str]]:
    order = np.argsort(np.abs(coeffs))[::-1][:k]
    return [{"name": names[int(i)], "coef": float(coeffs[int(i)])} for i in order]


def build_report(window: int) -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    y = moving_average(load_series(), window=window)
    rows: list[dict[str, object]] = []

    for name, theta in build_phase_maps(len(y), delta=delta):
        X, names, turns_total = build_basis(theta, delta=delta)
        coeffs, rmse, explained = fit_projection(y, X)
        rows.append(
            {
                "phase_map": name,
                "turns_total": turns_total,
                "rmse": rmse,
                "explained_fraction": float(explained),
                "top_coefficients": top_coefficients(coeffs, names),
            }
        )

    rows.sort(key=lambda row: row["explained_fraction"], reverse=True)
    return {
        "domain": "seismology_daily_k_eff",
        "data_path": str(SEIS_PATH),
        "window": int(window),
        "n_points": int(len(y)),
        "delta": delta,
        "rows": rows,
        "best": rows[0],
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Delta-Only Phase Scan",
        "",
        "## Domain",
        f"- data_path: `{report['data_path']}`",
        f"- window: `{report['window']}`",
        f"- n_points: `{report['n_points']}`",
        f"- delta: `{report['delta']}`",
        "",
        "## Best",
        f"- phase_map: `{report['best']['phase_map']}`",
        f"- turns_total: `{report['best']['turns_total']}`",
        f"- rmse: `{report['best']['rmse']}`",
        f"- explained_fraction: `{report['best']['explained_fraction']}`",
        "",
        "## Ranking",
    ]
    for row in report["rows"]:
        lines.append(
            f"- `{row['phase_map']}`: explained=`{row['explained_fraction']}`, rmse=`{row['rmse']}`, turns=`{row['turns_total']}`"
        )
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan delta-only helix phase mappings against one domain.")
    parser.add_argument("--window", type=int, default=15)
    parser.add_argument("--out-json", default="analysis_results/delta_only_phase_scan.json")
    parser.add_argument("--out-md", default="analysis_results/delta_only_phase_scan.md")
    args = parser.parse_args()

    report = build_report(window=args.window)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"best_phase_map={report['best']['phase_map']}")
    print(f"best_explained={report['best']['explained_fraction']}")
    print(f"best_rmse={report['best']['rmse']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
