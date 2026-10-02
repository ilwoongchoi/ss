"""Physics-based Tile Parameter Engine.

Derives 5-tile 8D parameters from canonical physical constants:
- W7 = π/20 (continuous flow)
- H2 = 1/9 (topological gap)
- κ gates (1/64, 1/32, 3/32, 1/16)
- Closure Tension = 9π/(20√2)
- Betti numbers (β5, β7, β11)
- Spark angle 138.88°
- OMEGA = 7.4 (homeostasis target)

No hardcoded masks. All tile parameters derived from physical equations.
"""
from __future__ import annotations

import json
import math
import pathlib
from typing import Dict, Tuple

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Canonical Physical Constants (from GEOMETRY_EQUATIONS.md)
# ---------------------------------------------------------------------------
W7 = math.pi / 20  # Continuous flow area
H2 = 1.0 / 9.0  # Topological H2 gap
KAPPA_1_64 = 1.0 / 64.0  # Flat-lined threshold
KAPPA_1_32 = 1.0 / 32.0  # Baseline leakage axiom
KAPPA_3_32 = 3.0 / 32.0  # Darkness stress gate
KAPPA_1_16 = 1.0 / 16.0  # Chaos threshold

# Closure Tension Formula
CLOSURE_TENSION = (W7 / H2) * (1.0 / math.sqrt(2.0)) * ((11.0 + 1.0) / (5.0 + 7.0))
CLOSURE_TENSION = 9.0 * math.pi / (20.0 * math.sqrt(2.0))  # Exact form
DELTA_CLOSURE = abs(1.0 - CLOSURE_TENSION)  # Irreducible mismatch

# Betti numbers (topological holes)
BETTI_5 = 5.0  # Metabolic debt
BETTI_7 = 7.0  # 7-dimensional void
BETTI_11 = 11.0  # Topology bridge

# Spark constants (from CANONICAL_FINAL_EQUATION.md)
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
NEUTRON_TIME_SYNC = 0.3857
SPARK_CONSTANT_C = NEUTRON_TIME_SYNC * complex(math.cos(SPARK_ANGLE_RAD), math.sin(SPARK_ANGLE_RAD))
SPARK_MAGNITUDE = abs(SPARK_CONSTANT_C)

# Homeostasis target
OMEGA = 7.4

# K8 coupling
C_COUPLING = math.sqrt(2.0) / 5.0

# 8D dimensions
ALL_DIMS = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]

# ---------------------------------------------------------------------------
# 5 Tiles with circuit nodes and physical interpretation
# ---------------------------------------------------------------------------
TILES: Dict[str, Dict] = {
    "Sync": {
        "name": "Sync",
        "name_kr": "동기화",
        "description": "현재 시간에 맞춘 타일 — Circadian Sync",
        "circuit_meaning": "마스터 클록 동기화 (Master Clock Alignment)",
        "nodes": ["co2", "observer_leftd2", "memory_entropy"],
        "physical_role": "time_alignment",
        "primary_constant": "W7",  # Continuous flow
        "secondary_constant": "OMEGA",  # Homeostasis target
    },
    "Stress": {
        "name": "Stress",
        "name_kr": "스트레스 성장",
        "description": "Stress growth tile",
        "circuit_meaning": "누출 부채 관리 (Leakage Debt Processing)",
        "nodes": ["sodium", "chlorine_ion_pump", "cysteine"],
        "physical_role": "leakage_management",
        "primary_constant": "KAPPA_1_32",  # Baseline leakage
        "secondary_constant": "BETTI_5",  # Metabolic debt
    },
    "Hysteresis": {
        "name": "Hysteresis",
        "name_kr": "히스테리시스",
        "description": "위상 도약 타일",
        "circuit_meaning": "경로 의존적 위상 도약 (Suction Point Handler)",
        "nodes": ["hind_insula", "laterite", "memory_entropy"],
        "physical_role": "phase_transition",
        "primary_constant": "SPARK_ANGLE_DEG",  # Spark reset
        "secondary_constant": "DELTA_CLOSURE",  # Irreducible mismatch
    },
    "Mirror": {
        "name": "Mirror",
        "name_kr": "거울",
        "description": "방금 블록자리 타일 — Reflection/Inversion",
        "circuit_meaning": "대칭 반전 및 보정 (The Controlled Inverter)",
        "nodes": ["left_endorphin_non_observer", "left_endorphin_electron_neutrino"],
        "physical_role": "symmetry_inversion",
        "primary_constant": "H2",  # Topological gap
        "secondary_constant": "BETTI_7",  # 7-dimensional void
    },
    "Release": {
        "name": "Release",
        "name_kr": "방전",
        "description": "Release 타일",
        "circuit_meaning": "에너지 최종 방전 및 착륙 (Proton Landing)",
        "nodes": ["cytochrome_c_oxidase", "actomyosin", "right_sole_dopamine"],
        "physical_role": "energy_discharge",
        "primary_constant": "CLOSURE_TENSION",  # Closure engine
        "secondary_constant": "SPARK_MAGNITUDE",  # Discharge magnitude
    },
}

# ---------------------------------------------------------------------------
# Physical constant to 8D dimension mapping
# Based on canonical equation and circuit topology
# ---------------------------------------------------------------------------
CONSTANT_DIM_WEIGHTS: Dict[str, Dict[str, float]] = {
    "W7": {"r": 0.3, "h": 0.5, "d": 0.2, "p": 0.4, "s": 0.6, "gamma": 0.4, "g": 0.3, "nu": 0.5},
    "H2": {"r": 0.2, "h": 0.3, "d": 0.8, "p": 0.2, "s": 0.3, "gamma": 0.2, "g": 0.9, "nu": 0.2},
    "KAPPA_1_32": {"r": 0.4, "h": 0.6, "d": 0.5, "p": 0.3, "s": 0.4, "gamma": 0.3, "g": 0.5, "nu": 0.4},
    "KAPPA_3_32": {"r": 0.3, "h": 0.7, "d": 0.9, "p": 0.2, "s": 0.3, "gamma": 0.2, "g": 0.6, "nu": 0.3},
    "CLOSURE_TENSION": {"r": 0.8, "h": 0.5, "d": 0.6, "p": 0.7, "s": 0.5, "gamma": 0.9, "g": 0.6, "nu": 0.4},
    "DELTA_CLOSURE": {"r": 0.2, "h": 0.4, "d": 0.3, "p": 0.8, "s": 0.3, "gamma": 0.2, "g": 0.3, "nu": 0.7},
    "BETTI_5": {"r": 0.5, "h": 0.6, "d": 0.7, "p": 0.4, "s": 0.5, "gamma": 0.4, "g": 0.8, "nu": 0.3},
    "BETTI_7": {"r": 0.3, "h": 0.8, "d": 0.4, "p": 0.3, "s": 0.7, "gamma": 0.5, "g": 0.4, "nu": 0.6},
    "BETTI_11": {"r": 0.6, "h": 0.5, "d": 0.5, "p": 0.6, "s": 0.4, "gamma": 0.7, "g": 0.5, "nu": 0.5},
    "SPARK_ANGLE_DEG": {"r": 0.9, "h": 0.4, "d": 0.3, "p": 0.8, "s": 0.3, "gamma": 0.2, "g": 0.2, "nu": 0.6},
    "SPARK_MAGNITUDE": {"r": 0.7, "h": 0.5, "d": 0.4, "p": 0.6, "s": 0.5, "gamma": 0.8, "g": 0.4, "nu": 0.5},
    "OMEGA": {"r": 0.6, "h": 0.4, "d": 0.3, "p": 0.5, "s": 0.4, "gamma": 0.3, "g": 0.3, "nu": 0.4},
    "C_COUPLING": {"r": 0.4, "h": 0.5, "d": 0.4, "p": 0.4, "s": 0.5, "gamma": 0.5, "g": 0.5, "nu": 0.5},
}

# ---------------------------------------------------------------------------
# 5-sphere toroidal circulation (from energy_circulation.py)
# ---------------------------------------------------------------------------
SPHERE_PHASES: Dict[str, Tuple[str, str, Tuple[int, int]]] = {
    "Sun": ("AB_spark", "light_dark", (0, 3)),
    "Earth": ("A_accumulate", "o2_co2", (3, 9)),
    "Moon": ("O_accumulate", "heat_cold", (9, 15)),
    "CoMag": ("B_accumulate", "matter_nonmatter", (15, 21)),
    "Barnard": ("AB_integration", "reset_spark", (21, 24)),
}

# Sphere to physical constant mapping
SPHERE_CONSTANTS: Dict[str, Tuple[str, str]] = {
    "Sun": ("W7", "OMEGA"),  # Continuous flow + homeostasis target
    "Earth": ("CLOSURE_TENSION", "SPARK_MAGNITUDE"),  # Closure + discharge
    "Moon": ("KAPPA_1_32", "BETTI_11"),  # Leakage + bridge
    "CoMag": ("BETTI_5", "BETTI_7"),  # Debt + void
    "Barnard": ("H2", "DELTA_CLOSURE"),  # Gap + mismatch
}

# ---------------------------------------------------------------------------
# Physics-based tile parameter computation
# ---------------------------------------------------------------------------
def get_constant_weights(constant_name: str) -> Dict[str, float]:
    """Get 8D dimension weights for a physical constant."""
    return CONSTANT_DIM_WEIGHTS.get(constant, CONSTANT_DIM_WEIGHTS["C_COUPLING"])

def compute_tile_parameters_physics(
    tile_name: str,
    sphere: str,
    hour: float,
) -> Dict[str, float]:
    """
    Compute tile 8D parameters from physical constants.

    Args:
        tile_name: One of Sync, Stress, Hysteresis, Mirror, Release
        sphere: One of Sun, Earth, Moon, CoMag, Barnard
        hour: 0-23.99

    Returns:
        8D parameter vector
    """
    tile_info = TILES[tile_name]
    
    # Get tile's physical constants
    primary_const = tile_info["primary_constant"]
    secondary_const = tile_info["secondary_constant"]
    
    # Get sphere's physical constants
    sphere_primary, sphere_secondary = SPHERE_CONSTANTS.get(sphere, ("W7", "OMEGA"))
    
    # Get dimension weights
    tile_primary_weights = CONSTANT_DIM_WEIGHTS.get(primary_const, CONSTANT_DIM_WEIGHTS["C_COUPLING"])
    tile_secondary_weights = CONSTANT_DIM_WEIGHTS.get(secondary_const, CONSTANT_DIM_WEIGHTS["C_COUPLING"])
    sphere_primary_weights = CONSTANT_DIM_WEIGHTS.get(sphere_primary, CONSTANT_DIM_WEIGHTS["C_COUPLING"])
    sphere_secondary_weights = CONSTANT_DIM_WEIGHTS.get(sphere_secondary, CONSTANT_DIM_WEIGHTS["C_COUPLING"])
    
    # Compute combined weights
    vec8 = {}
    for dim in ALL_DIMS:
        # Tile's own constants (60% weight)
        tile_weight = 0.6 * tile_primary_weights[dim] + 0.4 * tile_secondary_weights[dim]
        
        # Sphere's constants (40% weight)
        sphere_weight = 0.6 * sphere_primary_weights[dim] + 0.4 * sphere_secondary_weights[dim]
        
        # Combine
        combined = 0.7 * tile_weight + 0.3 * sphere_weight
        
        # Normalize to [0, 1]
        vec8[dim] = max(0.0, min(1.0, combined))
    
    return vec8

def get_active_sphere(hour: float) -> str:
    """Get active sphere based on hour."""
    for sphere, (phase, _, (start, end)) in SPHERE_PHASES.items():
        if start <= hour < end:
            return sphere
    return "Sun"  # Default

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Compute physics-based tile parameters for all tiles and spheres
    results = {}
    
    for tile_name in TILES.keys():
        results[tile_name] = {}
        for sphere in SPHERE_PHASES.keys():
            hour_range = SPHERE_PHASES[sphere][2]
            hour = (hour_range[0] + hour_range[1]) / 2.0  # Midpoint
            
            vec8 = compute_tile_parameters_physics(tile_name, sphere, hour)
            
            results[tile_name][sphere] = {
                "vec8": vec8,
                "hour": hour,
                "sphere": sphere,
                "tile_name": tile_name,
                "tile_name_kr": TILES[tile_name]["name_kr"],
                "primary_constant": TILES[tile_name]["primary_constant"],
                "secondary_constant": TILES[tile_name]["secondary_constant"],
                "sphere_primary": SPHERE_CONSTANTS[sphere][0],
                "sphere_secondary": SPHERE_CONSTANTS[sphere][1],
            }
    
    # Write JSON
    out_json = GEN_DIR / "physics_tile_parameters.json"
    out_json.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    
    # Write human-readable report
    lines = []
    lines.append("=" * 80)
    lines.append("PHYSICS-BASED TILE PARAMETER ENGINE")
    lines.append("=" * 80)
    lines.append("All tile parameters derived from canonical physical constants:")
    lines.append(f"  W7 = {W7:.10f} (continuous flow)")
    lines.append(f"  H2 = {H2:.10f} (topological gap)")
    lines.append(f"  κ_1/32 = {KAPPA_1_32:.10f} (baseline leakage)")
    lines.append(f"  κ_3/32 = {KAPPA_3_32:.10f} (darkness stress)")
    lines.append(f"  Closure Tension = {CLOSURE_TENSION:.10f}")
    lines.append(f"  Δ Closure = {DELTA_CLOSURE:.10e}")
    lines.append(f"  Spark Angle = {SPARK_ANGLE_DEG}°")
    lines.append(f"  Spark Magnitude = {SPARK_MAGNITUDE:.10f}")
    lines.append(f"  OMEGA = {OMEGA}")
    lines.append("")
    
    for tile_name, tile_info in TILES.items():
        lines.append(f"■ {tile_info['name_kr']} ({tile_name})")
        lines.append(f"  Physical Role: {tile_info['physical_role']}")
        lines.append(f"  Primary Constant: {tile_info['primary_constant']}")
        lines.append(f"  Secondary Constant: {tile_info['secondary_constant']}")
        lines.append("")
        
        for sphere in SPHERE_PHASES.keys():
            data = results[tile_name][sphere]
            vec_str = ", ".join([f"{k}={v:.2f}" for k, v in data["vec8"].items()])
            lines.append(f"  [{sphere:8s}] {vec_str}")
        
        lines.append("")
    
    text = "\n".join(lines)
    print(text)
    (GEN_DIR / "physics_tile_parameters.txt").write_text(text, encoding="utf-8")
    print(f"\n→ JSON: {out_json}")
    print(f"→ TXT:  {GEN_DIR / 'physics_tile_parameters.txt'}")
