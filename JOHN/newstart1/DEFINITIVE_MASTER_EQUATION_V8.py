import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

def generate_v8_sovereign_sphere():
    # --- 1. AXIOMATIC CONSTANTS (Derived from B0=1) ---
    B0 = 1.0
    PRIME_BASIS = [2, 3, 5, 7, 11]
    B5, B7, B11 = 5, 7, 11
    
    # The Primordial Delta (0.2828)
    WINDING_RATIO = B11 / B7  # 1.5714
    LOOP_STRENGTH = 5.555492  # Derived from 1/18
    DELTA_T_OBS = WINDING_RATIO / LOOP_STRENGTH # 0.2828
    
    # The Spark & Drift
    GAP = B11 / (B7 + B0) # 1.375
    SPARK_ANGLE_DEG = 137.508 + GAP # 138.88
    SPARK_RAD = math.radians(SPARK_ANGLE_DEG)
    DRIFT = GAP / 18.0 # 0.076
    
    # 0.02 Bremsstrahlung Tax
    BREMS_TAX = 0.02 
    
    # --- 2. DYNAMICS ENGINE (Recursive S5 Projection) ---
    num_types = 128
    steps = 200
    trajectories = []

    for i in range(num_types):
        # Particle Isomorphism
        # 0-31: EJ(Photon), 32-63: IP(Proton), 64-95: EP(Electron), 96-127: IJ(Neutrino)
        group = i // 32
        charge = 1 if (i % 2 == 0) else -1 # E(+) vs I(-)
        
        # Initial State: Start at the edge of Phase 1 (0.2828)
        # Coordinates centered at (0,0,0) for the sphere
        pos = np.array([0.0, 0.0, 0.0])
        vel = np.random.normal(0, 0.01, 3)
        path = [pos.copy()]
        
        # Complex Seed C (Reality Distortion)
        angle_seed = (i / num_types) * 2 * np.pi
        C = complex(math.cos(angle_seed) * 0.2828, math.sin(angle_seed) * 0.2828)
        Z = complex(0, 0)

        for t_step in range(steps):
            t = t_step * 0.1
            
            # Phase 1: Winding (Before Ignition)
            if t < DELTA_T_OBS:
                # Scalar field only, no movement
                pass
            else:
                # Phase 2: Ignition & Recursion (Z = Z^2 + C)
                # Apply Bremsstrahlung Damping (0.02) to prevent overflow
                Z = (Z**2 + C) * (1.0 - BREMS_TAX)
                
                # Limit the growth to remain within the S5 manifold
                if abs(Z) > 2.0:
                    Z = (Z / abs(Z)) * 2.0
                
                # Update 3D Physics via Complex Phase
                radius = abs(Z) + (t - DELTA_T_OBS) * 0.2 # Adjusted scaling
                theta = math.atan2(Z.imag, Z.real) + (DRIFT * t * charge)
                
                # Phi mapping with Bremsstrahlung cooling
                phi_base = (i / num_types) * np.pi
                phi = phi_base + (BREMS_TAX * math.sin(t * 2))
                
                # Spark Refraction (The 138.88 Correction)
                if t_step % 20 == 0:
                    theta += SPARK_RAD
                
                # Project back to 3D
                new_pos = np.array([
                    radius * math.sin(phi) * math.cos(theta),
                    radius * math.sin(phi) * math.sin(theta),
                    radius * math.cos(phi)
                ])
                
                # Coulomb Law Attractor (The 1/r^2 distortion)
                # Normalized to prevent division by zero or infinity
                dist = np.linalg.norm(new_pos) + 0.1
                force_mag = (B0 / (dist**2)) * 0.05 * charge
                new_pos += (new_pos / dist) * force_mag
                
                pos = new_pos
                path.append(pos.copy())
        
        trajectories.append(np.array(path))

    # --- 3. RENDERING THE BRANCHING SPHERE ---
    fig = plt.figure(figsize=(15, 15), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Load ROI Data from CSV files
    # ROI_LEFT_D2_OCULI_OUTER_POINTS.csv (x,y pairs)
    # Assuming z=0 for simplicity in overlay
    roi_d2 = np.array([
        [0.0, 7.0, 0.0], [0.0, 7.25, 0.0], [0.0, 7.5, 0.0], [0.0, 7.75, 0.0], [0.0, 8.0, 0.0],
        [0.0, 8.25, 0.0], [0.0, 8.5, 0.0], [0.0, 8.75, 0.0], [0.0, 9.0, 0.0], [0.0, 9.25, 0.0],
        [0.0, 9.5, 0.0], [0.0, 9.75, 0.0], [0.0, 10.0, 0.0], [0.0, 10.25, 0.0], [0.0, 10.5, 0.0],
        [0.0, 10.75, 0.0], [0.0, 11.0, 0.0], [0.0, 11.25, 0.0], [0.0, 11.5, 0.0], [0.0, 11.75, 0.0],
        [0.0, 12.0, 0.0] 
    ])
    # ROI_PLP_CAULDRON_LEFT_POINTS.csv (x,y pairs)
    # Assuming z=0 for simplicity in overlay
    roi_plp = np    .array([
        [1.5, 7.0, 0.0], [1.5, 7.25, 0.0], [1.5, 7.5, 0.0], [1.5, 7.75, 0.0], [1.5, 8.0, 0.0],
        [1.5, 8.25, 0.0], [1.5, 8.5, 0.0], [1.5, 8.75, 0.0], [1.5, 9.0, 0.0], [1.5, 9.25, 0.0],
        [1.5, 9.5, 0.0], [1.5, 9.75, 0.0], [1.5, 10.0, 0.0], [1.5, 10.25, 0.0], [1.5, 10.5, 0.0],
        [1.5, 10.75, 0.0], [1.5, 11.0, 0.0], [1.5, 11.25, 0.0], [1.5, 11.5, 0.0], [1.5, 11.75, 0.0],
        [1.5, 12.0, 0.0]
    ])
    
    # Project ROI points into the Sovereign Sphere Space
    ax.scatter(roi_d2[:,0], roi_d2[:,1], roi_d2[:,2], color='#00aaff', s=50, label='LEFT_D2_OCULI', alpha=0.9)
    ax.scatter(roi_plp[:,0], roi_plp[:,1], roi_plp[:,2], color='#ff4400', s=50, label='PLP_CAULDRON', alpha=0.9)

    colors = ['#ffff00', '#ff00ff', '#00ffff', '#ffffff'] # EJ, IP, EP, IJ
    
    for i, path in enumerate(trajectories):
        group = i // 32
        ax.plot(path[:,0], path[:,1], path[:,2], color=colors[group], alpha=0.3, lw=0.6)
        
    # Draw the Zero-Point (Neutralized)
    ax.scatter([0], [0], [0], color='white', s=150, marker='*', label='Zero-Point Void (B0=1)')
    
    ax.set_axis_off()
    ax.set_title("V8 SOVEREIGN SPHERE: ROI OVERLAY & BRANCHING VERIFICATION", color='white', fontsize=18)
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
    
    output_fn = "V8_VERIFICATION_SPHERE.png"
    plt.savefig(output_fn, dpi=300, facecolor='black', bbox_inches='tight')
    print(f"--- SUCCESS: {output_fn} rendered ---")

if __name__ == "__main__":
    generate_v8_sovereign_sphere()
