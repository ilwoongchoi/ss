import os
import sys

# NUCLEAR CPU LOCK: Completely bypass broken CUDA environment
os.environ["CUDA_VISIBLE_DEVICES"] = "" 
os.environ['JAX_PLATFORMS'] = 'cpu'

import jax
import jax.numpy as jnp
from jax import jit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from IPython.display import HTML, display
import math

# ==============================================================================
# UNIFIED GEOMETRY CONSTANTS
# ==============================================================================
W7, H2 = math.pi / 20.0, 1.0 / 9.0
K, PHI = 0.03125, 1.9860
D = (1/128) / (1/256)
METRIC_4D, TORSION_4D = 1.0661, 0.1746

S_ELECTRON, S_PHOTON = 1/8, 1/16
S_PROTON, S_DARKMAT = 1/32, 1/64
S_NEUTRINO, S_GRAVITON = 1/128, 1/256

@jit
def OMEGA_UNIVERSE(t):
    Slotting = 1.4 - (0.076 * t)
    return (Slotting / (K * D)) * (PHI / (W7 + H2))

@jit
def unified_physics_kernel(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) 
    
    Omega = OMEGA_UNIVERSE(eff_t)
    scales_dim = scales[:, jnp.newaxis]
    
    # 4D Torsion derived from Omega
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0:1], vel[:, 1:2], vel[:, 2:3], vel[:, 3:4]
    vx_new, vy_new = c * vx - s * vy, s * vx + c * vy
    vel = jnp.concatenate([vx_new, vy_new, vz, vw], axis=1)
    
    # V-Magnitude: Ghost speed > Matter speed
    v_base = jnp.maximum(1.4 - (0.076 * eff_t), K)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * (Omega / 7.4)
    
    pos += (vel * 0.05 * METRIC_4D)
    return pos, vel, Omega

def execute_final_visible_projection():
    print("\n--- INITIATING HIGH-VISIBILITY UNIFIED PROJECTION ---")
    
    # Total population 500k for faster Colab rendering
    N_TOTAL = 500_000
    N_NEUT, N_PHOT, N_DARK = 200_000, 200_000, 99_800
    N_PROT, N_ELEC = 100, 100
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, S_NEUTRINO), jnp.full(N_PHOT, S_PHOTON),
        jnp.full(N_DARK, S_DARKMAT),  jnp.full(N_PROT, S_PROTON),
        jnp.full(N_ELEC, S_ELECTRON)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black')
    
    # VISIBILITY OVERHAUL: Increased sizes
    sc_neut = ax.scatter([], [], s=0.5, color='#00f2ff', alpha=0.2) 
    sc_phot = ax.scatter([], [], s=0.5, color='#ffff00', alpha=0.2) 
    sc_dark = ax.scatter([], [], s=0.1, color='#440066', alpha=0.1) 
    sc_prot = ax.scatter([], [], s=50.0, color='#ff0000', alpha=1.0, edgecolors='white') # Heavy Red
    sc_elec = ax.scatter([], [], s=30.0, color='#00ff00', alpha=1.0, edgecolors='white') # Vivid Green
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=12, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega = unified_physics_kernel(pos, vel, jnp.array(frame), scales)
        
        # Consistent display sampling
        sc_neut.set_offsets(np.array(pos[:10000, :2]))
        sc_phot.set_offsets(np.array(pos[N_NEUT:N_NEUT+10000, :2]))
        sc_dark.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+5000, :2]))
        sc_prot.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_DARK:N_NEUT+N_PHOT+N_DARK+100, :2]))
        sc_elec.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_DARK+100:, :2]))
        
        # Manual Viewport Expansion
        limit = 1.0 + (frame * 0.05)
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        if frame % 100 == 0: print(f"Rendering Frame: {frame}/900...")
        
        text.set_text(f"OMEGA: {float(omega):.4f}\nSPARK: 138.88°\nSCALES: 1/8 to 1/256 DETECTED")
        return sc_neut, sc_phot, sc_dark, sc_prot, sc_elec, text

    print("Starting Physics Render Engine...")
    ani = FuncAnimation(fig, update, frames=900, blit=True)
    out_file = "DEFINITIVE_UNIVERSE_HISTORY.mp4"
    writer = FFMpegWriter(fps=30, bitrate=4000)
    ani.save(out_file, writer=writer)
    plt.close()
    
    print(f"File Generated: {out_file} ({os.path.getsize(out_file)} bytes)")
    
    # Force automatic download if in Colab
    try:
        from google.colab import files
        files.download(out_file)
    except:
        pass

if __name__ == "__main__":
    execute_final_visible_projection()
