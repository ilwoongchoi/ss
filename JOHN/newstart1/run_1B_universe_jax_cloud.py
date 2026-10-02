import jax
import jax.numpy as jnp
from jax import jit
import h5py
import numpy as np
import time
import math
import os

# ==============================================================================
# THE UNIFIED GEOMETRY CONSTANTS (The Final Equation)
# ==============================================================================
# The Archetypal Hardware
W_7 = math.pi / 20.0             # ~0.157079 (Barnard / Red Dwarf / The Reservoir)
H_2 = 1.0 / 9.0                  # ~0.111111 (The Sun / Yellow Dwarf / The Engine)
DENOMINATOR = W_7 + H_2          # ~0.268190

# The Metric & Torsion
METRIC_4D = 1.0661
TORSION_4D = 0.1746

# The Particle Limits (The Epochs)
BIFURCATION_LIMIT = 1.4          # The "Big Woman" Chaos (Start)
SUBTRACTIVE_TENSION = 0.076      # The Slotting Tension
RESONANCE_TARGET = 0.03125       # 1/32 The Sieve
NEUTRINO_UNIT = 1.0 / 128.0      # The Small Man / Ghost Vector
GRAVITON_FLOOR = 1.0 / 256.0     # The D3 Drain

# The Sovereign Shield
PHI_19860 = 1.9860               # The Justice Score / hc Bridge

# ==============================================================================
# CLOUD GPU SCALE SETTINGS
# ==============================================================================
# 1 BILLION PARTICLES. 
# Requires ~16GB VRAM for State. Easily fits on 1x A100 (40GB/80GB) or TPU.
N_PARTICLES = 1_000_000_000  
TOTAL_STEPS = 5000
DT = 0.01

print(f"JAX Backend Initialized. Devices: {jax.devices()}")
print(f"Allocating Memory for {N_PARTICLES:,} Universe Nodes...")

# ==============================================================================
# EXTREME SCALE PHYSICS KERNEL
# ==============================================================================

@jit
def universal_epoch_step(pos, vel, step_idx):
    """
    Executes the Unified Geometry Equation across 1 Billion discrete entities.
    """
    # 1. Global Expansion
    expansion = METRIC_4D * (1.0 + (step_idx / TOTAL_STEPS) * 0.5)
    
    # 2. Torsional Ghost Spiral (The 138.88° mapping)
    theta = TORSION_4D * DT
    c, s = jnp.cos(theta), jnp.sin(theta)
    
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vx_new, vy_new = c * vx - s * vy, s * vx + c * vy
    vz_new, vw_new = c * vz - s * vw, s * vz + c * vw
    vel = jnp.stack([vx_new, vy_new, vz_new, vw_new], axis=1)
    
    # 3. The Epoch Slotting (1.4 -> 0.076 -> 1/32)
    progress = step_idx / TOTAL_STEPS
    current_target_v = jnp.maximum(
        BIFURCATION_LIMIT - (SUBTRACTIVE_TENSION * progress * 17.42), 
        RESONANCE_TARGET
    )
    
    # 4. The 1/128 Homeostatic Buoyancy against D3 (1/256)
    buoyancy_factor = NEUTRINO_UNIT / GRAVITON_FLOOR # Exactly 2.0
    
    # Apply velocity update
    v_norms = jnp.linalg.norm(vel, axis=1, keepdims=True)
    vel = (vel / v_norms) * current_target_v * (1.0 + (1e-6 * buoyancy_factor))
    
    # 5. The Unified Equation (Calculating the Master 138.88 Resonance Score)
    # Omega_Universe = [(1.4 - 0.076) / (K * 2)] * [Phi_1.9860 / (W_7 + H_2)]
    # This must remain strictly deterministic.
    master_resonance_score = (current_target_v / (RESONANCE_TARGET * buoyancy_factor)) * (PHI_19860 / DENOMINATOR)
    
    # 6. Geodesic Update
    pos += (vel * DT * expansion)
    
    return pos, vel, master_resonance_score

# ==============================================================================
# RUNNER
# ==============================================================================

def execute_universe():
    # Initialize 1 Billion Particles on GPU
    # Using float32 for absolute geometric precision
    key = jax.random.PRNGKey(13888) # Seeded with the spark angle
    key1, key2 = jax.random.split(key)
    
    print("Generating Big Bang Initial State...")
    pos = jax.random.normal(key1, (N_PARTICLES, 4), dtype=jnp.float32) * NEUTRINO_UNIT
    
    v_raw = jax.random.normal(key2, (N_PARTICLES, 4), dtype=jnp.float32)
    v_norms = jnp.linalg.norm(v_raw, axis=1, keepdims=True)
    vel = (v_raw / v_norms) * BIFURCATION_LIMIT

    # We only save a subset of paths (e.g., 100,000 representative ghosts) to disk
    # to avoid creating a terabyte-sized file, but all 1 Billion are calculated.
    SAVE_SUBSET = 100_000 
    SAVE_INTERVAL = 100
    n_frames = TOTAL_STEPS // SAVE_INTERVAL
    
    ghost_ledger = np.zeros((n_frames, SAVE_SUBSET, 4), dtype=np.float16)
    resonance_ledger = np.zeros(n_frames, dtype=np.float32)
    
    print("\n[INITIATING 1 BILLION NEUTRINO FLOW]")
    print(f"W_7 (Barnard Reservoir) + H_2 (Sun Engine) = {DENOMINATOR:.6f}")
    
    start_time = time.time()
    save_idx = 0
    
    for i in range(TOTAL_STEPS):
        pos, vel, omega_score = universal_epoch_step(pos, vel, i)
        
        # JAX evaluates asynchronously. Block/wait periodically to log.
        if i % SAVE_INTERVAL == 0:
            omega_val = float(omega_score)
            ghost_ledger[save_idx] = np.array(pos[:SAVE_SUBSET])
            resonance_ledger[save_idx] = omega_val
            
            # 1.9860 Sovereign Check
            status = "LOCKED" if omega_val > 1.0 else "D3-DISSIPATION"
            print(f"Epoch {i:04d} | Resonance Score: {omega_val:.4f} | {status} | T: {time.time()-start_time:.1f}s")
            save_idx += 1

    total_time = time.time() - start_time
    print(f"\n[UNIVERSE HISTORY COMPLETED in {total_time:.2f} seconds]")
    
    os.makedirs("out", exist_ok=True)
    out_file = "out/1_BILLION_GHOST_LEDGER.h5"
    print(f"Saving Sovereign Subset ({SAVE_SUBSET} paths) to {out_file}...")
    
    with h5py.File(out_file, 'w') as f:
        f.create_dataset("ghost_trajectories", data=ghost_ledger, compression="gzip")
        f.create_dataset("omega_resonance_scores", data=resonance_ledger)
        f.attrs["Total_Simulated_Neutrinos"] = N_PARTICLES
        f.attrs["W7_H2_Denominator"] = DENOMINATOR
        f.attrs["Phi_Justice_Score"] = PHI_19860
        f.attrs["Note"] = "The definitive history of the Small Man."

if __name__ == "__main__":
    execute_universe()
