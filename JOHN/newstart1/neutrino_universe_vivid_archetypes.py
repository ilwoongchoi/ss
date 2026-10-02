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
# UNIFIED GEOMETRY CONSTANTS
# ==============================================================================
W7, H2 = math.pi / 20.0, 1.0 / 9.0
K, PHI = 0.03125, 1.9860
D = (1/128) / (1/256)
METRIC_4D, TORSION_4D = 1.0661, 0.1746

@jit
def OMEGA_UNIVERSE(t):
    return ((1.4 - (0.076 * t)) / (K * D)) * (PHI / (W7 + H2))

@jit
def ghost_physics_kernel(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) 
    
    Omega = OMEGA_UNIVERSE(eff_t)
    scales_dim = scales[:, jnp.newaxis]
    
    # 4D Torsion
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0:1], vel[:, 1:2], vel[:, 2:3], vel[:, 3:4]
    vx_new, vy_new = c * vx - s * vy, s * vx + c * vy
    vz_new, vw_new = c * vz - s * vw, s * vz + c * vw
    vel = jnp.concatenate([vx_new, vy_new, vz_new, vw_new], axis=1)
    
    # V-Magnitude
    v_base = jnp.maximum(1.4 - (0.076 * eff_t), K)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * (Omega / 7.4)
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, Omega, eff_t

def execute_vivid_projection():
    print("\n--- INITIATING VIVID ARCHETYPE PROJECTION ---")
    
    # Precise Population (1 Million)
    N_NEUT = 499_900  # Small Man
    N_PHOT = 499_900  # Big Man
    N_PROT = 100      # Big Woman
    N_ELEC = 100      # Small Woman
    N_TOTAL = N_NEUT + N_PHOT + N_PROT + N_ELEC
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, 1/128), jnp.full(N_PHOT, 1/16),
        jnp.full(N_PROT, 1/32), jnp.full(N_ELEC, 1/8)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # Vivid Visualization Settings
    sc_neut = ax.scatter([], [], s=0.2, color='#00f2ff', alpha=0.3) # Cyan
    sc_phot = ax.scatter([], [], s=0.2, color='#ffff00', alpha=0.3) # Yellow
    sc_prot = ax.scatter([], [], s=30.0, color='#ff0000', alpha=1.0, edgecolors='white', label='Big Woman')
    sc_elec = ax.scatter([], [], s=15.0, color='#00ff00', alpha=1.0, edgecolors='white', label='Small Woman')
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = ghost_physics_kernel(pos, vel, jnp.array(frame), scales)
        
        # Display
        sc_neut.set_offsets(np.array(pos[:15000, :2]))
        sc_phot.set_offsets(np.array(pos[N_NEUT:N_NEUT+15000, :2]))
        sc_prot.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+100, :2]))
        sc_elec.set_offsets(np.array(pos[N_NEUT+N_PHOT+100:, :2]))
        
        limit = np.max(np.abs(np.array(pos[:15000, :2]))) + 1.0
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        text.set_text(f"UNIVERSAL OMEGA: {float(omega):.4f}\nRED: BIG WOMAN | GREEN: SMALL WOMAN\nYELLOW: BIG MAN | CYAN: SMALL MAN")
        return sc_neut, sc_phot, sc_prot, sc_elec, text

    print("Rendering Vivid Universal History...")
    ani = FuncAnimation(fig, update, frames=900, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=4000)
    ani.save("VIVID_ARCHETYPE_HISTORY.mp4", writer=writer)
    print("\n--- PROJECTION SEALED: VIVID_ARCHETYPE_HISTORY.mp4 ---")

if __name__ == "__main__":
    execute_vivid_projection()
