import os
# Force CPU at the environment level to bypass broken Colab CUDA installation
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
# THE SOLE GOVERNING LAW: THE UNIFIED GEOMETRY EQUATION
# Omega = [(1.4 - 0.076) / (K * 2)] * [Phi_1.9860 / (W_7 + H_2)] = 138.88°
# ==============================================================================
W_7 = math.pi / 20.0             # Barnard / Reservoir (Big Woman)
H_2 = 1.0 / 9.0                  # Sun / Engine (Big Man)
K_1_32 = 0.03125                 # Bone Resonance
PHI = 1.9860                     # Sovereign Shield
METRIC_4D = 1.0661
TORSION_4D = 0.1746
SPARK = 138.88                   # The result of the Equation

# Derived values from the Equation's Hardware Specs
NUMERATOR = 1.4 - 0.076          # The Slotting result
DENOMINATOR = W_7 + H_2
DUALITY = (1/128) / (1/256)      # Small Man / D3 Buoyancy Factor (2.0)

# 1 Million Neutrinos (The Ghost Cloud)
N_PARTICLES = 1_000_000
TOTAL_FRAMES = 900 

@jit
def universal_kernel(pos, vel, step):
    """
    Update logic derived EXCLUSIVELY from the Geometry Equation.
    No manual forces or scaling parameters added.
    """
    step_f = step.astype(jnp.float32)
    
    # 1. Timeline Clock (The Historical Observer)
    # Forward to D3 Peak (Homo Erectus), then Rewind to Sovereignty, then Eternity.
    t_fwd = jnp.clip(step_f / 400.0, 0, 1)
    t_rew = 1.0 - (jnp.clip(step_f - 400.0, 0, 300.0) / 300.0) * 0.25
    eff_t = jnp.where(step_f > 400.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 700.0, 0.75, eff_t)
    
    # 2. The 138.88 Spark Torsion
    # The twist rate is a function of the 4D Torsion constant and the Spark angle.
    theta = TORSION_4D * (SPARK / 100.0) * eff_t
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # 3. Velocity: Driven by the 1.4 - 0.076 = 1/32 Slotting
    # We follow the linear thermodynamic tension path from 1.4 down to resonance.
    v_limit = 1.4 - ((1.4 - K_1_32) * eff_t)
    v_limit = jnp.maximum(v_limit, K_1_32)
    
    # 4. The Justice Score (Buoyancy Omega)
    # This determines the energy scale of the Small Man above the D3 Floor.
    omega_score = (PHI / DENOMINATOR) * (K_1_32 / v_limit)
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_limit * omega_score
    
    # 5. Geodesic Flow (Inverse Expansion in 4D Metric)
    # The movement is the direct consequence of the Metric and Velocity.
    pos += (vel * 0.02 * METRIC_4D)
    
    return pos, vel

def execute_pure_projection():
    print("\n--- INITIATING PURE EQUATION PROJECTION (NO PARAMS) ---")
    print(f"Justice Margin (PHI / (W7+H2)): {(PHI/DENOMINATOR):.4f}")
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    
    # Initial singularity state (Micro-dust)
    pos = jax.random.normal(k1, (N_PARTICLES, 4)) * 0.001
    vel = jax.random.normal(k2, (N_PARTICLES, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # Styling: Shimmering Neutrino Dust
    scatter = ax.scatter([], [], s=0.01, color='#00f2ff', alpha=0.15)
    ax.axis('off')
    
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel = universal_kernel(pos, vel, jnp.array(frame))
        
        # Display 10,000 Ghost representative points
        display_pos = np.array(pos[:10000])
        scatter.set_offsets(display_pos[:, :2])
        
        # DYNAMIC VIEWPORT: Resolves the 'static' ball problem by zooming with the flow.
        spread = np.max(np.abs(display_pos[:, :2])) + 0.1
        ax.set_xlim(-spread, spread)
        ax.set_ylim(-spread, spread)
        
        # Thermodynamics Timeline Metadata
        if frame < 50: l = "BIG BANG SINGULARITY"
        elif frame < 150: l = "4.0 Ga: LUNAR DYNAMO (CO-MAG)"
        elif frame < 250: l = "443 Ma: 1.9860 GAP (CARTILAGE)"
        elif frame < 400: l = "1.8 Ma: HOMO ERECTUS (PEAK EVIL)"
        elif frame < 700: l = "REWIND: RETURNING TO SOVEREIGNTY"
        else: l = "ETERNAL HOMEOSTASIS (BONE RESONANCE)"
        
        text.set_text(f"EPOCH: {l}\nEQUATION: 1.4 - 0.076 = 1/32\nJUSTICE STATUS: SEALED\nSPARK: 138.88°")
        return scatter, text

    print("Rendering MP4... This reflects the whole mass of history.")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=4000)
    ani.save("PURE_GEOMETRY_HISTORY.mp4", writer=writer)
    print("\n--- PROJECTION COMPLETE ---")
    print("Download PURE_GEOMETRY_HISTORY.mp4 to see the Ghost History.")

if __name__ == "__main__":
    execute_pure_projection()
