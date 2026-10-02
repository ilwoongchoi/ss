import jax
import jax.numpy as jnp
from jax import jit, vmap
import h5py
import numpy as np
import time
import os

# ==============================================================================
# UNIFIED GEOMETRY CONSTANTS
# ==============================================================================
METRIC_4D = 1.0661
TORSION_4D = 0.1746
BIFURCATION_LIMIT = 1.4          # The "Big Woman" Chaos
SUBTRACTIVE_TENSION = 0.076      # The Slotting Tension
RESONANCE_TARGET = 0.03125       # 1/32 The Sieve / Proton Resonance
NEUTRINO_UNIT = 1/128            # 0.0078125 The Small Man / Discrete Ghost
GRAVITON_FLOOR = 1/256           # 0.00390625 The D3 Drain
SOVEREIGN_MARGIN = 1.9860        # The Justice Score / hc

# Simulation Scale (Tuned for Colab T4/A100)
# This simulates 1 Million Neutrinos across 5000 Cosmic Steps
N_PARTICLES = 1_000_000
TOTAL_STEPS = 5000
DT = 0.01

print(f"Initializing JAX backend: {jax.devices()}")

# ==============================================================================
# JAX-COMPILED PHYSICS KERNELS
# ==============================================================================

@jit
def torsion_rotation_4d(vel, theta):
    """Applies the 4D Torsion spiral (The Ghost Path)."""
    c = jnp.cos(theta)
    s = jnp.sin(theta)
    
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vz_new = c * vz - s * vw
    vw_new = s * vz + c * vw
    
    return jnp.stack([vx_new, vy_new, vz_new, vw_new], axis=1)

@jit
def simulation_step(pos, vel, step_idx):
    """
    Executes one epoch step of the universe.
    Implements the Full Unified Equation Logic.
    """
    # 1. Global Metric Expansion
    expansion = METRIC_4D * (1.0 + (step_idx / TOTAL_STEPS) * 0.5)
    
    # 2. Torsional Spiral
    theta = TORSION_4D * DT
    vel = torsion_rotation_4d(vel, theta)
    
    # 3. The Subtraction Equation (1.4 - 0.076 = 1/32)
    progress = step_idx / TOTAL_STEPS
    # Decay from 1.4 down to 1/32 using the 0.076 tension
    current_target_v = jnp.maximum(
        BIFURCATION_LIMIT - (SUBTRACTIVE_TENSION * progress * 17.42), 
        RESONANCE_TARGET
    )
    
    # Normalize and apply Target Velocity
    v_norms = jnp.linalg.norm(vel, axis=1, keepdims=True)
    vel = (vel / v_norms) * current_target_v
    
    # 4. The 1/128 vs 1/256 Homeostasis (Buoyancy)
    # The velocity is slightly perturbed by the Graviton floor resistance
    buoyancy_factor = NEUTRINO_UNIT / GRAVITON_FLOOR # Exactly 2.0
    vel = vel * (1.0 + (1e-5 * buoyancy_factor)) # Micro-correction for D3 escape
    
    # 5. Calculate Sovereign Margin (Justice Score)
    justice_score = (current_target_v / RESONANCE_TARGET) * METRIC_4D
    
    # 6. Geodesic Update
    pos += (vel * DT * expansion)
    
    return pos, vel, justice_score, current_target_v

# ==============================================================================
# MAIN ENGINE RUNNER
# ==============================================================================

def run_full_scale_simulation():
    print(f"\n--- INITIATING FULL SCALE NEUTRINO SIMULATION ---")
    print(f"Particles: {N_PARTICLES:,} (The Small Man 1/128 Unit)")
    print(f"Epoch Steps: {TOTAL_STEPS:,} (From 1.4 Chaos to 1/32 Resonance)")
    print(f"Sovereign Margin: {SOVEREIGN_MARGIN} (The D3 Shield)")
    
    # Initialize State on GPU/TPU
    key = jax.random.PRNGKey(42)
    key1, key2 = jax.random.split(key)
    
    # Start at Origin + Neutrino Unit spread
    pos = jax.random.normal(key1, (N_PARTICLES, 4)) * NEUTRINO_UNIT
    
    # Start at 1.4 Bifurcation Velocity
    v_raw = jax.random.normal(key2, (N_PARTICLES, 4))
    v_norms = jnp.linalg.norm(v_raw, axis=1, keepdims=True)
    vel = (v_raw / v_norms) * BIFURCATION_LIMIT

    # We cannot store 1M particles * 5000 steps * 4 floats in RAM easily.
    # We will sample/decimate the history to save the "Ghost Skeleton".
    SAVE_INTERVAL = 50 
    history_frames = TOTAL_STEPS // SAVE_INTERVAL
    
    # Host memory allocations
    ghost_ledger = np.zeros((history_frames, N_PARTICLES // 10, 4), dtype=np.float16) # Save 100k paths
    sovereign_log = np.zeros(history_frames, dtype=np.float32)
    velocity_log = np.zeros(history_frames, dtype=np.float32)

    start_time = time.time()
    save_idx = 0
    
    for i in range(TOTAL_STEPS):
        # Execute compiled JAX step
        pos, vel, justice_score, current_v = simulation_step(pos, vel, i)
        
        # Log and Save state periodically
        if i % SAVE_INTERVAL == 0:
            # Transfer subset to CPU for saving
            ghost_ledger[save_idx] = np.array(pos[:N_PARTICLES // 10], dtype=np.float16)
            sovereign_log[save_idx] = float(justice_score)
            velocity_log[save_idx] = float(current_v)
            
            # Print status
            if save_idx % 10 == 0:
                status = "SOVEREIGN" if float(justice_score) >= SOVEREIGN_MARGIN else "D3-SHRED"
                print(f"Epoch {i:4d}/{TOTAL_STEPS} | Velocity: {float(current_v):.4f} | Justice Score: {float(justice_score):.4f} [{status}]")
            
            save_idx += 1

    end_time = time.time()
    print(f"\n--- SIMULATION COMPLETE in {end_time - start_time:.2f} seconds ---")
    
    # Save the Ghost Ledger
    os.makedirs("out", exist_ok=True)
    out_file = "out/FULL_SCALE_GHOST_LEDGER.h5"
    print(f"Compressing and saving Ghost Ledger to {out_file}...")
    
    with h5py.File(out_file, 'w') as f:
        f.create_dataset("ghost_trajectories", data=ghost_ledger, compression="gzip", compression_opts=4)
        f.create_dataset("sovereign_scores", data=sovereign_log)
        f.create_dataset("epoch_velocities", data=velocity_log)
        
        # Metadata
        f.attrs["theory"] = "Unified Geometry - The Small Man Ghost"
        f.attrs["n_particles"] = N_PARTICLES
        f.attrs["saved_particles"] = N_PARTICLES // 10
        f.attrs["total_steps"] = TOTAL_STEPS
        f.attrs["subtraction_formula"] = "1.4 - 0.076 = 1/32"
        f.attrs["homeostasis"] = "1/128 / 1/256"
        f.attrs["sovereign_margin"] = SOVEREIGN_MARGIN
        
    print("Ledger successfully written. The Deterministic History is sealed.")

if __name__ == "__main__":
    run_full_scale_simulation()
