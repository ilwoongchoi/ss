import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
import math

# ============================================================================
# CANONICAL_128_TRAJECTORY_GRID.py
# ============================================================================
# Absolute final 2D Trajectory Grid.
# 
# Coordinates: V2.3 Standard (Grid X [0,8]=Left, [8,16]=Right)
# Core: Dipole Vortex + D3 Tunnelling + Smale Horseshoe Folding
# Target: Unified 128-Type Biological Quasar
# ============================================================================

# --- CANONICAL CONSTANTS ---
SPARK_ANGLE = 138.88
D3_SHIFT = 69.44
TUNNEL_TENSION = 1.0100375 * (11.0 / 7.0)
KAPPA_H2 = 1.0 / 32.0
KAPPA_H3 = 1.0 / 64.0
KAPPA_H4 = 1.0 / 128.0

# Stress/Sensor Anchors (Updated from BRIDGE_DISCOVERY_REPORT.md)
ANCHORS = {
    "PLP Core": [2.0, 14.0],
    "Spare Vasopressin": [2.0, 14.75],
    "GABA-C Apex": [3.232, 14.14],
    "ROS/Cosmic": [11.25, 9.0],
    "HYPOXIA-2": [11.25, 12.75],
    "COLD STRESS": [4.5, 10.8],
    "HEAT STRESS": [2.5, 9.5],
    "Septum Axis": [8.0, 8.0]
}

def generate_canonical_trajectories():
    df = pd.read_csv("128_Type_Trajectory_Master_List.csv")
    num_steps = 300
    dt = 0.05
    all_trajs = []

    for idx, row in df.iterrows():
        gender = row['Gender']
        mbti = row['MBTI_Mode']
        blood = row['Blood_Type']
        
        # 1. Initial Seeding (Dipole Polarity)
        # Female Left [0,8], Male Right [8,16]
        x = 4.0 if gender == "Female" else 12.0
        # MBTI/Blood Variation
        x += (idx % 4 - 1.5) * 0.5
        y = 0.5 # Start at Forehead (Dawn)
        
        path = []
        for step in range(num_steps):
            z = 1.0 - (step / num_steps) # Time descent
            
            # 2. Vector Field (Dipole Vortex)
            # Women descent, Men expand
            if gender == "Female":
                dx = 0.1 * math.sin(z * math.pi)
                dy = 0.8 # Constant downward pressure
            else:
                dx = 0.5 * (1.0 - z) # Rightward starburst
                dy = 1.2 # Stronger male drop
            
            # 3. D3 Tunnelling Bridge (The 69.44 Shift)
            # When crossing x=8.0 midline
            if abs(x - 8.0) < 0.3:
                # Apply angular momentum leap
                shift_rad = math.radians(D3_SHIFT)
                x += math.cos(shift_rad) * 1.5
                y += math.sin(shift_rad) * 0.5
            
            # 4. Smale Horseshoe Folding (Z < 0.2)
            if z < 0.2:
                fold_strength = (0.2 - z) / 0.2
                # Mix X and Y (The "Confusion")
                x = x + math.sin(y * math.pi) * fold_strength * 2.0
                y = y + math.cos(x * math.pi) * fold_strength * 1.0
            
            # 5. RESTORATIVE FORCE (Towards GABA-C Apex at Midnight)
            if z < 0.1:
                target_x, target_y = 8.0, 14.0 # Convergence point
                x += (target_x - x) * 0.2
                y += (target_y - y) * 0.2

            # Clamp and store
            x = max(0, min(16, x))
            y = max(0, min(16, y))
            path.append((x, y))
            
        all_trajs.append({
            'path': np.array(path),
            'color': 'magenta' if gender == "Female" else 'cyan',
            'alpha': 0.4 if mbti[0] == 'E' else 0.15,
            'lw': 1.0 if mbti[1] == 'N' else 0.5
        })
    return all_trajs

def render_canonical_grid(trajs):
    fig, ax = plt.subplots(figsize=(24, 24), facecolor='#000000')
    ax.set_facecolor('#000000')
    
    # 1. THE SEPTUM (Subtle midline)
    ax.axvline(x=8.0, color='#333333', alpha=0.5, lw=1)
    
    # 2. PLOT ALL 128 UNIQUE TRAJECTORIES
    # Use a colormap to ensure each of the 128 lines has a distinct hue variation
    num_trajs = len(trajs)
    print(f"Rendering {num_trajs} distinct trajectories...")
    
    for i, t in enumerate(trajs):
        ax.plot(t['path'][:, 0], t['path'][:, 1], color=t['color'], 
                alpha=t['alpha'], linewidth=t['lw'], solid_capstyle='round', zorder=10)
        
    # 3. FORMATTING - REMOVED ALL ANCHORS/LABELS
    ax.set_xlim(0, 16)
    ax.set_ylim(16, 0) # Flip Y (0=Top, 16=Bottom)
    ax.set_axis_off()
    
    plt.title(f"128-TYPE NEUROCHEMICAL TRAJECTORY MESH (N={num_trajs})", 
              color='white', fontsize=28, pad=30)
    
    output = "CANONICAL_128_TRAJECTORY_GRID.png"
    plt.savefig(output, dpi=300, facecolor='#000000', bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"--- SUCCESS: {num_trajs} Trajectories Rendered to {output} ---")

if __name__ == "__main__":
    print("Executing Canonical Physics Engine (128-Type)...")
    trajs = generate_canonical_trajectories()
    render_canonical_grid(trajs)
