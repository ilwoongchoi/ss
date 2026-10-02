from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
ECON_PATH = Path(r"d:\Users\user\Documents\newstart\data\econ_crypto\econ_crypto_ohlcv_daily_long.csv")
OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\pelvic_lunar_hybrid_validation.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\pelvic_lunar_hybrid_validation.md")


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


def sigmoid(x: float) -> float:
    return float(1.0 / (1.0 + np.exp(-x)))


def build_reduced_features(n: int, econ_macro: np.ndarray) -> np.ndarray:
    # Reduced latent dynamics with economic forcing.
    dt = 1.0
    a, b = 1.1, 0.95
    alpha, beta, gamma, delta = 0.9, 0.8, 1.1, 0.4
    eta, lam, kappa, theta = 0.65, 0.30, 2.7, 0.42
    wm = 2.0 * np.pi / 28.0
    wl = 2.0 * np.pi / 29.53

    G, C = 0.32, 0.24
    pm, pl = 0.0, np.pi / 6.0
    rows: list[list[float]] = []
    for i in range(n):
        M = np.sin(pm)
        L = np.sin(pl)
        E = float(econ_macro[i]) if i < econ_macro.size else 0.0
        drive = alpha * M + beta * L - gamma * C + delta * E
        dG = a * sigmoid(drive) - b * G
        dC = eta * np.tanh(kappa * (G - theta)) - lam * C
        G += dt * dG
        C += dt * dC
        pm += dt * wm
        pl += dt * wl
        rows.append([1.0, G, C, M, L, E, dG, dC, np.sin(pm), np.cos(pm), np.sin(pl), np.cos(pl)])
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
    econ_macro = load_econ_macro_scalar(states.shape[0] - 1, train_len=split)
    X_reduced = build_reduced_features(states.shape[0] - 1, econ_macro)
    X_hybrid = np.column_stack([X_state, X_reduced[:, 1:]])  # avoid duplicate bias

    report = {
        "n_points": int(y_next.size),
        "split_index": int(split),
        "models": {
            "state_only": fit_eval(X_state, y_next, split),
            "reduced_only": fit_eval(X_reduced, y_next, split),
            "hybrid_state_plus_reduced": fit_eval(X_hybrid, y_next, split),
        },
    }
    report["delta_hybrid_vs_state_test"] = float(
        report["models"]["hybrid_state_plus_reduced"]["test_explained"]
        - report["models"]["state_only"]["test_explained"]
    )

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Pelvic-Lunar Hybrid Validation",
        "",
        f"- n_points: `{report['n_points']}`",
        f"- split_index: `{report['split_index']}`",
        "",
        f"- state_only test: `{report['models']['state_only']['test_explained']}`",
        f"- reduced_only test: `{report['models']['reduced_only']['test_explained']}`",
        f"- hybrid_state_plus_reduced test: `{report['models']['hybrid_state_plus_reduced']['test_explained']}`",
        f"- delta_hybrid_vs_state_test: `{report['delta_hybrid_vs_state_test']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

