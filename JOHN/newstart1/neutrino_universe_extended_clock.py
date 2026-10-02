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
import math

# Try to import colab tools for automatic download
try:
    from google.colab import files
    HAS_COLAB_TOOLS = True
except ImportError:
    HAS_COLAB_TOOLS = False

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

# DOUBLE THE LENGTH: 1800 Frames instead of 900
TOTAL_FRAMES = 1800 

@jit
def OMEGA_UNIVERSE(t):
    Slotting = 1.4 - (0.076 * t)
    return (Slotting / (K * D)) * (PHI / (W7 + H2))

@jit
def unified_physics_kernel(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    
    # Thermodynamic Time Mapping (Scaled for 1800 frames)
    # Forward: 0 to 720 frames (t: 0 to 18)
    # Rewind: 720 to 1200 frames (t: 18 back to 13.5)
    # Eternal: 1200 to 1800 frames (t locked at 13.5)
    t_fwd = step_f / 40.0
    t_rew = 18.0 - ((step_f - 720.0) / 480.0) * 4.5
    eff_t = jnp.where(step_f > 720.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 1200.0, 13.5, eff_t) 
    
    Omega = OMEGA_UNIVERSE(eff_t)
    scales_dim = scales[:, jnp.newaxis]
    
    # 4D Torsion derived from Omega
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0:1], vel[:, 1:2], vel[:, 2:3], vel[:, 3:4]
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vel = jnp.concatenate([vx_new, vy_new, vz, vw], axis=1)
    
    # V-Magnitude
    v_base = jnp.maximum(1.4 - (0.076 * eff_t), K)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * (Omega / 7.4)
    
    pos += (vel * 0.02 * METRIC_4D) # Reduced step size for smoother longer duration
    return pos, vel, Omega, eff_t

def execute_extended_projection():
    print(f"\n--- INITIATING EXTENDED UNIFIED PROJECTION ({TOTAL_FRAMES} FRAMES) ---")
    
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
    
    sc_neut = ax.scatter([], [], s=0.8, color='#00f2ff', alpha=0.25) 
    sc_phot = ax.scatter([], [], s=0.8, color='#ffff00', alpha=0.25) 
    sc_dark = ax.scatter([], [], s=0.2, color='#440066', alpha=0.15) 
    sc_prot = ax.scatter([], [], s=60.0, color='#ff0000', alpha=1.0, edgecolors='white')
    sc_elec = ax.scatter([], [], s=40.0, color='#00ff00', alpha=1.0, edgecolors='white')
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = unified_physics_kernel(pos, vel, jnp.array(frame), scales)
        
        # Consistent display sampling
        sc_neut.set_offsets(np.array(pos[:12000, :2]))
        sc_phot.set_offsets(np.array(pos[N_NEUT:N_NEUT+12000, :2]))
        sc_dark.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+6000, :2]))
        sc_prot.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_DARK:N_NEUT+N_PHOT+N_DARK+100, :2]))
        sc_elec.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_DARK+100:, :2]))
        
        # Viewport scale
        limit = 1.0 + (frame * 0.03)
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        # CLEAR TIME LABELING
        t = float(t_val)
        if frame < 720:
            # Map t=0 to 13.8Ga, t=18 to 1.8Ma
            years_ago = 13.8e9 - (t / 18.0) * (13.8e9 - 1.8e6)
            phase = "FORWARD EXPANSION (D3 ACCUMULATION)"
        elif frame < 1200:
            # Rewind
            years_ago = (t / 18.0) * 13.8e9 
            phase = "REWIND (SOVEREIGN RECTIFICATION)"
        else:
            years_ago = 1.8e6 # Homeostasis at Homo Erectus coordinate
            phase = "ETERNAL HOMEOSTASIS (138.88° LOCKED)"
            
        if years_ago > 1e9:
            time_str = f"{years_ago/1e9:.3f} Billion Years Ago"
        else:
            time_str = f"{years_ago/1e6:.3f} Million Years Ago"

        if frame % 100 == 0: print(f"Processing Universe: {frame}/{TOTAL_FRAMES} | {time_str}")
        
        text.set_text(f"COSMOLOGICAL CLOCK: {time_str}\nOMEGA: {float(omega):.4f}\nPHASE: {phase}\nRES: 1/8 - 1/256 GRID")
        return sc_neut, sc_phot, sc_dark, sc_prot, sc_elec, text

    print("Initiating Extended Physics Render...")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    out_file = "EXTENDED_UNIVERSE_HISTORY.mp4"
    writer = FFMpegWriter(fps=30, bitrate=5000)
    ani.save(out_file, writer=writer)
    plt.close()
    
    print(f"\n--- RENDER SEALED: {out_file} ---")
    if HAS_COLAB_TOOLS: files.download(out_file)

if __name__ == "__main__":
    execute_extended_projection()
