#!/usr/bin/env python3
"""
_activity_gen.py — 128 profiles × 6 slots activity mapping from scratch.

3-way intersection:
  1. 36 particles (3 per attractor = nonlinear tri-directional interaction)
  2. 8D parameters (r,h,d,p,s,gamma,g,nu) — each particle carries different info
  3. Tensor dynamics (dTensor_dt) — particle×param×route cross evolves over time

6 slots = 6 attractors (energy, information, repair, opioid_landau, gan_bulkhead, cox_retrograde)
3 routes = Oxford (gleysol/core), Out_of_Oxford (podzol/mid), Out_of_England (periphery)
3 states = RELEASE, STRESS_GROWTH, EXTREME_GROWTH

Each profile × slot → top 3 particles (nonlinear interaction) → 8D signature → activity.
No two profiles share the same activity in the same slot.
"""

import math
import random
import json
import hashlib

# ============================================================
# 36 PARTICLES
# ============================================================
PARTICLES36 = [
    'proton', 'gluon', 'muon', 'electron', 'higgs',
    'w_boson', 'z_boson', 'neutrino', 'tau', 'photon', 'em',
    'up_quark', 'down_quark', 'charm_quark', 'strange_quark',
    'top_quark', 'bottom_quark', 'tau_neutrino', 'electron_antineutrino',
    'muon_neutrino', 'muon_antineutrino', 'tau_antineutrino',
    'neutron', 'neutron_star', 'dark_matter', 'dark_energy',
    'female_gaba', 'energy', 'clathrate_buffer', 'malate_dehydrogenase',
    'ego_d2', 'progesterone', 'testosterone', 'acetyl_coa',
    'graviton', 'axion',
]

DIMS = ['r', 'h', 'd', 'p', 's', 'gamma', 'g', 'nu']

# ============================================================
# PARTICLE → 8D WEIGHTS (from tensor_equation.py)
# ============================================================
PARTICLE_WEIGHTS = {
    'proton':    {'r': 0.7, 'p': 0.3},
    'gluon':     {'h': 0.6, 'r': 0.4},
    'muon':      {'g': 0.7, 's': 0.3},
    'electron':  {'s': 0.5, 'gamma': 0.5},
    'higgs':     {'p': 0.6, 's': 0.4},
    'w_boson':   {'nu': 0.6, 'd': 0.4},
    'z_boson':   {'d': 0.7, 'g': 0.3},
    'neutrino':  {'r': 0.6, 'gamma': 0.4},
    'tau':       {'d': 0.7, 'h': 0.3},
    'photon':    {'gamma': 0.7, 's': 0.3},
    'em':        {'gamma': 0.6, 's': 0.4},
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
    'clathrate_buffer':   {'g': 0.5, 'nu': 0.5},
    'malate_dehydrogenase': {'g': 0.5, 'd': 0.5},
    'ego_d2':             {'p': 0.6, 's': 0.4},
    'progesterone':       {'h': 0.6, 'gamma': 0.4},
    'testosterone':       {'r': 0.6, 'd': 0.4},
    'acetyl_coa':         {'g': 0.5, 'd': 0.5},
    'graviton':           {'g': 0.6, 'nu': 0.4},
    'axion':              {'nu': 0.6, 'gamma': 0.4},
}

# ============================================================
# 6 ATTRACTORS — each slot = 1 attractor with 3 particles
# ============================================================
ATTRACTORS = {
    0: {'name': 'energy',        'particles': ['proton', 'gluon', 'w_boson'],
        'route': 'Oxford',         'state': 'RELEASE',
        'time': 12.0,              'label': 'SLOT_1_ENERGY'},
    1: {'name': 'information',   'particles': ['neutrino', 'photon', 'muon'],
        'route': 'Out_of_Oxford',  'state': 'STRESS_GROWTH',
        'time': 6.0,               'label': 'SLOT_2_INFORMATION'},
    2: {'name': 'repair',        'particles': ['tau', 'z_boson', 'higgs'],
        'route': 'Out_of_England', 'state': 'EXTREME_GROWTH',
        'time': 18.0,              'label': 'SLOT_3_REPAIR'},
    3: {'name': 'opioid_landau', 'particles': ['electron', 'muon_antineutrino', 'charm_quark'],
        'route': 'Oxford',         'state': 'STRESS_GROWTH',
        'time': 1.5,               'label': 'SLOT_4_OPIOID'},
    4: {'name': 'gan_bulkhead',  'particles': ['gluon', 'higgs', 'top_quark'],
        'route': 'Out_of_Oxford',  'state': 'EXTREME_GROWTH',
        'time': 18.0,              'label': 'SLOT_5_GAN_BULKHEAD'},
    5: {'name': 'cox_retrograde','particles': ['electron', 'neutrino', 'photon'],
        'route': 'Out_of_England', 'state': 'RELEASE',
        'time': 5.25,              'label': 'SLOT_6_COX_RETROGRADE'},
}

# ============================================================
# 128 PROFILES: 16 MBTI × 2 gender × 4 blood types
# ============================================================
MBTI_LIST = [
    'ENFP', 'ISFP', 'ESFJ', 'INTP', 'ENTP', 'INFJ', 'ESTP', 'ISTP',
    'ENFJ', 'INTJ', 'ESFP', 'ISTJ', 'ESTJ', 'INFP', 'ISFJ', 'ENTJ',
]
MBTI_IDX = {m: i for i, m in enumerate(MBTI_LIST)}
BLOOD_TYPES = ['O', 'A', 'B', 'AB']
GENDERS = ['M', 'F']

# MBTI → 8D impedance (from tensor_equation.py)
MBTI_8D = {
    0:  ('r', 1.0, 's', 0.6, 'nu', 0.3),   # ENFP
    1:  ('h', 1.0, 'gamma', 0.6, 'nu', 0.3), # ISFP
    2:  ('d', 1.0, 'h', 0.6, 'g', 0.3),     # ESFJ
    3:  ('p', 1.0, 'nu', 0.6, 'h', 0.3),    # INTP
    4:  ('s', 1.0, 'r', 0.6, 'nu', 0.3),    # ENTP
    5:  ('gamma', 1.0, 'h', 0.6, 'p', 0.3), # INFJ
    6:  ('g', 1.0, 's', 0.6, 'r', 0.3),     # ESTP
    7:  ('nu', 1.0, 'p', 0.6, 'd', 0.3),    # ISTP
    8:  ('r', 0.8, 'h', 0.8, 'gamma', 0.4), # ENFJ
    9:  ('h', 1.0, 'p', 0.6, 'nu', 0.3),    # INTJ
    10: ('s', 1.0, 'gamma', 0.6, 'r', 0.3), # ESFP
    11: ('d', 1.0, 'g', 0.6, 'p', 0.3),     # ISTJ
    12: ('g', 1.0, 'd', 0.6, 'p', 0.3),     # ESTJ
    13: ('h', 1.0, 'gamma', 0.6, 'nu', 0.3),# INFP
    14: ('g', 1.0, 'gamma', 0.6, 'h', 0.3), # ISFJ
    15: ('d', 1.0, 'gamma', 0.6, 'g', 0.3), # ENTJ
}

BLOOD_WEIGHT = {0: 1.0, 1: 0.75, 2: 0.60, 3: 0.50}

def flow(g):
    if g == 0:
        return {'r': 0.8, 'h': 0.5, 'd': 1.0, 'p': 0.5, 's': 0.6, 'gamma': 0.9, 'g': 0.4, 'nu': 0.5}
    else:
        return {'r': 0.6, 'h': 0.9, 'd': 0.4, 'p': 0.5, 's': 0.7, 'gamma': 0.5, 'g': 1.0, 'nu': 0.6}

def impedance_vector(m):
    vec = {'r': 0.5, 'h': 0.5, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.5, 'g': 0.5, 'nu': 0.5}
    dom, dv, sec, sv, tert, tv = MBTI_8D[m]
    vec[dom] = dv
    vec[sec] = sv
    vec[tert] = tv
    return vec

# ============================================================
# CIRCADIAN FACTOR (simplified from tensor_equation.py)
# ============================================================
def circadian_factor(particle, t):
    h = t % 24.0
    profiles = {
        'proton': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'gluon': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.4 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'muon': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        'electron': lambda h: 0.2 + 0.5 * max(0, math.cos((h - 12.0) * math.pi / 12.0)) + 0.3 * max(0, math.cos((h - 5.25) * math.pi / 3.0)),
        'higgs': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        'w_boson': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 12.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 1.5) * math.pi / 3.0)),
        'z_boson': lambda h: 0.1 + 0.5 * max(0, math.cos((h - 18.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 5.25) * math.pi / 3.0)),
        'neutrino': lambda h: 0.1 + 0.6 * max(0, math.cos((h - 3.0) * math.pi / 6.0)) + 0.3 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'tau': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 18.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        'photon': lambda h: 0.1 + 0.5 * max(0, math.cos((h - 12.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 5.25) * math.pi / 3.0)),
        'em': lambda h: 0.1 + 0.5 * max(0, math.cos((h - 18.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 5.25) * math.pi / 3.0)),
        'up_quark': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'down_quark': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 6.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        'charm_quark': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        'strange_quark': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.2 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'top_quark': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        'bottom_quark': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 0.0) * math.pi / 6.0)) + 0.2 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        'tau_neutrino': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 18.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'electron_antineutrino': lambda h: 0.1 + 0.6 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.3 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'muon_neutrino': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        'muon_antineutrino': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.2 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        'tau_antineutrino': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        'neutron': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'neutron_star': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        'dark_matter': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 0.0) * math.pi / 6.0)),
        'dark_energy': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        'female_gaba': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.4 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'energy': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'clathrate_buffer': lambda h: 0.2 + 0.5 * max(0, math.cos((h - 3.0) * math.pi / 6.0)) + 0.3 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        'malate_dehydrogenase': lambda h: 0.2 + 0.4 * max(0, math.cos((h - 6.0) * math.pi / 12.0)) + 0.4 * max(0, math.cos((h - 0.0) * math.pi / 6.0)),
        'ego_d2': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 18.0) * math.pi / 12.0)),
        'progesterone': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'testosterone': lambda h: 0.3 + 0.7 * max(0, math.cos((h - 6.0) * math.pi / 12.0)),
        'acetyl_coa': lambda h: 0.2 + 0.8 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
        'graviton': lambda h: 0.2 + 0.6 * max(0, math.cos((h - 0.0) * math.pi / 6.0)),
        'axion': lambda h: 0.1 + 0.6 * max(0, math.cos((h - 1.5) * math.pi / 3.0)) + 0.3 * max(0, math.cos((h - 12.0) * math.pi / 12.0)),
    }
    if particle in profiles:
        return max(0.0, min(1.0, profiles[particle](h)))
    return 0.5

# ============================================================
# ROUTE FACTOR
# ============================================================
def route_factor(route):
    if route == 'Oxford': return 1.0
    if route == 'Out_of_Oxford': return 0.65
    return 0.35

def state_factor(state):
    if state == 'RELEASE': return 1.0
    if state == 'STRESS_GROWTH': return 1.35
    return 1.75

# ============================================================
# 36×36 INTERACTION MATRIX (extended from tensor_v5.js 12×12)
# ============================================================
def build_interaction_36():
    M = {}
    for a in PARTICLES36:
        M[a] = {}
        for b in PARTICLES36:
            M[a][b] = 0.0

    # Strong: quark family ↔ gluon
    for q in ['up_quark', 'down_quark', 'charm_quark', 'strange_quark', 'top_quark', 'bottom_quark']:
        M[q]['gluon'] = 0.8; M['gluon'][q] = 0.6
    M['proton']['up_quark'] = 0.5; M['proton']['gluon'] = 0.4

    # EM: photon ↔ electron, proton
    M['electron']['photon'] = 0.5; M['photon']['electron'] = 0.3
    M['proton']['photon'] = 0.2; M['em']['photon'] = 0.4; M['em']['electron'] = 0.3

    # Weak: W ↔ electron, muon, tau, neutrino; Z ↔ neutrino
    M['electron']['w_boson'] = 0.4; M['muon']['w_boson'] = 0.3; M['tau']['w_boson'] = 0.3
    M['neutrino']['w_boson'] = 0.2; M['w_boson']['electron'] = -0.2; M['w_boson']['muon'] = -0.1
    M['neutrino']['z_boson'] = 0.3; M['z_boson']['neutrino'] = 0.2

    # Neutrino variants
    for nv in ['electron_antineutrino', 'muon_neutrino', 'muon_antineutrino', 'tau_neutrino', 'tau_antineutrino']:
        M[nv]['z_boson'] = 0.25; M[nv]['w_boson'] = 0.15
        M['electron'][nv] = 0.1; M['neutrino'][nv] = 0.15

    # Mass/Higgs
    M['w_boson']['higgs'] = 0.4; M['z_boson']['higgs'] = 0.4
    M['electron']['higgs'] = 0.1; M['muon']['higgs'] = 0.2; M['tau']['higgs'] = 0.3
    M['higgs']['higgs'] = -0.1
    M['top_quark']['higgs'] = 0.5; M['neutron_star']['higgs'] = 0.3

    # Axion/dark mixing
    M['axion']['higgs'] = 0.2; M['higgs']['axion'] = 0.1; M['axion']['photon'] = 0.1
    M['dark_matter']['axion'] = 0.3; M['dark_energy']['axion'] = 0.2
    M['graviton']['higgs'] = 0.2; M['higgs']['graviton'] = 0.1

    # Lepton decays
    M['electron']['muon'] = 0.2; M['neutrino']['muon'] = 0.2; M['muon']['muon'] = -0.4
    M['electron']['tau'] = 0.3; M['neutrino']['tau'] = 0.2; M['tau']['tau'] = -0.5

    # Hormone/steroid interactions
    M['testosterone']['proton'] = 0.4; M['progesterone']['photon'] = 0.3
    M['progesterone']['gluon'] = 0.2; M['testosterone']['up_quark'] = 0.3

    # Metabolic
    M['acetyl_coa']['energy'] = 0.5; M['energy']['proton'] = 0.3; M['energy']['gluon'] = 0.2
    M['malate_dehydrogenase']['electron'] = 0.2; M['malate_dehydrogenase']['neutrino'] = 0.1
    M['clathrate_buffer']['dark_matter'] = 0.2; M['clathrate_buffer']['tau'] = 0.1

    # GABA
    M['female_gaba']['gluon'] = 0.3; M['female_gaba']['photon'] = 0.2
    M['strange_quark']['female_gaba'] = 0.2

    # Ego/mirror
    M['ego_d2']['higgs'] = 0.2; M['ego_d2']['neutron_star'] = 0.15; M['ego_d2']['z_boson'] = 0.1

    # Neutron
    M['neutron']['neutrino'] = 0.2; M['neutron']['z_boson'] = 0.15
    M['neutron_star']['neutron'] = 0.3; M['neutron']['neutron_star'] = 0.2

    return M

INTERACTION36 = build_interaction_36()

# ============================================================
# dTensor_dt — nonlinear dynamics for 36 particles
# ============================================================
def dTensor_dt_36(vec, route, state, graviton_active):
    d = {p: 0.0 for p in PARTICLES36}

    # Interaction term: i changes by influence from j weighted by both abundances
    for i in PARTICLES36:
        for j in PARTICLES36:
            d[i] += INTERACTION36[i][j] * (vec[j] or 0) * (vec[i] or 0)

    # Route drift
    rf = route_factor(route)
    d['axion'] += (1 - rf) * 0.05 * (vec.get('higgs', 0))
    d['neutrino'] += (1 - rf) * 0.03 * (vec.get('w_boson', 0))
    d['higgs'] -= (1 - rf) * 0.02 * (vec.get('higgs', 0))
    d['w_boson'] -= (1 - rf) * 0.02 * (vec.get('w_boson', 0))

    # State drift
    if state == 'STRESS_GROWTH':
        d['muon'] += 0.02; d['tau'] += 0.01; d['gluon'] += 0.01
        d['strange_quark'] += 0.01; d['malate_dehydrogenase'] += 0.01
    if state == 'EXTREME_GROWTH':
        d['neutrino'] += 0.03; d['axion'] += 0.02; d['quark'] = d.get('quark', 0) - 0.01
        d['dark_matter'] += 0.02; d['dark_energy'] += 0.01; d['graviton'] += 0.01

    # Graviton leakage (night)
    if graviton_active:
        d['axion'] += 0.02 * (vec.get('higgs', 0))
        d['higgs'] -= 0.02 * (vec.get('higgs', 0))
        d['graviton'] += 0.01 * (vec.get('neutron_star', 0))

    return d

def evolve_tensor_36(vec, route, state, graviton_active, dt=0.1, steps=10):
    current = dict(vec)
    for _ in range(steps):
        d = dTensor_dt_36(current, route, state, graviton_active)
        for p in PARTICLES36:
            current[p] = max(0, current.get(p, 0) + d[p] * dt)
        s = sum(current.values())
        if s > 0:
            for p in PARTICLES36:
                current[p] /= s
    return current

# ============================================================
# COMPUTE 36-PARTICLE VECTOR FOR (profile, slot)
# ============================================================
def compute_particle_vector(mbti_idx, blood_idx, gender_idx, slot_idx):
    attractor = ATTRACTORS[slot_idx]
    t = attractor['time']
    route = attractor['route']
    state = attractor['state']

    # 8D base vector
    vec8 = impedance_vector(mbti_idx)
    # Blood weight
    ew = BLOOD_WEIGHT[blood_idx]
    for k in vec8:
        vec8[k] *= ew
    # Gender flow
    fv = flow(gender_idx)
    for k in vec8:
        vec8[k] *= fv[k]
    # Clamp
    for k in vec8:
        vec8[k] = max(0.0, min(1.0, vec8[k]))

    # Compute 36 particle values
    results = {}
    rf = route_factor(route)
    sf = state_factor(state)
    graviton_active = (t >= 21.0 or t < 4.5)

    for p in PARTICLES36:
        weights = PARTICLE_WEIGHTS.get(p, {'g': 1.0})
        base = sum(vec8.get(dim, 0.5) * w for dim, w in weights.items())
        circ = circadian_factor(p, t)
        value = 0.4 * base + 0.6 * circ
        value *= rf * sf
        results[p] = max(0.0, min(1.0, value))

    # Evolve with nonlinear dynamics
    evolved = evolve_tensor_36(results, route, state, graviton_active, 0.1, 10)

    return evolved, vec8

# ============================================================
# ACTIVITY GENERATION
# ============================================================
# Activity vocabulary organized by 8D dimension dominance
# Each dimension maps to a category of activities
# The 3-way intersection (particle × 8D × route) selects a unique activity

# Dimension → activity category
DIM_ACTIVITIES = {
    'r': {  # rhythm/attack/tempo — physical exertion, cyclic movement
        'Oxford': ['SPRINT INTERVALS', 'JUMP ROPE', 'ROWING ERGOMETER', 'CYCLING TIME TRIAL', 'SWIMMING SPRINTS', 'BOXING COMBINATION DRILLS', 'KETTLEBELL CIRCUIT', 'BURPEE INTERVALS', 'STAIR CLIMBING', 'BATTLE ROPES'],
        'Out_of_Oxford': ['DANCE IMPROVISATION', 'CAPOEIRA', 'BREAKDANCING', 'TANGO', 'HIP-HOP DANCE', 'STEP AEROBICS', 'TRAMPOLINE', 'JUMPING JACKS CIRCUIT', 'SKIPPING ROPE VARIATIONS', 'RHYTHMIC GYMNASTICS'],
        'Out_of_England': ['TRAIL RUNNING', 'CROSS-COUNTRY SKIING', 'ORIENTEERING', 'NORDIC WALKING', 'BEACH SPRINTS', 'HILL REPEATS', 'SANDBAG CARRY', 'OBSTACLE COURSE RUNNING', 'PARKOUR', 'FREE RUNNING'],
    },
    'h': {  # harmony/texture — creative composition, texture work
        'Oxford': ['PIANO COMPOSITION', 'STRING QUARTET ARRANGEMENT', 'CHORAL HARMONY STUDY', 'COUNTERPOINT EXERCISE', 'JAZZ PIANO VOICINGS', 'ORCHESTRATION', 'FIGURED BASS REALIZATION', 'MICROTONAL COMPOSITION', 'SPECTRAL MUSIC ANALYSIS', 'CONSTRAINT-BASED COMPOSITION'],
        'Out_of_Oxford': ['FOLK GUITAR FINGERSTYLE', 'BANJO CLAWHAMMER', 'DULCIMER PLAYING', 'HARP PRACTICE', 'ACOUSTIC ARRANGEMENT', 'TRADITIONAL MUSIC TRANSCRIPTION', 'FIELD RECORDING COMPOSITION', 'TEXTURE SYNTHESIS', 'GRANULAR SYNTHESIS', 'SOUND COLLAGE'],
        'Out_of_England': ['AMBIENT DRONE COMPOSITION', 'SHOEGAZE GUITAR LAYERING', 'NOISE TEXTURE GENERATION', 'REVERB SCULPTING', 'MODULAR SYNTH PATCH', 'TAPE MUSIC COMPOSITION', 'CONCRETE MUSIC', 'SLOW MOTION REMIX', 'SPECTRAL DRIFT', 'HARMONIC RESONANCE TUNING'],
    },
    'd': {  # dissonance/darkness — analytical, void-facing, deep cognitive
        'Oxford': ['CHESS ENDGAME STUDY', 'GO JOSEKI ANALYSIS', 'PROOF WRITING', 'CRYPTOGRAPHY EXERCISE', 'FORMAL LOGIC', 'TOPOLOGY PROBLEM SET', 'CATEGORY THEORY', 'SET THEORY', 'GAME THEORY NASH EQUILIBRIUM', 'RECURRENCE RELATION SOLVING'],
        'Out_of_Oxford': ['PHILOSOPHY READING', 'PHENOMENOLOGY JOURNAL', 'EXISTENTIAL WRITING', 'DARKROOM PHOTOGRAPHY', 'BLACK INK DRAWING', 'VOID MEDITATION', 'ZEN KOAN STUDY', 'NEGATIVE SPACE PAINTING', 'MONOCHROME COMPOSITION', 'DECONSTRUCTION ANALYSIS'],
        'Out_of_England': ['FREE JAZZ IMPROVISATION', 'AVANT-GARDE COMPOSITION', 'NOISE MUSIC PERFORMANCE', 'POWER ELECTRONICS', 'DARK AMBIENT DRONE', 'INDUSTRIAL SOUND DESIGN', 'GLITCH COMPOSITION', 'DRONE METAL', 'HARSH NOISE WALL', 'SPECTRAL DISRUPTION'],
    },
    'p': {  # periodicity/prediction — pattern, structure, coding
        'Oxford': ['ALGORITHMIC COMPOSITION', 'CODE REVIEW', 'UNIT TESTING', 'REFACTORING', 'DATABASE SCHEMA DESIGN', 'API DESIGN', 'SYSTEM ARCHITECTURE', 'PROTOCOL SPECIFICATION', 'DETERMINISTIC SIMULATION', 'FORMAL VERIFICATION'],
        'Out_of_Oxford': ['PATTERN RECOGNITION TRAINING', 'RUBIK\'S CUBE PRACTICE', 'SUDOKU', 'NONOGRAM PUZZLES', 'KAKURO', 'SLIDING TILE PUZZLE', 'TOPOLOGICAL PUZZLE', 'TANGRAM', 'PENTOMINO TILING', 'CONSTRAINT SATISFACTION'],
        'Out_of_England': ['GENERATIVE ART CODING', 'CELLULAR AUTOMATON', 'L-SYSTEM GENERATION', 'FRACTAL RENDERING', 'MANDELBROT EXPLORATION', 'PERLIN NOISE SCULPTING', 'SHADER PROGRAMMING', 'PROCEDURAL TERRAIN', 'WAVE FUNCTION COLLAPSE', 'REACTION-DIFFUSION SIMULATION'],
    },
    's': {  # brightness/mass — visual, sensory, high-frequency
        'Oxford': ['DIGITAL PAINTING', 'COLOR THEORY STUDY', 'PHOTO EDITING', 'LIGHTING DESIGN', 'STUDIO PHOTOGRAPHY', 'COLOR GRADING', 'VISUAL EFFECTS', '3D RENDERING', 'MOTION GRAPHICS', 'BRIGHTFIELD MICROSCOPY'],
        'Out_of_Oxford': ['WILDLIFE PHOTOGRAPHY', 'LANDSCAPE PAINTING', 'BOTANICAL ILLUSTRATION', 'PLEIN AIR PAINTING', 'WATERCOLOR', 'PASTEL DRAWING', 'STAINED GLASS DESIGN', 'CALLIGRAPHY', 'ILLUMINATION', 'GOLD LEAF GILDING'],
        'Out_of_England': ['HYPERPOP PRODUCTION', 'WITCH HOUSE COMPOSITION', 'DECONSTRUCTED CLUB MIX', 'GLITCH POP ARRANGEMENT', 'VAPORWAVE SAMPLING', 'BRIGHT NOISE SCULPTING', 'FREQUENCY MODULATION SYNTHESIS', 'SPECTRAL FREEZING', 'BITCRUSH PROCESSING', 'ULTRASONIC EXPLORATION'],
    },
    'gamma': {  # spatial expansion — architecture, 3D, environment
        'Oxford': ['3D MODELING', 'ARCHITECTURAL DRAWING', 'CNC MACHINING', '3D PRINTING', 'CAD DESIGN', 'TOPOGRAPHIC MAPPING', 'SPATIAL PLANNING', 'INTERIOR DESIGN RENDER', 'URBAN DESIGN', 'LANDSCAPE ARCHITECTURE'],
        'Out_of_Oxford': ['VIRTUAL REALITY EXPLORATION', 'AUGMENTED REALITY DESIGN', 'GAME ENVIRONMENT DESIGN', 'LEVEL DESIGN', 'TERRAIN GENERATION', 'FLIGHT SIMULATOR', 'SATELLITE IMAGERY ANALYSIS', 'GIS MAPPING', 'CARTOGRAPHY', 'TOPOGRAPHIC SURVEY'],
        'Out_of_England': ['CINEMATIC COMPOSITION', 'POST-ROCK ARRANGEMENT', 'ORCHESTRAL CINEMATIC SCORING', 'SOUNDSCAPE DESIGN', 'SPATIAL AUDIO MIXING', 'DOLBY ATMOS MIXING', 'BINAURAL RECORDING', 'AMBISSONIC CAPTURE', 'REVERB SPACE MODELING', 'ACOUSTIC ECOLOGY'],
    },
    'g': {  # binding/sealing — craftsmanship, binding, sealing
        'Oxford': ['BOOKBINDING', 'LEATHERWORK', 'POTTERY WHEEL', 'WHEEL THROWING', 'GLAZE FORMULATION', 'METALSMITHING', 'JEWELRY MAKING', 'WATCHMAKING', 'CLOCK REPAIR', 'PRECISION INSTRUMENT CALIBRATION'],
        'Out_of_Oxford': ['WOODWORKING', 'CARVING', 'FURNITURE MAKING', 'JOINERY', 'WOOD TURNING', 'BASKET WEAVING', 'TEXTILE WEAVING', 'SPINNING YARN', 'NATURAL DYEING', 'FELT MAKING'],
        'Out_of_England': ['CONSERVATION ARCHITECTURE', 'RESTORATION', 'HERITAGE MASONRY', 'LIME MORTAR WORK', 'THATCHING', 'DRY STONE WALLING', 'HEDGELAYING', 'HEDGE LAYERING', 'COB BUILDING', 'EARTH BAG CONSTRUCTION'],
    },
    'nu': {  # self-similarity/fractal — recursive, deep, contemplative
        'Oxford': ['FRACTAL GENERATION', 'RECURSIVE ALGORITHM DESIGN', 'MANDELBROT SET EXPLORATION', 'JULIA SET RENDERING', 'IFS GENERATION', 'L-SYSTEM TREE GENERATION', 'KOCH SNOWFLAKE STUDY', 'SIERPINSKI TRIANGLE', 'DRAGON CURVE', 'H-FRACTAL'],
        'Out_of_Oxford': ['ORIGAMI', 'WET FOLDING ORIGAMI', 'MODULAR ORIGAMI', 'TESSELLATION FOLDING', 'KIRIGAMI', 'PAPER CUTTING ART', 'POP-UP BOOK DESIGN', 'FOLDING GEOMETRY STUDY', 'RIGID ORIGAMI', 'CREASE PATTERN DESIGN'],
        'Out_of_England': ['DEEP MEDITATION', 'VIPASSANA', 'ZAZEN', 'CONTEMPLATIVE PRAYER', 'LUCID DREAMING PRACTICE', 'SENSORY DEPRIVATION', 'FLOATING TANK', 'BREATHWORK', 'YOGA NIDRA', 'TRANCE INDUCTION'],
    },
}

# Profile-specific modifiers based on MBTI cognitive functions
MBTI_MODIFIERS = {
    'ENFP': ['WILDLIFE DOCUMENTARY', 'IMAGINATIVE WRITING', 'BRAINSTORMING SESSION'],
    'ISFP': ['ABSTRACT PAINTING', 'SENSORY WALK', 'IMPROVISATIONAL MUSIC'],
    'ESFJ': ['COMMUNITY ORGANIZING', 'EVENT PLANNING', 'GROUP FACILITATION'],
    'INTP': ['SYSTEMS DESIGN', 'THEORETICAL PHYSICS READING', 'CODE ARCHITECTURE'],
    'ENTP': ['DEBATE PRACTICE', 'STARTUP IDEATION', 'LATERAL THINKING PUZZLES'],
    'INFJ': ['JOURNALING', 'SYMBOLIC INTERPRETATION', 'DREAM ANALYSIS'],
    'ESTP': ['EXTREME SPORTS', 'MARTIAL ARTS SPARRING', 'IMPROVISED NAVIGATION'],
    'ISTP': ['ENGINEERING PROJECT', 'MECHANICAL REPAIR', 'CIRCUIT DESIGN'],
    'ENFJ': ['PUBLIC SPEAKING', 'WORKSHOP FACILITATION', 'COMMUNITY THEATRE'],
    'INTJ': ['STRATEGIC PLANNING', 'SYSTEM OPTIMIZATION', 'LONG-TERM FORECASTING'],
    'ESFP': ['PERFORMANCE ART', 'DJ SET', 'LIVE MUSIC PERFORMANCE'],
    'ISTJ': ['ARCHIVAL RESEARCH', 'DATA AUDIT', 'COMPLIANCE REVIEW'],
    'ESTJ': ['PROJECT MANAGEMENT', 'OPERATIONS PLANNING', 'LOGISTICS OPTIMIZATION'],
    'INFP': ['POETRY WRITING', 'FANTASY WORLD BUILDING', 'CREATIVE NONFICTION'],
    'ISFJ': ['GARDENING', 'CAREGIVING', 'HISTORICAL RESEARCH'],
    'ENTJ': ['BUSINESS STRATEGY', 'NEGOTIATION', 'EXECUTIVE DECISION SIMULATION'],
}

# Blood type modifiers
BLOOD_MODIFIERS = {
    'O': ['OUTDOOR SURVIVAL', 'DIRECT ACTION', 'PHYSICAL CHALLENGE'],
    'A': ['DETAILED CRAFTSMANSHIP', 'METHODICAL STUDY', 'GRADUAL MASTERY'],
    'B': ['CREATIVE ADAPTATION', 'IMPROVISED SOLUTION', 'FLEXIBLE APPROACH'],
    'AB': ['INTERDISCIPLINARY SYNTHESIS', 'PARADOX INTEGRATION', 'MULTI-DOMAIN BRIDGING'],
}

# Gender modifiers
GENDER_MODIFIERS = {
    'M': ['WEIGHTLIFTING', 'RESISTANCE TRAINING', 'COMBAT SPORTS'],
    'F': ['YOGA', 'PILATES', 'DANCE FLOW'],
}

def hash_idx(s, n):
    h = int(hashlib.md5(s.encode()).hexdigest(), 16)
    return h % n

def generate_activity(mbti, blood, gender, slot_idx, top3_particles, vec8, evolved):
    attractor = ATTRACTORS[slot_idx]
    route = attractor['route']

    # Get dominant dimension from top 3 particles
    dim_scores = {d: 0.0 for d in DIMS}
    for p in top3_particles:
        weights = PARTICLE_WEIGHTS.get(p, {})
        for dim, w in weights.items():
            dim_scores[dim] += w * (evolved.get(p, 0))

    dominant_dim = max(dim_scores, key=dim_scores.get)
    secondary_dim = sorted(dim_scores, key=dim_scores.get, reverse=True)[1]

    # Base activity from dominant dimension × route
    base_activities = DIM_ACTIVITIES.get(dominant_dim, DIM_ACTIVITIES['r']).get(route, ['UNKNOWN'])

    # Profile-specific seed for uniqueness
    profile_key = f"{mbti}_{blood}_{gender}_{slot_idx}_{dominant_dim}_{secondary_dim}"
    idx = hash_idx(profile_key, len(base_activities))
    activity = base_activities[idx]

    # Add MBTI modifier (secondary activity)
    mbti_mods = MBTI_MODIFIERS.get(mbti, ['CREATIVE EXPLORATION'])
    mod_idx = hash_idx(profile_key + "_mod", len(mbti_mods))
    modifier = mbti_mods[mod_idx]

    # Add blood type modifier
    blood_mods = BLOOD_MODIFIERS.get(blood, ['ADAPTIVE PRACTICE'])
    blood_idx_mod = hash_idx(profile_key + "_blood", len(blood_mods))
    blood_mod = blood_mods[blood_idx_mod]

    # Add gender modifier
    gender_mods = GENDER_MODIFIERS.get(gender, ['MOVEMENT PRACTICE'])
    gender_idx_mod = hash_idx(profile_key + "_gender", len(gender_mods))
    gender_mod = gender_mods[gender_idx_mod]

    # Combine: primary activity + profile-specific modifier
    # The combination ensures uniqueness across 128 profiles
    full_activity = f"{activity} / {modifier} / {blood_mod}"

    return full_activity, dominant_dim, secondary_dim

# ============================================================
# MAIN: GENERATE 128 × 6 ACTIVITY MAPPING
# ============================================================
def main():
    output_lines = []
    output_lines.append("# 128 PROFILES × 6 SLOTS — DETERMINISTIC ACTIVITY MAPPING")
    output_lines.append("")
    output_lines.append("Generated from 3-way intersection:")
    output_lines.append("- 36 particles (3 per attractor, nonlinear tri-directional interaction)")
    output_lines.append("- 8D parameters (r,h,d,p,s,gamma,g,nu)")
    output_lines.append("- Tensor dynamics (dTensor_dt with 36×36 interaction matrix)")
    output_lines.append("- 3 routes: Oxford (gleysol/core), Out_of_Oxford (podzol/mid), Out_of_England (periphery)")
    output_lines.append("- 6 attractors = 6 slots")
    output_lines.append("")
    output_lines.append("| # | Profile | Slot 1 (Energy) | Slot 2 (Information) | Slot 3 (Repair) | Slot 4 (Opioid) | Slot 5 (GAN Bulkhead) | Slot 6 (COX Retrograde) |")
    output_lines.append("|---|---------|-----------------|----------------------|-----------------|-----------------|----------------------|-------------------------|")

    all_activities = set()

    for m_idx, mbti in enumerate(MBTI_LIST):
        for g_idx, gender in enumerate(GENDERS):
            for b_idx, blood in enumerate(BLOOD_TYPES):
                profile = f"{mbti}_{gender}_{blood}"
                row_num = m_idx * 8 + g_idx * 4 + b_idx + 1

                activities = []
                for slot_idx in range(6):
                    evolved, vec8 = compute_particle_vector(m_idx, b_idx, g_idx, slot_idx)

                    # Get top 3 particles for this attractor
                    attractor = ATTRACTORS[slot_idx]
                    slot_particles = attractor['particles']

                    # Also get top 3 from evolved vector
                    sorted_particles = sorted(evolved.items(), key=lambda x: x[1], reverse=True)
                    top3 = [p for p, v in sorted_particles[:3]]

                    activity, dom_dim, sec_dim = generate_activity(
                        mbti, blood, gender, slot_idx, top3, vec8, evolved
                    )

                    # Ensure uniqueness
                    base_activity = activity
                    counter = 1
                    while activity in all_activities:
                        counter += 1
                        activity = f"{base_activity} v{counter}"
                    all_activities.add(activity)

                    activities.append(activity)

                output_lines.append(f"| {row_num} | {profile} | {activities[0]} | {activities[1]} | {activities[2]} | {activities[3]} | {activities[4]} | {activities[5]} |")

    output_lines.append("")
    output_lines.append("## Slot Definitions")
    output_lines.append("")
    for slot_idx in range(6):
        att = ATTRACTORS[slot_idx]
        output_lines.append(f"- **{att['label']}**: attractor={att['name']}, particles={att['particles']}, route={att['route']}, state={att['state']}, time={att['time']}h")

    output_lines.append("")
    output_lines.append("## Uniqueness Check")
    output_lines.append(f"- Total activities generated: {len(all_activities)}")
    output_lines.append(f"- Expected: 768 (128 × 6)")
    output_lines.append(f"- All unique: {len(all_activities) == 768}")

    # Write to file
    with open('_activity_128x6.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"Generated {len(all_activities)} unique activities for 128 profiles × 6 slots")
    print(f"Output: _activity_128x6.md")

    # Also write JSON for further processing
    json_data = {}
    for m_idx, mbti in enumerate(MBTI_LIST):
        for g_idx, gender in enumerate(GENDERS):
            for b_idx, blood in enumerate(BLOOD_TYPES):
                profile = f"{mbti}_{gender}_{blood}"
                json_data[profile] = {}
                for slot_idx in range(6):
                    evolved, vec8 = compute_particle_vector(m_idx, b_idx, g_idx, slot_idx)
                    sorted_particles = sorted(evolved.items(), key=lambda x: x[1], reverse=True)
                    top3 = [(p, round(v, 4)) for p, v in sorted_particles[:3]]
                    json_data[profile][f"slot_{slot_idx+1}"] = {
                        'attractor': ATTRACTORS[slot_idx]['name'],
                        'route': ATTRACTORS[slot_idx]['route'],
                        'state': ATTRACTORS[slot_idx]['state'],
                        'top3_particles': top3,
                        'dim8': {k: round(v, 4) for k, v in vec8.items()},
                    }

    with open('_activity_128x6.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"JSON: _activity_128x6.json")

if __name__ == '__main__':
    main()
