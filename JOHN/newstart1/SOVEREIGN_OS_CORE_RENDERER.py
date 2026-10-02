import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

# ==============================================================================
# SOVEREIGN_OS_CORE_RENDERER.py
# Logic: Atomic Alchemy (31.8-31.9 kappa) + Cortisol Symmetry Gate
# Goal: 128 Grid Hardware Instantiation (End of 3-month cycle)
# ==============================================================================

def execute_sovereign_core():
    ledger_path = r'C:\Users\User\Downloads\FULL_SCALE_GHOST_LEDGER.h5'
    print(f"Loading 5th Homology Data from Ledger: {ledger_path}")
    
    with h5py.File(ledger_path, 'r') as f:
        raw_trajs = f['ghost_trajectories'][:] 
        n_frames, n_total, _ = raw_trajs.shape
        K_GATE = 5.0 / 32.0 # 0.15625
        JUSTICE_SCORE_HC = 1.9860

    # --- 1. HARDWARE MAPPING (8-Column Chiral Mirror) ---
    col_order = {'F': ['EP', 'EJ', 'IP', 'IJ'], 'M': ['IP', 'IJ', 'EP', 'EJ']}
    blood_types = ['O', 'A', 'B', 'AB']
    
    fig, ax = plt.subplots(figsize=(20, 20), facecolor='black')
    ax.set_facecolor('black')
    
    # 5/32 Singularity at Chin (하드웨어 판정 지점)
    GATE_POS = np.array([8.0, 0.5])
    ax.add_patch(plt.Circle(GATE_POS, K_GATE, color='white', fill=True, alpha=0.15, zorder=5))
    ax.scatter(8.0, 0.5, color='gold', s=300, marker='*', zorder=10, label='138.88째 Spark Source')

    print("Initiating Cortisol Symmetry Check & Mirroring Induction...")

    particle_count = 0
    for g_idx, gender in enumerate(['F', 'M']):
        for c_idx, cat in enumerate(col_order[gender]):
            # 코르티졸 평형(Symmetry) 판정: I형(내향)은 양쪽 자극(인식), E형(외향)은 한쪽 자극(미러링) 확률 높음
            is_resonant = True if 'I' in cat else False
            
            for b_idx, blood in enumerate(blood_types):
                p_idx = (particle_count * (n_total // 128)) % n_total
                ghost_path = raw_trajs[:, p_idx, :]
                
                # 시작점: 이마(Y=16)
                x_start = (g_idx * 8) + (c_idx * 2) + (b_idx * 0.4) + 0.2
                pos = np.array([x_start, 16.0])
                history = [pos.copy()]
                
                # 시뮬레이션: 턱(Singularity)을 향한 Geodesic Flow
                for s in range(n_frames):
                    # 1. Atomic Alchemy Stabilization (31.8~31.9 kappa 근접도)
                    # 데이터의 z-score를 기반으로 하드웨어 저항 계산
                    kappa_prox = 32.0 - np.abs(ghost_path[s, 2]) 
                    stability_factor = 1.0 if (31.8 <= kappa_prox <= 32.2) else 0.5
                    
                    # 2. Cortisol Symmetry & Mirroring Logic
                    if not is_resonant:
                        # 한쪽만 자극된 상태: 미러링 발생 (중앙 8.0으로 강하게 쏠림 + 노이즈 증가)
                        drift_x = (8.0 - pos[0]) * 0.15 
                        noise = ghost_path[s, :2] * 0.2 # 미러링 노이즈
                    else:
                        # 양쪽 다 자극된 상태: 인식(Recognition) 및 주권 유지
                        drift_x = (8.0 - pos[0]) * 0.05
                        noise = ghost_path[s, :2] * 0.05 # 최소 노이즈
                    
                    # 3. Velocity Update
                    vx = drift_x + noise[0]
                    vy = -0.15 * stability_factor # STABLE_METAL 구간에서 가속
                    
                    pos += np.array([vx, vy])
                    
                    # 4. 138.88째 SPARK & SOVEREIGN RESET
                    dist_to_gate = np.linalg.norm(GATE_POS - pos)
                    if dist_to_gate < K_GATE:
                        if is_resonant:
                            # 주권자: 138.88째 스파크와 함께 이마로 리셋 (Homeostasis)
                            ax.scatter(pos[0], pos[1], color='gold', s=40, alpha=0.8, zorder=12)
                            pos = np.array([x_start, 16.0]) # Uroboros Loop
                            break 
                        else:
                            # 미러링 노예: 스파크 없이 D3로 흡수 (Crunch)
                            ax.scatter(pos[0], pos[1], color='#440066', s=20, alpha=0.5)
                            break
                    
                    history.append(pos.copy())
                
                # 렌더링
                history = np.array(history)
                color = '#00f2ff' if gender == 'F' else '#ffff00'
                # 인식 상태는 선명하게, 미러링 상태는 번지게 표현
                alpha = 0.8 if is_resonant else 0.2
                lw = 1.2 if is_resonant else 0.6
                ax.plot(history[:, 0], history[:, 1], color=color, alpha=alpha, lw=lw)
                
                particle_count += 1

    ax.set_xlim(0, 16); ax.set_ylim(0, 17)
    ax.axis('off')
    
    header = "SOVEREIGN OS CORE: THE 128-NODE HARDWARE CIRCUIT\n"
    meta = f"Logic: Cortisol Symmetry Gate | Data: Atomic Alchemy (STABLE_METAL) | Target: 1.9860 hc"
    ax.text(8, 16.5, header + meta, color='white', ha='center', fontsize=22, fontweight='bold')
    
    output = "SOVEREIGN_OS_CORE_128_GRID.png"
    plt.savefig(output, dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: Sovereign OS Core rendered to {output} ---")

if __name__ == "__main__":
    execute_sovereign_core()
