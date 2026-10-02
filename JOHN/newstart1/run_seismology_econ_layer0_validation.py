from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

from fusion_clean import edge_stack_master_step
from geometry_package.layer_extension_equation import run_layered_step
from run_edge_stack_seismology_validation import build_feature_matrix, explained_fraction, state_embed

SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
ECON_PATH = Path(r"d:\Users\user\Documents\newstart\data\econ_crypto\econ_crypto_ohlcv_daily_long.csv")
OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\seismology_econ_layer0_validation.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\seismology_econ_layer0_validation.md")


def load_seis_series() -> np.ndarray:
    values: list[float] = []
    with SEIS_PATH.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                values.append(float(row["k_eff"]))
            except (TypeError, ValueError):
                continue
    x = np.asarray(values, dtype=float)
    return (x - np.mean(x)) / (np.std(x) + 1.0e-12)


def load_econ_macro_scalar(n_target: int) -> np.ndarray:
    df = pd.read_csv(ECON_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "ticker", "close"])

    tickers = ["BTC-USD", "SPY", "^VIX", "GC=F", "ETH-USD", "CL=F"]
    use = df[df["ticker"].isin(tickers)].copy()
    pivot = use.pivot_table(index="date", columns="ticker", values="close", aggfunc="last").sort_index()
    ret = np.log(pivot / pivot.shift(1)).replace([np.inf, -np.inf], np.nan)

    # Robust composite macro scalar: mean z-score across available ticker returns per day.
    z = (ret - ret.mean()) / (ret.std() + 1.0e-12)
    macro = z.mean(axis=1, skipna=True).fillna(0.0).to_numpy(dtype=float)
    macro = (macro - np.mean(macro)) / (np.std(macro) + 1.0e-12)

    if macro.size == 0:
        return np.zeros(n_target, dtype=float)

    src_x = np.linspace(0.0, 1.0, num=macro.size, dtype=float)
    dst_x = np.linspace(0.0, 1.0, num=n_target, dtype=float)
    return np.interp(dst_x, src_x, macro)


def fit_eval(X: np.ndarray, y: np.ndarray, split: int) -> dict[str, float]:
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    coeffs, *_ = np.linalg.lstsq(X_train, y_train, rcond=None)
    yhat_train = X_train @ coeffs
    yhat_test = X_test @ coeffs
    return {
        "feature_count": int(X.shape[1]),
        "train_explained": float(explained_fraction(y_train, yhat_train)),
        "test_explained": float(explained_fraction(y_test, yhat_test)),
        "train_rmse": float(np.sqrt(np.mean((y_train - yhat_train) ** 2))),
        "test_rmse": float(np.sqrt(np.mean((y_test - yhat_test) ** 2))),
    }


def build_layer0_features(states: np.ndarray, macro: np.ndarray) -> np.ndarray:
    n = states.shape[0]
    rows: list[list[float]] = []

    u0_prev = np.asarray(states[0], dtype=float)
    us_prev = np.asarray(states[0], dtype=float)

    for i in range(n):
        fill = float(i / max(n - 1, 1))
        minute = int((i % 96) * 15)
        hh, mm = minute // 60, minute % 60
        clock = f"{hh:02d}:{mm:02d}"

        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock)
        split = step["tunnel_transfer_split"]
        resonance = float(split["bm_sm_effective"] - split["bw_bw_container_reserve"])

        lay = run_layered_step(
            states[i],
            u0_prev,
            us_prev,
            macro_scalar=float(macro[i]),
            resonance_scalar=resonance,
            phase_fill=fill,
        )
        u0_next = np.asarray(lay["u0_next"], dtype=float)
        us_next = np.asarray(lay["u_self_next"], dtype=float)

        rows.append([
            float(macro[i]),
            resonance,
            *u0_next.tolist(),
            *us_next.tolist(),
        ])

        u0_prev = u0_next
        us_prev = us_next

    return np.asarray(rows, dtype=float)


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    y = load_seis_series()
    states = state_embed(y)
    y_next = y[1:]
    split = int(0.7 * y_next.size)

    # Baselines
    X_state = np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]])
    X_edge, edge_names = build_feature_matrix(states[:-1])

    # 0-scale economy coupling features
    macro = load_econ_macro_scalar(states.shape[0] - 1)
    X_l0 = build_layer0_features(states[:-1], macro)

    X_edge_l0 = np.column_stack([X_edge, X_l0])

    report = {
        "domain": "seismology_daily_k_eff",
        "seis_path": str(SEIS_PATH),
        "econ_path": str(ECON_PATH),
        "n_points": int(y_next.size),
        "split_index": int(split),
        "models": {
            "state_only": fit_eval(X_state, y_next, split),
            "edge_full": fit_eval(X_edge, y_next, split),
            "edge_plus_econ_layer0": fit_eval(X_edge_l0, y_next, split),
        },
        "edge_feature_count": int(X_edge.shape[1]),
        "layer0_feature_count": int(X_l0.shape[1]),
        "edge_feature_names": edge_names,
        "layer0_feature_names": [
            "macro_scalar",
            "resonance_scalar",
            "u0_next_0", "u0_next_1", "u0_next_2", "u0_next_3",
            "u_self_next_0", "u_self_next_1", "u_self_next_2", "u_self_next_3",
        ],
    }

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    m = report["models"]
    lines = [
        "# Seismology + Economy Layer0 Validation",
        "",
        f"- seis_path: `{report['seis_path']}`",
        f"- econ_path: `{report['econ_path']}`",
        f"- n_points: `{report['n_points']}`",
        f"- split_index: `{report['split_index']}`",
        f"- edge_feature_count: `{report['edge_feature_count']}`",
        f"- layer0_feature_count: `{report['layer0_feature_count']}`",
        "",
        "## Models",
        f"- state_only: features=`{m['state_only']['feature_count']}`, train=`{m['state_only']['train_explained']}`, test=`{m['state_only']['test_explained']}`, test_rmse=`{m['state_only']['test_rmse']}`",
        f"- edge_full: features=`{m['edge_full']['feature_count']}`, train=`{m['edge_full']['train_explained']}`, test=`{m['edge_full']['test_explained']}`, test_rmse=`{m['edge_full']['test_rmse']}`",
        f"- edge_plus_econ_layer0: features=`{m['edge_plus_econ_layer0']['feature_count']}`, train=`{m['edge_plus_econ_layer0']['train_explained']}`, test=`{m['edge_plus_econ_layer0']['test_explained']}`, test_rmse=`{m['edge_plus_econ_layer0']['test_rmse']}`",
        "",
        f"- delta_vs_state_only_test: `{m['edge_plus_econ_layer0']['test_explained'] - m['state_only']['test_explained']}`",
        f"- delta_vs_edge_full_test: `{m['edge_plus_econ_layer0']['test_explained'] - m['edge_full']['test_explained']}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"state_only_test={m['state_only']['test_explained']}")
    print(f"edge_full_test={m['edge_full']['test_explained']}")
    print(f"edge_plus_econ_layer0_test={m['edge_plus_econ_layer0']['test_explained']}")
    print(f"json={OUT_JSON}")
    print(f"md={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
