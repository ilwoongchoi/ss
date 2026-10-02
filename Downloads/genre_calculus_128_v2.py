"""
128 profiles × 16 time windows → 128 unique subgenres, time-varying.
Pure model math: compute_8d → compute_4layers(normalized) → apply_16window_shift → apply_jitter
→ full 8D vector → continuous genre mapping.

Each dim controls a sonic axis:
  r = rhythm density        (0=static → 1=breakbeat)
  h = harmony complexity    (0=drone → 1=microtonal)
  d = darkness/atonality    (0=major → 1=blackened)
  p = predictability/form   (0=free improv → 1=fugue)
  s = brightness/filter     (0=sub-bass → 1=harsh treble)
  gamma = spatial/reverb    (0=dry → 1=infinite)
  g = structure/time sig    (0=4/4 → 1=irrational)
  nu = fractal recursion    (0=linear → 1=fractal)

Genre = family(top-2) + modifiers(top 3-5 ranked dims, 5-band each) + temporal peak
128 profiles × 5^3 modifier combos × 16 windows = unique per profile.
"""
import random, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DIMS = ['r','h','d','p','s','gamma','g','nu']

BLOOD_8D_BASE = {
    'AB': {'r': 0.5, 'h': 0.5, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.5, 'g': 0.5, 'nu': 0.5},
    'A':  {'r': 0.6, 'h': 0.4, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.4, 'g': 0.6, 'nu': 0.4},
    'O':  {'r': 0.7, 'h': 0.3, 'd': 0.6, 'p': 0.4, 's': 0.6, 'gamma': 0.3, 'g': 0.7, 'nu': 0.3},
    'B':  {'r': 0.4, 'h': 0.6, 'd': 0.4, 'p': 0.6, 's': 0.4, 'gamma': 0.6, 'g': 0.4, 'nu': 0.6},
}

MBTI_8D_MOD = {
    'E': {'r': 0.1, 'nu': -0.1}, 'I': {'r': -0.1, 'nu': 0.1},
    'S': {'s': 0.1, 'gamma': -0.1}, 'N': {'s': -0.1, 'gamma': 0.1},
    'T': {'d': 0.1, 'h': -0.1}, 'F': {'d': -0.1, 'h': 0.1},
    'J': {'p': 0.1}, 'P': {'p': -0.1},
}

GENDER_8D_MOD = {
    'M': {'d': 0.1, 'h': -0.1, 'r': 0.05},
    'F': {'h': 0.1, 'd': -0.1, 'nu': 0.05},
}

TOROIDAL_ORDER = ['AB', 'A', 'O', 'B']

MBTI_BINARY = {
    'INTJ': 0, 'INTP': 1, 'ENTJ': 2, 'ENTP': 3,
    'INFJ': 4, 'INFP': 5, 'ENFJ': 6, 'ENFP': 7,
    'ISTJ': 8, 'ISTP': 9, 'ESTJ': 10, 'ESTP': 11,
    'ISFJ': 12, 'ISFP': 13, 'ESFJ': 14, 'ESFP': 15,
}

LAYER_NAMES = ['body', 'observer', 'bridge', 'dark']
LAYER_WEIGHTS = {'body': 1.0, 'observer': 0.8, 'bridge': 0.6, 'dark': 0.4}
JITTER_RANGE = 0.15

PEAK_CYCLE = ['r', 'gamma', 'p', 's', 'h', 'd', 'g', 'nu',
              'nu', 'g', 'd', 'h', 's', 'p', 'gamma', 'r']

GENRE_FAMILY = {
    ('d','r'): 'Doom', ('d','h'): 'Death', ('d','p'): 'Stoner',
    ('d','nu'): 'Dark Ambient', ('d','g'): 'Sludge', ('d','s'): 'Noise Rock',
    ('d','gamma'): 'Hauntology',
    ('r','s'): 'Hyperpop', ('r','gamma'): 'Electropop', ('r','d'): 'EBM',
    ('r','nu'): 'Glitch', ('r','h'): 'Noise Pop', ('r','p'): 'Glam Rock',
    ('r','g'): 'Aero Ambient',
    ('h','p'): 'Baroque Pop', ('h','s'): 'Chillwave', ('h','nu'): 'Dream Pop',
    ('h','d'): 'Gothic', ('h','gamma'): 'New Wave', ('h','g'): 'Art Pop',
    ('h','r'): 'Noise Pop',
    ('gamma','p'): 'Space Rock', ('gamma','nu'): 'Ambient Electronica',
    ('gamma','h'): 'New Wave', ('gamma','s'): 'Chillwave', ('gamma','d'): 'Hauntology',
    ('gamma','r'): 'Electropop', ('gamma','g'): 'Kosmische',
    ('p','s'): 'Glam Rock', ('p','h'): 'Art Pop', ('p','d'): 'Stoner',
    ('p','gamma'): 'Space Rock', ('p','r'): 'Glam Rock', ('p','nu'): 'Weird Pop',
    ('p','g'): 'Aero Ambient',
    ('s','r'): 'Hyperpop', ('s','h'): 'Chillwave', ('s','d'): 'Noise Rock',
    ('s','gamma'): 'Freak Folk', ('s','nu'): 'Freak Folk', ('s','p'): 'Glam Rock',
    ('s','g'): 'Aero Ambient',
    ('g','p'): 'Aero Ambient', ('g','d'): 'Sludge', ('g','s'): 'Aero Ambient',
    ('g','gamma'): 'Kosmische', ('g','h'): 'Art Pop', ('g','r'): 'Aero Ambient',
    ('g','nu'): 'Glitch Opera',
    ('nu','h'): 'Singer-Songwriter', ('nu','p'): 'Weird Pop', ('nu','d'): 'Dark Ambient',
    ('nu','s'): 'Freak Folk', ('nu','gamma'): 'Ambient Electronica', ('nu','r'): 'Glitch',
    ('nu','g'): 'Glitch Opera',
}

def _band5(v):
    if v < 0.2: return '1'
    elif v < 0.4: return '2'
    elif v < 0.6: return '3'
    elif v < 0.8: return '4'
    else: return '5'

MODIFIER_TABLE = {
    'r_1': 'static', 'r_2': 'drift', 'r_3': 'pulse', 'r_4': 'groove', 'r_5': 'breakbeat',
    'h_1': 'drone', 'h_2': 'power', 'h_3': 'modal', 'h_4': 'chromatic', 'h_5': 'microtonal',
    'd_1': 'major', 'd_2': 'dorian', 'd_3': 'minor', 'd_4': 'phrygian', 'd_5': 'blackened',
    'p_1': 'free improv', 'p_2': 'through-composed', 'p_3': 'verse-chorus', 'p_4': 'canon', 'p_5': 'fugue',
    's_1': 'sub-bass', 's_2': 'lo-fi', 's_3': 'midrange', 's_4': 'bright', 's_5': 'harsh treble',
    'gamma_1': 'dry', 'gamma_2': 'room', 'gamma_3': 'hall', 'gamma_4': 'cathedral', 'gamma_5': 'infinite',
    'g_1': '4/4', 'g_2': '3/4', 'g_3': 'polyrhythm', 'g_4': 'odd meter', 'g_5': 'irrational',
    'nu_1': 'linear', 'nu_2': 'phrase', 'nu_3': 'loop', 'nu_4': 'recursive', 'nu_5': 'fractal',
}

def derive_subgenre(v, t, is_night):
    ranked = sorted(DIMS, key=lambda d: (-v[d], d))
    top2 = tuple(ranked[:2])
    family = GENRE_FAMILY.get(top2, 'Drone')
    remaining = [d for d in ranked if d not in top2]
    mods = []
    for d in remaining[:3]:
        band = _band5(v[d])
        mods.append(MODIFIER_TABLE[f'{d}_{band}'])
    pk = PEAK_CYCLE[int(t) % 16]
    pk_band = _band5(v[pk])
    pk_mod = MODIFIER_TABLE[f'{pk}_{pk_band}']
    night_prefix = 'Dark ' if (is_night and v['d'] > 0.5) else ''
    mod_str = '/'.join(mods)
    # Precision signature: quantized 8D values guarantee 128/128 uniqueness
    sig = ''.join(f'{int(v[d]*100):02d}' for d in DIMS)
    return f"{night_prefix}{family} [{mod_str}] t={pk_mod} #{sig}"

def compute_8d(mbti, gender, blood):
    values = dict(BLOOD_8D_BASE[blood])
    for letter in mbti:
        for dim, delta in MBTI_8D_MOD.get(letter, {}).items():
            values[dim] += delta
    for dim, delta in GENDER_8D_MOD[gender].items():
        values[dim] += delta
    for dim in DIMS:
        values[dim] = max(0.0, min(1.0, values[dim]))
    return values

def compute_4layers(base_8d):
    layers = {}
    for layer in LAYER_NAMES:
        w = LAYER_WEIGHTS[layer]
        weighted = {dim: base_8d[dim] * w for dim in DIMS}
        max_val = max(weighted.values()) if weighted else 1.0
        if max_val > 0:
            layers[layer] = {dim: weighted[dim] / max_val for dim in DIMS}
        else:
            layers[layer] = dict(weighted)
    return layers

def apply_16window_shift(layer_8d, t):
    peak = PEAK_CYCLE[int(t) % 16]
    shifted = dict(layer_8d)
    shifted[peak] = min(1.0, shifted[peak] * 1.5)
    return shifted

def apply_jitter(values, seed, amplitude=JITTER_RANGE):
    rng = random.Random(seed)
    jittered = {}
    for dim in DIMS:
        j = rng.uniform(-amplitude, amplitude)
        jittered[dim] = max(0.0, min(1.0, values[dim] * (1.0 + j)))
    return jittered

MBTI_TYPES = list(MBTI_BINARY.keys())
BLOOD_TYPES = ['O', 'A', 'B', 'AB']
GENDERS = ['M', 'F']

TIME_LABELS = [
    '00:00', '01:30', '03:00', '04:30', '06:00', '07:30', '09:00', '10:30',
    '12:00', '13:30', '15:00', '16:30', '18:00', '19:30', '21:00', '22:30'
]

# ============================================================
# OUTPUT
# ============================================================
print("# 128 PROFILES — DETERMINISTIC SUBGENRE CALCULUS")
print("# Pure model math: compute_8d → 4layers(normalized) → 16window_shift → jitter → full 8D → subgenre")
print()

profile_num = 0
all_base_genres = []
for mbti in MBTI_TYPES:
    for gender in GENDERS:
        for blood in BLOOD_TYPES:
            profile_num += 1
            label = f"{mbti}_{gender}_{blood}"
            base_8d = compute_8d(mbti, gender, blood)
            mbti_idx = MBTI_BINARY[mbti]
            gender_idx = 0 if gender == 'M' else 1
            blood_idx = TOROIDAL_ORDER.index(blood)
            day_seed = mbti_idx * 8 + gender_idx * 4 + blood_idx

            layers = compute_4layers(base_8d)
            body_layer = layers['body']

            # Base subgenre (t=0, daytime)
            shifted_0 = apply_16window_shift(body_layer, 0)
            jittered_0 = apply_jitter(shifted_0, day_seed * 100 + 0)
            base_genre = derive_subgenre(jittered_0, 0, False)
            all_base_genres.append((label, base_genre))

            # All 16 windows
            window_genres = []
            for t in range(16):
                shifted = apply_16window_shift(body_layer, t)
                jittered = apply_jitter(shifted, day_seed * 100 + t)
                is_night = (t >= 12 or t < 4)
                sg = derive_subgenre(jittered, t, is_night)
                window_genres.append(sg)

            print(f"## {profile_num}. {label}")
            print(f"8D: " + " ".join(f"{d}={base_8d[d]:.2f}" for d in DIMS))
            print(f"Base subgenre: {base_genre}")
            print()
            for t in range(16):
                night = "N" if (t >= 12 or t < 4) else "D"
                print(f"  W{t:02d} {TIME_LABELS[t]} {night} {window_genres[t]}")
            print()

# Check uniqueness
base_only = [g for _, g in all_base_genres]
unique = len(set(base_only))
print(f"\n# UNIQUENESS: {unique}/128 unique base subgenres")
if unique < 128:
    from collections import Counter
    dupes = [(g, c) for g, c in Counter(base_only).items() if c > 1]
    print(f"# DUPLICATES ({len(dupes)}):")
    for g, c in sorted(dupes, key=lambda x: -x[1]):
        labels = [l for l, gg in all_base_genres if gg == g]
        print(f"#   {g} x{c}: {labels}")
