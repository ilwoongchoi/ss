# -*- coding: utf-8 -*-
"""
128_TRUE_DIVERGENCE_GRID.py
Simulates 128 distinct trajectories with basin-based divergence.
Aesthetic: White background, Lattice-snapped sharp lines, PLP Spine.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_package.absolute_constants import *

# 1. TRIPLE BASIN FIELD (The Engine of the User Image)
def get_triple_basin_velocity(x, y, gender, mbti):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Static Vertical Speed
    vy = 1.5 if gender == "M" else 0.8
    vx = 0.0
    
    # 31:1 Dynamics - The '1' is the Basin Pull
    k_loop = 1.0/32.0
    
    # Three Basins (Left, Center, Right)
    basins = [2.0, 8.0, 14.0]
    # Small Woman (I-type) gravitates to Left (2) or Center (8)
    # Big Man (E-type) gravitates to Right (14) or Center (8)
    
    # Decision: Which basin does this identity belong to?
    if gender == "F":
        target_x = 2.0 if ei == "E" else 8.0
    else:
        target_x = 14.0 if ei == "E" else 8.0
        
    # Attraction to Basin
    vx = (target_x - x) * k_loop * 5.0
    
    # PLP Spine Interaction (X+Y=16)
    spine_dist = (x + y) - 16.0
    if abs(spine_dist) < 1.0:
        vx += np.sign(spine_dist) * 0.5 # Reflection force
        
    # Cognitive Jitter (Discrete paths)
    if sn == "N": vx *= 1.2
    if tf == "F": vy *= 0.9
    
    return np.array([vx, vy])

# 2. DISCRETE TRAJECTORY GENERATOR
def generate_discrete_trajectory(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Quasar Layout
    group_map_f = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    group_map_m = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    base_x = group_map_f[f"{ei}{jp}"] if gender == "F" else group_map_m[f"{ei}{jp}"]
    
    # Initial Dispersion (128 individual seeds)
    blood_offset = {"O": 0.1, "A": 0.3, "B": 0.5, "AB": 0.7}[blood]
    x = base_x + blood_offset + (0.2 if sn=="N" else 0.0)
    y = 0.5
    
    pts = [(x, y)]
    dt = 0.5 # Larger steps for sharp lattice-like lines
    
    for _ in range(32): # 32 time steps
        if y >= 16.0: break
        
        V = get_triple_basin_velocity(x, y, gender, mbti)
        x += V[0] * dt
        y += V[1] * dt
        
        # 3/32 Spark Gate Snap (y around 10-12)
        if 10.0 < y < 12.0 and 6.0 < x < 10.0:
            x = np.round((x - 8.0) / 0.09375) * 0.09375 + 8.0
            
        pts.append((x, y))
        
    return pts

# 3. REPLICATING THE AESTHETIC
def main():
    print("Replicating Intuitive Divergence...")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    
    # Draw Background Grid
    for i in range(17):
        ax.axhline(i, color="#EEEEEE", lw=0.5, zorder=0)
        ax.axvline(i, color="#EEEEEE", lw=0.5, zorder=0)
        
    # Landmarks
    ax.plot([0, 16], [16, 0], color="orange", linestyle="--", alpha=0.4, lw=2, label="PLP Spine")
    ax.add_patch(plt.Rectangle((6, 10), 4, 1.5, color="black", alpha=0.05)) # Spark Gate
    
    ALL_MBTI = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    BLOODS = ["O", "A", "B", "AB"]
    BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    for m in ALL_MBTI:
        for b in BLOODS:
            for g in ["M", "F"]:
                pts = generate_discrete_trajectory(m, b, g)
                xs, ys = zip(*pts)
                
                # Use distinct colors for 128 types
                bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[b]))[:3]
                color = 0.7*bc + 0.3*(np.array([1,0.4,0]) if g=="F" else np.array([0,0.4,1]))
                
                # Sharp, clear lines with high visibility
                ax.plot(xs, ys, color=color, alpha=0.6, lw=1.0, zorder=10)

    # Quasar Labels
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -0.8, label, ha="center", weight="bold", size=14)

    ax.set_title("128-TYPE TRUE DIVERGENCE GRID | Basin Dynamics | One Form Logic", 
                 fontsize=26, pad=50, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_TRUE_DIVERGENCE_QUASAR.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Success: Final Intuitive Grid rendered to {output}.")

if __name__ == "__main__":
    main()
