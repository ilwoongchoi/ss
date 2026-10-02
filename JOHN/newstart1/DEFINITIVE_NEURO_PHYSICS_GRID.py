# -*- coding: utf-8 -*-
"""
DEFINITIVE_NEURO_PHYSICS_GRID.py
The final grid engine, driven by the user's explicit neurochemical toggle rules.
- D2 = Extraversion Switch
- T/F = Hormonal Forces (Testosterone/Estrogen/Progesterone)
- NT/ST/NF/SF = Social Attraction/Repulsion
- J = GABAergic Damping
- Blood Type = Metabolic Profile (Mass, Energy)
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_package.absolute_constants import *

# 1. NEUROCHEMICAL -> PHYSICAL MAPPING
def get_neuro_params(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Base Gender Polarity & Speed
    vy = 1.5 if gender == "M" else 0.8
    
    # Blood Type: Metabolic Profile
    # O=High Energy/Mass, A=Structure/Damping, B=Voltage/Chaos, AB=Integrator/Low Mass
    mass = {"O": 1.5, "A": 1.2, "B": 0.9, "AB": 0.6}[blood]
    energy = {"O": 1.2, "A": 0.9, "B": 1.1, "AB": 1.0}[blood]
    
    # T/F Hormonal Forces
    # T=Resistance to Big Opposite, F=Amity to Small
    testosterone = 1.0 if tf == "T" else 0.0
    estrogen = 1.0 if tf == "F" else 0.0
    
    # S/N -> Right D2 (Creativity) Affinity
    # N-types have a higher chance of activating Right D2
    r_d2_affinity = 1.0 if sn == "N" else 0.2
    
    # J -> GABA Damping
    damping = 1.2 if jp == "J" else 0.5
    
    return {
        "vy": vy, "mass": mass, "energy": energy,
        "T": testosterone, "E": estrogen,
        "r_d2_affinity": r_d2_affinity, "damping": damping,
        "ei": ei, "sn": sn, "tf": tf, "jp": jp, "gender": gender
    }

# 2. THE SIMULATION ENGINE
def generate_neuro_path(mbti, blood, gender, all_trajectories):
    params = get_neuro_params(mbti, blood, gender)
    
    # Starting Position (Quasar Symmetry)
    group_map = {"EJ":0,"EP":2,"IJ":4,"IP":6} if gender=="F" else {"IP":8,"IJ":10,"EP":12,"EJ":14}
    x = group_map[params["ei"]+params["jp"]] + 1.0
    y = 0.5
    start_pos = np.array([x, y])
    
    pts = [start_pos.copy()]
    curr_pos = start_pos.copy()
    dt = 0.1
    
    # State variables
    d2_right_on = np.random.rand() < params["r_d2_affinity"] * 0.5

    for step in range(200):
        if curr_pos[1] >= 16.0: break
        
        # A. D2 EXTRAVERSION FORCE
        # D2 activates attraction to the opposite side's "Extraversion Zone"
        vx_ext = 0.0
        if (gender == "F" and not d2_right_on) or (gender == "M" and d2_right_on): # Left D2 ON
             # Attracted to LEFT Extraversion zone (imagined)
            vx_ext = (2.0 - curr_pos[0]) * 0.1
        else: # Right D2 ON
            # Attracted to RIGHT Extraversion zone
            vx_ext = (14.0 - curr_pos[0]) * 0.1

        # B. HORMONAL & SOCIAL FORCES
        # Simplified: T resists, F attracts
        vx_social = 0.0
        if params["T"] > 0: vx_social -= np.sign(curr_pos[0] - 8.0) * 0.05 # Resist cross
        if params["E"] > 0: vx_social += np.sign(8.0 - curr_pos[0]) * 0.05 # Attract cross
            
        # C. BASE PHYSICS
        vx_total = (vx_ext + vx_social) * params["energy"]
        vy_total = params["vy"]
        
        # D. DAMPING & MASS
        v_final = np.array([vx_total, vy_total]) / params["mass"]
        v_final *= params["damping"]

        curr_pos += v_final * dt
        
        # DREAM FOLDING (The 45-min Rule)
        is_fold = (curr_pos[1] >= 13.0 and curr_pos[1] < 13.5) if gender == "M" else (curr_pos[1] >= 13.5 and curr_pos[1] < 14.0)
        if is_fold:
            pts.append(start_pos.copy())
            break

        pts.append(curr_pos.copy())
    
    return pts

# 3. RENDERING
def main():
    print("Simulating Neuro-Physical Grid...")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    
    for i in range(17): ax.axhline(i, color="#F5F5F5", lw=0.5); ax.axvline(i, color="#F5F5F5", lw=0.5)

    MBTI_16 = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
    BLOODS = ["O", "A", "B", "AB"]
    BLOOD_COLORS = {"O":"#D32F2F","A":"#1976D2","B":"#388E3C","AB":"#7B1FA2"}
    
    all_trajectories = {}
    
    # Generate all trajectories first to enable social interaction logic
    for m in MBTI_16:
        for b in BLOODS:
            for g in ["M", "F"]:
                key = f"{m}-{b}-{g}"
                all_trajectories[key] = generate_neuro_path(m, b, g, all_trajectories)

    # Render trajectories
    for key, pts in all_trajectories.items():
        m, b, g = key.split('-')
        xs, ys = zip(*pts)
        bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[b]))[:3]
        color = 0.7 * bc + 0.3 * (np.array([1,0.5,0]) if g=="F" else np.array([0,0.5,1]))
        ax.plot(xs, ys, color=color, alpha=0.4, lw=0.9)

    labels = ["EJ WOMEN","EP WOMEN","IJ WOMEN","IP WOMEN","IP MEN","IJ MEN","EP MEN","EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -0.8, label, ha="center", weight="bold", size=14)

    ax.set_title("128-TYPE NEURO-PHYSICAL GRID", fontsize=28, pad=50, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_DEFINITIVE_NEURO_PHYSICS.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Success: {output} rendered.")

if __name__ == "__main__":
    main()
