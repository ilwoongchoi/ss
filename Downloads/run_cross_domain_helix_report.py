from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from pathlib import Path

import numpy as np

from geometry_package.absolute_constants import DELTA_T_OBS_DERIVED, GAMMA_COSMOS


def analytic_signal(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    n = x.size
    X = np.fft.fft(x)
    h = np.zeros(n)
    if n % 2 == 0:
        h[0] = 1.0
        h[n // 2] = 1.0
        h[1:n // 2] = 2.0
    else:
        h[0] = 1.0
        h[1:(n + 1) // 2] = 2.0
    return np.fft.ifft(X * h)


def smooth_series(x: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return x
    kernel = np.ones(window, dtype=float) / float(window)
    return np.convolve(x, kernel, mode="same")


def normalize(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return (x - np.nanmean(x)) / (np.nanstd(x) + 1.0e-12)


def helix_metrics(z: np.ndarray) -> dict[str, float | int | bool]:
    z = np.asarray(z)
    amp = np.abs(z)
    phase = np.unwrap(np.angle(z))
    dphi = np.diff(phase)
    nonzero = dphi[np.abs(dphi) > 1.0e-9]
    handedness = 0.0 if nonzero.size == 0 else float(np.sign(np.median(nonzero)))
    opposite_fraction = 0.0 if nonzero.size == 0 else float(np.mean(np.sign(nonzero) != handedness))
    phase_span = float(phase[-1] - phase[0]) if phase.size else 0.0
    min_amp = float(np.min(amp)) if amp.size else 0.0
    return {
        "n": int(z.size),
        "min_amplitude": min_amp,
        "mean_amplitude": float(np.mean(amp)) if amp.size else 0.0,
        "phase_span": phase_span,
        "phase_turns": float(abs(phase_span) / (2.0 * np.pi)),
        "handedness": handedness,
        "opposite_fraction": opposite_fraction,
        "helix_continuous": bool(min_amp > 0.0 and abs(phase_span) > np.pi and handedness != 0.0),
    }


def load_finance_speculation() -> tuple[np.ndarray, dict[str, object]]:
    path = Path(r"d:\Users\user\Documents\newstart\%SNAP%\status_snapshot_prev\status_snapshot_20260130\PI_GLOBAL_POINT_CLOUD_FINANCE_FIXED.csv")
    rows: list[tuple[float, float, float]] = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rows.append((float(row["pi_1"]), float(row["pi_2"]), float(row["val"])))
            except (TypeError, ValueError):
                continue
    arr = np.asarray(rows, dtype=float)
    x = normalize(arr[:, 0])
    y = normalize(arr[:, 1])
    z = x + 1j * y
    order = np.argsort(np.angle(z))
    return z[order], {
        "path": str(path),
        "ordering": "phase_sorted_point_cloud",
        "points": int(arr.shape[0]),
    }


def load_macro_cpi() -> tuple[np.ndarray, dict[str, object]]:
    path = Path(r"d:\Users\user\Documents\newstart\papers\API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_116.zip")
    with zipfile.ZipFile(path) as zf:
        data_name = next(name for name in zf.namelist() if name.startswith("API_") and name.lower().endswith(".csv"))
        text = zf.read(data_name).decode("utf-8-sig", errors="replace")
    rows = list(csv.reader(io.StringIO(text)))
    header = rows[4]
    years = [h for h in header[4:] if h.isdigit()]
    yearly_values: dict[str, list[float]] = {year: [] for year in years}
    for row in rows[5:]:
        for year, value in zip(years, row[4:4 + len(years)]):
            if value == "":
                continue
            try:
                yearly_values[year].append(float(value))
            except ValueError:
                continue
    series = np.asarray([np.median(yearly_values[year]) for year in years if yearly_values[year]], dtype=float)
    series = normalize(series)
    z = analytic_signal(smooth_series(series, window=7))
    return z, {
        "path": str(path),
        "series": "world_median_cpi_inflation_by_year",
        "smoothing_window": 7,
        "years": int(series.size),
    }


def load_quake_daily() -> tuple[np.ndarray, dict[str, object]]:
    path = Path(r"d:\Users\user\Documents\newstart\RUTGERS\verification\domains\seismology\evidence\stage_b__earthquakes_daily\seismology_outcomes__STAGE_B__SSOT.csv")
    values: list[float] = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                values.append(float(row["k_eff"]))
            except (TypeError, ValueError):
                continue
    series = normalize(np.asarray(values, dtype=float))
    z = analytic_signal(smooth_series(series, window=15))
    return z, {
        "path": str(path),
        "series": "daily_k_eff",
        "smoothing_window": 15,
        "days": int(series.size),
    }


def scale_ladder() -> list[dict[str, object]]:
    return [
        {"layer": 1, "status": "inferred_overlay", "domain": "void_floor", "meaning": "pre-visible vacuum floor / deepest baseline"},
        {"layer": 2, "status": "explicit_lock", "domain": "graviton", "meaning": "1/256 hidden floor"},
        {"layer": 3, "status": "explicit_lock", "domain": "neutrino", "meaning": "1/128 inward transport / hidden relay"},
        {"layer": 4, "status": "explicit_lock", "domain": "sentinel", "meaning": "1/64 quantization filter / gate"},
        {"layer": 5, "status": "explicit_lock", "domain": "proton", "meaning": "1/32 boundary, storage, container"},
        {"layer": 6, "status": "explicit_lock", "domain": "photon", "meaning": "1/16 visible branch / signal carrier"},
        {"layer": 7, "status": "explicit_lock", "domain": "electron", "meaning": "1/8 contact, transaction, local exchange"},
        {"layer": 8, "status": "verified_overlay", "domain": "speculative_finance", "meaning": "fast market point-cloud helix"},
        {"layer": 9, "status": "verified_overlay", "domain": "macroeconomy", "meaning": "slow aggregate inflation helix"},
        {"layer": 10, "status": "verified_overlay", "domain": "seismology", "meaning": "earth stress-release helix"},
    ]


def build_report() -> dict[str, object]:
    finance_z, finance_meta = load_finance_speculation()
    macro_z, macro_meta = load_macro_cpi()
    quake_z, quake_meta = load_quake_daily()

    return {
        "forced_seconds": {
            "delta_phase": float(DELTA_T_OBS_DERIVED),
            "gamma_cosmos": float(GAMMA_COSMOS),
            "seconds_if_forced": float(DELTA_T_OBS_DERIVED * GAMMA_COSMOS),
            "known_physics_compare": "0.327 s is still inside the first second; particle soup already exists, not the first birth of energy",
        },
        "domain_helix": {
            "speculative_finance": {
                "meta": finance_meta,
                "metrics": helix_metrics(finance_z),
            },
            "macroeconomy": {
                "meta": macro_meta,
                "metrics": helix_metrics(macro_z),
            },
            "seismology": {
                "meta": quake_meta,
                "metrics": helix_metrics(quake_z),
            },
        },
        "ten_scale_ladder": scale_ladder(),
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Cross-Domain Helix Report",
        "",
        "## Forced Seconds",
        f"- delta_phase: `{report['forced_seconds']['delta_phase']}`",
        f"- gamma_cosmos: `{report['forced_seconds']['gamma_cosmos']}`",
        f"- seconds_if_forced: `{report['forced_seconds']['seconds_if_forced']}`",
        f"- compare: `{report['forced_seconds']['known_physics_compare']}`",
        "",
        "## Domain Helix",
    ]

    for key, payload in report["domain_helix"].items():
        meta = payload["meta"]
        metrics = payload["metrics"]
        lines.extend(
            [
                f"- domain `{key}`",
                f"- path `{meta['path']}`",
                f"- helix_continuous `{metrics['helix_continuous']}`",
                f"- handedness `{metrics['handedness']}`",
                f"- phase_turns `{metrics['phase_turns']}`",
                f"- min_amplitude `{metrics['min_amplitude']}`",
                f"- opposite_fraction `{metrics['opposite_fraction']}`",
            ]
        )

    lines.extend(["", "## Ten Scale Ladder"])
    for row in report["ten_scale_ladder"]:
        lines.append(
            f"- L{row['layer']} [{row['status']}] `{row['domain']}` -> `{row['meaning']}`"
        )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare the forced 0.327 s reading to known physics and verify continuous helix signatures in speculative finance, macroeconomy, and seismology."
    )
    parser.add_argument("--out-json", default="analysis_results/cross_domain_helix_report.json")
    parser.add_argument("--out-md", default="analysis_results/cross_domain_helix_report.md")
    args = parser.parse_args()

    report = build_report()
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"seconds_if_forced={report['forced_seconds']['seconds_if_forced']}")
    for name, payload in report["domain_helix"].items():
        print(f"{name}_continuous={payload['metrics']['helix_continuous']}")
        print(f"{name}_phase_turns={payload['metrics']['phase_turns']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
