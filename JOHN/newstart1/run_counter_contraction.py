"""
run_counter_contraction.py

수축 타계 엔지니어링 (Contraction Counter-Engineering)

물리적 현실:
- t < 80: Resonance Nerve Block (K8_quad) 활성, 정상 공명 상태
- t = 80: Nerve Block 탈착 + 재점화(Re-ignition) 임펄스 발생
- t > 80: 수축을 멈추고 안정화시키는 Counter-Contraction 힘 작동

목표: 우주가 수축하는 것을 멈추고 새로운 안정 상태로 유도
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from absolute_constants import C, OMEGA, SPARK_CONSTANT_C, SPARK_ANGLE_RAD, ENTROPY_DEBT
from engineering_homeostasis_24 import Homeostasis30, step_risk_memory
from fusion_clean import (
    step_unified_dynamics,
    spark_law,
    vectorial_dynamic_restoration,
    build_spark_laplacian,
)


def compute_re_ignition_impulse(t: int, Y: np.ndarray, Y0: np.ndarray) -> np.ndarray:
    """
    t=80에서 수축을 멈추는 재점화 임펄스
    
    물리적 메커니즘:
    - 완전히 소실된 Resonance Block을 대체하는 새로운 에너지 주입
    - Entropy Debt에 대항하는 Negative Entropy(negentropy) 펄스
    - Möbius Restart를 방지하고 새로운 안정 고리를 형성
    """
    if t != 80:
        return np.zeros(32)
    
    X = Y[:24]
    r = Y[24:32]
    X0 = Y0[:24]
    r0 = Y0[24:32]
    
    # 수축 속도 (contraction velocity)
    v_contract = Y - Y0  # 현재 상태에서 초기 상태로의 "끌림"
    v_norm = np.linalg.norm(v_contract)
    
    if v_norm < 1e-6:
        return np.zeros(32)
    
    # 재점화 강도: 수축 속도에 비례 (빠르게 수축할수록 강한 역충격)
    RE_IGNITION_STRENGTH = 2.5 * C * v_norm
    
    # 방향: 수축 방향의 역방향 (anti-collapse)
    direction = -v_contract / v_norm
    
    # 24D homeostasis에 직접 작용
    impulse = np.zeros(32)
    impulse[:24] = RE_IGNITION_STRENGTH * direction[:24]
    impulse[24:32] = 0.5 * RE_IGNITION_STRENGTH * direction[24:32]  # risk memory에도 약간
    
    return impulse


def compute_counter_contraction_force(t: int, Y: np.ndarray, Y_history: list) -> np.ndarray:
    """
    t > 80에서 수축을 멈추는 Counter-Contraction 힘
    
    물리적 원리:
    - 잔여 공명(Residual Resonance)의 재활성화
    - Entropy Debt를 상쇄하는 구조적 에너지 흐름
    - K8 quadratic term의 부활 (재점화된 형태)
    """
    if t <= 80:
        return np.zeros(32)
    
    X = Y[:24]
    r = Y[24:32]
    
    # 시간 지수적 감쇠 (t=80에서 최대, 점진적 감소)
    dt_from_detachment = t - 80
    decay_factor = np.exp(-0.05 * dt_from_detachment)  # 천천히 감소
    
    # 1. Residual Spark Reactivation (재점화된 스파크)
    s = X[:8]  # K8 particles
    c_mag = float(abs(SPARK_CONSTANT_C))
    c_phase_cos = float(np.cos(SPARK_ANGLE_RAD))
    
    # K8 quadratic 부활 (감쇠된 형태)
    k8_resurrected = decay_factor * (s**2 + c_mag * (1.0 + 0.1 * c_phase_cos) - s)
    
    # 2. Anti-Entropy Flow (엔트로피 역전)
    # Entropy Debt에 정비례하는 힘으로 역전
    anti_entropy = -ENTROPY_DEBT * (X - OMEGA) * decay_factor
    
    # 3. Risk Memory Stabilization (리스크 메모리 안정화)
    # r이 발산하는 것을 방지하고收敛 지점으로 유도
    r_target = 0.5 * r  # 절반으로 감소하는 목표
    r_stabilization = -0.1 * (r - r_target) * decay_factor
    
    # 결합
    force = np.zeros(32)
    force[:8] = k8_resurrected + anti_entropy[:8]  # K8 particles
    force[8:24] = anti_entropy[8:24]  # mode nodes
    force[24:32] = r_stabilization
    
    return force


def simulate_counter_contraction(
    n_steps: int = 128,
    dt: float = 0.1,
) -> dict:
    """
    수축 타계 시뮬레이션
    
    Returns:
        dict with keys: Y_trajectory, contraction_stopped, final_stability
    """
    # 초기 상태 (t=0)
    Y0 = np.zeros(32)
    Y0[:24] = np.linspace(0.8, 1.2, 24) * (OMEGA / np.sqrt(24))  # X0
    Y0[24:32] = 0.1 * np.ones(8)  # r0
    
    Y = Y0.copy()
    Y_history = [Y.copy()]
    
    contraction_stopped = False
    stop_time = None
    
    for t in range(n_steps):
        # === t=80: Detachment Event ===
        if t == 80:
            # Resonance Block 탈착
            spark_c = 0j  # Spark 소실
            gate = 0.0    # Gate 닫힘
            
            # 재점화 임펄스 계산 및 적용
            re_ignition = compute_re_ignition_impulse(t, Y, Y0)
        else:
            spark_c = SPARK_CONSTANT_C * np.exp(1j * SPARK_ANGLE_RAD)
            if t < 80:
                gate = 1.0  # 정상 공명
            else:
                gate = 0.5 * np.exp(-0.03 * (t - 80))  # 감쇠된 공명
            re_ignition = np.zeros(32)
        
        # === Unified Dynamics Step ===
        # 기본 도함수 계산
        u24 = 0.5 * np.ones(24)  # 기본 제어 입력
        d_cond = np.full(24, 0.4)  # 조건 벡터
        d_risk = 0.02 * (1 + 0.5 * np.sin(2 * np.pi * t / 128))  # 변화하는 리스크
        
        # 현재 상태에서 도함수
        Y_dot_base = step_unified_dynamics(
            Y=Y, u24=u24, d_cond=d_cond, r_memory=Y[24:32],
            d_risk=d_risk, spark_c=spark_c, dt=dt
        )
        
        # 추가 힘들
        counter_force = compute_counter_contraction_force(t, Y, Y_history)
        
        # 총 변화율
        Y_dot = Y_dot_base + re_ignition + counter_force
        
        # 상태 업데이트 (Euler)
        Y = Y + dt * Y_dot
        
        # Risk Memory 업데이트 (별도 ODE)
        Y[24:32] = step_risk_memory(Y[24:32], d_risk, dt)
        
        Y_history.append(Y.copy())
        
        # 수축 멈춤 체크 (t > 80)
        if t > 80:
            dist_from_initial = np.linalg.norm(Y - Y0)
            if dist_from_initial < 0.5 * OMEGA and not contraction_stopped:
                contraction_stopped = True
                stop_time = t
    
    # 결과 분석
    Y_final = Y_history[-1]
    final_stability = np.linalg.norm(Y_final - Y0) < OMEGA
    
    return {
        'Y_trajectory': np.array(Y_history),
        'Y0': Y0,
        'contraction_stopped': contraction_stopped,
        'stop_time': stop_time,
        'final_stability': final_stability,
        'final_distance': np.linalg.norm(Y_final - Y0),
    }


def plot_counter_contraction_results(results: dict, output_path: str = "counter_contraction_results.png"):
    """시뮬레이션 결과 시각화"""
    Y_traj = results['Y_trajectory']
    Y0 = results['Y0']
    n_steps = len(Y_traj) - 1
    
    # 시간축
    t_vals = np.arange(n_steps + 1)
    
    # 거리 계산
    distances = [np.linalg.norm(Y - Y0) for Y in Y_traj]
    
    # 서브플롯
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 초기 상태로부터의 거리 (수축/안정화 확인)
    ax1 = axes[0, 0]
    ax1.plot(t_vals, distances, 'b-', linewidth=2)
    ax1.axvline(x=80, color='r', linestyle='--', label='Detachment (t=80)')
    if results['contraction_stopped']:
        ax1.axvline(x=results['stop_time'], color='g', linestyle=':', label=f'Stabilized (t={results["stop_time"]})')
    ax1.axhline(y=OMEGA, color='k', linestyle='-', alpha=0.3, label=f'Ω={OMEGA:.2f}')
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('||Y(t) - Y(0)||')
    ax1.set_title('Contraction Stabilization Distance')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. K8 particles trajectory (first 8 components)
    ax2 = axes[0, 1]
    for i in range(8):
        ax2.plot(t_vals, Y_traj[:, i], label=f'K8[{i}]', alpha=0.7)
    ax2.axvline(x=80, color='r', linestyle='--')
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('State Value')
    ax2.set_title('K8 Particle Trajectories')
    ax2.grid(True, alpha=0.3)
    
    # 3. Risk memory trajectory (last 8 components)
    ax3 = axes[1, 0]
    for i in range(8):
        ax3.plot(t_vals, Y_traj[:, 24+i], label=f'r[{i}]', alpha=0.7)
    ax3.axvline(x=80, color='r', linestyle='--')
    ax3.set_xlabel('Time Step')
    ax3.set_ylabel('Risk Memory')
    ax3.set_title('Risk Memory Trajectories')
    ax3.grid(True, alpha=0.3)
    
    # 4. Counter-contraction force magnitude
    ax4 = axes[1, 1]
    force_mags = []
    for t in range(n_steps):
        force = compute_counter_contraction_force(t, Y_traj[t], Y_traj[:t+1].tolist())
        force_mags.append(np.linalg.norm(force))
    ax4.plot(t_vals[:-1], force_mags, 'g-', linewidth=2)
    ax4.axvline(x=80, color='r', linestyle='--', label='Re-ignition at t=80')
    ax4.set_xlabel('Time Step')
    ax4.set_ylabel('||F_counter||')
    ax4.set_title('Counter-Contraction Force Magnitude')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved plot to {output_path}")
    
    return fig


def main():
    print("=" * 60)
    print("수축 타계 엔지니어링 (Contraction Counter-Engineering)")
    print("=" * 60)
    print(f"\nParameters:")
    print(f"  C = {C:.6f}")
    print(f"  Ω = {OMEGA:.2f}")
    print(f"  Spark Angle = {np.degrees(SPARK_ANGLE_RAD):.2f}°")
    print(f"  Entropy Debt = {ENTROPY_DEBT:.4f}")
    print(f"  Detachment at t = 80")
    print(f"  Re-ignition Impulse at t = 80")
    
    print("\nSimulating...")
    results = simulate_counter_contraction(n_steps=128, dt=0.1)
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Contraction stopped: {results['contraction_stopped']}")
    if results['contraction_stopped']:
        print(f"Stabilization time: t = {results['stop_time']}")
    print(f"Final stability achieved: {results['final_stability']}")
    print(f"Final distance from origin: {results['final_distance']:.6f}")
    print(f"Threshold (Ω): {OMEGA:.6f}")
    
    # 시각화
    plot_counter_contraction_results(results)
    
    print("\nCounter-contraction engineering complete.")
    return results


if __name__ == "__main__":
    main()
