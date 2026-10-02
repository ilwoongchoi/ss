
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# 1. ABSOLUTE CONSTANTS (Literal - No Imports)
C = 0.282842712474619 # sqrt(2)/5
C2 = 0.08
OMEGA = 7.4
LOCK_1_64 = 0.015625
CHIRALITY_1_18 = 0.05555555555555555
NEUTRINO_1_128 = 0.0078125
REFRACTION_1_4 = 1.4
SPARK_138_88 = 2.4239 # rad
DT_BASE = 0.02 # Higher resolution

def run_final_lockdown_engine():
    print("[SYSTEM] Executing Final 30-Node Universal Geometry Lockdown...")
    
    # Load Archetype Seeds
    path = "128_GRID_MASTER_CALC.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            seeds = json.load(f)
    else:
        seeds = {f"Type_{i}": {"omega": 3.8 + i*0.02} for i in range(128)}

    results = []
    
    for i, (name, data) in enumerate(seeds.items()):
        # Initialize K8 State (x8)
        # q, g, nu, ph, el, hi, w, z
        omega_i = data.get("omega", 7.4)
        x = np.full(8, omega_i / np.sqrt(8)) 
        
        # Identity Logic
        is_you = "ENTP_AB" in name
        is_esfj = "ESFJ_A" in name
        is_istp = "ISTP_B" in name
        is_enfj = "ENFJ_AB" in name
        
        traj = []
        for t in range(128):
            # --- 1. TIME & PHASE MAPPING ---
            hour = (t / 128.0) * 24.0
            
            # --- 2. THE 3 WINDOWS & ARCHETYPE INTERVENTION ---
            h_eff = C
            direction = 1.0
            dt = DT_BASE
            
            # [15:00 - Coulomb Debt / ESFJ Intervention]
            if 78 <= t <= 82: # ~15:00
                if is_esfj: 
                    x[5] = OMEGA # ESFJ usage of Right Cortisol (Higgs)
                direction = -1.0 if is_you else 1.0
            
            # [16:30 - Neutralization / RIGHT LOVE LOCK]
            elif 86 <= t <= 90: # ~16:30 (Window 8 Start)
                h_eff = C - CHIRALITY_1_18 + LOCK_1_64
                # Apply Bremsstrahlung Correction: exp(-sqrt(Z)/64)
                z_val = np.abs(x[3] + 1j*x[1]) # Photon-Gluon complex
                decay = np.exp(-np.sqrt(z_val + 1e-9) / 64.0)
                x = x * decay
                dt = DT_BASE * REFRACTION_1_4 # Time dilation
            
            # [03:15 - Confinement / LEFT LOVE RESET]
            elif 16 <= t <= 20: # ~03:15 (Reverse Spark)
                if is_enfj:
                    x[0] = 0 # ENFJ Sleep (Stop 5HT1A/Quark)
                direction = 1.0 if is_you else -1.0 # Reverse Reversal
                dt = DT_BASE / REFRACTION_1_4 # Time compression
            
            # [04:30 - Bremsstrahlung Seal / ISTP Spark]
            elif 24 <= t <= 28: # ~04:30
                if is_istp:
                    x[3] = OMEGA * 1.5 # ISTP Spark Ignition
            
            # --- 3. BOSON BINDING DYNAMICS ---
            # Z-Boson: [Proton + Electron] Binding
            # W-Boson: [Neutrino + Photon] Binding
            # Simplified binding force: delta_a = delta_b
            avg_z = (x[0] + x[4]) / 2.0 # Proton(q) + Electron
            x[0], x[4] = avg_z, avg_z
            
            avg_w = (x[2] + x[3]) / 2.0 # Neutrino + Photon
            x[2], x[3] = avg_w, avg_w

            # --- 4. MASTER EQUATION: dx/dt = (x^2 - x + h) * Dir ---
            dx = (x**2 - x + h_eff) * direction * dt
            x = x + dx
            
            # Homeostasis Clamping
            norm_x = np.linalg.norm(x)
            if norm_x > OMEGA * 2.0:
                x = (x / norm_x) * OMEGA * 2.0
                
            traj.append(np.linalg.norm(x))
            
        results.append(np.array(traj))
        
    return np.array(results)

def main():
    os.makedirs("analysis_results", exist_ok=True)
    grid = run_final_lockdown_engine()
    
    # Final 128x128 Trajectory Grid Visualization
    plt.figure(figsize=(12, 10))
    plt.imshow(grid, aspect='auto', cmap='magma', origin='lower')
    plt.colorbar(label='Energy Intensity (||x||)')
    
    # Lines of Truth
    plt.axvline(88, color='cyan', linestyle='--', label='16:30 Neutralization')
    plt.axvline(17, color='white', linestyle=':', label='03:15 Reset')
    
    plt.title("FINAL UNIVERSAL LOCKDOWN: 128 ARCHETYPE TRAJECTORY GRID")
    plt.xlabel("Time (128 Windows / 24h)")
    plt.ylabel("Archetype Index (1-128)")
    plt.legend()
    plt.savefig("analysis_results/FINAL_UNIVERSAL_LOCKDOWN_GRID.png", dpi=300)
    
    print("\n[SUCCESS] Universal Geometry LOCKED and SEALED.")
    print("1. sqrt(Z) Correction: APPLIED")
    print("2. Boson Binding (Z, W): APPLIED")
    print("3. Time Refraction (1.4): APPLIED")
    print("4. Multi-Archetype Intervention: EXECUTED")
    print("Final Map: analysis_results/FINAL_UNIVERSAL_LOCKDOWN_GRID.png")

if __name__ == "__main__":
    main()
