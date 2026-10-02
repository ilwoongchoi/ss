from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v
import fusion_clean as eq


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\physics_constraint_sweep.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\physics_constraint_sweep.md")


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1.0e-12:
        return 0.0
    err = y - y_hat
    return float(1.0 - (np.mean(err * err) / var))


def eval_once(split: int, y_next: np.ndarray, states: np.ndarray) -> dict[str, float]:
    X_edge = v.build_edge_features(states[:-1])
    macro = v.load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
    X_l0 = v.build_layer0_features(states[:-1], macro)
    X15 = np.column_stack([v.build_edge15_features(states[:-1]), X_l0])
    X_edge_l0 = np.column_stack([X_edge, X_l0])
    Xp2 = v._build_physics_pruned2_edge_l0(X_edge_l0)

    a = v.fit_ridge_cv_with_preds(Xp2, y_next, split)
    b = v.fit_ridge_cv_with_preds(X15, y_next, split)
    yv = np.asarray(a["y_val"], dtype=float)
    yva = np.asarray(a["yhat_val"], dtype=float)
    yvb = np.asarray(b["yhat_val"], dtype=float)
    yt = np.asarray(a["y_test"], dtype=float)
    yta = np.asarray(a["yhat_test"], dtype=float)
    ytb = np.asarray(b["yhat_test"], dtype=float)

    best_val = -1.0e18
    best_w = 0.5
    for w in np.linspace(0.0, 1.0, 201):
        yhat = w * yva + (1.0 - w) * yvb
        s = explained_fraction(yv, yhat)
        if s > best_val:
            best_val = float(s)
            best_w = float(w)
    yhat_test = best_w * yta + (1.0 - best_w) * ytb
    test_score = explained_fraction(yt, yhat_test)
    abs_res = np.abs(yt - yhat_test)
    lensing_norm = X_edge[split:, 21]
    lens_corr = 0.0
    if float(np.std(lensing_norm)) > 1.0e-12 and float(np.std(abs_res)) > 1.0e-12:
        lens_corr = float(np.corrcoef(lensing_norm, abs_res)[0, 1])
    return {
        "test_explained": float(test_score),
        "blend_w_pruned2": float(best_w),
        "blend_w_edge15": float(1.0 - best_w),
        "lensing_norm_abs_res_corr": float(lens_corr),
    }


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    y_raw = v.load_seis_series()
    split = int(0.7 * (y_raw.size - 1))
    y_mu = float(np.mean(y_raw[: split + 1]))
    y_sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - y_mu) / y_sd
    states = v.causal_state_embed(y)
    y_next = y[1:]

    original = dict(eq.PHYSICS_BRIDGE_CONSTRAINTS)
    rows = []
    try:
        for direct in [0.25, 0.35, 0.45]:
            for core_boost in [0.12, 0.18, 0.24]:
                for unveil in [0.20, 0.35, 0.50]:
                    eq.PHYSICS_BRIDGE_CONSTRAINTS["bm_sm_direct_day_suppress"] = float(direct)
                    eq.PHYSICS_BRIDGE_CONSTRAINTS["indirect_day_core_boost"] = float(core_boost)
                    eq.PHYSICS_BRIDGE_CONSTRAINTS["day_lensing_unveil_gain"] = float(unveil)
                    r = eval_once(split, y_next, states)
                    rows.append(
                        {
                            "bm_sm_direct_day_suppress": float(direct),
                            "indirect_day_core_boost": float(core_boost),
                            "day_lensing_unveil_gain": float(unveil),
                            **r,
                            # Combined objective: prefer high test score and lower lensing bottleneck.
                            "objective": float(r["test_explained"] - 0.02 * abs(r["lensing_norm_abs_res_corr"])),
                        }
                    )
    finally:
        eq.PHYSICS_BRIDGE_CONSTRAINTS.clear()
        eq.PHYSICS_BRIDGE_CONSTRAINTS.update(original)

    rows_sorted = sorted(rows, key=lambda z: z["objective"], reverse=True)
    best = rows_sorted[0] if rows_sorted else {}
    out = {"best": best, "top10": rows_sorted[:10], "n_runs": len(rows_sorted)}
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Physics Constraint Sweep",
        "",
        f"- n_runs: `{out['n_runs']}`",
        f"- best_test_explained: `{best.get('test_explained')}`",
        f"- best_lensing_norm_abs_res_corr: `{best.get('lensing_norm_abs_res_corr')}`",
        f"- best_params: `direct_day={best.get('bm_sm_direct_day_suppress')}, core_boost={best.get('indirect_day_core_boost')}, unveil={best.get('day_lensing_unveil_gain')}`",
        "",
        "## Top 10",
    ]
    for i, row in enumerate(out["top10"], 1):
        lines.append(
            f"- {i}. test `{row['test_explained']}` | corr `{row['lensing_norm_abs_res_corr']}` | params ({row['bm_sm_direct_day_suppress']}, {row['indirect_day_core_boost']}, {row['day_lensing_unveil_gain']})"
        )
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

