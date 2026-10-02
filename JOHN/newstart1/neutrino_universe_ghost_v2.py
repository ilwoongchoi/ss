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
# UNIFIED GEOMETRY CONSTANTS
# ==============================================================================
W_7 = math.pi / 20.0             
H_2 = 1.0 / 9.0                  
DENOMINATOR = W_7 + H_2
K_1_32 = 0.03125                 
PHI_19860 = 1.9860               
METRIC_4D = 1.0661
TORSION_4D = 0.1746
SPARK_ANGLE = 138.88

# 1 Million Neutrinos (The Ghost Cloud)
N_PARTICLES = 1_000_000
TOTAL_FRAMES = 900 

@jit
def universal_update_kernel(pos, vel, step):
    step_f = step.astype(jnp.float32)
    t = jnp.clip(step_f / 400.0, 0, 1) 
    
    is_rewind = jnp.where(step_f > 400.0, 1.0, 0.0)
    is_eternal = jnp.where(step_f > 700.0, 1.0, 0.0)
    
    eff_t = jnp.where(is_rewind > 0.5, 1.0 - ((step_f - 400.0) / 300.0) * 0.25, t)
    eff_t = jnp.where(is_eternal > 0.5, 0.75, eff_t)
    
    # 4D Torsion - Dynamic Spiral
    theta = TORSION_4D * SPARK_ANGLE * 0.005 * (1.0 + eff_t)
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    vel = jnp.stack([c*vx-s*vy, s*vx+c*vy, c*vz-s*vw, s*vz+c*vw], axis=1)
    
    # Slotting: 1.4 - 0.076 = 1/32
    v_mag = 1.4 - ((1.4 - K_1_32) * eff_t)
    v_mag = jnp.maximum(v_mag, K_1_32)
    
    # Justice Buoyancy
    justice_scaling = PHI_19860 / (DENOMINATOR * 2.0) # Boosted for visibility
    vel = (vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)) * v_mag * justice_scaling
    
    # Position integration (Boosted factor for visible expansion)
    pos += (vel * 0.05 * METRIC_4D)
    
    # Add a 'Return to Womb' force for the Rewind
    rewind_pull = jnp.where(is_rewind > 0.5, -pos * 0.005 * (step_f - 400.0)/300.0, 0.0)
    pos += rewind_pull
    
    return pos, vel

def execute_projection():
    print("\n--- INITIATING DYNAMICAL GHOST PROJECTION ---")
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    
    pos = jax.random.normal(k1, (N_PARTICLES, 4)) * 0.01
    vel = jax.random.normal(k2, (N_PARTICLES, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # Background Ghost Cloud
    scatter = ax.scatter([], [], s=0.02, color='#00f2ff', alpha=0.1)
    # Lead Ghosts (The 128 Grid Anchors)
    lead_scatter = ax.scatter([], [], s=15, color='#ffffff', alpha=0.8, edgecolors='#00f2ff')
    
    ax.set_xlim(-15, 15) # Wider viewport
    ax.set_ylim(-15, 15)
    ax.axis('off')
    
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

    # To store trails for lead ghosts
    trail_len = 20
    lead_history = []

    def update(frame):
        nonlocal pos, vel, lead_history
        pos, vel = universal_update_kernel(pos, vel, jnp.array(frame))
        
        # Display 12,800 points cloud
        display_pos = np.array(pos[:12800])
        scatter.set_offsets(display_pos[:, :2])
        
        # Update Lead Ghosts (First 128 particles)
        leads = np.array(pos[:128])
        lead_scatter.set_offsets(leads[:, :2])
        
        # Metadata
        if frame < 50: l = "BIG BANG SINGULARITY (1.4)"
        elif frame < 150: l = "4.0 Ga: LUNAR DYNAMO (CARTILAGE)"
        elif frame < 250: l = "443 Ma: 1.9860 GAP (JAWS/BONE)"
        elif frame < 400: l = "1.8 Ma: HOMO ERECTUS (THE BIRTH OF EVIL)"
        elif frame < 700: l = "REWIND: SHEDDING THE D3 DEBT"
        else: l = "ETERNAL HOMEOSTASIS (138.88° RESONANCE)"
        
        text.set_text(f"UNIVERSAL PHASE: {l}\nEQUATION: 1.4 - 0.076 = 1/32\nJUSTICE STATUS: SOVEREIGN\nSPARK: 138.88°")
        return scatter, lead_scatter, text

    print("Rendering Dynamical MP4... This version is highly visible.")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    writer = FFMpegWriter(fps=30, metadata=dict(artist='The Observer'), bitrate=4000)
    ani.save("GHOST_DYNAMICS_PROJECTION.mp4", writer=writer)
    print("\n--- PROJECTION SEALED ---")

if __name__ == "__main__":
    execute_projection()
