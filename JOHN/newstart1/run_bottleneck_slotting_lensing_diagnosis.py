from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\bottleneck_slotting_lensing_diagnosis.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\bottleneck_slotting_lensing_diagnosis.md")


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1.0e-12:
        return 0.0
    err = y - y_hat
    return float(1.0 - (np.mean(err * err) / var))


def fit_ridge_cv_with_preds(X: np.ndarray, y: np.ndarray, split: int) -> dict[str, np.ndarray | float | int]:
    return v.fit_ridge_cv_with_preds(X, y, split)


def binned_abs_residual(x: np.ndarray, abs_res: np.ndarray, n_bins: int = 10) -> dict[str, object]:
    q = np.quantile(x, np.linspace(0.0, 1.0, n_bins + 1))
    rows = []
    for i in range(n_bins):
        lo = float(q[i])
        hi = float(q[i + 1])
        if i < n_bins - 1:
            m = (x >= lo) & (x < hi)
        else:
            m = (x >= lo) & (x <= hi)
        if not np.any(m):
            rows.append({"bin": i, "lo": lo, "hi": hi, "count": 0, "mean_abs_residual": None})
            continue
        rows.append(
            {
                "bin": i,
                "lo": lo,
                "hi": hi,
                "count": int(np.sum(m)),
                "mean_abs_residual": float(np.mean(abs_res[m])),
            }
        )
    return {"bins": rows}


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    y_raw = v.load_seis_series()
    split = int(0.7 * (y_raw.size - 1))
    y_mu = float(np.mean(y_raw[: split + 1]))
    y_sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - y_mu) / y_sd
    states = v.causal_state_embed(y)
    y_next = y[1:]

    X_state = np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]])
    X_edge = v.build_edge_features(states[:-1])
    macro = v.load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
    X_l0 = v.build_layer0_features(states[:-1], macro)
    X_edge15 = v.build_edge15_features(states[:-1])
    X_edge_l0 = np.column_stack([X_edge, X_l0])
    X_edge15_l0 = np.column_stack([X_edge15, X_l0])
    X_edge_l0_pruned = v._build_physics_pruned2_edge_l0(X_edge_l0)

    # Auto-select blend weights on validation for current best candidate:
    # edge_pruned + edge15_plus_econ_layer0.
    e = fit_ridge_cv_with_preds(X_edge_l0_pruned, y_next, split)
    q = fit_ridge_cv_with_preds(X_edge15_l0, y_next, split)
    yv = np.asarray(e["y_val"], dtype=float)
    yve = np.asarray(e["yhat_val"], dtype=float)
    yvq = np.asarray(q["yhat_val"], dtype=float)
    best = (-1.0e18, 0.5)
    for w in np.linspace(0.0, 1.0, 41):
        yhat = w * yve + (1.0 - w) * yvq
        score = explained_fraction(yv, yhat)
        if score > best[0]:
            best = (float(score), float(w))
    w_edge = best[1]
    w_edge15 = 1.0 - w_edge
    yhat_test = w_edge * np.asarray(e["yhat_test"], dtype=float) + w_edge15 * np.asarray(q["yhat_test"], dtype=float)
    y_test = np.asarray(e["y_test"], dtype=float)
    res = y_test - yhat_test
    abs_res = np.abs(res)

    # Test-slice features from X_edge_l0 prefix (= X_edge columns).
    X_edge_test = X_edge_l0[split:, : X_edge.shape[1]]
    slotting = X_edge_test[:, 2]
    lensing_delta = X_edge_test[:, 16]
    lensing_norm = X_edge_test[:, 21]
    bm_sm_effective = X_edge_test[:, 12]
    bw_bw_container_reserve = X_edge_test[:, 13]
    quark_9 = X_edge_test[:, 61]
    gluon_10 = X_edge_test[:, 62]
    is_tunnel = X_edge_test[:, 7]

    # Correlations with signed/absolute residual.
    def corr(a: np.ndarray, b: np.ndarray) -> float:
        if float(np.std(a)) < 1.0e-12 or float(np.std(b)) < 1.0e-12:
            return 0.0
        return float(np.corrcoef(a, b)[0, 1])

    corrs = {
        "slotting_vs_abs_residual": corr(slotting, abs_res),
        "lensing_delta_vs_abs_residual": corr(lensing_delta, abs_res),
        "lensing_norm_vs_abs_residual": corr(lensing_norm, abs_res),
        "bm_sm_effective_vs_abs_residual": corr(bm_sm_effective, abs_res),
        "bw_bw_container_reserve_vs_abs_residual": corr(bw_bw_container_reserve, abs_res),
        "quark_9_vs_abs_residual": corr(quark_9, abs_res),
        "gluon_10_vs_abs_residual": corr(gluon_10, abs_res),
        "slotting_vs_signed_residual": corr(slotting, res),
        "lensing_delta_vs_signed_residual": corr(lensing_delta, res),
    }

    tunnel_mask = is_tunnel >= 0.5
    day_mask = ~tunnel_mask
    tunnel_mae = float(np.mean(abs_res[tunnel_mask])) if np.any(tunnel_mask) else None
    day_mae = float(np.mean(abs_res[day_mask])) if np.any(day_mask) else None

    report = {
        "split_index": int(split),
        "n_test": int(y_test.size),
        "blend_weights": {"edge": w_edge, "edge15": w_edge15},
        "test_explained_blend": float(explained_fraction(y_test, yhat_test)),
        "test_rmse_blend": float(np.sqrt(np.mean((res) ** 2))),
        "test_mae_blend": float(np.mean(abs_res)),
        "corrs": corrs,
        "regime_mae": {
            "tunnel": tunnel_mae,
            "day": day_mae,
            "delta_tunnel_minus_day": (None if tunnel_mae is None or day_mae is None else float(tunnel_mae - day_mae)),
        },
        "bins": {
            "slotting": binned_abs_residual(slotting, abs_res, n_bins=10),
            "lensing_delta": binned_abs_residual(lensing_delta, abs_res, n_bins=10),
            "lensing_norm": binned_abs_residual(lensing_norm, abs_res, n_bins=10),
            "gluon_10": binned_abs_residual(gluon_10, abs_res, n_bins=10),
            "bw_bw_container_reserve": binned_abs_residual(bw_bw_container_reserve, abs_res, n_bins=10),
        },
    }

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Bottleneck Diagnosis (Slotting/Lensing)",
        "",
        f"- n_test: `{report['n_test']}`",
        f"- test_explained_blend: `{report['test_explained_blend']}`",
        f"- test_rmse_blend: `{report['test_rmse_blend']}`",
        f"- test_mae_blend: `{report['test_mae_blend']}`",
        "",
        "## Correlation With |Residual|",
        f"- slotting: `{corrs['slotting_vs_abs_residual']}`",
        f"- lensing_delta: `{corrs['lensing_delta_vs_abs_residual']}`",
        f"- lensing_norm: `{corrs['lensing_norm_vs_abs_residual']}`",
        f"- bm_sm_effective: `{corrs['bm_sm_effective_vs_abs_residual']}`",
        f"- bw_bw_container_reserve: `{corrs['bw_bw_container_reserve_vs_abs_residual']}`",
        f"- quark_9: `{corrs['quark_9_vs_abs_residual']}`",
        f"- gluon_10: `{corrs['gluon_10_vs_abs_residual']}`",
        "",
        "## Regime MAE",
        f"- tunnel_mae: `{report['regime_mae']['tunnel']}`",
        f"- day_mae: `{report['regime_mae']['day']}`",
        f"- delta_tunnel_minus_day: `{report['regime_mae']['delta_tunnel_minus_day']}`",
        "",
        "Detailed decile tables are in JSON.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
