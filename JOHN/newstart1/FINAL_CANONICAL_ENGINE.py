import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from geometry_package.absolute_constants import *

# ---------------------------------------------------------
# 1. LOAD REAL-WORLD DATA (2016-2017)
# ---------------------------------------------------------
DATA_PATH = "out/unified_12m_hysteresis_data_ts.csv"
df_raw = pd.read_csv(DATA_PATH)
STDR_NORM = (df_raw['flux_wm2'].values - np.mean(df_raw['flux_wm2'].values)) / np.std(df_raw['flux_wm2'].values)
NMDB_NORM = (df_raw['nmdb_counts'].ffill().values - np.mean(df_raw['nmdb_counts'].ffill().values)) / np.std(df_raw['nmdb_counts'].ffill().values)

# ---------------------------------------------------------
# 2. CANONICAL GRID ENGINE (Discrete Circuit Logic)
# ---------------------------------------------------------
def run_canonical_grid():
    # Final Physics constants
    Q_FACTOR = 11.8
    TORSION_4D = 0.1746
    METRIC_4D = 1.0661
    SMOOTHING_RESID = 0.00083
    LATTICE_3_32 = 0.09375
    SPARK_ANGLE = 138.88
    SPARK_LEAP = 2.5
    
    # Grid Setup (16x16)
    N_COLS, N_ROWS = 16, 16
    
    # Archetype Definitions
    mbti_list = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    bloods = ["O", "A", "B", "AB"]
    genders = ["M", "F"]
    
    # User's Column Layout
    female_order = ["EJ", "EP", "IJ", "IP"] # 0-8
    male_order = ["IP", "IJ", "EP", "EJ"]   # 8-16
    blood_phase = {"O": 0.0, "A": 0.5 * np.pi, "B": np.pi, "AB": 1.5 * np.pi}
    blood_colors = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

    # Initialize 128 Trajectories
    num_types = 128
    states = np.zeros((num_types, 3)) # [X, Y, Memory]
    seeds = np.zeros(num_types, dtype=complex)
    archetypes = []
    
    idx = 0
    for m in mbti_list:
        for b in bloods:
            for g in genders:
                ei, jp = m[0], m[3]
                group = f"{ei}{jp}"
                if g == "F":
                    base_x = female_order.index(group) * 2.0
                else:
                    base_x = 8.0 + male_order.index(group) * 2.0
                
                # Starting position at the Hairline (Y=0)
                # Spread O, A, B, AB within the 2-cell column
                b_idx = bloods.index(b)
                states[idx, 0] = base_x + 0.5 + (b_idx * 0.3)
                states[idx, 1] = 0.0
                states[idx, 2] = 0.0 # Memory
                
                # Mandelbrot Seed c
                angle = blood_phase[b]
                seeds[idx] = complex(0.618 * np.cos(angle), 0.618 * np.sin(angle)) + complex(0.1618, 0)
                archetypes.append({'blood': b, 'gender': g, 'mode': group, 'mbti': m})
                idx += 1

    all_paths = [[] for _ in range(num_types)]
    
    # Discrete Steps: 16 vertical rows
    rows = 16
    for r in range(rows + 1):
        # Sample reality data for this "hour" of the face
        data_idx = int((r / rows) * (len(STDR_NORM) - 1))
        sun = STDR_NORM[data_idx]
        truth = NMDB_NORM[data_idx]
        tension = TUNNEL_TENSION + (sun * 0.02) - (truth * 0.01)
        
        for i in range(num_types):
            x, y, mem = states[i]
            all_paths[i].append((x, y))
            
            # A. Maxwell Impedance Seams (X=6, 10)
            margin_dist = min(abs(x - 6.0), abs(x - 10.0))
            impedance = 1.0 + (Q_FACTOR * np.exp(-(margin_dist**2) / 0.5))
            
            # B. Mandelbrot Recursion (Core Drive)
            zx, zy = (x - 8.0)/4.0, (y - 8.0)/4.0
            z = complex(zx, zy)
            z_next = (z**2 + seeds[i]) * (1.0 / impedance)
            
            vx = (z_next.real - zx) * tension * METRIC_4D
            vy_drift = (z_next.imag - zy) * TORSION_4D
            
            # C. Melatonin Smoothing (Nose Bridge)
            smoothing = np.exp(-(abs(x - 8.0)**2) / (SMOOTHING_RESID * 100))
            vx *= (1.0 - smoothing)
            
            # D. Hysteresis Memory & Spark Leap
            states[i, 2] = mem + (y - mem) / 2.32 * 1.0 # Step dt=1.0
            lag = mem - y
            
            # Spark Condition (Trapped in 3/32 gate in the central zone)
            if abs(lag) > LATTICE_3_32 and 6.0 < x < 10.0 and y > 8.0:
                rad = np.radians(SPARK_ANGLE)
                states[i, 0] += SPARK_LEAP * np.cos(rad)
                states[i, 1] += SPARK_LEAP * np.sin(rad)
                states[i, 2] = states[i, 1]
            else:
                # Flow to next row
                states[i, 0] += vx * 0.5 # Lateral shift
                states[i, 1] += 1.0 + vy_drift # Move to next row
            
            # Grid Clamping
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            if states[i, 1] > 16: states[i, 1] = 16

    # ---------------------------------------------------------
    # 3. RENDER THE CANONICAL CIRCUIT (MATCHING THE IMAGE)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(24, 15), facecolor="#FDFDFD")
    
    # 1. Background Layers (The Twilight Bands)
    ax.add_patch(mpatches.Rectangle((0, 1.0), 16, 2.5, facecolor="#E3F2FD", alpha=0.5, zorder=0)) # Morning Blue
    ax.add_patch(mpatches.Rectangle((0, 8.5), 16, 3.0, facecolor="#F3E5F5", alpha=0.5, zorder=0)) # Evening Purple
    
    # 2. The 16x16 Grid
    for c in range(17): ax.axvline(c, color="#EEEEEE", lw=0.5, zorder=1)
    for r in range(17): ax.axhline(r, color="#EEEEEE", lw=0.5, zorder=1)
    
    # 3. The PLP Spine (X+Y=16)
    ax.plot([0, 16], [16, 0], color="#FF9800", ls="--", lw=2, alpha=0.6, label="PLP Spine (X+Y=16)", zorder=2)
    
    # 4. Draw Trajectories
    for i in range(num_types):
        path = np.array(all_paths[i])
        mode = archetypes[i]['mode']
        ls = "-" if mode.endswith("J") else "--"
        ax.plot(path[:, 0], path[:, 1], color=blood_colors[archetypes[i]['blood']], lw=1.2, ls=ls, alpha=0.7, zorder=10)
        # Start marker
        ax.scatter(path[0, 0], path[0, 1], color=blood_colors[archetypes[i]['blood']], s=20, zorder=11)

    # 5. Nodes (Anatomical Overlay)
    nodes = [
        (6.5, 5.0, "Left Cortisol\n(Horizontal Tension)", "red"),
        (9.5, 5.0, "Right Ach\n(Vertical Tension)", "blue"),
        (8.0, 10.0, "Darkness Stress\n3/32 Spark Gate", "black"),
        (8.0, 14.5, "Gravity Sensor\n(0-Phase Reset)", "purple")
    ]
    for x, y, txt, col in nodes:
        ax.text(x, y, txt, color=col, ha="center", va="center", fontsize=10, weight="bold", 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # 6. Column Labels
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -0.5, label, ha="center", weight="bold", fontsize=14)

    # Final Formatting
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(16.5, -1.5) # Top-down
    ax.axis("off")
    plt.title("THE 128-GRID CANONICAL CIRCUIT: Final Physics Integration", fontsize=24, pad=20, weight="bold")
    
    # Custom Legend
    legend_elements = [plt.Line2D([0], [0], color=c, lw=3, label=f"Type {k}") for k, c in blood_colors.items()]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=12)
    
    output_fn = "FINAL_CANONICAL_GRID_FACE.png"
    plt.savefig(output_fn, dpi=200, bbox_inches='tight')
    print(f"Engine Success: {output_fn} generated with exact background layers, nodes, and PLP spine.")

if __name__ == "__main__":
    run_canonical_grid()
