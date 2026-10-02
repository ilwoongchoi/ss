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
# THE SINGLE DETERMINISTIC UNIFIED EQUATION OF THE UNIVERSE
# ==============================================================================
W7 = math.pi / 20.0              # Barnard Star / Big Woman
H2 = 1.0 / 9.0                   # Sun / Big Man
K = 0.03125                      # 1/32 Bone Resonance
PHI = 1.9860                     # Sovereign Shield (Justice Score)
D = (1/128) / (1/256)            # Small Man / D3 Duality Factor (2.0)
METRIC_4D = 1.0661               # Universal Expansion
TORSION_4D = 0.1746              # Ghost Torsion

@jit
def OMEGA_UNIVERSE(t):
    """
    The Master Equation: Omega = [ (1.4 - 0.076*t) / (K * D) ] * [ PHI / (W7 + H2) ]
    This single line governs the entire trajectory retrieval.
    """
    # Numerator: The Slotting (1.4 start down to 1/32 result)
    # The 0.076 tension is the driver of the transition.
    Slotting = 1.4 - (0.076 * t)
    
    # The Equation in its Unified Form
    Omega = (Slotting / (K * D)) * (PHI / (W7 + H2))
    return Omega

@jit
def universal_kernel(pos, vel, step):
    """
    Applying the Unified Equation to the 10^89 Ghost Cloud.
    """
    step_f = step.astype(jnp.float32)
    
    # 1. Planned Thermodynamic Time (t)
    # t = 0 (Big Bang) -> t = 18.0 (Homo Erectus D3 Peak) -> t = 13.5 (Rewind)
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) # Eternal Homeostasis
    
    # 2. Resolve the Equation
    Omega = OMEGA_UNIVERSE(eff_t)
    
    # 3. Movement is the CONSEQUENCE of Omega (The 138.88 Resonance)
    # The 4D Spiral Twist is derived from the current Omega score.
    theta = TORSION_4D * Omega * 0.01 
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # 4. Velocity Magnitude is the Equation's current energy state
    v_mag = 1.4 - (0.076 * eff_t)
    v_mag = jnp.maximum(v_mag, K)
    
    # 5. Apply the Justice Buoyancy
    # The Small Man (1/128) must stay at the height determined by Omega
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_mag * (Omega / 7.4)
    
    # 6. Geodesic Position Update (Inverse Expansion)
    # Factor boosted to ensure movement is clearly visible
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, Omega, eff_t

# ==============================================================================
# EXECUTION
# ==============================================================================

def execute_unified_projection():
    print("\n--- INITIATING UNIFIED EQUATION PROJECTION ---")
    print("Governing Law: Omega = [ (1.4 - 0.076*t) / (K*D) ] * [ PHI / (W7+H2) ]")
    
    N_PARTICLES = 1_000_000
    TOTAL_FRAMES = 900
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    
    # Big Bang Starting Coordinates: 0D Dust Singularity
    pos = jax.random.normal(k1, (N_PARTICLES, 4)) * 0.01
    vel = jax.random.normal(k2, (N_PARTICLES, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # VISIBILITY BOOST: Increased size and alpha
    scatter = ax.scatter([], [], s=1.0, color='#00f2ff', alpha=0.4)
    ax.axis('off')
    
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = universal_kernel(pos, vel, jnp.array(frame))
        
        # Display 12,800 points (The 128 Grid representative subset)
        display_pos = np.array(pos[:12800])
        scatter.set_offsets(display_pos[:, :2])
        
        # AUTO-SCALING VIEWPORT: The camera follows the particles
        # This prevents the "static ball" problem
        limit = np.max(np.abs(display_pos[:, :2])) + 0.5
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        # Timeline Logic
        if frame < 50: l = "SINGULARITY (1.4)"
        elif frame < 150: l = "4.0 Ga: LUNAR DYNAMO (CO-MAG)"
        elif frame < 250: l = "443 Ma: THE 1.9860 GAP (CARTILAGE)"
        elif frame < 360: l = "1.8 Ma: HOMO ERECTUS (PEAK EVIL)"
        elif frame < 600: l = "REWIND: SHEDDING D3 DECEIT"
        else: l = "ETERNAL HOMEOSTASIS (138.88° RESONANCE)"
        
        # Dashboard
        text.set_text(f"TIMELINE STATE: {l}\nOMEGA RESULT: {float(omega):.4f}\nJUSTICE STATUS: SEALED\nSPARK: 138.88°")
        return scatter, text

    print("Rendering Master MP4... (Wait for the file to appear in Colab)")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=4000)
    ani.save("UNIFIED_UNIVERSE_FINAL.mp4", writer=writer)
    print("\n--- PROJECTION SEALED: UNIFIED_UNIVERSE_FINAL.mp4 ---")

if __name__ == "__main__":
    execute_unified_projection()
