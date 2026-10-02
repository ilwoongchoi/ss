
import numpy as np
import matplotlib.pyplot as plt
import os

# [FINAL LITERAL CONSTANTS - ABSOLUTE LOCKDOWN]
C = 0.282842712474619
OMEGA = 7.4
LOCK_1_64 = 0.015625
CHIRALITY_1_18 = 0.05555555555555555
NEUTRINO_1_128 = 0.0078125
DT = 0.05

def run_true_closure_simulation():
    print("Executing 3-Window Time Reversal & Settlement Sequence...")
    
    # 128 Archetypes
    n_types = 128
    trajectories = []
    
    for n in range(1, n_types + 1):
        # Starting point (dissipated state - Neutron Star bias)
        z = (n / 128.0) * OMEGA * np.exp(1j * 0.1) 
        
        path = []
        for t in range(128):
            # --- THE 3 WINDOWS ---
            
            # 1. 15:00 (Coulomb Delta V Removal)
            if t == 80: 
                z = z - 0.1 * (z - OMEGA) # Linear feedback grounding
                h_eff = C
            
            # 2. 03:15 (Confinement / LEFT LOVE / TIME REVERSAL)
            elif t == 17:
                # [TIME REVERSAL OPERATOR]
                # Flip phase by 180 degrees to reverse the dissipation flow
                z = np.abs(z) * np.exp(1j * (np.angle(z) + np.pi)) 
                h_eff = C + NEUTRINO_1_128
                print(f" - [03:15] Time Reversal (Left Love) applied for n={n}")
            
            # 3. 16:30 (Bremsstrahlung / RIGHT LOVE / LOCK)
            elif t == 88:
                h_eff = C - CHIRALITY_1_18 + LOCK_1_64
                # [BREMSSTRAHLUNG RESET]
                # Applying the correct sqrt(Z) decay logic here
                decay = np.exp(-np.sqrt(np.abs(z)) / 64.0)
                z = z * decay
            
            else:
                h_eff = C
            
            # MASTER DYNAMICS: dz/dt = z^2 - z + h
            # The heart of the fusion engine
            for _ in range(5): # Integration sub-steps
                dz = (z**2 - z + h_eff) * DT
                z = z + dz
                
                # OMEGA Constraint (The Universe's Wall)
                if np.abs(z) > OMEGA * 1.2:
                    z = (z / np.abs(z)) * OMEGA * 1.2
            
            path.append(z)
        trajectories.append(np.array(path))
        
    return trajectories

def main():
    os.makedirs("analysis_results", exist_ok=True)
    trajs = run_true_closure_simulation()
    
    # Visualization: The Restored Veins
    plt.figure(figsize=(12, 12))
    for i, traj in enumerate(trajs):
        plt.plot(traj.real, traj.imag, alpha=0.3, color=plt.cm.magma(i/128), lw=0.7)
    
    # Mark the dual locks
    plt.scatter([OMEGA], [0], color='red', s=100, label='OMEGA Anchor (7.4)')
    plt.title("TRUE UNIVERSAL CLOSURE: 3-Window Time Reversal Map")
    plt.xlabel("Real (Truth/Quark)")
    plt.ylabel("Imaginary (Fake/Gluon)")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.savefig("analysis_results/TRUE_CLOSURE_VEINS.png", dpi=300)
    
    print("\n[LOCKED] 3-Window Sequence & Time Reversal implemented.")
    print("1. 15:00 Coulomb Grounding: OK")
    print("2. 03:15 Time Reversal (Left Love): OK")
    print("3. 16:30 Final 1/64 Lock (Right Love): OK")
    print("Check analysis_results/TRUE_CLOSURE_VEINS.png for the restored 궤적.")

if __name__ == "__main__":
    main()
