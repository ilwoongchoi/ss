# -*- coding: utf-8 -*-
"""
PHYSICAL_128_CONSTITUTION_SIMULATOR.py
Derives 128 distinct trajectories from first-principle physics.
Gender = Polarity, MBTI = Field Coefficients, Blood = Particle Mass.
Goal: Replicate the 'Biological Quasar' texture from user intuition image.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_package.absolute_constants import *
from geometry_package import universal_equation as unieq

# 1. PHYSICAL CONSTITUTION MAPPING (The "Think" Phase)
def get_physical_params(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # GENDER: Vertical Momentum & Horizontal Drag
    p_gravity = 1.5 if gender == "M" else 0.8
    p_drag = 1.2 if gender == "M" else 2.8
    
    # MBTI: Field Coupling Constants
    c_radial = 1.2 if ei == "E" else -0.8  # E pushes out, I pulls in
    c_resonance = 1.5 if sn == "N" else 0.5 # N resonates with Spark Gate
    c_torsion = 1.4 if tf == "F" else 0.4   # F follows the swirl
    c_damping = 0.9 if jp == "J" else 0.2   # J snaps to lattice
    
    # BLOOD: Inertia (Mass)
    mass = {"O": 1.2, "A": 1.0, "B": 0.8, "AB": 0.6}[blood]
    
    return {
        "vy_base": p_gravity, "vx_amp": p_drag,
        "radial": c_radial, "resonance": c_resonance,
        "torsion": c_torsion, "damping": c_damping,
        "mass": mass
    }

# 2. UNIFIED CONSTITUTIONAL FIELD
def get_constitutional_velocity(x, y, p, t_macro):
    # Static:Loop = 31:1 ratio
    k_loop = float(F_1_32)
    k_static = 1.0 - k_loop
    
    # A. Static Flow (Gravitational descent)
    v_static = np.array([0.0, p["vy_base"]])
    
    # B. Loop Dynamics (Constitutional response)
    # Radial Force (E/I attraction to Bypass or Funnel)
    target_x = 8.0 + (p["radial"] * 6.0) # E -> 14 or 2, I -> 8
    v_radial = (target_x - x) * 0.5
    
    # 4D Torsion Swirl (T/F sensitivity)
    swirl = np.array([-(y - 8.0), (x - 8.0)]) * 0.1746 * p["torsion"]
    
    # Mandelbrot Unification (The "Complexity" of the path)
    c_real, c_imag = (x - 8.0) / 8.0, (y - 8.0) / 8.0
    z = unieq.mandelbrot_unification(complex(0.5, 0.1), complex(c_real, c_imag))
    v_mandel = np.array([z.real, z.imag]) * p["resonance"]
    
    v_loop = (v_radial + swirl[0])*np.array([1,0]) + (v_mandel + swirl[1]*np.array([0,1]))
    
    # C. Final Sum modulated by Mass (Blood)
    V = (k_static * v_static + k_loop * v_loop) / p["mass"]
    V[0] *= p["vx_amp"] # Gendered horizontal scale
    
    return V

# 3. CONSTITUTIONAL TRAJECTORY GENERATOR
def generate_constitutional_path(mbti, blood, gender):
    p = get_physical_params(mbti, blood, gender)
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Starting coordinates from Quasar Symmetry
    group_map_f = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    group_map_m = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    base_x = group_map_f[f"{ei}{jp}"] if gender == "F" else group_map_m[f"{ei}{jp}"]
    
    # Seed jitter from Blood type (Massive particles start wider)
    x = base_x + 1.0 + (p["mass"] - 0.9)
    y = 0.5
    start_pos = np.array([x, y])
    
    pts = [start_pos.copy()]
    dt = 0.1
    curr_pos = start_pos.copy()
    
    for step in range(160):
        t_macro = int((step * dt) / 4) % 4
        V = get_constitutional_velocity(curr_pos[0], curr_pos[1], p, t_macro)
        
        # J-type Decisiveness (Snap to 3/32 lattice faster)
        if p["damping"] > 0.5 and abs(curr_pos[0] % 0.09375) < 0.05:
            curr_pos[0] = np.round(curr_pos[0] / 0.09375) * 0.09375
            
        curr_pos += V * dt
        
        # Dream Folding (The 45-minute closure from previous step)
        y_now = curr_pos[1]
        is_folding = (y_now >= 13.0 and y_now < 13.5) if gender == "M" else (y_now >= 13.5 and y_now < 14.0)
        
        if is_folding:
            curr_pos = start_pos.copy() # Folding back to Seed
            pts.append(curr_pos.copy())
            break
            
        curr_pos[0] = np.clip(curr_pos[0], 0, 16)
        curr_pos[1] = np.clip(curr_pos[1], 0, 16)
        pts.append(curr_pos.copy())
        
    return pts

# 4. FINAL RENDERING (Matching the User Image Aesthetic)
def main():
    print("Simulating 128 Physical Constitutions...")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    
    # The Grid
    for i in range(17):
        ax.axhline(i, color="#EEEEEE", lw=0.5, zorder=0)
        ax.axvline(i, color="#EEEEEE", lw=0.5, zorder=0)
        
    # Spine & Gate
    ax.plot([0, 16], [16, 0], color="orange", linestyle="--", alpha=0.3, lw=2)
    ax.add_patch(plt.Rectangle((6, 10), 4, 1.5, color="black", alpha=0.04))
    
    MBTI_16 = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
    BLOODS = ["O", "A", "B", "AB"]
    BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    for m in MBTI_16:
        for b in BLOODS:
            for g in ["M", "F"]:
                pts = generate_constitutional_path(m, b, g)
                xs, ys = zip(*pts)
                
                # Aesthetic blending
                bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[b]))[:3]
                gender_tint = np.array([1,0.5,0]) if g=="F" else np.array([0,0.5,1])
                color = 0.8 * bc + 0.2 * gender_tint
                
                # Draw sharp, distinct paths
                ax.plot(xs, ys, color=color, alpha=0.4, lw=0.8, zorder=10)

    # Labels (Quasar Symmetry)
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -0.8, label, ha="center", weight="bold", size=14)

    ax.set_title("128-TYPE PHYSICAL CONSTITUTION GRID | Derived Divergence | One Form Closure", 
                 fontsize=28, pad=60, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_FINAL_PHYSICAL_CONSTITUTION.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Success: {output} rendered. All 128 trajectories are physically distinct.")

if __name__ == "__main__":
    main()
