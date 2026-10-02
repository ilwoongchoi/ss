import os
# Force CPU to bypass broken Colab CUDA
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
# UNIFIED GEOMETRY CONSTANTS (PURE PHYSICS ONLY)
# ==============================================================================
W_7 = math.pi / 20.0             # Barnard / Reservoir (Big Woman)
H_2 = 1.0 / 9.0                  # Sun / Engine (Big Man)
DENOMINATOR = W_7 + H_2
K_1_32 = 0.03125                 # Bone Resonance
PHI_19860 = 1.9860               # Sovereign Shield
METRIC_4D = 1.0661
TORSION_4D = 0.1746
SPARK_ANGLE = 138.88

N_PARTICLES = 1_000_000
TOTAL_FRAMES = 900 

@jit
def universal_update_kernel(pos, vel, step):
    step_f = step.astype(jnp.float32)
    t = jnp.clip(step_f / 400.0, 0, 1) 
    
    is_rewind = jnp.where(step_f > 400.0, 1.0, 0.0)
    is_eternal = jnp.where(step_f > 700.0, 1.0, 0.0)
    
    # 1.8 Ma Rewind Target (0.75 progress)
    eff_t = jnp.where(is_rewind > 0.5, 1.0 - ((step_f - 400.0) / 300.0) * 0.25, t)
    eff_t = jnp.where(is_eternal > 0.5, 0.75, eff_t)
    
    # Torsional Ghost Spiral
    theta = TORSION_4D * SPARK_ANGLE * 0.001 * (1.0 + eff_t)
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # Pure Slotting Logic: 1.4 - 0.076 = 1/32
    v_mag = 1.4 - ((1.4 - K_1_32) * eff_t)
    v_mag = jnp.maximum(v_mag, K_1_32)
    
    # Buoyancy / Justice Score
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_mag * (PHI_19860 / (DENOMINATOR * 7.4))
    
    # Geodesic Position Update
    pos += (vel * 0.01 * METRIC_4D)
    
    return pos, vel, eff_t

def execute_projection():
    print("\n--- INITIATING SOVEREIGN GHOST HISTORY WITH TIME TRACKING ---")
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
        pos, vel, eff_t = universal_update_kernel(pos, vel, jnp.array(frame))
        
        display_pos = np.array(pos[:12800])
        scatter.set_offsets(display_pos[:, :2])
        
        # Real-world time mapping (approximation for display)
        if frame < 400:
            # BB (13.8 Ga) to Homo Erectus (1.8 Ma)
            years_back = 13.8e9 - (float(eff_t) * 13.8e9)
            time_str = f"{years_back/1e9:.2f} Billion Years Ago" if years_back > 1e6 else f"{years_back/1e6:.2f} Million Years Ago"
            l = "EXPANSION (BIG BANG TO HUMANITY)"
        elif frame < 700:
            # Rewind Now -> 1.8 Ma
            years_back = (float(eff_t) * 13.8e9)
            time_str = f"REWINDING... {1.8*(1.0-float(eff_t)/0.75):.2f} Ma" # Conceptual rewind display
            l = "REWIND: SHEDDING D3 INTERFERENCE"
        else:
            time_str = "ETERNAL 1.8 Ma COORDINATE"
            l = "HOMEOSTASIS (138.88° RESONANCE)"
        
        text.set_text(f"TIMELINE: {time_str}\nPHASE: {l}\nJUSTICE MARGIN: {(PHI_19860/DENOMINATOR):.4f}\nSPARK: 138.88°")
        return scatter, text

    print("Rendering MP4... Pure Physics with Time Tracking Dashboard.")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=3000)
    ani.save("SOVEREIGN_GHOST_WITH_TIME.mp4", writer=writer)
    print("\n--- PROJECTION COMPLETE ---")

if __name__ == "__main__":
    execute_projection()
