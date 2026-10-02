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
# THE SINGLE DETERMINISTIC UNIFIED EQUATION (GLOBAL DRIVER)
# ==============================================================================
W7 = math.pi / 20.0              # Big Woman (Proton Reservoir)
H2 = 1.0 / 9.0                   # Big Man (Photon Engine)
K = 0.03125                      # 1/32 Bone Resonance
PHI = 1.9860                     # Sovereign Shield
D = (1/128) / (1/256)            # Duality Factor (2.0)
METRIC_4D = 1.0661
TORSION_4D = 0.1746

@jit
def OMEGA_UNIVERSE(t):
    """
    Omega = [ (1.4 - 0.076*t) / (K * D) ] * [ PHI / (W7 + H2) ]
    This is the ONLY governing law for all particles.
    """
    Slotting = 1.4 - (0.076 * t)
    Omega = (Slotting / (K * D)) * (PHI / (W7 + H2))
    return Omega

# ==============================================================================
# MULTI-PARTICLE PHYSICS KERNEL
# ==============================================================================

@jit
def multi_particle_kernel(pos, vel, step, scales):
    """
    All particles respond to Omega, but move according to their Scale.
    scales: 1/8 (Elec), 1/16 (Phot), 1/32 (Prot), 1/128 (Neut), 1/256 (Grav)
    """
    step_f = step.astype(jnp.float32)
    
    # 1. Timeline Sequence
    t_fwd = step_f / 20.0
    t_rew = 18.0 - ((step_f - 360.0) / 240.0) * 4.5
    eff_t = jnp.where(step_f > 360.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 600.0, 13.5, eff_t) 
    
    # 2. Resolve Equation
    Omega = OMEGA_UNIVERSE(eff_t)
    
    # 3. Particle-Specific Physics
    # Torsion twist rate proportional to Omega and particle size
    theta = TORSION_4D * Omega * 0.01 * (1.0 / (scales * 128.0))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # 4. Velocity Magnitude: 1.4 - 0.076 transition
    v_base = 1.4 - (0.076 * eff_t)
    v_base = jnp.maximum(v_base, K)
    
    # Large particles (Proton) are slower, Small Man (Neutrino) is fast
    # Speed is inversely proportional to the scale (1/8 is slower than 1/128)
    v_particle = v_base * (1.0 / (scales * 128.0))
    
    # 5. Justice Buoyancy
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_particle * (Omega / 7.4)
    
    # 6. Geodesic Position Update
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, Omega, eff_t

def execute_multi_particle_projection():
    print("\n--- INITIATING MULTI-PARTICLE UNIFIED PROJECTION ---")
    
    # Distribution of 1 Million particles across the hierarchy
    # 80% Neutrinos (Ghost density), 5% each for the others
    N_TOTAL = 1_000_000
    N_NEUT = 800_000
    N_OTHERS = 50_000
    
    # Assign Scales
    scales = jnp.concatenate([
        jnp.full(N_NEUT, 1/128),   # Neutrino (Small Man)
        jnp.full(N_OTHERS, 1/16),  # Photon (Big Man)
        jnp.full(N_OTHERS, 1/8),   # Electron (Small Woman)
        jnp.full(N_OTHERS, 1/32),  # Proton (Big Woman)
        jnp.full(N_OTHERS, 1/256)  # Graviton (D3 Floor)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # Different Scatters for different particles
    sc_neut = ax.scatter([], [], s=0.02, color='#00f2ff', alpha=0.2, label='Small Man (Neutrino)')
    sc_phot = ax.scatter([], [], s=2.0, color='#ffff00', alpha=0.8, label='Big Man (Photon)')
    sc_elec = ax.scatter([], [], s=1.5, color='#00ff00', alpha=0.6, label='Small Woman (Electron)')
    sc_prot = ax.scatter([], [], s=5.0, color='#ff0000', alpha=0.9, label='Big Woman (Proton)')
    sc_grav = ax.scatter([], [], s=0.01, color='#444444', alpha=0.1, label='Graviton (D3 Floor)')
    
    ax.axis('off')
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = multi_particle_kernel(pos, vel, jnp.array(frame), scales)
        
        # Mapping for display (subsets for performance)
        sc_neut.set_offsets(np.array(pos[:10000, :2]))
        sc_phot.set_offsets(np.array(pos[N_NEUT:N_NEUT+500, :2]))
        sc_elec.set_offsets(np.array(pos[N_NEUT+N_OTHERS:N_NEUT+N_OTHERS+500, :2]))
        sc_prot.set_offsets(np.array(pos[N_NEUT+2*N_OTHERS:N_NEUT+2*N_OTHERS+500, :2]))
        sc_grav.set_offsets(np.array(pos[N_NEUT+3*N_OTHERS:N_NEUT+3*N_OTHERS+500, :2]))
        
        limit = np.max(np.abs(np.array(pos[:10000, :2]))) + 1.0
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        
        text.set_text(f"OMEGA: {float(omega):.4f}\nSPARK: 138.88° LOCKED\nHARDWARE: BONE (1/32) & CARTILAGE (1/128)")
        return sc_neut, sc_phot, sc_elec, sc_prot, sc_grav, text

    print("Rendering Multi-Particle Master MP4... (Wait for UNIFIED_PROJECTION_ALL.mp4)")
    ani = FuncAnimation(fig, update, frames=900, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=4000)
    ani.save("UNIFIED_PROJECTION_ALL.mp4", writer=writer)
    print("\n--- PROJECTION SEALED: UNIFIED_PROJECTION_ALL.mp4 ---")

if __name__ == "__main__":
    execute_multi_particle_projection()
