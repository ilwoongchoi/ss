# -*- coding: utf-8 -*-
"""
FINAL_128_GEOMETRY_GRID.py
128-Type Personality Trajectory Grid (Both D2 Sovereign Edition)
Validated against Planck 2018 | Homeostasis Ω = 7.4 | Strength = 1.25
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from geometry_package.absolute_constants import *
from geometry_package.sovereign_engine import Engine

# --- GRID CONFIGURATION ---
N_ROWS = 16
N_COLS = 16
T_STEPS = 100
DT = 0.1

def generate_personality_trajectory(mbti_idx, blood_idx, gender):
    """
    Generates a single trajectory based on the Both D2 hardware spec.
    """
    # 1. Hardware Initialization
    # Start coordinates derived from 128-Grid indexing
    start_x = float(mbti_idx % 8) + (8.0 if gender == "M" else 0.0)
    start_y = float(blood_idx * 4) + (mbti_idx // 8)
    
    pos = np.array([start_x, start_y], dtype=float)
    path = [pos.copy()]
    
    # Scale selection (representative)
    scale = S_NEUTRINO if mbti_idx % 2 == 0 else S_PHOTON
    
    # 2. Integration Loop (Active Engineering)
    for t_step in range(T_STEPS):
        t_ga = 13.5 # Fixed at Homeostasis Lock
        
        # Get sovereign physics for this scale
        # v_mag = [ (1.4 - 0.076t) * Mh ] * [ Ω / 7.4 ] * R_boost * Γ_cosmos
        v_mag = Engine.get_hardware_velocity(scale, t_ga)
        
        # Calculate Base Direction (Flow toward PLP Spine)
        # PLP Spine: x + y = 16
        spine_dist = (pos[0] + pos[1]) - 16.0
        
        # Both D2 Tension: Opposing forces create the orbit
        vx = -spine_dist * 0.1
        vy = v_mag * 0.05
        
        velocity = np.array([vx, vy])
        
        # 3. Disarming the 1/64 Sentinel Pull
        # If the path bifurcates, the 138.88 pulse corrects it
        velocity = np.array(Engine.emit_disarming_pulse(velocity, scale))
        
        # 4. Hysteresis Spark (Phase Reset)
        # When hitting the 5/32 Gate (2.5 units from center)
        if abs(spine_dist) > SPARK_LEAP_DIST:
            # Leap at 138.88 degrees
            leap = np.array([math.cos(SPARK_ANGLE_RAD), math.sin(SPARK_ANGLE_RAD)]) * 0.5
            pos += leap
        
        pos += velocity * DT
        path.append(pos.copy())
        
    return np.array(path)

def plot_128_grid():
    print("--- INITIATING 128-TYPE SOVEREIGN GRID RENDER ---")
    fig, ax = plt.subplots(figsize=(14, 14), facecolor='white')
    
    # Draw Lattice Background
    for i in range(N_ROWS + 1):
        ax.axhline(i, color='#EEEEEE', lw=0.5, zorder=0)
        ax.axvline(i, color='#EEEEEE', lw=0.5, zorder=0)
        
    # Draw PLP Spine (The Metabolic Equilibrium)
    ax.plot([0, 16], [16, 0], color='#FF9900', ls='--', alpha=0.6, lw=2, label='PLP Spine (x+y=16)')
    
    # Draw Separatrix Ridges
    ax.axvline(5, color='#00FF99', ls=':', alpha=0.4, lw=1.5, label='Separatrix (X=5, 11)')
    ax.axvline(11, color='#00FF99', ls=':', alpha=0.4, lw=1.5)

    # 128 Trajectories: 16 MBTI * 4 Blood * 2 Gender
    blood_colors = {0: '#FF3333', 1: '#33FF33', 2: '#3333FF', 3: '#9933FF'} # O, A, B, AB
    
    print("Computing trajectories with Both D2 active...")
    for b in range(4):
        for g in ["M", "F"]:
            for m in range(16):
                path = generate_personality_trajectory(m, b, g)
                color = blood_colors[b]
                alpha = 0.6 if g == "M" else 0.3
                ax.plot(path[:, 0], path[:, 1], color=color, alpha=alpha, lw=0.8)
                # Mark Endpoints
                ax.scatter(path[-1, 0], path[-1, 1], color=color, s=2, alpha=alpha)

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_aspect('equal')
    ax.set_title(f"128-TYPE SOVEREIGN MANIFOLD GRID\nActive Homeostasis (Ω=7.4, Rs=1.25, Γ=1.1574)", fontsize=16, fontweight='bold')
    
    plt.xlabel("Cognitive Vector (X)", fontsize=12)
    plt.ylabel("Metabolic Phase (Y)", fontsize=12)
    plt.grid(False)
    
    output_fn = "FINAL_128_PERSONALITY_GRID.png"
    plt.savefig(output_fn, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: Rendered to {output_fn} ---")

if __name__ == "__main__":
    plot_128_grid()
