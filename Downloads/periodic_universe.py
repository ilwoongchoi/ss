import math

"""Periodic table as a deterministic projection of the 8D x 6-sphere model.

This file is the clean, model-derived element map.  It does NOT contain
empirical constants (mass, spectra, decay half-lives) because those are
measurements produced by history.  What it does contain is the relational
generator: every element's sphere of nucleosynthesis, its 8D color-pigment
channel, its circuit particle, and the logic from which its chemical behavior
(oxidation, reactivity, phase, electron-shell filling order) is derived.
"""

from universe_math_structures import (
    SIX_SPHERES,
    PIGMENT_DIM,
    compute_8d,
    peak_dim,
)
from particle_to_8d import (
    DAY_PARTICLE_COLORS,
    NIGHT_PARTICLE_COLORS,
    SIX_SPHERE_DISTANCES,
)

__all__ = [
    'PERIODIC_118', 'derive_element', 'derive_chemistry',
    'derive_observer_element', 'derive_compound', 'derive_reaction',
]

# ---------------------------------------------------------------------------
# 118 element symbols in atomic-number order
# ---------------------------------------------------------------------------
SYMBOLS = (
    'H','He','Li','Be','B','C','N','O','F','Ne',
    'Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca',
    'Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',
    'Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr',
    'Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn',
    'Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd',
    'Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb',
    'Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg',
    'Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th',
    'Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm',
    'Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds',
    'Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og'
)

# ---------------------------------------------------------------------------
# 6-sphere nucleosynthesis ranges
# ---------------------------------------------------------------------------
SPHERE_RANGES = {
    'sun':     (1, 2),    # Big Bang H/He
    'earth':   (3, 5),    # light species (Li,Be,B)
    'moon':    (6, 10),   # CNO/Ne burning
    'comag':   (11, 20),  # Na-Ca, late stellar burning
    'barnard': (21, 30),  # Fe group, core collapse
    'geomag':  (31, 118), # r/s process, supernova
}

# 8D dimension order used for the z-modulo mapping
DIMS = ('r','h','d','p','s','gamma','g','nu')

# Particle and color names come directly from the existing PIGMENT_DIM map
DIM_PARTICLE = {d: PIGMENT_DIM[d].split('/')[0] for d in PIGMENT_DIM}
DIM_COLOR    = {d: PIGMENT_DIM[d].split('/')[1] for d in PIGMENT_DIM}


def _sphere(z):
    for s, (lo, hi) in SPHERE_RANGES.items():
        if lo <= z <= hi:
            return s
    return 'geomag'


def _dim(z):
    return DIMS[(z - 1) % 8]


def _group(z):
    """Periodic block (s/p/d/f) from atomic number."""
    if 1 <= z <= 2:
        return 's-block'
    if 3 <= z <= 4 or 11 <= z <= 12 or 19 <= z <= 20 or 37 <= z <= 38 or 55 <= z <= 56 or 87 <= z <= 88:
        return 's-block'
    if (5 <= z <= 10) or (13 <= z <= 18) or (31 <= z <= 36) or (49 <= z <= 54) or (81 <= z <= 86) or (113 <= z <= 118):
        return 'p-block'
    if (21 <= z <= 30) or (39 <= z <= 48) or (72 <= z <= 80) or (104 <= z <= 112):
        return 'd-block'
    if (57 <= z <= 71) or (89 <= z <= 103):
        return 'f-block'
    return 'unknown'


def _electron_shells(z):
    """Aufbau subshell filling (s,p,d,f) up to Z=118."""
    subshells = [
        ('1s', 2), ('2s', 2), ('2p', 6), ('3s', 2), ('3p', 6),
        ('4s', 2), ('3d', 10), ('4p', 6), ('5s', 2), ('4d', 10),
        ('5p', 6), ('6s', 2), ('4f', 14), ('5d', 10), ('6p', 6),
        ('7s', 2), ('5f', 14), ('6d', 10), ('7p', 6),
    ]
    filling = {}
    remaining = z
    for name, cap in subshells:
        if remaining <= cap:
            filling[name] = remaining
            break
        filling[name] = cap
        remaining -= cap
    return filling


def _valence(filling):
    """Valence electrons = electrons in the highest principal quantum shell."""
    if not filling:
        return 0
    max_n = max(int(name[0]) for name in filling)
    return sum(v for name, v in filling.items() if int(name[0]) == max_n)


def _chemistry_tendency(group, valence):
    """Oxidation/phase tendency from block and valence count."""
    if group == 's-block':
        return ('donate', 'solid_metal')
    if group == 'd-block':
        return ('variable', 'solid_metal')
    if group == 'f-block':
        return ('variable', 'solid_metal')
    if group == 'p-block':
        if valence <= 3:
            return ('donate', 'metalloid')
        if valence >= 6:
            return ('accept', 'nonmetal_gas_liquid')
        return ('amphoteric', 'nonmetal_solid')
    return ('unknown', 'unknown')


def _physics_tendency(group, d):
    """Electromagnetic/thermal/optical tendency from block and 8D color."""
    if group in ('d-block', 'f-block'):
        return 'conductor', 'ferromagnetic_paramagnetic', 'thermal_conductor'
    if group == 's-block':
        return 'conductor', 'paramagnetic', 'thermal_conductor'
    if group == 'p-block':
        if d in ('r', 's'):
            return 'insulator', 'diamagnetic', 'thermal_insulator'
        if d in ('p', 'nu'):
            return 'semiconductor', 'diamagnetic', 'variable_thermal'
        return 'semiconductor', 'paramagnetic', 'moderate_thermal'
    return 'unknown', 'unknown', 'unknown'


SPHERE_TITLE = {
    'sun': 'Sun', 'earth': 'Earth', 'moon': 'Moon',
    'comag': 'CoMag', 'barnard': 'Barnard', 'geomag': 'Geomagnetic',
}


def derive_element(z, mbti=None, gender=None, blood=None, t_hours=None):
    """Return the complete model-derived description of element z (1-118)."""
    if not 1 <= z <= 118:
        return None
    d = _dim(z)
    sphere = _sphere(z)
    sphere_info = SIX_SPHERES[sphere]
    particle = DIM_PARTICLE[d]
    day_info = DAY_PARTICLE_COLORS.get(particle, {})
    night_info = NIGHT_PARTICLE_COLORS.get(particle, {})
    heliosphere = SIX_SPHERE_DISTANCES.get(SPHERE_TITLE.get(sphere))
    return {
        'z': z,
        'symbol': SYMBOLS[z - 1],
        'sphere': sphere,
        'sphere_core_color': sphere_info['color'],
        'sphere_attractor': sphere_info.get('attractor'),
        'stellar_stage': sphere_info.get('stage'),
        'nucleosynthesis_process': sphere_info.get('process'),
        'astronomical_distance': heliosphere.get('distance') if heliosphere else None,
        'time_slot': heliosphere.get('time') if heliosphere else None,
        'celestial_brain': heliosphere.get('brain_celestial') if heliosphere else None,
        '8d_dimension': d,
        'particle': particle,
        'color_channel': DIM_COLOR[d],
        'day_color': day_info.get('color'),
        'day_hex': day_info.get('hex'),
        'night_color': night_info.get('color'),
        'night_hex': night_info.get('hex'),
        'group_block': _group(z),
        'electron_shells': _electron_shells(z),
    }


def derive_chemistry(z, mbti=None, gender=None, blood=None, t_hours=None):
    """Return chemistry as a circuit projection: oxidation, reactivity, phase.

    The element's chemical character is not memorized; it is derived from
    the same 8D vector that governs the observer, the peak particle, and
    the active blood route at the given time.
    """
    if not 1 <= z <= 118:
        return None
    out = derive_element(z, mbti, gender, blood, t_hours)
    filling = out['electron_shells']
    valence = _valence(filling)
    ox, phase = _chemistry_tendency(out['group_block'], valence)
    conductivity, magnetism, thermal = _physics_tendency(out['group_block'], out['8d_dimension'])
    out['valence_electrons'] = valence
    out['oxidation_tendency'] = ox
    out['phase_tendency'] = phase
    out['conductivity_tendency'] = conductivity
    out['magnetic_tendency'] = magnetism
    out['thermal_tendency'] = thermal
    if mbti and gender and blood:
        v_8d = compute_8d(mbti, gender, blood)
        out['observer_8d'] = v_8d
        out['resonant_dim'] = out['8d_dimension']
        out['resonant_value'] = v_8d.get(out['8d_dimension'], 0.5)
    return out


def derive_observer_element(mbti, gender, blood, t_hours):
    """Return the element that is resonant with the observer's peak dimension.

    Each time slot maps one of the 8D dimensions to a seed element (1-8).
    This links the observer's present peak to its corresponding element.
    """
    active_dim = peak_dim(t_hours)
    z = DIMS.index(active_dim) + 1
    return derive_chemistry(z, mbti, gender, blood, t_hours)


def _charge_from_chemistry(chem):
    """Derive a formal ionic charge from the element's chemical tendency."""
    ox = chem.get('oxidation_tendency')
    v = chem.get('valence_electrons', 1)
    if ox == 'donate':
        return +v
    if ox == 'accept':
        return -(8 - v)
    # amphoteric/variable/metals default to cationic valence for formula
    return +v


def _is_metal(chem):
    return chem.get('phase_tendency') == 'solid_metal' and chem.get('symbol') != 'H'


def _bond_type(a, b):
    """Predict bond type from two element chemistry dictionaries."""
    m1, m2 = _is_metal(a), _is_metal(b)
    if m1 and m2:
        return 'metallic'
    if m1 or m2:
        return 'ionic'
    ox1, ox2 = a['oxidation_tendency'], b['oxidation_tendency']
    if ox1 == 'accept' and ox2 == 'accept':
        return 'covalent_network'
    if (ox1 in ('donate', 'amphoteric') and ox2 == 'accept') or \
       (ox2 in ('donate', 'amphoteric') and ox1 == 'accept'):
        return 'covalent_polar'
    return 'covalent'


def derive_compound(z1, z2, mbti=None, gender=None, blood=None, t_hours=None):
    """Return a model-derived binary compound between elements z1 and z2."""
    for z in (z1, z2):
        if not 1 <= z <= 118:
            return None
    a = derive_chemistry(z1, mbti, gender, blood, t_hours)
    b = derive_chemistry(z2, mbti, gender, blood, t_hours)
    bond = _bond_type(a, b)
    c1 = _charge_from_chemistry(a)
    c2 = _charge_from_chemistry(b)
    # swap so cation is first
    if c1 < 0 and c2 > 0:
        a, b = b, a
        c1, c2 = c2, c1
        z1, z2 = z2, z1
    if bond == 'metallic':
        formula = f"{a['symbol']}_{b['symbol']}"
    else:
        g = math.gcd(abs(c1) if c1 else 1, abs(c2) if c2 else 1)
        n1 = abs(c2) // g if c2 else 1
        n2 = abs(c1) // g if c1 else 1
        s1 = '' if n1 == 1 else str(n1)
        s2 = '' if n2 == 1 else str(n2)
        formula = f"{a['symbol']}{s1}{b['symbol']}{s2}"
    return {
        'cation': a['symbol'], 'anion': b['symbol'],
        'bond_type': bond,
        'formula': formula,
        'charge_balance': (c1 * abs(c2) // math.gcd(abs(c1) if c1 else 1, abs(c2) if c2 else 1)
                           + c2 * abs(c1) // math.gcd(abs(c1) if c1 else 1, abs(c2) if c2 else 1)) == 0
        if c1 and c2 else True,
        'elements': [a, b],
    }


def derive_reaction(z1, z2, mbti=None, gender=None, blood=None, t_hours=None):
    """Return a synthesis reaction between two elements as the next layer."""
    compound = derive_compound(z1, z2, mbti, gender, blood, t_hours)
    if compound is None:
        return None
    e1, e2 = compound['elements'][0], compound['elements'][1]
    equation = f"{e1['symbol']} + {e2['symbol']} -> {compound['formula']}"
    spontaneous = compound['bond_type'] in ('ionic', 'covalent_polar', 'metallic')
    return {
        'reactants': [e1['z'], e2['z']],
        'products': [compound['formula']],
        'reaction_type': 'synthesis',
        'equation': equation,
        'spontaneous': spontaneous,
        'compound': compound,
    }


# ---------------------------------------------------------------------------
# Precomputed lookup table for 118 elements
# ---------------------------------------------------------------------------
PERIODIC_118 = [derive_element(z) for z in range(1, 119)]


if __name__ == '__main__':
    import json
    print(json.dumps(PERIODIC_118[:10], ensure_ascii=False, indent=2))
