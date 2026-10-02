import jax
import jax.numpy as jnp
from jax import jit, lax, vmap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# --- 1. SOVEREIGN PHYSICAL CONSTANTS (FULL CLOSURE DATA) ---
W7 = jnp.pi / 20.0          
H2 = 1.0 / 9.0              
PHI = 1.9860                
K_GATE = 5.0 / 32.0         # 5/32 Singularity Aperture
D_DUAL = 2.0                
GAMMA = 1.157407            
METRIC_4D = 1.0661
TORSION_4D = 0.1746

# Particle Scales
S_NEUTRINO = 1/128; S_PHOTON = 1/16; S_DARKMAT = 1/64; S_PROTON = 1/32; S_ELECTRON = 1/8

# Simulation Config (Exact matching for 3000 frames logic)
TOTAL_FRAMES = 3000
N_TOTAL = 100_000
N_NEUT, N_PHOT, N_DARK = 40_000, 40_000, 19_800

@jit
def unified_sovereign_kernel(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    scales_dim = scales[:, jnp.newaxis]
    
    # 2. TEMPORAL MAP (The Homo Erectus Rewind Logic)
    # 0-1200: Forward to Crunch (0 to 18 Ga)
    t_fwd = step_f / 66.6 
    # 1200-2200: Disarmament Rewind (18 to 13.5 Ga)
    t_rew = 18.0 - ((jnp.clip(step_f, 1200, 2200) - 1200.0) / 1000.0) * 4.5
    eff_t = jnp.where(step_f > 1200.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 2200.0, 13.5, eff_t)
    
    # 3. MASTER OMEGA (5/32 Reflected)
    # Correcting shapes to (N_TOTAL, 1) to prevent broadcasting errors
    Omega = ((1.4 - (0.076 * eff_t)) / (K_GATE * D_DUAL)) * (PHI / (W7 + H2))
    
    # Resonance Boost (Photon/Neutrino only during Rewind/Stable phase)
    is_engineered = (step_f > 1200.0) & ((scales == S_PHOTON) | (scales == S_NEUTRINO))
    boost = jnp.where(is_engineered, 1.1, 1.0)[:, jnp.newaxis]
    Omega_eff = Omega * boost # (N_TOTAL, 1)
    
    # 4. 4D Torsion
    theta = TORSION_4D * Omega_eff * 0.005 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    
    vx, vy = vel[:, 0:1], vel[:, 1:2]
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    new_vel_rot = jnp.concatenate([vx_new, vy_new, vel[:, 2:]], axis=1)
    
    # 5. Velocity Magnitude
    v_base = jnp.maximum(1.4 - (0.076 * eff_t), 1/32)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    
    vel_unit = new_vel_rot / (jnp.linalg.norm(new_vel_rot, axis=1, keepdims=True) + 1e-8)
    # Omega/7.4 normalization + Gamma Gear
    vel_final = vel_unit * v_particle * (Omega_eff / 7.4) * GAMMA
    
    # 6. Position Update
    new_pos = pos + (vel_final * 0.015 * METRIC_4D)
    
    # 7. Singularity Hit (5/32 Filter)
    dist_to_center = jnp.linalg.norm(new_pos[:, :2], axis=1)
    hit = (dist_to_center < K_GATE) & (step_f > 1200.0)
    
    # Rewind Reset: If hit during engineering, return to forehead state
    reset_pos = jnp.zeros_like(new_pos)
    new_pos = jnp.where(hit[:, jnp.newaxis], reset_pos, new_pos)
    
    return new_pos, vel_final, jnp.mean(Omega_eff), eff_t

def run_simulation():
    print("--- INITIATING SOVEREIGN REWIND (HOMO ERECTUS) SIMULATION ---")
    scales = jnp.concatenate([
        jnp.full(N_NEUT, S_NEUTRINO), jnp.full(N_PHOT, S_PHOTON),
        jnp.full(N_DARK, S_DARKMAT),  jnp.full(N_TOTAL-N_NEUT-N_PHOT-N_DARK, S_PROTON)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.1
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black'); ax.axis('off')
    
    sc_neut = ax.scatter([], [], s=0.1, color='#00f2ff', alpha=0.2)
    sc_phot = ax.scatter([], [], s=0.1, color='#ffff00', alpha=0.2)
    sc_dark = ax.scatter([], [], s=0.05, color='#440066', alpha=0.1)
    
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=12, fontfamily='monospace')
    circle = plt.Circle((0, 0), K_GATE, color='white', fill=False, lw=1, alpha=0.3)
    ax.add_patch(circle)

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega, t_val = unified_sovereign_kernel(pos, vel, jnp.array(frame), scales)
        
        sc_neut.set_offsets(np.array(pos[:5000, :2]))
        sc_phot.set_offsets(np.array(pos[N_NEUT:N_NEUT+5000, :2]))
        sc_dark.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+3000, :2]))
        
        limit = 1.0 + (frame * 0.002)
        ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
        
        if frame < 1200: phase = "NATURAL CRUNCH FLOW"
        elif frame < 2200: phase = "SOVEREIGN TIME REWIND (TO 13.5 Ga)"
        else: phase = "ETERNAL STABILITY (HOMO ERECTUS RESET)"
        
        text.set_text(f"TIME: {float(t_val):.2f} Ga\nOMEGA: {float(omega):.4f}\nPHASE: {phase}\nGATE: 5/32 SINGULARITY")
        return sc_neut, sc_phot, sc_dark, text

    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    out_file = "sovereign_rewind_proof.mp4"
    ani.save(out_file, writer=FFMpegWriter(fps=30), dpi=100)
    print(f"--- SUCCESS: {out_file} SAVED ---")

if __name__ == "__main__":
    run_simulation()
