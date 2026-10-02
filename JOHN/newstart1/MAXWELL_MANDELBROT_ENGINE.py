import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
# 2. MAXWELL IMPEDANCE + MANDELBROT INTEGRATED ENGINE
# ---------------------------------------------------------
def run_maxwell_mandelbrot_engine():
    # Final Physics Constants
    Q_FACTOR = 11.8
    METRIC_4D = 1.0661
    TORSION_4D = 0.1746
    GEAR_RATIO = 0.618
    BUDGE = 0.1618
    LATTICE_3_32 = 0.09375
    SMOOTHING_RESID = 0.00083
    
    # Archetype Definitions
    mbti_list = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    bloods = ["O", "A", "B", "AB"]
    blood_phase = {"O": 0.0, "A": 0.5 * np.pi, "B": np.pi, "AB": 1.5 * np.pi}
    blood_colors = {"O": "#ff4444", "A": "#44ff44", "B": "#4444ff", "AB": "#ffffff"}
    
    female_order = ["EP", "EJ", "IJ", "IP"]
    male_order = ["IP", "IJ", "EP", "EJ"]

    num_types = 128
    states = np.zeros((num_types, 3)) # [X, Y, Memory]
    seeds = np.zeros(num_types, dtype=complex)
    archetypes = []
    
    # Hairline Initialization (Y=0)
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
                # Starting X based on canonical distribution
                states[idx, 0] = base_x + 1.0 + (np.random.rand() - 0.5) * 0.4
                states[idx, 1] = 0.0
                states[idx, 2] = 0.0 # Memory
                
                # Complex Seed c: Gear Ratio + Blood Phase + Budge
                angle = blood_phase[b]
                seeds[idx] = complex(GEAR_RATIO * np.cos(angle), GEAR_RATIO * np.sin(angle)) + complex(BUDGE, 0.0)
                archetypes.append({'blood': b, 'gender': g, 'mbti': m})

    all_paths = [[] for _ in range(num_types)]
    steps = 600
    dt = 0.04

    for s in range(steps):
        # Sample reality data
        d_idx = int((s / steps) * len(STDR_NORM))
        sun = STDR_NORM[d_idx]
        truth = NMDB_NORM[d_idx]
        
        # Tension (1.01) modulated by data
        tension = TUNNEL_TENSION + (sun * 0.02) - (truth * 0.01)
        
        for i in range(num_types):
            x, y, mem = states[i]
            all_paths[i].append((x, y))
            
            # 1. MAXWELL IMPEDANCE (Z)
            # Damping increases at Alpha-2 Margins (X=6, 10)
            margin_dist = min(abs(x - 6.0), abs(x - 10.0))
            # Q-Factor 11.8 determines the sharpness of the impedance seam
            impedance = 1.0 + (Q_FACTOR * np.exp(-(margin_dist**2) / 0.1))
            
            # 2. COMPLEX MANDELBROT RECURSION (Gear Meshing)
            zx, zy = (x - 8.0)/4.0, (y - 8.0)/4.0
            z = complex(zx, zy)
            # Flow is inversely proportional to Impedance (High Z = Slow/Resonant)
            z_next = (z**2 + seeds[i]) * (1.0 / impedance)
            
            vx = (z_next.real - zx) * tension * METRIC_4D
            vy = (z_next.imag - zy) * tension
            
            # 3. MELATONIN SMOOTHING (Nose Bridge)
            dist_center = abs(x - 8.0)
            smoothing = np.exp(-(dist_center**2) / (SMOOTHING_RESID * 100))
            vx *= (1.0 - smoothing)
            
            # 4. HYSTERESIS (1.3228) & SPARK (138.88)
            states[i, 2] = mem + (y - mem) / 2.32 * dt
            lag = mem - y
            
            if abs(lag) > LATTICE_3_32 and y > 9.0:
                # 138.88 Spark Leap (Discharge)
                rad = np.radians(138.88)
                states[i, 0] += 2.5 * np.cos(rad)
                states[i, 1] += 2.5 * np.sin(rad)
                states[i, 2] = states[i, 1]
            else:
                # Normal Descent
                states[i, 0] += vx * dt
                states[i, 1] += (1.0 + vy * 0.1) * dt
            
            # Clamp to 16x16 Grid
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            if states[i, 1] > 16: states[i, 1] = 16

    # ---------------------------------------------------------
    # 3. RENDER THE CANONICAL FACE (60FPS LOGIC)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 16), facecolor="#050510")
    for i in range(num_types):
        path = np.array(all_paths[i])
        ax.plot(path[:, 0], path[:, 1], color=blood_colors[archetypes[i]['blood']], lw=0.8, alpha=0.4)
        
    # Overlay Maxwell Cavity Seams
    ax.axvline(x=8.0, color="white", ls="--", alpha=0.1) # Melatonin
    ax.axvline(x=6.0, color="cyan", ls=":", alpha=0.2) # Alpha-2 Seam L
    ax.axvline(x=10.0, color="cyan", ls=":", alpha=0.2) # Alpha-2 Seam R
    
    ax.set_xlim(0, 16); ax.set_ylim(16, 0)
    ax.axis("off")
    
    plt.title("THE INTEGRATED MAXWELL-MANDELBROT FACE: 128 Trajectories", color="white", fontsize=20)
    output_fn = "ULTIMATE_MAXWELL_MANDELBROT_FACE.png"
    plt.savefig(output_fn, dpi=300, facecolor="#050510")
    print(f"Engine: Saved {output_fn} | Integrated Maxwell Impedance & Complex Gear Meshing.")

if __name__ == "__main__":
    run_maxwell_mandelbrot_engine()
