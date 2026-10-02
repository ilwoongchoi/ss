from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from geometry_package import absolute_constants as ac


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


def rotate_complex(z: complex, angle_rad: float) -> complex:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return complex((c * z.real) - (s * z.imag), (s * z.real) + (c * z.imag))


def normalize(v: np.ndarray) -> np.ndarray:
    v = np.nan_to_num(v, nan=0.0, posinf=0.0, neginf=0.0)
    m = float(np.max(np.abs(v)))
    if m <= 1.0e-12:
        return np.zeros_like(v)
    return v / m


def simulate_minimal_state(n: int, delta: float, kappa: float, theta_deg: float, phi: float) -> dict[str, np.ndarray]:
    z = complex(delta, kappa)
    theta = math.radians(theta_deg)
    z_hist = np.zeros(n, dtype=np.complex128)

    for i in range(n):
        level = (i % 10) + 1
        phi_scale = phi ** (-(level - 1))
        c_level = complex(delta * phi_scale, kappa * phi_scale)
        raw = (z * z) + c_level
        if not math.isfinite(raw.real) or not math.isfinite(raw.imag):
            raw = complex(0.0, 0.0)
        raw_norm = abs(raw)
        if raw_norm > 1.0e6:
            raw = raw / raw_norm
        z = rotate_complex(raw, theta)
        if not math.isfinite(z.real) or not math.isfinite(z.imag):
            z = complex(0.0, 0.0)
        z_hist[i] = z

    real = z_hist.real
    imag = z_hist.imag
    amp = np.abs(z_hist)
    phase = np.unwrap(np.angle(z_hist + 1.0e-12))
    dphase = np.gradient(phase)

    return {
        "z_real": normalize(real),
        "z_imag": normalize(imag),
        "z_abs": normalize(amp),
        "phase": normalize(phase),
        "dphase": normalize(dphase),
    }


def build_basis(state: dict[str, np.ndarray]) -> tuple[np.ndarray, list[str]]:
    n = state["z_real"].size
    X = np.column_stack(
        [
            np.ones(n),
            state["z_real"],
            state["z_imag"],
            state["z_abs"],
            state["phase"],
            state["dphase"],
        ]
    )
    names = ["bias", "z_real", "z_imag", "z_abs", "phase", "dphase"]
    return X, names


def score_fit(y: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, float, float]:
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)
    coeffs = np.linalg.pinv(X) @ y
    fit = X @ coeffs
    resid = y - fit
    rmse = float(np.sqrt(np.mean(resid * resid)))
    explained = 1.0 - float(np.var(resid) / max(np.var(y), 1.0e-12))
    return coeffs, rmse, explained


def evaluate_params(y: np.ndarray, delta: float, kappa: float, theta_deg: float, phi: float) -> dict[str, object]:
    state = simulate_minimal_state(len(y), delta=delta, kappa=kappa, theta_deg=theta_deg, phi=phi)
    X, names = build_basis(state)
    coeffs, rmse, explained = score_fit(y, X)
    return {
        "delta": float(delta),
        "kappa": float(kappa),
        "theta_deg": float(theta_deg),
        "phi": float(phi),
        "coeffs": {name: float(coeffs[i]) for i, name in enumerate(names)},
        "rmse": rmse,
        "explained_fraction": explained,
    }


def search(y: np.ndarray, trials: int, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)

    delta0 = float(ac.DELTA_T_OBS_DERIVED)
    kappa0 = float(ac.OMEGA_KAPPA)
    theta0 = float(ac.SPARK_ANGLE_DEG)
    phi0 = float(ac.PHI)

    best = evaluate_params(y, delta=delta0, kappa=kappa0, theta_deg=theta0, phi=phi0)

    coarse_bounds = {
        "delta": (0.05, 0.8),
        "kappa": (0.005, 0.25),
        "theta_deg": (90.0, 180.0),
        "phi": (1.2, 2.2),
    }

    for _ in range(trials):
        cand = evaluate_params(
            y,
            delta=float(rng.uniform(*coarse_bounds["delta"])),
            kappa=float(rng.uniform(*coarse_bounds["kappa"])),
            theta_deg=float(rng.uniform(*coarse_bounds["theta_deg"])),
            phi=float(rng.uniform(*coarse_bounds["phi"])),
        )
        if cand["explained_fraction"] > best["explained_fraction"]:
            best = cand

    local_scales = [
        (0.10, 0.05, 8.0, 0.12),
        (0.04, 0.02, 3.0, 0.05),
        (0.015, 0.008, 1.0, 0.02),
        (0.006, 0.003, 0.4, 0.008),
    ]
    for delta_s, kappa_s, theta_s, phi_s in local_scales:
        for _ in range(max(64, trials // 4)):
            cand = evaluate_params(
                y,
                delta=max(0.001, best["delta"] + float(rng.normal(0.0, delta_s))),
                kappa=max(0.0005, best["kappa"] + float(rng.normal(0.0, kappa_s))),
                theta_deg=float(np.clip(best["theta_deg"] + rng.normal(0.0, theta_s), 60.0, 220.0)),
                phi=max(1.01, best["phi"] + float(rng.normal(0.0, phi_s))),
            )
            if cand["explained_fraction"] > best["explained_fraction"]:
                best = cand

    best["hint_values"] = {
        "delta_hint": delta0,
        "kappa_hint": kappa0,
        "theta_hint_deg": theta0,
        "phi_hint": phi0,
    }
    return best


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Minimal Skeleton Hint Fit",
        "",
        "## Domain",
        f"- data_path: `{report['data_path']}`",
        f"- window: `{report['window']}`",
        f"- n_points: `{report['n_points']}`",
        "",
        "## Skeleton",
        "- state_equation: `z_(n+1) = R_theta(z_n^2 + phi^(-(level-1)) * (delta + i*kappa))`",
        "- basis: `bias, z_real, z_imag, z_abs, phase, dphase`",
        "",
        "## Hint Values",
        f"- delta_hint: `{report['hint_values']['delta_hint']}`",
        f"- kappa_hint: `{report['hint_values']['kappa_hint']}`",
        f"- theta_hint_deg: `{report['hint_values']['theta_hint_deg']}`",
        f"- phi_hint: `{report['hint_values']['phi_hint']}`",
        "",
        "## Tuned Parameters",
        f"- delta: `{report['delta']}`",
        f"- kappa: `{report['kappa']}`",
        f"- theta_deg: `{report['theta_deg']}`",
        f"- phi: `{report['phi']}`",
        "",
        "## Fit",
        f"- rmse: `{report['rmse']}`",
        f"- explained_fraction: `{report['explained_fraction']}`",
        "",
        "## Projection Coefficients",
    ]
    for name, value in report["coeffs"].items():
        lines.append(f"- `{name}` = `{value}`")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fit seismology with the minimal skeleton only; repo constants are hints, not locked terms.")
    parser.add_argument("--window", type=int, default=15)
    parser.add_argument("--trials", type=int, default=320)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out-json", default="analysis_results/minimal_skeleton_hint_fit.json")
    parser.add_argument("--out-md", default="analysis_results/minimal_skeleton_hint_fit.md")
    args = parser.parse_args()

    y = moving_average(load_series(), window=args.window)
    best = search(y, trials=args.trials, seed=args.seed)
    report = {
        "data_path": str(SEIS_PATH),
        "window": int(args.window),
        "n_points": int(y.size),
        **best,
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"explained={report['explained_fraction']}")
    print(f"rmse={report['rmse']}")
    print(f"delta={report['delta']}")
    print(f"kappa={report['kappa']}")
    print(f"theta_deg={report['theta_deg']}")
    print(f"phi={report['phi']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
