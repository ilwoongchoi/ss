from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import numpy as np

from fusion_clean import MinimalPhysicalParams, physical_minimal_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_JSON = ROOT / "analysis_results" / "physical_minimal_param_search.json"
OUT_MD = ROOT / "analysis_results" / "physical_minimal_param_search.md"


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


def zscore(x: np.ndarray) -> np.ndarray:
    return (x - np.mean(x)) / (np.std(x) + 1.0e-12)


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


def rmse_for_slice(
    states: np.ndarray,
    clocks: list[str],
    p: MinimalPhysicalParams,
    i0: int,
    i1: int,
) -> float:
    err2 = 0.0
    n = 0
    end = min(i1, states.shape[0] - 1)
    for i in range(i0, end):
        fill = float(i / max(states.shape[0] - 2, 1))
        clock = clocks[i] if i < len(clocks) else "00:00"
        out = physical_minimal_step(states[i], phase_fill=fill, clock_hhmm=clock, params=p)
        pred = np.asarray(out["state_out"], dtype=float)
        tgt = states[i + 1]
        d = pred - tgt
        err2 += float(np.dot(d, d))
        n += 4
    return float(np.sqrt(err2 / max(n, 1)))


def sample_params(rng: np.random.Generator, base: MinimalPhysicalParams, scale: float) -> MinimalPhysicalParams:
    b = np.array(
        [
            base.a_core,
            base.a_edge,
            base.a_cross,
            base.a_cancel,
            base.a_void,
            base.a_tunnel,
            base.a_capture,
            base.a_escape,
        ],
        dtype=float,
    )
    noise = rng.normal(0.0, scale, size=8)
    v = b + noise
    # Keep tunnel/capture/escape in a compact stable range.
    v[5:] = np.clip(v[5:], -1.0, 1.0)
    return MinimalPhysicalParams(
        a_core=float(v[0]),
        a_edge=float(v[1]),
        a_cross=float(v[2]),
        a_cancel=float(v[3]),
        a_void=float(v[4]),
        a_tunnel=float(v[5]),
        a_capture=float(v[6]),
        a_escape=float(v[7]),
    )


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    path = ROOT / "earthquake_1995-2023.csv"
    mags, clocks = load_catalog_csv(path)
    y = zscore(mags)
    states = state_embed(y)

    n_steps = states.shape[0] - 1
    split = int(0.7 * n_steps)

    p_best = MinimalPhysicalParams()
    best_train = rmse_for_slice(states, clocks, p_best, 0, split)

    rng = np.random.default_rng(42)
    scales = [0.25, 0.10, 0.05, 0.02]
    trials_per_scale = [140, 140, 140, 140]

    for scale, n_trial in zip(scales, trials_per_scale):
        for _ in range(n_trial):
            cand = sample_params(rng, p_best, scale)
            train_rmse = rmse_for_slice(states, clocks, cand, 0, split)
            if train_rmse < best_train:
                best_train = train_rmse
                p_best = cand

    train_rmse = rmse_for_slice(states, clocks, p_best, 0, split)
    test_rmse = rmse_for_slice(states, clocks, p_best, split, n_steps)

    out = {
        "dataset": path.name,
        "n_events": int(mags.size),
        "n_steps": int(n_steps),
        "split_index": int(split),
        "baseline_params": asdict(MinimalPhysicalParams()),
        "baseline_train_rmse": rmse_for_slice(states, clocks, MinimalPhysicalParams(), 0, split),
        "baseline_test_rmse": rmse_for_slice(states, clocks, MinimalPhysicalParams(), split, n_steps),
        "best_params": asdict(p_best),
        "best_train_rmse": train_rmse,
        "best_test_rmse": test_rmse,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Physical Minimal Parameter Search",
        "",
        f"- dataset: `{out['dataset']}`",
        f"- n_events: `{out['n_events']}`",
        f"- n_steps: `{out['n_steps']}`",
        f"- split_index: `{out['split_index']}`",
        "",
        "## RMSE",
        f"- baseline_train_rmse: `{out['baseline_train_rmse']}`",
        f"- baseline_test_rmse: `{out['baseline_test_rmse']}`",
        f"- best_train_rmse: `{out['best_train_rmse']}`",
        f"- best_test_rmse: `{out['best_test_rmse']}`",
        "",
        "## Best Params",
        f"- `{out['best_params']}`",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
