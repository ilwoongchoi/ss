import jax
import jax.numpy as jnp
from jax import jit, lax, vmap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# --- 어제 사용된 상수 그대로 (FULL CLOSURE 기반) ---
W7 = jnp.pi / 20.0
H2 = 1.0 / 9.0
PHI = 1.9860
D = 2.0
METRIC_4D = 1.0661
TORSION_4D = 0.1746
GAMMA = 1.157407
RESONANT_STRENGTH = 1.25

# --- [사용자 지시: 5/32 하드웨어 주입] ---
K = 5.0 / 32.0  # 0.15625 (기존 1/32에서 교체)

# 입자 스케일
S_NEUTRINO = 1/128; S_PHOTON = 1/16; S_DARKMAT = 1/64; S_PROTON = 1/32; S_ELECTRON = 1/8

# 시뮬레이션 설정 (어제와 동일)
TOTAL_FRAMES = 3000
N_TOTAL = 100_000 

@jit
def unified_disarm_kernel(pos, vel, step, scales, filter_mask):
    step_f = step.astype(jnp.float32)
    
    # [어제 로직: Homo Erectus 시간 역행]
    t_fwd = step_f / 66.6  
    t_rew = 18.0 - ((jnp.clip(step_f, 1200, 2200) - 1200.0) / 1000.0) * 4.5
    eff_t = jnp.where(step_f > 1200.0, t_rew, t_fwd)
    eff_t = jnp.where(step_f > 2200.0, 13.5, eff_t)

    # [수정된 방정식: K = 5/32 반영]
    Omega = ((1.4 - (0.076 * eff_t)) / (K * D)) * (PHI / (W7 + H2))
    
    scales_dim = scales[:, jnp.newaxis]
    
    # 4D Torsion
    theta = TORSION_4D * Omega * 0.005 * (1.0 / (scales_dim * 128.0 + 1e-8))
    c, s = jnp.cos(theta), jnp.sin(theta)
    
    vx, vy, vz, vw = vel[:, 0:1], vel[:, 1:2], vel[:, 2:3], vel[:, 3:4]
    vx_new = c * vx - s * vy
    vy_new = s * vx + c * vy
    vz_new = c * vz - s * vw
    vw_new = s * vz + c * vw
    vel = jnp.concatenate([vx_new, vy_new, vz_new, vw_new], axis=1)
    
    # V-Magnitude
    v_base = jnp.maximum(1.4 - (0.076 * eff_t), 1/32)
    v_particle = v_base * (1.0 / (scales_dim * 128.0 + 1e-8))
    
    vel_unit = vel / (jnp.linalg.norm(vel, axis=1, keepdims=True) + 1e-8)
    vel = vel_unit * v_particle * (Omega / 7.4) * GAMMA
    
    # Pos integration
    pos += (vel * 0.015 * METRIC_4D)
    
    # Sentinel Pull
    dark_pull = jnp.where(scales_dim == S_DARKMAT, -pos * 0.01, 0.0)
    pos += dark_pull * filter_mask
    
    return pos, vel, Omega, eff_t

def run_simulation():
    print("--- INITIATING SOVEREIGN 5/32 EXACT REPRO (HOMO ERECTUS) ---")
    scales = jnp.concatenate([
        jnp.full(40000, S_NEUTRINO), jnp.full(40000, S_PHOTON),
        jnp.full(19800, S_DARKMAT),  jnp.full(200, S_PROTON)
    ])
    
    key = jax.random.PRNGKey(13888)
    k1, k2 = jax.random.split(key)
    pos = jax.random.normal(k1, (N_TOTAL, 4)) * 0.01
    vel = jax.random.normal(k2, (N_TOTAL, 4))
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black'); ax.axis('off')
    
    sc_neut = ax.scatter([], [], s=0.5, color='#00f2ff', alpha=0.3)
    sc_phot = ax.scatter([], [], s=0.5, color='#ffff00', alpha=0.3)
    sc_dark = ax.scatter([], [], s=0.2, color='#440066', alpha=0.2)
    
    text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize=12, fontfamily='monospace')

    def update(frame):
        nonlocal pos, vel
        is_filtered = 1.0 if frame < 1200 else (1.0 - RESONANT_STRENGTH)
        filter_mask = jnp.where(scales == S_DARKMAT, is_filtered, 1.0)[:, jnp.newaxis]
        
        pos, vel, omega, t_val = unified_disarm_kernel(pos, vel, jnp.array(frame), scales, filter_mask)
        
        sc_neut.set_offsets(np.array(pos[:10000, :2]))
        sc_phot.set_offsets(np.array(pos[40000:50000, :2]))
        sc_dark.set_offsets(np.array(pos[80000:85000, :2]))
        
        limit = 1.0 + (frame * 0.02)
        ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
        
        status = "BIFURCATION PULL" if frame < 1200 else "RESONANT REWIND (13.5 Ga)"
        text.set_text(f"OMEGA: {float(omega):.4f}\nTIME: {float(t_val):.2f} Ga\nPHASE: {status}\nHARDWARE: 5/32 FIXED")
        return sc_neut, sc_phot, sc_dark, text

    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)
    ani.save("sovereign_5_32_exact_repro.mp4", writer=FFMpegWriter(fps=30), dpi=100)
    print("--- SIMULATION COMPLETE: sovereign_5_32_exact_repro.mp4 SAVED ---")

if __name__ == "__main__":
    run_simulation()
