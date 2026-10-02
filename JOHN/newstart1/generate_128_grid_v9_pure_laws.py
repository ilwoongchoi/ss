# -*- coding: utf-8 -*-
"""
generate_128_grid_v9_pure_laws.py
=================================
UNIVERSAL GEOMETRY: PURE PHYSICAL LAWS ONLY.
1. Pillars: 11 (Source), 7 (Void), 5 (Debt), 1/64 (Action)
2. Tension: Delta = 0.00035
3. Refraction: PLP Boundary (X+Y=16) @ 138.88 deg
4. Lag: UV Ray vs Water Surface (Hysteresis 0.1569)
"""

import numpy as np
import matplotlib.pyplot as plt

def run_pure_laws():
    # --- PHYSICAL CONSTANTS ---
    W11, W7, W5 = 11.0, 7.0, 5.0
    ACTION_STEP = 1.0/64.0
    DELTA_TENSION = 0.00035
    PLP_REFRACTION = np.radians(138.88)
    UV_LAG = 0.1569
    
    fig = plt.figure(figsize=(16, 16), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')

    for i in range(128):
        # 7-Bit Vector Initialization (No Labels)
        bits = [(i >> j) & 1 for j in range(7)]
        
        # Initial Physics State
        pos = np.array([float(bits[1]*8 + bits[2]*4), float(bits[3]*8 + bits[4]*4), 10.0])
        vel = np.array([0.0, 0.0, -0.1])
        charge = W11 if bits[0] == 0 else W7
        
        path = []
        for t in range(500):
            # 1. UV Lagging (Hysteresis)
            photon_pos = t * ACTION_STEP
            actual_pos = photon_pos - (UV_LAG * DELTA_TENSION)
            
            # 2. PLP Optical Boundary (X+Y=16)
            # 수면을 치는 순간 굴절 발생
            if (pos[0] + pos[1]) > 16.0:
                rot = np.array([
                    [np.cos(PLP_REFRACTION), -np.sin(PLP_REFRACTION), 0],
                    [np.sin(PLP_REFRACTION),  np.cos(PLP_REFRACTION), 0],
                    [0, 0, 1]
                ])
                vel = rot @ vel * (charge / W11)
            
            # 3. Pillar Forces
            gravity = -W5 * 0.01
            void_pull = (W7 / np.linalg.norm(pos)) * 0.05
            
            vel[2] += gravity + DELTA_TENSION
            pos += vel + void_pull
            
            path.append(pos.copy())
            if pos[2] < 0: break # Hit the Betti 0 Ground

        path = np.array(path)
        color = plt.cm.magma(i/128.0)
        ax.plot(path[:,0], path[:,1], path[:,2], color=color, alpha=0.6, linewidth=0.8)

    ax.axis('off')
    plt.savefig("v9_pure_laws_128_grid.png", dpi=300, facecolor='black')
    print("V9 Pure Laws Rendered: v9_pure_laws_128_grid.png")

if __name__ == "__main__":
    run_pure_laws()
