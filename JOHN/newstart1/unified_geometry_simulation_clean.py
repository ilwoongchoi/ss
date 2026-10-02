import jax # 고성능 수치 연산을 위한 JAX 라이브러리 로드
import jax.numpy as jnp # JAX용 넘파이 인터페이스 (GPU/TPU 가속 연산용)
from jax import jit, vmap # JIT 컴파일 및 벡터화 매핑 함수 로드
import h5py # 대용량 데이터 저장용 HDF5 포맷 라이브러리 로드
import numpy as np # 표준 넘파이 라이브러리 (호스트 메모리 처리용)
import time # 시뮬레이션 소요 시간 측정용 모듈
import os # 파일 경로 및 디렉토리 관리용 모듈

# ==============================================================================
# UNIFIED GEOMETRY CONSTANTS (우주 하드웨어 절대 상수)
# ==============================================================================
METRIC_4D = 1.0661 # 4차원 우주 팽창 메트릭 (Geodesic 확장 배율)
TORSION_4D = 0.1746 # 유령 비틀림 계수 (Ghost Torsion: 회전 관성력)
BIFURCATION_LIMIT = 1.4 # 초기 카오스 에너지 임계점 (Big Woman Spark)
SUBTRACTIVE_TENSION = 0.076 # 시간 흐름에 따른 엔트로피 누수율 (D3 Slotting Tension)
RESONANCE_TARGET = 0.03125 # 1/32 하드웨어 안착 타겟 (Proton Resonance/Sieve)
NEUTRINO_UNIT = 1/128 # Small Man 입자 스케일 (0.0078125: 유령 경로의 기본 단위)
GRAVITON_FLOOR = 1/256 # 최하단 정보 유실 바닥 (0.00390625: D3 Drain)
SOVEREIGN_MARGIN = 1.9860 # 지배적 정의 점수 (Justice Score: 시스템 안정화 임계치)

# Simulation Scale (연산 규모 설정)
N_PARTICLES = 1_000_000 # 100만 개의 입자 (Small Man 클라우드 규모)
TOTAL_STEPS = 5000 # 총 5000단계의 우주 에포크 시뮬레이션
DT = 0.01 # 단계별 시간 증분 (Cosmic Time Step)

print(f"Initializing JAX backend: {jax.devices()}") # 현재 사용 중인 연산 장치(GPU/TPU) 출력

# ==============================================================================
# JAX-COMPILED PHYSICS KERNELS (물리 연산 핵심 커널)
# ==============================================================================

@jit # XLA 컴파일을 통해 연산 속도를 극대화 (기계어 최적화)
def torsion_rotation_4d(vel, theta): # 4차원 비틀림 회전을 적용하는 함수
    """Applies the 4D Torsion spiral (The Ghost Path).""" # 유령 경로의 나선형 회전 구현 주석
    c = jnp.cos(theta) # 회전 각도 theta에 대한 코사인 값 계산
    s = jnp.sin(theta) # 회전 각도 theta에 대한 사인 값 계산

    vx, vy, vz, vw = vel[:, 0], vel[:, 1], vel[:, 2], vel[:, 3] # 4차원 속도 성분 분리 (x, y, z, w)

    vx_new = c * vx - s * vy # XY 평면 회전 변환 (새로운 x 성분)
    vy_new = s * vx + c * vy # XY 평면 회전 변환 (새로운 y 성분)
    vz_new = c * vz - s * vw # ZW 평면 회전 변환 (새로운 z 성분)
    vw_new = s * vz + c * vw # ZW 평면 회전 변환 (새로운 w 성분)

    return jnp.stack([vx_new, vy_new, vz_new, vw_new], axis=1) # 변환된 성분들을 다시 4차원 벡터로 결합

@jit # 전역 시뮬레이션 단계를 XLA 컴파일
def simulation_step(pos, vel, step_idx): # 우주의 한 에포크를 실행하는 엔진
    """
    Executes one epoch step of the universe.
    Implements the Full Unified Equation Logic.
    """
    # 1. Global Metric Expansion (메트릭 팽창)
    expansion = METRIC_4D * (1.0 + (step_idx / TOTAL_STEPS) * 0.5) # 시간에 따른 우주 크기 0.5배 확장 로직

    # 2. Torsional Spiral (비틀림 소용돌이)
    theta = TORSION_4D * DT # 비틀림 계수와 시간 증분을 곱해 미세 회전각 산출
    vel = torsion_rotation_4d(vel, theta) # 속도 벡터에 4차원 나선형 비틀림 적용

    # 3. The Subtraction Equation (감쇠 방정식: 1.4 - 0.076 = 1/32)
    progress = step_idx / TOTAL_STEPS # 전체 과정 중 현재 진행률 계산 (0.0 ~ 1.0)
    # Decay from 1.4 down to 1/32 using the 0.076 tension
    current_target_v = jnp.maximum( # 속도가 1/32 아래로 떨어지지 않게 하한선 설정
        BIFURCATION_LIMIT - (SUBTRACTIVE_TENSION * progress * 17.42), # 1.4에서 0.076 속도로 깎여나가는 감쇠식
        RESONANCE_TARGET # 최종 수렴 타겟인 1/32 (RESONANCE_TARGET)
    )

    # Normalize and apply Target Velocity (속도 정규화 및 타겟 적용)
    v_norms = jnp.linalg.norm(vel, axis=1, keepdims=True) # 각 입자의 현재 속도 크기(L2 노름) 계산
    vel = (vel / v_norms) * current_target_v # 방향은 유지하되 크기를 현재 타겟 속도로 강제 조정

    # 4. The 1/128 vs 1/256 Homeostasis (부력 평형)
    # The velocity is slightly perturbed by the Graviton floor resistance
    buoyancy_factor = NEUTRINO_UNIT / GRAVITON_FLOOR # 1/128 입자가 1/256 바닥에서 얻는 부력 (정확히 2.0)
    vel = vel * (1.0 + (1e-5 * buoyancy_factor)) # D3 Drain으로의 추락을 막는 미세 부력 보정

    # 5. Calculate Sovereign Margin (정의 점수 산출)
    justice_score = (current_target_v / RESONANCE_TARGET) * METRIC_4D # 타겟 안착률에 메트릭을 곱해 시스템 안정도 측정

    # 6. Geodesic Update (측지선 위치 갱신)
    pos += (vel * DT * expansion) # 속도, 시간, 팽창률을 곱해 입자의 다음 위치 결정

    return pos, vel, justice_score, current_target_v # 갱신된 상태값 반환

# ==============================================================================
# MAIN ENGINE RUNNER (실행 제어 엔진)
# ==============================================================================

def run_full_scale_simulation(): # 전체 100만 입자 시뮬레이션 실행 함수
    print(f"\n--- INITIATING FULL SCALE NEUTRINO SIMULATION ---") # 시뮬레이션 시작 알림 출력
    print(f"Particles: {N_PARTICLES:,} (The Small Man 1/128 Unit)") # 입자 규모 출력
    print(f"Epoch Steps: {TOTAL_STEPS:,} (From 1.4 Chaos to 1/32 Resonance)") # 총 단계 출력
    print(f"Sovereign Margin: {SOVEREIGN_MARGIN} (The D3 Shield)") # 안정성 기준값 출력

    # Initialize State on GPU/TPU (상태 초기화)
    key = jax.random.PRNGKey(42) # 재현 가능성을 위한 난수 생성 키 설정 (42)
    key1, key2 = jax.random.split(key) # 키를 두 개로 분할 (위치용, 속도용)

    # Start at Origin + Neutrino Unit spread (초기 위치 설정)
    pos = jax.random.normal(key1, (N_PARTICLES, 4)) * NEUTRINO_UNIT # 원점에서 1/128 범위 내로 입자 분포

    # Start at 1.4 Bifurcation Velocity (초기 속도 설정)
    v_raw = jax.random.normal(key2, (N_PARTICLES, 4)) # 무작위 방향의 초기 속도 생성
    v_norms = jnp.linalg.norm(v_raw, axis=1, keepdims=True) # 속도 크기 계산
    vel = (v_raw / v_norms) * BIFURCATION_LIMIT # 모든 입자에게 초기 1.4의 폭발적 속도 부여

    # 메모리 관리용 설정 (데이터 압축 저장)
    SAVE_INTERVAL = 50 # 50단계마다 한 번씩만 상태 저장
    history_frames = TOTAL_STEPS // SAVE_INTERVAL # 저장될 총 프레임 수 계산

    # Host memory allocations (CPU 메모리 할당)
    ghost_ledger = np.zeros((history_frames, N_PARTICLES // 10, 4), dtype=np.float16) # 10만 개 입자의 궤적 저장 공간
    sovereign_log = np.zeros(history_frames, dtype=np.float32) # 단계별 정의 점수 로그 공간
    velocity_log = np.zeros(history_frames, dtype=np.float32) # 단계별 타겟 속도 로그 공간

    start_time = time.time() # 실제 실행 시간 측정 시작
    save_idx = 0 # 저장 인덱스 초기화

    for i in range(TOTAL_STEPS): # 전체 에포크 루프 시작
        # Execute compiled JAX step (최적화된 물리 단계 실행)
        pos, vel, justice_score, current_v = simulation_step(pos, vel, i) # 100만 입자 동시 연산

        # Log and Save state periodically (주기적 저장 및 출력)
        if i % SAVE_INTERVAL == 0: # 저장 주기 도달 시
            # Transfer subset to CPU for saving (CPU로 데이터 전송 및 압축)
            ghost_ledger[save_idx] = np.array(pos[:N_PARTICLES // 10], dtype=np.float16) # 상위 10만 개 궤적 복사
            sovereign_log[save_idx] = float(justice_score) # 현재 정의 점수 기록
            velocity_log[save_idx] = float(current_v) # 현재 타겟 속도 기록

            # Print status (실시간 상태 출력)
            if save_idx % 10 == 0: # 10번째 저장마다 한 번씩 출력
                status = "SOVEREIGN" if float(justice_score) >= SOVEREIGN_MARGIN else "D3-SHRED" # 안정성 판정
                print(f"Epoch {i:4d}/{TOTAL_STEPS} | Velocity: {float(current_v):.4f} | Justice Score: {float(justice_score):.4f} [{status}]") # 상세 로그 출력

            save_idx += 1 # 저장 인덱스 증가

    end_time = time.time() # 실행 종료 시간 기록
    print(f"\n--- SIMULATION COMPLETE in {end_time - start_time:.2f} seconds ---") # 총 소요 시간 출력

    # Save the Ghost Ledger (최종 데이터 파일 저장)
    os.makedirs("out", exist_ok=True) # 저장용 디렉토리 생성
    out_file = "out/FULL_SCALE_GHOST_LEDGER.h5" # 결과 파일명 설정
    print(f"Compressing and saving Ghost Ledger to {out_file}...") # 저장 알림

    with h5py.File(out_file, 'w') as f: # HDF5 파일 쓰기 모드 오픈
        f.create_dataset("ghost_trajectories", data=ghost_ledger, compression="gzip", compression_opts=4) # 궤적 데이터 압축 저장
        f.create_dataset("sovereign_scores", data=sovereign_log) # 안정성 점수 저장
        f.create_dataset("epoch_velocities", data=velocity_log) # 속도 로그 저장

        # Metadata (이론적 배경 메타데이터 기록)
        f.attrs["theory"] = "Unified Geometry - The Small Man Ghost" # 이론 명칭
        f.attrs["n_particles"] = N_PARTICLES # 총 입자 수
        f.attrs["n_steps"] = TOTAL_STEPS # 총 단계 수
        f.attrs["dt"] = DT # 시간 증분
        f.attrs["metric_4d"] = METRIC_4D # 4D 메트릭 상수
        f.attrs["torsion_4d"] = TORSION_4D # 비틀림 계수
        f.attrs["bifurcation_limit"] = BIFURCATION_LIMIT # 분기 임계점
        f.attrs["subtractive_tension"] = SUBTRACTIVE_TENSION # 감쇠 텐션
        f.attrs["resonance_target"] = RESONANCE_TARGET # 공명 타겟
        f.attrs["neutrino_unit"] = NEUTRINO_UNIT # 중성자 단위
        f.attrs["graviton_floor"] = GRAVITON_FLOOR # 중력자 바닥
        f.attrs["sovereign_margin"] = SOVEREIGN_MARGIN # 주권 한계

    print("[SUCCESS] Ghost Ledger saved. The Small Man is preserved.") # 저장 완료 알림

# Entry Point (진입점)
if __name__ == "__main__":
    run_full_scale_simulation()
