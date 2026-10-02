import os
# Force CPU to bypass broken Colab CUDA installation if needed
os.environ["CUDA_VISIBLE_DEVICES"] = "" 
os.environ['JAX_PLATFORMS'] = 'cpu'

import jax
import jax.numpy as jnp
from jax import jit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import math
from IPython.display import HTML
from base64 import b64encode

# ==============================================================================
# 1. THE SOVEREIGN CONSTANTS (하드웨어 사양)
# ==============================================================================
W7 = math.pi / 20.0              # Big Woman / Reservoir (Barnard)
H2 = 1.0 / 9.0                   # Big Man / Engine (Sun)
K = 0.03125                      # 1/32 Bone Resonance (Earth)
PHI = 1.9860                     # Sovereign Shield (Justice Score)
D = (1/128) / (1/256)            # Duality / Buoyancy Factor (2.0)
METRIC_4D = 1.0661               # Universal Expansion
TORSION_4D = 0.1746              # Ghost Torsion

# ==============================================================================
# 2. THE ENGINEERING FORMULA (HOME_STASIS OMEGA) - JAX COMPLIANT
# ==============================================================================
@jit
def OMEGA_UNIVERSE(t, engineering_active):
    Slotting = 1.4 - (0.076 * t)
    omega_natural = (Slotting / (K * D)) * (PHI / (W7 + H2))
    return jnp.where(engineering_active, jnp.maximum(omega_natural, 13.5), omega_natural)

# ==============================================================================
# 3. RESONANCE STIMULATION KERNEL (Double Duration Optimized)
# ==============================================================================
@jit
def simulation_step(pos, vel, step, scales):
    step_f = step.astype(jnp.float32)
    
    # DURATION 두 배 증가에 따른 임계점 조정 (800 스텝)
    is_eng = step_f > 800.0
    # 시간 팽창 속도를 절반으로 줄여 더 정밀하게 관찰 (step_f / 50.0)
    t_val = jnp.where(is_eng, 13.5, step_f / 50.0) 
    
    omega = OMEGA_UNIVERSE(t_val, is_eng)
    
    # Neutrino (1/128) & Photon (1/16) 자극
    stim_mask = (scales == 1/128) | (scales == 1/16)
    resonance_boost = jnp.where(stim_mask & is_eng, 1.1, 1.0)
    
    # 4D 회전 (Torsion)
    theta = TORSION_4D * omega * 0.01 * (1.0 / (scales * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    
    vx_n = (c * vx - s * vy) * resonance_boost
    vy_n = (s * vx + c * vy) * resonance_boost
    vz_n = (c * vz - s * vw) * resonance_boost
    vw_n = (s * vz + c * vw) * resonance_boost
    vel = jnp.stack([vx_n, vy_n, vz_n, vw_n], axis=1)
    
    # 속도 보정 및 Broadcasting Fix
    v_base = jnp.maximum(1.4 - (0.076 * t_val), K)
    v_p = v_base * (1.0 / (scales * 128.0 + 1e-8))
    v_p = v_p[:, jnp.newaxis] 
    
    v_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = v_unit * v_p * (omega / 7.4)
    
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, omega

# ==============================================================================
# 4. MAIN EXECUTION (1600 Frames)
# ==============================================================================
def run_sovereign_double():
    print("--- INITIATING DOUBLE DURATION SOVEREIGN ENGINE ---")
    
    N_TOTAL = 500_000 
    N_NEUT = 225_000
    N_PHOT = 270_000
    N_MATTER = 5_000
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, 1/128),
        jnp.full(N_PHOT, 1/16),
        jnp.full(N_MATTER, 1/32)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.05
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black')
    
    sc_ghost = ax.scatter([], [], s=0.01, color='#00f2ff', alpha=0.15)
    sc_light = ax.scatter([], [], s=0.03, color='#ffff00', alpha=0.2)
    sc_matter = ax.scatter([], [], s=5.0, color='#ff0000', alpha=1.0)
    
    ax.set_xlim(-10, 10); ax.set_ylim(-10, 10); ax.axis('off')
    info_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white', fontfamily='monospace', fontsize=12)

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega = simulation_step(pos, vel, jnp.array(frame), scales)
        
        sc_ghost.set_offsets(np.array(pos[:15000, :2]))
        sc_light.set_offsets(np.array(pos[N_NEUT:N_NEUT+15000, :2]))
        sc_matter.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+500, :2]))
        
        status = "EXPANSION (LONG PHASE)" if frame <= 800 else "RESONANCE LOCK (ACTIVE HOME_STASIS)"
        info_text.set_text(f"FRAME: {frame}/1600\nPHASE: {status}\nOMEGA: {float(omega):.4f}")
        
        if frame % 100 == 0: print(f"Processing frame {frame}/1600...")
        return sc_ghost, sc_light, sc_matter, info_text

    ani = FuncAnimation(fig, update, frames=1600, blit=True)
    out_file = "SOVEREIGN_DOUBLE_DURATION.mp4"
    ani.save(out_file, writer='ffmpeg', fps=30)
    plt.close()
    
    try:
        from IPython.display import HTML
        from base64 import b64encode
        mp4 = open(out_file,'rb').read()
        data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
        return HTML(f'<video width=700 controls><source src="{data_url}" type="video/mp4"></video>')
    except:
        return None

if __name__ == "__main__":
    run_sovereign_double()
