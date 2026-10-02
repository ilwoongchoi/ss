# -*- coding: utf-8 -*-
"""
FINAL_ONE_FORM_QUASAR.py
The Definitive 128-Type Biological Quasar Grid.
Physics: Static:Loop = 31:1 Unified Field
Symmetry: Quasar Symmetry (E-Edges, I-Center)
Tunnelling: Small Woman (I) -> D3 Tunnel -> Right D2
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from geometry_package.absolute_constants import (
    F_1_32, PHI, SPARK_ANGLE_DEG, SPARK_LEAP_DIST, 
    GABA_C_R_CAB, GABA_C_R_CA, GABA_C_V_APEX, LOOP_STRENGTH_5, NIGHT_HYSTERESIS
)

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 1. THE UNIFIED QUASAR LAW (31:1)
def get_quasar_velocity(x, y, mbti, gender):
    # Static:Loop = 31:1 ratio
    k_loop = float(F_1_32) # 1/32
    k_static = 1.0 - k_loop # 31/32
    
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # A. Static Flow (31/32)
    v_static_y = 1.5 if gender == "M" else 0.8
    v_static = np.array([0.0, v_static_y])
    
    # B. Loop Dynamics (1/32) - Dipole + Torsion
    # Dipole: Source(Right D2: 14, 6), Sink(Left Cortisol: 3.2, 11.2)
    dx_source, dy_source = x - 14.0, y - 6.0
    dx_sink, dy_sink = x - 3.2, y - 11.2
    
    dist_source = np.sqrt(dx_source**2 + dy_source**2) + 0.1
    dist_sink = np.sqrt(dx_sink**2 + dy_sink**2) + 0.1
    
    v_dipole = np.array([
        (dx_source/dist_source**2) * 2.0 - (dx_sink/dist_sink**2) * 1.5,
        (dy_source/dist_source**2) * 2.0 - (dy_sink/dist_sink**2) * 1.5
    ])
    
    # 4D Torsion (The Swirl)
    v_torsion = np.array([-(y - 8.0), (x - 8.0)]) * 0.1746
    
    # C. MBTI Cognitive Modulation (Parameters, not if/else)
    # T/F modulates torsion sensitivity, S/N modulates lateral expansion
    tf_mod = 0.3 if tf == "T" else 1.3
    sn_mod = 1.5 if sn == "N" else 0.7
    
    v_loop = (v_dipole + v_torsion * tf_mod) * sn_mod
    
    # D. Final Vector Sum
    V = k_static * v_static + k_loop * v_loop
    
    # Gendered Lateral Amplitude
    lat_amp = 2.8 if gender == "F" else 1.2
    if ei == "I": lat_amp *= 0.6 # Introvert shielding
    V[0] *= lat_amp
    
    return V

def generate_trajectory(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # QUASAR SYMMETRY: E(Extreme) -> I(Inside)
    # Women: EJ(0), EP(2), IJ(4), IP(6)
    # Men: IP(8), IJ(10), EP(12), EJ(14)
    group_map_f = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    group_map_m = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    
    base_x = group_map_f[f"{ei}{jp}"] if gender == "F" else group_map_m[f"{ei}{jp}"]
    
    # Micro-offsets
    x = base_x + 1.0 + (0.25 if sn=="N" else -0.25)
    y = 0.5 + (0.06 if blood=="O" else -0.06)
    
    pts = [(x, y)]
    dt = 0.1
    memory_y = y
    switch_state = False
    
    for row in range(16):
        target_y = row + 0.5
        while y < target_y - 0.001:
            step = min(dt, target_y - y)
            V = get_quasar_velocity(x, y, mbti, gender)
            
            # Hysteresis (1/32 Phase)
            tau = (2.317 / 1.5) * float(F_1_32)
            alpha = min(0.5, step / (tau + 1e-6))
            memory_y = (1.0 - alpha) * memory_y + alpha * y
            lag = memory_y - y
            
            if lag < -tau * 0.6: switch_state = True
            elif lag > -tau * 0.18: switch_state = False
            
            # 1. D3 TUNNELING (Introverted Women only)
            if gender == "F" and ei == "I" and 12.0 < x < 14.5 and 7.0 < y < 9.5:
                if abs(lag) > 0.85: # Spark Voltage
                    x, y = 14.0, 6.0 # Right D2 Flash
                    pts.append((x, y))
                    continue
            
            # 2. 3/32 SPARK GATE
            if y > 10.0 and switch_state and 6.0 < x < 10.0:
                x = np.round((x - 8.0) / 0.09375) * 0.09375 + 8.0
                x += float(SPARK_LEAP_DIST) * np.cos(np.radians(SPARK_ANGLE_DEG))
                y += float(SPARK_LEAP_DIST) * np.sin(np.radians(SPARK_ANGLE_DEG))
                pts.append((x, y))
                switch_state = False
                continue
            
            x = max(0, min(16, x + V[0] * (step / dt)))
            y += V[1] * (step / dt)
            
        pts.append((x, y))
    return pts

# 3. RENDERER (Intuition-Aligned)
def main():
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    
    # Nodes & Landmarks
    ax.add_patch(mpatches.Rectangle((0, 1), 16, 2.5, color="#99CCFF", alpha=0.1)) # Twilight 1
    ax.add_patch(mpatches.Rectangle((0, 8.5), 16, 3, color="#CC99FF", alpha=0.1)) # Twilight 2
    ax.add_patch(mpatches.Ellipse((3.2, 11.2), 3, 2, angle=-10, color="red", alpha=0.08)) # Cortisol
    ax.add_patch(mpatches.Ellipse((14.0, 6.0), 2, 2, color="blue", alpha=0.08)) # Right D2
    ax.add_patch(mpatches.Rectangle((6, 10), 4, 1.5, color="black", alpha=0.15)) # Spark Gate
    ax.plot([0, 16], [16, 0], color="orange", linestyle="--", alpha=0.4, lw=2) # PLP Spine
    
    # Grid Lines
    for i in range(17):
        ax.axhline(i, color="#E0E0E0", lw=0.5, zorder=0)
        ax.axvline(i, color="#E0E0E0", lw=0.5, zorder=0)

    # 128 Trajectories
    ALL_MBTI = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    for m in ALL_MBTI:
        for b in ["O", "A", "B", "AB"]:
            for g in ["M", "F"]:
                pts = generate_trajectory(m, b, g)
                xs, ys = zip(*pts)
                
                bc = np.array(matplotlib.colors.to_rgba(BLOOD_COLORS[b]))[:3]
                tint = np.array([1.0, 0.5, 0.1]) if g == "F" else np.array([0.1, 0.6, 1.0])
                color = 0.8 * bc + 0.2 * tint
                ax.plot(xs, ys, color=color, alpha=0.5, lw=1.2, zorder=10)

    # Labels
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -1.2, label, ha="center", weight="bold", size=14)

    ax.set_title(f"THE BIOLOGICAL QUASAR (ONE FORM) | Static:Loop=31:1 | Corrected Symmetry", 
                 fontsize=26, pad=50, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_FINAL_ONE_FORM_QUASAR.png"
    plt.savefig(output, dpi=300)
    print(f"Success: {output} is now aligned to Quasar intuition.")

if __name__ == "__main__":
    main()
