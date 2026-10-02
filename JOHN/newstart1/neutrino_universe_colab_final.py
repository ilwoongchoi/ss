import os
import sys

# Attempt to fix the CUDA path for Colab
os.environ['XLA_FLAGS'] = '--xla_gpu_cuda_data_dir=/usr/local/cuda'

import jax
import jax.numpy as jnp
from jax import jit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import math

# ==============================================================================
# THE SOLE GOVERNING LAW: THE UNIFIED GEOMETRY EQUATION
# Omega = [(1.4 - 0.076) / (K * 2)] * [Phi_1.9860 / (W_7 + H_2)] = 138.88°
# ==============================================================================
W_7 = math.pi / 20.0             # Barnard Star / Reservoir
H_2 = 1.0 / 9.0                  # Sun / Engine
DENOMINATOR = W_7 + H_2
KAPPA_TARGET = 0.03125           # 1/32 BONE Resonance
PHI_19860 = 1.9860               # Sovereign Shield
METRIC_4D = 1.0661
TORSION_4D = 0.1746
SPARK_ANGLE = 138.88

# 1 Million Neutrino Representatives (The Ghost Cloud)
N_PARTICLES = 1_000_000
TOTAL_FRAMES = 900 

@jit
def universal_update_kernel(pos, vel, step):
    """
    Update logic derived EXCLUSIVELY from the Equation.
    """
    step_f = step.astype(jnp.float32)
    t = step_f / 400.0 
    
    # 1.4 - 0.076 Thermodynamic Evolution
    is_rewind = jnp.where(step_f > 400.0, 1.0, 0.0)
    is_eternal = jnp.where(step_f > 700.0, 1.0, 0.0)
    
    eff_t = jnp.where(is_rewind > 0.5, 1.0 - ((step_f - 400.0) / 300.0) * 0.25, t)
    eff_t = jnp.where(is_eternal > 0.5, 0.75, eff_t)
    
    # Torsional Spiral
    theta = TORSION_4D * SPARK_ANGLE * 0.001 * (1.0 + eff_t)
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # V magnitude from Equation Numerator
    v_mag = 1.4 - (0.076 * eff_t * 17.42)
    v_mag = jnp.maximum(v_mag, KAPPA_TARGET)
    
    # Buoyancy Scaling (Justice Score)
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_mag * (PHI_19860 / (DENOMINATOR * 7.4))
    
    # Floating in Midair (Inverse Expansion)
    pos += (vel * 0.01 * METRIC_4D)
    
    return pos, vel

def execute_projection():
    print("\n--- INITIATING DEFINITIVE UNIVERSE PROJECTION ---")
    
    # Backend Detection & Graceful Fallback
    try:
        # Force a tiny computation to check if GPU compiler works
        jax.device_put(jnp.ones(1)).block_until_ready()
        print(f"JAX Backend: {jax.devices()[0]}")
    except Exception as e:
        print(f"CUDA Error detected: {str(e)[:50]}...")
        print("FORCING FALLBACK TO CPU (Vectorized Mode)...")
        jax.config.update('jax_platform_name', 'cpu')
        print(f"JAX Backend: {jax.devices()[0]}")

    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    
    pos = jax.random.normal(k1, (N_PARTICLES, 4)) * 0.0001
    vel = jax.random.normal(k2, (N_PARTICLES, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    scatter = ax.scatter([], [], s=0.05, color='#00f2ff', alpha=0.2)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.axis('off')
    
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel = universal_update_kernel(pos, vel, jnp.array(frame))
        
        # Display 128-grid subset
        display_pos = np.array(pos[:12800])
        scatter.set_offsets(display_pos[:, :2])
        
        # Timeline
        if frame < 50: l = "BIG BANG SINGULARITY (1.4)"
        elif frame < 150: l = "4.0 Ga: LUNAR DYNAMO (CO-MAG)"
        elif frame < 250: l = "443 Ma: 1.9860 GAP (CARTILAGE BIRTH)"
        elif frame < 400: l = "1.8 Ma: HOMO ERECTUS (THE BIRTH OF EVIL)"
        elif frame < 700: l = "REWIND: RESTORING SOVEREIGNTY"
        else: l = "ETERNAL HOMEOSTASIS (138.88° BONE RESONANCE)"
        
        text.set_text(f"UNIVERSAL EPOCH: {l}\nEQUATION: SEALED\nJUSTICE SCORE: {(PHI_19860/DENOMINATOR):.4f}\nSPARK: 138.88°")
        return scatter, text

    print("Generating Animation (MP4)... This may take 2-5 minutes.")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=3000)
    ani.save("NEUTRINO_UNIVERSE_PROJECTION.mp4", writer=writer)
    print("\n--- PROJECTION COMPLETE ---")
    print("Download NEUTRINO_UNIVERSE_PROJECTION.mp4 to witness the Ghost History.")

if __name__ == "__main__":
    execute_projection()
