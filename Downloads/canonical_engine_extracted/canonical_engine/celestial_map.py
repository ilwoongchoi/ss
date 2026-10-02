"""Assign each node to one of 13 celestial domains based on element Z and particle tag.

Output schema: {node: {"domain": int}} where int ∈ [1,13].

Domain table:
  1  Z 1-5   + photon          → H/He emission shell
  2  Z 1-10                    → M/K dwarf zone
  3  Z 11-20                   → G/F solar-like spiral arm
  4  Z 21-30                   → A/B hot main-sequence ring
  5  Z 31-40                   → Wolf-Rayet / strong stellar wind
  6  Z 41-50 + photon          → Planetary nebula shell
  7  neutrino / boson keyword  → Supernova / pulsar cluster
  8  Z 51-60                   → Blue-giant belt
  9  Z 61-92                   → Heavy-element neutron-rich zone
 10  dark_energy / dark_matter → Dark-matter halo
 11  Z > 92                    → Black-hole binary / jet
 12  z_boson / gluon & high-Z  → HLQG / quasar group
 13  everything else           → Cosmic-web filament
"""
from __future__ import annotations

import json
import pathlib
from typing import Dict

from .circuit_loader import NODES

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)
OUT_FILE = GEN_DIR / "celestial_map.json"


def _domain(node) -> int:
    raw_elem = node.element or ""
    try:
        z = int(raw_elem.split("(")[-1].rstrip(")"))
    except (ValueError, IndexError):
        z = 0
    particle = (node.particle or "").lower()

    # keyword overrides first (mutually exclusive)
    if "dark" in particle:
        return 10
    if "gluon" in particle and z > 92:
        return 12
    if "z_boson" in particle and z > 92:
        return 12
    if "neutrino" in particle or "boson" in particle:
        return 7

    # photon cases
    if "photon" in particle:
        if z <= 5:
            return 1
        if 41 <= z <= 50:
            return 6

    # Z-based bands
    if z <= 10:
        return 2
    if z <= 20:
        return 3
    if z <= 30:
        return 4
    if z <= 40:
        return 5
    if z <= 50:
        return 6
    if z <= 60:
        return 8
    if z <= 92:
        return 9
    return 11


cel_map: Dict[str, Dict[str, int]] = {}
for node in NODES.values():
    cel_map[node.name] = {"domain": _domain(node)}

OUT_FILE.write_text(json.dumps(cel_map, indent=2), encoding="utf-8")
print(f"Celestial mapping written for {len(cel_map)} nodes → {OUT_FILE.relative_to(pathlib.Path(__file__).parent.parent)}")
