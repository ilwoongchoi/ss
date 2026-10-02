"""
Personality Delta Table
=======================
16 MBTI × 2 Gender × 4 Blood = 128 profiles
Each profile = delta from ENTP_M_O anchor

Delta logic:
- MBTI: affects specific 8D dimensions based on cognitive functions
- Gender: affects polarity (female = energy/phantom, male = creation/mass)
- Blood: affects complexity and growth direction
"""

import itertools

# ============================================================
# MBTI DELTA (from ENTP anchor)
# ============================================================
# ENTP = Ne-Ti-Fe-Si = maximum divergence + logical structure
# Each MBTI type is a delta from this baseline

MBTI_DELTAS = {
    'ENTP': {  # ANCHOR - no delta
        'r': 0.00, 'h': 0.00, 'd': 0.00, 'p': 0.00,
        's': 0.00, 'gamma': 0.00, 'g': 0.00, 'nu': 0.00,
    },
    'INTP': {  # Ne-Ti but introverted → less r, more nu
        'r': -0.10, 'h': 0.00, 'd': 0.05, 'p': 0.05,
        's': -0.05, 'gamma': -0.05, 'g': 0.00, 'nu': 0.10,
    },
    'ENTJ': {  # Te-Ni → more structure, less divergence
        'r': 0.05, 'h': -0.05, 'd': 0.00, 'p': 0.15,
        's': 0.05, 'gamma': 0.05, 'g': 0.05, 'nu': -0.10,
    },
    'INTJ': {  # Ni-Te → deep structure, introverted
        'r': -0.05, 'h': -0.05, 'd': 0.05, 'p': 0.20,
        's': -0.05, 'gamma': 0.00, 'g': 0.05, 'nu': 0.05,
    },
    'ENFP': {  # Ne-Fi → divergence + emotion → more h, less structure
        'r': 0.00, 'h': 0.10, 'd': -0.05, 'p': -0.05,
        's': 0.05, 'gamma': 0.05, 'g': 0.05, 'nu': 0.00,
    },
    'INFP': {  # Fi-Ne → deep emotion, introverted
        'r': -0.15, 'h': 0.15, 'd': -0.10, 'p': -0.05,
        's': -0.10, 'gamma': -0.10, 'g': 0.05, 'nu': 0.05,
    },
    'ENFJ': {  # Fe-Ni → social harmony, structure
        'r': 0.05, 'h': 0.10, 'd': -0.05, 'p': 0.10,
        's': 0.00, 'gamma': 0.05, 'g': 0.10, 'nu': -0.05,
    },
    'INFJ': {  # Ni-Fe → deep harmony, introverted
        'r': -0.10, 'h': 0.10, 'd': 0.00, 'p': 0.10,
        's': -0.10, 'gamma': -0.05, 'g': 0.10, 'nu': 0.05,
    },
    'ESTP': {  # Se-Ti → action, present moment
        'r': 0.15, 'h': -0.10, 'd': 0.10, 'p': -0.15,
        's': 0.10, 'gamma': 0.10, 'g': -0.05, 'nu': -0.10,
    },
    'ISTP': {  # Ti-Se → analytical action, introverted
        'r': 0.00, 'h': -0.10, 'd': 0.10, 'p': -0.05,
        's': 0.00, 'gamma': 0.00, 'g': -0.05, 'nu': 0.05,
    },
    'ESTJ': {  # Te-Si → maximum structure, tradition
        'r': 0.10, 'h': -0.05, 'd': 0.05, 'p': 0.25,
        's': 0.05, 'gamma': 0.00, 'g': 0.10, 'nu': 0.10,
    },
    'ISTJ': {  # Si-Te → internal structure, introverted
        'r': -0.05, 'h': -0.05, 'd': 0.05, 'p': 0.25,
        's': -0.05, 'gamma': -0.05, 'g': 0.05, 'nu': 0.10,
    },
    'ESFP': {  # Se-Fi → sensory enjoyment, present
        'r': 0.15, 'h': 0.05, 'd': -0.05, 'p': -0.15,
        's': 0.15, 'gamma': 0.10, 'g': 0.00, 'nu': -0.10,
    },
    'ISFP': {  # Fi-Se → aesthetic, introverted
        'r': -0.10, 'h': 0.10, 'd': -0.05, 'p': -0.10,
        's': 0.05, 'gamma': -0.05, 'g': 0.00, 'nu': 0.00,
    },
    'ESFJ': {  # Fe-Si → social tradition, harmony
        'r': 0.05, 'h': 0.05, 'd': -0.05, 'p': 0.15,
        's': 0.05, 'gamma': 0.00, 'g': 0.15, 'nu': 0.05,
    },
    'ISFJ': {  # Si-Fe → protective tradition, introverted
        'r': -0.10, 'h': 0.05, 'd': -0.05, 'p': 0.15,
        's': -0.05, 'gamma': -0.05, 'g': 0.10, 'nu': 0.05,
    },
}

# ============================================================
# GENDER DELTA
# ============================================================
# Female = energy/phantom polarity (GABA-A phasic, cold, horizontal)
# Male = creation/mass polarity (GABA-A tonic, mass-lock, discrete)
#
# From universe-prose.md:23
# "female GABA-A는 phasic/냉감/수평선형 억제,
#  male GABA-A는 tonic/mass-lock/단절적 억제"

GENDER_DELTAS = {
    'M': {  # Male = creation mode
        'r': 0.03, 'h': -0.03, 'd': 0.05, 'p': 0.00,
        's': 0.03, 'gamma': 0.03, 'g': -0.03, 'nu': 0.03,
    },
    'F': {  # Female = energy/phantom mode
        'r': -0.03, 'h': 0.03, 'd': -0.05, 'p': 0.00,
        's': -0.03, 'gamma': -0.03, 'g': 0.03, 'nu': -0.03,
    },
}

# ============================================================
# BLOOD TYPE DELTA
# ============================================================
# O = archetype (complexity 1) = original pattern
# A = structured (complexity 2) = organized
# B = experimental (complexity 3) = divergent
# AB = hybrid (complexity 4) = maximum complexity
#
# Growth rule: release=own blood | stress=blood+1 | extreme=opposite temperament

BLOOD_DELTAS = {
    'O': {  # archetype = baseline
        'r': 0.00, 'h': 0.00, 'd': 0.00, 'p': 0.00,
        's': 0.00, 'gamma': 0.00, 'g': 0.00, 'nu': 0.00,
    },
    'A': {  # structured = more p, more g, less d
        'r': 0.00, 'h': 0.03, 'd': -0.05, 'p': 0.08,
        's': -0.03, 'gamma': -0.03, 'g': 0.05, 'nu': 0.03,
    },
    'B': {  # experimental = more d, more s, less p
        'r': 0.03, 'h': -0.03, 'd': 0.08, 'p': -0.08,
        's': 0.05, 'gamma': 0.05, 'g': -0.03, 'nu': -0.03,
    },
    'AB': {  # hybrid = maximum complexity, all dimensions stretched
        'r': 0.02, 'h': 0.05, 'd': 0.05, 'p': -0.03,
        's': 0.03, 'gamma': 0.05, 'g': 0.02, 'nu': 0.05,
    },
}

# ============================================================
# SLOT ROUTING RULES
# ============================================================
# Given final 8D, determine which slots are active/blocked
# and what state (forward/reverse/spark) they're in

SLOT_RULES = {
    'electron_hole': {
        'description': 'Composition / Production / Sexual energy',
        'circuit_node': 'heme → steel → COX forward/reverse',
        'activate_when': {
            's': '>= 0.5',       # needs brightness to produce
            'gamma': '>= 0.5',   # needs spatial expansion to create
        },
        'state_rules': {
            'forward':  's >= 0.5 and d <= 0.4',   # bright + harmonious = production
            'reverse':  's >= 0.5 and d > 0.4',    # bright + dissonant = destructive production
            'spark':    's < 0.5 and gamma >= 0.6', # dim but expansive = creative spark
        },
    },
    'mitochondria': {
        'description': 'Listening / Consumption / ATP metabolism',
        'circuit_node': 'COX → ATP → energy processing',
        'activate_when': {
            # Always active (listening is always possible unless blocked)
        },
        'state_rules': {
            'forward':  'r >= 0.5 and d <= 0.4',   # fast + harmonious = active listening
            'reverse':  'd > 0.5',                  # dissonant = deconstructive listening
            'spark':    'r < 0.4 and h >= 0.5',     # slow + harmonic = deep listening
        },
    },
    'gaba_c': {
        'description': 'Music generation / Pattern creation / Sealing',
        'circuit_node': 'clay_gouge → water_vapour → g-dim',
        'activate_when': {
            'gamma': '>= 0.4',   # needs some spatial capacity
            'p': '<= 0.5',       # needs some unpredictability
        },
        'state_rules': {
            'forward':  'g >= 0.5 and p <= 0.3',   # sealed + unpredictable = generative
            'reverse':  'g < 0.3 and nu >= 0.5',   # unsealed + fractal = deconstructive gen
            'spark':    'nu < 0.4 and r >= 0.5',    # low fractal + tempo = spark generation
        },
    },
    'bilirubin': {
        'description': 'Competition / Extreme growth / Spatial art',
        'circuit_node': 'fold_belt → gamma-dim',
        'activate_when': {
            'gamma': '>= 0.3',   # needs some spatial capacity
        },
        'state_rules': {
            'forward':  'gamma >= 0.6 and p >= 0.4',  # expansive + structured = growth
            'reverse':  'gamma >= 0.6 and p < 0.4',   # expansive + unstructured = extreme growth
            'spark':    'gamma < 0.4 and d >= 0.5',   # compressed + dissonant = competitive spark
        },
    },
    'pancreas': {
        'description': 'Material production / Digestion / Craft',
        'circuit_node': 'CCK → digestion → material formation',
        'activate_when': {
            # Always active (material processing is constant)
        },
        'state_rules': {
            'forward':  'r >= 0.4 and h >= 0.4',   # structured = material production
            'reverse':  's >= 0.5 and gamma >= 0.5', # expansive = transparent material
            'spark':    'd >= 0.5 and p < 0.3',     # dissonant + unpredictable = material spark
        },
    },
}

# ============================================================
# ACTIVITY GENERATION RULES
# ============================================================
# Given slot + state + 8D, generate activity description
# This replaces manual 640-entry mapping with rule-based generation

ACTIVITY_TEMPLATES = {
    'electron_hole': {
        'forward': {
            'high_r_high_s': 'bright rhythmic music production',
            'high_h_low_d':  'warm harmonic composition',
            'default':       'music composition and production',
        },
        'reverse': {
            'high_r_high_d': 'aggressive sound production / noise art',
            'high_gamma':    'spatial sound art / immersive production',
            'default':       'reverse-phase creative production',
        },
        'spark': {
            'high_nu':       'fractal pattern composition',
            'high_gamma':    'expansive creative spark production',
            'default':       'spark-based creative generation',
        },
    },
    'mitochondria': {
        'forward': {
            'high_r':        'fast-paced music listening / active consumption',
            'high_h':        'deep harmonic listening / analytical listening',
            'default':       'music listening and consumption',
        },
        'reverse': {
            'high_d':        'deconstructive listening / noise archive art',
            'high_r':        'rapid media processing / archive deconstruction',
            'default':       'reverse-phase listening / media deconstruction',
        },
        'spark': {
            'high_h_low_r':  'deep slow listening / meditative consumption',
            'default':       'spark-based listening',
        },
    },
    'gaba_c': {
        'forward': {
            'high_g':        'sealed pattern generation / structured composition',
            'high_nu':       'fractal music generation / self-similar pattern',
            'default':       'music pattern generation',
        },
        'reverse': {
            'low_g_high_nu': 'deconstructive pattern generation / unsealed creation',
            'default':       'reverse-phase music generation',
        },
        'spark': {
            'high_r_low_nu': 'rhythmic spark generation / beat creation',
            'default':       'spark-based music generation',
        },
    },
    'bilirubin': {
        'forward': {
            'high_gamma':    'spatial art / expansive creative growth',
            'default':       'extreme growth activity',
        },
        'reverse': {
            'high_gamma':    'spatial diffusion art / immersive installation',
            'default':       'reverse-phase spatial art',
        },
        'spark': {
            'high_d':        'competitive spark / physical challenge',
            'default':       'spark-based competitive activity',
        },
    },
    'pancreas': {
        'forward': {
            'high_r_high_h': 'material craft / structured production',
            'default':       'material production and crafting',
        },
        'reverse': {
            'high_s':        'transparent material art / optical / glass art',
            'default':       'reverse-phase material art',
        },
        'spark': {
            'high_d':        'material spark / experimental craft',
            'default':       'spark-based material creation',
        },
    },
}

# ============================================================
# GENERATE ALL 128 PROFILES
# ============================================================

MBTI_LIST = list(MBTI_DELTAS.keys())
GENDERS = ['M', 'F']
BLOODS = ['O', 'A', 'B', 'AB']

def generate_profile_id(mbti, gender, blood):
    return f"{mbti}_{gender}_{blood}"

def generate_all_profile_ids():
    profiles = []
    for mbti in MBTI_LIST:
        for gender in GENDERS:
            for blood in BLOODS:
                profiles.append(generate_profile_id(mbti, gender, blood))
    return profiles

# Default haplogroup mapping (can be overridden)
# In practice, each profile can have any haplogroup
# This is a default assignment based on population frequency
DEFAULT_HAPLOGROUP = 'DEFAULT'  # User specifies per-profile
