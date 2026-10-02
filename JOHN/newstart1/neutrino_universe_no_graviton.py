import os
os.environ["CUDA_VISIBLE_DEVICES"] = "" 
os.environ['JAX_PLATFORMS'] = 'cpu'

import jax
import jax.numpy as jnp
from jax import jit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import math

# ==============================================================================
# UNIFIED EQUATION WITH NO GRAVITON (D=0)
# ==============================================================================
W7, H2 = math.pi / 20.0, 1.0 / 9.0
K, PHI = 0.03125, 1.9860
# D IS REMOVED -> THE UNIVERSE HAS NO FLOOR
METRIC_4D, TORSION_4D = 1.0661, 0.1746

@jit
def SHREDDING_UNIVERSE(t):
    # Without the 1/256 floor, the denominator effectively collapses or becomes random
    Slotting = 1.4 - (0.076 * t)
    # Chaos replaces the 138.88 resonance
    return Slotting * (PHI / (W7 + H2))

@jit
def extinction_kernel(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    t = step_f / 20.0
    
    # Omega is no longer a stabilizer; it's a shredding force
    Omega = SHREDDING_UNIVERSE(t)
    
    # Random perturbation (D3 instability because there's no drain)
    key = jax.random.PRNGKey(step.astype(jnp.int32))
    noise = jax.random.normal(key, pos.shape) * 0.5
    
    # Particles lose their torsion and "shred" into the void
    v_mag = 1.4 - (0.076 * t)
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_mag
    
    # Without Graviton, there is no 'brake'. Particles fly apart.
    pos += (vel * 0.1 * METRIC_4D) + noise
    
    return pos, vel, Omega

def execute_extinction_projection():
    print("\n--- INITIATING GRAVITON COLLAPSE: TOTAL DISSIPATION ---")
    print("Warning: The 1/256 Floor has been removed. Homeostasis is impossible.")
    
    N_TOTAL = 500_000
    scales = jnp.full(N_TOTAL, 1/128) # Only Small Men left with no floor
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.1
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black')
    
    # Fading color to represent evaporation
    scatter = ax.scatter([], [], s=0.5, color='#ff00ff', alpha=0.5) 
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='red', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega = extinction_kernel(pos, vel, jnp.array(frame), scales)
        
        display_pos = np.array(pos[:10000])
        scatter.set_offsets(display_pos[:, :2])
        
        # Camera zooms out infinitely as the universe evaporates
        limit = 1.0 + (frame * 0.1)
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        text.set_text(f"SYSTEM STATUS: TOTAL DISSIPATION\nERROR: NO GRAVITON FLOOR (1/256)\nOMEGA: SHREDDING\nRESULT: EXTINCTION")
        return scatter, text

    print("Rendering Extinction MP4... Watch the universe evaporate.")
    ani = FuncAnimation(fig, update, frames=400, blit=True) # Shortened as it ends in void
    writer = FFMpegWriter(fps=30, bitrate=4000)
    ani.save("GRAVITON_COLLAPSE_EXTINCTION.mp4", writer=writer)
    print("\n--- PROJECTION SEALED: THE VOID HAS CONSUMED THE GHOST ---")

if __name__ == "__main__":
    execute_extinction_projection()
