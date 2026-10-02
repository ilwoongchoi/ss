# -*- coding: utf-8 -*-
"""
PURE_128_TRAJECTORY_GRID.py
128-Type Trajectory Simulation - PURE VERSION.
Removed all labels and landmarks (Bypass, Spine, Sensors, etc.).
Focus: 128 unique paths driven by Gender, MBTI, and Blood mass.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_package.absolute_constants import *
from geometry_package import universal_equation as unieq

# 1. PURE PHYSICAL CONSTANTS
def get_params(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    return {
        "vy": 1.5 if gender == "M" else 0.8,
        "vx_amp": 1.2 if gender == "M" else 2.8,
        "target_x": (14.0 if ei == "E" else 8.0) if gender == "M" else (2.0 if ei == "E" else 8.0),
        "torsion": 1.5 if tf == "F" else 0.3,
        "mass": {"O": 1.4, "A": 1.1, "B": 0.9, "AB": 0.6}[blood]
    }

# 2. TRAJECTORY ENGINE
def generate_path(mbti, blood, gender):
    p = get_params(mbti, blood, gender)
    group_map_f = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    group_map_m = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    base_x = group_map_f[mbti[0]+mbti[3]] if gender == "F" else group_map_m[mbti[0]+mbti[3]]
    
    x = base_x + 1.0 + (p["mass"] - 1.0)
    y = 0.5
    start_pos = (x, y)
    pts = [start_pos]
    dt = 0.2
    
    for _ in range(100):
        if y >= 16.0: break
        
        # Physics
        vx = ((p["target_x"] - x) * 0.15 + np.sin(y*0.5)*p["torsion"]) * p["vx_amp"] / p["mass"]
        vy = p["vy"]
        
        x += vx * dt
        y += vy * dt
        
        # Dream Folding (The 45-min Rule)
        is_fold = (y >= 13.0 and y < 13.5) if gender == "M" else (y >= 13.5 and y < 14.0)
        if is_fold:
            pts.append(start_pos)
            break
        
        pts.append((x, y))
    return pts

# 3. RENDER
def main():
    print("Rendering Pure 128 Trajectories...")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    
    # Grid Only
    for i in range(17):
        ax.axhline(i, color="#EEEEEE", lw=0.5, zorder=0)
        ax.axvline(i, color="#EEEEEE", lw=0.5, zorder=0)
        
    MBTI_16 = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
    BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    for m in MBTI_16:
        for b in ["O", "A", "B", "AB"]:
            for g in ["M", "F"]:
                pts = generate_path(m, b, g)
                xs, ys = zip(*pts)
                bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[b]))[:3]
                color = 0.8*bc + 0.2*(np.array([1,0.5,0]) if g=="F" else np.array([0,0.5,1]))
                ax.plot(xs, ys, color=color, alpha=0.3, lw=0.8, zorder=10)

    # Minimal Title
    ax.set_title("128-TYPE PURE TRAJECTORY GRID", fontsize=24, pad=40, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_PURE_TRAJECTORY_GRID.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Success: {output} rendered. No labels, no clutter.")

if __name__ == "__main__": main()
