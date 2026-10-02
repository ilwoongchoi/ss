from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from fusion_clean import edge_stack_master_step
from geometry_package.layer_extension_equation import run_layered_step
from geometry_package.six_particle_15_edge_geometry import geometry_step_15


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
ECON_PATH = Path(r"d:\Users\user\Documents\newstart\data\econ_crypto\econ_crypto_ohlcv_daily_long.csv")
OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\seismology_econ_layer0_strict_validation.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\seismology_econ_layer0_strict_validation.md")
EDGE15_GAIN = float(os.getenv("EDGE15_GAIN", "0.0"))


def load_seis_series() -> np.ndarray:
    values: list[float] = []
    with SEIS_PATH.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                values.append(float(row["k_eff"]))
            except (TypeError, ValueError):
                continue
    return np.asarray(values, dtype=float)


def causal_state_embed(y_norm: np.ndarray) -> np.ndarray:
    n = y_norm.size
    ma = np.zeros(n, dtype=float)
    d1 = np.zeros(n, dtype=float)
    d2 = np.zeros(n, dtype=float)
    csum = 0.0
    window = 15
    for i in range(n):
        csum += y_norm[i]
        if i >= window:
            csum -= y_norm[i - window]
        denom = min(i + 1, window)
        ma[i] = csum / float(denom)
        if i > 0:
            d1[i] = y_norm[i] - y_norm[i - 1]
        if i > 1:
            d2[i] = d1[i] - d1[i - 1]
    return np.column_stack([y_norm, ma, d1, d2]).astype(float)


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1.0e-12:
        return 0.0
    err = y - y_hat
    return float(1.0 - (np.mean(err * err) / var))


def fit_eval(X: np.ndarray, y: np.ndarray, split: int) -> dict[str, float]:
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    coeffs, *_ = np.linalg.lstsq(X_train, y_train, rcond=None)
    yhat_train = X_train @ coeffs
    yhat_test = X_test @ coeffs
    return {
        "feature_count": int(X.shape[1]),
        "train_explained": float(explained_fraction(y_train, yhat_train)),
        "test_explained": float(explained_fraction(y_test, yhat_test)),
        "train_rmse": float(np.sqrt(np.mean((y_train - yhat_train) ** 2))),
        "test_rmse": float(np.sqrt(np.mean((y_test - yhat_test) ** 2))),
    }


def _zscore_from_train(X_train: np.ndarray, X_apply: np.ndarray) -> np.ndarray:
    mu = np.mean(X_train, axis=0)
    sd = np.std(X_train, axis=0) + 1.0e-12
    Xn = (X_apply - mu) / sd
    # Keep intercept columns untouched if present.
    intercept_mask = np.all(np.isclose(X_train, X_train[0:1], atol=1.0e-12), axis=0)
    Xn[:, intercept_mask] = X_apply[:, intercept_mask]
    return Xn


def _ridge_predict(X_train: np.ndarray, y_train: np.ndarray, X_pred: np.ndarray, alpha: float) -> np.ndarray:
    p = X_train.shape[1]
    reg = alpha * np.eye(p, dtype=float)
    # Do not regularize intercept-style constant columns.
    intercept_mask = np.all(np.isclose(X_train, X_train[0:1], atol=1.0e-12), axis=0)
    reg[intercept_mask, intercept_mask] = 0.0
    a_mat = X_train.T @ X_train + reg
    b_vec = X_train.T @ y_train
    beta = np.linalg.pinv(a_mat) @ b_vec
    return X_pred @ beta


def fit_eval_ridge_cv(X: np.ndarray, y: np.ndarray, split: int) -> dict[str, float]:
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    n_train = X_train.shape[0]
    val_start = max(16, int(0.8 * n_train))
    X_fit = X_train[:val_start]
    y_fit = y_train[:val_start]
    X_val = X_train[val_start:]
    y_val = y_train[val_start:]
    alphas = np.logspace(-6, 4, 21)
    best_alpha = float(alphas[0])
    best_val = -1.0e18
    X_fit_n = _zscore_from_train(X_fit, X_fit)
    X_val_n = _zscore_from_train(X_fit, X_val)
    for a in alphas:
        yhat_val = _ridge_predict(X_fit_n, y_fit, X_val_n, float(a))
        score = explained_fraction(y_val, yhat_val)
        if score > best_val:
            best_val = float(score)
            best_alpha = float(a)
    X_train_n = _zscore_from_train(X_train, X_train)
    X_test_n = _zscore_from_train(X_train, X_test)
    yhat_train = _ridge_predict(X_train_n, y_train, X_train_n, best_alpha)
    yhat_test = _ridge_predict(X_train_n, y_train, X_test_n, best_alpha)
    return {
        "feature_count": int(X.shape[1]),
        "alpha": float(best_alpha),
        "val_explained": float(best_val),
        "train_explained": float(explained_fraction(y_train, yhat_train)),
        "test_explained": float(explained_fraction(y_test, yhat_test)),
        "train_rmse": float(np.sqrt(np.mean((y_train - yhat_train) ** 2))),
        "test_rmse": float(np.sqrt(np.mean((y_test - yhat_test) ** 2))),
    }


def fit_ridge_cv_with_preds(X: np.ndarray, y: np.ndarray, split: int) -> dict[str, object]:
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    n_train = X_train.shape[0]
    val_start = max(16, int(0.8 * n_train))
    X_fit = X_train[:val_start]
    y_fit = y_train[:val_start]
    X_val = X_train[val_start:]
    y_val = y_train[val_start:]
    alphas = np.logspace(-6, 4, 21)
    best_alpha = float(alphas[0])
    best_val = -1.0e18
    X_fit_n = _zscore_from_train(X_fit, X_fit)
    X_val_n = _zscore_from_train(X_fit, X_val)
    for a in alphas:
        yhat_val = _ridge_predict(X_fit_n, y_fit, X_val_n, float(a))
        score = explained_fraction(y_val, yhat_val)
        if score > best_val:
            best_val = float(score)
            best_alpha = float(a)
    X_train_n = _zscore_from_train(X_train, X_train)
    X_test_n = _zscore_from_train(X_train, X_test)
    X_val_from_train_n = _zscore_from_train(X_train, X_val)
    yhat_train = _ridge_predict(X_train_n, y_train, X_train_n, best_alpha)
    yhat_test = _ridge_predict(X_train_n, y_train, X_test_n, best_alpha)
    yhat_val = _ridge_predict(X_train_n, y_train, X_val_from_train_n, best_alpha)
    return {
        "alpha": float(best_alpha),
        "val_explained": float(best_val),
        "val_start": int(val_start),
        "yhat_train": yhat_train,
        "yhat_test": yhat_test,
        "yhat_val": yhat_val,
        "y_train": y_train,
        "y_test": y_test,
        "y_val": y_val,
    }


def fit_eval_blend_ridge_cv(
    X_a: np.ndarray,
    X_b: np.ndarray,
    y: np.ndarray,
    split: int,
) -> dict[str, float]:
    a = fit_ridge_cv_with_preds(X_a, y, split)
    b = fit_ridge_cv_with_preds(X_b, y, split)
    y_val = np.asarray(a["y_val"], dtype=float)
    ya_val = np.asarray(a["yhat_val"], dtype=float)
    yb_val = np.asarray(b["yhat_val"], dtype=float)
    best_w = 0.0
    best_val = -1.0e18
    for w in np.linspace(0.0, 1.0, 201):
        yhat = w * ya_val + (1.0 - w) * yb_val
        s = explained_fraction(y_val, yhat)
        if s > best_val:
            best_val = float(s)
            best_w = float(w)
    y_train = np.asarray(a["y_train"], dtype=float)
    y_test = np.asarray(a["y_test"], dtype=float)
    ya_train = np.asarray(a["yhat_train"], dtype=float)
    yb_train = np.asarray(b["yhat_train"], dtype=float)
    ya_test = np.asarray(a["yhat_test"], dtype=float)
    yb_test = np.asarray(b["yhat_test"], dtype=float)
    yhat_train = best_w * ya_train + (1.0 - best_w) * yb_train
    yhat_test = best_w * ya_test + (1.0 - best_w) * yb_test
    return {
        "feature_count": int(X_a.shape[1] + X_b.shape[1]),
        "blend_weight_a": float(best_w),
        "blend_weight_b": float(1.0 - best_w),
        "alpha_a": float(a["alpha"]),
        "alpha_b": float(b["alpha"]),
        "val_explained": float(best_val),
        "train_explained": float(explained_fraction(y_train, yhat_train)),
        "test_explained": float(explained_fraction(y_test, yhat_test)),
        "train_rmse": float(np.sqrt(np.mean((y_train - yhat_train) ** 2))),
        "test_rmse": float(np.sqrt(np.mean((y_test - yhat_test) ** 2))),
    }


def fit_eval_phase_bin_blend_ridge_cv(
    X_a: np.ndarray,
    X_b: np.ndarray,
    y: np.ndarray,
    split: int,
    phase_series: np.ndarray,
    n_bins: int = 8,
) -> dict[str, float]:
    a = fit_ridge_cv_with_preds(X_a, y, split)
    b = fit_ridge_cv_with_preds(X_b, y, split)
    val_start = int(a["val_start"])
    phase = np.asarray(phase_series, dtype=float).reshape(-1)
    phase_train = phase[:split]
    phase_test = phase[split:]
    phase_val = phase_train[val_start:]

    y_val = np.asarray(a["y_val"], dtype=float)
    ya_val = np.asarray(a["yhat_val"], dtype=float)
    yb_val = np.asarray(b["yhat_val"], dtype=float)
    ya_train = np.asarray(a["yhat_train"], dtype=float)
    yb_train = np.asarray(b["yhat_train"], dtype=float)
    ya_test = np.asarray(a["yhat_test"], dtype=float)
    yb_test = np.asarray(b["yhat_test"], dtype=float)
    y_train = np.asarray(a["y_train"], dtype=float)
    y_test = np.asarray(a["y_test"], dtype=float)

    # global fallback weight
    global_w = 0.5
    best_val_global = -1.0e18
    for w in np.linspace(0.0, 1.0, 41):
        yhat = w * ya_val + (1.0 - w) * yb_val
        s = explained_fraction(y_val, yhat)
        if s > best_val_global:
            best_val_global = float(s)
            global_w = float(w)

    edges = np.linspace(float(np.min(phase_val)), float(np.max(phase_val)) + 1.0e-12, n_bins + 1)
    weights = np.full(n_bins, global_w, dtype=float)
    for bi in range(n_bins):
        lo = edges[bi]
        hi = edges[bi + 1]
        if bi < n_bins - 1:
            mask = (phase_val >= lo) & (phase_val < hi)
        else:
            mask = (phase_val >= lo) & (phase_val <= hi)
        idx = np.where(mask)[0]
        if idx.size < 32:
            continue
        yv = y_val[idx]
        yva = ya_val[idx]
        yvb = yb_val[idx]
        best_w = global_w
        best_s = -1.0e18
        for w in np.linspace(0.0, 1.0, 41):
            yhat = w * yva + (1.0 - w) * yvb
            s = explained_fraction(yv, yhat)
            if s > best_s:
                best_s = float(s)
                best_w = float(w)
        weights[bi] = best_w

    def apply_blend(phase_arr: np.ndarray, pa: np.ndarray, pb: np.ndarray) -> np.ndarray:
        out = np.zeros_like(pa)
        for i in range(phase_arr.size):
            p = float(phase_arr[i])
            bi = int(np.searchsorted(edges, p, side="right") - 1)
            bi = max(0, min(n_bins - 1, bi))
            w = float(weights[bi])
            out[i] = w * pa[i] + (1.0 - w) * pb[i]
        return out

    yhat_train = apply_blend(phase_train, ya_train, yb_train)
    yhat_test = apply_blend(phase_test, ya_test, yb_test)
    yhat_val = apply_blend(phase_val, ya_val, yb_val)
    return {
        "feature_count": int(X_a.shape[1] + X_b.shape[1]),
        "alpha_a": float(a["alpha"]),
        "alpha_b": float(b["alpha"]),
        "global_blend_weight_a": float(global_w),
        "val_explained": float(explained_fraction(y_val, yhat_val)),
        "train_explained": float(explained_fraction(y_train, yhat_train)),
        "test_explained": float(explained_fraction(y_test, yhat_test)),
        "train_rmse": float(np.sqrt(np.mean((y_train - yhat_train) ** 2))),
        "test_rmse": float(np.sqrt(np.mean((y_test - yhat_test) ** 2))),
        "n_bins": int(n_bins),
    }


def fit_eval_triple_blend_ridge_cv(
    X_state: np.ndarray,
    X_edge: np.ndarray,
    X_edge15: np.ndarray,
    y: np.ndarray,
    split: int,
) -> dict[str, float]:
    s = fit_ridge_cv_with_preds(X_state, y, split)
    e = fit_ridge_cv_with_preds(X_edge, y, split)
    q = fit_ridge_cv_with_preds(X_edge15, y, split)

    y_val = np.asarray(s["y_val"], dtype=float)
    ys_val = np.asarray(s["yhat_val"], dtype=float)
    ye_val = np.asarray(e["yhat_val"], dtype=float)
    yq_val = np.asarray(q["yhat_val"], dtype=float)

    best = (-1.0e18, 1.0, 0.0, 0.0)  # score, ws, we, wq
    grid = np.linspace(0.0, 1.0, 41)
    for ws in grid:
        for we in grid:
            wq = 1.0 - ws - we
            if wq < 0.0:
                continue
            yhat = ws * ys_val + we * ye_val + wq * yq_val
            sc = explained_fraction(y_val, yhat)
            if sc > best[0]:
                best = (float(sc), float(ws), float(we), float(wq))
    _, ws, we, wq = best

    y_train = np.asarray(s["y_train"], dtype=float)
    y_test = np.asarray(s["y_test"], dtype=float)
    ys_train = np.asarray(s["yhat_train"], dtype=float)
    ye_train = np.asarray(e["yhat_train"], dtype=float)
    yq_train = np.asarray(q["yhat_train"], dtype=float)
    ys_test = np.asarray(s["yhat_test"], dtype=float)
    ye_test = np.asarray(e["yhat_test"], dtype=float)
    yq_test = np.asarray(q["yhat_test"], dtype=float)

    yhat_train = ws * ys_train + we * ye_train + wq * yq_train
    yhat_test = ws * ys_test + we * ye_test + wq * yq_test
    return {
        "feature_count": int(X_state.shape[1] + X_edge.shape[1] + X_edge15.shape[1]),
        "alpha_state": float(s["alpha"]),
        "alpha_edge": float(e["alpha"]),
        "alpha_edge15": float(q["alpha"]),
        "blend_weight_state": float(ws),
        "blend_weight_edge": float(we),
        "blend_weight_edge15": float(wq),
        "val_explained": float(best[0]),
        "train_explained": float(explained_fraction(y_train, yhat_train)),
        "test_explained": float(explained_fraction(y_test, yhat_test)),
        "train_rmse": float(np.sqrt(np.mean((y_train - yhat_train) ** 2))),
        "test_rmse": float(np.sqrt(np.mean((y_test - yhat_test) ** 2))),
    }


def _build_physics_pruned_edge_l0(X_edge_l0: np.ndarray) -> np.ndarray:
    # Bottleneck-driven pruning:
    # - drop core_gate_phase (1..6)
    # - drop transfer_split (11..19)
    # - drop edge_norms (24..32)
    drop = list(range(1, 7)) + list(range(11, 20)) + list(range(24, 33))
    keep = np.ones(X_edge_l0.shape[1], dtype=bool)
    keep[np.asarray(drop, dtype=int)] = False
    return X_edge_l0[:, keep]


def _build_physics_pruned2_edge_l0(X_edge_l0: np.ndarray) -> np.ndarray:
    # Start from physics-pruned baseline, then remove bottleneck columns discovered by
    # column-wise ablation inside interaction/cancel/void block.
    # Extra original columns removed: 40, 50, 38, 37
    base_drop = set(list(range(1, 7)) + list(range(11, 20)) + list(range(24, 33)))
    keep_orig = [i for i in range(X_edge_l0.shape[1]) if i not in base_drop]
    orig_to_pruned = {orig: pi for pi, orig in enumerate(keep_orig)}
    extra_orig = [40, 50, 38, 37]
    extra_pruned = sorted(orig_to_pruned[o] for o in extra_orig if o in orig_to_pruned)
    X1 = X_edge_l0[:, keep_orig]
    return np.delete(X1, np.asarray(extra_pruned, dtype=int), axis=1)


def _fit_predict_regime_ridge(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    X_test: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    alphas = np.logspace(-6, 4, 21)
    X_train_n = _zscore_from_train(X_train, X_train)
    X_val_n = _zscore_from_train(X_train, X_val)
    best_alpha = float(alphas[0])
    best_val = -1.0e18
    for a in alphas:
        yhat_val = _ridge_predict(X_train_n, y_train, X_val_n, float(a))
        score = explained_fraction(y_val, yhat_val)
        if score > best_val:
            best_val = float(score)
            best_alpha = float(a)
    X_test_n = _zscore_from_train(X_train, X_test)
    yhat_val_best = _ridge_predict(X_train_n, y_train, X_val_n, best_alpha)
    yhat_test_best = _ridge_predict(X_train_n, y_train, X_test_n, best_alpha)
    return yhat_val_best, yhat_test_best, float(best_alpha), float(best_val)


def fit_eval_mode_switch_ridge_cv(
    X: np.ndarray,
    y: np.ndarray,
    split: int,
    mode_col_idx: int | None = None,
    mode_series: np.ndarray | None = None,
    threshold: float = 0.5,
) -> dict[str, float]:
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    if mode_series is not None:
        mode_arr = np.asarray(mode_series, dtype=float).reshape(-1)
        mode_train = mode_arr[:split]
        mode_test = mode_arr[split:]
    elif mode_col_idx is not None:
        mode_train = X_train[:, mode_col_idx]
        mode_test = X_test[:, mode_col_idx]
    else:
        base = fit_eval_ridge_cv(X, y, split)
        base["mode_switch_fallback"] = 1.0
        return base
    n_train = X_train.shape[0]
    val_start = max(16, int(0.8 * n_train))
    X_fit = X_train[:val_start]
    y_fit = y_train[:val_start]
    X_val = X_train[val_start:]
    y_val = y_train[val_start:]
    mode_fit = mode_train[:val_start]
    mode_val = mode_train[val_start:]
    fit_mask_tunnel = mode_fit >= threshold
    fit_mask_day = ~fit_mask_tunnel
    val_mask_tunnel = mode_val >= threshold
    val_mask_day = ~val_mask_tunnel
    test_mask_tunnel = mode_test >= threshold
    test_mask_day = ~test_mask_tunnel

    # Fallback to single-model ridge if one regime is too sparse.
    if (
        int(np.sum(fit_mask_tunnel)) < 32
        or int(np.sum(fit_mask_day)) < 32
        or int(np.sum(val_mask_tunnel)) < 8
        or int(np.sum(val_mask_day)) < 8
    ):
        base = fit_eval_ridge_cv(X, y, split)
        base["mode_switch_fallback"] = 1.0
        return base

    yhat_val = np.zeros_like(y_val)
    yhat_test = np.zeros_like(y_test)

    yhat_val_t, yhat_test_t, a_t, v_t = _fit_predict_regime_ridge(
        X_fit[fit_mask_tunnel],
        y_fit[fit_mask_tunnel],
        X_val[val_mask_tunnel],
        y_val[val_mask_tunnel],
        X_test[test_mask_tunnel],
    )
    yhat_val_d, yhat_test_d, a_d, v_d = _fit_predict_regime_ridge(
        X_fit[fit_mask_day],
        y_fit[fit_mask_day],
        X_val[val_mask_day],
        y_val[val_mask_day],
        X_test[test_mask_day],
    )
    yhat_val[val_mask_tunnel] = yhat_val_t
    yhat_val[val_mask_day] = yhat_val_d
    yhat_test[test_mask_tunnel] = yhat_test_t
    yhat_test[test_mask_day] = yhat_test_d

    # Refit train predictions per-regime for train score.
    train_mask_tunnel = mode_train >= threshold
    train_mask_day = ~train_mask_tunnel
    yhat_train = np.zeros_like(y_train)
    X_tt = X_train[train_mask_tunnel]
    X_td = X_train[train_mask_day]
    y_tt = y_train[train_mask_tunnel]
    y_td = y_train[train_mask_day]
    X_tt_n = _zscore_from_train(X_tt, X_tt)
    X_td_n = _zscore_from_train(X_td, X_td)
    yhat_train[train_mask_tunnel] = _ridge_predict(X_tt_n, y_tt, X_tt_n, a_t)
    yhat_train[train_mask_day] = _ridge_predict(X_td_n, y_td, X_td_n, a_d)

    return {
        "feature_count": int(X.shape[1]),
        "alpha_tunnel": float(a_t),
        "alpha_day": float(a_d),
        "val_explained_tunnel": float(v_t),
        "val_explained_day": float(v_d),
        "train_explained": float(explained_fraction(y_train, yhat_train)),
        "test_explained": float(explained_fraction(y_test, yhat_test)),
        "train_rmse": float(np.sqrt(np.mean((y_train - yhat_train) ** 2))),
        "test_rmse": float(np.sqrt(np.mean((y_test - yhat_test) ** 2))),
        "tunnel_ratio_train": float(np.mean(train_mask_tunnel)),
        "tunnel_ratio_test": float(np.mean(test_mask_tunnel)),
        "mode_switch_fallback": 0.0,
    }


def load_econ_macro_scalar(n_target: int, train_len: int) -> np.ndarray:
    df = pd.read_csv(ECON_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "ticker", "close"])
    tickers = ["BTC-USD", "SPY", "^VIX", "GC=F", "ETH-USD", "CL=F"]
    use = df[df["ticker"].isin(tickers)].copy()
    pivot = use.pivot_table(index="date", columns="ticker", values="close", aggfunc="last").sort_index()
    ret = np.log(pivot / pivot.shift(1)).replace([np.inf, -np.inf], np.nan)
    z = (ret - ret.mean()) / (ret.std() + 1.0e-12)
    macro = z.mean(axis=1, skipna=True).fillna(0.0).to_numpy(dtype=float)
    if macro.size == 0:
        return np.zeros(n_target, dtype=float)
    src_x = np.linspace(0.0, 1.0, num=macro.size, dtype=float)
    dst_x = np.linspace(0.0, 1.0, num=n_target, dtype=float)
    macro_interp = np.interp(dst_x, src_x, macro)
    m_mu = float(np.mean(macro_interp[:train_len]))
    m_sd = float(np.std(macro_interp[:train_len]) + 1.0e-12)
    return (macro_interp - m_mu) / m_sd


def build_edge_features(states: np.ndarray) -> np.ndarray:
    n = states.shape[0]
    rows: list[list[float]] = []
    for i in range(n):
        fill = float(i / max(n - 1, 1))
        minute = int((i % 96) * 15)
        clock = f"{minute // 60:02d}:{minute % 60:02d}"
        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock, edge15_gain=EDGE15_GAIN)
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
        bm_bw_unveiled = bm_bw_norm - float(split["lensing_delta"])
        bm_sm_unveiled = bm_sm_norm + float(split["bm_sm_effective"])
        bm_sw_unveiled = bm_sw_norm - float(split["stimulated_delta"])
        row = [
            1.0,
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
            float(step["edge15_term_norm"]),
            *np.asarray(step["edge15_term"], dtype=float).tolist(),
            *np.asarray(step["gated_branch"], dtype=float).tolist(),
        ]
        rows.append(row)
    return np.asarray(rows, dtype=float)


def build_layer0_features(states: np.ndarray, macro: np.ndarray) -> np.ndarray:
    n = states.shape[0]
    rows: list[list[float]] = []
    u0_prev = np.asarray(states[0], dtype=float)
    us_prev = np.asarray(states[0], dtype=float)
    for i in range(n):
        fill = float(i / max(n - 1, 1))
        minute = int((i % 96) * 15)
        clock = f"{minute // 60:02d}:{minute % 60:02d}"
        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock, edge15_gain=EDGE15_GAIN)
        split = step["tunnel_transfer_split"]
        resonance = float(split["bm_sm_effective"] - split["bw_bw_container_reserve"])
        lay = run_layered_step(
            states[i],
            u0_prev,
            us_prev,
            macro_scalar=float(macro[i]),
            resonance_scalar=resonance,
            phase_fill=fill,
        )
        u0_next = np.asarray(lay["u0_next"], dtype=float)
        us_next = np.asarray(lay["u_self_next"], dtype=float)
        rows.append([float(macro[i]), resonance, *u0_next.tolist(), *us_next.tolist()])
        u0_prev = u0_next
        us_prev = us_next
    return np.asarray(rows, dtype=float)


def build_edge15_features(states: np.ndarray) -> np.ndarray:
    """
    Build 6-particle / 15-edge geometry features from current 4-state + quark/gluon lifts.
    state4 order: [BM, BW, SM, SW] = [photon, proton, neutrino, electron]
    state6 order: [quark, gluon, neutrino, photon, proton, electron]
    """
    n = states.shape[0]
    rows: list[list[float]] = []
    for i in range(n):
        fill = float(i / max(n - 1, 1))
        minute = int((i % 96) * 15)
        clock = f"{minute // 60:02d}:{minute % 60:02d}"
        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock, edge15_gain=EDGE15_GAIN)
        s = np.asarray(states[i], dtype=float)
        bm, bw, sm, sw = float(s[0]), float(s[1]), float(s[2]), float(s[3])
        q9 = float(step["quark_9"])
        g10 = float(step["gluon_10"])
        state6 = np.array([q9, g10, sm, bm, bw, sw], dtype=float)
        geo = geometry_step_15(state6, dt=1.0)
        d6 = np.asarray(geo["dstate"], dtype=float)
        et6 = np.asarray(geo["edge_total"], dtype=float)
        eig = np.linalg.eigvalsh(np.asarray(geo["laplacian"], dtype=float))
        rows.append(
            [
                1.0,
                *state6.tolist(),
                *d6.tolist(),
                *et6.tolist(),
                *eig.tolist(),
            ]
        )
    return np.asarray(rows, dtype=float)


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    y_raw = load_seis_series()
    split = int(0.7 * (y_raw.size - 1))
    # strict normalization: train-only stats
    y_mu = float(np.mean(y_raw[: split + 1]))
    y_sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - y_mu) / y_sd

    states = causal_state_embed(y)
    y_next = y[1:]

    X_state = np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]])
    X_edge = build_edge_features(states[:-1])
    macro = load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
    X_l0 = build_layer0_features(states[:-1], macro)
    X_edge15 = build_edge15_features(states[:-1])
    X_edge_l0 = np.column_stack([X_edge, X_l0])
    X_edge15_l0 = np.column_stack([X_edge15, X_l0])
    X_union_l0 = np.column_stack([X_edge, X_edge15, X_l0])
    X_edge_l0_pruned = _build_physics_pruned_edge_l0(X_edge_l0)
    X_edge_l0_pruned2 = _build_physics_pruned2_edge_l0(X_edge_l0)

    report = {
        "domain": "seismology_daily_k_eff",
        "strict_holdout": True,
        "normalization": "train_only",
        "state_embedding": "causal",
        "edge15_gain": float(EDGE15_GAIN),
        "n_points": int(y_next.size),
        "split_index": int(split),
        "models": {
            "state_only": fit_eval(X_state, y_next, split),
            "edge_full": fit_eval(X_edge, y_next, split),
            "edge_plus_econ_layer0": fit_eval(X_edge_l0, y_next, split),
            "edge15_only": fit_eval(X_edge15, y_next, split),
            "edge15_plus_econ_layer0": fit_eval(X_edge15_l0, y_next, split),
            "edge_union_plus_econ_layer0": fit_eval(X_union_l0, y_next, split),
            "edge_plus_econ_layer0_pruned": fit_eval(X_edge_l0_pruned, y_next, split),
            "edge_plus_econ_layer0_pruned2": fit_eval(X_edge_l0_pruned2, y_next, split),
        },
        "models_ridge_cv": {
            "state_only": fit_eval_ridge_cv(X_state, y_next, split),
            "edge_full": fit_eval_ridge_cv(X_edge, y_next, split),
            "edge_plus_econ_layer0": fit_eval_ridge_cv(X_edge_l0, y_next, split),
            "edge15_only": fit_eval_ridge_cv(X_edge15, y_next, split),
            "edge15_plus_econ_layer0": fit_eval_ridge_cv(X_edge15_l0, y_next, split),
            "edge_union_plus_econ_layer0": fit_eval_ridge_cv(X_union_l0, y_next, split),
            "edge_plus_econ_layer0_pruned": fit_eval_ridge_cv(X_edge_l0_pruned, y_next, split),
            "edge_plus_econ_layer0_pruned2": fit_eval_ridge_cv(X_edge_l0_pruned2, y_next, split),
        },
        "models_mode_switch_ridge_cv": {
            "edge_plus_econ_layer0": fit_eval_mode_switch_ridge_cv(
                X_edge_l0, y_next, split, mode_col_idx=7
            ),
            "edge15_plus_econ_layer0": fit_eval_mode_switch_ridge_cv(
                X_edge15_l0, y_next, split, mode_series=X_edge_l0[:, 7]
            ),
        },
        "models_blend_ridge_cv": {
            "edge_and_edge15_plus_econ_layer0": fit_eval_blend_ridge_cv(
                X_edge_l0, X_edge15_l0, y_next, split
            ),
            "edge_pruned_and_edge15_plus_econ_layer0": fit_eval_blend_ridge_cv(
                X_edge_l0_pruned, X_edge15_l0, y_next, split
            ),
            "edge_pruned2_and_edge15_plus_econ_layer0": fit_eval_blend_ridge_cv(
                X_edge_l0_pruned2, X_edge15_l0, y_next, split
            ),
        },
        "models_phase_bin_blend_ridge_cv": {
            "edge_and_edge15_plus_econ_layer0": fit_eval_phase_bin_blend_ridge_cv(
                X_edge_l0, X_edge15_l0, y_next, split, phase_series=X_edge_l0[:, 5], n_bins=8
            ),
        },
        "models_triple_blend_ridge_cv": {
            "state_edge_edge15_plus_econ_layer0": fit_eval_triple_blend_ridge_cv(
                X_state, X_edge_l0, X_edge15_l0, y_next, split
            ),
        },
    }
    report["delta_vs_state_only_test"] = float(
        report["models"]["edge_plus_econ_layer0"]["test_explained"]
        - report["models"]["state_only"]["test_explained"]
    )
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    m = report["models"]
    lines = [
        "# Seismology + Economy Layer0 Strict Validation",
        "",
        f"- strict_holdout: `{report['strict_holdout']}`",
        f"- normalization: `{report['normalization']}`",
        f"- state_embedding: `{report['state_embedding']}`",
        f"- edge15_gain: `{report['edge15_gain']}`",
        f"- n_points: `{report['n_points']}`",
        f"- split_index: `{report['split_index']}`",
        "",
        f"- state_only test: `{m['state_only']['test_explained']}`",
        f"- edge_full test: `{m['edge_full']['test_explained']}`",
        f"- edge_plus_econ_layer0 test: `{m['edge_plus_econ_layer0']['test_explained']}`",
        f"- edge15_only test: `{m['edge15_only']['test_explained']}`",
        f"- edge15_plus_econ_layer0 test: `{m['edge15_plus_econ_layer0']['test_explained']}`",
        f"- edge_union_plus_econ_layer0 test: `{m['edge_union_plus_econ_layer0']['test_explained']}`",
        f"- edge_plus_econ_layer0_pruned test: `{m['edge_plus_econ_layer0_pruned']['test_explained']}`",
        f"- edge_plus_econ_layer0_pruned2 test: `{m['edge_plus_econ_layer0_pruned2']['test_explained']}`",
        f"- delta_vs_state_only_test: `{report['delta_vs_state_only_test']}`",
        "",
        "## Ridge CV",
        "",
        f"- state_only test: `{report['models_ridge_cv']['state_only']['test_explained']}` (alpha `{report['models_ridge_cv']['state_only']['alpha']}`)",
        f"- edge_full test: `{report['models_ridge_cv']['edge_full']['test_explained']}` (alpha `{report['models_ridge_cv']['edge_full']['alpha']}`)",
        f"- edge_plus_econ_layer0 test: `{report['models_ridge_cv']['edge_plus_econ_layer0']['test_explained']}` (alpha `{report['models_ridge_cv']['edge_plus_econ_layer0']['alpha']}`)",
        f"- edge15_only test: `{report['models_ridge_cv']['edge15_only']['test_explained']}` (alpha `{report['models_ridge_cv']['edge15_only']['alpha']}`)",
        f"- edge15_plus_econ_layer0 test: `{report['models_ridge_cv']['edge15_plus_econ_layer0']['test_explained']}` (alpha `{report['models_ridge_cv']['edge15_plus_econ_layer0']['alpha']}`)",
        f"- edge_union_plus_econ_layer0 test: `{report['models_ridge_cv']['edge_union_plus_econ_layer0']['test_explained']}` (alpha `{report['models_ridge_cv']['edge_union_plus_econ_layer0']['alpha']}`)",
        f"- edge_plus_econ_layer0_pruned test: `{report['models_ridge_cv']['edge_plus_econ_layer0_pruned']['test_explained']}` (alpha `{report['models_ridge_cv']['edge_plus_econ_layer0_pruned']['alpha']}`)",
        f"- edge_plus_econ_layer0_pruned2 test: `{report['models_ridge_cv']['edge_plus_econ_layer0_pruned2']['test_explained']}` (alpha `{report['models_ridge_cv']['edge_plus_econ_layer0_pruned2']['alpha']}`)",
        "",
        "## Mode Switch Ridge CV",
        "",
        f"- edge_plus_econ_layer0 test: `{report['models_mode_switch_ridge_cv']['edge_plus_econ_layer0']['test_explained']}`",
        f"- edge15_plus_econ_layer0 test: `{report['models_mode_switch_ridge_cv']['edge15_plus_econ_layer0']['test_explained']}`",
        "",
        "## Blend Ridge CV",
        "",
        f"- edge_and_edge15_plus_econ_layer0 test: `{report['models_blend_ridge_cv']['edge_and_edge15_plus_econ_layer0']['test_explained']}`",
        f"- blend weights (edge, edge15): `({report['models_blend_ridge_cv']['edge_and_edge15_plus_econ_layer0']['blend_weight_a']}, {report['models_blend_ridge_cv']['edge_and_edge15_plus_econ_layer0']['blend_weight_b']})`",
        f"- edge_pruned_and_edge15_plus_econ_layer0 test: `{report['models_blend_ridge_cv']['edge_pruned_and_edge15_plus_econ_layer0']['test_explained']}`",
        f"- blend weights (edge_pruned, edge15): `({report['models_blend_ridge_cv']['edge_pruned_and_edge15_plus_econ_layer0']['blend_weight_a']}, {report['models_blend_ridge_cv']['edge_pruned_and_edge15_plus_econ_layer0']['blend_weight_b']})`",
        f"- edge_pruned2_and_edge15_plus_econ_layer0 test: `{report['models_blend_ridge_cv']['edge_pruned2_and_edge15_plus_econ_layer0']['test_explained']}`",
        f"- blend weights (edge_pruned2, edge15): `({report['models_blend_ridge_cv']['edge_pruned2_and_edge15_plus_econ_layer0']['blend_weight_a']}, {report['models_blend_ridge_cv']['edge_pruned2_and_edge15_plus_econ_layer0']['blend_weight_b']})`",
        "",
        "## Phase Bin Blend Ridge CV",
        "",
        f"- edge_and_edge15_plus_econ_layer0 test: `{report['models_phase_bin_blend_ridge_cv']['edge_and_edge15_plus_econ_layer0']['test_explained']}`",
        f"- global_blend_weight_a: `{report['models_phase_bin_blend_ridge_cv']['edge_and_edge15_plus_econ_layer0']['global_blend_weight_a']}`",
        f"- n_bins: `{report['models_phase_bin_blend_ridge_cv']['edge_and_edge15_plus_econ_layer0']['n_bins']}`",
        "",
        "## Triple Blend Ridge CV",
        "",
        f"- state_edge_edge15_plus_econ_layer0 test: `{report['models_triple_blend_ridge_cv']['state_edge_edge15_plus_econ_layer0']['test_explained']}`",
        f"- blend weights (state, edge, edge15): `({report['models_triple_blend_ridge_cv']['state_edge_edge15_plus_econ_layer0']['blend_weight_state']}, {report['models_triple_blend_ridge_cv']['state_edge_edge15_plus_econ_layer0']['blend_weight_edge']}, {report['models_triple_blend_ridge_cv']['state_edge_edge15_plus_econ_layer0']['blend_weight_edge15']})`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
