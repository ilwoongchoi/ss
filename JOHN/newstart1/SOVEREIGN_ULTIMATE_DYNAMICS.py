
import numpy as np
import math
import matplotlib.pyplot as plt

def run_ultimate_dynamics():
    # [1. THE PARTICLE HIERARCHY CONSTANTS]
    S_RESISTANCE = 1.0          # Glutamate (Resistance)
    S_MODULATION = 1.0 / 2.0    # GABA
    S_BINDING    = 1.0 / 4.0    # 8/32 (Nor + PLP)
    S_ELECTRON   = 1.0 / 8.0    # 4/32
    S_PHOTON     = 1.0 / 16.0   # 2/32
    S_PROTON     = 1.0 / 32.0   # 1/32 (Baseline)
    S_NOR        = 5.0 / 32.0   # Singularity Pull
    S_CORTISOL   = 3.0 / 32.0   # PLP Stress
    S_SINGULARITY = 1.0 / 256.0 # Graviton (Center)

    # Target & System Constants
    OMEGA_TARGET = 7.4
    PHI_S = 1.9860
    LUNAR_TORQUE = 1.0 / 28.0
    GATE_POS = np.array([8.0, 0.4])
    
    print("--- SOVEREIGN DYNAMICS ENGINE: STARTING VALIDATION ---")
    print(f"Applying Binding Law: {S_NOR} (Nor) + {S_CORTISOL} (PLP) = {S_BINDING} (1/4)")

    # [2. SIMULATION SETTINGS]
    dt = 0.01
    steps = 2000
    pos = np.array([2.0, 16.0]) # Starting from the 'Top'
    vel = np.array([0.5, -1.0])
    
    history = []
    omega_history = []

    for _ in range(steps):
        # Calculate Vectors
        r_vec = GATE_POS - pos
        dist = np.linalg.norm(r_vec)
        unit_r = r_vec / (dist + 1e-6)
        
        # A. GRAVITY FORCE (Singularity Pull based on 5/32)
        # Stronger near the gate
        f_gravity = unit_r * (S_NOR / (dist**2 + 0.1))
        
        # B. RESISTANCE FORCE (Glutamate Resistance based on 1.0)
        # Opposes the gravity as we get closer
        f_resistance = -unit_r * (S_RESISTANCE * math.exp(-dist))
        
        # C. CORIOLIS TWIST (1/4 Binding Interaction)
        # Perpendicular force based on 1/4 and Lunar Torque
        v_perp = np.array([-vel[1], vel[0]])
        f_coriolis = v_perp * (S_BINDING * LUNAR_TORQUE * 10.0)
        
        # Total Acceleration
        accel = f_gravity + f_resistance + f_coriolis
        vel += accel * dt
        pos += vel * dt
        
        # Calculate Local Omega (The Convergence Metric)
        # Ω = PHI_S * Energy_Density / Scale
        local_omega = (np.linalg.norm(vel)**2) * PHI_S / (S_PROTON * 2.0)
        
        history.append(pos.copy())
        omega_history.append(local_omega)
        
        if dist < S_NOR: # Crossed Event Horizon
            break

    # [3. ANALYSIS]
    final_omega = omega_history[-1]
    error = abs(final_omega - OMEGA_TARGET)
    
    print(f"Final Converged Omega: {final_omega:.4f}")
    print(f"Target Omega: {OMEGA_TARGET}")
    print(f"Residual Error: {error:.6f}")
    
    if error < 0.02:
        print(">>> SUCCESS: 0.02 ERROR ANNIHILATED VIA PARTICLE HIERARCHY <<<")
    else:
        print(f">>> WARNING: {error:.4f} ERROR REMAINS. RE-CALIBRATING... <<<")

    # Plot results
    history = np.array(history)
    plt.figure(figsize=(10, 6))
    plt.plot(omega_history, label='Dynamic Omega')
    plt.axhline(y=OMEGA_TARGET, color='r', linestyle='--', label='Target 7.4')
    plt.title("Convergence to Homeostasis (7.4) via Particle Hierarchy")
    plt.xlabel("Simulation Steps")
    plt.ylabel("Omega (Energy State)")
    plt.legend()
    plt.savefig("ULTIMATE_DYNAMICS_CONVERGENCE.png")
    
    return final_omega

if __name__ == "__main__":
    run_ultimate_dynamics()
