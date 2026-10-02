
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# [THE ABSOLUTE MATHEMATICAL CODE]
C = 0.282842712474619
OMEGA = 7.4
LOCK_1_64 = 0.015625
CHIRALITY_1_18 = 0.05555555555555555
NEUTRINO_LEAK = 0.0078125
REFRACTION_1_4 = 1.4
DT_BASE = 0.01 

def generate_128_locked_grid():
    print("[SYSTEM] Compiling Universal 128 Grid with 8-Phase Discharge Dynamics...")
    
    # Load Seeds (3.8 - 6.4 range)
    path = "128_GRID_MASTER_CALC.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            seeds = json.load(f)
    else:
        seeds = {f"Type_{i}": {"omega": 3.8 + i*0.02} for i in range(128)}

    grid = np.zeros((128, 128)) # Archetype x Time
    
    for i, (name, data) in enumerate(seeds.items()):
        # Initialize K8 State
        val = data.get("omega", 7.4)
        x = np.full(8, val / np.sqrt(8))
        
        # Identity Flags
        is_you = (i == 127) # ENTP AB
        is_enfp_b = (i == 110)
        
        for t in range(128):
            # --- PHASE DYNAMICS ---
            direction = 1.0
            scale = 1.0
            h_eff = C
            discharge = 0.0
            
            # 1. Day Reversal (13:30 - 15:15)
            if 72 <= t <= 82:
                if is_you: direction = -1.0 # Your counter-flow
                scale = REFRACTION_1_4
            
            # 2. Neutralization (16:30)
            elif 86 <= t <= 90:
                h_eff = C - CHIRALITY_1_18 + LOCK_1_64
                # Physical Seal: exp(-sqrt(Z)/64)
                z_mag = np.abs(x[3] + 1j*x[1])
                x = x * np.exp(-np.sqrt(z_mag + 1e-9) / 64.0)
            
            # 3. Discharge Window (18:00 - 21:00) - AUTOMATIC
            elif 96 <= t <= 112:
                discharge = 0.15 # Entropy Sink active
                if is_enfp_b: discharge = 0.3 # ENFP B-type extra discharge
            
            # 4. Night Reset (03:15)
            elif 16 <= t <= 20:
                if is_you: direction = 1.0 # Re-reversal
                else: direction = -1.0
                scale = 1.0 / REFRACTION_1_4

            # --- MASTER EQUATION EXECUTION ---
            # dx/dt = (x^2 - x + h - delta) * direction * scale - discharge
            # We treat 'delta' as part of the neutralization step for precision
            dx = ((x**2 - x + h_eff) * direction * scale - (x * discharge)) * DT_BASE
            x = x + dx
            
            # Homeostasis Boundary
            norm_x = np.linalg.norm(x)
            if norm_x > 15.0: x = (x / norm_x) * 15.0
            
            grid[i, t] = norm_x

    return grid

def main():
    os.makedirs("analysis_results", exist_ok=True)
    final_field = generate_128_locked_grid()
    
    # Render the 128 Grid of Truth
    plt.figure(figsize=(14, 10))
    plt.imshow(final_field, aspect='auto', cmap='magma', origin='lower')
    plt.colorbar(label='Sovereign Intensity (||x||)')
    
    # Anchors
    plt.axvline(88, color='cyan', linestyle='--', label='16:30 Lock')
    plt.axvspan(96, 112, color='green', alpha=0.15, label='6-9 PM Discharge')
    plt.axvline(17, color='white', linestyle=':', label='03:15 Reset')
    
    plt.title("THE FINAL 128 GRID: 8-PHASE RECURSIVE CLOSURE")
    plt.xlabel("Time Dimension (24h Loop)")
    plt.ylabel("Archetype Dimension (1-128)")
    plt.legend()
    
    plt.savefig("analysis_results/THE_REAL_128_GRID.png", dpi=300)
    print("\n[SUCCESS] The 128 Grid has been extracted based on the Master Equation.")
    print("Equation: dx/dt = (x^2 - x + h) * Dir * Scale - Discharge")
    print("Check: analysis_results/THE_REAL_128_GRID.png")

if __name__ == "__main__":
    main()
