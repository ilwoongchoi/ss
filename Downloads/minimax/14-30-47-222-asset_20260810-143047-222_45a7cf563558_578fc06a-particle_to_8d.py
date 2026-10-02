#!/usr/bin/env python3
"""
particle_to_8d.py — 14-particle to 8D personality dimension mapper
Synced with particle_to_8d.js

14 particles: 12 base + 2 derived (EM path replaces axion, graviton)
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
"""

import math
import sys

# ============================================================
# GEOMETRY CONSTANTS (from geometry_package/absolute_constants.py)
# ============================================================
PHI = (1 + math.sqrt(5)) / 2
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
DELTA_T_OBS_DERIVED = 0.8418
OMEGA_KAPPA = 1.0 / 28.0

DIM_ORDER = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]

PARTICLE_ORDER = [
    "proton", "photon", "electron", "neutrino",
    "muon", "tau", "gluon", "w_boson",
    "z_boson", "higgs", "axion", "quark",
]

# 14 particles: 12 base + 2 derived (em_path, graviton)
PARTICLE_ORDER_14 = PARTICLE_ORDER + ["em_path", "graviton"]

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
    [40,"Zr","INFJ_F_B","hauntology","deconstructed club","Boards of Canada"],
    [41,"Nb","INTP_F_O","DRONE","CINEMATIC","PIANO"],
    [42,"Mo","ISTJ_F_AB","DRONE","orchestral","minimalistic"],
    [43,"Tc","INTP_F_AB","neo-classical","strings","DRONE"],
    [44,"Ru","INFP_M_B","hauntology","power electronics","shoegaze"],
    [45,"Rh","ISFJ_M_AB","AMBIENT","INDIE FOLK","folk"],
    [46,"Pd","INTJ_F_O","dark ambient","deconstructed club","DRONE"],
    [47,"Ag","ESFP_M_A","dream pop","dark ambient","deconstructed club"],
    [48,"Cd","ESFP_F_B","deconstructed club","noise","IDM"],
    [49,"In","ESFP_F_O","hyperpop","DRONE","dream pop"],
    [50,"Sn","ENFJ_M_AB","strings","Boards of Canada","CINEMATIC"],
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
    [86,"Rn","ENTP_M_A","IDM","DRONE","electronic experimental"],
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
DIM_PEAK_SHIFT = {i: DIM_ORDER[i % 8] for i in range(16)}

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
# 7-SPHERE PHASES — 6-sphere + heliosphere (7th container)
# Model ends at solar system edge — no 8th beyond the Oort Cloud
# ============================================================
SEVEN_SPHERE_PHASES = {
    "proton":     {"phase": 1, "flow": "Sun→Earth",       "meaning": "정보 점화 = 빅뱅 = H→O 스파크"},
    "photon":     {"phase": 2, "flow": "Earth→Moon",      "meaning": "수리 축적 = O2 광합성 = 빛→시간"},
    "z_boson":    {"phase": 3, "flow": "Moon→CoMag",      "meaning": "시간→결합 전환 = 약력 붕괴"},
    "w_boson":    {"phase": 4, "flow": "CoMag→Barnard",   "meaning": "결합→질량 압축 = 약력 붕괴"},
    "gluon":      {"phase": 4, "flow": "CoMag→Barnard",   "meaning": "결합 에너지 = 강력 = 결합 밀도"},
    "quark":      {"phase": 5, "flow": "Barnard→Heliosphere", "meaning": "질량→정보 충전 = heliosphere cavity 충전"},
    "higgs":      {"phase": 5, "flow": "Barnard→Heliosphere", "meaning": "질량 부여 = heliosphere cavity 안으로"},
}

# Heliosphere: 7th container — bubble-like cavity / cosmic airbag
# Solar system ends here. Oort Cloud is the outer marker, not a separate layer.
HELIOSPHERE = {
    "phase": 7,
    "role": "7번째 container = heliosphere cavity / cosmic airbag / protective shield",
    "boundary_inner": {
        "name": "termination_shock",
        "distance_au": 75,  # ~75-90 AU from Sun
        "role": "supersonic solar wind → subsonic 감속; 1차 impedance discontinuity",
        "body_map": "inner_impedance_point"
    },
    "boundary_outer": {
        "name": "heliopause",
        "distance_au": 123,  # ~123 AU average
        "role": "solar wind pressure = interstellar pressure; outer wall; 2차 impedance boundary; cavity/airbag outer membrane",
        "body_map": "outer_impedance_point"
    },
    "oort_cloud": {
        "name": "Oort Cloud",
        "distance_au": 2500,  # ~2,500-100,000 AU — gravitational edge, "true edge of solar system"
        "role": "transition marker; gravitational envelope; model ends here — solar system boundary",
        "note": "not a container, not a cavity — reservoir / outer horizon"
    },
    "particle_anchor": "axion",
    "impedance_type": "pressure_balance",
    "leakage_cavity_count": 7  # axion, EM, GABA-C, mitochondria, bilirubin, electron_hole, pancreas
}

# ============================================================
# 7 LEAKAGE SLOTS — impedance cavity/airbag formation at heliosphere boundaries
# Each leakage path = 1 impedance point = 1 cavity in the body
# ============================================================
LEAKAGE_SLOTS_7 = {
    1: {
        "name": "axion_leakage",
        "anatomy": "Skull Vertex / CSF Sagittal gap",
        "particle": "axion",
        "route": "138.88° CSF spark → outward EM radiation (3rd direction)",
        "impedance_partner": "em_leakage",
        "boundary": "termination_shock",
        "role": "Rootless 3rd direction radiator; initiates all other leakage paths"
    },
    2: {
        "name": "em_leakage",
        "anatomy": "Bypass route 131→129 (Right STG → Right V1)",
        "particle": "em_path",
        "route": "EM recapturing → observer closure retrograde",
        "impedance_partner": "axion_leakage",
        "boundary": "heliopause",
        "role": "Observer closure EM loop; EM field leaks at heliopause"
    },
    3: {
        "name": "gaba_c_leakage",
        "anatomy": "GABA-C (GABRR1/RR2 rho subunits) — retina, brainstem",
        "particle": "gluon",
        "route": "GABA-C mediated inhibition → color confinement → skin sealing",
        "impedance_partner": "mitochondria_leakage",
        "boundary": "termination_shock",
        "role": "GABA-A/B combined; slow chloride channel; seals heliosphere interior"
    },
    4: {
        "name": "mitochondria_leakage",
        "anatomy": "ATP synthase / Adrenal Medulla / w_boson",
        "particle": "w_boson",
        "route": "ATP hydrolysis → beta decay collapse → adrenaline surge",
        "impedance_partner": "gaba_c_leakage",
        "boundary": "heliopause",
        "role": "Weak force leakage; metabolic energy → cosmic energy conversion at boundary"
    },
    5: {
        "name": "bilirubin_leakage",
        "anatomy": "Heme oxygenase (HO-1) / heme breakdown → bilirubin",
        "particle": "higgs",
        "route": "Heme → biliverdin → bilirubin → dark matter noise accumulation",
        "impedance_partner": "electron_hole_leakage",
        "boundary": "heliopause",
        "role": "Higgs repair attractor; bilirubin's antioxidant role = heliosphere shield function"
    },
    6: {
        "name": "electron_hole_death_sensor_darkness_stress_patch_leakage",
        "anatomy": "Chlorine ion pump / heme.out1 (HO-1 ETC path) / tau",
        "particle": "tau",
        "route": "Z-boson decay → rectal anchor → thalamic pain signal",
        "impedance_partner": "bilirubin_leakage",
        "boundary": "termination_shock",
        "role": "Death sensor / darkness stress patch; electron hole = charge vacancy at boundary"
    },
    7: {
        "name": "pancreas_leakage",
        "anatomy": "ATP / CCK switch (Pancreas / Gut)",
        "particle": "energy",
        "route": "ATP fueling → W-boson collapse fuel → CCK satiety gate",
        "impedance_partner": "axion_leakage (closure)",
        "boundary": "heliopause",
        "role": "Closes the 7-slot loop; ATP thermodynamic fuel = heliosphere energy source"
    },
}

# ============================================================
# HELIOSPHERE → BODY IMPEDANCE POINT MAPPING
# Cosmic heliosphere structures map to specific body loci
# ============================================================
HELIOSPHERE_BODY_MAP = {
    "termination_shock": {
        "anatomy": "CSF- blood-brain barrier / dural venous sinus / arachnoid granulation",
        "impedance_type": "velocity discontinuity (supersonic → subsonic solar wind)",
        "particle_signature": "axion",
        "body_role": "inner impedance point; 1st cavity wall; axion spark initiates here"
    },
    "heliopause": {
        "anatomy": "Skull vertex / CSF sagittal sinus / pineal gland region",
        "impedance_type": "pressure balance (solar wind = interstellar medium)",
        "particle_signature": "em_path",
        "body_role": "outer impedance point; 2nd cavity wall; EM leakage / observer closure site"
    },
    "impedance_cavities": {
        "anatomy": "Subarachnoid space / perivascular space (Virchow-Robin spaces)",
        "impedance_type": "7 leakage slot intersection points",
        "count": 7,
        "cavities": [
            "axion_cavity",   # Slot 1
            "em_cavity",      # Slot 2
            "gaba_c_cavity",  # Slot 3
            "mito_cavity",     # Slot 4
            "bilirubin_cavity",# Slot 5
            "electron_hole_cavity", # Slot 6
            "pancreas_cavity"  # Slot 7
        ],
        "body_role": "Impedance point intersections form invisible cavities in the body; these are the 'personal leakage cavities' felt as pressure points, fatigue, or dark sensations"
    }
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
    "proton":    {"r": 1},
    "photon":    {"s": 1},
    "electron":  {"d": 1},
    "neutrino":  {"nu": 1},
    "muon":      {"h": 1},
    "tau":       {"g": 1},
    "gluon":     {"g": 1},
    "w_boson":   {"p": 1},
    "z_boson":   {"gamma": 1},
    "higgs":     {"d": 1},
    "axion":     {"nu": 1},
    "quark":     {"r": 1},
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
        "skin_sweat":        {"particle": "axion",    "coord": None,               "mechanism": "water_evaporation_CP_leak"},
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
    {"name":"gluon","particle":"gluon","body_site":"philtrum","coord":(0,+46,+7),"failure":"color_confinement_fails","cosmic_analog":"failed_confinement","dim_trigger":"g"},
    {"name":"muon","particle":"muon","body_site":"left_temporalis","coord":(+7,+25,+3),"failure":"higgs_gate_opens","cosmic_analog":"cosmic_ray_shower","dim_trigger":"h"},
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
# DETERMINISTIC 34-COMPONENT TRANSITION ROUTES
# ============================================================
DETERMINISTIC_34_COMPONENTS = {
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
    "axion": {
        "anatomy": "Skull Vertex / CSF Space",
        "nm_scale": "5-5000nm Sagittal gap",
        "route": "138.88° CSF spark -> Outward EM radiation (3rd direction)",
        "deterministic_role": "Rootless 3rd direction radiator"
    },
    "em_path": {
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
    "progesterone": {
        "anatomy": "Right Eye (Levator superioris) / R. MPOA",
        "nm_scale": "50um fascia",
        "route": "3D volume expansion -> Depth perception igniter",
        "deterministic_role": "3D spatial expansion vector"
    },
    "testosterone": {
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
     "forward":"left_sulfur_Mn_internal_return","reverse":"left_foot_leakage=left_foot_coldness"},
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
            if dims["g"] < 0.3 or dims["nu"] < 0.3:
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

    # Clamp
    for d in DIM_ORDER:
        dims[d] = clamp(dims[d])

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

    # Genre
    seed = hash_code(profile_label + time_phase)
    genre = pick_genre(time_phase, seed)

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

    # Universe cycle
    universe_cycle = compute_universe_cycle(dims)

    # Compartment route
    comp_route = compute_compartment_route(mbti, gender, dims, time_phase)

    # All leakage
    all_leakage = compute_all_leakage(dims, time_phase)

    # Neutrino routes
    neutrino_routes = get_neutrino_routes(time_phase)

    # Deterministic 34 components
    deterministic_routes = DETERMINISTIC_34_COMPONENTS

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
        "deterministic_routes": deterministic_routes
    }

# ============================================================
# MAIN
# ============================================================
def main():
    output_lines = []

    header = ["profile", "element_num", "element_sym", "release_genre", "stress_growth_genre", "extreme_growth_genre"]
    for g in GEO_LABELS:
        for d in DIM_ORDER:
            header.append(f"{g}_{d}")
        header.extend([
            f"{g}_em_path", f"{g}_graviton", f"{g}_leakage", f"{g}_leakage_cavity",
            f"{g}_genre", f"{g}_pact", f"{g}_neutron_star", f"{g}_dark_matter", f"{g}_cck",
            f"{g}_toroidal_slot", f"{g}_universe_chirality", f"{g}_universe_hidden",
            f"{g}_compartment", f"{g}_comp_inlet", f"{g}_comp_outlet", f"{g}_em_bypass",
            f"{g}_cosmic_leak_count", f"{g}_cosmic_leak_names",
            f"{g}_personal_leak_count", f"{g}_personal_leak_names",
            f"{g}_internal_cavity_count", f"{g}_internal_cavity_names",
            f"{g}_neutrino_route_1", f"{g}_neutrino_route_2", f"{g}_neutrino_route_3",
        ])
        for k in DETERMINISTIC_34_COMPONENTS.keys():
            header.append(f"{g}_det_{k}")
        for layer in LAYER_NAMES:
            for d in DIM_ORDER:
                header.append(f"{g}_{layer}_{d}")
    output_lines.append(",".join(header))

    for profile in sorted(ALL_PROFILES.keys()):
        elem = ELEMENT_MAP.get(profile, {})
        row_parts = [
            profile,
            str(elem.get("number", "")),
            elem.get("symbol", ""),
            elem.get("release", ""),
            elem.get("stress_growth", ""),
            elem.get("extreme_growth", ""),
        ]
        for i, geo_label in enumerate(GEO_LABELS):
            tp = classify_time(geo_label)
            hour = extract_hour(geo_label)
            slot = get_toroidal_slot(hour)
            result = particles_to_dims(profile, tp)
            seed_val = abs(hash_code(profile)) % 100000
            layers = compute_4layers(result["dims"], i, seed_val)
            uc = result["universe_cycle"]

            for d in DIM_ORDER:
                row_parts.append(f"{result['dims'][d]:.4f}")
            row_parts.append(f"{result['em_path']:.4f}")
            row_parts.append(f"{result['graviton']:.4f}")
            row_parts.append(f"{result['leakage']:.4f}")
            row_parts.append(result["leakage_cavity"])
            row_parts.append(result["genre"])
            row_parts.append(f"{result['pact_retention']:.4f}")
            row_parts.append(f"{result['neutron_star_oscillation']:.4f}")
            row_parts.append(f"{result['dark_matter']:.4f}")
            row_parts.append(str(result["cck_switch"]))
            row_parts.append(slot["label"])
            row_parts.append(f"{uc['current_chirality']:.6f}")
            row_parts.append(f"{uc['current_hidden']:.6f}")
            cr = result["compartment_route"]
            al = result["all_leakage"]
            nr = result["neutrino_routes"]
            row_parts.append(str(cr["compartment"]))
            row_parts.append(cr["inlet_particle"])
            row_parts.append(cr["outlet_particle"])
            row_parts.append(str(cr["em_bypass_active"]))
            row_parts.append(str(len(al["cosmic_leakage"])))
            row_parts.append(";".join([c["name"] for c in al["cosmic_leakage"]]))
            row_parts.append(str(len(al["personal_leakage"])))
            row_parts.append(";".join([p["name"] for p in al["personal_leakage"]]))
            row_parts.append(str(len(al["internal_cavities"])))
            row_parts.append(";".join([c["name"] for c in al["internal_cavities"]]))
            nr_keys = list(nr.keys())
            for j in range(3):
                if j < len(nr_keys):
                    row_parts.append(f"{nr_keys[j]}:{nr[nr_keys[j]]['transition'][:40]}")
                else:
                    row_parts.append("")

            dr = result["deterministic_routes"]
            for k in DETERMINISTIC_34_COMPONENTS.keys():
                row_parts.append(dr[k]["route"])

            for ln in LAYER_NAMES:
                for d in DIM_ORDER:
                    row_parts.append(f"{layers[ln][d]:.4f}")
        output_lines.append(",".join(row_parts))

    csv_output = "\n".join(output_lines)
    with open("particle_to_8d_output.csv", "w", encoding="utf-8") as f:
        f.write(csv_output)
    print(csv_output)

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
            print("  deterministic_34_routes:")
            for k, v in result["deterministic_routes"].items():
                print(f"    {k}: {v['deterministic_role']}")
                print(f"      anatomy: {v['anatomy']} ({v['nm_scale']})")
                print(f"      route: {v['route']}")
            for ln in ["body", "observer", "bridge", "dark"]:
                print(f"  {ln} layer: {layers[ln]}")

if __name__ == "__main__":
    main()
