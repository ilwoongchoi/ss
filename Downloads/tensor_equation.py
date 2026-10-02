#!/usr/bin/env python3
"""
TENSOR EQUATION T[m,b,g,l,t] → 36 PARTICLE FIELD VALUES AT 0.01 RESOLUTION

From prose_new/05_energy_master.md and 04_attractors_5structure.md:

V_k = impedance(m) × energy_weight(b) × flow(g) × peak_dim(t mod 16) × layer_transform(l) × Obs(t)

The 36 particles = 11 SM particles + Electromagnetism + 24 extended particles:
  proton, gluon, muon, electron, quark, higgs, w_boson, z_boson,
  neutrino, tau, photon, em,
  up_quark, down_quark, charm_quark, strange_quark, top_quark, bottom_quark,
  tau_neutrino, electron_antineutrino, muon_neutrino, muon_antineutrino, tau_antineutrino,
  neutron, neutron_star, dark_matter, dark_energy, female_gaba, energy,
  clathrate_buffer, malate_dehydrogenase, ego_d2, progesterone, testosterone,
  acetyl_coa, graviton, axion

Each particle maps to an 8D dimension and a circuit node cluster.
The tensor outputs a field value in [0.00, 1.00] for each particle at any time t.

8D dimensions: r, h, d, p, s, gamma, g, nu
Peak dimension per window: [r,h,d,p,s,gamma,g,nu,STOP,—,—,—,—,—,—,—]
"""

import math
import random

# ============================================================
# 1. INPUT SPACE
# ============================================================
# m = MBTI index (0-15): ENFP=0, ISFP=1, ESFJ=2, INTP=3, ENTP=4, INFJ=5, ESTP=6, ISTP=7,
#                         ENFJ=8, INTJ=9, ESFP=10, ISTJ=11, ESTJ=12, INFP=13, ISFJ=14, ENTJ=15
# b = blood type (0-3): O=0, A=1, B=2, AB=3
# g = gender (0-1): M=0, F=1
# l = layer (0-3): A=0, B=1, C=2, D=3
# t = time in hours (0.0-24.0), resolution 0.01

# ============================================================
# Φ–MATRIX / PHASE COUPLING DEFINITIONS
# ============================================================
# Each 8D dimension has an intrinsic phase frequency (rad / hour).
# These are placeholders tied to 1.5 h window structure; should be updated once empirical EEG / LFP data are available.
# No direct empirical constants found in 영점.md for these frequencies.
PHASE_FREQ = {
    'r': 2 * math.pi / 1.5,     # matches 1.5 h window – rhythm clock
    'h': 2 * math.pi / 3.0,
    'd': 2 * math.pi / 4.5,
    'p': 2 * math.pi / 6.0,
    's': 2 * math.pi / 24.0,
    'gamma': 2 * math.pi / 12.0,
    'g': 2 * math.pi / 9.0,
    'nu': 2 * math.pi / 18.0,
}

# κ antisymmetric coupling coefficients κ_ij = –κ_ji  (units: scalar)
# Use C² = 0.08 from 영점.md (Yukawa quantum = minimum delta unit)
_C2 = 0.08
KAPPA = {}
_dims = ['r','h','d','p','s','gamma','g','nu']
for i, a in enumerate(_dims):
    for b in _dims[i+1:]:
        if (a, b) in [('r','nu'), ('g','gamma'), ('s','d')]:
            val = _C2  # strong inverse reciprocal
        else:
            val = _C2 * 0.5  # weaker generic coupling
        KAPPA[(a,b)] = val
        KAPPA[(b,a)] = -val

def _theta(dim: str, t: float) -> float:
    """Phase angle θ_i(t) in radians for dimension 'dim' at time t (hours)."""
    return PHASE_FREQ[dim] * t

def apply_phase_coupling(vec: dict, t: float) -> dict:
    """Apply Φ-matrix sin(Δϕ) modulation: Δϕ_ij = θ_i - θ_j.
    Returns NEW vec with coupling injected (does not mutate original)."""
    new_vec = dict(vec)
    for i in vec:
        delta = 0.0
        for j in vec:
            if i == j:
                continue
            k = KAPPA.get((i, j), 0.0)
            if k == 0:
                continue
            dphi = _theta(i, t) - _theta(j, t)
            delta += k * math.sin(dphi)
        # add but clamp 0–1
        new_vec[i] = max(0.0, min(1.0, new_vec[i] + delta))
    return new_vec

def universe_ended(vec: dict, t: float, axion_val: float = 0.0, co2_leak: float = 0.0, redox_delta: float = 0.0) -> dict:
    """
    Check if universe has reached steady-state (all antagonisms zero).
    Returns dict with boolean 'ended' and component-wise status.
    """
    eps = 1e-6
    status = {'ended': True, 'components': {}}
    
    # 1. Phase coupling antagonisms: κ·sin Δϕ must be ~0 for all pairs
    total_phase_antagonism = 0.0
    for i in vec:
        for j in vec:
            if i == j:
                continue
            k = KAPPA.get((i, j), 0.0)
            if k == 0:
                continue
            dphi = _theta(i, t) - _theta(j, t)
            term = k * math.sin(dphi)
            total_phase_antagonism += abs(term)
    status['components']['phase_antagonism'] = total_phase_antagonism < eps
    if total_phase_antagonism >= eps:
        status['ended'] = False
    
    # 2. Axion crushing: ψ·axion must equal gamma (crush complete)
    psi = 0.6
    crush = psi * axion_val
    # If gamma in vec, check crush balance
    if 'gamma' in vec:
        gamma_val = vec['gamma']
        status['components']['axion_crush'] = abs(gamma_val - crush) < eps
        if abs(gamma_val - crush) >= eps:
            status['ended'] = False
    else:
        status['components']['axion_crush'] = True  # not applicable
    
    # 3. CO₂ leakage: must be fully buffered by clathrate
    status['components']['co2_leak'] = co2_leak < eps
    if co2_leak >= eps:
        status['ended'] = False
    
    # 4. Redox ΔE: malate_dehydrogenase g↔d balance
    status['components']['redox_balance'] = redox_delta < eps
    if redox_delta >= eps:
        status['ended'] = False
    
    # 5. p stability: p must not be in 3AM random zone (21:00-03:00)
    # During random zone, p is set to random.random() — universe cannot end
    h = t % 24.0
    in_random_zone = (h >= 21.0 or h < 3.0)
    if in_random_zone and 'p' in vec:
        # p is randomized — cannot converge
        status['components']['p_stability'] = False
        status['ended'] = False
    else:
        status['components']['p_stability'] = True
    
    # 6. p convergence: p must be near 0 or 1 (bistable attractor)
    if 'p' in vec and not in_random_zone:
        p_val = vec['p']
        p_converged = (p_val < eps) or (abs(1.0 - p_val) < eps)
        status['components']['p_convergence'] = p_converged
        if not p_converged:
            status['ended'] = False
    else:
        status['components']['p_convergence'] = True
    
    return status

# ============================================================
# 2. COMPONENT FUNCTIONS
# ============================================================

# 2a. Window index from time
def window(t):
    return int((t % 24.0) / 1.5)  # W0-W15

# 2b. Peak 8D dimension per window
PEAK_DIMS = ['r','h','d','p','s','gamma','g','nu',
             'r','h','d','p','s','gamma','g','nu']  # W0-W15 (W8-W15 = auxiliary repeat)

def peak_dim(t):
    w = window(t)
    if w >= 8:
        return PEAK_DIMS[w]  # auxiliary = same dim but discharging
    return PEAK_DIMS[w]

# 2c. Peak value — cosine modulated within each 1.5h window
def peak_value(t):
    w = window(t)
    phase = ((t % 1.5) / 1.5) * 2 * math.pi  # 0 to 2π within window
    if w < 8:
        # Building phase: cosine rises from 0.5 to 1.0 to 0.5
        return 0.5 + 0.5 * (0.5 + 0.5 * math.cos(phase - math.pi))
    else:
        # Discharging phase: cosine falls from 1.0 to 0.5 to 0.0
        return 0.5 + 0.5 * (0.5 - 0.5 * math.cos(phase))

# 2d. Impedance per MBTI (cognitive function → 8D weight vector)
# Each MBTI has a dominant 8D dimension with value 1.0, secondary at 0.6, tertiary at 0.3
MBTI_8D = {
    # (dom_dim, dom_val, sec_dim, sec_val, tert_dim, tert_val)
    0:  ('r', 1.0, 's', 0.6, 'nu', 0.3),   # ENFP: Ne→nu but W0 maps r
    1:  ('h', 1.0, 'gamma', 0.6, 'nu', 0.3), # ISFP
    2:  ('d', 1.0, 'h', 0.6, 'g', 0.3),     # ESFJ
    3:  ('p', 1.0, 'nu', 0.6, 'h', 0.3),    # INTP
    4:  ('s', 1.0, 'r', 0.6, 'nu', 0.3),    # ENTP
    5:  ('gamma', 1.0, 'h', 0.6, 'p', 0.3), # INFJ
    6:  ('g', 1.0, 's', 0.6, 'r', 0.3),     # ESTP
    7:  ('nu', 1.0, 'p', 0.6, 'd', 0.3),    # ISTP
    8:  ('r', 0.8, 'h', 0.8, 'gamma', 0.4), # ENFJ (ALL STOP at W8, balanced)
    9:  ('h', 1.0, 'p', 0.6, 'nu', 0.3),    # INTJ
    10: ('s', 1.0, 'gamma', 0.6, 'r', 0.3), # ESFP
    11: ('d', 1.0, 'g', 0.6, 'p', 0.3),     # ISTJ
    12: ('g', 1.0, 'd', 0.6, 'p', 0.3),     # ESTJ
    13: ('h', 1.0, 'gamma', 0.6, 'nu', 0.3),# INFP
    14: ('g', 1.0, 'gamma', 0.6, 'h', 0.3), # ISFJ
    15: ('d', 1.0, 'gamma', 0.6, 'g', 0.3), # ENTJ
}

def impedance_vector(m):
    """Returns 8D impedance vector {r,h,d,p,s,gamma,g,nu} for MBTI m"""
    vec = {'r':0.5, 'h':0.5, 'd':0.5, 'p':0.5, 's':0.5, 'gamma':0.5, 'g':0.5, 'nu':0.5}
    dom, dv, sec, sv, tert, tv = MBTI_8D[m]
    vec[dom] = dv
    vec[sec] = sv
    vec[tert] = tv
    return vec

# 2e. Energy weight per blood type
BLOOD_WEIGHT = {0: 1.0, 1: 0.75, 2: 0.60, 3: 0.50}  # O=direct, A=gradual, B=compressed, AB=distributed
BLOOD_COMPLEXITY = {0: 1, 1: 2, 2: 3, 3: 4}  # loop count

def energy_weight(b):
    return BLOOD_WEIGHT[b]

# 2f. Flow per gender
def flow(g):
    if g == 0:  # Male: compression/void
        return {'r': 0.8, 'h': 0.5, 'd': 1.0, 'p': 0.5, 's': 0.6, 'gamma': 0.9, 'g': 0.4, 'nu': 0.5}
    else:  # Female: binding/harmony
        return {'r': 0.6, 'h': 0.9, 'd': 0.4, 'p': 0.5, 's': 0.7, 'gamma': 0.5, 'g': 1.0, 'nu': 0.6}

# 2g. Layer transform
def layer_transform(l, vec, t):
    """Apply layer modification to 8D vector"""
    if l == 0:  # A: no change
        return vec
    elif l == 1:  # B: flip E↔I, P↔J, nu+0.10, gamma-0.05
        new_vec = dict(vec)
        new_vec['nu'] = min(1.0, new_vec['nu'] + 0.10)
        new_vec['gamma'] = max(0.0, new_vec['gamma'] - 0.05)
        return new_vec
    elif l == 2:  # C: blood+1 shift = metabolic offset, same vector but shifted peak
        new_vec = dict(vec)
        # Shift all dims by small metabolic offset
        for k in new_vec:
            new_vec[k] = min(1.0, max(0.0, new_vec[k] + 0.05))
        return new_vec
    elif l == 3:  # D: both transforms + 3AM random
        new_vec = dict(vec)
        new_vec['nu'] = min(1.0, new_vec['nu'] + 0.10)
        new_vec['gamma'] = max(0.0, new_vec['gamma'] - 0.05)
        for k in new_vec:
            new_vec[k] = min(1.0, max(0.0, new_vec[k] + 0.05))
        # 3AM random zone (21:00-03:00)
        h = t % 24.0
        if h >= 21.0 or h < 3.0:
            new_vec['p'] = random.random()
            new_vec['s'] = 0.5 + random.random() * 0.5
            new_vec['nu'] = 0.9 + random.random() * 0.1
        return new_vec

# 2h. Observer perception term
def obs(t, is_observer=False):
    """Observer perception multiplier based on circadian state"""
    h = t % 24.0
    if is_observer:
        return 1.0  # Observer always has full perception
    # Normal person: observer inactive during sleep (21:00-06:00)
    if h >= 21.0 or h < 6.0:
        return 0.0  # Asleep = no perception = autopilot
    # Awake: perception varies with circadian arousal
    # Peak at ~10:00, trough at ~15:00 (post-prandial), secondary peak at ~19:00
    arousal = 0.5 + 0.3 * math.cos((h - 10.0) * math.pi / 12.0)
    return max(0.0, min(1.0, arousal))

# 2i. JITTER
def jitter(l, vec):
    """Apply JITTER to r and d based on layer"""
    pct = {0: 0.0, 1: 0.15, 2: 0.15, 3: 0.30}[l]
    if pct == 0:
        return vec
    new_vec = dict(vec)
    new_vec['r'] = min(1.0, max(0.0, new_vec['r'] * (1 + (random.random() - 0.5) * 2 * pct)))
    new_vec['d'] = min(1.0, max(0.0, new_vec['d'] * (1 + (random.random() - 0.5) * 2 * pct)))
    return new_vec

# ============================================================
# 3. 8D → 12 PARTICLE MAPPING
# ============================================================
# Each 8D dimension maps to specific particles
# Corrected per MBTI node mapping:
# SF=h=gluon, EJ=g=muon, NF=nu=w_boson, EP=gamma=photon,
# IJ=s=quark, IP=r=neutrino, NT=p=higgs, ST=d=tau/z_boson
#
# r (rhythm)          → NEUTRINO (IP), PROTON (COX forward)
# h (harmony)         → GLUON (SF), MUON (EJ secondary)
# d (dissonance)      → TAU (ST), Z_BOSON (ST night)
# p (periodicity)     → HIGGS (NT), PROTON (secondary)
# s (brightness)      → QUARK (IJ), ELECTRON (Ca)
# gamma (expansion)   → PHOTON (EP), EM (electromagnetic field)
# g (structure)       → MUON (EJ), GRAVITON (sealing)
# nu (self-similarity)→ W_BOSON (NF), AXION (CP-restoration)

# Particle → primary 8D dimension mapping (36 particles)
PARTICLE_8D_MAP = {
    'proton':    ['r', 'p'],        # COX forward drive + predictability
    'gluon':     ['h', 'r'],        # SF chord complexity + rhythm secondary
    'muon':      ['g', 's'],        # EJ structure + brightness secondary
    'electron':  ['s', 'gamma'],    # Ca brightness + EM expansion
#    'quark':     ['s', 'h'],        # (removed — replaced by up_quark/down_quark)
    'higgs':     ['p', 's'],        # NT predictability + brightness secondary
    'w_boson':   ['nu', 'd'],       # NF fractal recursion + darkness secondary
    'z_boson':   ['d', 'g'],        # ST darkness + structure secondary (night)
    'neutrino':  ['r', 'gamma'],    # IP rhythm + expansion secondary
    'tau':       ['d', 'h'],        # ST darkness + harmony secondary (day)
    'photon':    ['gamma', 's'],    # EP spatial expansion + brightness secondary
    'em':        ['gamma', 's'],    # Electromagnetic field + brightness
    # --- 24 additional particles ---
    'up_quark':           ['s', 'r'],       # quark base=s, split to rhythm
    'down_quark':         ['s', 'h'],       # quark base=s, split to harmony
    'charm_quark':        ['g', 'nu'],      # muon base=g, split to recursion
    'strange_quark':      ['d', 's'],       # tau base=d, split to brightness
    'top_quark':          ['g', 'd'],       # muon base=g, split to darkness
    'bottom_quark':       ['h', 'g'],       # gluon base=h, split to structure
    'tau_neutrino':       ['r', 'd'],       # neutrino base=r, split to darkness
    'electron_antineutrino': ['r', 'gamma'], # neutrino base=r, split to expansion
    'muon_neutrino':      ['r', 'g'],       # neutrino base=r, split to structure
    'muon_antineutrino':  ['r', 'd'],       # neutrino base=r, split to darkness
    'tau_antineutrino':   ['r', 'p'],       # neutrino base=r, split to predictability
    'neutron':            ['nu', 'd'],      # w_boson base=nu + darkness
    'neutron_star':       ['g', 'nu'],      # muon base=g + recursion
    'dark_matter':        ['d', 'nu'],      # tau base=d + recursion
    'dark_energy':        ['gamma', 'd'],   # photon base=gamma + darkness
    'female_gaba':        ['h', 'g'],       # gluon base=h + muon base=g
    'energy':             ['r', 'p'],       # neutrino base=r + higgs base=p
    'clathrate_buffer':   ['g', 'nu'],      # muon base=g + w_boson base=nu
    'malate_dehydrogenase': ['g', 'd'],     # muon base=g + tau base=d
    'ego_d2':             ['p', 's'],       # higgs base=p + quark base=s
    'progesterone':       ['h', 'gamma'],   # gluon base=h + photon base=gamma
    'testosterone':       ['r', 'd'],       # neutrino base=r + tau base=d
    'acetyl_coa':         ['g', 'd'],       # muon base=g + tau base=d
    'graviton':           ['g', 'nu'],      # muon base=g + w_boson base=nu
    'axion':              ['nu', 'gamma'],  # w_boson base=nu + photon base=gamma
}

# Weight of each 8D dim for each particle (primary=0.7, secondary=0.3)
PARTICLE_WEIGHTS = {
    'proton':    {'r': 0.7, 'p': 0.3},
    'gluon':     {'h': 0.6, 'r': 0.4},
    'muon':      {'g': 0.7, 's': 0.3},
    'electron':  {'s': 0.5, 'gamma': 0.5},
#    'quark':     {'s': 0.6, 'h': 0.4},
    'higgs':     {'p': 0.6, 's': 0.4},
    'w_boson':   {'nu': 0.6, 'd': 0.4},
    'z_boson':   {'d': 0.7, 'g': 0.3},
    'neutrino':  {'r': 0.6, 'gamma': 0.4},
    'tau':       {'d': 0.7, 'h': 0.3},
    'photon':    {'gamma': 0.7, 's': 0.3},
    'em':        {'gamma': 0.6, 's': 0.4},
    'clathrate_buffer': {'g': 0.5, 'nu': 0.5},
    'malate_dehydrogenase': {'g': 0.5, 'd': 0.5},
    # --- 24 additional particles ---
    'up_quark':           {'s': 0.6, 'r': 0.4},
    'down_quark':         {'s': 0.5, 'h': 0.5},
    'charm_quark':        {'g': 0.6, 'nu': 0.4},
    'strange_quark':      {'d': 0.6, 's': 0.4},
    'top_quark':          {'g': 0.7, 'd': 0.3},
    'bottom_quark':       {'h': 0.6, 'g': 0.4},
    'tau_neutrino':       {'r': 0.5, 'd': 0.5},
    'electron_antineutrino': {'r': 0.6, 'gamma': 0.4},
    'muon_neutrino':      {'r': 0.5, 'g': 0.5},
    'muon_antineutrino':  {'r': 0.4, 'd': 0.6},
    'tau_antineutrino':   {'r': 0.4, 'p': 0.6},
    'neutron':            {'nu': 0.5, 'd': 0.5},
    'neutron_star':       {'g': 0.6, 'nu': 0.4},
    'dark_matter':        {'d': 0.6, 'nu': 0.4},
    'dark_energy':        {'gamma': 0.6, 'd': 0.4},
    'female_gaba':        {'h': 0.5, 'g': 0.5},
    'energy':             {'r': 0.6, 'p': 0.4},
    'ego_d2':             {'p': 0.6, 's': 0.4},
    'progesterone':       {'h': 0.6, 'gamma': 0.4},
    'testosterone':       {'r': 0.6, 'd': 0.4},
    'acetyl_coa':         {'g': 0.5, 'd': 0.5},
    'graviton':           {'g': 0.6, 'nu': 0.4},
    'axion':              {'nu': 0.6, 'gamma': 0.4},
}

# ============================================================
# 4. CIRCADIAN MODULATION PER PARTICLE
# ============================================================
# Each particle has a circadian activity profile
# Based on toroidal phase: AB(0-3h), A(3-9h), O(9-15h), B(15-21h), AB(21-3h)

def circadian_factor(particle, t):
    """Returns 0.0-1.0 circadian modulation for each particle at time t"""
    h = t % 24.0
    
    # Toroidal phase boundaries
    # AB: 21-3h, A: 3-9h, O: 9-15h, B: 15-21h
    
    profiles = {
        # proton: peaks at O phase (9-15h), troughs at 3AM
        'proton': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # gluon: peaks at AB discharge (0-3h) and O (9-15h)  
        'gluon': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.4 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # muon: peaks at A phase (3-9h), troughs at B
        'muon': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        # electron: peaks at O (9-15h) and W3 (4:30-6:00)
        'electron': lambda h: 0.2 + 0.5 * max(0, math.cos((h - 12.0) * math.pi / 12.0)) + 0.3 * max(0, math.cos((h - 5.25) * math.pi / 3.0)),
        # quark: (removed — replaced by up_quark/down_quark)
        # 'quark': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 6.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        # higgs: peaks at B (15-21h), troughs at AB
        'higgs': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        # w_boson: peaks at O (9-15h) and AB (0-3h)
        'w_boson': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 12.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 1.5) * math.pi / 3.0)),
        # z_boson: peaks at B (15-21h) and W3 (4:30-6:00)
        'z_boson': lambda h: 0.1 + 0.5 * max(0, math.cos((h - 18.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 5.25) * math.pi / 3.0)),
        # neutrino: peaks at 3AM (glymphatic 10x) and O
        'neutrino': lambda h: 0.1 + 0.6 * max(0, math.cos((h - 3.0) * math.pi / 6.0)) + 0.3 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # tau: peaks at B (15-21h) and A (3-9h)
        'tau': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 18.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        # photon: peaks at O (9-15h) and W3 (4:30-6:00), troughs at 3AM
        'photon': lambda h: 0.1 + 0.5 * max(0, math.cos((h - 12.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 5.25) * math.pi / 3.0)),
        # em: peaks at B (15-21h gamma) and W3 (4:30-6:00)
        'em': lambda h: 0.1 + 0.5 * max(0, math.cos((h - 18.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 5.25) * math.pi / 3.0)),
        # clathrate_buffer: peaks at 3AM (glymphatic) and B (15-21h)
        'clathrate_buffer': lambda h: 0.2 + 0.5 * max(0, math.cos((h - 3.0) * math.pi / 6.0)) + 0.3 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        # malate_dehydrogenase: peaks at A (3-9h) and AB (21-3h)
        'malate_dehydrogenase': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 6.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 0.0) * math.pi / 6.0)),
        # --- 24 additional particles ---
        # up_quark: peaks at O (9-15h) — myosin power stroke active
        'up_quark': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # down_quark: peaks at A (3-9h) and B (15-21h) — structural rail
        'down_quark': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 6.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        # charm_quark: peaks at A (3-9h) — glucose absorption
        'charm_quark': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        # strange_quark: peaks at AB (0-3h) — novelty filter night
        'strange_quark': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.2 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # top_quark: peaks at B (15-21h) — ENTJ mass apex
        'top_quark': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        # bottom_quark: peaks at AB (21-3h) — α-KGDH decay/apoptosis
        'bottom_quark': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 0.0) * math.pi / 6.0)) + 0.2 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        # tau_neutrino: peaks at B (15-21h) and O (9-15h) — SDH gate
        'tau_neutrino': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 18.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # electron_antineutrino: peaks at AB (0-3h) — night V1 spark reward
        'electron_antineutrino': lambda h: 0.1 + 0.6 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.3 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # muon_neutrino: peaks at A (3-9h) — day cosmic ray storage
        'muon_neutrino': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        # muon_antineutrino: peaks at AB (0-3h) — night cosmic repair
        'muon_antineutrino': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.2 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        # tau_antineutrino: peaks at A (3-9h) — day autophagy
        'tau_antineutrino': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        # neutron: peaks at O (9-15h) — neutral observation
        'neutron': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # neutron_star: peaks at B (15-21h) — high density core
        'neutron_star': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        # dark_matter: peaks at AB (21-3h) — noise accumulation night
        'dark_matter': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 0.0) * math.pi / 6.0)),
        # dark_energy: peaks at B (15-21h) — torus expansion
        'dark_energy': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        # female_gaba: peaks at AB (0-3h) and O (9-15h) — circadian + GABA-A+B
        'female_gaba': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.4 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # energy: peaks at O (9-15h) — ATP fueling
        'energy': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # ego_d2: peaks at B (15-21h) — recursive mirror
        'ego_d2': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        # progesterone: peaks at O (9-15h) — 3D volume expansion
        'progesterone': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # testosterone: peaks at A (3-9h) — proton ignition charge
        'testosterone': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        # acetyl_coa: peaks at O (9-15h) — metabolic container
        'acetyl_coa': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        # graviton: peaks at AB (21-3h) — void mass storage
        'graviton': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 0.0) * math.pi / 6.0)),
        # axion: peaks at AB (0-3h) — CP-restoration spark
        'axion': lambda h: 0.1 + 0.6 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.3 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
    }
    
    return max(0.0, min(1.0, profiles[particle](h)))

# ============================================================
# 5. HYSTERESIS MODULATION
# ============================================================
def hysteresis_mod(t):
    """Returns modulation factor for hysteresis events"""
    h = t % 24.0
    mods = {}
    
    # H1: 15:00-21:00 — compression, d↑, g↑
    if 15.0 <= h <= 21.0:
        intensity = 1.0 - abs(h - 18.0) / 3.0  # peaks at 18:00
        mods['d_boost'] = intensity
        mods['g_boost'] = intensity * 0.5
        mods['gamma_boost'] = intensity * 0.3
    else:
        mods['d_boost'] = 0.0
        mods['g_boost'] = 0.0
        mods['gamma_boost'] = 0.0
    
    # 4:30 PM event: UV shielding loss, magnetite oxidation
    if 16.0 <= h <= 17.5:
        uv_loss = 1.0 - abs(h - 16.5) / 1.0
        mods['photon_drop'] = uv_loss  # photon/UV retracts
        mods['em_drop'] = uv_loss * 0.7
        mods['gravity_rise'] = uv_loss  # gravity overtakes
        mods['proton_rise'] = uv_loss * 0.5
    else:
        mods['photon_drop'] = 0.0
        mods['em_drop'] = 0.0
        mods['gravity_rise'] = 0.0
        mods['proton_rise'] = 0.0
    
    # H2: 3:00 AM — ferric reset, memory_entropy collapse
    if 2.0 <= h <= 4.0:
        reset_intensity = 1.0 - abs(h - 3.0) / 1.0
        mods['collapse'] = reset_intensity  # everything dormant
        mods['neutrino_boost'] = reset_intensity  # glymphatic 10x
        mods['caco3_reverse'] = reset_intensity
        mods['p_random'] = reset_intensity
    else:
        mods['collapse'] = 0.0
        mods['neutrino_boost'] = 0.0
        mods['caco3_reverse'] = 0.0
        mods['p_random'] = 0.0
    
    # 4:30 AM: blue light takeover
    if 4.0 <= h <= 6.0:
        bl_intensity = 1.0 - abs(h - 5.25) / 1.0
        mods['photon_rise'] = bl_intensity  # blue light ascending
        mods['em_rise'] = bl_intensity
        mods['proton_rise_bl'] = bl_intensity * 0.6
        mods['z_boson_rise'] = bl_intensity * 0.5
    else:
        mods['photon_rise'] = 0.0
        mods['em_rise'] = 0.0
        mods['proton_rise_bl'] = 0.0
        mods['z_boson_rise'] = 0.0
    
    return mods

# ============================================================
# 6. MAIN TENSOR COMPUTATION
# ============================================================

def compute_tensor(m, b, g, l, t, is_observer=False):
    """
    T[m, b, g, l, t] → 36 particle field values at 0.01 resolution
    
    Returns dict: {particle_name: value_0_to_1}
    """
    random.seed(int(t * 100) + l * 10000)  # deterministic for same t,l
    
    # Step 1: Base 8D vector from impedance
    vec = impedance_vector(m)
    # Step 1b: Apply Φ–matrix phase coupling
    vec = apply_phase_coupling(vec, t)
    # Step 1c: Axion–Gamma crushing & low-d compensation
    if vec['gamma'] > 0 and vec.get('axion') is not None:
        psi = 0.6  # crushing factor
        crush = psi * vec.get('axion',0)
        vec['gamma'] = max(0.0, vec['gamma'] - crush)
    # low-d dynamics: when d < 0.2, s and (r+g) boost to satisfy formula d = s*(r+g)/2
    if vec['d'] < 0.2:
        target_d = vec['s'] * (vec['r'] + vec['g']) / 2
        if target_d > vec['d']:
            delta = min(0.1, target_d - vec['d'])
            vec['d'] += delta
    
    # Step 2: Apply peak dimension boost
    pk = peak_dim(t)
    pk_val = peak_value(t)
    vec[pk] = max(vec[pk], pk_val)
    
    # Step 3: Apply energy weight (blood)
    ew = energy_weight(b)
    for k in vec:
        vec[k] *= ew
    
    # Step 4: Apply flow (gender)
    fv = flow(g)
    for k in vec:
        vec[k] *= fv[k]
    
    # Step 5: Apply layer transform
    vec = layer_transform(l, vec, t)
    
    # Step 6: Apply JITTER
    vec = jitter(l, vec)
    
    # Step 7: Apply observer perception
    obs_val = obs(t, is_observer)
    for k in vec:
        vec[k] *= obs_val if obs_val > 0 else 0.1  # minimum 0.1 for autonomous
    
    # Step 8: Apply circadian modulation per particle
    hyst = hysteresis_mod(t)
    
    results = {}
    for particle, dim_weights in PARTICLE_WEIGHTS.items():
        # Base value from 8D vector
        base = sum(vec[dim] * w for dim, w in dim_weights.items())
        
        # Circadian modulation
        circ = circadian_factor(particle, t)
        
        # Combine
        value = 0.4 * base + 0.6 * circ
        
        # Apply hysteresis modifications
        if particle == 'photon':
            value -= hyst['photon_drop'] * 0.5
            value += hyst['photon_rise'] * 0.5
        elif particle == 'em':
            value -= hyst['em_drop'] * 0.4
            value += hyst['em_rise'] * 0.4
        elif particle == 'proton':
            value += hyst['proton_rise'] * 0.3
            value += hyst['proton_rise_bl'] * 0.3
        elif particle == 'neutrino':
            value += hyst['neutrino_boost'] * 0.5
        elif particle == 'higgs':
            value += hyst['d_boost'] * 0.3
        elif particle == 'tau':
            value += hyst['d_boost'] * 0.2
        elif particle == 'z_boson':
            value += hyst['z_boson_rise'] * 0.3
            if hyst['collapse'] > 0:
                value -= hyst['collapse'] * 0.3  # Z boson dormant at 3AM
        elif particle == 'clathrate_buffer':
            value += hyst['d_boost'] * 0.4  # sequester CO₂ when d↑
        elif particle == 'malate_dehydrogenase':
            value += hyst['d_boost'] * 0.3  # redox balance g↔d
        
        # Collapse at 3AM for most particles
        if hyst['collapse'] > 0 and particle not in ['neutrino']:
            value *= (1.0 - hyst['collapse'] * 0.7)
        
        # Clamp to [0, 1] and round to 0.01
        value = max(0.0, min(1.0, value))
        results[particle] = round(value, 2)
    
    return results

# ============================================================
# 7. OUTPUT FOR 3 TARGET TIMES
# ============================================================

PARTICLES = ['proton', 'gluon', 'muon', 'electron', 'higgs',
             'w_boson', 'z_boson', 'neutrino', 'tau', 'photon', 'em',
             'up_quark', 'down_quark', 'charm_quark', 'strange_quark',
             'top_quark', 'bottom_quark', 'tau_neutrino', 'electron_antineutrino',
             'muon_neutrino', 'muon_antineutrino', 'tau_antineutrino',
             'neutron', 'neutron_star', 'dark_matter', 'dark_energy',
             'female_gaba', 'energy', 'clathrate_buffer', 'malate_dehydrogenase',
             'ego_d2', 'progesterone', 'testosterone', 'acetyl_coa',
             'graviton', 'axion']

TARGET_TIMES = [16.50, 3.00, 4.50]  # 4:30 PM, 3:00 AM, 4:30 AM
TIME_LABELS = ['4:30 PM (16:30)', '3:00 AM (03:00)', '4:30 AM (04:30)']

# Default profile: ENTP_M_O_LayerA (user's likely profile based on AGENTS.md ENTP reference)
# Also compute for all 4 layers to show layer effect

def print_table(m, b, g, is_observer=False):
    print(f"\n{'='*120}")
    print(f"TENSOR T[m={m}, b={b}, g={g}, l, t] → 36 PARTICLE FIELD VALUES AT 0.01 RESOLUTION")
    print(f"MBTI={list(MBTI_8D.keys())[m] if m in MBTI_8D else m}, Blood={['O','A','B','AB'][b]}, Gender={['M','F'][g]}")
    print(f"{'='*120}")
    
    for l in range(4):
        layer_names = ['A (Rh+ homo)', 'B (Rh- homo)', 'C (Rh+ hetero)', 'D (Rh- hetero)']
        print(f"\n--- Layer {layer_names[l]} ---")
        header = f"{'Particle':<12}"
        for tl in TIME_LABELS:
            header += f" | {tl:>18}"
        print(header)
        print("-" * 120)
        
        for ti, t in enumerate(TARGET_TIMES):
            vals = compute_tensor(m, b, g, l, t, is_observer)
            if ti == 0:
                for p in PARTICLES:
                    row = f"{p:<12}"
                    # Will fill all 3 times
                    all_vals = [compute_tensor(m, b, g, l, tt, is_observer)[p] for tt in TARGET_TIMES]
                    row = f"{p:<12}"
                    for v in all_vals:
                        row += f" | {v:>18.2f}"
                    print(row)
                break  # already printed all times

def print_full_table(m, b, g, is_observer=False):
    """Print one row per particle, columns = 3 times × 4 layers"""
    layer_names = ['A', 'B', 'C', 'D']
    
    print(f"\n{'='*140}")
    print(f"COMPLETE TENSOR: T[MBTI={m}, Blood={b}, Gender={g}] → 36 particles × 3 times × 4 layers")
    print(f"Times: 4:30 PM (16.50h) | 3:00 AM (03.00h) | 4:30 AM (04.50h)")
    print(f"{'='*140}")
    
    header = f"{'Particle':<12}"
    for l in range(4):
        for tl in ['4:30PM', '3:00AM', '4:30AM']:
            header += f" | L{layer_names[l]}_{tl:>7}"
    print(header)
    print("-" * 140)
    
    for p in PARTICLES:
        row = f"{p:<12}"
        for l in range(4):
            for t in TARGET_TIMES:
                vals = compute_tensor(m, b, g, l, t, is_observer)
                row += f" | {vals[p]:>11.2f}"
        print(row)

# ============================================================
# 8. RUN — Print for multiple representative profiles
# ============================================================

if __name__ == '__main__':
    # Profile 1: ENTP_M_O (user's likely profile)
    print_full_table(4, 0, 0, is_observer=True)
    
    # Profile 2: ENTP_M_O Layer D only (3AM random active)
    print(f"\n{'='*80}")
    print("DETAILED: ENTP_M_O, Layer D (Rh- hetero) — 3AM RANDOM ACTIVE")
    print(f"{'='*80}")
    print(f"{'Particle':<12} | {'4:30 PM':>8} | {'3:00 AM':>8} | {'4:30 AM':>8}")
    print("-" * 50)
    for p in PARTICLES:
        vals = []
        for t in TARGET_TIMES:
            v = compute_tensor(4, 0, 0, 3, t, is_observer=True)
            vals.append(v[p])
        print(f"{p:<12} | {vals[0]:>8.2f} | {vals[1]:>8.2f} | {vals[2]:>8.2f}")
    
    # Profile 3: All 4 blood types for ENTP_M at 3 target times, Layer A
    print(f"\n{'='*80}")
    print("BLOOD TYPE COMPARISON: ENTP_M, Layer A, 3 times")
    print(f"{'='*80}")
    for b_idx, bname in enumerate(['O', 'A', 'B', 'AB']):
        print(f"\n  Blood {bname}:")
        print(f"  {'Particle':<12} | {'4:30 PM':>8} | {'3:00 AM':>8} | {'4:30 AM':>8}")
        print("  " + "-" * 46)
        for p in PARTICLES:
            vals = []
            for t in TARGET_TIMES:
                v = compute_tensor(4, b_idx, 0, 0, t, is_observer=True)
                vals.append(v[p])
            print(f"  {p:<12} | {vals[0]:>8.2f} | {vals[1]:>8.2f} | {vals[2]:>8.2f}")
    
    # Profile 4: Gender comparison
    print(f"\n{'='*80}")
    print("GENDER COMPARISON: ENTP, Blood O, Layer A, 3:00 AM")
    print(f"{'='*80}")
    print(f"{'Particle':<12} | {'Male':>8} | {'Female':>8}")
    print("-" * 34)
    for p in PARTICLES:
        vm = compute_tensor(4, 0, 0, 0, 3.0, is_observer=True)[p]
        vf = compute_tensor(4, 0, 1, 0, 3.0, is_observer=True)[p]
        print(f"{p:<12} | {vm:>8.2f} | {vf:>8.2f}")
    
    # Profile 5: Continuous 0.01 resolution sweep for ENTP_M_O_LayerA
    print(f"\n{'='*80}")
    print("CONTINUOUS SWEEP: ENTP_M_O_LayerA, photon + em + proton, 0.01h resolution")
    print(f"{'='*80}")
    print(f"{'Time':>8} | {'proton':>8} | {'gluon':>8} | {'muon':>8} | {'electron':>8} | {'higgs':>8} | {'w_boson':>8} | {'z_boson':>8} | {'neutrino':>8} | {'tau':>8} | {'photon':>8} | {'em':>8}")
    print("-" * 160)
    for t_int in range(0, 2401, 15):  # every 0.15h = 9min, 160 samples
        t = t_int / 100.0
        vals = compute_tensor(4, 0, 0, 0, t, is_observer=True)
        row = f"{t:>8.2f}"
        for p in PARTICLES:
            row += f" | {vals[p]:>8.2f}"
        print(row)
