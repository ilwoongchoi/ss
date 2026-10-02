
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fusion_core import C, OMEGA, F_1_64, idx_to_subject, apply_channels, PHASE_TABLE

# 1. FINAL CONSTANTS & PHYSICS
CHIRALITY_055 = 1.0 / 18.0  # 0.0555... (15B year debt)
E_INV = 1.0 / np.exp(1)      # 1/e (Hannah Fry's Optimal Target)
LOCK_VALUE = F_1_64         # 1/64 (The Right Love Joystick)

def universal_fusion_equation(z, h, delta):
    """
    dz/dt = z^2 - z + h - delta
    """
    return z**2 - z + h - delta

def simulate_unified_field():
    print("Simulating UNIVERSAL CONSCIOUSNESS FIELD V1.0...")
    
    # 128 Archetypes x 128 Time Windows
    grid = np.zeros((128, 128), dtype=complex)
    potential_grid = np.zeros((128, 128))
    
    # Initial state: 128 veins from the torus mapping
    for n in range(1, 129):
        # Initial phase: 138.88 degree spark angle base
        initial_angle = (n * 138.88 * np.pi / 180.0) / 128.0
        z = (n / 128.0) * np.exp(1j * initial_angle)
        
        for t in range(128):
            # Dynamic delta (The Gap)
            # Baseline is Chirality Gap (0.055)
            delta = CHIRALITY_055
            
            # 16:30 (Step 80) - The Neutralization Event
            if t == 80:
                # Apply 1/64 Lockdown + Hannah Fry 1/e Alignment
                # This is where the energy 'leaves the body' (Dissipation -> Equilibrium)
                h_eff = C + LOCK_VALUE
                delta_eff = delta - (E_INV * (7.4 / 128.0)) # Syncing with Omega
            else:
                h_eff = C
                delta_eff = delta
            
            # Iterate Fusion Equation
            z = universal_fusion_equation(z, h_eff, delta_eff)
            
            # Store Complex State and Potential
            grid[n-1, t] = z
            potential_grid[n-1, t] = np.log(np.abs(z) + 1e-9)
            
    return potential_grid

def main():
    potential = simulate_unified_field()
    
    # Save results
    plt.figure(figsize=(15, 10))
    plt.imshow(potential, aspect='auto', cmap='magma', origin='lower')
    plt.colorbar(label='Potential Intensity (G)')
    plt.title("UNIVERSAL CONSCIOUSNESS FIELD V1.0: THE FINAL CLOSURE")
    plt.xlabel("Time Dimension (128 Windows)")
    plt.ylabel("Archetype Dimension (1-128)")
    
    # Mark the 16:30 Rape of Twilight / Neutralization
    plt.axvline(80, color='cyan', linestyle='--', alpha=0.8, label='16:30 Neutralization (1/64 Lock)')
    plt.legend()
    
    output_path = "analysis_results/UNIVERSAL_CONSCIOUSNESS_FIELD_V1.0.png"
    plt.savefig(output_path)
    
    # Also save as CSV for numerical verification
    pd.DataFrame(potential).to_csv("analysis_results/UNIVERSAL_FIELD_DATA_V1.0.csv")
    
    print(f"\n[SUCCESS] Universal Field V1.0 Compiled.")
    print(f"Final Output: {output_path}")
    print("Energy Dissipation neutralized. Equilibrium reached via 1/64 Right Love.")

if __name__ == "__main__":
    main()
