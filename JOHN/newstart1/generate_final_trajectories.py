
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# [ABSOLUTE UNIVERSE CONSTANTS - HARDCODED]
C = 0.282842712474619
OMEGA = 7.4
LOCK_1_64 = 0.015625
CHIRALITY_1_18 = 0.05555555555555555
NEUTRINO_LEAK = 0.0078125
REFRACTION_1_4 = 1.4
DT = 0.01 # Ultra-high resolution for line continuity

def generate_128_trajectories():
    print("[SYSTEM] Extracting 128 Individual Life Trajectories (The Veins)...")
    
    # Load seeds (3.8 - 6.4)
    path = "128_GRID_MASTER_CALC.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            seeds = json.load(f)
    else:
        seeds = {f"Type_{i}": {"omega": 3.8 + i*0.02} for i in range(128)}

    trajectories = []
    
    for i, (name, data) in enumerate(seeds.items()):
        val = data.get("omega", 7.4)
        # Each archetype starts at a unique phase point
        z = (val / OMEGA) * np.exp(1j * (i * 2 * np.pi / 128.0))
        
        path_z = []
        is_you = (i == 127) # ENTP AB
        
        # 128 windows * 10 sub-steps = 1280 integration points
        for t_step in range(128):
            # --- DYNAMIC PHASE CONTROL ---
            direction = 1.0
            scale = 1.0
            h_eff = C
            discharge = 0.0
            
            # 1. 03:15 Reset (Step 17)
            if 16 <= t_step <= 18:
                if is_you: direction = 1.0
                else: direction = -1.0
                scale = 1.0 / REFRACTION_1_4
            
            # 2. 16:30 Neutralization (Step 88)
            elif 87 <= t_step <= 89:
                h_eff = C - CHIRALITY_1_18 + LOCK_1_64
                # exp(-sqrt(Z)/64)
                z = z * np.exp(-np.sqrt(np.abs(z) + 1e-9) / 64.0)
                scale = REFRACTION_1_4
            
            # 3. 18:00-21:00 Discharge (Step 96-112)
            elif 96 <= t_step <= 112:
                discharge = 0.2
            
            # Sub-step integration for smoothness
            for _ in range(10):
                dz = (z**2 - z + h_eff) * direction * scale * DT
                z = z + dz - (z * discharge * DT)
                
                # Saturation Clamping
                mag = np.abs(z)
                if mag > OMEGA * 1.5: z = (z / mag) * OMEGA * 1.5
            
            path_z.append(z)
        trajectories.append(np.array(path_z))
        
    return trajectories

def main():
    os.makedirs("analysis_results", exist_ok=True)
    trajs = generate_128_trajectories()
    
    # 1. Complex Plane Trajectories (Real vs Imaginary)
    plt.figure(figsize=(12, 12))
    plt.axhline(0, color='black', lw=1, alpha=0.3)
    plt.axvline(0, color='black', lw=1, alpha=0.3)
    
    for i, traj in enumerate(trajs):
        plt.plot(traj.real, traj.imag, alpha=0.5, lw=0.6, color=plt.cm.turbo(i/128))
        
    # Mark the OMEGA circle
    circle = plt.Circle((0, 0), OMEGA, color='green', fill=False, linestyle='--', alpha=0.4, label='OMEGA 7.4')
    plt.gca().add_patch(circle)
    
    plt.title("THE 128 TRAJECTORIES: INDIVIDUAL LIFE VEINS (COMPLEX PLANE)")
    plt.xlabel("Quark (Real - Truth)")
    plt.ylabel("Gluon (Imaginary - Deception)")
    plt.grid(True, alpha=0.1)
    plt.savefig("analysis_results/THE_128_TRAJECTORIES_COMPLEX.png", dpi=300)
    
    # 2. Temporal Magnitude Trajectories (Time vs Magnitude)
    plt.figure(figsize=(14, 8))
    t_axis = np.linspace(0, 24, 128)
    for i, traj in enumerate(trajs):
        plt.plot(t_axis, np.abs(traj), alpha=0.4, lw=0.5, color=plt.cm.turbo(i/128))
        
    plt.axvline(16.5, color='cyan', linestyle='--', label='16:30 Neutralization')
    plt.axvspan(18, 21, color='green', alpha=0.1, label='6-9 PM Discharge')
    plt.axhline(OMEGA, color='red', linestyle='-', alpha=0.3, label='7.4 Goal')
    
    plt.title("128 ARCHETYPE ENERGY EVOLUTION (TIME AXIS)")
    plt.xlabel("Time (Hours)")
    plt.ylabel("Energy Intensity (|z|)")
    plt.legend(loc='upper right')
    plt.savefig("analysis_results/THE_128_TRAJECTORIES_TIME.png", dpi=300)
    
    print("\n[SUCCESS] 128 Continuous Trajectories extracted.")
    print("Files created:")
    print(" - analysis_results/THE_128_TRAJECTORIES_COMPLEX.png (The Veins)")
    print(" - analysis_results/THE_128_TRAJECTORIES_TIME.png (The Flow)")

if __name__ == "__main__":
    main()
