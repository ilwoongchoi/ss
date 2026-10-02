from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from fusion_clean import edge_stack_master_step


SEIS_PATH = Path(
    r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv"
)
OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\seismology_ablation.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\seismology_ablation.md")


def load_series() -> np.ndarray:
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


def moving_average(x: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return x.copy()
    kernel = np.ones(window, dtype=float) / float(window)
    return np.convolve(x, kernel, mode="same")


def state_embed(x: np.ndarray) -> np.ndarray:
    ma = moving_average(x, 15)
    d1 = np.gradient(x)
    d2 = np.gradient(d1)
    states = np.column_stack([x, ma, d1, d2]).astype(float)
    norms = np.std(states, axis=0) + 1.0e-12
    return states / norms


def explained_fraction(y: np.ndarray, y_hat: np.ndarray) -> float:
    var = float(np.var(y))
    if var <= 1.0e-12:
        return 0.0
    err = y - y_hat
    return float(1.0 - (np.mean(err * err) / var))


def fit_eval(X: np.ndarray, y: np.ndarray, split: int) -> dict[str, float]:
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    coeffs, *_ = np.linalg.lstsq(X_train, y_train, rcond=None)
    hat_train = X_train @ coeffs
    hat_test = X_test @ coeffs
    return {
        "feature_count": int(X.shape[1]),
        "train_explained": explained_fraction(y_train, hat_train),
        "test_explained": explained_fraction(y_test, hat_test),
        "train_rmse": float(np.sqrt(np.mean((y_train - hat_train) ** 2))),
        "test_rmse": float(np.sqrt(np.mean((y_test - hat_test) ** 2))),
    }


def clock_for_index(i: int) -> str:
    minute = int((i % 96) * 15)
    return f"{minute // 60:02d}:{minute % 60:02d}"


def build_features(states: np.ndarray, mode: str) -> np.ndarray:
    rows: list[list[float]] = []
    n = states.shape[0]
    for i in range(n):
        fill = float(i / max(n - 1, 1))
        clock = clock_for_index(i)
        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock)
        face = step["face_state"] or {}
        split = step["tunnel_transfer_split"]
        base = [
            1.0,
            float(step["gate"]),
            float(step["slotting"]),
            float(step["forward_phase"]),
            float(step["reverse_phase"]),
            float(step["net_phase"]),
            float(step["cancellation"]),
            *np.asarray(step["mandelbrot_core"], dtype=float).tolist(),
            *np.asarray(step["edge_total"], dtype=float).tolist(),
            *np.asarray(step["cancel_pair"], dtype=float).tolist(),
            *np.asarray(step["bw_bw_void"], dtype=float).tolist(),
            *np.asarray(step["gated_branch"], dtype=float).tolist(),
        ]
        if mode == "edge_core":
            rows.append(base)
            continue
        if mode == "edge_face":
            rows.append(
                base
                + [
                    float(face.get("is_tunnel", 0.0)),
                    float(face.get("window_position", 0.0)),
                    float(face.get("female_container_activity", 0.0)),
                    float(face.get("male_capture_activity", 1.0)),
                ]
            )
            continue
        if mode == "edge_face_transfer":
            rows.append(
                base
                + [
                    float(face.get("is_tunnel", 0.0)),
                    float(face.get("window_position", 0.0)),
                    float(face.get("female_container_activity", 0.0)),
                    float(face.get("male_capture_activity", 1.0)),
                    float(split["transfer_efficiency"]),
                    float(split["bm_sm_effective"]),
                    float(split["bw_bw_container_reserve"]),
                ]
            )
            continue
        raise ValueError(f"unknown mode: {mode}")
    return np.asarray(rows, dtype=float)


def main() -> int:
    y = load_series()
    states = state_embed(y)
    y_next = y[1:]
    split = int(0.7 * y_next.size)

    X_state = np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]])
    X_core = build_features(states[:-1], "edge_core")
    X_face = build_features(states[:-1], "edge_face")
    X_transfer = build_features(states[:-1], "edge_face_transfer")

    report = {
        "domain": "seismology_daily_k_eff",
        "n_points": int(y_next.size),
        "split_index": int(split),
        "models": {
            "state_only": fit_eval(X_state, y_next, split),
            "edge_core": fit_eval(X_core, y_next, split),
            "edge_face": fit_eval(X_face, y_next, split),
            "edge_face_transfer": fit_eval(X_transfer, y_next, split),
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        "# Seismology Ablation",
        "",
        f"- n_points: `{report['n_points']}`",
        f"- split_index: `{report['split_index']}`",
        "",
        "## Models",
        "",
    ]
    for name, r in report["models"].items():
        lines.append(
            f"- `{name}`: features=`{r['feature_count']}`, "
            f"train_explained=`{r['train_explained']}`, test_explained=`{r['test_explained']}`, "
            f"train_rmse=`{r['train_rmse']}`, test_rmse=`{r['test_rmse']}`"
        )
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

