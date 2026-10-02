from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\engineering_fallback_check.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\engineering_fallback_check.md")


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1.0e-12:
        return 0.0
    err = y - y_hat
    return float(1.0 - (np.mean(err * err) / var))


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    # Base dataset
    y_raw = v.load_seis_series()
    split = int(0.7 * (y_raw.size - 1))
    y_mu = float(np.mean(y_raw[: split + 1]))
    y_sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - y_mu) / y_sd
    states = v.causal_state_embed(y)
    y_next = y[1:]

    # Best current predictor family: pruned2 + edge15 blend
    X_edge = v.build_edge_features(states[:-1])
    macro = v.load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
    X_l0 = v.build_layer0_features(states[:-1], macro)
    X_pruned2 = v._build_physics_pruned2_edge_l0(np.column_stack([X_edge, X_l0]))
    X_edge15_l0 = np.column_stack([v.build_edge15_features(states[:-1]), X_l0])

    a = v.fit_ridge_cv_with_preds(X_pruned2, y_next, split)
    b = v.fit_ridge_cv_with_preds(X_edge15_l0, y_next, split)
    yv = np.asarray(a["y_val"], dtype=float)
    yva = np.asarray(a["yhat_val"], dtype=float)
    yvb = np.asarray(b["yhat_val"], dtype=float)
    yt = np.asarray(a["y_test"], dtype=float)
    yta = np.asarray(a["yhat_test"], dtype=float)
    ytb = np.asarray(b["yhat_test"], dtype=float)

    best_val = -1.0e18
    w = 0.5
    for ww in np.linspace(0.0, 1.0, 201):
        s = explained_fraction(yv, ww * yva + (1.0 - ww) * yvb)
        if s > best_val:
            best_val = float(s)
            w = float(ww)
    yhat_base = w * yta + (1.0 - w) * ytb
    base_test = explained_fraction(yt, yhat_base)

    # Engineering fallback (not default): fixed RHS closure in normalized space.
    # Target homeostasis index in normalized residual space is 0.
    omega_target = 0.0
    kappa = 0.2828
    # x_{t+1} = x_t + kappa*(omega - x_t)  => one-step contraction to fixed point
    yhat_eng = yhat_base + kappa * (omega_target - yhat_base)
    eng_test = explained_fraction(yt, yhat_eng)

    out = {
        "base_test_explained": float(base_test),
        "engineering_fallback_test_explained": float(eng_test),
        "delta_test": float(eng_test - base_test),
        "blend_weight_pruned2": float(w),
        "blend_weight_edge15": float(1.0 - w),
        "omega_target": float(omega_target),
        "kappa": float(kappa),
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Engineering Fallback Check",
        "",
        f"- base_test_explained: `{out['base_test_explained']}`",
        f"- engineering_fallback_test_explained: `{out['engineering_fallback_test_explained']}`",
        f"- delta_test: `{out['delta_test']}`",
        f"- blend weights (pruned2, edge15): `({out['blend_weight_pruned2']}, {out['blend_weight_edge15']})`",
        f"- omega_target: `{out['omega_target']}`",
        f"- kappa: `{out['kappa']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

