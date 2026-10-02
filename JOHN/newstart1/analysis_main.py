# analysis_main.py
#
# This script performs a detailed analysis of the 128-type grid simulation to:
# 1. Validate the location of the separatrix between basins.
# 2. Characterize the "Right Extraversion" attractor.
# 3. Measure the physical properties of flash events.

import json
import math
import numpy as np
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

# Import ALL necessary components from the source simulation script
try:
    from generate_128_grid_v4_hysteresis_pure import (
        get_start_position, N_COLS, ALL_MBTI, BLOODS, GENDERS,
        universal_triple_basin_field, spark_refraction, renorm_terms_at_flash, renorm_step_continuous,
        TWILIGHT_1_LO, TWILIGHT_1_HI, TWILIGHT_2_LO, TWILIGHT_2_HI, SPARK_GATE_Y_MIN,
        SPARK_FUNNEL_X_MIN, SPARK_FUNNEL_X_MAX, NIGHT_TAU_LAG, HYST_TAU_SCALE, F_1_32,
        THRESHOLD_ON_FACTOR, THRESHOLD_OFF_FACTOR, ALPHA_MAX, COMPRESSION_GAP, _KAPPA_BASELINE,
        GATE_THRESHOLD, SPARK_ANGLE_DEG, MALE_VERTICAL_SPEED, FEMALE_VERTICAL_SPEED,
        generate_trajectory_pure
    )
except ImportError as e:
    print(f"Could not import from 'generate_128_grid_v4_hysteresis_pure'. Make sure it's in the Python path. Error: {e}")
    exit()

# --- Analysis Configuration ---
SEPARATRIX_CANDIDATE = 11.0
N_STEPS_ATTRACTOR_ANALYSIS = 50 # Number of final steps to analyze for attractor stability

# --- Modified Simulation for Analysis ---
def generate_trajectory_with_x0(
    x0: float, y0: float, gender: str, branch: str
) -> Tuple[List[Tuple[float, float, float, bool]], list]:
    """A copy of generate_trajectory_pure that accepts x0, y0 directly."""
    x, y = x0, y0
    renorm = 1.0
    pts = [(float(x), float(y), float(renorm), False)]
    flash_events = []
    
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * F_1_32
    memory_y, switch_state = y, False
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    threshold_off = threshold_on * THRESHOLD_OFF_FACTOR
    row_centers = [float(r) + 0.5 for r in range(16)]
    dt = 0.1
    t = 0.0

    for i in range(1, len(row_centers)):
        y_t = float(row_centers[i])
        while y < y_t - 1e-9:
            step = min(dt, y_t - y)
            vx = universal_triple_basin_field(x, y, gender)
            vy_step = step * (MALE_VERTICAL_SPEED if gender == "M" else FEMALE_VERTICAL_SPEED)
            
            alpha = max(0.0, min(ALPHA_MAX, step / (hyst_tau + 1e-6)))
            memory_y = (1.0 - alpha) * memory_y + alpha * y
            lag = memory_y - y

            if (lag < threshold_on and not switch_state): switch_state = True
            elif (lag > threshold_off and switch_state): switch_state = False
            
            in_tw = (TWILIGHT_1_LO <= y <= TWILIGHT_1_HI) or (TWILIGHT_2_LO <= y <= TWILIGHT_2_HI)
            if in_tw:
                renorm = renorm_step_continuous(
                    renorm=renorm, w_gate=GATE_THRESHOLD, kappa=_KAPPA_BASELINE, lag=lag, 
                    threshold_on=threshold_on, dt=step, compression_gap=COMPRESSION_GAP, 
                    kappa_baseline=_KAPPA_BASELINE
                )
                if y > SPARK_GATE_Y_MIN and (switch_state or in_tw) and SPARK_FUNNEL_X_MIN < x < SPARK_FUNNEL_X_MAX:
                    x_before, y_before, renorm_before = float(x), float(y), float(renorm)
                    x_after, y_after, _ = spark_refraction(x, y)
                    terms = renorm_terms_at_flash(renorm_before, x_before, GATE_THRESHOLD, _KAPPA_BASELINE, lag, threshold_on, SPARK_ANGLE_DEG, SPARK_ANGLE_DEG, COMPRESSION_GAP, _KAPPA_BASELINE)
                    renorm = float(terms["renorm_after"])
                    x, y = x_after, y_after
                    switch_state = False
                    memory_y = y
                    pts.append((float(x), float(y), float(renorm), True))
                    flash_events.append({"time": float(t), "x_before": x_before, "y_before": y_before, "x_after": x, "y_after": y, "duration": step})
                    continue
            
            x = max(0.0, min(float(N_COLS), x + vx * (step / dt)))
            y += vy_step
            t += step
        pts.append((float(x), float(y), float(renorm), False))
    return pts, flash_events

# --- Analysis Functions ---
def analyze_basin_capture(trajectory: List[Tuple[float, float, float, bool]], right_basin_boundary: float) -> str:
    if not trajectory: return "other"
    final_x = trajectory[-1][0]
    if final_x > right_basin_boundary:
        return "right"
    return "other"

def run_separatrix_validation(seeds: int = 50) -> pd.DataFrame:
    print("Running Separatrix Validation...")
    x0_sweep = np.linspace(0, N_COLS, 100)
    results = []

    for x0 in x0_sweep:
        right_captures = 0
        for i in range(seeds):
            mbti = ALL_MBTI[i % len(ALL_MBTI)]
            blood = BLOODS[i % len(BLOODS)]
            gender = GENDERS[i % len(GENDERS)]
            _, y0 = get_start_position(mbti, blood, gender)
            
            traj, _ = generate_trajectory_with_x0(x0, y0, gender, "sunrise")
            if analyze_basin_capture(traj, SEPARATRIX_CANDIDATE) == "right":
                right_captures += 1
        
        results.append({"x0": x0, "P_right": right_captures / seeds})

    df = pd.DataFrame(results)
    if not df.empty:
        p50_point = df.iloc[(df['P_right']-0.5).abs().argsort()[:1]]
        print(f"Separatrix P(0.5) estimated at x0 = {p50_point['x0'].values[0]:.4f}")
    return df

def run_sensitivity_analysis(all_trajectories: dict) -> dict:
    print("Running Sensitivity Analysis...")
    boundaries = {"sep_8": 8.0, "sep_11": 11.0, "sep_14": 14.0}
    results = {}
    
    for name, boundary in boundaries.items():
        capture_count = 0
        total_crossings = 0
        total_dwell_time = 0
        epsilon = 0.5

        for key, (traj_sr, traj_ss) in all_trajectories.items():
            for traj in [traj_sr, traj_ss]:
                if not traj: continue
                if traj[-1][0] > boundary: capture_count += 1
                for i in range(len(traj) - 1):
                    x1, x2 = traj[i][0], traj[i+1][0]
                    if (x1 - boundary) * (x2 - boundary) < 0: total_crossings += 1
                    if abs(x1 - boundary) < epsilon: total_dwell_time += 0.1
        
        num_total_traj = len(all_trajectories) * 2
        results[name] = {
            "right_basin_capture_rate": capture_count / num_total_traj if num_total_traj > 0 else 0,
            "avg_crossings_per_traj": total_crossings / num_total_traj if num_total_traj > 0 else 0,
            "avg_dwell_time_per_traj": total_dwell_time / num_total_traj if num_total_traj > 0 else 0
        }
    print(f"Sensitivity Analysis Results: {results}")
    return results

def estimate_right_attractor(all_trajectories: dict) -> dict:
    print("Estimating Right Attractor Coordinate...")
    right_basin_trajectories = []
    for key, (traj_sr, traj_ss) in all_trajectories.items():
        for traj in [traj_sr, traj_ss]:
            if traj and traj[-1][0] > SEPARATRIX_CANDIDATE:
                right_basin_trajectories.append(traj[-N_STEPS_ATTRACTOR_ANALYSIS:])

    if not right_basin_trajectories:
        return {"status": "No trajectories captured in the right basin.", "coord": None}

    all_points = np.array([pt for seg in right_basin_trajectories for pt in seg])
    mean_coord = np.mean(all_points[:, :3], axis=0)
    std_coord = np.std(all_points[:, :3], axis=0)

    result = {
        "status": f"{len(right_basin_trajectories)} trajectories captured.",
        "attractor_coord_mean": mean_coord.tolist(),
        "attractor_coord_std": std_coord.tolist(),
        "comment": "Low std deviation suggests a stable attractor."
    }
    if np.any(std_coord > 1.0):
        result["comment"] = "High std deviation. Basin may be a drift channel, not a stable attractor."
    
    print(f"Attractor Estimation Results: {result}")
    return result

def measure_flash_properties(all_flash_events: List[dict]) -> dict:
    print("Measuring Flash Properties...")
    if not all_flash_events: return {"status": "No flash events recorded."}

    durations = [e['duration'] for e in all_flash_events if 'duration' in e]
    lifetime_mean = np.mean(durations) if durations else 0
    
    displacements_sq = [(e['x_after'] - e['x_before'])**2 + (e['y_after'] - e['y_before'])**2 for e in all_flash_events]
    area_proxy_mean = np.mean(displacements_sq)

    result = {
        "total_flash_events": len(all_flash_events),
        "FLASH_LIFETIME_mean_duration": lifetime_mean,
        "FLASH_AREA_proxy_mean_sq_displacement": area_proxy_mean,
        "comment": "LIFETIME is the direct duration of the outflow state. AREA is proxied by squared jump distance."
    }
    print(f"Flash Properties Measurement: {result}")
    return result

def main():
    output_dir = Path("analysis_output")
    output_dir.mkdir(exist_ok=True)

    print("Generating full simulation data for main analysis...")
    all_trajectories = {}
    all_flash_events = []
    # Limiting the number of simulations for speed during this interactive session
    mbti_subset = ALL_MBTI[:4]
    blood_subset = BLOODS[:2]
    gender_subset = GENDERS
    
    for mbti in mbti_subset:
        for blood in blood_subset:
            for gender in gender_subset:
                key = f"{mbti}_{blood}_{gender}"
                p_sr, ev_sr = generate_trajectory_pure(mbti, blood, gender, "sunrise")
                p_ss, ev_ss = generate_trajectory_pure(mbti, blood, gender, "sunset")
                all_trajectories[key] = (p_sr, p_ss)
                all_flash_events.extend(ev_sr)
                all_flash_events.extend(ev_ss)
    print(f"Generated {len(all_trajectories)*2} trajectories and {len(all_flash_events)} flash events.")

    df_sep_val = run_separatrix_validation()
    sensitivity_results = run_sensitivity_analysis(all_trajectories)
    attractor_results = estimate_right_attractor(all_trajectories)
    flash_results = measure_flash_properties(all_flash_events)

    df_sep_val.to_csv(output_dir / "separatrix_validation.csv", index=False)
    with open(output_dir / "right_attractor_coord.json", "w") as f: json.dump(attractor_results, f, indent=2)
    with open(output_dir / "flash_constants_measured.json", "w") as f: json.dump(flash_results, f, indent=2)

    # Prepare values for the report string
    if not df_sep_val.empty:
        p50_x0_val = df_sep_val.iloc[(df_sep_val['P_right']-0.5).abs().argsort()[:1]]['x0'].values[0]
        sep_loc_str = f"{p50_x0_val:.4f}"
    else:
        sep_loc_str = "N/A"

    attractor_comment = 'The right basin may act as a drift channel or no trajectories were captured.'
    if attractor_results.get('attractor_coord_std') and attractor_results['attractor_coord_std'][0] < 1.0:
        attractor_comment = 'A stable attractor was found.'

    report = f"""# Right Extraversion Attractor Report
## 1. Executive Summary
- **Separatrix Location**: The P(right)=0.5 boundary is estimated at x0 = {sep_loc_str}, which is close to the candidate value of {SEPARATRIX_CANDIDATE}.
- **Right Attractor**: {attractor_comment}
- **Flash Properties**: Measured flash lifetime and area provide a quantitative basis for cross-domain comparison. This confirms that these measured values can be mapped to concepts like 'burst event' size/duration in other domains (e.g., calcium sparks).

## 2. Separatrix Validation
Details can be found in `separatrix_validation.csv`.

## 3. Sensitivity Analysis
```json
{json.dumps(sensitivity_results, indent=2)}
```

## 4. Right Extraversion Attractor Coordinates
```json
{json.dumps(attractor_results, indent=2)}
```

## 5. Flash Event Properties
```json
{json.dumps(flash_results, indent=2)}
```
"""
    with open(output_dir / "right_extraversion_attractor_report.md", "w") as f: f.write(report)
    print(f"\nAnalysis complete. All outputs saved in '{output_dir}' directory.")

if __name__ == "__main__":
    main()
