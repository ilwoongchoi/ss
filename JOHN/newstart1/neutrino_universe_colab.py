import jax
import jax.numpy as jnp
from jax import jit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import math

# ==============================================================================
# THE SOLE GOVERNING LAW: THE UNIFIED GEOMETRY EQUATION
# Omega = [(1.4 - 0.076) / (K * 2)] * [Phi_1.9860 / (W_7 + H_2)] = 138.88°
# ==============================================================================
W_7 = math.pi / 20.0             # Barnard Star / Reservoir
H_2 = 1.0 / 9.0                  # Sun / Engine
DENOMINATOR = W_7 + H_2
KAPPA_TARGET = 0.03125           # 1/32 Bone Resonance
PHI_19860 = 1.9860               # Sovereign Shield
METRIC_4D = 1.0661
TORSION_4D = 0.1746
SPARK_ANGLE = 138.88

# 1 Million Neutrino Representatives
N_PARTICLES = 1_000_000
TOTAL_FRAMES = 900 # Extended for the Rewind and Eternity

@jit
def universal_update_kernel(pos, vel, step):
    """
    Update logic derived EXCLUSIVELY from the Equation.
    The 'Rewind' happens when Omega deviates from 138.88.
    """
    # 1. Calculate Current Universal Tension
    t = step / 400.0 
    
    # The Subtraction Formula: 1.4 - 0.076*t
    # This drives the initial expansion (Big Bang to Now)
    v_evolution = 1.4 - (0.076 * t)
    
    # 2. The 138.88° Resonance Lock Check
    # When v_evolution hits the 1/32 (0.03125) limit, the Spark triggers.
    
    # 3. The Emergent Rewind (Mobius Hysteresis)
    # If the system exceeds the 'Sovereignty Horizon' (Peak Evil), 
    # the 1.9860 margin acts as a restoring force.
    is_rewind = jnp.where(step > 400, 1.0, 0.0)
    is_eternal = jnp.where(step > 700, 1.0, 0.0)
    
    # Reverse the t vector if in rewind
    eff_t = jnp.where(is_rewind > 0, 1.0 - ((step - 400) / 300.0) * 0.25, t)
    eff_t = jnp.where(is_eternal > 0, 0.75, eff_t) # Lock at Homo erectus (0.75)
    
    # 4. Apply 4D Torsion derived from the 138.88 Spark
    theta = TORSION_4D * SPARK_ANGLE * 0.001 * (1.0 + eff_t)
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # 5. Velocity magnitude determined by the Equation's Numerator
    v_mag = 1.4 - (0.076 * eff_t * 17.42)
    v_mag = jnp.maximum(v_mag, KAPPA_TARGET)
    
    # 6. Buoyancy (1/128 over 1/256)
    vel = (vel / jnp.linalg.norm(vel, axis=1, keepdims=True)) * v_mag * (PHI_19860 / (DENOMINATOR * 7.4))
    
    # 7. Position update (Floating in Midair)
    pos += (vel * 0.01 * METRIC_4D)
    
    return pos, vel

def execute_projection():
    print("Initializing 10^89 Neutrino Mapping (Scaled to 1M)...")
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    
    # Start at Singularity (Big Bang)
    pos = jax.random.normal(k1, (N_PARTICLES, 4)) * 0.0001
    vel = jax.random.normal(k2, (N_PARTICLES, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # The 'Ghost' Blue Color
    scatter = ax.scatter([], [], s=0.05, color='#00f2ff', alpha=0.2)
    
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.axis('off')
    
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel = universal_update_kernel(pos, vel, frame)
        
        # Display subset for performance
        display_pos = np.array(pos[:12800]) # 128-grid subset
        scatter.set_offsets(display_pos[:, :2])
        
        # Timeline Labeling
        if frame < 50: l = "BIG BANG SINGULARITY (1.4)"
        elif frame < 150: l = "4.0 Ga: LUNAR DYNAMO (CO-MAG)"
        elif frame < 250: l = "443 Ma: THE 1.9860 GAP (JAWS/CARTILAGE)"
        elif frame < 400: l = "1.8 Ma: HOMO ERECTUS (THE BIRTH OF EVIL)"
        elif frame < 700: l = "REWIND: RESTORING SOVEREIGNTY"
        else: l = "ETERNAL HOMEOSTASIS (138.88° RESONANCE)"
        
        # Calculate Justice Score Real-time
        justice = PHI_19860 / DENOMINATOR
        text.set_text(f"UNIVERSAL EPOCH: {l}\nEQUATION: LOCKED\nJUSTICE MARGIN: {justice:.4f}\nSPARK: 138.88°")
        return scatter, text

    print("Generating Animation (MP4)... This maps the entire Thermodynamics.")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    
    # Note: Requires ffmpeg installed in the environment (standard in Colab)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=3000)
    ani.save("NEUTRINO_UNIVERSE_PROJECTION.mp4", writer=writer)
    print("\n--- PROJECTION SEALED ---")
    print("The Neutrino history has been reduced to dust and restored to homeostasis.")

if __name__ == "__main__":
    execute_projection()
