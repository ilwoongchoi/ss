from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, Mapping

import numpy as np

from geometry_package.absolute_constants import (
    DELTA_T_OBS_DERIVED,
    SPARK_ANGLE_DEG,
    TORSION_4D,
)
from geometry_package.edge_stack_master_equation import (
    as_state4,
    gate_02828,
    helical_time_components,
    mandelbrot_core_4d,
    spark_torsion_4d,
    EDGE_VECTORS,
    EDGE_DOMAIN_STACK,
)

# --- THE SOVEREIGN CONSTANTS ---
# Betti numbers as fundamental "Brick Counts"
BETTI_11 = 11.0  # Structural Bridges (Positive Reinforcement)
BETTI_5  = 5.0   # Topological Leaks (Asymmetry / 4:30 AM Debt)
BETTI_7  = 7.0   # Sinks / Darkness (Lensing Artifact)
BETTI_0  = 1.0   # The Witness / Seed (B0=1)

# Lensing artifact scale from repo
LENSING_ARTIFACT_SCALE = 7.4

# The Closure Axiom: (11 + 1) / (5 + 7) = 1.0
CLOSURE_METRIC = (BETTI_11 + BETTI_0) / (BETTI_5 + BETTI_7)

@dataclass(frozen=True)
class FinalBossParams:
    """
    Final Boss Coefficients derived from Betti Numbers.
    No regression, only structural counts.
    """
    w_bridge: float = BETTI_11 / 12.0  # Normalized bridge power
    w_leak: float = BETTI_5 / 12.0     # Normalized leak debt
    w_sink: float = BETTI_7 / 12.0     # Normalized sink (Lensing)
    w_witness: float = BETTI_0 / 12.0  # Seed/Witness bias
    
    # 12th Node Control: Conscious removal of Right Dopamine (BM_BM / BM_BW)
    remove_lensing: bool = True
    lensing_factor: float = LENSING_ARTIFACT_SCALE

def sovereign_final_boss_step(
    state4: Iterable[float],
    phase_fill: float,
    *,
    params: FinalBossParams | None = None,
) -> Dict[str, object]:
    """
    The Ultimate Sovereign Equation.
    Automates artifact removal using Betti Motif Counts.
    """
    p = params or FinalBossParams()
    state = as_state4(state4)
    
    # 1. Gate and Time Symmetry Logic
    gate = gate_02828(phase_fill)
    helix = helical_time_components(phase_fill)
    
    # Net Energy Calculation (12th Node Operation)
    # net_time removes the forward/backward Histamine Path 공모
    net_time_scale = helix["net"] 
    
    # 2. Core Mandelbrot Engine
    core = mandelbrot_core_4d(state)
    
    # 3. Domain Contributions (Grouped by Betti Role)
    # Bridges (BETTI_11): BM_SM, SM_SM, SM_SW
    bridge_vec = (
        EDGE_VECTORS["BM_SM"] * np.dot(state, EDGE_VECTORS["BM_SM"]) +
        EDGE_VECTORS["SM_SM"] * np.dot(state, EDGE_VECTORS["SM_SM"]) +
        EDGE_VECTORS["SM_SW"] * np.dot(state, EDGE_VECTORS["SM_SW"])
    )
    
    # Leaks (BETTI_5): SW_SW, SM_BW
    leak_vec = (
        EDGE_VECTORS["SW_SW"] * np.dot(state, EDGE_VECTORS["SW_SW"]) +
        EDGE_VECTORS["SM_BW"] * np.dot(state, EDGE_VECTORS["SM_BW"])
    )
    
    # Sinks (BETTI_7): BM_BW (Lensing), BW_BW
    sink_vec = (
        EDGE_VECTORS["BM_BW"] * np.dot(state, EDGE_VECTORS["BM_BW"]) +
        EDGE_VECTORS["BW_BW"] * np.dot(state, EDGE_VECTORS["BW_BW"])
    )
    
    # 4. Artifact Removal (The 12th Node Subtraction)
    # net_energy = (Bridges + Witness) - (Leaks + Sinks)
    # Lensing artifact (7.4) is explicitly countered here.
    lensing_artifact = EDGE_VECTORS["BM_BW"] * p.lensing_factor * np.dot(state, EDGE_VECTORS["BM_BW"])
    
    # Net energy term scaled by R4 (0.2828)
    net_physical = DELTA_T_OBS_DERIVED * (
        p.w_bridge * bridge_vec + 
        p.w_leak * (-leak_vec) +
        p.w_sink * (-sink_vec - lensing_artifact)
    )

    # 5. Torsion and Spark
    # Formula: R_138.88 * [ (Un^2 + B0) + R4 * (Net_Physical) ]
    # core is Un^2. state_in is B0 (the starting seed).
    
    seed = np.array([BETTI_0, 0.0, 0.0, 0.0]) # B0 = 1.0
    post_core = core + seed + net_physical
    
    angle_sign = 1.0 if net_time_scale >= 0.0 else -1.0
    torsion_eff = TORSION_4D * (1.0 + helix["cancellation"])
    
    # Spark Ignition
    rotated = spark_torsion_4d(post_core, angle_deg=angle_sign * SPARK_ANGLE_DEG, torsion_4d=torsion_eff)
    
    # 6. Final State Transition
    # slotting based on net_time (removes time-symmetry noise)
    # Includes 0.02 Bremsstrahlung Tax as steady-state jitter
    slotting = 1.0 - (0.02 * abs(net_time_scale)) 
    
    gated_branch = slotting * rotated
    
    # Renormalize to prevent divergence (Stationary Resonance)
    norm = np.linalg.norm(gated_branch)
    if norm > 2.0:
        gated_branch = (gated_branch / norm) * 1.5 # Lock to resonance orbit
    
    # (1-G) * Observer + G * Reality
    state_out = ((1.0 - gate) * state) + (gate * gated_branch)
    
    return {
        "state_in": state,
        "phase_fill": phase_fill,
        "net_time": net_time_scale,
        "closure": CLOSURE_METRIC,
        "net_physical": net_physical,
        "state_out": state_out,
        "is_genuine": gate > 0.5
    }

def run_final_boss_simulation():
    print("=== Sovereign Final Boss Dynamics ===")
    print(f"Betti Ratio (11+1)/(5+7) = {CLOSURE_METRIC:.4f} (Target: 1.0)")
    print(f"Artifact Offset (Lensing) = {LENSING_ARTIFACT_SCALE}")
    print(f"Invariant Period = {DELTA_T_OBS_DERIVED}")
    
    # Initialize at Witness Seed (B0=1)
    state = np.array([1.0, 0.0, 0.0, 0.0])
    
    steps = 100
    for i in range(steps):
        fill = i / (steps - 1)
        res = sovereign_final_boss_step(state, fill)
        state = res["state_out"]
        
        if i % 10 == 0 or i == 28: # Highlight the 0.2828 mark
            mark = " [0.2828 GATE OPENED]" if i == 28 else ""
            print(f"Step {i:02d} | Phase {fill:.4f} | Net Energy {np.linalg.norm(res['net_physical']):.6f}{mark}")

if __name__ == "__main__":
    run_final_boss_simulation()
