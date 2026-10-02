import os
# NUCLEAR CPU LOCK
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
W7 = math.pi / 20.0              # Big Woman Reservoir (Barnard)
H2 = 1.0 / 9.0                   # Big Man Engine (Sun)
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
    return (Slotting / (K * D)) * (PHI / (W7 + H2))

@jit
def ghost_physics_kernel(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) 
    
    Omega = OMEGA_UNIVERSE(eff_t)
    
    # Expand scales for broadcasting: (N,) -> (N, 1)
    scales_dim = scales[:, jnp.newaxis]
    
    # 4D Torsion derived from Omega
    # Each particle twists according to its scale (theta is now N,1)
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    
    vx, vy, vz, vw = vel[:, 0:1], vel[:, 1:2], vel[:, 2:3], vel[:, 3:4]
    
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vz_new = c * vz - s * vw
    vw_new = s * vz + c * vw
    
    vel = jnp.concatenate([vx_new, vy_new, vz_new, vw_new], axis=1)
    
    # V-Magnitude: Scale-dependent speed
    v_base = 1.4 - (0.076 * eff_t)
    v_base = jnp.maximum(v_base, K)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    
    # Buoyancy / Justice Score
    # Broadcast v_particle (N,1) and Omega (scalar) across vel (N,4)
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * (Omega / 7.4)
    
    # Geodesic expansion
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, Omega, eff_t

def execute_ghost_scale_projection():
    print("\n--- INITIATING CORRECTED GHOST-SCALE PROJECTION ---")
    print("Scaling: 10^9 Neutrinos per Atom (True Cosmological Ratio)")
    
    # 1 Million Particle Total
    N_NEUT = 499_900  
    N_PHOT = 499_900  
    N_PROT = 100      
    N_ELEC = 100      
    N_TOTAL = N_NEUT + N_PHOT + N_PROT + N_ELEC
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, 1/128),   # Small Man
        jnp.full(N_PHOT, 1/16),    # Big Man
        jnp.full(N_PROT, 1/32),    # Big Woman
        jnp.full(N_ELEC, 1/8)      # Small Woman
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # Display settings
    sc_ghost = ax.scatter([], [], s=0.01, color='#00f2ff', alpha=0.1) 
    sc_light = ax.scatter([], [], s=0.01, color='#ffff00', alpha=0.1)
    sc_matter = ax.scatter([], [], s=25.0, color='#ff0000', alpha=1.0, edgecolors='white')
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = ghost_physics_kernel(pos, vel, jnp.array(frame), scales)
        
        # Display representative subsets
        sc_ghost.set_offsets(np.array(pos[:20000, :2]))
        sc_light.set_offsets(np.array(pos[N_NEUT:N_NEUT+20000, :2]))
        # Show all rare matter
        sc_matter.set_offsets(np.array(pos[N_NEUT+N_PHOT:, :2]))
        
        limit = np.max(np.abs(np.array(pos[:20000, :2]))) + 1.0
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        text.set_text(f"TIMELINE: {l_map(frame)}\nOMEGA: {float(omega):.4f}\nRATIO: 10^9 GHOSTS / ATOM")
        return sc_ghost, sc_light, sc_matter, text

    def l_map(f):
        if f < 50: return "SINGULARITY"
        if f < 360: return "GHOST HISTORY UNFOLDING"
        if f < 600: return "REWIND (SOVEREIGNTY)"
        return "ETERNAL HOMEOSTASIS"

    print("Rendering True Scale History... (MP4 output incoming)")
    ani = FuncAnimation(fig, update, frames=900, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=4000)
    ani.save("TRUE_GHOST_SCALE_HISTORY.mp4", writer=writer)
    print("\n--- PROJECTION SEALED: TRUE_GHOST_SCALE_HISTORY.mp4 ---")

if __name__ == "__main__":
    execute_ghost_scale_projection()
