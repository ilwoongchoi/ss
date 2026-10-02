from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np

from fusion_clean import edge_stack_master_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_JSON = ROOT / "analysis_results" / "seismology_raw_catalog_validation.json"
OUT_MD = ROOT / "analysis_results" / "seismology_raw_catalog_validation.md"


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


def parse_dt_csv(s: str) -> datetime:
    return datetime.strptime(s, "%d-%m-%Y %H:%M")


def load_catalog_csv(path: Path) -> tuple[np.ndarray, list[str]]:
    rows: list[tuple[datetime, float]] = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                mag = float(row["magnitude"])
                dt = parse_dt_csv(str(row["date_time"]))
            except Exception:
                continue
            rows.append((dt, mag))
    rows.sort(key=lambda x: x[0])
    mags = np.asarray([m for _, m in rows], dtype=float)
    clocks = [dt.strftime("%H:%M") for dt, _ in rows]
    return mags, clocks


def load_geojson_usgs(path: Path) -> tuple[np.ndarray, list[str]]:
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    feats = data.get("features", [])
    rows: list[tuple[datetime, float]] = []
    for feat in feats:
        p = feat.get("properties", {})
        try:
            mag = float(p["mag"])
            t_ms = int(p["time"])
            dt = datetime.fromtimestamp(t_ms / 1000.0, tz=timezone.utc)
        except Exception:
            continue
        rows.append((dt, mag))
    rows.sort(key=lambda x: x[0])
    mags = np.asarray([m for _, m in rows], dtype=float)
    clocks = [dt.strftime("%H:%M") for dt, _ in rows]
    return mags, clocks


def zscore(x: np.ndarray) -> np.ndarray:
    return (x - np.mean(x)) / (np.std(x) + 1.0e-12)


def build_edge_features(states: np.ndarray, clocks: Iterable[str]) -> np.ndarray:
    rows: list[list[float]] = []
    n = states.shape[0]
    clock_list = list(clocks)
    for i in range(n):
        fill = float(i / max(n - 1, 1))
        clock = clock_list[i] if i < len(clock_list) else "00:00"
        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock)
        face = step["face_state"] or {}
        split = step["tunnel_transfer_split"]
        row = [
            1.0,
            float(step["gate"]),
            float(step["slotting"]),
            float(step["forward_phase"]),
            float(step["reverse_phase"]),
            float(step["net_phase"]),
            float(step["cancellation"]),
            float(face.get("is_tunnel", 0.0)),
            float(face.get("window_position", 0.0)),
            float(face.get("female_container_activity", 0.0)),
            float(face.get("male_capture_activity", 1.0)),
            float(split["transfer_efficiency"]),
            float(split["bm_sm_effective"]),
            float(split["bw_bw_container_reserve"]),
            *np.asarray(step["mandelbrot_core"], dtype=float).tolist(),
            *np.asarray(step["edge_total"], dtype=float).tolist(),
            *np.asarray(step["interaction_total"], dtype=float).tolist(),
            *np.asarray(step["cancel_pair"], dtype=float).tolist(),
            *np.asarray(step["bw_bw_void"], dtype=float).tolist(),
            *np.asarray(step["patch_total"], dtype=float).tolist(),
            *np.asarray(step["particle_9_13_total"], dtype=float).tolist(),
            float(step["quark_9"]),
            float(step["gluon_10"]),
            float(step["muon_11"]),
            float(step["tau_12"]),
            float(step["higgs_13"]),
            *np.asarray(step["gated_branch"], dtype=float).tolist(),
        ]
        rows.append(row)
    return np.asarray(rows, dtype=float)


def build_edge_best_pruned_features(states: np.ndarray, clocks: Iterable[str]) -> np.ndarray:
    # Ablation-selected best subset on raw catalogs:
    # keep only Mandelbrot core + edge_total (+ bias).
    rows: list[list[float]] = []
    n = states.shape[0]
    clock_list = list(clocks)
    for i in range(n):
        fill = float(i / max(n - 1, 1))
        clock = clock_list[i] if i < len(clock_list) else "00:00"
        step = edge_stack_master_step(states[i], phase_fill=fill, clock_hhmm=clock)
        row = [
            1.0,
            *np.asarray(step["mandelbrot_core"], dtype=float).tolist(),
            *np.asarray(step["edge_total"], dtype=float).tolist(),
        ]
        rows.append(row)
    return np.asarray(rows, dtype=float)


def eval_dataset(name: str, mags: np.ndarray, clocks: list[str]) -> dict[str, object]:
    if mags.size < 200:
        return {"name": name, "n_events": int(mags.size), "skipped": True, "reason": "too_few_events"}
    y = zscore(mags)
    states = state_embed(y)
    y_next = y[1:]
    split = int(0.7 * y_next.size)
    X_state = np.column_stack([np.ones(states.shape[0] - 1, dtype=float), states[:-1]])
    X_edge = build_edge_features(states[:-1], clocks[:-1])
    X_edge_best = build_edge_best_pruned_features(states[:-1], clocks[:-1])
    return {
        "name": name,
        "n_events": int(mags.size),
        "skipped": False,
        "split_index": int(split),
        "state_only": fit_eval(X_state, y_next, split),
        "edge_full": fit_eval(X_edge, y_next, split),
        "edge_best_pruned": fit_eval(X_edge_best, y_next, split),
    }


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    datasets: list[dict[str, object]] = []

    csv1 = ROOT / "earthquake_1995-2023.csv"
    if csv1.exists():
        mags, clocks = load_catalog_csv(csv1)
        datasets.append(eval_dataset(csv1.name, mags, clocks))

    csv2 = ROOT / "earthquake_data.csv"
    if csv2.exists():
        mags, clocks = load_catalog_csv(csv2)
        datasets.append(eval_dataset(csv2.name, mags, clocks))

    gj = ROOT / "usgs_events_2026-02-01_2026-03-01_ca_bbox.geojson"
    if gj.exists():
        mags, clocks = load_geojson_usgs(gj)
        datasets.append(eval_dataset(gj.name, mags, clocks))

    report = {"datasets": datasets}
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Seismology Raw Catalog Validation", ""]
    for d in datasets:
        lines.append(f"## {d['name']}")
        lines.append("")
        lines.append(f"- n_events: `{d['n_events']}`")
        if d.get("skipped"):
            lines.append(f"- skipped: `{d['reason']}`")
            lines.append("")
            continue
        lines.append(f"- split_index: `{d['split_index']}`")
        s = d["state_only"]
        e = d["edge_full"]
        lines.append(
            f"- state_only: features=`{s['feature_count']}`, train=`{s['train_explained']}`, test=`{s['test_explained']}`, "
            f"train_rmse=`{s['train_rmse']}`, test_rmse=`{s['test_rmse']}`"
        )
        lines.append(
            f"- edge_full: features=`{e['feature_count']}`, train=`{e['train_explained']}`, test=`{e['test_explained']}`, "
            f"train_rmse=`{e['train_rmse']}`, test_rmse=`{e['test_rmse']}`"
        )
        b = d["edge_best_pruned"]
        lines.append(
            f"- edge_best_pruned: features=`{b['feature_count']}`, train=`{b['train_explained']}`, test=`{b['test_explained']}`, "
            f"train_rmse=`{b['train_rmse']}`, test_rmse=`{b['test_rmse']}`"
        )
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
