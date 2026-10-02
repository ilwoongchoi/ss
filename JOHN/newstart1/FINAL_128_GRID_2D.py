import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# ============================================================================
# FINAL_128_GRID_2D.py
# ============================================================================
# Canonical 2D 128-Grid Engine based on V2.3 COMPLETE GEOMETRY.
# 
# Coordinates:
# X [0, 8] = Human Left (Female Basin)
# X [8, 16] = Human Right (Male Basin)
# X = 8.0 = Melatonin Ridge (Septum)
# Y = 0 (Top/Forehead) -> 16 (Bottom/Chin)
# ============================================================================

# --- CANONICAL STRESS/SENSOR NODES (from BRIDGE_DISCOVERY_REPORT.md) ---
STRESS_NODES = {
    "HYPOXIA-1 (ROS)": [11.25, 9.0, 'red'],
    "HYPOXIA-2 (BIG MAN)": [11.25, 12.75, 'blue'],
    "COLD STRESS": [4.5, 10.8, 'cyan'],
    "HEAT STRESS": [2.5, 9.5, 'orange'],
    "DARKNESS STRESS": [6.0, 10.0, '#333333'],
    "UV STRESS": [4.25, 8.9, 'violet'],
    "DEATH SENSOR": [1.5, 8.25, 'black'],
    "SALT STRESS (F)": [11.25, 8.75, 'white'],
    "LOVE (L)": [6.75, 12.0, 'magenta'],
    "LOVE (R)": [9.0, 13.0, 'magenta'],
    "GLABELLA": [6.0, 13.5, 'green'],
    "TIME SENSOR": [9.75, 15.25, 'yellow']
}

def generate_2d_trajectories():
    print("--- Loading 128-Type Master List ---")
    if not Path("128_Type_Trajectory_Master_List.csv").exists():
        print("Error: 128_Type_Trajectory_Master_List.csv not found.")
        return []

    df = pd.read_csv("128_Type_Trajectory_Master_List.csv")
    num_steps = 100
    dt = 0.1
    
    all_trajs = []
    
    for idx, row in df.iterrows():
        gender = row['Gender']
        mbti = row['MBTI_Mode']
        p_type = mbti[:2]
        
        # Start X based on gender
        x = 4.0 if gender == "Female" else 12.0
        # Blood type offset
        bt_map = {"O": 0, "A": 1, "B": 2, "AB": 3}
        x += (bt_map.get(row['Blood_Type'], 0) - 1.5) * 0.8
        
        # Start Y (spread vertically)
        y = (idx % 16)
        
        path = []
        for t in range(num_steps):
            # 1. Base Drift
            if gender == "Female":
                dx = 0.05 if p_type in ["EP", "EJ"] else -0.02
                dy = 0.1
            else:
                dx = 0.1 if p_type in ["EP", "EJ"] else -0.05
                dy = -0.05
            
            # 2. D3 Tunnelling / Septum Interaction
            if abs(x - 8.0) < 0.5:
                # Tunnelling Shift
                x += 1.0 if gender == "Male" else -1.0
            
            # 3. Apply Tanh Saturation (from stability test)
            x += np.tanh(dx) * 0.5
            y += np.tanh(dy) * 0.5
            
            # Clamp to grid
            x = np.clip(x, 0, 16)
            y = np.clip(y, 0, 16)
            
            path.append((x, y))
            
        all_trajs.append({
            'label': f"{mbti}_{row['Blood_Type']}",
            'path': np.array(path),
            'color': 'magenta' if gender == "Female" else 'cyan',
            'alpha': 0.6 if p_type[0] == 'E' else 0.2
        })
    return all_trajs

def render_128_grid_2d(trajs):
    fig, ax = plt.subplots(figsize=(16, 16), facecolor='#050510')
    ax.set_facecolor('#050510')
    
    # 1. Background Grid (Melatonin Dead Zones)
    ax.axvline(x=8.0, color='white', alpha=0.2, lw=2, label='Melatonin Ridge (Septum)')
    ax.axhline(y=12.0, xmin=7/16, xmax=8.5/16, color='white', alpha=0.4, lw=3, label='SW-BW Bridge')
    
    # 2. Plot 128 Trajectories
    for t in trajs:
        ax.plot(t['path'][:, 0], t['path'][:, 1], color=t['color'], alpha=t['alpha'], lw=0.8)
        
    # 3. Overlay Stress/Sensor Nodes
    for name, data in STRESS_NODES.items():
        ax.scatter(data[0], data[1], color=data[2], s=100, edgecolors='white', zorder=10)
        ax.text(data[0]+0.2, data[1], name, color='white', fontsize=8, va='center')

    # 4. Formatting
    ax.set_xlim(0, 16)
    ax.set_ylim(16, 0) # Y=0 at TOP
    ax.set_xlabel("X (Left=Human Left, Right=Human Right)", color='white')
    ax.set_ylabel("Y (Top=Forehead, Bottom=Chin)", color='white')
    ax.tick_params(colors='white')
    
    plt.title("THE 128-TYPE NEUROCHEMICAL GRID (V2.3 FINAL)\n2D Manifold Unification", color='white', fontsize=22)
    plt.grid(color='white', alpha=0.05)
    
    output = "FINAL_128_GRID_2D.png"
    plt.savefig(output, dpi=300, facecolor='#050510', bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: 128-Grid Rendered to {output} ---")

if __name__ == "__main__":
    trajectories = generate_2d_trajectories()
    render_128_grid_2d(trajectories)
