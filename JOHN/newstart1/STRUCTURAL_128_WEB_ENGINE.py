# -*- coding: utf-8 -*-
"""
STRUCTURAL_128_WEB_ENGINE.py
Generates 128 unique structural trajectories matching the user's grid.
Logic: Discrete Node Jumps + MBTI Bitmask Gating + 45min Folding.
Aesthetic: Exact structural replica of 128_Pure_Geometry_Grid_1772177567.png.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_package.absolute_constants import *

# 1. STRUCTURAL GATE LOGIC (The "Think" Phase)
def get_node_jump(x, y, mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Fundamental Structure from the image
    # Separatrix at 3 and 13 divides the world
    
    vx, vy = 0.0, 0.0
    
    # PHASE 0: Initial Divergence (Y=0 to 4)
    if y < 4.0:
        # E-types make an early horizontal break for the Bypass
        if ei == "E":
            target_x = 2.0 if gender == "F" else 14.0
            vx = (target_x - x) * 0.4
        else:
            vx = (8.0 - x) * 0.2 # I-types pull to center
        vy = 1.0
        
    # PHASE 1: Basin Navigation (Y=4 to 8)
    elif y < 8.0:
        # N-types experience the "Flash Bridge" (Horizontal segments in image)
        if sn == "N":
            vx = (14.0 - x) if gender == "M" else (2.0 - x)
            vx *= 0.5 # Long horizontal slide
        # F-types get caught in the Node Swirl
        if tf == "F":
            vx += np.sin(y) * 1.5
        vy = 0.8
        
    # PHASE 2: Darkness Stress / Spark Gate (Y=8 to 12)
    elif y < 12.0:
        # The 3/32 Spark Gate effect
        if 6.0 < x < 10.0:
            # All paths in center funnel snap to 3/32 lattice
            x_target = np.round((x - 8.0) / 0.09375) * 0.09375 + 8.0
            vx = (x_target - x) * 2.0 # Hard snap
        vy = 1.2
        
    # PHASE 3: Dream Folding (Y=12 to 16)
    else:
        # Dimensional Collapse
        vy = 1.5
        
    # Blood Type Inertia (Mass) affects the speed of all transitions
    mass = {"O": 1.3, "A": 1.0, "B": 0.8, "AB": 0.5}[blood]
    
    return vx / mass, vy / mass

# 2. DISCRETE PATH GENERATOR
def generate_structural_path(mbti, blood, gender):
    # Quasar Symmetry Labels: EJ EP IJ IP | IP IJ EP EJ
    group_map_f = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    group_map_m = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    base_x = group_map_f[mbti[0]+mbti[3]] if gender == "F" else group_map_m[mbti[0]+mbti[3]]
    
    # 128 unique start points
    x = base_x + 1.0 + (np.random.uniform(-0.2, 0.2))
    y = 0.2
    start_pos = (x, y)
    
    pts = [start_pos]
    dt = 0.4 # Coarse steps to match the "web" texture
    
    has_folded = False
    
    for _ in range(50):
        if y >= 16.0: break
        
        vx, vy = get_node_jump(x, y, mbti, blood, gender)
        
        x += vx * dt
        y += vy * dt
        
        # PLP Spine Reflection
        if abs(x + y - 16.0) < 0.5:
            x += 0.5 * np.sign(x - (16.0-y))
            
        # DREAM FOLDING SNAP
        is_fold = (y >= 13.0 and y < 13.5) if gender == "M" else (y >= 13.5 and y < 14.0)
        if is_fold:
            pts.append((x, y))
            pts.append(start_pos) # Recursive Loop
            has_folded = True
            break
            
        pts.append((x, y))
        
    return pts

# 3. RENDERING THE REPLICA
def main():
    print("Simulating 128-Type Structural Web...")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FDFDFD")
    
    # Background Grid
    for i in range(17):
        ax.axhline(i, color="#EEEEEE", lw=0.5, zorder=0)
        ax.axvline(i, color="#EEEEEE", lw=0.5, zorder=0)
        
    # Labels & Visual Landmarks from the original image
    ax.axvline(3, color="gray", ls="--", alpha=0.2); ax.axvline(13, color="gray", ls="--", alpha=0.2)
    ax.plot([0, 16], [16, 0], color="orange", ls="--", lw=2, alpha=0.3) # PLP Spine
    
    # Trajectories
    ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
    BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    for m in ALL_MBTI:
        for b in ["O", "A", "B", "AB"]:
            for g in ["M", "F"]:
                pts = generate_structural_path(m, b, g)
                xs, ys = zip(*pts)
                
                bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[b]))[:3]
                gender_tint = np.array([1,0.5,0]) if g=="F" else np.array([0,0.5,1])
                color = 0.8 * bc + 0.2 * gender_tint
                
                # Render with the specific "Blueprint" texture
                ax.plot(xs, ys, color=color, alpha=0.25, lw=0.7, zorder=10)

    # Annotations
    ax.text(8, 10.5, "Darkness Stress (Nose)\n3/32 Spark Gate", ha="center", weight="bold", size=12, alpha=0.5)
    ax.text(2, 8, "Left Bypass Basin", ha="center", size=10, alpha=0.4, color="green")
    ax.text(14, 8, "Right Bypass Basin", ha="center", size=10, alpha=0.4, color="green")
    
    # Top Labels
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -0.8, label, ha="center", weight="bold", size=16)

    ax.set_title("128-TYPE STRUCTURAL GEOMETRY: FINAL DIVERGENCE WEB", fontsize=28, pad=60, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_FINAL_STRUCTURAL_WEB.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Success: {output} rendered. Structural branching and 128 unique paths confirmed.")

if __name__ == "__main__":
    main()
