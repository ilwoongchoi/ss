import os
# Force JAX to find the correct CUDA path in Colab
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
# ==============================================================================
W_7 = math.pi / 20.0             
H_2 = 1.0 / 9.0                  
DENOMINATOR = W_7 + H_2
KAPPA_TARGET = 0.03125           
PHI_19860 = 1.9860               
METRIC_4D = 1.0661
TORSION_4D = 0.1746
SPARK_ANGLE = 138.88

# 1 Million Neutrino Representatives
N_PARTICLES = 1_000_000
TOTAL_FRAMES = 900 

@jit
def universal_update_kernel(pos, vel, step):
    """
    Update logic derived EXCLUSIVELY from the Equation.
    """
    # Ensure step is treated as a float32 for JAX consistency
    step_f = step.astype(jnp.float32)
    t = step_f / 400.0 
    
    # The Subtraction Formula
    v_evolution = 1.4 - (0.076 * t)
    
    # Emergent Rewind (Mobius Hysteresis)
    is_rewind = jnp.where(step_f > 400.0, 1.0, 0.0)
    is_eternal = jnp.where(step_f > 700.0, 1.0, 0.0)
    
    # Reverse the t vector if in rewind
    eff_t = jnp.where(is_rewind > 0.5, 1.0 - ((step_f - 400.0) / 300.0) * 0.25, t)
    eff_t = jnp.where(is_eternal > 0.5, 0.75, eff_t)
    
    # 4D Torsion from the Spark
    theta = TORSION_4D * SPARK_ANGLE * 0.001 * (1.0 + eff_t)
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # Velocity magnitude determined by Numerator
    v_mag = 1.4 - (0.076 * eff_t * 17.42)
    v_mag = jnp.maximum(v_mag, KAPPA_TARGET)
    
    # Buoyancy (1/128 over 1/256)
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_mag * (PHI_19860 / (DENOMINATOR * 7.4))
    
    # Position update
    pos += (vel * 0.01 * METRIC_4D)
    
    return pos, vel

def execute_projection():
    print("Initiating Fixed 10^89 Neutrino Mapping...")
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    
    # Start at Singularity
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
        # Convert frame to JAX array to prevent recompilation
        pos, vel = universal_update_kernel(pos, vel, jnp.array(frame))
        
        display_pos = np.array(pos[:12800])
        scatter.set_offsets(display_pos[:, :2])
        
        if frame < 50: l = "BIG BANG SINGULARITY (1.4)"
        elif frame < 150: l = "4.0 Ga: LUNAR DYNAMO (CO-MAG)"
        elif frame < 250: l = "443 Ma: THE 1.9860 GAP (JAWS/CARTILAGE)"
        elif frame < 400: l = "1.8 Ma: HOMO ERECTUS (THE BIRTH OF EVIL)"
        elif frame < 700: l = "REWIND: RESTORING SOVEREIGNTY"
        else: l = "ETERNAL HOMEOSTASIS (138.88° RESONANCE)"
        
        justice = PHI_19860 / DENOMINATOR
        text.set_text(f"UNIVERSAL EPOCH: {l}\nEQUATION: LOCKED\nJUSTICE MARGIN: {justice:.4f}\nSPARK: 138.88°")
        return scatter, text

    print("Generating Animation (MP4)...")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=3000)
    ani.save("NEUTRINO_UNIVERSE_PROJECTION.mp4", writer=writer)
    print("\n--- PROJECTION SEALED ---")

if __name__ == "__main__":
    execute_projection()
