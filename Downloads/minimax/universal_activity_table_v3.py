"""
universal_activity_table_v3.py — Math-determined activity table.

5 columns (5 energy stages) instead of 14 (too many per day).
Each cell = math function f(8D vector, archetype, stage, blood) — no random,
no pool choice. Activity string is the deterministic output of math formulas.
"""
import csv
import os
import sys
import math
import hashlib

sys.path.insert(0, os.path.dirname(__file__))
import kernel_v1 as k


# ============================================================
# STAGE 5: AB / A / O / B / AB (24h cycle, 5 phases)
# ============================================================
STAGE_5 = ["AB_spark", "A_light", "O_info", "B_binding", "AB_mass"]


# ============================================================
# MBTI 8D vector (math: average of 4 letter dims)
# ============================================================
DIMS_8D = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]
MBTI_LIST = ['ENTJ', 'ENTP', 'ENFJ', 'ENFP',
             'ESTJ', 'ESTP', 'ESFJ', 'ESFP',
             'INTJ', 'INTP', 'INFJ', 'INFP',
             'ISTJ', 'ISTP', 'ISFJ', 'ISFP']

MBTI_LETTER_8D = {
    'E': {'r': 0.85, 'h': 0.5, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.5, 'g': 0.4, 'nu': 0.2},
    'I': {'r': 0.2,  'h': 0.5, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.5, 'g': 0.5, 'nu': 0.85},
    'S': {'r': 0.5,  'h': 0.3, 'd': 0.7, 'p': 0.5, 's': 0.85, 'gamma': 0.3, 'g': 0.55, 'nu': 0.4},
    'N': {'r': 0.5,  'h': 0.7, 'd': 0.3, 'p': 0.5, 's': 0.3, 'gamma': 0.85, 'g': 0.4, 'nu': 0.6},
    'T': {'r': 0.4,  'h': 0.3, 'd': 0.85, 'p': 0.7, 's': 0.5, 'gamma': 0.5, 'g': 0.6, 'nu': 0.4},
    'F': {'r': 0.6,  'h': 0.85, 'd': 0.2, 'p': 0.4, 's': 0.6, 'gamma': 0.5, 'g': 0.4, 'nu': 0.6},
    'J': {'r': 0.5,  'h': 0.5, 'd': 0.6, 'p': 0.85, 's': 0.5, 'gamma': 0.4, 'g': 0.7, 'nu': 0.4},
    'P': {'r': 0.5,  'h': 0.5, 'd': 0.4, 'p': 0.2, 's': 0.5, 'gamma': 0.7, 'g': 0.3, 'nu': 0.6},
}

MBTI_8D = {}
for mbti in MBTI_LIST:
    MBTI_8D[mbti] = {dim: sum(MBTI_LETTER_8D[L][dim] for L in mbti) / 4.0
                      for dim in DIMS_8D}

# Blood 8D (math: defined as inverse of MBTI mean to diversify)
BLOOD_8D = {
    'O':  {'r': 0.7, 'h': 0.3, 'd': 0.6, 'p': 0.4, 's': 0.6, 'gamma': 0.3, 'g': 0.7, 'nu': 0.3},
    'A':  {'r': 0.6, 'h': 0.4, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.4, 'g': 0.6, 'nu': 0.4},
    'B':  {'r': 0.4, 'h': 0.6, 'd': 0.4, 'p': 0.6, 's': 0.4, 'gamma': 0.6, 'g': 0.4, 'nu': 0.6},
    'AB': {'r': 0.5, 'h': 0.5, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.5, 'g': 0.5, 'nu': 0.5},
}


def profile_8d(mbti, blood):
    return {dim: (MBTI_8D[mbti][dim] + BLOOD_8D[blood][dim]) / 2.0 for dim in DIMS_8D}


# ============================================================
# ARCHETYPE (4 cells)
# ============================================================
def archetype(mbti, gender):
    """4 archetype from E/I × W/M (Woman/Man)."""
    ei = "E" if mbti[0] == "E" else "I"
    mf = "W" if gender == "F" else "M"  # W for woman (F), M for man (M)
    return f"{ei}{mf}"  # EW, EM, IW, IM


# ============================================================
# DIM VERB (8 dim → activity verb)  — math-derived, no random
# Each dim has 5 intensity-bin verbs (low, mid-low, mid, mid-high, high)
# ============================================================
DIM_VERB = {
    "r": ["walking", "drumming", "dancing", "running", "rhythmic performance"],
    "h": ["humming", "listening", "singing", "harmonizing", "composing"],
    "d": ["observing", "questioning", "analyzing", "dialecticizing", "axiomatizing"],
    "p": ["pausing", "synchronizing", "timing", "precision-exercising", "calibrating"],
    "s": ["gazing", "sensing", "perceiving", "sensory-fusing", "synesthetizing"],
    "gamma": ["resting", "ascending", "flying", "extreme-aerially-moving", "boundary-breaking"],
    "g": ["floating", "grounding", "weightlifting", "constructing", "monumentalizing"],
    "nu": ["daydreaming", "contemplating", "meditating", "abstract-reasoning", "pure-thinking"],
}


# ============================================================
# INTENSITY BIN  (5 bins from value 0-1)
# ============================================================
def intensity_bin(value):
    if value < 0.2: return 0
    if value < 0.4: return 1
    if value < 0.6: return 2
    if value < 0.8: return 3
    return 4


# ============================================================
# STAGE NOUN  (5 stages)
# ============================================================
STAGE_NOUN = {
    "AB_spark":  "at dawn spark",
    "A_light":   "in morning light",
    "O_info":    "at noon organization",
    "B_binding": "in evening binding",
    "AB_mass":   "at night mass",
}


# ============================================================
# ARCHETYPE OBJECT  (4 cells × 5 stages = 20)
# ============================================================
ARCH_OBJECT = {
    "EW": {"AB_spark": "with group spark", "A_light": "leading people", "O_info": "directing collective", "B_binding": "nurturing team", "AB_mass": "gathering community"},
    "EM": {"AB_spark": "with systems spark", "A_light": "organizing structures", "O_info": "leading institutions", "B_binding": "binding organizations", "AB_mass": "consolidating power"},
    "IW": {"AB_spark": "with inner spark", "A_light": "feeling into values", "O_info": "holding meaning", "B_binding": "deepening care", "AB_mass": "introspective rest"},
    "IM": {"AB_spark": "with idea spark", "A_light": "drafting concepts", "O_info": "modeling systems", "B_binding": "synthesizing", "AB_mass": "deep thinking"},
}


# ============================================================
# BLOOD ADJECTIVE  (4 blood types)
# ============================================================
BLOOD_ADJ = {
    "O":  "with hard physical effort",
    "A":  "with collaborative care",
    "B":  "with adaptive independence",
    "AB": "with universal balance",
}


# ============================================================
# MATH-DETERMINED ACTIVITY  (no pool, no random, no lookup)
# ============================================================
def activity(mbti, blood, gender, stage):
    """
    Activity = math-determined function of profile + stage.
    No pool, no random choice. Pure math formula.

    5 stages = top 5 dims of profile (sorted by 8D value, descending).
    Each profile's day has 5 different dominant activities.
    """
    vec = profile_8d(mbti, blood)              # 8D from math
    sorted_dims = sorted(DIMS_8D, key=lambda d: vec[d], reverse=True)  # top 8 → 8
    stage_idx = STAGE_5.index(stage)            # 0..4
    peak_dim = sorted_dims[stage_idx]           # top 1, 2, 3, 4, 5
    intensity = vec[peak_dim]                   # continuous
    ibin = intensity_bin(intensity)             # 0-4
    arch = archetype(mbti, gender)               # 4 cell

    dim_v = DIM_VERB[peak_dim][ibin]             # verb from dim + intensity
    stage_n = STAGE_NOUN[stage]                  # noun from stage
    arch_o = ARCH_OBJECT[arch][stage]            # object from arch + stage
    blood_a = BLOOD_ADJ[blood]                   # adjective from blood

    return f"{dim_v} {stage_n} {arch_o} {blood_a}"


# ============================================================
# GENERATE TABLE  (128 profiles × 5 stages)
# ============================================================
def generate_table():
    rows = []
    rows.append(['profile'] + STAGE_5)
    for mbti in MBTI_LIST:
        for gender in ['M', 'F']:
            for blood in ['O', 'A', 'B', 'AB']:
                profile = f"{mbti}_{blood}_{gender}"
                row = [profile] + [activity(mbti, blood, gender, st) for st in STAGE_5]
                rows.append(row)
    return rows


# ============================================================
# VERIFY
# ============================================================
def verify():
    # Determinism
    t1 = generate_table()
    t2 = generate_table()
    same = all(r1 == r2 for r1, r2 in zip(t1, t2))
    # Unique activities
    all_activities = []
    for r in t1[1:]:
        all_activities.extend(r[1:])
    unique = set(all_activities)
    print(f"Determinism (same args → same output): {same}")
    print(f"Total cells (128 × 5): {len(all_activities)}")
    print(f"Unique activities: {len(unique)}")
    print(f"Duplicate ratio: {(len(all_activities) - len(unique)) / len(all_activities) * 100:.2f}%")
    print()
    # Sample ENTJ (user complained)
    print("=" * 70)
    print("ENTJ samples (user's complaint):")
    for r in t1[1:]:
        if r[0].startswith("ENTJ_"):
            print(f"  {r[0]}:")
            for st, act in zip(STAGE_5, r[1:]):
                print(f"    {st:12s}: {act}")
    print()
    # Sample INFP
    print("INFP samples:")
    for r in t1[1:]:
        if r[0].startswith("INFP_"):
            print(f"  {r[0]}:")
            for st, act in zip(STAGE_5, r[1:]):
                print(f"    {st:12s}: {act}")
            break
    print()
    # Sample ISTJ
    print("ISTJ samples:")
    for r in t1[1:]:
        if r[0].startswith("ISTJ_"):
            print(f"  {r[0]}:")
            for st, act in zip(STAGE_5, r[1:]):
                print(f"    {st:12s}: {act}")
            break


if __name__ == "__main__":
    verify()
    print()
    table = generate_table()
    out_path = os.path.join(os.path.dirname(__file__), "activity_5stage_math.csv")
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerows(table)
    print(f"Generated {len(table)-1} rows × {len(table[0])} cols → {out_path}")
