from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from fusion_clean import edge_stack_master_step


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\control_injection_progress.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\control_injection_progress.md")


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


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1.0e-12:
        return 0.0
    e = y - y_hat
    return float(1.0 - np.mean(e * e) / var)


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
        ma[i] = csum / float(min(i + 1, window))
        if i > 0:
            d1[i] = y_norm[i] - y_norm[i - 1]
        if i > 1:
            d2[i] = d1[i] - d1[i - 1]
    return np.column_stack([y_norm, ma, d1, d2]).astype(float)


def build_control_signal(states: np.ndarray) -> np.ndarray:
    n = states.shape[0]
    u = np.zeros(n, dtype=float)
    for i in range(n):
        fill = float(i / max(n - 1, 1))
        minute = int((i % 96) * 15)
        hh, mm = minute // 60, minute % 60
        clock = f"{hh:02d}:{mm:02d}"
        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock, edge15_gain=0.0)
        split = step["tunnel_transfer_split"]
        # Deterministic core-control composition (no fitting):
        # gate and 5/32-like transfer asymmetry drive correction; cancellation damps.
        transfer = float(split["bm_sm_effective"] - split["bw_bw_container_reserve"])
        u[i] = (
            0.15625 * float(step["gate"])
            + 0.03125 * transfer
            - 0.03125 * float(step["cancellation"])
            + 0.015625 * float(split["transfer_efficiency"])
        )
    return u


def recursive_forecast(y: np.ndarray, u: np.ndarray, split: int) -> tuple[np.ndarray, np.ndarray]:
    """
    No fitted coefficients.
    Baseline: y_{t+1}=rho*y_t
    Control:  y_{t+1}=rho*y_t + k_u*u_t + k_r*(0-y_t)
    """
    rho = 31.0 / 32.0      # 0.96875
    k_u = 1.0 / 16.0       # 0.0625
    k_r = 1.0 / 32.0       # 0.03125

    n = y.size - 1
    yhat_base = np.zeros(n, dtype=float)
    yhat_ctrl = np.zeros(n, dtype=float)

    # warm start from true value at split boundary (causal)
    y_prev_base = float(y[split])
    y_prev_ctrl = float(y[split])

    for t in range(split, n):
        y_next_base = rho * y_prev_base
        y_next_ctrl = rho * y_prev_ctrl + (k_u * float(u[t])) + (k_r * (0.0 - y_prev_ctrl))
        yhat_base[t] = y_next_base
        yhat_ctrl[t] = y_next_ctrl
        y_prev_base = y_next_base
        y_prev_ctrl = y_next_ctrl

    return yhat_base, yhat_ctrl


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    y_raw = load_series()
    split = int(0.7 * (y_raw.size - 1))
    mu = float(np.mean(y_raw[: split + 1]))
    sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - mu) / sd
    states = causal_state_embed(y)
    u = build_control_signal(states[:-1])

    y_true = y[1:]
    yhat_base, yhat_ctrl = recursive_forecast(y, u, split)

    # evaluate on strict test block only
    yt = y_true[split:]
    yb = yhat_base[split:]
    yc = yhat_ctrl[split:]
    rep = {
        "baseline_recursive_test_explained": explained_fraction(yt, yb),
        "control_recursive_test_explained": explained_fraction(yt, yc),
        "baseline_recursive_test_rmse": float(np.sqrt(np.mean((yt - yb) ** 2))),
        "control_recursive_test_rmse": float(np.sqrt(np.mean((yt - yc) ** 2))),
    }
    rep["delta_test"] = float(rep["control_recursive_test_explained"] - rep["baseline_recursive_test_explained"])

    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Control Injection Progress",
        "",
        f"- baseline_recursive_test_explained: `{rep['baseline_recursive_test_explained']}`",
        f"- control_recursive_test_explained: `{rep['control_recursive_test_explained']}`",
        f"- baseline_recursive_test_rmse: `{rep['baseline_recursive_test_rmse']}`",
        f"- control_recursive_test_rmse: `{rep['control_recursive_test_rmse']}`",
        f"- delta_test: `{rep['delta_test']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

