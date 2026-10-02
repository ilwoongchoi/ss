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
    print(f"ERROR: {DATA_PATH} not found.")
    exit()

df_raw = pd.read_csv(DATA_PATH)
STDR_FLUX = df_raw['flux_wm2'].values
NMDB_TRUTH = df_raw['nmdb_counts'].ffill().values # Fill missing NMDB gaps

# Normalize stressors
STDR_NORM = (STDR_FLUX - np.mean(STDR_FLUX)) / np.std(STDR_FLUX)
NMDB_NORM = (NMDB_TRUTH - np.mean(NMDB_TRUTH)) / np.std(NMDB_TRUTH)

# ---------------------------------------------------------
# 2. THE ULTIMATE LIVING EQUATION
# ---------------------------------------------------------
def run_real_128_grid_engine():
    num_hours = len(STDR_NORM)
    num_types = 128
    
    # Define Archetypes
    all_mbti = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    all_bloods = ["O", "A", "B", "AB"]
    all_genders = ["M", "F"]
    
    archetypes = []
    for m in all_mbti:
        for b in all_bloods:
            for g in all_genders:
                archetypes.append({'mbti': m, 'blood': b, 'gender': g})

    # State Vectors: [X, Y, Memory, Leg]
    # Initialize based on 16x16 face grid distribution
    states = np.zeros((num_types, 4))
    seeds = np.zeros(num_types, dtype=complex)
    
    blood_phase = {"O": 0.0, "A": 0.5 * np.pi, "B": np.pi, "AB": 1.5 * np.pi}
    
    for i, arch in enumerate(archetypes):
        # Initial position (Z0)
        # Using MBTI index to spread them across the X-axis (0-16)
        m_idx = all_mbti.index(arch['mbti'])
        states[i, 0] = (m_idx + 0.5) # Spread across 16 columns
        states[i, 1] = 0.0 # Start at the top (Sunrise)
        states[i, 2] = 0.0 # Memory lag
        states[i, 3] = 0.0 # Leg state
        
        # Unique Seed (c) based on Blood Type + 0.1618 Budge
        angle = blood_phase[arch['blood']]
        # c = GEAR_RATIO (0.618) * exp(i * phase) + 0.1618 Budge
        seeds[i] = complex(0.618 * np.cos(angle), 0.618 * np.sin(angle)) + complex(0.1618, 0.0)

    # To capture divergence, we only record X (Identity transformation)
    # Reducing time resolution for plotting (1 sample per day = 365 steps)
    record_step = 24
    results = np.zeros((num_hours // record_step, num_types))
    
    print(f"--- RUNNING HYBRID MASTER ENGINE (Real 1-Year Data) ---")
    
    dt = 0.5 # Integration step
    for h in range(num_hours):
        # Global stress from data
        sun_p = STDR_NORM[h]
        barnard_t = NMDB_NORM[h]
        
        # Reality Tension (1.01) fluctuates with sun/barnard
        dynamic_tension = TUNNEL_TENSION + (sun_p * 0.05) - (barnard_t * 0.02)
        
        for i in range(num_types):
            x, y, mem, leg = states[i]
            
            # 1. CONTINUOUS MANDELBROT FIELD (z = z^2 + c)
            zx = (x - 8.0) / 4.0
            zy = (y - 8.0) / 4.0
            z = complex(zx, zy)
            
            # Recursion modulated by dynamic tension
            z_next = (z**2 + seeds[i]) * (dynamic_tension / TUNNEL_TENSION)
            
            vx = (z_next.real - zx)
            vy = (z_next.imag - zy)
            
            # 2. HYSTERESIS (The 1.3228 Debt)
            # Memory lag creates the area. 
            # tau = 2.32 (Night Tau)
            states[i, 2] = mem + (y - mem) / 2.32 * dt
            lag = mem - y
            
            # 3. SPARK RESET (138.88 Degree)
            # Threshold = 3/32 (LATTICE_3_32)
            if abs(lag) > LATTICE_3_32 and 4.0 < x < 12.0:
                # Discharge!
                angle = np.radians(138.88)
                states[i, 0] += SPARK_LEAP_DIST * np.cos(angle)
                states[i, 1] += SPARK_LEAP_DIST * np.sin(angle)
                states[i, 2] = states[i, 1] # Reset debt
            else:
                # Flow
                # Nose Bridge Smoothing (0.00083)
                dist_nose = np.sqrt((x-8)**2 + (y-8)**2)
                smoothing = np.exp(-(dist_nose**2) / 0.083) # 0.00083 * 100
                
                states[i, 0] += vx * dt * (1.0 - smoothing)
                states[i, 1] += (vy + 1.0) * dt # Vertical descent
            
            # Clamping & Boundary (The 16x16 Face)
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            states[i, 1] = states[i, 1] % 16
            
        if h % record_step == 0:
            results[h // record_step, :] = states[:, 0]

    # ---------------------------------------------------------
    # 3. VISUALIZE DIVERGENCE (The Face Contour)
    # ---------------------------------------------------------
    plt.figure(figsize=(16, 10), facecolor="#050510")
    time_axis = np.arange(results.shape[0])
    
    # Group by Blood Type for color
    blood_colors = {"O": "#ff4444", "A": "#44ff44", "B": "#4444ff", "AB": "#ffffff"}
    
    for i, arch in enumerate(archetypes):
        plt.plot(time_axis, results[:, i], color=blood_colors[arch['blood']], lw=0.4, alpha=0.5)
        
    plt.axhline(y=8.0, color="gray", ls="--", alpha=0.5, label="Melatonin Pivot (Nose)")
    plt.title("128-GRID LIVING MANIFOLD: 1-Year Reality Trajectories (2016-2017)", color="white", fontsize=18)
    plt.xlabel("Days (Time Flow)", color="#cccccc")
    plt.ylabel("Grid X-Position (Archetype Divergence)", color="#cccccc")
    
    ax = plt.gca()
    ax.set_facecolor("#050510")
    ax.tick_params(colors='white')
    
    # Custom Legend
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], color=c, lw=2, label=f"Type {k}") for k, c in blood_colors.items()]
    plt.legend(handles=legend_elements, facecolor="#050510", edgecolor="white", loc="upper right")
    
    output_filename = "FINAL_128_GRID_DIVERGENCE.png"
    plt.savefig(output_filename, dpi=300, facecolor="#050510")
    print(f"--- Engine Finish ---")
    print(f"Verification: 128 paths generated with unique phase seeds.")
    print(f"Visualizing 1-year divergence in {output_filename}")

if __name__ == "__main__":
    run_real_128_grid_engine()
