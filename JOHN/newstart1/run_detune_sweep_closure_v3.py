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
SPARK_LEAP_DIST = 2.5
F_1_32 = 1/32.0
COMPRESSION_GAP = 3.0 * F_1_32

# Field & Dynamics Constants
REALITY_TENSION = 1.0
MALE_HORIZONTAL_AMP = 1.2
# Reduced torsion to keep it stable in funnel for this test
TORSION_4D = 0.02 
GABA_C_V_APEX = 0.14

# Hysteresis - Tuned for frequent flashes
# lag ~ vy * tau. vy=1.5. tau ~ 0.05 (with scale 0.5 and lag 2.3).
# lag ~ 0.075. thresh = 0.05 * 0.2 = 0.01.
# So lag > thresh should be easy.
HYST_TAU_SCALE = 0.5  
THRESHOLD_ON_FACTOR = 0.2 
THRESHOLD_OFF_FACTOR = 0.3
ALPHA_MAX = 0.5
NIGHT_TAU_LAG = SPARK_ANGLE_DEG / 60.0

# Spark Gate Geometry - NARROW FUNNEL for production
SPARK_FUNNEL_X_MIN = 6.0
SPARK_FUNNEL_X_MAX = 10.0
SPARK_GATE_Y_MIN = 10.0

# ==============================================================================
# LOGIC
# ==============================================================================
def load_data():
    if not os.path.exists(CONSTANTS_PATH):
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
    
    if in_band:
        reset_val = 0.380657
        recovery_rate = 0.05
    else:
        # Scale reset
        dev = abs(kappa - 1/32.0) / (1/32.0)
        reset_val = min(0.9, 0.380657 + dev * 0.4)
        recovery_rate = 0.02
        
    for i in range(steps):
        t = i * dt
        vx = universal_field(x, y)
        
        alpha = max(0.0, min(ALPHA_MAX, dt / (hyst_tau + 1e-6)))
        memory_y = (1.0 - alpha) * memory_y + alpha * y
        lag = memory_y - y
        
        if lag < threshold_on and not switch_state: 
            switch_state = True
        elif lag > threshold_on * THRESHOLD_OFF_FACTOR and switch_state: 
            switch_state = False
            
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
            memory_y = y 
            did_spark = True
            
        x += vx * renorm * dt
        y += 1.5 * dt
        renorm += (1.0 - renorm) * recovery_rate * dt
        x = max(0, min(N_COLS, x))
        
        trajectory.append({"t": t, "x": x, "y": y, "renorm": renorm, "spark": did_spark})
        if y > 10 * N_ROWS: break # Allow multiple cycles
        
        if debug and i % 50 == 0:
            print(f"Step {i}: y={y:.2f}, x={x:.2f}, lag={lag:.4f}, thresh={threshold_on:.4f}, switch={switch_state}")
            
    return trajectory, flashes

def main():
    constants, df = load_data()
    summary_rows = []
    
    print("Running Detune Closure Sweep (V3)...")
    
    for pt in POINTS:
        tag, r, q0 = pt["label"], pt["r"], pt["q0"]
        print(f"\n--- Running {tag} ---")
        kappa = get_kappa_eff(r, q0, df)
        in_band = check_in_band(r, q0, constants)
        
        traj, flashes = run_simulation(r, q0, kappa, in_band, debug=(tag=="center_in"))
        print(f"Flashes detected: {len(flashes)}")
        
        # Save JSON
        with open(os.path.join(OUTPUT_DIR, f"flash_events_{tag}.json"), 'w') as f:
            json.dump({"flash_events": flashes}, f, indent=2)
            
        # Plot
        plt.figure(figsize=(10, 8))
        ts, xs, ys, rs = zip(*[(p['t'], p['x'], p['y'], p['renorm']) for p in traj])
        
        plt.subplot(2,2,1); plt.plot(xs, ys, 'b-'); plt.title(f"{tag} Trajectory")
        plt.xlim(0, 16); plt.ylim(0, 16)
        plt.axvline(SPARK_FUNNEL_X_MIN, ls=':', c='g')
        plt.axvline(SPARK_FUNNEL_X_MAX, ls=':', c='g')
        if flashes:
            fx, fy = zip(*[(p['x'], p['y']) for p in traj if p['spark']])
            plt.plot(fx, fy, 'r*', markersize=12)
            
        plt.subplot(2,2,2); plt.plot(ts, rs, 'g-'); plt.title("Renorm")
        plt.subplot(2,2,3); plt.plot(ts, xs, 'k-'); plt.title("X vs Time")
        plt.subplot(2,2,4)
        if flashes:
            plt.hist([f['renorm_after'] for f in flashes], bins=5)
            plt.title("Renorm Reset")
        else:
            plt.text(0.5, 0.5, "No Flashes", ha='center')
            
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, f"QUASAR_KAPPA_TDA_{tag}.png"))
        plt.close()
        
        residuals = []
        if flashes:
            for f in flashes:
                x_before = f['state_before']
                x_compressed = round((x_before - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
                residuals.append(x_before - x_compressed)
            
        renorms = [f['renorm_after'] for f in flashes] if flashes else []
        summary_rows.append({
            "tag": tag, "r": r, "q0": q0, "kappa_eff": kappa, "in_band": in_band,
            "flash_count": len(flashes),
            "flash_rate": len(flashes) / traj[-1]['t'] if traj else 0,
            "residual_mean": np.mean(residuals) if residuals else np.nan,
            "residual_std": np.std(residuals) if residuals else np.nan,
            "renorm_mean": np.mean(renorms) if renorms else np.nan,
            "renorm_min": np.min(renorms) if renorms else np.nan,
            "renorm_max": np.max(renorms) if renorms else np.nan
        })
        
    pd.DataFrame(summary_rows).to_csv(os.path.join(OUTPUT_DIR, "summary.csv"), index=False)
    
    # Print comparison table
    print("\n" + "="*110)
    print(f"{'tag':<12} | {'kappa_eff':<10} | {'in_band':<7} | {'flash_count':<11} | {'flash_rate':<10} | {'residual_mean/std':<20} | {'renorm_after_mean':<17}")
    print("-" * 110)
    for row in summary_rows:
        rm = row['residual_mean']
        rs = row['residual_std']
        r_str = f"{rm:.4f}/{rs:.4f}" if not np.isnan(rm) else "NaN"
        print(f"{row['tag']:<12} | {row['kappa_eff']:.5f}    | {str(row['in_band']):<7} | {row['flash_count']:<11} | {row['flash_rate']:.3f}      | {r_str:<20} | {row['renorm_mean']:.3f}")
    print("="*110 + "\n")

    print("\nDone.")

if __name__ == "__main__":
    main()
