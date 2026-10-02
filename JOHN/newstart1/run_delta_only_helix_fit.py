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


def build_delta_helix_basis(n: int, delta: float) -> tuple[np.ndarray, list[str], dict[str, float]]:
    t = np.arange(n, dtype=float)
    t_norm = t / max(n - 1, 1)
    theta = 2.0 * math.pi * delta * t

    c = np.cos(theta)
    s = np.sin(theta)

    # delta only:
    # - phase increment uses delta
    # - axial lift uses t_norm scaled by delta
    # - mixed dimensions use only products of those same coordinates
    z = delta * t_norm
    xz = c * z
    yz = s * z

    X = np.column_stack(
        [
            np.ones(n),
            c,
            s,
            z,
            xz,
            yz,
        ]
    )
    names = ["bias", "x_cos", "y_sin", "z_axial", "xz_mix", "yz_mix"]
    meta = {
        "delta": float(delta),
        "phase_turns_total": float((theta[-1] - theta[0]) / (2.0 * math.pi)) if n > 1 else 0.0,
        "z_max": float(z[-1]) if n > 0 else 0.0,
    }
    return X, names, meta


def fit_projection(y: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, float]:
    coeffs = np.linalg.pinv(X) @ y
    fit = X @ coeffs
    resid = y - fit
    rmse = float(np.sqrt(np.mean(resid * resid)))
    explained = 1.0 - float(np.var(resid) / max(np.var(y), 1.0e-12))
    return coeffs, resid, rmse, explained


def build_report(window: int) -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    y = moving_average(load_series(), window=window)
    X, names, meta = build_delta_helix_basis(len(y), delta=delta)
    coeffs, resid, rmse, explained = fit_projection(y, X)

    return {
        "domain": "seismology_daily_k_eff",
        "data_path": str(SEIS_PATH),
        "window": int(window),
        "n_points": int(len(y)),
        "delta_only_helix": meta,
        "basis": names,
        "fit": {
            "rmse": rmse,
            "explained_fraction": float(explained),
            "residual_std": float(np.std(resid)),
            "residual_mean": float(np.mean(resid)),
            "coefficients": {name: float(coeffs[i]) for i, name in enumerate(names)},
        },
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Delta-Only Helix Fit",
        "",
        "## Domain",
        f"- data_path: `{report['data_path']}`",
        f"- window: `{report['window']}`",
        f"- n_points: `{report['n_points']}`",
        "",
        "## Fixed Geometry",
        f"- delta: `{report['delta_only_helix']['delta']}`",
        f"- phase_turns_total: `{report['delta_only_helix']['phase_turns_total']}`",
        f"- z_max: `{report['delta_only_helix']['z_max']}`",
        "- basis: `bias, cos(theta), sin(theta), delta*t, cos(theta)*delta*t, sin(theta)*delta*t`",
        "",
        "## Fit",
        f"- rmse: `{report['fit']['rmse']}`",
        f"- explained_fraction: `{report['fit']['explained_fraction']}`",
        f"- residual_std: `{report['fit']['residual_std']}`",
        f"- residual_mean: `{report['fit']['residual_mean']}`",
        "",
        "## Coefficients",
    ]
    for name, value in report["fit"]["coefficients"].items():
        lines.append(f"- `{name}` = `{value}`")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fit a real domain using a delta-only helix with dimensional mixing.")
    parser.add_argument("--window", type=int, default=15)
    parser.add_argument("--out-json", default="analysis_results/delta_only_helix_fit.json")
    parser.add_argument("--out-md", default="analysis_results/delta_only_helix_fit.md")
    args = parser.parse_args()

    report = build_report(window=args.window)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"explained={report['fit']['explained_fraction']}")
    print(f"rmse={report['fit']['rmse']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
