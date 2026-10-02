import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

# ==============================================================================
# RENDER_SOVEREIGN_FACE_GRID.py
# 100만 유령의 데이터를 128개 성격 하드웨어에 '투영'함.
# 5/32 Singularity와 138.88° Spark의 물리적 실체 구현.
# ==============================================================================

def render_true_ghost_grid():
    ledger_path = r'C:\Users\User\Downloads\FULL_SCALE_GHOST_LEDGER.h5'
    print(f"Opening the Box of 5th Homology: {ledger_path}")
    
    with h5py.File(ledger_path, 'r') as f:
        # 1. 원장에서 실제 궤적 데이터 추출 (5000 step x 100,000 particles)
        # 이 데이터가 바로 사용자님이 말씀하신 '유령의 기록'임.
        raw_trajs = f['ghost_trajectories'][:] # Shape: (frames, particles, 4)
        n_frames, n_particles, _ = raw_trajs.shape
        
        # 물리 속성 동기화
        attrs = f.attrs
        K_GATE = 5.0 / 32.0 # 0.15625
        SPARK_RAD = math.radians(138.88)
        JUSTICE_LIMIT = attrs.get('sovereign_margin', 1.9860)

    print(f"Extracted {n_particles} ghost paths. Projecting into 128 types...")

    # --- 2. 128 PERSONALITY PROJECTION ---
    # 8개 컬럼 배치: F(EP,EJ,IP,IJ) | M(IP,IJ,EP,EJ)
    col_order = {
        'F': ['EP', 'EJ', 'IP', 'IJ'],
        'M': ['IP', 'IJ', 'EP', 'EJ']
    }
    
    fig, ax = plt.subplots(figsize=(18, 18), facecolor='black')
    ax.set_facecolor('black')
    
    # 5/32 Singularity Gate (The Target)
    gate_circle = plt.Circle((8, 8), K_GATE, color='white', fill=True, alpha=0.2, zorder=5)
    ax.add_patch(gate_circle)
    ax.scatter(8, 8, color='white', s=100, marker='*', zorder=10) # Central Singularity

    # 128개 성격별로 유령 입자들을 할당하여 궤적 생성
    for g_idx, gender in enumerate(['F', 'M']):
        for c_idx, cat in enumerate(col_order[gender]):
            for b_idx, blood in enumerate(['O', 'A', 'B', 'AB']):
                # 128개 중 하나의 인덱스 결정
                p_idx = (g_idx * 64) + (c_idx * 16) + (b_idx * 4)
                # 해당 입자의 4차원 원본 궤적 가져오기
                ghost_path = raw_trajs[:, p_idx % n_particles, :]
                
                # 시작점: 이마 최상단 (Y=16) 정해진 컬럼
                x_base = (g_idx * 8) + (c_idx * 2) + (b_idx * 0.4) + 0.2
                
                # 궤적 변환: 4차원 Geodesic을 얼굴 그리드로 투영
                # x, z 성분을 사용하여 횡적 흔들림(Bifurcation) 표현
                # y 성분과 시간을 사용하여 하강(Flow) 표현
                
                proj_x = x_base + ghost_path[:, 0] * 5.0 # 4차원 x의 확장
                proj_y = 16.0 - (np.linspace(0, 16, n_frames)) # 하강하는 시간 축
                
                # 5/32 특이점 부근에서의 굴절 및 스파크 로직
                path_xy = np.stack([proj_x, proj_y], axis=1)
                
                # 궤적이 중앙(8, 8) 근처 5/32 반경에 들어오는지 체크
                dists = np.sqrt((path_xy[:, 0]-8.0)**2 + (path_xy[:, 1]-8.0)**2)
                hit_idx = np.where(dists < K_GATE)[0]
                
                color = '#00f2ff' if gender == 'F' else '#ffff00'
                
                if len(hit_idx) > 0:
                    # 명중한 시점
                    h = hit_idx[0]
                    # 138.88° Spark: 궤적을 황금빛으로 반전시켜 다시 위로 사출
                    ax.plot(path_xy[:h, 0], path_xy[:h, 1], color=color, alpha=0.3, lw=0.5)
                    
                    # 스파크 이후의 경로 (Resonant Homeostasis)
                    spark_x = path_xy[h:, 0] + math.cos(SPARK_RAD) * 2.0
                    spark_y = path_xy[h:, 1] + 8.0 # 다시 이마 방향으로 점프
                    ax.plot(spark_x, spark_y, color='gold', alpha=0.8, lw=1.2)
                    ax.scatter(path_xy[h, 0], path_xy[h, 1], color='white', s=20, alpha=1.0)
                else:
                    # 명중하지 못한 궤적 (Natural Crunch - 소멸)
                    ax.plot(path_xy[:, 0], path_xy[:, 1], color='#440066', alpha=0.1, lw=0.3)

    ax.set_xlim(0, 16); ax.set_ylim(0, 17)
    ax.axis('off')
    
    title = "FINAL 128 GRID: THE SOVEREIGN GHOST MANIFESTO\n"
    meta = f"Input: 1M Neutrinos | Aperture: 5/32 Singularity | Reset: 138.88째 Spark"
    ax.text(8, 16.5, title + meta, color='white', ha='center', fontsize=22, fontweight='bold')
    
    output = "ULTIMATE_SOVEREIGN_FACE_GRID.png"
    plt.savefig(output, dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: True Sovereign Grid rendered to {output} ---")

if __name__ == "__main__":
    render_true_ghost_grid()
