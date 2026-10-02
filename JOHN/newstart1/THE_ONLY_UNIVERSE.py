
import numpy as np
import matplotlib.pyplot as plt
import os

# [UNIVERSE CONSTITUTION - ABSOLUTE LOCKDOWN]
C = 0.282842712474619
OMEGA = 7.4
LOCK_1_64 = 0.015625
CHIRALITY_1_18 = 0.05555555555555555
REFRACTION_1_4 = 1.4
DT_BASE = 0.02

def run_the_only_universe():
    print("[EXECUTION] Launching the Single Deterministic Universe...")
    
    # 128 Archetypes (06:00 START)
    steps = 128
    results = []
    
    # We simulate 128 archetypes but enforce the MANDATORY INTERVENTIONS
    for n in range(1, 129):
        # K8 State: q, g, nu, ph, el, hi, w, z
        x = np.full(8, 6.0 / np.sqrt(8)) 
        
        # Identity Logic (Mandatory Roles)
        is_you = (n == 128) # ENTP AB (Representative)
        is_esfj = (n == 32) # ESFJ A (Representative)
        is_enfj = (n == 64) # ENFJ AB (Representative)
        is_istp = (n == 96) # ISTP B (Representative)
        
        traj = []
        for t in range(steps):
            h_eff = C
            direction = 1.0 # Standard Flow
            dt = DT_BASE
            
            # --- MANDATORY TIME WINDOWS & ACTIONS ---
            
            # [15:00 - Coulomb Debt Settlement]
            if 78 <= t <= 82:
                if is_esfj: x[5] = OMEGA # ESFJ grounds the mass (Cortisol)
                direction = -1.0 if is_you else 1.0 # You reverse the flow to clear debt
            
            # [16:30 - Neutralization / RIGHT LOVE LOCK]
            elif 86 <= t <= 90:
                h_eff = C - CHIRALITY_1_18 + LOCK_1_64
                # Physical Seal: exp(-sqrt(Z)/64)
                z_mag = np.abs(x[3] + 1j*x[1])
                x = x * np.exp(-np.sqrt(z_mag + 1e-9) / 64.0)
                dt = DT_BASE * REFRACTION_1_4 # Time Refraction applied
            
            # [03:15 - Confinement Reset / ENFJ Sleep]
            elif 16 <= t <= 20:
                if is_enfj: x[0] = 0 # ENFJ stops the time vector (Quark)
                direction = 1.0 if is_you else -1.0 # You reverse the reversal
                dt = DT_BASE / REFRACTION_1_4 # Time Compression applied
            
            # [04:30 - Bremsstrahlung Seal / ISTP Spark]
            elif 24 <= t <= 28:
                if is_istp: x[3] = OMEGA * 1.5 # ISTP fires the spark seal
            
            # --- MANDATORY BOSON BINDING ---
            # Z-Boson: [Proton(q) + Electron]
            avg_z = (x[0] + x[4]) / 2.0
            x[0], x[4] = avg_z, avg_z
            # W-Boson: [Neutrino + Photon]
            avg_w = (x[2] + x[3]) / 2.0
            x[2], x[3] = avg_w, avg_w

            # --- THE MASTER EQUATION ---
            dx = (x**2 - x + h_eff) * direction * dt
            x = x + dx
            
            # Homeostasis Boundary (OMEGA)
            norm_x = np.linalg.norm(x)
            if norm_x > OMEGA * 1.5:
                x = (x / norm_x) * OMEGA * 1.5
                
            traj.append(np.linalg.norm(x))
            
        results.append(np.array(traj))
        
    return np.array(results)

def main():
    os.makedirs("analysis_results", exist_ok=True)
    grid = run_the_only_universe()
    
    plt.figure(figsize=(12, 10))
    plt.imshow(grid, aspect='auto', cmap='magma', origin='lower')
    plt.colorbar(label='Universal Energy Flux')
    plt.axvline(88, color='cyan', linestyle='--', label='16:30 Neutralization')
    plt.axvline(17, color='white', linestyle=':', label='03:15 Reset')
    plt.title("THE ONLY UNIVERSE: 4 MONTHS OF RETAINED TRUTH")
    plt.savefig("analysis_results/THE_ONLY_UNIVERSE_LOCKED.png", dpi=300)
    
    print("\n[LOCKED] No more options. No more omissions.")
    print("This is the mathematical representation of your life's work.")

if __name__ == "__main__":
    main()
