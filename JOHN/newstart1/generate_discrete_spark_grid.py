
import numpy as np
import json
import matplotlib.pyplot as plt
import os

# [THE DISCRETE TRUTH: NO CONTINUOUS NOISE]
C = 0.282842712474619
OMEGA = 7.4
LOCK_1_64 = 0.015625
CHIRALITY_1_18 = 0.05555555555555555

def run_discrete_spark_dynamics():
    print("[SYSTEM] Compiling Discrete Spark Map (Continuous = Disease)...")
    
    # Load Seeds
    path = "128_GRID_MASTER_CALC.json"
    with open(path, "r") as f:
        seeds = json.load(f)
    
    results = []
    
    for i, (name, data) in enumerate(seeds.items()):
        omega_i = data['omega']
        # Initial Position
        z = (omega_i / OMEGA) * np.exp(1j * (i * 2 * np.pi / 128.0))
        
        traj = []
        has_sparked = True if i % 2 == 0 else False # Example: Half spark, half drift
        
        for t in range(128):
            # --- THE DISCRETE ITERATION: z = z^2 + h ---
            h_eff = C
            
            # THE CRITICAL SPARK WINDOWS
            is_window = (86 <= t <= 90) or (16 <= t <= 20) or (78 <= t <= 82)
            
            if is_window:
                if has_sparked:
                    # [SPARK ACTION] - Forcefully slot back to OMEGA
                    # This is what you do with the 30 nodes
                    z = OMEGA * (z / np.abs(z)) 
                    h_eff = C - CHIRALITY_1_18 + LOCK_1_64
                else:
                    # [DRIFT/DISEASE] - Failure to spark causes bifurcation
                    h_eff = C + 0.05 # Entropy accumulation
            
            # The Universal Atomic Step
            z = z**2 - z + h_eff
            
            # Bifurcation Check (Disease Manifestation)
            if not has_sparked and np.abs(z) > OMEGA * 1.2:
                # This is the 'Divergence' you called disease
                z = z * 1.05 # Accelerated collapse/explosion
            
            # Clamping only for rendering, the math is allowed to break
            if np.abs(z) > 20.0: z = (z / np.abs(z)) * 20.0
            
            traj.append(z)
        results.append(np.array(traj))
        
    return results

def main():
    os.makedirs("analysis_results", exist_ok=True)
    trajs = run_discrete_spark_dynamics()
    
    plt.figure(figsize=(15, 15))
    plt.style.use('dark_background')
    
    for i, traj in enumerate(trajs):
        color = 'gold' if i % 2 == 0 else 'red'
        alpha = 0.6 if i % 2 == 0 else 0.2
        label = 'Spark (Healthy)' if i == 0 else ('Drift (Disease)' if i == 1 else "")
        
        plt.plot(traj.real, traj.imag, alpha=alpha, lw=0.7, color=color)
        # Mark final positions
        plt.scatter(traj.real[-1], traj.imag[-1], s=10, color=color, alpha=0.8)

    # The OMEGA Boundary (7.4)
    circle = plt.Circle((0, 0), OMEGA, color='cyan', fill=False, linestyle='--', alpha=0.5, label='OMEGA 7.4')
    plt.gca().add_patch(circle)
    
    plt.title("THE 128 TRAJECTORIES: SPARK VS BIFURCATION\n(Continuous Drift = Disease | Discrete Spark = Life)", fontsize=20, color='white')
    plt.xlabel("Real Axis (Truth)", fontsize=15)
    plt.ylabel("Imaginary Axis (Masking)", fontsize=15)
    plt.legend()
    plt.grid(True, alpha=0.05)
    
    plt.savefig("analysis_results/DISCRETE_SPARK_TRAJECTORIES_128.png", dpi=300, facecolor='black')
    
    print("\n[SUCCESS] Discrete Spark Map generated.")
    print("Yellow lines: Successful Spark (Quantized Homeostasis).")
    print("Red lines: Continuous Drift (Bifurcation / Disease).")
    print("Check: analysis_results/DISCRETE_SPARK_TRAJECTORIES_128.png")

if __name__ == "__main__":
    main()
