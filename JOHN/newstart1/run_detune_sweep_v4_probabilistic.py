# run_detune_sweep_v4_probabilistic.py
# Flash를 확률 모델로 변경: p = clamp(lambda0 * w_gate * dt, 0, 1)

import numpy as np
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# ==============================================================================
# IMPORT GEOMETRY PACKAGE
# ==============================================================================
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry_package.universal_equation import w_gate, kappa_eff, in_sh_band
from geometry_package.north_pole_renorm import renorm_terms_at_flash, renorm_step_continuous

# ==============================================================================
# CONFIGURATION
# ==============================================================================
CONSTANTS_PATH = "out/geometry_constants_from_dist_all.json"
DIST_DATA_PATH = "out/dist_all_with_kappa.csv"
OUTPUT_DIR = "out/detune_closure_sweep_v4"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# RNG Seed for reproducibility
RNG_SEED = 42

# 4 Test Points
POINTS = [
    {"label": "center_in", "r": 0.1117, "q0": 0.9750},
    {"label": "r_out",     "r": 0.1130, "q0": 0.9750},
    {"label": "q0_out",    "r": 0.1117, "q0": 0.9850},
    {"label": "both_out",  "r": 0.1130, "q0": 0.9850}
]

# Physical Constants
N_ROWS = 16
N_COLS = 16
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = np.radians(SPARK_ANGLE_DEG)
SPARK_LEAP_DIST = 2.5
F_1_32 = 1/32.0
COMPRESSION_GAP = 3.0 * F_1_32

# Field & Dynamics Constants
REALITY_TENSION = 1.0
MALE_HORIZONTAL_AMP = 1.2
TORSION_4D = 0.02 
GABA_C_V_APEX = 0.14

# Hysteresis
HYST_TAU_SCALE = 0.5  
THRESHOLD_ON_FACTOR = 0.2 
THRESHOLD_OFF_FACTOR = 0.3
ALPHA_MAX = 0.5
NIGHT_TAU_LAG = SPARK_ANGLE_DEG / 60.0

# Spark Gate Geometry - PRODUCTION values
SPARK_FUNNEL_X_MIN = 6.0
SPARK_FUNNEL_X_MAX = 10.0
SPARK_GATE_Y_MIN = 10.0
Y_WRAP = 32.0

# Lambda0 tuning: target center_in flash count = 20~100
# Will be calibrated in first run
LAMBDA0 = 20.0  # Fixed reasonable value (5-50 range), p will NOT be clipped to 1

# ==============================================================================
# FIELD LOGIC
# ==============================================================================
def _v_shape(x, y):
    xn, yn = (x - 8.0) / 8.0, (y - 8.0) / 8.0
    return np.exp(-(xn**2 + yn**2) / (2 * (GABA_C_V_APEX ** 2)))

def universal_field(x, y, in_band=False):
    """
    Field with BALANCE tuned for funnel contact.
    
    CORRECT STRATEGY (based on observed behavior):
    - In-band: Need ORBIT around funnel (like out-band currently has)
    - Out-band: Should drift away from funnel (like in-band currently does)
    
    So we SWAP the configurations.
    """
    # Spiral drift
    drift_x = -TORSION_4D * (y - 8.0)
    drift_y = TORSION_4D * (x - 8.0)
    
    if in_band:
        # In-band: Use OUT-BAND configuration (creates orbits near funnel)
        tx, ty = 3.2, 14.0  # Left side terminal
        d_terminal = np.sqrt((x - tx)**2 + (y - ty)**2)
        terminal = -2.5 * np.exp(-d_terminal**2 / (2 * 1.5**2))
        v_shape_term = 1.2 * _v_shape(x, y)
    else:
        # Out-band: Use IN-BAND configuration (drifts to x=0)
        tx, ty = 8.0, 14.0  # Center terminal (weaker effect)
        d_terminal = np.sqrt((x - tx)**2 + (y - ty)**2)
        terminal = -0.5 * np.exp(-d_terminal**2 / (2 * 2.0**2))
        v_shape_term = -4.0 * _v_shape(x, y)  # Repulsion from center
    
    return (terminal + drift_x + 1.35 * drift_y + v_shape_term) * MALE_HORIZONTAL_AMP * REALITY_TENSION

def spark_refraction(x, y):
    x_c = round((x - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
    return max(0.0, min(float(N_COLS), x_c + SPARK_LEAP_DIST * np.cos(SPARK_ANGLE_RAD))), y + SPARK_LEAP_DIST * np.sin(SPARK_ANGLE_RAD)

# ==============================================================================
# PROBABILISTIC SPARK SIMULATION
# ==============================================================================
def run_simulation_probabilistic(r, q0, kappa, in_band, lambda0, rng_seed=None, debug=False):
    """
    Spark를 확률 모델로 변경.
    
    p = clamp(lambda0 * w_gate(r,q0) * dt, 0, 1)
    if rng.rand() < p: spark
    else: no spark
    """
    # RNG for reproducibility
    rng = np.random.RandomState(rng_seed)
    
    x, y = 8.0, 0.0
    memory_y = y
    switch_state = False
    renorm = 1.0
    dt = 0.05
    steps = int(1000.0 / dt)  # Extended for more contact opportunities
    
    trajectory, flashes = [], []
    
    # Instrumentation counters
    contact_count = 0
    expected_sparks = 0.0
    
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * F_1_32
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    
    # Pre-compute w_gate for this (r,q0) point
    w_gate_val = w_gate(r, q0)
    
    if debug:
        print(f"  w_gate({r:.4f}, {q0:.4f}) = {w_gate_val:.6f}")
        print(f"  kappa = {kappa:.6f}, in_band = {in_band}")
        print(f"  lambda0 = {lambda0:.4f}, dt = {dt}")
    
    for i in range(steps):
        t = i * dt
        vx = universal_field(x, y, in_band)
        
        alpha = max(0.0, min(ALPHA_MAX, dt / (hyst_tau + 1e-6)))
        memory_y = (1.0 - alpha) * memory_y + alpha * y
        lag = memory_y - y
        
        if lag < threshold_on and not switch_state: 
            switch_state = True
        elif lag > threshold_on * THRESHOLD_OFF_FACTOR and switch_state: 
            switch_state = False
        
        did_spark = False
        
        # Spark condition check (funnel + switch)
        in_funnel = (y > SPARK_GATE_Y_MIN and 
                     SPARK_FUNNEL_X_MIN < x < SPARK_FUNNEL_X_MAX)
        
        if in_funnel and switch_state:
            # Instrumentation: count contact
            contact_count += 1
            p_spark = np.clip(lambda0 * w_gate_val * dt, 0.0, 1.0)
            expected_sparks += p_spark
            
            if rng.rand() < p_spark:
                x_before = float(x)
                y_before = float(y)
                # canonical core snap (logged)
                # (computed inside renorm_terms_at_flash as well)
                x_after, y_after = spark_refraction(x_before, y_before)
                dx = x_after - x_before
                dy = y_after - y_before
                theta_obs = float(np.degrees(np.arctan2(dy, dx)))
                turn_idx = int(np.floor(y_before / Y_WRAP))

                terms = renorm_terms_at_flash(
                    renorm_before=float(renorm),
                    x_before=float(x_before),
                    w_gate=float(w_gate_val),
                    kappa=float(kappa),
                    lag=float(lag),
                    threshold_on=float(threshold_on),
                    theta_obs_deg=float(theta_obs),
                    spark_angle_deg=float(SPARK_ANGLE_DEG),
                    compression_gap=float(COMPRESSION_GAP),
                    kappa_baseline=float(F_1_32),
                )
                renorm_after = float(terms["renorm_after"])

                flashes.append({
                    "time": t, "tension_before": lag, "state_before": x,
                    "renorm_before": renorm, "kappa_at_flash": kappa,
                    "in_band": in_band,
                    "renorm_after": renorm_after,
                    "L_comp": float(terms["L_comp"]),
                    "E_pole": float(terms["E_pole"]),
                    "G_recover": float(terms["G_recover"]),
                    "x_compressed": float(terms["x_compressed"]),
                    "w_gate": w_gate_val, "p_spark": p_spark,
                    "x_before": x_before, "y_before": y_before,
                    "x_after": x_after, "y_after": y_after,
                    "theta_obs": theta_obs,
                    "turn": turn_idx, "leg": "B",
                    "lag": float(lag),
                    "lag_sign": int(np.sign(lag)) if lag != 0 else 0
                })
                x, y = x_after, y_after
                renorm = renorm_after
                switch_state = False
                memory_y = y 
                did_spark = True
        
        x += vx * renorm * dt
        y += 1.5 * dt

        renorm = renorm_step_continuous(
            renorm=float(renorm),
            w_gate=float(w_gate_val),
            kappa=float(kappa),
            lag=float(lag),
            threshold_on=float(threshold_on),
            dt=float(dt),
            compression_gap=float(COMPRESSION_GAP),
            kappa_baseline=float(F_1_32),
        )
        
        # Reflective boundary at x=0 to prevent getting stuck
        if x < 0:
            x = -x  # Bounce back
            # Add some random kick to help escape
            x += 0.5 * rng.random()
        x = min(N_COLS, x)
        
        trajectory.append({"t": t, "x": x, "y": y, "renorm": renorm, "spark": did_spark})
        if y > 30 * N_ROWS: break  # Extended vertical range
        
        if debug and i % 50 == 0:
            print(f"Step {i}: y={y:.2f}, x={x:.2f}, lag={lag:.4f}, switch={switch_state}")
    
    # Compute instrumentation metrics
    eligible_time = contact_count * dt
    spark_count = len(flashes)
    conditional_prob = spark_count / contact_count if contact_count > 0 else 0.0
    
    if debug:
        print(f"\n  [INSTRUMENTATION]")
        print(f"    contact_count: {contact_count}")
        print(f"    eligible_time: {eligible_time:.2f}s")
        print(f"    spark_count: {spark_count}")
        print(f"    expected_sparks: {expected_sparks:.2f}")
        print(f"    conditional_prob: {conditional_prob:.4f}")
            
    return trajectory, flashes, {
        "contact_count": contact_count,
        "eligible_time": eligible_time,
        "spark_count": spark_count,
        "expected_sparks": expected_sparks,
        "conditional_prob": conditional_prob,
        "p_per_dt": np.clip(lambda0 * w_gate_val * dt, 0.0, 1.0)
    }

def tune_lambda0_fixed():
    """
    Lambda0를 고정값으로 설정 (w_gate selectivity 유지).
    Target: center_in에서 flash_count 20~100
    """
    # Optional override for sweep automation.
    env_override = os.getenv("LAMBDA0_FIXED_OVERRIDE")
    if env_override is not None and env_override != "":
        lambda0 = float(env_override)
    else:
        # Keep center_in unsaturated: p_spark = lambda0 * w_gate * dt
        # For center_in w_gate~0.615 and dt=0.05, lambda0 in [3,6] gives p_spark~0.092..0.185.
        lambda0 = 5.0
    print("=" * 60)
    print(f"Using FIXED lambda0 = {lambda0}")
    print(f"  center_in: w_gate=0.615 -> p_spark ~= {lambda0 * 0.615 * 0.05:.4f} (unsaturated)")
    print(f"  r_out:     w_gate=2.9e-8 -> p_spark ~= {lambda0 * 2.9e-8 * 0.05:.2e} (suppressed)")
    print("=" * 60)
    return lambda0

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    print("=" * 70)
    print("Detune Closure Sweep V4 - Probabilistic Spark Model")
    print("=" * 70)
    
    # Step 1: Set lambda0
    lambda0 = tune_lambda0_fixed()
    
    # Step 2: Run all 4 points with fixed lambda0
    print("\n" + "=" * 70)
    print("Running 4-point sweep with calibrated lambda0...")
    print("=" * 70)
    
    summary_rows = []
    
    for i, pt in enumerate(POINTS):
        tag, r, q0 = pt["label"], pt["r"], pt["q0"]
        print(f"\n--- [{i+1}/4] Running {tag}: r={r}, q0={q0} ---")
        
        kappa = kappa_eff(r, q0)
        in_band = in_sh_band(r, q0)
        w_gate_val = w_gate(r, q0)
        
        print(f"  w_gate = {w_gate_val:.6f}, kappa = {kappa:.6f}, in_band = {in_band}")
        
        # Run with same seed for reproducibility
        traj, flashes, metrics = run_simulation_probabilistic(
            r, q0, kappa, in_band, lambda0, 
            rng_seed=RNG_SEED,
            debug=(tag == "center_in")
        )
        
        flash_count = len(flashes)
        total_time = traj[-1]["t"] if traj else 0
        flash_rate = flash_count / total_time if total_time > 0 else 0
        
        print(f"  Flash count: {flash_count}")
        print(f"  Flash rate: {flash_rate:.6f}")
        print(f"  Contact count: {metrics['contact_count']}")
        print(f"  Eligible time: {metrics['eligible_time']:.2f}s")
        print(f"  Conditional prob: {metrics['conditional_prob']:.4f}")
        print(f"  Total simulation time: {total_time:.2f}")
        
        # Save flash events
        with open(os.path.join(OUTPUT_DIR, f"flash_events_{tag}.json"), 'w') as f:
            json.dump({
                "point": {"r": r, "q0": q0, "label": tag},
                "parameters": {"lambda0": lambda0, "w_gate": w_gate_val, "kappa": kappa, "in_band": in_band},
                "flash_events": flashes
            }, f, indent=2)
        
        summary_rows.append({
            "point": tag,
            "r": r,
            "q0": q0,
            "w_gate": w_gate_val,
            "kappa": kappa,
            "in_band": in_band,
            "flash_count": flash_count,
            "flash_rate": flash_rate,
            "total_time": total_time,
            "contact_count": metrics["contact_count"],
            "eligible_time": metrics["eligible_time"],
            "expected_sparks": metrics["expected_sparks"],
            "conditional_prob": metrics["conditional_prob"],
            "p_per_dt": metrics["p_per_dt"]
        })
    
    # Save summary
    df_summary = pd.DataFrame(summary_rows)
    summary_path = os.path.join(OUTPUT_DIR, "summary.csv")
    df_summary.to_csv(summary_path, index=False)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(df_summary.to_string(index=False))
    print(f"\nSaved to: {summary_path}")
    
    # Check if band selectivity is visible
    in_band_rates = df_summary[df_summary['in_band'] == True]['flash_rate'].values
    out_band_rates = df_summary[df_summary['in_band'] == False]['flash_rate'].values
    
    if len(in_band_rates) > 0 and len(out_band_rates) > 0:
        avg_in = np.mean(in_band_rates)
        avg_out = np.mean(out_band_rates)
        ratio = avg_in / avg_out if avg_out > 0 else float('inf')
        
        print("\n" + "=" * 70)
        print("BAND SELECTIVITY CHECK")
        print("=" * 70)
        print(f"  Avg flash rate IN-BAND:  {avg_in:.6f}")
        print(f"  Avg flash rate OUT-BAND: {avg_out:.6f}")
        print(f"  Ratio (in/out):          {ratio:.2f}x")
        if ratio > 1.5:
            print("  [OK] Band selectivity VISIBLE")
        else:
            print("  [WEAK] Band selectivity WEAK")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
