# -*- coding: utf-8 -*-
"""
generate_128_grid_v10_universal.py
==================================
THE COMPLETE UNIVERSAL GEOMETRY ENGINE.
No simplifications. No hardcoding. Only pure integrated laws.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Particle:
    id: int
    bits: list
    pos: np.ndarray
    vel: np.ndarray
    mass: float
    charge: float
    dimension: int # 1D or 3D
    hysteresis_lag: float

def run_universal_engine(steps=1440):
    # --- UNIVERSAL CONSTANTS ---
    W11, W7, W5, W1 = 11.0, 7.0, 5.0, 1.0
    DELTA = 0.00035
    REFR_ANGLE = np.radians(138.88)
    LAG_BASE = 0.1569
    dt = 0.1
    
    particles = []
    for i in range(128):
        bits = [(i >> j) & 1 for j in range(7)]
        # Bit 0: M/F | 1-2: Blood | 3: E/I | 4: S/N | 5: T/F | 6: J/P
        
        # 128-Type Physical Derivation
        mass = [1.0, 1.5, 1.2, 0.8][(i >> 1) & 3]
        charge = W11 if bits[0] == 0 else W7
        dim = 3 if bits[4] == 1 else 1
        lag = LAG_BASE * (1.0 + bits[6]*0.1) # J/P affects lag
        
        x_start = 2.0 + (i // 16) * 4.0 + (i % 16) * 0.1
        pos = np.array([x_start, 18.0, 10.0])
        vel = np.array([0.0, -0.1, 0.0])
        
        particles.append(Particle(i, bits, pos, vel, mass, charge, dim, lag))

    paths = [[] for _ in range(128)]

    for t in range(steps):
        is_night = t > 720
        u_time = t * 0.01
        
        for i, p in enumerate(particles):
            # Law 1: 11/7 Dipole Field
            # Right side (Men) pushes, Left side (Women) pulls
            dipole_fx = (16.0 - p.pos[0]) * (p.charge / 16.0) * 0.01
            
            # Law 2: PLP Spine Refraction (X+Y=16)
            # 수면을 치는 UV Ray의 굴절
            if (p.pos[0] + p.pos[1]) > 16.0:
                rot = np.array([
                    [np.cos(REFR_ANGLE), -np.sin(REFR_ANGLE), 0],
                    [np.sin(REFR_ANGLE),  np.cos(REFR_ANGLE), 0],
                    [0, 0, 1]
                ])
                p.vel = rot @ p.vel * 1.01 # Energy gain from Spark
            
            # Law 3: UV Lag (Hysteresis)
            # The actual force is delayed by the hysteresis lag
            effective_time = u_time - (p.hysteresis_lag * DELTA)
            wave_force = np.sin(effective_time + p.pos[0] * 0.1) * 0.05
            
            # Law 4: Day/Night Shifting (Metabolic Need)
            metabolic_force = np.zeros(3)
            if not is_night:
                # DAY: Starburst Expansion
                metabolic_force[0] = (1.0 if p.bits[3]==1 else -1.0) * 0.2
            else:
                # NIGHT: Dream-Folding
                if p.bits[0] == 1: # WOMAN: Linear Static
                    p.vel[0:2] *= 0.95 # Horizontal freeze
                    metabolic_force[2] = -0.3 # Deep gravity sink
                else: # MAN: Column Hopping
                    metabolic_force[0] = np.sin(t * 0.2) * 3.0 # Jumps columns
                    metabolic_force[2] = 0.1 # Resurrection lift

            # Law 5: Harshness (T/F Collision Response)
            # T types resist the field, F types flow with it
            viscosity = 0.1 if p.bits[5] == 1 else 0.01
            friction = -p.vel * viscosity
            
            # Law 6: The 4 Pillars Gravity
            gravity = np.array([0, 0, -W5 * 0.02])
            
            # Law 7: Space Creation Neutralizes Viscosity
            volume = np.linalg.norm(p.vel) * 0.1
            friction *= np.exp(-volume) # Creation > GABA
            
            # Total Integration
            total_force = dipole_fx + wave_force + metabolic_force + gravity + friction + DELTA
            accel = total_force / p.mass
            
            p.vel += accel * dt
            p.pos += p.vel * dt
            
            # Law 8: 4D Wormhole Return
            if p.pos[2] < 0: # Hit the Betti 5 Sink
                p.pos[2] = 15.0 # Teleport back to North Pole
                p.pos[0:2] = np.array([16.0, 16.0]) # Reset to Center
            
            paths[i].append(p.pos.copy())

    return [np.array(path) for path in paths]

def render_universal_map(paths):
    fig = plt.figure(figsize=(20, 20), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    for i, path in enumerate(paths):
        bits = [(i >> j) & 1 for j in range(7)]
        # Color by Gender and Extraversion
        color = 'cyan' if bits[0] == 0 else 'magenta'
        alpha = 0.7 if bits[3] == 1 else 0.3
        lw = 1.2 if bits[4] == 1 else 0.6 # N types have thicker lines
        
        ax.plot(path[:,0], path[:,1], path[:,2], color=color, alpha=alpha, linewidth=lw)

    ax.set_title("UNIVERSAL GEOMETRY: THE COMPLETE 128-GRID INTEGRATION", color='white', fontsize=20)
    ax.axis('off')
    plt.savefig("v10_universal_128_grid.png", dpi=300, facecolor='black', bbox_inches='tight')
    print("V10 Universal Engine Rendered: v10_universal_128_grid.png")

if __name__ == "__main__":
    trajs = run_universal_engine()
    render_universal_map(trajs)
