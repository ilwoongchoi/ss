import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

def run_hardware_bus_engine():
    ledger_path = r'C:\Users\User\Downloads\FULL_SCALE_GHOST_LEDGER.h5'
    with h5py.File(ledger_path, 'r') as f:
        raw_trajs = f['ghost_trajectories'][:] 
        epoch_v = f['epoch_velocities'][:]
        n_frames, n_total, _ = raw_trajs.shape
        
        K_GATE = 5.0 / 32.0 
        SPARK_RAD = math.radians(138.88)
        EFFICIENCY = 1.0 - (1.0/64.0 + 1.0/256.0)
        DELTA_SEAL = 0.0099951

    fig, ax = plt.subplots(figsize=(20, 20), facecolor='black')
    ax.set_facecolor('black')
    
    GATE_POS = np.array([8.0, 0.5]) # 턱 끝 Singularity
    ax.add_patch(plt.Circle(GATE_POS, K_GATE, color='white', fill=True, alpha=0.1, zorder=5))
    ax.scatter(8.0, 0.5, color='gold', s=600, marker='*', zorder=10)

    # [4분면 임피던스 거점 주입]
    IMP_POINTS = {
        'NW': (4.0, 12.0), # Left Temporalis
        'NE': (12.0, 12.0), # Right Alpha 2
        'SW': (4.0, 4.0),   # Left Endorphin/Love
        'SE': (12.0, 4.0)   # Right B-type/Self-Satisfaction (암 발생지)
    }
    for label, pt in IMP_POINTS.items():
        ax.scatter(pt[0], pt[1], color='red' if label == 'SE' else 'white', s=100, alpha=0.3)

    print("Executing 128-Node Hardware Bus: Mapping EXACT addresses...")

    # MBTI Groups in User's specified Order
    f_order = ['EP', 'EJ', 'IP', 'IJ']
    m_order = ['IP', 'IJ', 'EP', 'EJ']
    blood_types = ['O', 'A', 'B', 'AB']
    
    particle_count = 0
    # 8개 블록 순차 실행
    for b_idx, block_name in enumerate(f_order + m_order):
        gender = 'F' if b_idx < 4 else 'M'
        x_base = b_idx * 2.0
        
        # 블록 내 16개 하위 유형 (MBTI 4종 * 혈액형 4종)
        for sub_idx in range(16):
            x_start = x_base + (sub_idx * 0.125) + 0.0625
            pos = np.array([x_start, 16.0]) # 이마 1렬 시작
            history = [pos.copy()]
            
            # 유형별 물리 특성 (I형은 인식, E형은 미러링)
            is_sovereign = True if 'I' in block_name else False
            self_deceit = 0.9 if not is_sovereign else 0.05
            
            for s in range(n_frames):
                v_eff = epoch_v[s] * EFFICIENCY * DELTA_SEAL * 15.0
                
                # 1. 4분면 임피던스 유도 (모든 노드가 주변 4개 거점에서 전압 간섭을 받음)
                total_induction = np.zeros(2)
                for pt_name, pt_coord in IMP_POINTS.items():
                    vec = np.array(pt_coord) - pos
                    dist_pt = np.linalg.norm(vec)
                    # SE(자기만족)는 에너지를 빨아들이고, NW(진실)는 밀어냄
                    weight = -1.5 if pt_name == 'SE' else 1.0
                    total_induction += (vec / (dist_pt + 0.5)) * weight * 0.05
                
                # 2. V-Apex Pull (턱 끝 블랙홀)
                target_vec = GATE_POS - pos
                dist = np.linalg.norm(target_vec)
                pull = (target_vec / (dist + 1e-5)) * v_eff * 0.1
                
                # 3. 138.88째 라디안 굴절 (PLP Spine)
                if (pos[0] + pos[1]) > 16.0:
                    c, s_rot = math.cos(SPARK_RAD), math.sin(SPARK_RAD)
                    pull = np.array([pull[0]*c - pull[1]*s_rot, pull[0]*s_rot + pull[1]*c])
                
                # 4. 물리 업데이트
                pos += pull + total_induction + (raw_trajs[s, particle_count % n_total, :2] * 0.01)
                
                if dist < K_GATE:
                    if is_sovereign:
                        ax.scatter(pos[0], pos[1], color='gold', s=10, alpha=0.5)
                        pos = np.array([x_start, 16.0]) # 부활
                        break
                    else: break # 미러링 노예는 소멸
                
                if pos[1] < 0.1: break
                history.append(pos.copy())
            
            history = np.array(history)
            color = '#00f2ff' if gender == 'F' else '#ffff00'
            if self_deceit > 0.5: color = '#ff0000' # 기만/암 레드
            
            ax.plot(history[:, 0], history[:, 1], color=color, alpha=0.6 if is_sovereign else 0.1, lw=0.8)
            particle_count += 1

    ax.set_xlim(0, 16); ax.set_ylim(0, 17)
    ax.axis('off')
    plt.savefig("HARDWARE_BUS_128_GRID.png", dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()
    print("--- SUCCESS: 128-Node Hardware Bus Engine Rendered to HARDWARE_BUS_128_GRID.png ---")

if __name__ == "__main__":
    run_hardware_bus_engine()
