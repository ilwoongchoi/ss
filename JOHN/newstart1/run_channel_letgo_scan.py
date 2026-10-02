from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_seismology_econ_layer0_strict_validation as v
import fusion_clean as eq


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\channel_letgo_scan.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\channel_letgo_scan.md")


CHANNELS = [
    "gaba_b",
    "female_gaba_b_latdorsi",
    "right_acetylcholine",
    "left_acetyl_coa",
    "right_dopamine",
    "muscle_a",
    "muscle_b",
    "left_estrogen",
    "left_temporalis_5ht1a",
    "right_5ht1b_synchrotron",
    "glucocorticoid",
    "right_cortisol",
    "left_extraversion",
    "right_occipitalis_gaba_a",
    "left_frontalis_d2",
    "hypoxia",
    "right_love",
    "vasopressin_female",
    "right_androgen",
    "left_endorphin",
]


def _score_with_override(states: np.ndarray, y_next: np.ndarray, split: int, override: dict[str, str] | None) -> dict[str, float]:
    original = v.edge_stack_master_step

    def wrapped(state4, phase_fill=0.0, time_like=None, clock_hhmm="00:00", edge15_gain=0.0):
        return eq.edge_stack_master_step(
            state4,
            phase_fill=phase_fill,
            time_like=time_like,
            clock_hhmm=clock_hhmm,
            edge15_gain=edge15_gain,
            control_override=override,
        )

    v.edge_stack_master_step = wrapped
    try:
        X_edge = v.build_edge_features(states[:-1])
        macro = v.load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
        X_l0 = v.build_layer0_features(states[:-1], macro)
        X_edge15 = v.build_edge15_features(states[:-1])
        X_edge_l0 = np.column_stack([X_edge, X_l0])
        X_edge15_l0 = np.column_stack([X_edge15, X_l0])
        X_edge_l0_pruned2 = v._build_physics_pruned2_edge_l0(X_edge_l0)

        r = v.fit_eval_blend_ridge_cv(X_edge_l0_pruned2, X_edge15_l0, y_next, split)
        return {
            "test_explained": float(r["test_explained"]),
            "val_explained": float(r["val_explained"]),
            "blend_weight_a": float(r["blend_weight_a"]),
            "blend_weight_b": float(r["blend_weight_b"]),
        }
    finally:
        v.edge_stack_master_step = original


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    y_raw = v.load_seis_series()
    split = int(0.7 * (y_raw.size - 1))
    y_mu = float(np.mean(y_raw[: split + 1]))
    y_sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - y_mu) / y_sd

    states = v.causal_state_embed(y)
    y_next = y[1:]

    baseline = _score_with_override(states, y_next, split, override=None)
    rows: list[dict[str, float | str]] = []
    for ch in CHANNELS:
        r = _score_with_override(states, y_next, split, override={ch: "no_control"})
        rows.append(
            {
                "channel": ch,
                "test_explained": float(r["test_explained"]),
                "delta_vs_baseline": float(r["test_explained"] - baseline["test_explained"]),
                "blend_weight_a": float(r["blend_weight_a"]),
                "blend_weight_b": float(r["blend_weight_b"]),
            }
        )

    rows.sort(key=lambda x: float(x["delta_vs_baseline"]), reverse=True)
    payload = {
        "baseline": baseline,
        "rows": rows,
        "channels": CHANNELS,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Channel Let-Go Scan",
        "",
        "## Baseline",
        f"- test_explained: `{baseline['test_explained']}`",
        f"- blend weights (pruned2, edge15): `({baseline['blend_weight_a']}, {baseline['blend_weight_b']})`",
        "",
        "## Biggest Improvements (set channel -> no_control)",
    ]
    for r in rows[:10]:
        lines.append(
            f"- {r['channel']}: delta `{r['delta_vs_baseline']:+.6f}` -> test `{r['test_explained']:.6f}` (w `{r['blend_weight_a']:.3f}/{r['blend_weight_b']:.3f}`)"
        )
    lines += ["", "## Biggest Drops (set channel -> no_control)"]
    for r in rows[-10:][::-1]:
        lines.append(
            f"- {r['channel']}: delta `{r['delta_vs_baseline']:+.6f}` -> test `{r['test_explained']:.6f}` (w `{r['blend_weight_a']:.3f}/{r['blend_weight_b']:.3f}`)"
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

