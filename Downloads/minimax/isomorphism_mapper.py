"""
isomorphism_mapper.py — 84 circuit nodes ↔ (geology, biochemistry, cosmic) automatic isomorphism

Strategy: encode each node in 9 vector attributes, then cosine-similarity-match
to candidate geology, biochemistry, cosmic structures.

Date: 2026-09-09
"""

from __future__ import annotations
import json
import math
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ============================================================
# 9-VECTOR ATTRIBUTE SPACE
# ============================================================
# Each attribute ∈ [0, 1]
# 0: dim:          0=scalar, 1=tensor(rank≥2)
# 1: direction:    0=unidirectional, 1=oscillatory/rotational
# 2: scale_log:    log10(scale in meters) normalized to [-2, +26] → [0,1]
# 3: phase:        0=static, 1=phase-transitioning
# 4: coupling:     0=weak (gravity), 1=strong (QCD)
# 5: symmetry:     0=fully broken, 1=fully conserved
# 6: time_response: 0=instant, 1=exponential decay / periodic
# 7: boundary:     0=open, 1=closed/periodic
# 8: energy_flow:  0=sink, 0.5=passthrough, 1=source/amplifier

ATTR_NAMES = ["dim", "direction", "scale_log", "phase", "coupling",
              "symmetry", "time_response", "boundary", "energy_flow"]

# ============================================================
# CIRCUIT NODES (84) — extracted from CIRCUITFILE.MD
# Each row: name, body_site, particle, dim, geol_struct, attr_vector
# ============================================================

# Body site → scale encoding
def scale_encode(scale_m: float) -> float:
    """log10(scale in meters) → [0,1] over [-12, 26]"""
    if scale_m <= 0:
        return 0.0
    log = math.log10(scale_m)
    return max(0.0, min(1.0, (log + 12.0) / 38.0))

# Particle → coupling strength (Standard Model analogy)
PARTICLE_COUPLING = {
    "proton": 0.85, "gluon": 0.95, "quark": 0.95, "photon": 0.5, "electron": 0.4,
    "neutrino": 0.05, "muon": 0.3, "tau": 0.3, "w_boson": 0.6, "z_boson": 0.6,
    "higgs": 0.7, "axion": 0.05, "graviton": 0.01, "dark_matter": 0.1, "dark_energy": 0.02,
    "neutron": 0.85, "neutron_star": 0.95, "ferritin": 0.5, "heme": 0.6,
    "up_quark": 0.95, "down_quark": 0.95, "charm_quark": 0.95, "strange_quark": 0.95,
    "top_quark": 0.95, "bottom_quark": 0.95, "tau_neutrino": 0.05,
    "electron_neutrino": 0.05, "muon_neutrino": 0.05, "tau_antineutrino": 0.05,
    "electron_antineutrino": 0.05, "muon_antineutrino": 0.05,
    "energy": 0.5, "clathrate_buffer": 0.3, "malate_dehydrogenase": 0.4,
    "ego_d2": 0.4, "progesterone": 0.2, "testosterone": 0.2, "acetyl_coa": 0.4,
    "female_gaba": 0.4, "em": 0.5, "co2": 0.4, "cytochrome_c_oxidase": 0.6,
    "observer_left_endorphin_electron_antineutrino": 0.3, "observer_leftd2": 0.4,
    "right_sole_dopamine": 0.4, "right_acetylcholine": 0.4, "left_endorphin_non_observer": 0.3,
    "nonobserver_left_d2": 0.4, "left_genital_d2": 0.4, "carbon": 0.5,
    "mc1r": 0.4, "methanogenesis": 0.3, "memory_entropy": 0.5, "hind_insula": 0.4,
    "substance_p": 0.4, "methionine": 0.4, "adapter_protein": 0.4, "succinate_dehydrogenase": 0.5,
    "collagen": 0.4, "andosol": 0.5, "cambisol": 0.4, "podzol": 0.4, "histosol": 0.4,
    "laterite": 0.5, "plume": 0.5, "outer_core_convection": 0.6, "fold_belt": 0.5,
    "basin": 0.4, "lower_mantle": 0.7, "quark_orogen_magma": 0.95, "caco3": 0.4,
    "peonidine": 0.3, "co2_node": 0.4, "glp1": 0.4, "manganese_nodule": 0.4,
    "pentose_phosphate": 0.4, "disulfide_bond": 0.4, "nitrogenase": 0.5, "water": 0.4,
    "large_igneous_province": 0.6, "subduction_zone": 0.7, "craton": 0.5, "actinide": 0.5,
    "iron": 0.6, "thorium": 0.5, "uranium": 0.5, "monazite": 0.4, "sulfur": 0.5,
    "pi_electron_cloud": 0.5, "chloride": 0.3, "sodium": 0.4, "calcium": 0.4,
    "potassium": 0.4, "magnesium": 0.4, "zinc": 0.4, "copper": 0.4,
    "lactate_dehydrogenase": 0.4, "pyrite": 0.5, "strontium": 0.4, "barium": 0.4,
    "sulforaphane": 0.3, "cysteine": 0.4, "glymphatic_system": 0.3, "aurora": 0.4,
    "heath_aerenchyma": 0.3, "mangrove_aerenchyma": 0.3, "autophagy": 0.4,
    "chlorine_ion_pump": 0.3, "t_FF": 0.4, "carbonic_anhydrase": 0.4, "mycorradicin": 0.3,
    "copper_iron_complex": 0.5, "NaCl": 0.4, "actinide_isomorph": 0.5,
    "NaCl_in0_xor": 0.4, "NaCl_in1_xor": 0.4, "sodium_in0_xor": 0.4, "sodium_in1_xor": 0.4,
}

# Dim → direction encoding
DIM_DIRECTION = {
    "r": 0.85,      # rhythm = oscillatory
    "h": 0.3,       # harmony = static blend
    "d": 0.7,       # dissonance = oscillating tension
    "p": 0.2,       # predictability = static pattern
    "s": 0.3,       # brightness = scalar amplitude
    "gamma": 0.6,   # spatial spread = directional
    "g": 0.5,       # binding = static
    "nu": 0.9,      # fractal recursion = self-similar oscillation
    "g/nu": 0.7, "h/g": 0.4, "h/nu": 0.65, "r/d": 0.78, "r/s": 0.58,
    "r/h": 0.58, "r/gamma": 0.7, "r/p": 0.53, "h/gamma": 0.45, "h/d": 0.5,
    "d/p": 0.45, "d/s": 0.5, "p/s": 0.25, "p/nu": 0.55, "s/gamma": 0.45,
    "s/d": 0.5, "s/nu": 0.6, "d/nu": 0.8, "gamma/g": 0.55, "gamma/nu": 0.75,
    "gamma/d": 0.65, "g/d": 0.5, "d/r": 0.78, "d/h": 0.5, "p/d": 0.45,
    "nu/gamma": 0.75,
}

# ============================================================
# 84 CIRCUIT NODES (extracted from CIRCUITFILE.MD)
# ============================================================
CIRCUIT_84 = [
    # Body master + 7 system
    {"id": 1,  "name": "observer_leftd2",            "particle": "observer_leftd2",  "body": "outer left frontalis",                "geol": "regional crustal tension permit (master bus)", "dim": "p",    "scale_m": 1e-3},
    {"id": 2,  "name": "nonobserver_left_d2",        "particle": "nonobserver_left_d2","body": "left frontalis outer strip lower",    "geol": "crustal transparency / seismic window",       "dim": "p",    "scale_m": 1e-3},
    {"id": 3,  "name": "electric_grid_and",          "particle": "strange_quark",     "body": "left forehead inner strip top",        "geol": "global galvanotactic grid (tectonic)",          "dim": "r",    "scale_m": 1e-2},
    {"id": 4,  "name": "opioid_and",                 "particle": "electron_antineutrino", "body": "left of philtrum",                  "geol": "eclogite-facies sync (deep crust)",             "dim": "h",    "scale_m": 1e-2},
    {"id": 5,  "name": "opioid_nor",                 "particle": "electron_antineutrino", "body": "left of philtrum (vacuum)",         "geol": "deep-mantle vacuum void (subduction)",           "dim": "d",    "scale_m": 1e-2},
    {"id": 6,  "name": "opioid_xnor_or",             "particle": "electron_antineutrino", "body": "left of philtrum (phase)",          "geol": "supercontinent cycle stability (tectonic)",     "dim": "p",    "scale_m": 1e-2},
    {"id": 7,  "name": "bioenergetic_drive_and",      "particle": "w_boson",            "body": "mitochondrial",                       "geol": "geothermal convective drive (mantle)",           "dim": "r",    "scale_m": 1e-5},
    {"id": 8,  "name": "heme",                       "particle": "right_testosterone", "body": "inner to left nipple",                "geol": "iron-rich BIF (banded iron formation)",         "dim": "s",    "scale_m": 1e-9},
    {"id": 9,  "name": "cytochrome_c_oxidase",       "particle": "down_quark",         "body": "inner surface of intestine (left)",   "geol": "deep-sea terminal hydrothermal vent (COX)",     "dim": "r",    "scale_m": 1e-8},
    {"id": 10, "name": "water_vapour",               "particle": "photon",             "body": "thoracic spinous processes",          "geol": "global hydrological cycle (troposphere/strat)","dim": "g",    "scale_m": 1e-3},
    {"id": 11, "name": "steel",                      "particle": "muon_neutrino",      "body": "left anus muscle / rectum",           "geol": "iron-carbon martensitic/austenitic (BCC/FCC)",   "dim": "s",    "scale_m": 1e-3},
    {"id": 12, "name": "clay_gouge",                 "particle": "electron_neutrino",  "body": "right anus muscle / rectum",          "geol": "fault-zone phyllosilicate matrix (clay)",       "dim": "g",    "scale_m": 1e-3},
    {"id": 13, "name": "quark_orogen_magma",         "particle": "neutron_star",       "body": "right inner bum",                     "geol": "subduction slab dehydration melting (deep)",     "dim": "nu",   "scale_m": 1e-3},
    {"id": 14, "name": "observer_left_endorphin",    "particle": "electron_antineutrino","body": "left of philtrum",                  "geol": "mu-opioid receptor MOR",                          "dim": "h",    "scale_m": 1e-9},
    {"id": 15, "name": "left_endorphin_non_observer","particle": "electron_neutrino",  "body": "LEFT LEVATOR SUPERIORIS inner edge",  "geol": "MOR presynaptic switch (Day spark)",             "dim": "h",    "scale_m": 1e-9},
    {"id": 16, "name": "mc1r",                       "particle": "higgs",              "body": "skin / D-FF",                         "geol": "MC1R melanocortin receptor",                     "dim": "p",    "scale_m": 1e-9},
    {"id": 17, "name": "methanogenesis",             "particle": "higgs",              "body": "gut archaeal",                       "geol": "anaerobic CH4 production (early Earth)",         "dim": "p",    "scale_m": 1e-6},
    {"id": 18, "name": "histosol",                   "particle": "muon_antineutrino",  "body": "sulfur cycle node",                   "geol": "peat / sulfur cycle soil (Histosol)",            "dim": "h",    "scale_m": 1e-3},
    {"id": 19, "name": "sulforaphane",               "particle": "gluon",              "body": "Nrf2 activator",                     "geol": "Nrf2 antioxidant response (broccoli)",           "dim": "g",    "scale_m": 1e-8},
    {"id": 20, "name": "aurora",                     "particle": "muon",               "body": "Na+ threshold detector",              "geol": "Na+ oxidation threshold",                        "dim": "s",    "scale_m": 1e-8},
    {"id": 21, "name": "glymphatic_system",          "particle": "strange_quark",      "body": "AQP4 CSF-ISF exchange",               "geol": "AQP4 perivascular pump",                         "dim": "g",    "scale_m": 1e-8},
    {"id": 22, "name": "cysteine",                   "particle": "energy",             "body": "GSH precursor gate",                  "geol": "cysteine → glutathione pathway",                 "dim": "s",    "scale_m": 1e-9},
    {"id": 23, "name": "memory_entropy",             "particle": "electron",           "body": "right hippocampal CA1",              "geol": "novelty-mismatch detection",                     "dim": "r",    "scale_m": 1e-5},
    {"id": 24, "name": "hind_insula",                "particle": "neutron",            "body": "right posterior insula",              "geol": "neutron / neutral observation",                  "dim": "d",    "scale_m": 1e-2},
    {"id": 25, "name": "carbon",                     "particle": "photon",             "body": "metabolic carbon latch",              "geol": "carbon cycle / D-FF",                            "dim": "p",    "scale_m": 1e-6},
    {"id": 26, "name": "fold_belt",                  "particle": "muon",               "body": "fold-thrust belt",                    "geol": "Andesite ridge, fold-thrust belt (compression)", "dim": "r",    "scale_m": 1e3},
    {"id": 27, "name": "substance_p",                "particle": "tau_antineutrino",   "body": "NK1R Substance P",                    "geol": "pain/inflammation signaling",                    "dim": "d",    "scale_m": 1e-9},
    {"id": 28, "name": "methionine",                 "particle": "z_boson",            "body": "sulfur amino acid gate",              "geol": "methionine / S-AdoMet cycle",                    "dim": "p",    "scale_m": 1e-9},
    {"id": 29, "name": "adapter_protein",            "particle": "tau_neutrino",       "body": "somatic signal adapter",              "geol": "adapter protein / D-FF",                          "dim": "h",    "scale_m": 1e-8},
    {"id": 30, "name": "succinate_dehydrogenase",    "particle": "muon_neutrino",      "body": "Complex II / SDH",                    "geol": "TCA cycle Complex II",                           "dim": "r",    "scale_m": 1e-8},
    {"id": 31, "name": "collagen",                   "particle": "tau_neutrino",       "body": "ECM triple-helix",                    "geol": "collagen / ECM structural protein",              "dim": "h",    "scale_m": 1e-7},
    {"id": 32, "name": "andosol",                    "particle": "neutron",            "body": "left sole",                           "geol": "volcanic ash soil (Andosol)",                    "dim": "g",    "scale_m": 1e-3},
    {"id": 33, "name": "cambisol",                   "particle": "energy",             "body": "bilateral Achilles tendons",          "geol": "young weathered soil (Cambisol)",                "dim": "h",    "scale_m": 1e-3},
    {"id": 34, "name": "podzol",                     "particle": "strange_quark",      "body": "lower extremities podzol",            "geol": "acidic leaching soil (Podzol)",                  "dim": "h",    "scale_m": 1e-3},
    {"id": 35, "name": "NaCl",                       "particle": "proton",             "body": "halite evaporite",                    "geol": "NaCl evaporite / ionic halite",                  "dim": "r",    "scale_m": 1e-3},
    {"id": 36, "name": "sodium",                     "particle": "w_boson",            "body": "left lateral orbicularis oris",      "geol": "sodium pump / Na+/K+ ATPase",                    "dim": "r",    "scale_m": 1e-8},
    {"id": 37, "name": "mycorradicin",               "particle": "electron_antineutrino","body": "AM symbiosis",                        "geol": "AM fungal apocarotenoid signal",                 "dim": "nu",   "scale_m": 1e-8},
    {"id": 38, "name": "copper_iron_complex",        "particle": "z_boson",            "body": "right 5th metatarsal base",           "geol": "Cu-Fe mixed-valence redox",                      "dim": "h",    "scale_m": 1e-9},
    {"id": 39, "name": "autophagy",                  "particle": "charm_quark",        "body": "subduction-related recycling",        "geol": "catabolic clearing / lithospheric recycling",   "dim": "d",    "scale_m": 1e-6},
    {"id": 40, "name": "chlorine_ion_pump",          "particle": "electron",           "body": "right ventral wrist",                "geol": "Cl- ATPase acid-rhizosphere flux",               "dim": "d",    "scale_m": 1e-8},
    {"id": 41, "name": "heath_aerenchyma",           "particle": "tau_antineutrino",   "body": "Erica aerenchyma",                    "geol": "bog/wetland aerenchyma O2",                      "dim": "d",    "scale_m": 1e-4},
    {"id": 42, "name": "podzol_out0_nand",           "particle": "strange_quark",      "body": "podzol output",                       "geol": "lysosomal acidification",                        "dim": "h",    "scale_m": 1e-8},
    {"id": 43, "name": "water",                      "particle": "right_testosterone", "body": "upper philtrum",                      "geol": "hydrological cycle / H+ source",                 "dim": "g",    "scale_m": 1e-3},
    {"id": 44, "name": "nitrogenase",                "particle": "higgs",              "body": "biological N2-fixation",              "geol": "Mo-Fe nitrogenase cofactor",                     "dim": "p",    "scale_m": 1e-8},
    {"id": 45, "name": "caco3",                      "particle": "up_quark",           "body": "carbonate buffer",                    "geol": "CaCO3 sedimentary carbonate",                    "dim": "r",    "scale_m": 1e-5},
    {"id": 46, "name": "peonidine",                  "particle": "energy",             "body": "anthocyanin cycle",                   "geol": "anthocyanin / estrogen conjugate",               "dim": "h",    "scale_m": 1e-9},
    {"id": 47, "name": "right_acetylcholine",        "particle": "tau_neutrino",       "body": "alpha7 nAChR (vagal)",                "geol": "cholinergic anti-inflammatory",                  "dim": "r",    "scale_m": 1e-9},
    {"id": 48, "name": "co2",                        "particle": "dark_energy",        "body": "CO2/Adenosine time-energy",           "geol": "atmospheric CO2 / volcanic degassing",           "dim": "p",    "scale_m": 1e-3},
    {"id": 49, "name": "glp1",                       "particle": "gluon",              "body": "GLP-1 incretin vagal latch",          "geol": "incretin postprandial satiety",                  "dim": "s",    "scale_m": 1e-9},
    {"id": 50, "name": "laterite",                   "particle": "left_progesterone",  "body": "tropical weathering latch (TimeLatch)","geol": "laterite / tropical weathering (TimeLatch)",     "dim": "s",    "scale_m": 1e-3},
    {"id": 51, "name": "manganese_nodule",           "particle": "muon_antineutrino",  "body": "deep-sea Mn nodule",                  "geol": "deep-sea Mn nodule (abyssal plain)",              "dim": "p",    "scale_m": 1e-2},
    {"id": 52, "name": "pentose_phosphate",          "particle": "down_quark",         "body": "PPP redox gate",                      "geol": "pentose phosphate pathway (PPP)",                 "dim": "p",    "scale_m": 1e-8},
    {"id": 53, "name": "disulfide_bond",             "particle": "z_boson",            "body": "disulfide bond",                      "geol": "disulfide bond / S-S",                           "dim": "p",    "scale_m": 1e-9},
    {"id": 54, "name": "large_igneous_province",     "particle": "tau",                "body": "LIP eruption",                        "geol": "large igneous province (flood basalt)",          "dim": "d",    "scale_m": 1e5},
    {"id": 55, "name": "subduction_zone",            "particle": "tau",                "body": "subduction slab",                     "geol": "subduction zone (slab rollback)",                "dim": "p",    "scale_m": 1e5},
    {"id": 56, "name": "craton",                     "particle": "strange_quark",      "body": "stable continental nucleus",          "geol": "craton (Archean core)",                           "dim": "p",    "scale_m": 1e5},
    {"id": 57, "name": "basin",                      "particle": "left_progesterone",  "body": "sedimentary basin",                   "geol": "foreland basin / back-arc basin",                "dim": "g",    "scale_m": 1e4},
    {"id": 58, "name": "lower_mantle",               "particle": "muon",               "body": "lower mantle bridgmanite",            "geol": "lower mantle (post-perovskite)",                  "dim": "nu",   "scale_m": 1e6},
    {"id": 59, "name": "outer_core_convection",      "particle": "dark_matter",        "body": "outer core Fe MHD",                   "geol": "outer core Fe convection (geodynamo)",           "dim": "d",    "scale_m": 1e6},
    {"id": 60, "name": "thorium",                    "particle": "strange_quark",      "body": "REE thorium node",                    "geol": "thorium / REE catalyst (monazite)",              "dim": "d",    "scale_m": 1e-9},
    {"id": 61, "name": "monazite",                   "particle": "tau_neutrino",       "body": "REE phosphate",                       "geol": "monazite (Ce,La,Th,Nd) PO4",                      "dim": "h",    "scale_m": 1e-6},
    {"id": 62, "name": "manganese_oxygen_complex",   "particle": "gluon",              "body": "OEC manganese cluster",               "geol": "Mn4CaO5 cluster (oxygen evolving complex)",      "dim": "g",    "scale_m": 1e-9},
    {"id": 63, "name": "oxidised_manganese",         "particle": "higgs",              "body": "Mn oxide",                            "geol": "Mn-oxide / birnessite",                           "dim": "g",    "scale_m": 1e-8},
    {"id": 64, "name": "sulfur_iron_complex",        "particle": "higgs",              "body": "Fe-S cluster",                        "geol": "Fe-S cluster (nitrogenase cofactor)",            "dim": "g",    "scale_m": 1e-9},
    {"id": 65, "name": "pyrite",                     "particle": "higgs",              "body": "FeS2 mineral",                        "geol": "pyrite FeS2 (fool's gold)",                       "dim": "g",    "scale_m": 1e-4},
    {"id": 66, "name": "left_genital_d2",            "particle": "w_boson",            "body": "MPOA D2 brake",                       "geol": "MPOA climax brake (D3-like)",                     "dim": "d",    "scale_m": 1e-3},
    {"id": 67, "name": "left_female_vasopressin",    "particle": "tau_antineutrino",   "body": "V1B vasopressin HPA",                 "geol": "V1B receptor / HPA stress",                      "dim": "d",    "scale_m": 1e-9},
    {"id": 68, "name": "male_gaba_a",                "particle": "tau",                "body": "GABA-A male tonic",                   "geol": "GABA-A tonic inhibition (mass lock)",            "dim": "d",    "scale_m": 1e-8},
    {"id": 69, "name": "female_gaba_a",              "particle": "gluon",              "body": "GABA-A female phasic",                "geol": "GABA-A phasic inhibition (cold sense)",          "dim": "r",    "scale_m": 1e-8},
    {"id": 70, "name": "female_gaba_b",              "particle": "tau_neutrino",       "body": "GABA-B female postsynaptic",          "geol": "GABA-B slow IPSP / GIRK",                         "dim": "h",    "scale_m": 1e-8},
    {"id": 71, "name": "male_gaba_b",                "particle": "tau",                "body": "GABA-B male presynaptic",             "geol": "GABA-B presynaptic autoreceptor",                 "dim": "d",    "scale_m": 1e-8},
    {"id": 72, "name": "right_sole_dopamine",        "particle": "photon",             "body": "D1/D5 right sole",                    "geol": "dopamine D1/D5 (Gs-coupled)",                    "dim": "s",    "scale_m": 1e-9},
    {"id": 73, "name": "pi_electron_cloud",          "particle": "photon",             "body": "delocalized e-",                      "geol": "delocalized π-electron cloud",                   "dim": "g",    "scale_m": 1e-9},
    {"id": 74, "name": "citric_acid_cycle",          "particle": "photon",             "body": "TCA cycle",                           "geol": "TCA / Krebs cycle",                               "dim": "r",    "scale_m": 1e-8},
    {"id": 75, "name": "actinide_latch",             "particle": "tau_antineutrino",   "body": "actinide D-latch",                    "geol": "actinide series (U, Th, Pa)",                     "dim": "d",    "scale_m": 1e-9},
    {"id": 76, "name": "actinide",                   "particle": "tau_antineutrino",   "body": "actinide analogue",                   "geol": "actinide / REE",                                  "dim": "d",    "scale_m": 1e-9},
    {"id": 77, "name": "thorium_node",               "particle": "higgs",              "body": "thorium node",                        "geol": "thorium decay chain (catalyst)",                  "dim": "d",    "scale_m": 1e-9},
    {"id": 78, "name": "actinide_node",              "particle": "tau_antineutrino",   "body": "actinide node",                       "geol": "actinide complex (U, Th, Np, Pu)",               "dim": "d",    "scale_m": 1e-9},
    {"id": 79, "name": "lactate_dehydrogenase",      "particle": "electron",           "body": "LDH enzyme",                          "geol": "lactate dehydrogenase (glycolysis)",             "dim": "r",    "scale_m": 1e-9},
    {"id": 80, "name": "strontium",                  "particle": "tau_neutrino",       "body": "Sr2+ node",                           "geol": "strontium (alkaline earth)",                      "dim": "h",    "scale_m": 1e-9},
    {"id": 81, "name": "barium",                     "particle": "charm_quark",        "body": "Ba2+ node",                           "geol": "barium (alkaline earth)",                         "dim": "h",    "scale_m": 1e-9},
    {"id": 82, "name": "cesium",                     "particle": "strange_quark",      "body": "Cs+ node (glymphatic)",               "geol": "cesium (alkali metal)",                           "dim": "g",    "scale_m": 1e-9},
    {"id": 83, "name": "francium",                   "particle": "energy",             "body": "Fr+ (glymphatic GSH)",                "geol": "francium (alkali metal, rare)",                   "dim": "s",    "scale_m": 1e-9},
    {"id": 84, "name": "astatine",                   "particle": "higgs",              "body": "At (nitrogenase)",                    "geol": "astatine (halogen, radioactive)",                 "dim": "p",    "scale_m": 1e-9},
]
assert len(CIRCUIT_84) == 84, f"expected 84, got {len(CIRCUIT_84)}"

# ============================================================
# CANDIDATE COSMIC STRUCTURES (9-vector each)
# ============================================================
COSMIC_CANDIDATES = [
    # Solar System (8 planets + sun + moon + oort + heliosphere)
    {"name": "Sun",                   "scale_m": 1.39e9,   "coupling": 0.85, "phase": 0.4, "sym": 0.7, "time": 0.7, "boundary": 0.5, "energy": 0.95},
    {"name": "Mercury",               "scale_m": 2.44e6,   "coupling": 0.4, "phase": 0.3, "sym": 0.5, "time": 0.6, "boundary": 0.6, "energy": 0.3},
    {"name": "Venus",                 "scale_m": 6.05e6,   "coupling": 0.4, "phase": 0.3, "sym": 0.5, "time": 0.6, "boundary": 0.6, "energy": 0.3},
    {"name": "Earth",                 "scale_m": 6.37e6,   "coupling": 0.5, "phase": 0.6, "sym": 0.6, "time": 0.7, "boundary": 0.7, "energy": 0.5},
    {"name": "Moon",                  "scale_m": 1.74e6,   "coupling": 0.3, "phase": 0.7, "sym": 0.5, "time": 0.6, "boundary": 0.6, "energy": 0.2},
    {"name": "Mars",                  "scale_m": 3.39e6,   "coupling": 0.3, "phase": 0.4, "sym": 0.5, "time": 0.6, "boundary": 0.6, "energy": 0.2},
    {"name": "Jupiter",               "scale_m": 6.99e7,   "coupling": 0.4, "phase": 0.5, "sym": 0.5, "time": 0.7, "boundary": 0.5, "energy": 0.6},
    {"name": "Saturn",                "scale_m": 5.82e7,   "coupling": 0.3, "phase": 0.6, "sym": 0.4, "time": 0.7, "boundary": 0.5, "energy": 0.4},
    {"name": "Uranus",                "scale_m": 2.54e7,   "coupling": 0.3, "phase": 0.7, "sym": 0.4, "time": 0.7, "boundary": 0.5, "energy": 0.3},
    {"name": "Neptune",               "scale_m": 2.46e7,   "coupling": 0.3, "phase": 0.7, "sym": 0.4, "time": 0.7, "boundary": 0.5, "energy": 0.3},
    {"name": "Oort_Cloud",           "scale_m": 1e15,     "coupling": 0.05,"phase": 0.8, "sym": 0.7, "time": 0.9, "boundary": 0.95,"energy": 0.1},
    {"name": "Heliosphere",           "scale_m": 1e13,     "coupling": 0.3, "phase": 0.7, "sym": 0.6, "time": 0.8, "boundary": 0.95,"energy": 0.6},
    {"name": "Solar_Wind",            "scale_m": 1e11,     "coupling": 0.3, "phase": 0.6, "sym": 0.5, "time": 0.9, "boundary": 0.0, "energy": 0.7},
    {"name": "Termination_Shock",     "scale_m": 1.13e13,  "coupling": 0.3, "phase": 0.7, "sym": 0.5, "time": 0.8, "boundary": 0.85,"energy": 0.6},
    {"name": "Heliopause",            "scale_m": 1.85e13,  "coupling": 0.3, "phase": 0.8, "sym": 0.5, "time": 0.8, "boundary": 0.95,"energy": 0.4},
    # Galaxy / Local Group
    {"name": "Milky_Way_Galaxy",      "scale_m": 9.5e20,   "coupling": 0.7, "phase": 0.7, "sym": 0.7, "time": 0.9, "boundary": 0.7, "energy": 0.7},
    {"name": "Sagittarius_A*",        "scale_m": 2.4e10,   "coupling": 0.95,"phase": 0.5, "sym": 0.95,"time": 0.9, "boundary": 0.95,"energy": 0.95},
    {"name": "Andromeda_Galaxy",      "scale_m": 1.1e22,   "coupling": 0.6, "phase": 0.7, "sym": 0.7, "time": 0.9, "boundary": 0.7, "energy": 0.6},
    {"name": "Triangulum_Galaxy",     "scale_m": 6e21,     "coupling": 0.4, "phase": 0.7, "sym": 0.6, "time": 0.9, "boundary": 0.7, "energy": 0.4},
    {"name": "Large_Magellanic_Cloud","scale_m": 1.4e21,   "coupling": 0.3, "phase": 0.6, "sym": 0.5, "time": 0.9, "boundary": 0.7, "energy": 0.3},
    {"name": "Small_Magellanic_Cloud","scale_m": 7e20,     "coupling": 0.2, "phase": 0.6, "sym": 0.5, "time": 0.9, "boundary": 0.7, "energy": 0.2},
    # Galaxy clusters
    {"name": "Local_Group",           "scale_m": 1.1e22,   "coupling": 0.5, "phase": 0.7, "sym": 0.6, "time": 0.9, "boundary": 0.7, "energy": 0.4},
    {"name": "Virgo_Cluster",        "scale_m": 1.5e23,   "coupling": 0.6, "phase": 0.7, "sym": 0.7, "time": 0.9, "boundary": 0.7, "energy": 0.5},
    {"name": "Coma_Cluster",          "scale_m": 3e23,     "coupling": 0.7, "phase": 0.7, "sym": 0.7, "time": 0.9, "boundary": 0.7, "energy": 0.6},
    {"name": "Perseus_Cluster",       "scale_m": 2.5e23,   "coupling": 0.7, "phase": 0.7, "sym": 0.7, "time": 0.9, "boundary": 0.7, "energy": 0.6},
    {"name": "Norma_Cluster",         "scale_m": 2.5e23,   "coupling": 0.7, "phase": 0.7, "sym": 0.7, "time": 0.9, "boundary": 0.7, "energy": 0.5},
    # Specific structures (already in CIRCUITFILE)
    {"name": "TRAPPIST-1",            "scale_m": 5.7e10,   "coupling": 0.3, "phase": 0.5, "sym": 0.5, "time": 0.7, "boundary": 0.5, "energy": 0.3},
    {"name": "K2-18b",                "scale_m": 1.0e21,   "coupling": 0.3, "phase": 0.5, "sym": 0.5, "time": 0.7, "boundary": 0.5, "energy": 0.3},
    {"name": "NGC_4889",              "scale_m": 1.5e22,   "coupling": 0.85,"phase": 0.5, "sym": 0.6, "time": 0.7, "boundary": 0.7, "energy": 0.85},
    {"name": "NGC_4874",              "scale_m": 1.5e22,   "coupling": 0.7, "phase": 0.5, "sym": 0.6, "time": 0.7, "boundary": 0.7, "energy": 0.6},
    {"name": "NGC_1275",              "scale_m": 7e22,     "coupling": 0.95,"phase": 0.6, "sym": 0.6, "time": 0.8, "boundary": 0.8, "energy": 0.95},
    {"name": "NGC_1265",              "scale_m": 7e22,     "coupling": 0.7, "phase": 0.6, "sym": 0.6, "time": 0.8, "boundary": 0.7, "energy": 0.7},
    {"name": "Helix_Nebula_NGC7293",  "scale_m": 1.4e17,   "coupling": 0.4, "phase": 0.7, "sym": 0.6, "time": 0.9, "boundary": 0.5, "energy": 0.4},
    {"name": "Crab_Nebula",           "scale_m": 5e16,     "coupling": 0.5, "phase": 0.8, "sym": 0.5, "time": 0.9, "boundary": 0.5, "energy": 0.5},
    {"name": "Barnards_Star",         "scale_m": 5.96e16,  "coupling": 0.2, "phase": 0.4, "sym": 0.4, "time": 0.6, "boundary": 0.3, "energy": 0.2},
    # Large-scale structure
    {"name": "Laniakea_Supercluster", "scale_m": 2.4e24,   "coupling": 0.5, "phase": 0.7, "sym": 0.7, "time": 0.9, "boundary": 0.7, "energy": 0.4},
    {"name": "Cosmic_Web_Filament",   "scale_m": 1e25,     "coupling": 0.4, "phase": 0.7, "sym": 0.6, "time": 0.95,"boundary": 0.0, "energy": 0.5},
    {"name": "Boötes_Void",           "scale_m": 3.3e24,   "coupling": 0.05,"phase": 0.3, "sym": 0.3, "time": 0.5, "boundary": 0.6, "energy": 0.05},
    {"name": "CMB_Anisotropy",        "scale_m": 4.4e26,   "coupling": 0.4, "phase": 0.95,"sym": 0.95,"time": 0.95,"boundary": 0.99,"energy": 0.5},
    {"name": "Cosmic_Microwave_Background","scale_m": 4.4e26,"coupling": 0.5,"phase": 0.95,"sym": 0.95,"time": 0.95,"boundary": 0.99,"energy": 0.4},
    # Specific exotic
    {"name": "Quasar_3C_273",         "scale_m": 2.5e22,   "coupling": 0.95,"phase": 0.6, "sym": 0.6, "time": 0.9, "boundary": 0.6, "energy": 0.95},
    {"name": "Magnetar_SGR_1935",     "scale_m": 1.5e4,    "coupling": 0.95,"phase": 0.7, "sym": 0.5, "time": 0.9, "boundary": 0.7, "energy": 0.95},
    {"name": "Black_Hole_SMBH",       "scale_m": 1e10,     "coupling": 0.95,"phase": 0.3, "sym": 0.5, "time": 0.95,"boundary": 0.95,"energy": 0.95},
    {"name": "White_Dwarf",           "scale_m": 7e6,      "coupling": 0.5, "phase": 0.3, "sym": 0.4, "time": 0.7, "boundary": 0.8, "energy": 0.4},
    {"name": "Neutron_Star",          "scale_m": 1e4,      "coupling": 0.85,"phase": 0.4, "sym": 0.5, "time": 0.8, "boundary": 0.95,"energy": 0.7},
    {"name": "Main_Sequence_Star",    "scale_m": 7e8,      "coupling": 0.7, "phase": 0.5, "sym": 0.6, "time": 0.7, "boundary": 0.7, "energy": 0.85},
    {"name": "Red_Giant",             "scale_m": 1e10,     "coupling": 0.5, "phase": 0.6, "sym": 0.4, "time": 0.8, "boundary": 0.5, "energy": 0.5},
    {"name": "Stellar_Nursery_Molecular_Cloud","scale_m": 1e16,"coupling": 0.3,"phase": 0.6,"sym": 0.5,"time": 0.9,"boundary": 0.4,"energy": 0.4},
    {"name": "Accretion_Disk",        "scale_m": 1e10,     "coupling": 0.6, "phase": 0.7, "sym": 0.6, "time": 0.95,"boundary": 0.5, "energy": 0.7},
    {"name": "Gamma_Ray_Burst",       "scale_m": 1e22,     "coupling": 0.7, "phase": 0.95,"sym": 0.3, "time": 0.99,"boundary": 0.5, "energy": 0.95},
    {"name": "Cosmic_String",         "scale_m": 1e25,     "coupling": 0.4, "phase": 0.5, "sym": 0.7, "time": 0.5, "boundary": 0.0, "energy": 0.6},
    {"name": "Primordial_BH",         "scale_m": 1e-3,     "coupling": 0.6, "phase": 0.3, "sym": 0.3, "time": 0.5, "boundary": 0.95,"energy": 0.4},
    {"name": "Dark_Matter_Halo",      "scale_m": 1e22,     "coupling": 0.1, "phase": 0.3, "sym": 0.7, "time": 0.9, "boundary": 0.95,"energy": 0.0},
    {"name": "Cosmic_Void",           "scale_m": 1e25,     "coupling": 0.05,"phase": 0.2, "sym": 0.3, "time": 0.5, "boundary": 0.7, "energy": 0.0},
    {"name": "Galaxy_Cluster_Coma",   "scale_m": 3e23,     "coupling": 0.7, "phase": 0.7, "sym": 0.7, "time": 0.9, "boundary": 0.7, "energy": 0.6},
    {"name": "Intergalactic_Medium",  "scale_m": 1e24,     "coupling": 0.1, "phase": 0.5, "sym": 0.5, "time": 0.9, "boundary": 0.0, "energy": 0.2},
    {"name": "Active_Galactic_Nucleus","scale_m": 1e20,    "coupling": 0.85,"phase": 0.7, "sym": 0.5, "time": 0.9, "boundary": 0.7, "energy": 0.95},
    {"name": "Globular_Cluster",      "scale_m": 1e17,     "coupling": 0.5, "phase": 0.5, "sym": 0.7, "time": 0.7, "boundary": 0.6, "energy": 0.3},
    {"name": "Open_Cluster",          "scale_m": 1e17,     "coupling": 0.3, "phase": 0.4, "sym": 0.5, "time": 0.6, "boundary": 0.4, "energy": 0.2},
    {"name": "Supernova_Remnant",     "scale_m": 1e16,     "coupling": 0.5, "phase": 0.8, "sym": 0.5, "time": 0.9, "boundary": 0.5, "energy": 0.6},
    {"name": "Planetary_Nebula",      "scale_m": 1e15,     "coupling": 0.4, "phase": 0.7, "sym": 0.5, "time": 0.8, "boundary": 0.5, "energy": 0.4},
    {"name": "Pulsar_Wind_Nebula",    "scale_m": 1e16,     "coupling": 0.6, "phase": 0.8, "sym": 0.5, "time": 0.9, "boundary": 0.5, "energy": 0.6},
    {"name": "Fast_Radio_Burst_Source","scale_m": 1e22,    "coupling": 0.7, "phase": 0.95,"sym": 0.4, "time": 0.99,"boundary": 0.5, "energy": 0.7},
    {"name": "Hot_Jupiter_Exoplanet", "scale_m": 1e8,      "coupling": 0.3, "phase": 0.5, "sym": 0.4, "time": 0.7, "boundary": 0.5, "energy": 0.3},
    {"name": "Super_Earth",           "scale_m": 1e7,      "coupling": 0.3, "phase": 0.4, "sym": 0.4, "time": 0.6, "boundary": 0.5, "energy": 0.2},
    {"name": "Cosmic_String_Cusp",    "scale_m": 1e22,     "coupling": 0.4, "phase": 0.5, "sym": 0.5, "time": 0.5, "boundary": 0.5, "energy": 0.5},
    {"name": "Tidal_Disruption_Event","scale_m": 1e10,     "coupling": 0.7, "phase": 0.95,"sym": 0.4, "time": 0.95,"boundary": 0.5, "energy": 0.85},
    {"name": "Kilonova",              "scale_m": 1e10,     "coupling": 0.7, "phase": 0.85,"sym": 0.4, "time": 0.95,"boundary": 0.5, "energy": 0.85},
    {"name": "Primordial_Black_Hole_Evaporation","scale_m": 1e-15,"coupling": 0.5,"phase": 0.95,"sym": 0.3,"time": 0.95,"boundary": 0.95,"energy": 0.7},
    {"name": "Hawking_Radiation_Zone","scale_m": 1e-3,     "coupling": 0.05,"phase": 0.7, "sym": 0.3, "time": 0.7, "boundary": 0.95,"energy": 0.1},
    {"name": "Primordial_Grav_Wave_Bkg","scale_m": 4.4e26,"coupling": 0.1, "phase": 0.95,"sym": 0.95,"time": 0.95,"boundary": 0.99,"energy": 0.3},
    {"name": "Inflationary_Perturbation","scale_m": 1e-50,  "coupling": 0.7, "phase": 0.95,"sym": 0.95,"time": 0.95,"boundary": 0.0, "energy": 0.95},
    {"name": "Cosmic_Inflaton_Field",  "scale_m": 4.4e26,   "coupling": 0.4, "phase": 0.95,"sym": 0.7, "time": 0.95,"boundary": 0.99,"energy": 0.95},
    {"name": "Reheating_Plasma",       "scale_m": 1e26,     "coupling": 0.6, "phase": 0.95,"sym": 0.5, "time": 0.95,"boundary": 0.5, "energy": 0.95},
]

# ============================================================
# BIOCHEMISTRY CANDIDATES (9-vector each)
# ============================================================
BIOCHEM_CANDIDATES = [
    # Receptors
    {"name": "MC1R_receptor",         "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "DRD2_receptor",         "scale_m": 1e-9,    "coupling": 0.5, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "D1_D5_receptor",        "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.4},
    {"name": "GABA_A_receptor",       "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.6, "sym": 0.3, "time": 0.4, "boundary": 0.7, "energy": 0.3},
    {"name": "GABA_B_receptor",       "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.6, "sym": 0.3, "time": 0.5, "boundary": 0.7, "energy": 0.3},
    {"name": "NMDA_receptor",         "scale_m": 1e-9,    "coupling": 0.5, "phase": 0.5, "sym": 0.3, "time": 0.4, "boundary": 0.7, "energy": 0.4},
    {"name": "AMPA_receptor",         "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.3, "time": 0.4, "boundary": 0.7, "energy": 0.4},
    {"name": "alpha7_nAChR",          "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "5HT1A_receptor",       "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "V1A_vasopressin",       "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "V1B_vasopressin",       "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "OXT_oxytocin",          "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "MOR_opioid",            "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "NK1R_SubstanceP",       "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "glucocorticoid_receptor","scale_m": 1e-9,  "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "AQP4_aquaporin",        "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.5, "sym": 0.3, "time": 0.5, "boundary": 0.7, "energy": 0.2},
    {"name": "MHC_complex",           "scale_m": 1e-8,    "coupling": 0.3, "phase": 0.4, "sym": 0.5, "time": 0.4, "boundary": 0.7, "energy": 0.3},
    {"name": "T_cell_receptor",       "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "Insulin_receptor",      "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.4},
    {"name": "GLP1_receptor",         "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "CCK_receptor",          "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    # Enzymes
    {"name": "cytochrome_c_oxidase",  "scale_m": 1e-8,    "coupling": 0.6, "phase": 0.6, "sym": 0.5, "time": 0.6, "boundary": 0.7, "energy": 0.7},
    {"name": "heme_oxygenase_HO1",    "scale_m": 1e-8,    "coupling": 0.5, "phase": 0.6, "sym": 0.5, "time": 0.6, "boundary": 0.7, "energy": 0.5},
    {"name": "ATP_synthase",          "scale_m": 1e-8,    "coupling": 0.6, "phase": 0.7, "sym": 0.6, "time": 0.7, "boundary": 0.8, "energy": 0.95},
    {"name": "succinate_dehydrogenase","scale_m": 1e-8,    "coupling": 0.5, "phase": 0.6, "sym": 0.5, "time": 0.6, "boundary": 0.7, "energy": 0.6},
    {"name": "nitrogenase",           "scale_m": 1e-8,    "coupling": 0.5, "phase": 0.5, "sym": 0.5, "time": 0.5, "boundary": 0.7, "energy": 0.5},
    {"name": "lactate_dehydrogenase", "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "pyruvate_dehydrogenase","scale_m": 1e-8,    "coupling": 0.5, "phase": 0.6, "sym": 0.5, "time": 0.6, "boundary": 0.7, "energy": 0.6},
    {"name": "carbonic_anhydrase",    "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "acetyl_CoA_carboxylase","scale_m": 1e-8,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "Na_K_ATPase",           "scale_m": 1e-8,    "coupling": 0.6, "phase": 0.6, "sym": 0.5, "time": 0.7, "boundary": 0.8, "energy": 0.85},
    {"name": "Cl_ATPase",             "scale_m": 1e-8,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.7, "energy": 0.5},
    {"name": "Ca_ATPase_SERCA",       "scale_m": 1e-8,    "coupling": 0.5, "phase": 0.6, "sym": 0.5, "time": 0.6, "boundary": 0.7, "energy": 0.7},
    {"name": "proteasome",            "scale_m": 1e-8,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.7, "energy": 0.4},
    # Cell biology
    {"name": "mitochondrion",         "scale_m": 1e-6,    "coupling": 0.7, "phase": 0.7, "sym": 0.7, "time": 0.7, "boundary": 0.85,"energy": 0.85},
    {"name": "lysosome",              "scale_m": 1e-6,    "coupling": 0.4, "phase": 0.6, "sym": 0.5, "time": 0.6, "boundary": 0.8, "energy": 0.4},
    {"name": "nucleus",               "scale_m": 1e-5,    "coupling": 0.6, "phase": 0.5, "sym": 0.6, "time": 0.5, "boundary": 0.85,"energy": 0.6},
    {"name": "ribosome",              "scale_m": 1e-8,    "coupling": 0.5, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.7, "energy": 0.4},
    {"name": "endoplasmic_reticulum", "scale_m": 1e-6,    "coupling": 0.5, "phase": 0.6, "sym": 0.5, "time": 0.6, "boundary": 0.7, "energy": 0.5},
    {"name": "golgi_apparatus",       "scale_m": 1e-6,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.7, "energy": 0.4},
    {"name": "peroxisome",            "scale_m": 1e-6,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.7, "energy": 0.4},
    {"name": "nucleolus",             "scale_m": 1e-6,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.7, "energy": 0.4},
    {"name": "cytoskeleton",          "scale_m": 1e-7,    "coupling": 0.5, "phase": 0.5, "sym": 0.5, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "myosin_filament",       "scale_m": 1e-6,    "coupling": 0.6, "phase": 0.7, "sym": 0.6, "time": 0.6, "boundary": 0.7, "energy": 0.85},
    {"name": "actin_filament",        "scale_m": 1e-6,    "coupling": 0.5, "phase": 0.6, "sym": 0.6, "time": 0.5, "boundary": 0.7, "energy": 0.5},
    {"name": "neuron",                "scale_m": 1e-5,    "coupling": 0.7, "phase": 0.7, "sym": 0.5, "time": 0.7, "boundary": 0.6, "energy": 0.6},
    {"name": "axon",                  "scale_m": 1e-3,    "coupling": 0.5, "phase": 0.6, "sym": 0.5, "time": 0.7, "boundary": 0.4, "energy": 0.5},
    {"name": "dendrite",              "scale_m": 1e-5,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.4, "energy": 0.4},
    {"name": "synapse",               "scale_m": 1e-8,    "coupling": 0.5, "phase": 0.6, "sym": 0.4, "time": 0.6, "boundary": 0.7, "energy": 0.4},
    {"name": "synaptic_vesicle",      "scale_m": 1e-8,    "coupling": 0.3, "phase": 0.5, "sym": 0.3, "time": 0.5, "boundary": 0.7, "energy": 0.3},
    {"name": "myelin_sheath",         "scale_m": 1e-6,    "coupling": 0.3, "phase": 0.4, "sym": 0.5, "time": 0.4, "boundary": 0.7, "energy": 0.2},
    # Hormones
    {"name": "cortisol",              "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.3, "time": 0.5, "boundary": 0.4, "energy": 0.3},
    {"name": "testosterone",          "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.4},
    {"name": "progesterone",          "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.4},
    {"name": "estradiol",             "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.3},
    {"name": "thyroxine_T4",          "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.3, "time": 0.5, "boundary": 0.4, "energy": 0.4},
    {"name": "growth_hormone",        "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.4},
    {"name": "epinephrine",           "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.3, "time": 0.5, "boundary": 0.4, "energy": 0.4},
    {"name": "norepinephrine",       "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.3, "time": 0.5, "boundary": 0.4, "energy": 0.4},
    {"name": "serotonin",             "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.3},
    {"name": "dopamine",              "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.3, "time": 0.5, "boundary": 0.4, "energy": 0.4},
    {"name": "endorphin",             "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.3},
    {"name": "acetylcholine",         "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.3},
    {"name": "GABA",                  "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.3},
    {"name": "glutamate",             "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.4},
    {"name": "adenosine",             "scale_m": 1e-9,    "coupling": 0.3, "phase": 0.4, "sym": 0.3, "time": 0.4, "boundary": 0.4, "energy": 0.3},
    # Tissue / organ
    {"name": "liver_hepatocyte",      "scale_m": 1e-5,    "coupling": 0.5, "phase": 0.5, "sym": 0.5, "time": 0.5, "boundary": 0.7, "energy": 0.5},
    {"name": "kidney_nephron",        "scale_m": 1e-4,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.7, "energy": 0.4},
    {"name": "lung_alveolus",         "scale_m": 1e-4,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.7, "energy": 0.4},
    {"name": "heart_myocyte",         "scale_m": 1e-4,    "coupling": 0.5, "phase": 0.7, "sym": 0.5, "time": 0.7, "boundary": 0.7, "energy": 0.7},
    {"name": "skin_keratinocyte",     "scale_m": 1e-5,    "coupling": 0.3, "phase": 0.4, "sym": 0.4, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "bone_osteocyte",        "scale_m": 1e-5,    "coupling": 0.4, "phase": 0.4, "sym": 0.4, "time": 0.4, "boundary": 0.6, "energy": 0.4},
    {"name": "adipocyte",             "scale_m": 1e-4,    "coupling": 0.3, "phase": 0.4, "sym": 0.4, "time": 0.4, "boundary": 0.6, "energy": 0.5},
    {"name": "intestinal_epithelium", "scale_m": 1e-5,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "astrocyte",             "scale_m": 1e-5,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "microglia",             "scale_m": 1e-5,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "oligodendrocyte",       "scale_m": 1e-5,    "coupling": 0.3, "phase": 0.4, "sym": 0.4, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "purkinje_neuron",       "scale_m": 1e-4,    "coupling": 0.5, "phase": 0.6, "sym": 0.5, "time": 0.6, "boundary": 0.6, "energy": 0.5},
    {"name": "place_cell",            "scale_m": 1e-4,    "coupling": 0.5, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "grid_cell",             "scale_m": 1e-4,    "coupling": 0.5, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "head_direction_cell",   "scale_m": 1e-4,    "coupling": 0.5, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    # Blood
    {"name": "hemoglobin",            "scale_m": 1e-8,    "coupling": 0.5, "phase": 0.5, "sym": 0.5, "time": 0.5, "boundary": 0.7, "energy": 0.5},
    {"name": "ferritin",              "scale_m": 1e-8,    "coupling": 0.4, "phase": 0.4, "sym": 0.4, "time": 0.4, "boundary": 0.7, "energy": 0.4},
    {"name": "transferrin",           "scale_m": 1e-8,    "coupling": 0.4, "phase": 0.4, "sym": 0.4, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "albumin",               "scale_m": 1e-8,    "coupling": 0.3, "phase": 0.4, "sym": 0.4, "time": 0.4, "boundary": 0.6, "energy": 0.3},
    {"name": "cytochrome_c",          "scale_m": 1e-8,    "coupling": 0.5, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.7, "energy": 0.4},
    {"name": "ubiquinone",            "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "coenzyme_Q10",          "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    # Mineral / element
    {"name": "iron_Fe",               "scale_m": 1e-9,    "coupling": 0.5, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "magnesium_Mg",          "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "calcium_Ca",            "scale_m": 1e-9,    "coupling": 0.5, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "potassium_K",           "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "sodium_Na",             "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "zinc_Zn",               "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "copper_Cu",             "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "selenium_Se",           "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
    {"name": "iodine_I",              "scale_m": 1e-9,    "coupling": 0.4, "phase": 0.5, "sym": 0.4, "time": 0.5, "boundary": 0.6, "energy": 0.4},
]

# ============================================================
# 9-VECTOR ENCODER
# ============================================================
def encode_circuit_node(node: dict) -> List[float]:
    """Encode a circuit node into 9-vector."""
    p = node["particle"]
    coupling = PARTICLE_COUPLING.get(p, 0.5)
    direction = DIM_DIRECTION.get(node["dim"], 0.5)
    scale = scale_encode(node["scale_m"])
    # Heuristics for remaining dimensions
    # phase: 0.7 if "decay"/"out" in name else 0.4
    phase = 0.7 if any(k in node["name"].lower() for k in ["decay","out","fire","release","spike","burst"]) else 0.4
    # symmetry: 0.5 default, higher for "latch"/"d_ff" (preserves state)
    symmetry = 0.7 if any(k in node["name"].lower() for k in ["latch","ff","d_ff","t_ff","sr","preservation"]) else 0.4
    # time_response: 0.7 if dim in {r, nu, gamma} (oscillating/dynamic) else 0.4
    time_r = 0.7 if node["dim"] in {"r","nu","gamma","d"} else 0.4
    # boundary: 0.7 if "and" or "nand" (closed gate) else 0.5
    boundary = 0.8 if any(k in node["name"].lower() for k in ["and","nand","ff","latch"]) else 0.5
    # energy_flow: 0.7 for source particles (proton, heme), 0.3 for sink (tau, axion)
    source_particles = {"proton", "photon", "heme", "right_testosterone", "higgs", "gluon"}
    energy = 0.7 if p in source_particles else (0.3 if p in {"tau", "axion", "bottom_quark"} else 0.5)
    return [0.3, direction, scale, phase, coupling, symmetry, time_r, boundary, energy]

def encode_candidate(c: dict) -> List[float]:
    """Encode a cosmic or biochem candidate into 9-vector."""
    scale = scale_encode(c["scale_m"])
    return [
        0.5,                    # dim (assume tensor for cosmic, scalar for biochem)
        0.5,                    # direction
        scale,
        c.get("phase", 0.5),
        c.get("coupling", 0.5),
        c.get("sym", 0.5),
        c.get("time", 0.5),
        c.get("boundary", 0.5),
        c.get("energy", 0.5),
    ]

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Cosine similarity in 9-dim space."""
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

# ============================================================
# MAIN: Map each of 84 circuit nodes to top-3 cosmic + biochem isomorphism
# ============================================================
def main():
    results = []
    for node in CIRCUIT_84:
        node_vec = encode_circuit_node(node)

        # Score against cosmic candidates
        cosmic_scored = [(c["name"], cosine_similarity(node_vec, encode_candidate(c))) for c in COSMIC_CANDIDATES]
        cosmic_scored.sort(key=lambda x: -x[1])

        # Score against biochem candidates
        biochem_scored = [(c["name"], cosine_similarity(node_vec, encode_candidate(c))) for c in BIOCHEM_CANDIDATES]
        biochem_scored.sort(key=lambda x: -x[1])

        results.append({
            "id": node["id"],
            "name": node["name"],
            "particle": node["particle"],
            "body": node["body"],
            "geol_native": node["geol"],
            "dim": node["dim"],
            "vector": [round(x, 4) for x in node_vec],
            "cosmic_top3": [(name, round(s, 4)) for name, s in cosmic_scored[:3]],
            "biochem_top3": [(name, round(s, 4)) for name, s in biochem_scored[:3]],
        })

    out = {
        "_version": "v1.0",
        "_date": "2026-09-09",
        "_method": "9-vector cosine similarity in physics attribute space",
        "_n_circuit_nodes": len(CIRCUIT_84),
        "_n_cosmic_candidates": len(COSMIC_CANDIDATES),
        "_n_biochem_candidates": len(BIOCHEM_CANDIDATES),
        "results": results,
    }
    out_path = Path(__file__).parent / "circuit84_isomorphism.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"  Circuit nodes: {len(CIRCUIT_84)}")
    print(f"  Cosmic candidates: {len(COSMIC_CANDIDATES)}")
    print(f"  Biochem candidates: {len(BIOCHEM_CANDIDATES)}")
    print(f"  Per-node top-3 cosmic + top-3 biochem isomorphism = {len(results)*6} mappings")

    # Print top 5 nodes summary
    print("\nTop 5 isomorphism summaries:")
    for r in results[:5]:
        print(f"  [{r['id']}] {r['name']} (particle={r['particle']}, dim={r['dim']})")
        print(f"      cosmic: {r['cosmic_top3']}")
        print(f"      biochem: {r['biochem_top3']}")

    return out

if __name__ == "__main__":
    main()
