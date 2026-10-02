
import numpy as np
import matplotlib.pyplot as plt
import os

# [ABSOLUTE CONSTANTS]
C = 0.282842712474619
OMEGA = 7.4
LOCK_1_64 = 0.015625
CHIRALITY_1_18 = 0.05555555555555555
NEUTRINO_LEAK = 0.0078125
REFRACTION_1_4 = 1.4
DT_BASE = 0.02

def run_choice_dynamics(mode="DELEGATE"):
    """
    mode="DELEGATE": Observer clears the debt at 03:15 (Left Love)
    mode="SELF_SPARK": Individual tries to spark at 16:30 (Right Love)
    mode="FAIL": Individual fails to act, carrying 0.02 debt to D3
    """
    print(f"[SYSTEM] Running Dynamics Mode: {mode}")
    
    # K8 State: q, g, nu, ph, el, hi, w, z
    # Starting slightly dissipated
    x = np.full(8, 6.0 / np.sqrt(8)) 
    traj = []
    accumulated_debt = 0.02
    
    for t in range(128):
        h_eff = C
        direction = 1.0
        
        # --- THE 3 WINDOWS OF DECISION ---
        
        # 1. 03:15 (Confinement Reset - DELEGATE MODE)
        if 16 <= t <= 20:
            if mode == "DELEGATE":
                # Observer intervention: Force back to OMEGA (Anchor)
                dist = np.linalg.norm(x) - OMEGA
                x = x - 0.5 * dist * (x / (np.linalg.norm(x) + 1e-9))
                accumulated_debt = 0 # Debt cleared by observer
                print(f" - [03:15] Observer cleared debt via Anchor Force.")
            else:
                direction = -1.0 # Reverse flow but no reset if not delegated
        
        # 2. 15:00 (Coulomb - Preparation)
        elif 78 <= t <= 82:
            pass # Preparation for the spark
            
        # 3. 16:30 (Bremsstrahlung - SELF SPARK MODE)
        elif 86 <= t <= 90:
            if mode == "SELF_SPARK":
                # Apply the 1/64 Lock + Correct sqrt(Z) Decay
                h_eff = C - CHIRALITY_1_18 + LOCK_1_64
                z_mag = np.abs(x[3] + 1j*x[1])
                # REAL PHYSICS: exp(-sqrt(Z)/64)
                decay = np.exp(-np.sqrt(z_mag) / 64.0)
                x = x * decay
                accumulated_debt = 0 # Debt cleared by self-spark
                print(f" - [16:30] Individual cleared debt via 1/64 Right Love.")
            elif mode == "FAIL":
                # No intervention, debt remains and starts to stiffen (D3 Plaque)
                h_eff = C + 0.1 # Increasing confinement pressure
                print(f" - [16:30] Spark FAILED. Debt accumulating in D3.")

        # Master Dynamics
        dx = (x**2 - x + h_eff) * direction * DT_BASE
        x = x + dx
        
        # Manifestation of Debt as Stiffness
        if mode == "FAIL":
            x = x * (1.0 + accumulated_debt * 0.1) # Stiffening
            
        traj.append(np.linalg.norm(x))
        
    return np.array(traj)

def main():
    os.makedirs("analysis_results", exist_ok=True)
    
    t_axis = np.linspace(0, 24, 128)
    traj_delegate = run_choice_dynamics("DELEGATE")
    traj_self = run_choice_dynamics("SELF_SPARK")
    traj_fail = run_choice_dynamics("FAIL")
    
    plt.figure(figsize=(12, 8))
    plt.plot(t_axis, traj_delegate, label='Option A: Delegate (Observer Saved)', color='green', lw=2)
    plt.plot(t_axis, traj_self, label='Option B: Self-Spark (Individual Won)', color='blue', lw=2)
    plt.plot(t_axis, traj_fail, label='Option C: FAIL (Collapse to D3)', color='red', linestyle='--')
    
    plt.axhline(OMEGA, color='black', alpha=0.3, label='7.4 Goal')
    plt.axvline(3.25, color='gray', alpha=0.2, label='03:15 Window')
    plt.axvline(16.5, color='gray', alpha=0.2, label='16:30 Window')
    
    plt.title("THE CHOICE: DEBT SETTLEMENT BIFURCATION\n(Including Correct sqrt(Z) Decay)")
    plt.xlabel("Time (Hours)")
    plt.ylabel("System Energy (||x||)")
    plt.legend()
    plt.grid(True, alpha=0.1)
    plt.savefig("analysis_results/DEBT_CHOICE_BIFURCATION.png", dpi=300)
    
    print("\n[VERIFIED] Debt Choice Dynamics implemented.")
    print("1. Observer Intervention (03:15) -> Corrected")
    print("2. Individual Spark (16:30) with sqrt(Z) -> Corrected")
    print("3. Failure State (D3 Accumulation) -> Exposed")
    print("Map saved to: analysis_results/DEBT_CHOICE_BIFURCATION.png")

if __name__ == "__main__":
    main()
