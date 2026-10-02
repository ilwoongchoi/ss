from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\gate_area_impact_test.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\gate_area_impact_test.md")

GATE_5_32 = 5.0 / 32.0  # 0.15625


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


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1e-12:
        return 0.0
    e = y - y_hat
    return float(1.0 - np.mean(e * e) / var)


def fit_eval(X: np.ndarray, y: np.ndarray, split: int) -> dict[str, float]:
    coef, *_ = np.linalg.lstsq(X[:split], y[:split], rcond=None)
    tr = X[:split] @ coef
    te = X[split:] @ coef
    return {
        "feature_count": int(X.shape[1]),
        "train_explained": explained_fraction(y[:split], tr),
        "test_explained": explained_fraction(y[split:], te),
        "train_rmse": float(np.sqrt(np.mean((y[:split] - tr) ** 2))),
        "test_rmse": float(np.sqrt(np.mean((y[split:] - te) ** 2))),
    }


def rolling_hysteresis_area(y: np.ndarray, w: int = 28) -> np.ndarray:
    """
    Proxy loop area from (y_t, y_{t-1}) phase portrait over rolling window.
    """
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
        # polygon area (shoelace)
        x1 = np.concatenate([xx, xx[:1]])
        y1 = np.concatenate([yy, yy[:1]])
        area = 0.5 * np.abs(np.sum(x1[:-1] * y1[1:] - y1[:-1] * x1[1:]))
        out[i] = float(area)
    return out


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    y_raw = load_series()
    split = int(0.7 * (y_raw.size - 1))
    mu = float(np.mean(y_raw[: split + 1]))
    sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - mu) / sd
    states = causal_state_embed(y)
    y_next = y[1:]

    X_state = np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]])

    area = rolling_hysteresis_area(y, w=28)
    area_err = np.abs(area - GATE_5_32)
    area_gap = area - GATE_5_32
    area_sign = np.sign(area_gap)
    # strict normalization by train window
    e_mu = float(np.mean(area_err[: split + 1]))
    e_sd = float(np.std(area_err[: split + 1]) + 1.0e-12)
    g_mu = float(np.mean(area_gap[: split + 1]))
    g_sd = float(np.std(area_gap[: split + 1]) + 1.0e-12)
    err_n = (area_err - e_mu) / e_sd
    gap_n = (area_gap - g_mu) / g_sd

    X_gate_area = np.column_stack([X_state, err_n[:-1], gap_n[:-1], area_sign[:-1]])

    report = {
        "gate_5_32": GATE_5_32,
        "n_points": int(y_next.size),
        "split_index": int(split),
        "models": {
            "state_only": fit_eval(X_state, y_next, split),
            "state_plus_gate_area": fit_eval(X_gate_area, y_next, split),
        },
    }
    report["delta_test"] = float(
        report["models"]["state_plus_gate_area"]["test_explained"]
        - report["models"]["state_only"]["test_explained"]
    )

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Gate-Area Impact Test",
        "",
        f"- gate_5_32: `{report['gate_5_32']}`",
        f"- n_points: `{report['n_points']}`",
        f"- split_index: `{report['split_index']}`",
        "",
        f"- state_only test: `{report['models']['state_only']['test_explained']}`",
        f"- state_plus_gate_area test: `{report['models']['state_plus_gate_area']['test_explained']}`",
        f"- delta_test: `{report['delta_test']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

