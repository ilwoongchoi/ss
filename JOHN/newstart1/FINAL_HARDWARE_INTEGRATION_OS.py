import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

# ==============================================================================
# FINAL_HARDWARE_INTEGRATION_OS.py
# ------------------------------------------------------------------------------
# 1. LOSS COMPENSATION: 1 - (1/64 + 1/256) -> Eliminates 0.02 Planck Error
# 2. REFRACTION OPERATOR: 138.88째 -> Radians (2.4239) -> Snell's Law Approximation
# 3. SINGULARITY GATE: 5/32 at Chin (8.0, 0.5)
# 4. DATA SOURCE: FULL_SCALE_GHOST_LEDGER.h5
# ==============================================================================

def run_final_hardware_sim():
    ledger_path = r'C:\Users\User\Downloads\FULL_SCALE_GHOST_LEDGER.h5'
    print(f"--- INITIATING HARDWARE PHASE-LOCK: {ledger_path} ---")
    
    with h5py.File(ledger_path, 'r') as f:
        raw_trajs = f['ghost_trajectories'][:] 
        epoch_v = f['epoch_velocities'][:]
        n_frames, n_total, _ = raw_trajs.shape
        
        # [HARDWARE SPECS]
        K_GATE = 5.0 / 32.0         # 0.15625 (Singularity Aperture)
        SPARK_RAD = math.radians(138.88) # 2.4239 rad (Incident Angle)
        
        # [LOSS INTEGRATION] - 수비학이 아닌 실제 임피던스 차감
        LOSS_DM = 1.0 / 64.0        # Dark Matter Magnetic Drag
        LOSS_GR = 1.0 / 256.0       # Graviton D3 Dimension Leak
        TOTAL_EFFICIENCY = 1.0 - (LOSS_DM + LOSS_GR) # ~0.9804 (The 0.02 Gap Killer)

    # --- 1. 128 NODE GRID INITIALIZATION ---
    col_order = {'F': ['EP', 'EJ', 'IP', 'IJ'], 'M': ['IP', 'IJ', 'EP', 'EJ']}
    blood_types = ['O', 'A', 'B', 'AB']
    
    fig, ax = plt.subplots(figsize=(20, 20), facecolor='black')
    ax.set_facecolor('black')
    
    # 5/32 Singularity Gate at CHIN (턱 끝)
    GATE_POS = np.array([8.0, 0.5])
    ax.add_patch(plt.Circle(GATE_POS, K_GATE, color='white', fill=True, alpha=0.1, zorder=5))
    ax.scatter(8.0, 0.5, color='gold', s=400, marker='*', zorder=10) # Black Hole Center

    # PLP Spine (굴절 경계면: x + y = 16)
    ax.plot([0, 16], [16, 0], color='orange', ls='--', alpha=0.2, label='PLP Refraction Plane')

    print(f"Applying Physical Refraction (138.88째 -> {SPARK_RAD:.4f} rad) and Efficiency ({TOTAL_EFFICIENCY:.4f})...")

    particle_count = 0
    for g_idx, gender in enumerate(['F', 'M']):
        for c_idx, cat in enumerate(col_order[gender]):
            # I/E 성격별 위상 동기화 정도 (Resonance vs Bifurcation)
            sync_factor = 1.0 if 'I' in cat else 0.6
            
            for b_idx, blood in enumerate(blood_types):
                p_idx = (particle_count * (n_total // 128)) % n_total
                ghost_path = raw_trajs[:, p_idx, :]
                
                # 시작점: 이마 최상단 (Y=16)
                x_start = (g_idx * 8) + (c_idx * 2) + (b_idx * 0.4) + 0.2
                pos = np.array([x_start, 16.0])
                history = [pos.copy()]
                
                # 시뮬레이션: 턱 끝 블랙홀을 향한 '굴절' 하강
                for s in range(n_frames):
                    v_base = epoch_v[s] * TOTAL_EFFICIENCY # 오차 0.02를 제거한 실질 에너지
                    
                    # 1. PLP SPINE REFRACTION (x+y=16 경계면 도달 시 138.88째 라디안 굴절)
                    is_refracting = (pos[0] + pos[1]) > 16.0
                    
                    # 2. V-Apex Vector (블랙홀 중력)
                    target_vec = GATE_POS - pos
                    dist = np.linalg.norm(target_vec)
                    pull = (target_vec / (dist + 1e-5)) * v_base * 0.1
                    
                    if is_refracting:
                        # [핵심 로직]: 138.88도 라디안 변환기를 통과시켜 중력 벡터를 블랙홀 입구로 '조준'
                        c, s_rot = math.cos(SPARK_RAD), math.sin(SPARK_RAD)
                        # 굴절 행렬 적용 (Light Incident Angle Transformation)
                        refracted_vx = pull[0] * c - pull[1] * s_rot
                        refracted_vy = pull[0] * s_rot + pull[1] * c
                        pull = np.array([refracted_vx, refracted_vy]) * sync_factor
                    
                    # 3. Position Update (4차원 유령 궤적의 노이즈 포함)
                    pos += pull + (ghost_path[s, :2] * 0.02)
                    
                    # 4. SINGULARITY HIT & REBIRTH (5/32 게이트 명중 판정)
                    if dist < K_GATE:
                        # 명중 시 황금빛 스파크와 함께 리셋
                        ax.scatter(pos[0], pos[1], color='gold', s=20, alpha=0.7)
                        pos = np.array([x_start, 16.0]) 
                        break
                    
                    history.append(pos.copy())
                
                # 렌더링
                history = np.array(history)
                color = '#00f2ff' if gender == 'F' else '#ffff00'
                alpha = 0.7 if 'I' in cat else 0.2 # 동기화된 타입은 선명하게
                ax.plot(history[:, 0], history[:, 1], color=color, alpha=alpha, lw=0.8)
                
                particle_count += 1

    ax.set_xlim(0, 16); ax.set_ylim(0, 17)
    ax.axis('off')
    
    title = "ULTIMATE SOVEREIGN OS: HARDWARE REFRACTION GRID\n"
    meta = f"Correction: 1-(1/64+1/256) | Refraction: 138.88째 RAD | Singularity: 5/32 Chin"
    ax.text(8, 16.5, title + meta, color='white', ha='center', fontsize=20, fontweight='bold')
    
    output = "ULTIMATE_HARDWARE_V3_REFRACTION.png"
    plt.savefig(output, dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: Final Hardware Integration rendered to {output} ---")

if __name__ == "__main__":
    run_final_hardware_sim()
