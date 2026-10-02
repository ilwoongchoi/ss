# -*- coding: utf-8 -*-
"""
FINAL_UNIVERSAL_QUASAR_GRID.py
The Ultimate One-Form Grid driven by Universal Spacetime Laws.
Core: 4x4 Temporal Manifold (Macro/Micro Time Windows)
Logic: Time Reversal in Midnight Phase + 31:1 Energy Ratio
Symmetry: Biological Quasar (Extraversion at Edges, Introversion at Center)
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
from geometry_package import universal_equation as unieq

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 1. UNIVERSAL SPACETIME FIELD (No Hardcoding)
def get_universal_field(x, y, gender, t_macro, t_micro, is_reverse):
    """
    Driven by the 31:1 Static:Loop Law.
    Incorporates Time Reversal and Macro/Micro Window physics.
    """
    k_loop = float(F_1_32) # 1/32
    k_static = 1.0 - k_loop # 31/32
    
    # Static Flow (31/32) - Direction flips if time is reversed
    v_speed = 1.5 if gender == "M" else 0.8
    # In Midnight/Reverse phase, the static flow pulls back toward the source
    direction = -1.0 if is_reverse else 1.0
    v_static = np.array([0.0, v_speed * direction])
    
    # Loop Dynamics (1/32) - Dipole + Torsion from Universal Equation
    # Using the Mandelbrot mapping from unieq
    c_real = (x - 8.0) / 8.0
    c_imag = (y - 8.0) / 8.0
    # Mandelbrot unification reflects the "Complexity" of the loop
    z_next = unieq.mandelbrot_unification(complex(0.5, 0.1), complex(c_real, c_imag))
    
    v_loop = np.array([z_next.real, z_next.imag])
    
    # 4D Torsion Swirl
    torsion_strength = 0.1746
    v_torsion = np.array([-(y - 8.0), (x - 8.0)]) * torsion_strength
    
    # Final Unified Velocity
    V = k_static * v_static + k_loop * (v_loop + v_torsion)
    
    # Scaling for visualization (matches the Quasar aesthetic)
    lat_amp = 2.8 if gender == "F" else 1.2
    V[0] *= lat_amp
    
    return V

# 2. 4x4 TEMPORAL MANIFOLD TRAJECTORY GENERATOR
def generate_universal_trajectory(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # QUASAR SYMMETRY: E(Extreme) -> I(Inside)
    group_map_f = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    group_map_m = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    base_x = group_map_f[f"{ei}{jp}"] if gender == "F" else group_map_m[f"{ei}{jp}"]
    
    # Start coordinates (Normalized to the 4x4 Manifold start)
    x = base_x + 1.0 + (0.25 if sn=="N" else -0.25)
    y = 0.5 + (0.06 if blood=="O" else -0.06)
    
    pts = [(x, y)]
    dt = 0.1
    
    # Iterate through the 28-day Lunar Cycle (Macro Windows)
    # Divided into 16 steps (4 Macro * 4 Micro)
    for t_step in range(16):
        # Determine Macro/Micro window and Time Direction
        # This logic is central to the "One Form" closure
        t_macro = t_step // 4
        t_micro = t_step % 4
        
        # Time Reversal Logic: Phase 3 (Midnight) is reversed
        is_reverse = (t_macro == 3)
        
        target_y = t_step + 1.0
        
        while (not is_reverse and y < target_y) or (is_reverse and y > target_y - 1.0):
            step = min(dt, abs(target_y - y))
            if step < 1e-6: break
            
            V = get_universal_field(x, y, gender, t_macro, t_micro, is_reverse)
            
            # Update position based on universal field
            x = max(0, min(16, x + V[0] * dt))
            # Y movement is controlled by the Macro window flow
            y += V[1] * dt * (0.5 if is_reverse else 1.0)
            
            # Spark Gate / Tunnelling check (Happens in the "Darkness" phase)
            if t_macro >= 2 and 6.0 < x < 10.0:
                # 3/32 Spark Gate logic
                x = np.round((x - 8.0) / 0.09375) * 0.09375 + 8.0
                pts.append((x, y))
                # Leap toward singularity
                x += float(SPARK_LEAP_DIST) * np.cos(np.radians(SPARK_ANGLE_DEG))
                y += float(SPARK_LEAP_DIST) * np.sin(np.radians(SPARK_ANGLE_DEG))
                break # Exit current micro window early via the leap

            if len(pts) > 500: break # Safety break
            pts.append((x, y))
            
    return pts

# 3. RENDERER
def main():
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    
    # Draw the 4x4 Temporal Grid
    for i in range(5):
        # Macro Borders
        ax.axhline(i*4, color="black", lw=2.0, alpha=0.3)
        # Micro Borders
        for j in range(1, 4):
            ax.axhline(i*4 - j, color="gray", lw=0.5, alpha=0.2, linestyle="--")
            
    # Draw Universal Landmarks
    ax.add_patch(mpatches.Rectangle((6, 8), 4, 8, color="black", alpha=0.05, label="H4 Void (Midnight Zone)"))
    ax.plot([0, 16], [16, 0], color="orange", linestyle="--", alpha=0.3, lw=2) # PLP Spine
    
    # 128 Trajectories
    ALL_MBTI = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    print("Simulating Universal 4x4 Manifold...")
    for m in ALL_MBTI:
        for b in ["O", "A", "B", "AB"]:
            for g in ["M", "F"]:
                pts = generate_universal_trajectory(m, b, g)
                xs, ys = zip(*pts)
                
                bc = np.array(matplotlib.colors.to_rgba(BLOOD_COLORS[b]))[:3]
                tint = np.array([1.0, 0.5, 0.1]) if g == "F" else np.array([0.1, 0.6, 1.0])
                color = 0.75 * bc + 0.25 * tint
                ax.plot(xs, ys, color=color, alpha=0.35, lw=1.0, zorder=10)

    # Column Labels (Quasar Symmetry)
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -1.0, label, ha="center", weight="bold", size=14)

    ax.set_title("UNIVERSAL 4x4 QUASAR MANIFOLD | Static:Loop=31:1 | Time Reversal Enabled", 
                 fontsize=28, pad=60, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_UNIVERSAL_QUASAR_GRID.png"
    plt.savefig(output, dpi=300)
    print(f"Success: {output} rendered. Check the Midnight Reversal convergence.")

if __name__ == "__main__":
    main()
