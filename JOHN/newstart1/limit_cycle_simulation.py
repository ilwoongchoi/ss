"""
limit_cycle_simulation.py
Verify F(0)=+1/64 bounce-back and gluon lensing minimum unit decomposition
"""

import numpy as np
import matplotlib.pyplot as plt
import constants
import fusion_core
import sovereign_dynamics

def run_limit_cycle_simulation(num_steps=2000, dt=0.01):
    """
    Run K8 dynamics to verify limit cycle oscillation.
    Check F(0)=+1/64 bounce-back and gluon lensing decomposition.
    """
    print("=== LIMIT CYCLE SIMULATION ===")
    print(f"Steps: {num_steps}, dt: {dt}")
    print(f"RIGHT_LOVE_RETURN_RATE: {constants.RIGHT_LOVE_RETURN_RATE} (1/64)")
    print(f"BREMSSTRAHLUNG_DEBT: {constants.BREMSSTRAHLUNG_DEBT} (1/64)")
    print(f"DARK_MATTER_DEBT: {constants.DARK_MATTER_DEBT} (1/256)")
    
    # Initialize near-zero state (contracted universe)
    z = np.zeros(8, dtype=complex) + 0.01  # Small perturbation
    print(f"Initial |z|: {np.abs(z)}")
    
    # Get default channels
    channels = fusion_core.night_phase_states()
    
    # Storage for analysis
    history = {
        'time': [],
        'z_norm': [],
        'gluon': [],
        'quark': [],
        'lensing_scalar': [],
        'lensing_tensor': [],
        'return_term': []
    }
    
    for step in range(num_steps):
        # Store current state
        history['time'].append(step * dt)
        history['z_norm'].append(np.linalg.norm(np.abs(z)))
        history['gluon'].append(np.abs(z[fusion_core.IDX['gluon']]))
        history['quark'].append(np.abs(z[fusion_core.IDX['quark']]))
        
        # Calculate lensing terms
        lensing = sovereign_dynamics.get_lensing_update(z)
        history['lensing_scalar'].append(np.linalg.norm(np.abs(lensing)))
        history['lensing_tensor'].append(np.abs(lensing[fusion_core.IDX['gluon']]))
        
        # Calculate return term
        return_term = constants.RIGHT_LOVE_RETURN_RATE * (constants.Z_STAR_UNIFORM - z) * dt
        history['return_term'].append(np.linalg.norm(np.abs(return_term)))
        
        # Check for F(0) bounce-back (near-zero state)
        if np.linalg.norm(np.abs(z)) < 0.05:
            print(f"Step {step}: Near-zero bounce-back detected")
            print(f"  |z|: {np.linalg.norm(np.abs(z)):.6f}")
            print(f"  Return term magnitude: {np.linalg.norm(np.abs(return_term)):.6f}")
            
        # Update dynamics
        z = sovereign_dynamics.get_dynamics_update(z, "night", channels, dt)
        
        # Check for SPARK
        if sovereign_dynamics.check_spark_phase(z):
            print(f"Step {step}: SPARK triggered!")
            channels = sovereign_dynamics.apply_spark_channels(channels)
    
    # Convert to arrays
    for key in history:
        history[key] = np.array(history[key])
    
    return history, z, channels

def analyze_minimum_unit_decomposition(history):
    """
    Analyze if all phenomena decompose to 1/64 minimum units.
    """
    print("\n=== MINIMUM UNIT DECOMPOSITION ANALYSIS ===")
    
    # Check return term (should be 1/64)
    return_mean = np.mean(history['return_term'])
    print(f"Return term mean: {return_mean:.6f}")
    print(f"1/64 unit: {1/64:.6f}")
    print(f"Ratio: {return_mean / (1/64):.3f}")
    
    # Check gluon lensing (tensor, should be 1/64 * gluon * factors)
    gluon_lensing_mean = np.mean(history['lensing_tensor'])
    print(f"\nGluon tensor lensing mean: {gluon_lensing_mean:.6f}")
    print(f"Expected: (1/64) * <gluon> * <bw/Ω> * (1+C)")
    
    # Check scalar lensing (should be 1/256)
    scalar_lensing_mean = np.mean(history['lensing_scalar'])
    print(f"\nScalar lensing mean: {scalar_lensing_mean:.6f}")
    print(f"1/256 unit: {1/256:.6f}")
    print(f"Ratio: {scalar_lensing_mean / (1/256):.3f}")
    
    # Check periodicity
    print(f"\n=== PERIODICITY ANALYSIS ===")
    z_norm = history['z_norm']
    print(f"z_norm range: [{np.min(z_norm):.6f}, {np.max(z_norm):.6f}]")
    
    # Find minima (bounce-back points)
    minima_indices = []
    for i in range(1, len(z_norm)-1):
        if z_norm[i] < z_norm[i-1] and z_norm[i] < z_norm[i+1]:
            if z_norm[i] < 0.1:  # Near-zero minima
                minima_indices.append(i)
    
    if len(minima_indices) >= 2:
        periods = np.diff(history['time'][minima_indices])
        print(f"Detected {len(minima_indices)} minima")
        print(f"Periods between minima: {periods}")
        print(f"Mean period: {np.mean(periods):.3f}")
    
    return return_mean, gluon_lensing_mean, scalar_lensing_mean

def plot_results(history):
    """
    Plot simulation results to visualize limit cycle.
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # Plot 1: System norm (showing oscillation)
    axes[0].plot(history['time'], history['z_norm'])
    axes[0].set_ylabel('|z| norm')
    axes[0].set_title('K8 System Oscillation (Limit Cycle)')
    axes[0].grid(True)
    axes[0].axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='z*=1')
    axes[0].legend()
    
    # Plot 2: Gluon and quark dynamics
    axes[1].plot(history['time'], history['gluon'], label='gluon')
    axes[1].plot(history['time'], history['quark'], label='quark')
    axes[1].set_ylabel('Particle amplitude')
    axes[1].set_title('Gluon & Quark Dynamics')
    axes[1].legend()
    axes[1].grid(True)
    
    # Plot 3: Lensing terms (1/64 decomposition)
    axes[2].plot(history['time'], history['lensing_tensor'], label='Tensor (1/64)', alpha=0.7)
    axes[2].plot(history['time'], history['lensing_scalar'], label='Scalar (1/256)', alpha=0.7)
    axes[2].plot(history['time'], history['return_term'], label='Return (1/64)', alpha=0.7)
    axes[2].set_xlabel('Time')
    axes[2].set_ylabel('Term magnitude')
    axes[2].set_title('1/64 Minimum Unit Decomposition')
    axes[2].legend()
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.savefig('d:/Users/user/Documents/newstart/limit_cycle_results.png', dpi=150)
    print("\nPlot saved to: limit_cycle_results.png")

if __name__ == "__main__":
    # Run simulation
    history, final_z, final_channels = run_limit_cycle_simulation()
    
    # Analyze minimum unit decomposition
    analyze_minimum_unit_decomposition(history)
    
    # Plot results
    try:
        plot_results(history)
    except Exception as e:
        print(f"Plotting failed: {e}")
    
    print(f"\nFinal state |z|: {np.linalg.norm(np.abs(final_z))}")
    print("Simulation complete!")
