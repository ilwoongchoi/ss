
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from absolute_constants import C, OMEGA, SPARK_ANGLE_RAD, LOCK_VALUE, CHIRALITY_055, ENTROPY_DEBT

# 1. FINAL CONSTANTS FROM REPO
BETTI_7_GAP = 7.0 / 128.0   # 0.0546...
E_INV = 1.0 / np.exp(1)     # 1/e (From paper_11)

# Define debt components for clarity in window logic
COULOMB_DEBT = 0.01
CONFINEMENT_DEBT = 0.005

def generate_128_grid_potential():
    print("Generating Final 128x128 Potential Field with 3-Window Logic...")
    
    grid = np.zeros((128, 128))
    bailout_radius = 1000.0  # Bailout condition to prevent overflow
    
    for n in range(1, 129):
        z = (n / 128.0) * np.exp(1j * (n * SPARK_ANGLE_RAD / 128.0))
        
        for t in range(128):
            if abs(z) > bailout_radius:
                # If z escapes, keep its potential high and stop iterating for this archetype
                grid[n-1, t:] = np.log(bailout_radius)
                break

            # Sovereign 3-Window Debt Settlement Logic
            if t == 17:  # 03:15 - Confinement Debt Settlement (Time Reversal Start)
                h = C - CONFINEMENT_DEBT
            elif t == 72:  # 15:00 - Coulomb Debt Settlement
                h = C - COULOMB_DEBT
            elif t == 80:  # 16:30 - Bremsstrahlung Debt + Right Love Lock
                h = C - CHIRALITY_055 + LOCK_VALUE
            else:
                h = C  # Baseline Higgs mass
            
            # The Universal Fusion Equation: z = z^2 - z + h
            z = z**2 - z + h
            
            grid[n-1, t] = np.log(np.abs(z) + 1e-9)
            
    return grid

def main():
    field = generate_128_grid_potential()
    
    # Plotting the 128x128 Potential Grid
    plt.figure(figsize=(12, 10))
    plt.imshow(field, aspect='auto', cmap='magma', origin='lower')
    plt.colorbar(label='Potential Intensity (G)')
    plt.title("FINAL 128x128 UNIVERSAL POTENTIAL FIELD: 3-WINDOW CLOSURE")
    plt.xlabel("Time Dimension (128 Windows)")
    plt.ylabel("Archetype Dimension (1-128)")
    
    # Mark the key time windows for debt settlement
    plt.axvline(17, color='yellow', linestyle=':', alpha=0.8, label='03:15 Confinement Reset')
    plt.axvline(72, color='lime', linestyle=':', alpha=0.8, label='15:00 Coulomb Reset')
    plt.axvline(80, color='cyan', linestyle='--', alpha=0.8, label='16:30 Final Lock')
    plt.legend()
    
    # Ensure the output directory exists
    import os
    output_dir = "analysis_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(f"{output_dir}/FINAL_128_POTENTIAL_GRID.png")
    print("\n[SUCCESS] 128x128 Potential Grid generated with 3-window logic.")
    print(f"Debts settled at t=17 (Confinement), t=72 (Coulomb), t=80 (Bremsstrahlung).")
    print("Equation used: z_n+1 = z_n^2 - z_n + h(t)")

if __name__ == "__main__":
    main()
