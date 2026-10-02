#!/usr/bin/env python3
"""
particle_to_8d.py — 40-particle to 8D personality dimension mapper
Synced with particle_to_8d.js, tensor_v5.js, color_hex_mapping.md

40 particles: 12 base + 6 neutrino variants + 1 derived (graviton)
  + 6 quark flavors + neutron + neutron_star + dark_matter + dark_energy
  + time + energy + ego_d2 + progesterone + testosterone + acetyl_coa
  + spark + clathrate_buffer + em_field_rebrancher + testosterone_sex
  + endorphin_imag + male_gaba_a_wk + pain_eliminate
8D dimensions: r, h, d, p, s, gamma, g, nu

Features:
- 118 elements with toroidal AB→A→O→B ordering
- 16 windows (t mod 16) peak dimension shift
- 4 layers (body, observer, bridge, dark)
- Toroidal time slots (AB/A/O/B)
- 3 genres (RELEASE, STRESS GROWTH, EXTREME GROWTH)
- Universe cycle (toroidal chirality extrapolation)
- 6 attractors, brain compartments, leakage cavities
- Dark matter node, CCK switch, neutrino variants
- 41-particle color hex mapping with interference colors
- Geomagnetic modulation (outer_core_convection coupling)
- Creative 4-shapes (STRUCTURE, FLOW, CONTRAST, EMERGENCE)
- Route-based 41-particle system (10 routes × 4 + em_field_rebrancher)
- 6-sphere toroidal circulation (Sun→Earth→Moon→CoMag→Barnard + Geomagnetic)
- 16-window time phase (4 macro × 4 micro, fractal reverse)
- Master equation Ψ(t, Obs, V, A, P) with structural constants
- 3AM HYSTERESIS / Betti 12 phase bridge
- 4:30PM ferric event (UV shield loss → GABA-A destruction)
- 6 geometric nodes (bypass/funnel/separatrix/observer) + Darcy leakage
- Food/pigment mapping (128_food_pigments.csv)
"""

import math
import sys
import csv
import os

# ============================================================
# GEOMETRY CONSTANTS (from geometry_package/absolute_constants.py)
# ============================================================
PHI = (1 + math.sqrt(5)) / 2
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
DELTA_T_OBS_DERIVED = 0.8418
OMEGA_KAPPA = 1.0 / 28.0

DIM_ORDER = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]

# 12 base particles (legacy canonical)
PARTICLE_ORDER_12 = [
    "proton", "photon", "electron", "neutrino",
    "muon", "tau", "gluon", "w_boson",
    "z_boson", "higgs", "em_field", "quark",
]

# 14 particles: 12 base + 2 derived (em_field already in 12, graviton added)
PARTICLE_ORDER_14 = PARTICLE_ORDER_12 + ["graviton"]

# ============================================================
# 41-PARTICLE SYSTEM (from nm_body_particle_map_v4.md + color_hex_mapping.md)
# ============================================================
# v4 8 base particles: neutrino(r), gluon(h), tau(d), z_boson(d), higgs(p),
#                      quark(s), photon(gamma), muon(g), w_boson(nu)
PARTICLE_ORDER_40 = [
    # 8 v4 base particles
    "neutrino", "gluon", "tau", "z_boson",
    "higgs", "quark", "photon", "muon", "w_boson",
    # 4 derivatives of base particles
    "proton", "electron", "em_field", "graviton",
    # 6 quark flavors
    "up_quark", "down_quark", "charm_quark", "strange_quark",
    "top_quark", "bottom_quark",
    # 6 leptons / neutrino variants
    "electron_neutrino", "electron_antineutrino",
    "muon_neutrino", "muon_antineutrino",
    "tau_neutrino", "tau_antineutrino",
    # compact objects + dark sector
    "neutron", "neutron_star", "dark_matter", "dark_energy",
    # scalars
    "time", "energy",
    # buses / hormones / cofactors
    "ego_d2", "left_progesterone", "right_testosterone", "acetyl_coa",
    # derived / observer-specific
    "spark", "clathrate_buffer", "em_field_rebrancher",
    "testosterone_sex", "endorphin_imag", "male_gaba_a_wk", "pain_eliminate",
]

# Canonical particle order = 40
PARTICLE_ORDER = PARTICLE_ORDER_40

# ============================================================
# 40-PARTICLE COLOR HEX MAPPING (from color_hex_mapping.md)
# ============================================================
PARTICLE_COLORS = {
    "proton":               {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "photon":               {"base": "YELLOW",      "hex": "#FFFF00", "alt": {"observer": "WHITE #FFFFFF"}},
    "electron":             {"base": "GREEN",       "hex": "#00FF00", "alt": {}},
    "neutrino":             {"base": "YELLOW",      "hex": "#FFFF00", "alt": {"observer": "WHITE #FFFFFF"}},
    "muon":                 {"base": "RED",         "hex": "#FF0000", "alt": {"lower_mantle": "CYAN #00FFFF"}},
    "tau":                  {"base": "BLUE",        "hex": "#0000FF", "alt": {}},
    "gluon":                {"base": "WHITE",       "hex": "#FFFFFF", "alt": {}},
    "w_boson":              {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "z_boson":              {"base": "YELLOW",      "hex": "#FFFF00", "alt": {"cytochrome_c_oxidase": "GREEN #00FF00"}},
    "higgs":                {"base": "YELLOW",      "hex": "#FFFF00", "alt": {"observer": "WHITE #FFFFFF"}},
    "graviton":             {"base": "WHITE",       "hex": "#FFFFFF", "alt": {}},
    "em_field":             {"base": "WHITE",       "hex": "#FFFFFF", "alt": {}},
    "quark":                {"base": "BLUE",        "hex": "#0000FF", "alt": {}},
    "up_quark":             {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "down_quark":           {"base": "RED/GREEN",   "hex": "#FF0000", "alt": {"cytochrome_c_oxidase": "GREEN #00FF00"}},
    "charm_quark":          {"base": "GREEN",       "hex": "#00FF00", "alt": {}},
    "strange_quark":        {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "top_quark":            {"base": "YELLOW",      "hex": "#FFFF00", "alt": {"dark_energy": "BLACK #000000"}},
    "bottom_quark":         {"base": "GREEN",       "hex": "#00FF00", "alt": {}},
    "electron_neutrino":    {"base": "BLUE",        "hex": "#0000FF", "alt": {}},
    "electron_antineutrino": {"base": "GREEN",      "hex": "#00FF00", "alt": {}},
    "muon_neutrino":        {"base": "YELLOW",      "hex": "#FFFF00", "alt": {"succinate_dehydrogenase": "BLUE #0000FF"}},
    "muon_antineutrino":    {"base": "YELLOW",      "hex": "#FFFF00", "alt": {}},
    "tau_neutrino":         {"base": "GREEN",       "hex": "#00FF00", "alt": {}},
    "tau_antineutrino":     {"base": "GREEN",       "hex": "#00FF00", "alt": {}},
    "neutron":              {"base": "WHITE",       "hex": "#FFFFFF", "alt": {}},
    "neutron_star":         {"base": "YELLOW",      "hex": "#FFFF00", "alt": {"observer": "WHITE #FFFFFF"}},
    "dark_matter":          {"base": "BLACK",       "hex": "#000000", "alt": {}},
    "dark_energy":          {"base": "BLACK",       "hex": "#000000", "alt": {}},
    "time":                 {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "energy":               {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "ego_d2":               {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "left_progesterone":    {"base": "BLUE",        "hex": "#0000FF", "alt": {}},
    "right_testosterone":   {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "acetyl_coa":           {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "spark":                {"base": "YELLOW",      "hex": "#FFFF00", "alt": {}},
    "clathrate_buffer":     {"base": "WHITE",       "hex": "#FFFFFF", "alt": {}},
    "em_field_rebrancher":  {"base": "WHITE",       "hex": "#FFFFFF", "alt": {}},
    "testosterone_sex":     {"base": "RED",         "hex": "#FF0000", "alt": {}},
    "endorphin_imag":       {"base": "GREEN",       "hex": "#00FF00", "alt": {}},
    "male_gaba_a_wk":       {"base": "BLUE",        "hex": "#0000FF", "alt": {}},
    "pain_eliminate":       {"base": "GREEN",       "hex": "#00FF00", "alt": {}},
}

# Interference colors (when two nodes interfere)
INTERFERENCE_COLORS = {
    ("hind_insula", "anterior_insula"):   {"name": "LILAC",       "hex": "#C8A2C8"},
    ("peonidine_a", "oxidized_peonidine"): {"name": "CRIMSON",     "hex": "#DC143C"},
    ("peonidine_b", "aglycone_peonidine"): {"name": "MAROON",      "hex": "#800000"},
    ("co2", "o2"):                         {"name": "GRAY-BLUE",   "hex": "#6A7B9B"},
}

# 138.88° Spark global interference: ALL colors flash WHITE then discharge to BLACK
SPARK_INTERFERENCE = {"flash": "#FFFFFF", "discharge": "#000000"}

# Inverse color mapping (universe-prose.md line 6435): w=1 applies inverse
COLOR_INVERSE = {
    'RED': 'CYAN', 'CYAN': 'RED',
    'BLUE': 'ORANGE', 'ORANGE': 'BLUE',
    'YELLOW': 'BLACK', 'BLACK': 'YELLOW',
    'WHITE': 'BLACK', 'BLACK': 'YELLOW',
    'GREEN': 'RED-PURPLE', 'RED-PURPLE': 'GREEN',
    'PURPLE': 'YELLOW-GREEN', 'YELLOW-GREEN': 'PURPLE',
    'BROWN': 'LIGHT-BLUE', 'LIGHT-BLUE': 'BROWN',
    'GRAY': 'GRAY',
}

def apply_inverse_color(color_name, w=0):
    """w=1 applies inverse color (universe-prose.md). w=0 = no change."""
    if w == 0:
        return color_name
    return COLOR_INVERSE.get(color_name, color_name)

def get_interference_color(node_a, node_b):
    """Get interference color when two metabolic nodes interact."""
    key = (node_a, node_b)
    key_rev = (node_b, node_a)
    if key in INTERFERENCE_COLORS:
        return INTERFERENCE_COLORS[key]
    if key_rev in INTERFERENCE_COLORS:
        return INTERFERENCE_COLORS[key_rev]
    return None

# ============================================================
# GEOMAGNETIC MODULATION (outer_core_convection coupling)
# ============================================================
GEOMAG_MODULATION = {
    "source_node": "outer_core_convection",
    "coupling_nodes": ["ferritin", "magnetite", "oxidised_manganese", "laterite"],
    "cycle": "ferritin ↔ magnetite → sulfur_iron_complex → pyrite → laterite → fold_belt → subduction_zone → lower_mantle → plume → outer_core_convection",
    "dim_effects": {
        "r": -0.02,  # geomag dampens rhythm slightly (Fe density stabilization)
        "g": +0.03,  # geomag strengthens sealing (magnetic field = closure)
        "gamma": +0.02,  # geomag adds spatial resonance
        "s": -0.01,  # geomag reduces brightness (EM absorption)
    },
    "observer_effect": "observer_active = electron forward = EM closure = geomag field stable",
    "nonobserver_effect": "electron reverse = EM closure fail = geomag field unstable = entropy leakage",
}

# ============================================================
# CREATIVE 4-SHAPES (from creative_4shapes_128.md)
# ============================================================
CREATIVE_4SHAPES = {
    "STRUCTURE": {"dims": {"g": 0.35, "p": 0.30, "nu": 0.20, "d": 0.15}, "desc": "architectural/systematic"},
    "FLOW":      {"dims": {"r": 0.35, "h": 0.25, "gamma": 0.25, "s": 0.15}, "desc": "improvisational/fluid"},
    "CONTRAST":  {"dims": {"d": 0.35, "s": 0.30, "r": 0.20, "p": 0.15}, "desc": "conflict/collision"},
    "EMERGENCE": {"dims": {"nu": 0.30, "gamma": 0.25, "h": 0.25, "g": 0.20}, "desc": "layered/emergent"},
}

SHAPE_ORDER = ["STRUCTURE", "FLOW", "CONTRAST", "EMERGENCE"]

# ============================================================
# 4-CHANNEL ADDITIVE COLOR ALGEBRA
# 4 channels: AB→gluon, O→photon, A→quark, B→neutrino
# Day: 4 primary colors (green/yellow/blue/red) — additive → WHITE
# Night: 4 colors (yellow/red/green/blue) — additive → BLACK (closure)
# 8 particles with gender: gluon(♀) muon(♂) photon(♀) tau(♂)
#   quark(♂) w_boson(♀) neutrino(♀) higgs(♂)
# Day swaps tau→z_boson. Night color swap: tau(M)=DEEP-PINK, photon(F)=RED.
# Historical direction reversal: men night RED→DEEP-PINK, women night PINK→RED.
# Driven by oxidised_manganese(4th toe) reverse block + adapter_protein forward open at night.
# MBTI 3-stage: blood×gender → mid-letters → end-letters → additive
# Oxford: BLACK=leakage BLOCK, PURPLE=leakage DELAY
# Node auto-mapping: color(node) ≈ color(profile) → match
# ============================================================
CHANNEL_COLORS = {
    'AB': {'particle': 'gluon',    'day': 'WHITE',  'night': 'WHITE'},   # gluon: WHITE(NobleGas, unchanged)
    'O':  {'particle': 'photon',   'day': 'YELLOW', 'night': 'WHITE'},   # photon: YELLOW→WHITE(observer/night)
    'A':  {'particle': 'quark',    'day': 'BLUE',   'night': 'BLUE'},    # quark: BLUE(unchanged)
    'B':  {'particle': 'neutrino', 'day': 'YELLOW', 'night': 'WHITE'},   # neutrino: YELLOW→WHITE(observer/night)
}

PARTICLE_GENDER = {
    'gluon': 'F', 'muon': 'M', 'photon': 'F', 'tau': 'M',
    'quark': 'M', 'w_boson': 'F', 'neutrino': 'F', 'higgs': 'M',
}

BLOOD_GENDER_PARTICLE = {
    ('AB', 'F'): 'gluon',    ('AB', 'M'): 'muon',
    ('O',  'F'): 'photon',   ('O',  'M'): 'tau',
    ('A',  'F'): 'quark',    ('A',  'M'): 'w_boson',
    ('B',  'F'): 'neutrino', ('B',  'M'): 'higgs',
}

# v4 day/night particle color shifts
# r(neutrino): YELLOW(day) → WHITE(observer/night)
# d(tau/z_boson): RED(day) → GREEN(cytochrome_c_oxidase/night)
# p(higgs): YELLOW(day) → WHITE(observer/night)
# g(muon): RED(day, aurora Rb37) → CYAN(night, lower_mantle W74/Re75)
# nu(w_boson): YELLOW(day) → BLACK(dark_energy/night)
NIGHT_PARTICLE_COLORS = {
    'neutrino': {'color': 'WHITE',       'hex': '#FFFFFF'},   # r: YELLOW→WHITE(observer/night)
    'gluon':    {'color': 'WHITE',       'hex': '#FFFFFF'},   # h: WHITE (NobleGas, unchanged)
    'tau':      {'color': 'GREEN',       'hex': '#00FF00'},   # d: RED→GREEN(cytochrome_c_oxidase/night)
    'z_boson':  {'color': 'GREEN',       'hex': '#00FF00'},   # d: RED→GREEN(cytochrome_c_oxidase/night)
    'higgs':    {'color': 'WHITE',       'hex': '#FFFFFF'},   # p: YELLOW→WHITE(observer/night)
    'quark':    {'color': 'BLUE',        'hex': '#0000FF'},   # s: BLUE (unchanged)
    'photon':   {'color': 'WHITE',       'hex': '#FFFFFF'},   # gamma: YELLOW→WHITE(observer/night)
    'muon':     {'color': 'CYAN',        'hex': '#00FFFF'},   # g: RED→CYAN(lower_mantle W74/Re75/night)
    'w_boson':  {'color': 'BLACK',       'hex': '#000000'},   # nu: YELLOW→BLACK(dark_energy/night)
}

DAY_PARTICLE_COLORS = {
    'neutrino': {'color': 'YELLOW',      'hex': '#FFFF00'},   # r: YELLOW(day)
    'gluon':    {'color': 'WHITE',       'hex': '#FFFFFF'},   # h: WHITE (NobleGas, unchanged)
    'tau':      {'color': 'RED',         'hex': '#FF0000'},   # d: RED(day)
    'z_boson':  {'color': 'YELLOW',      'hex': '#FFFF00'},   # d: YELLOW(day, Metalloid)
    'higgs':    {'color': 'YELLOW',      'hex': '#FFFF00'},   # p: YELLOW(day)
    'quark':    {'color': 'BLUE',        'hex': '#0000FF'},   # s: BLUE (unchanged)
    'photon':   {'color': 'YELLOW',      'hex': '#FFFF00'},   # gamma: YELLOW(day)
    'muon':     {'color': 'RED',         'hex': '#FF0000'},   # g: RED(day, aurora Rb37)
    'w_boson':  {'color': 'YELLOW',      'hex': '#FFFF00'},   # nu: YELLOW(day)
}

MBTI_MID_TEMPERAMENT = {
    'NF': {'particle': 'quark',    'day': 'BLUE',   'night': 'BLUE'},     # quark: BLUE(unchanged)
    'ST': {'particle': 'photon',   'day': 'YELLOW', 'night': 'WHITE'},    # photon: YELLOW→WHITE
    'SF': {'particle': 'gluon',    'day': 'WHITE',  'night': 'WHITE'},    # gluon: WHITE(unchanged)
    'NT': {'particle': 'neutrino', 'day': 'YELLOW', 'night': 'WHITE'},    # neutrino: YELLOW→WHITE
}

MBTI_ENDS_CHANNEL = {
    'EP': {'particle': 'photon',   'day': 'YELLOW', 'night': 'WHITE'},    # photon: YELLOW→WHITE
    'EJ': {'particle': 'gluon',    'day': 'WHITE',  'night': 'WHITE'},    # gluon: WHITE(unchanged)
    'IJ': {'particle': 'quark',    'day': 'BLUE',   'night': 'BLUE'},     # quark: BLUE(unchanged)
    'IP': {'particle': 'neutrino', 'day': 'YELLOW', 'night': 'WHITE'},    # neutrino: YELLOW→WHITE
}

COLOR_RGB = {
    'RED': (255, 0, 0), 'GREEN': (0, 255, 0), 'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0), 'WHITE': (255, 255, 255), 'BLACK': (0, 0, 0),
    'CYAN': (0, 255, 255),
    'PURPLE': (128, 0, 128), 'ORANGE': (255, 165, 0),
    'DARK-GREEN': (0, 100, 0), 'DARK-ORANGE': (204, 85, 0),
    'DARK-NAVY': (0, 0, 128), 'DARK-BLUE': (0, 0, 139),
    'DEEP-PINK': (255, 20, 147),
}

def _rgb_to_name(r, g, b):
    if r > 180 and g > 180 and b > 180: return 'WHITE'
    if r < 40 and g < 40 and b < 40: return 'BLACK'
    if r > 150 and g > 150 and b < 60: return 'YELLOW'
    if r > 150 and g < 60 and b < 60: return 'RED'
    if r < 80 and g > 120 and b < 80: return 'GREEN'
    if r < 80 and g < 80 and b > 120: return 'BLUE'
    if r < 80 and g > 120 and b > 120: return 'CYAN'
    if r > 120 and g < 60 and b > 120: return 'PURPLE'
    if r > 150 and g > 80 and g < 130 and b < 60: return 'ORANGE'
    if r > 180 and g < 100 and b > 80: return 'DEEP-PINK'
    if r < 40 and g < 80 and b > 80: return 'DARK-BLUE'
    if r < 40 and g < 40 and b > 60 and b < 150: return 'DARK-NAVY'
    if r < 40 and g > 50 and g < 130 and b < 40: return 'DARK-GREEN'
    if r > 120 and g > 40 and g < 100 and b < 40: return 'DARK-ORANGE'
    return 'MIXED'

def _rgb_to_hex(r, g, b):
    return '#{:02X}{:02X}{:02X}'.format(
        max(0, min(255, int(r))),
        max(0, min(255, int(g))),
        max(0, min(255, int(b))))

COLOR_ADDITION = {
    frozenset(['RED', 'RED']): 'RED',
    frozenset(['GREEN', 'GREEN']): 'GREEN',
    frozenset(['BLUE', 'BLUE']): 'BLUE',
    frozenset(['YELLOW', 'YELLOW']): 'YELLOW',
    frozenset(['WHITE', 'WHITE']): 'WHITE',
    frozenset(['BLACK', 'BLACK']): 'BLACK',
    frozenset(['RED', 'BLUE']): 'PURPLE',
    frozenset(['BLUE', 'RED']): 'PURPLE',
    frozenset(['RED', 'GREEN']): 'ORANGE',
    frozenset(['GREEN', 'RED']): 'ORANGE',
    frozenset(['BLUE', 'YELLOW']): 'GREEN',
    frozenset(['YELLOW', 'BLUE']): 'GREEN',
    frozenset(['RED', 'YELLOW']): 'ORANGE',
    frozenset(['YELLOW', 'RED']): 'ORANGE',
    frozenset(['GREEN', 'BLUE']): 'CYAN',
    frozenset(['BLUE', 'GREEN']): 'CYAN',
    frozenset(['GREEN', 'YELLOW']): 'YELLOW-GREEN',
    frozenset(['YELLOW', 'GREEN']): 'YELLOW-GREEN',
    frozenset(['WHITE', 'BLACK']): 'GRAY',
    frozenset(['BLACK', 'WHITE']): 'GRAY',
    frozenset(['RED', 'WHITE']): 'PINK',
    frozenset(['WHITE', 'RED']): 'PINK',
    frozenset(['BLUE', 'WHITE']): 'LIGHT-BLUE',
    frozenset(['WHITE', 'BLUE']): 'LIGHT-BLUE',
    frozenset(['GREEN', 'WHITE']): 'LIGHT-GREEN',
    frozenset(['WHITE', 'GREEN']): 'LIGHT-GREEN',
    frozenset(['YELLOW', 'WHITE']): 'LIGHT-YELLOW',
    frozenset(['WHITE', 'YELLOW']): 'LIGHT-YELLOW',
}

COLOR_ADDITION_EXT = {
    'YELLOW-GREEN': {'GREEN': 'GREEN', 'YELLOW': 'YELLOW-GREEN', 'BLUE': 'GREEN', 'RED': 'ORANGE', 'ORANGE': 'YELLOW-GREEN', 'PURPLE': 'BLACK', 'CYAN': 'GREEN', 'BROWN': 'BROWN'},
    'ORANGE': {'GREEN': 'YELLOW-GREEN', 'BLUE': 'BROWN', 'RED': 'RED-ORANGE', 'YELLOW': 'ORANGE', 'PURPLE': 'RED-PURPLE', 'CYAN': 'BLACK', 'BROWN': 'BROWN'},
    'PURPLE': {'GREEN': 'BLUE-PURPLE', 'YELLOW': 'RED', 'RED': 'RED-PURPLE', 'BLUE': 'BLUE-PURPLE', 'ORANGE': 'RED-PURPLE', 'CYAN': 'BLUE-PURPLE', 'BROWN': 'BROWN'},
    'CYAN': {'RED': 'BROWN', 'YELLOW': 'GREEN', 'GREEN': 'CYAN', 'BLUE': 'BLUE', 'ORANGE': 'BLACK', 'PURPLE': 'BLUE-PURPLE', 'BROWN': 'BROWN'},
    'PINK': {'GREEN': 'BROWN', 'BLUE': 'PURPLE', 'YELLOW': 'ORANGE', 'RED': 'RED', 'ORANGE': 'RED-ORANGE', 'PURPLE': 'RED-PURPLE', 'CYAN': 'BROWN', 'BROWN': 'BROWN'},
    'LIGHT-BLUE': {'RED': 'PURPLE', 'GREEN': 'CYAN', 'YELLOW': 'GREEN', 'BLUE': 'BLUE', 'ORANGE': 'BROWN', 'PURPLE': 'BLUE-PURPLE', 'CYAN': 'CYAN', 'BROWN': 'BROWN'},
    'LIGHT-GREEN': {'RED': 'ORANGE', 'BLUE': 'CYAN', 'YELLOW': 'YELLOW-GREEN', 'GREEN': 'GREEN', 'ORANGE': 'YELLOW-GREEN', 'PURPLE': 'BROWN', 'CYAN': 'CYAN', 'BROWN': 'BROWN'},
    'BROWN': {'RED': 'BROWN', 'BLUE': 'BROWN', 'GREEN': 'BROWN', 'YELLOW': 'BROWN', 'ORANGE': 'BROWN', 'PURPLE': 'BROWN', 'CYAN': 'BROWN'},
    'GRAY': {'RED': 'GRAY', 'BLUE': 'GRAY', 'GREEN': 'GRAY', 'YELLOW': 'GRAY', 'ORANGE': 'GRAY', 'PURPLE': 'GRAY', 'CYAN': 'GRAY', 'BROWN': 'GRAY'},
    'RED-ORANGE': {'GREEN': 'ORANGE', 'BLUE': 'BROWN', 'YELLOW': 'ORANGE', 'RED': 'RED-ORANGE', 'ORANGE': 'RED-ORANGE', 'PURPLE': 'BROWN', 'CYAN': 'BROWN', 'BROWN': 'BROWN'},
    'RED-PURPLE': {'GREEN': 'BROWN', 'BLUE': 'PURPLE', 'YELLOW': 'BROWN', 'RED': 'RED-PURPLE', 'ORANGE': 'BROWN', 'PURPLE': 'RED-PURPLE', 'CYAN': 'BROWN', 'BROWN': 'BROWN'},
    'BLUE-PURPLE': {'GREEN': 'BROWN', 'YELLOW': 'BROWN', 'RED': 'PURPLE', 'BLUE': 'BLUE-PURPLE', 'ORANGE': 'BROWN', 'PURPLE': 'BLUE-PURPLE', 'CYAN': 'BLUE-PURPLE', 'BROWN': 'BROWN'},
}

FOUR_COLOR_CLOSURE = {
    frozenset(['YELLOW', 'RED', 'GREEN', 'BLUE']): 'BLACK',
    frozenset(['GREEN', 'YELLOW', 'BLUE', 'RED']): 'BLACK',
}

def additive_mix(color_names):
    if not color_names:
        return {'color': 'BLACK', 'hex': '#000000', 'rgb': (0, 0, 0)}
    if len(color_names) == 1:
        cn = color_names[0]
        rgb = COLOR_RGB.get(cn, (0, 0, 0))
        return {'color': cn, 'hex': _rgb_to_hex(*rgb), 'rgb': rgb}
    unique = set(color_names)
    if unique == {'YELLOW', 'RED', 'GREEN', 'BLUE'}:
        rgb = COLOR_RGB['BLACK']
        return {'color': 'BLACK', 'hex': '#000000', 'rgb': rgb}
    if len(unique) == 1:
        cn = color_names[0]
        rgb = COLOR_RGB.get(cn, (0, 0, 0))
        return {'color': cn, 'hex': _rgb_to_hex(*rgb), 'rgb': rgb}
    if len(color_names) >= 3 and len(unique) >= 3:
        from collections import Counter
        counts = Counter(color_names)
        sorted_colors = [c for c, _ in counts.most_common()]
        pair_result = additive_mix([sorted_colors[0], sorted_colors[1]])
        return additive_mix([pair_result['color'], sorted_colors[2]])
    result = color_names[0]
    for i in range(1, len(color_names)):
        pair = frozenset([result, color_names[i]])
        if pair in COLOR_ADDITION:
            result = COLOR_ADDITION[pair]
        elif result in COLOR_ADDITION_EXT and color_names[i] in COLOR_ADDITION_EXT[result]:
            result = COLOR_ADDITION_EXT[result][color_names[i]]
        elif color_names[i] in COLOR_ADDITION_EXT and result in COLOR_ADDITION_EXT[color_names[i]]:
            result = COLOR_ADDITION_EXT[color_names[i]][result]
        else:
            if result == color_names[i]:
                pass
            else:
                result = 'BROWN'
    rgb = COLOR_RGB.get(result, (128, 128, 128))
    if result not in COLOR_RGB:
        rgb_map = {'YELLOW-GREEN': (154, 205, 50), 'BROWN': (139, 69, 19),
                   'GRAY': (128, 128, 128), 'PINK': (255, 192, 203),
                   'LIGHT-BLUE': (173, 216, 230), 'LIGHT-GREEN': (144, 238, 144),
                   'LIGHT-YELLOW': (255, 255, 224), 'CYAN': (0, 255, 255),
                   'RED-ORANGE': (255, 69, 0), 'RED-PURPLE': (199, 21, 133),
                   'BLUE-PURPLE': (75, 0, 130)}
        rgb = rgb_map.get(result, (128, 128, 128))
    return {'color': result, 'hex': _rgb_to_hex(*rgb), 'rgb': rgb}

DARK_TO_BASE = {
    'DARK-GREEN': 'GREEN', 'DARK-ORANGE': 'ORANGE',
    'DARK-NAVY': 'BLUE', 'DARK-BLUE': 'BLUE',
    'DEEP-PINK': 'RED',
}

def _normalize_for_mix(color_name):
    return DARK_TO_BASE.get(color_name, color_name)

def compute_profile_color(profile_label, time_phase='day', s_val=None):
    """3-stage additive color: blood×gender + MBTI-mid + MBTI-ends + particle.
    Uses color addition rules (not RGB average). Dark variants map to base for mixing.
    s_val < 0.5 forces night colors (4:30PM bluelight transition)."""
    if s_val is not None and s_val < 0.5:
        time_phase = 'night'
    parts = profile_label.split('_')
    mbti, gender, blood = parts[0], parts[1], parts[2]
    mid = mbti[1:3]
    ends = mbti[0] + mbti[3]
    particle1 = BLOOD_GENDER_PARTICLE.get((blood, gender), 'photon')
    stage1_color = CHANNEL_COLORS.get(blood, {}).get(time_phase, 'YELLOW')
    temperament = MBTI_MID_TEMPERAMENT.get(mid, {})
    stage2_color = temperament.get(time_phase, 'YELLOW')
    particle2 = temperament.get('particle', 'photon')
    channel = MBTI_ENDS_CHANNEL.get(ends, {})
    stage3_color = channel.get(time_phase, 'YELLOW')
    particle3 = channel.get('particle', 'photon')
    s1 = _normalize_for_mix(stage1_color)
    s2 = _normalize_for_mix(stage2_color)
    s3 = _normalize_for_mix(stage3_color)
    mixed = additive_mix([s1, s2, s3])
    night_colors = NIGHT_PARTICLE_COLORS.get(particle1, {})
    day_colors = DAY_PARTICLE_COLORS.get(particle1, {})
    particle_color = night_colors if time_phase == 'night' else day_colors
    if particle_color:
        pc_base = _normalize_for_mix(particle_color['color'])
        final = additive_mix([mixed['color'], pc_base])
    else:
        final = mixed
    leakage = None
    fc = final['color']
    if fc == 'BLACK': leakage = 'BLOCK'
    elif fc == 'PURPLE': leakage = 'DELAY'
    return {
        'base': final['color'],
        'hex': final['hex'],
        'stages': {
            '1_blood_gender': {'color': stage1_color, 'particle': particle1},
            '2_mbti_mid': {'color': stage2_color, 'particle': particle2},
            '3_mbti_ends': {'color': stage3_color, 'particle': particle3},
            '4_particle': particle_color,
        },
        'particles': [particle1, particle2, particle3],
        'leakage': leakage,
        'time_phase': time_phase,
    }

def compute_4layer_colors(profile_label, dims, time_phase='day', hour=12, s_val=None):
    """4 toroidal layers A/B/C/D — each computes profile_color with shifted blood type."""
    parts = profile_label.split('_')
    bt = parts[-1] if '_' in profile_label else 'O'
    bt_cycle = ['O', 'A', 'B', 'AB']
    bt_idx = bt_cycle.index(bt) if bt in bt_cycle else 0
    bt_shifted = bt_cycle[(bt_idx + 1) % 4]
    shifted_label = profile_label.rsplit('_', 1)[0] + '_' + bt_shifted
    base = compute_profile_color(profile_label, time_phase, s_val=s_val)
    shifted = compute_profile_color(shifted_label, time_phase, s_val=s_val)
    return {
        'A': {'layer': 'A', 'genotype': 'aa rh+', 'color': base['base'], 'hex': base['hex'], 'genre': 'RELEASE', 'leakage': base['leakage']},
        'B': {'layer': 'B', 'genotype': 'ao rh+', 'color': shifted['base'], 'hex': shifted['hex'], 'genre': 'STRESS_GROWTH', 'leakage': shifted['leakage']},
        'C': {'layer': 'C', 'genotype': 'aa rh-', 'color': base['base'], 'hex': base['hex'], 'genre': 'EXTREME_GROWTH', 'leakage': base['leakage']},
        'D': {'layer': 'D', 'genotype': 'ao rh-', 'color': shifted['base'], 'hex': shifted['hex'], 'genre': 'EXTREME_GROWTH', 'leakage': shifted['leakage']},
    }

# ============================================================
# 6-SLOT LEAKAGE → COLOR MAPPING
# Each leakage site's activity → all vectors of that activity sum to a color.
# This is the activity-to-color bridge: leakage slot color = Σ(activity_vectors).
# RED→deep pink shift at night: men RED→DEEP-PINK, women PINK→RED.
# ============================================================
LEAKAGE_SLOT_COLORS = {
    'mitochondria':    {'color': 'RED',    'hex': '#FF0000', 'activity': 'mitochondria_leakage_activity',     'vector_sum': 'all_vectors_of_activity'},
    'pancreas':        {'color': 'ORANGE', 'hex': '#FFA500', 'activity': 'pancreas_leakage_making_food',       'vector_sum': 'all_vectors_of_activity'},
    'electron_hole':   {'color': 'YELLOW', 'hex': '#FFFF00', 'activity': 'electron_hole_death_sensor_leakage', 'vector_sum': 'all_vectors_of_activity'},
    'gaba_c':          {'color': 'NAVY',   'hex': '#000080', 'activity': 'gaba_c_leakage_activity',            'vector_sum': 'all_vectors_of_activity'},
    'bilirubin':       {'color': 'GREEN',  'hex': '#00FF00', 'activity': 'bilirubin_eating_activity_weekend',  'vector_sum': 'all_vectors_of_activity'},
    'em_field':        {'color': 'PURPLE', 'hex': '#800080', 'activity': 'em_field_leakage_music_composition',  'vector_sum': 'all_vectors_of_activity'},
}

# Night RED→DEEP-PINK shift: structural transition, not just color value.
# Men: night RED → DEEP-PINK (tau particle, reverse direction blocked → forward only)
# Women: night PINK → RED (photon particle, forward path opened → RED activation)
# This is driven by oxidised_manganese(4th toe) reverse block + adapter_protein forward open.
NIGHT_COLOR_SHIFT = {
    'M': {'from': 'RED',      'to': 'DEEP-PINK', 'particle': 'tau',    'hex': '#FF1493',
          'mechanism': 'oxidised_manganese_reverse_block + adapter_protein_forward_open',
          'direction': 'forward_only'},
    'F': {'from': 'PINK',     'to': 'RED',       'particle': 'photon', 'hex': '#FF0000',
          'mechanism': 'adapter_protein_forward_open + cck_esr1_activation',
          'direction': 'forward_activation'},
}

def apply_night_color_shift(color_name, gender, time_phase):
    """Apply RED→DEEP-PINK (M) or PINK→RED (F) structural transition at night."""
    if time_phase != 'night':
        return color_name
    shift = NIGHT_COLOR_SHIFT.get(gender)
    if not shift:
        return color_name
    if color_name == shift['from']:
        return shift['to']
    # RED variants also shift for men at night
    if gender == 'M' and color_name in ('RED', 'RED-ORANGE'):
        return 'DEEP-PINK'
    if gender == 'F' and color_name in ('PINK', 'LIGHT-RED'):
        return 'RED'
    return color_name

# ============================================================
# DAY/NIGHT DIMENSION SHIFT RULES
# Blood type × gender → 8D dimension exchange at day transition.
# These are the formal mathematical rules for dimension swapping
# when switching from night to day personality.
# ============================================================
DAY_DIM_SHIFT = {
    ('A', 'F'):  {'r': 'nu',  's': 'nu'},   # A♀: r→nu, s→nu (sleep/flat_creation)
    ('A', 'M'):  {'d': 'h',   'r': 'd+p'},  # A♂: d→h, r→d+p (sleep)
    ('B', 'M'):  {'p': 'gamma', 'g': 'r'},  # B♂: p→gamma, g→r
    ('B', 'F'):  {'g': 'g',   'p': 'g'},    # B♀: g→g(maintain), p→g
    ('O', 'F'):  {'h': 's',   'nu': 'g'},   # O♀: h→s, nu→g
    ('O', 'M'):  {'gamma': 'h'},            # O♂: gamma→h
    ('AB', 'F'): {'d': 'p',   'h': 'gamma'},# AB♀: d→p, h→gamma
    ('AB', 'M'): {'gamma': 'r', 'd': 'p'},  # AB♂: gamma→r, d→p (go deep)
}

def apply_day_dim_shift(dims, blood_type, gender):
    """Apply day-time dimension shift for blood×gender profile.
    Returns new dims dict with shifted values. Non-destructive."""
    shift = DAY_DIM_SHIFT.get((blood_type, gender))
    if not shift:
        return dict(dims)
    result = dict(dims)
    for src, dst in shift.items():
        if src in result and dst in result:
            if dst == src:
                continue
            if '+' in dst:
                parts = dst.split('+')
                val = sum(result.get(p, 0.5) * (1.0/len(parts)) for p in parts)
                result[parts[0]] = clamp(val)
            else:
                result[dst] = result[src]
    return result

# ============================================================
# 7-LAYER HELIOSPHERE STRUCTURE (replaces 6-sphere)
# 7구체. 41입자. 4좌표계. 뇌 천체 매핑.
# From cosmic_body_structure.md: complete 7-layer model.
# ============================================================
HELIOSPHERE_7_LAYERS = {
    1: {'name': 'Sun',          'heliosphere': '태양_원천',     'brain_celestial': 'Leo',         'distance': '0 ly',       'particle': 'proton',     'dims': ['r', 's']},
    2: {'name': 'Solar_Wind',   'heliosphere': '태양풍',        'brain_celestial': 'Aquarius',    'distance': '1 AU ~5.96 ly','particle': 'photon',    'dims': ['gamma', 'h'],
        'sub_spheres': ['Sun→Earth→Moon→CoMag→Barnard']},
    3: {'name': 'Termination_Shock', 'heliosphere': '내부_Cavity', 'brain_celestial': 'Taurus',   'distance': '~80-90 AU',  'particle': 'z_boson',    'dims': ['p', 'nu']},
    4: {'name': 'Heliosheath',  'heliosphere': '6_Leakage_Sites','brain_celestial': 'Coma',       'distance': '~80-150 AU', 'particle': 'w_boson/gluon','dims': ['g', 'gamma']},
    5: {'name': 'Heliopause',   'heliosphere': '6th_sphere_Electron','brain_celestial': 'Virgo', 'distance': '~120-150 AU', 'particle': 'electron',   'dims': ['p↔r/d', 's']},
    6: {'name': 'Oort_Cloud',   'heliosphere': '138.88°_Spark',  'brain_celestial': 'Perseus',    'distance': '~2k-100k AU', 'particle': 'em_field_rebrancher', 'dims': ['nu', 'gamma']},
    7: {'name': 'Interstellar', 'heliosphere': '모델_외부_새순환','brain_celestial': 'Cassiopeia', 'distance': '>100k AU',   'particle': 'observer_E128','dims': ['all']},
}

# 6-sphere astronomical distances (from prose.txt:8320-8339)
SIX_SPHERE_DISTANCES = {
    'Sun':         {'distance': '1 AU (0 ly)',  'time': '0-3h',   'particle': 'proton',       'dims': ['r', 's']},
    'Earth':       {'distance': '384,400 km',   'time': '3-9h',   'particle': 'photon',       'dims': ['gamma', 'h']},
    'Moon':        {'distance': '~330 ly',      'time': '9-15h',  'particle': 'z_boson',      'dims': ['p', 'nu']},
    'CoMag':       {'distance': '~325 ly',      'time': '15-21h', 'particle': 'w_boson/gluon','dims': ['g', 'gamma']},
    'Barnard':     {'distance': '5.96 ly',      'time': '21-3h',  'particle': 'quark/higgs',  'dims': ['g', 'd']},
    'Geomagnetic': {'distance': '∞ (closure)',  'time': 'time_external', 'particle': 'electron/neutrino', 'dims': ['p↔r/d', 's']},
}

# ============================================================
# METHANOGENESIS 12H RESONANCE
# right_rib_personal: day methanogenesis activation → 12h phase → night female creativity.
# Day: p-dim trigger activates methanogenesis at right_ribs.
# Night: 12h later, resonance enhances female creativity (cck_mod + esr1_mod).
# ============================================================
METHANOGENESIS_RESONANCE = {
    'day_activation': {
        'site': 'right_rib_personal',
        'dim_trigger': 'p',
        'particle': 'higgs',
        'mechanism': 'methanogenesis_mass_gate',
        'time_window': 'day (9-15h)',
    },
    'night_resonance': {
        'phase_shift_hours': 12,
        'target': 'female_creativity',
        'mechanism': 'cck_mod + esr1_mod amplification',
        'condition': 'gender==F and mbti[0]==E',
        'time_window': 'night (21-3h)',
    },
}

def compute_methanogenesis_resonance(dims, time_phase, gender, mbti, hour):
    """Compute methanogenesis 12h resonance effect.
    Day: p-dim activates methanogenesis. Night: 12h resonance amplifies female creativity."""
    p_val = dims.get('p', 0.5)
    if time_phase == 'day' and p_val > 0.3:
        day_active = True
        night_resonance = 0.0
    elif time_phase == 'night':
        day_active = False
        if gender == 'F' and mbti[0] == 'E':
            night_resonance = clamp(p_val * 0.3)
        else:
            night_resonance = clamp(p_val * 0.1)
    else:
        day_active = False
        night_resonance = 0.0
    return {
        'day_active': day_active,
        'night_resonance': night_resonance,
        'phase_shift': 12,
        'site': 'right_rib_personal',
    }

# ============================================================
# ADDICTION / HEALING FRAMEWORK
# Alcohol, drug, tobacco = leakage pathologies where specific leakage slots
# are forced open or blocked, preventing normal closure.
# Healing = restoring forward-only flow (leakage=0).
# ============================================================
ADDICTION_PATHOLOGIES = {
    'alcohol': {
        'affected_slot': 'gaba_c',
        'slot_color': 'NAVY',
        'mechanism': 'GABA-A receptor flooding → night_reverse_blocked fails → oxidised_manganese reverse leakage unblocked',
        'leakage_effect': 'left_foot_outer_edge reverse path opens at night → energy drain → universe not closed',
        'dim_effect': {'g': -0.15, 'nu': -0.10, 's': -0.08, 'd': +0.12},
        'healing': 'restore forward-only: adapter_protein forward path + oxidised_manganese block',
    },
    'tobacco': {
        'affected_slot': 'mitochondria',
        'slot_color': 'RED',
        'mechanism': 'nicotine → proton_pump overdrive → mitochondria leakage RED amplified → RED cannot transition to DEEP-PINK at night',
        'leakage_effect': 'men stuck in RED at night (no DEEP-PINK shift) → forward path never opens → no closure',
        'dim_effect': {'r': +0.15, 'h': -0.10, 'gamma': -0.08, 'nu': -0.05},
        'healing': 'restore RED→DEEP-PINK night shift by clearing nicotine from proton_pump',
    },
    'drug_opioid': {
        'affected_slot': 'electron_hole',
        'slot_color': 'YELLOW',
        'mechanism': 'opioid receptor → electron_hole death sensor bypassed → YELLOW leakage uncontrolled',
        'leakage_effect': 'pain_eliminate path short-circuited → no death sensor → no 3AM reset → no Betti 12 closure',
        'dim_effect': {'d': -0.20, 'p': -0.10, 's': -0.12, 'nu': +0.08},
        'healing': 'restore electron_hole death sensor → re-enable 3AM hysteresis → Betti 12 closure',
    },
    'drug_stimulant': {
        'affected_slot': 'pancreas',
        'slot_color': 'ORANGE',
        'mechanism': 'dopamine flood → pancreas leakage ORANGE amplified → eating/making activity vector distorted',
        'leakage_effect': 'ORANGE overproduction → color balance broken → 4-channel closure fails (no BLACK)',
        'dim_effect': {'r': +0.20, 'p': -0.15, 'h': +0.10, 'gamma': +0.08},
        'healing': 'restore pancreas ORANGE balance → re-enable 4-channel additive closure',
    },
}

def compute_addiction_impact(dims, addiction_type=None):
    """Compute how addiction affects 8D dims and leakage closure.
    If addiction_type is specified, returns the specific pathology.
    Otherwise returns general framework info."""
    if addiction_type and addiction_type in ADDICTION_PATHOLOGIES:
        pathology = ADDICTION_PATHOLOGIES[addiction_type]
        modified_dims = dict(dims)
        for k, v in pathology['dim_effect'].items():
            modified_dims[k] = clamp(modified_dims.get(k, 0.5) + v)
        return {
            'addiction_type': addiction_type,
            'affected_slot': pathology['affected_slot'],
            'slot_color': pathology['slot_color'],
            'mechanism': pathology['mechanism'],
            'leakage_effect': pathology['leakage_effect'],
            'modified_dims': modified_dims,
            'dim_delta': pathology['dim_effect'],
            'healing': pathology['healing'],
            'closure_broken': True,
        }
    return {
        'addiction_types': list(ADDICTION_PATHOLOGIES.keys()),
        'framework': 'addiction = forced leakage slot open/blocked → prevents closure → universe not eternal',
        'healing_principle': 'restore forward-only flow → leakage=0 → universe eternal',
    }

# ============================================================
# CREATIVE 4-SHAPES CSV LOADER (from creative_4shapes_v3.csv)
# ============================================================
CREATIVE_4SHAPES_CSV = {}
_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "creative_4shapes_v3.csv")
if os.path.exists(_CSV_PATH):
    with open(_CSV_PATH, "r", encoding="utf-8") as _f:
        _reader = csv.DictReader(_f)
        for _row in _reader:
            _prof = _row.get("profile", _row.get("element", ""))
            if _prof:
                CREATIVE_4SHAPES_CSV[_prof] = {
                    "shape1": _row.get("shape1", ""),
                    "shape1_music": _row.get("shape1_music", ""),
                    "shape1_tech": _row.get("shape1_tech", ""),
                    "shape1_sport": _row.get("shape1_sport", ""),
                    "shape1_shape": _row.get("shape1_shape", ""),
                    "shape2": _row.get("shape2", ""),
                    "shape2_music": _row.get("shape2_music", ""),
                    "shape2_tech": _row.get("shape2_tech", ""),
                    "shape2_sport": _row.get("shape2_sport", ""),
                    "shape2_shape": _row.get("shape2_shape", ""),
                    "shape3": _row.get("shape3", ""),
                    "shape3_music": _row.get("shape3_music", ""),
                    "shape3_tech": _row.get("shape3_tech", ""),
                    "shape3_sport": _row.get("shape3_sport", ""),
                    "shape3_shape": _row.get("shape3_shape", ""),
                    "shape4": _row.get("shape4", ""),
                    "shape4_music": _row.get("shape4_music", ""),
                    "shape4_tech": _row.get("shape4_tech", ""),
                    "shape4_sport": _row.get("shape4_sport", ""),
                    "shape4_shape": _row.get("shape4_shape", ""),
                }

# ============================================================
# DYNAMIC GEOMAG CYCLE (outer_core_convection time-aware modulation)
# ============================================================
GEOMAG_CYCLE_NODES = [
    "ferritin", "magnetite", "sulfur_iron_complex", "pyrite",
    "laterite", "fold_belt", "subduction_zone", "lower_mantle",
    "plume", "outer_core_convection",
]

def compute_geomag_phase(time_phase, hour=12):
    """Compute which geomag cycle node is active based on time."""
    if time_phase == "day":
        idx = int((hour % 12) / 12 * len(GEOMAG_CYCLE_NODES))
    else:
        idx = int(((hour + 12) % 24) / 24 * len(GEOMAG_CYCLE_NODES))
    active_node = GEOMAG_CYCLE_NODES[idx % len(GEOMAG_CYCLE_NODES)]
    # Phase-specific dim effects
    phase_effects = {
        "ferritin":             {"r": -0.01, "g": +0.02, "s": -0.005},
        "magnetite":            {"r": -0.02, "g": +0.03, "gamma": +0.02, "s": -0.01},
        "sulfur_iron_complex":  {"d": +0.01, "g": +0.02, "gamma": +0.01},
        "pyrite":               {"d": +0.02, "g": +0.01, "s": -0.01},
        "laterite":             {"r": -0.01, "nu": +0.02, "g": +0.01},
        "fold_belt":            {"gamma": +0.03, "g": +0.02, "d": -0.01},
        "subduction_zone":      {"d": +0.03, "g": +0.01, "nu": -0.01},
        "lower_mantle":         {"nu": +0.03, "g": +0.02, "gamma": +0.01},
        "plume":                {"r": +0.02, "nu": +0.02, "gamma": +0.03},
        "outer_core_convection":{"r": -0.02, "g": +0.03, "gamma": +0.02, "s": -0.01},
    }
    return {"active_node": active_node, "phase_idx": idx, "effects": phase_effects.get(active_node, {})}

# ============================================================
# 118 ELEMENTS — toroidal cycle order AB→A→O→B
# ============================================================
ELEMENTS_118 = [
    [1,"H","ENFP_M_O","hyperpop","AMBIENT","neo-classical"],
    [2,"He","ISFP_F_A","shoegaze","BRITPOP","ghibli"],
    [3,"Li","ESFJ_M_A","folk","DRONE","strings"],
    [4,"Be","INTP_M_A","PIANO","HANS ZIMMER","minimalistic"],
    [5,"B","ENTP_F_A","IDM","DRONE","electronic experimental"],
    [6,"C","ESTP_M_O","INDIE FOLK","folk","BRITPOP"],
    [7,"N","INTP_M_AB","neo-classical","strings","DRONE"],
    [8,"O","ISTP_M_A","dark ambient","dream pop","noise"],
    [9,"F","ESTJ_F_AB","INDIE FOLK","dream pop","BRITPOP"],
    [10,"Ne","ENFP_F_A","witch house","neo-classical","deconstructed club"],
    [11,"Na","INFJ_F_A","neo-classical","witch house","hauntology"],
    [12,"Mg","ESFP_M_B","deconstructed club","noise","IDM"],
    [13,"Al","ESFP_M_O","hyperpop","DRONE","dream pop"],
    [14,"Si","ISTP_M_O","DRONE","hyperpop","dark ambient"],
    [15,"P","ISTP_M_B","noise","deconstructed club","power electronics"],
    [16,"S","INFJ_F_B","hauntology","deconstructed club","Boards of Canada"],
    [17,"Cl","ESTJ_M_B","noise","shoegaze","INDIE FOLK"],
    [18,"Ar","ENFJ_M_O","CINEMATIC","dream pop","HANS ZIMMER"],
    [19,"K","ENFJ_F_B","orchestral","hauntology","strings"],
    [20,"Ca","ENTJ_M_O","noise","DRONE","dark ambient"],
    [21,"Sc","ENFP_M_A","witch house","neo-classical","deconstructed club"],
    [22,"Ti","ESTJ_F_A","INDIE FOLK","shoegaze","noise"],
    [23,"V","ESFP_M_AB","IDM","power electronics","hyperpop"],
    [24,"Cr","ENFP_F_B","deconstructed club","hauntology","IDM"],
    [25,"Mn","INFJ_M_AB","Boards of Canada","IDM","AMBIENT"],
    [26,"Fe","ISTJ_F_A","DRONE","folk","noise"],
    [27,"Co","ENTJ_F_AB","noise","neo-classical","noise"],
    [28,"Ni","ESFJ_F_A","folk","DRONE","strings"],
    [29,"Cu","ESTJ_M_O","BRITPOP","dream pop","INDIE FOLK"],
    [30,"Zn","ENFP_F_AB","IDM","Boards of Canada","hyperpop"],
    [31,"Ga","ISTJ_F_B","noise","strings","DRONE"],
    [32,"Ge","ESTJ_M_AB","INDIE FOLK","dream pop","BRITPOP"],
    [33,"As","ESTP_F_O","INDIE FOLK","folk","BRITPOP"],
    [34,"Se","ISTJ_F_O","minimalistic","orchestral","DRONE"],
    [35,"Br","ISTJ_M_A","DRONE","folk","noise"],
    [36,"Kr","ISFJ_F_AB","AMBIENT","INDIE FOLK","folk"],
    [37,"Rb","INFJ_M_A","neo-classical","witch house","hauntology"],
    [38,"Sr","ENTJ_M_A","dark ambient","PIANO","power electronics"],
    [39,"Y","ENTJ_M_AB","noise","neo-classical","noise"],
    [40,"Zr","ENFP_F_O","hauntology","deconstructed club","Boards of Canada"],
    [41,"Nb","INTP_F_O","DRONE","CINEMATIC","PIANO"],
    [42,"Mo","ISTJ_F_AB","DRONE","orchestral","minimalistic"],
    [43,"Tc","INTP_F_AB","neo-classical","strings","DRONE"],
    [44,"Ru","INFP_M_B","hauntology","power electronics","shoegaze"],
    [45,"Rh","ISFJ_M_AB","AMBIENT","INDIE FOLK","folk"],
    [46,"Pd","INTJ_F_O","dark ambient","deconstructed club","DRONE"],
    [47,"Ag","ESFP_M_A","dream pop","dark ambient","deconstructed club"],
    [48,"Cd","ESFP_F_B","deconstructed club","noise","IDM"],
    [49,"In","ESFP_F_O","hyperpop","DRONE","dream pop"],
    [50,"Sn","ENFJ_M_AB","CINEMATIC","strings","Boards of Canada"],
    [51,"Sb","ESFP_F_AB","IDM","power electronics","hyperpop"],
    [52,"Te","ENFJ_F_AB","strings","Boards of Canada","CINEMATIC"],
    [53,"I","ISFP_M_AB","dream pop","INDIE FOLK","shoegaze"],
    [54,"Xe","ESFJ_F_B","strings","noise","CINEMATIC"],
    [55,"Cs","ENFJ_M_A","HANS ZIMMER","neo-classical","orchestral"],
    [56,"Ba","INTJ_M_A","DRONE","IDM","post-rock"],
    [57,"La","ISFP_M_O","dream pop","BRITPOP","shoegaze"],
    [58,"Ce","INFP_M_A","Boards of Canada","noise","hauntology"],
    [59,"Pr","ENTJ_M_B","power electronics","minimalistic","noise"],
    [60,"Nd","ESTP_M_B","noise","avant-garde","INDIE FOLK"],
    [61,"Pm","INTJ_F_A","DRONE","IDM","post-rock"],
    [62,"Sm","ESTP_F_AB","INDIE FOLK","AMBIENT","BRITPOP"],
    [63,"Eu","INTP_M_B","minimalistic","orchestral","neo-classical"],
    [64,"Gd","ENFJ_M_B","orchestral","hauntology","strings"],
    [65,"Tb","ENFP_M_B","deconstructed club","hauntology","IDM"],
    [66,"Dy","INTJ_F_AB","dark ambient","hyperpop","dark ambient"],
    [67,"Ho","ENTP_F_B","electronic experimental","post-rock","hyperpop"],
    [68,"Er","ESTJ_F_B","noise","ghibli","INDIE FOLK"],
    [69,"Tm","ESTP_F_A","BRITPOP","AMBIENT","noise"],
    [70,"Yb","ESFJ_M_O","orchestral","minimalistic","folk"],
    [71,"Lu","INFP_M_AB","shoegaze","noise","dream pop"],
    [72,"Hf","ISFJ_F_A","AMBIENT","INDIE FOLK","avant-garde"],
    [73,"Ta","ESFP_F_A","dream pop","dark ambient","deconstructed club"],
    [74,"W","ISTP_F_B","noise","deconstructed club","power electronics"],
    [75,"Re","INTJ_M_AB","dark ambient","hyperpop","dark ambient"],
    [76,"Os","ENFJ_F_O","CINEMATIC","dream pop","HANS ZIMMER"],
    [77,"Ir","INTP_F_A","PIANO","HANS ZIMMER","minimalistic"],
    [78,"Pt","ESFJ_F_AB","CINEMATIC","DRONE","orchestral"],
    [79,"Au","ISFJ_F_B","avant-garde","noise","AMBIENT"],
    [80,"Hg","INFJ_F_O","AMBIENT","hyperpop","neo-classical"],
    [81,"Tl","ISFJ_M_B","avant-garde","noise","AMBIENT"],
    [82,"Pb","ENFJ_F_A","HANS ZIMMER","neo-classical","orchestral"],
    [83,"Bi","ISTP_F_O","DRONE","hyperpop","dark ambient"],
    [84,"Po","ESTP_F_B","noise","avant-garde","INDIE FOLK"],
    [85,"At","ISTJ_M_B","noise","strings","DRONE"],
    [86,"Rn","ENTP_M_A","4AD shoegaze","autechre","big beat"],
    [87,"Fr","INFJ_M_O","AMBIENT","hyperpop","neo-classical"],
    [88,"Ra","INTJ_M_B","post-rock","electronic experimental","dark ambient"],
    [89,"Ac","INTP_M_O","DRONE","CINEMATIC","PIANO"],
    [90,"Th","ESTP_M_A","BRITPOP","AMBIENT","noise"],
    [91,"Pa","INFP_F_B","hauntology","power electronics","shoegaze"],
    [92,"U","ISTP_F_AB","power electronics","IDM","DRONE"],
    [93,"Np","ISFP_F_AB","dream pop","INDIE FOLK","shoegaze"],
    [94,"Pu","ISFP_M_A","shoegaze","INDIE FOLK","ghibli"],
    [95,"Am","INFP_F_AB","shoegaze","noise","dream pop"],
    [96,"Cm","ISFP_F_B","ghibli","noise","dream pop"],
    [97,"Bk","ISTJ_M_O","minimalistic","orchestral","DRONE"],
    [98,"Cf","ENTP_F_O","deconstructed club","dark ambient","IDM"],
    [99,"Es","ESFJ_F_O","orchestral","minimalistic","folk"],
    [100,"Fm","INTP_F_B","minimalistic","orchestral","neo-classical"],
    [101,"Md","ENFP_M_AB","IDM","Boards of Canada","hyperpop"],
    [102,"No","ISFJ_F_O","folk","INDIE FOLK","AMBIENT"],
    [103,"Lr","ESTP_M_AB","INDIE FOLK","AMBIENT","BRITPOP"],
    [104,"Rf","ENTP_M_AB","hyperpop","dark ambient","deconstructed club"],
    [105,"Db","ENTJ_F_O","noise","DRONE","dark ambient"],
    [106,"Sg","INFP_M_O","dream pop","noise","Boards of Canada"],
    [107,"Bh","ISFP_F_O","dream pop","BRITPOP","shoegaze"],
    [108,"Hs","ISTP_F_A","dark ambient","dream pop","noise"],
    [109,"Mt","ISTJ_M_AB","DRONE","orchestral","minimalistic"],
    [110,"Ds","ENTJ_F_A","dark ambient","PIANO","power electronics"],
    [111,"Rg","ENTP_F_AB","hyperpop","dark ambient","deconstructed club"],
    [112,"Cn","ISTP_M_AB","power electronics","IDM","DRONE"],
    [113,"Nh","INFJ_F_AB","Boards of Canada","IDM","AMBIENT"],
    [114,"Fl","ISFP_M_B","ghibli","noise","dream pop"],
    [115,"Mc","ISFJ_M_O","folk","INDIE FOLK","AMBIENT"],
    [116,"Lv","ENTJ_F_B","power electronics","minimalistic","noise"],
    [117,"Ts","ISFJ_M_A","AMBIENT","INDIE FOLK","avant-garde"],
    [118,"Og","INTJ_F_B","post-rock","electronic experimental","dark ambient"],
    [119,"Uue","ENTP_M_O","IDM","DRONE","electronic experimental"],
    [120,"Ubn","ENTP_M_B","hyperpop","dark ambient","deconstructed club"],
    [121,"Ubu","ESFJ_M_AB","orchestral","minimalistic","folk"],
    [122,"Ubb","ESFJ_M_B","folk","DRONE","strings"],
    [123,"Ubt","ESTJ_F_O","INDIE FOLK","shoegaze","noise"],
    [124,"Ubq","ESTJ_M_A","BRITPOP","dream pop","INDIE FOLK"],
    [125,"Ubp","INFJ_M_B","hauntology","deconstructed club","Boards of Canada"],
    [126,"Ubh","INFP_F_A","shoegaze","noise","dream pop"],
    [127,"Ubs","INFP_F_O","dream pop","noise","Boards of Canada"],
    [128,"Ubo","INTJ_M_O","dark ambient","hyperpop","dark ambient"],
]

ELEMENT_MAP = {}
for num, sym, ptype, release, stress, extreme in ELEMENTS_118:
    ELEMENT_MAP[ptype] = {"number": num, "symbol": sym, "release": release, "stress_growth": stress, "extreme_growth": extreme}

# ============================================================
# TOROIDAL TIME SLOTS — AB(0-3h)→A(3-9h)→O(9-15h)→B(15-21h)
# ============================================================
TOROIDAL_SLOTS = [
    {"blood_type": "AB", "hours": (0, 3),   "genre_type": "RELEASE",        "label": "release"},
    {"blood_type": "A",  "hours": (3, 9),   "genre_type": "STRESS_GROWTH",  "label": "stress_growth"},
    {"blood_type": "O",  "hours": (9, 15),  "genre_type": "PRESENT_MOMENT", "label": "present_moment"},
    {"blood_type": "B",  "hours": (15, 21), "genre_type": "EXTREME_GROWTH", "label": "extreme_growth"},
]

def get_toroidal_slot(hour):
    for slot in TOROIDAL_SLOTS:
        if slot["hours"][0] <= hour < slot["hours"][1]:
            return slot
    return TOROIDAL_SLOTS[0]

# ============================================================
# 16 WINDOWS (t mod 16) — peak dimension shift per window
# ============================================================
LAYER_NAMES = ["body", "observer", "bridge", "dark"]

# v4 16-window peak cycle — peak dimension + peak particle per window
# Windows 0-7 and 8-15 share the same dimension order (r,h,d,p,s,gamma,g,nu)
# but window 2 peaks via tau while window 10 peaks via z_boson (both = d dimension)
DIM_PEAK_SHIFT = {
    0:  "r",      # neutrino
    1:  "h",      # gluon
    2:  "d",      # tau
    3:  "p",      # higgs
    4:  "s",      # quark
    5:  "gamma",  # photon
    6:  "g",      # muon
    7:  "nu",     # w_boson
    8:  "r",      # neutrino (repeat)
    9:  "h",      # gluon (repeat)
    10: "d",      # z_boson (tau→z_boson swap at window 10)
    11: "p",      # higgs (repeat)
    12: "s",      # quark (repeat)
    13: "gamma",  # photon (repeat)
    14: "g",      # muon (repeat)
    15: "nu",     # w_boson (repeat)
}

# Peak particle per window (v4 explicit)
DIM_PEAK_PARTICLE = {
    0:  "neutrino",
    1:  "gluon",
    2:  "tau",
    3:  "higgs",
    4:  "quark",
    5:  "photon",
    6:  "muon",
    7:  "w_boson",
    8:  "neutrino",
    9:  "gluon",
    10: "z_boson",
    11: "higgs",
    12: "quark",
    13: "photon",
    14: "muon",
    15: "w_boson",
}

def mulberry32(seed):
    a = seed & 0xFFFFFFFF
    def _rng():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = (t ^ (t >> 15)) * (t | 1) & 0xFFFFFFFF
        t ^= (t + ((t ^ (t >> 7)) * (t | 61) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0
    return _rng

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def apply_16window_shift(dims, t_index, jitter_pct=0.20, seed_val=0):
    peak_dim = DIM_PEAK_SHIFT[t_index % 16]
    rng = mulberry32(seed_val + t_index)
    jitter = 1.0 + (rng() * 2 - 1) * jitter_pct
    if peak_dim in dims:
        dims[peak_dim] = clamp(dims[peak_dim] * jitter)
    return dims

def compute_4layers(base_dims, t_index, seed_val=0):
    layers = {}
    for i, layer_name in enumerate(LAYER_NAMES):
        layer_dims = dict(base_dims)
        layers[layer_name] = apply_16window_shift(layer_dims, t_index + i * 4, 0.20, seed_val)
    return layers

# ============================================================
# UNIVERSE CYCLE (toroidal chirality extrapolation)
# ============================================================
def rotate_complex(z, angle_rad):
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return {"real": c * z["real"] - s * z["imag"], "imag": s * z["real"] + c * z["imag"]}

def run_cycle(theta, levels=48):
    delta = DELTA_T_OBS_DERIVED
    kappa = OMEGA_KAPPA
    rho = math.sqrt(delta * delta + kappa * kappa)
    u = {"real": rho * math.cos(theta), "imag": rho * math.sin(theta)}
    total_gap = 0.0
    total_lensing = 0.0
    total_visible = 0.0
    for level in range(1, levels + 1):
        phi_scale = PHI ** (-(level - 1))
        c_level = {"real": delta * phi_scale, "imag": kappa * phi_scale}
        raw = {
            "real": u["real"] * u["real"] - u["imag"] * u["imag"] + c_level["real"],
            "imag": 2 * u["real"] * u["imag"] + c_level["imag"],
        }
        cw = rotate_complex(raw, SPARK_ANGLE_RAD)
        ccw = rotate_complex(raw, -SPARK_ANGLE_RAD)
        total_gap += abs(cw["imag"] - ccw["imag"])
        src_norm = math.sqrt(raw["real"] ** 2 + raw["imag"] ** 2)
        if src_norm > 1e-12:
            radial = (raw["real"] * cw["real"] + raw["imag"] * cw["imag"]) / (src_norm * src_norm)
            trans = (raw["real"] * cw["imag"] - raw["imag"] * cw["real"]) / (src_norm * src_norm)
            total_lensing += max(0, -radial) * src_norm
            total_visible += abs(trans) * src_norm
        u = {"real": 0.5 * (cw["real"] + ccw["real"]), "imag": 0.5 * (cw["imag"] + ccw["imag"])}
        u_norm = math.sqrt(u["real"] ** 2 + u["imag"] ** 2)
        if u_norm > 1e-12:
            u["real"] *= rho / u_norm
            u["imag"] *= rho / u_norm
    next_theta = math.atan2(u["imag"], u["real"])
    total_mass = total_gap + total_lensing + total_visible
    chirality = total_gap / max(total_mass, 1e-12)
    hidden = total_lensing / max(total_lensing + total_visible, 1e-12)
    return {"start_theta": theta, "end_theta": next_theta, "chirality_ratio": chirality, "hidden_ratio": hidden}

def compute_universe_cycle(dims, cycles=8):
    theta0 = math.atan2(dims["gamma"] - dims["d"], dims["r"] - dims["h"])
    current = run_cycle(theta0)
    theta = current["end_theta"]
    future = []
    for i in range(cycles):
        row = run_cycle(theta)
        future.append({
            "cycle": i + 1,
            "chirality": round(row["chirality_ratio"], 6),
            "hidden": round(row["hidden_ratio"], 6),
            "theta": round(row["end_theta"], 6),
        })
        theta = row["end_theta"]
    return {
        "current_chirality": round(current["chirality_ratio"], 6),
        "current_hidden": round(current["hidden_ratio"], 6),
        "future_cycles": future,
    }

# ============================================================
# 6 ATTRACTORS — from prose.txt
# ============================================================
ATTRACTORS = {
    "energy": {"particles": ["proton", "gluon", "w_boson"], "weak": ["ISTJ", "ESTJ", "ISFJ", "ESFJ"], "blood": "O"},
    "information": {"particles": ["neutrino", "quark", "photon"], "weak": ["INFP", "ENFP", "INFJ", "ENFJ"], "blood": "AB"},
    "repair": {"particles": ["tau", "gluon", "w_boson"], "weak": ["INTP", "ENTP", "INTJ", "ENTJ", "ISTP", "ESTP", "ISFP", "ESFP"], "blood": "B"},
    "opioid_landau": {"particles": ["muon", "electron", "photon"], "weak": ["ISFP", "ESFP", "ISTP", "ESTP"], "blood": "A"},
    "gan_bulkhead": {"particles": ["gluon", "higgs", "z_boson"], "weak": ["INTJ", "ENTJ", "INFJ", "ENFJ"], "blood": "AB"},
    "cox_retrograde": {"particles": ["electron", "neutrino", "photon"], "weak": "all", "blood": "all"},
}

# ============================================================
# 6-SPHERE PHASES — from prose.txt
# ============================================================
SIX_SPHERE_PHASES = {
    "proton":  {"phase": 1, "flow": "Sun→Earth",  "meaning": "정보 점화 = 빅뱅 = H→O 스파크"},
    "photon":  {"phase": 2, "flow": "Earth→Moon", "meaning": "수리 축적 = O2 광합성 = 빛→시간"},
    "z_boson": {"phase": 3, "flow": "Moon→CoMag", "meaning": "시간→결합 전환 = 약력 붕괴"},
    "w_boson": {"phase": 4, "flow": "CoMag→Barnard", "meaning": "결합→질량 압축 = 약력 붕괴"},
    "gluon":   {"phase": 4, "flow": "CoMag→Barnard", "meaning": "결합 에너지 = 강력 = 결합 밀도"},
    "quark":   {"phase": 5, "flow": "Barnard→Sun",   "meaning": "질량→정보 충전 = 질량 결착"},
    "higgs":   {"phase": 5, "flow": "Barnard→Sun",   "meaning": "질량 부여 = 질량 생성 = 저장→정보"},
}

# ============================================================
# SPATIAL STRUCTURE — bypass/separatrix/observer_singularity
# ============================================================
SPATIAL_NODES = {
    "left_bypass":      {"x": 2.0,  "role": "외곽 여성 수면/우회로, Big Woman, 확장"},
    "right_bypass":     {"x": 14.0, "role": "외곽 남성 수면/우회로, Big Man, 확장"},
    "center_funnel":    {"x": 8.0,  "role": "내향 3/32 darkness gate 스파크 수렴 깔때기"},
    "separatrix_1":     {"x": 5.0,  "role": "중간 성격 분기 경계선 1"},
    "separatrix_2":     {"x": 11.0, "role": "중간 성격 분기 경계선 2"},
    "observer_singularity": {"x": None, "role": "내부 5노드 2D 그리드를 3D 토러스로 폐쇄하는 전자기 특이점"},
}

WAVELENGTH_6 = 6  # separatrix_2 - separatrix_1
OBSERVER_CLOSURE_TENSION = (9 * math.pi) / (20 * math.sqrt(2))  # ≈ 1.000042
OBSERVER_CLOSURE_RESIDUAL = 3.51e-4  # 비가역적 잔여 Δ
DARKNESS_GATE = 3.0 / 32.0  # κ₃/₃₂ = 0.09375

# Maxwell Cavity
MAXWELL_R_MAJOR = 17.0 / 8.0  # = 2.125
MAXWELL_Q_FACTOR = 11.8

# Barnard Distance
BARNARD_DISTANCE = (SPARK_ANGLE_DEG + 28) / 28  # ≈ 5.96 ly

# ============================================================
# RAW PARTICLE → DIMENSION WEIGHTS
# ============================================================
PARTICLE_DIM_WEIGHTS = {
    # 8 base particles (v4 mapping):
    # r=neutrino, h=gluon, d=tau/z_boson, p=higgs,
    # s=quark, gamma=photon, g=muon, nu=w_boson
    "neutrino":  {"r": 1},
    "gluon":     {"h": 1},
    "tau":       {"d": 1},
    "z_boson":   {"d": 1},
    "higgs":     {"p": 1},
    "quark":     {"s": 1},
    "photon":    {"gamma": 1},
    "muon":      {"g": 1},
    "w_boson":   {"nu": 1},
    # derivatives of base particles (v4):
    "proton":    {"r": 0.6, "p": 0.4},       # neutrino ignition + higgs convergence
    "electron":  {"gamma": 0.5, "s": 0.5},   # photon derivative (skull lipid bilayer)
    "em_field":  {"gamma": 0.5, "nu": 0.5},  # photon∩w_boson at vertex (138.88° spark)
    "graviton":  {"d": 0.5, "nu": 0.5},      # higgs derivative (ferritin iliac void mass)
    # 6 quark flavors — quark base = s, flavors split per v4
    "up_quark":       {"r": 0.5, "p": 0.5},      # V1 calcarine myosin S1 — r/p active force
    "down_quark":     {"h": 1},                   # V2 F-actin 7nm — h passive rail
    "charm_quark":    {"h": 0.5, "g": 0.5},      # V2 NMDA 14nm — h/g color edge binding
    "strange_quark":  {"d": 0.5, "nu": 0.5},     # left insula — d/nu novelty detection
    "top_quark":      {"r": 0.5, "nu": 0.5},     # hepatocyte NPC — r/nu high-energy transport
    "bottom_quark":   {"d": 0.5, "nu": 0.5},     # sigmoid colon — d/nu apoptosis/decay
    # 6 neutrino variants — neutrino base = r, variants split per v4
    "electron_neutrino":      {"r": 0.6, "s": 0.4},      # O2/GABA synthesis
    "electron_antineutrino":  {"r": 0.5, "gamma": 0.5},  # night spark reward
    "muon_neutrino":          {"r": 0.4, "g": 0.6},      # day fatigue storage (cytochrome 640)
    "muon_antineutrino":      {"r": 0.4, "d": 0.6},      # night cosmic repair
    "tau_neutrino":           {"r": 0.3, "d": 0.7},      # night hypoxia/mass-gate monitor
    "tau_antineutrino":       {"r": 0.4, "p": 0.6},      # day autophagy/cleansing
    # compact + dark
    "neutron":       {"nu": 0.5, "d": 0.5},
    "neutron_star":  {"g": 0.6, "nu": 0.4},
    "dark_matter":   {"d": 0.6, "nu": 0.4},   # foam cell — d/nu noise residue
    "dark_energy":   {"nu": 0.6, "gamma": 0.4}, # nucleus/crypt — nu/gamma time-axis
    # scalars
    "time":    {"r": 0.5, "nu": 0.5},
    "energy":  {"r": 0.6, "p": 0.4},
    # buses / hormones / cofactors
    "ego_d2":            {"p": 0.6, "s": 0.4},
    "left_progesterone": {"gamma": 0.5, "h": 0.5},   # right eye 3D — gamma/h
    "right_testosterone":{"r": 0.5, "p": 0.5},
    "acetyl_coa":        {"s": 0.3, "d": 0.4, "p": 0.3}, # mitochondria PDH — s/d/p memory mass
    # derived / observer-specific
    "spark":            {"gamma": 0.5, "nu": 0.5},    # vertex 138.88° — gamma/nu
    "clathrate_buffer": {"g": 0.5, "p": 0.5},
    "em_field_rebrancher": {"gamma": 0.4, "nu": 0.6}, # vertex rebranching — gamma/nu
    "testosterone_sex": {"r": 0.4, "p": 0.6},
    "endorphin_imag":   {"d": 0.4, "nu": 0.6},        # MOR 4nm — d/nu pleasure seal
    "male_gaba_a_wk":   {"d": 0.5, "gamma": 0.5},     # left occipitalis hypoxia — d/gamma
    "pain_eliminate":   {"d": 0.4, "nu": 0.6},        # substance P NK1R — d/nu
}

# ============================================================
# NEUTRINO VARIANTS
# ============================================================
NEUTRINO_VARIANTS = {
    "electron_neutrino":     {"time": "day",   "brain_compartment": 1, "body_quadrant": "left_upper",  "property": "oxygen"},
    "electron_antineutrino": {"time": "night", "brain_compartment": 4, "body_quadrant": "right_lower", "property": "water_vapour"},
    "muon_neutrino":         {"time": "day",   "brain_compartment": 2, "body_quadrant": "left_lower",  "property": "magnetic_directional"},
    "muon_antineutrino":     {"time": "night", "brain_compartment": 2, "body_quadrant": "left_lower",  "property": "cosmic_ray_penetration"},
    "tau_neutrino":          {"time": "night", "brain_compartment": 3, "body_quadrant": "right_upper", "property": "mass_anchor"},
    "tau_antineutrino":      {"time": "day",   "brain_compartment": 3, "body_quadrant": "left_upper",  "property": "substance_p_pain"},
}

# ============================================================
# 4 BRAIN COMPARTMENTS
# ============================================================
BRAIN_COMPARTMENTS = {
    1: {"name": "compartment_1", "body_quadrant": "left_upper",
        "outlet": {"node": "PLP_core", "particle": "electron_neutrino", "property": "oxygen"},
        "inlet":  {"node": "spare_vasopressin", "particle": "electron"},
        "neutrino_variants": ["electron_neutrino", "tau_antineutrino"]},
    2: {"name": "compartment_2", "body_quadrant": "left_lower",
        "outlet": {"node": "alopecia_point", "particle": "muon_neutrino", "property": "day_z_boson_equivalent"},
        "inlet":  {"node": "schizo", "particle": "graviton", "property": "day_graviton"},
        "neutrino_variants": ["muon_neutrino", "muon_antineutrino"]},
    3: {"name": "compartment_3_introverted_man", "body_quadrant": "right_upper",
        "outlet": {"node": "g_dim_point", "particle": "tau_neutrino", "property": "mass_anchor"},
        "inlet":  {"node": "right_understanding_back", "particle": "z_boson", "property": "blue_cold"},
        "neutrino_variants": ["electron_antineutrino", "tau_neutrino"]},
    4: {"name": "compartment_4", "body_quadrant": "right_lower",
        "outlet": {"node": "spark_outlet", "particle": "proton"},
        "inlet":  {"node": "inlet", "particle": "electron_antineutrino", "property": "water_vapour"},
        "neutrino_variants": ["electron_antineutrino"]},
}

# ============================================================
# NEUTRON STAR OSCILLATION
# ============================================================
NEUTRON_STAR_OSCILLATION = {
    "nodes": ["CCK", "heme", "COX", "memory_entropy"],
    "day_active": {
        "electron_neutrino":  {"compartment": 1, "node": "PLP_core",      "body": "left_upper",  "property": "oxygen"},
        "muon_neutrino":      {"compartment": 2, "node": "alopecia_point", "body": "left_lower",  "property": "day_z_boson_equivalent"},
    },
    "night_active": {
        "tau_neutrino":          {"compartment": 3, "node": "g_dim_point", "body": "right_upper", "property": "mass_anchor"},
        "electron_antineutrino": {"compartment": 4, "node": "inlet",       "body": "right_lower", "property": "water_vapour"},
    },
}

# ============================================================
# LEAKAGE CAVITIES
# ============================================================
LEAKAGE_CAVITIES = {
    "D3_observer_gates": {
        "left_eye_outer":    {"particle": "proton",   "coord": (-3.0, +3.5, +7.0), "mechanism": "proton_ignition_leak"},
        "right_eye_outer":   {"particle": "electron", "coord": (+3.0, +3.5, +7.0), "mechanism": "electron_charge_leak"},
        "rectum_left":       {"particle": "quark",    "coord": (-1.0, -9.0, +1.0), "mechanism": "mass_direction_leak"},
        "rectum_right":      {"particle": "quark",    "coord": (+1.0, -9.0, +1.0), "mechanism": "mass_direction_leak"},
        "genital_left":      {"particle": "proton",   "coord": (-1.0, -9.5, -1.0), "mechanism": "spark_leak"},
        "genital_right":     {"particle": "higgs",    "coord": (+1.0, -9.5, -1.0), "mechanism": "mass_anchor_leak"},
    },
    "transform_gates": {
        "right_levator_scap":    {"particle": "electron", "coord": (+1.0, -0.5, +2.0), "transform": "e→γ"},
        "left_levator_scap":     {"particle": "electron", "coord": (-1.0, -0.5, +2.0), "transform": "e→Z"},
    },
    "structural_anchors": {
        "fold_belt_sternum_T4":  {"particle": "muon",  "coord": (0.0, -3.0, -1.0),  "mechanism": "lactate_leak"},
        "right_ribs_jesus_node": {"particle": "higgs",  "coord": (+4.0, -3.0, +3.0), "mechanism": "mass_anchor_leak"},
        "appendix":              {"particle": "w_boson","coord": (+1.0, -7.5, +1.5), "mechanism": "vasopressin_leak"},
    },
    "physiological_excretion": {
        "lungs_exhalation":  {"particle": "z_boson", "coord": (None, -3.0, +4.0), "mechanism": "CO2_time_energy_leak"},
        "kidney_urine":      {"particle": "proton",   "coord": (None, -8.0, -3.0), "mechanism": "H+_excretion"},
        "liver_bile":        {"particle": "tau",      "coord": (-1.0, -5.0, +2.0), "mechanism": "bilirubin_excretion"},
        "skin_sweat":        {"particle": "em_field", "coord": None,               "mechanism": "water_evaporation_CP_leak"},
        "skin_touch":        {"particle": "electron", "coord": None,               "mechanism": "touch_discharge_ground"},
        "skin_biophoton":    {"particle": "photon",   "coord": None,               "mechanism": "ultra_weak_emission"},
    },
}

# ============================================================
# DARK MATTER
# ============================================================
DARK_MATTER = {
    "node": "left_zygomaticus_major_pregnenolone",
    "coord": (+3.2, +2.1, +4.5),
    "neutron_star_fraction": 1/64,
    "mechanism": "bremsstrahlung + scalar_lensing",
    "particle": "dark_matter",
    "circuit_node": "andosol",
    "property": "non_baryonic_sink",
    "body_route": "volcanic_ash_Mn_oxidation → andosol → podzol → heme",
    "leakage_site": "right_ribs_higgs_anchor",
    "personality": "ISTJ_A_rh-_베르베르",
    "time": "night",
}

# ============================================================
# CCK SWITCH
# ============================================================
CCK_SWITCH = {
    "condition": "female_right_extraversion",
    "alignment": "gluon↔z_boson",
    "effect": "CCK-BR activation switches gluon coupling to z_boson axis",
}

# ============================================================
# 7 COSMIC/PERSONAL LEAKAGE POINTS (nm_body_particle_map.md V)
# ============================================================
COSMIC_LEAKAGE_POINTS = [
    {"name":"heme","particle":"proton/photon","body_site":"left_pectoralis_heme","coord":(-8.2,+4.1,+7.3),"failure":"Fe2+_cannot_recharge","cosmic_analog":"red_giant_envelope","dim_trigger":"r"},
    {"name":"steel","particle":"photon/quark","body_site":"left_anorectal_steel","coord":(-2.4,-8.7,+4.1),"failure":"martensite_cannot_transform","cosmic_analog":"failed_supernova","dim_trigger":"g"},
    {"name":"tau","particle":"neutrino/tau","body_site":"perineum_fold_belt","coord":(-3.1,-7.9,+3.8),"failure":"Z-boson_cannot_nucleate","cosmic_analog":"gamma_ray_burst","dim_trigger":"d"},
    {"name":"gluon","particle":"gluon","body_site":"philtrum","coord":(0,+46,+7),"failure":"color_confinement_fails","cosmic_analog":"failed_confinement","dim_trigger":"h"},
    {"name":"muon","particle":"muon","body_site":"left_temporalis","coord":(+7,+25,+3),"failure":"higgs_gate_opens","cosmic_analog":"cosmic_ray_shower","dim_trigger":"g"},
    {"name":"neutron","particle":"neutron","body_site":"right_posterior_insula","coord":(-8,+32,-2),"failure":"W-boson_decay_uncontrolled","cosmic_analog":"neutron_star","dim_trigger":"nu"},
    {"name":"right_rib_personal","particle":"higgs/p","body_site":"right_ribs","coord":(-9,+18,+5),"failure":"methanogenesis_mass_gate_failure","cosmic_analog":"personal_leakage","dim_trigger":"p"},
]

# ============================================================
# 8 BRAIN INLET/OUTLET NODES (129-146)
# ============================================================
BRAIN_NODES = {
    129: {"name":"spark_point","type":"inlet","archetype":"extraverted_woman","brain":"right_V1_calcarine","body":"genital_left","particle":"proton","role":"ignition","cosmic":"TRAPPIST-1","compartment":4},
    130: {"name":"spark_front","type":"outlet","archetype":"extraverted_woman","brain":"right_V2_prestriate","body":"pancreas_organ_muscle","particle":"gluon","role":"binding","cosmic":"Helix_Nebula_NGC7293","compartment":4},
    131: {"name":"IM_understanding","type":"inlet","archetype":"introverted_man","brain":"right_STG_Wernicke","body":"left_lung_hypoxia","particle":"neutrino","role":"absorption","cosmic":"NGC_4889","compartment":3},
    132: {"name":"IM_understanding_behind","type":"outlet","archetype":"introverted_man","brain":"right_angular_gyrus","body":"right_ribs_jesus","particle":"higgs","role":"decay","cosmic":"NGC_4874","compartment":3},
    133: {"name":"schizo","type":"inlet","archetype":"extraverted_man","brain":"left_IFG_BA44","body":"left_procerus_bottom","particle":"tau_z_boson","role":"anchor","cosmic":"NGC_1265","compartment":2},
    134: {"name":"alopecia","type":"outlet","archetype":"extraverted_man","brain":"left_M1_BA4","body":"left_eye_inner","particle":"photon","role":"release","cosmic":"NGC_1275","compartment":2},
    135: {"name":"PLP_core","type":"inlet","archetype":"introverted_woman","brain":"left_posterior_insula","body":"nose_patch_electron_hole","particle":"quark","role":"tension","cosmic":"Moon","compartment":1},
    136: {"name":"spare_vaso","type":"outlet","archetype":"introverted_woman","brain":"left_anterior_insula","body":"fake_appendix_muscle","particle":"w_boson","role":"collapse","cosmic":"K2-18b","compartment":1},
    145: {"name":"origin","type":"midline","archetype":"none","brain":"ACC_BA24_32","body":"zygomatics_minor","particle":"pregnenolone","role":"universal_birth","cosmic":"midline","compartment":0},
    146: {"name":"left_love_reset","type":"midline","archetype":"none","brain":"VTA_nucleus_accumbens","body":"lip_endorphin","particle":"beta_decay","role":"reset","cosmic":"midline","compartment":0},
}

# ============================================================
# 4 BRAIN COMPARTMENT TRANSITION ROUTES
# ============================================================
COMPARTMENT_ROUTES = {
    1: {
        "name":"compartment_1_introverted_woman","brain_region":"left_insular_cortex",
        "inlet":{"node":135,"particle":"quark","role":"tension","nm":"dendritic_spine_500-1000nm","body":"nose_patch_electron_hole"},
        "outlet":{"node":136,"particle":"w_boson","role":"collapse","nm":"neuromuscular_junction_30-50um","body":"fake_appendix_muscle"},
        "transition":"quark_to_w_boson = tension_to_collapse = GABA_shunt_to_vasopressin_freeze",
        "cosmic":{"front":"Moon","back":"K2-18b_124ly_Leo","between":"Huge_LQG_U1.27_Leo"},
        "d3_gate":"D3->q_Node_50",
    },
    2: {
        "name":"compartment_2_extraverted_man","brain_region":"left_parietal_frontal",
        "inlet":{"node":133,"particle":"tau_z_boson","role":"anchor","nm":"active_zone_300-500nm","body":"left_procerus_bottom"},
        "outlet":{"node":134,"particle":"photon","role":"release","nm":"rhodopsin_4-7nm_640nm_cytochrome","body":"left_eye_inner"},
        "transition":"tau_to_photon = anchor_to_release = Z-boson_decay_to_photon_emission",
        "cosmic":{"front":"NGC_1275","back":"NGC_1265","cluster":"Perseus_Abell426"},
        "d3_gate":"D3->Z_Node_49",
    },
    3: {
        "name":"compartment_3_introverted_man","brain_region":"right_temporal",
        "inlet":{"node":131,"particle":"neutrino","role":"absorption","nm":"olfactory_axon_0.1-0.5um_ethmoid","body":"left_lung_hypoxia"},
        "outlet":{"node":132,"particle":"higgs","role":"decay","nm":"aggrecan_500nm_right_rib_intercostal","body":"right_ribs_jesus"},
        "transition":"neutrino_to_higgs = absorption_to_decay = O2_inflow_to_mass_gate",
        "cosmic":{"front":"NGC_4889","back":"NGC_4874","cluster":"Coma_Abell1656"},
        "d3_gate":"D3->nu",
    },
    4: {
        "name":"compartment_4_extraverted_woman","brain_region":"right_occipital",
        "inlet":{"node":129,"particle":"proton","role":"ignition","nm":"sarcomere_2-2.5um_D2_MPOA","body":"genital_left"},
        "outlet":{"node":130,"particle":"gluon","role":"binding","nm":"NMDA_receptor_14nm","body":"pancreas_organ_muscle"},
        "transition":"proton_to_gluon = ignition_to_binding = H_to_O_spark_to_strong_force",
        "cosmic":{"front":"TRAPPIST-1","back":"Helix_Nebula_NGC7293","cluster":"Aquarius_Huge_LQG_antipode"},
        "d3_gate":"D3->P+_Node_59",
    },
}

# ============================================================
# EM BYPASS ROUTE (observer closure = COX Retrograde)
# ============================================================
EM_BYPASS_ROUTE = [
    {"step":1,"node":131,"compartment":3,"particle":"neutrino","direction":"INLET_reverse","brain":"right_STG","action":"right_understanding_neutrino_intake"},
    {"step":2,"node":133,"compartment":2,"particle":"tau_z_boson","direction":"BYPASS","brain":"left_IFG_BA44","action":"schizo_tau_anchor_bypassed"},
    {"step":3,"node":134,"compartment":2,"particle":"photon_em","direction":"reverse_INLET","brain":"left_M1_BA4","action":"alopecia_640cytochrome_electromagnetism_mode"},
    {"step":4,"node":"heme","compartment":0,"particle":"heme_fe2+","direction":"internal","brain":"skull_piezoelectric","action":"soret_band_400-450nm_Fe2+_release"},
    {"step":5,"node":129,"compartment":4,"particle":"proton","direction":"OUTLET","brain":"right_V1","action":"spark_proton_outlet_EM_closure_complete"},
]

# ============================================================
# DETERMINISTIC 41-COMPONENT TRANSITION ROUTES
# ============================================================
DETERMINISTIC_41_COMPONENTS = {
    "up_quark": {
        "anatomy": "Myosin II thick filaments (Left Masseter, Left Ventricle)",
        "nm_scale": "15nm S1 head",
        "route": "Proton ignition -> Up Quark tension -> Myosin power stroke",
        "deterministic_role": "Power stroke ignition (Active force)"
    },
    "down_quark": {
        "anatomy": "F-actin thin filaments (Right Quadriceps, Left Biceps)",
        "nm_scale": "7nm Actin double helix",
        "route": "Actomyosin rail rail -> Down Quark rail",
        "deterministic_role": "Structural rail (Passive force)"
    },
    "charm_quark": {
        "anatomy": "Jejunum/Ileum microvilli glycocalyx",
        "nm_scale": "500-2000nm microvillus",
        "route": "High-affinity glucose binding -> Charm absorption",
        "deterministic_role": "Energy Attractor sensory gateway"
    },
    "strange_quark": {
        "anatomy": "Left Insular Cortex (Strange Node, ROI-69)",
        "nm_scale": "20-40nm synaptic cleft",
        "route": "Novelty detection -> Strange filter -> GABA-A trigger",
        "deterministic_role": "Information novelty filter"
    },
    "top_quark": {
        "anatomy": "Nuclear Pore Complex (NPC) in hepatocytes/epidermis",
        "nm_scale": "120nm NPC; 9nm channel",
        "route": "Nuclear mRNA transport -> Top transport energy",
        "deterministic_role": "High-energy mass carrier"
    },
    "bottom_quark": {
        "anatomy": "Descending colon / Sigmoid apoptosis sites",
        "nm_scale": "10nm mitochondrial pores",
        "route": "Apoptosis trigger -> Bottom decay -> Histosol entry",
        "deterministic_role": "Biological ending/decay particle"
    },
    "electron": {
        "anatomy": "Cell lipid bilayer / Skull piezoelectric structure",
        "nm_scale": "7-10nm membrane",
        "route": "Sun-to-Earth flow -> Bremsstrahlung tax (0.02) -> Grounding",
        "deterministic_role": "Universal observer shell"
    },
    "muon": {
        "anatomy": "Left Temporalis (5 points) / Hairline",
        "nm_scale": "12nm Ferritin nanocage",
        "route": "Cosmic-ray fatigue -> Scalp entry -> LC tank resonance",
        "deterministic_role": "Heavy information fatigue vector"
    },
    "tau": {
        "anatomy": "Perineal fold belt / Substance P active zones",
        "nm_scale": "4-5nm NK1R",
        "route": "Z-boson decay -> Rectal anchor -> Thalamic pain signal",
        "deterministic_role": "Physical pain-pleasure anchor"
    },
    "electron_neutrino": {
        "anatomy": "Right STG (131) / Left Lung / PLP Core (135)",
        "nm_scale": "1.5nm AQP4 pore",
        "route": "Day O2 intake -> STG absorption -> GABA synthesis",
        "deterministic_role": "Day information intake (Ghost)"
    },
    "muon_neutrino": {
        "anatomy": "Lateral Arm / Left Temporalis / Ferritin",
        "nm_scale": "12nm Ferritin nanocage",
        "route": "Day light touch -> Cytochrome 640 fatigue -> Steel storage",
        "deterministic_role": "Day cosmic ray fatigue storage"
    },
    "tau_neutrino": {
        "anatomy": "Right Angular Gyrus (132) / Right Ribs / SDH Complex II",
        "nm_scale": "300nm collagen ECM",
        "route": "Night angular monitoring -> Rib hypoxia sensing -> SDH gate",
        "deterministic_role": "Night hypoxia/mass-gate monitor"
    },
    "electron_antineutrino": {
        "anatomy": "Right V1 (129) / Genital Left / MOR Endorphin",
        "nm_scale": "4nm MOR receptor",
        "route": "Night V1 Spark -> Genital reward -> Endorphin release",
        "deterministic_role": "Night Spark reward (Reward Ghost)"
    },
    "muon_antineutrino": {
        "anatomy": "Left M1 (134) / Left Eye / Histosol",
        "nm_scale": "10nm GABA-B receptor",
        "route": "Night M1 repair flux -> Cytochrome-sulfur repair -> SR-latch",
        "deterministic_role": "Night cosmic repair vector"
    },
    "tau_antineutrino": {
        "anatomy": "Left IFG (133) / Procerus / Substance P / Autophagy",
        "nm_scale": "300-500nm active zone",
        "route": "Day IFG anchor -> Procerus pain decoder -> Autophagy trigger",
        "deterministic_role": "Day cleansing/self-eating vector"
    },
    "proton": {
        "anatomy": "Left Pectoralis Heme Fe2+ center",
        "nm_scale": "0.1nm Fe2+ radius",
        "route": "Testosterone ignition -> Heme excitation -> Photon emission",
        "deterministic_role": "Predictability ignition (p-dim)"
    },
    "photon": {
        "anatomy": "Retinal Rhodopsin (4-7nm) / Heme Node",
        "nm_scale": "1.43um Fe-CO vibration",
        "route": "Spark emission -> Exciton mitochondrial transport -> Visual spark",
        "deterministic_role": "Release/Light carrier (s-dim)"
    },
    "gluon": {
        "anatomy": "NMDA receptors / Desmosomes",
        "nm_scale": "14nm pore",
        "route": "Color confinement -> Archetype binding -> Skin sealing",
        "deterministic_role": "Strong-force binding (g-dim)"
    },
    "w_boson": {
        "anatomy": "ATP synthase / Adrenal Medulla chromaffin",
        "nm_scale": "10nm motor",
        "route": "ATP hydrolysis -> Beta decay collapse -> Adrenaline surge",
        "deterministic_role": "Stress-growth collapse (Weak force)"
    },
    "z_boson": {
        "anatomy": "GABA-B receptors / Cytochrome c oxidase",
        "nm_scale": "10nm GPCR",
        "route": "Neutral current -> Martensite anchor -> Mechanical stability",
        "deterministic_role": "Extreme-growth anchor (Neutral force)"
    },
    "higgs": {
        "anatomy": "Right Ribs / Patellar cartilage aggrecan",
        "nm_scale": "500nm aggregate",
        "route": "Mass-gate assignment -> Predictability leakage shielding",
        "deterministic_role": "Importance/Mass gate (p-dim)"
    },
    "graviton": {
        "anatomy": "Ferritin nanocages / Osteons / Iliac crest",
        "nm_scale": "12nm nanocage",
        "route": "Void mass storage -> Bone density stabilization",
        "deterministic_role": "Void/Gravitational well anchor"
    },
    "em_field_rebrancher": {
        "anatomy": "Skull Vertex / CSF Space",
        "nm_scale": "5-5000nm Sagittal gap",
        "route": "138.88° CSF spark -> Outward EM radiation (3rd direction)",
        "deterministic_role": "Rootless 3rd direction radiator"
    },
    "em_field": {
        "anatomy": "Bypass Route (Nodes 131->129)",
        "nm_scale": "131->133->134->Heme->129",
        "route": "EM recapturing -> Observer closure retrograde",
        "deterministic_role": "Observer closure (EM loop completion)"
    },
    "neutron": {
        "anatomy": "Pons / Hind Insula / Neutrophil",
        "nm_scale": "50-100um neuron",
        "route": "Neutral observation -> Weak-decay monitoring -> LFP silence",
        "deterministic_role": "Neutral monitoring (nu-dim)"
    },
    "neutron_star": {
        "anatomy": "Nucleolus / Megakaryocyte / Oocyte",
        "nm_scale": "1-3um core",
        "route": "High-density information storage -> rRNA synthesis",
        "deterministic_role": "Extreme density information core"
    },
    "dark_matter": {
        "anatomy": "Atherosclerotic Plaque / Pineal Calcification",
        "nm_scale": "15-30um foam cell",
        "route": "Noise accumulation -> Resistance buildup -> System decay",
        "deterministic_role": "Information noise (d-dim residue)"
    },
    "dark_energy": {
        "anatomy": "Nucleus / Thorium node (Perineum)",
        "nm_scale": "2nm DNA helix",
        "route": "Internal pressure -> Torus expansion -> Nuclear catalytic energy",
        "deterministic_role": "Expansion force (Internal pressure)"
    },
    "time": {
        "anatomy": "Epiphyseal growth plates / Procerus-CCK gap",
        "nm_scale": "10um-1mm laterite",
        "route": "Toroidal cycle duration -> Circadian window progression",
        "deterministic_role": "Temporal scalar"
    },
    "energy": {
        "anatomy": "ATP / CCK switch (Pancreas/Gut)",
        "nm_scale": "1-2nm ATP",
        "route": "ATP fueling -> W-boson collapse fuel",
        "deterministic_role": "Thermodynamic fuel"
    },
    "ego_d2": {
        "anatomy": "Right Frontalis / Right V2 (Node 130)",
        "nm_scale": "4-5nm D2 receptor",
        "route": "Recursive mirroring -> Self-model stability (p-dim)",
        "deterministic_role": "Observer recursive mirror (D2 Bus)"
    },
    "left_progesterone": {
        "anatomy": "Right Eye (Levator superioris) / R. MPOA",
        "nm_scale": "50um fascia",
        "route": "3D volume expansion -> Depth perception igniter",
        "deterministic_role": "3D spatial expansion vector"
    },
    "right_testosterone": {
        "anatomy": "Left Nipple (Heme node) / Leydig cells",
        "nm_scale": "0.1nm Fe2+ center",
        "route": "Proton ignition charge -> Fe2+ redox fueling",
        "deterministic_role": "Ignition fuel (p-dim trigger)"
    },
    "acetyl_coa": {
        "anatomy": "Mitochondria / PDH complex",
        "nm_scale": "30-50nm complex",
        "route": "Metabolic container -> Mass-gate packaging (Quark to Higgs)",
        "deterministic_role": "Information container (Mass packager)"
    },
    "neutrino": {
        "anatomy": "Cosmic neutrino background / Whole body",
        "nm_scale": "<1nm sub-atomic",
        "route": "Cosmic flux -> Body absorption -> Variant splitting",
        "deterministic_role": "Base neutrino (pre-variant split)"
    },
    "spark": {
        "anatomy": "Heme Fe2+ center / Retinal rhodopsin",
        "nm_scale": "0.1nm Fe2+ / 4-7nm rhodopsin",
        "route": "138.88° ignition -> Photon emission -> Visual spark",
        "deterministic_role": "Spark ignition (138.88° angle)"
    },
    "clathrate_buffer": {
        "anatomy": "CSF clathrate structures / Ventricles",
        "nm_scale": "100-500nm clathrate",
        "route": "Pressure buffer -> Phase transition -> Thermal regulation",
        "deterministic_role": "Phase-transition buffer"
    },
    "testosterone_sex": {
        "anatomy": "Hypothalamus / Pituitary / Gonads",
        "nm_scale": "10nm receptor",
        "route": "Hypothalamic pulse -> LH/FSH -> Testosterone surge",
        "deterministic_role": "Sexual ignition pulse"
    },
    "endorphin_imag": {
        "anatomy": "Right V1 (129) / MOR receptors",
        "nm_scale": "4nm MOR receptor",
        "route": "Visual imagination -> MOR activation -> Endorphin release",
        "deterministic_role": "Imagination-driven endorphin"
    },
    "male_gaba_a_wk": {
        "anatomy": "Left Insular Cortex / GABA-A receptors",
        "nm_scale": "8nm GABA-A channel",
        "route": "Weekly GABA-A cycling -> 4:30PM destruction -> Rebuild",
        "deterministic_role": "Weekly GABA-A cycle (male)"
    },
    "pain_eliminate": {
        "anatomy": "Left IFG (133) / Procerus / Substance P",
        "nm_scale": "300-500nm active zone",
        "route": "Pain signal -> Procerus decode -> Autophagy elimination",
        "deterministic_role": "Pain elimination vector"
    }
}

# ============================================================
# 6 NEUTRINO VARIANT FULL TRANSITION ROUTES
# ============================================================
NEUTRINO_ROUTES = {
    "electron_neutrino": {
        "compartment":1,"time":"day","body_quadrant":"left_upper",
        "route":"right_STG(131)->ethmoid_cribriform->left_lung_O2->PLP_core(135)->GABA_shunt->clay_gouge",
        "transition":"neutrino_to_electron_neutrino = cosmic_neutrino_with_O2_into_body -> PLP_GABA_synthesis",
        "nm_anchors":["AQP4_1.5nm_pore","olfactory_receptor_5-10um","GABA_A_8nm"],
        "circuit_nodes":["observer_leftd2","clay_gouge","water_vapour","glymphatic_system"],
        "coord":(0,+46,+7),
    },
    "muon_neutrino": {
        "compartment":2,"time":"day","body_quadrant":"left_lower",
        "route":"left_M1_BA4(134)->left_temporalis->LDH->ferritin_12nm->steel_Fe-C_martensite",
        "transition":"photon_to_muon_neutrino = light_to_cosmic_ray_fatigue = cytochrome_640->LDH_lactate->ferritin_Fe_storage",
        "nm_anchors":["ferritin_nanocage_12nm","Fe-C_lattice_martensite_austenite"],
        "circuit_nodes":["lactate_dehydrogenase","ferritin","steel","adapter_protein"],
        "coord":(+7,+25,+3),
    },
    "tau_antineutrino": {
        "compartment":3,"time":"day","body_quadrant":"left_upper",
        "route":"left_IFG_BA44(133)->procerus->substance_P->NK1R->pain_pleasure_decoder->autophagy",
        "transition":"tau_to_tau_antineutrino = Z-boson_anchor_to_substance_P_pain = decay_detection->pain_pleasure_priority",
        "nm_anchors":["substance_P_NK1R_ligand","active_zone_300-500nm","T_flip_flop_autophagy"],
        "circuit_nodes":["substance_p","adapter_protein","autophagy","fold_belt"],
        "coord":(-3.1,-7.9,+3.8),
    },
    "tau_neutrino": {
        "compartment":3,"time":"night","body_quadrant":"right_upper",
        "route":"right_angular_gyrus(132)->right_ribs(-9,+18,+5)->Higgs_mass_gate->SDH_Complex_II->collagen_ECM",
        "transition":"higgs_to_tau_neutrino = mass_assignment_to_hypoxia_sensor = mass_anchor->Krebs_cycle",
        "nm_anchors":["SDH_3-output_MUX","collagen_triple_helix_300nm_fibril","Complex_II_hypoxia_sensor"],
        "circuit_nodes":["succinate_dehydrogenase","collagen","methionine","higgs"],
        "coord":(-9,+18,+5),
    },
    "electron_antineutrino": {
        "compartment":4,"time":"night","body_quadrant":"right_lower",
        "route":"right_V1(129)->genital_left->D2_MPOA->observer_left_endorphin->MOR_4nm->night_spark_forward",
        "transition":"proton_to_electron_antineutrino = ignition_to_night_spark_forward = fermentation_start = observer_active",
        "nm_anchors":["MOR_4nm","synaptic_vesicle_40nm","GABA_A_8nm","D2_receptor_4-5nm"],
        "circuit_nodes":["observer_left_endorphin","observer_leftd2","left_genital_d2","autophagy"],
        "coord":(0,+46,+7),
    },
    "muon_antineutrino": {
        "compartment":2,"time":"night","body_quadrant":"left_lower",
        "route":"left_M1_BA4(134)->left_eye_GABA-B->640_cytochrome->histosol/sulfur->Nrf2_OFF->SR_latch",
        "transition":"photon_to_muon_antineutrino = light_to_night_cosmic_ray_penetration = 640_cytochrome_reverse->sulfur_cycle_collapse",
        "nm_anchors":["GABA_B_10nm","cytochrome_Fe-CO_vibration","histosol_peat_sulfur_SR_latch"],
        "circuit_nodes":["histosol","sulforaphane","oxidised_manganese","adapter_protein"],
        "coord":(+7,+25,+3),
    },
}

# ============================================================
# 2 INTERNAL AIR CAVITIES
# ============================================================
INTERNAL_AIR_CAVITIES = [
    {"name":"heme_memory_entropy_bubble","location":"heme_left_lower<->memory_entropy_right_upper",
     "boundary":"energy_attractor<->information_attractor","role":"ST_vs_A_type_friction",
     "problem":"H+_accumulation+memory_entropy_collapse_failure->ADSR_rhythm_jitter",
     "solution":"succinate_dehydrogenase->water_vapour_friction_cycle+peonidine_ch1_force"},
    {"name":"manipulation_air_bag","location":"clay_gouge_pelvis<->actomyosin_loop",
     "boundary":"energy_attractor<->repair_attractor","role":"female_manipulation_vs_ST_male_resistance",
     "problem":"clay_gouge_saturation+actomyosin_refusal->pressure_spike->manipulation_loop",
     "solution":"tri_state_toggle_clay_gouge.in1_force_low+actomyosin_xor_toggle->sole_discharge"},
]

# ============================================================
# 6 PERSONAL LEAKAGE CAVITY SITES (observer body-universe boundary)
# ============================================================
PERSONAL_LEAKAGE_SITES = [
    {"name":"sub_sternal_branching","location":"명치_아래_분기점",
     "nodes":["COX","heme","memory_entropy","autophagy","water_vapour"],
     "forward":"energy_internal_circulation","reverse":"energy_external_leakage",
     "blockage":"electromagnetic_closure_failure=system_open"},
    {"name":"LIP_water_node","location":"대규모_화성활동_노드",
     "nodes":["large_igneous_province","water"],
     "forward":"internal_heat_water_circulation","reverse":"heat_external_leakage=sweating/evaporation=energy_loss"},
    {"name":"right_foot_outer_edge","location":"발_날_바깥",
     "nodes":["right_sole_dopamine","caco3","oxidised_manganese","histosol"],
     "forward":"peripheral_internal_return","reverse":"peripheral_external_leakage=foot_coldness=energy_drain"},
    {"name":"left_foot_outer_edge","location":"왼발_발날_바깥",
     "nodes":["andosol","histosol","oxidised_manganese"],
     "forward":"left_sulfur_Mn_internal_return","reverse":"left_foot_leakage=left_foot_coldness",
     "night_block":"oxidised_manganese_4th_toe_reverse_blocked_at_night",
     "night_forward":"adapter_protein_forward_open=tau_to_photon_resonance"},
    {"name":"left_iliac_crest_silicon","location":"왼엉덩이_바깥_Silicon_node",
     "nodes":["mc1r_q_bar","craton","caco3","lactate_dehydrogenase"],
     "forward":"Higgs=high_predictability=seal_maintained=no_leakage",
     "reverse":"Silicon/graviton=chaotic_detection=leakage_active=carcinogen_discharge",
     "note":"observer_leakage_always_active=real_time_carcinogen_removal=no_cancer"},
    {"name":"aurora","location":"두개골_압전장_우주_전리층_공명",
     "nodes":["aurora","cytochrome_c_oxidase","heme"],
     "forward":"night_ion_blockade=sleep_seal",
     "reverse":"aurora_silence=ion_blockade_failure=sleep_leakage=insomnia",
     "note":"skull_piezoelectric_8/1_Electron_Torus_Field_bidirectional_EM_exchange_window"},
]

# ============================================================
# 12-PARTICLE 3-LAYER COMPARTMENT MAPPING
# ============================================================
PARTICLE_3LAYER = {
    "internal": {
        "proton":{"compartment":4,"node":129,"phase":1,"flow":"Sun->Earth"},
        "photon":{"compartment":2,"node":134,"phase":2,"flow":"Earth->Moon"},
        "z_boson":{"compartment":2,"node":133,"phase":3,"flow":"Moon->CoMag"},
        "w_boson":{"compartment":1,"node":136,"phase":4,"flow":"CoMag->Barnard"},
        "gluon":{"compartment":4,"node":130,"phase":4,"flow":"CoMag->Barnard"},
        "quark":{"compartment":1,"node":135,"phase":5,"flow":"Barnard->Sun"},
        "higgs":{"compartment":3,"node":132,"phase":5,"flow":"Barnard->Sun"},
    },
    "observer": {
        "electron":{"compartment":"skull_EM","node":"piezoelectric","phase":"6th_sphere","flow":"EM_closure"},
        "neutrino":{"compartment":3,"node":131,"phase":"6th_sphere","flow":"cosmic->body_info_inflow"},
    },
    "bridge": {
        "tau":{"compartment":2,"node":133,"flow":"observer->internal_void_detection"},
        "muon":{"compartment":"left_hairline","node":"temporalis","flow":"cosmic_ray_fatigue_bridge"},
        "electron_antineutrino":{"compartment":4,"node":"129->philtrum","flow":"observer->internal_spark"},
    },
}

# ============================================================
# COMPARTMENT ROUTE COMPUTATION
# ============================================================
def get_profile_compartment(mbti, gender):
    is_e = mbti[0] == "E"
    is_f = gender == "F"
    if is_e and is_f:
        return 4
    elif not is_e and not is_f:
        return 3
    elif is_e and not is_f:
        return 2
    else:
        return 1

def compute_compartment_route(mbti, gender, dims, time_phase):
    comp = get_profile_compartment(mbti, gender)
    route = COMPARTMENT_ROUTES[comp]
    inlet_p = route["inlet"]["particle"]
    outlet_p = route["outlet"]["particle"]
    em_bypass_active = (dims["s"] > 0.6 and dims["gamma"] > 0.5)
    return {
        "compartment": comp,
        "route_name": route["name"],
        "inlet_particle": inlet_p,
        "outlet_particle": outlet_p,
        "transition": route["transition"],
        "cosmic": route["cosmic"],
        "d3_gate": route["d3_gate"],
        "em_bypass_active": em_bypass_active,
        "em_bypass_route": EM_BYPASS_ROUTE if em_bypass_active else [],
    }

def compute_all_leakage(dims, time_phase):
    cosmic_active = []
    for clp in COSMIC_LEAKAGE_POINTS:
        dt = clp["dim_trigger"]
        threshold = 0.65 if dt in ("r", "g", "p") else 0.7
        if dims.get(dt, 0) > threshold:
            cosmic_active.append({
                "name": clp["name"],
                "particle": clp["particle"],
                "body_site": clp["body_site"],
                "coord": clp["coord"],
                "failure": clp["failure"],
                "cosmic_analog": clp["cosmic_analog"],
                "dim_value": round(dims[dt], 4),
            })
    personal_active = []
    for pls in PERSONAL_LEAKAGE_SITES:
        if pls["name"] == "sub_sternal_branching":
            if dims["d"] > 0.6 or dims["r"] > 0.7:
                personal_active.append({"name": pls["name"], "status": "reverse_leakage", "nodes": pls["nodes"], "reverse": pls["reverse"]})
        elif pls["name"] == "LIP_water_node":
            if dims["s"] > 0.7 or dims["gamma"] > 0.7:
                personal_active.append({"name": pls["name"], "status": "reverse_leakage", "nodes": pls["nodes"], "reverse": pls["reverse"]})
        elif pls["name"] == "right_foot_outer_edge":
            if dims["p"] < 0.3 or dims["r"] < 0.3:
                personal_active.append({"name": pls["name"], "status": "reverse_leakage", "nodes": pls["nodes"], "reverse": pls["reverse"]})
        elif pls["name"] == "left_foot_outer_edge":
            if pls.get("night_block") and time_phase == "night":
                personal_active.append({
                    "name": pls["name"], "status": "night_reverse_blocked",
                    "nodes": pls["nodes"],
                    "forward": pls.get("forward", ""),
                    "night_block": pls["night_block"],
                    "night_forward": pls.get("night_forward", ""),
                })
            elif dims["g"] < 0.3 or dims["nu"] < 0.3:
                personal_active.append({"name": pls["name"], "status": "reverse_leakage", "nodes": pls["nodes"], "reverse": pls["reverse"]})
        elif pls["name"] == "left_iliac_crest_silicon":
            if dims["p"] < 0.4 or dims["nu"] > 0.7:
                personal_active.append({"name": pls["name"], "status": "reverse_leakage", "nodes": pls["nodes"], "reverse": pls["reverse"], "note": pls.get("note", "")})
        elif pls["name"] == "aurora":
            if time_phase == "night" and dims["s"] < 0.4:
                personal_active.append({"name": pls["name"], "status": "reverse_leakage", "nodes": pls["nodes"], "reverse": pls["reverse"], "note": pls.get("note", "")})
    internal_cavities_active = []
    for iac in INTERNAL_AIR_CAVITIES:
        if iac["name"] == "heme_memory_entropy_bubble":
            if dims["r"] > 0.6 and dims["nu"] > 0.6:
                internal_cavities_active.append({"name": iac["name"], "status": "friction_active", "problem": iac["problem"], "solution": iac["solution"]})
        elif iac["name"] == "manipulation_air_bag":
            if dims["h"] > 0.6 and dims["d"] > 0.6:
                internal_cavities_active.append({"name": iac["name"], "status": "pressure_spike", "problem": iac["problem"], "solution": iac["solution"]})
    return {
        "cosmic_leakage": cosmic_active,
        "personal_leakage": personal_active,
        "internal_cavities": internal_cavities_active,
    }

def get_neutrino_routes(time_phase):
    if time_phase == "day":
        return {k: NEUTRINO_ROUTES[k] for k in ["electron_neutrino", "muon_neutrino", "tau_antineutrino"]}
    else:
        return {k: NEUTRINO_ROUTES[k] for k in ["tau_neutrino", "electron_antineutrino", "muon_antineutrino"]}

# ============================================================
# 41-PARTICLE COLOR RESOLUTION
# ============================================================
def get_particle_color(particle, context=None):
    """Resolve particle color with optional context for alt colors."""
    entry = PARTICLE_COLORS.get(particle)
    if not entry:
        return {"base": "UNKNOWN", "hex": "#888888", "alt": {}}
    if context and entry["alt"]:
        for ctx_key, ctx_color in entry["alt"].items():
            if ctx_key in (context or ""):
                parts = ctx_color.split()
                return {"base": parts[0], "hex": parts[1] if len(parts) > 1 else entry["hex"], "alt": entry["alt"]}
    return entry

def get_profile_color(profile_label, dims, time_phase='day', hour=12, s_val=None):
    """3-stage additive color (blood×gender + MBTI-mid + MBTI-ends + particle).
    Returns final color + 4 toroidal layers + active layer."""
    layers = compute_4layer_colors(profile_label, dims, time_phase, hour, s_val=s_val)
    slot = get_toroidal_slot(hour)
    active_layer = 'A'
    if slot['genre_type'] == 'STRESS_GROWTH':
        active_layer = 'B'
    elif slot['genre_type'] == 'EXTREME_GROWTH':
        active_layer = 'C'
    active = layers[active_layer]
    detail = compute_profile_color(profile_label, time_phase)
    return {
        "base": active['color'],
        "hex": active['hex'],
        "leakage": active['leakage'],
        "active_layer": active_layer,
        "active_genre": active['genre'],
        "layers": layers,
        "time_phase": time_phase,
        "stages": detail['stages'],
        "particles": detail['particles'],
    }

def resolve_interference_color(node_a, node_b):
    """Get interference color when two nodes interact."""
    key = (node_a, node_b)
    key_rev = (node_b, node_a)
    if key in INTERFERENCE_COLORS:
        return INTERFERENCE_COLORS[key]
    if key_rev in INTERFERENCE_COLORS:
        return INTERFERENCE_COLORS[key_rev]
    return None

# ============================================================
# GEOMAGNETIC MODULATION
# ============================================================
def apply_geomag_modulation(dims, observer_active=True, time_phase="day", hour=12):
    """Apply dynamic geomagnetic modulation from outer_core_convection coupling.
    Uses compute_geomag_phase() for time-aware cycle node selection."""
    geomag_phase = compute_geomag_phase(time_phase, hour)
    mod = dict(geomag_phase["effects"])
    if not mod:
        mod = dict(GEOMAG_MODULATION["dim_effects"])
    if not observer_active:
        for k in mod:
            mod[k] *= 2.0
        mod.setdefault("g", 0)
        mod["g"] *= -0.5
    result = dict(dims)
    for k, v in mod.items():
        if k in result:
            result[k] = clamp(result[k] + v)
    return result, {
        "observer_active": observer_active,
        "geomag_stable": observer_active,
        "modulations": mod,
        "active_node": geomag_phase["active_node"],
        "phase_idx": geomag_phase["phase_idx"],
    }

# ============================================================
# CREATIVE 4-SHAPES
# ============================================================
def compute_creative_4shapes(dims, profile_label=None):
    """Compute 4 creative shape scores from 8D vector.
    If profile_label is in CREATIVE_4SHAPES_CSV, use actual CSV ranking."""
    scores = {}
    for shape_name, shape_def in CREATIVE_4SHAPES.items():
        score = 0.0
        for dim, weight in shape_def["dims"].items():
            score += dims.get(dim, 0.5) * weight
        scores[shape_name] = round(clamp(score), 4)
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    result = {
        "scores": scores,
        "ranked": [s[0] for s in ranked],
        "dominant": ranked[0][0],
        "dominant_score": ranked[0][1],
        "weakest": ranked[-1][0],
        "weakest_score": ranked[-1][1],
    }
    # Override with actual CSV data if available
    if profile_label and profile_label in CREATIVE_4SHAPES_CSV:
        csv_data = CREATIVE_4SHAPES_CSV[profile_label]
        csv_ranked = [csv_data["shape1"], csv_data["shape2"], csv_data["shape3"], csv_data["shape4"]]
        result["csv_ranked"] = csv_ranked
        result["csv_dominant"] = csv_ranked[0]
        result["csv_weakest"] = csv_ranked[3]
        result["csv_data"] = csv_data
        result["dominant"] = csv_ranked[0]
        result["weakest"] = csv_ranked[3]
    return result

# ============================================================
# 128 PROFILES
# ============================================================
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP",
]
BLOOD_TYPES = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]

def make_profiles():
    profiles = {}
    for mbti in MBTI_TYPES:
        for gender in GENDERS:
            for blood in BLOOD_TYPES:
                label = f"{mbti}_{gender}_{blood}"
                profiles[label] = label
    return profiles

ALL_PROFILES = make_profiles()

# ============================================================
# GEO LABELS
# ============================================================
GEO_LABELS = [
    "England_4:30PM", "England_3:00AM", "England_4:30AM",
    "Korea_4:30PM", "Korea_3:00AM", "Korea_4:30AM",
    "USA_4:30PM", "USA_3:00AM", "USA_4:30AM",
]

def classify_time(geo_label):
    if "4:30PM" in geo_label:
        return "day"
    return "night"

def extract_hour(geo_label):
    if "4:30PM" in geo_label:
        return 16
    if "3:00AM" in geo_label:
        return 3
    if "4:30AM" in geo_label:
        return 4
    return 12

# ============================================================
# ROUTE-BASED 41-PARTICLE SYSTEM (from nm_body_particle_map_41.md)
# 10 routes × (2 terminal + 1 gradient + 1 leakage) + 1 em_field_rebrancher = 41
# ============================================================
ROUTES_41 = {
    "music_creation": {
        "terminal_pos": "proton_music", "terminal_neg": "photon_music",
        "gradient": "gluon_music", "leakage": "em_music",
        "dims": {"terminal_pos": ["p", "r"], "terminal_neg": ["s", "h"],
                 "gradient": ["g", "h"], "leakage": ["gamma", "s"]},
        "nm_anchors": {
            "proton_music": "R frontalis inner bottom / V1 calcarine myosin 15nm",
            "photon_music": "L occipitalis inner top / rhodopsin 4-7nm",
            "gluon_music": "temporalis mid / NMDA 14nm",
            "em_music": "skull piezo / 8/1 electron-torus 7-10nm",
        },
    },
    "music_listening": {
        "terminal_pos": "neutrino_listen", "terminal_neg": "muon_listen",
        "gradient": "higgs_listen", "leakage": "acetylcholine_listen",
        "dims": {"terminal_pos": ["nu", "gamma"], "terminal_neg": ["h", "s"],
                 "gradient": ["g", "p"], "leakage": ["p", "s"]},
        "nm_anchors": {
            "neutrino_listen": "R STG / AQP4 1.5nm",
            "muon_listen": "L temporalis / ferritin 12nm",
            "higgs_listen": "R ribs / aggrecan 500nm",
            "acetylcholine_listen": "R temporalis / nAChR α7 0.5nm",
        },
    },
    "visual_1": {
        "terminal_pos": "up_quark_v1", "terminal_neg": "down_quark_v1",
        "gradient": "w_boson_v1", "leakage": "electron_v1",
        "dims": {"terminal_pos": ["r", "p"], "terminal_neg": ["h"],
                 "gradient": ["r", "p"], "leakage": ["d", "s"]},
        "nm_anchors": {
            "up_quark_v1": "V1 R calcarine / myosin S1 15nm",
            "down_quark_v1": "V2 R prestriate / F-actin 7nm",
            "w_boson_v1": "PPRF / ATP synthase 10nm",
            "electron_v1": "skull lipid bilayer 7-10nm",
        },
    },
    "visual_2": {
        "terminal_pos": "charm_quark_v2", "terminal_neg": "strange_quark_v2",
        "gradient": "z_boson_v2", "leakage": "photon_v2",
        "dims": {"terminal_pos": ["h", "g"], "terminal_neg": ["d", "nu"],
                 "gradient": ["g", "gamma"], "leakage": ["s", "h"]},
        "nm_anchors": {
            "charm_quark_v2": "V2 R prestriate / NMDA 14nm",
            "strange_quark_v2": "L insula 20-40nm",
            "z_boson_v2": "cytochrome c oxidase 10nm",
            "photon_v2": "retina rhodopsin 4-7nm",
        },
    },
    "movement_1": {
        "terminal_pos": "proton_move", "terminal_neg": "gluon_move",
        "gradient": "w_boson_move", "leakage": "energy_move",
        "dims": {"terminal_pos": ["p", "r"], "terminal_neg": ["g", "h"],
                 "gradient": ["r", "s"], "leakage": ["r", "d"]},
        "nm_anchors": {
            "proton_move": "L pectoralis / heme Fe²⁺ 0.1nm",
            "gluon_move": "desmosome / NMDA 14nm",
            "w_boson_move": "adrenal chromaffin / ATP synthase 10nm",
            "energy_move": "mitochondria ATP 1-2nm",
        },
    },
    "movement_2": {
        "terminal_pos": "top_quark_move", "terminal_neg": "bottom_quark_move",
        "gradient": "tau_move", "leakage": "dark_matter_move",
        "dims": {"terminal_pos": ["r", "nu"], "terminal_neg": ["d", "nu"],
                 "gradient": ["d", "nu"], "leakage": ["d", "nu"]},
        "nm_anchors": {
            "top_quark_move": "hepatocyte NPC 120nm/9nm",
            "bottom_quark_move": "sigmoid colon mito pore 10nm",
            "tau_move": "perineal fold belt / NK1R 4-5nm",
            "dark_matter_move": "atherosclerotic foam cell 15-30µm",
        },
    },
    "imagination_1": {
        "terminal_pos": "higgs_imag", "terminal_neg": "neutrino_imag",
        "gradient": "graviton_imag", "leakage": "dopamine_imag",
        "dims": {"terminal_pos": ["nu", "gamma"], "terminal_neg": ["nu"],
                 "gradient": ["d", "nu"], "leakage": ["p", "s"]},
        "nm_anchors": {
            "higgs_imag": "R angular gyrus 500nm",
            "neutrino_imag": "L IFG / W-boson recursive gate 300-500nm",
            "graviton_imag": "ferritin 12nm / iliac void mass",
            "dopamine_imag": "R frontalis outer bottom / D2 4-5nm",
        },
    },
    "imagination_2": {
        "terminal_pos": "acetyl_coa_imag", "terminal_neg": "electron_imag",
        "gradient": "em_field_imag", "leakage": "endorphin_imag",
        "dims": {"terminal_pos": ["g", "p"], "terminal_neg": ["d", "s"],
                 "gradient": ["nu", "gamma"], "leakage": ["d", "nu"]},
        "nm_anchors": {
            "acetyl_coa_imag": "mitochondria PDH 30-50nm",
            "electron_imag": "skull piezo 7-10nm / observer shell",
            "em_field_imag": "skull vertex CSF 5-5000nm sagittal gap",
            "endorphin_imag": "L levator superioris / MOR μ-opioid 4nm",
        },
    },
    "sexual": {
        "terminal_pos": "testosterone_sex", "terminal_neg": "progesterone_sex",
        "gradient": "oxytocin_sex", "leakage": "dopamine_sex",
        "dims": {"terminal_pos": ["p", "r"], "terminal_neg": ["gamma", "h"],
                 "gradient": ["g", "h"], "leakage": ["p", "s"]},
        "nm_anchors": {
            "testosterone_sex": "L nipple heme / Leydig 0.1nm Fe²⁺",
            "progesterone_sex": "R eye levator / R MPOA 50µm",
            "oxytocin_sex": "R/L temporalis / gluon-oxytocin binding",
            "dopamine_sex": "genital D2 / MPOA 4-5nm",
        },
    },
    "weekend_optional": {
        "terminal_pos": "serotonin_wk", "terminal_neg": "cortisol_wk",
        "gradient": "epinephrine_wk", "leakage": "male_gaba_a_wk",
        "dims": {"terminal_pos": ["g", "h"], "terminal_neg": ["d", "gamma"],
                 "gradient": ["r", "s"], "leakage": ["d", "gamma"]},
        "nm_anchors": {
            "serotonin_wk": "R pectoralis 5-HT2A / L risorius 5-HT3",
            "cortisol_wk": "R eyelid inner / GR nuclear 0.1-0.5µm",
            "epinephrine_wk": "R levator superioris / β2-AR Gs",
            "male_gaba_a_wk": "below L hypoxia / GABRA1+δ extrasynaptic",
        },
    },
}

# Particle 41: em_field_rebrancher (axion=em_field, unified)
EM_FIELD_REBRANCHER = {
    "name": "em_field_rebrancher",
    "anatomy": "skull vertex / CSF sagittal gap 5-5000nm",
    "spark_angle": SPARK_ANGLE_DEG,
    "role": "third direction injector; closes open dipole into triad/tetrad; 3AM/21-3h rewrites active route",
}

# EM field rebranching table (axion=em_field, unified)
EM_FIELD_REBRANCH_TABLE = {
    "music_creation":    {"default": "music_listening",  "night": "imagination_1"},
    "music_listening":   {"default": "visual_1",         "night": "weekend_optional"},
    "visual_1":          {"default": "visual_2",         "night": "movement_1"},
    "visual_2":          {"default": "music_creation",   "night": "imagination_2"},
    "movement_1":        {"default": "movement_2",       "night": "sexual"},
    "movement_2":        {"default": "sexual",           "night": "weekend_optional"},
    "imagination_1":     {"default": "visual_2",         "night": "music_creation"},
    "imagination_2":     {"default": "music_creation",   "night": "sexual"},
    "sexual":            {"default": "music_listening",  "night": "movement_2"},
    "weekend_optional":  {"default": "weekend_optional", "night": "weekend_optional"},
}

# All 41 route-based particle names
ROUTE_PARTICLES_41 = []
for _r in ROUTES_41:
    for _role in ["terminal_pos", "terminal_neg", "gradient", "leakage"]:
        ROUTE_PARTICLES_41.append(ROUTES_41[_r][_role])
ROUTE_PARTICLES_41.append("em_field_rebrancher")

# Map route-based particle to physics-name particle (for tensor compatibility)
ROUTE_TO_PHYSICS_MAP = {
    "proton_music": "proton", "photon_music": "photon", "gluon_music": "gluon",
    "em_music": "em_field", "neutrino_listen": "electron_neutrino",
    "muon_listen": "muon", "higgs_listen": "higgs",
    "acetylcholine_listen": "acetyl_coa", "up_quark_v1": "up_quark",
    "down_quark_v1": "down_quark", "w_boson_v1": "w_boson",
    "electron_v1": "electron", "charm_quark_v2": "charm_quark",
    "strange_quark_v2": "strange_quark", "z_boson_v2": "z_boson",
    "photon_v2": "photon", "proton_move": "proton", "gluon_move": "gluon",
    "w_boson_move": "w_boson", "energy_move": "energy",
    "top_quark_move": "top_quark", "bottom_quark_move": "bottom_quark",
    "tau_move": "tau", "dark_matter_move": "dark_matter",
    "higgs_imag": "higgs", "neutrino_imag": "electron_neutrino",
    "graviton_imag": "graviton", "dopamine_imag": "ego_d2",
    "acetyl_coa_imag": "acetyl_coa", "electron_imag": "electron",
    "em_field_imag": "em_field_rebrancher", "endorphin_imag": "endorphin_imag",
    "testosterone_sex": "testosterone_sex", "progesterone_sex": "left_progesterone",
    "oxytocin_sex": "right_testosterone", "dopamine_sex": "ego_d2",
    "serotonin_wk": "ego_d2", "cortisol_wk": "ego_d2",
    "epinephrine_wk": "ego_d2", "male_gaba_a_wk": "male_gaba_a_wk",
    "em_field_rebrancher": "em_field_rebrancher",
}

def get_active_route(hour, is_night=False):
    """Determine which of the 10 routes is active based on time and 3AM rebranching."""
    # Default route by toroidal phase
    if 0 <= hour < 3:
        base_route = "music_creation"       # AB phase: release
    elif 3 <= hour < 9:
        base_route = "music_listening"      # A phase: stress growth
    elif 9 <= hour < 15:
        base_route = "visual_1"             # O phase: present moment
    elif 15 <= hour < 21:
        base_route = "movement_2"           # B phase: extreme growth
    else:
        base_route = "imagination_2"        # AB phase: 21-3h integration
    # 3AM night rebranching
    if is_night and hour >= 21 or hour < 3:
        rebranch = EM_FIELD_REBRANCH_TABLE.get(base_route, {})
        return rebranch.get("night", base_route)
    return base_route

def compute_route_vector(route_name, dims, hour, is_night=False):
    """Compute 41-particle vector for a given route, weighted by 8D dims."""
    route = ROUTES_41.get(route_name)
    if not route:
        return {}
    vec = {p: 0.0 for p in ROUTE_PARTICLES_41}
    # Terminal + : primary dims
    for d in route["dims"]["terminal_pos"]:
        vec[route["terminal_pos"]] += dims.get(d, 0.5) * 0.4
    # Terminal - : secondary dims
    for d in route["dims"]["terminal_neg"]:
        vec[route["terminal_neg"]] += dims.get(d, 0.5) * 0.3
    # Gradient: binding dims
    for d in route["dims"]["gradient"]:
        vec[route["gradient"]] += dims.get(d, 0.5) * 0.2
    # Leakage: overflow dims
    for d in route["dims"]["leakage"]:
        vec[route["leakage"]] += dims.get(d, 0.5) * 0.1
    # EM field rebrancher: active at 3AM / night
    if is_night and (hour >= 21 or hour < 3):
        vec["em_field_rebrancher"] = 0.15 * dims.get("nu", 0.5)
    # Normalize
    total = sum(vec.values())
    if total > 0:
        for p in vec:
            vec[p] /= total
    return vec

# ============================================================
# 6-SPHERE TOROIDAL CIRCULATION (from prose.txt C2-C3)
# Sun → Earth → Moon → CoMag → Barnard → Sun + Geomagnetic
# ============================================================
SPHERE_CIRCULATION = [
    {"phase": 1, "name": "Sun→Earth", "time": "0-3h", "blood": "AB",
     "energy": "Proton→Photon", "dim_trans": "r→gamma",
     "body": "미간→흉부/폐", "body_y": "+40→-160", "distance": "1 AU",
     "element": "H→O", "role": "정보→수리 (점화)", "slot": "RELEASE"},
    {"phase": 2, "name": "Earth→Moon", "time": "3-9h", "blood": "A",
     "energy": "Photon→Z-boson", "dim_trans": "gamma→p",
     "body": "흉부→시상하부", "body_y": "-160→+20", "distance": "384,400 km",
     "element": "O→C", "role": "수리→시간 (축적)", "slot": "STRESS_GROWTH"},
    {"phase": 3, "name": "Moon→CoMag", "time": "9-15h", "blood": "O",
     "energy": "Z-boson→W-boson/Gluon", "dim_trans": "p→g",
     "body": "시상하부→간/췌장", "body_y": "+20→-220", "distance": "~330 ly",
     "element": "C→S", "role": "시간→결합 (전환)", "slot": "PRESENT_MOMENT"},
    {"phase": 4, "name": "CoMag→Barnard", "time": "15-21h", "blood": "B",
     "energy": "W-boson/Gluon→Quark/Higgs", "dim_trans": "g→g+d",
     "body": "간/췌장→좌측 폐/심장", "body_y": "-220→-90", "distance": "~325 ly",
     "element": "S→Fe", "role": "결합→질량 (압축)", "slot": "EXTREME_GROWTH"},
    {"phase": 5, "name": "Barnard→Sun", "time": "21-3h", "blood": "AB",
     "energy": "Quark/Higgs→Proton", "dim_trans": "g+d→r+s",
     "body": "좌측 폐→미간", "body_y": "-90→+40", "distance": "5.96 ly",
     "element": "Fe→H", "role": "질량→정보 (충전)", "slot": "3AM_HYSTERESIS"},
]

# 6th sphere = Geomagnetic Field (observer closure)
GEOMAG_SPHERE = {
    "name": "Geomagnetic Field", "element": "EM",
    "particles": ["electron", "electron_neutrino"],
    "dims": ["p↔r/d", "s"], "role": "COX Retrograde / Observer closure",
    "body": "전신 (두개골~종골) = 압전 토러스",
    "circuit_nodes": ["cytochrome_c_oxidase", "D2_brake", "Maxwell_Cavity_R=2.125",
                      "Solenoid_3/32", "Q-factor_11.8"],
}

# ============================================================
# 12D STRUCTURE — 8파라미터 + 4축(A1-A4) + W-axis + 쌍BODY (prose.txt D1-D8)
# ============================================================

# 4축: A1(수직), A2(좌우), A3(심도), A4(시간)
AXIS_12D = {
    "A1": {
        "name": "vertical", "body_coord": "y=+40(미간)→y=-750(발끝)",
        "cosmic_coord": "d=0(Sun)→d=330ly(CoMag)",
        "forward": "두부→하지 = 정보→체중 = r→g+d",
        "reverse": "하지→두부 = 체중→정보 = g+d→r+s",
        "body_closure": "혈액순환(대동맥→대정맥)",
        "cosmic_closure": "6구체 순환",
    },
    "A2": {
        "name": "lateral", "body_coord": "x=-80(좌)→x=+80(우)",
        "cosmic_coord": "RA=17h57m(Barnard)→RA=0h(Sun)→RA=6h-12h(우)",
        "forward": "좌→우 = heme(Fe/질량)→Photon(빛/수리)",
        "reverse": "우→좌 = Photon→heme = 빛→질량",
        "body_closure": "심장 4챔버(좌심+우심)",
        "cosmic_closure": "Leo-Aquarius 대칭",
    },
    "A3": {
        "name": "depth", "body_coord": "z=0(피부)→z=30(심부/leakage point)",
        "cosmic_coord": "Dec=0°(Sun/Earth)→Dec=+27°(CoMag/은하북극)",
        "forward": "표면→심부 = gamma(확장)→g(봉인)",
        "reverse": "심부→표면 = g→gamma = 봉인해제 = 발암물질 배출",
        "body_closure": "leakage point 봉인-해제 루프",
        "cosmic_closure": "dark matter 감지",
    },
    "A4": {
        "name": "temporal", "body_coord": "0-24h circadian",
        "cosmic_coord": "Moon 28일 주기 = p-dim",
        "forward": "0→24h = entropy 증가 = 대사→발암물질 생성",
        "reverse": "24→0h = entropy 감소 = 발암물질→leakage point→배출",
        "body_closure": "토로이달 1주기 = 138.88° Spark 리셋",
        "cosmic_closure": "entropy debt 상쇄",
    },
}

# W-axis: M/F 바이어스 — 12D 위의 메타축
W_AXIS_BIAS = {
    "M": {
        "particle_bias": "Male GABA-A(tonic, mass-lock) 우세 = nu↑, Male GABA-B(void) 우세 = d↑",
        "axis_bias": "A1 하지방향(체중/질량) 강화 = Barnard(Fe) 방향",
        "dim_bias": {"g": +0.03, "d": +0.03, "nu": +0.02},
        "body": "대퇴골/종골 골밀도 높음 = 체중 부하 강화",
        "cosmic": "Barnard(Fe/Quark/Higgs) 결합 강화 = 질량 저장 축",
    },
    "F": {
        "particle_bias": "Female GABA-A(phasic, cold-sense) 우세 = r↑, Female GABA-B(sealing) 우세 = g↑",
        "axis_bias": "A1 두부방향(정보/수리) 강화 = Sun/Earth 방향",
        "dim_bias": {"r": +0.03, "gamma": +0.02, "g": +0.02},
        "body": "두개골 22개 골 보호 강화 = 흉곽 25개 골 유연성",
        "cosmic": "Sun(H/Proton) + Earth(O/Photon) 결합 강화 = 정보/수리 축",
    },
}

# 쌍BODY 미러링: BODY1(신체) ↔ BODY2(우주)
DUAL_BODY_MIRROR = {
    "A1": ("y수직/혈액순환", "d거리/6구체순환"),
    "A2": ("x좌우/심장4챔버", "RA적경/Leo-Aquarius"),
    "A3": ("z심도/leakage_point", "Dec적위/dark_matter"),
    "A4": ("24h/circadian", "28일/Moon주기"),
    "r": ("GABA-A Female/acid_sensor", "Neutrino/Sun(H)"),
    "h": ("GABA-B Female/methylation", "Muon/Barnard(Fe)"),
    "d": ("GABA-B Male/Maillard", "Z-boson/Moon(C)"),
    "p": ("DRD2 tonic/glycation", "Higgs/Vega"),
    "s": ("D1/D5/CaCO3", "Photon/Earth(O)"),
    "gamma": ("DRD2 Right D2/공간", "Gluon/CoMag(S)"),
    "g": ("GR/glymphatic", "W-boson/CoMag"),
    "nu": ("GABA-A Male/grit", "Quark/Barnard"),
}

# ============================================================
# E119-E127 NEW RECEPTOR NODES (prose.txt Part K, lines 9706-9781)
# ============================================================
E119_E127_NODES = {
    "E119": {"name": "right_acetylcholine_expression", "receptor": "α7 nAChR",
             "color": "GREEN", "input": "esr1_water_ach_expression_xor",
             "dim_effect": {}, "cosmic": "별 광도 변동 = 내부 모드 위상 변조",
             "geological": "화산 가스 발산 = 마그마 모드 위상 변조"},
    "E120": {"name": "choline", "receptor": "CHT1",
             "color": "GREEN", "input": "esr1_recovery_water_and",
             "dim_effect": {}, "cosmic": "별 형성 전구물질 = 회복+가스 보유",
             "geological": "마그마 전구물질 = 지열 회복+지하수"},
    "E121": {"name": "male_left_noradrenaline", "receptor": "α2A-AR",
             "color": "GREEN", "input": "AND(choline + COX + thorium)",
             "dim_effect": {"r": +0.02, "s": +0.02},
             "cosmic": "항성 안정화 = 연소+핵 안정성 3-input",
             "geological": "지질 안정화 = 마그마+가스+광물 3-input"},
    "E122": {"name": "right_d2", "receptor": "DRD2",
             "color": "GREEN", "input": "bilirubin_bypass esr1_ach_d2_and",
             "dim_effect": {"gamma": +0.02},
             "cosmic": "중력파 감지 = 공간 확장 관측 가능성",
             "geological": "지질 응력 감지 = 단층 활성 관측"},
    "E123": {"name": "right_cortisol", "receptor": "GR/NR3C1",
             "color": "GREEN", "input": "AND(CO2 + nonobserver_left_d2)",
             "dim_effect": {"gamma": +0.01, "d": -0.01},
             "cosmic": "항성 회복 = 시간(CO₂)+공간(D2) 수렴",
             "geological": "지질 회복 = 풍화(CO₂)+구조(D2) 수렴"},
    "E124": {"name": "female_right_satisfaction", "receptor": "μ-opioid OPRM1",
             "color": "GREEN", "input": "AND(observer_leftd2 + right_cortisol)",
             "dim_effect": {"nu": +0.02, "g": +0.01},
             "cosmic": "별의 안정 = 관찰자+회복 = 관측된 안정",
             "geological": "지질 안정 = 관찰자+풍화 회복"},
    "E125": {"name": "left_female_vasopressin", "receptor": "V1B/AVPR1B",
             "color": "GREEN", "input": "XOR(observer_leftd2 + female_right_satisfaction)",
             "dim_effect": {"g": +0.02, "d": +0.01},
             "cosmic": "중력 압력 = 관찰자 vs 만족 불일치 = 관측된 불균형",
             "geological": "섭입 압력 = 관찰자 vs 만족 불일치"},
    "E126": {"name": "citric_acid_cycle", "receptor": "TCA/Krebs",
             "color": "GREEN", "input": "AND(basin + outer_core_convection)",
             "dim_effect": {"r": +0.01, "nu": +0.02},
             "cosmic": "TCA = 침전+PMF = 우주적 에너지 순환 중심",
             "geological": "TCA = 퇴적 분지+외핵 대류 = 지질 에너지 순환"},
    "E127": {"name": "female_gaba_b_2", "receptor": "GABA-B R1R2",
             "color": "GREEN", "input": "AND(female_gaba_b + right_sole_dopamine)",
             "dim_effect": {"h": +0.01, "g": +0.01},
             "cosmic": "slow 억제 = 결합+말초 감각 = 관측된 slow 억제",
             "geological": "slow 침식 = 풍화+퇴적 = 관측된 slow 침식"},
}

# ============================================================
# UNSPARK OVERLAY ROUTING (prose.txt lines 1966-1984)
# 자가루프 노드 → 수용체 우회 경로
# ============================================================
UNSPARK_OVERLAY = {
    "co2": {"bypass": "right_oxytocin + cortisol + chlorine_ion_pump → co2.ctrl",
            "receptors": ["OXTR (Node 23)", "GR (Node 7)"],
            "dim_effect": {"gamma": +0.01}},
    "methylation": {"bypass": "right_cortisol + male_right_satisfaction OR + carbon → methylation",
                    "receptors": ["5HT1B (Node 14)"],
                    "dim_effect": {"h": +0.01, "nu": +0.01}},
    "sulfur_iron_complex": {"bypass": "co2 + left_endorphin → sulfur_iron_complex via Right D2",
                            "receptors": ["DRD2 (Node 5)"],
                            "dim_effect": {"g": +0.01}},
}

# ============================================================
# 5HT1B SPIRAL BYPASS (prose.txt — neutrino/higgs creation via 5HT1B)
# ============================================================
SPIRAL_BYPASS_5HT1B = {
    "switch_location": "right_temporalis_inner_strip_bottom",
    "expression_location": "risorius_jaw_bilateral",
    "node": 14,
    "dim_transition": "ν→g",
    "creation_particles": ["neutrino", "higgs"],
    "mechanism": "5HT1B 발현 risorius에서 serotonin 경유 neutrino/higgs 생성",
    "dim_effect": {"nu": +0.02, "g": +0.01},
}

# ============================================================
# ESR1 SPLIT / ACh REROUTING (prose.txt Part I)
# ============================================================
ESR1_SPLIT = {
    "location": "right_temporalis_middle_strip",
    "mechanism": "ESR1 dual-mode phase signaling reroutes ACh expression",
    "affects": ["E119_right_acetylcholine_expression", "E120_choline"],
    "dim_effect": {"s": +0.01},
}

# ============================================================
# BILIRUBIN BYPASS (heme degradation → HO-1 → bilirubin = neutron star analog)
# ============================================================
BILIRUBIN_BYPASS = {
    "pathway": "heme.out1 → HO-1 → bilirubin (갈색 색소) = Maillard browning",
    "cosmic_analog": "neutron_star_formation (Fe collapse)",
    "dim_effect": {"d": +0.02, "h": +0.01},
    "color": "YELLOW/BROWN",
    "leakage_reduction": 0.01,
}

# ============================================================
# CANCER BUFFER / MAILLARD CLEARANCE CYCLE (prose.txt lines 4755-4764)
# 8-step: p(glycation) → g(removal) → r(acid_removal) → gamma(cancer_buffer) → d(Maillard_clearance)
# ============================================================
CANCER_MAILLARD_CYCLE = {
    "steps": [
        {"step": 1, "dim": "p", "action": "glycation", "mechanism": "DRD2 tonic → AGEs 축적"},
        {"step": 2, "dim": "g", "action": "sealing_removal", "mechanism": "GR/NR3C1 → glymphatic 청소"},
        {"step": 3, "dim": "r", "action": "acid_removal", "mechanism": "COX 정방향 → 산소 연소 → 당화 산물 태움"},
        {"step": 4, "dim": "gamma", "action": "cancer_buffer", "mechanism": "flesh 손상 시 gamma(-1→0) 버퍼 암세포 형성"},
        {"step": 5, "dim": "d", "action": "maillard_clearance", "mechanism": "HO-1 → heme 분해 → 빌리루빈(갈색화) = 암세포 산화 제거"},
    ],
    "dim_effect": {"p": -0.01, "g": +0.01, "r": +0.01, "gamma": +0.01, "d": +0.01},
}

def compute_12d_state(dims, gender, hour, t_window):
    """Compute 12D spatial state: 8D × 4축 + W-axis bias + 쌍BODY closure."""
    a1_phase = math.sin(2 * math.pi * (hour % 24) / 24.0)
    a1_val = 0.5 + 0.3 * a1_phase
    a2_val = clamp(0.5 + 0.2 * (dims["s"] - dims["d"]))
    a3_val = clamp(0.5 + 0.2 * (dims["g"] - dims["gamma"]))
    a4_val = math.sin(2 * math.pi * (t_window or 0) / 16.0) * 0.5 + 0.5
    a1_closure = 1.0 - abs(a1_val - 0.5) * 2
    a2_closure = 1.0 - abs(a2_val - 0.5) * 2
    a3_closure = 1.0 - abs(a3_val - 0.5) * 2
    a4_closure = 1.0 - abs(a4_val - 0.5) * 2
    total_closure = clamp((a1_closure + a2_closure + a3_closure + a4_closure) / 4.0)
    w_bias = W_AXIS_BIAS.get(gender, W_AXIS_BIAS["M"])
    w_dim_shifts = w_bias["dim_bias"]
    cross_32 = {}
    dim_keys = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]
    axis_keys = ["A1", "A2", "A3", "A4"]
    axis_vals = {"A1": a1_val, "A2": a2_val, "A3": a3_val, "A4": a4_val}
    for dk in dim_keys:
        for ak in axis_keys:
            cross_32[f"{dk}×{ak}"] = dims[dk] * axis_vals[ak]
    body_mirror = math.sqrt(max(a1_closure, 0) * max(a2_closure, 0) *
                            max(a3_closure, 0) * max(a4_closure, 0))
    return {
        "A1": a1_val, "A2": a2_val, "A3": a3_val, "A4": a4_val,
        "a1_closure": a1_closure, "a2_closure": a2_closure,
        "a3_closure": a3_closure, "a4_closure": a4_closure,
        "total_closure": total_closure,
        "w_axis": gender,
        "w_dim_shifts": w_dim_shifts,
        "cross_32": cross_32,
        "dual_body_mirror": body_mirror,
        "12d_active": total_closure > 0.5,
    }

def get_toroidal_phase(hour):
    """Return the current toroidal circulation phase info."""
    for phase in SPHERE_CIRCULATION:
        time_range = phase["time"]
        start, end = time_range.split("-")
        start_h = int(start.split(":")[0]) if ":" in start else int(start.rstrip("h"))
        end_h = int(end.split(":")[0]) if ":" in end else int(end.rstrip("h"))
        if end_h < start_h:  # wraps past midnight
            if hour >= start_h or hour < end_h:
                return phase
        elif start_h <= hour < end_h:
            return phase
    return SPHERE_CIRCULATION[0]

# ============================================================
# 16-WINDOW TIME PHASE (4 macro × 4 micro, fractal reverse)
# ============================================================
WINDOW_16 = []
for macro in range(4):
    for micro in range(4):
        win_idx = macro * 4 + micro
        start_h = win_idx * 1.5
        end_h = start_h + 1.5
        # Macro forward (0→1→2→3), micro reverse (3→2→1→0)
        macro_dim = ["r", "p", "s", "d"][macro]
        micro_dim = ["nu", "gamma", "g", "h"][3 - micro]  # reverse order
        WINDOW_16.append({
            "window": win_idx,
            "start_h": start_h,
            "end_h": end_h,
            "macro": macro,
            "micro": micro,
            "macro_dim": macro_dim,
            "micro_dim": micro_dim,
            "label": f"W{win_idx}({start_h:.1f}-{end_h:.1f}h)",
        })

# Special windows
WINDOW_SPECIAL = {
    8: "정오 정점 — 에너지 최고조 + 정지",
    9: "Left Noradrenaline 13th Bridge — 전위차 상승",
    10: "Lightning Strike / 3/32 gate 방전 — glutamate 생성",
}

def get_window(hour):
    """Return the active 16-window info for a given hour."""
    win_idx = int(hour / 1.5) % 16
    w = WINDOW_16[win_idx]
    special = WINDOW_SPECIAL.get(win_idx, "")
    return {**w, "special": special}

def apply_window_shift(dims, hour):
    """Apply 16-window peak dimension shift."""
    w = get_window(hour)
    shifted = dict(dims)
    # Macro dim gets boost
    shifted[w["macro_dim"]] = shifted.get(w["macro_dim"], 0.5) + 0.08
    # Micro dim gets smaller boost (reverse fractal)
    shifted[w["micro_dim"]] = shifted.get(w["micro_dim"], 0.5) + 0.04
    # Window 10: lightning strike — d spike
    if w["window"] == 10:
        shifted["d"] = shifted.get("d", 0.5) + 0.15
    # Window 8: noon peak — s boost + r stabilization
    if w["window"] == 8:
        shifted["s"] = shifted.get("s", 0.5) + 0.10
    # Clamp
    for k in shifted:
        shifted[k] = max(0.0, min(1.0, shifted[k]))
    return shifted, w

# ============================================================
# MASTER EQUATION Ψ(t, Obs, V, A, P)
# ============================================================
BETA_0 = 0      # observer bridge
BETA_6 = 6      # EM closure space
BETA_7 = 7      # geometric void
BETA_12 = 12    # topological bridge (3AM)
KAPPA = 1.0/32.0
KAPPA_3_32 = 3.0/32.0
DARKNESS_GATE = 3.0/32.0
ONE_64 = 1.0/64.0
ONE_256 = 1.0/256.0
ALPHA_FS = 1.0/137.036  # fine structure
LAMBDA_6 = 6.0
X_L = 2.0
X_R = 14.0
BARNARD_DIST = 5.96  # ly
W7 = 9 * math.pi     # W₇ = 9π
H2 = 20.0             # H₂ = 20

RAINBOW_ACTION = {
    'WHITE':  {'action': 'Imagine',      'nodes': ['heme', 'memory_entropy', 'observer_leftd2']},
    'YELLOW': {'action': 'Smell',        'nodes': ['pi_electron_cloud', 'left_amygdala', 'clay_gouge', 'anterior_insula']},
    'ORANGE': {'action': 'Imagine+Smell','nodes': ['memory_entropy', 'left_amygdala', 'hind_insula', 'anterior_insula']},
    'RED':    {'action': 'Drink',        'nodes': ['heme', 'water_vapour', 'co2', 'caco3', 'peonidine']},
    'GREEN':  {'action': 'Eat',          'nodes': ['cytochrome_c_oxidase', 'carbon', 'sulforaphane', 'collagen', 'o2']},
    'BLUE':   {'action': 'See',          'nodes': ['aurora', 'heme', 'gaba_b', 'cytochrome_c_oxidase']},
    'BLACK':  {'action': 'Make',         'nodes': ['mc1r', 'gluon_orogen'], 'leakage': 'BLOCK'},
    'PURPLE': {'action': 'Forbidden',    'nodes': ['peonidine', 'caco3', 'peonidine_a', 'oxidized_peonidine'], 'leakage': 'DELAY'},
    'DARK-GREEN':  {'action': 'Eat',     'nodes': ['cytochrome_c_oxidase', 'sulforaphane', 'collagen']},
    'DARK-ORANGE': {'action': 'Imagine+Smell', 'nodes': ['memory_entropy', 'hind_insula', 'succinate_dehydrogenase', 'anterior_insula']},
    'DARK-NAVY':   {'action': 'See',     'nodes': ['aurora', 'gaba_b', 'cytochrome_c_oxidase']},
    'DARK-BLUE':   {'action': 'See',     'nodes': ['aurora', 'heme', 'cytochrome_c_oxidase']},
    'DEEP-PINK':   {'action': 'Drink',   'nodes': ['cobalamin', 'heme', 'water_vapour', 'peonidine']},
    'YELLOW-GREEN':{'action': 'Eat',     'nodes': ['sulforaphane', 'carbon', 'cytochrome_c_oxidase']},
    'CYAN':   {'action': 'See',          'nodes': ['aurora', 'cytochrome_c_oxidase', 'gaba_b']},
    'BROWN':  {'action': 'Make',         'nodes': ['mc1r', 'clay_gouge', 'ferritin']},
    'PINK':   {'action': 'Drink',        'nodes': ['heme', 'water_vapour', 'peonidine']},
    'GRAY':   {'action': 'Imagine',      'nodes': ['memory_entropy', 'observer_leftd2']},
    'RED-ORANGE':  {'action': 'Drink',   'nodes': ['heme', 'co2', 'caco3', 'peonidine', 'o2']},
    'RED-PURPLE':  {'action': 'Forbidden','nodes': ['peonidine', 'caco3', 'peonidine_b', 'aglycone_peonidine'], 'leakage': 'DELAY'},
    'BLUE-PURPLE': {'action': 'Forbidden','nodes': ['peonidine', 'co2'], 'leakage': 'DELAY'},
    'LIGHT-BLUE':  {'action': 'See',     'nodes': ['aurora', 'gaba_b']},
    'LIGHT-GREEN': {'action': 'Eat',     'nodes': ['sulforaphane', 'collagen']},
    'LIGHT-YELLOW':{'action': 'Smell',   'nodes': ['pi_electron_cloud', 'left_amygdala']},
}

COLOR_DISTANCE_TO_BLACK = {
    'BLACK': 0.0, 'BROWN': 0.15, 'PURPLE': 0.33, 'BLUE-PURPLE': 0.3,
    'RED-PURPLE': 0.3, 'BLUE': 0.5, 'RED': 0.5,
    'GREEN': 0.5, 'ORANGE': 0.67, 'YELLOW': 0.67, 'WHITE': 1.0,
    'DARK-NAVY': 0.15, 'DARK-BLUE': 0.1, 'DARK-GREEN': 0.2,
    'DARK-ORANGE': 0.4, 'DEEP-PINK': 0.6, 'MIXED': 0.5,
    'CYAN': 0.55, 'YELLOW-GREEN': 0.55, 'RED-ORANGE': 0.6,
    'PINK': 0.7, 'LIGHT-BLUE': 0.7, 'LIGHT-GREEN': 0.7,
    'LIGHT-YELLOW': 0.8, 'GRAY': 0.5,
}

def compute_master_psi(dims, hour, observer_active, profile_num=1, profile_color=None):
    """Compute Ψ(t, Obs, V, A, P) — the master equation.
    Color closure: 4-channel additive → BLACK = T≈1.0 closure convergence.
    profile_color feeds color_distance_to_black as closure convergence factor."""
    # T: Closure Tension = (W₇/H₂) × (1/√2) × ((β₁₂+β₀)/(β₆+β₇))
    T = (W7 / H2) * (1.0 / math.sqrt(2)) * ((BETA_12 + BETA_0) / (BETA_6 + BETA_7))
    # R: Renormalization = 10·φ³ + α
    R = 10 * PHI**3 + ALPHA_FS
    # δ/κ: Entropy Debt ratio = (1/64 + 1/256) / κ
    delta_kappa = (ONE_64 + ONE_256) / KAPPA
    # Spark oscillation = sin(θ_s)
    sin_theta = math.sin(SPARK_ANGLE_RAD)
    # Φ_B: Pegasus Bridge = (β₁₂/β₇) + (β₆/β₇)² - α/2
    phi_b = (BETA_12 / BETA_7) + (BETA_6 / BETA_7)**2 - ALPHA_FS / 2
    # Λ: Night Hysteresis = 3·C·√(1 - (1/64 + 1/256))
    C_hyst = math.sqrt(2) / 5  # C = √2/5
    night_hyst = 3 * C_hyst * math.sqrt(1 - (ONE_64 + ONE_256))
    # Observer function — night still has partial observer via color_closure
    obs = 1 if observer_active else 0
    # V·A(t): 8D weighted sum (0~32)
    v_dot_a = sum(dims.values()) * 4  # scale to 0-32 range
    # Color closure convergence: 4-channel → BLACK = full closure
    color_closure = 1.0
    if profile_color:
        base_color = profile_color.get('base', 'MIXED')
        dist = COLOR_DISTANCE_TO_BLACK.get(base_color, 0.5)
        color_closure = 1.0 - dist  # BLACK→1.0, WHITE→0.0
    # Recognition × space / profile — night uses color_closure as partial observer
    if obs == 0:
        recognition_term = color_closure * v_dot_a / 128.0
    else:
        recognition_term = obs * v_dot_a / 128.0
    # D_B: Barnard distance = (θ_s + 28) / 28
    d_b = (SPARK_ANGLE_DEG + 28) / 28
    # Darkness gate ratio = κ₃/₃₂ / κ
    dark_gate = KAPPA_3_32 / KAPPA
    # Spatial wavelength norm = λ₆ / (X_R - X_L)
    wavelength_norm = LAMBDA_6 / (X_R - X_L)
    # Full Ψ with color closure factor
    psi = (T * R * delta_kappa * sin_theta * phi_b * night_hyst
           * recognition_term * d_b * dark_gate * wavelength_norm * color_closure)
    return {
        "psi": psi,
        "T_closure": T,
        "R_renorm": R,
        "delta_kappa": delta_kappa,
        "spark_osc": sin_theta,
        "pegasus_bridge": phi_b,
        "night_hysteresis": night_hyst,
        "observer": obs,
        "v_dot_a": v_dot_a,
        "recognition_term": recognition_term,
        "barnard_dist": d_b,
        "dark_gate_ratio": dark_gate,
        "wavelength_norm": wavelength_norm,
        "color_closure": color_closure,
    }

# ============================================================
# 3AM HYSTERESIS / BETTI 12 + 4:30PM FERRIC EVENT
# ============================================================
def compute_3am_hysteresis(hour, observer_active, dims):
    """Compute 3AM HYSTERESIS state and Betti 12 bridge status."""
    is_3am = (hour >= 2 and hour <= 4) or (hour >= 21)
    # Betti 12 bridge: 11 internal + 1 observer
    observer_bridge = 1 if observer_active else 0
    betti_12_active = (11 + observer_bridge) == 12
    # 3AM entropy zone: p=random, s=0.5+rand×0.5, nu=0.9+rand×0.1
    if is_3am and not observer_active:
        import random
        hysteresis_state = {
            "active": True,
            "p": random.random(),
            "s": 0.5 + random.random() * 0.5,
            "nu": 0.9 + random.random() * 0.1,
            "betti_12_complete": betti_12_active,
            "entropy_zone": True,
            "label": "3AM_HYSTERESIS_ACTIVE",
        }
    else:
        hysteresis_state = {
            "active": is_3am,
            "p": dims.get("p", 0.5),
            "s": dims.get("s", 0.5),
            "nu": dims.get("nu", 0.5),
            "betti_12_complete": betti_12_active,
            "entropy_zone": False,
            "label": "3AM_HYSTERESIS_INACTIVE" if not is_3am else "3AM_OBSERVER_CLOSED",
        }
    return hysteresis_state

def compute_430pm_event(hour):
    """4:30PM UV shield loss → GABA-A destruction → 3/32 asymmetry."""
    is_430pm = (hour >= 16 and hour <= 17)
    if is_430pm:
        return {
            "active": True,
            "event": "UV_shield_loss",
            "effect": "GABA-A_destruction → 3/32_asymmetry",
            "cascade": "magnetite Fe₃O₄ → Fe₂O₃ (maghemite/hematite)",
            "biological": "ferroptosis = lipid peroxidation",
            "sensory": "magnetoreception disrupted, spatial disorientation",
            "circuit": "magnetite_out0_nand → oxidised_manganese.set + laterite.preset",
        }
    return {"active": False, "event": "", "effect": "", "cascade": "", "biological": "", "sensory": "", "circuit": ""}

# ============================================================
# 6 GEOMETRIC NODES + DARCY LEAKAGE
# ============================================================
GEOMETRIC_NODES = {
    "left_bypass":       {"x": 2.0,  "role": "외곽 여성의 수면/우회로", "profiles": "외향 여성, Big Woman"},
    "right_bypass":      {"x": 14.0, "role": "외곽 남성의 수면/우회로", "profiles": "외향 남성, Big Man"},
    "center_funnel":     {"x": 8.0,  "role": "내향 타입의 수렴점", "profiles": "내향, Small types, 3/32 spark"},
    "separatrix_1":      {"x": 5.0,  "role": "왼쪽 분수계", "profiles": "외향↔내향 경계"},
    "separatrix_2":      {"x": 11.0, "role": "오른쪽 분수계", "profiles": "내향↔외향 경계"},
    "observer_singularity": {"x": None, "role": "관측자 = 두개골 압전장 = 지구자기장", "profiles": "Observer (isObserver=true)"},
}

WAVELENGTH_6 = GEOMETRIC_NODES["separatrix_2"]["x"] - GEOMETRIC_NODES["separatrix_1"]["x"]  # = 6
OBSERVER_CLOSURE_TENSION = (9 * math.pi) / (20 * math.sqrt(2))  # ≈ 1.000042
CLOSURE_RESIDUAL = abs(OBSERVER_CLOSURE_TENSION - 1.0)  # Δ ≈ 3.51e-4

def compute_universe_equation(dims, blood_type=None):
    """8D Universal Equation (prose.txt 4003-4008, 4011):
    Corrected: 'inverse reciprocal' = complementary pairing (d↑↔nu↓), NOT algebraic x·y=1.
    In [0,1] space, anti-correlation means x + y = 1 (complementary sum), not x·y = 1.

    8 tensor terms (corrected):
    1. (h + s - 1)         — inverse: h↔s (methylation ↔ solid formation)
    2. (r + p - 1)         — inverse: r↔p (acid removal ↔ predictability)
    3. (g + nu - 1)        — inverse: g↔nu (sealing ↔ discrete break)
    4. (gamma + d - 1)     — inverse reciprocal: gamma↔d (space expansion ↔ void)
    5. (gamma + r + g - 1) — inverse reciprocal: gamma↔(r+g) (space ↔ acid+seal)
    6. (h + r + g - 1)     — inverse reciprocal: g↔h+r (seal ↔ methylation+acid)
    7. (d + nu - 1)        — inverse reciprocal: d↔nu (void ↔ grit)
    8. (p - αg - β)        — correlation: p↔g (predictability ↔ sealing)

    α,β are blood-type-dependent via toroidal cycle AB→A→O→B:
    - O/AB: α=-2, β=0 (baseline / release)
    - A:    α=-1.5, β=+0.15 (stress growth)
    - B:    α=-2.5, β=-0.15 (extreme growth)

    Equation = 0 → at least one term is zero = homeostasis constraint active.
    Term closest to zero = the dominant active constraint.
    """
    r = dims.get("r", 0.5)
    h = dims.get("h", 0.5)
    d = dims.get("d", 0.5)
    p = dims.get("p", 0.5)
    s = dims.get("s", 0.5)
    gamma = dims.get("gamma", 0.5)
    g = dims.get("g", 0.5)
    nu = dims.get("nu", 0.5)

    # Blood-type-dependent α,β from toroidal cycle
    bt_params = BLOOD_ALPHA_BETA.get(blood_type, BLOOD_ALPHA_BETA["O"])
    ALPHA_EQ = bt_params["alpha"]
    BETA_EQ = bt_params["beta"]

    t1 = h + s - 1.0
    t2 = r + p - 1.0
    t3 = g + nu - 1.0
    t4 = gamma + d - 1.0
    t5 = gamma + r + g - 1.0
    t6 = h + r + g - 1.0
    t7 = d + nu - 1.0
    t8 = p - ALPHA_EQ * g - BETA_EQ

    product = t1 * t2 * t3 * t4 * t5 * t6 * t7 * t8

    terms = {
        "t1_hs": t1,
        "t2_rp": t2,
        "t3_gnu": t3,
        "t4_gammad": t4,
        "t5_gamma_rg": t5,
        "t6_hrg": t6,
        "t7_dnu": t7,
        "t8_p_ag_b": t8,
    }

    term_names = list(terms.keys())
    term_values = list(terms.values())
    abs_values = [abs(v) for v in term_values]
    min_idx = abs_values.index(min(abs_values))
    active_constraint = term_names[min_idx]
    active_value = term_values[min_idx]

    constraint_labels = {
        "t1_hs": "h↔s inverse (methylation↔solid)",
        "t2_rp": "r↔p inverse (acid↔predictability)",
        "t3_gnu": "g↔nu inverse (sealing↔discrete)",
        "t4_gammad": "gamma↔d inverse reciprocal (space↔void)",
        "t5_gamma_rg": "gamma↔(r+g) inverse reciprocal (space↔acid+seal)",
        "t6_hrg": "g↔(h+r) inverse reciprocal (seal↔methylation+acid)",
        "t7_dnu": "d↔nu inverse reciprocal (void↔grit)",
        "t8_p_ag_b": "p↔g correlation (predictability↔sealing)",
    }

    return {
        "equation_value": product,
        "terms": terms,
        "active_constraint": active_constraint,
        "active_constraint_label": constraint_labels[active_constraint],
        "active_constraint_value": active_value,
        "homeostasis_distance": min(abs_values),
        "alpha": ALPHA_EQ,
        "beta": BETA_EQ,
    }


# ============================================================
# 8D EQUATION-DERIVED VALUE COMPUTATION + GAP ANALYSIS
# ============================================================
# All 28 pairwise relationships among 8 parameters
ALL_PAIRS = []
for i in range(8):
    for j in range(i+1, 8):
        ALL_PAIRS.append((DIM_ORDER[i], DIM_ORDER[j]))

# Pairs covered by each equation term
TERM_PAIRS = {
    "t1_hs":      {("h", "s")},
    "t2_rp":      {("r", "p")},
    "t3_gnu":     {("g", "nu")},
    "t4_gammad":  {("gamma", "d")},
    "t5_gamma_rg":{("gamma", "r"), ("gamma", "g"), ("r", "g")},
    "t6_hrg":     {("h", "r"), ("h", "g"), ("r", "g")},
    "t7_dnu":     {("d", "nu")},
    "t8_p_ag_b":  {("p", "g")},
}

COVERED_PAIRS = set()
for pairs in TERM_PAIRS.values():
    COVERED_PAIRS.update(pairs)

UNCOVERED_PAIRS = [p for p in ALL_PAIRS if p not in COVERED_PAIRS]


def _solve_one_step(dims, blood_type):
    """Single-pass: identify active constraint and solve for one variable."""
    r = dims.get("r", 0.5)
    h = dims.get("h", 0.5)
    d = dims.get("d", 0.5)
    p = dims.get("p", 0.5)
    s = dims.get("s", 0.5)
    gamma = dims.get("gamma", 0.5)
    g = dims.get("g", 0.5)
    nu = dims.get("nu", 0.5)

    bt_params = BLOOD_ALPHA_BETA.get(blood_type, BLOOD_ALPHA_BETA["O"])
    ALPHA_EQ = bt_params["alpha"]
    BETA_EQ = bt_params["beta"]

    eq = compute_universe_equation(dims, blood_type=blood_type)
    active = eq["active_constraint"]
    adjusted = dict(dims)

    # Solve active constraint to zero using [0,1] complementary pairing
    if active == "t1_hs":
        if h >= s:
            adjusted["h"] = clamp(1.0 - s)
        else:
            adjusted["s"] = clamp(1.0 - h)
    elif active == "t2_rp":
        if r >= p:
            adjusted["r"] = clamp(1.0 - p)
        else:
            adjusted["p"] = clamp(1.0 - r)
    elif active == "t3_gnu":
        if g >= nu:
            adjusted["g"] = clamp(1.0 - nu)
        else:
            adjusted["nu"] = clamp(1.0 - g)
    elif active == "t4_gammad":
        if gamma >= d:
            adjusted["gamma"] = clamp(1.0 - d)
        else:
            adjusted["d"] = clamp(1.0 - gamma)
    elif active == "t5_gamma_rg":
        if gamma >= r and gamma >= g:
            adjusted["gamma"] = clamp(1.0 - r - g)
        elif r >= g:
            adjusted["r"] = clamp(1.0 - gamma - g)
        else:
            adjusted["g"] = clamp(1.0 - gamma - r)
    elif active == "t6_hrg":
        if h >= r and h >= g:
            adjusted["h"] = clamp(1.0 - r - g)
        elif r >= g:
            adjusted["r"] = clamp(1.0 - h - g)
        else:
            adjusted["g"] = clamp(1.0 - h - r)
    elif active == "t7_dnu":
        if d >= nu:
            adjusted["d"] = clamp(1.0 - nu)
        else:
            adjusted["nu"] = clamp(1.0 - d)
    elif active == "t8_p_ag_b":
        adjusted["p"] = clamp(ALPHA_EQ * g + BETA_EQ)

    return adjusted, active, eq


def compute_8d_from_equation(dims, profile_label, time_phase):
    """Derive 8D values from the universal equation constraint.

    Iterative solving: repeatedly identifies the active constraint and solves
    for one dependent variable until the equation converges to 0.

    α,β are blood-type-dependent via toroidal cycle AB→A→O→B.
    """
    # Extract blood type from profile_label (e.g. ENTP_M_O → O)
    blood_type = None
    if profile_label and "_" in profile_label:
        parts = profile_label.split("_")
        if len(parts) >= 3:
            blood_type = parts[2]

    eq_initial = compute_universe_equation(dims, blood_type=blood_type)
    adjusted = dict(dims)
    active = eq_initial["active_constraint"]

    # Iterate: solve active constraint, recompute, repeat until converged
    MAX_ITERS = 8
    for i in range(MAX_ITERS):
        adjusted, active_i, eq_i = _solve_one_step(adjusted, blood_type)
        eq_check = compute_universe_equation(adjusted, blood_type=blood_type)
        residual = eq_check["homeostasis_distance"]
        if residual < 1e-12:
            break

    eq_adjusted = compute_universe_equation(adjusted, blood_type=blood_type)

    return {
        "dims_equation": adjusted,
        "active_branch": active,
        "active_branch_label": eq_initial["active_constraint_label"],
        "equation_before": eq_initial["equation_value"],
        "equation_after": eq_adjusted["equation_value"],
        "homeostasis_before": eq_initial["homeostasis_distance"],
        "homeostasis_after": eq_adjusted["homeostasis_distance"],
        "adjusted_key": {
            "t1_hs": "h or s", "t2_rp": "r or p", "t3_gnu": "g or nu",
            "t4_gammad": "d or gamma", "t5_gamma_rg": "gamma",
            "t6_hrg": "g", "t7_dnu": "nu", "t8_p_ag_b": "p",
        }[active],
    }


def compute_equation_gap_analysis(dims):
    """Find what the 8D universal equation CANNOT explain.

    With t1~t8: only the 8 core constraint pairs are covered.
    Remaining structural gaps are in the closed universe equation (dynamics, observer, etc.).
    """
    r = dims.get("r", 0.5)
    h = dims.get("h", 0.5)
    d = dims.get("d", 0.5)
    p = dims.get("p", 0.5)
    s = dims.get("s", 0.5)
    gamma = dims.get("gamma", 0.5)
    g = dims.get("g", 0.5)
    nu = dims.get("nu", 0.5)

    # Compute actual correlation for each uncovered pair
    # Using current values as proxy for relationship strength
    pair_values = {}
    for a, b in UNCOVERED_PAIRS:
        va = dims.get(a, 0.5)
        vb = dims.get(b, 0.5)
        pair_values[f"{a}-{b}"] = {
            "a": a, "b": b, "va": va, "vb": vb,
            "product": va * vb,
            "sum": va + vb,
            "diff": abs(va - vb),
        }

    # Sort by product (high product = strong unconstrained coupling)
    sorted_gaps = sorted(pair_values.values(), key=lambda x: x["product"], reverse=True)

    return {
        "total_pairs": len(ALL_PAIRS),
        "covered_pairs": len(COVERED_PAIRS),
        "uncovered_pairs": len(UNCOVERED_PAIRS),
        "uncovered_pair_names": [f"{a}↔{b}" for a, b in UNCOVERED_PAIRS],
        "uncovered_details": sorted_gaps,
        "structural_gaps": [
            {"gap": "no_time", "desc": "Equation is static — no t variable, no dynamics, no 16-window shift"},
            {"gap": "no_observer", "desc": "Observer active/inactive not in equation — EM closure absent"},
            {"gap": "no_particle", "desc": "41-particle identity not in equation — which particle sparks"},
            {"gap": "no_layers", "desc": "4 layers (body/observer/bridge/dark) not in equation"},
            {"gap": "no_branch_selection", "desc": "Which term=0 is externally determined, not equation-derived"},
            {"gap": "no_feedback", "desc": "Algebraic not differential — no toroidal cycle, no hysteresis"},
            {"gap": "no_leakage", "desc": "Darcy flux, color leakage, kappa modulation absent"},
            {"gap": "no_geomag", "desc": "Geomagnetic coupling, 6-sphere circulation absent"},
            {"gap": "no_input", "desc": "Food/pigment input pathway not in equation"},
            {"gap": "fixed_alpha_beta", "desc": "α=-2, β=0 are global constants — not profile-dependent"},
        ],
    }

# ============================================================
# CLOSED UNIVERSE EQUATION — T(t, φ_obs, {λ_i}) = 0
# Eliminates all 6 structural gaps from gap analysis
# ============================================================

# 40-particle → 8D dimension coupling constants {λ_i}
# Each particle couples to one or more dimensions; λ = coupling strength
# v4 mapping: r=neutrino, h=gluon, d=tau/z_boson, p=higgs,
#             s=quark, gamma=photon, g=muon, nu=w_boson
PARTICLE_DIM_COUPLING = {
    # 8 base particles — strong coupling to primary dimension
    "neutrino":           {"r": 0.9},
    "gluon":              {"h": 0.9},
    "tau":                {"d": 0.9},
    "z_boson":            {"d": 0.9},
    "higgs":              {"p": 0.9},
    "quark":              {"s": 0.9},
    "photon":             {"gamma": 0.9},
    "muon":               {"g": 0.9},
    "w_boson":            {"nu": 0.9},
    # derivatives of base particles (v4)
    "proton":             {"r": 0.6, "p": 0.4},       # neutrino ignition + higgs convergence
    "electron":           {"gamma": 0.5, "s": 0.5},   # photon derivative (skull lipid bilayer)
    "em_field":           {"gamma": 0.5, "nu": 0.5},  # photon∩w_boson at vertex (138.88° spark)
    "graviton":           {"d": 0.5, "nu": 0.5},      # higgs derivative (ferritin iliac void mass)
    # 6 quark flavors — quark base = s, flavors split per v4
    "up_quark":           {"r": 0.5, "p": 0.5},       # V1 calcarine myosin S1 — r/p active force
    "down_quark":         {"h": 0.9},                  # V2 F-actin 7nm — h passive rail
    "charm_quark":        {"h": 0.5, "g": 0.5},       # V2 NMDA 14nm — h/g color edge binding
    "strange_quark":      {"d": 0.5, "nu": 0.5},      # left insula — d/nu novelty detection
    "top_quark":          {"r": 0.5, "nu": 0.5},      # hepatocyte NPC — r/nu high-energy transport
    "bottom_quark":       {"d": 0.5, "nu": 0.5},      # sigmoid colon — d/nu apoptosis/decay
    # 6 neutrino variants — neutrino base = r, variants split per v4
    "electron_neutrino":      {"r": 0.6, "s": 0.4},   # O2/GABA synthesis
    "electron_antineutrino":  {"r": 0.5, "gamma": 0.5}, # night spark reward
    "muon_neutrino":          {"r": 0.4, "g": 0.6},   # day fatigue storage (cytochrome 640)
    "muon_antineutrino":      {"r": 0.4, "d": 0.6},   # night cosmic repair
    "tau_neutrino":           {"r": 0.3, "d": 0.7},   # night hypoxia/mass-gate monitor
    "tau_antineutrino":       {"r": 0.4, "p": 0.6},   # day autophagy/cleansing
    # compact + dark
    "neutron":            {"nu": 0.5, "d": 0.5},
    "neutron_star":       {"g": 0.6, "nu": 0.4},
    "dark_matter":        {"d": 0.6, "nu": 0.4},      # foam cell — d/nu noise residue
    "dark_energy":        {"nu": 0.6, "gamma": 0.4},  # nucleus/crypt — nu/gamma time-axis
    # scalars
    "time":               {"r": 0.5, "nu": 0.5},
    "energy":             {"r": 0.6, "p": 0.4},
    # buses / hormones / cofactors
    "ego_d2":             {"p": 0.6, "s": 0.4},
    "left_progesterone":  {"gamma": 0.5, "h": 0.5},   # right eye 3D — gamma/h
    "right_testosterone": {"r": 0.5, "p": 0.5},
    "acetyl_coa":         {"s": 0.3, "d": 0.4, "p": 0.3}, # mitochondria PDH — s/d/p memory mass
    # derived / observer-specific
    "spark":              {"gamma": 0.5, "nu": 0.5},  # vertex 138.88° — gamma/nu
    "clathrate_buffer":   {"g": 0.5, "p": 0.5},
    "em_field_rebrancher": {"gamma": 0.4, "nu": 0.6}, # vertex rebranching — gamma/nu
    "testosterone_sex":   {"r": 0.4, "p": 0.6},
    "endorphin_imag":     {"d": 0.4, "nu": 0.6},      # MOR 4nm — d/nu pleasure seal
    "male_gaba_a_wk":     {"d": 0.5, "gamma": 0.5},   # left occipitalis hypoxia — d/gamma
    "pain_eliminate":     {"d": 0.4, "nu": 0.6},      # substance P NK1R — d/nu
}

# Symmetry group: 8D rotations that leave the equation invariant
# The gauge group is generated by 3 independent rotations in 8D space
# G = SO(2)_rs × SO(2)_hd × SO(2)_gpn (3 commuting rotation planes)
GAUGE_GENERATORS = {
    "rs_plane":   ("r", "s"),       # rhythm ↔ brightness rotation
    "hd_plane":   ("h", "d"),       # harmony ↔ darkness rotation
    "gpn_plane":  ("g", "p", "nu"), # seal ↔ predictability ↔ grit (3-cycle)
}

# Layer scales: body < observer < bridge < dark
LAYER_SCALES = {
    "body":     1.0,       # nm to cm scale
    "observer": 10.0,      # neural circuit scale
    "bridge":   100.0,     # Betti/cosmic scale
    "dark":     1000.0,    # dark matter/void scale
}

# Observer phase: k_stress→impulse determines φ_obs
# k_stress→impulse ≈ 0 → φ_obs = singularity (fixed point)
# k_stress→impulse > 0 → φ_obs = noisy (catecholamine jitter)
def compute_observer_phase(profile_label, k_stress_impulse=0.0):
    """φ_obs = lim_{k→0} arg(z_obs) where k = k_stress→impulse.
    For observer (k≈0): φ_obs = π/2 (pure imaginary axis = resonance projection).
    For normal (k>0): φ_obs = π/2 + noise(k)."""
    if k_stress_impulse < 1e-6:
        phi = math.pi / 2.0  # singularity: pure resonance
        noise = 0.0
        is_observer = True
    else:
        noise = k_stress_impulse * math.sin(k_stress_impulse * 100)
        phi = math.pi / 2.0 + noise
        is_observer = False
    return {
        "phi_obs": phi,
        "noise": noise,
        "is_observer": is_observer,
        "k_stress_impulse": k_stress_impulse,
        "singularity": k_stress_impulse < 1e-6,
    }

# Time-dependent dimension modulation: 16-window shift via sin waves
def compute_time_dependent_dims(dims, t_window, hour):
    """r(t) = r_base + A_r × sin(2πt/16 + φ_r)
    Each dimension has different amplitude and phase → no tile repeats."""
    t = float(t_window) if t_window is not None else (float(hour) / 24.0 * 16.0)
    omega = 2.0 * math.pi / 16.0

    # Amplitude and phase per dimension (determined by toroidal slot position)
    dim_oscillation = {
        "r":     {"amp": 0.08, "phase": 0.0},
        "h":     {"amp": 0.06, "phase": math.pi / 4},
        "d":     {"amp": 0.10, "phase": math.pi / 2},
        "p":     {"amp": 0.05, "phase": 3 * math.pi / 4},
        "s":     {"amp": 0.12, "phase": math.pi},
        "gamma": {"amp": 0.07, "phase": 5 * math.pi / 4},
        "g":     {"amp": 0.06, "phase": 3 * math.pi / 2},
        "nu":    {"amp": 0.09, "phase": 7 * math.pi / 4},
    }

    dims_t = {}
    for d in DIM_ORDER:
        osc = dim_oscillation[d]
        mod = osc["amp"] * math.sin(omega * t + osc["phase"])
        dims_t[d] = clamp(dims.get(d, 0.5) + mod)
    return dims_t, {"t": t, "omega": omega, "oscillation": dim_oscillation}

# Multi-scale layer decomposition
def compute_layer_terms(dims, phi_obs, t):
    """4 layers as multi-scale contributions to the equation.
    Each layer operates at a different scale factor."""
    # Body layer: direct dimension values
    body_term = sum(dims[d] for d in DIM_ORDER) / 8.0

    # Observer layer: weighted by φ_obs (resonance projection)
    obs_weight = math.sin(phi_obs)  # = 1.0 for observer (φ=π/2)
    observer_term = obs_weight * (dims["s"] * dims["gamma"] + dims["h"] * dims["nu"])

    # Bridge layer: Betti 6/12 closure
    betti_6 = abs(dims["s"] + dims["gamma"] - 1.0)  # EM closure
    betti_12 = abs(dims["g"] * dims["nu"] - dims["d"] * dims["p"])  # topological bridge
    bridge_term = math.exp(-betti_6) * math.exp(-betti_12)

    # Dark layer: dark matter / void contribution
    dark_term = dims["d"] * (1.0 - dims["s"]) + dims["nu"] * (1.0 - dims["gamma"])

    return {
        "body": body_term,
        "observer": observer_term,
        "bridge": bridge_term,
        "dark": dark_term,
        "betti_6": betti_6,
        "betti_12": betti_12,
    }

# Gauge transformation: apply symmetry rotation to dims
def apply_gauge_transform(dims, theta_rs=0.0, theta_hd=0.0, theta_gpn=0.0):
    """Apply SO(2) rotations in 3 commuting planes.
    The equation is invariant under these rotations."""
    r, s = dims["r"], dims["s"]
    r_new = r * math.cos(theta_rs) - s * math.sin(theta_rs)
    s_new = r * math.sin(theta_rs) + s * math.cos(theta_rs)

    h, d = dims["h"], dims["d"]
    h_new = h * math.cos(theta_hd) - d * math.sin(theta_hd)
    d_new = h * math.sin(theta_hd) + d * math.cos(theta_hd)

    # 3-cycle in g, p, nu (discrete rotation)
    g, p, nu = dims["g"], dims["p"], dims["nu"]
    cos_t = math.cos(theta_gpn)
    sin_t = math.sin(theta_gpn)
    g_new = g * cos_t - p * sin_t
    p_new = g * sin_t + p * cos_t
    # nu is invariant under this rotation (it's the axis)

    return {
        "r": clamp(r_new), "h": clamp(h_new), "d": clamp(d_new),
        "p": clamp(p_new), "s": clamp(s_new), "gamma": dims["gamma"],
        "g": clamp(g_new), "nu": nu,
    }

# SH constants (locked from prose.txt calibration)
SH_R_STAR = 0.11214750
SH_Q0_STAR = 0.977738
SH_SIGMA_L = 0.003717
SH_SIGMA_R = 0.000908

# Blood type → α,β modulation: toroidal cycle AB→A→O→B
# O = present moment (center) → α=-2, β=0 (baseline)
# AB = RELEASE (symmetric to O) → α=-2, β=0
# A = STRESS_GROWTH → α=-1.5, β=+0.15 (structure influence weakens, base form rises)
# B = EXTREME_GROWTH → α=-2.5, β=-0.15 (structure influence intensifies, base form drops)
BLOOD_ALPHA_BETA = {
    "O":  {"alpha": -2.0,  "beta": 0.0},   # present moment = baseline
    "AB": {"alpha": -2.0,  "beta": 0.0},   # release = symmetric to O
    "A":  {"alpha": -1.5,  "beta": 0.15},  # stress growth = structure weakens
    "B":  {"alpha": -2.5,  "beta": -0.15}, # extreme growth = structure intensifies
}

# Geology → α,β modulation: Oxford Gleysol vs Bath Limestone
GEOLOGY_ALPHA_BETA = {
    "oxford_gleysol":  {"alpha": -2.0, "beta": 0.0,  "caco3_bias": 0.0,  "o2_level": 0.3},
    "bath_limestone":  {"alpha": -1.5, "beta": 0.15, "caco3_bias": 0.3,  "o2_level": 0.7},
    "korea_granite":   {"alpha": -2.2, "beta": -0.1, "caco3_bias": -0.1, "o2_level": 0.6},
    "default":         {"alpha": -2.0, "beta": 0.0,  "caco3_bias": 0.0,  "o2_level": 0.5},
}

# 49. SOIL_NODE_DAY_NIGHT: 8 soil × day/night = 16 circuit node connections
# Each soil maps to a CIRCUITFILE.MD node by day/night phase.
# Node → 8D dim effect derived from CIRCUITFILE.MD axis definitions.
SOIL_NODE_DAY_NIGHT = {
    "andosol": {
        "day":  {"node": "hind_insula",       "dim_effect": {"d": -0.02, "s": +0.03}},
        "night": {"node": "peonidine",        "dim_effect": {"h": +0.03, "gamma": +0.04}},
    },
    "podzol": {
        "day":  {"node": "right_nose_male_NE","dim_effect": {"r": +0.03, "h": +0.02}},
        "night": {"node": "mc1r",            "dim_effect": {"s": +0.03, "d": +0.02}},
    },
    "cambisol_L": {
        "day":  {"node": "ferritin",         "dim_effect": {"s": +0.04}},
        "night": {"node": "pi_electron_cloud","dim_effect": {"gamma": +0.04}},
    },
    "cambisol_R": {
        "day":  {"node": "cck",              "dim_effect": {"r": +0.02, "d": +0.02}},
        "night": {"node": "disulfide_bond",  "dim_effect": {"p": +0.03, "nu": +0.03}},
    },
    "mollisol": {
        "day":  {"node": "heme",             "dim_effect": {"s": +0.03, "d": +0.02}},
        "night": {"node": "mycorradicin",    "dim_effect": {"g": +0.03, "nu": +0.03}},
    },
    "histosol": {
        "day":  {"node": "cytochrome_c_oxidase","dim_effect": {"r": +0.03, "d": +0.02}},
        "night": {"node": "fold_belt",       "dim_effect": {"r": +0.02, "gamma": +0.03}},
    },
    "cryosol": {
        "day":  {"node": "left_genital_d2",  "dim_effect": {"p": +0.04}},
        "night": {"node": "g_element_4th_toe","dim_effect": {"g": +0.04}},
    },
    "gleysol": {
        "day":  {"node": "steel",            "dim_effect": {"s": +0.03, "gamma": +0.03}},
        "night": {"node": "clay_gouge",      "dim_effect": {"g": +0.04}},
    },
}

# Color → pigment → dim reverse feedback (색소가 바뀌면 dim이 shift)
COLOR_PIGMENT_DIM = {
    "BLACK":  {"g": +0.05},              # Eumelanin: mc1r q_bar = seal/block
    "RED":    {"r": +0.03, "d": +0.03},  # Heme b: Fe2+ → r↑, d↑
    "BLUE":   {"s": +0.04},              # Phycocyanobilin: GABA-B 640 → s↑
    "GREEN":  {"s": +0.04},              # Biliverdin IXα: cytochrome_c_oxidase → s↑
    "YELLOW": {"h": +0.03},              # Bilirubin: pi_electron_cloud → h↑
    "PURPLE": {"gamma": +0.04},          # Peonidin: 역방향 → gamma↑ (leakage DELAY)
    "WHITE":  {"s": +0.03, "nu": +0.03}, # Leucoanthocyanidin: heme/memory_entropy → s↑, nu↑
    "ORANGE": {"nu": +0.04},             # β-Carotene: memory_entropy + amygdala → nu↑
    "CYAN":   {"d": -0.03, "s": +0.03}, # Hemocyanin Cu²⁺ oxy: succinate_dehydrogenase → d↓, s↑
}

# The closed universe equation: T(t, φ_obs, {λ_i}, SH, Ψ, color, route, leakage, geomag, geology) = 0
def compute_closed_universe_equation(dims, t_window, hour, profile_label,
                                      k_stress_impulse=0.0, active_particles=None,
                                      geology="default",
                                      observer_active=True, time_phase="day",
                                      profile_color=None):
    """Fully closed universe equation. All gaps eliminated.

    T(t, φ_obs, {λ_i}) = Π_k τ_k(r(t), h(t), d(t), p(t), s(t), γ(t), g(t), ν(t), φ_obs, {λ_i}, layers) × SH × Ψ × ... = 0

    Each tensor term τ_k now integrates:
    - Time: ω(t) = sin(2πt/16) phase shift INSIDE each term (16-window shift derived from equation)
    - Observer: φ_obs singularity (obs_factor) INSIDE each term
    - Particle: {λ_i} coupling (particle_weight_for_dims) INSIDE each term
    - Layers: 4-layer multi-scale (body×observer×bridge×dark) INSIDE each term
    - Spontaneous symmetry breaking: argmin_k |τ_k| selects active constraint from within equation
    - tau_phase(k, ω): time-dependent phase distributes minimization across t — equation self-selects

    Integrates ALL existing code:
    1. Time: sin oscillation (16-window shift) — INSIDE τ_k via omega_t and tau_phase
    2. Observer: φ_obs singularity (k_stress→impulse≈0) — INSIDE τ_k via obs_factor
    3. Particle: {λ_i} 41-particle coupling — INSIDE τ_k via particle_weight_for_dims
    4. Layer: body/observer/bridge/dark multi-scale — INSIDE τ_k via layer_full
    5. Gauge: SO(2)×SO(2)×SO(2) symmetry — gauge invariance check with rotated τ_k
    6. Spontaneous breaking: argmin_k |τ_k| — equation self-selects active constraint
    7. Feedback: 3AM hysteresis + 4:30PM ferric event (discrete event terms)
    8. Leakage: Darcy flux + color leakage + all_leakage (kappa modulation)
    9. Geomag: geomagnetic modulation (outer_core_convection coupling)
    10. α,β geology-dependent (Oxford Gleysol vs Bath Limestone)
    11. CaCO₃ asymmetry: schizo point left block vs right forward
    12. 118 elements: toroidal AB→A→O→B from symmetry group
    13. Observer closure: 9π/(20√2) in φ_obs
    14. Spark angle: 138.88° in {λ_i} coupling
    15. Discrete slots: from sin periodicity via toroidal slot mapping
    16. Color→pigment→dim reverse feedback (color events shift dims)
    17. Master Ψ equation (closure tension + renormalization + color closure)
    18. Universe cycle (Mandelbrot chirality → inverse color → dim shift)
    19. 41-particle route vector (active route weights)
    20. Compartment route (4-quadrant inlet/outlet)
    21. Neutrino routes (day/night 6-variant)
    22. Creative 4-shapes (STRUCTURE/FLOW/CONTRAST/EMERGENCE)
    23. 4-layer colors (A/B/C/D toroidal blood shift)
    24. Toroidal phase (6-sphere circulation)
    25. EM bypass route (5-step COX retrograde observer closure)
    26. 23 tensor terms covering ALL 28 pairwise relationships (t1~t23)
    """
    parts = profile_label.split("_")
    mbti, gender = parts[0], parts[1]
    is_night = (time_phase == "night")

    # 1. TIME: make dims time-dependent
    dims_t, time_info = compute_time_dependent_dims(dims, t_window, hour)

    # 16. COLOR→PIGMENT→DIM REVERSE FEEDBACK: color events shift dims
    color_feedback_shifts = {}
    if profile_color:
        base_color = profile_color.get("base", "")
        shifts = COLOR_PIGMENT_DIM.get(base_color, {})
        for dim_key, delta in shifts.items():
            dims_t[dim_key] = clamp(dims_t[dim_key] + delta)
            color_feedback_shifts[dim_key] = delta
    # Inverse color (chirality > midpoint): inverse color → inverse dim shift
    if profile_color and profile_color.get("inverted", False):
        inv_base = profile_color.get("base", "")
        inv_shifts = COLOR_PIGMENT_DIM.get(inv_base, {})
        for dim_key, delta in inv_shifts.items():
            dims_t[dim_key] = clamp(dims_t[dim_key] + delta * 0.5)  # half-strength inverse

    # 2. OBSERVER: compute φ_obs with closure tension
    obs_info = compute_observer_phase(profile_label, k_stress_impulse)
    phi_obs = obs_info["phi_obs"]
    # Observer closure: 9π/(20√2) ≈ 1.000042 defines the fixed point
    closure_tension = OBSERVER_CLOSURE_TENSION  # ≈ 1.000042
    closure_residual = CLOSURE_RESIDUAL  # ≈ 3.51e-4
    # φ_obs anchored to closure tension: sin(φ_obs) = 1/closure_tension for observer
    if obs_info["singularity"]:
        obs_factor = 1.0 / closure_tension  # ≈ 0.999958 (nearly 1.0, residual = irreversibility)
    else:
        obs_factor = math.sin(phi_obs) / closure_tension

    # 25. EM BYPASS ROUTE: 5-step COX retrograde → observer closure modulation
    em_bypass_steps = len(EM_BYPASS_ROUTE)  # 5 steps
    em_bypass_mod = 1.0
    if observer_active:
        em_bypass_mod = 1.0 + 0.01 * em_bypass_steps  # 5-step closure adds 5%

    # 26. GEOMETRIC NODE: x-coordinate spatial modulation
    geo_node = get_geometric_node(mbti, gender, observer_active)
    geo_node_info = GEOMETRIC_NODES.get(geo_node, {})
    geo_x = geo_node_info.get("x", 8.0)
    if geo_x is None:
        geo_x = 8.0  # observer singularity = center
    geo_mod = 1.0 + 0.01 * abs(geo_x - 8.0) / 6.0  # deviation from center

    # 27. 41-PARTICLE COLOR RESOLUTION: day/night alt colors → dim shift
    particle_color_shifts = {}
    for pname in PARTICLE_ORDER_40:
        pcol = get_particle_color(pname, context="night" if is_night else "day")
        pbase = pcol.get("base", "")
        # Handle alt colors (e.g. photon YELLOW→WHITE at night)
        if is_night and "alt" in pcol and pcol["alt"]:
            for ctx, alt_color in pcol["alt"].items():
                if ctx in ("observer", "lower_mantle", "cytochrome_c_oxidase",
                           "dark_energy", "succinate_dehydrogenase"):
                    parts_alt = alt_color.split()
                    pbase = parts_alt[0] if parts_alt else pbase
                    break
        # Normalize composite colors
        if "/" in pbase:
            pbase = pbase.split("/")[0]
        shifts = COLOR_PIGMENT_DIM.get(pbase, {})
        for dk, dv in shifts.items():
            if dk not in particle_color_shifts:
                particle_color_shifts[dk] = 0.0
            particle_color_shifts[dk] += dv * 0.005  # per-particle: small cumulative
    for dk, dv in particle_color_shifts.items():
        dims_t[dk] = clamp(dims_t[dk] + dv)

    # 28. INTERFERENCE COLORS: metabolic node pair interactions → dim shift
    interference_shifts = {}
    if profile_color:
        base_color = profile_color.get("base", "")
        pathway = color_to_metabolic_pathway(base_color)
        nodes = pathway.get("nodes", [])
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                ic = get_interference_color(nodes[i], nodes[j])
                if ic:
                    ic_name = ic.get("name", "")
                    ic_shifts = COLOR_PIGMENT_DIM.get(ic_name, {})
                    for dk, dv in ic_shifts.items():
                        if dk not in interference_shifts:
                            interference_shifts[dk] = 0.0
                        interference_shifts[dk] += dv * 0.5  # interference = strong
        for dk, dv in interference_shifts.items():
            dims_t[dk] = clamp(dims_t[dk] + dv)

    # 29. SPARK INTERFERENCE: 138.88° global flash → WHITE→BLACK discharge
    _spark_sin_val = math.sin(SPARK_ANGLE_RAD)
    spark_interference_mod = 1.0
    spark_flash = abs(_spark_sin_val) > 0.99  # near peak of sin(138.88°)
    if spark_flash:
        # WHITE flash → s↑, nu↑ then BLACK discharge → g↑
        dims_t["s"] = clamp(dims_t["s"] + 0.02)
        dims_t["nu"] = clamp(dims_t["nu"] + 0.02)
        dims_t["g"] = clamp(dims_t["g"] + 0.03)  # BLACK discharge seals
        spark_interference_mod = 1.05  # 5% boost from flash event

    # 30. WINDOW SHIFT: specific boosts (lightning strike, noon peak)
    window_info = get_window(hour)
    window_boost_mod = 1.0
    if window_info.get("window") == 10:  # lightning strike
        dims_t["d"] = clamp(dims_t["d"] + 0.05)
        window_boost_mod = 1.03
    elif window_info.get("window") == 8:  # noon peak
        dims_t["s"] = clamp(dims_t["s"] + 0.03)
        window_boost_mod = 1.02

    # 31. 4-LAYER JITTER: mulberry32 stochastic variation
    seed_val = abs(hash(profile_label)) % 100000
    rng = mulberry32(seed_val + int(hour))
    jitter_mod = 1.0 + (rng() - 0.5) * 0.02  # ±1% stochastic

    # 32. EQUATION-CONSTRAINED DIM ADJUSTMENT: active branch solving
    eq_adjusted = compute_8d_from_equation(dims_t, profile_label, time_phase)
    eq_branch_mod = 1.0 + 0.01 * (1.0 - eq_adjusted.get("homeostasis_after", 0.5))

    # 33. QCD CONFINEMENT / DE SITTER: gamma·d product feedback
    gamma_d = dims_t["gamma"] * dims_t["d"]
    confinement = "CONFINED" if gamma_d <= 1.0 else "DECONFINED"
    de_sitter = max(0.0, 1.0 - gamma_d) if gamma_d < 1.0 else 0.0
    qcd_mod = 1.0 + 0.02 * de_sitter  # de Sitter expansion modulates

    # 34. EM PATH: (s+gamma)/2 + day/night offset — EM closure strength
    em_path_val = clamp((dims_t["s"] + dims_t["gamma"]) / 2 + 0.1 * (1 if not is_night else -1))
    em_path_mod = 1.0 + 0.02 * em_path_val

    # 35. GRAVITON: (g+nu)/2 + day/night offset — void mass storage
    graviton_val = clamp((dims_t["g"] + dims_t["nu"]) / 2 + 0.1 * (1 if is_night else -1))
    graviton_mod = 1.0 + 0.02 * graviton_val

    # 36. LEAKAGE CAVITY: direct dim-driven leakage (d>0.7 or nu>0.7)
    leakage_cavity_name = ""
    cavity_leak = 0.0
    if dims_t["d"] > 0.7:
        cavity_leak = (dims_t["d"] - 0.7) * 0.3
        leakage_cavity_name = "D3_observer_gates"
    elif dims_t["nu"] > 0.7:
        cavity_leak = (dims_t["nu"] - 0.7) * 0.2
        leakage_cavity_name = "structural_anchors"
    cavity_mod = 1.0 - cavity_leak  # active cavity reduces closure

    # 37. PACT RETENTION: p*0.5 + r*0.3 + time_phase factor
    pact_val = clamp(dims_t["p"] * 0.5 + dims_t["r"] * 0.3 + 0.2 * (0.5 if not is_night else 0.3))
    pact_mod = 1.0 + 0.01 * pact_val

    # 38. NEUTRON STAR OSCILLATION: 1/64 + g*0.3 + nu*0.1
    ns_osc_val = clamp(ONE_64 + dims_t["g"] * 0.3 + dims_t["nu"] * 0.1)
    ns_osc_mod = 1.0 + 0.01 * ns_osc_val

    # 39. DARK MATTER: night-only, d-scaled noise accumulation
    dark_matter_val = clamp(0.017 * (1 + dims_t["d"] * 0.5)) if is_night else 0.0
    dark_matter_mod = 1.0 + 0.01 * dark_matter_val

    # 40. CCK SWITCH: female right extraversion → gluon↔z_boson alignment
    cck_active = (gender == "F" and mbti[0] == "E")
    cck_mod = 1.0
    if cck_active:
        cck_mod = 1.0 + 0.02 * dims_t.get("g", 0.5)

    # 41. 12D / W-AXIS: 8D × 4축(A1-A4) + W-axis(M/F bias) + 쌍BODY closure
    state_12d = compute_12d_state(dims_t, gender, hour, t_window)
    # W-axis dim shifts applied to dims_t
    for dk, dv in state_12d["w_dim_shifts"].items():
        dims_t[dk] = clamp(dims_t[dk] + dv)
    w_axis_mod = 1.0 + 0.03 * state_12d["total_closure"]
    dual_body_mod = 1.0 + 0.02 * state_12d["dual_body_mirror"]

    # 42. E119-E127 RECEPTOR NODES: 9 new element dim transitions
    e119_127_shifts = {}
    for eid, einfo in E119_E127_NODES.items():
        for dk, dv in einfo.get("dim_effect", {}).items():
            dims_t[dk] = clamp(dims_t[dk] + dv * 0.5)  # half-strength (receptor-level)
            e119_127_shifts[dk] = e119_127_shifts.get(dk, 0.0) + dv * 0.5
    e119_127_mod = 1.0 + 0.01 * len(E119_E127_NODES) / 9.0  # 9 nodes active = +1%

    # 43. UNSPARK OVERLAY: self-loop receptor bypass routing
    unspark_shifts = {}
    for node_name, overlay in UNSPARK_OVERLAY.items():
        for dk, dv in overlay.get("dim_effect", {}).items():
            unspark_shifts[dk] = unspark_shifts.get(dk, 0.0) + dv
    for dk, dv in unspark_shifts.items():
        dims_t[dk] = clamp(dims_t[dk] + dv)
    unspark_mod = 1.0 + 0.01 * len(UNSPARK_OVERLAY) / 3.0

    # 44. 5HT1B SPIRAL BYPASS: ν→g transition, neutrino/higgs creation
    spiral_5ht1b_shifts = SPIRAL_BYPASS_5HT1B.get("dim_effect", {})
    for dk, dv in spiral_5ht1b_shifts.items():
        dims_t[dk] = clamp(dims_t[dk] + dv)
    spiral_5ht1b_mod = 1.0 + 0.02 * dims_t.get("nu", 0.5)

    # 45. ESR1 SPLIT / ACh REROUTING: dual-mode phase signaling
    esr1_shifts = ESR1_SPLIT.get("dim_effect", {})
    for dk, dv in esr1_shifts.items():
        dims_t[dk] = clamp(dims_t[dk] + dv)
    esr1_mod = 1.0 + 0.01 * dims_t.get("s", 0.5)

    # 46. BILIRUBIN BYPASS: heme → HO-1 → bilirubin = neutron star analog
    bili_shifts = BILIRUBIN_BYPASS.get("dim_effect", {})
    for dk, dv in bili_shifts.items():
        dims_t[dk] = clamp(dims_t[dk] + dv)
    bili_mod = 1.0 + 0.01 * dims_t.get("d", 0.5)
    # Bilirubin reduces leakage (applied later after leakage_mod is defined)
    _bili_leakage_reduction = BILIRUBIN_BYPASS.get("leakage_reduction", 0.0)

    # 47. CANCER BUFFER / MAILLARD CLEARANCE: p→g→r→gamma→d cycle
    cm_cycle = CANCER_MAILLARD_CYCLE.get("dim_effect", {})
    # Cycle active when p > 0.6 (glycation accumulation)
    cycle_active = dims_t.get("p", 0.5) > 0.6
    cancer_maillard_mod = 1.0
    if cycle_active:
        for dk, dv in cm_cycle.items():
            dims_t[dk] = clamp(dims_t[dk] + dv)
        cancer_maillard_mod = 1.0 + 0.02 * dims_t.get("d", 0.5)

    # 48. 쌍BODY CLOSURE: BODY1(신체) ↔ BODY2(우주) 미러링 완성도
    # 4축 모두 폐쇄 = 12D 공간 완전 닫힘 = 토로이달 완성
    dual_body_closure = state_12d["dual_body_mirror"]
    body_closure_mod = 1.0 + 0.03 * dual_body_closure

    # 49. SOIL_NODE_DAY_NIGHT: 8 soil × day/night = 16 circuit node dim shifts
    soil_node_shifts = {}
    soil_active_nodes = []
    for soil_name, soil_map in SOIL_NODE_DAY_NIGHT.items():
        phase = "night" if is_night else "day"
        node_info = soil_map.get(phase, {})
        node_name = node_info.get("node", "")
        soil_active_nodes.append(f"{soil_name}:{node_name}")
        for dk, dv in node_info.get("dim_effect", {}).items():
            dims_t[dk] = clamp(dims_t[dk] + dv)
            soil_node_shifts[dk] = soil_node_shifts.get(dk, 0.0) + dv
    soil_node_mod = 1.0 + 0.01 * len(soil_active_nodes) / 8.0  # 8 soil active = +1%

    # 3. PARTICLE: coupling with spark angle modulation
    if active_particles is None:
        active_particles = PARTICLE_ORDER_40

    # Spark angle coupling: 138.88° modulates particle weights
    spark_sin = math.sin(SPARK_ANGLE_RAD)
    spark_cos = math.cos(SPARK_ANGLE_RAD)

    def particle_weight_for_dims(dim_set):
        w = 1.0
        for pname in active_particles:
            coupling = PARTICLE_DIM_COUPLING.get(pname, {})
            for d in dim_set:
                if d in coupling:
                    # Spark angle modulates coupling: CW vs CCW interference
                    w *= (1.0 + coupling[d] * 0.1 * spark_sin)
        return w / max(1, len(active_particles))

    # 11. GEOLOGY: α,β depend on geology
    geo_params = GEOLOGY_ALPHA_BETA.get(geology, GEOLOGY_ALPHA_BETA["default"])
    ALPHA_EQ = geo_params["alpha"]
    BETA_EQ = geo_params["beta"]
    caco3_bias = geo_params["caco3_bias"]
    o2_level = geo_params["o2_level"]

    r = dims_t["r"]; h = dims_t["h"]; d = dims_t["d"]; p = dims_t["p"]
    s = dims_t["s"]; gamma = dims_t["gamma"]; g = dims_t["g"]; nu = dims_t["nu"]
    # Re-read after all feedback shifts (color, particle, interference, spark, window, jitter)

    # 4. LAYER terms
    layers = compute_layer_terms(dims_t, phi_obs, time_info["t"])
    layer_mod = layers["bridge"]  # exp(-betti) closure factor

    # 17. MASTER Ψ: closure tension + renormalization + color closure
    psi_info = compute_master_psi(dims_t, hour, observer_active, profile_num=1, profile_color=profile_color)
    # Normalize: divide out constant scale (T*R) to get dynamic ratio ~1.0
    _psi_scale = abs(psi_info.get("T_closure", 1.0) * psi_info.get("R_renorm", 1.0)) + 1e-10
    psi_mod = clamp(abs(psi_info["psi"]) / _psi_scale, 0.1, 3.0)

    # 18. UNIVERSE CYCLE: Mandelbrot chirality
    universe_cycle = compute_universe_cycle(dims_t)
    chirality = universe_cycle.get("current_chirality", 0.5)
    cycle_mod = 1.0 + abs(chirality - 0.38) * 0.1  # deviation from midpoint

    # 19. ROUTE VECTOR: 41-particle active route weights
    active_route = get_active_route(hour, is_night)
    route_vec = compute_route_vector(active_route, dims_t, hour, is_night)
    route_weight_sum = sum(route_vec.values()) if route_vec else 1.0
    route_mod = clamp(route_weight_sum, 0.5, 2.0)  # route density

    # 20. COMPARTMENT ROUTE: 4-quadrant inlet/outlet
    comp_route = compute_compartment_route(mbti, gender, dims_t, time_phase)
    comp_mod = 1.0 + 0.02 * comp_route.get("compartment", 1)

    # 21. NEUTRINO ROUTES: day/night 6-variant
    neutrino_routes = get_neutrino_routes(time_phase)
    neutrino_mod = 1.0 + 0.01 * len(neutrino_routes)  # 3 active variants

    # 22. CREATIVE 4-SHAPES: STRUCTURE/FLOW/CONTRAST/EMERGENCE
    creative_shapes = compute_creative_4shapes(dims_t, profile_label)
    creative_mod = 1.0 + 0.01 * creative_shapes["dominant_score"]

    # 23. 4-LAYER COLORS: A/B/C/D toroidal blood shift
    layer_colors = compute_4layer_colors(profile_label, dims_t, time_phase, hour)
    active_layer = "A"
    slot = get_toroidal_slot(hour)
    if slot.get("genre_type") == "STRESS_GROWTH":
        active_layer = "B"
    elif slot.get("genre_type") == "EXTREME_GROWTH":
        active_layer = "C"
    active_layer_color = layer_colors.get(active_layer, {}).get("color", "MIXED")
    layer_color_shifts = COLOR_PIGMENT_DIM.get(active_layer_color, {})
    for dk, dv in layer_color_shifts.items():
        dims_t[dk] = clamp(dims_t[dk] + dv * 0.3)  # weaker than main color
    layer_color_mod = 1.0 + 0.01 * COLOR_DISTANCE_TO_BLACK.get(active_layer_color, 0.5)

    # 24. TOROIDAL PHASE: 6-sphere circulation
    toroidal_phase = get_toroidal_phase(hour)
    toroidal_mod = 1.0 + 0.02 * (toroidal_phase.get("phase", 1) / 6.0)

    # 7. FEEDBACK: discrete event terms (3AM hysteresis + 4:30PM ferric)
    hysteresis_3am = compute_3am_hysteresis(hour, observer_active, dims_t)
    ferric_430pm = compute_430pm_event(hour)
    # 3AM: Betti 12 closure event → modulates t3 (g+nu) and t7 (d*nu)
    feedback_mod = 1.0
    if hysteresis_3am.get("active") and hysteresis_3am.get("betti_12_complete"):
        feedback_mod *= 0.5  # Betti 12 closure halves the sealing terms
    if hysteresis_3am.get("entropy_zone"):
        feedback_mod *= 0.3  # Entropy zone randomizes → strong modulation
    # 4:30PM: ferric event → modulates s-axis (GABA-A destruction)
    ferric_mod = 1.0
    if ferric_430pm.get("active"):
        ferric_mod = 0.7  # 3/32 asymmetry → s-axis weakened by 30%

    # 8. LEAKAGE: Darcy flux + all_leakage
    # Night-time leakage blocking: night_reverse_blocked sites have leakage=0
    # (forward-only flow enforced by oxidised_manganese block + adapter_protein forward open)
    darcy = compute_darcy_leakage(dims_t, observer_active)
    kappa_eff = darcy["kappa"]
    leakage_count = 0
    night_blocked_count = 0
    all_leak = compute_all_leakage(dims_t, time_phase)
    # Separate night_blocked from actual leakage — blocked sites DON'T count as leakage
    for leak_item in all_leak["personal_leakage"]:
        if leak_item.get("status") == "night_reverse_blocked":
            night_blocked_count += 1
        else:
            leakage_count += 1
    leakage_count += len(all_leak["cosmic_leakage"]) + len(all_leak["internal_cavities"])
    # Leakage modulates equation: each active leakage site adds noise
    leakage_mod = (KAPPA / kappa_eff) if kappa_eff > 0 else 1.0
    leakage_mod *= (1.0 - 0.05 * leakage_count)  # each leakage site reduces closure by 5%
    leakage_mod *= (1.0 - _bili_leakage_reduction)  # bilirubin bypass reduces leakage
    # Night reverse blocked sites ENHANCE closure: forward-only flow = universe eternal
    leakage_mod *= (1.0 + 0.03 * night_blocked_count)  # each blocked site improves closure by 3%

    # 9. GEOMAG: geomagnetic modulation
    dims_geomag, geomag_info = apply_geomag_modulation(dims_t, observer_active, time_phase, hour)
    geomag_mod = 1.0
    for k, v in geomag_info.get("modulations", {}).items():
        geomag_mod *= (1.0 + abs(v))  # geomag modulation magnitude

    # 11. CaCO₃ ASYMMETRY: left schizo block vs right forward
    # Left block = caco3 frozen (schizo point) → reduces t8 (p-αg-β) sensitivity
    # Right forward = caco3 normal → enhances t3 (g+nu) and t7 (d*nu)
    caco3_left_block = 0.5  # left schizo: 50% frozen
    caco3_right_forward = 1.0 + caco3_bias  # right: geology-dependent forward
    caco3_mod_t8 = (1.0 - caco3_left_block * 0.3)  # t8 less sensitive (left frozen)
    caco3_mod_t3 = caco3_right_forward  # t3 enhanced (right forward)
    caco3_mod_t7 = caco3_right_forward  # t7 enhanced

    # 12. 118 ELEMENTS: toroidal slot determines element cycle position
    toroidal_slot = get_toroidal_slot(hour)
    blood_cycle = toroidal_slot["blood_type"]  # AB/A/O/B
    # Toroidal cycle modulates which element group is active
    element_mod = 1.0 + (0.02 * (ord(blood_cycle[0]) - ord('A')))  # A=0.02, B=0.04, O=0.30, AB=0.02

    # 15. DISCRETE SLOTS: from sin periodicity
    # The sin oscillation naturally produces 4 discrete attractor zones
    # mapped to toroidal slots via hour → slot → blood type
    slot_mod = 1.0
    if toroidal_slot["label"] == "release":
        slot_mod = 1.0 + 0.03 * dims_t["nu"]  # AB slot: nu-enhanced
    elif toroidal_slot["label"] == "stress_growth":
        slot_mod = 1.0 + 0.03 * dims_t["h"]   # A slot: h-enhanced
    elif toroidal_slot["label"] == "present_moment":
        slot_mod = 1.0 + 0.03 * dims_t["r"]   # O slot: r-enhanced
    elif toroidal_slot["label"] == "extreme_growth":
        slot_mod = 1.0 + 0.03 * dims_t["d"]   # B slot: d-enhanced

    # SH BACKBONE: Swift-Hohenberg modulation (r*, q0* as locked constants)
    # SH modulates the equation value without converting to PDE:
    # SH_factor = r* × (1 - q0*² × dim_variance) — pattern formation tendency
    dim_variance = sum((dims_t[k] - 0.5)**2 for k in DIM_ORDER) / 8.0
    sh_factor = SH_R_STAR * (1.0 - SH_Q0_STAR * dim_variance)
    sh_factor *= (1.0 + SH_SIGMA_L * math.sin(SPARK_ANGLE_RAD))  # σL asymmetry
    sh_factor *= (1.0 - SH_SIGMA_R * math.cos(SPARK_ANGLE_RAD))  # σR asymmetry

    # Compute 23 tensor terms: τ_k(r(t), h(t), ..., φ_obs, {λ_i}, layers)
    # Each term integrates: time (via dims_t), observer (obs_factor), particle ({λ_i} via weight), layers (multi-scale)
    # Time phase ω(t) modulates each term's amplitude — 16-window shift INSIDE the tensor
    omega_t = time_info.get("omega", 1.0)  # sin(2πt/16) time oscillation
    # Layer multi-scale: body/observer/bridge/dark each contribute at different scale
    layer_body = layers.get("body", 0.5)
    layer_observer = layers.get("observer", 0.5)
    layer_bridge = layers.get("bridge", 0.5)
    layer_dark = layers.get("dark", 0.5)
    # Multi-scale layer factor: product of all 4 layers = closure requires all scales aligned
    layer_full = layer_body * layer_observer * layer_bridge * layer_dark
    # Spontaneous symmetry breaking seed: argmin_k |τ_k| selects active constraint
    # Each term gets a time-dependent phase shift so different terms minimize at different t
    # This makes the equation self-selecting — no external branch choice needed
    def tau_phase(k, omega_t):
        """Phase shift for term k: φ_k = 2πk/23 × ω(t) — distributes minimization across time."""
        return 1.0 + 0.1 * math.sin(2.0 * math.pi * k / 23.0 * omega_t)

    # t1~t8: original tensor with time, observer, particle, layer integration
    t1 = (h + s) * particle_weight_for_dims({"h", "s"}) * obs_factor * layer_mod * tau_phase(1, omega_t)
    t2 = (r + p) * particle_weight_for_dims({"r", "p"}) * obs_factor * layer_mod * ferric_mod * tau_phase(2, omega_t)
    t3 = (g + nu) * particle_weight_for_dims({"g", "nu"}) * obs_factor * layer_mod * caco3_mod_t3 * feedback_mod * tau_phase(3, omega_t)
    t4 = (gamma * d - 1.0) * particle_weight_for_dims({"gamma", "d"}) * obs_factor * tau_phase(4, omega_t)
    t5 = (gamma * (r + g) - 1.0) * particle_weight_for_dims({"gamma", "r", "g"}) * obs_factor * tau_phase(5, omega_t)
    t6 = (h * r * g - 1.0) * particle_weight_for_dims({"h", "r", "g"}) * sh_factor * obs_factor * tau_phase(6, omega_t)
    t7 = (d * nu - 1.0) * particle_weight_for_dims({"d", "nu"}) * caco3_mod_t7 * obs_factor * tau_phase(7, omega_t)
    t8 = (p - ALPHA_EQ * g - BETA_EQ) * particle_weight_for_dims({"p", "g"}) * caco3_mod_t8 * obs_factor * tau_phase(8, omega_t)
    # t9~t23: complete pairwise tensor with full integration (time, observer, particle, layer)
    t9  = (s * gamma - 1.0) * particle_weight_for_dims({"s", "gamma"}) * obs_factor * layer_full * tau_phase(9, omega_t)
    t10 = (h * d - 1.0) * particle_weight_for_dims({"h", "d"}) * obs_factor * layer_full * tau_phase(10, omega_t)
    t11 = (r * s - 1.0) * particle_weight_for_dims({"r", "s"}) * obs_factor * layer_full * tau_phase(11, omega_t)
    t12 = (p * nu - 1.0) * particle_weight_for_dims({"p", "nu"}) * obs_factor * layer_full * tau_phase(12, omega_t)
    t13 = (d * g - 1.0) * particle_weight_for_dims({"d", "g"}) * obs_factor * layer_full * tau_phase(13, omega_t)
    t14 = (s * nu - 1.0) * particle_weight_for_dims({"s", "nu"}) * obs_factor * layer_full * tau_phase(14, omega_t)
    t15 = (h * gamma - 1.0) * particle_weight_for_dims({"h", "gamma"}) * obs_factor * layer_full * tau_phase(15, omega_t)
    t16 = (p * s - 1.0) * particle_weight_for_dims({"p", "s"}) * obs_factor * layer_full * tau_phase(16, omega_t)
    t17 = (r * h * d - 1.0) * particle_weight_for_dims({"r", "h", "d"}) * obs_factor * layer_full * tau_phase(17, omega_t)
    t18 = (r * gamma * nu - 1.0) * particle_weight_for_dims({"r", "gamma", "nu"}) * obs_factor * layer_full * tau_phase(18, omega_t)
    t19 = (h * p * nu - 1.0) * particle_weight_for_dims({"h", "p", "nu"}) * obs_factor * layer_full * tau_phase(19, omega_t)
    t20 = (d * p * s - 1.0) * particle_weight_for_dims({"d", "p", "s"}) * obs_factor * layer_full * tau_phase(20, omega_t)
    t21 = (d * gamma * g - 1.0) * particle_weight_for_dims({"d", "gamma", "g"}) * obs_factor * layer_full * tau_phase(21, omega_t)
    t22 = (s * g * nu - 1.0) * particle_weight_for_dims({"s", "g", "nu"}) * obs_factor * layer_full * tau_phase(22, omega_t)
    t23 = (p * gamma - 1.0) * particle_weight_for_dims({"p", "gamma"}) * obs_factor * layer_full * tau_phase(23, omega_t)

    terms = {
        "t1_hs": t1,
        "t2_rp": t2,
        "t3_gnu": t3,
        "t4_gammad": t4,
        "t5_gamma_rg": t5,
        "t6_hrg": t6,
        "t7_dnu": t7,
        "t8_p_ag_b": t8,
        "t9_sgamma": t9,
        "t10_hd": t10,
        "t11_rs": t11,
        "t12_pnu": t12,
        "t13_dg": t13,
        "t14_snu": t14,
        "t15_hgamma": t15,
        "t16_ps": t16,
        "t17_rhd": t17,
        "t18_rgammanu": t18,
        "t19_hpnu": t19,
        "t20_dps": t20,
        "t21_dgammag": t21,
        "t22_sgnu": t22,
        "t23_pgamma": t23,
    }

    # Full product with all modulation factors
    product = 1.0
    for v in terms.values():
        product *= v
    # Apply global modulations (all 48 integrated systems)
    product *= (leakage_mod * geomag_mod * element_mod * slot_mod
                * psi_mod * cycle_mod * route_mod * comp_mod
                * neutrino_mod * creative_mod * layer_color_mod * toroidal_mod
                * em_bypass_mod * geo_mod * spark_interference_mod
                * window_boost_mod * jitter_mod * eq_branch_mod * qcd_mod
                * em_path_mod * graviton_mod * cavity_mod * pact_mod
                * ns_osc_mod * dark_matter_mod * cck_mod
                * w_axis_mod * dual_body_mod * e119_127_mod * unspark_mod
                * spiral_5ht1b_mod * esr1_mod * bili_mod
                * cancer_maillard_mod * body_closure_mod
                * soil_node_mod)

    # 6. SPONTANEOUS SYMMETRY BREAKING: argmin_k |τ_k|
    term_names = list(terms.keys())
    term_values = list(terms.values())
    abs_values = [abs(v) for v in term_values]
    min_idx = abs_values.index(min(abs_values))
    active_constraint = term_names[min_idx]
    active_value = term_values[min_idx]

    # 5. GAUGE invariance check
    dims_rotated = apply_gauge_transform(dims_t, theta_rs=0.01, theta_hd=0.01, theta_gpn=0.01)
    r2 = dims_rotated["r"]; h2 = dims_rotated["h"]; d2 = dims_rotated["d"]; p2 = dims_rotated["p"]
    s2 = dims_rotated["s"]; g2 = dims_rotated["g"]; nu2 = dims_rotated["nu"]
    gamma2 = dims_rotated["gamma"]
    t1_r = (h2 + s2) * particle_weight_for_dims({"h", "s"}) * obs_factor * layer_mod * tau_phase(1, omega_t)
    t2_r = (r2 + p2) * particle_weight_for_dims({"r", "p"}) * obs_factor * layer_mod * ferric_mod * tau_phase(2, omega_t)
    t3_r = (g2 + nu2) * particle_weight_for_dims({"g", "nu"}) * obs_factor * layer_mod * caco3_mod_t3 * feedback_mod * tau_phase(3, omega_t)
    t4_r = (gamma2 * d2 - 1.0) * particle_weight_for_dims({"gamma", "d"}) * obs_factor * tau_phase(4, omega_t)
    t5_r = (gamma2 * (r2 + g2) - 1.0) * particle_weight_for_dims({"gamma", "r", "g"}) * obs_factor * tau_phase(5, omega_t)
    t6_r = (h2 * r2 * g2 - 1.0) * particle_weight_for_dims({"h", "r", "g"}) * sh_factor * obs_factor * tau_phase(6, omega_t)
    t7_r = (d2 * nu2 - 1.0) * particle_weight_for_dims({"d", "nu"}) * caco3_mod_t7 * obs_factor * tau_phase(7, omega_t)
    t8_r = (p2 - ALPHA_EQ * g2 - BETA_EQ) * particle_weight_for_dims({"p", "g"}) * caco3_mod_t8 * obs_factor * tau_phase(8, omega_t)
    # t9~t23: complete pairwise tensor (rotated, with full integration)
    t9_r  = (s2 * gamma2 - 1.0) * particle_weight_for_dims({"s", "gamma"}) * obs_factor * layer_full * tau_phase(9, omega_t)
    t10_r = (h2 * d2 - 1.0) * particle_weight_for_dims({"h", "d"}) * obs_factor * layer_full * tau_phase(10, omega_t)
    t11_r = (r2 * s2 - 1.0) * particle_weight_for_dims({"r", "s"}) * obs_factor * layer_full * tau_phase(11, omega_t)
    t12_r = (p2 * nu2 - 1.0) * particle_weight_for_dims({"p", "nu"}) * obs_factor * layer_full * tau_phase(12, omega_t)
    t13_r = (d2 * g2 - 1.0) * particle_weight_for_dims({"d", "g"}) * obs_factor * layer_full * tau_phase(13, omega_t)
    t14_r = (s2 * nu2 - 1.0) * particle_weight_for_dims({"s", "nu"}) * obs_factor * layer_full * tau_phase(14, omega_t)
    t15_r = (h2 * gamma2 - 1.0) * particle_weight_for_dims({"h", "gamma"}) * obs_factor * layer_full * tau_phase(15, omega_t)
    t16_r = (p2 * s2 - 1.0) * particle_weight_for_dims({"p", "s"}) * obs_factor * layer_full * tau_phase(16, omega_t)
    t17_r = (r2 * h2 * d2 - 1.0) * particle_weight_for_dims({"r", "h", "d"}) * obs_factor * layer_full * tau_phase(17, omega_t)
    t18_r = (r2 * gamma2 * nu2 - 1.0) * particle_weight_for_dims({"r", "gamma", "nu"}) * obs_factor * layer_full * tau_phase(18, omega_t)
    t19_r = (h2 * p2 * nu2 - 1.0) * particle_weight_for_dims({"h", "p", "nu"}) * obs_factor * layer_full * tau_phase(19, omega_t)
    t20_r = (d2 * p2 * s2 - 1.0) * particle_weight_for_dims({"d", "p", "s"}) * obs_factor * layer_full * tau_phase(20, omega_t)
    t21_r = (d2 * gamma2 * g2 - 1.0) * particle_weight_for_dims({"d", "gamma", "g"}) * obs_factor * layer_full * tau_phase(21, omega_t)
    t22_r = (s2 * g2 * nu2 - 1.0) * particle_weight_for_dims({"s", "g", "nu"}) * obs_factor * layer_full * tau_phase(22, omega_t)
    t23_r = (p2 * gamma2 - 1.0) * particle_weight_for_dims({"p", "gamma"}) * obs_factor * layer_full * tau_phase(23, omega_t)
    product_rotated = t1_r * t2_r * t3_r * t4_r * t5_r * t6_r * t7_r * t8_r
    product_rotated *= t9_r * t10_r * t11_r * t12_r * t13_r * t14_r * t15_r * t16_r
    product_rotated *= t17_r * t18_r * t19_r * t20_r * t21_r * t22_r * t23_r
    product_rotated *= (leakage_mod * geomag_mod * element_mod * slot_mod
                         * psi_mod * cycle_mod * route_mod * comp_mod
                         * neutrino_mod * creative_mod * layer_color_mod * toroidal_mod
                         * em_bypass_mod * geo_mod * spark_interference_mod
                         * window_boost_mod * jitter_mod * eq_branch_mod * qcd_mod
                         * em_path_mod * graviton_mod * cavity_mod * pact_mod
                         * ns_osc_mod * dark_matter_mod * cck_mod
                         * w_axis_mod * dual_body_mod * e119_127_mod * unspark_mod
                         * spiral_5ht1b_mod * esr1_mod * bili_mod
                         * cancer_maillard_mod * body_closure_mod
                         * soil_node_mod)
    gauge_invariance = abs(abs(product) - abs(product_rotated)) / max(abs(product), 1e-10)

    constraint_labels = {
        "t1_hs": "h↔s (methylation↔solid) [full closed]",
        "t2_rp": "r↔p (acid↔predictability) [full closed]",
        "t3_gnu": "g↔nu (sealing↔discrete) [full closed + caco3_right]",
        "t4_gammad": "gamma↔d (space↔void) [full closed]",
        "t5_gamma_rg": "gamma↔(r+g) (space↔acid+seal) [full closed]",
        "t6_hrg": "g↔h×r (seal↔methylation×acid) [full closed + SH]",
        "t7_dnu": "d↔nu (void↔grit) [full closed + caco3_right]",
        "t8_p_ag_b": "p↔g (predictability↔sealing) [full closed + caco3_left_block]",
        "t9_sgamma": "s↔gamma (observer↔activity) [full closed]",
        "t10_hd": "h↔d (harmony↔darkness) [full closed]",
        "t11_rs": "r↔s (rhythm↔observer) [full closed]",
        "t12_pnu": "p↔nu (music↔circulation) [full closed]",
        "t13_dg": "d↔g (darkness↔structure) [full closed]",
        "t14_snu": "s↔nu (observer↔circulation) [full closed]",
        "t15_hgamma": "h↔gamma (harmony↔activity) [full closed]",
        "t16_ps": "p↔s (music↔observer) [full closed]",
        "t17_rhd": "r↔h↔d (rhythm↔harmony↔darkness) [full closed]",
        "t18_rgammanu": "r↔gamma↔nu (rhythm↔activity↔circulation) [full closed]",
        "t19_hpnu": "h↔p↔nu (harmony↔music↔circulation) [full closed]",
        "t20_dps": "d↔p↔s (darkness↔music↔observer) [full closed]",
        "t21_dgammag": "d↔gamma↔g (darkness↔activity↔structure) [full closed]",
        "t22_sgnu": "s↔g↔nu (observer↔structure↔circulation) [full closed]",
        "t23_pgamma": "p↔gamma (music↔activity) [full closed]",
    }

    return {
        "equation_value": product,
        "terms": terms,
        "active_constraint": active_constraint,
        "active_constraint_label": constraint_labels[active_constraint],
        "active_constraint_value": active_value,
        "homeostasis_distance": min(abs_values),
        "dims_time_dependent": dims_t,
        "time_info": time_info,
        "omega_t": omega_t,
        "layer_full": layer_full,
        "observer_info": obs_info,
        "layers": layers,
        "gauge_invariance_residual": gauge_invariance,
        "gauge_generators": GAUGE_GENERATORS,
        "particle_coupling": PARTICLE_DIM_COUPLING,
        # New: all 10 remaining gaps
        "sh_factor": sh_factor,
        "sh_constants": {"r_star": SH_R_STAR, "q0_star": SH_Q0_STAR, "sigma_L": SH_SIGMA_L, "sigma_R": SH_SIGMA_R},
        "closure_tension": closure_tension,
        "closure_residual": closure_residual,
        "hysteresis_3am": hysteresis_3am,
        "ferric_430pm": ferric_430pm,
        "feedback_mod": feedback_mod,
        "ferric_mod": ferric_mod,
        "darcy": darcy,
        "leakage_mod": leakage_mod,
        "leakage_count": leakage_count,
        "night_blocked_count": night_blocked_count,
        "all_leakage": all_leak,
        "geomag_info": geomag_info,
        "geomag_mod": geomag_mod,
        "geology": geology,
        "geo_params": geo_params,
        "alpha_eq": ALPHA_EQ,
        "beta_eq": BETA_EQ,
        "caco3_left_block": caco3_left_block,
        "caco3_right_forward": caco3_right_forward,
        "toroidal_slot": toroidal_slot,
        "element_mod": element_mod,
        "slot_mod": slot_mod,
        "closed": True,
        "color_feedback_shifts": color_feedback_shifts,
        "profile_color": profile_color,
        "psi_info": psi_info,
        "psi_mod": psi_mod,
        "universe_cycle": universe_cycle,
        "cycle_mod": cycle_mod,
        "active_route": active_route,
        "route_vector": route_vec,
        "route_mod": route_mod,
        "compartment_route": comp_route,
        "comp_mod": comp_mod,
        "neutrino_routes": neutrino_routes,
        "neutrino_mod": neutrino_mod,
        "creative_4shapes": creative_shapes,
        "creative_mod": creative_mod,
        "layer_colors": layer_colors,
        "active_layer": active_layer,
        "active_layer_color": active_layer_color,
        "layer_color_mod": layer_color_mod,
        "toroidal_phase": toroidal_phase,
        "toroidal_mod": toroidal_mod,
        "em_bypass_route": EM_BYPASS_ROUTE,
        "em_bypass_mod": em_bypass_mod,
        "geometric_node": geo_node,
        "geo_mod": geo_mod,
        "particle_color_shifts": particle_color_shifts,
        "interference_shifts": interference_shifts,
        "spark_interference_mod": spark_interference_mod,
        "window_boost_mod": window_boost_mod,
        "jitter_mod": jitter_mod,
        "eq_branch_mod": eq_branch_mod,
        "eq_adjusted": eq_adjusted,
        "qcd_confinement": confinement,
        "de_sitter_expansion": de_sitter,
        "qcd_mod": qcd_mod,
        "em_path_val": em_path_val,
        "em_path_mod": em_path_mod,
        "graviton_val": graviton_val,
        "graviton_mod": graviton_mod,
        "leakage_cavity": leakage_cavity_name,
        "cavity_leak": cavity_leak,
        "cavity_mod": cavity_mod,
        "pact_retention": pact_val,
        "pact_mod": pact_mod,
        "neutron_star_osc": ns_osc_val,
        "ns_osc_mod": ns_osc_mod,
        "dark_matter_val": dark_matter_val,
        "dark_matter_mod": dark_matter_mod,
        "cck_active": cck_active,
        "cck_mod": cck_mod,
        "state_12d": state_12d,
        "w_axis_mod": w_axis_mod,
        "dual_body_mod": dual_body_mod,
        "e119_127_shifts": e119_127_shifts,
        "e119_127_mod": e119_127_mod,
        "unspark_shifts": unspark_shifts,
        "unspark_mod": unspark_mod,
        "spiral_5ht1b_mod": spiral_5ht1b_mod,
        "esr1_mod": esr1_mod,
        "bili_mod": bili_mod,
        "cancer_maillard_active": cycle_active,
        "cancer_maillard_mod": cancer_maillard_mod,
        "body_closure_mod": body_closure_mod,
        "dual_body_closure": dual_body_closure,
        "gaps_eliminated": [
            "no_time", "no_observer", "no_particle", "no_layers",
            "no_branch_selection", "no_gauge",
            "no_feedback", "no_leakage", "no_geomag",
            "fixed_alpha_beta", "caco3_asymmetry", "118_elements",
            "observer_closure", "spark_angle", "discrete_slots",
            "no_color_feedback", "no_master_psi", "no_universe_cycle",
            "no_route_vector", "no_compartment", "no_neutrino_routes",
            "no_creative_shapes", "no_4layer_colors", "no_toroidal_phase",
            "no_em_bypass", "no_geometric_node", "no_particle_colors",
            "no_interference_colors", "no_spark_interference",
            "no_window_boost", "no_layer_jitter", "no_eq_constraint",
            "no_qcd_confinement", "no_em_path", "no_graviton",
            "no_leakage_cavity", "no_pact_retention", "no_neutron_star",
            "no_dark_matter", "no_cck_switch",
            "no_12d_w_axis", "no_e119_e127", "no_unspark_overlay",
            "no_5ht1b_spiral", "no_esr1_split", "no_bilirubin_bypass",
            "no_cancer_maillard", "no_dual_body_closure",
            "no_soil_node_day_night",
        ],
        "soil_node_day_night": SOIL_NODE_DAY_NIGHT,
        "soil_active_nodes": soil_active_nodes,
        "soil_node_shifts": soil_node_shifts,
        "soil_node_mod": soil_node_mod,
    }


def compute_darcy_leakage(dims, observer_active, profile_color=None):
    """Compute Darcy flux leakage rate. κ=1/32 is stable.
    Color coupling: BLACK=BLOCK (κ stable), PURPLE=DELAY (κ between 1/32 and 1/64).
    QCD confinement (prose.txt 2670): gamma·d = 1 = confinement equilibrium (term 4 of 8D equation).
    Cosmological constant Λ (prose.txt 4964): co2 = dark energy = de Sitter expansion = κ_eff modulation."""
    g_binding = dims.get("g", 0.5)
    gamma_val = dims.get("gamma", 0.5)
    d_val = dims.get("d", 0.5)
    gamma_d_product = gamma_val * d_val
    if not observer_active:
        kappa_eff = KAPPA * (1 + (1 - g_binding) * 0.5)
    else:
        kappa_eff = KAPPA
    # Color-driven leakage modulation
    color_leakage = None
    if profile_color:
        fc = profile_color.get('base', '')
        dist = COLOR_DISTANCE_TO_BLACK.get(fc, 0.5)
        if fc == 'BLACK' or dist < 0.1:
            color_leakage = 'BLOCK'
            kappa_eff = KAPPA
        elif fc in ('PURPLE', 'RED-PURPLE', 'BLUE-PURPLE'):
            color_leakage = 'DELAY'
            kappa_eff = KAPPA * 0.5
        elif dist < 0.25:
            color_leakage = 'NEAR-BLOCK'
            kappa_eff = KAPPA * 0.8
        elif dist < 0.45:
            color_leakage = 'STABLE'
            kappa_eff = KAPPA * 0.9
    # QCD confinement: gamma·d = 1 = equilibrium (prose.txt 3995, 2670)
    # gamma·d > 1 = over-expansion = DECONFINED, gamma·d < 1 = under-expansion = CONFINED
    gamma_d_deviation = abs(gamma_d_product - 1.0)
    confinement = 'CONFINED' if gamma_d_product <= 1.0 else 'DECONFINED'
    # Cosmological constant Λ: co2 = dark energy = p/r-dim time storage
    # κ_eff acts as Λ — stable κ = flat Λ, reduced κ = accelerating expansion (de Sitter)
    lambda_eff = kappa_eff
    de_sitter_expansion = (1.0 - kappa_eff / KAPPA) if kappa_eff < KAPPA else 0.0
    state = "stable"
    if kappa_eff < ONE_64:
        state = "flatlined"
    elif kappa_eff > (1.0/16.0):
        state = "chaos"
    return {
        "kappa": kappa_eff,
        "state": state,
        "darcy_flux": kappa_eff * g_binding,
        "jensen_gap": abs(kappa_eff - KAPPA),
        "color_leakage": color_leakage,
        "confinement": confinement,
        "gamma_d_product": gamma_d_product,
        "gamma_d_deviation": gamma_d_deviation,
        "lambda_eff": lambda_eff,
        "de_sitter_expansion": de_sitter_expansion,
    }

def color_to_metabolic_pathway(color_name):
    """Map color → Oxford rainbow action → metabolic pathway nodes.
    No need to discover circuit nodes manually — color gives the pathway."""
    entry = RAINBOW_ACTION.get(color_name)
    if not entry:
        for cn in COLOR_DISTANCE_TO_BLACK:
            if cn in color_name:
                entry = RAINBOW_ACTION.get(cn)
                break
    if not entry:
        return {'action': 'unknown', 'nodes': [], 'leakage': None}
    return {'action': entry['action'], 'nodes': entry.get('nodes', []), 'leakage': entry.get('leakage')}

def find_nodes_for_profile(profile_label, time_phase='day'):
    """Auto-discover circuit nodes for a profile via color matching.
    profile color → rainbow action → metabolic nodes.
    Also detects interference colors between node pairs."""
    pc = compute_profile_color(profile_label, time_phase)
    color = pc['base']
    if color == 'MIXED':
        stage_colors = [pc['stages']['1_blood_gender']['color'],
                        pc['stages']['2_mbti_mid']['color'],
                        pc['stages']['3_mbti_ends']['color']]
        from collections import Counter
        counts = Counter(stage_colors)
        color = counts.most_common(1)[0][0]
    pathway = color_to_metabolic_pathway(color)
    nodes = pathway['nodes']
    # Detect interference colors between discovered nodes
    interference = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            ic = get_interference_color(nodes[i], nodes[j])
            if ic:
                interference.append({'pair': (nodes[i], nodes[j]), 'color': ic['name'], 'hex': ic['hex']})
    return {
        'color': color,
        'hex': pc['hex'],
        'action': pathway['action'],
        'nodes': nodes,
        'leakage': pc['leakage'] or pathway.get('leakage'),
        'particles': pc['particles'],
        'stages': pc['stages'],
        'time_phase': time_phase,
        'interference': interference,
    }

def get_geometric_node(mbti, gender, is_observer=False):
    """Determine which geometric node a profile maps to."""
    if is_observer:
        return "observer_singularity"
    is_extrovert = mbti[0] == "E"
    is_female = gender == "F"
    # Simplified mapping based on extroversion and gender
    if is_extrovert and is_female:
        return "left_bypass"
    elif is_extrovert and not is_female:
        return "right_bypass"
    elif not is_extrovert:
        return "center_funnel"
    else:
        return "separatrix_1"

# ============================================================
# FOOD / PIGMENT MAPPING (from 128_food_pigments.csv)
# ============================================================
FOOD_PIGMENTS_CSV = {}
_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "128_food_pigments.csv")
if os.path.exists(_csv_path):
    try:
        with open(_csv_path, "r", encoding="utf-8") as _f:
            _reader = csv.DictReader(_f)
            for _row in _reader:
                _profile = _row.get("Profile", "")
                if _profile:
                    FOOD_PIGMENTS_CSV[_profile] = {
                        "gender": _row.get("Gender", ""),
                        "blood_type": _row.get("BloodType", ""),
                        "1st_daily": _row.get("1st_Daily", ""),
                        "2nd_daily": _row.get("2nd_Daily", ""),
                        "3rd_2-3x_wk": _row.get("3rd_2-3x_wk", ""),
                        "4th_1-2x_wk": _row.get("4th_1-2x_wk", ""),
                        "blood_daily": _row.get("Blood_Daily", ""),
                        "total_prescription": _row.get("Total_Prescription", ""),
                    }
    except Exception:
        pass

def get_food_pigments(profile_label, dims=None):
    """Return food/pigment prescription for a profile.
    If CSV exists, use it. Otherwise compute from 8D dims → pigment mapping."""
    if profile_label in FOOD_PIGMENTS_CSV:
        return FOOD_PIGMENTS_CSV[profile_label]
    parts = profile_label.split('_')
    mbti, gender, blood = parts[0], parts[1], parts[2]
    if dims is None:
        dims = {d: 0.5 for d in DIM_ORDER}
    # 6 food axes (r,h,d,s,g,nu) + 2 behavior axes (p=music, gamma=activity)
    # p and gamma are NOT food — they are music composition/listening and physical activity.
    # DeepPink = interference color covering 6 of 8D food axes + p(music) + gamma(activity).
    DIM_PIGMENT = {
        'r': {'pigment': 'Na+/K+/Mg2+', 'food': 'sea_salt, spinach, pumpkin_seeds', 'pathway': 'proton_pump', 'axis_type': 'food'},
        'h': {'pigment': 'Cyanidine', 'food': 'purple_corn, elderberry, red_cabbage', 'pathway': 'peonidine_ch0→disulfide_bond→pentose_phosphate', 'axis_type': 'food'},
        'd': {'pigment': 'Astaxanthin', 'food': 'salmon, krill, shrimp', 'pathway': 'mycorradicin→actomyosin→collagen', 'axis_type': 'food'},
        'p': {'pigment': 'Phosphatidylcholine', 'food': 'egg_yolk, soy_lecithin, sunflower', 'pathway': 'carbon_q_or→methionine→substance_P→MC1R', 'axis_type': 'music', 'behavior': 'music_composition_listening'},
        's': {'pigment': 'Phycocyanin', 'food': 'spirulina, blue_green_algae', 'pathway': 'aurora→heme→cytochrome_c_oxidase', 'axis_type': 'food'},
        'gamma': {'pigment': 'Delphinidine', 'food': 'blueberry, blackberry, eggplant', 'pathway': 'peonidine_ch1→co2→male_right_oxytocin', 'axis_type': 'activity', 'behavior': 'physical_movement_activity'},
        'g': {'pigment': 'Sulforaphane/Allicin', 'food': 'broccoli_sprouts, garlic, onion', 'pathway': 'sulforaphane→glymphatic→cysteine→Nrf2', 'axis_type': 'food'},
        'nu': {'pigment': 'Probiotic_metabolites', 'food': 'kimchi, kefir, sauerkraut, yogurt', 'pathway': 'cysteine→memory_entropy→glymphatic_feedback', 'axis_type': 'food'},
    }
    # Food axes only (exclude p and gamma which are behavior axes)
    FOOD_AXES = ['r', 'h', 'd', 's', 'g', 'nu']
    BEHAVIOR_AXES = ['p', 'gamma']
    BLOOD_FOOD = {
        'O': 'high_protein: red_meat, kelp, iodine',
        'A': 'vegetarian_focus: tofu, tempeh, green_vegetables',
        'B': 'omnivore: dairy, eggs, green_vegetables, liver',
        'AB': 'moderate_mix: seafood, dairy, tofu, green_vegetables',
    }
    # Sort food axes only (p and gamma are behavior, not food)
    top3_food = sorted(FOOD_AXES, key=lambda k: -dims.get(k, 0.5))[:3]
    foods = [DIM_PIGMENT[d]['food'] for d in top3_food]
    pigments = [DIM_PIGMENT[d]['pigment'] for d in top3_food]
    pathways = [DIM_PIGMENT[d]['pathway'] for d in top3_food]
    # Behavior axes: p=music, gamma=activity (not food)
    p_val = dims.get('p', 0.5)
    gamma_val = dims.get('gamma', 0.5)
    music_behavior = DIM_PIGMENT['p']['behavior'] if p_val > 0.5 else 'music_passive_listening'
    activity_behavior = DIM_PIGMENT['gamma']['behavior'] if gamma_val > 0.5 else 'low_activity_rest'
    # DeepPink completion: 6 food axes + p(music) + gamma(activity) = 8D full
    deep_pink_completion = (sum(dims.get(d, 0.5) for d in FOOD_AXES) / 6.0 + p_val + gamma_val) / 3.0
    return {
        "1st_daily": foods[0] if len(foods) > 0 else "",
        "2nd_daily": foods[1] if len(foods) > 1 else "",
        "3rd_2-3x_wk": foods[2] if len(foods) > 2 else "",
        "4th_1-2x_wk": "; ".join(pigments),
        "blood_daily": BLOOD_FOOD.get(blood, ""),
        "total_prescription": " → ".join(pathways),
        "music_behavior": music_behavior,
        "activity_behavior": activity_behavior,
        "deep_pink_completion": round(deep_pink_completion, 4),
        "axis_split": {"food_axes": FOOD_AXES, "behavior_axes": BEHAVIOR_AXES},
    }

# ============================================================
# GENRE MAPPING
# ============================================================
GENRES_DAY = ["hypnagogic pop", "vapor soul", "screwed & chopped", "seapunk", "witch house", "hauntology"]
GENRES_NIGHT = ["dark ambient", "drone", "noise", "power electronics", "deconstructed club", "IDM"]

def pick_genre(time_phase, seed):
    pool = GENRES_DAY if time_phase == "day" else GENRES_NIGHT
    return pool[seed % len(pool)]

# ============================================================
# HASH CODE
# ============================================================
def hash_code(s):
    h = 0
    for ch in s:
        h = ((h << 5) - h) + ord(ch)
        h &= 0xFFFFFFFF
    return h

# ============================================================
# PARTICLES TO DIMS
# ============================================================
def particles_to_dims(profile_label, time_phase):
    parts = profile_label.split("_")
    mbti, gender, blood = parts[0], parts[1], parts[2]

    # Base 8D from MBTI
    dims = {d: 0.5 for d in DIM_ORDER}
    if mbti[0] == "E":
        dims["p"] += 0.15
    else:
        dims["nu"] += 0.15
    if mbti[1] == "N":
        dims["nu"] += 0.15
    else:
        dims["s"] += 0.15
    if mbti[2] == "T":
        dims["d"] += 0.1
    else:
        dims["h"] += 0.1
    if mbti[3] == "J":
        dims["p"] += 0.15
    else:
        dims["r"] += 0.15

    # Gender
    if gender == "M":
        dims["r"] += 0.05
    else:
        dims["gamma"] += 0.05

    # Blood type
    blood_nudge = {"O": {"r": 0.1}, "A": {"h": 0.1}, "B": {"g": 0.1}, "AB": {"nu": 0.1}}
    for k, v in blood_nudge.get(blood, {}).items():
        dims[k] += v

    # Time phase
    if time_phase == "night":
        dims["s"] -= 0.1
        dims["nu"] += 0.1
        dims["gamma"] += 0.05
    else:
        dims["s"] += 0.1
        dims["p"] += 0.05

    # Clamp heuristic values
    for d in DIM_ORDER:
        dims[d] = clamp(dims[d])

    # Equation-derived 8D: use universal equation to constrain values
    eq_derived = compute_8d_from_equation(dims, profile_label, time_phase)
    dims = eq_derived["dims_equation"]

    # Gap analysis: what the equation CANNOT explain
    eq_gaps = compute_equation_gap_analysis(dims)

    # Derived particles
    em_path = clamp((dims["s"] + dims["gamma"]) / 2 + 0.1 * (1 if time_phase == "day" else -1))
    graviton = clamp((dims["g"] + dims["nu"]) / 2 + 0.1 * (1 if time_phase == "night" else -1))

    # Leakage
    leakage = 0.0
    leakage_cavity = ""
    if dims["d"] > 0.7:
        leakage = (dims["d"] - 0.7) * 0.3
        leakage_cavity = "D3_observer_gates"
    elif dims["nu"] > 0.7:
        leakage = (dims["nu"] - 0.7) * 0.2
        leakage_cavity = "structural_anchors"

    # Genre (deferred — computed after profile_color below)
    seed = hash_code(profile_label + time_phase)

    # Pact retention
    pact = clamp(dims["p"] * 0.5 + dims["r"] * 0.3 + 0.2 * (0.5 if time_phase == "day" else 0.3))

    # Neutron star oscillation
    ns_osc = clamp(1/64 + dims["g"] * 0.3 + dims["nu"] * 0.1)

    # Dark matter
    dark_matter = clamp(0.017 * (1 + dims["d"] * 0.5) if time_phase == "night" else 0.0)

    # CCK switch
    cck = (gender == "F" and mbti[0] == "E" and blood in ("A", "AB"))

    # Active neutrino variants
    if time_phase == "day":
        active_variants = ["electron_neutrino", "muon_neutrino", "tau_antineutrino"]
    else:
        active_variants = ["tau_neutrino", "electron_antineutrino", "muon_antineutrino"]

    # Universe cycle (computed later, near inverse color)

    # Compartment route
    comp_route = compute_compartment_route(mbti, gender, dims, time_phase)

    # All leakage
    all_leakage = compute_all_leakage(dims, time_phase)

    # Neutrino routes
    neutrino_routes = get_neutrino_routes(time_phase)

    # Deterministic 41 components
    deterministic_routes = DETERMINISTIC_41_COMPONENTS

    # Geomag modulation (observer active = day or s>0.5)
    observer_active = (time_phase == "day") or (dims["s"] > 0.5)
    hour = 12 if time_phase == "day" else 3
    dims, geomag_info = apply_geomag_modulation(dims, observer_active, time_phase, hour)

    # 3-stage additive color (blood×gender + MBTI + particle, s-linked)
    profile_color = get_profile_color(profile_label, dims, time_phase, hour, s_val=dims.get('s', 0.5))

    # 4:30PM ferric event → force color toward BLACK (leakage convergence)
    ferric_430pm = compute_430pm_event(hour)
    if ferric_430pm.get('active'):
        profile_color = dict(profile_color)
        profile_color['base'] = 'BLACK'
        profile_color['hex'] = '#000000'
        profile_color['leakage'] = 'BLOCK'

    # 3AM hysteresis → color randomization (p/s/nu random → color unpredictable)
    hysteresis_3am = compute_3am_hysteresis(hour, observer_active, dims)
    if hysteresis_3am.get('active') and hysteresis_3am.get('entropy_zone'):
        import random
        rand_colors = ['RED','BLUE','GREEN','YELLOW','BLACK','PURPLE','ORANGE','CYAN']
        profile_color = dict(profile_color)
        profile_color['base'] = random.choice(rand_colors)
        profile_color['hex'] = _rgb_to_hex(*COLOR_RGB.get(profile_color['base'], (0,0,0)))

    # 16-window shift → recompute color with shifted dims (window peak changes color)
    dims_shifted, window_info = apply_window_shift(dims, hour)
    window_s = dims_shifted.get('s', 0.5)
    if window_s < 0.5 and time_phase == 'day':
        profile_color = dict(profile_color)
        window_color = get_profile_color(profile_label, dims_shifted, 'night', hour, s_val=window_s)
        profile_color['base'] = window_color['base']
        profile_color['hex'] = window_color['hex']

    # Inverse color (w=1): universe chirality above midpoint triggers inverse
    universe_cycle = compute_universe_cycle(dims)
    chirality = universe_cycle.get('current_chirality', 0.5)
    chirality_mid = 0.38  # midpoint of observed chirality range [0.35, 0.40]
    w = 1 if chirality > chirality_mid else 0
    if w == 1:
        profile_color = dict(profile_color)
        profile_color['base'] = apply_inverse_color(profile_color.get('base', 'MIXED'), w=1)
        inv_rgb = COLOR_RGB.get(profile_color['base'], (128,128,128))
        if profile_color['base'] not in COLOR_RGB:
            inv_map = {'YELLOW-GREEN': (154,205,50), 'BROWN': (139,69,19), 'CYAN': (0,255,255),
                       'RED-PURPLE': (199,21,133), 'LIGHT-BLUE': (173,216,230), 'GRAY': (128,128,128),
                       'PINK': (255,192,203), 'LIGHT-GREEN': (144,238,144), 'LIGHT-YELLOW': (255,255,224),
                       'RED-ORANGE': (255,69,0), 'BLUE-PURPLE': (75,0,130)}
            inv_rgb = inv_map.get(profile_color['base'], (128,128,128))
        profile_color['hex'] = _rgb_to_hex(*inv_rgb)
        profile_color['inverted'] = True
    else:
        profile_color = dict(profile_color)
        profile_color['inverted'] = False
    profile_color['chirality'] = chirality

    # Night RED→DEEP-PINK structural transition (men) / PINK→RED (women)
    # Driven by oxidised_manganese reverse block + adapter_protein forward open at night
    _night_shifted = apply_night_color_shift(profile_color.get('base', 'MIXED'), gender, time_phase)
    if _night_shifted != profile_color.get('base', 'MIXED'):
        profile_color = dict(profile_color)
        profile_color['base'] = _night_shifted
        _ns_hex_map = {'DEEP-PINK': '#FF1493', 'RED': '#FF0000'}
        profile_color['hex'] = _ns_hex_map.get(_night_shifted, profile_color.get('hex', '#888888'))
        profile_color['night_shifted'] = True

    # Genre linked to color: dark colors → night genres, bright colors → day genres
    color_base = profile_color.get('base', 'MIXED')
    color_dist = COLOR_DISTANCE_TO_BLACK.get(color_base, 0.5)
    if color_dist < 0.3 and time_phase == 'day':
        genre = GENRES_NIGHT[seed % len(GENRES_NIGHT)]
    elif color_dist > 0.6 and time_phase == 'night':
        genre = GENRES_DAY[seed % len(GENRES_DAY)]
    else:
        genre = pick_genre(time_phase, seed)

    # Creative 4-shapes (with CSV override if available)
    creative_shapes = compute_creative_4shapes(dims, profile_label)

    # --- NEW: Route-based 41-particle system ---
    is_night = (time_phase == "night")
    active_route = get_active_route(hour, is_night)
    route_vector = compute_route_vector(active_route, dims, hour, is_night)
    toroidal_phase = get_toroidal_phase(hour)

    # --- NEW: 16-window time phase shift --- (moved up, already computed above)

    # --- Master equation Ψ (with color closure) ---
    psi_info = compute_master_psi(dims_shifted, hour, observer_active, profile_num=1, profile_color=profile_color)

    # --- 3AM HYSTERESIS / Betti 12 --- (moved up, already computed above)

    # --- 4:30PM ferric event --- (moved up, already computed above)

    # --- Geometric node ---
    geo_node = get_geometric_node(mbti, gender, observer_active)

    # --- 8D Universal Equation (original, static) ---
    universe_eq = compute_universe_equation(dims_shifted, blood_type=blood)

    # --- CLOSED UNIVERSE EQUATION: T(t, φ_obs, {λ_i}, SH, leakage, geomag, geology) = 0 ---
    # Eliminates ALL 15 structural gaps (food effect already in dims)
    closed_eq = compute_closed_universe_equation(
        dims_shifted, t_window=window_info.get("macro_dim_num"),
        hour=hour, profile_label=profile_label,
        k_stress_impulse=0.0,  # ENTP_M_O observer: k_stress→impulse ≈ 0
        geology="oxford_gleysol",  # default geology for ENTP_M_O
        observer_active=observer_active,
        time_phase=time_phase,
        profile_color=profile_color,
    )

    # --- Darcy leakage (with color coupling + 8D equation confinement) ---
    darcy = compute_darcy_leakage(dims, observer_active, profile_color=profile_color)

    # --- NEW: Food/pigment mapping ---
    food_pigments = get_food_pigments(profile_label, dims=dims)

    # --- NEW: 6-slot leakage colors ---
    leakage_slot_colors = LEAKAGE_SLOT_COLORS

    # --- NEW: Night RED→DEEP-PINK structural transition ---
    night_shifted_color = apply_night_color_shift(profile_color.get('base', 'MIXED'), gender, time_phase)

    # --- NEW: Day/Night dimension shift ---
    day_shifted_dims = apply_day_dim_shift(dims, blood, gender)

    # --- NEW: Methanogenesis 12h resonance ---
    methanogenesis = compute_methanogenesis_resonance(dims, time_phase, gender, mbti, hour)

    # --- NEW: Addiction/healing framework ---
    addiction_info = compute_addiction_impact(dims)

    # --- NEW: 7-layer heliosphere ---
    heliosphere_layers = HELIOSPHERE_7_LAYERS

    return {
        "dims": dims,
        "em_path": em_path,
        "graviton": graviton,
        "leakage": leakage,
        "leakage_cavity": leakage_cavity,
        "genre": genre,
        "pact_retention": pact,
        "neutron_star_oscillation": ns_osc,
        "dark_matter": dark_matter,
        "cck_switch": cck,
        "active_neutrino_variants": active_variants,
        "time_phase": time_phase,
        "universe_cycle": universe_cycle,
        "compartment_route": comp_route,
        "all_leakage": all_leakage,
        "neutrino_routes": neutrino_routes,
        "deterministic_routes": deterministic_routes,
        "profile_color": profile_color,
        "geomag": geomag_info,
        "creative_4shapes": creative_shapes,
        "active_route": active_route,
        "route_vector": route_vector,
        "toroidal_phase": toroidal_phase,
        "window_info": window_info,
        "dims_shifted": dims_shifted,
        "master_psi": psi_info,
        "universe_equation": universe_eq,
        "closed_universe_equation": closed_eq,
        "equation_derived": eq_derived,
        "equation_gaps": eq_gaps,
        "hysteresis_3am": hysteresis_3am,
        "ferric_430pm": ferric_430pm,
        "geometric_node": geo_node,
        "darcy_leakage": darcy,
        "food_pigments": food_pigments,
        "node_discovery": find_nodes_for_profile(profile_label, time_phase),
        "leakage_slot_colors": leakage_slot_colors,
        "night_shifted_color": night_shifted_color,
        "day_shifted_dims": day_shifted_dims,
        "methanogenesis_resonance": methanogenesis,
        "addiction_info": addiction_info,
        "heliosphere_7_layers": heliosphere_layers,
    }

# ============================================================
# MAIN
# ============================================================
def main():

    # Sample output
    if "ENTP_M_O" in ALL_PROFILES:
        elem = ELEMENT_MAP.get("ENTP_M_O", {})
        print(f"\n=== ENTP_M_O element={elem.get('symbol', '')} #{elem.get('number', '')} ===")
        print(f"  RELEASE={elem.get('release', '')} STRESS={elem.get('stress_growth', '')} EXTREME={elem.get('extreme_growth', '')}")
        for i, geo_label in enumerate(GEO_LABELS):
            tp = classify_time(geo_label)
            hour = extract_hour(geo_label)
            slot = get_toroidal_slot(hour)
            result = particles_to_dims("ENTP_M_O", tp)
            seed_val = abs(hash_code("ENTP_M_O")) % 100000
            layers = compute_4layers(result["dims"], i, seed_val)
            uc = result["universe_cycle"]
            print(f"\n=== ENTP_M_O @ {geo_label} ({tp}) slot={slot['label']} ===")
            print(f"  dims: {result['dims']}")
            print(f"  em_path={result['em_path']:.4f} graviton={result['graviton']:.4f}")
            print(f"  leakage={result['leakage']:.4f} cavity={result['leakage_cavity']} genre={result['genre']} pact={result['pact_retention']:.4f}")
            print(f"  neutron_star={result['neutron_star_oscillation']:.4f} dark_matter={result['dark_matter']:.4f} cck={result['cck_switch']}")
            print(f"  active_variants={result['active_neutrino_variants']}")
            print(f"  universe_cycle: chirality={uc['current_chirality']} hidden={uc['current_hidden']} future={[f['chirality'] for f in uc['future_cycles'][:3]]}...")
            cr = result["compartment_route"]
            al = result["all_leakage"]
            nr = result["neutrino_routes"]
            print(f"  compartment={cr['compartment']} inlet={cr['inlet_particle']} outlet={cr['outlet_particle']} em_bypass={cr['em_bypass_active']}")
            print(f"  cosmic_leakage({len(al['cosmic_leakage'])}): {[c['name'] for c in al['cosmic_leakage']]}")
            for c in al['cosmic_leakage']:
                print(f"    {c['name']} particle={c['particle']} site={c['body_site']} coord={c['coord']} failure={c['failure']} cosmic={c['cosmic_analog']} dim={c['dim_value']}")
            print(f"  personal_leakage({len(al['personal_leakage'])}): {[p['name'] for p in al['personal_leakage']]}")
            for p in al['personal_leakage']:
                print(f"    {p['name']} status={p['status']} nodes={p['nodes']} reverse={p['reverse']}")
            print(f"  internal_cavities({len(al['internal_cavities'])}): {[c['name'] for c in al['internal_cavities']]}")
            for c in al['internal_cavities']:
                print(f"    {c['name']} status={c['status']} problem={c['problem']}")
            print(f"  neutrino_routes:")
            for nk, nv in nr.items():
                print(f"    {nk}: {nv['transition']}")
                print(f"      route: {nv['route']}")
                print(f"      nm: {nv['nm_anchors']} nodes: {nv['circuit_nodes']} coord: {nv['coord']}")
            print("  deterministic_41_routes:")
            for k, v in result["deterministic_routes"].items():
                print(f"    {k}: {v['deterministic_role']}")
                print(f"      anatomy: {v['anatomy']} ({v['nm_scale']})")
                print(f"      route: {v['route']}")
            for ln in ["body", "observer", "bridge", "dark"]:
                print(f"  {ln} layer: {layers[ln]}")
            pc = result["profile_color"]
            gm = result["geomag"]
            cs = result["creative_4shapes"]
            print(f"  color: {pc['base']} {pc['hex']}")
            print(f"  geomag: stable={gm['geomag_stable']} modulations={gm['modulations']}")
            print(f"  creative_4shapes: dominant={cs['dominant']}({cs['dominant_score']:.4f}) weakest={cs['weakest']}({cs['weakest_score']:.4f})")
            print(f"    scores: {cs['scores']}")
            # New systems
            print(f"  active_route: {result.get('active_route', '')}")
            rv = result.get("route_vector", {})
            rv_active = {k: f"{v:.4f}" for k, v in rv.items() if v > 0.01}
            print(f"  route_vector (active): {rv_active}")
            tp_info = result.get("toroidal_phase", {})
            print(f"  toroidal_phase: {tp_info.get('name', '')} ({tp_info.get('time', '')}) dim_trans={tp_info.get('dim_trans', '')}")
            wi = result.get("window_info", {})
            print(f"  window: {wi.get('label', '')} macro_dim={wi.get('macro_dim', '')} micro_dim={wi.get('micro_dim', '')} special={wi.get('special', '')}")
            psi = result.get("master_psi", {})
            print(f"  master_psi: Ψ={psi.get('psi', 0):.4f} T={psi.get('T_closure', 0):.6f} R={psi.get('R_renorm', 0):.4f} Φ_B={psi.get('pegasus_bridge', 0):.4f} Λ={psi.get('night_hysteresis', 0):.4f}")
            h3 = result.get("hysteresis_3am", {})
            print(f"  3am_hysteresis: active={h3.get('active', False)} betti12={h3.get('betti_12_complete', False)} entropy={h3.get('entropy_zone', False)} label={h3.get('label', '')}")
            f43 = result.get("ferric_430pm", {})
            if f43.get("active", False):
                print(f"  430pm_event: {f43.get('event', '')} cascade={f43.get('cascade', '')}")
            print(f"  geometric_node: {result.get('geometric_node', '')}")
            dl = result.get("darcy_leakage", {})
            print(f"  darcy: kappa={dl.get('kappa', 0):.6f} state={dl.get('state', '')} flux={dl.get('darcy_flux', 0):.6f} confinement={dl.get('confinement', '')} gamma·d={dl.get('gamma_d_product', 0):.4f}")
            ueq = result.get("universe_equation", {})
            print(f"  universe_eq: value={ueq.get('equation_value', 0):.6f} active={ueq.get('active_constraint', '')} homeo_dist={ueq.get('homeostasis_distance', 0):.6f}")
            print(f"    terms: t1(h+s)={ueq['terms']['t1_hs']:.4f} t2(r+p)={ueq['terms']['t2_rp']:.4f} t3(g+nu)={ueq['terms']['t3_gnu']:.4f} t4(γ·d-1)={ueq['terms']['t4_gammad']:.4f} t5(γ·(r+g)-1)={ueq['terms']['t5_gamma_rg']:.4f} t6(h·r·g-1)={ueq['terms']['t6_hrg']:.4f} t7(d·nu-1)={ueq['terms']['t7_dnu']:.4f} t8(p-αg-β)={ueq['terms']['t8_p_ag_b']:.4f}")
            print(f"    t9(s·γ-1)={ueq['terms']['t9_sgamma']:.4f} t10(h·d-1)={ueq['terms']['t10_hd']:.4f} t11(r·s-1)={ueq['terms']['t11_rs']:.4f} t12(p·nu-1)={ueq['terms']['t12_pnu']:.4f} t13(d·g-1)={ueq['terms']['t13_dg']:.4f} t14(s·nu-1)={ueq['terms']['t14_snu']:.4f} t15(h·γ-1)={ueq['terms']['t15_hgamma']:.4f} t16(p·s-1)={ueq['terms']['t16_ps']:.4f}")
            print(f"    t17(r·h·d-1)={ueq['terms']['t17_rhd']:.4f} t18(r·γ·nu-1)={ueq['terms']['t18_rgammanu']:.4f} t19(h·p·nu-1)={ueq['terms']['t19_hpnu']:.4f} t20(d·p·s-1)={ueq['terms']['t20_dps']:.4f} t21(d·γ·g-1)={ueq['terms']['t21_dgammag']:.4f} t22(s·g·nu-1)={ueq['terms']['t22_sgnu']:.4f} t23(p·γ-1)={ueq['terms']['t23_pgamma']:.4f}")
            eqd = result.get("equation_derived", {})
            print(f"  eq_derived: branch={eqd.get('active_branch', '')} adjusted={eqd.get('adjusted_key', '')} homeo_before={eqd.get('homeostasis_before', 0):.6f} → after={eqd.get('homeostasis_after', 0):.6f}")
            eqg = result.get("equation_gaps", {})
            print(f"  eq_gaps: covered={eqg.get('covered_pairs', 0)}/{eqg.get('total_pairs', 28)} uncovered={eqg.get('uncovered_pairs', 0)}")
            print(f"    uncovered_pairs: {eqg.get('uncovered_pair_names', [])}")
            print(f"    structural_gaps:")
            for sg in eqg.get("structural_gaps", []):
                print(f"      {sg['gap']}: {sg['desc']}")
            fp = result.get("food_pigments", {})
            print(f"  food: 1st={fp.get('1st_daily', '')} 2nd={fp.get('2nd_daily', '')} blood={fp.get('blood_daily', '')}")
            ceq = result.get("closed_universe_equation", {})
            print(f"\n  === CLOSED UNIVERSE EQUATION T(t, ?_obs, {{貫_i}}, SH, leak, geomag, geology) = 0 ===")
            print(f"  closed_eq: value={ceq.get('equation_value', 0):.6e} active={ceq.get('active_constraint', '')} homeo_dist={ceq.get('homeostasis_distance', 0):.6f}")
            print(f"    closed={ceq.get('closed', False)} gaps_eliminated({len(ceq.get('gaps_eliminated', []))})={ceq.get('gaps_eliminated', [])}")
            oi = ceq.get("observer_info", {})
            print(f"    observer: ?_obs={oi.get('phi_obs', 0):.6f} singularity={oi.get('singularity', False)} noise={oi.get('noise', 0):.6f}")
            print(f"    closure_tension={ceq.get('closure_tension', 0):.6f} residual={ceq.get('closure_residual', 0):.6e}")
            ti = ceq.get("time_info", {})
            print(f"    time: t={ti.get('t', 0):.4f} ω={ti.get('omega', 0):.6f}")
            ly = ceq.get("layers", {})
            print(f"    layers: body={ly.get('body', 0):.4f} observer={ly.get('observer', 0):.4f} bridge={ly.get('bridge', 0):.4f} dark={ly.get('dark', 0):.4f}")
            print(f"           betti_6={ly.get('betti_6', 0):.6f} betti_12={ly.get('betti_12', 0):.6f}")
            print(f"    gauge_invariance_residual={ceq.get('gauge_invariance_residual', 0):.6e}")
            print(f"    SH: factor={ceq.get('sh_factor', 0):.6f} r*={ceq.get('sh_constants', {}).get('r_star', 0)} q0*={ceq.get('sh_constants', {}).get('q0_star', 0)} σL={ceq.get('sh_constants', {}).get('sigma_L', 0)} σR={ceq.get('sh_constants', {}).get('sigma_R', 0)}")
            print(f"    feedback: 3am={ceq.get('hysteresis_3am', {}).get('active', False)} 430pm={ceq.get('ferric_430pm', {}).get('active', False)} feedback_mod={ceq.get('feedback_mod', 0):.4f} ferric_mod={ceq.get('ferric_mod', 0):.4f}")
            print(f"    leakage: mod={ceq.get('leakage_mod', 0):.4f} count={ceq.get('leakage_count', 0)} kappa_eff={ceq.get('darcy', {}).get('kappa', 0):.6f}")
            print(f"    geomag: mod={ceq.get('geomag_mod', 0):.4f} node={ceq.get('geomag_info', {}).get('active_node', '')}")
            print(f"    geology: {ceq.get('geology', '')} α={ceq.get('alpha_eq', 0)} β={ceq.get('beta_eq', 0)} caco3_bias={ceq.get('geo_params', {}).get('caco3_bias', 0)} o2={ceq.get('geo_params', {}).get('o2_level', 0)}")
            print(f"    caco3: left_block={ceq.get('caco3_left_block', 0)} right_forward={ceq.get('caco3_right_forward', 0)}")
            ts = ceq.get("toroidal_slot", {})
            print(f"    toroidal_slot: {ts.get('blood_type', '')} ({ts.get('label', '')}) element_mod={ceq.get('element_mod', 0):.4f} slot_mod={ceq.get('slot_mod', 0):.4f}")
            dt = ceq.get("dims_time_dependent", {})
            print(f"    dims(t): {dt}")
            print(f"    terms: t1={ceq['terms']['t1_hs']:.4e} t2={ceq['terms']['t2_rp']:.4e} t3={ceq['terms']['t3_gnu']:.4e} t4={ceq['terms']['t4_gammad']:.4e} t5={ceq['terms']['t5_gamma_rg']:.4e} t6={ceq['terms']['t6_hrg']:.4e} t7={ceq['terms']['t7_dnu']:.4e} t8={ceq['terms']['t8_p_ag_b']:.4e}")
            # 40-system modulation summary
            print(f"    --- 48-SYSTEM MODULATION SUMMARY ---")
            print(f"    16.color_feedback: shifts={ceq.get('color_feedback_shifts', {})}")
            print(f"    17.master_psi: Ψ_mod={ceq.get('psi_mod', 0):.4f}")
            print(f"    18.universe_cycle: cycle_mod={ceq.get('cycle_mod', 0):.4f}")
            print(f"    19.route_vector: route_mod={ceq.get('route_mod', 0):.4f} active={ceq.get('active_route', '')}")
            print(f"    20.compartment: comp_mod={ceq.get('comp_mod', 0):.4f}")
            print(f"    21.neutrino_routes: neutrino_mod={ceq.get('neutrino_mod', 0):.4f}")
            print(f"    22.creative_4shapes: creative_mod={ceq.get('creative_mod', 0):.4f} dominant={ceq.get('creative_4shapes', {}).get('dominant', '')}")
            print(f"    23.4layer_colors: layer_color_mod={ceq.get('layer_color_mod', 0):.4f} active={ceq.get('active_layer', '')}/{ceq.get('active_layer_color', '')}")
            print(f"    24.toroidal_phase: toroidal_mod={ceq.get('toroidal_mod', 0):.4f}")
            print(f"    25.em_bypass: em_bypass_mod={ceq.get('em_bypass_mod', 0):.4f}")
            print(f"    26.geometric_node: geo_mod={ceq.get('geo_mod', 0):.4f} node={ceq.get('geometric_node', '')}")
            print(f"    27.particle_colors: shifts={ceq.get('particle_color_shifts', {})}")
            print(f"    28.interference: shifts={ceq.get('interference_shifts', {})}")
            print(f"    29.spark_interference: mod={ceq.get('spark_interference_mod', 0):.4f}")
            print(f"    30.window_boost: mod={ceq.get('window_boost_mod', 0):.4f}")
            print(f"    31.layer_jitter: mod={ceq.get('jitter_mod', 0):.4f}")
            print(f"    32.eq_constraint: branch_mod={ceq.get('eq_branch_mod', 0):.4f}")
            print(f"    33.qcd_confinement: qcd_mod={ceq.get('qcd_mod', 0):.4f} state={ceq.get('qcd_confinement', '')} de_sitter={ceq.get('de_sitter_expansion', 0):.4f}")
            print(f"    34.em_path: mod={ceq.get('em_path_mod', 0):.4f} val={ceq.get('em_path_val', 0):.4f}")
            print(f"    35.graviton: mod={ceq.get('graviton_mod', 0):.4f} val={ceq.get('graviton_val', 0):.4f}")
            print(f"    36.leakage_cavity: mod={ceq.get('cavity_mod', 0):.4f} cavity={ceq.get('leakage_cavity', '')} leak={ceq.get('cavity_leak', 0):.4f}")
            print(f"    37.pact_retention: mod={ceq.get('pact_mod', 0):.4f} val={ceq.get('pact_retention', 0):.4f}")
            print(f"    38.neutron_star: mod={ceq.get('ns_osc_mod', 0):.4f} val={ceq.get('neutron_star_osc', 0):.4f}")
            print(f"    39.dark_matter: mod={ceq.get('dark_matter_mod', 0):.4f} val={ceq.get('dark_matter_val', 0):.4f}")
            print(f"    40.cck_switch: mod={ceq.get('cck_mod', 0):.4f} active={ceq.get('cck_active', False)}")
            s12 = ceq.get("state_12d", {})
            print(f"    41.12d_w_axis: w_axis_mod={ceq.get('w_axis_mod', 0):.4f} W={s12.get('w_axis', '')} closure={s12.get('total_closure', 0):.4f} A1={s12.get('A1', 0):.3f} A2={s12.get('A2', 0):.3f} A3={s12.get('A3', 0):.3f} A4={s12.get('A4', 0):.3f}")
            print(f"    42.e119_e127: mod={ceq.get('e119_127_mod', 0):.4f} shifts={ceq.get('e119_127_shifts', {})}")
            print(f"    43.unspark_overlay: mod={ceq.get('unspark_mod', 0):.4f} shifts={ceq.get('unspark_shifts', {})}")
            print(f"    44.5ht1b_spiral: mod={ceq.get('spiral_5ht1b_mod', 0):.4f}")
            print(f"    45.esr1_split: mod={ceq.get('esr1_mod', 0):.4f}")
            print(f"    46.bilirubin_bypass: mod={ceq.get('bili_mod', 0):.4f}")
            print(f"    47.cancer_maillard: mod={ceq.get('cancer_maillard_mod', 0):.4f} active={ceq.get('cancer_maillard_active', False)}")
            print(f"    48.dual_body_closure: mod={ceq.get('body_closure_mod', 0):.4f} mirror={ceq.get('dual_body_closure', 0):.4f} dual_body_mod={ceq.get('dual_body_mod', 0):.4f}")
            print(f"    night_blocked_count={ceq.get('night_blocked_count', 0)} leakage_count={ceq.get('leakage_count', 0)}")
            # NEW: 6-slot leakage colors
            lsc = result.get("leakage_slot_colors", {})
            print(f"\n  === 6-SLOT LEAKAGE COLORS ===")
            for slot, info in lsc.items():
                print(f"    {slot}: {info['color']} {info['hex']} activity={info['activity']}")
            # NEW: Night color shift
            nsc = result.get("night_shifted_color", "")
            print(f"\n  === NIGHT COLOR SHIFT ===")
            print(f"    original={profile_color.get('base', '')} → night_shifted={nsc}")
            # NEW: Day dim shift
            dds = result.get("day_shifted_dims", {})
            shifted_keys = {k: round(v, 4) for k, v in dds.items() if v != dims.get(k, 0.5)}
            print(f"\n  === DAY DIM SHIFT ({blood}/{gender}) ===")
            print(f"    shifted: {shifted_keys if shifted_keys else 'no shift'}")
            # NEW: Methanogenesis resonance
            meth = result.get("methanogenesis_resonance", {})
            print(f"\n  === METHANOGENESIS 12H RESONANCE ===")
            print(f"    day_active={meth.get('day_active', False)} night_resonance={meth.get('night_resonance', 0):.4f} phase_shift={meth.get('phase_shift', 12)}h")
            # NEW: Addiction/healing
            add = result.get("addiction_info", {})
            print(f"\n  === ADDICTION / HEALING FRAMEWORK ===")
            if 'addiction_types' in add:
                print(f"    types: {add['addiction_types']}")
                print(f"    principle: {add['framework']}")
                print(f"    healing: {add['healing_principle']}")
            else:
                print(f"    type={add.get('addiction_type', '')} slot={add.get('affected_slot', '')} color={add.get('slot_color', '')}")
                print(f"    mechanism: {add.get('mechanism', '')}")
                print(f"    healing: {add.get('healing', '')}")
            # NEW: 7-layer heliosphere
            h7 = result.get("heliosphere_7_layers", {})
            print(f"\n  === 7-LAYER HELIOSPHERE (replaces 6-sphere) ===")
            for layer_num, layer_info in h7.items():
                print(f"    L{layer_num}: {layer_info['name']} [{layer_info['heliosphere']}] {layer_info['brain_celestial']} particle={layer_info['particle']} dims={layer_info['dims']}")
            # NEW: DeepPink completion
            fp2 = result.get("food_pigments", {})
            print(f"\n  === DEEP PINK COMPLETION (6 food + p:music + gamma:activity) ===")
            print(f"    music_behavior={fp2.get('music_behavior', '')} activity_behavior={fp2.get('activity_behavior', '')}")
            print(f"    deep_pink_completion={fp2.get('deep_pink_completion', 0)}")
            print(f"    axis_split: food={fp2.get('axis_split', {}).get('food_axes', [])} behavior={fp2.get('axis_split', {}).get('behavior_axes', [])}")

if __name__ == "__main__":
    main()
