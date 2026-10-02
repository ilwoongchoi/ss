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


def build_fill_maps(n: int, delta: float) -> list[tuple[str, np.ndarray]]:
    t = np.arange(n, dtype=float)
    t_norm = t / max(n - 1, 1)
    log_plain = np.log1p((n - 1) * t_norm)
    log_plain /= max(float(np.log1p(n - 1)), 1.0e-12)
    log_delta = np.log1p(delta * (n - 1) * t_norm)
    log_delta /= max(float(np.log1p(delta * (n - 1))), 1.0e-12)
    power_delta = np.power(t_norm, delta)
    return [
        ("norm_fill", t_norm),
        ("log_fill", log_plain),
        ("log_delta_fill", log_delta),
        ("power_delta_fill", power_delta),
    ]


def build_phase_maps(s: np.ndarray, delta: float) -> list[tuple[str, np.ndarray]]:
    log_num = np.log1p(delta * s)
    log_den = max(float(np.log1p(delta)), 1.0e-12)
    return [
        ("linear_post", 2.0 * math.pi * s),
        ("log_post", 2.0 * math.pi * (log_num / log_den)),
        ("power_delta_post", 2.0 * math.pi * np.power(s, delta)),
        ("power_complement_post", 2.0 * math.pi * np.power(s, 1.0 - delta)),
    ]


def build_basis(fill: np.ndarray, theta: np.ndarray, delta: float, gate_mode: str) -> tuple[np.ndarray, list[str], dict[str, float]]:
    if gate_mode == "hard":
        gate = (fill >= delta).astype(float)
    else:
        sharpness = 40.0
        gate = 1.0 / (1.0 + np.exp(-sharpness * (fill - delta)))

    post = np.clip((fill - delta) / max(1.0 - delta, 1.0e-12), 0.0, 1.0)
    x = gate * np.cos(theta)
    y = gate * np.sin(theta)
    z = gate * delta * post

    X = np.column_stack(
        [
            np.ones(fill.size),
            1.0 - gate,
            gate,
            x,
            y,
            z,
            x * y,
            x * z,
            y * z,
            z * z,
            x * y * z,
        ]
    )
    names = ["bias", "observer_only", "energy_on", "x", "y", "z", "xy", "xz", "yz", "z2", "xyz"]
    meta = {
        "gate_fraction_on": float(np.mean(gate)),
        "post_extent": float(np.max(post)),
        "turns_total": float((theta[-1] - theta[0]) / (2.0 * math.pi)) if theta.size > 1 else 0.0,
    }
    return X, names, meta


def fit_projection(y: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, float, float]:
    coeffs = np.linalg.pinv(X) @ y
    fit = X @ coeffs
    resid = y - fit
    rmse = float(np.sqrt(np.mean(resid * resid)))
    explained = 1.0 - float(np.var(resid) / max(np.var(y), 1.0e-12))
    return coeffs, rmse, explained


def top_coefficients(coeffs: np.ndarray, names: list[str], k: int = 6) -> list[dict[str, float | str]]:
    order = np.argsort(np.abs(coeffs))[::-1][:k]
    return [{"name": names[int(i)], "coef": float(coeffs[int(i)])} for i in order]


def build_report(window: int) -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    y = moving_average(load_series(), window=window)
    rows: list[dict[str, object]] = []

    for fill_name, fill in build_fill_maps(len(y), delta=delta):
        post = np.clip((fill - delta) / max(1.0 - delta, 1.0e-12), 0.0, 1.0)
        for phase_name, theta in build_phase_maps(post, delta=delta):
            for gate_mode in ("hard", "smooth"):
                X, names, meta = build_basis(fill, theta, delta=delta, gate_mode=gate_mode)
                coeffs, rmse, explained = fit_projection(y, X)
                rows.append(
                    {
                        "fill_map": fill_name,
                        "phase_map": phase_name,
                        "gate_mode": gate_mode,
                        "rmse": rmse,
                        "explained_fraction": float(explained),
                        "gate_fraction_on": meta["gate_fraction_on"],
                        "turns_total": meta["turns_total"],
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
        "best": rows[0],
        "rows": rows,
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Delta Gate Phase Scan",
        "",
        "## Domain",
        f"- data_path: `{report['data_path']}`",
        f"- window: `{report['window']}`",
        f"- n_points: `{report['n_points']}`",
        f"- delta: `{report['delta']}`",
        "",
        "## Best",
        f"- fill_map: `{report['best']['fill_map']}`",
        f"- phase_map: `{report['best']['phase_map']}`",
        f"- gate_mode: `{report['best']['gate_mode']}`",
        f"- explained_fraction: `{report['best']['explained_fraction']}`",
        f"- rmse: `{report['best']['rmse']}`",
        f"- gate_fraction_on: `{report['best']['gate_fraction_on']}`",
        f"- turns_total: `{report['best']['turns_total']}`",
        "",
        "## Ranking",
    ]
    for row in report["rows"][:12]:
        lines.append(
            f"- `{row['fill_map']} / {row['phase_map']} / {row['gate_mode']}`: explained=`{row['explained_fraction']}`, rmse=`{row['rmse']}`, on=`{row['gate_fraction_on']}`, turns=`{row['turns_total']}`"
        )
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan delta-threshold gate models on one domain.")
    parser.add_argument("--window", type=int, default=15)
    parser.add_argument("--out-json", default="analysis_results/delta_gate_phase_scan.json")
    parser.add_argument("--out-md", default="analysis_results/delta_gate_phase_scan.md")
    args = parser.parse_args()

    report = build_report(window=args.window)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"best_fill_map={report['best']['fill_map']}")
    print(f"best_phase_map={report['best']['phase_map']}")
    print(f"best_gate_mode={report['best']['gate_mode']}")
    print(f"best_explained={report['best']['explained_fraction']}")
    print(f"best_rmse={report['best']['rmse']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
