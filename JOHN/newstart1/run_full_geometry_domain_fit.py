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


def build_feature_matrix(n: int) -> tuple[np.ndarray, list[str]]:
    idx = np.arange(n, dtype=float)
    t_norm = idx / max(n - 1, 1)
    t_hours = 24.0 * t_norm

    theta = ac.SPARK_ANGLE_RAD * idx
    half_theta = math.radians(ac.HALF_SPARK_ANGLE) * idx
    d3_theta = math.radians(ac.D3_DELTA_THETA_CW) * idx
    phi_decay = np.power(ac.PHI, -t_norm * 10.0)
    phi_decay2 = phi_decay * phi_decay
    phi_decay3 = phi_decay2 * phi_decay

    omega_terms = [ac.OMEGA_TERMS(float(t)) for t in t_hours]
    omega = np.asarray([row["omega_natural"] for row in omega_terms], dtype=float)
    engine = np.asarray([row["engine"] for row in omega_terms], dtype=float)
    reservoir = np.asarray([row["reservoir"] for row in omega_terms], dtype=float)
    schedule = np.asarray([row["schedule"] for row in omega_terms], dtype=float)
    comag = np.asarray([row["comag"] for row in omega_terms], dtype=float)

    omega_n = omega / (np.max(np.abs(omega)) + 1.0e-12)
    engine_n = engine / (np.max(np.abs(engine)) + 1.0e-12)
    reservoir_n = reservoir / (np.max(np.abs(reservoir)) + 1.0e-12)
    schedule_n = schedule / (np.max(np.abs(schedule)) + 1.0e-12)
    comag_n = comag / (np.max(np.abs(comag)) + 1.0e-12)

    edges = edge_strengths_6()
    edge_vec = np.asarray(
        [
            edges["BM_BW"],
            edges["BM_SW"],
            edges["BW_SW"],
            edges["SM_SW"],
            edges["SM_BW"],
            edges["BM_SM"],
        ],
        dtype=float,
    )
    edge_vec = edge_vec / (np.max(np.abs(edge_vec)) + 1.0e-12)

    particle_scales = np.asarray(
        [ac.S_ELECTRON, ac.S_PHOTON, ac.S_PROTON, ac.S_SENTINEL, ac.S_NEUTRINO, ac.S_GRAVITON],
        dtype=float,
    )
    particle_scales = particle_scales / np.max(np.abs(particle_scales))

    features: list[np.ndarray] = []
    names: list[str] = []

    def add(name: str, arr: np.ndarray) -> None:
        features.append(np.asarray(arr, dtype=float))
        names.append(name)

    add("bias", np.ones(n))
    add("t", t_norm)
    add("t2", t_norm * t_norm)
    add("t3", t_norm * t_norm * t_norm)

    add("phi_decay", phi_decay)
    add("phi_decay2", phi_decay2)
    add("phi_decay3", phi_decay3)

    add("cos_theta", np.cos(theta))
    add("sin_theta", np.sin(theta))
    add("cos_half_theta", np.cos(half_theta))
    add("sin_half_theta", np.sin(half_theta))
    add("cos_d3_theta", np.cos(d3_theta))
    add("sin_d3_theta", np.sin(d3_theta))

    add("omega", omega_n)
    add("engine", engine_n)
    add("reservoir", reservoir_n)
    add("schedule", schedule_n)
    add("comag", comag_n)

    add("torsion_omega", ac.TORSION_4D * omega_n)
    add("metric_phi", ac.METRIC_4D * phi_decay)
    add("kappa_phi", ac.OMEGA_KAPPA * phi_decay)
    add("gate_phi", ac.GATE_5_32 * phi_decay)
    add("lattice_phi", ac.LATTICE_3_32 * phi_decay)
    add("chirality_phi", ac.CHIRALITY_CONSTANT * phi_decay)
    add("drift_t", ac.OMEGA_SLOTTING_DELTA * t_norm)
    add("night_cycle", ac.LUNAR_CYCLE * np.sin(2.0 * np.pi * 28.0 * t_norm))
    add("alpha_bridge", ac.ALPHA_KAPPA_BRIDGE * phi_decay2)
    add("renorm_bridge", ac.RENORMALIZATION_BRIDGE * phi_decay3)
    add("event_horizon", ac.EVENT_HORIZON_RADIUS_RS * phi_decay)
    add("maxwell_major", ac.MAXWELL_R_MAJOR * phi_decay)
    add("maxwell_minor", ac.MAXWELL_R_MINOR * phi_decay)
    add("maxwell_q", ac.MAXWELL_Q_FACTOR * phi_decay2)

    for i, value in enumerate(edge_vec):
        add(f"edge_{i}_cos", value * np.cos(theta))
        add(f"edge_{i}_sin", value * np.sin(theta))

    for i, scale in enumerate(particle_scales):
        add(f"scale_{i}_cos", scale * np.cos(theta))
        add(f"scale_{i}_sin", scale * np.sin(theta))

    X = np.column_stack(features)
    return X, names


def prune_overlap_features(X: np.ndarray, names: list[str], corr_threshold: float = 0.995, residual_threshold: float = 1.0e-3) -> tuple[np.ndarray, list[str], list[dict[str, object]]]:
    X = np.asarray(X, dtype=float)
    keep_cols: list[np.ndarray] = []
    keep_names: list[str] = []
    dropped: list[dict[str, object]] = []

    for j, name in enumerate(names):
        col = X[:, j]
        norm = float(np.linalg.norm(col))
        if norm < 1.0e-10:
            dropped.append({"name": name, "reason": "zero_norm"})
            continue

        if not keep_cols:
            keep_cols.append(col)
            keep_names.append(name)
            continue

        # 1) Pairwise overlap gate.
        overlapped = False
        for k, prev in enumerate(keep_cols):
            prev_norm = float(np.linalg.norm(prev))
            corr = float(abs(np.dot(col, prev)) / max(norm * prev_norm, 1.0e-12))
            if corr >= corr_threshold:
                dropped.append({"name": name, "reason": "pairwise_overlap", "with": keep_names[k], "corr": corr})
                overlapped = True
                break
        if overlapped:
            continue

        # 2) Residual margin gate against the full kept span.
        K = np.column_stack(keep_cols)
        coeffs, *_ = np.linalg.lstsq(K, col, rcond=None)
        resid = col - (K @ coeffs)
        resid_norm = float(np.linalg.norm(resid))
        resid_ratio = resid_norm / max(norm, 1.0e-12)
        if resid_ratio <= residual_threshold:
            dropped.append({"name": name, "reason": "span_overlap", "residual_ratio": resid_ratio})
            continue

        keep_cols.append(resid)
        keep_names.append(name)

    return np.column_stack(keep_cols), keep_names, dropped


def fit_domain(y: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, float]:
    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ coeffs
    resid = y - fit
    rmse = float(np.sqrt(np.mean(resid * resid)))
    explained = 1.0 - float(np.var(resid) / max(np.var(y), 1.0e-12))
    return coeffs, fit, rmse, explained


def top_coefficients(coeffs: np.ndarray, names: list[str], k: int = 20) -> list[dict[str, float | str]]:
    order = np.argsort(np.abs(coeffs))[::-1][:k]
    rows = []
    for idx in order:
        rows.append({"name": names[int(idx)], "coef": float(coeffs[int(idx)])})
    return rows


def build_report(window: int) -> dict[str, object]:
    y_raw = load_series()
    y = moving_average(y_raw, window=window)
    X, names = build_feature_matrix(len(y))
    X_pruned, names_pruned, dropped = prune_overlap_features(X, names)
    coeffs, fit, rmse, explained = fit_domain(y, X_pruned)
    resid = y - fit

    return {
        "domain": "seismology_daily_k_eff",
        "data_path": str(SEIS_PATH),
        "locked_seed": {
            "delta": float(ac.DELTA_T_OBS_DERIVED),
            "spark_angle_deg": float(ac.SPARK_ANGLE_DEG),
            "window": int(window),
            "n_points": int(len(y)),
        },
        "inventory": {
            "n_features": int(X.shape[1]),
            "n_features_after_prune": int(X_pruned.shape[1]),
            "feature_names": names,
            "feature_names_after_prune": names_pruned,
            "dropped_overlap_features": dropped,
        },
        "fit": {
            "rmse": rmse,
            "explained_fraction": float(explained),
            "residual_std": float(np.std(resid)),
            "residual_mean": float(np.mean(resid)),
            "top_coefficients": top_coefficients(coeffs, names_pruned, k=24),
        },
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Full Geometry Domain Fit",
        "",
        "## Locked Seed",
        f"- delta: `{report['locked_seed']['delta']}`",
        f"- spark_angle_deg: `{report['locked_seed']['spark_angle_deg']}`",
        f"- window: `{report['locked_seed']['window']}`",
        f"- n_points: `{report['locked_seed']['n_points']}`",
        "",
        "## Inventory",
        f"- n_features: `{report['inventory']['n_features']}`",
        f"- n_features_after_prune: `{report['inventory']['n_features_after_prune']}`",
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
    parser = argparse.ArgumentParser(description="Fit one real domain using the broader geometry_package constant/operator inventory.")
    parser.add_argument("--window", type=int, default=15)
    parser.add_argument("--out-json", default="analysis_results/full_geometry_domain_fit.json")
    parser.add_argument("--out-md", default="analysis_results/full_geometry_domain_fit.md")
    args = parser.parse_args()

    report = build_report(window=args.window)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"n_features={report['inventory']['n_features']}")
    print(f"rmse={report['fit']['rmse']}")
    print(f"explained={report['fit']['explained_fraction']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
