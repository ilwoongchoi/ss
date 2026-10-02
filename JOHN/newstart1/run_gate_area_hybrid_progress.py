from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from run_seismology_econ_layer0_strict_validation import (
    causal_state_embed,
    explained_fraction,
    fit_eval,
    load_econ_macro_scalar,
    build_edge_features,
    build_layer0_features,
)


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\gate_area_hybrid_progress.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\gate_area_hybrid_progress.md")

GATE_5_32 = 5.0 / 32.0


def load_series() -> np.ndarray:
    vals: list[float] = []
    with SEIS_PATH.open("r", encoding="utf-8", errors="replace", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                vals.append(float(row["k_eff"]))
            except Exception:
                continue
    return np.asarray(vals, dtype=float)


def rolling_hysteresis_area(y: np.ndarray, w: int = 28) -> np.ndarray:
    n = y.size
    out = np.zeros(n, dtype=float)
    x = np.roll(y, 1)
    x[0] = y[0]
    for i in range(n):
        s = max(0, i - w + 1)
        xx = x[s : i + 1]
        yy = y[s : i + 1]
        if xx.size < 3:
            out[i] = 0.0
            continue
        x1 = np.concatenate([xx, xx[:1]])
        y1 = np.concatenate([yy, yy[:1]])
        out[i] = float(0.5 * np.abs(np.sum(x1[:-1] * y1[1:] - y1[:-1] * x1[1:])))
    return out


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    y_raw = load_series()
    split = int(0.7 * (y_raw.size - 1))
    y_mu = float(np.mean(y_raw[: split + 1]))
    y_sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - y_mu) / y_sd
    states = causal_state_embed(y)
    y_next = y[1:]

    # Best baseline branch so far: edge + econ-layer0
    X_edge = build_edge_features(states[:-1])
    macro = load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
    X_l0 = build_layer0_features(states[:-1], macro)
    X_best = np.column_stack([X_edge, X_l0])

    # Gate-area block (strictly normalized by train split)
    area = rolling_hysteresis_area(y, w=28)
    err = np.abs(area - GATE_5_32)
    gap = area - GATE_5_32
    sign = np.sign(gap)
    e_mu = float(np.mean(err[: split + 1]))
    e_sd = float(np.std(err[: split + 1]) + 1.0e-12)
    g_mu = float(np.mean(gap[: split + 1]))
    g_sd = float(np.std(gap[: split + 1]) + 1.0e-12)
    err_n = (err - e_mu) / e_sd
    gap_n = (gap - g_mu) / g_sd
    GA = np.column_stack([err_n[:-1], gap_n[:-1], sign[:-1]])

    # Interaction expansion with state derivatives for stronger dynamical coupling
    d1 = states[:-1, 2]
    d2 = states[:-1, 3]
    GA_int = np.column_stack(
        [
            GA[:, 0] * d1,
            GA[:, 1] * d1,
            GA[:, 0] * d2,
            GA[:, 1] * d2,
            GA[:, 0] * GA[:, 1],
        ]
    )
    X_best_plus_gate = np.column_stack([X_best, GA, GA_int])

    rep_best = fit_eval(X_best, y_next, split)
    rep_plus = fit_eval(X_best_plus_gate, y_next, split)
    rep_state = fit_eval(
        np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]]),
        y_next,
        split,
    )

    report = {
        "gate_5_32": GATE_5_32,
        "n_points": int(y_next.size),
        "split_index": int(split),
        "models": {
            "state_only": rep_state,
            "best_edge_plus_econ": rep_best,
            "best_plus_gate_area_interactions": rep_plus,
        },
        "delta_plus_vs_best_test": float(rep_plus["test_explained"] - rep_best["test_explained"]),
        "delta_plus_vs_state_test": float(rep_plus["test_explained"] - rep_state["test_explained"]),
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Gate-Area Hybrid Progress",
        "",
        f"- gate_5_32: `{report['gate_5_32']}`",
        f"- n_points: `{report['n_points']}`",
        f"- split_index: `{report['split_index']}`",
        "",
        f"- state_only test: `{rep_state['test_explained']}`",
        f"- best_edge_plus_econ test: `{rep_best['test_explained']}`",
        f"- best_plus_gate_area_interactions test: `{rep_plus['test_explained']}`",
        f"- delta_plus_vs_best_test: `{report['delta_plus_vs_best_test']}`",
        f"- delta_plus_vs_state_test: `{report['delta_plus_vs_state_test']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

