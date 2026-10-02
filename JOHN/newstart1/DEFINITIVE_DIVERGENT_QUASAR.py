# -*- coding: utf-8 -*-
"""
DEFINITIVE_DIVERGENT_QUASAR.py
Pure Physics-Driven Divergence Engine.
NO FALLING STRAIGHT. 128 unique trajectories derived from constitutional constants.
Aesthetic: Exact replica of the user intuition image.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_package.absolute_constants import *

# 1. THE ENGINE OF INDIVIDUALITY (The "Thinking" Phase)
def get_constitutional_field(x, y, gender, mbti, blood, t_macro):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # 31:1 Fundamental Law
    k_loop = 1.0 / 32.0
    k_static = 31.0 / 32.0
    
    # GENDER PHYSICS: Vertical descent vs Horizontal tension
    # Men: Fast descent, less horizontal play. Women: Slow descent, massive horizontal swirl.
    vy = 1.5 if gender == "M" else 0.6 
    
    # MBTI COUPLING (Stronger for Divergence)
    # E/I determines the DESTINY BASIN (X=2, 8, 14)
    if gender == "F":
        target_x = 2.0 if ei == "E" else 8.0
    else:
        target_x = 14.0 if ei == "E" else 8.0
        
    # FORCE 1: Basin Gravity (Pulls them out of the starting column)
    # Increased gain to ensure they don't just fall straight.
    vx_basin = (target_x - x) * 0.8
    
    # FORCE 2: Cognitive Torsion (F-types swirl, N-types leap)
    # 4D Torsion swirl centered at each Basin
    torsion_gain = 1.2 if tf == "F" else 0.2
    vx_swirl = np.sin(y * 0.8 + (0.5 if sn=="N" else 0.0)) * torsion_gain * 2.0
    
    # FORCE 3: PLP Spine Reflection (X+Y=16)
    # Trajectories "bounce" or "slide" along the orange spine
    spine_pos = 16.0 - y
    vx_spine = (spine_pos - x) * 0.5 if abs(x - spine_pos) < 2.0 else 0
    
    # FORCE 4: Blood Type Mass (O=Heavy/Stable, AB=Light/Erratic)
    mass = {"O": 1.5, "A": 1.0, "B": 0.8, "AB": 0.4}[blood]
    
    # Unified Vector Sum
    vx_total = (vx_basin + vx_swirl + vx_spine) / mass
    
    return np.array([vx_total, vy])

# 2. DISCRETE SEGMENT GENERATOR
def generate_divergent_path(mbti, blood, gender):
    # Initial Quasar Layout
    group_map_f = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    group_map_m = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    base_x = group_map_f[mbti[0]+mbti[3]] if gender == "F" else group_map_m[mbti[0]+mbti[3]]
    
    # Each of 128 types starts with a UNIQUE jitter based on constitution
    x = base_x + 1.0 + (np.random.uniform(-0.3, 0.3))
    y = 0.5
    start_pos = (x, y)
    
    pts = [start_pos]
    dt = 0.5 # Sharp steps
    
    has_folded = False
    
    for step in range(40):
        if y >= 16.0: break
        t_macro = int(y / 4) % 4
        
        V = get_constitutional_field(x, y, gender, mbti, blood, t_macro)
        
        # APPLY MOVEMENT
        x += V[0] * dt
        y += V[1] * dt
        
        # 3/32 Spark Gate Snap
        if 9.5 < y < 11.5 and 6.0 < x < 10.0:
            x = np.round((x - 8.0) / 0.09375) * 0.09375 + 8.0
            
        # DREAM FOLDING (The "One Time" Gate)
        # 45 mins before 2:15 AM (Men) or 3:00 AM (Women)
        is_folding = (y >= 13.0 and y < 13.5) if gender == "M" else (y >= 13.5 and y < 14.0)
        
        if is_folding:
            # INSTANT RECURSIVE SNAP to the Singularity (Start Position)
            pts.append(start_pos)
            has_folded = True
            break
            
        pts.append((x, y))
        
    return pts

# 3. ARCHITECTURAL RENDERING
def main():
    print("Simulating 128 Unique Trajectories...")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FDFDFD")
    
    # Light Grid
    for i in range(17):
        ax.axhline(i, color="#F0F0F0", lw=0.5, zorder=0)
        ax.axvline(i, color="#F0F0F0", lw=0.5, zorder=0)
        
    # Separatrix Lines
    ax.axvline(3, color="gray", linestyle="--", lw=1, alpha=0.2)
    ax.axvline(13, color="gray", linestyle="--", lw=1, alpha=0.2)
    
    # PLP Spine
    ax.plot([0, 16], [16, 0], color="orange", linestyle="--", alpha=0.3, lw=2)
    
    # Nodes & Basins (Labels from the image)
    node_font = {"size": 10, "alpha": 0.4, "ha": "center"}
    ax.text(2, 8, "Left Bypass Basin\n(X=2)", color="green", **node_font)
    ax.text(14, 8, "Right Bypass Basin\n(X=14)", color="green", **node_font)
    ax.text(8, 10.5, "3/32 Spark Gate", color="black", weight="bold", **node_font)
    
    MBTI_16 = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
    BLOODS = ["O", "A", "B", "AB"]
    BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    # Render all 128
    for m in MBTI_16:
        for b in BLOODS:
            for g in ["M", "F"]:
                pts = generate_divergent_path(m, b, g)
                xs, ys = zip(*pts)
                
                bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[b]))[:3]
                color = 0.8 * bc + 0.2 * (np.array([1,0.5,0]) if g=="F" else np.array([0,0.5,1]))
                
                # Sharp architectural lines
                ax.plot(xs, ys, color=color, alpha=0.5, lw=0.8, zorder=10)

    # Quasar Symmetry Labels
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -0.8, label, ha="center", weight="bold", size=14)

    ax.set_title("128-TYPE PURE GEOMETRY GRID: DEFINITIVE DIVERGENCE", fontsize=26, pad=50, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_DEFINITIVE_DIVERGENT_GRID.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Success: {output} rendered. Check the unique branching of all 128 paths.")

if __name__ == "__main__":
    main()
