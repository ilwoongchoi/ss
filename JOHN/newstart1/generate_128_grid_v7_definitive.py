# -*- coding: utf-8 -*-
"""
generate_128_grid_v7_definitive.py
==================================
REPLICATING THE DEFINITIVE PURE GEOMETRY GRID.
1. 8-Section Layout (EJ Women -> EJ Men)
2. Node-to-Node Trajectories (Crowns -> Basins -> Nose -> Gravity)
3. PLP Spine & 138.88° Spark Geometry
"""

import numpy as np
import matplotlib.pyplot as plt

def generate_definitive_grid():
    fig = plt.figure(figsize=(24, 15), facecolor='white')
    ax = fig.add_subplot(111)
    
    # 1. Setup the 8 Columns
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    x_centers = np.linspace(2, 30, 8)
    
    # Grid Metadata
    ax.set_xlim(0, 32)
    ax.set_ylim(-2, 20)
    
    # 2. Define the Master Nodes (The "Junctions" of the Universe)
    nodes = {
        "Nose": [16, 4],           # Darkness Stress / 3/32 Spark Gate
        "Left_Bypass": [6, 6],     # Left Bypass Basin
        "Right_Bypass": [26, 6],   # Right Bypass Basin
        "Gravity": [16, 0],        # Gravity Sensor (Reset)
        "Left_Cortisol": [12, 12], # Horizontal Tension
        "Right_ACh": [18, 12]      # Vertical Tension
    }
    
    # Draw Background Grid & Labels
    for i, label in enumerate(labels):
        ax.text(x_centers[i], 18, label, ha='center', fontweight='bold', fontsize=12)
        ax.axvline(x_centers[i], color='gray', alpha=0.1, linestyle='--')

    # 3. Generate 128 Orderly Trajectories
    for i in range(128):
        bits = [(i >> j) & 1 for j in range(7)]
        # Group determination
        group_idx = i // 16
        x_start = x_centers[group_idx] + (i % 16 - 7.5) * 0.3
        y_start = 17.5
        
        # Determine the Path based on 7-bit Logic
        path = [[x_start, y_start]]
        
        # Step 1: Descend to Hierarchy/Tension Layer
        y_mid = 13.0
        x_mid = x_start
        if bits[3] == 1: # Extravert -> Widens
            x_mid += (bits[3]*2-1) * 1.5
        path.append([x_mid, y_mid])
        
        # Step 2: The "Bypass or Nose" Decision (The 3/32 Funnel)
        if bits[5] == 0: # Thinking/Rigid -> Hits the Nose (Truth)
            target = nodes["Nose"]
            # Add a "Saddle" point before the Nose
            path.append([x_mid * 0.8 + target[0] * 0.2, 8.0])
            path.append(target)
        else: # Feeling/Fluid -> Goes to Bypass
            target = nodes["Left_Bypass"] if x_mid < 16 else nodes["Right_Bypass"]
            path.append(target)
            
        # Step 3: Final Convergence to Gravity Sensor
        path.append(nodes["Gravity"])
        
        # Draw the Path with Type-Specific Colors
        path = np.array(path)
        # Use more distinct colors and solid lines for visibility
        color = '#1f77b4' if bits[0] == 0 else '#d62728' # Distinct Blue for Men, Red for Women
        style = '-' if bits[4] == 1 else '--'     # Intuition/Sensing
        alpha = 0.85 # Increased alpha for solid lines
        lw = 1.8     # Increased linewidth
        ax.plot(path[:,0], path[:,1], color=color, linestyle=style, alpha=alpha, linewidth=lw)
        ax.scatter(path[0,0], path[0,1], color=color, s=15, alpha=1.0) # Clearer starting points

    # 4. Draw the PLP Spine (X + Y = 16 or similar diagonal)
    spine_x = np.linspace(0, 32, 100)
    spine_y = 16 - (spine_x / 2.0) # Corrected diagonal for the grid aspect
    ax.plot(spine_x, spine_y, color='orange', linestyle='--', alpha=0.6, label="PLP Spine X+Y=16")

    # Annotate Key Junctions
    for name, pos in nodes.items():
        ax.scatter(pos[0], pos[1], color='black', s=20, zorder=5)
        ax.text(pos[0]+0.2, pos[1], name.replace("_", " "), fontsize=8, alpha=0.7)

    ax.set_title("128-TYPE PURE GEOMETRY GRID | Definitive Ordered Mapping", fontsize=16, pad=20)
    ax.axis('off')
    
    output_fn = "final_128_grid_orderly.png"
    plt.savefig(output_fn, dpi=300, bbox_inches='tight')
    print(f"Definitive Orderly 128-Grid Rendered: {output_fn}")

if __name__ == "__main__":
    generate_definitive_grid()
