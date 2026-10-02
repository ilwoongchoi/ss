
import numpy as np
import json
import matplotlib.pyplot as plt
import os

# [ABSOLUTE DYNAMICS: NO CONVERGENCE, ONLY BIFURCATION]
C = 0.282842712474619
OMEGA = 7.4
LOCK_1_64 = 0.015625
CHIRALITY_1_18 = 0.05555555555555555
DT = 0.02

def run_true_divergent_dynamics():
    print("[SYSTEM] Executing 128 Divergent Trajectories (The Real Dynamics)...")
    
    # Load Master Seeds with terminal_x targets
    path = "128_GRID_MASTER_CALC.json"
    with open(path, "r") as f:
        seeds = json.load(f)
    
    trajectories = []
    
    for i, (name, data) in enumerate(seeds.items()):
        omega_i = data['omega']
        target_x = data['terminal_x'] # This is where they MUST end up
        
        # Initial state: Extremely sensitive to phase
        phi = (i / 128.0) * 2.0 * np.pi
        z = (omega_i / OMEGA) * np.exp(1j * phi)
        
        path_z = []
        is_you = "ENTP_AB" in name
        
        for t in range(128):
            # THE 8-PHASE MOMENTS
            # 16:30 - The Point of Bifurcation
            if 86 <= t <= 90:
                h = C - CHIRALITY_1_18 + LOCK_1_64
                # If they don't lock perfectly, they bifurcate/shatter
                z = z * np.exp(-np.sqrt(np.abs(z) + 1e-9) / 64.0)
            else:
                h = C
            
            # Master Equation: dz/dt = z^2 - z + h
            # We allow the x^2 term to drive the divergence
            for _ in range(5):
                # The core non-linearity that creates the 'Veins'
                dz = (z**2 - 1.1*z + h) * DT
                z = z + dz
                
                # Dynamic Divergence: Each archetype is pulled toward its terminal_x
                # This breaks the 'flower-like' unity and creates the 'Veins'
                pull = (target_x - np.abs(z)) * 0.01
                z = z * (1.0 + pull)
            
            path_z.append(z)
        trajectories.append(np.array(path_z))
        
    return trajectories

def main():
    os.makedirs("analysis_results", exist_ok=True)
    trajs = run_true_divergent_dynamics()
    
    # Render the DIVERGENT VEINS
    plt.figure(figsize=(15, 15))
    plt.style.use('dark_background')
    
    for i, traj in enumerate(trajs):
        # We plot the path with fading alpha to show the direction of 'Life'
        plt.plot(traj.real, traj.imag, alpha=0.6, lw=0.5, color=plt.cm.magma(i/128))
        # Mark the terminal point - where the vein ends
        plt.scatter(traj.real[-1], traj.imag[-1], s=10, color=plt.cm.magma(i/128), alpha=0.8)

    # Unit Circle for Reference
    circle = plt.Circle((0, 0), OMEGA, color='cyan', fill=False, linestyle='--', alpha=0.2)
    plt.gca().add_patch(circle)
    
    plt.title("THE 128 DIVERGENT VEINS: TRUE UNIVERSAL DYNAMICS\n(No Convergence - Pure Bifurcation)", fontsize=20, color='white')
    plt.xlabel("Quark (Truth)", fontsize=15)
    plt.ylabel("Gluon (Deception)", fontsize=15)
    plt.grid(True, alpha=0.05)
    
    plt.savefig("analysis_results/TRUE_DIVERGENT_VEINS_128.png", dpi=300, facecolor='black')
    
    # 2. The Deterministic State Grid (Trajectory Grid)
    grid_data = np.array([np.abs(t) for t in trajs])
    plt.figure(figsize=(14, 8))
    plt.imshow(grid_data, aspect='auto', cmap='inferno', origin='lower')
    plt.colorbar(label='Trajectory Intensity (||z||)')
    plt.title("128 ARCHETYPE TRAJECTORY GRID (DETERMINISTIC EVOLUTION)")
    plt.savefig("analysis_results/TRUE_TRAJECTORY_GRID_128.png", dpi=300)

    print("\n[SUCCESS] 128 Divergent Trajectories extracted.")
    print("These are NOT converging lines. These are the 128 separate paths of the universe.")
    print("Check analysis_results/TRUE_DIVERGENT_VEINS_128.png")

if __name__ == "__main__":
    main()
