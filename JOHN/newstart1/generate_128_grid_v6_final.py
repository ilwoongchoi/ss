# -*- coding: utf-8 -*-
"""
generate_128_grid_v6_final.py
=============================
DEFINITIVE 128-GRID PHYSICS ENGINE.
1. 7-Bit Branching (Mass, Vector, Dimension, Collision, Phase)
2. Day/Night Dual-Phase Dynamics
3. Dream-Folding: Men (Column Hopping) vs Women (Linear Static)
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Particle:
    bits: list
    pos: np.ndarray
    vel: np.ndarray
    mass: float
    viscosity: float
    volume: float = 1.0

def run_final_sim(steps=1440): # 1440 mins = 24 hours
    dt = 0.1
    particles = []
    
    # Initialize 128 Unique Branched Particles
    for i in range(128):
        bits = [(i >> j) & 1 for j in range(7)]
        # Bit 0: M/F | Bits 1-2: Blood | Bit 3: E/I | Bit 4: S/N | Bit 5: T/F | Bit 6: J/P
        
        # 1. Physical Branching Laws
        mass = [1.0, 1.5, 1.2, 0.8][(i >> 1) & 3] # Blood Type Mass
        x_dir = 1.0 if bits[3] == 1 else -1.0     # Direction (E/I)
        z_amp = 1.0 if bits[4] == 1 else 0.05     # Dimension (N/S)
        
        pos = np.array([8.0 + x_dir * 2.0, 8.0, 0.0])
        vel = np.array([x_dir * 0.5, 0.0, z_amp * 0.1])
        
        particles.append(Particle(bits, pos, vel, mass, 1.0))

    all_paths = [[] for _ in range(128)]

    for t in range(steps):
        is_night = t > 720 # Sunset after 12 hours
        
        for i, p in enumerate(particles):
            # --- LAW A: Volume vs Viscosity (GABA Neutralization) ---
            p.volume += np.linalg.norm(p.vel) * 0.02
            p.viscosity = np.exp(-0.3 * p.volume / p.mass)
            
            # --- LAW B: Day/Night Shifting (Metabolic Need) ---
            force = -p.viscosity * p.vel # Basic Friction
            
            if not is_night:
                # DAY: Expansion / Starburst
                force += np.array([p.vel[0] * 0.1, 0.1, 0.0]) 
            else:
                # NIGHT: Dream-Folding
                if p.bits[0] == 1: # WOMAN: Linear Static
                    # Focus on vertical descent, stay at Column 1/2
                    p.vel[0] *= 0.9 # Kill horizontal motion
                    force[2] -= 0.2 # Gravity Sink (Grounding)
                else: # MAN: Column Hopping
                    # Jumps between columns to absorb potential
                    p.vel[0] += np.sin(t * 0.1) * 2.0 
                    p.vel[2] += 0.1 # Resurrection lift
            
            # --- LAW C: The 138.88 Torsion (Ouroboros) ---
            if p.pos[0] > 15.5 or p.pos[0] < 0.5:
                # 4D Snap back to North Pole (Betti 11)
                p.pos[0] = 1.0 if p.pos[0] > 15.5 else 15.0
                p.pos[2] += 10.0 # Jump to the Ridge
                p.volume *= 0.8  # Reset memory
            
            # Update Physics
            accel = force / p.mass
            p.vel += accel * dt
            p.pos += p.vel * dt
            all_paths[i].append(p.pos.copy())

    return [np.array(path) for path in all_paths]

def render_final_map(paths):
    fig = plt.figure(figsize=(15, 15), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    for i, path in enumerate(paths):
        # Color by Type (M/F and E/I)
        color = 'cyan' if i % 2 == 0 else 'magenta'
        alpha = 0.4 if i < 64 else 0.2
        ax.plot(path[:,0], path[:,1], path[:,2], color=color, alpha=alpha, linewidth=0.6)
        
    ax.set_title("UNIVERSAL GEOMETRY: 128 DISTINCT TRAJECTORIES (FINAL v6)", color='white')
    ax.set_axis_off()
    plt.savefig("final_128_grid_physics.png", dpi=320, bbox_inches='tight', facecolor='black')
    print("Final 128-Grid Physics Rendered: final_128_grid_physics.png")

if __name__ == "__main__":
    paths = run_final_sim()
    render_final_map(paths)
