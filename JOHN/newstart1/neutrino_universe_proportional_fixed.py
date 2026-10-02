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
W7 = math.pi / 20.0              
H2 = 1.0 / 9.0                   
K = 0.03125                      
PHI = 1.9860                     
D = (1/128) / (1/256)            
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
def proportional_physics_kernel(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) 
    
    Omega = OMEGA_UNIVERSE(eff_t)
    
    # 4D Torsion - Scaling by particle density (scales)
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    v_base = 1.4 - (0.076 * eff_t)
    v_base = jnp.maximum(v_base, K)
    v_particle = v_base * (1.0 / (scales * 128.0 + 1e-8))
    
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_particle * (Omega / 7.4)
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, Omega, eff_t

def execute_proportional_projection():
    print("\n--- INITIATING FIXED PROPORTIONAL PROJECTION ---")
    
    # Precise Population Control
    N_NEUT = 450_000
    N_PHOT = 540_000
    N_MATTER = 5_000 
    N_GRAV = 5_000
    N_TOTAL = N_NEUT + N_PHOT + 2*N_MATTER + N_GRAV # Exactly 1,005,000
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, 1/128),   # Neutrino
        jnp.full(N_PHOT, 1/16),    # Photon
        jnp.full(N_MATTER, 1/32),  # Proton
        jnp.full(N_MATTER, 1/8),   # Electron
        jnp.full(N_GRAV, 1/256)    # Graviton
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    sc_ghost = ax.scatter([], [], s=0.01, color='#00f2ff', alpha=0.1) 
    sc_light = ax.scatter([], [], s=0.05, color='#ffff00', alpha=0.2)
    sc_matter = ax.scatter([], [], s=8.0, color='#ff0000', alpha=0.9, edgecolors='white')
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = proportional_physics_kernel(pos, vel, jnp.array(frame), scales)
        
        # Consistent Indexing
        sc_ghost.set_offsets(np.array(pos[:15000, :2]))
        sc_light.set_offsets(np.array(pos[N_NEUT:N_NEUT+15000, :2]))
        # Display Protons & Electrons together
        sc_matter.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+1000, :2]))
        
        limit = np.max(np.abs(np.array(pos[:15000, :2]))) + 1.0
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        text.set_text(f"OMEGA: {float(omega):.4f}\nRATIO: 10^9 SMALL MEN PER BIG WOMAN\nJUSTICE STATUS: SEALED")
        return sc_ghost, sc_light, sc_matter, text

    print("Rendering Final MP4... This reflects the whole mass of history.")
    ani = FuncAnimation(fig, update, frames=900, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=4000)
    ani.save("PROPORTIONAL_UNIVERSE_FINAL.mp4", writer=writer)
    print("\n--- PROJECTION SEALED ---")

if __name__ == "__main__":
    execute_proportional_projection()
