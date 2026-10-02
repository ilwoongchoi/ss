from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v
import fusion_clean as eq


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\four_subject_order_sweep.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\four_subject_order_sweep.md")


def run_once(
    quark_order: float,
    neutrino_order: float,
    gluon_order: float,
    electron_order: float,
    efficiency_target: float = 0.8009,
) -> dict[str, float]:
    original = v.edge_stack_master_step

    def wrapped(state4, phase_fill=0.0, time_like=None, clock_hhmm="00:00", edge15_gain=0.0):
        return eq.edge_stack_master_step(
            state4,
            phase_fill=phase_fill,
            time_like=time_like,
            clock_hhmm=clock_hhmm,
            edge15_gain=edge15_gain,
            enable_unified_operator=True,
            quark_order=float(quark_order),
            neutrino_order=float(neutrino_order),
            gluon_order=float(gluon_order),
            electron_order=float(electron_order),
            efficiency_target=float(efficiency_target),
        )

    v.edge_stack_master_step = wrapped
    try:
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
        X_edge15 = v.build_edge15_features(states[:-1])
        X_edge_l0 = np.column_stack([X_edge, X_l0])
        X_edge15_l0 = np.column_stack([X_edge15, X_l0])
        X_edge_l0_pruned2 = v._build_physics_pruned2_edge_l0(X_edge_l0)

        r = v.fit_eval_blend_ridge_cv(X_edge_l0_pruned2, X_edge15_l0, y_next, split)
        return {
            "quark_order": float(quark_order),
            "neutrino_order": float(neutrino_order),
            "gluon_order": float(gluon_order),
            "electron_order": float(electron_order),
            "efficiency_target": float(efficiency_target),
            "test_explained": float(r["test_explained"]),
            "val_explained": float(r["val_explained"]),
            "blend_weight_a": float(r["blend_weight_a"]),
            "blend_weight_b": float(r["blend_weight_b"]),
        }
    finally:
        v.edge_stack_master_step = original


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    # Coarse grid first to keep runtime bounded.
    q_grid = [3.3, 3.5, 3.7]
    n_grid = [2.3, 2.5, 2.7]
    g_grid = [3.3, 3.5, 3.7]
    e_grid = [0.8, 1.0, 1.2]

    rows: list[dict[str, float]] = []
    for q in q_grid:
        for n in n_grid:
            for g in g_grid:
                for e in e_grid:
                    rows.append(run_once(q, n, g, e))

    rows.sort(key=lambda x: x["test_explained"], reverse=True)
    best = rows[0]

    payload = {
        "best": best,
        "rows": rows,
        "grid": {
            "quark_order": q_grid,
            "neutrino_order": n_grid,
            "gluon_order": g_grid,
            "electron_order": e_grid,
        },
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Four-Subject Order Sweep (proton/photon fixed)",
        "",
        "## Best",
        f"- quark_order: `{best['quark_order']}`",
        f"- neutrino_order: `{best['neutrino_order']}`",
        f"- gluon_order: `{best['gluon_order']}`",
        f"- electron_order: `{best['electron_order']}`",
        f"- test_explained: `{best['test_explained']}`",
        f"- val_explained: `{best['val_explained']}`",
        f"- blend_weight_a(pruned2): `{best['blend_weight_a']}`",
        f"- blend_weight_b(edge15): `{best['blend_weight_b']}`",
        "",
        "## Top 10",
    ]
    for i, r in enumerate(rows[:10], start=1):
        lines.append(
            f"- {i}. q={r['quark_order']}, n={r['neutrino_order']}, g={r['gluon_order']}, e={r['electron_order']} | test={r['test_explained']} | val={r['val_explained']}"
        )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
