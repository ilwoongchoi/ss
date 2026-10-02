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
# 2. PURE PHYSICS FACE ENGINE (Torsion + Metric + Recursion)
# ---------------------------------------------------------
def run_pure_physics_face():
    # Canonical Ratios
    METRIC_4D = 1.0661
    TORSION_4D = 0.1746
    SMOOTHING_RESID = 0.00083
    GEAR_RATIO = 0.618
    BUDGE = 0.1618
    
    # Archetype Setup
    mbti_list = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    bloods = ["O", "A", "B", "AB"]
    blood_map = {"O": 0, "A": 1, "B": 2, "AB": 3}
    blood_colors = {"O": "#ff4444", "A": "#44ff44", "B": "#4444ff", "AB": "#ffffff"}
    # Metric Ratios: GABA(-0.5), ACh(1.0), Glu(0.5), 5HT(1.5)
    blood_metrics = [-0.5, 1.0, 0.5, 1.5] 

    female_order = ["EP", "EJ", "IJ", "IP"]
    male_order = ["IP", "IJ", "EP", "EJ"]

    num_types = 128
    states = np.zeros((num_types, 2)) # [X, Y]
    archetypes = []
    
    # Hairline Initialization (Y=0)
    for i, m in enumerate(mbti_list):
        for b in bloods:
            for g in ["M", "F"]:
                ei = m[0]; jp = m[3]
                group = f"{ei}{jp}"
                if g == "F":
                    base_x = female_order.index(group) * 2.0
                else:
                    base_x = 8.0 + male_order.index(group) * 2.0
                
                # Precise physics-based start
                states[len(archetypes), 0] = base_x + 1.0 + (blood_metrics[blood_map[b]] * 0.2)
                states[len(archetypes), 1] = 0.0
                archetypes.append({'blood': b, 'gender': g, 'metric': blood_metrics[blood_map[b]]})

    all_paths = [[] for _ in range(num_types)]
    steps = 400
    dt = 0.05

    for s in range(steps):
        # Sample reality data
        d_idx = int((s / steps) * len(STDR_NORM))
        sun = STDR_NORM[d_idx]
        truth = NMDB_NORM[d_idx]
        
        # Macro/Micro Time Reversal (1/28)
        phase = (s / steps) * 28.0 * np.pi
        t_micro = np.sin(phase)
        is_reverse = np.cos(phase) < 0
        direction = -1.0 if is_reverse else 1.0

        for i in range(num_types):
            x, y = states[i]
            all_paths[i].append((x, y))
            
            # 1. Mandelbrot Core (z = z^2 + c)
            zx, zy = (x - 8.0)/4.0, (y - 8.0)/4.0
            z = complex(zx, zy)
            c = complex(GEAR_RATIO, BUDGE) * direction
            z_next = z**2 + c
            
            # 2. 4D Torsion & Metric (Chiral Muscle Wrap)
            # Lateral expansion scaled by blood metric
            vx_geom = (z_next.real - zx) * METRIC_4D * archetypes[i]['metric']
            vy_geom = (z_next.imag - zy) * METRIC_4D
            
            # 3. Nose Bridge Smoothing (0.00083)
            # Straightens the center axis to prevent "beard" effect
            center_pull = (8.0 - x)
            smoothing = np.exp(-(center_pull**2) / (SMOOTHING_RESID * 100))
            
            # 4. PLP Spine (X+Y=16) & Terminal Attractors
            # Creates the jawline and cheek contour
            target_x = 16.0 - y
            spine_drift = (target_x - x) * 0.1
            
            # Global Reality Forcing
            vx_total = (vx_geom + spine_drift + (sun * 0.1)) * (1.0 - smoothing)
            vy_total = 1.0 + (vy_geom * 0.1) - (truth * 0.05)
            
            states[i, 0] += vx_total * dt
            states[i, 1] += vy_total * dt
            
            # Clamp to 16x16 face grid
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            if states[i, 1] > 16: states[i, 1] = 16

    # ---------------------------------------------------------
    # 3. RENDER THE PURE GEOMETRY FACE
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 16), facecolor="#050510")
    for i in range(num_types):
        path = np.array(all_paths[i])
        ax.plot(path[:, 0], path[:, 1], color=blood_colors[archetypes[i]['blood']], lw=0.7, alpha=0.4)
        
    ax.axvline(x=8.0, color="white", ls="--", alpha=0.1) # Melatonin Axis
    ax.set_xlim(0, 16); ax.set_ylim(16, 0)
    ax.set_facecolor("#050510")
    ax.axis("off")
    
    plt.title("THE 128-GRID PURE PHYSICS FACE: Torsion & Metric Divergence", color="white", fontsize=20)
    output_fn = "PURE_PHYSICS_FACE_GRID.png"
    plt.savefig(output_fn, dpi=150, facecolor="#050510")
    print(f"Engine: Result saved to {output_fn}")

if __name__ == "__main__":
    run_pure_physics_face()
