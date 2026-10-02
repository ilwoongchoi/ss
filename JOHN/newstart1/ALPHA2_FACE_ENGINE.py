import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from geometry_package.absolute_constants import *

# ---------------------------------------------------------
# 1. LOAD REAL-WORLD DATA (2016-2017 NMDB/STDR)
# ---------------------------------------------------------
DATA_PATH = "out/unified_12m_hysteresis_data_ts.csv"
df_raw = pd.read_csv(DATA_PATH)
STDR_NORM = (df_raw['flux_wm2'].values - np.mean(df_raw['flux_wm2'].values)) / np.std(df_raw['flux_wm2'].values)
NMDB_NORM = (df_raw['nmdb_counts'].ffill().values - np.mean(df_raw['nmdb_counts'].ffill().values)) / np.std(df_raw['nmdb_counts'].ffill().values)

# ---------------------------------------------------------
# 2. THE ALPHA-2 DUAL-MARGIN ENGINE (PURE PHYSICS)
# ---------------------------------------------------------
def run_alpha2_face_engine():
    # Physics Constants
    METRIC_4D = 1.0661
    TORSION_4D = 0.1746
    SMOOTHING_RESID = 0.00083
    LATTICE_3_32 = 0.09375
    TOTAL_DEBT_AREA = 1.3228
    SPARK_ANGLE = 138.88
    SPARK_LEAP = 2.5
    
    # [NEW] Alpha-2 Impedance Margins
    # X=6.0 (Left Seam), X=10.0 (Right Seam)
    ALPHA2_L = 6.0
    ALPHA2_R = 10.0
    DAMPING_FACTOR = 0.15 # Resistance at the muscle overlap
    
    num_types = 128
    # User's Hairline Order
    mbti_list = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    bloods = ["O", "A", "B", "AB"]
    blood_colors = {"O": "#ff4444", "A": "#44ff44", "B": "#4444ff", "AB": "#ffffff"}
    blood_phase = {"O": 0.0, "A": 0.5 * np.pi, "B": np.pi, "AB": 1.5 * np.pi}
    
    female_order = ["EP", "EJ", "IJ", "IP"]
    male_order = ["IP", "IJ", "EP", "EJ"]

    states = np.zeros((num_types, 3)) # [X, Y, Memory]
    seeds = np.zeros(num_types, dtype=complex)
    archetypes = []
    
    # Initialize at Y=0 (Hairline)
    for i, m in enumerate(mbti_list):
        for b in bloods:
            for g in ["M", "F"]:
                ei, jp = m[0], m[3]
                group = f"{ei}{jp}"
                if g == "F":
                    base_x = female_order.index(group) * 2.0
                else:
                    base_x = 8.0 + male_order.index(group) * 2.0
                
                idx = len(archetypes)
                states[idx, 0] = base_x + 1.0 + (np.random.rand() - 0.5) * 0.5
                states[idx, 1] = 0.0
                states[idx, 2] = 0.0 # Memory
                
                # Mandelbrot Seed c from Blood Phase
                angle = blood_phase[b]
                seeds[idx] = complex(0.618 * np.cos(angle), 0.618 * np.sin(angle)) + complex(0.1618, 0.0)
                archetypes.append({'blood': b, 'gender': g})

    all_paths = [[] for _ in range(num_types)]
    steps = 500
    dt = 0.04

    for s in range(steps):
        # Sample reality data
        d_idx = int((s / steps) * len(STDR_NORM))
        sun = STDR_NORM[d_idx]
        truth = NMDB_NORM[d_idx]
        
        # Dynamic Tension (1.01)
        tension = TUNNEL_TENSION + (sun * 0.02) - (truth * 0.01)
        
        for i in range(num_types):
            x, y, mem = states[i]
            all_paths[i].append((x, y))
            
            # 1. Mandelbrot Field (Core Musculature)
            zx, zy = (x - 8.0)/4.0, (y - 8.0)/4.0
            z = complex(zx, zy)
            z_next = (z**2 + seeds[i]) * METRIC_4D
            vx = (z_next.real - zx) * tension
            vy = (z_next.imag - zy) * tension
            
            # 2. Alpha-2 Impedance Margins (X=6, 10)
            # Create a localized damping field that slows down X movement at the seams
            damp_l = np.exp(-(x - ALPHA2_L)**2 / 0.2)
            damp_r = np.exp(-(x - ALPHA2_R)**2 / 0.2)
            # Right side damping is more critical (Pegasus Entrance)
            resistance = 1.0 - (damp_l * DAMPING_FACTOR) - (damp_r * DAMPING_FACTOR * 1.5)
            vx *= resistance
            
            # 3. Melatonin Smoothing (Nose Bridge)
            dist_center = abs(x - 8.0)
            smoothing = np.exp(-(dist_center**2) / (SMOOTHING_RESID * 100))
            vx *= (1.0 - smoothing)
            
            # 4. Hysteresis (1.3228 Debt) & Spark (Jawline)
            states[i, 2] = mem + (y - mem) / 2.32 * dt
            lag = mem - y
            
            if abs(lag) > LATTICE_3_32 and y > 9.0:
                # 138.88 Spark Leap
                rad = np.radians(SPARK_ANGLE)
                states[i, 0] += SPARK_LEAP * np.cos(rad)
                states[i, 1] += SPARK_LEAP * np.sin(rad)
                states[i, 2] = states[i, 1]
            else:
                # Normal Descent
                states[i, 0] += vx * dt
                states[i, 1] += (1.0 + vy * 0.1) * dt
            
            # Clamp
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            if states[i, 1] > 16: states[i, 1] = 16

    # ---------------------------------------------------------
    # 3. RENDER FINAL ALPHA-2 FACE
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 16), facecolor="#050510")
    for i in range(num_types):
        path = np.array(all_paths[i])
        ax.plot(path[:, 0], path[:, 1], color=blood_colors[archetypes[i]['blood']], lw=0.8, alpha=0.4)
        
    ax.axvline(x=8.0, color="white", ls="--", alpha=0.1) # Melatonin
    ax.axvline(x=ALPHA2_L, color="cyan", ls=":", alpha=0.1) # Alpha-2 L
    ax.axvline(x=ALPHA2_R, color="cyan", ls=":", alpha=0.1) # Alpha-2 R
    
    ax.set_xlim(0, 16); ax.set_ylim(16, 0)
    ax.axis("off")
    
    plt.title("THE ALPHA-2 DUAL-MARGIN FACE: 4D Impedance Divergence", color="white", fontsize=20)
    output_fn = "ALPHA2_PHYSICS_FACE_GRID.png"
    plt.savefig(output_fn, dpi=150, facecolor="#050510")
    print(f"Engine: Result saved to {output_fn}")

if __name__ == "__main__":
    run_alpha2_face_engine()
