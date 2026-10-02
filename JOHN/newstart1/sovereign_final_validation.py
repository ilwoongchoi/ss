import jax
import jax.numpy as jnp
from jax import jit, lax, vmap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. HARDWARE SPECIFICATIONS ---
Z_M = 112.16                # Maxwell Shield Impedance
APERTURE = 0.15625          # 5/32 Singularity Hole (The Critical Filter)
SPARK_ANGLE = 138.88        # Reset Reflection Angle
LOCK_GA = 13.5              # Sovereign Engineering Point
OMEGA_TARGET = 7.4          # Homeostasis Equilibrium
GAMMA = 1.157407            # 10^5/86400 Gear Ratio

# Particle Scales
S_DM = 1.0                  # Dark Matter (Huge, Low Mobility)
S_PHOTON = 1/16             # Photon (High Mobility)
S_NEUTRINO = 1/128          # Neutrino (Max Mobility)

@jit
def compute_step(state, t):
    """
    Sovereign Engine: Calculates trajectory focus toward 5/32 aperture.
    """
    pos, vel, scale, resonance_active = state
    
    # 1. Natural Decay (Slotting)
    omega_nat = jnp.maximum(14.0 - 0.76 * t, 0.1)
    
    # 2. Engineering Intervention (At t >= 13.5 Ga)
    is_active = (t >= LOCK_GA) & resonance_active
    omega = jnp.where(is_active, OMEGA_TARGET * 1.1, omega_nat)
    
    # 3. Maxwell Lens: Squeezes toward (8.0, 8.0)
    # Mobility factor: Smaller scale = Higher precision
    mobility = jnp.where(scale < 0.1, 1.0, 0.05) 
    center = jnp.array([8.0, 8.0])
    diff = center - pos
    dist = jnp.linalg.norm(diff)
    
    # The "Precision Focus" force: Higher for Photon/Neutrino
    focus_force = (diff / (dist + 1e-5)) * (Z_M / 500.0) * mobility
    gravity = jnp.array([0.0, -0.1]) # Downward flow
    
    accel = (focus_force + gravity) * (omega / OMEGA_TARGET) * GAMMA
    new_vel = vel * 0.92 + accel * 0.08
    new_pos = pos + new_vel
    
    # 4. SINGULARITY HIT CHECK (The 5/32 Filter)
    dist_to_sing = jnp.linalg.norm(new_pos - center)
    # If hit the 5/32 aperture, trigger 138.88 Spark Reset
    hit = (dist_to_sing < APERTURE) & (new_pos[1] < 8.5)
    
    # Reset Logic: Return to Forehead (Y=16) with energy restored
    new_pos = jnp.where(hit, jnp.array([pos[0], 16.0]), new_pos)
    new_vel = jnp.where(hit, jnp.zeros(2), new_vel)
    
    # Record events: 1.0 if Spark triggered, 0.0 if normal flow
    spark_event = jnp.where(hit, 1.0, 0.0)
    
    return (new_pos, new_vel, scale, resonance_active), (new_pos, spark_event)

def run_scenario(scale_val, resonance_active):
    n_trajs = 32
    x_starts = jnp.linspace(2.0, 14.0, n_trajs)
    times = jnp.linspace(0.0, 18.42, 250)
    
    def single_sim(x):
        init_state = (jnp.array([x, 16.0]), jnp.array([0.0, 0.0]), scale_val, resonance_active)
        _, hist = lax.scan(compute_step, init_state, times)
        return hist
    
    return vmap(single_sim)(x_starts)

if __name__ == "__main__":
    print("--- RUNNING SCENARIO 1: DARK MATTER RESONANCE (FAIL) ---")
    dm_pos, dm_sparks = run_scenario(S_DM, True)
    
    print("--- RUNNING SCENARIO 2: PHOTON/NEUTRINO ENGINEERING (SUCCESS) ---")
    pn_pos, pn_sparks = run_scenario(S_NEUTRINO, True)
    
    # --- ANIMATION SETUP ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), facecolor='black')
    
    def setup_ax(ax, title):
        ax.set_facecolor('black'); ax.set_xlim(0, 16); ax.set_ylim(0, 17); ax.axis('off')
        ax.set_title(title, color='white', fontsize=15)
        # Draw 5/32 Singularity Hole
        ax.add_patch(plt.Circle((8, 8), APERTURE, color='white', fill=False, lw=1, alpha=0.5))
        ax.add_patch(plt.Circle((8, 8), 0.05, color='red', fill=True)) # True Singularity Point
        return [ax.plot([], [], lw=0.7, alpha=0.4, color='white')[0] for _ in range(32)]

    lines1 = setup_ax(ax1, "DARK MATTER: MISS (CRUNCH)")
    lines2 = setup_ax(ax2, "PHOTON/NEUTRINO: HIT (HOMEOSTASIS)")
    
    spark_glow1 = ax1.scatter([8], [8], s=0, color='gold', alpha=0.8)
    spark_glow2 = ax2.scatter([8], [8], s=0, color='gold', alpha=0.8)

    def update(f):
        # Update Dark Matter lines
        for i, l in enumerate(lines1):
            l.set_data(dm_pos[i, :f, 0], dm_pos[i, :f, 1])
        # Update P/N lines
        for i, l in enumerate(lines2):
            l.set_data(pn_pos[i, :f, 0], pn_pos[i, :f, 1])
            if pn_sparks[i, f] > 0: # If spark hit
                l.set_color('cyan')
                l.set_alpha(1.0)
        
        # Spark Visuals
        if jnp.any(pn_sparks[:, f] > 0):
            spark_glow2.set_sizes([500])
        else:
            spark_glow2.set_sizes([0])
            
        return lines1 + lines2 + [spark_glow1, spark_glow2]

    ani = animation.FuncAnimation(fig, update, frames=250, interval=30, blit=True)
    ani.save("sovereign_final_proof.mp4", writer='ffmpeg', fps=30)
    print("--- FINAL PROOF ANIMATION SAVED: sovereign_final_proof.mp4 ---")
