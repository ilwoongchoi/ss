import numpy as np
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# ==============================================================================
# CONFIGURATION
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

# Physical Constants
N_ROWS = 16
N_COLS = 16
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = np.radians(SPARK_ANGLE_DEG)
SPARK_LEAP_DIST = 4.0
F_1_32 = 1/32.0
COMPRESSION_GAP = 3.0 * F_1_32

# Field & Dynamics Constants
REALITY_TENSION = 1.0
MALE_HORIZONTAL_AMP = 1.2
TORSION_4D = 0.111
GABA_C_V_APEX = 0.14

# --- TUNED PARAMETERS FOR FLASHING ---
# We need enough lag to trigger the switch.
# Alpha = dt / hyst_tau. Smaller alpha = more lag.
# hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE).
# To get smaller alpha, we need larger hyst_tau, so smaller SCALE.
HYST_TAU_SCALE = 0.5  # Reduced from 1.5 to increase lag
THRESHOLD_ON_FACTOR = 0.2 # Reduced from 0.6 to make triggering easier
THRESHOLD_OFF_FACTOR = 0.3
ALPHA_MAX = 0.5
NIGHT_TAU_LAG = SPARK_ANGLE_DEG / 60.0

# Spark Gate Geometry
SPARK_FUNNEL_X_MIN = 6.0
SPARK_FUNNEL_X_MAX = 10.0
SPARK_GATE_Y_MIN = 8.0 # Lowered from 10.0 to catch earlier sparks if needed

# ==============================================================================
# LOGIC
# ==============================================================================
def load_data():
    if not os.path.exists(CONSTANTS_PATH):
        # Fallback constants
        constants = {'calibrated': {'CALIBRATED_SH_BOUNDARY_MIN': 0.1116, 'CALIBRATED_SH_BOUNDARY_MAX': 0.1126, 'CALIBRATED_Q0_MIN': 0.961, 'CALIBRATED_Q0_MAX': 0.983}}
    else:
        with open(CONSTANTS_PATH, 'r') as f:
            constants = json.load(f)
    
    if not os.path.exists(DIST_DATA_PATH):
        df = pd.DataFrame()
    else:
        df = pd.read_csv(DIST_DATA_PATH)
    return constants, df

def get_kappa_eff(r, q0, df):
    if df.empty: return 1/32.0
    dists = np.sqrt((df['r'] - r)**2 + (df['q0'] - q0)**2)
    row = df.iloc[dists.idxmin()]
    return float(row['kappa_tda']) if 'kappa_tda' in row else 1/32.0

def check_in_band(r, q0, constants):
    band = constants.get('calibrated', {})
    r_min = band.get('CALIBRATED_SH_BOUNDARY_MIN', 0.1116)
    r_max = band.get('CALIBRATED_SH_BOUNDARY_MAX', 0.1126)
    q0_min = band.get('CALIBRATED_Q0_MIN', 0.961)
    q0_max = band.get('CALIBRATED_Q0_MAX', 0.983)
    return (r_min <= r <= r_max) and (q0_min <= q0 <= q0_max)

def _v_shape(x, y):
    xn, yn = (x - 8.0) / 8.0, (y - 8.0) / 8.0
    return np.exp(-(xn**2 + yn**2) / (2 * (GABA_C_V_APEX ** 2)))

def universal_field(x, y):
    tx, ty = 3.2, 14.0
    d_terminal = np.sqrt((x - tx)**2 + (y - ty)**2)
    terminal = -2.5 * np.exp(-d_terminal**2 / (2 * 1.5**2))
    drift_x = -TORSION_4D * (y - 8.0)
    drift_y = TORSION_4D * (x - 8.0)
    return (terminal + drift_x + 1.35 * drift_y + 1.2 * _v_shape(x, y)) * MALE_HORIZONTAL_AMP * REALITY_TENSION

def spark_refraction(x, y):
    x_c = round((x - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
    # Spark jumps to the RIGHT and UP
    return max(0.0, min(float(N_COLS), x_c + SPARK_LEAP_DIST * np.cos(SPARK_ANGLE_RAD))), y + SPARK_LEAP_DIST * np.sin(SPARK_ANGLE_RAD)

def run_simulation(r, q0, kappa, in_band, debug=False):
    x, y = 8.0, 0.0
    memory_y = y
    switch_state = False
    renorm = 1.0
    dt = 0.05
    steps = int(300.0 / dt)
    
    trajectory, flashes = [], []
    
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * F_1_32
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    
    # KAPPA DEPENDENT RENORM LOGIC
    if in_band:
        reset_val = 0.380657
        recovery_rate = 0.05
    else:
        # Out-of-band: Weaker reset (less energy loss), slower recovery
        dev = abs(kappa - 1/32.0) / (1/32.0)
        reset_val = min(0.9, 0.380657 + dev * 0.4)
        recovery_rate = 0.02 
        
    for i in range(steps):
        t = i * dt
        vx = universal_field(x, y)
        
        # Hysteresis
        alpha = max(0.0, min(ALPHA_MAX, dt / (hyst_tau + 1e-6)))
        memory_y = (1.0 - alpha) * memory_y + alpha * y
        lag = memory_y - y
        
        # Switch Logic
        if lag < threshold_on and not switch_state: 
            switch_state = True
        elif lag > threshold_on * THRESHOLD_OFF_FACTOR and switch_state: 
            switch_state = False
            
        # Spark Gate Logic
        did_spark = False
        if y > SPARK_GATE_Y_MIN and switch_state and SPARK_FUNNEL_X_MIN < x < SPARK_FUNNEL_X_MAX:
            flashes.append({
                "time": t, "tension_before": lag, "state_before": x,
                "renorm_before": renorm, "kappa_at_flash": kappa,
                "in_band": in_band, "renorm_after": reset_val
            })
            x, y = spark_refraction(x, y)
            renorm = reset_val
            switch_state = False
            memory_y = y # Reset memory
            did_spark = True
            
        # Move
        x += vx * renorm * dt
        y += 1.5 * dt # Constant upward drive
        renorm += (1.0 - renorm) * recovery_rate * dt
        x = max(0, min(N_COLS, x))
        
        trajectory.append({"t": t, "x": x, "y": y, "renorm": renorm, "spark": did_spark})
        if y > N_ROWS: break
        
        if debug and i % 50 == 0:
            print(f"Step {i}: y={y:.2f}, lag={lag:.4f}, thresh={threshold_on:.4f}, switch={switch_state}")
            
    return trajectory, flashes

def main():
    constants, df = load_data()
    summary_rows = []
    
    for pt in POINTS:
        tag, r, q0 = pt["label"], pt["r"], pt["q0"]
        print(f"\n--- Running {tag} ---")
        kappa = get_kappa_eff(r, q0, df)
        in_band = check_in_band(r, q0, constants)
        
        # Run simulation
        traj, flashes = run_simulation(r, q0, kappa, in_band, debug=(tag=="center_in"))
        print(f"Flashes detected: {len(flashes)}")
        
        # Save JSON
        with open(os.path.join(OUTPUT_DIR, f"flash_events_{tag}.json"), 'w') as f:
            json.dump({"flash_events": flashes}, f, indent=2)
            
        # Plot
        plt.figure(figsize=(10, 8))
        ts, xs, ys, rs = zip(*[(p['t'], p['x'], p['y'], p['renorm']) for p in traj])
        
        plt.subplot(2,2,1)
        plt.plot(xs, ys, 'b-'); plt.title(f"{tag} Trajectory")
        plt.xlim(0, 16); plt.ylim(0, 16)
        if flashes:
            fx, fy = zip(*[(p['x'], p['y']) for p in traj if p['spark']])
            plt.plot(fx, fy, 'r*', markersize=12)
            
        plt.subplot(2,2,2); plt.plot(ts, rs, 'g-'); plt.title("Renorm")
        plt.subplot(2,2,3); plt.plot(ts, xs, 'k-'); plt.title("X vs Time")
        
        # Renorm distribution or text
        plt.subplot(2, 2, 4)
        if flashes:
            plt.hist([f['renorm_after'] for f in flashes], bins=5)
            plt.title("Renorm Reset Values")
        else:
            plt.text(0.5, 0.5, "No Flashes", ha='center')
            
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, f"QUASAR_KAPPA_TDA_{tag}.png"))
        plt.close()
        
        summary_rows.append({
            "tag": tag, "kappa": kappa, "in_band": in_band, 
            "flashes": len(flashes), 
            "renorm_mean": np.mean([f['renorm_after'] for f in flashes]) if flashes else 0
        })
        
    pd.DataFrame(summary_rows).to_csv(os.path.join(OUTPUT_DIR, "summary.csv"), index=False)
    print("\nDone. Results in out/detune_closure_sweep/")

if __name__ == "__main__":
    main()
