import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from pathlib import Path

# ============================================================================
# PHYSICS_128_GRID_FINAL.py
# ============================================================================
# The absolute master engine for the 128-Type Biological Quasar.
# Implements:
# 1. 128 Unique Trajectories (from Master List)
# 2. Dipole Vortex Flow (Left/Right Grid)
# 3. Smale Horseshoe Folding (Dream mixing at Z < 0.2)
# 4. D3 Tunnelling Bridge (Phase jumping)
# 5. Continuous Manifold Closure
# ============================================================================

# --- PHYSICAL CONSTANTS (from absolute_constants.py) ---
REALITY_TENSION = 1.0100375
TUNNEL_TENSION = (11.0 / 7.0) * REALITY_TENSION # ~1.587
KAPPA_BASE = 1.0 / 32.0
D3_CORRECTION = 69.44 # Degrees
SPARK_ANGLE = 138.88

class QuasarPhysics:
    @staticmethod
    def get_drift(gender, p_type, z):
        """Calculates dx, dy based on gender and MBTI quadrant."""
        # Baseline from MASTER_GEOMETRY_REFERENCE_FINAL.md
        if gender == "Female":
            if p_type == "IP": return 0.0, -0.5  # Vertical descent
            if p_type == "IJ": return 0.5, -0.5  # Maintenance
            if p_type == "EP": return 2.0, -0.5  # Max spiral
            if p_type == "EJ": return np.sin(z * np.pi) * 1.5, -0.5 # Accretion twist
        else: # Male
            if p_type == "IP": return 1.0, 0.5   # Rightward logic
            if p_type == "IJ": return 0.5, 0.5   # Structural anchor
            if p_type == "EP": return 2.0 * np.cos(z * np.pi), 0.5 # Expanding
            if p_type == "EJ": return 3.0 * (1.0 - z), 0.5 # Starburst
        return 0.0, 0.0

    @staticmethod
    def smale_fold(x, y, z):
        """Dream folding at Z < 0.2."""
        if z >= 0.2: return x, y, z
        fold_strength = (0.2 - z) / 0.2
        # Fold X around septum (8.0)
        xf = 8.0 + (x - 8.0) * np.cos(fold_strength * np.pi)
        # Fold Y (Phase mixing)
        yf = y + np.sin(x * np.pi / 4.0) * fold_strength * 4.0
        return xf, yf, z

def generate_trajectories():
    print("--- Loading 128-Type Master List ---")
    df = pd.read_csv("128_Type_Trajectory_Master_List.csv")
    
    num_steps = 200
    z_span = np.linspace(1.0, 0.0, num_steps)
    dt = 1.0 / num_steps
    
    all_results = []
    
    for idx, row in df.iterrows():
        gender = row['Gender']
        mbti = row['MBTI_Mode']
        p_type = mbti[:2] # Extract IP, IJ, EP, EJ
        
        # Initial position based on 16x16 Grid
        # Women Left (0-8), Men Right (8-16)
        x_start = 4.0 if gender == "Female" else 12.0
        # Add blood type variation to start point
        bt_offset = {"O": 0, "A": 1, "B": 2, "AB": 3}[row['Blood_Type']]
        x_start += (bt_offset - 1.5) * 0.5
        
        y_start = (idx % 16) # Spread across phase
        
        traj = np.zeros((num_steps, 3))
        x, y = x_start, y_start
        
        for i, z in enumerate(z_span):
            dx, dy = QuasarPhysics.get_drift(gender, p_type, z)
            
            # Apply D3 Tunnelling logic near septum
            if abs(x - 8.0) < 0.5:
                # Tunnel jump
                x += (8.0 - x) * 2.0 
            
            x += dx * dt
            y += dy * dt
            
            # Fold if near midnight
            xf, yf, zf = QuasarPhysics.smale_fold(x, y, z)
            traj[i] = [xf, yf, zf]
            
        all_results.append({
            'label': f"{mbti}_{row['Blood_Type']}_{gender}",
            'data': traj,
            'color': 'magenta' if gender == "Female" else 'cyan'
        })
        
    return all_results

def render_3d_quasar(results):
    fig = plt.figure(figsize=(16, 12), facecolor="#050510")
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor("#050510")
    
    for item in results:
        data = item['data']
        ax.plot(data[:, 0], data[:, 1], data[:, 2], color=item['color'], alpha=0.3, lw=0.5)
        
    # Plot Singularity
    ax.scatter([8.0], [8.0], [0.0], color='gold', s=300, marker='*', label="Singularity (0D/4D)")
    
    # Labeling
    ax.set_title("THE 128-TYPE BIOLOGICAL QUASAR (V2.3 FINAL)\nUnified Closed Manifold", color='white', fontsize=20)
    ax.set_xlabel("X (Gender Polarity)", color='white')
    ax.set_ylabel("Y (Phase)", color='white')
    ax.set_zlabel("Z (Time)", color='white')
    
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_zlim(0, 1)
    
    output = "128_GRID_PHYSICS_FINAL.png"
    plt.savefig(output, dpi=300, facecolor="#050510")
    print(f"--- SUCCESS: Rendered 128 Trajectories to {output} ---")

if __name__ == "__main__":
    trajectories = generate_trajectories()
    render_3d_quasar(trajectories)
