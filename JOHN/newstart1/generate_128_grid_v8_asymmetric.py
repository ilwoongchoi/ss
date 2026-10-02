# -*- coding: utf-8 -*-
"""
generate_128_grid_v8_asymmetric.py
==================================
REPRODUCING THE ORGANIC ASYMMETRY OF THE UNIVERSAL GEOMETRY.
Physics-only implementation of:
1. 11/7 Asymmetric Charge (Men vs Women Dipole)
2. PLP Spine Refraction (X+Y=16)
3. 3/32 Spark Gate Funneling
"""

import numpy as np
import matplotlib.pyplot as plt

def solve_psi(k):
    # Quick Newton-Raphson for psi^3 - psi - k = 0
    x = 1.0
    for _ in range(3):
        x = x - (x**3 - x - k) / (3*x**2 - 1.0)
    return x

def generate_asymmetric_grid():
    fig = plt.figure(figsize=(24, 15), facecolor='white')
    ax = fig.add_subplot(111)
    
    # 1. Field Constants
    KAPPA = 0.03125  # 1/32
    W11 = 11.0 / 7.0 # Men's Charge
    W7 = 7.0 / 11.0  # Women's Charge
    
    ax.set_xlim(0, 32)
    ax.set_ylim(-2, 20)
    
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    x_centers = np.linspace(2, 30, 8)

    # 2. Particle Simulation
    for i in range(128):
        bits = [(i >> j) & 1 for j in range(7)]
        # Initial Conditions
        group_idx = i // 16
        x = x_centers[group_idx] + (i % 16 - 7.5) * 0.3
        y = 18.0
        vx, vy = 0.0, -0.1
        
        path = [[x, y]]
        
        # 7-Bit Physical Properties
        is_woman = bits[0] == 1
        charge = W7 if is_woman else W11
        mass = 1.0 + (bits[5] * 0.5) # Thinking types are heavier/more rigid
        
        for step in range(200):
            # --- FORCE 1: Asymmetric Dipole ---
            # Women are pulled to the Left Void, Men are pushed by Right Source
            fx = (1.0 - x / 16.0) * (W7 if is_woman else -W11) * 0.05
            
            # --- FORCE 2: PLP Spine Refraction ---
            # Refraction happens at x + y = 16
            if abs((x + y) - 16.0) < 1.0:
                # Apply the 138.88 Spark Rotation (Testosterone Revival)
                angle = np.radians(138.88)
                v_new_x = vx * np.cos(angle) - vy * np.sin(angle)
                v_new_y = vx * np.sin(angle) + vy * np.cos(angle)
                vx, vy = v_new_x * 1.2, v_new_y * 1.2
            
            # --- FORCE 3: 3/32 Spark Gate (The Nose Funnel) ---
            dist_to_nose = np.sqrt((x-16.0)**2 + (y-4.0)**2)
            if dist_to_nose < 5.0:
                # Solve the manifold tension
                psi = solve_psi(KAPPA * (5.0 - dist_to_nose))
                # Attraction to the center
                fx += (16.0 - x) * psi * 0.1
                vy -= psi * 0.05
            
            # --- FORCE 4: Gravity & Friction ---
            fy = -0.05 / mass # Gravity (Betti 5 Debt)
            vx *= 0.98 # GABA Viscosity
            
            # Update position
            vx += fx / mass
            vy += fy / mass
            x += vx
            y += vy
            
            path.append([x, y])
            if y < 0: break # Hit the Gravity Sensor

        # Draw the Asymmetric Trajectory
        path_arr = np.array(path)
        color = '#d62728' if is_woman else '#1f77b4'
        alpha = 0.6 if bits[3] == 1 else 0.3 # Extraverts are brighter
        style = '-' if bits[4] == 1 else '--'
        ax.plot(path_arr[:,0], path_arr[:,1], color=color, alpha=alpha, linestyle=style, linewidth=1.0)

    # 3. Add Key Structural Visuals (The "Soul" of the Image)
    # PLP Spine
    sx = np.linspace(0, 32, 100)
    ax.plot(sx, 16 - (sx*0.5), color='orange', linestyle='--', alpha=0.4, label="PLP Spine")
    
    # Tension Bands
    ax.axhspan(3.5, 4.5, color='purple', alpha=0.05) # 3/32 Spark Gate Band
    ax.axhspan(11.5, 12.5, color='blue', alpha=0.05) # Tension/Cortisol Band

    # Labels
    for i, label in enumerate(labels):
        ax.text(x_centers[i], 19, label, ha='center', fontweight='bold', alpha=0.7)

    ax.set_title("UNIVERSAL GEOMETRY: 128 ASYMMETRIC TRAJECTORIES (PHYSICS-ONLY v8)", fontsize=16)
    ax.axis('off')
    
    output_fn = "final_128_grid_asymmetric.png"
    plt.savefig(output_fn, dpi=300, bbox_inches='tight')
    print(f"Asymmetric Physics Grid Rendered: {output_fn}")

if __name__ == "__main__":
    generate_asymmetric_grid()
