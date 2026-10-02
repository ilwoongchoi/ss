# -*- coding: utf-8 -*-
"""
AUTONOMOUS_PERFECT_QUASAR_GRID.py
Autonomous Rendering Engine for the 128-Type "One Form".
Final Judgment: Organic Convergence, White Aesthetic, Universal Physics.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_package.absolute_constants import *
from geometry_package import universal_equation as unieq

# 1. ORGANIC FIELD ENGINE (Enhanced Curvature)
def get_organic_quasar_field(x, y, gender, t_macro, is_folding):
    k_loop = float(F_1_32)
    k_static = 1.0 - k_loop
    
    # Static Flow (31/32)
    direction = -1.0 if t_macro == 3 else 1.0
    v_speed = 1.5 if gender == "M" else 0.8
    v_static = np.array([0.0, v_speed * direction])
    
    # Loop Dynamics (1/32) - HEAVILY REINFORCED for Organic Flow
    # Quasar Torsion + Dipole
    c_real, c_imag = (x - 8.0) / 8.0, (y - 8.0) / 8.0
    z_unified = unieq.mandelbrot_unification(complex(0.5, 0.1), complex(c_real, c_imag))
    
    # 11:7 Betti Torsion (Curvature)
    v_torsion = np.array([-(y - 8.0), (x - 8.0)]) * 0.45 # Increased for visible swirl
    v_loop = np.array([z_unified.real, z_unified.imag]) * 2.0 + v_torsion
    
    # 45-MINUTE SINGULARITY FUNNEL (The "One Time" Difference)
    if is_folding:
        target_singularity = np.array([8.0, 0.5]) # Convergence point
        curr_pos = np.array([x, y])
        dist = np.linalg.norm(curr_pos - target_singularity)
        # Super-gravity during folding window
        v_funnel = (target_singularity - curr_pos) * (15.0 / (dist + 0.1))
        return v_funnel # Pure convergence overrides everything
        
    return k_static * v_static + k_loop * v_loop

# 2. HIGH-FIDELITY GENERATOR
def generate_organic_trajectory(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Quasar Symmetry Grid Mapping
    group_map_f = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    group_map_m = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    base_x = group_map_f[f"{ei}{jp}"] if gender == "F" else group_map_m[f"{ei}{jp}"]
    
    # Initial seed point
    x = base_x + 1.0 + (0.1 if sn=="N" else -0.1)
    y = 0.5 + (0.05 if blood=="O" else -0.05)
    start_pos = (x, y)
    
    pts = [start_pos]
    dt = 0.04 # Finer time steps for smoother curves
    curr_pos = np.array([x, y])
    
    for step in range(500):
        t_macro = int((step * dt) / 4) % 4
        y_now = curr_pos[1]
        
        # Gender-specific Folding Windows (The 45-min Rule)
        if gender == "M":
            is_folding = (y_now >= 13.0 and y_now < 13.5)
        else:
            is_folding = (y_now >= 13.5 and y_now < 14.0)
            
        V = get_organic_quasar_field(curr_pos[0], curr_pos[1], gender, t_macro, is_folding)
        
        # Cognitive Modulators (Shape the divergence)
        amp = 2.8 if gender == "F" else 1.2
        if ei == "I": amp *= 0.6
        if tf == "F": V[0] *= 1.4 # Emotional lateral expansion
        
        curr_pos += V * amp * dt
        
        # Singularity Lock (After folding window, stay unified)
        if step > 400 and np.linalg.norm(curr_pos - np.array([base_x+1.0, 0.5])) < 0.2:
            curr_pos = np.array([base_x+1.0, 0.5])
            
        pts.append(curr_pos.copy())
        if step > 450 and np.linalg.norm(curr_pos - np.array([base_x+1.0, 0.5])) < 0.01:
            break
            
    return pts

# 3. FINAL AESTHETIC RENDERING
def main():
    print("Initiating Final Intuitive Rendering...")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    
    # Organic Grid (Light and airy)
    for i in range(17):
        ax.axhline(i, color="#F0F0F0", lw=0.8, zorder=0)
        ax.axvline(i, color="#F0F0F0", lw=0.8, zorder=0)
        
    # Landmarks from the intuition image
    ax.add_patch(plt.Rectangle((6, 10), 4, 1.5, color="black", alpha=0.03, label="3/32 Spark Gate"))
    ax.plot([0, 16], [16, 0], color="orange", linestyle=":", alpha=0.2, lw=1) # PLP Spine
    
    ALL_MBTI = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    for m in ALL_MBTI:
        for b in ["O", "A", "B", "AB"]:
            for g in ["M", "F"]:
                pts = generate_organic_trajectory(m, b, g)
                xs, ys = zip(*pts)
                
                # Aesthetic Color Blending
                bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[b]))[:3]
                gender_tint = np.array([1.0, 0.6, 0.2]) if g == "F" else np.array([0.2, 0.6, 1.0])
                color = 0.85 * bc + 0.15 * gender_tint
                
                # Thin, ethereal lines to show "Form" through density
                ax.plot(xs, ys, color=color, alpha=0.2, lw=0.6, zorder=10)

    # Quasar Labels
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -0.8, label, ha="center", weight="bold", size=14, color="#333333")

    ax.set_title("THE 128-TYPE BIOLOGICAL QUASAR | THE ONE FORM (DREAM FOLDING)", 
                 fontsize=28, pad=60, weight="bold", color="#111111")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_PERFECT_INTUITIVE_QUASAR.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Final Judgment: SUCCESS. Intuition Image rendered to {output}.")

if __name__ == "__main__":
    main()
