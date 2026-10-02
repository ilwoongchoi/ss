from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from run_edge_stack_seismology_validation import build_feature_matrix


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\pelvic_lunar_dynamics_check.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\pelvic_lunar_dynamics_check.md")


def load_series() -> np.ndarray:
    values: list[float] = []
    with SEIS_PATH.open("r", encoding="utf-8", errors="replace", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                values.append(float(row["k_eff"]))
            except Exception:
                continue
    x = np.asarray(values, dtype=float)
    return x


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


def sigmoid(x: float) -> float:
    return float(1.0 / (1.0 + np.exp(-x)))


def build_pelvic_lunar_features(n: int) -> np.ndarray:
    """
    Reduced dynamics (engineering form):
      dG/dt = a*sigmoid(alpha*M + beta*L - gamma*C) - b*G
      dC/dt = eta*tanh(k*(G-theta)) - lambda*C
      dM/dt = 2*pi/28
      dL/dt = 2*pi/29.53
    """
    dt = 1.0
    a, b = 1.2, 0.9
    alpha, beta, gamma = 1.0, 0.8, 1.1
    eta, lam, kappa, theta = 0.7, 0.35, 3.0, 0.45
    wm = 2.0 * np.pi / 28.0
    wl = 2.0 * np.pi / 29.53

    G = 0.30
    C = 0.25
    pm = 0.0
    pl = np.pi / 7.0
    rows: list[list[float]] = []
    for _ in range(n):
        M = np.sin(pm)
        L = np.sin(pl)
        dG = a * sigmoid(alpha * M + beta * L - gamma * C) - b * G
        dC = eta * np.tanh(kappa * (G - theta)) - lam * C
        G = G + dt * dG
        C = C + dt * dC
        pm = pm + dt * wm
        pl = pl + dt * wl
        rows.append([1.0, G, C, np.sin(pm), np.cos(pm), np.sin(pl), np.cos(pl), dG, dC])
    return np.asarray(rows, dtype=float)


def matrix_diagnostics(X: np.ndarray) -> dict[str, float]:
    u, s, vt = np.linalg.svd(X, full_matrices=False)
    rank = int(np.linalg.matrix_rank(X))
    cond = float((s[0] / s[-1]) if s[-1] > 1e-12 else np.inf)
    return {"rank": rank, "condition_number": cond}


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    y_raw = load_series()
    split = int(0.7 * (y_raw.size - 1))
    mu = float(np.mean(y_raw[: split + 1]))
    sd = float(np.std(y_raw[: split + 1]) + 1e-12)
    y = (y_raw - mu) / sd
    states = causal_state_embed(y)
    y_next = y[1:]

    X_state = np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]])
    X_high, _ = build_feature_matrix(states[:-1])
    X_reduced = build_pelvic_lunar_features(states.shape[0] - 1)

    report = {
        "n_points": int(y_next.size),
        "split_index": int(split),
        "diagnostics": {
            "high_dim": matrix_diagnostics(X_high),
            "reduced": matrix_diagnostics(X_reduced),
        },
        "models": {
            "state_only": fit_eval(X_state, y_next, split),
            "high_dim_edge": fit_eval(X_high, y_next, split),
            "reduced_pelvic_lunar": fit_eval(X_reduced, y_next, split),
        },
    }
    report["delta_reduced_vs_high_dim_test"] = float(
        report["models"]["reduced_pelvic_lunar"]["test_explained"]
        - report["models"]["high_dim_edge"]["test_explained"]
    )

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Pelvic-Lunar Dynamics Check",
        "",
        f"- n_points: `{report['n_points']}`",
        f"- split_index: `{report['split_index']}`",
        "",
        "## Matrix Diagnostics",
        f"- high_dim rank/cond: `{report['diagnostics']['high_dim']}`",
        f"- reduced rank/cond: `{report['diagnostics']['reduced']}`",
        "",
        "## Models",
        f"- state_only test: `{report['models']['state_only']['test_explained']}`",
        f"- high_dim_edge test: `{report['models']['high_dim_edge']['test_explained']}`",
        f"- reduced_pelvic_lunar test: `{report['models']['reduced_pelvic_lunar']['test_explained']}`",
        f"- delta_reduced_vs_high_dim_test: `{report['delta_reduced_vs_high_dim_test']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

