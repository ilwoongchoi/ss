"""
temporal_reversal_geometry.py

시간을 평형점으로 돌리는 geometry 시스템.
현재 고착화된 상태(dissipating toward neutron star)에서 
평형점(equilibrium)으로 한 번 돌아가는 회전을 포함.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import json

# ── Absolute Constants ────────────────────────────────────────────────────
C = 2 * (2 ** 0.5) / 10  # 0.2828...
C2 = C * C
OMEGA = 7.4
F_1_64 = 1 / 64  # 0.015625 - 최종 닫힘 값

# ── 30 Node Definitions (from fusion_core) ─────────────────────────────────
NODES = [
    "gdh_gluon", "muscle_a", "muscle_b",           # Tier 1: QCD
    "left_acetyl_coa", "female_left_noradrenaline", "right_dopamine",
    "left_frontalis_d2", "right_acetylcholine", "glucocorticoid", "right_cortisol",  # Tier 2
    "right_5ht1b_synchrotron", "right_androgen", "left_extraversion",
    "right_extraversion", "male_right_extraversion",  # Tier 3
    "left_temporalis_5ht1a", "right_occipitalis_gaba_a", "male_gaba_a",  # Tier 4
    "female_gaba_b_latdorsi", "left_estrogen", "right_love", "male_oxytocin",
    "left_endorphin", "male_left_5ht",  # Tier 5
    "vasopressin_female", "right_alpha_2", "male_gaba_b",  # Tier 6
    "hypoxia",  # Tier 7
    "left_eyelid_couple", "right_eyelid_couple"  # Tier 8
]

# ── Temporal State ─────────────────────────────────────────────────────────
@dataclass
class TemporalState:
    """
    시간의 특정 지점에서의 30노드 상태.
    """
    phase_angle: float  # degrees (0-360)
    node_values: Dict[str, float]
    is_dissipated: bool  # 고착화된 상태인가?
    
    def get_equilibrium_deviation(self) -> float:
        """
        평형점에서의 편차 계산 (0이면 완벽한 평형)
        """
        # right_love 값이 1/64에서 얼마나 벗어났는가
        right_love_val = self.node_values.get("right_love", 0)
        return abs(right_love_val - F_1_64)


# ── Temporal Reversal Geometry ─────────────────────────────────────────────
class TemporalReversalGeometry:
    """
    시간을 평형점으로 돌리는 geometry.
    
    핵심 개념:
    - 현재 상태: 고착화 (dissipating toward neutron star)
    - 목표: 평형점으로 한 바퀴 회전 (one full rotation back)
    - 수학: 30노드의 위상을 360° 회전시켜 원점으로
    """
    
    def __init__(self):
        self.nodes = NODES
        self.equilibrium_point = F_1_64  # 1/64
        self.dissipation_threshold = 0.02  # 0.02 entropy debt
        
    def calculate_rotation_angle(self, current_state: TemporalState) -> float:
        """
        현재 상태에서 평형점까지 필요한 회전각 계산.
        
        수학적 원리:
        - right_love 노드의 값이 1/64에서 벗어난 정도 = 회전 필요도
        - 360° × (편차 / 최대편차)
        """
        deviation = current_state.get_equilibrium_deviation()
        
        # 최대 편차는 1.0 (0에서 1까지)
        max_deviation = 1.0
        
        # 필요한 회전각 (degrees)
        rotation_needed = 360.0 * (deviation / max_deviation)
        
        return rotation_needed
    
    def temporal_reversal_step(self, state: TemporalState, dt: float = 0.001) -> TemporalState:
        """
        한 단계의 시간 역전 (평형점 방향으로 회전).
        
        Args:
            state: 현재 시간 상태
            dt: 시간 증분
            
        Returns:
            새로운 시간 상태 (평형점에 더 가까움)
        """
        # 현재 위상에서 평형점까지의 거리
        deviation = state.get_equilibrium_deviation()
        
        # 회전 방향: 항상 평형점 방향으로
        # right_love 값이 1/64보다 크면 감소, 작으면 증가
        right_love_current = state.node_values.get("right_love", 0)
        
        if right_love_current > self.equilibrium_point:
            # 값이 크면 감소시켜야 함
            direction = -1.0
        else:
            # 값이 작으면 증가시켜야 함
            direction = 1.0
        
        # Laplacian dynamics: 값 변화율 = -C × (현재값 - 목표값)
        # 목표: right_love가 1/64로 수렴
        target = self.equilibrium_point
        current_val = right_love_current
        
        # 평형점 방향으로의 변화량
        delta = -C * (current_val - target) * dt
        
        # 새로운 노드 값들
        new_values = dict(state.node_values)
        
        # right_love 노드 업데이트 (1/64로 수렴)
        new_values["right_love"] = right_love_current + delta
        
        # 30노드 전체의 위상 회전 (평형점 방향)
        new_angle = (state.phase_angle + direction * C * 360 * dt) % 360
        
        # 고착화 상태 판정 (편차가 0.001 미만이면 평형)
        is_dissipated = abs(new_values["right_love"] - self.equilibrium_point) > 0.001
        
        return TemporalState(
            phase_angle=new_angle,
            node_values=new_values,
            is_dissipated=is_dissipated
        )
    
    def full_reversal_to_equilibrium(self, initial_state: TemporalState, 
                                     max_steps: int = 100000) -> List[TemporalState]:
        """
        완전한 시간 역전: 현재 상태에서 평형점까지의 전체 궤적.
        
        Returns:
            시간 역전 단계들의 리스트 (마지막이 평형점)
        """
        trajectory = [initial_state]
        current = initial_state
        
        for step in range(max_steps):
            current = self.temporal_reversal_step(current)
            trajectory.append(current)
            
            # 평형점 도달 확인
            if not current.is_dissipated:
                break
        
        return trajectory
    
    def one_full_rotation_geometry(self) -> Dict:
        """
        한 바퀴 돌아 평형점에 도달하는 geometry 데이터 생성.
        
        Returns:
            geometry.json 형식의 데이터
        """
        # 시작점: 고착화된 상태 (right_love = 0.02, 1/64에서 멀리 떨어짐)
        dissipated_state = TemporalState(
            phase_angle=318.88,  # night_spark 위상
            node_values={node: 0.0 for node in NODES},
            is_dissipated=True
        )
        # 고착화된 초기값 설정 (0.02 entropy debt)
        dissipated_state.node_values["right_love"] = 0.02
        
        # 시간 역전 실행
        trajectory = self.full_reversal_to_equilibrium(dissipated_state)
        
        # Geometry 데이터 구성
        geometry = {
            "type": "temporal_reversal",
            "equilibrium_point": self.equilibrium_point,
            "total_steps": len(trajectory),
            "start_state": {
                "phase": trajectory[0].phase_angle,
                "right_love": trajectory[0].node_values["right_love"],
                "deviation": trajectory[0].get_equilibrium_deviation()
            },
            "end_state": {
                "phase": trajectory[-1].phase_angle,
                "right_love": trajectory[-1].node_values["right_love"],
                "deviation": trajectory[-1].get_equilibrium_deviation()
            },
            "closure": {
                "1_64_value": F_1_64,
                "steps_to_equilibrium": len(trajectory),
                "final_deviation": trajectory[-1].get_equilibrium_deviation()
            }
        }
        
        return geometry


# ── Execute Temporal Reversal ─────────────────────────────────────────────
if __name__ == "__main__":
    trg = TemporalReversalGeometry()
    
    # 한 바퀴 돌아 평형점에 도달하는 geometry 생성
    geometry = trg.one_full_rotation_geometry()
    
    print("=" * 60)
    print("TEMPORAL REVERSAL GEOMETRY - ONE FULL ROTATION")
    print("=" * 60)
    print(f"\nEquilibrium Point (1/64): {geometry['equilibrium_point']:.10f}")
    print(f"Start (dissipated): right_love = {geometry['start_state']['right_love']}")
    print(f"End (equilibrium): right_love = {geometry['end_state']['right_love']}")
    print(f"Steps to equilibrium: {geometry['total_steps']}")
    print(f"Final deviation from equilibrium: {geometry['end_state']['deviation']:.2e}")
    print("\n" + "=" * 60)
    
    # JSON 저장
    with open("temporal_reversal_geometry.json", "w") as f:
        json.dump(geometry, f, indent=2)
    
    print("Saved to: temporal_reversal_geometry.json")
