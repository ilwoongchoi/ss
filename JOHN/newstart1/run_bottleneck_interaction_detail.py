from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\bottleneck_interaction_detail.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\bottleneck_interaction_detail.md")


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
    X_edge_l0 = np.column_stack([X_edge, X_l0])

    # Use physics-pruned base as current stable baseline.
    X_base = v._build_physics_pruned_edge_l0(X_edge_l0)
    base = v.fit_eval_ridge_cv(X_base, y_next, split)

    # Map original edge_l0 columns to pruned columns.
    drop_physics = set(list(range(1, 7)) + list(range(11, 20)) + list(range(24, 33)))
    keep_cols = [i for i in range(X_edge_l0.shape[1]) if i not in drop_physics]
    col_to_pruned = {orig: pi for pi, orig in enumerate(keep_cols)}

    # Interaction block in original indexing.
    interaction_cols = list(range(37, 57))
    rows = []
    for oc in interaction_cols:
        if oc not in col_to_pruned:
            continue
        pc = col_to_pruned[oc]
        keep = np.ones(X_base.shape[1], dtype=bool)
        keep[pc] = False
        r = v.fit_eval_ridge_cv(X_base[:, keep], y_next, split)
        rows.append(
            {
                "orig_col": int(oc),
                "pruned_col": int(pc),
                "test_explained": float(r["test_explained"]),
                "delta_vs_base": float(r["test_explained"] - base["test_explained"]),
                "alpha": float(r["alpha"]),
            }
        )

    rows_sorted = sorted(rows, key=lambda z: z["delta_vs_base"], reverse=True)
    report = {
        "base_test_explained": float(base["test_explained"]),
        "base_alpha": float(base["alpha"]),
        "drops": rows_sorted,
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Bottleneck Interaction Detail (column-wise drop)",
        "",
        f"- base_test_explained: `{report['base_test_explained']}`",
        f"- base_alpha: `{report['base_alpha']}`",
        "",
        "## Drops (sorted by improvement)",
    ]
    for row in rows_sorted:
        lines.append(
            f"- drop col `{row['orig_col']}` (pruned idx `{row['pruned_col']}`): test `{row['test_explained']}` | delta `{row['delta_vs_base']}`"
        )
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

