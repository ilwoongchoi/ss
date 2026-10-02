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
    
    # 4D Torsion derived from Omega
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # V-Magnitude: Scale-dependent speed
    v_base = 1.4 - (0.076 * eff_t)
    v_base = jnp.maximum(v_base, K)
    v_particle = v_base * (1.0 / (scales * 128.0 + 1e-8))
    
    # Buoyancy / Justice Score
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_particle * (Omega / 7.4)
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, Omega, eff_t

def execute_ghost_scale_projection():
    print("\n--- INITIATING TRUE GHOST-SCALE PROJECTION ---")
    print("Scaling: Ghosts (99.98%) vs Matter (0.02%)")
    print("This matches the 10^89 vs 10^80 Universal Ratio.")
    
    # 1 Million Particle Total
    N_NEUT = 499_900  # Small Man (Ghost)
    N_PHOT = 499_900  # Big Man (Light)
    N_PROT = 100      # Big Woman (Bone) - Extreme Rarity
    N_ELEC = 100      # Small Woman (Metabolism)
    
    N_TOTAL = N_NEUT + N_PHOT + N_PROT + N_ELEC
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, 1/128),   # Neutrino
        jnp.full(N_PHOT, 1/16),    # Photon
        jnp.full(N_PROT, 1/32),    # Proton
        jnp.full(N_ELEC, 1/8)      # Electron
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # The Sea of Ghosts (Blue/Cyan)
    sc_ghost = ax.scatter([], [], s=0.01, color='#00f2ff', alpha=0.1) 
    # The Sea of Light (Yellow)
    sc_light = ax.scatter([], [], s=0.01, color='#ffff00', alpha=0.1)
    # The Rare Matter (Red/White) - Big dots to make them visible
    sc_matter = ax.scatter([], [], s=20.0, color='#ff0000', alpha=1.0, edgecolors='white', marker='o')
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = ghost_physics_kernel(pos, vel, jnp.array(frame), scales)
        
        # Display subsets
        sc_ghost.set_offsets(np.array(pos[:20000, :2]))
        sc_light.set_offsets(np.array(pos[N_NEUT:N_NEUT+20000, :2]))
        # Show ALL Protons and Electrons (The rare 200 dots)
        sc_matter.set_offsets(np.array(pos[N_NEUT+N_PHOT:, :2]))
        
        limit = np.max(np.abs(np.array(pos[:20000, :2]))) + 1.0
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        text.set_text(f"TIMELINE: {l_map(frame)}\nOMEGA: {float(omega):.4f}\nRATIO: 10^9 NEUTRINOS PER ATOM")
        return sc_ghost, sc_light, sc_matter, text

    def l_map(f):
        if f < 50: return "BIG BANG"
        if f < 360: return "FORWARD EVOLUTION"
        if f < 600: return "REWIND (1.8 Ma)"
        return "ETERNAL HOMEOSTASIS"

    print("Rendering True Scale MP4... Watch how rare the Matter is.")
    ani = FuncAnimation(fig, update, frames=900, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=4000)
    ani.save("GHOST_SCALE_UNIVERSE.mp4", writer=writer)
    print("\n--- PROJECTION SEALED: GHOST_SCALE_UNIVERSE.mp4 ---")

if __name__ == "__main__":
    execute_ghost_scale_projection()
