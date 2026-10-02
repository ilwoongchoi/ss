import os
import sys

# NUCLEAR CPU LOCK: Bypasses broken Colab CUDA installation
os.environ["CUDA_VISIBLE_DEVICES"] = "" 
os.environ['JAX_PLATFORMS'] = 'cpu'

import jax
import jax.numpy as jnp
from jax import jit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import math

# Try to import colab tools for automatic download
try:
    from google.colab import files
    HAS_COLAB_TOOLS = True
except ImportError:
    HAS_COLAB_TOOLS = False

# ==============================================================================
# THE SOLE GOVERNING LAW: THE UNIFIED GEOMETRY EQUATION
# ==============================================================================
W7, H2 = math.pi / 20.0, 1.0 / 9.0
K, PHI = 0.03125, 1.9860
D = (1/128) / (1/256)            # Buoyancy Factor
METRIC_4D, TORSION_4D = 1.0661, 0.1746

# Particle Scales
S_ELECTRON, S_PHOTON = 1/8, 1/16
S_PROTON, S_DARKMAT  = 1/32, 1/64
S_NEUTRINO, S_GRAVITON = 1/128, 1/256

@jit
def unified_kernel(pos, vel, step, scales, filter_mask):
    """
    Update logic with Broadcasting Fix.
    pos: (N, 4), vel: (N, 4), filter_mask: (N, 1)
    """
    step_f = step.astype(jnp.float32)
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) 
    
    # The Equation
    Slotting = 1.4 - (0.076 * eff_t)
    Omega = (Slotting / (K * D)) * (PHI / (W7 + H2))
    
    scales_dim = scales[:, jnp.newaxis]
    
    # 4D Torsion
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0:1], vel[:, 1:2], vel[:, 2:3], vel[:, 3:4]
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vz_new = c * vz - s * vw
    vw_new = s * vz + c * vw
    vel = jnp.concatenate([vx_new, vy_new, vz_new, vw_new], axis=1)
    
    # V-Magnitude with the ACTIVE WAVE FILTER
    v_base = jnp.maximum(1.4 - (0.076 * eff_t), K)
    # The 138.88 resonance actively targets the 1/64 particles.
    # filter_mask is (N, 1), scales_dim is (N, 1) -> result is (N, 1)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8)) * filter_mask
    
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * (Omega / 7.4)
    
    # Geodesic Expansion
    pos += (vel * 0.05 * METRIC_4D)
    
    # Inward pull of Dark Matter (1/64)
    dark_pull = jnp.where(scales_dim == S_DARKMAT, -pos * 0.01, 0.0)
    pos += dark_pull * filter_mask
    
    return pos, vel, Omega

def execute_sovereign_filter():
    print("\n--- INITIATING FIXED ACTIVE HOMEOTASIS PROJECTION ---")
    
    N_TOTAL = 500_000
    N_NEUT, N_PHOT, N_DARK = 200_000, 200_000, 99_800
    N_PROT, N_ELEC, N_GRAV = 50, 50, 100
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, S_NEUTRINO), jnp.full(N_PHOT, S_PHOTON),
        jnp.full(N_DARK, S_DARKMAT),  jnp.full(N_PROT, S_PROTON),
        jnp.full(N_ELEC, S_ELECTRON), jnp.full(N_GRAV, S_GRAVITON)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    sc_neut = ax.scatter([], [], s=0.5, color='#00f2ff', alpha=0.3) 
    sc_phot = ax.scatter([], [], s=0.5, color='#ffff00', alpha=0.3) 
    sc_dark = ax.scatter([], [], s=0.2, color='#440066', alpha=0.2) 
    sc_matter = ax.scatter([], [], s=40.0, color='#ff0000', alpha=1.0, edgecolors='white') 
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=12, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        # Broadcasting Fix: expand filter_mask to (N, 1)
        is_filtered = 1.0 if frame < 360 else 0.0
        filter_mask = jnp.where(scales == S_DARKMAT, is_filtered, 1.0)[:, jnp.newaxis]
        
        pos, vel, omega = unified_kernel(pos, vel, jnp.array(frame), scales, filter_mask)
        
        # Display subsets
        sc_neut.set_offsets(np.array(pos[:10000, :2]))
        sc_phot.set_offsets(np.array(pos[N_NEUT:N_NEUT+10000, :2]))
        sc_dark.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+5000, :2]))
        sc_matter.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_DARK:N_NEUT+N_PHOT+N_DARK+100, :2]))
        
        limit = 1.0 + (frame * 0.05)
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        if frame % 100 == 0: print(f"Processing Universe: {frame}/900...")
        
        status = "BIFURCATION ACTIVE" if frame < 360 else "WAVE EMITTED: SENTINEL REMOVED"
        text.set_text(f"OMEGA: {float(omega):.4f}\nPHASE: {status}\nHOMEOTASIS: LOCKED")
        return sc_neut, sc_phot, sc_dark, sc_matter, text

    print("Rendering Homeostatic Universal History...")
    ani = FuncAnimation(fig, update, frames=900, blit=True)
    out_file = "HOMEOSTATIC_UNIVERSE_FINAL.mp4"
    writer = FFMpegWriter(fps=30, bitrate=4000)
    ani.save(out_file, writer=writer)
    plt.close()
    
    print(f"\n--- MISSION COMPLETE: {out_file} ---")
    if HAS_COLAB_TOOLS: files.download(out_file)

if __name__ == "__main__":
    execute_sovereign_filter()
