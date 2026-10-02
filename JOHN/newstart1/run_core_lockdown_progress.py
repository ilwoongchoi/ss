from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

from fusion_clean import edge_stack_master_step


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
ECON_PATH = Path(r"d:\Users\user\Documents\newstart\data\econ_crypto\econ_crypto_ohlcv_daily_long.csv")
OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\core_lockdown_progress.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\core_lockdown_progress.md")


def load_seis_series() -> np.ndarray:
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
    if var <= 1.0e-12:
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


def load_econ_macro_scalar(n_target: int, train_len: int) -> np.ndarray:
    df = pd.read_csv(ECON_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "ticker", "close"])
    tickers = ["BTC-USD", "SPY", "^VIX", "GC=F", "ETH-USD", "CL=F"]
    use = df[df["ticker"].isin(tickers)].copy()
    pivot = use.pivot_table(index="date", columns="ticker", values="close", aggfunc="last").sort_index()
    ret = np.log(pivot / pivot.shift(1)).replace([np.inf, -np.inf], np.nan)
    z = (ret - ret.mean()) / (ret.std() + 1.0e-12)
    macro = z.mean(axis=1, skipna=True).fillna(0.0).to_numpy(dtype=float)
    if macro.size == 0:
        return np.zeros(n_target, dtype=float)
    src_x = np.linspace(0.0, 1.0, num=macro.size, dtype=float)
    dst_x = np.linspace(0.0, 1.0, num=n_target, dtype=float)
    macro_interp = np.interp(dst_x, src_x, macro)
    mu = float(np.mean(macro_interp[:train_len]))
    sd = float(np.std(macro_interp[:train_len]) + 1.0e-12)
    return (macro_interp - mu) / sd


def build_core_features(states: np.ndarray, macro: np.ndarray) -> np.ndarray:
    n = states.shape[0]
    rows: list[list[float]] = []
    for i in range(n):
        fill = float(i / max(n - 1, 1))
        minute = int((i % 96) * 15)
        hh, mm = minute // 60, minute % 60
        clock = f"{hh:02d}:{mm:02d}"
        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock, edge15_gain=0.0)
        split = step["tunnel_transfer_split"]
        face = step["face_state"] or {}
        rows.append(
            [
                1.0,
                float(step["gate"]),                       # 5/32 gate axis
                float(step["slotting"]),                   # 1.4 - 0.076t axis
                float(step["cancellation"]),               # lensing-PLP macro cancellation
                float(split["transfer_efficiency"]),       # core transfer
                float(split["bm_sm_effective"]),           # BM-SM effective bridge
                float(split["bw_bw_container_reserve"]),   # BW-BW reserve
                float(face.get("is_tunnel", 0.0)),
                float(face.get("window_position", 0.0)),
                float(macro[i]) if i < macro.size else 0.0,  # economy 0-layer forcing
            ]
        )
    return np.asarray(rows, dtype=float)


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    y_raw = load_seis_series()
    split = int(0.7 * (y_raw.size - 1))
    y_mu = float(np.mean(y_raw[: split + 1]))
    y_sd = float(np.std(y_raw[: split + 1]) + 1.0e-12)
    y = (y_raw - y_mu) / y_sd
    states = causal_state_embed(y)
    y_next = y[1:]

    X_state = np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]])
    macro = load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
    X_core = build_core_features(states[:-1], macro)
    X_state_core = np.column_stack([X_state, X_core[:, 1:]])  # remove duplicate bias

    report = {
        "n_points": int(y_next.size),
        "split_index": int(split),
        "models": {
            "state_only": fit_eval(X_state, y_next, split),
            "core_only": fit_eval(X_core, y_next, split),
            "state_plus_core": fit_eval(X_state_core, y_next, split),
        },
    }
    report["delta_state_plus_core_vs_state_test"] = float(
        report["models"]["state_plus_core"]["test_explained"] - report["models"]["state_only"]["test_explained"]
    )

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Core Lockdown Progress",
        "",
        f"- n_points: `{report['n_points']}`",
        f"- split_index: `{report['split_index']}`",
        "",
        f"- state_only test: `{report['models']['state_only']['test_explained']}`",
        f"- core_only test: `{report['models']['core_only']['test_explained']}`",
        f"- state_plus_core test: `{report['models']['state_plus_core']['test_explained']}`",
        f"- delta_state_plus_core_vs_state_test: `{report['delta_state_plus_core_vs_state_test']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

