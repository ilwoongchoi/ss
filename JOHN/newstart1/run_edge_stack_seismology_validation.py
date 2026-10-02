from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from fusion_clean import edge_stack_master_step


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
OUT_JSON = Path("analysis_results/edge_stack_seismology_validation.json")
OUT_MD = Path("analysis_results/edge_stack_seismology_validation.md")


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
        return x.copy()
    kernel = np.ones(window, dtype=float) / float(window)
    return np.convolve(x, kernel, mode="same")


def state_embed(x: np.ndarray) -> np.ndarray:
    ma = moving_average(x, 15)
    d1 = np.gradient(x)
    d2 = np.gradient(d1)
    states = np.column_stack([x, ma, d1, d2]).astype(float)
    norms = np.std(states, axis=0) + 1.0e-12
    return states / norms


def build_feature_matrix(states: np.ndarray) -> tuple[np.ndarray, list[str]]:
    n = states.shape[0]
    rows: list[list[float]] = []
    feature_names: list[str] | None = None
    for i in range(n):
        fill = float(i / max(n - 1, 1))
        minute = int((i % 96) * 15)
        hh = minute // 60
        mm = minute % 60
        clock = f"{hh:02d}:{mm:02d}"
        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock)
        face = step["face_state"] or {}
        split = step["tunnel_transfer_split"]
        edge_terms = step["edge_terms"]
        lensing_norm = float(np.linalg.norm(np.asarray(step["lensing"], dtype=float)))
        plp_norm = float(np.linalg.norm(np.asarray(step["plp"], dtype=float)))
        cancel_norm = float(np.linalg.norm(np.asarray(step["cancel_pair"], dtype=float)))
        bm_bw_norm = float(np.linalg.norm(np.asarray(edge_terms["BM_BW"], dtype=float)))
        bm_sw_norm = float(np.linalg.norm(np.asarray(edge_terms["BM_SW"], dtype=float)))
        bm_sm_norm = float(np.linalg.norm(np.asarray(edge_terms["BM_SM"], dtype=float)))
        sm_bw_norm = float(np.linalg.norm(np.asarray(edge_terms["SM_BW"], dtype=float)))
        bw_sw_norm = float(np.linalg.norm(np.asarray(edge_terms["BW_SW"], dtype=float)))
        sm_sw_norm = float(np.linalg.norm(np.asarray(edge_terms["SM_SW"], dtype=float)))

        # Process-level lensing-unveil approximations:
        # expose raw bridge magnitudes and lensing-corrected BM/BW-BM/SM channels separately.
        bm_bw_unveiled = bm_bw_norm - float(split["lensing_delta"])
        bm_sm_unveiled = bm_sm_norm + float(split["bm_sm_effective"])
        bm_sw_unveiled = bm_sw_norm - float(split["stimulated_delta"])

        row = [
            1.0,  # bias
            float(step["gate"]),
            float(step["slotting"]),
            float(step["forward_phase"]),
            float(step["reverse_phase"]),
            float(step["net_phase"]),
            float(step["cancellation"]),
            float(face.get("is_tunnel", 0.0)),
            float(face.get("window_position", 0.0)),
            float(face.get("female_container_activity", 0.0)),
            float(face.get("male_capture_activity", 1.0)),
            float(split["transfer_efficiency"]),
            float(split["bm_sm_effective"]),
            float(split["bw_bw_container_reserve"]),
            float(split["lensing_share"]),
            float(split["stimulated_share"]),
            float(split["lensing_delta"]),
            float(split["stimulated_delta"]),
            float(split["transfer_total"]),
            float(split["closure_target"]),
            float(split["static_efficiency"]),
            lensing_norm,
            plp_norm,
            cancel_norm,
            bm_bw_norm,
            bm_sw_norm,
            bm_sm_norm,
            sm_bw_norm,
            bw_sw_norm,
            sm_sw_norm,
            bm_bw_unveiled,
            bm_sw_unveiled,
            bm_sm_unveiled,
            *np.asarray(step["mandelbrot_core"], dtype=float).tolist(),
            *np.asarray(step["edge_total"], dtype=float).tolist(),
            *np.asarray(step["interaction_total"], dtype=float).tolist(),
            *np.asarray(step["cancel_pair"], dtype=float).tolist(),
            *np.asarray(step["bw_bw_void"], dtype=float).tolist(),
            *np.asarray(step["patch_total"], dtype=float).tolist(),
            *np.asarray(step["particle_9_13_total"], dtype=float).tolist(),
            float(step["quark_9"]),
            float(step["gluon_10"]),
            float(step["muon_11"]),
            float(step["tau_12"]),
            float(step["higgs_13"]),
            *np.asarray(step["gated_branch"], dtype=float).tolist(),
        ]
        if feature_names is None:
            feature_names = [
                "bias",
                "gate",
                "slotting",
                "forward_phase",
                "reverse_phase",
                "net_phase",
                "cancellation",
                "is_tunnel",
                "window_position",
                "female_container_activity",
                "male_capture_activity",
                "transfer_efficiency",
                "bm_sm_effective",
                "bw_bw_container_reserve",
                "lensing_share",
                "stimulated_share",
                "lensing_delta",
                "stimulated_delta",
                "transfer_total",
                "closure_target",
                "static_efficiency",
                "lensing_norm",
                "plp_norm",
                "cancel_norm",
                "bm_bw_norm",
                "bm_sw_norm",
                "bm_sm_norm",
                "sm_bw_norm",
                "bw_sw_norm",
                "sm_sw_norm",
                "bm_bw_unveiled",
                "bm_sw_unveiled",
                "bm_sm_unveiled",
                "mandelbrot_core_0",
                "mandelbrot_core_1",
                "mandelbrot_core_2",
                "mandelbrot_core_3",
                "edge_total_0",
                "edge_total_1",
                "edge_total_2",
                "edge_total_3",
                "interaction_total_0",
                "interaction_total_1",
                "interaction_total_2",
                "interaction_total_3",
                "cancel_pair_0",
                "cancel_pair_1",
                "cancel_pair_2",
                "cancel_pair_3",
                "bw_bw_void_0",
                "bw_bw_void_1",
                "bw_bw_void_2",
                "bw_bw_void_3",
                "patch_total_0",
                "patch_total_1",
                "patch_total_2",
                "patch_total_3",
                "particle_9_13_total_0",
                "particle_9_13_total_1",
                "particle_9_13_total_2",
                "particle_9_13_total_3",
                "quark_9",
                "gluon_10",
                "muon_11",
                "tau_12",
                "higgs_13",
                "gated_branch_0",
                "gated_branch_1",
                "gated_branch_2",
                "gated_branch_3",
            ]
        rows.append(row)
    return np.asarray(rows, dtype=float), (feature_names or [])


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1.0e-12:
        return 0.0
    err = y - y_hat
    return float(1.0 - (np.mean(err * err) / var))


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    y = load_series()
    states = state_embed(y)
    X_full, feature_names = build_feature_matrix(states[:-1])
    y_next = y[1:]

    split = int(0.7 * y_next.size)
    X_train = X_full[:split]
    X_test = X_full[split:]
    y_train = y_next[:split]
    y_test = y_next[split:]

    coeffs, *_ = np.linalg.lstsq(X_train, y_train, rcond=None)
    y_hat_train = X_train @ coeffs
    y_hat_test = X_test @ coeffs

    baseline_X_full = np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]])
    baseline_train = baseline_X_full[:split]
    baseline_test = baseline_X_full[split:]
    baseline_coeffs, *_ = np.linalg.lstsq(baseline_train, y_train, rcond=None)
    baseline_hat_train = baseline_train @ baseline_coeffs
    baseline_hat_test = baseline_test @ baseline_coeffs

    report = {
        "domain": "seismology_daily_k_eff",
        "data_path": str(SEIS_PATH),
        "n_points": int(y_next.size),
        "split_index": int(split),
        "feature_count": int(X_full.shape[1]),
        "baseline_feature_count": int(baseline_X_full.shape[1]),
        "train_explained_fraction_edge_stack": explained_fraction(y_train, y_hat_train),
        "test_explained_fraction_edge_stack": explained_fraction(y_test, y_hat_test),
        "train_explained_fraction_state_only": explained_fraction(y_train, baseline_hat_train),
        "test_explained_fraction_state_only": explained_fraction(y_test, baseline_hat_test),
        "train_rmse_edge_stack": float(np.sqrt(np.mean((y_train - y_hat_train) ** 2))),
        "test_rmse_edge_stack": float(np.sqrt(np.mean((y_test - y_hat_test) ** 2))),
        "train_rmse_state_only": float(np.sqrt(np.mean((y_train - baseline_hat_train) ** 2))),
        "test_rmse_state_only": float(np.sqrt(np.mean((y_test - baseline_hat_test) ** 2))),
        "feature_names": feature_names,
        "coefficients": {k: float(v) for k, v in zip(feature_names, coeffs)},
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Edge Stack Seismology Validation",
        "",
        f"- data_path: `{report['data_path']}`",
        f"- n_points: `{report['n_points']}`",
        f"- split_index: `{report['split_index']}`",
        f"- feature_count: `{report['feature_count']}`",
        f"- train_explained_fraction_edge_stack: `{report['train_explained_fraction_edge_stack']}`",
        f"- test_explained_fraction_edge_stack: `{report['test_explained_fraction_edge_stack']}`",
        f"- train_explained_fraction_state_only: `{report['train_explained_fraction_state_only']}`",
        f"- test_explained_fraction_state_only: `{report['test_explained_fraction_state_only']}`",
        f"- train_rmse_edge_stack: `{report['train_rmse_edge_stack']}`",
        f"- test_rmse_edge_stack: `{report['test_rmse_edge_stack']}`",
        f"- train_rmse_state_only: `{report['train_rmse_state_only']}`",
        f"- test_rmse_state_only: `{report['test_rmse_state_only']}`",
        "",
        "## Selected Coefficients",
        f"- gate: `{report['coefficients'].get('gate')}`",
        f"- slotting: `{report['coefficients'].get('slotting')}`",
        f"- lensing_delta: `{report['coefficients'].get('lensing_delta')}`",
        f"- stimulated_delta: `{report['coefficients'].get('stimulated_delta')}`",
        f"- bm_bw_unveiled: `{report['coefficients'].get('bm_bw_unveiled')}`",
        f"- bm_sm_unveiled: `{report['coefficients'].get('bm_sm_unveiled')}`",
        f"- bm_sw_unveiled: `{report['coefficients'].get('bm_sw_unveiled')}`",
        f"- quark_9: `{report['coefficients'].get('quark_9')}`",
        f"- gluon_10: `{report['coefficients'].get('gluon_10')}`",
        f"- muon_11: `{report['coefficients'].get('muon_11')}`",
        f"- tau_12: `{report['coefficients'].get('tau_12')}`",
        f"- higgs_13: `{report['coefficients'].get('higgs_13')}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"edge_stack_test_explained={report['test_explained_fraction_edge_stack']}")
    print(f"state_only_test_explained={report['test_explained_fraction_state_only']}")
    print(f"json={OUT_JSON}")
    print(f"md={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
