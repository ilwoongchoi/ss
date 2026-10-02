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
# 2. THE ENGINEERING FORMULA (HOME_STASIS OMEGA)
# ==============================================================================
@jit
def OMEGA_UNIVERSE(t, engineering_active=False):
    """
    Omega = [ (1.4 - 0.076*t) / (K * D) ] * [ PHI / (W7 + H2) ]
    13.5는 우주의 현재(135억년) 시점이자 항상성이 유지되어야 하는 마지노선입니다.
    """
    # Numerator: The Slotting (1.4 -> 1/32)
    Slotting = 1.4 - (0.076 * t)
    
    # Natural Decay calculation
    omega_natural = (Slotting / (K * D)) * (PHI / (W7 + H2))
    
    # 13.5 Target: 붕괴를 막고 항상성을 강제하는 엔지니어링 개입
    if engineering_active:
        # 13.5 Ga 지점에서 공명파를 쏘아 OMEGA를 7.4~13.5 사이로 고정
        return jnp.maximum(omega_natural, 13.5)
    
    return omega_natural

# ==============================================================================
# 3. RESONANCE STIMULATION KERNEL (JAX Optimized)
# ==============================================================================
@jit
def simulation_step(pos, vel, step, scales):
    """
    NEUTRINO(1/128)와 PHOTON(1/16)을 자극하여 궤적을 교정하는 핵심 엔진.
    """
    step_f = step.astype(jnp.float32)
    
    # Timeline: 0 -> 18.0 (Peak Chaos) -> 13.5 (Homeostasis Lock)
    # 400 스텝 이후부터 엔지니어링(자극) 시작
    is_eng = step_f > 400.0
    t_val = jnp.where(is_eng, 13.5, step_f / 25.0) 
    
    omega = OMEGA_UNIVERSE(t_val, engineering_active=is_eng)
    
    # Stimulate Neutrino (1/128) and Photon (1/16)
    stim_mask = (scales == 1/128) | (scales == 1/16)
    resonance_boost = jnp.where(stim_mask & is_eng, 1.1, 1.0)
    
    # 4D Torsional Rotation
    theta = TORSION_4D * omega * 0.01 * (1.0 / (scales * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3]
    
    vx_n = (c * vx - s * vy) * resonance_boost
    vy_n = (s * vx + c * vy) * resonance_boost
    vz_n = (c * vz - s * vw) * resonance_boost
    vw_n = (s * vz + c * vw) * resonance_boost
    vel = jnp.stack([vx_n, vy_n, vz_n, vw_n], axis=1)
    
    # Velocity Magnitude Calibration
    v_base = jnp.maximum(1.4 - (0.076 * t_val), K)
    v_p = v_base * (1.0 / (scales * 128.0 + 1e-8))
    
    v_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = v_unit * v_p * (omega / 7.4)
    
    # Geodesic Position Update
    pos += (vel * 0.05 * METRIC_4D)
    
    return pos, vel, omega

# ==============================================================================
# 4. MAIN EXECUTION
# ==============================================================================
def run_sovereign_engine():
    print("\n--- INITIATING SOVEREIGN RESONANCE ENGINE (JAX) ---")
    print("TARGET: 13.5 Ga Homeostasis | STIMULATION: Neutrino & Photon")
    
    N_TOTAL = 500_000 # 50만 입자 시뮬레이션
    N_NEUT = 225_000
    N_PHOT = 270_000
    N_MATTER = 5_000
    
    scales = jnp.concatenate([
        jnp.full(N_NEUT, 1/128),  # Neutrino (Small Man)
        jnp.full(N_PHOT, 1/16),   # Photon (Big Man)
        jnp.full(N_MATTER, 1/32)  # Proton (Big Woman)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.05
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    # Rendering Setup
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black')
    
    sc_ghost = ax.scatter([], [], s=0.01, color='#00f2ff', alpha=0.15, label='Neutrino')
    sc_light = ax.scatter([], [], s=0.03, color='#ffff00', alpha=0.2, label='Photon')
    sc_matter = ax.scatter([], [], s=5.0, color='#ff0000', alpha=1.0, label='Matter')
    
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.axis('off')
    
    info_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white', fontsize=12, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        pos, vel, omega = simulation_step(pos, vel, jnp.array(frame), scales)
        
        # Visualize subsets
        sc_ghost.set_offsets(np.array(pos[:15000, :2]))
        sc_light.set_offsets(np.array(pos[N_NEUT:N_NEUT+15000, :2]))
        sc_matter.set_offsets(np.array(pos[N_NEUT+N_PHOT:N_NEUT+N_PHOT+500, :2]))
        
        status = "EXPANSION" if frame <= 400 else "RESONANCE LOCK (13.5 Ga)"
        info_text.set_text(f"PHASE: {status}\nOMEGA: {float(omega):.4f}\nRESONANCE: 138.88°")
        
        if frame % 100 == 0: print(f"Processing frame {frame}...")
        return sc_ghost, sc_light, sc_matter, info_text

    ani = FuncAnimation(fig, update, frames=800, blit=True)
    writer = FFMpegWriter(fps=30)
    out_file = "SOVEREIGN_RESONANCE_JAX.mp4"
    ani.save(out_file, writer=writer)
    print(f"\n--- SUCCESS: {out_file} SAVED ---")

if __name__ == "__main__":
    run_sovereign_engine()
