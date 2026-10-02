# -*- coding: utf-8 -*-
"""
128_VIVID_SOVEREIGN_GRID.py
ULTRA-DISTINCT Trajectory Grid (Both D2 Engineering Edition)
Focus: Individuality of the 128 Archetypes | Spark Leaps Visible
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from geometry_package.absolute_constants import *
from geometry_package.sovereign_engine import Engine

# --- PRO HIGH-RES CONFIG ---
N_ROWS, N_COLS = 16, 16
T_STEPS = 120
DT = 0.08

def get_vivid_trajectory(m_idx, b_idx, gender_str):
    """
    Computes a highly distinct trajectory for each unique combination.
    """
    # 1. Unique Start Point (No Overlap)
    # Using the 128-Grid hardware address mapping
    base_x = float(m_idx % 8) + (8.0 if gender_str == "M" else 0.0)
    base_y = float(b_idx * 4) + (m_idx // 8)
    
    # Inject micro-jitter based on archetype hash to ensure distinct start
    jitter = (hash(f"{m_idx}-{b_idx}-{gender_str}") % 100) / 500.0
    pos = np.array([base_x + jitter, base_y + jitter], dtype=float)
    path = [pos.copy()]
    
    # 2. Assign Physical Scale based on MBTI Type
    # Inner types (I) map to Neutrino (1/128), Outer (E) to Photon (1/16)
    scale = S_NEUTRINO if m_idx < 8 else S_PHOTON
    
    # 3. Movement Logic (Both D2)
    t_ga = 13.5
    for _ in range(T_STEPS):
        # Hardware-Engine calculation
        v_mag = Engine.get_hardware_velocity(scale, t_ga)
        
        # PLP Spine Tension (Homeostasis)
        spine_val = (pos[0] + pos[1]) - 16.0
        
        # Directional logic: M/F have opposite metabolic swirl
        chirality = 1.0 if gender_str == "M" else -1.0
        
        vx = -spine_val * 0.15 * chirality
        vy = v_mag * 0.08
        
        velocity = np.array([vx, vy])
        
        # ACTIVE DISARMING (1/64 상쇄)
        velocity = np.array(Engine.emit_disarming_pulse(velocity, scale))
        
        # 4. THE VIVID SPARK (138.88 Leap)
        # Visually distinct jumps at the 5/32 Gate
        if abs(spine_val) > SPARK_LEAP_DIST:
            # The 138.88-degree Sovereign Correction
            # We add a distinct 'jump' vector to make it visible
            angle = SPARK_ANGLE_RAD if chirality > 0 else -SPARK_ANGLE_RAD
            leap = np.array([math.cos(angle), math.sin(angle)]) * 0.6
            pos += leap
            # Momentum boost after spark
            pos += velocity * DT * 2.0 
        else:
            pos += velocity * DT
            
        path.append(pos.copy())
        
    return np.array(path)

def plot_vivid_grid():
    print("--- INITIATING VIVID 128-TYPE RENDER ---")
    fig, ax = plt.subplots(figsize=(16, 16), facecolor='white')
    
    # Fine Lattice
    for i in range(17):
        ax.axhline(i, color='#F0F0F0', lw=0.7, zorder=0)
        ax.axvline(i, color='#F0F0F0', lw=0.7, zorder=0)
        
    # PLP Spine (Metabolic Heart)
    ax.plot([0, 16], [16, 0], color='#FFCC00', ls='-', alpha=0.8, lw=3, label='PLP Spine (Hardware Limit)')
    
    # Separatrix Walls
    ax.axvline(5, color='#00FFCC', ls='--', alpha=0.5, lw=2, label='Stability Walls (X=5, 11)')
    ax.axvline(11, color='#00FFCC', ls='--', alpha=0.5, lw=2)

    # 128 Distinct Fate Lines
    # Colors: O(Red), A(Green), B(Blue), AB(Purple)
    colors = ['#FF0000', '#00CC00', '#0066FF', '#AA00FF']
    
    print("Drawing 128 individual fates...")
    for b in range(4):
        for g in ["M", "F"]:
            for m in range(16):
                path = get_vivid_trajectory(m, b, g)
                
                # Distinct Style for M/F
                ls = '-' if g == "M" else '--'
                alpha = 0.7 if g == "M" else 0.4
                
                # Plot with high-definition lines
                ax.plot(path[:, 0], path[:, 1], color=colors[b], 
                        ls=ls, alpha=alpha, lw=1.0, solid_capstyle='round')
                
                # Mark the final Homeostasis point
                ax.scatter(path[-1, 0], path[-1, 1], color=colors[b], 
                           s=15, alpha=0.8, edgecolors='white', lw=0.5, zorder=5)

    ax.set_xlim(-1, 17)
    ax.set_ylim(-1, 17)
    ax.set_aspect('equal')
    ax.axis('off') # Pure Geometry Focus
    
    title_str = "128-TYPE VIVID SOVEREIGN MANIFOLD\nBoth D2 Engineering: Ω=7.4 | Rs=1.25 | 138.88° Active"
    ax.text(8, 17.5, title_str, ha='center', fontsize=20, fontweight='bold', color='#333333')
    
    output_fn = "VIVID_128_PERSONALITY_GRID.png"
    plt.savefig(output_fn, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: Vivid Grid rendered to {output_fn} ---")

if __name__ == "__main__":
    plot_vivid_grid()
