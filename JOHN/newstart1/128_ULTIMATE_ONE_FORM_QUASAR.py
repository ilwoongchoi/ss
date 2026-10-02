# -*- coding: utf-8 -*-
"""
128_ULTIMATE_ONE_FORM_QUASAR.py
The Sovereign Engineering Resolution.
Instead of 128 scattered fates, the 138.88° Resonance forces all 128 bifurcated types 
to converge into the SINGLE, unified Final Route (The Homeostasis Operator).
"""

import matplotlib.pyplot as plt
import numpy as np
import math

# --- THE ENGINEERING FINAL ROUTE EQUATION ---
# From UNIFIED_GEOMETRY_EQUATION.md Section 5.2
def get_unified_final_route(t_array):
    """
    The Single Consistent Solution that all 128 types converge into 
    when the Active Engineering (Both D2 / 138.88 Resonance) is applied.
    """
    # x(t) = 2 + 12 * sin^2(pi * (t-10.5)/10.5) * (1 - e^(-t/2))
    # y(t) = 6 + 6 * sin(pi * (t-10.5)/10.5) * cos(pi * (t-10.5)/10.5)
    
    # Avoid division by zero at t=0 for exp part if necessary, but t/2 is fine.
    pi_term = np.pi * (t_array - 10.5) / 10.5
    
    x = 2.0 + 12.0 * (np.sin(pi_term)**2) * (1.0 - np.exp(-t_array / 2.0))
    y = 6.0 + 6.0 * np.sin(pi_term) * np.cos(pi_term)
    
    return x, y

def plot_one_form_quasar():
    print("--- INITIATING THE ONE FORM SOVEREIGN RENDER ---")
    fig, ax = plt.subplots(figsize=(16, 16), facecolor='#050508')
    ax.set_facecolor('#050508')
    
    # 1. Background: The 128 Ghost Points (The Natural, Broken State)
    # This represents where they *would* have scattered without engineering.
    np.random.seed(13888) # The Resonance Seed
    raw_x = np.random.uniform(1, 15, 128)
    raw_y = np.random.uniform(1, 15, 128)
    ax.scatter(raw_x, raw_y, color='#444455', s=10, alpha=0.3, label='128 Bifurcated Origins (Natural Crunch State)')
    
    # 2. The Pull of the Engineering (Convergence lines)
    # Showing all 128 points being structurally pulled into the start of the Final Route
    target_start_x, target_start_y = 2.0, 6.0 # LEFT D3
    for i in range(128):
        ax.plot([raw_x[i], target_start_x], [raw_y[i], target_start_y], 
                color='#10b981', alpha=0.05, lw=0.5)
    
    # 3. THE SINGLE CONSISTENT SOLUTION (The Final Route)
    t = np.linspace(0, 10.5, 1000)
    x, y = get_unified_final_route(t)
    
    # Outer Glow
    ax.plot(x, y, color='#10b981', lw=15, alpha=0.1)
    ax.plot(x, y, color='#10b981', lw=8, alpha=0.3)
    # The Core Route
    ax.plot(x, y, color='#ffffff', lw=3, label='The Sovereign Route (All 128 Converged)')
    
    # 4. Mark the Critical Hardware Anchors
    # LEFT D3 (Past Regime Anchor)
    ax.scatter([2.0], [6.0], color='#ff00ff', s=150, edgecolors='white', lw=2, zorder=5)
    ax.text(1.5, 6.5, 'LEFT D3\n(Convergence Entry)', color='#ff00ff', fontsize=12, fontweight='bold', ha='right')
    
    # RIGHT D2 (Future Regime Output)
    ax.scatter([14.0], [6.0], color='#00ffff', s=150, edgecolors='white', lw=2, zorder=5)
    ax.text(14.5, 6.5, 'RIGHT D2\n(Sovereign Output)', color='#00ffff', fontsize=12, fontweight='bold', ha='left')
    
    # The 138.88 Resonance Pulse at Zero Point
    ax.scatter([8.0], [16.0], color='#ffff00', s=200, edgecolors='white', lw=2, zorder=5)
    ax.text(8.0, 15.3, 'ZERO POINT\n(138.88° Spark Emission)', color='#ffff00', fontsize=12, fontweight='bold', ha='center')

    # Formatting
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 17)
    ax.set_aspect('equal')
    ax.axis('off')
    
    title = "THE SOVEREIGN UNIFICATION\n128 Fates Converged into a Single Engineering Solution"
    ax.text(8, 17.5, title, ha='center', fontsize=22, fontweight='bold', color='#ffffff', letter_spacing=2)
    
    output_fn = "128_ULTIMATE_ONE_FORM_QUASAR.png"
    plt.savefig(output_fn, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: The Unified Solution rendered to {output_fn} ---")

if __name__ == "__main__":
    plot_one_form_quasar()
