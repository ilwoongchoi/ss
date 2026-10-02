from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\day_bottleneck_operator_test.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\day_bottleneck_operator_test.md")


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1.0e-12:
        return 0.0
    err = y - y_hat
    return float(1.0 - (np.mean(err * err) / var))


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    y_raw = v.load_seis_series()
    split = int(0.7 * (y_raw.size - 1))
    y_mu = float(np.mean(y_raw[: split + 1]))
    y_sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - y_mu) / y_sd
    states = v.causal_state_embed(y)
    y_next = y[1:]

    X_edge = v.build_edge_features(states[:-1])
    macro = v.load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
    X_l0 = v.build_layer0_features(states[:-1], macro)
    X_edge15_l0 = np.column_stack([v.build_edge15_features(states[:-1]), X_l0])
    X_pruned2 = v._build_physics_pruned2_edge_l0(np.column_stack([X_edge, X_l0]))

    # Base blend (current best family)
    a = v.fit_ridge_cv_with_preds(X_pruned2, y_next, split)
    b = v.fit_ridge_cv_with_preds(X_edge15_l0, y_next, split)
    yv = np.asarray(a["y_val"], dtype=float)
    yva = np.asarray(a["yhat_val"], dtype=float)
    yvb = np.asarray(b["yhat_val"], dtype=float)
    yt = np.asarray(a["y_test"], dtype=float)
    yta = np.asarray(a["yhat_test"], dtype=float)
    ytb = np.asarray(b["yhat_test"], dtype=float)
    best_w = 0.5
    best_val = -1.0e18
    for w in np.linspace(0.0, 1.0, 201):
        s = explained_fraction(yv, w * yva + (1.0 - w) * yvb)
        if s > best_val:
            best_val = float(s)
            best_w = float(w)
    yhat_base_train = best_w * np.asarray(a["yhat_train"], dtype=float) + (1.0 - best_w) * np.asarray(b["yhat_train"], dtype=float)
    yhat_base_test = best_w * yta + (1.0 - best_w) * ytb
    y_train = np.asarray(a["y_train"], dtype=float)
    y_test = np.asarray(a["y_test"], dtype=float)

    # Day-bottleneck features from edge table.
    # cols: is_tunnel=7, lensing_norm=21, quark_9=61, gluon_10=62
    xe_train = X_edge[:split]
    xe_test = X_edge[split:]
    day_train = xe_train[:, 7] < 0.5
    day_test = xe_test[:, 7] < 0.5
    F_train = np.column_stack(
        [
            np.ones(np.sum(day_train), dtype=float),
            xe_train[day_train, 21],
            xe_train[day_train, 61],
            xe_train[day_train, 62],
        ]
    )
    F_test = np.column_stack(
        [
            np.ones(np.sum(day_test), dtype=float),
            xe_test[day_test, 21],
            xe_test[day_test, 61],
            xe_test[day_test, 62],
        ]
    )
    r_train = (y_train - yhat_base_train)[day_train]

    # Ridge fit for residual operator with validation on tail of train-day.
    n_day = F_train.shape[0]
    val_start = max(16, int(0.8 * n_day))
    F_fit, F_val = F_train[:val_start], F_train[val_start:]
    r_fit, r_val = r_train[:val_start], r_train[val_start:]
    mu = np.mean(F_fit, axis=0)
    sd = np.std(F_fit, axis=0) + 1.0e-12
    F_fit_n = (F_fit - mu) / sd
    F_val_n = (F_val - mu) / sd
    F_train_n = (F_train - mu) / sd
    F_test_n = (F_test - mu) / sd
    F_fit_n[:, 0] = 1.0
    F_val_n[:, 0] = 1.0
    F_train_n[:, 0] = 1.0
    F_test_n[:, 0] = 1.0

    best_alpha = 1e-6
    best_day_val = -1.0e18
    best_beta = None
    for alpha in np.logspace(-6, 3, 19):
        reg = np.eye(F_fit_n.shape[1], dtype=float) * float(alpha)
        reg[0, 0] = 0.0
        beta = np.linalg.pinv(F_fit_n.T @ F_fit_n + reg) @ (F_fit_n.T @ r_fit)
        rv = F_val_n @ beta
        sc = explained_fraction(r_val, rv)
        if sc > best_day_val:
            best_day_val = float(sc)
            best_alpha = float(alpha)
            best_beta = beta

    corr_train_day = F_train_n @ best_beta
    corr_test_day = F_test_n @ best_beta

    # Blend day-operator strength gamma via validation on overall train tail.
    # Use original time split tail for objective.
    y_tail = y_train[split - (y_train.size - split) :] if False else y_train  # no-op placeholder
    # Build corrected train for gamma search.
    yhat_train_corr = yhat_base_train.copy()
    yhat_train_corr[day_train] = yhat_train_corr[day_train] + corr_train_day
    # gamma search on full train explained (conservative).
    best_gamma = 0.0
    best_train_score = explained_fraction(y_train, yhat_base_train)
    for gamma in np.linspace(0.0, 1.0, 101):
        yhat_g = yhat_base_train.copy()
        yhat_g[day_train] = yhat_base_train[day_train] + gamma * corr_train_day
        sc = explained_fraction(y_train, yhat_g)
        if sc > best_train_score:
            best_train_score = float(sc)
            best_gamma = float(gamma)

    yhat_test = yhat_base_test.copy()
    yhat_test[day_test] = yhat_base_test[day_test] + best_gamma * corr_test_day

    base_test = explained_fraction(y_test, yhat_base_test)
    corr_test = explained_fraction(y_test, yhat_test)
    out = {
        "base_test_explained": float(base_test),
        "corrected_test_explained": float(corr_test),
        "delta_test": float(corr_test - base_test),
        "blend_weight_pruned2": float(best_w),
        "blend_weight_edge15": float(1.0 - best_w),
        "day_operator_alpha": float(best_alpha),
        "day_operator_gamma": float(best_gamma),
        "day_val_explained_on_residual": float(best_day_val),
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Day Bottleneck Operator Test",
        "",
        f"- base_test_explained: `{out['base_test_explained']}`",
        f"- corrected_test_explained: `{out['corrected_test_explained']}`",
        f"- delta_test: `{out['delta_test']}`",
        f"- blend weights (pruned2, edge15): `({out['blend_weight_pruned2']}, {out['blend_weight_edge15']})`",
        f"- day_operator_alpha: `{out['day_operator_alpha']}`",
        f"- day_operator_gamma: `{out['day_operator_gamma']}`",
        f"- day_val_explained_on_residual: `{out['day_val_explained_on_residual']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

