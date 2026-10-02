import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

def render_final_ghost_grid():
    ledger_path = r'C:\Users\User\Downloads\FULL_SCALE_GHOST_LEDGER.h5'
    print(f"Accessing Deterministic Ledger: {ledger_path}")
    
    with h5py.File(ledger_path, 'r') as f:
        # 실제 궤적 데이터 로드 (frames, particles, 4)
        # 100만 개 중 128개를 샘플링하기 위해 간격 조정
        raw_data = f['ghost_trajectories'][:] 
        n_frames, n_total_particles, _ = raw_data.shape
        
        K_GATE = 5.0 / 32.0 # 0.15625
        SPARK_RAD = math.radians(138.88)

    print(f"Data Loaded. Frames: {n_frames}, Sampled Particles: {n_total_particles}")

    # 128개 성격 레이아웃 (사용자 지시 컬럼)
    col_order = {
        'F': ['EP', 'EJ', 'IP', 'IJ'],
        'M': ['IP', 'IJ', 'EP', 'EJ']
    }
    
    fig, ax = plt.subplots(figsize=(16, 16), facecolor='black')
    ax.set_facecolor('black')
    
    # 5/32 하드웨어 게이트 (Singularity)
    ax.add_patch(plt.Circle((8, 8), K_GATE, color='red', fill=False, lw=2, alpha=0.8))
    ax.scatter(8, 8, color='white', s=50, marker='*')

    # 궤적들이 화면에 보이도록 스케일링 계수 산출 (데이터 기반)
    # 데이터의 최대 변화량을 확인하여 0~16 범위 내로 압축
    max_val = np.abs(raw_data).max()
    scale_factor = 8.0 / (max_val + 1e-8) # 중앙(8)으로 수렴하도록 조절

    particle_count = 0
    for g_idx, gender in enumerate(['F', 'M']):
        for c_idx, cat in enumerate(col_order[gender]):
            for b_idx, blood in enumerate(['O', 'A', 'B', 'AB']):
                # 128개 성격에 맞춘 데이터 추출
                p_idx = (particle_count * (n_total_particles // 128)) % n_total_particles
                ghost_path = raw_data[:, p_idx, :]
                
                # 시작점 설정: 이마(Y=16), X는 컬럼별 배치
                x_start = (g_idx * 8) + (c_idx * 2) + (b_idx * 0.4) + 0.2
                
                # 파일의 4차원 데이터를 2차원 얼굴 평면으로 매핑
                # 데이터의 x, y 변화량을 시작점에 더함
                # y는 16에서 아래로 흐르도록 반전
                proj_x = x_start + (ghost_path[:, 0] * scale_factor * 0.5)
                proj_y = 16.0 - (np.abs(ghost_path[:, 1]) * scale_factor * 2.0)
                
                path_xy = np.stack([proj_x, proj_y], axis=1)
                
                # 5/32 게이트 명중 체크 (중심 8, 8 기준)
                dists = np.sqrt((path_xy[:, 0]-8.0)**2 + (path_xy[:, 1]-8.0)**2)
                hit_idx = np.where(dists < K_GATE)[0]
                
                color = '#00f2ff' if gender == 'F' else '#ffff00'
                
                if len(hit_idx) > 0:
                    h = hit_idx[0]
                    # 명중 전: 하강 경로
                    ax.plot(path_xy[:h, 0], path_xy[:h, 1], color=color, alpha=0.4, lw=1.0)
                    # 명중 후: 138.88° 스파크 부활 (위로 튕김)
                    spark_x = path_xy[h:, 0] + math.cos(SPARK_RAD) * 3.0
                    spark_y = path_xy[h:, 1] + 6.0 
                    ax.plot(spark_x, spark_y, color='gold', alpha=0.9, lw=1.5)
                    ax.scatter(path_xy[h, 0], path_xy[h, 1], color='white', s=30, alpha=1.0, zorder=10)
                else:
                    # 명중 실패: Crunch (희미하게 소멸)
                    ax.plot(path_xy[:, 0], path_xy[:, 1], color='#440066', alpha=0.2, lw=0.8)
                
                particle_count += 1

    ax.set_xlim(0, 16); ax.set_ylim(0, 17)
    ax.axis('off')
    
    header = "FINAL 128 GRID: DETERMINISTIC GHOST PROJECTION\n"
    meta = f"Source: FULL_SCALE_GHOST_LEDGER.h5 | Hardware: 5/32 Gate | Logic: 138.88째 Spark"
    ax.text(8, 16.5, header + meta, color='white', ha='center', fontsize=18, fontweight='bold')
    
    plt.savefig("ULTIMATE_SOVEREIGN_FACE_GRID_V2.png", dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()
    print("--- SUCCESS: Final 128 Grid Rendered to ULTIMATE_SOVEREIGN_FACE_GRID_V2.png ---")

if __name__ == "__main__":
    render_final_ghost_grid()
