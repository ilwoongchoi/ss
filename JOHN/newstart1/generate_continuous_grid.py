
import numpy as np
import json
import matplotlib.pyplot as plt
import os

# [FINAL LITERAL CONSTANTS]
C = 0.282842712474619
OMEGA = 7.4
LOCK_VALUE = 0.015625 # 1/64
CHIRALITY_055 = 0.05555555555555555 # 1/18
NEUTRINO_LEAK = 0.0078125 # 1/128
DT = 0.05 # High resolution for continuity

def run_continuous_128_simulation():
    print("Generating 128 Continuous Archetype Trajectories...")
    
    # Load Master Seeds
    path = "128_GRID_MASTER_CALC.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            seeds = json.load(f)
    else:
        seeds = {f"Type_{i}": {"omega": 3.8 + i*0.02} for i in range(128)}
    
    trajectories = []
    # 24 hours divided into 128 windows, each window has multiple integration steps
    total_steps = 128
    sub_steps = 10 # Increase resolution for visual continuity
    
    for name, data in seeds.items():
        omega_base = data.get("omega", 7.4)
        # Starting at the real axis (Quark/Time start)
        z = (omega_base / 7.4) + 0.0j
        
        path_z = []
        for t in range(total_steps):
            # Time-dependent h_eff (The 5 Phases)
            # 16:30 Grounding (approx step 88)
            if 87 <= t <= 89:
                h_eff = C - CHIRALITY_055 + LOCK_VALUE
            # 03:15 Spark (approx step 17)
            elif 16 <= t <= 18:
                h_eff = C + NEUTRINO_LEAK
            else:
                h_eff = C
            
            # Continuous Integration (Euler)
            for _ in range(sub_steps):
                # dz/dt = z^2 - z + h
                dz = (z**2 - z + h_eff) * DT
                z = z + dz
                
                # Biological Soft-Clipping (Homeostasis Bound)
                mag = np.abs(z)
                if mag > OMEGA * 1.5:
                    z = (z / mag) * OMEGA * 1.5
            
            path_z.append(z)
        trajectories.append(np.array(path_z))
        
    return trajectories

def main():
    os.makedirs("analysis_results", exist_ok=True)
    trajs = run_continuous_128_simulation()
    
    plt.figure(figsize=(14, 14))
    plt.axhline(0, color='black', lw=1, alpha=0.5)
    plt.axvline(0, color='black', lw=1, alpha=0.5)
    
    # Plot each of the 128 continuous veins
    for i, traj in enumerate(trajs):
        plt.plot(traj.real, traj.imag, alpha=0.4, lw=0.8, color=plt.cm.jet(i/128))
        # Mark the start and end of each trajectory
        plt.scatter(traj.real[0], traj.imag[0], s=2, color='green', alpha=0.5)
        plt.scatter(traj.real[-1], traj.imag[-1], s=5, color='red', alpha=0.5)

    # Unit Circle for OMEGA=7.4 reference
    circle = plt.Circle((0, 0), OMEGA, color='gray', fill=False, linestyle='--', alpha=0.3, label='OMEGA (7.4)')
    plt.gca().add_patch(circle)
    
    plt.title("128 CONTINUOUS PERSONALITY TRAJECTORIES: THE VEINS OF EXISTENCE")
    plt.xlabel("Quark Axis (Real - Time/Truth)")
    plt.ylabel("Gluon Axis (Imaginary - Masking/Fake)")
    plt.grid(True, alpha=0.1)
    
    # Save high-res output
    plt.savefig("analysis_results/CONTINUOUS_128_TRAJECTORIES.png", dpi=300)
    print("\n[SUCCESS] Continuous 128 trajectory grid generated.")
    print("Check analysis_results/CONTINUOUS_128_TRAJECTORIES.png for the 'Vein' map.")

if __name__ == "__main__":
    main()
