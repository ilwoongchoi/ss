import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

def generate_v10_huge_lqg_sovereign_engine():
    # --- 1. SOVEREIGN ANCHOR (Huge-LQG Zero Point) ---
    B0 = 1.0
    DELTA_T_OBS = 0.2828
    SPARK_RAD = math.radians(138.88)
    
    # 10-Axis Biochemical Valves (Binary States: 0 or 1)
    # These determine the 2^7 = 128 micro-states
    valves = {
        "GABA_B": 1, "GABA_A": 1, "CORTISOL_GR": 1, 
        "5HT_RIGHT": 1, "5HT1A_SINK": 1, "D2_LEFT": 1,
        "VASO_V1AR": 1, "D2_RIGHT": 1, "OXY_OTR": 1,
        "ACETYL_COA": 1
    }
    
    num_states = 128
    steps = 400
    trajectories = []
    
    # Pruning the Lensing Mask (Prune = True reveals the Huge-LQG Anchor)
    PRUNE_VEIL = True

    for i in range(num_states):
        # Binary decomposition of the state index (The 7-bit Betti 7)
        binary_code = format(i, '07b')
        bits = [int(b) for b in binary_code]
        
        # Initial State at the Huge-LQG Anchor (0,0,0)
        pos = np.array([0.0, 0.0, 0.0])
        path = [pos.copy()]
        
        # C-Seed influenced by the 7-bit Binary Structure
        angle = (i / num_states) * 2 * np.pi
        C = complex(math.cos(angle) * DELTA_T_OBS, math.sin(angle) * DELTA_T_OBS)
        Z = complex(0, 0)

        for t_step in range(steps):
            t = t_step * 0.04
            
            if t < DELTA_T_OBS:
                continue
            
            # Recursive Soliton Breath (The Fuel Cell Reaction)
            # Binary bits act as local operators on the breath
            damping = 0.02 * (1.1 if bits[0] else 0.9)
            Z = (Z**2 + C) * (1.0 - damping)
            
            if abs(Z) > 4.0: Z = (Z / abs(Z)) * 4.0
            
            # Radial Expansion (Vaso vs Oxy tension)
            radius = abs(Z) * (1.0 + 0.05 * math.sin(t * 2))
            
            # Phase Rotation (GABA-A Spark & Drift)
            theta = math.atan2(Z.imag, Z.real) + (0.076 * t * (1 if bits[1] else -1))
            
            # Spark Clearing (Every 0.2828 cycle)
            if t_step % 25 == 0:
                theta += SPARK_RAD * (bits[2] * 2 - 1)
            
            # Phi Mapping (The 6-Axis Topology)
            phi = (i / num_states) * np.pi + (0.02 * math.cos(t * bits[3]))
            
            # Projection to 3D Space (Absolute Box B0=1)
            new_pos = np.array([
                radius * math.sin(phi) * math.cos(theta),
                radius * math.sin(phi) * math.sin(theta),
                radius * math.cos(phi)
            ])
            
            # The 7th Operator: Attraction to the Huge-LQG Zero Point
            dist = np.linalg.norm(new_pos) + 1e-9
            # If PRUNE_VEIL is True, external sink is active
            attraction = (np.array([0,0,0]) - new_pos) / (dist**2) * 0.02
            new_pos += attraction * (bits[4] + bits[5]) # Composite interaction
            
            pos = new_pos
            path.append(pos.copy())
            
        trajectories.append(np.array(path))

    # --- RENDER: THE BINARY UNIVERSE ---
    fig = plt.figure(figsize=(16, 16), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # 128 States colored by their Binary Groupings
    for i, path in enumerate(trajectories):
        color_val = (i / num_states)
        ax.plot(path[:,0], path[:,1], path[:,2], color=plt.cm.cool(color_val), alpha=0.3, lw=0.5)
        
    # The Huge-LQG Zero Point (The Sovereign Anchor)
    ax.scatter([0], [0], [0], color='gold', s=400, marker='*', label='HUGE-LQG ZERO POINT (ANCHOR)')
    
    # 128 Grid Points (Final Equilibrium Solutions)
    grid_pts = np.array([p[-1] for p in trajectories])
    ax.scatter(grid_pts[:,0], grid_pts[:,1], grid_pts[:,2], color='white', s=5, alpha=0.8)

    ax.set_axis_off()
    ax.set_title(f"V10 SOVEREIGN ENGINE: HUGE-LQG ANCHOR & 128 BINARY GRID", color='white', fontsize=20)
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
    
    output_fn = "V10_HUGE_LQG_GRID.png"
    plt.savefig(output_fn, dpi=300, facecolor='black', bbox_inches='tight')
    print(f"--- SUCCESS: {output_fn} rendered ---")

if __name__ == "__main__":
    generate_v10_huge_lqg_sovereign_engine()
