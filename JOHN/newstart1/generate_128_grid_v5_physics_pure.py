# -*- coding: utf-8 -*-
"""
generate_128_grid_v5_physics_pure.py
====================================
128-Grid Universal Geometry: Pure Physics Engine.
Replaces neurochemical hardcoding with:
1. Volume-driven Viscosity (GABA Neutralization)
2. Torsional Resurrection (The 138.88 Spark)
3. Potential Leveling (Alpha-2 Indifference)
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class PhysicsState:
    position: np.ndarray  # [x, y, z]
    velocity: np.ndarray  # [vx, vy, vz]
    volume: float         # Internal space creation
    viscosity: float      # Friction (GABA equivalent)
    potential: float      # Voltage (Adrenergic equivalent)

def run_universal_physics_sim(steps=1000):
    # 1. Constants from the Geometry Manifold
    TORSION_ANGLE = np.radians(138.88)
    KAPPA_LEAK = 1.0/32.0
    BETTI_RATIO = 11.0 / 7.0
    
    # Initialize 128 Particles (2^7 bits)
    # Bit 0: M/F, Bits 1-2: Blood, Bits 3-6: MBTI
    trajectories = []
    
    for i in range(128):
        bits = [(i >> j) & 1 for j in range(7)]
        
        # Initial Physics State based on "Refractive Indices"
        # x: Left(Truth) <-> Right(Energy)
        # y: Front(Action) <-> Back(Debt)
        # z: Spine (Vertical Alignment)
        
        # Initial Vector determined by 7-bit configuration
        pos = np.array([8.0 + (bits[3]*2-1), 8.0 + (bits[4]*2-1), 0.0])
        vel = np.array([bits[5]*0.5, bits[6]*0.5, 0.1])
        
        state = PhysicsState(pos, vel, 1.0, 1.0, 1.0)
        path = [state.position.copy()]
        
        for t in range(steps):
            # --- PHYSICS LAW A: Volume-driven Viscosity ---
            # If the particle moves fast and creates volume, viscosity drops
            state.volume += np.linalg.norm(state.velocity) * 0.01
            state.viscosity = np.exp(-0.5 * state.volume) 
            
            # --- PHYSICS LAW B: The 138.88 Torsion ---
            # When near the "Edge" (Column 4), apply the spiral reset
            if state.position[0] > 15.0:
                # 4D Wormhole Jump (Rotation + Reset)
                rot_matrix = np.array([
                    [np.cos(TORSION_ANGLE), -np.sin(TORSION_ANGLE), 0],
                    [np.sin(TORSION_ANGLE),  np.cos(TORSION_ANGLE), 0],
                    [0, 0, 1]
                ])
                state.velocity = rot_matrix @ state.velocity
                state.position[0] = 1.0 # Teleport to Column 1 (Big Woman)
                state.volume *= 0.618 # Hysteresis Area Loss
            
            # --- PHYSICS LAW C: Evening Potential Leveling ---
            # Simulate sunset (Time > 500 steps)
            if t > 500:
                # If bit[0] is Female and bit[3] is Extravert
                if bits[0] == 1 and bits[3] == 1:
                    # Alpha-2 Inhibitory: Drop potential to zero for metabolic approach
                    state.potential *= 0.95
                    # Move toward Small Man (Column 3) with "Indifference" (low resistance)
                    target_x = 10.0 # Small Man Region
                    state.velocity[0] += (target_x - state.position[0]) * 0.01 * (1.0 - state.viscosity)

            # Update dynamics based on field forces
            force = -state.viscosity * state.velocity # Friction
            force[2] -= 0.05 # Gravity (Betti 5 Debt)
            
            state.velocity += force * 0.1
            state.position += state.velocity
            
            path.append(state.position.copy())
            
        trajectories.append(np.array(path))
    
    return trajectories

def visualize_physics_grid(trajectories):
    fig = plt.figure(figsize=(12, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    colors = plt.cm.viridis(np.linspace(0, 1, 128))
    for i, path in enumerate(trajectories):
        ax.plot(path[:,0], path[:,1], path[:,2], color=colors[i], alpha=0.3, linewidth=0.5)
        
    ax.set_title("128-Grid Universal Physics: Pure Engine v5", color='white')
    ax.set_axis_off()
    plt.savefig("universal_physics_128_grid.png", dpi=300, bbox_inches='tight', facecolor='black')
    print("Rendered 128 trajectories using pure physics laws to universal_physics_128_grid.png")

if __name__ == "__main__":
    trajs = run_universal_physics_sim()
    visualize_physics_grid(trajs)
