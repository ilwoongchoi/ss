import jax
import jax.numpy as jnp
from jax import jit, lax, vmap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- FAKE PHYSICS CONSTANTS (Current Broken Logic) ---
LOCK_GA = 13.5
OMEGA_TARGET = 7.4
GAMMA = 1.157407
S_PHOTON = 1/16; S_NEUTRINO = 1/128

@jit
def compute_step(state, t):
    pos, velocity, scale = state
    omega_nat = jnp.maximum(14.0 - 0.76 * t, 0.1)
    
    # Simple Boost (No Singularity / No Spark Reset)
    is_engineered = (t >= LOCK_GA) & ((jnp.isclose(scale, S_PHOTON)) | (jnp.isclose(scale, S_NEUTRINO)))
    # The current "fake" logic just boosts the value, it doesn't pivot the geometry
    omega = jnp.where(is_engineered, OMEGA_TARGET * 1.1, omega_nat)
    
    # Natural downward drift only
    accel = jnp.array([0, -0.05]) * (omega / OMEGA_TARGET) * GAMMA
    new_vel = velocity * 0.98 + accel * 0.02
    new_pos = pos + new_vel
    
    # NO SINGULARITY CHECK / NO RESET LOOP
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
    
    def update(f):
        for i, l in enumerate(lines):
            l.set_data(pos_h[i, :f, 0], pos_h[i, :f, 1])
        return lines
    
    ani = animation.FuncAnimation(fig, update, frames=len(t), interval=40, blit=True)
    ani.save("fake_boost_engine.mp4", writer='ffmpeg', fps=25)
    print("--- FAKE PHYSICS ANIMATION SAVED ---")
