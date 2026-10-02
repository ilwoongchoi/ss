import jax
import jax.numpy as jnp
from jax import jit, lax, vmap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- HARDWARE & SOVEREIGN CONSTANTS ---
Z_M = 112.16                # Maxwell Impedance
APERTURE_5_32 = 0.15625     # Singularity Hole
SPARK_ANGLE = 138.88        # Reflection Angle
LOCK_GA = 13.5              # Sovereign Engineering Point
OMEGA_TARGET = 7.4          # Homeostasis Goal
GAMMA = 1.157407            # Gear Ratio
S_PHOTON = 1/16; S_NEUTRINO = 1/128

@jit
def compute_step(state, t):
    pos, velocity, scale = state
    omega_nat = jnp.maximum(14.0 - 0.76 * t, 0.1)
    
    # Sovereign Engineering (13.5 Ga Lock + Resonance)
    is_engineered = (t >= LOCK_GA) & ((jnp.isclose(scale, S_PHOTON)) | (jnp.isclose(scale, S_NEUTRINO)))
    omega = jnp.where(is_engineered, OMEGA_TARGET * 1.1, omega_nat)
    
    # Maxwell Lens: Squeezes toward (8.0, 8.0)
    center = jnp.array([8.0, 8.0])
    diff = center - pos
    dist = jnp.linalg.norm(diff)
    lens_force = (diff / (dist + 1e-5)) * (Z_M / 800.0)
    
    accel = (lens_force + jnp.array([0, -0.08])) * (omega / OMEGA_TARGET) * GAMMA
    new_vel = velocity * 0.94 + accel * 0.06
    new_pos = pos + new_vel
    
    # Singularity 명중 및 138.88° Spark 리셋
    dist_to_sing = jnp.linalg.norm(new_pos - center)
    hit_singularity = (dist_to_sing < APERTURE_5_32) & (new_pos[1] < 8.5)
    
    # Reset to Forehead (Y=16) on hit
    new_pos = jnp.where(hit_singularity, jnp.array([pos[0], 16.0]), new_pos)
    new_vel = jnp.where(hit_singularity, jnp.zeros(2), new_vel)
    
    return (new_pos, new_vel, scale), (new_pos, omega)

def run_sim():
    n_trajs = 64
    x_starts = jnp.linspace(1.0, 15.0, n_trajs)
    scales = jnp.where(x_starts < 8.0, S_NEUTRINO, S_PHOTON)
    times = jnp.linspace(0.0, 18.42, 200)
    
    def single_sim(x, s):
        _, hist = lax.scan(compute_step, (jnp.array([x, 16.0]), jnp.array([0.0, 0.0]), s), times)
        return hist
    
    pos_hist, _ = vmap(single_sim)(x_starts, scales)
    return times, pos_hist, scales

if __name__ == "__main__":
    t, pos_h, scales = run_sim()
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black'); ax.set_xlim(0, 16); ax.set_ylim(0, 17); ax.axis('off')
    lines = [ax.plot([], [], lw=0.8, alpha=0.5, color='cyan' if s < 1/32 else 'orange')[0] for s in scales]
    sing = ax.add_patch(plt.Circle((8, 8), APERTURE_5_32, color='white', fill=True, alpha=0.5))
    
    def update(f):
        for i, l in enumerate(lines):
            l.set_data(pos_h[i, :f, 0], pos_h[i, :f, 1])
        if t[f] >= LOCK_GA: sing.set_color('gold')
        return lines + [sing]
    
    ani = animation.FuncAnimation(fig, update, frames=len(t), interval=40, blit=True)
    ani.save("sovereign_maxwell_engine.mp4", writer='ffmpeg', fps=25)
    print("--- REAL PHYSICS ANIMATION SAVED ---")
