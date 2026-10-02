from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from geometry_package.absolute_constants import DELTA_T_OBS_DERIVED, SPARK_ANGLE_DEG, SPARK_ANGLE_RAD


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)


def load_k_eff() -> np.ndarray:
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


def fit_3d_helix(x: np.ndarray, delta: float, theta: float) -> dict[str, object]:
    n = x.size
    phase = theta * np.arange(n, dtype=float)

    # Best 3D cylinder fit with fixed chirality radius.
    # x_obs is mapped against the rotating x-z projection with fixed radius delta.
    basis_cos = delta * np.cos(phase)
    basis_sin = delta * np.sin(phase)
    A = np.vstack([basis_cos, basis_sin, np.ones(n)]).T
    coeffs, *_ = np.linalg.lstsq(A, x, rcond=None)
    fit = A @ coeffs
    residual = x - fit

    return {
        "coeff_cos": float(coeffs[0]),
        "coeff_sin": float(coeffs[1]),
        "bias": float(coeffs[2]),
        "fit": fit,
        "residual": residual,
        "rmse": float(np.sqrt(np.mean(residual * residual))),
    }


def fit_w_constant(residual: np.ndarray) -> dict[str, float]:
    w_abs = float(np.sqrt(np.mean(residual * residual)))
    return {
        "w_constant_rms": w_abs,
        "residual_mean": float(np.mean(residual)),
        "residual_std": float(np.std(residual)),
    }


def fit_w_function(residual: np.ndarray) -> dict[str, object]:
    n = residual.size
    t = np.arange(n, dtype=float)
    t_norm = t / max(n - 1, 1)
    B = np.vstack([np.ones(n), t_norm, t_norm * t_norm]).T
    coeffs, *_ = np.linalg.lstsq(B, residual, rcond=None)
    fitted = B @ coeffs
    rem = residual - fitted
    return {
        "w0": float(coeffs[0]),
        "w1": float(coeffs[1]),
        "w2": float(coeffs[2]),
        "rmse_after_w": float(np.sqrt(np.mean(rem * rem))),
        "fitted": fitted,
        "remaining": rem,
    }


def build_report(window: int) -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    theta = float(SPARK_ANGLE_RAD)
    series_raw = load_k_eff()
    series = moving_average(series_raw, window=window)

    fit3d = fit_3d_helix(series, delta=delta, theta=theta)
    w_const = fit_w_constant(np.asarray(fit3d["residual"], dtype=float))
    w_func = fit_w_function(np.asarray(fit3d["residual"], dtype=float))

    explained_3d = 1.0 - (fit3d["rmse"] ** 2 / max(float(np.var(series)), 1.0e-12))
    explained_4d = 1.0 - (w_func["rmse_after_w"] ** 2 / max(float(np.var(series)), 1.0e-12))

    return {
        "domain": "seismology_daily_k_eff",
        "data_path": str(SEIS_PATH),
        "locked_parameters": {
            "delta": delta,
            "spark_angle_deg": float(SPARK_ANGLE_DEG),
            "window": int(window),
            "n_points": int(series.size),
        },
        "fit_3d": {
            "coeff_cos": fit3d["coeff_cos"],
            "coeff_sin": fit3d["coeff_sin"],
            "bias": fit3d["bias"],
            "rmse": fit3d["rmse"],
            "explained_fraction": float(explained_3d),
        },
        "fit_4d": {
            "w_constant_rms": w_const["w_constant_rms"],
            "residual_mean": w_const["residual_mean"],
            "residual_std": w_const["residual_std"],
            "w0": w_func["w0"],
            "w1": w_func["w1"],
            "w2": w_func["w2"],
            "rmse_after_w": w_func["rmse_after_w"],
            "explained_fraction_after_w": float(explained_4d),
        },
        "verdict": {
            "w_needed": bool(w_const["w_constant_rms"] > 0.0),
            "w_behaves_like_constant": bool(abs(w_func["w1"]) < 1.0e-3 and abs(w_func["w2"]) < 1.0e-3),
            "candidate_4d_constant": float(w_const["w_constant_rms"]),
        },
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Single Domain 4D Fit",
        "",
        "## Locked Parameters",
        f"- delta: `{report['locked_parameters']['delta']}`",
        f"- spark_angle_deg: `{report['locked_parameters']['spark_angle_deg']}`",
        f"- window: `{report['locked_parameters']['window']}`",
        f"- n_points: `{report['locked_parameters']['n_points']}`",
        "",
        "## 3D Fit",
        f"- coeff_cos: `{report['fit_3d']['coeff_cos']}`",
        f"- coeff_sin: `{report['fit_3d']['coeff_sin']}`",
        f"- bias: `{report['fit_3d']['bias']}`",
        f"- rmse: `{report['fit_3d']['rmse']}`",
        f"- explained_fraction: `{report['fit_3d']['explained_fraction']}`",
        "",
        "## 4D Fit",
        f"- w_constant_rms: `{report['fit_4d']['w_constant_rms']}`",
        f"- residual_std: `{report['fit_4d']['residual_std']}`",
        f"- w0: `{report['fit_4d']['w0']}`",
        f"- w1: `{report['fit_4d']['w1']}`",
        f"- w2: `{report['fit_4d']['w2']}`",
        f"- rmse_after_w: `{report['fit_4d']['rmse_after_w']}`",
        f"- explained_fraction_after_w: `{report['fit_4d']['explained_fraction_after_w']}`",
        "",
        "## Verdict",
        f"- w_needed: `{report['verdict']['w_needed']}`",
        f"- w_behaves_like_constant: `{report['verdict']['w_behaves_like_constant']}`",
        f"- candidate_4d_constant: `{report['verdict']['candidate_4d_constant']}`",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fit one real domain with fixed delta=0.2828 and theta=138.88deg, then push residual into a 4D term."
    )
    parser.add_argument("--window", type=int, default=15)
    parser.add_argument("--out-json", default="analysis_results/single_domain_4d_fit.json")
    parser.add_argument("--out-md", default="analysis_results/single_domain_4d_fit.md")
    args = parser.parse_args()

    report = build_report(window=args.window)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"rmse_3d={report['fit_3d']['rmse']}")
    print(f"w_constant={report['fit_4d']['w_constant_rms']}")
    print(f"rmse_4d={report['fit_4d']['rmse_after_w']}")
    print(f"candidate_4d_constant={report['verdict']['candidate_4d_constant']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
