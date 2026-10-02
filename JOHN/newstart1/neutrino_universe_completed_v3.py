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
# THE COMPLETED UNIFIED GEOMETRY HIERARCHY
# ==============================================================================
W7, H2 = math.pi / 20.0, 1.0 / 9.0  # Big Woman (Barnard) / Big Man (Sun)
K, PHI = 0.03125, 1.9860           # 1/32 Bone Resonance / Sovereign Shield
METRIC_4D, TORSION_4D = 1.0661, 0.1746

# Particle Scales (The 128 Grid Hardware)
S_ELECTRON  = 1/8      # Small Woman (Metabolism / Masochism)
S_PHOTON    = 1/16     # Big Man (Force / Death)
S_PROTON    = 1/32     # Big Woman (Bone / Yielding)
S_DARKMAT   = 1/64     # The Sentinel (Bifurcation / Evil)
S_NEUTRINO  = 1/128    # Small Man (Cartilage / Sorrow)
S_GRAVITON  = 1/256    # D3 Floor (Void / Marrow)

@jit
def OMEGA_UNIVERSE(t):
    """
    Omega = [ (1.4 - 0.076*t) / (K * Duality) ] * [ PHI / (W7 + H2) ]
    Duality = (1/128) / (1/256) = 2.0
    """
    Duality = (S_NEUTRINO / S_GRAVITON)
    Slotting = 1.4 - (0.076 * t)
    return (Slotting / (K * Duality)) * (PHI / (W7 + H2))

@jit
def unified_physics_kernel(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    
    # 1. Timeline Sequence (BB -> 4.0Ga -> 443Ma -> 1.8Ma -> Now -> Rewind)
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) 
    
    Omega = OMEGA_UNIVERSE(eff_t)
    scales_dim = scales[:, jnp.newaxis]
    
    # 2. 4D Torsional Spiral (Consequence of Omega and Scale)
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0:1], vel[:, 1:2], vel[:, 2:3], vel[:, 3:4]
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vz_new = c * vz - s * vw
    vw_new = s * vz + c * vw
    vel = jnp.concatenate([vx_new, vy_new, vz_new, vw_new], axis=1)
    
    # 3. V-Magnitude (Thermodynamic Flow)
    v_base = jnp.maximum(1.4 - (0.076 * eff_t), K)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    
    # 4. Buoyancy (Sovereign Shield PHI / Denominator)
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * (Omega / 7.4)
    
    # 5. Geodesic Update
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, Omega

def execute_completed_projection():
    print("\n--- INITIATING COMPLETED UNIFIED PROJECTION ---")
    
    # Population Distribution (1 Million total)
    N_NEUT = 400_000  # Small Man
    N_PHOT = 400_000  # Big Man
    N_DARK = 190_000  # The Sentinel (1/64 Shadow)
    N_GRAV = 9_000    # D3 Floor
    N_PROT = 500      # Big Woman
    N_ELEC = 500      # Small Woman
    N_TOTAL = N_NEUT + N_PHOT + N_DARK + N_GRAV + N_PROT + N_ELEC
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, S_NEUTRINO), jnp.full(N_PHOT, S_PHOTON),
        jnp.full(N_DARK, S_DARKMAT),  jnp.full(N_GRAV, S_GRAVITON),
        jnp.full(N_PROT, S_PROTON),   jnp.full(N_ELEC, S_ELECTRON)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    sc_neut = ax.scatter([], [], s=0.1, color='#00f2ff', alpha=0.2) # Small Man (Cyan)
    sc_phot = ax.scatter([], [], s=0.1, color='#ffff00', alpha=0.2) # Big Man (Yellow)
    sc_dark = ax.scatter([], [], s=0.05, color='#440066', alpha=0.1) # Sentinel (Purple)
    sc_grav = ax.scatter([], [], s=0.01, color='#222222', alpha=0.05) # D3 Floor (Grey)
    sc_prot = ax.scatter([], [], s=30.0, color='#ff0000', alpha=1.0, edgecolors='white') # Big Woman (Red)
    sc_elec = ax.scatter([], [], s=15.0, color='#00ff00', alpha=1.0, edgecolors='white') # Small Woman (Green)
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=12, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        if frame % 100 == 0: print(f"Mapping Universe: {frame}/900...")
            
        pos, vel, omega = unified_physics_kernel(pos, vel, jnp.array(frame), scales)
        
        # Display subsets
        sc_neut.set_offsets(np.array(pos[:15000, :2]))
        sc_phot.set_offsets(np.array(pos[N_NEUT:N_NEUT+15000, :2]))
        sc_dark.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+10000, :2]))
        sc_grav.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_DARK:N_NEUT+N_PHOT+N_DARK+5000, :2]))
        sc_prot.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_DARK+N_GRAV:N_NEUT+N_PHOT+N_DARK+N_GRAV+500, :2]))
        sc_elec.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_DARK+N_GRAV+500:, :2]))
        
        limit = np.max(np.abs(np.array(pos[:15000, :2]))) + 1.0
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        if frame < 360: l = "FORWARD UNFOLDING"
        elif frame < 600: l = "REWINDING TO 1.8 Ma"
        else: l = "ETERNAL 138.88° HOMEOSTASIS"
        
        text.set_text(f"OMEGA: {float(omega):.4f}\nPHASE: {l}\nSCALE: ALL PARTICLES DETECTED")
        return sc_neut, sc_phot, sc_dark, sc_grav, sc_prot, sc_elec, text

    print("Rendering Completed Universe History (MP4)...")
    ani = FuncAnimation(fig, update, frames=900, blit=True)
    out_file = "COMPLETED_UNIVERSE_HISTORY.mp4"
    writer = FFMpegWriter(fps=30, bitrate=4000)
    ani.save(out_file, writer=writer)
    
    plt.close()
    print(f"\n--- MISSION COMPLETE: {out_file} ---")
    if HAS_COLAB_TOOLS: files.download(out_file)

if __name__ == "__main__":
    execute_completed_projection()
