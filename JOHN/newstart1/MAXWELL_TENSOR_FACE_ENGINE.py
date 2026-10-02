import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from geometry_package.absolute_constants import *

# ---------------------------------------------------------
# 1. LOAD REAL-WORLD DATA
# ---------------------------------------------------------
DATA_PATH = "out/unified_12m_hysteresis_data_ts.csv"
df_raw = pd.read_csv(DATA_PATH)
STDR_NORM = (df_raw['flux_wm2'].values - np.mean(df_raw['flux_wm2'].values)) / np.std(df_raw['flux_wm2'].values)
NMDB_NORM = (df_raw['nmdb_counts'].ffill().values - np.mean(df_raw['nmdb_counts'].ffill().values)) / np.std(df_raw['nmdb_counts'].ffill().values)

# ---------------------------------------------------------
# 2. MAXWELL BASIN + MBTI TENSOR ENGINE
# ---------------------------------------------------------
def run_maxwell_tensor_face():
    num_types = 128
    mbti_list = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    bloods = ["O", "A", "B", "AB"]
    genders = ["M", "F"]
    
    # MBTI Physical Tensor Mapping
    # [Torsion, Fixation, Conductivity, Viscosity]
    mbti_tensors = {
        "J": [0.5, 2.0, 1.2, 0.8], # Fixation (Linear)
        "P": [2.5, 0.5, 0.8, 1.5], # Entropy (Spiral)
        "T": [0.8, 1.0, 2.5, 0.5], # Conductivity (ACh)
        "F": [1.2, 1.0, 0.5, 2.5]  # Viscosity (Serotonin)
    }

    female_order = ["EJ", "EP", "IJ", "IP"]
    male_order = ["IP", "IJ", "EP", "EJ"]
    blood_colors = {"O": "#ff4444", "A": "#44ff44", "B": "#4444ff", "AB": "#ffffff"}

    states = np.zeros((num_types, 3)) # [X, Y, Memory]
    seeds = np.zeros(num_types, dtype=complex)
    type_tensors = np.zeros((num_types, 4))
    archetypes = []

    # Initialize at Y=0 (Hairline) based on User's Canonical Layout
    idx = 0
    for m in mbti_list:
        for b in bloods:
            for g in genders:
                ei, sn, tf, jp = m[0], m[1], m[2], m[3]
                group = f"{ei}{jp}"
                if g == "F":
                    base_x = female_order.index(group) * 2.0
                else:
                    base_x = 8.0 + male_order.index(group) * 2.0
                
                states[idx, 0] = base_x + 1.0 + (np.random.rand()-0.5)*0.3
                states[idx, 1] = 0.0
                
                # Compose Tensor: Combine J/P and T/F traits
                t1 = mbti_tensors[jp]
                t2 = mbti_tensors[tf]
                type_tensors[idx] = [(t1[0]+t2[0])/2, (t1[1]+t2[1])/2, (t1[2]+t2[2])/2, (t1[3]+t2[3])/2]
                
                # Complex Seed (Blood Phase)
                angle = {"O":0, "A":0.5*np.pi, "B":np.pi, "AB":1.5*np.pi}[b]
                seeds[idx] = complex(0.618 * np.cos(angle), 0.618 * np.sin(angle)) + complex(0.1618, 0)
                archetypes.append({'blood':b, 'gender':g})
                idx += 1

    all_paths = [[] for _ in range(num_types)]
    steps = 600
    dt = 0.04

    for s in range(steps):
        d_idx = int((s/steps) * len(STDR_NORM))
        force_sun = STDR_NORM[d_idx]
        
        for i in range(num_types):
            x, y, mem = states[i]
            all_paths[i].append((x, y))
            torsion, fixation, cond, visc = type_tensors[i]
            
            # 1. MAXWELL TRIPLE-BASIN POTENTIAL (The Face Geometry)
            # Separatrices at X=5, X=11. Impedance peaks at X=6, 10.
            margin_dist = min(abs(x - 6.0), abs(x - 10.0))
            impedance = 1.0 + (11.8 * np.exp(-(margin_dist**2) / 0.2))
            
            # 2. THE EQUATION OF LIFE (Tensor-Modulated Mandelbrot)
            zx, zy = (x - 8.0)/4.0, (y - 8.0)/4.0
            z = complex(zx, zy)
            # Torsion scale driven by P-types, Conductivity by T-types
            z_next = (z**2 + seeds[i]) * (cond / impedance)
            
            vx = (z_next.real - zx) * torsion
            vy = (z_next.imag - zy) * fixation
            
            # 3. NOSE BRIDGE SMOOTHING
            center_smoothing = np.exp(-(abs(x-8.0)**2) / 0.083)
            vx *= (1.0 - center_smoothing)
            
            # 4. HYSTERESIS & SPARK (Metabolic Debt)
            states[i, 2] = mem + (y - mem) / (2.32 * visc) * dt
            lag = mem - y
            
            if abs(lag) > 0.09375 and y > 9.0:
                rad = np.radians(138.88)
                states[i, 0] += 2.5 * np.cos(rad)
                states[i, 1] += 2.5 * np.sin(rad)
                states[i, 2] = states[i, 1]
            else:
                states[i, 0] += (vx + force_sun*0.05) * dt
                states[i, 1] += (1.0 + vy*0.1) * dt
            
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            if states[i, 1] > 16: states[i, 1] = 16

    # RENDER
    fig, ax = plt.subplots(figsize=(16, 16), facecolor="#050510")
    for i in range(num_types):
        path = np.array(all_paths[i])
        ax.plot(path[:, 0], path[:, 1], color=blood_colors[archetypes[i]['blood']], lw=0.8, alpha=0.4)
    
    # Separating lines from your image
    ax.axvline(x=5.0, color="gray", ls="--", alpha=0.3)
    ax.axvline(x=11.0, color="gray", ls="--", alpha=0.3)
    ax.axvline(x=8.0, color="white", ls="--", alpha=0.1)
    
    ax.set_xlim(0, 16); ax.set_ylim(16, 0)
    ax.axis("off")
    plt.title("THE MAXWELL TENSOR FACE: Emergent 128-Type Geometry", color="white", fontsize=20)
    plt.savefig("MAXWELL_TENSOR_FACE_GRID.png", dpi=300, facecolor="#050510")
    print("Engine: Final divergence mapped to Maxwell Basins.")

if __name__ == "__main__":
    run_maxwell_tensor_face()
