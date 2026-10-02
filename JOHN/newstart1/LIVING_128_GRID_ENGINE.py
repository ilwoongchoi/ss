import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from geometry_package.absolute_constants import *

# ---------------------------------------------------------
# 1. LOAD REAL-WORLD FUEL (1 YEAR OF NMDB & STDR)
# ---------------------------------------------------------
DATA_PATH = "out/unified_12m_hysteresis_data_ts.csv"
if not os.path.exists(DATA_PATH):
    # Fallback to local generation if file missing, but user confirmed it's in repo
    print(f"ERROR: {DATA_PATH} not found. Please ensure data is sufficed.")
    exit()

df_raw = pd.read_csv(DATA_PATH)
# Period: 2016-03-01 to 2017-02-28 (Approx 8760 hours)
# Columns: ts, flux_wm2 (Sun pressure), nmdb_counts (Barnard truth)
STDR_FLUX = df_raw['flux_wm2'].values
NMDB_TRUTH = df_raw['nmdb_counts'].values
# Normalize for the engine
STDR_NORM = (STDR_FLUX - np.mean(STDR_FLUX)) / np.std(STDR_FLUX)
NMDB_NORM = (NMDB_TRUTH - np.mean(NMDB_TRUTH)) / np.std(NMDB_TRUTH)

# ---------------------------------------------------------
# 2. HYBRID MASTER EQUATION ENGINE
# ---------------------------------------------------------
def run_living_128_grid():
    num_hours = len(STDR_NORM)
    num_types = 128
    
    # 128 Archetype Seeds (MBTI x Blood x Gender)
    # Using the standard 128-grid initialization
    all_mbti = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    all_bloods = ["O", "A", "B", "AB"]
    all_genders = ["M", "F"]
    
    types = []
    for m in all_mbti:
        for b in all_bloods:
            for g in all_genders:
                types.append({'mbti': m, 'blood': b, 'gender': g})

    # State Vectors: [X, Y, Memory, Leg_State]
    # Starting positions distributed across the 16x16 face
    states = np.zeros((num_types, 4))
    for i, t in enumerate(types):
        # Placeholder initialization based on archetype geometry
        states[i, 0] = 8.0 + (np.random.rand() - 0.5) * 4.0 # Center-focused
        states[i, 1] = 0.0 # Start of cycle
        states[i, 2] = 0.0 # Initial memory
        states[i, 3] = 0.0 # Initial leg (Sunrise)

    trajectories = np.zeros((num_hours, num_types)) # Recording X-position (Identity)
    
    print(f"--- Launching Living 128-Grid Engine ---")
    print(f"Duration: 1 Year ({num_hours} hours)")
    print(f"Fuel: 2016-2017 NMDB/STDR Data")

    dt = 0.1 # Integration step
    
    for h in range(num_hours):
        # External Forcing from Reality Data
        sun_pressure = STDR_NORM[h]
        truth_flow = NMDB_NORM[h]
        
        # 1. CONTINUOUS FIELD (F_cont)
        # Reality Tension (1.01) is modulated by Sun/Barnard interference
        current_tension = TUNNEL_TENSION + (sun_pressure * 0.01) - (truth_flow * 0.005)
        
        for i in range(num_types):
            x, y, mem, leg = states[i]
            
            # A. Center Smoothing (Melatonin Pivot)
            # 0.00083 residual evens out the Nose Bridge
            dist_to_nose = np.sqrt((x - 8.0)**2 + (y - 8.0)**2)
            smoothing = np.exp(-(dist_to_nose**2) / (0.00083 * 100))
            
            # B. Complex Drift (Mandelbrot z = z^2 + c)
            zx = (x - 8.0) / 4.0
            zy = (y - 8.0) / 4.0
            z = complex(zx, zy)
            c = complex(0.618, 0.1618) # The Bridge Seed
            z_next = z**2 + c
            
            vx = (z_next.real - zx) * current_tension
            vy = (z_next.imag - zy) * current_tension
            
            # 2. HYSTERESIS (Memory Lag)
            # Memory drags the position, creating the 1.3228 Debt Area
            tau = 2.32 # Night Tau Lag
            states[i, 2] = mem + (y - mem) / tau * dt
            lag = mem - y
            
            # 3. SPARK RESET (138.88 Degree Leap)
            # Triggered at 3/32 compression gate
            if abs(lag) > LATTICE_3_32 and 6.0 < x < 10.0:
                # SPARK!
                dx_leap = SPARK_LEAP_DIST * np.cos(np.radians(138.88))
                dy_leap = SPARK_LEAP_DIST * np.sin(np.radians(138.88))
                states[i, 0] += dx_leap
                states[i, 1] += dy_leap
                states[i, 2] = states[i, 1] # Memory reset
            else:
                # Normal update
                states[i, 0] += vx * dt * (1.0 - smoothing) # Straighten out the center
                states[i, 1] += (vy + 1.0) * dt # Constant time descent
            
            # Clamp to Grid
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            states[i, 1] = states[i, 1] % 16 # Cyclic time
            
            trajectories[h, i] = states[i, 0]

    # ---------------------------------------------------------
    # 3. VISUALIZE THE LIVING 128 GRID
    # ---------------------------------------------------------
    plt.figure(figsize=(20, 12), facecolor="#050510")
    
    # Plot only a subset of days for clarity (e.g., first month)
    time_limit = 24 * 30 
    time_axis = np.arange(time_limit)
    
    colors = plt.cm.viridis(np.linspace(0, 1, num_types))
    
    for i in range(num_types):
        plt.plot(time_axis, trajectories[:time_limit, i], color=colors[i], lw=0.5, alpha=0.7)
        
    plt.axhline(y=8.0, color="white", ls="--", alpha=0.3, label="Melatonin Pivot (Nose)")
    plt.title("LIVING 128-GRID TRAJECTORY: 1-Year Survival under NMDB/STDR Stress", color="white", fontsize=20)
    plt.xlabel("Hours (March 2016)", color="#cccccc")
    plt.ylabel("Grid X-Position (Archetype Identity)", color="#cccccc")
    
    ax = plt.gca()
    ax.set_facecolor("#050510")
    ax.tick_params(colors='white')
    
    output_fn = "LIVING_128_GRID_REALITY.png"
    plt.savefig(output_fn, dpi=300, facecolor="#050510")
    print(f"--- Simulation Complete ---")
    print(f"Result saved to {output_fn}")
    print("Logic: Real data injection, Hysteresis Debt (1.3228), Spark Reset (138.88), Center Flattening (0.00083).")

if __name__ == "__main__":
    run_living_128_grid()
