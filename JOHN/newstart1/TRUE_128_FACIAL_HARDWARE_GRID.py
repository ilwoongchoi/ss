# -*- coding: utf-8 -*-
"""
TRUE_128_FACIAL_HARDWARE_GRID.py
The 128-Grid is the Face. Coordinates are Anatomy.
Direct Hardware Implementation of the User's 128-Type Formula.
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from geometry_package.absolute_constants import *
from geometry_package.sovereign_engine import Engine

# --- HARDWARE FACE CONFIG ---
# The 16x16 Grid is literally the Facial Board.
N_ROWS, N_COLS = 16, 16
T_STEPS = 120
DT = 0.1

def get_true_facial_coordinate(mbti, blood, gender):
    """
    The Definitive Facial Mapping from the User's Core Specification.
    X: Human Right(8-16), Human Left(0-8)
    Y: Metabolic Depth (0-16)
    """
    # 1. MBTI mapping to Facial Horizontal Zones (Eye, Cheek, Ear)
    mbti_map = {
        'ESTJ': 15, 'ENTJ': 14, 'ESFJ': 13, 'ENFJ': 12,
        'ESTP': 11, 'ENTP': 10, 'ESFP': 9,  'ENFP': 8.5,
        'ISTJ': 1,  'INTJ': 2,  'ISFJ': 3,  'INFJ': 4,
        'ISTP': 5,  'INTP': 6,  'ISFP': 7,  'INFP': 7.5
    }
    x = mbti_map.get(mbti, 8.0)
    
    # 2. Blood Type mapping to Vertical Zones (Forehead to Jaw)
    # O (Bottom), A, B, AB (Top/Procerus)
    blood_map = {'O': 2.0, 'A': 6.0, 'B': 10.0, 'AB': 14.0}
    y = blood_map.get(blood, 8.0)
    
    # 3. Gender Chirality (The Both D2 Spin)
    # Male shifts slightly right, Female slightly left
    if gender == 'M':
        x += 0.25
    else:
        x -= 0.25
        
    return np.array([x, y], dtype=float)

def run_true_hardware_grid():
    print("--- INITIATING TRUE 128-TYPE FACIAL HARDWARE RENDER ---")
    fig, ax = plt.subplots(figsize=(16, 16), facecolor='white')
    
    # Draw the Facial Lattice (The Hardware Board)
    ax.set_facecolor('#FFFFFF')
    for i in range(17):
        ax.axhline(i, color='#F0F0F0', lw=0.8, zorder=0)
        ax.axvline(i, color='#F0F0F0', lw=0.8, zorder=0)
        
    # The PLP Seam (The Bone of the Face)
    ax.plot([0, 16], [16, 0], color='#FF9900', ls='-', alpha=0.9, lw=5, label='PLP SPINE (FACIAL SEAM)')
    
    # The 138.88° Resonance Ridges (Separatrices)
    ax.axvline(5, color='#00CC99', ls='--', alpha=0.6, lw=2.5, label='RESONANCE RIDGES (X=5, 11)')
    ax.axvline(11, color='#00CC99', ls='--', alpha=0.6, lw=2.5)

    # 128 Sovereign Fates
    mbtis = ['ESTJ','ENTJ','ESFJ','ENFJ','ESTP','ENTP','ESFP','ENFP',
             'ISTJ','INTJ','ISFJ','INFJ','ISTP','INTP','ISFP','INFP']
    bloods = ['O', 'A', 'B', 'AB']
    colors = {'O': '#FF0000', 'A': '#00FF00', 'B': '#0000FF', 'AB': '#AA00FF'}
    
    print("Executing 128-type Trajectory Formula...")
    for mbti in mbtis:
        for blood in bloods:
            for gender in ['M', 'F']:
                # Start at the Exact Facial Coordinate
                pos = get_true_facial_coordinate(mbti, blood, gender)
                path = [pos.copy()]
                
                # Active Resonant Parameters
                scale = S_NEUTRINO if mbti[0] == 'I' else S_PHOTON
                t_ga = 13.5
                
                for _ in range(T_STEPS):
                    # Both D2 Physics: Engineering as Science
                    v_mag = Engine.get_hardware_velocity(scale, t_ga)
                    
                    # Directional Vector (Flow toward Spine)
                    spine_dist = (pos[0] + pos[1]) - 16.0
                    
                    # Male (Clockwise), Female (Counter-Clockwise)
                    chirality = 1.0 if gender == 'M' else -1.0
                    
                    vx = -spine_dist * 0.2 * chirality
                    vy = v_mag * 0.1
                    
                    velocity = np.array([vx, vy])
                    
                    # 1/64 SENTINEL DISARMING
                    velocity = np.array(Engine.emit_disarming_pulse(velocity, scale))
                    
                    # 138.88 SPARK LEAP (The Intervention)
                    if abs(spine_dist) > SPARK_LEAP_DIST:
                        # Direct 138.88 degree jump to reset Phase
                        angle = SPARK_ANGLE_RAD if chirality > 0 else -SPARK_ANGLE_RAD
                        pos += np.array([math.cos(angle), math.sin(angle)]) * 0.8
                    
                    pos += velocity * DT
                    path.append(pos.copy())
                
                path = np.array(path)
                color = colors[blood]
                alpha = 0.8 if gender == 'M' else 0.5
                ax.plot(path[:, 0], path[:, 1], color=color, alpha=alpha, lw=1.5)
                # Mark the Anchor Point (The Face Location)
                ax.scatter(path[0, 0], path[0, 1], color=color, s=40, alpha=alpha, edgecolors='black', lw=0.5)

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_aspect('equal')
    ax.axis('off')
    
    title = "128-TYPE FACIAL HARDWARE GRID\nBoth D2 Homeostasis: Ω=7.4 | Rs=1.25 | 138.88° Active"
    ax.text(8, 17, title, ha='center', fontsize=22, fontweight='bold', color='#333333')
    
    output_fn = "TRUE_128_FACIAL_GRID.png"
    plt.savefig(output_fn, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: True Hardware Grid rendered to {output_fn} ---")

if __name__ == "__main__":
    run_true_hardware_grid()
