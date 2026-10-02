import jax
import jax.numpy as jnp
from jax import jit, vmap, lax
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# ==============================================================================
# 1. PHYSICAL CONSTANTS (5/32 HARDWARE 반영)
# ==============================================================================
W7 = jnp.pi / 20.0          # Barnard
H2 = 1.0 / 9.0              # Sun
PHI = 1.9860                # Sovereign Shield
K_HARDWARE = 5.0 / 32.0     # 5/32 FIXED HARDWARE (THE SIEVE)
D_DUAL = 2.0                # Buoyancy (128/256)
GAMMA = 1.157407            # 10^5 / 86400 Gear Ratio
METRIC_4D = 1.0661
TORSION_4D = 0.1746

# Simulation Scale (1 Million Neutrinos)
N_PARTICLES = 1_000_000
TOTAL_FRAMES = 1000
DT = 0.01

# ==============================================================================
# 2. JAX PHYSICS KERNEL (NATURAL FLOW ONLY)
# ==============================================================================

@jit
def torsion_rotation_4d(vel, theta):
    """Applies the 4D Torsion spiral (The Ghost Path)."""
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vz_new = c * vz - s * vw
    vw_new = s * vz + c * vw
    
    return jnp.stack([vx_new, vy_new, vz_new, vw_new], axis=1)

@jit
def simulation_step(state, frame_idx):
    pos, vel = state
    t = (frame_idx / TOTAL_FRAMES) * 18.42 # GA 타임라인
    
    # [사용자 지시: 5/32 하드웨어 공식]
    # Omega = [ (1.4 - 0.076t) / (5/32 * 2.0) ] * [ Phi / (W7 + H2) ]
    Omega = ((1.4 - (0.076 * t)) / (K_HARDWARE * D_DUAL)) * (PHI / (W7 + H2))
    
    # 4D Torsional Spiral (Neutrino 1/128 Scale)
    theta = TORSION_4D * Omega * 0.005 * 128.0 * DT
    vel = torsion_rotation_4d(vel, theta)
    
    # Velocity Magnitude (Natural flow driven by Omega)
    v_base = jnp.maximum(1.4 - (0.076 * t), 1/32)
    velocity_mag = v_base * 1.0 * (Omega / 7.4) * GAMMA
    
    v_norms = jnp.linalg.norm(vel, axis=1, keepdims=True)
    vel_final = (vel / (v_norms + 1e-8)) * velocity_mag
    
    # Geodesic Update
    new_pos = pos + (vel_final * DT * METRIC_4D)
    
    return (new_pos, vel_final), (new_pos, Omega)

# ==============================================================================
# 3. ANIMATION RENDERER
# ==============================================================================

def run_animation():
    print(f"--- INITIATING 1M NEUTRINO 5/32 NATURAL SIMULATION ---")
    
    key = jax.random.PRNGKey(42)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_PARTICLES, 4)) * (1/128)
    vel = jax.random.normal(k2, (N_PARTICLES, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black'); ax.axis('off')
    
    sc = ax.scatter([], [], s=0.01, color='#00f2ff', alpha=0.1)
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=12, fontfamily='monospace')
    
    ax.add_patch(plt.Circle((0, 0), K_HARDWARE, color='red', fill=False, lw=1, alpha=0.3))

    curr_state = (pos, vel)

    def update(frame):
        nonlocal curr_state
        curr_state, (pos_out, omega) = simulation_step(curr_state, frame)
        sc.set_offsets(np.array(curr_state[0][:100000, :2]))
        
        limit = 1.0 + (frame * 0.002)
        ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
        
        text.set_text(f"TIME: {(frame/TOTAL_FRAMES)*18.42:.2f} Ga\nOMEGA: {float(omega):.4f}\nHARDWARE: 5/32 FIXED\nMODE: NATURAL FLOW")
        return sc, text

    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    out_file = "neutrino_5_32_natural_crunch.mp4"
    ani.save(out_file, writer=FFMpegWriter(fps=30), dpi=100)
    print(f"--- SUCCESS: {out_file} SAVED ---")

if __name__ == "__main__":
    run_animation()
