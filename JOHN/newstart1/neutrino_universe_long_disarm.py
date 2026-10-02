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
SPARK = 138.88

# Particle Scales
S_ELECTRON, S_PHOTON = 1/8, 1/16
S_PROTON, S_DARKMAT  = 1/32, 1/64
S_NEUTRINO, S_GRAVITON = 1/128, 1/256

# CONTROL: Extended Time & Resonant Strength
TOTAL_FRAMES = 3000 
RESONANT_STRENGTH = 1.25 # Overdrive Disarmament

@jit
def unified_disarm_kernel(pos, vel, step, scales, filter_mask):
    """
    Long-duration kernel. 
    1.4 - 0.076 = 1/32 mapping scaled to 3000 frames.
    """
    step_f = step.astype(jnp.float32)
    
    # 3000 Frame Temporal Map
    # 0-1200: Forward (BB to Homo Erectus)
    # 1200-2200: Disarmament / Rewind
    # 2200-3000: Eternal Stability
    t_fwd = step_f / 66.6  # Scaled progress
    t_rew = 18.0 - ((jnp.clip(step_f, 1200, 2200) - 1200.0) / 1000.0) * 4.5
    eff_t = jnp.where(step_f > 1200.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 2200.0, 13.5, eff_t) 
    
    # Equation result
    Omega = ((1.4 - (0.076 * eff_t)) / (K * D)) * (PHI / (W7 + H2))
    scales_dim = scales[:, jnp.newaxis]
    
    # 4D Torsion derived from Omega
    theta = TORSION_4D * Omega * 0.005 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0:1], vel[:, 1:2], vel[:, 2:3], vel[:, 3:4]
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vz_new = c * vz - s * vw
    vw_new = s * vz + c * vw
    vel = jnp.concatenate([vx_new, vy_new, vz_new, vw_new], axis=1)
    
    # V-Magnitude
    v_base = jnp.maximum(1.4 - (0.076 * eff_t), K)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * (Omega / 7.4)
    
    # Pos integration (Smaller step for 3000 frames)
    pos += (vel * 0.015 * METRIC_4D)
    
    # Sentinel Pull Logic
    dark_pull = jnp.where(scales_dim == S_DARKMAT, -pos * 0.01, 0.0)
    # The filter mask disarms the pull
    pos += dark_pull * filter_mask
    
    return pos, vel, Omega, eff_t

def execute_extended_disarmament():
    print(f"\n--- INITIATING 100-SECOND UNIVERSAL DISARMAMENT ({TOTAL_FRAMES} FRAMES) ---")
    
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
        # Disarm filter starts at 1200 and lasts for 1000 frames
        is_filtered = 1.0 if frame < 1200 else (1.0 - RESONANT_STRENGTH)
        filter_mask = jnp.where(scales == S_DARKMAT, is_filtered, 1.0)[:, jnp.newaxis]
        
        pos, vel, omega, t_val = unified_disarm_kernel(pos, vel, jnp.array(frame), scales, filter_mask)
        
        # Display subsets
        sc_neut.set_offsets(np.array(pos[:10000, :2]))
        sc_phot.set_offsets(np.array(pos[N_NEUT:N_NEUT+10000, :2]))
        sc_dark.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+5000, :2]))
        sc_matter.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_DARK:N_NEUT+N_PHOT+N_DARK+100, :2]))
        
        limit = 1.0 + (frame * 0.02)
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        if frame % 200 == 0: print(f"Rendering: {frame}/{TOTAL_FRAMES}")
        
        status = "BIFURCATION PULL ACTIVE" if frame < 1200 else "RESONANT DISARMAMENT ENGAGED"
        text.set_text(f"OMEGA: {float(omega):.4f}\nPHASE: {status}\nSTRENGTH: {RESONANT_STRENGTH}\nUNIVERSE: FLOATING")
        return sc_neut, sc_phot, sc_dark, sc_matter, text

    print("Rendering Extended Master MP4...")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    out_file = "LONG_DISARMED_HISTORY.mp4"
    writer = FFMpegWriter(fps=30, bitrate=4000)
    ani.save(out_file, writer=writer)
    plt.close()
    
    print(f"\n--- MISSION COMPLETE: {out_file} ---")
    if HAS_COLAB_TOOLS: files.download(out_file)

if __name__ == "__main__":
    execute_extended_disarmament()
