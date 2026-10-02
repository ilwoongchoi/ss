
import numpy as np
import matplotlib.pyplot as plt
import os

# [UNIVERSE CONSTITUTION: NO IMPORTS, NO ADDITIONS, ONLY PHASE CONTROL]
C = 0.282842712474619
OMEGA = 7.4
LOCK_1_64 = 0.015625
CHIRALITY_1_18 = 0.05555555555555555
REFRACTION_1_4 = 1.4
DT_BASE = 0.05

def run_sovereign_engine():
    print("[INIT] Launching 30-Node Reciprocal Phase Engine...")
    
    # 128 Archetypes
    n_types = 128
    trajectories = []
    
    for n in range(1, n_types + 1):
        # Initial state x0
        z = (n / 128.0) * OMEGA
        path = []
        
        for t in range(128):
            # --- THE SOVEREIGN PHASE CONTROL (Your Intent) ---
            
            # 1. DAY PHASE (13:30 - 15:15, 105 mins)
            # Population: Forward (28 Nodes) | You: REVERSE (30 Nodes)
            if 72 <= t <= 86: 
                direction = -1.0 # Your Reverse Flow to cancel debt
                h_eff = C
                dt = DT_BASE * REFRACTION_1_4 # Time stretching
            
            # 2. NEUTRALIZATION (16:30, The 1-Phase Grounding)
            # The Rape of Twilight: 1/64 Lock
            elif t == 88:
                direction = 0.0 # Moment of stillness/grounding
                h_eff = C - CHIRALITY_1_18 + LOCK_1_64
                dt = DT_BASE
                # Apply Skeletal Neutralization directly to the state
                z = z * np.exp(-np.sqrt(np.abs(z)) / 64.0) 
            
            # 3. NIGHT PHASE (03:00 - 04:30, 105 mins)
            # Population: Reverse (30 Nodes) | You: FORWARD (28 Nodes, No Muscle)
            elif 16 <= t <= 30:
                direction = 1.0 # Your Forward Flow to reset stasis
                h_eff = C
                dt = DT_BASE / REFRACTION_1_4 # Time compression for discharge
            
            else:
                direction = 1.0 # Normal progression
                h_eff = C
                dt = DT_BASE

            # MASTER DYNAMICS: dz/dt = (z^2 - z + h) * Direction
            # The direction flips the entire universe's causality
            dz = (z**2 - z + h_eff) * direction * dt
            z = z + dz
            
            # Homeostasis Boundary
            if np.abs(z) > OMEGA * 1.5:
                z = (z / np.abs(z)) * OMEGA * 1.5
                
            path.append(z)
        trajectories.append(np.array(path))
        
    return trajectories

def main():
    os.makedirs("analysis_results", exist_ok=True)
    trajs = run_sovereign_engine()
    
    # Render the 128 Veins of Reciprocity
    plt.figure(figsize=(12, 12))
    for i, traj in enumerate(trajs):
        plt.plot(traj.real, traj.imag, alpha=0.4, lw=0.8, color=plt.cm.coolwarm(i/128))
    
    plt.scatter([OMEGA], [0], color='green', s=100, label='7.4 Center')
    plt.title("THE 128 VEINS OF RECIPROCITY: 30-NODE PHASE CONTROL")
    plt.xlabel("Real Axis (Time/Truth)")
    plt.ylabel("Imaginary Axis (Phase/Deception)")
    plt.legend()
    plt.grid(True, alpha=0.1)
    plt.savefig("analysis_results/SOVEREIGN_30_NODE_VEINS.png", dpi=300)
    
    print("\n[LOCKED] 30-Node Directional Switching retained and executed.")
    print(" - Day: Reverse Flow (30 Nodes) applied.")
    print(" - Night: Forward Flow (28 Nodes) applied.")
    print(" - 16:30: 1/64 Neutralization applied.")
    print("Final visualization: analysis_results/SOVEREIGN_30_NODE_VEINS.png")

if __name__ == "__main__":
    main()
