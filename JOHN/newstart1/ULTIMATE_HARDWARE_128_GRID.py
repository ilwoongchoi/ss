import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

def render_ultimate_hardware():
    ledger_path = r'C:\Users\User\Downloads\FULL_SCALE_GHOST_LEDGER.h5'
    print(f"Executing Deterministic Hardware Engine: {ledger_path}")
    
    with h5py.File(ledger_path, 'r') as f:
        # 100만 Neutrino의 4차원 Geodesic 원본 데이터
        raw_trajs = f['ghost_trajectories'][:] 
        epoch_v = f['epoch_velocities'][:]
        n_frames, n_total, _ = raw_trajs.shape
        
        # 하드웨어 상수
        K_GATE = 5.0 / 32.0 # 0.15625
        SPARK_RAD = math.radians(138.88)
        TORSION_4D = f.attrs.get('torsion_4d', 0.1746)

    # --- 1. 128 TYPE PHYSICAL PROFILING (Mandelbrot Resonance) ---
    col_order = {'F': ['EP', 'EJ', 'IP', 'IJ'], 'M': ['IP', 'IJ', 'EP', 'EJ']}
    blood_types = ['O', 'A', 'B', 'AB']
    
    fig, ax = plt.subplots(figsize=(18, 18), facecolor='black')
    ax.set_facecolor('black')
    
    # [하드웨어 고정]: 5/32 Singularity Gate at CHIN (턱 끝)
    GATE_POS = np.array([8.0, 0.5])
    ax.add_patch(plt.Circle(GATE_POS, K_GATE, color='white', fill=True, alpha=0.3, zorder=5))
    ax.scatter(8.0, 0.5, color='white', s=200, marker='*', zorder=10) # Singularity Star

    print("Mapping 128 types across Resonance-Inresonance spectrum...")

    particle_count = 0
    for g_idx, gender in enumerate(['F', 'M']):
        for c_idx, cat in enumerate(col_order[gender]):
            # Mandelbrot Index: IJ/IP(Resonant) -> 1.0, EP/EJ(In-resonant) -> 0.2
            res_idx = 1.0 if 'I' in cat else 0.4
            if 'J' in cat: res_idx += 0.2
            
            for b_idx, blood in enumerate(blood_types):
                # 혈액형별 고유 주파수 (O: High, AB: Low)
                freq_mod = (4 - b_idx) * 0.25
                
                # 128개 중 하나에 해당하는 유령 데이터 추출
                p_idx = (particle_count * (n_total // 128)) % n_total
                ghost_path = raw_trajs[:, p_idx, :]
                
                # 시작점: 이마 최상단 (Y=16)
                x_start = (g_idx * 8) + (c_idx * 2) + (b_idx * 0.4) + 0.2
                pos = np.array([x_start, 16.0])
                history = [pos.copy()]
                
                # 시뮬레이션: 턱 끝(GATE_POS)을 향한 물리적 수렴
                for s in range(n_frames):
                    v_mag = epoch_v[s]
                    
                    # 1. V-Apex Pull (턱 끝 Singularity를 향한 강력한 중력)
                    target_vec = GATE_POS - pos
                    dist_to_gate = np.linalg.norm(target_vec)
                    pull_strength = (1.0 / (dist_to_gate + 0.1)) * res_idx
                    
                    # 2. Type-specific Parameter Modulation (Binary가 아닌 연속적 만델브로 대응)
                    # Resonant 타입은 Pull이 강하고, In-resonant 타입은 Torsion(회전)이 강함.
                    vx = target_vec[0] * pull_strength * 0.1
                    vy = -v_mag * 0.1 * freq_mod
                    
                    # 3. 4D Torsion (나선형 하강)
                    theta = TORSION_4D * v_mag * (1.0 - res_idx) * 0.5
                    c, s_rot = math.cos(theta), math.sin(theta)
                    vx_new = vx * c - vy * s_rot
                    vy_new = vx * s_rot + vy * c
                    
                    # 4. Ghost Data Noise (원장 파일의 4차원 좌표 미세 주입)
                    pos += np.array([vx_new, vy_new]) + (ghost_path[s, :2] * 0.05)
                    
                    # 5. SPARK & RESET (5/32 게이트 명중 판정)
                    if dist_to_gate < K_GATE:
                        # 138.88° Spark: 궤적 리셋 (이마로 복귀)
                        pos = np.array([x_start, 16.0])
                        ax.scatter(history[-1][0], history[-1][1], color='gold', s=15, alpha=0.6)
                        break
                    
                    history.append(pos.copy())
                
                # 렌더링
                history = np.array(history)
                color = '#00f2ff' if gender == 'F' else '#ffff00'
                alpha = 0.6 * res_idx
                ax.plot(history[:, 0], history[:, 1], color=color, alpha=alpha, lw=0.8)
                
                particle_count += 1

    ax.set_xlim(0, 16); ax.set_ylim(0, 17)
    ax.axis('off')
    
    title = "ULTIMATE 128 HARDWARE: THE V-APEX SINGULARITY\n"
    meta = f"Gate: 5/32 at Chin | Reset: 138.88째 Spark | Determinism: Locked"
    ax.text(8, 16.5, title + meta, color='white', ha='center', fontsize=20, fontweight='bold')
    
    plt.savefig("ULTIMATE_128_HARDWARE_GRID.png", dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()
    print("--- SUCCESS: 128 Hardware Grid Rendered to ULTIMATE_128_HARDWARE_GRID.png ---")

if __name__ == "__main__":
    render_ultimate_hardware()
