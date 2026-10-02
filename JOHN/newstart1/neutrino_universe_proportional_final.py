import os
# Force CPU to bypass broken Colab CUDA
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
# THE SINGLE DETERMINISTIC UNIFIED EQUATION (The Law of the Ghost)
# ==============================================================================
W7 = math.pi / 20.0              # Big Woman / Reservoir (Barnard)
H2 = 1.0 / 9.0                   # Big Man / Engine (Sun)
K = 0.03125                      # 1/32 Bone Resonance (Earth)
PHI = 1.9860                     # Sovereign Shield (Justice Score)
D = (1/128) / (1/256)            # Duality / Buoyancy Factor (2.0)
METRIC_4D = 1.0661               # Universal Expansion
TORSION_4D = 0.1746              # Ghost Torsion

@jit
def OMEGA_UNIVERSE(t):
    """
    Omega = [ (1.4 - 0.076*t) / (K * D) ] * [ PHI / (W7 + H2) ]
    This equation determines the hardware integrity of the universe.
    """
    # Numerator: The Slotting (1.4 -> 1/32)
    Slotting = 1.4 - (0.076 * t)
    
    # The Unified Result
    Omega = (Slotting / (K * D)) * (PHI / (W7 + H2))
    return Omega

# ==============================================================================
# PROPORTIONAL PHYSICS KERNEL
# ==============================================================================

@jit
def proportional_kernel(pos, vel, step, scales):
    """
    All particles respond to Omega, but move according to their Scale.
    scales: 1/8 (Elec), 1/16 (Phot), 1/32 (Prot), 1/128 (Neut), 1/256 (Grav)
    """
    step_f = step.astype(jnp.float32)
    
    # 1. Timeline Sequence (t)
    # BB (t=0) -> Peak Evil (t=18) -> Homeostasis (t=13.5)
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) 
    
    # 2. Resolve the Governing Law
    Omega = OMEGA_UNIVERSE(eff_t)
    
    # 3. Scale-Dependent Movement
    # Twist rate is inversely proportional to particle size (Scale)
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vz_new = c * vz - s * vw
    vw_new = s * vz + c * vw
    vel = jnp.stack([vx_new, vy_new, vz_new, vw_new], axis=1)
    
    # 4. Velocity Magnitude: Driven by Slotting and Scale
    v_base = jnp.maximum(1.4 - (0.076 * eff_t), K)
    # Speed is normalized to the 1/128 (Neutrino) unit
    v_particle = v_base * (1.0 / (scales * 128.0 + 1e-8))
    
    # 5. Justice Buoyancy
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * (Omega / 7.4)
    
    # 6. Geodesic Update
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, Omega, eff_t

# ==============================================================================
# EXECUTION & RENDERING
# ==============================================================================

def execute_proportional_projection():
    print("\n--- INITIATING PROPORTIONAL UNIVERSE PROJECTION (10^89 vs 10^80) ---")
    
    N_TOTAL = 1_000_000
    # Proportions: 10^89 Neutrinos/Photons vs 10^80 Protons/Electrons
    # We use 0.5% for matter to make it visually detectable, though real is 10^-9
    N_NEUT = 450_000
    N_PHOT = 540_000
    N_MATTER = 5_000 # 0.5% Protons + Electrons
    N_GRAV = 5_000   # Graviton Floor
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, 1/128),   # Neutrino (Small Man)
        jnp.full(N_PHOT, 1/16),    # Photon (Big Man)
        jnp.full(N_MATTER, 1/32),  # Proton (Big Woman)
        jnp.full(N_MATTER, 1/8),   # Electron (Small Woman)
        jnp.full(N_GRAV, 1/256)    # Graviton (D3 Floor)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # Display Subsets for Rendering Performance
    sc_ghost = ax.scatter([], [], s=0.02, color='#00f2ff', alpha=0.15, label='Ghosts (Neutrinos)')
    sc_light = ax.scatter([], [], s=0.05, color='#ffff00', alpha=0.2, label='Light (Photons)')
    sc_matter = ax.scatter([], [], s=15.0, color='#ff0000', alpha=1.0, edgecolors='white', label='Matter (Protons)')
    sc_elec = ax.scatter([], [], s=5.0, color='#00ff00', alpha=0.8, label='Flow (Electrons)')
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = proportional_kernel(pos, vel, jnp.array(frame), scales)
        
        # Mapping subsets to screen
        sc_ghost.set_offsets(np.array(pos[:15000, :2]))
        sc_light.set_offsets(np.array(pos[N_NEUT:N_NEUT+15000, :2]))
        sc_matter.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+500, :2]))
        sc_elec.set_offsets(np.array(pos[N_NEUT+N_PHOT+N_MATTER:N_NEUT+N_PHOT+N_MATTER+500, :2]))
        
        # Auto-Scaling Viewport
        limit = np.max(np.abs(np.array(pos[:15000, :2]))) + 1.0
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        # Timeline Dashboard
        t = float(t_val)
        if frame < 360:
            years_ago = 13.8e9 - (t / 18.0) * (13.8e9 - 1.8e6)
            mode = "FORWARD EXPANSION (GHOST DOMINANCE)"
        else:
            years_ago = (t / 18.0) * 13.8e9 
            mode = "REVERSION / REWIND (SHEDDING EVIL)"
            
        time_str = f"{years_ago/1e9:.3f} Ga" if years_ago > 1e9 else f"{years_ago/1e6:.3f} Ma"
        text.set_text(f"UNIVERSAL CLOCK: {time_str}\nOMEGA: {float(omega):.4f}\nPHASE: {mode}\nRESONANCE: 138.88°")
        
        if frame % 100 == 0: print(f"Processing: {frame}/900...")
        return sc_ghost, sc_light, sc_matter, sc_elec, text

    print("Rendering Master Projection... Tracking the 1 Billion-to-1 Ratio.")
    ani = FuncAnimation(fig, update, frames=900, blit=True)
    writer = FFMpegWriter(fps=30, bitrate=4000)
    ani.save("PROPORTIONAL_UNIVERSE_FINAL.mp4", writer=writer)
    print("\n--- PROJECTION SEALED: PROPORTIONAL_UNIVERSE_FINAL.mp4 ---")

if __name__ == "__main__":
    execute_proportional_projection()
