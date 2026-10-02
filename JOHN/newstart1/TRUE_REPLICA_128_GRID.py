# -*- coding: utf-8 -*-
"""
TRUE_REPLICA_128_GRID.py
A precise replica of the 128-Type Pure Geometry Grid.
Matches the architectural aesthetic, labels, and triple-basin physics.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from geometry_package.absolute_constants import *

# 1. ARCHITECTURAL CONSTANTS (From Image Inspection)
AESTHETIC = {
    "bg_color": "#FDFDFD",
    "grid_color": "#EEEEEE",
    "spine_color": "orange",
    "labels": ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"],
    "blood_colors": {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
}

# 2. THE REPLICA PHYSICS ENGINE
def get_replica_velocity(x, y, gender, mbti, blood):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Static Flow vs Loop (31:1)
    vy = 1.5 if gender == "M" else 0.8
    vx = 0.0
    
    # BASIN PHYSICS (The 3-Basin Topology from image)
    # Left Bypass (X=2), Center (X=8), Right Bypass (X=14)
    if gender == "F":
        target_x = 2.0 if ei == "E" else 8.0
    else:
        target_x = 14.0 if ei == "E" else 8.0
        
    # Smooth attraction to basin
    vx = (target_x - x) * 0.12
    
    # 4D TORSION (Swirl near the nodes)
    if 4.0 < y < 8.0:
        vx += np.sin(y * 0.5) * (0.5 if tf == "F" else 0.1)
        
    # PLP SPINE INTERACTION (X+Y=16)
    if abs((x + y) - 16.0) < 0.5:
        vx += 0.3 # Deflection from spine
        
    return np.array([vx, vy])

# 3. DISCRETE SEGMENT GENERATOR
def generate_replica_path(mbti, blood, gender):
    # Starting offset
    group_map = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6} if gender == "F" else {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    base_x = group_map[mbti[0]+mbti[3]]
    
    # Discrete Seed Dispersion
    x = base_x + 1.0 + (0.2 if blood in ["O", "AB"] else -0.2)
    y = 0.5
    start_pos = (x, y)
    
    pts = [start_pos]
    dt = 0.4 # Coarse steps for architectural lines
    
    for _ in range(40):
        if y >= 16.0: break
        
        V = get_replica_velocity(x, y, gender, mbti, blood)
        x += V[0] * dt
        y += V[1] * dt
        
        # LATTICE SNAPPING (3/32 Gate)
        if 9.5 < y < 11.5 and 6.0 < x < 10.0:
            x = np.round((x - 8.0) / 0.09375) * 0.09375 + 8.0
            
        pts.append((x, y))
        
        # DREAM FOLDING (The Reset)
        is_fold = (y >= 13.0 and y < 13.5) if gender == "M" else (y >= 13.5 and y < 14.0)
        if is_fold:
            pts.append(start_pos)
            break
            
    return pts

# 4. RENDERING THE BLUEPRINT
def main():
    print("Executing Precise Architectural Replica...")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor(AESTHETIC["bg_color"])
    
    # 1. Background Grid & Separators
    for i in range(17):
        ax.axhline(i, color=AESTHETIC["grid_color"], lw=0.8, zorder=0)
        ax.axvline(i, color=AESTHETIC["grid_color"], lw=0.8, zorder=0)
    
    # Dotted Separators (X=3, X=13)
    ax.axvline(3, color="gray", linestyle="--", lw=1, alpha=0.3)
    ax.axvline(13, color="gray", linestyle="--", lw=1, alpha=0.3)
    ax.text(3, 1, "Separatrix (X=3)\nDivides Bypass & Center", ha="center", size=10, alpha=0.5)
    ax.text(13, 1, "Separatrix (X=13)\nDivides Bypass & Center", ha="center", size=10, alpha=0.5)

    # 2. Landscapes & Nodes
    ax.plot([0, 16], [16, 0], color="orange", linestyle="--", alpha=0.4, lw=2) # PLP Spine
    ax.text(15.5, 0.5, "PLP Spine X+Y=16", color="orange", weight="bold", size=10)
    
    # Basins
    ax.text(2, 8, "Left Bypass Basin\n(X=2)", color="green", ha="center", alpha=0.3, size=12)
    ax.text(14, 8, "Right Bypass Basin\n(X=14)", color="green", ha="center", alpha=0.3, size=12)
    
    # Center Gate
    ax.add_patch(plt.Rectangle((6, 10), 4, 1.5, color="black", alpha=0.03))
    ax.text(8, 10.75, "Darkness Stress (Nose)\n3/32 Spark Gate", ha="center", weight="bold", size=12, alpha=0.6)
    
    # 3. 128 Trajectories
    ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
    for m in ALL_MBTI:
        for b in ["O", "A", "B", "AB"]:
            for g in ["M", "F"]:
                pts = generate_replica_path(m, b, g)
                xs, ys = zip(*pts)
                
                bc = np.array(plt.cm.colors.to_rgba(AESTHETIC["blood_colors"][b]))[:3]
                gender_tint = np.array([1,0.5,0]) if g=="F" else np.array([0,0.5,1])
                color = 0.8 * bc + 0.2 * gender_tint
                
                ax.plot(xs, ys, color=color, alpha=0.5, lw=0.8, zorder=10)

    # 4. Labels & Title
    for i, label in enumerate(AESTHETIC["labels"]):
        ax.text(i*2 + 1, -0.8, label, ha="center", weight="bold", size=16)

    ax.set_title(f"128-TYPE PURE GEOMETRY GRID | Static:Loop=31:1 | W5={LOOP_STRENGTH_5:.2f} W7=0.157 W11=0.842", 
                 fontsize=28, pad=60, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_TRUE_ARCHITECTURAL_REPLICA.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Final Judgment: Replica rendered to {output}. Analyzing similarity now...")

if __name__ == "__main__":
    main()
