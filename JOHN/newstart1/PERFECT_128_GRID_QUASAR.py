# -*- coding: utf-8 -*-
"""
PERFECT_128_GRID_QUASAR.py
128-Type Grid V4 - FULL BIOLOGICAL QUASAR LANDSCAPE
Layout: E-Women (0-4) | I-Women (4-8) || I-Men (8-12) | E-Men (12-16)
Visuals: Cortisol/Ach Nodes, 3/32 Gate, PLP Spine, Twilight Bands
Physics: Static:Loop=31:1 | D3 Tunnel for Small Women (I) to Right D2
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import json
from geometry_package.absolute_constants import (
    F_1_32, PHI, SPARK_ANGLE_DEG, SPARK_LEAP_DIST, 
    GABA_C_R_CAB, GABA_C_R_CA, GABA_C_V_APEX, LOOP_STRENGTH_5, NIGHT_HYSTERESIS
)

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 1. Constants & Quasar Layout
CONST = {
    "night_tau_lag_hours": 2.317382542906709,
    "w5": float(LOOP_STRENGTH_5),
    "w7": 0.1569768596,
    "w11": float(NIGHT_HYSTERESIS),
    "kappa_1_32": float(F_1_32),
    "spark_angle_deg": float(SPARK_ANGLE_DEG),
    "spark_leap_distance": float(SPARK_LEAP_DIST),
    "female_horizontal_amp": 2.8, "male_horizontal_amp": 1.2,
    "female_vertical_speed": 0.8, "male_vertical_speed": 1.5,
    # QUASAR SYMMETRY: E at edges, I in middle
    "female_group_order": ["EJ", "EP", "IJ", "IP"], # 0 -> 8
    "male_group_order": ["IP", "IJ", "EP", "EJ"],   # 8 -> 16
    "group_map_female": {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6},
    "group_map_male": {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14},
}

ALL_MBTI = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
            "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

# 2. Universal Quasar Field
def get_field(x, y, mbti, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    torsion = 0.1746
    
    # 4D Torsion swirl
    vx = -torsion * (y - 8.0)
    if tf == "T": vx *= 0.3
    else: vx *= 1.3
    
    if sn == "N": vx *= 1.5
    if jp == "J": vx += (16.0 - y - x) * 0.05
    else: vx += np.sign(x - 8.0) * 0.1
    
    # Terminal Attractor (Left Cortisol)
    tx, ty = 3.2, 11.2
    d_term = np.sqrt((x-tx)**2 + (y-ty)**2)
    vx -= 2.5 * np.exp(-d_term**2 / 4.5) * (x-tx)/max(0.1, d_term)
    
    amp = CONST["male_horizontal_amp"] if gender == "M" else CONST["female_horizontal_amp"]
    if ei == "I": amp *= 0.6
    return vx * amp * 1.0100375

def generate_trajectory(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_map = CONST["group_map_female"] if gender == "F" else CONST["group_map_male"]
    x = group_map[f"{ei}{jp}"] + 1.0 + (0.25 if sn=="N" else -0.25)
    y = 0.5 + (0.06 if blood=="O" else -0.06)
    
    pts = [(x, y, False)]
    dt = 0.1
    hyst_tau = (2.317 / 1.5) * CONST["kappa_1_32"]
    memory_y, switch_state = y, False
    
    for row in range(16):
        target_y = row + 0.5
        while y < target_y - 0.001:
            step = min(dt, target_y - y)
            vx = get_field(x, y, mbti, gender)
            vy = step * (CONST["male_vertical_speed"] if gender == "M" else CONST["female_vertical_speed"])
            
            # Hysteresis
            if (1.0 <= y <= 3.5) or (8.5 <= y <= 11.5):
                alpha = min(0.5, step / (hyst_tau + 1e-6))
                memory_y = (1.0 - alpha) * memory_y + alpha * y
                if (memory_y - y) < -hyst_tau * 0.6: switch_state = True
                elif (memory_y - y) > -hyst_tau * 0.18: switch_state = False
                
                # D3 Tunnel for Small Women (I)
                if gender == "F" and ei == "I" and abs(x-13.0)<1.5 and abs(y-8.0)<1.5:
                    if abs(memory_y - y) > 0.85: # Threshold
                        x, y = 14.0, 6.0
                        pts.append((x, y, "TUNNEL"))
                        continue

                # Spark Gate (3/32)
                if y > 10.0 and switch_state and 6.0 < x < 10.0:
                    x = (np.round((x - 8.0) / 0.09375) * 0.09375 + 8.0) + CONST["spark_leap_distance"] * np.cos(np.radians(SPARK_ANGLE_DEG))
                    y += CONST["spark_leap_distance"] * np.sin(np.radians(SPARK_ANGLE_DEG))
                    pts.append((x, y, True))
                    switch_state = False
                    continue
            
            x = max(0, min(16, x + vx * (step / dt)))
            y += vy
        pts.append((x, y, False))
    return pts

# 3. Main Renderer
def main():
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#F8F8F8")
    
    # Visual Landscape
    ax.add_patch(mpatches.Rectangle((0, 1), 16, 2.5, color="#99CCFF", alpha=0.1, zorder=1)) # Twilight 1
    ax.add_patch(mpatches.Rectangle((0, 8.5), 16, 3, color="#CC99FF", alpha=0.1, zorder=1)) # Twilight 2
    ax.plot([0, 16], [16, 0], color="orange", linestyle="--", alpha=0.4, lw=2, label="PLP Spine")
    ax.add_patch(mpatches.Ellipse((6.5, 5.0), 3, 2, angle=-10, color="red", alpha=0.08)) # Cortisol
    ax.add_patch(mpatches.Ellipse((9.5, 5.0), 2, 3, color="blue", alpha=0.08)) # Ach
    ax.add_patch(mpatches.Rectangle((6, 10), 4, 1.5, color="black", alpha=0.15)) # 3/32 Gate
    ax.add_patch(mpatches.Circle((8, 14.5), 1.0, color="purple", alpha=0.15)) # Gravity
    
    # Grid
    for r in range(16):
        for c in range(16):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, facecolor="white", edgecolor="#E0E0E0", lw=0.5, alpha=0.5))

    # Column Labels (Quasar Symmetry)
    col_groups = (
        [(f"{k} WOMEN", CONST["group_map_female"][k], CONST["group_map_female"][k] + 2) for k in CONST["female_group_order"]]
        + [(f"{k} MEN", CONST["group_map_male"][k], CONST["group_map_male"][k] + 2) for k in CONST["male_group_order"]]
    )
    for label, xs, xe in col_groups:
        ax.text((xs+xe)/2, -1.2, label, ha="center", weight="bold", size=14)

    # Render 128 Types
    for m in ALL_MBTI:
        for b in ["O", "A", "B", "AB"]:
            for g in ["M", "F"]:
                pts = generate_trajectory(m, b, g)
                bc = np.array(matplotlib.colors.to_rgba(BLOOD_COLORS[b]))
                tint = np.array([1.0, 0.5, 0.1]) if g == "F" else np.array([0.1, 0.6, 1.0])
                color = 0.75 * bc[:3] + 0.25 * tint
                ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, alpha=0.45, lw=1.2, zorder=20)

    ax.set_title(f"128-TYPE PERFECT QUASAR GRID | Static:Loop=31:1 | W5={CONST['w5']:.2f} W7={CONST['w7']:.3f} W11={CONST['w11']:.3f}", 
                 fontsize=24, pad=45, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    plt.tight_layout()
    plt.savefig("128_PERFECT_QUASAR_GRID.png", dpi=300)
    print("Saved: 128_PERFECT_QUASAR_GRID.png")

if __name__ == "__main__": main()
