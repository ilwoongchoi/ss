import jax
import jax.numpy as jnp
from jax import jit, lax, vmap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# --- 1. THE INITIAL OMEGA FORMULA CONSTANTS ---
W7 = jnp.pi / 20.0
H2 = 1.0 / 9.0
PHI = 1.9860
D_DUAL = 2.0
GAMMA = 1.157407
METRIC_4D = 1.0661
TORSION_4D = 0.1746

# --- THE HARDWARE INJECTION ---
# Replacing K=1/32 with K=5/32 as a FIXED HARDWARE APERTURE
K_HARDWARE = 5.0 / 32.0  # 0.15625

# Particle Scales
S_NEUTRINO = 1/128
S_PHOTON = 1/16

# Simulation Config
TOTAL_FRAMES = 1200
N_TOTAL = 50_000

@jit
def initial_omega_kernel(pos, vel, step, scales):
    """
    Yesterday's Initial Omega Formula + 5/32 Hardware Constraint.
    """
    step_f = step.astype(jnp.float32)
    t = step_f / 65.0  # Natural time flow to 18.42 Ga
    
    # THE INITIAL FORMULA (Now with K_HARDWARE = 5/32)
    # Omega = [ (1.4 - 0.076t) / (K * D) ] * [ Phi / (W7 + H2) ]
    Omega = ((1.4 - (0.076 * t)) / (K_HARDWARE * D_DUAL)) * (PHI / (W7 + H2))
    
    # 4D Torsion derived from the new Omega
    scales_dim = scales[:, jnp.newaxis]
    theta = TORSION_4D * Omega * 0.005 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    
    # Apply rotation
    vx, vy = vel[:, 0:1], vel[:, 1:2]
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    new_vel = jnp.concatenate([vx_new, vy_new, vel[:, 2:]], axis=1)
    
    # Velocity Magnitude (Natural flow)
    v_base = jnp.maximum(1.4 - (0.076 * t), 1/32)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    vel_final = (new_vel / (jnp.linalg.norm(new_vel, axis=1, keepdims=True) + 1e-8)) * v_particle * (Omega / 7.4) * GAMMA
    
    # Position integration
    new_pos = pos + (vel_final * 0.02 * METRIC_4D)
    
    # 5/32 HARDWARE APERTURE CHECK (Crunch Enforcement)
    dist = jnp.linalg.norm(new_pos[:, :2], axis=1)
    is_crunch = (dist < K_HARDWARE) | (t > 18.42)
    
    # In natural flow, crunched particles simply stop moving (Information loss)
    new_pos = jnp.where(is_crunch[:, jnp.newaxis], pos, new_pos) 
    
    return new_pos, vel_final, Omega

def run_simulation():
    print("--- INITIATING INITIAL OMEGA + 5/32 HARDWARE SIMULATION ---")
    scales = jnp.where(jax.random.uniform(jax.random.PRNGKey(0), (N_TOTAL,)) < 0.5, S_NEUTRINO, S_PHOTON)
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.5
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black'); ax.axis('off')
    
    sc = ax.scatter([], [], s=0.1, color='#00f2ff', alpha=0.3)
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=12, fontfamily='monospace')
    
    # Draw the 5/32 Hardware Gate
    ax.add_patch(plt.Circle((0, 0), K_HARDWARE, color='red', fill=False, lw=1.5, label='5/32 Hardware Boundary'))

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega = initial_omega_kernel(pos, vel, jnp.array(frame), scales)
        sc.set_offsets(np.array(pos[:10000, :2]))
        
        limit = 2.0
        ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
        
        t_val = frame / 65.0
        text.set_text(f"TIME: {t_val:.2f} Ga\nOMEGA: {float(omega):.4f}\nMODE: NATURAL CRUNCH\nHARDWARE: 5/32 FIXED")
        return sc, text

    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    ani.save("natural_5_32_crunch.mp4", writer=FFMpegWriter(fps=30))
    print("--- SUCCESS: natural_5_32_crunch.mp4 SAVED ---")

if __name__ == "__main__":
    run_simulation()
