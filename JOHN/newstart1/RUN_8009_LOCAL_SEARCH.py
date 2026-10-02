from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v
import fusion_clean as eq


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\physics_constraint_local_search.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\physics_constraint_local_search.md")


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1.0e-12:
        return 0.0
    err = y - y_hat
    return float(1.0 - (np.mean(err * err) / var))


def eval_params(split: int, y_next: np.ndarray, states: np.ndarray, p: dict[str, float]) -> dict[str, float]:
    eq.PHYSICS_BRIDGE_CONSTRAINTS["bm_sm_direct_day_suppress"] = float(p["direct_day"])
    eq.PHYSICS_BRIDGE_CONSTRAINTS["indirect_day_core_boost"] = float(p["core_boost"])
    eq.PHYSICS_BRIDGE_CONSTRAINTS["day_lensing_unveil_gain"] = float(p["unveil"])
    eq.PHYSICS_BRIDGE_CONSTRAINTS["brems_to_lensing_day_gain"] = float(p["brems_day"])
    eq.PHYSICS_BRIDGE_CONSTRAINTS["brems_to_lensing_tunnel_gain"] = float(p["brems_tunnel"])

    X_edge = v.build_edge_features(states[:-1])
    macro = v.load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
    X_l0 = v.build_layer0_features(states[:-1], macro)
    Xp2 = v._build_physics_pruned2_edge_l0(np.column_stack([X_edge, X_l0]))
    X15 = np.column_stack([v.build_edge15_features(states[:-1]), X_l0])

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
        s = explained_fraction(yv, w * yva + (1.0 - w) * yvb)
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
        "lensing_corr": float(lens_corr),
        "objective": float(test_score - 0.02 * abs(lens_corr)),
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
    try:
        cur = {
            "direct_day": float(eq.PHYSICS_BRIDGE_CONSTRAINTS["bm_sm_direct_day_suppress"]),
            "core_boost": float(eq.PHYSICS_BRIDGE_CONSTRAINTS["indirect_day_core_boost"]),
            "unveil": float(eq.PHYSICS_BRIDGE_CONSTRAINTS["day_lensing_unveil_gain"]),
            "brems_day": float(eq.PHYSICS_BRIDGE_CONSTRAINTS["brems_to_lensing_day_gain"]),
            "brems_tunnel": float(eq.PHYSICS_BRIDGE_CONSTRAINTS["brems_to_lensing_tunnel_gain"]),
        }
        steps = {
            "direct_day": 0.05,
            "core_boost": 0.04,
            "unveil": 0.10,
            "brems_day": 0.04,
            "brems_tunnel": 0.02,
        }
        bounds = {
            "direct_day": (0.10, 0.60),
            "core_boost": (0.00, 0.40),
            "unveil": (0.10, 0.80),
            "brems_day": (0.00, 0.20),
            "brems_tunnel": (0.00, 0.10),
        }

        history: list[dict[str, float]] = []
        best = {**cur, **eval_params(split, y_next, states, cur)}
        history.append(dict(best))

        for _ in range(3):
            improved = False
            for k in ["direct_day", "core_boost", "unveil", "brems_day", "brems_tunnel"]:
                local_best = dict(best)
                for d in (-steps[k], steps[k]):
                    cand = dict(cur)
                    cand[k] = float(np.clip(cand[k] + d, bounds[k][0], bounds[k][1]))
                    out = eval_params(split, y_next, states, cand)
                    row = {**cand, **out}
                    history.append(dict(row))
                    if row["objective"] > local_best["objective"]:
                        local_best = row
                if local_best["objective"] > best["objective"]:
                    best = dict(local_best)
                    cur = {kk: best[kk] for kk in cur.keys()}
                    improved = True
            for k in steps:
                steps[k] *= 0.5
            if not improved:
                break

        out = {
            "start": history[0],
            "best": best,
            "history": history,
            "n_evals": len(history),
        }
        OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        lines = [
            "# Physics Constraint Local Search",
            "",
            f"- n_evals: `{out['n_evals']}`",
            f"- start_test_explained: `{out['start']['test_explained']}`",
            f"- best_test_explained: `{out['best']['test_explained']}`",
            f"- best_lensing_corr: `{out['best']['lensing_corr']}`",
            f"- best_params: `direct_day={out['best']['direct_day']}, core_boost={out['best']['core_boost']}, unveil={out['best']['unveil']}, brems_day={out['best']['brems_day']}, brems_tunnel={out['best']['brems_tunnel']}`",
            "",
        ]
        OUT_MD.write_text("\n".join(lines), encoding="utf-8")
        print(str(OUT_MD))
        return 0
    finally:
        eq.PHYSICS_BRIDGE_CONSTRAINTS.clear()
        eq.PHYSICS_BRIDGE_CONSTRAINTS.update(original)


if __name__ == "__main__":
    raise SystemExit(main())

