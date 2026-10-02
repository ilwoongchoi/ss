"""5-Tile Recommendation Engine using existing canonical data.

Combines:
  1. 128-slot 8D vectors (128_UNIFIED_MASTER_8D_fixed.csv)
  2. 5-sphere toroidal circulation (energy_circulation.py)
  3. 4 stress pairs with toroidal mapping
  4. 3 attractors with circuit loops
  5. 5 tiles with circuit node mappings

Deterministic flow:
  Current time → circadian phase → active stress pair → active sphere
  → sphere-specific 8D modulation → tile-specific 8D base → final tile 8D
"""
from __future__ import annotations

import csv
import json
import pathlib
from typing import Dict, List, Tuple

from .circuit_loader import NODES

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)

ROOT = pathlib.Path(__file__).parent.parent
CSV_128 = ROOT / "128_UNIFIED_MASTER_8D_fixed.csv"

# ---------------------------------------------------------------------------
# 5 Tiles with circuit nodes and 8D dimensions
# ---------------------------------------------------------------------------
TILES: Dict[str, Dict] = {
    "Sync": {
        "name": "Sync",
        "name_kr": "동기화",
        "description": "현재 시간에 맞춘 타일 — Circadian Sync",
        "circuit_meaning": "마스터 클록 동기화 (Master Clock Alignment)",
        "nodes": ["co2", "observer_leftd2", "memory_entropy"],
        "dims": ("r", "p"),  # rhythm, periodicity
        "sphere_primary": "Moon",  # time regulator
        "sphere_secondary": "Sun",  # spark source
    },
    "Stress": {
        "name": "Stress",
        "name_kr": "스트레스 성장",
        "description": "Stress growth tile",
        "circuit_meaning": "누출 부채 관리 (Leakage Debt Processing)",
        "nodes": ["sodium", "chlorine_ion_pump", "cysteine"],
        "dims": ("h", "d"),  # harmonic, dissonance
        "sphere_primary": "Earth",  # repair engine
        "sphere_secondary": "Barnard",  # mass storage
    },
    "Hysteresis": {
        "name": "Hysteresis",
        "name_kr": "히스테리시스",
        "description": "위상 도약 타일",
        "circuit_meaning": "경로 의존적 위상 도약 (Suction Point Handler)",
        "nodes": ["hind_insula", "laterite", "memory_entropy"],
        "dims": ("p", "nu"),  # periodicity, self-similarity
        "sphere_primary": "Moon",  # time clock
        "sphere_secondary": "CoMag",  # bridge coupling
    },
    "Mirror": {
        "name": "Mirror",
        "name_kr": "거울",
        "description": "방금 블록자리 타일 — Reflection/Inversion",
        "circuit_meaning": "대칭 반전 및 보정 (The Controlled Inverter)",
        "nodes": ["left_endorphin_non_observer", "left_endorphin_electron_neutrino"],
        "dims": ("s", "g"),  # brightness, binding
        "sphere_primary": "Sun",  # spark source
        "sphere_secondary": "CoMag",  # sulfur bridge
    },
    "Release": {
        "name": "Release",
        "name_kr": "방전",
        "description": "Release 타일",
        "circuit_meaning": "에너지 최종 방전 및 착륙 (Proton Landing)",
        "nodes": ["cytochrome_c_oxidase", "actomyosin", "right_sole_dopamine"],
        "dims": ("gamma", "d"),  # expansion, dissonance
        "sphere_primary": "Earth",  # oxygen repair
        "sphere_secondary": "Barnard",  # mass discharge
    },
}

ALL_DIMS = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]

# ---------------------------------------------------------------------------
# 5 Sphere 8D activation profiles
# ---------------------------------------------------------------------------
SPHERE_DIM_PROFILES: Dict[str, Dict[str, float]] = {
    "Sun": {"r": 0.8, "s": 0.8, "h": 0.3, "d": 0.2, "p": 0.3, "gamma": 0.4, "g": 0.3, "nu": 0.2},
    "Earth": {"r": 0.3, "s": 0.4, "h": 0.7, "d": 0.5, "p": 0.4, "gamma": 0.8, "g": 0.6, "nu": 0.3},
    "Moon": {"r": 0.4, "s": 0.3, "h": 0.4, "d": 0.4, "p": 0.9, "gamma": 0.3, "g": 0.4, "nu": 0.8},
    "CoMag": {"r": 0.3, "s": 0.5, "h": 0.5, "d": 0.6, "p": 0.4, "gamma": 0.7, "g": 0.9, "nu": 0.4},
    "Barnard": {"r": 0.2, "s": 0.3, "h": 0.4, "d": 0.8, "p": 0.3, "gamma": 0.4, "g": 0.9, "nu": 0.3},
}

# ---------------------------------------------------------------------------
# Load 128-slot vectors
# ---------------------------------------------------------------------------
def load_128_vectors() -> Dict[str, Dict[str, float]]:
    """Load 128-slot 8D vectors from CSV."""
    vectors = {}
    if not CSV_128.exists():
        print(f"Warning: {CSV_128} not found, using zeros")
        return {}
    with CSV_128.open(encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            key = row.get("profile_key") or row.get("key") or row.get("slot")
            if not key:
                continue
            vec = {}
            for dim in ALL_DIMS:
                val = row.get(dim, "0").strip()
                try:
                    vec[dim] = float(val)
                except:
                    vec[dim] = 0.0
            vectors[key] = vec
    return vectors

_128_VECTORS = load_128_vectors()

# ---------------------------------------------------------------------------
# Circadian phase from hour
# ---------------------------------------------------------------------------
def phase_from_hour(hour: float) -> str:
    if 0 <= hour < 3:
        return "AB_spark"
    if 3 <= hour < 9:
        return "A_accumulate"
    if 9 <= hour < 15:
        return "O_accumulate"
    if 15 <= hour < 21:
        return "B_accumulate"
    return "AB_integration"

# Phase → active stress pair → active sphere
PHASE_MAPPING: Dict[str, Tuple[str, str]] = {
    "AB_spark": ("light_dark", "Sun"),
    "A_accumulate": ("o2_co2", "Earth"),
    "O_accumulate": ("heat_cold", "Moon"),
    "B_accumulate": ("matter_nonmatter", "CoMag"),
    "AB_integration": ("reset_spark", "Barnard"),
}

# ---------------------------------------------------------------------------
# Tile recommendation computation
# ---------------------------------------------------------------------------
def compute_tile_recommendations(
    profile_key: str,
    hour: float,
    layer: str = "A",
) -> Dict[str, Dict]:
    """
    Compute deterministic 8D recommendations for all 5 tiles.

    Args:
        profile_key: e.g. "ENFP_F_O"
        hour: 0-23.99
        layer: A/B/C/D (RH layer)

    Returns:
        Dict mapping tile name to {vec8, sphere_influence, phase, ...}
    """
    # 1. Get circadian phase and active sphere
    phase = phase_from_hour(hour)
    stress_pair, active_sphere = PHASE_MAPPING.get(phase, ("light_dark", "Sun"))

    # 2. Get base 128-slot vector for this profile
    slot_key = f"{profile_key}_{layer}"
    base_vec = _128_VECTORS.get(slot_key, _128_VECTORS.get(profile_key, {}))
    if not base_vec:
        base_vec = {dim: 0.5 for dim in ALL_DIMS}

    # 3. Get sphere modulation profile
    sphere_profile = SPHERE_DIM_PROFILES.get(active_sphere, SPHERE_DIM_PROFILES["Sun"])

    # 4. Compute each tile's recommendation
    results = {}
    for tile_name, tile_info in TILES.items():
        # Tile-specific base: emphasize tile's dims, de-emphasize others
        tile_vec = {}
        for dim in ALL_DIMS:
            base_val = base_vec.get(dim, 0.5)
            if dim in tile_info["dims"]:
                # Tile's primary dims: boost by sphere influence
                sphere_mod = sphere_profile.get(dim, 0.5)
                tile_vec[dim] = base_val * 0.7 + sphere_mod * 0.3
            else:
                # Non-primary dims: keep closer to base
                tile_vec[dim] = base_val * 0.9 + sphere_profile.get(dim, 0.5) * 0.1

        # Apply sphere-specific modulation
        primary_sphere = tile_info["sphere_primary"]
        secondary_sphere = tile_info["sphere_secondary"]
        primary_profile = SPHERE_DIM_PROFILES.get(primary_sphere, {})
        secondary_profile = SPHERE_DIM_PROFILES.get(secondary_sphere, {})

        final_vec = {}
        for dim in ALL_DIMS:
            val = tile_vec[dim]
            if dim in tile_info["dims"]:
                # Strong modulation from primary sphere
                val = val * 0.6 + primary_profile.get(dim, 0.5) * 0.4
            else:
                # Weak modulation from secondary sphere
                val = val * 0.8 + secondary_profile.get(dim, 0.5) * 0.2
            final_vec[dim] = max(0.0, min(1.0, val))

        results[tile_name] = {
            "vec8": final_vec,
            "tile_name": tile_info["name"],
            "tile_name_kr": tile_info["name_kr"],
            "description": tile_info["description"],
            "circuit_meaning": tile_info["circuit_meaning"],
            "nodes": tile_info["nodes"],
            "dims": tile_info["dims"],
            "primary_sphere": primary_sphere,
            "secondary_sphere": secondary_sphere,
            "phase": phase,
            "active_sphere": active_sphere,
            "stress_pair": stress_pair,
            "hour": hour,
            "profile_key": profile_key,
            "layer": layer,
        }

    return results

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Demo: compute for a sample profile at different hours
    demo_profile = "ENFP_F_O"
    demo_hours = [0, 6, 12, 18, 21]

    all_results = {}
    for h in demo_hours:
        all_results[f"hour_{h:02d}"] = compute_tile_recommendations(demo_profile, h)

    # Write JSON
    out_json = GEN_DIR / "tile_recommendations.json"
    out_json.write_text(
        json.dumps(all_results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Write human-readable report
    lines = []
    lines.append("=" * 80)
    lines.append("5-TILE RECOMMENDATION ENGINE (Deterministic)")
    lines.append("=" * 80)
    lines.append(f"Profile: {demo_profile}")
    lines.append("")

    for h in demo_hours:
        phase = phase_from_hour(h)
        _, active_sphere = PHASE_MAPPING.get(phase, ("light_dark", "Sun"))
        lines.append(f"■ Hour {h:02d}:00 — Phase: {phase} — Active Sphere: {active_sphere}")
        lines.append("-" * 80)

        recs = compute_tile_recommendations(demo_profile, h)
        for tile_name, rec in recs.items():
            vec_str = ", ".join([f"{k}={v:.2f}" for k, v in rec["vec8"].items()])
            lines.append(f"  {rec['tile_name_kr']:8s} ({tile_name:8s})")
            lines.append(f"    dims: {rec['dims']}")
            lines.append(f"    spheres: {rec['primary_sphere']} + {rec['secondary_sphere']}")
            lines.append(f"    vec8:  {vec_str}")
            lines.append("")

        lines.append("")

    text = "\n".join(lines)
    print(text)
    (GEN_DIR / "tile_recommendations.txt").write_text(text, encoding="utf-8")
    print(f"\n→ JSON: {out_json}")
    print(f"→ TXT:  {GEN_DIR / 'tile_recommendations.txt'}")
