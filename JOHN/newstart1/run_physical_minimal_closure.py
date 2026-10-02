from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from fusion_clean import physical_minimal_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_JSON = ROOT / "analysis_results" / "physical_minimal_closure.json"
OUT_MD = ROOT / "analysis_results" / "physical_minimal_closure.md"


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


def eval_closure(name: str, mags: np.ndarray, clocks: list[str]) -> dict[str, object]:
    if mags.size < 50:
        return {"name": name, "n_events": int(mags.size), "skipped": True, "reason": "too_few_events"}
    y = zscore(mags)
    states = state_embed(y)
    n = states.shape[0] - 1
    pred = np.zeros((n, 4), dtype=float)
    truth = states[1:]
    tunnel_count = 0

    for i in range(n):
        fill = float(i / max(n - 1, 1))
        clock = clocks[i] if i < len(clocks) else "00:00"
        step = physical_minimal_step(states[i], phase_fill=fill, clock_hhmm=clock)
        pred[i] = np.asarray(step["state_out"], dtype=float)
        tunnel_count += int(step["is_tunnel"] > 0.5)

    err = pred - truth
    rmse4 = float(np.sqrt(np.mean(err * err)))
    mae4 = float(np.mean(np.abs(err)))
    rmse_dim = np.sqrt(np.mean(err * err, axis=0))
    mae_dim = np.mean(np.abs(err), axis=0)

    return {
        "name": name,
        "n_events": int(mags.size),
        "skipped": False,
        "n_steps": int(n),
        "tunnel_steps": int(tunnel_count),
        "tunnel_ratio": float(tunnel_count / max(n, 1)),
        "rmse_4d": rmse4,
        "mae_4d": mae4,
        "rmse_by_dim": [float(v) for v in rmse_dim],
        "mae_by_dim": [float(v) for v in mae_dim],
    }


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    datasets: list[dict[str, object]] = []

    csv1 = ROOT / "earthquake_1995-2023.csv"
    if csv1.exists():
        mags, clocks = load_catalog_csv(csv1)
        datasets.append(eval_closure(csv1.name, mags, clocks))

    csv2 = ROOT / "earthquake_data.csv"
    if csv2.exists():
        mags, clocks = load_catalog_csv(csv2)
        datasets.append(eval_closure(csv2.name, mags, clocks))

    gj = ROOT / "usgs_events_2026-02-01_2026-03-01_ca_bbox.geojson"
    if gj.exists():
        mags, clocks = load_geojson_usgs(gj)
        datasets.append(eval_closure(gj.name, mags, clocks))

    report = {"datasets": datasets}
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Physical Minimal Closure (No Regression)", ""]
    for d in datasets:
        lines.append(f"## {d['name']}")
        lines.append("")
        lines.append(f"- n_events: `{d['n_events']}`")
        if d.get("skipped"):
            lines.append(f"- skipped: `{d['reason']}`")
            lines.append("")
            continue
        lines.append(f"- n_steps: `{d['n_steps']}`")
        lines.append(f"- tunnel_steps: `{d['tunnel_steps']}`")
        lines.append(f"- tunnel_ratio: `{d['tunnel_ratio']}`")
        lines.append(f"- rmse_4d: `{d['rmse_4d']}`")
        lines.append(f"- mae_4d: `{d['mae_4d']}`")
        lines.append(f"- rmse_by_dim[x,y,z,w]: `{d['rmse_by_dim']}`")
        lines.append(f"- mae_by_dim[x,y,z,w]: `{d['mae_by_dim']}`")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

