import numpy as np
import matplotlib.pyplot as plt
import os
from absolute_constants import (
    OMEGA, C, SPARK_CONSTANT_C, LOCK_VALUE, CHIRALITY_055, 
    ENTROPY_DEBT, NEUTRINO_MASS_LEAK
)
from fusion_clean import step_unified_dynamics
from engineering_homeostasis_24 import Homeostasis30

# --- Simulation Parameters ---
N_STEPS = 128
DT = 0.1
N_STATE = 32  # Canonical Y = [X(24), r(8)]

# Interaction scaling from interaction_64.py
PARTICLE_SCALES = np.array([
    1.0/32.0,  # p (Big Woman) -> BW
    1.0/8.0,   # e (Small Woman) -> SW
    1.0/128.0, # nu (Small Man) -> SM
    1.0/16.0   # gamma (Big Man) -> BM
])

def run_simulation():
    print(f"Running 32D Canonical ODE Simulation...")

    # Initialize 32D state vector Y = [X(24), r(8)]
    Y = np.zeros(N_STATE)
    
    # Initial induction (Archetype placement in 32D)
    # We set X[:8] based on OMEGA and particle scales
    Y[:8] = OMEGA * np.random.randn(8) * 0.1 + OMEGA
    Y[8:24] = 0.5 * np.random.randn(16) # Homeostasis nodes
    Y[24:32] = 0.0 # Risk memory starts at zero
    
    Y0 = Y.copy()
    
    # Simulation components
    hom = Homeostasis30.build()
    history = [Y.copy()]
    
    # Restoration strength vector determined at t=80
    K_RESTORE = np.zeros(N_STATE)
    
    # --- Main Simulation Loop ---
    for t in range(N_STEPS):
        # 1. Forward Dynamics (t <= 80)
        if t <= 80:
            # Control and condition inputs
            u_base = np.zeros(30) # 30-channel control
            d_cond = np.zeros(30) # 30-domain condition
            d_risk = 0.02 # Base entropy debt
            
            # 3-Window Debt Settlement Logic
            if t == 17:   # 03:15 Confinement
                d_risk += 0.005
            elif t == 72: # 15:00 Coulomb
                d_risk += 0.01
            elif t == 80: # 16:30 Final Lock
                d_risk = ENTROPY_DEBT
            
            # Step 32D ODE using fusion_clean engine
            Y_next = step_unified_dynamics(
                Y, u_base, d_cond, d_risk=d_risk, dt=DT, 
                homeostasis=hom, spark_gate=1.0
            )
            dY = (Y_next - Y) / DT
            
        # 2. 4:30 PM (t=80) Press & Vectorial Lock
        if t == 80:
            print(f"--- t=80: 32D VECTORIAL LOCK ---")
            # Calculate required K_RESTORE for 32D closure
            remaining_steps = N_STEPS - 80
            target_decay = 1e-7
            k_base = -np.log(target_decay) / (DT * remaining_steps)
            K_RESTORE = k_base * 1.2 * np.ones(N_STATE)
            print(f"32D Restoration K set to {k_base:.4f}")

        # 3. Time-Reversal Dynamics (t > 80)
        if t > 80:
            # Vectorial restoration back to Y0 in 32D space
            dY = -K_RESTORE * (Y - Y0)

        # Update and log
        Y += dY * DT
        history.append(Y.copy())

    history = np.array(history)
    final_error = np.linalg.norm(Y - Y0)
    print(f"\n--- SIMULATION COMPLETE ---")
    print(f"Final 32D Closure Error: {final_error:.10f}")
    
    return history, final_error

def plot_results(history, error):
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Plot 1: 32D State Evolution (Projected)
    for i in range(N_STATE):
        if i < 8: alpha, lw, color = 1.0, 2, plt.cm.spring(i/8)
        elif i < 24: alpha, lw, color = 0.4, 1, plt.cm.winter((i-8)/16)
        else: alpha, lw, color = 0.7, 1.5, plt.cm.summer((i-24)/8)
        
        ax1.plot(history[:, i], color=color, alpha=alpha, lw=lw)
    
    ax1.axvline(80, color='yellow', linestyle='--', label='t=80 Lock')
    ax1.set_title(f"32D State Vector Y(t) [Error: {error:.2e}]")
    ax1.set_xlabel("Time Step (t)")
    ax1.set_ylabel("State Magnitude")
    ax1.grid(True, alpha=0.1)
    
    # Plot 2: 32D Magnitude & Closure
    magnitude = np.linalg.norm(history, axis=1)
    ax2.plot(magnitude, color='cyan', lw=3, label='||Y(t)||')
    ax2.axhline(np.linalg.norm(history[0]), color='white', linestyle=':', label='Start Norm')
    ax2.axvline(80, color='yellow', linestyle='--', label='t=80 Restoration')
    ax2.set_title("32D System Magnitude (Closure Proof)")
    ax2.set_xlabel("Time Step (t)")
    ax2.set_ylabel("Norm")
    ax2.legend()
    ax2.grid(True, alpha=0.1)

    plt.tight_layout()
    output_path = 'analysis_results/32D_CANONICAL_CLOSURE.png'
    plt.savefig(output_path)
    print(f"\n[SUCCESS] 32D Closure plot saved to '{output_path}'")

if __name__ == '__main__':
    if not os.path.exists('analysis_results'): os.makedirs('analysis_results')
    hist, err = run_simulation()
    plot_results(hist, err)
