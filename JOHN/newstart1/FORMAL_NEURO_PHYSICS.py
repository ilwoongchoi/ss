# -*- coding: utf-8 -*-
"""
FORMAL_NEURO_PHYSICS.py
A formal physics engine for the 128-type quasar.
- Social forces are modeled as Lennard-Jones & Coulombic potentials.
- D2 Toggle is a metaparameter switch changing the particle's constitution.
- Blood Types are mapped to physical constants (mass, damping, resonance).
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_package.absolute_constants import *

# 1. FORMAL MAPPING: Neurochemistry -> Physics
def get_formal_params(mbti, blood, gender, d2_state):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # D2 Toggle modifies the base EI state
    effective_ei = ei
    if (gender == "F" and d2_state == "R") or (gender == "M" and d2_state == "L"):
        effective_ei = "E" # Lie/Extraversion Switch ON
    
    # Blood Type -> Physical Constants
    # O=High Mass/Inertia, A=High Damping/Stability, B=High Resonance/Chaos, AB=Low Mass/Reactive
    mass = {"O": 1.5, "A": 1.2, "B": 1.0, "AB": 0.7}[blood]
    damping = {"O": 0.5, "A": 1.5, "B": 0.8, "AB": 1.0}[blood]
    resonance = {"O": 0.6, "A": 0.2, "B": 1.5, "AB": 1.0}[blood]
    
    # Gender -> Base Momentum
    vy_base = 1.5 if gender == "M" else 0.8
    
    # MBTI -> Field Interaction Coefficients
    target_x = (14.0 if effective_ei == "E" else 8.0) if gender == "M" else (2.0 if effective_ei == "E" else 8.0)
    
    return {
        "mass": mass, "damping": damping, "resonance": resonance,
        "vy_base": vy_base, "target_x": target_x,
        "is_T": tf == "T", "is_F": tf == "F",
        "mbti": mbti, "gender": gender, "blood": blood
    }

# 2. POTENTIAL-BASED FORCE CALCULATOR
def calculate_forces(particle, all_particles):
    params = particle["params"]
    pos = particle["pos"]
    
    # Base 31:1 Physics
    v_static = np.array([0.0, params["vy_base"]])
    v_basin = (params["target_x"] - pos[0]) * 0.1
    
    # Social/Hormonal Potentials (Pairwise interactions)
    f_social = np.zeros(2)
    for other in all_particles:
        if other["id"] == particle["id"]: continue
        
        d = other["pos"] - pos
        dist = np.linalg.norm(d)
        if dist < 0.1: continue
            
        # T-type Resistance to Big Opposite
        if params["is_T"]:
            # Simplified: Check if other is "Big" (E) and opposite gender
            if other["params"]["ei"] == "E" and other["params"]["gender"] != params["gender"]:
                f_social -= (d / dist**3) * 0.5 # Repulsive 1/r^2
                
        # F-type Amity/Camaraderie
        if params["is_F"]:
             f_social += (d / dist**3) * 0.2 # Weak general attraction
    
    # Final force vector
    F = np.array([v_basin + f_social[0], v_static[1]])
    
    return F

# 3. SIMULATION ENGINE
def run_simulation():
    print("Initiating Formal Neuro-Physical Simulation...")
    # Initialize all 128 particles
    particles = []
    pid = 0
    for mbti in ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]:
        for blood in ["O","A","B","AB"]:
            for gender in ["M","F"]:
                params = get_formal_params(mbti, blood, gender, "L" if gender=="F" else "R")
                group_map = {"EJ":0,"EP":2,"IJ":4,"IP":6} if gender=="F" else {"IP":8,"IJ":10,"EP":12,"EJ":14}
                x_start = group_map[params["mbti"][0]+params["mbti"][3]] + 1.0
                
                particles.append({
                    "id": pid,
                    "params": params,
                    "pos": np.array([x_start, 0.5]),
                    "vel": np.zeros(2),
                    "path": [np.array([x_start, 0.5])]
                })
                pid += 1

    # Time evolution
    dt = 0.1
    for step in range(200):
        # Calculate forces for all particles
        forces = [calculate_forces(p, particles) for p in particles]
        
        # Update positions
        for i, p in enumerate(particles):
            accel = forces[i] / p["params"]["mass"]
            p["vel"] += accel * dt
            p["vel"] *= p["params"]["damping"] # Apply damping
            p["pos"] += p["vel"] * dt
            p["path"].append(p["pos"].copy())
            
            # Dream Folding
            is_fold = (p["pos"][1] >= 13.0 and p["pos"][1] < 13.5) if p["params"]["gender"]=="M" else (p["pos"][1] >= 13.5 and p["pos"][1] < 14.0)
            if is_fold:
                p["path"].append(p["path"][0])
                # Mark as 'done' for this cycle
                p["pos"][1] = 99 

    return particles

# 4. RENDERER
def main():
    particles = run_simulation()
    
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    for i in range(17): ax.axhline(i, color="#F0F0F0", lw=0.5); ax.axvline(i, color="#F0F0F0", lw=0.5)

    for p in particles:
        path = np.array(p["path"])
        blood = p["params"]["blood"]
        gender = p["params"]["gender"]
        
        bc = np.array(plt.cm.colors.to_rgba({"O":"#D32F2F","A":"#1976D2","B":"#388E3C","AB":"#7B1FA2"}[blood]))[:3]
        color = 0.8 * bc + 0.2 * (np.array([1,0.5,0]) if gender=="F" else np.array([0,0.5,1]))
        ax.plot(path[:, 0], path[:, 1], color=color, alpha=0.5, lw=0.8)

    ax.set_title("128-TYPE FORMAL NEURO-PHYSICS | Potential-Based Divergence", fontsize=26, pad=50)
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_FORMAL_NEURO_PHYSICS.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Success: {output} rendered.")

if __name__ == "__main__":
    main()
