# -*- coding: utf-8 -*-
"""
VISUALIZE BIFURCATION GEOMETRY
==============================
Generates a visual map of the 'Envelope Layer' trajectories:
- Female Pact (0 -> Glabella)
- Muscle Line Strips (Vertical)
- ESFX Confidence / ISFX Self-Esteem
- Pathological Descent/Climb
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def draw_bifurcation_map(gender="M"):
    fig, ax = plt.subplots(figsize=(10, 12), facecolor='white')
    
    # 1. Base Grid (0-16)
    ax.set_xlim(-1, 17)
    ax.set_ylim(17, -1)
    ax.grid(True, which='both', linestyle='--', alpha=0.3)
    ax.set_title(f"BIFURCATION GEOMETRY MAP (Gender: {gender})", fontsize=15, pad=20)
    
    # 2. Load ROI Data
    roi = pd.read_csv("ROI_SUPER_LAYER_BIFURCATION.csv")
    
    # 3. Draw Vertical Strips (Muscle Strips)
    for name, group in roi[roi['Layer'] == 'Muscle'].groupby('Node_Name').apply(lambda x: x.iloc[0]).reset_index(drop=True).iterrows():
        # Handle top/bottom strips
        pass # Simplified for plot
    
    # Frontalis Strips
    ax.vlines(x=14.5, ymin=0.5, ymax=2.5, color='red', linewidth=4, label='Frontalis Strip (R)')
    ax.vlines(x=1.5, ymin=0.5, ymax=2.5, color='blue', linewidth=4, label='Frontalis Strip (L)')
    
    # Temporalis Trunks
    ax.vlines(x=11.5, ymin=7.0, ymax=10.0, color='orange', linewidth=3, label='Temporalis Trunk 1')
    ax.vlines(x=12.5, ymin=7.0, ymax=10.0, color='orange', linewidth=3, linestyle='--')
    
    # Occipitalis Strips
    ax.vlines(x=13.0, ymin=14.0, ymax=16.0, color='green', linewidth=4, label='Occipitalis Strip (R)')
    ax.vlines(x=3.0, ymin=14.0, ymax=16.0, color='purple', linewidth=4, label='Occipitalis Strip (L)')
    
    # 4. Draw Envelope Nodes
    for i, row in roi[roi['Layer'] != 'Muscle'].iterrows():
        color = 'black'
        if 'Confidence' in row['Impact']: color = 'cyan'
        if 'Self-Esteem' in row['Impact']: color = 'magenta'
        if 'Pathology' in row['Impact']: color = 'darkred'
        if 'Origin' in row['Impact']: color = 'gold'
        
        ax.scatter(row['Grid_X'], row['Grid_Y'], c=color, s=100, edgecolors='black', zorder=5)
        ax.text(row['Grid_X']+0.3, row['Grid_Y'], row['Node_Name'], fontsize=9, verticalalignment='center')

    # 5. Draw CURVED TRAJECTORIES (The "휘감는" Layers)
    
    # A. Female Pact (0 -> Glabella)
    t = np.linspace(0, 1, 50)
    # Start at (8,0), End at (7.6, 2.2)
    x_pact = 8.0 * (1-t) + 7.6 * t - 0.8 * np.sin(np.pi * t) 
    y_pact = 2.2 * t
    ax.plot(x_pact, y_pact, color='gold', linewidth=3, linestyle='-', label='Female Pact Route')
    
    # B. Extraversion Re-branching (Frontalis -> Schiz Descent)
    # Path from Frontalis R (14.5, 2.5) to Schiz Descent (15.0, 11.5)
    x_schiz = [14.5, 15.5, 15.0]
    y_schiz = [2.5, 7.0, 11.5]
    t_interp = np.linspace(0, 1, 50)
    from scipy.interpolate import make_interp_spline
    try:
        spl = make_interp_spline(y_schiz, x_schiz, k=2)
        y_new = np.linspace(2.5, 11.5, 50)
        x_new = spl(y_new)
        ax.plot(x_new, y_new, color='darkred', linewidth=2, alpha=0.6, label='Schiz Descent Path')
    except:
        ax.plot(x_schiz, y_schiz, color='darkred', linewidth=2, alpha=0.6)

    # C. Preservation Re-branching (Self-Esteem -> Cancer Climb)
    # Path from Self-Esteem L (2.5, 12.5) to Cancer Climb (13.0, 11.5) ? 
    # User said Cancer is "Climb (상승)" so it starts lower.
    ax.vlines(x=13.0, ymin=15.0, ymax=8.0, color='darkgreen', linewidth=2, label='Cancer Climb Line')
    ax.vlines(x=15.0, ymin=8.0, ymax=15.0, color='red', linewidth=2, label='Schiz Descent Line')

    # 6. Final Polish
    ax.legend(loc='upper right', fontsize=8)
    plt.savefig(f"BIFURCATION_GEOMETRY_{gender}.png", dpi=300)
    print(f"Saved: BIFURCATION_GEOMETRY_{gender}.png")

if __name__ == "__main__":
    draw_bifurcation_map("M")
    draw_bifurcation_map("F")
