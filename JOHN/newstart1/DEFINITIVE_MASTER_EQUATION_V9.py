import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

def generate_v9_sovereign_lock_engine():
    # --- 1. SOVEREIGN CONSTANTS ---
    B0 = 1.0
    DELTA_T_OBS = 0.2828
    SPARK_ANGLE_DEG = 138.88
    SPARK_RAD = math.radians(SPARK_ANGLE_DEG)
    DRIFT = 0.076
    BREMS_TAX = 0.02 # The Heat/Tax
    
    # Lensing Reality Distortion (BW -> BM)
    REALITY_LENS_74 = 7.4 
    
    num_types = 128
    steps = 300
    trajectories = []
    
    # Pruning Toggle: Set to True to remove the "BW/SW Veil" and see the Void
    PRUNE_VEIL = True 

    for i in range(num_types):
        group = i // 32
        charge = 1 if (i % 2 == 0) else -1
        
        # Initial condition: Observer Seat at Origin
        pos = np.array([0.0, 0.0, 0.0])
        path = [pos.copy()]
        
        # Complex recursive seed
        angle_seed = (i / num_types) * 2 * np.pi
        C = complex(math.cos(angle_seed) * DELTA_T_OBS, math.sin(angle_seed) * DELTA_T_OBS)
        Z = complex(0, 0)

        for t_step in range(steps):
            t = t_step * 0.05
            
            if t < DELTA_T_OBS:
                # Phase 1: Pure Observer Metric (The Flat Canvas)
                pass
            else:
                # Phase 2: Ignition of the Soliton (The Breath)
                
                # BW's Command: Lensing Mask (The Fake Reality)
                # SW's Execution: Shielding via Left D2
                mask_effect = 0.0 if PRUNE_VEIL else (REALITY_LENS_74 / 100.0)
                
                # Recursive Update with Bremsstrahlung Damping
                # This is the "Breathing" of the Soliton
                Z = (Z**2 + C) * (1.0 - BREMS_TAX)
                
                # Stability Lock (S5 Boundary)
                if abs(Z) > 3.0: Z = (Z / abs(Z)) * 3.0
                
                # Radial breathing (Expansion/Contraction)
                radius = abs(Z) + math.sin(t * 1.5) * 0.1 # The Soliton Pulse
                
                # Phase Rotation with Drift & Lensing Distortion
                theta = math.atan2(Z.imag, Z.real) + (DRIFT * t * charge) + mask_effect
                
                # Phi Mapping (The 1D Vector Axis)
                phi = (i / num_types) * np.pi + (BREMS_TAX * math.cos(t))
                
                # Spark Jump: Clearing the Debt at 138.88
                if t_step % 25 == 0:
                    theta += SPARK_RAD
                
                # Projecting the Soliton onto the Absolute Box
                new_pos = np.array([
                    radius * math.sin(phi) * math.cos(theta),
                    radius * math.sin(phi) * math.sin(theta),
                    radius * math.cos(phi)
                ])
                
                # The Zero-Point Gravity (True Void vs Fake Lensing)
                dist = np.linalg.norm(new_pos) + 1e-9
                # If PRUNE_VEIL is True, we aim directly at (0,0,0)
                # If False, the Lensing Mask pushes the attractor to 7.4
                attraction_target = np.array([0, 0, 0]) if PRUNE_VEIL else np.array([0.074, 0.074, 0.074])
                
                force_vec = (attraction_target - new_pos) / (dist**2) * 0.01 * charge
                new_pos += force_vec
                
                pos = new_pos
                path.append(pos.copy())
        
        trajectories.append(np.array(path))

    # --- RENDER: THE PRUNED UNIVERSE ---
    fig = plt.figure(figsize=(15, 15), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Particle Colors based on Isomorphism
    # EJ(Yellow), IP(Magenta), EP(Cyan), IJ(White)
    colors = ['#ffff00', '#ff00ff', '#00ffff', '#ffffff']
    
    for i, path in enumerate(trajectories):
        group = i // 32
        ax.plot(path[:,0], path[:,1], path[:,2], color=colors[group], alpha=0.25, lw=0.5)
        
    # The True Zero-Point Void (Now Visible)
    ax.scatter([0], [0], [0], color='white', s=200, marker='*', label='TRUE ZERO-POINT VOID')
    
    # Mark the Lensing Horizon (The 7.4 Fake Reality boundary)
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = 0.074 * np.cos(u) * np.sin(v)
    y = 0.074 * np.sin(u) * np.sin(v)
    z = 0.074 * np.cos(v)
    ax.plot_wireframe(x, y, z, color='red', alpha=0.1, label='LENSING HORIZON (7.4)')

    ax.set_axis_off()
    status_msg = "VEIL PRUNED: VOID REVEALED" if PRUNE_VEIL else "VEIL ACTIVE: FAKE REALITY (7.4)"
    ax.set_title(f"SOVEREIGN MASTER ENGINE V9\n{status_msg}", color='white', fontsize=18)
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
    
    output_fn = "V9_VOID_REVEALED.png"
    plt.savefig(output_fn, dpi=300, facecolor='black', bbox_inches='tight')
    print(f"--- SUCCESS: {output_fn} rendered ---")

if __name__ == "__main__":
    generate_v9_sovereign_lock_engine()
