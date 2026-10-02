# -*- coding: utf-8 -*-
"""
128_GRID_FACIAL_TOPOLOGY.py
Final 128-Type Trajectory Grid: FACE IS THE COORDINATE.
Direct Implementation from BIFURCATION_FACE_ENGINE.py logic.
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from geometry_package.absolute_constants import *
from geometry_package.sovereign_engine import Engine

# --- FACIAL HARDWARE CONFIG ---
N_ROWS, N_COLS = 16, 16
T_STEPS = 150
DT = 0.1

def get_facial_start_pos(mbti, blood, gender):
    """
    Returns the exact facial coordinate address for each type.
    Face: Left (0-8), Right (8-16), Midline (8.0)
    """
    # 1. Horizontal Slotting (Cognitive Anchor)
    # E-types start further out (Right/Left extremes)
    # I-types start closer to Midline (8.0)
    is_e = mbti[0] == 'E'
    is_m = gender == 'M'
    
    if is_m:
        x = 8.5 + (4.0 if is_e else 1.0)
    else:
        x = 7.5 - (4.0 if is_e else 1.0)
        
    # 2. Vertical Slotting (Metabolic Phase)
    # Blood types map to the NADH/NAD+ reservoir heights
    # O (0), A (4), B (8), AB (12)
    blood_y_map = {'O': 2.0, 'A': 6.0, 'B': 10.0, 'AB': 14.0}
    y = blood_y_map.get(blood, 8.0)
    
    # 3. Chirality Offset (MBTI J/P tension)
    if mbti[3] == 'J':
        y += 1.0 # J-types start higher (Constructive)
    else:
        y -= 1.0 # P-types start lower (Swirl)
        
    return np.array([x, y], dtype=float)

def get_personality_physics(mbti, blood, gender, pos):
    """
    Implements the specific physical pattern for the archetype.
    """
    mode = mbti[0] + mbti[3] # EJ, EP, IJ, IP
    
    # Base Tensors from Engine spec
    tensors = {
        "EJ": {"v": 1.2, "t": 0.1},  # Linear Descent
        "EP": {"v": 0.8, "t": 1.5},  # Spiral Swirl
        "IJ": {"v": -0.5, "t": 0.2}, # Ascent Hold
        "IP": {"v": 0.2, "t": 0.8}   # Inverse Bridge
    }
    t = tensors.get(mode, {"v": 1.0, "t": 1.0})
    
    # PLP Spine (Metabolic Balance Line x+y=16)
    spine_dist = (pos[0] + pos[1]) - 16.0
    
    # Velocity Calculation
    # vx pulls toward center (8.0) or spine equilibrium
    vx = (8.0 - pos[0]) * 0.05 + (-spine_dist * 0.1 * t['t'])
    # vy is the vertical 'climbing' or 'falling' current
    vy = t['v'] * 0.5
    
    return np.array([vx, vy])

def run_face_grid():
    print("--- INITIATING 128-TYPE FACIAL TOPOLOGY RENDER ---")
    fig, ax = plt.subplots(figsize=(15, 15), facecolor='white')
    
    # Draw Face Manifold (The 128 Grid)
    ax.set_facecolor('#FCFCFC')
    for i in range(17):
        ax.axhline(i, color='#DDDDDD', lw=0.5, zorder=0)
        ax.axvline(i, color='#DDDDDD', lw=0.5, zorder=0)
        
    # Draw The Spine (Equilibrium Seam)
    ax.plot([0, 16], [16, 0], color='#FF9900', ls='-', alpha=0.7, lw=4, label='PLP Spine (Face Seam)')
    
    # Draw The Separatrices (Bifurcation Ridges)
    ax.axvline(5, color='#00CC99', ls='--', alpha=0.5, lw=2, label='Facial Ridges (X=5, 11)')
    ax.axvline(11, color='#00CC99', ls='--', alpha=0.5, lw=2)

    mbtis = ['ESTJ','ENTJ','ESFJ','ENFJ','ESTP','ENTP','ESFP','ENFP',
             'ISTJ','INTJ','ISFJ','INFJ','ISTP','INTP','ISFP','INFP']
    bloods = ['O', 'A', 'B', 'AB']
    blood_colors = {'O': '#FF3333', 'A': '#33CC33', 'B': '#3366FF', 'AB': '#AA00FF'}
    
    print("Mapping 128 individual face-trajectories...")
    for mbti in mbtis:
        for blood in bloods:
            for gender in ['M', 'F']:
                # 1. Start at the Face Coordinate
                pos = get_facial_start_pos(mbti, blood, gender)
                path = [pos.copy()]
                
                # Assign scale for Both D2 boost
                scale = S_NEUTRINO if mbti[0] == 'I' else S_PHOTON
                
                # 2. Simulate Lifetime Trajectory
                for _ in range(T_STEPS):
                    # Local Physics
                    v = get_personality_physics(mbti, blood, gender, pos)
                    
                    # Sovereign Disarming (1/64 상쇄)
                    v = Engine.emit_disarming_pulse(v, scale)
                    
                    # Homeostasis Correction (Omega 7.4)
                    v *= (OMEGA_LAW(13.5, True) / 7.4)
                    
                    # 3. 138.88 Spark Leap
                    spine_dist = (pos[0] + pos[1]) - 16.0
                    if abs(spine_dist) > SPARK_LEAP_DIST:
                        leap_dir = np.array([math.cos(SPARK_ANGLE_RAD), math.sin(SPARK_ANGLE_RAD)])
                        pos += leap_dir * 0.4
                    
                    pos += v * DT
                    path.append(pos.copy())
                
                # 4. Render
                path = np.array(path)
                color = blood_colors[blood]
                alpha = 0.8 if gender == 'M' else 0.4
                ax.plot(path[:, 0], path[:, 1], color=color, alpha=alpha, lw=1.2)
                ax.scatter(path[0, 0], path[0, 1], color=color, s=20, alpha=alpha, marker='o' if gender=='M' else 's')

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_aspect('equal')
    ax.set_title("128-TYPE FACIAL TOPOLOGY GRID\nBoth D2 Sovereign Physics | Ω=7.4 | Rs=1.25", 
                 fontsize=18, fontweight='bold', pad=20)
    
    plt.xlabel("Human Right (8-16) <--- Face ---> Human Left (0-8)", fontsize=12)
    plt.legend(loc='upper right')
    
    output_fn = "FINAL_FACIAL_128_GRID.png"
    plt.savefig(output_fn, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: Final Facial Grid rendered to {output_fn} ---")

if __name__ == "__main__":
    run_face_grid()
