"""Proximal Area Resonance: Why all subjects co-locate and exchange energy.

Core thesis: The circuit's 4 stress pairs drive geological processes that create
specific soil types. Those soils support specific biomes and food chains. Human
haplogroups adapted to those biomes over 50,000+ years. The 8D vector of each
subject (particle, organism, human, biochemistry, geology) resonates with the
underlying geological node's stress pair. Temporal jetlag (circadian phase offset)
creates resonance windows where co-located subjects exchange energy.

This script:
  1. Defines proximal areas centered on geological nodes
  2. Identifies ALL co-located subjects within each area
  3. Explains the historical/evolutionary reason for co-location
  4. Formalizes resonance strength between co-located subjects
  5. Maps temporal jetlag — when each subject's stress pair activates
  6. Computes energy exchange dynamics within each proximal area

Outputs:
  generated/proximal_resonance_report.txt  — full explanation
  generated/proximal_resonance.json        — structured data
  generated/proximal_resonance_map.png     — visualization
"""
from __future__ import annotations

import json
import math
import pathlib
from typing import Dict, List, Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)

import sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from haplogroup_vector_mapping import Y_DNA, MTDNA, ETHNIC_ARCHETYPES
from canonical_engine.earth_energy_map import (
    Y_DNA_COORDS, MTDNA_COORDS, GEO_NODE_COORDS,
    SPHERE_PROJECTIONS, ATTRACTOR_CENTERS,
    haversine, STRESS_PAIRS,
)

# ===========================================================================
# 1. PROXIMAL AREA DEFINITIONS
# ===========================================================================
# Each proximal area is centered on a geological node.
# Radius: ~2000km (great circle) defines the co-location zone.

PROXIMAL_RADIUS_KM = 2500

# ===========================================================================
# 2. NON-HUMAN BIOLOGICAL SUBJECTS (fauna/flora/microbiome per biome)
# ===========================================================================

BIOME_SUBJECTS: Dict[str, List[Dict]] = {
    "boreal": [
        {"name": "reindeer (Rangifer tarandus)", "type": "mammal", "element": "Fe", "particle": "muon",
         "dims": ("h", "d"), "stress": "heat_cold", "role": "migratory anchor, iron-blood cold adaptation"},
        {"name": "Siberian larch (Larix sibirica)", "type": "plant", "element": "C", "particle": "photon",
         "dims": ("gamma", "h"), "stress": "light_dark", "role": "deciduous conifer, seasonal light gate"},
        {"name": "mycorrhizal fungi (Suillus)", "type": "fungi", "element": "N", "particle": "electron_neutrino",
         "dims": ("g", "nu"), "stress": "matter_nonmatter", "role": "soil binding, nitrogen fixation proxy"},
        {"name": "podzol soil microbiome", "type": "microbiome", "element": "Si", "particle": "graviton",
         "dims": ("p", "nu"), "stress": "heat_cold", "role": "acidic leach, slow decomposition"},
    ],
    "tropical": [
        {"name": "African elephant (Loxodonta)", "type": "mammal", "element": "Ca", "particle": "electron",
         "dims": ("r", "s"), "stress": "o2_co2", "role": "keystone herbivore, calcium bone mass"},
        {"name": "Ficus (strangler fig)", "type": "plant", "element": "C", "particle": "photon",
         "dims": ("gamma", "g"), "stress": "light_dark", "role": "canopy dominance, light competition"},
        {"name": "termites (Macrotermes)", "type": "insect", "element": "Si", "particle": "graviton",
         "dims": ("p", "g"), "stress": "o2_co2", "role": "soil engineering, methane production"},
        {"name": "Ferralsol microbiome", "type": "microbiome", "element": "Fe", "particle": "quark",
         "dims": ("s", "d"), "stress": "matter_nonmatter", "role": "iron oxide lock, P+ sequestration"},
    ],
    "volcanic": [
        {"name": "extremophile archaea (Sulfolobus)", "type": "archaea", "element": "S", "particle": "gluon",
         "dims": ("g", "nu"), "stress": "matter_nonmatter", "role": "sulfur oxidation, Nrf2 analog"},
        {"name": "volcanic grass (Miscanthus)", "type": "plant", "element": "P", "particle": "higgs",
         "dims": ("p", "h"), "stress": "o2_co2", "role": "phosphorus accumulator, pioneer species"},
        {"name": "Andosol microbiome", "type": "microbiome", "element": "Al", "particle": "down_quark",
         "dims": ("d", "s"), "stress": "o2_co2", "role": "allophane mineral, phosphorus retention"},
    ],
    "desert": [
        {"name": "dromedary camel (Camelus dromedarius)", "type": "mammal", "element": "Na", "particle": "w_boson",
         "dims": ("r", "nu"), "stress": "heat_cold", "role": "water conservation, sodium pump"},
        {"name": "date palm (Phoenix dactylifera)", "type": "plant", "element": "K", "particle": "photon",
         "dims": ("gamma", "p"), "stress": "light_dark", "role": "oasis anchor, potassium salt tolerance"},
        {"name": "halophile archaea (Haloquadratum)", "type": "archaea", "element": "Cl", "particle": "gluon",
         "dims": ("g", "d"), "stress": "matter_nonmatter", "role": "salt crystallization, chlorine pump analog"},
        {"name": "Arenosol microbiome", "type": "microbiome", "element": "Si", "particle": "graviton",
         "dims": ("p", "nu"), "stress": "o2_co2", "role": "quartz sand, minimal organic buffer"},
    ],
    "mountain": [
        {"name": "snow leopard (Panthera uncia)", "type": "mammal", "element": "Mg", "particle": "muon",
         "dims": ("h", "d"), "stress": "heat_cold", "role": "apex predator, altitude hypoxia adaptation"},
        {"name": "rhododendron (Rhododendron)", "type": "plant", "element": "B", "particle": "graviton",
         "dims": ("p", "gamma"), "stress": "light_dark", "role": "MC1R analog, UV tolerance"},
        {"name": "Leptosol microbiome", "type": "microbiome", "element": "Mn", "particle": "muon_antineutrino",
         "dims": ("h", "nu"), "stress": "heat_cold", "role": "skeletal soil, direct Z-boson foundation"},
    ],
    "steppe": [
        {"name": "Przewalski's horse (Equus ferus)", "type": "mammal", "element": "Fe", "particle": "quark",
         "dims": ("r", "s"), "stress": "matter_nonmatter", "role": "nomadic grazer, iron-blood kinetic"},
        {"name": "Stipa feather grass", "type": "plant", "element": "C", "particle": "photon",
         "dims": ("gamma", "p"), "stress": "light_dark", "role": "steppe anchor, deep root periodicity"},
        {"name": "Chernozem microbiome", "type": "microbiome", "element": "C", "particle": "photon",
         "dims": ("g", "h"), "stress": "o2_co2", "role": "maximal organic carbon, gluon homeostasis"},
    ],
    "rift": [
        {"name": "gelada baboon (Theropithecus)", "type": "mammal", "element": "Fe", "particle": "quark",
         "dims": ("r", "p"), "stress": "matter_nonmatter", "role": "highland primate, iron-rich diet"},
        {"name": "acacia (Vachellia)", "type": "plant", "element": "N", "particle": "electron_neutrino",
         "dims": ("g", "nu"), "stress": "o2_co2", "role": "nitrogen fixation, rift valley transmitter"},
        {"name": "Nitisol microbiome", "type": "microbiome", "element": "Fe", "particle": "quark",
         "dims": ("s", "d"), "stress": "matter_nonmatter", "role": "iron antenna, P+ stored at surface"},
    ],
    "temperate": [
        {"name": "red fox (Vulpes vulpes)", "type": "mammal", "element": "Cu", "particle": "muon_neutrino",
         "dims": ("r", "gamma"), "stress": "light_dark", "role": "adaptable predator, copper metabolism"},
        {"name": "oak (Quercus robur)", "type": "plant", "element": "C", "particle": "photon",
         "dims": ("gamma", "h"), "stress": "light_dark", "role": "keystone tree, tannin binding"},
        {"name": "Cambisol microbiome", "type": "microbiome", "element": "Si", "particle": "graviton",
         "dims": ("p", "g"), "stress": "o2_co2", "role": "moderate weathering, balanced nutrient cycling"},
    ],
    "pelagic": [
        {"name": "blue whale (Balaenoptera musculus)", "type": "mammal", "element": "Fe", "particle": "quark",
         "dims": ("s", "g"), "stress": "matter_nonmatter", "role": "largest organism, iron ocean fertilization"},
        {"name": "diatom (Thalassiosira)", "type": "algae", "element": "Si", "particle": "graviton",
         "dims": ("p", "gamma"), "stress": "o2_co2", "role": "silica frustule, ocean carbon pump"},
        {"name": "Prochlorococcus", "type": "cyanobacteria", "element": "O", "particle": "photon",
         "dims": ("gamma", "s"), "stress": "light_dark", "role": "most abundant photosynthesizer, O2 production"},
    ],
    "permafrost": [
        {"name": "musk ox (Ovibos moschatus)", "type": "mammal", "element": "Fe", "particle": "quark",
         "dims": ("h", "d"), "stress": "heat_cold", "role": "arctic survivor, qiviut insulation"},
        {"name": "Sphagnum moss", "type": "plant", "element": "C", "particle": "photon",
         "dims": ("g", "nu"), "stress": "matter_nonmatter", "role": "peat accumulator, carbon lock"},
        {"name": "Cryosol microbiome", "type": "microbiome", "element": "H", "particle": "right_testosterone",
         "dims": ("d", "s"), "stress": "heat_cold", "role": "frozen organic matter, methane reservoir"},
    ],
    "subduction": [
        {"name": "deep-sea tube worm (Riftia pachyptila)", "type": "invertebrate", "element": "S", "particle": "gluon",
         "dims": ("g", "nu"), "stress": "matter_nonmatter", "role": "hydrothermal vent, sulfur chemosynthesis"},
        {"name": "vent archaea (Methanopyrus)", "type": "archaea", "element": "P", "particle": "higgs",
         "dims": ("p", "h"), "stress": "o2_co2", "role": "methanogenesis at 122°C, extremophile limit"},
        {"name": "manganese nodule microbiome", "type": "microbiome", "element": "Mn", "particle": "muon_antineutrino",
         "dims": ("h", "nu"), "stress": "matter_nonmatter", "role": "deep-sea metal precipitation"},
    ],
}

# Map geological nodes to biomes
GEO_TO_BIOME: Dict[str, str] = {
    "steel": "temperate", "clay_gouge": "mountain", "craton": "steppe",
    "laterite": "tropical", "podzol": "boreal", "andosol": "volcanic",
    "cambisol": "temperate", "histosol": "permafrost", "pyrite": "subduction",
    "fold_belt": "mountain", "subduction_zone": "subduction", "basin": "desert",
    "monazite": "rift", "plume": "volcanic", "large_igneous_province": "boreal",
    "manganese_nodule": "pelagic", "gluon_orogen": "mountain",
    "outer_core_convection": "pelagic", "lower_mantle": "pelagic",
    "oxidised_manganese": "rift", "magnetite": "temperate",
    "thorium": "desert", "quark_orogen_magma": "volcanic",
    "succinate_dehydrogenase": "temperate", "ferritin": "temperate",
}

# ===========================================================================
# 3. CIRCADIAN JETLAG PHASES
# ===========================================================================
# Each stress pair has a circadian activation window.
# "Jetlag" = the phase offset between a subject's native stress pair
# and the local geological node's stress pair.
# When jetlag = 0, subjects are in sync (maximum resonance).
# When jetlag = 12h, subjects are anti-phase (minimum resonance, stress).

CIRCADIAN_HOURS = {
    "o2_co2": (3, 9),        # A_accumulate
    "heat_cold": (9, 15),    # O_accumulate
    "matter_nonmatter": (15, 21),  # B_accumulate
    "light_dark": (0, 3),    # AB_spark (also 21-3)
    "reset_spark": (21, 3),  # AB_integration
}

def circadian_center(sp: str) -> float:
    """Center hour of circadian window."""
    h = CIRCADIAN_HOURS.get(sp, (0, 12))
    return (h[0] + h[1]) / 2.0

def jetlag_hours(sp1: str, sp2: str) -> float:
    """Phase difference in hours between two stress pairs."""
    c1 = circadian_center(sp1)
    c2 = circadian_center(sp2)
    diff = abs(c1 - c2)
    if diff > 12:
        diff = 24 - diff
    return diff

def resonance_from_jetlag(jl: float) -> float:
    """Resonance strength from jetlag (0h=1.0, 12h=0.0)."""
    return max(0.0, 1.0 - jl / 12.0)

# ===========================================================================
# 4. FIND CO-LOCATED SUBJECTS
# ===========================================================================

def find_colocated(geo_name: str, geo: Dict) -> Dict:
    """Find all subjects co-located within PROXIMAL_RADIUS_KM of a geological node."""

    geo_lat, geo_lon = geo["lat"], geo["lon"]
    geo_sp = geo["stress_pair"]
    biome = GEO_TO_BIOME.get(geo_name, "temperate")

    colocated = {
        "geological_node": geo_name,
        "geo_type": geo["geo_type"],
        "geo_label": geo["label"],
        "biome": biome,
        "stress_pair": geo_sp,
        "lat": geo_lat, "lon": geo_lon,
        "haplogroups": [],
        "mtdna": [],
        "ethnic_archetypes": [],
        "biological_subjects": [],
        "spheres": [],
        "attractors": [],
    }

    # Y-DNA haplogroups within radius
    for hg_key, hg_coord in Y_DNA_COORDS.items():
        dist = haversine(geo_lat, geo_lon, hg_coord["lat"], hg_coord["lon"])
        if dist <= PROXIMAL_RADIUS_KM and hg_key in Y_DNA:
            hg = Y_DNA[hg_key]
            jl = jetlag_hours(hg.get("stress_pair", geo_sp) if "stress_pair" in hg else geo_sp, geo_sp)
            # Determine haplogroup stress pair from its dominant dims
            v = hg["v"]
            dim_pairs = {
                "o2_co2": ("h", "p"), "heat_cold": ("nu", "r"),
                "matter_nonmatter": ("s", "g"), "light_dark": ("gamma", "d"),
            }
            best_sp = geo_sp
            best_sum = 0
            for sp, (d1, d2) in dim_pairs.items():
                s = v[d1] + v[d2]
                if s > best_sum:
                    best_sum = s
                    best_sp = sp
            jl = jetlag_hours(best_sp, geo_sp)
            colocated["haplogroups"].append({
                "key": hg_key,
                "label": hg_coord["label"],
                "soil": hg.get("soil", ""),
                "geology": hg.get("geology", ""),
                "blood": hg.get("blood", ""),
                "rh": hg.get("rh", ""),
                "vector8": hg["v"],
                "dominant_stress": best_sp,
                "jetlag_hours": round(jl, 2),
                "resonance": round(resonance_from_jetlag(jl), 4),
                "distance_km": round(dist, 1),
            })

    # mtDNA within radius
    for mt_key, mt_coord in MTDNA_COORDS.items():
        dist = haversine(geo_lat, geo_lon, mt_coord["lat"], mt_coord["lon"])
        if dist <= PROXIMAL_RADIUS_KM and mt_key in MTDNA:
            colocated["mtdna"].append({
                "key": mt_key,
                "label": mt_coord["label"],
                "distance_km": round(dist, 1),
            })

    # Ethnic archetypes within radius
    for ek, ec in ETHNIC_ARCHETYPES.items():
        # Use Y-DNA coordinate as proxy
        ydna_key = ek.get("ydna", "") if isinstance(ek, dict) else ""
        # Actually ETHNIC_ARCHETYPES keys are strings, values are dicts
        pass

    # Use ETHNIC_COORDS from earth_energy_map
    from canonical_engine.earth_energy_map import ETHNIC_COORDS
    for ek, ec in ETHNIC_COORDS.items():
        dist = haversine(geo_lat, geo_lon, ec["lat"], ec["lon"])
        if dist <= PROXIMAL_RADIUS_KM:
            ev = ETHNIC_ARCHETYPES.get(ek, {})
            colocated["ethnic_archetypes"].append({
                "key": ek,
                "label": ec["label"],
                "ydna": ev.get("ydna", ""),
                "mtdna": ev.get("mtdna", ""),
                "blood_type": ev.get("blood_type", ""),
                "vector8": ev.get("vector8", {}),
                "distance_km": round(dist, 1),
            })

    # Biological subjects from biome
    biome_subjects = BIOME_SUBJECTS.get(biome, [])
    for bs in biome_subjects:
        bs_sp = bs["stress"]
        jl = jetlag_hours(bs_sp, geo_sp)
        colocated["biological_subjects"].append({
            "name": bs["name"],
            "type": bs["type"],
            "element": bs["element"],
            "particle": bs["particle"],
            "dims": list(bs["dims"]),
            "stress": bs_sp,
            "role": bs["role"],
            "jetlag_hours": round(jl, 2),
            "resonance": round(resonance_from_jetlag(jl), 4),
        })

    # Spheres within radius
    for sp_name, sp in SPHERE_PROJECTIONS.items():
        dist = haversine(geo_lat, geo_lon, sp["lat"], sp["lon"])
        if dist <= PROXIMAL_RADIUS_KM * 3:  # spheres have wider influence
            colocated["spheres"].append({
                "name": sp_name,
                "label": sp["label"],
                "dims": list(sp["dims"]),
                "attractor": sp["attractor"],
                "distance_km": round(dist, 1),
            })

    # Attractors within radius
    for attr_name, attr in ATTRACTOR_CENTERS.items():
        dist = haversine(geo_lat, geo_lon, attr["lat"], attr["lon"])
        if dist <= PROXIMAL_RADIUS_KM * 3:
            colocated["attractors"].append({
                "name": attr_name,
                "label": attr["label"],
                "dims": list(attr["dims"]),
                "sphere": attr["sphere"],
                "distance_km": round(dist, 1),
            })

    return colocated


# ===========================================================================
# 5. HISTORICAL EXPLANATION FOR CO-LOCATION
# ===========================================================================

def explain_colocation(geo_name: str, colocated: Dict) -> str:
    """Generate historical/evolutionary explanation for why subjects co-locate."""

    geo = GEO_NODE_COORDS[geo_name]
    biome = colocated["biome"]
    geo_sp = colocated["stress_pair"]
    sp_info = STRESS_PAIRS.get(geo_sp, {})
    sp_dims = sp_info.get("dims", ())

    lines: List[str] = []
    lines.append(f"  HISTORICAL EXPLANATION:")
    lines.append(f"  The geological process '{geo['geo_type']}' creates '{geo['label']}'.")

    # Geological formation
    geo_history = {
        "iron_formation": "Banded iron formations precipitated from Fe²⁺ in anoxic oceans ~2.4Ga during the Great Oxidation Event. The O₂/CO₂ stress pair (h,p) drove iron oxidation, locking Fe³⁺ into sedimentary layers. Human populations on these formations inherit iron-rich substrates that select for specific blood types and hemoglobin variants.",
        "fault_gouge": "Fault gouge forms from tectonic friction along plate boundaries. The heat/cold stress pair (nu,r) governs the frictional heating vs. ambient cooling cycle. Clay minerals in the gouge zone retain water and create micro-environments that support unique microbiomes.",
        "craton": "Cratons are the oldest stable continental fragments (>3Ga). Their deep lithospheric roots resist deformation, creating stable platforms where deep soils (chernozems, kastanozems) accumulate. The matter/non-matter stress pair (s,g) governs the slow mass accumulation vs. binding energy balance over geological time.",
        "tropical_weathering": "Tropical laterites form through intense leaching in hot, humid climates. The O₂/CO₂ stress pair (h,p) drives rapid organic decomposition, leaving iron and aluminum oxides. Human haplogroups here evolved high r (motor/kinetic) for tropical energy expenditure and adapted to iron-locked phosphorus deficiency.",
        "boreal_soil": "Podzols form under cold, acidic coniferous forests. The heat/cold stress pair (nu,r) governs the freeze-thaw cycle that drives eluviation. Slow decomposition locks carbon in permafrost. Human haplogroups here evolved high h+d (mass anchor + GABA) for cold patience and low r+p (not impulsive).",
        "volcanic_soil": "Andosols form from volcanic ash weathering. Fresh minerals (P, Fe, Mg) are released slowly. The O₂/CO₂ stress pair (h,p) governs the oxidation of reduced volcanic gases. Human haplogroups here evolved high h (structural tradition) from the reliable agricultural base.",
        "temperate_soil": "Cambisols form in temperate climates with moderate weathering. Balanced nutrient cycling supports diverse ecosystems. The O₂/CO₂ stress pair (h,p) drives seasonal decomposition. Human haplogroups here show balanced 8D vectors with moderate values across all axes.",
        "peatland": "Histosols form in waterlogged, anaerobic conditions where organic matter accumulates faster than it decomposes. The heat/cold stress pair (nu,r) governs the freeze-thaw that limits decomposition. These are major methane reservoirs — the circuit's methanogenesis node.",
        "hydrothermal_sulfide": "Pyrite forms at hydrothermal vents where reduced sulfur meets iron. The matter/non-matter stress pair (s,g) governs the metal sulfide precipitation. These environments host chemosynthetic ecosystems independent of sunlight — the circuit's subduction_zone / light_dark inversion.",
        "orogenic_belt": "Fold belts form from continental collision. The heat/cold stress pair (nu,r) governs the metamorphic grade via geothermal gradient vs. uplift cooling. Mountain barriers isolate populations, creating genetic bottlenecks that amplify specific haplogroup frequencies.",
        "subduction": "Subduction zones recycle oceanic crust into the mantle. The light/dark stress pair (gamma,d) governs the surface (light) vs. deep (dark) material cycle. Arc volcanism above subduction zones creates volcanic soils that support dense populations.",
        "sedimentary_basin": "Sedimentary basins accumulate eroded material from surrounding highlands. The O₂/CO₂ stress pair (h,p) governs the organic carbon burial vs. oxidation. River-fed alluvial soils (fluvisols) sustain agriculture, supporting high population densities.",
        "rare_earth": "Monazite deposits concentrate rare earth elements through magmatic and sedimentary processes. The light/dark stress pair (gamma,d) governs the radioactive decay (light/energy emission) vs. stable lattice (dark/binding).",
        "mantle_plume": "Mantle plumes deliver deep heat to the surface, creating hotspots and large igneous provinces. The heat/cold stress pair (nu,r) is directly expressed as the plume's thermal anomaly vs. ambient mantle temperature.",
        "LIP": "Large igneous provinces form from massive flood basalt eruptions, often correlated with mass extinctions. The matter/non-matter stress pair (s,g) governs the mass eruption vs. atmospheric gas binding (CO₂/SO₂).",
        "deep_sea_nodule": "Manganese nodules grow at ~1mm per million years on the deep seafloor. The matter/non-matter stress pair (s,g) governs the slow metal accretion vs. seawater dissolution balance.",
        "orogenic_core": "Orogenic cores represent the deep root of mountain belts where crustal thickening creates granitic magmas. The matter/non-matter stress pair (s,g) governs the mass accumulation vs. partial melting.",
        "deep_earth": "Core-mantle boundary convection drives plate tectonics. The heat/cold stress pair (nu,r) is the fundamental engine — hot core vs. cold surface.",
        "deep_mantle": "LLSVPs are thermochemical piles at the base of the mantle. The matter/non-matter stress pair (s,g) governs the dense material accumulation vs. convective stirring.",
        "manganese_oxide": "Manganese oxide deposits form in arid environments through evaporation. The O₂/CO₂ stress pair (h,p) governs the redox cycling of Mn²⁺/Mn⁴⁺.",
        "iron_oxide": "Magnetite deposits form through magmatic and hydrothermal processes. The light/dark stress pair (gamma,d) governs the Fe²⁺/Fe³⁺ redox — magnetite contains both, making it a 'light/dark' mineral.",
        "radioactive": "Thorium deposits concentrate in monazite sands. The light/dark stress pair (gamma,d) governs the radioactive decay (gamma emission) vs. stable crystal lattice (dark binding).",
        "arc_magma": "Arc magmas form above subduction zones through flux melting. The heat/cold stress pair (nu,r) governs the thermal budget — cold subducting slab releases fluids that melt hot mantle wedge.",
        "metabolic_reference": "Succinate dehydrogenase is the metabolic hub connecting TCA cycle to ETC. Its geological projection represents the Mediterranean — the crossroads of three continents where metabolic diversity is maximal.",
        "iron_storage": "Ferritin is the iron storage protein. Its geological projection represents iron storage deposits — the link between biological iron metabolism and geological iron formations.",
    }

    explanation = geo_history.get(geo["geo_type"], 
        f"The geological process creates a specific substrate that selects for co-located subjects through the {geo_sp} stress pair.")
    lines.append(f"  {explanation}")
    lines.append("")

    # Why haplogroups are here
    if colocated["haplogroups"]:
        lines.append(f"  WHY THESE HAPLOGROUPS ARE HERE:")
        for hg in colocated["haplogroups"]:
            lines.append(f"    {hg['key']} ({hg['label']}):")
            lines.append(f"      Soil: {hg['soil']}")
            lines.append(f"      Dominant stress: {hg['dominant_stress']} (jetlag={hg['jetlag_hours']}h, resonance={hg['resonance']:.2f})")
            lines.append(f"      The soil type matches the geological substrate. The haplogroup's 8D vector")
            lines.append(f"      evolved to resonate with the stress pair that created this soil.")
            if hg["resonance"] > 0.8:
                lines.append(f"      → HIGH RESONANCE: haplogroup is in circadian sync with geological node.")
            elif hg["resonance"] > 0.5:
                lines.append(f"      → MODERATE RESONANCE: partial sync, oscillating energy exchange.")
            else:
                lines.append(f"      → LOW RESONANCE: anti-phase, stress-driven adaptation rather than harmony.")
        lines.append("")

    # Why biological subjects are here
    if colocated["biological_subjects"]:
        lines.append(f"  WHY THESE BIOLOGICAL SUBJECTS ARE HERE:")
        for bs in colocated["biological_subjects"]:
            lines.append(f"    {bs['name']} ({bs['type']}):")
            lines.append(f"      Element: {bs['element']}, Particle: {bs['particle']}")
            lines.append(f"      Stress: {bs['stress']} (jetlag={bs['jetlag_hours']}h, resonance={bs['resonance']:.2f})")
            lines.append(f"      Role: {bs['role']}")
        lines.append("")

    # Energy exchange dynamics
    lines.append(f"  ENERGY EXCHANGE DYNAMICS:")
    all_subjects_stress = [(s["name"] if "name" in s else s["key"], s.get("dominant_stress", s.get("stress", geo_sp)), s.get("resonance", 0))
                           for s in colocated["haplogroups"] + colocated["biological_subjects"]]
    for name, sp, res in all_subjects_stress:
        jl = jetlag_hours(sp, geo_sp)
        direction = "SYNC" if jl < 4 else ("PARTIAL" if jl < 8 else "ANTI-PHASE")
        lines.append(f"    {name:40s}  stress={sp:20s}  jetlag={jl:5.1f}h  resonance={res:.2f}  [{direction}]")
    lines.append("")

    return "\n".join(lines)


# ===========================================================================
# 6. COMPUTE ALL PROXIMAL AREAS
# ===========================================================================

def compute_all_proximal_areas() -> List[Dict]:
    """Compute co-location analysis for all geological nodes."""
    results = []
    for geo_name, geo in GEO_NODE_COORDS.items():
        colocated = find_colocated(geo_name, geo)
        explanation = explain_colocation(geo_name, colocated)
        colocated["explanation"] = explanation
        results.append(colocated)
    return results


# ===========================================================================
# 7. ENERGY EXCHANGE MATRIX
# ===========================================================================

def compute_energy_exchange(areas: List[Dict]) -> Dict:
    """Compute energy exchange matrix between all co-located subjects."""
    exchange = {
        "total_subjects": 0,
        "total_pairs": 0,
        "sync_pairs": 0,
        "antiphase_pairs": 0,
        "by_biome": {},
    }

    for area in areas:
        biome = area["biome"]
        if biome not in exchange["by_biome"]:
            exchange["by_biome"][biome] = {
                "subjects": 0,
                "sync": 0,
                "partial": 0,
                "antiphase": 0,
            }

        all_subs = area["haplogroups"] + area["biological_subjects"]
        exchange["total_subjects"] += len(all_subs)
        exchange["by_biome"][biome]["subjects"] += len(all_subs)

        # Count pairwise relationships
        for i in range(len(all_subs)):
            for j in range(i + 1, len(all_subs)):
                s1 = all_subs[i]
                s2 = all_subs[j]
                sp1 = s1.get("dominant_stress", s1.get("stress", area["stress_pair"]))
                sp2 = s2.get("dominant_stress", s2.get("stress", area["stress_pair"]))
                jl = jetlag_hours(sp1, sp2)
                exchange["total_pairs"] += 1
                if jl < 4:
                    exchange["sync_pairs"] += 1
                    exchange["by_biome"][biome]["sync"] += 1
                elif jl < 8:
                    exchange["by_biome"][biome]["partial"] += 1
                else:
                    exchange["antiphase_pairs"] += 1
                    exchange["by_biome"][biome]["antiphase"] += 1

    return exchange


# ===========================================================================
# 8. PLOT PROXIMAL RESONANCE MAP
# ===========================================================================

def plot_resonance_map(areas: List[Dict]):
    """Plot proximal areas with resonance intensity."""

    fig, axes = plt.subplots(2, 2, figsize=(24, 16), facecolor="#0a0a12")
    fig.suptitle(
        "Proximal Area Resonance — Why All Subjects Co-Locate\n"
        "Geological Node → Soil → Biome → Haplogroup → Biological Subjects",
        fontsize=16, color="white", fontweight="bold", y=0.98
    )

    bg = "#0a0a12"
    text_color = "#E0E0E0"
    grid_color = "#1a1a2e"

    # --- Panel 1: Subject count per geological node ---
    ax1 = axes[0, 0]
    ax1.set_facecolor(bg)
    geo_names = [a["geological_node"] for a in areas]
    haplo_counts = [len(a["haplogroups"]) for a in areas]
    bio_counts = [len(a["biological_subjects"]) for a in areas]
    x = np.arange(len(geo_names))
    ax1.barh(x - 0.2, haplo_counts, 0.4, color="#4ECDC4", label="Haplogroups", alpha=0.8)
    ax1.barh(x + 0.2, bio_counts, 0.4, color="#FF6B6B", label="Biological subjects", alpha=0.8)
    ax1.set_yticks(x)
    ax1.set_yticklabels(geo_names, fontsize=7, color=text_color)
    ax1.set_xlabel("Count", color=text_color)
    ax1.set_title("Co-located Subjects per Geological Node", color=text_color, fontweight="bold")
    ax1.legend(facecolor=bg, edgecolor=grid_color, labelcolor=text_color, fontsize=8)
    ax1.tick_params(colors=text_color)
    ax1.invert_yaxis()
    for spine in ax1.spines.values():
        spine.set_color(grid_color)

    # --- Panel 2: Resonance distribution by biome ---
    ax2 = axes[0, 1]
    ax2.set_facecolor(bg)
    biomes = sorted(set(a["biome"] for a in areas))
    biome_sync = []
    biome_partial = []
    biome_antiphase = []
    for b in biomes:
        sync = sum(1 for a in areas if a["biome"] == b for h in a["haplogroups"] + a["biological_subjects"]
                   if h.get("resonance", 0) > 0.7)
        partial = sum(1 for a in areas if a["biome"] == b for h in a["haplogroups"] + a["biological_subjects"]
                      if 0.3 < h.get("resonance", 0) <= 0.7)
        antiphase = sum(1 for a in areas if a["biome"] == b for h in a["haplogroups"] + a["biological_subjects"]
                        if h.get("resonance", 0) <= 0.3)
        biome_sync.append(sync)
        biome_partial.append(partial)
        biome_antiphase.append(antiphase)

    ax2.barh(np.arange(len(biomes)) - 0.25, biome_sync, 0.25, color="#4CAF50", label="Sync (>0.7)", alpha=0.8)
    ax2.barh(np.arange(len(biomes)), biome_partial, 0.25, color="#FFC107", label="Partial (0.3-0.7)", alpha=0.8)
    ax2.barh(np.arange(len(biomes)) + 0.25, biome_antiphase, 0.25, color="#F44336", label="Anti-phase (<0.3)", alpha=0.8)
    ax2.set_yticks(np.arange(len(biomes)))
    ax2.set_yticklabels(biomes, fontsize=9, color=text_color)
    ax2.set_xlabel("Subject Count", color=text_color)
    ax2.set_title("Resonance Distribution by Biome", color=text_color, fontweight="bold")
    ax2.legend(facecolor=bg, edgecolor=grid_color, labelcolor=text_color, fontsize=8)
    ax2.tick_params(colors=text_color)
    ax2.invert_yaxis()
    for spine in ax2.spines.values():
        spine.set_color(grid_color)

    # --- Panel 3: Jetlag heatmap (haplogroup × geological node) ---
    ax3 = axes[1, 0]
    ax3.set_facecolor(bg)
    # Build matrix: rows=haplogroups, cols=geological nodes
    hg_keys = sorted(Y_DNA_COORDS.keys())
    geo_names_sorted = sorted(GEO_NODE_COORDS.keys())
    matrix = np.full((len(hg_keys), len(geo_names_sorted)), 12.0)
    for i, hgk in enumerate(hg_keys):
        for j, gn in enumerate(geo_names_sorted):
            geo = GEO_NODE_COORDS[gn]
            geo_sp = geo["stress_pair"]
            if hgk in Y_DNA:
                v = Y_DNA[hgk]["v"]
                dim_pairs = {
                    "o2_co2": ("h", "p"), "heat_cold": ("nu", "r"),
                    "matter_nonmatter": ("s", "g"), "light_dark": ("gamma", "d"),
                }
                best_sp = geo_sp
                best_sum = 0
                for sp, (d1, d2) in dim_pairs.items():
                    s = v[d1] + v[d2]
                    if s > best_sum:
                        best_sum = s
                        best_sp = sp
                matrix[i, j] = jetlag_hours(best_sp, geo_sp)

    im = ax3.imshow(matrix, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=12)
    ax3.set_xticks(np.arange(len(geo_names_sorted)))
    ax3.set_xticklabels(geo_names_sorted, rotation=90, fontsize=6, color=text_color)
    ax3.set_yticks(np.arange(len(hg_keys)))
    ax3.set_yticklabels(hg_keys, fontsize=7, color=text_color)
    ax3.set_title("Jetlag (hours): Haplogroup × Geological Node\n(green=sync, red=anti-phase)", color=text_color, fontweight="bold")
    ax3.tick_params(colors=text_color)
    cbar = plt.colorbar(im, ax=ax3, fraction=0.02)
    cbar.set_label("Jetlag (hours)", color=text_color)
    cbar.ax.tick_params(colors=text_color)

    # --- Panel 4: Circadian energy exchange timeline ---
    ax4 = axes[1, 1]
    ax4.set_facecolor(bg)
    hours = np.arange(0, 24, 0.5)

    # For each stress pair, compute a circadian activation curve
    stress_colors = {
        "o2_co2": "#4CAF50", "heat_cold": "#FF9800",
        "matter_nonmatter": "#9C27B0", "light_dark": "#FFC107",
        "reset_spark": "#F44336",
    }
    stress_labels = {
        "o2_co2": "CO2/O2 (3-9h)", "heat_cold": "Heat/Cold (9-15h)",
        "matter_nonmatter": "Matter/Non-matter (15-21h)", "light_dark": "Light/Dark (0-3h)",
        "reset_spark": "Reset Spark (21-3h)",
    }

    for sp, (h_start, h_end) in CIRCADIAN_HOURS.items():
        # Gaussian-like activation centered on window
        center = (h_start + h_end) / 2.0
        width = (h_end - h_start) / 2.0
        activation = np.exp(-((hours - center) ** 2) / (2 * width ** 2))
        # Handle wrap-around for 21-3h
        if h_start > h_end:
            activation2 = np.exp(-((hours - (center + 24)) ** 2) / (2 * width ** 2))
            activation = np.maximum(activation, activation2)
            activation3 = np.exp(-((hours - (center - 24)) ** 2) / (2 * width ** 2))
            activation = np.maximum(activation, activation3)

        ax4.plot(hours, activation, color=stress_colors.get(sp, "#888"),
                 linewidth=2.5, label=stress_labels.get(sp, sp), alpha=0.85)
        ax4.fill_between(hours, 0, activation, alpha=0.08, color=stress_colors.get(sp, "#888"))

    ax4.set_xlabel("Hour (UTC)", color=text_color)
    ax4.set_ylabel("Activation", color=text_color)
    ax4.set_title("Circadian Stress Pair Activation — Jetlag Windows", color=text_color, fontweight="bold")
    ax4.legend(facecolor=bg, edgecolor=grid_color, labelcolor=text_color, fontsize=8, loc="upper right")
    ax4.tick_params(colors=text_color)
    ax4.set_xlim(0, 24)
    ax4.set_xticks(range(0, 25, 3))
    for spine in ax4.spines.values():
        spine.set_color(grid_color)
    ax4.grid(True, alpha=0.15, color=grid_color)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = GEN_DIR / "proximal_resonance_map.png"
    fig.savefig(out_path, dpi=150, facecolor=bg, bbox_inches="tight")
    plt.close(fig)
    print(f"-> {out_path}")


# ===========================================================================
# 9. GENERATE FULL REPORT
# ===========================================================================

def generate_report(areas: List[Dict], exchange: Dict) -> str:
    """Generate the full proximal resonance report."""
    lines: List[str] = []
    lines.append("=" * 100)
    lines.append("PROXIMAL AREA RESONANCE — WHY ALL SUBJECTS CO-LOCATE AND EXCHANGE ENERGY")
    lines.append("=" * 100)
    lines.append("")
    lines.append("CORE THESIS:")
    lines.append("-" * 100)
    lines.append("The circuit's 4 stress pairs drive geological processes that create specific soil types.")
    lines.append("Those soils support specific biomes and food chains.")
    lines.append("Human haplogroups adapted to those biomes over 50,000+ years.")
    lines.append("Non-human organisms co-evolved with the same geological substrate.")
    lines.append("The 8D vector of each subject resonates with the underlying geological node's stress pair.")
    lines.append("Temporal jetlag (circadian phase offset) creates resonance windows where co-located")
    lines.append("subjects exchange energy — sync (high resonance) or anti-phase (stress-driven adaptation).")
    lines.append("")
    lines.append("STRESS PAIR → GEOLOGICAL PROCESS → SOIL → BIOME → HAPLOGROUP → CO-LOCATION")
    lines.append("")

    # Stress pair summary
    lines.append("■ 4 STRESS PAIRS → GEOLOGICAL DRIVERS")
    lines.append("-" * 100)
    sp_drivers = {
        "o2_co2": "Oxidation/reduction — drives iron precipitation, organic carbon burial, redox cycling",
        "heat_cold": "Thermal gradient — drives freeze-thaw, metamorphic grade, mantle convection",
        "matter_nonmatter": "Mass/binding balance — drives craton stability, metal accretion, LIP eruption",
        "light_dark": "Surface/depth cycle — drives subduction recycling, radioactive decay, UV adaptation",
    }
    for sp, desc in sp_drivers.items():
        dims = STRESS_PAIRS.get(sp, {}).get("dims", ())
        hours = CIRCADIAN_HOURS.get(sp, (0, 0))
        lines.append(f"  {sp:20s}  dims={dims}  hours={hours}  → {desc}")
    lines.append("")

    # Energy exchange summary
    lines.append("■ ENERGY EXCHANGE SUMMARY")
    lines.append("-" * 100)
    lines.append(f"  Total co-located subjects:   {exchange['total_subjects']}")
    lines.append(f"  Total subject pairs:         {exchange['total_pairs']}")
    lines.append(f"  Sync pairs (jetlag < 4h):    {exchange['sync_pairs']}")
    lines.append(f"  Anti-phase pairs (jetlag > 8h): {exchange['antiphase_pairs']}")
    lines.append(f"  Partial pairs:               {exchange['total_pairs'] - exchange['sync_pairs'] - exchange['antiphase_pairs']}")
    lines.append("")

    # By biome
    lines.append("■ RESONANCE BY BIOME")
    lines.append("-" * 100)
    for biome, stats in sorted(exchange["by_biome"].items(), key=lambda x: -x[1]["subjects"]):
        lines.append(f"  {biome:15s}  subjects={stats['subjects']:3d}  "
                     f"sync={stats['sync']:3d}  partial={stats['partial']:3d}  antiphase={stats['antiphase']:3d}")
    lines.append("")

    # Per-area detail
    lines.append("■ PROXIMAL AREA DETAILS (ALL 25 GEOLOGICAL NODES)")
    lines.append("-" * 100)

    for area in areas:
        lines.append("")
        lines.append("=" * 80)
        lines.append(f"  GEOLOGICAL NODE: {area['geological_node']}")
        lines.append(f"  Type: {area['geo_type']}  |  Biome: {area['biome']}  |  Stress: {area['stress_pair']}")
        lines.append(f"  Location: ({area['lat']:.2f}, {area['lon']:.2f})  |  {area['geo_label']}")
        lines.append("=" * 80)
        lines.append("")

        # Co-located subjects
        lines.append(f"  CO-LOCATED SUBJECTS:")
        lines.append(f"    Haplogroups:          {len(area['haplogroups'])}")
        lines.append(f"    mtDNA:                {len(area['mtdna'])}")
        lines.append(f"    Ethnic archetypes:    {len(area['ethnic_archetypes'])}")
        lines.append(f"    Biological subjects:  {len(area['biological_subjects'])}")
        lines.append(f"    Cosmic spheres:       {len(area['spheres'])}")
        lines.append(f"    Attractors:           {len(area['attractors'])}")
        lines.append("")

        if area["haplogroups"]:
            lines.append(f"  HAPLOGROUPS IN THIS AREA:")
            for hg in area["haplogroups"]:
                lines.append(f"    {hg['key']:10s}  {hg['label']}")
                lines.append(f"      soil: {hg['soil'][:60]}")
                lines.append(f"      blood: {hg['blood']}  rh: {hg['rh']}")
                lines.append(f"      dominant stress: {hg['dominant_stress']}  "
                           f"jetlag: {hg['jetlag_hours']}h  resonance: {hg['resonance']:.2f}")
                lines.append(f"      8D: r={hg['vector8']['r']:.2f} h={hg['vector8']['h']:.2f} "
                           f"d={hg['vector8']['d']:.2f} p={hg['vector8']['p']:.2f} "
                           f"s={hg['vector8']['s']:.2f} g={hg['vector8']['gamma']:.2f} "
                           f"g={hg['vector8']['g']:.2f} n={hg['vector8']['nu']:.2f}")
            lines.append("")

        if area["biological_subjects"]:
            lines.append(f"  BIOLOGICAL SUBJECTS IN THIS BIOME ({area['biome']}):")
            for bs in area["biological_subjects"]:
                lines.append(f"    {bs['name']}")
                lines.append(f"      type: {bs['type']}  element: {bs['element']}  particle: {bs['particle']}")
                lines.append(f"      stress: {bs['stress']}  jetlag: {bs['jetlag_hours']}h  resonance: {bs['resonance']:.2f}")
                lines.append(f"      role: {bs['role']}")
            lines.append("")

        if area["spheres"]:
            lines.append(f"  COSMIC SPHERE INFLUENCE:")
            for sp in area["spheres"]:
                lines.append(f"    {sp['name']:10s}  {sp['label']}  "
                           f"attractor={sp['attractor']}  dist={sp['distance_km']:.0f}km")
            lines.append("")

        # Historical explanation
        lines.append(area["explanation"])

    # Final synthesis
    lines.append("")
    lines.append("=" * 100)
    lines.append("SYNTHESIS: THE UNIVERSAL CO-LOCATION PRINCIPLE")
    lines.append("=" * 100)
    lines.append("")
    lines.append("1. GEOLOGICAL SUBSTRATE IS THE ANCHOR")
    lines.append("   Each geological node creates a specific soil through its stress pair process.")
    lines.append("   The soil's mineral composition, pH, water retention, and nutrient profile")
    lines.append("   are determined by the geological process (e.g., glaciation → podzol,")
    lines.append("   tropical weathering → ferralsol, volcanic ash → andosol).")
    lines.append("")
    lines.append("2. SOIL SELECTS BIOME")
    lines.append("   The soil type determines which plant communities can thrive.")
    lines.append("   Plants determine herbivore communities, which determine predators.")
    lines.append("   The entire food chain is anchored to the geological substrate.")
    lines.append("")
    lines.append("3. BIOME SELECTS HAPLOGROUP")
    lines.append("   Human populations adapted to each biome over 50,000+ years.")
    lines.append("   Diet (plant/animal availability), climate (cold/heat), altitude (O2),")
    lines.append("   and pathogen load (tropical vs. arctic) selected for specific")
    lines.append("   neurochemical receptor polymorphisms (D2, COMT, MAO-A, 5-HT).")
    lines.append("   These polymorphisms determine the 8D vector, which resonates")
    lines.append("   with the geological node's stress pair.")
    lines.append("")
    lines.append("4. 8D VECTOR RESONANCE IS THE BINDING MECHANISM")
    lines.append("   The haplogroup's 8D vector and the geological node's stress pair")
    lines.append("   share the same dimensional axes. When the haplogroup's dominant")
    lines.append("   stress pair matches the geological node's stress pair, they are")
    lines.append("   in circadian sync (jetlag ≈ 0h, resonance ≈ 1.0).")
    lines.append("   This creates maximum energy exchange — the haplogroup 'fits' the land.")
    lines.append("")
    lines.append("5. JETLAG CREATES TEMPORAL WINDOWS")
    lines.append("   Each stress pair activates during a specific circadian window:")
    lines.append("     light_dark:   0-3h   (AB spark — deep night)")
    lines.append("     o2_co2:       3-9h   (A accumulate — dawn to noon)")
    lines.append("     heat_cold:    9-15h  (O accumulate — noon to afternoon)")
    lines.append("     matter_non:   15-21h (B accumulate — afternoon to night)")
    lines.append("     reset_spark:  21-3h  (AB integration — night to dawn)")
    lines.append("   When two subjects share the same stress pair, their activation")
    lines.append("   windows overlap → continuous energy exchange (SYNC).")
    lines.append("   When stress pairs differ by 6h, they alternate → oscillating")
    lines.append("   exchange (PARTIAL). When they differ by 12h, they are anti-phase")
    lines.append("   → stress-driven adaptation rather than harmony (ANTI-PHASE).")
    lines.append("")
    lines.append("6. NON-HUMAN ORGANISMS ARE CO-RESONATORS")
    lines.append("   Each biome's fauna, flora, and microbiome carry 8D vectors")
    lines.append("   that match the geological stress pair. They are not passive")
    lines.append("   inhabitants — they actively modulate the soil chemistry,")
    lines.append("   nutrient cycling, and atmospheric gas composition, creating")
    lines.append("   feedback loops that reinforce the geological process.")
    lines.append("   Example: termite mounds in tropical laterites accelerate")
    lines.append("   iron oxide formation → reinforces ferralsol → selects for")
    lines.append("   E1b1a haplogroup (high r, iron-locked P+).")
    lines.append("")
    lines.append("7. THE CIRCUIT IS THE META-STRUCTURE")
    lines.append("   The neuro-bio-geochemical circuit is not just a metaphor —")
    lines.append("   it is the meta-structure that governs which subjects co-locate.")
    lines.append("   Each circuit node (e.g., steel, clay_gouge, craton) maps to")
    lines.append("   a geological process, which creates a soil, which selects a biome,")
    lines.append("   which selects a haplogroup, which carries an 8D vector that")
    lines.append("   resonates with the circuit node's stress pair.")
    lines.append("   The circuit is the cause; geography is the effect.")
    lines.append("")

    text = "\n".join(lines)
    (GEN_DIR / "proximal_resonance_report.txt").write_text(text, encoding="utf-8")
    print(text[:5000])
    print(f"\n... full report -> {GEN_DIR / 'proximal_resonance_report.txt'}")
    return text


# ===========================================================================
# MAIN
# ===========================================================================

if __name__ == "__main__":
    print("Computing proximal area resonance for all geological nodes...")
    areas = compute_all_proximal_areas()
    exchange = compute_energy_exchange(areas)

    # Export JSON
    export_data = {
        "total_areas": len(areas),
        "energy_exchange": exchange,
        "areas": [],
    }
    for area in areas:
        a_export = {k: v for k, v in area.items() if k != "explanation"}
        a_export["explanation"] = area["explanation"]
        export_data["areas"].append(a_export)

    (GEN_DIR / "proximal_resonance.json").write_text(
        json.dumps(export_data, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    print(f"-> {GEN_DIR / 'proximal_resonance.json'}")

    plot_resonance_map(areas)
    generate_report(areas, exchange)
