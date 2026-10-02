import numpy as np
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
CONSTANTS_PATH = "out/geometry_constants_from_dist_all.json"
DIST_DATA_PATH = "out/dist_all_with_kappa.csv"
OUTPUT_DIR = "out/detune_closure_sweep"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 4 Test Points
POINTS = [
    {"label": "center_in", "r": 0.1117, "q0": 0.9750},
    {"label": "r_out",     "r": 0.1130, "q0": 0.9750},
    {"label": "q0_out",    "r": 0.1117, "q0": 0.9850},
    {"label": "both_out",  "r": 0.1130, "q0": 0.9850}
]

# Physical Constants (from generate_128_grid_v4_hysteresis_pure.py)
N_ROWS = 16
N_COLS = 16
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = np.radians(SPARK_ANGLE_DEG)
SPARK_LEAP_DIST = 4.0  # Approx, tuning to match grid
F_1_32 = 1/32.0
COMPRESSION_GAP = 3.0 * F_1_32

# Field Constants
REALITY_TENSION = 1.0
MALE_HORIZONTAL_AMP = 1.2
FEMALE_HORIZONTAL_AMP = 2.8
TORSION_4D = 0.111
GABA_C_V_APEX = 0.14

# Hysteresis Constants
HYST_TAU_SCALE = 1.5
THRESHOLD_ON_FACTOR = 0.6
THRESHOLD_OFF_FACTOR = 0.3
ALPHA_MAX = 0.5
NIGHT_TAU_LAG = SPARK_ANGLE_DEG / 60.0

# Spark Gate
SPARK_FUNNEL_X_MIN = 6.0
SPARK_FUNNEL_X_MAX = 10.0
SPARK_GATE_Y_MIN = 10.0

# Twilight Bands
TWILIGHT_1_LO = 1.0
TWILIGHT_1_HI = 3.5
TWILIGHT_2_LO = 8.5
TWILIGHT_2_HI = 11.5

# ==============================================================================
# DATA LOADING & LOOKUP
# ==============================================================================
def load_data():
    if not os.path.exists(CONSTANTS_PATH):
        raise FileNotFoundError(f"{CONSTANTS_PATH} not found")
    with open(CONSTANTS_PATH, 'r') as f:
        constants = json.load(f)
    
    if not os.path.exists(DIST_DATA_PATH):
        raise FileNotFoundError(f"{DIST_DATA_PATH} not found")
    df = pd.read_csv(DIST_DATA_PATH)
    
    return constants, df

def get_kappa_eff(r, q0, df):
    # Euclidean distance in (r, q0) space
    dists = np.sqrt((df['r'] - r)**2 + (df['q0'] - q0)**2)
    nearest_idx = dists.idxmin()
    row = df.iloc[nearest_idx]
    
    # If kappa_tda column exists, use it, else generic
    if 'kappa_tda' in row:
        return float(row['kappa_tda'])
    return 1/32.0  # Fallback

def check_in_band(r, q0, constants):
    band = constants.get('calibrated', {})
    r_min = band.get('CALIBRATED_SH_BOUNDARY_MIN', 0.1116)
    r_max = band.get('CALIBRATED_SH_BOUNDARY_MAX', 0.1126)
    q0_min = band.get('CALIBRATED_Q0_MIN', 0.961)
    q0_max = band.get('CALIBRATED_Q0_MAX', 0.983)
    
    in_r = r_min <= r <= r_max
    in_q0 = q0_min <= q0 <= q0_max
    return in_r and in_q0

# ==============================================================================
# PHYSICS ENGINE
# ==============================================================================
def _v_shape(x, y):
    xn = (x - 8.0) / 8.0
    yn = (y - 8.0) / 8.0
    r_sq = xn * xn + yn * yn
    return np.exp(-r_sq / (2 * (GABA_C_V_APEX ** 2)))

def universal_triple_basin_field(x, y, gender="M"):
    # Simplified field for trajectory context
    tx, ty = 3.2, 14.0
    d_terminal = np.sqrt((x - tx) ** 2 + (y - ty) ** 2)
    terminal_attractor = -2.5 * np.exp(-d_terminal ** 2 / (2 * 1.5 ** 2))

    drift_x = -TORSION_4D * (y - 8.0)
    drift_y = TORSION_4D * (x - 8.0)

    amp = MALE_HORIZONTAL_AMP if gender == "M" else FEMALE_HORIZONTAL_AMP
    return (terminal_attractor + drift_x + 1.35 * drift_y + 1.2 * _v_shape(x, y)) * amp * REALITY_TENSION

def spark_refraction(x, y):
    x_compressed = round((x - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
    dx = SPARK_LEAP_DIST * np.cos(SPARK_ANGLE_RAD)
    dy = SPARK_LEAP_DIST * np.sin(SPARK_ANGLE_RAD)
    return max(0.0, min(float(N_COLS), x_compressed + dx)), y + dy

def get_renorm_reset_value(kappa, in_band):
    """
    Reset value for renormalization after a flash.
    Dependent on kappa as requested.
    """
    if in_band:
        return 0.3806568854998805  # Historical hard lock
    else:
        # Out of band: Weaker reset (less energy loss)
        # Scale linearly: at kappa=1/32 -> 0.38, at kappa=1/16 -> 0.8
        target = 0.380657 + (abs(kappa - 1/32.0) / (1/32.0)) * 0.4
        return min(0.9, target)

def run_simulation(r, q0, kappa, in_band):
    # Initial State
    x, y = 8.0, 0.0  # Start bottom center
    memory_y = y
    switch_state = False
    renorm = 1.0
    
    # Time params
    dt = 0.05
    t_max = 300.0  # Sufficient for full traversal
    steps = int(t_max / dt)
    
    trajectory = []
    flashes = []
    
    # Hysteresis params
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * F_1_32
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    threshold_off = threshold_on * THRESHOLD_OFF_FACTOR
    
    for i in range(steps):
        t = i * dt
        
        # 1. Calculate Forces
        vx_field = universal_triple_basin_field(x, y)
        vy_const = 1.5  # Constant upward drift
        
        # 2. Hysteresis Update
        # Alpha depends on renorm (lower renorm = slower adaptation?)
        alpha = max(0.0, min(ALPHA_MAX, dt / (hyst_tau + 1e-6)))
        memory_y = (1.0 - alpha) * memory_y + alpha * y
        lag = memory_y - y
        
        # 3. Switch Logic
        if lag < threshold_on and not switch_state:
            switch_state = True
        elif lag > threshold_off and switch_state:
            switch_state = False
            
        # 4. Spark Gate Logic
        did_spark = False
        if y > SPARK_GATE_Y_MIN and switch_state and SPARK_FUNNEL_X_MIN < x < SPARK_FUNNEL_X_MAX:
            # SPARK EVENT
            renorm_before = renorm
            renorm_after_val = get_renorm_reset_value(kappa, in_band)
            
            flashes.append({
                "time": t,
                "tension_before": lag, # Approximation of tension
                "state_before": x,
                "renorm_before": renorm_before,
                "kappa_at_flash": kappa,
                "in_band": in_band,
                "state_after": -1.0, # Placeholder
                "renorm_after": renorm_after_val
            })
            
            # Refract
            x, y = spark_refraction(x, y)
            renorm = renorm_after_val
            switch_state = False
            memory_y = y # Reset memory
            did_spark = True
            
        # 5. Apply Motion
        # Renorm affects how strongly the field pulls vs inertia
        # In this simplified model, we scale field effect by renorm
        x += vx_field * renorm * dt
        y += vy_const * dt
        
        # 6. Renorm Recovery
        # Recovers back to 1.0 over time
        recovery_rate = 0.05
        if not in_band:
            recovery_rate = 0.02 # Slower recovery out of band
            
        renorm += (1.0 - renorm) * recovery_rate * dt
        
        # Boundaries
        x = max(0, min(N_COLS, x))
        
        trajectory.append({
            "t": t, "x": x, "y": y, "renorm": renorm, "spark": did_spark
        })
        
        if y > N_ROWS:
            break
            
    return trajectory, flashes

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    print(f"Running Detune Sweep Closure...")
    constants, df = load_data()
    
    summary_rows = []
    
    for point in POINTS:
        tag = point["label"]
        r = point["r"]
        q0 = point["q0"]
        
        print(f"--- Processing {tag} (r={r}, q0={q0}) ---")
        
        # 1. Parameters
        kappa = get_kappa_eff(r, q0, df)
        in_band = check_in_band(r, q0, constants)
        print(f"  Kappa: {kappa:.6f}, In Band: {in_band}")
        
        # 2. Simulation
        traj, flashes = run_simulation(r, q0, kappa, in_band)
        print(f"  Flashes: {len(flashes)}")
        
        # 3. Outputs
        # a) JSON
        json_path = os.path.join(OUTPUT_DIR, f"flash_events_{tag}.json")
        with open(json_path, 'w') as f:
            json.dump({"flash_events": flashes}, f, indent=2)
            
        # b) PNG (Phase Plot)
        plt.figure(figsize=(10, 8))
        ts = [p['t'] for p in traj]
        xs = [p['x'] for p in traj]
        ys = [p['y'] for p in traj]
        rs = [p['renorm'] for p in traj]
        
        plt.subplot(2, 2, 1)
        plt.plot(xs, ys, 'b-')
        spark_xs = [p['x'] for p in traj if p['spark']]
        spark_ys = [p['y'] for p in traj if p['spark']]
        plt.plot(spark_xs, spark_ys, 'r*', markersize=10)
        plt.title(f"{tag}: Trajectory (r={r}, q0={q0})")
        plt.xlabel("X (Grid)")
        plt.ylabel("Y (Time)")
        plt.xlim(0, 16); plt.ylim(0, 16)
        plt.grid(True)
        
        plt.subplot(2, 2, 2)
        plt.plot(ts, rs, 'g-')
        plt.title(f"Renormalization (kappa={kappa:.4f})")
        plt.xlabel("Time")
        plt.ylabel("Renorm Factor")
        plt.grid(True)
        
        plt.subplot(2, 2, 3)
        plt.plot(ts, xs, 'k-')
        plt.title("X position vs Time")
        plt.grid(True)
        
        plt.subplot(2, 2, 4)
        if flashes:
            renorms_after = [f['renorm_after'] for f in flashes]
            plt.hist(renorms_after, bins=10)
            plt.title(f"Renorm Reset Values (Avg: {np.mean(renorms_after):.3f})")
        else:
            plt.text(0.5, 0.5, "No Flashes")
            
        png_path = os.path.join(OUTPUT_DIR, f"QUASAR_KAPPA_TDA_{tag}.png")
        plt.tight_layout()
        plt.savefig(png_path)
        plt.close()
        
        # c) Summary Row
        residual_mean = 0.0 # Placeholder logic for residual
        if flashes:
            # Simple residual proxy: diff between x and grid center
            residuals = [f['state_before'] - 8.0 for f in flashes]
            residual_mean = np.mean(residuals)
            residual_std = np.std(residuals)
            renorm_mean = np.mean([f['renorm_after'] for f in flashes])
        else:
            residual_mean = np.nan
            residual_std = np.nan
            renorm_mean = np.nan
            
        summary_rows.append({
            "tag": tag,
            "r": r,
            "q0": q0,
            "kappa_eff": kappa,
            "in_band": in_band,
            "flash_count": len(flashes),
            "flash_rate": len(flashes) / traj[-1]['t'] if traj else 0,
            "residual_mean": residual_mean,
            "residual_std": residual_std,
            "renorm_mean": renorm_mean
        })
        
    # Save Summary CSV
    summary_df = pd.DataFrame(summary_rows)
    summary_path = os.path.join(OUTPUT_DIR, "summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"\nSummary saved to {summary_path}")
    print(summary_df)

if __name__ == "__main__":
    main()