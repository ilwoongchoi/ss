"""Map each circuit node to one of 13 disciplinary/physical domains.

Output: generated/domain_map.json
"""
from __future__ import annotations

import json
import pathlib
from typing import Dict, List, Tuple

from .circuit_loader import NODES

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)
OUT_FILE = GEN_DIR / "domain_map.json"

# Order matters: first match wins
DOMAINS: List[Tuple[str, Tuple[str, ...]]] = [
    ("biochemistry", (
        "heme", "cytochrome", "ferritin", "cysteine", "glymphatic", "sulforaphane",
        "methanogenesis", "histosol", "pentose_phosphate", "disulfide_bond",
        "methylation", "chlorine_ion_pump", "substance_p", "methionine",
    )),
    ("neurochemistry", (
        "dopamine", "acetylcholine", "gaba", "endorphin", "oxytocin", "mc1r",
        "insula", "hippocampus", "glutamate", "temporalis", "frontalis",
        "occipitalis", "genital_d2", "right_love", "left_extraversion",
        "right_extraversion", "left_frontalis",
    )),
    ("microbial", (
        "methanogenesis", "histosol", "autophagy", "sulforaphane",
    )),
    ("soil_geology", (
        "clay_gouge", "steel", "cambisol", "andosol", "podzol", "laterite",
        "large_igneous_province", "subduction_zone", "fold_belt", "craton", "basin",
        "thorium", "monazite", "magnetite", "quark_orogen", "gluon_orogen",
        "copper_iron_complex", "pyrite", "caco3",
    )),
    ("mantle", (
        "lower_mantle", "outer_core_convection", "plume", "quark_orogen_magma",
    )),
    ("atmosphere_hydrosphere", (
        "water_vapour", "water", "nacl", "sodium", "co2", "chlorine_ion_pump",
        "heath_aerenchyma", "mangrove_aerenchyma",
    )),
    ("biology_muscle", (
        "actomyosin", "adapter_protein", "collagen", "right_sole_dopamine",
        "muscle_a", "muscle_b",
    )),
    ("astronomy", (
        "photon", "dark_energy", "large_igneous_province", "plume", "aurora",
        "star", "nebula",
    )),
    ("black_hole_gravity", (
        "dark_matter", "graviton", "black_hole", "singularity",
    )),
    ("particle_physics", (
        "quark", "gluon", "w_boson", "z_boson", "higgs", "neutron", "proton",
        "electron", "muon", "tau",
    )),
    ("math_dynamics", (
        "memory_entropy", "hind_insula", "adapter_protein",
        "left_endorphin_non_observer", "observer_leftd2", "nonobserver_left_d2",
    )),
    ("energy_thermodynamics", (
        "sulfur_iron_complex", "pyrite", "lactate_dehydrogenase",
        "succinate_dehydrogenase", "carbon", "heme",
    )),
    ("time_history", (
        "co2", "laterite", "basin", "lower_mantle", "gluon_orogen", "memory_entropy",
    )),
]


def _domain(node) -> str:
    text = f"{node.name} {node.element} {node.particle} {node.group}".lower()
    for domain, keywords in DOMAINS:
        for kw in keywords:
            if kw in text:
                return domain
    return "other"


domain_map: Dict[str, Dict[str, str]] = {}
for node in NODES.values():
    domain_map[node.name] = {"domain": _domain(node)}

OUT_FILE.write_text(json.dumps(domain_map, indent=2), encoding="utf-8")
print(f"Domain mapping written for {len(domain_map)} nodes → {OUT_FILE.relative_to(pathlib.Path(__file__).parent.parent)}")
