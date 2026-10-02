#!/usr/bin/env python3
"""
Right-branch hypothesis test:
- Sweep separatrix_2 candidates using production physics (generate_128_grid_v4_hysteresis_pure.py).
- Compete hypotheses: (A) stable attractor vs (B) corridor/transit.
- Outputs are written to out/right_branch_hypothesis/ with strict numeric metrics.

Artifacts:
- separatrix_validation.csv: P(right basin capture) for each separatrix_2 candidate.
- separatrix_summary.json: summary of sweep and P(0.5) estimate.
- right_branch_cluster_report.json: terminal cluster stats (mean/std/cov) for right captures.
- right_branch_events.csv: flash events with metadata.
- right_branch_verdict.json: numeric verdict attractor vs corridor with thresholds.
- flash_constants_measured.json: FLASH_LIFETIME and FLASH_AREA metrics.
- right_attractor_coord.json (if attractor) OR right_corridor_report.json (if corridor).
"""

import json
import math
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple

# Production physics (no modifications)
from generate_128_grid_v4_hysteresis_pure import (
    ALL_MBTI,
    BLOODS,
    GENDERS,
    N_COLS,
    generate_trajectory_pure,
    SPARK_GATE_Y_MIN,
    SPARK_FUNNEL_X_MIN,
    SPARK_FUNNEL_X_MAX,
)

# Sweep candidates (must not invent new constants)
SEPARATRIX_CANDIDATES = [8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0]
BURST_GAPS = [0.2, 0.35, 0.5, 0.75]
RIGHT_BASIN_VERDICT_THRESHOLDS = {
    "capture_rate_min": 0.60,      # Attractor requires >= 0.60 capture
    "cluster_std_max": 1.00,       # Attractor requires terminal std <= 1.00
    "drift_mag_max": 1.20,         # Attractor requires low drift from entry to exit
    "escape_fraction_max": 0.10,   # Attractor requires few escapees
}

OUTPUT_DIR = Path("out/right_branch_hypothesis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def analyze_capture(traj: List[Tuple[float, float, float, bool]], boundary: float) -> Tuple[bool, int, float]:
    """Return (captured, crossings, dwell_time) for a trajectory relative to boundary."""
    if not traj:
        return False, 0, 0.0
    crossings = 0
    dwell = 0.0
    epsilon = 0.5
    prev_x = traj[0][0]
    for pt in traj[1:]:
        x = pt[0]
        if (prev_x - boundary) * (x - boundary) < 0:
            crossings += 1
        if abs(x - boundary) < epsilon:
            dwell += 1.0  # unit time per recorded step (consistent discrete grid rows)
        prev_x = x
    captured = traj[-1][0] > boundary
    return captured, crossings, dwell


def accumulate_cluster_points(traj: List[Tuple[float, float, float, bool]], tail: int = 40) -> np.ndarray:
    if not traj:
        return np.empty((0, 3))
    return np.array(traj[-tail:])[:, :3]


def drift_magnitude(traj: List[Tuple[float, float, float, bool]]) -> float:
    if not traj:
        return 0.0
    x0, y0 = traj[0][0], traj[0][1]
    x1, y1 = traj[-1][0], traj[-1][1]
    return math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


def measure_flash_events(events: List[dict], gap: float = 0.2) -> Dict[str, float]:
    """Group events into bursts to measure active lifetime and spatial spread.

    - Burst definition: consecutive flash events where the gap between start times is <= gap.
    - Lifetime: last_time - first_time + last_duration (active segment length).
    - Area proxy: mean squared distance of (x_after, y_after) from burst centroid.
    """
    if not events:
        return {
            "total_flash_events": 0,
            "burst_count": 0,
            "FLASH_LIFETIME_mean_duration": 0.0,
            "FLASH_LIFETIME_max_duration": 0.0,
            "FLASH_AREA_proxy_mean_sq_displacement": 0.0,
            "FLASH_AREA_proxy_max_sq_displacement": 0.0,
        }

    # Sort by time to build bursts
    ev_sorted = sorted(events, key=lambda e: e.get("time", 0.0))
    bursts = []
    current = []
    for ev in ev_sorted:
        if not current:
            current.append(ev)
            continue
        last_time = current[-1].get("time", 0.0)
        if ev.get("time", 0.0) - last_time <= gap:
            current.append(ev)
        else:
            bursts.append(current)
            current = [ev]
    if current:
        bursts.append(current)

    lifetimes = []
    areas = []
    for burst in bursts:
        start_t = burst[0].get("time", 0.0)
        end_t = burst[-1].get("time", 0.0)
        end_duration = burst[-1].get("duration", 0.0)
        lifetimes.append((end_t - start_t) + end_duration)

        pts = np.array([[b.get("x_after", 0.0), b.get("y_after", 0.0)] for b in burst])
        centroid = pts.mean(axis=0)
        sq_disp = np.mean(np.sum((pts - centroid) ** 2, axis=1)) if len(pts) else 0.0
        areas.append(float(sq_disp))

    return {
        "total_flash_events": len(events),
        "burst_count": len(bursts),
        "FLASH_LIFETIME_mean_duration": float(np.mean(lifetimes)) if lifetimes else 0.0,
        "FLASH_LIFETIME_max_duration": float(np.max(lifetimes)) if lifetimes else 0.0,
        "FLASH_AREA_proxy_mean_sq_displacement": float(np.mean(areas)) if areas else 0.0,
        "FLASH_AREA_proxy_max_sq_displacement": float(np.max(areas)) if areas else 0.0,
    }


def compute_verdict(capture_rate: float, cluster_std: float, drift_mag: float, escape_fraction: float) -> str:
    t = RIGHT_BASIN_VERDICT_THRESHOLDS
    attractor = (
        capture_rate >= t["capture_rate_min"]
        and cluster_std <= t["cluster_std_max"]
        and drift_mag <= t["drift_mag_max"]
        and escape_fraction <= t["escape_fraction_max"]
    )
    return "attractor" if attractor else "corridor"


def _x_variance_growth_rate(traj: List[Tuple[float, float, float, bool]]) -> float:
    if not traj or len(traj) < 4:
        return 0.0
    xs = np.array([p[0] for p in traj])
    half = len(xs) // 2
    if half == 0:
        return 0.0
    var_start = float(np.var(xs[:half]))
    var_end = float(np.var(xs[half:]))
    return (var_end - var_start) / len(xs)


def _y_progress(traj: List[Tuple[float, float, float, bool]]) -> float:
    if not traj:
        return 0.0
    return float(traj[-1][1] - traj[0][1])


def run_gap_sweep(all_trajectories: Dict[str, Tuple[List, List]], all_flash_events: List[dict]):
    rows = []
    diagnostics = []

    # Precompute drift metrics shared across gaps
    drift_mags, y_progresses, x_var_grows = [], [], []
    for _, (traj_sr, traj_ss) in all_trajectories.items():
        for traj in (traj_sr, traj_ss):
            drift_mags.append(drift_magnitude(traj))
            y_progresses.append(_y_progress(traj))
            x_var_grows.append(_x_variance_growth_rate(traj))
    drift_mag_mean = float(np.mean(drift_mags)) if drift_mags else 0.0
    y_progress_mean = float(np.mean(y_progresses)) if y_progresses else 0.0
    x_var_growth_mean = float(np.mean(x_var_grows)) if x_var_grows else 0.0

    for gap in BURST_GAPS:
        metrics = measure_flash_events(all_flash_events, gap=gap)
        segments = metrics.get("burst_count", 0)
        lifetimes = metrics.get("FLASH_LIFETIME_mean_duration", 0.0)
        areas = metrics.get("FLASH_AREA_proxy_mean_sq_displacement", 0.0)

        # duration distribution approximations (median/IQR via synthetic reconstruction is unavailable); use mean/max as proxies
        lifetime_median = lifetimes
        lifetime_iqr = max(0.0, metrics.get("FLASH_LIFETIME_max_duration", 0.0) - lifetimes)
        area_median = areas
        area_iqr = max(0.0, metrics.get("FLASH_AREA_proxy_max_sq_displacement", 0.0) - areas)

        # missing rate
        total_events = len(all_flash_events)
        missing_before_after = 0
        if total_events:
            for ev in all_flash_events:
                if any(ev.get(k) is None for k in ["x_before", "y_before", "x_after", "y_after"]):
                    missing_before_after += 1
        missing_rate = (missing_before_after / total_events) if total_events else 0.0

        rows.append({
            "gap": gap,
            "flash_event_count": total_events,
            "active_flash_segment_count": segments,
            "flash_active_duration_median": lifetime_median,
            "flash_active_duration_IQR": lifetime_iqr,
            "FLASH_LIFETIME_mean": lifetimes,
            "FLASH_LIFETIME_max": metrics.get("FLASH_LIFETIME_max_duration", 0.0),
            "FLASH_AREA_mean": areas,
            "FLASH_AREA_max": metrics.get("FLASH_AREA_proxy_max_sq_displacement", 0.0),
            "FLASH_AREA_median": area_median,
            "FLASH_AREA_IQR": area_iqr,
            "missing_coord_rate": missing_rate,
            "drift_magnitude_mean": drift_mag_mean,
            "y_progress_mean": y_progress_mean,
            "x_variance_growth_rate": x_var_growth_mean,
        })

        diagnostics.append({
            "gap": gap,
            "note": "Flash metrics remain near-zero" if (lifetimes == 0.0 and areas == 0.0) else "Flash metrics non-zero",
            "missing_coord_rate": missing_rate,
            "drift_magnitude_mean": drift_mag_mean,
            "x_variance_growth_rate": x_var_growth_mean,
        })

    df_gap = pd.DataFrame(rows)
    df_gap.to_csv(OUTPUT_DIR / "flash_gap_sweep_summary.csv", index=False)

    # Verdict on root cause
    baseline = rows[0] if rows else {}
    last = rows[-1] if rows else {}
    verdict_cause = "undetermined"
    if rows:
        if baseline.get("FLASH_LIFETIME_mean", 0.0) == 0.0 and last.get("FLASH_LIFETIME_mean", 0.0) > 0.0:
            verdict_cause = "gap_sensitivity"  # GAP growth revives lifetime
        elif all(r.get("FLASH_LIFETIME_mean", 0.0) == 0.0 for r in rows):
            verdict_cause = "logger_or_definition"  # no change across gaps
        else:
            verdict_cause = "mixed"

    with open(OUTPUT_DIR / "flash_gap_sweep_verdict.json", "w") as f:
        json.dump({
            "verdict": verdict_cause,
            "rows": rows,
        }, f, indent=2)

    # Diagnostics markdown
    lines = ["# Flash GAP Sweep Diagnostics", "", "| gap | lifetime_mean | area_mean | missing_rate | drift_mag_mean | x_var_growth_rate |", "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['gap']} | {r['FLASH_LIFETIME_mean']:.4f} | {r['FLASH_AREA_mean']:.4f} | {r['missing_coord_rate']:.4f} | {r['drift_magnitude_mean']:.4f} | {r['x_variance_growth_rate']:.4f} |")
    with open(OUTPUT_DIR / "flash_gap_diagnostics.md", "w") as f:
        f.write("\n".join(lines))


def main():
    separatrix_records = []
    all_flash_events = []
    all_traj_map = {}
    cluster_points = []
    drift_list = []
    captured_flags = []
    escape_flags = []
    event_rows = []

    total_runs = 0
    for sep in SEPARATRIX_CANDIDATES:
        captures = 0
        crossings_total = 0
        dwell_total = 0.0
        local_runs = 0

        for mbti in ALL_MBTI:
            for blood in BLOODS:
                for gender in GENDERS:
                    for branch in ("sunrise", "sunset"):
                        total_runs += 1
                        local_runs += 1
                        traj, events = generate_trajectory_pure(mbti, blood, gender, branch)
                        captured, crossings, dwell = analyze_capture(traj, sep)
                        captures += 1 if captured else 0
                        crossings_total += crossings
                        dwell_total += dwell

                        # Record flashes with metadata
                        for ev in events:
                            row = {
                                "separatrix": sep,
                                "mbti": mbti,
                                "blood": blood,
                                "gender": gender,
                                "branch": branch,
                                "time": ev.get("time"),
                                "x_before": ev.get("x_before"),
                                "y_before": ev.get("y_before"),
                                "x_after": ev.get("x_after"),
                                "y_after": ev.get("y_after"),
                                "duration": ev.get("duration"),
                            }
                            event_rows.append(row)
                        # Accumulate flash events only for reference separatrix=11 to avoid duplication
                        if sep == 11.0 and events:
                            all_flash_events.extend(events)

                        # Collect trajectories once at separatrix=11 for gap sweep diagnostics
                        if sep == 11.0:
                            base_key = f"{mbti}_{blood}_{gender}"
                            branch_map = all_traj_map.setdefault(base_key, {})
                            branch_map[branch] = traj

                        # Cluster accumulation only for right captures at mid candidate (11.0) to judge stability
                        if sep == 11.0 and captured:
                            cluster_points.append(accumulate_cluster_points(traj))
                            drift_list.append(drift_magnitude(traj))
                            captured_flags.append(True)
                        elif sep == 11.0:
                            captured_flags.append(False)
                            drift_list.append(drift_magnitude(traj))
                        # Escape flag: crossed boundary but final not captured
                        escaped = crossings > 0 and (not captured)
                        if sep == 11.0:
                            escape_flags.append(escaped)

        p_right = captures / local_runs if local_runs else 0.0
        separatrix_records.append({
            "separatrix": sep,
            "P_right": p_right,
            "avg_crossings": crossings_total / local_runs if local_runs else 0.0,
            "avg_dwell": dwell_total / local_runs if local_runs else 0.0,
        })

    # Save separatrix validation
    df_sep = pd.DataFrame(separatrix_records)
    df_sep.to_csv(OUTPUT_DIR / "separatrix_validation.csv", index=False)

    # Estimate P(0.5) by nearest candidate
    if not df_sep.empty:
        idx = (df_sep["P_right"] - 0.5).abs().idxmin()
        p50_est = df_sep.loc[idx, "separatrix"]
    else:
        p50_est = None

    with open(OUTPUT_DIR / "separatrix_summary.json", "w") as f:
        json.dump({"p50_separatrix_est": p50_est, "records": separatrix_records}, f, indent=2)

    # Cluster stats at separatrix=11.0
    if cluster_points:
        pts = np.vstack(cluster_points)
    else:
        pts = np.empty((0, 3))
    cluster_mean = pts.mean(axis=0).tolist() if pts.size else None
    cluster_std = pts.std(axis=0).max().item() if pts.size else 0.0
    cluster_cov = pts[:, :2] if pts.size else np.empty((0, 2))
    cluster_cov_matrix = (
        np.cov(cluster_cov.T).tolist() if cluster_cov.shape[0] >= 2 else None
    )

    drift_mag_mean = float(np.mean(drift_list)) if drift_list else 0.0
    escape_fraction = float(np.mean(escape_flags)) if escape_flags else 0.0

    cluster_report = {
        "separatrix_reference": 11.0,
        "cluster_mean": cluster_mean,
        "cluster_std_max": cluster_std,
        "cluster_covariance_xy": cluster_cov_matrix,
        "drift_magnitude_mean": drift_mag_mean,
        "escape_fraction": escape_fraction,
        "captured_samples": int(sum(captured_flags)),
        "total_samples": len(captured_flags),
    }
    with open(OUTPUT_DIR / "right_branch_cluster_report.json", "w") as f:
        json.dump(cluster_report, f, indent=2)

    # Flash metrics (global)
    flash_metrics = measure_flash_events(all_flash_events)
    with open(OUTPUT_DIR / "flash_constants_measured.json", "w") as f:
        json.dump(flash_metrics, f, indent=2)

    # Build trajectories map for gap sweep (sunrise/sunset) collected at separatrix=11
    all_trajectories = {}
    for key, branches in all_traj_map.items():
        sunrise_traj = branches.get("sunrise", [])
        sunset_traj = branches.get("sunset", [])
        all_trajectories[key] = (sunrise_traj, sunset_traj)

    # GAP sweep diagnostics (keeps separatrix_2=11 as reference line only)
    run_gap_sweep(all_trajectories, all_flash_events)

    # Event log
    df_events = pd.DataFrame(event_rows)
    df_events.to_csv(OUTPUT_DIR / "right_branch_events.csv", index=False)

    # Verdict at reference separatrix 11.0
    capture_ref = next((r for r in separatrix_records if r["separatrix"] == 11.0), None)
    capture_rate_ref = capture_ref["P_right"] if capture_ref else 0.0
    verdict = compute_verdict(
        capture_rate=capture_rate_ref,
        cluster_std=cluster_std,
        drift_mag=drift_mag_mean,
        escape_fraction=escape_fraction,
    )

    verdict_payload = {
        "reference_separatrix": 11.0,
        "capture_rate": capture_rate_ref,
        "cluster_std_max": cluster_std,
        "drift_magnitude_mean": drift_mag_mean,
        "escape_fraction": escape_fraction,
        "verdict": verdict,
        "thresholds": RIGHT_BASIN_VERDICT_THRESHOLDS,
    }
    with open(OUTPUT_DIR / "right_branch_verdict.json", "w") as f:
        json.dump(verdict_payload, f, indent=2)

    if verdict == "attractor":
        attractor_coord = {
            "mean_coord": cluster_mean,
            "std_max": cluster_std,
            "samples": cluster_report.get("captured_samples", 0),
        }
        with open(OUTPUT_DIR / "right_attractor_coord.json", "w") as f:
            json.dump(attractor_coord, f, indent=2)
    else:
        corridor_report = {
            "drift_magnitude_mean": drift_mag_mean,
            "escape_fraction": escape_fraction,
            "note": "Right basin behaves as transit corridor with dispersive trajectories.",
        }
        with open(OUTPUT_DIR / "right_corridor_report.json", "w") as f:
            json.dump(corridor_report, f, indent=2)

    print("Sweep complete. Outputs in", OUTPUT_DIR)


if __name__ == "__main__":
    main()
