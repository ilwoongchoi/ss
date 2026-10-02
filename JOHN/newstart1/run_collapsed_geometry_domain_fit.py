from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from geometry_package import absolute_constants as ac
from geometry_package.interaction_64 import edge_strengths_6


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


def normalized(arr: np.ndarray) -> np.ndarray:
    scale = float(np.max(np.abs(arr)))
    if scale <= 1.0e-12:
        return np.zeros_like(arr)
    return arr / scale


def simulate_collapsed_state(n: int) -> dict[str, np.ndarray]:
    idx = np.arange(n, dtype=float)
    t_norm = idx / max(n - 1, 1)
    t_hours = 24.0 * t_norm

    edge_map = edge_strengths_6()
    edge_values = np.asarray(
        [
            edge_map["BM_BW"],
            edge_map["BM_SW"],
            edge_map["BW_SW"],
            edge_map["SM_SW"],
            edge_map["SM_BW"],
            edge_map["BM_SM"],
        ],
        dtype=float,
    )
    scale_values = np.asarray(
        [
            ac.S_ELECTRON,
            ac.S_PHOTON,
            ac.S_PROTON,
            ac.S_SENTINEL,
            ac.S_NEUTRINO,
            ac.S_GRAVITON,
        ],
        dtype=float,
    )

    z = 0.0 + 0.0j
    z_hist = np.zeros(n, dtype=np.complex128)
    omega_hist = np.zeros(n, dtype=float)
    engine_hist = np.zeros(n, dtype=float)
    reservoir_hist = np.zeros(n, dtype=float)
    schedule_hist = np.zeros(n, dtype=float)
    comag_hist = np.zeros(n, dtype=float)
    edge_hist = np.zeros(n, dtype=float)
    scale_hist = np.zeros(n, dtype=float)
    level_hist = np.zeros(n, dtype=float)

    for i, t in enumerate(t_hours):
        level = (i % 10) + 1
        if level == 1:
            z = 0.0 + 0.0j

        omega_terms = ac.OMEGA_TERMS(float(t))
        omega = float(omega_terms["omega_natural"])
        engine = float(omega_terms["engine"])
        reservoir = float(omega_terms["reservoir"])
        schedule = float(omega_terms["schedule"])
        comag = float(omega_terms["comag"])

        edge = float(edge_values[(level - 1) % edge_values.size])
        scale = float(scale_values[(level - 1) % scale_values.size])
        phi_scale = float(ac.PHI ** (-(level - 1)))
        omega_bound = omega / (1.0 + abs(omega))
        phase = float(ac.SPARK_ANGLE_RAD + (ac.TORSION_4D * omega_bound))

        seed = complex(ac.DELTA_T_OBS_DERIVED, ac.OMEGA_KAPPA)
        edge_force = complex(edge * math.cos(phase), edge * math.sin(phase))
        raw = (ac.METRIC_4D * z * z) + (phi_scale * seed) + (scale * edge_force)
        z = rotate_complex(raw, phase)

        z_hist[i] = z
        omega_hist[i] = omega
        engine_hist[i] = engine
        reservoir_hist[i] = reservoir
        schedule_hist[i] = schedule
        comag_hist[i] = comag
        edge_hist[i] = edge
        scale_hist[i] = scale
        level_hist[i] = float(level)

    abs_hist = np.abs(z_hist)
    phase_hist = np.unwrap(np.angle(z_hist + 1.0e-12))
    dphase_hist = np.gradient(phase_hist)

    return {
        "t_norm": t_norm,
        "z_real": z_hist.real,
        "z_imag": z_hist.imag,
        "z_abs": abs_hist,
        "phase": phase_hist,
        "dphase": dphase_hist,
        "omega": normalized(omega_hist),
        "engine": normalized(engine_hist),
        "reservoir": normalized(reservoir_hist),
        "schedule": normalized(schedule_hist),
        "comag": normalized(comag_hist),
        "edge": normalized(edge_hist),
        "scale": normalized(scale_hist),
        "level": level_hist / 10.0,
    }


def build_projection_basis(state: dict[str, np.ndarray]) -> tuple[np.ndarray, list[str]]:
    zr = normalized(state["z_real"])
    zi = normalized(state["z_imag"])
    za = normalized(state["z_abs"])
    phase = normalized(state["phase"])
    dphase = normalized(state["dphase"])
    omega = state["omega"]
    engine = state["engine"]
    reservoir = state["reservoir"]
    schedule = state["schedule"]
    comag = state["comag"]
    edge = state["edge"]
    scale = state["scale"]
    level = state["level"]
    t = state["t_norm"]

    features = [
        np.ones_like(t),
        zr,
        zi,
        za,
        phase,
        dphase,
        omega,
        engine,
        reservoir,
        schedule,
        comag,
        edge,
        scale,
        level,
        za * omega,
        za * edge,
        zr * scale,
        zi * omega,
        dphase * scale,
        schedule * edge,
        comag * za,
        t,
        t * t,
    ]
    names = [
        "bias",
        "z_real",
        "z_imag",
        "z_abs",
        "phase",
        "dphase",
        "omega",
        "engine",
        "reservoir",
        "schedule",
        "comag",
        "edge",
        "scale",
        "level",
        "z_abs_x_omega",
        "z_abs_x_edge",
        "z_real_x_scale",
        "z_imag_x_omega",
        "dphase_x_scale",
        "schedule_x_edge",
        "comag_x_z_abs",
        "t",
        "t2",
    ]
    return np.column_stack(features), names


def fit_projection(y: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ coeffs
    resid = y - fit
    rmse = float(np.sqrt(np.mean(resid * resid)))
    explained = 1.0 - float(np.var(resid) / max(np.var(y), 1.0e-12))
    return coeffs, fit, resid, rmse, explained


def top_coefficients(coeffs: np.ndarray, names: list[str], k: int = 12) -> list[dict[str, float | str]]:
    order = np.argsort(np.abs(coeffs))[::-1][:k]
    return [{"name": names[int(i)], "coef": float(coeffs[int(i)])} for i in order]


def build_report(window: int) -> dict[str, object]:
    y_raw = load_series()
    y = moving_average(y_raw, window=window)
    state = simulate_collapsed_state(len(y))
    X, names = build_projection_basis(state)
    coeffs, fit, resid, rmse, explained = fit_projection(y, X)

    return {
        "domain": "seismology_daily_k_eff",
        "data_path": str(SEIS_PATH),
        "locked_primitives": {
            "delta_phase": float(ac.DELTA_T_OBS_DERIVED),
            "spark_angle_deg": float(ac.SPARK_ANGLE_DEG),
            "kappa": float(ac.OMEGA_KAPPA),
            "phi": float(ac.PHI),
            "metric_4d": float(ac.METRIC_4D),
            "torsion_4d": float(ac.TORSION_4D),
            "window": int(window),
            "n_points": int(len(y)),
        },
        "skeleton": {
            "state_equation": (
                "z_(n+1,d)=Projection_d(R_(theta+torsion_4d*Omega(t_n))"
                "[metric_4d*z_n^2 + phi^(-(n-1))*(delta_phase+i*kappa) + Edge(s_n)])"
            ),
            "projection_basis": names,
        },
        "fit": {
            "rmse": rmse,
            "explained_fraction": float(explained),
            "residual_std": float(np.std(resid)),
            "residual_mean": float(np.mean(resid)),
            "top_coefficients": top_coefficients(coeffs, names),
        },
        "state_summary": {
            "z_abs_max": float(np.max(np.abs(state["z_abs"]))),
            "z_abs_mean": float(np.mean(np.abs(state["z_abs"]))),
            "dphase_mean": float(np.mean(state["dphase"])),
            "omega_mean": float(np.mean(state["omega"])),
        },
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Collapsed Geometry Domain Fit",
        "",
        "## Locked Primitives",
        f"- delta_phase: `{report['locked_primitives']['delta_phase']}`",
        f"- spark_angle_deg: `{report['locked_primitives']['spark_angle_deg']}`",
        f"- kappa: `{report['locked_primitives']['kappa']}`",
        f"- phi: `{report['locked_primitives']['phi']}`",
        f"- metric_4d: `{report['locked_primitives']['metric_4d']}`",
        f"- torsion_4d: `{report['locked_primitives']['torsion_4d']}`",
        f"- window: `{report['locked_primitives']['window']}`",
        f"- n_points: `{report['locked_primitives']['n_points']}`",
        "",
        "## Skeleton",
        f"- state_equation: `{report['skeleton']['state_equation']}`",
        "",
        "## Fit",
        f"- rmse: `{report['fit']['rmse']}`",
        f"- explained_fraction: `{report['fit']['explained_fraction']}`",
        f"- residual_std: `{report['fit']['residual_std']}`",
        f"- residual_mean: `{report['fit']['residual_mean']}`",
        "",
        "## Top Coefficients",
    ]
    for row in report["fit"]["top_coefficients"]:
        lines.append(f"- `{row['name']}` = `{row['coef']}`")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fit one domain with the concept-collapsed geometry skeleton.")
    parser.add_argument("--window", type=int, default=15)
    parser.add_argument("--out-json", default="analysis_results/collapsed_geometry_domain_fit.json")
    parser.add_argument("--out-md", default="analysis_results/collapsed_geometry_domain_fit.md")
    args = parser.parse_args()

    report = build_report(window=args.window)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"rmse={report['fit']['rmse']}")
    print(f"explained={report['fit']['explained_fraction']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
