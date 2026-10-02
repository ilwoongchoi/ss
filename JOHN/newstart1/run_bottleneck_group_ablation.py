from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\bottleneck_group_ablation.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\bottleneck_group_ablation.md")


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

    # Column groups inside X_edge (prefix of X_edge_l0).
    # Based on run_seismology_econ_layer0_strict_validation.build_edge_features
    groups = {
        "core_gate_phase": list(range(1, 7)),
        "face_tunnel": list(range(7, 11)),
        "transfer_split": list(range(11, 20)),
        "lensing_plp_norms": list(range(21, 24)),
        "edge_norms": list(range(24, 33)),
        "core_vectors": list(range(33, 37)),
        "edge_interaction_cancel_void": list(range(37, 57)),
        "particle_9_13_scalars": list(range(57, 62)),
        "edge15_projected": list(range(62, 67)),
        "gated_branch": list(range(67, 71)),
    }

    base = v.fit_eval_ridge_cv(X_edge_l0, y_next, split)
    results = {"base": base, "ablations": {}}
    ncols = X_edge_l0.shape[1]
    for name, gcols in groups.items():
        keep = np.ones(ncols, dtype=bool)
        keep[np.asarray(gcols, dtype=int)] = False
        X_drop = X_edge_l0[:, keep]
        r = v.fit_eval_ridge_cv(X_drop, y_next, split)
        results["ablations"][name] = {
            "feature_count": int(X_drop.shape[1]),
            "test_explained": float(r["test_explained"]),
            "delta_vs_base": float(r["test_explained"] - base["test_explained"]),
            "alpha": float(r["alpha"]),
        }

    OUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Bottleneck Group Ablation (Edge+Econ Layer0, Ridge-CV)",
        "",
        f"- base_test_explained: `{base['test_explained']}`",
        f"- base_alpha: `{base['alpha']}`",
        "",
        "## Group Drops",
    ]
    for name, row in sorted(results["ablations"].items(), key=lambda kv: kv[1]["delta_vs_base"]):
        lines.append(
            f"- drop `{name}`: test `{row['test_explained']}` | delta `{row['delta_vs_base']}` | alpha `{row['alpha']}`"
        )
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

