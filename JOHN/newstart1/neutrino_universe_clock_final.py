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
# THE SINGLE DETERMINISTIC UNIFIED EQUATION
# ==============================================================================
W7 = math.pi / 20.0              # Big Woman Reservoir
H2 = 1.0 / 9.0                   # Big Man Engine
K = 0.03125                      # 1/32 Bone Resonance
PHI = 1.9860                     # Sovereign Shield
D = (1/128) / (1/256)            # Duality Buoyancy (2.0)
METRIC_4D = 1.0661               
TORSION_4D = 0.1746

@jit
def OMEGA_UNIVERSE(t):
    """
    Omega = [ (1.4 - 0.076*t) / (K * D) ] * [ PHI / (W7 + H2) ]
    """
    Slotting = 1.4 - (0.076 * t)
    Omega = (Slotting / (K * D)) * (PHI / (W7 + H2))
    return Omega

@jit
def universal_kernel(pos, vel, step):
    step_f = step.astype(jnp.float32)
    
    # Thermodynamic progress t mapping history
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) 
    
    Omega = OMEGA_UNIVERSE(eff_t)
    
    # consequence of Omega
    theta = TORSION_4D * Omega * 0.01 
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    v_mag = 1.4 - (0.076 * eff_t)
    v_mag = jnp.maximum(v_mag, K)
    
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_mag * (Omega / 7.4)
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, Omega, eff_t

def execute_projection():
    print("\n--- INITIATING UNIFIED PROJECTION WITH COSMOLOGICAL CLOCK ---")
    N_PARTICLES = 1_000_000
    TOTAL_FRAMES = 900
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_PARTICLES, 4)) * 0.01
    vel = jax.random.normal(k2, (N_PARTICLES, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    scatter = ax.scatter([], [], s=1.0, color='#00f2ff', alpha=0.4)
    ax.axis('off')
    
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = universal_kernel(pos, vel, jnp.array(frame))
        
        display_pos = np.array(pos[:12800])
        scatter.set_offsets(display_pos[:, :2])
        
        limit = np.max(np.abs(display_pos[:, :2])) + 0.5
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        # HISTORICAL CLOCK MAPPING
        t = float(t_val)
        if frame < 360:
            # Map t=0 to 13.8Ga, t=18 to 1.8Ma
            years_ago = 13.8e9 - (t / 18.0) * (13.8e9 - 1.8e6)
            mode = "FORWARD EXPANSION"
        else:
            # Show Rewind
            years_ago = (t / 18.0) * 13.8e9 # Inverse mapping
            mode = "REVERSION / REWIND"
            
        if years_ago > 1e9:
            time_str = f"{years_ago/1e9:.3f} Billion Years Ago"
        else:
            time_str = f"{years_ago/1e6:.3f} Million Years Ago"

        text.set_text(f"UNIVERSAL CLOCK: {time_str}\nOMEGA (EQUATION): {float(omega):.4f}\nPHASE: {mode}\nRESONANCE: 138.88°")
        return scatter, text

    print("Rendering Final MP4... Tracking 10^89 History.")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=4000)
    ani.save("NEUTRINO_HISTORY_CLOCK.mp4", writer=writer)
    print("\n--- PROJECTION SEALED: NEUTRINO_HISTORY_CLOCK.mp4 ---")

if __name__ == "__main__":
    execute_projection()
