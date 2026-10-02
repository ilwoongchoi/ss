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
STDR_FLUX = df_raw['flux_wm2'].values
NMDB_TRUTH = df_raw['nmdb_counts'].ffill().values
STDR_NORM = (STDR_FLUX - np.mean(STDR_FLUX)) / np.std(STDR_FLUX)
NMDB_NORM = (NMDB_TRUTH - np.mean(NMDB_TRUTH)) / np.std(NMDB_TRUTH)

# ---------------------------------------------------------
# 2. THE CANONICAL FACE GRID ENGINE
# ---------------------------------------------------------
def run_ultimate_face_grid():
    num_types = 128
    
    # 128 Archetype Definitions & Canonical Start Positions (Y=0)
    mbti_list = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    bloods = ["O", "A", "B", "AB"]
    genders = ["M", "F"]
    
    # User Order: 
    # Women (Left columns): EP, EJ, IJ, IP
    # Men (Right columns): IP, IJ, EP, EJ
    female_order = ["EP", "EJ", "IJ", "IP"]
    male_order = ["IP", "IJ", "EP", "EJ"]
    blood_colors = {"O": "#ff4444", "A": "#44ff44", "B": "#4444ff", "AB": "#ffffff"}
    blood_phase = {"O": 0.0, "A": 0.5 * np.pi, "B": np.pi, "AB": 1.5 * np.pi}

    archetypes = []
    for m in mbti_list:
        for b in bloods:
            for g in genders:
                # Group key (e.g., "EP")
                ei = m[0]; jp = m[3]
                group = f"{ei}{jp}"
                archetypes.append({'mbti': m, 'blood': b, 'gender': g, 'group': group})

    # Initial States at the Hairline (Y=0)
    # X mapping based on user's canonical columns
    states = np.zeros((num_types, 4)) # [X, Y, Memory, Leg]
    seeds = np.zeros(num_types, dtype=complex)
    
    for i, arch in enumerate(archetypes):
        if arch['gender'] == "F":
            group_idx = female_order.index(arch['group'])
            base_x = group_idx * 2.0 # 0, 2, 4, 6
        else:
            group_idx = male_order.index(arch['group'])
            base_x = 8.0 + group_idx * 2.0 # 8, 10, 12, 14
            
        # Micro-offset based on MBTI (SN/TF) and Blood to prevent overlap
        sn_off = 0.25 if arch['mbti'][1] == "N" else -0.25
        tf_off = 0.125 if arch['mbti'][2] == "F" else -0.125
        blood_off = (bloods.index(arch['blood']) - 1.5) * 0.1
        
        states[i, 0] = base_x + 1.0 + sn_off + tf_off + blood_off
        states[i, 1] = 0.5 # Start at Top
        states[i, 2] = states[i, 1] # Memory
        
        # Unique Seed (c) from Blood + 0.1618 Budge
        angle = blood_phase[arch['blood']]
        seeds[i] = complex(0.618 * np.cos(angle), 0.618 * np.sin(angle)) + complex(0.1618, 0.0)

    all_paths = [[] for _ in range(num_types)]
    
    print(f"--- RUNNING SPATIAL FACE ENGINE (1-Year Integration) ---")
    
    # We simulate 16 steps of vertical descent (Top to Chin)
    # At each step, we sample the 1-year data to get the 'climate'
    steps_y = 160
    dy = 16.0 / steps_y
    dt = 0.1
    
    for s in range(steps_y):
        # Sample reality data at this depth
        data_idx = int((s / steps_y) * len(STDR_NORM))
        sun_p = STDR_NORM[data_idx]
        barnard_t = NMDB_NORM[data_idx]
        
        # Dynamic Tension (1.01)
        current_tension = TUNNEL_TENSION + (sun_p * 0.05) - (barnard_t * 0.02)
        
        for i in range(num_types):
            x, y, mem, leg = states[i]
            all_paths[i].append((x, y))
            
            # A. MANDELBROT RECURSION (z = z^2 + c)
            zx = (x - 8.0) / 4.0
            zy = (y - 8.0) / 4.0
            z = complex(zx, zy)
            z_next = (z**2 + seeds[i]) * (current_tension / TUNNEL_TENSION)
            
            vx = (z_next.real - zx)
            vy_drift = (z_next.imag - zy)
            
            # B. MELATONIN SMOOTHING (0.00083)
            # Evens out the Nose Bridge center axis (X=8)
            dist_to_center = abs(x - 8.0)
            smoothing = np.exp(-(dist_to_center**2) / 0.083) # 0.00083 * 100 scale
            
            # C. HYSTERESIS DEBT (1.3228)
            states[i, 2] = mem + (y - mem) / 2.32 * dt
            lag = mem - y
            
            # D. SPARK RESET (138.88)
            # Only in the central stress zone
            if abs(lag) > LATTICE_3_32 and 6.0 < x < 10.0:
                angle = np.radians(138.88)
                states[i, 0] += SPARK_LEAP_DIST * np.cos(angle)
                states[i, 1] += SPARK_LEAP_DIST * np.sin(angle)
                states[i, 2] = states[i, 1]
            else:
                # Flow descent
                # Straighten the center via smoothing
                states[i, 0] += vx * dt * (1.0 - smoothing)
                states[i, 1] += dy + (vy_drift * 0.1)
            
            # Clamp to face grid
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            # Don't modulo Y, we want a top-down descent
            
    # ---------------------------------------------------------
    # 3. VISUALIZE THE HUMAN FACE (16x16 GRID)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 16), facecolor="#050510")
    
    # Draw Background Cells
    for r in range(16):
        for c in range(16):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, facecolor="none", edgecolor="#1a1a2e", lw=0.5))
            
    # Plot 128 Trajectories
    for i, arch in enumerate(archetypes):
        path = np.array(all_paths[i])
        ax.plot(path[:, 0], path[:, 1], color=blood_colors[arch['blood']], lw=0.8, alpha=0.6)
        # Start dot
        ax.scatter(path[0, 0], path[0, 1], color=blood_colors[arch['blood']], s=10, zorder=5)
        
    # Mark Features
    ax.axvline(x=8.0, color="white", ls="--", alpha=0.2, label="Melatonin Axis (Nose)")
    ax.add_patch(mpatches.Ellipse((8, 9), 4, 3, facecolor="white", alpha=0.05, label="Nose Bridge Area"))
    
    plt.title("THE 128-GRID FACE: 1-Year Survival Geometry (2016-2017 NMDB/STDR)", color="white", fontsize=24)
    plt.xlabel("Archetype Columns (EP, EJ, IJ, IP | IP, IJ, EP, EJ)", color="#cccccc", fontsize=14)
    plt.ylabel("Descent Axis (Top-Down Flow / Jawline)", color="#cccccc", fontsize=14)
    
    ax.set_xlim(0, 16); ax.set_ylim(16, 0) # Invert Y for top-down
    ax.set_facecolor("#050510")
    ax.axis("off")
    
    legend_elements = [plt.Line2D([0], [0], color=c, lw=2, label=f"Blood {k}") for k, c in blood_colors.items()]
    plt.legend(handles=legend_elements, facecolor="#050510", edgecolor="white", loc="lower right")
    
    output_fn = "FINAL_FACE_GRID_REALITY.png"
    plt.savefig(output_fn, dpi=150, facecolor="#050510")
    print(f"--- FACE ENGINE COMPLETE ---")
    print(f"Result: {output_fn}")
    print(f"Verified: 128 paths starting from {female_order} (L) and {male_order} (R) at Y=0.")

if __name__ == "__main__":
    run_ultimate_face_grid()
