import os
import sys

# NUCLEAR CPU LOCK: Bypasses broken CUDA
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
# UNIFIED EQUATION: NO GRAVITON FLOOR (D=0 in buoyancy)
# ==============================================================================
W7, H2 = math.pi / 20.0, 1.0 / 9.0
K, PHI = 0.03125, 1.9860
METRIC_4D, TORSION_4D = 1.0661, 0.1746

@jit
def OMEGA_EXTINCTION(t):
    # Without the 1/256 floor, the system has no denominator lock
    # It shreds into chaos
    Slotting = 1.4 - (0.076 * t)
    return (Slotting / K) * (PHI / (W7 + H2))

@jit
def extinction_kernel(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    t = step_f / 20.0
    
    # Omega is now a chaotic dissipation factor
    Omega = OMEGA_EXTINCTION(t)
    scales_dim = scales[:, jnp.newaxis]
    
    # Random D3 shredding noise (because there's no drain)
    key = jax.random.PRNGKey(step.astype(jnp.int32))
    noise = jax.random.normal(key, pos.shape) * 0.1
    
    # 4D Torsion breaks down
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0:1], vel[:, 1:2], vel[:, 2:3], vel[:, 3:4]
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vel = jnp.concatenate([vx_new, vy_new, vz, vw], axis=1) # Half-broken torsion
    
    # V-Magnitude: No 'brake', infinite dissipation
    v_base = 1.4 - (0.076 * t)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * 2.0 # Excessive kinetic energy
    
    pos += (vel * 0.1 * METRIC_4D) + noise
    return pos, vel, Omega

def execute_extinction_projection():
    print("\n--- INITIATING NO-GRAVITON EXTINCTION PROJECTION ---")
    
    N_NEUT, N_PHOT = 499_900, 499_900
    N_PROT, N_ELEC = 100, 100
    N_TOTAL = N_NEUT + N_PHOT + N_PROT + N_ELEC
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, 1/128), jnp.full(N_PHOT, 1/16),
        jnp.full(N_PROT, 1/32), jnp.full(N_ELEC, 1/8)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black')
    
    sc_neut = ax.scatter([], [], s=0.2, color='#00f2ff', alpha=0.2) 
    sc_phot = ax.scatter([], [], s=0.2, color='#ffff00', alpha=0.2) 
    sc_prot = ax.scatter([], [], s=30.0, color='#ff0000', alpha=1.0, edgecolors='white')
    sc_elec = ax.scatter([], [], s=15.0, color='#00ff00', alpha=1.0, edgecolors='white')
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='red', fontsize=12, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        if frame % 50 == 0:
            print(f"Shredding Progress: {frame}/400...")
            
        pos, vel, omega = extinction_kernel(pos, vel, jnp.array(frame), scales)
        
        sc_neut.set_offsets(np.array(pos[:15000, :2]))
        sc_phot.set_offsets(np.array(pos[N_NEUT:N_NEUT+15000, :2]))
        sc_prot.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+100, :2]))
        sc_elec.set_offsets(np.array(pos[N_NEUT+N_PHOT+100:, :2]))
        
        limit = 1.0 + (frame * 0.2) # Zoom out infinitely
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        text.set_text(f"DISSIPATION DETECTED\nERROR: NO 1/256 GRAVITON FLOOR\nOMEGA: {float(omega):.4f}\nRESULT: EXTINCTION")
        return sc_neut, sc_phot, sc_prot, sc_elec, text

    print("Rendering Shredding MP4...")
    ani = FuncAnimation(fig, update, frames=400, blit=True)
    
    output_filename = "GRAVITON_COLLAPSE.mp4"
    writer = FFMpegWriter(fps=30, bitrate=4000)
    ani.save(output_filename, writer=writer)
    
    plt.close()
    print(f"\n--- VOID SEALED: {output_filename} ---")
    
    if HAS_COLAB_TOOLS:
        print("Downloading video now...")
        files.download(output_filename)

if __name__ == "__main__":
    execute_extinction_projection()
