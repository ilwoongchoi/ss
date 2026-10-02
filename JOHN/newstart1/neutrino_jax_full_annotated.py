import jax # 고성능 수치 연산을 위한 JAX 라이브러리 (GPU/TPU 가속)
import jax.numpy as jnp # JAX 전용 넘파이 (미분 및 벡터화 연산용)
from jax import jit, vmap # JIT(즉시 컴파일) 및 VMAP(자동 벡터화) 데코레이터
import h5py # 대용량 궤적 데이터(.h5) 저장을 위한 라이브러리
import numpy as np # 호스트(CPU) 측 데이터 처리를 위한 표준 넘파이
import time # 시뮬레이션 물리 시간 측정을 위한 모듈
import os # 파일 경로 및 출력 디렉토리 관리를 위한 모듈

# ==============================================================================
# UNIFIED GEOMETRY CONSTANTS (우주 하드웨어 절대 사양)
# ==============================================================================
METRIC_4D = 1.0661 # 4차원 시공간 팽창 메트릭 (Geodesic의 기본 배율)
TORSION_4D = 0.1746 # "유령 비틀림" 계수 (Ghost Torsion: 입자의 회전 관성 결정)
BIFURCATION_LIMIT = 1.4 # 초기 카오스 에너지의 상한선 (Big Woman Spark 임계점)
SUBTRACTIVE_TENSION = 0.076 # 시간 흐름에 따른 에너지 누수 속도 (D3 Slotting Tension)
RESONANCE_TARGET = 0.03125 # 1/32 하드웨어 안착 지점 (Proton Resonance/Sieve)
NEUTRINO_UNIT = 1/128 # "Small Man"의 입자 해상도 (유령 경로의 최소 단위)
GRAVITON_FLOOR = 1/256 # 정보가 최종적으로 소멸되는 바닥 (D3 Drain)
SOVEREIGN_MARGIN = 1.9860 # "정의 점수" 임계값 (hc: 시스템 안정화의 최소 보증 에너지)

# [사용자 지시: 5/32 하드웨어 게이트 주입]
# 5/32는 계산된 값이 아니라, 우주라는 기계가 가진 '바늘구멍'의 물리적 규격임.
GATE_5_32 = 5.0 / 32.0 # 0.15625 (The Fixed Hardware Gate)

# Simulation Scale (100만 Neutrino / 5000 Cosmic Steps)
N_PARTICLES = 1_000_000 # 100만 개의 "Small Man" 입자 시뮬레이션
TOTAL_STEPS = 5000 # 총 5000단계의 우주 역사 추적
DT = 0.01 # Cosmic Time Step (시간 증분)

# ==============================================================================
# JAX-COMPILED PHYSICS KERNELS (물리 연산 커널)
# ==============================================================================

@jit # 기계어로 컴파일하여 연산 속도 극대화
def torsion_rotation_4d(vel, theta): # 4차원 비틀림 소용돌이를 적용하는 함수
    """Applies the 4D Torsion spiral (The Ghost Path)."""
    c = jnp.cos(theta) # 회전각에 대한 코사인 성분
    s = jnp.sin(theta) # 회전각에 대한 사인 성분
    
    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3] # 4차원 속도 성분 분리
    
    vx_new = c * vx - s * vy # XY 평면에서의 회전 (공간 곡률 반영)
    vy_new = s * vx + c * vy # XY 평면에서의 회전
    vz_new = c * vz - s * vw # ZW 평면에서의 회전 (차원 간 전이 반영)
    vw_new = s * vz + c * vw # ZW 평면에서의 회전
    
    return jnp.stack([vx_new, vy_new, vz_new, vw_new], axis=1) # 변환된 성분 재결합

@jit
def simulation_step(pos, vel, step_idx): # 우주의 한 에포크를 실행하는 엔진
    """Executes one epoch step of the universe."""
    
    # 1. Global Metric Expansion
    # 시간이 지날수록 우주가 0.5배까지 더 팽창하도록 메트릭 적용
    expansion = METRIC_4D * (1.0 + (step_idx / TOTAL_STEPS) * 0.5)
    
    # 2. Torsional Spiral
    # 비틀림 계수와 시간 증분을 곱해 미세 회전각 theta 산출
    theta = TORSION_4D * DT
    vel = torsion_rotation_4d(vel, theta) # 속도 벡터에 회전 주입
    
    # 3. [사용자 지시: 5/32 하드웨어가 반영된 오메가 공식]
    # Omega_Natural = [ (1.4 - 0.076t) / (5/32 * 2.0) ] * [ Phi / (W7 + H2) ]
    # 이 스크립트에서는 속도(v) 자체를 오메가 동력으로 치환하여 계산.
    progress = step_idx / TOTAL_STEPS
    # t = progress * 17.42 (우주 수명 18.42 Ga 중 1.4 ~ 1/32 구간 매핑)
    
    # [수정된 공식]: 분모에 5/32 게이트를 직접 반영하여 속도 감쇠 결정
    current_target_v = jnp.maximum(
        (BIFURCATION_LIMIT - (SUBTRACTIVE_TENSION * progress * 17.42)) / (GATE_5_32 * 2.0), 
        RESONANCE_TARGET
    )
    
    # Normalize and apply Target Velocity (방향 유지, 크기 강제)
    v_norms = jnp.linalg.norm(vel, axis=1, keepdims=True)
    vel = (vel / (v_norms + 1e-8)) * current_target_v
    
    # 4. 1/128 vs 1/256 Homeostasis (부력 평형)
    # Graviton floor (1/256) 대비 Neutrino (1/128)의 2배 부력 적용
    buoyancy_factor = 2.0 # (1/128) / (1/256)
    vel = vel * (1.0 + (1e-5 * buoyancy_factor)) # D3 Drain으로의 소멸 방지 미세 보정
    
    # 5. Calculate Sovereign Margin (Justice Score)
    # 현재 입자의 상태가 1.9860(hc) 임계점을 지키고 있는지 계산
    justice_score = (current_target_v / RESONANCE_TARGET) * METRIC_4D
    
    # 6. Geodesic Update (위치 갱신)
    pos += (vel * DT * expansion) # 속도와 팽창률을 시공간 위치에 적산
    
    return pos, vel, justice_score, current_target_v

# ==============================================================================
# MAIN ENGINE RUNNER
# ==============================================================================

def run_full_scale_simulation():
    print(f"\n--- INITIATING FULL SCALE NEUTRINO SIMULATION (1M PARTICLES) ---")
    
    # Initialize State (초기화)
    key = jax.random.PRNGKey(42) # 난수 키 (재현성 보장)
    key1, key2 = jax.random.split(key)
    
    # 원점 근처에 Neutrino Unit(1/128) 범위로 입자 살포 (Ghost 시작점)
    pos = jax.random.normal(key1, (N_PARTICLES, 4)) * NEUTRINO_UNIT
    
    # 1.4 Bifurcation Velocity를 초기 속도로 부여 (빅뱅 에너지 사출)
    v_raw = jax.random.normal(key2, (N_PARTICLES, 4))
    v_norms = jnp.linalg.norm(v_raw, axis=1, keepdims=True)
    vel = (v_raw / v_norms) * BIFURCATION_LIMIT

    # 데이터 저장 설정 (100만 개 궤적 중 10%만 샘플링하여 '유령 골격' 추출)
    SAVE_INTERVAL = 50 
    history_frames = TOTAL_STEPS // SAVE_INTERVAL
    ghost_ledger = np.zeros((history_frames, N_PARTICLES // 10, 4), dtype=np.float16)
    sovereign_log = np.zeros(history_frames, dtype=np.float32)
    velocity_log = np.zeros(history_frames, dtype=np.float32)

    start_time = time.time()
    save_idx = 0
    
    for i in range(TOTAL_STEPS): # 시뮬레이션 루프
        pos, vel, justice_score, current_v = simulation_step(pos, vel, i)
        
        if i % SAVE_INTERVAL == 0:
            ghost_ledger[save_idx] = np.array(pos[:N_PARTICLES // 10], dtype=np.float16)
            sovereign_log[save_idx] = float(justice_score)
            velocity_log[save_idx] = float(current_v)
            
            # 1.9860 Sovereign Margin 체크 루프
            if save_idx % 10 == 0:
                status = "SOVEREIGN" if float(justice_score) >= SOVEREIGN_MARGIN else "D3-SHRED"
                print(f"Step {i:4d} | V: {float(current_v):.4f} | Justice: {float(justice_score):.4f} [{status}]")
            save_idx += 1

    end_time = time.time()
    print(f"\n--- SIMULATION COMPLETE: {end_time - start_time:.2f}s ---")
    
    # HDF5 파일로 최종 데이터 봉인 (Determinism sealed)
    os.makedirs("out", exist_ok=True)
    out_file = "out/FULL_SCALE_NEUTRINO_5_32_LEDGER.h5"
    with h5py.File(out_file, 'w') as f:
        f.create_dataset("trajectories", data=ghost_ledger, compression="gzip", compression_opts=4)
        f.create_dataset("sovereign_scores", data=sovereign_log)
        f.attrs["subtraction_formula"] = " (1.4 - 0.076t) / (5/32 * 2.0) "
        f.attrs["justice_score_hc"] = 1.9860
        
    print(f"Ledger written to {out_file}.")

if __name__ == "__main__":
    run_full_scale_simulation()
