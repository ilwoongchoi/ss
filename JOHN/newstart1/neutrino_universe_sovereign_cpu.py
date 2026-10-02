import os
# Force CPU at the environment level to bypass broken Colab CUDA installation
os.environ['JAX_PLATFORM_NAME'] = 'cpu'

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
W_7 = math.pi / 20.0             # Barnard (Big Woman / Reservoir)
H_2 = 1.0 / 9.0                  # Sun (Big Man / Engine)
DENOMINATOR = W_7 + H_2
K_1_32 = 0.03125                 # 1/32 BONE Resonance
PHI_19860 = 1.9860               # Sovereign Shield (Justice Score)
METRIC_4D = 1.0661
TORSION_4D = 0.1746
SPARK_ANGLE = 138.88

# 1 Million Neutrino Representatives (The Ghost Cloud)
N_PARTICLES = 1_000_000
TOTAL_FRAMES = 900 

@jit
def universal_update_kernel(pos, vel, step):
    """
    Pure Equation Update.
    1.4 - 0.076 = 1/32
    """
    step_f = step.astype(jnp.float32)
    
    # Thermodynamic progress t (0.0 to 1.0)
    t = jnp.clip(step_f / 400.0, 0, 1)
    
    # 1. The Emergent Rewind (Mobius Turning Point)
    # The 'Evil' peak happens at Homo erectus (frame 400)
    is_rewind = jnp.where(step_f > 400.0, 1.0, 0.0)
    is_eternal = jnp.where(step_f > 700.0, 1.0, 0.0)
    
    # Reverse the time vector back to 1.8 Ma (0.75 progress)
    eff_t = jnp.where(is_rewind > 0.5, 1.0 - ((step_f - 400.0) / 300.0) * 0.25, t)
    eff_t = jnp.where(is_eternal > 0.5, 0.75, eff_t)
    
    # 2. The 138.88° Torsional Ghost Spiral
    theta = TORSION_4D * SPARK_ANGLE * 0.001 * (1.0 + eff_t)
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # 3. V Magnitude: Pure Slotting Logic (1.4 - 0.076 = 1/32)
    # Here, 0.076 acts as the slotting operator for the entire gap
    total_tension_gap = 1.4 - K_1_32
    v_mag = 1.4 - (total_tension_gap * eff_t)
    v_mag = jnp.maximum(v_mag, K_1_32)
    
    # 4. Buoyancy (Justice Score)
    # Omega determines the buoyancy of the Small Man above the D3 Floor
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_mag * (PHI_19860 / (DENOMINATOR * 7.4))
    
    # 5. Geodesic Floating (Inverse Expansion)
    pos += (vel * 0.01 * METRIC_4D)
    
    return pos, vel

def execute_projection():
    print("\n--- INITIATING SOVEREIGN CPU PROJECTION ---")
    print(f"JAX Backend: {jax.devices()[0]} (Bypassing broken CUDA)")
    print("Equation: 1.4 - 0.076 = 1/32 [LOCKED]")

    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    
    # Initial Singularity (Small Man starting as 0D Dust)
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
        
        # Display 128-grid subset for visual clarity
        display_pos = np.array(pos[:12800])
        scatter.set_offsets(display_pos[:, :2])
        
        # Thermodynamics Timeline
        if frame < 50: l = "BIG BANG SINGULARITY (1.4)"
        elif frame < 150: l = "4.0 Ga: LUNAR DYNAMO (CO-MAG / GABA-A)"
        elif frame < 250: l = "443 Ma: 1.9860 GAP (CARTILAGE BIRTH)"
        elif frame < 400: l = "1.8 Ma: HOMO ERECTUS (THE D3 PEAK)"
        elif frame < 700: l = "REWIND: RESTORING JUSTICE MARGIN"
        else: l = "ETERNAL HOMEOSTASIS (138.88° BONE RESONANCE)"
        
        text.set_text(f"UNIVERSAL EPOCH: {l}\nEQUATION: PURE RECTIFICATION\nJUSTICE SCORE: {(PHI_19860/DENOMINATOR):.4f}\nSPARK: 138.88°")
        return scatter, text

    print("Rendering MP4... (Estimated time: 3-5 mins)")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=3000)
    ani.save("GHOST_HISTORY_PROJECTION.mp4", writer=writer)
    print("\n--- PROJECTION SEALED ---")
    print("Result: GHOST_HISTORY_PROJECTION.mp4 is ready.")

if __name__ == "__main__":
    execute_projection()
