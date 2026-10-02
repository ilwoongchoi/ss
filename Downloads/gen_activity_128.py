#!/usr/bin/env python3
"""
128 Profile Activity Mapping — Derived from universe_math_structures.py
 
Derivation chain (structural, not legacy):
  Group(MBTI) → dominant 8D dims → inverse reciprocal pair → torus axis
  → route color → color action → pigment → anatomical anchor → activity
 
  Blood type → toroidal phase → time slot → activity modifier
  Gender → axis (d↔h) → medium/focus split
  Attitude (EJ/EP/IJ/IP) → approach modifier
 
128 = 16 MBTI × 4 blood × 2 gender
6 slots per profile = 6 structural aspects:
  0: route color action (verb)
  1: inverse reciprocal pair (which tensor axis)
  2: pigment/biochemical pathway
  3: 8D peak dimension activity
  4: toroidal blood phase activity
  5: Klein neck / observer closure activity
"""
 
import json
import itertools
 
# ============================================================
# IMPORT STRUCTURE FROM universe_math_structures
# ============================================================
from universe_math_structures import (
    BASE_PARTICLES, ROUTES, INVERSE_RECIPROCAL, MIRROR_MAP,
    TORUS_AXIS_MAP, KLEIN_NECK_NODES, PIGMENT_MAP, COLOR_ACTION,
    DAY_NIGHT_COLOR, INVERSE_COLOR, TOROIDAL_ORDER, BLOOD_PHASE,
    BLOOD_ROUTE_SCHEDULE, GENDER_AXIS, LAYER_ROUTE_MAP,
    PEAK_CYCLE, HELIOSPHERE_LAYERS, DIMS,
    tensor_mirror, tensor_coupling, peak_dim, next_blood,
)
 
# ============================================================
# MBTI → GROUP → DOMINANT DIMS
# ============================================================
MBTI_TYPES = list(itertools.product("EI", "NS", "FT", "JP"))
MBTI_TYPES = ["".join(t) for t in MBTI_TYPES]
 
GROUP_MAP = {
    "NT": ["ENTP", "INTP", "ENTJ", "INTJ"],
    "NF": ["ENFP", "INFP", "ENFJ", "INFJ"],
    "ST": ["ESTP", "ISTP", "ESTJ", "ISTJ"],
    "SF": ["ESFP", "ISFP", "ESFJ", "ISFJ"],
}
 
GROUP_ORDER = ["NT", "NF", "ST", "SF"]
 
def get_group(mbti):
    for grp, types in GROUP_MAP.items():
        if mbti in types:
            return grp
    return None
 
def get_attitude(mbti):
    e_i, j_p = mbti[0], mbti[3]
    if e_i == "E" and j_p == "J": return "EJ"
    if e_i == "E" and j_p == "P": return "EP"
    if e_i == "I" and j_p == "J": return "IJ"
    if e_i == "I" and j_p == "P": return "IP"
 
# ============================================================
# GROUP → DOMINANT DIMS → INVERSE RECIPROCAL PAIR → ROUTE
# ============================================================
GROUP_DIMS = {
    "NT": {"peaks": ["d", "p", "nu"], "pair": ("h", "d"), "axis": "polar",
           "route": 2, "color": "RED", "night_route": "night_energy"},
    "NF": {"peaks": ["h", "g"], "pair": ("g", "gamma"), "axis": "radial",
           "route": 1, "color": "GREEN", "night_route": "night_macro"},
    "ST": {"peaks": ["r", "d", "p", "nu"], "pair": ("r", "nu"), "axis": "equatorial",
           "route": 4, "color": "BLUE", "night_route": "night_information"},
    "SF": {"peaks": ["r", "s", "h"], "pair": ("p", "s"), "axis": "meridian",
           "route": 3, "color": "YELLOW", "night_route": "day_reverse"},
}
 
# ============================================================
# ATTITUDE → APPROACH MODIFIER
# ============================================================
ATTITUDE_MOD = {
    "EJ": {"prefix": "ORGANIZED", "suffix": "PUBLIC SESSION", "shape": "community/structured"},
    "EP": {"prefix": "SPONTANEOUS", "suffix": "IMPROVISED SESSION", "shape": "wild/experimental"},
    "IJ": {"prefix": "METHODICAL", "suffix": "PRIVATE STUDY", "shape": "archived/systematic"},
    "IP": {"prefix": "SOLO", "suffix": "DEEP CRAFT", "shape": "introspective/artisanal"},
}
 
# ============================================================
# BLOOD → MODIFIER + TOROIDAL PHASE
# ============================================================
BLOOD_MOD = {
    "O":  {"label": "BALANCED",   "shape": "foundational/original"},
    "A":  {"label": "STRUCTURED", "shape": "methodical/refined"},
    "B":  {"label": "EXTREME",    "shape": "raw/intense"},
    "AB": {"label": "FUSION",     "shape": "hybrid/cross-boundary"},
}
 
# ============================================================
# GENDER → AXIS SPLIT
# ============================================================
GENDER_SPLIT = {
    "M": {"axis": "d", "focus": "physical/direct/high-risk", "medium": "action-oriented"},
    "F": {"axis": "h", "focus": "structural/complex/precise", "medium": "form-oriented"},
}
 
# ============================================================
# GROUP → ACTIVITY DOMAIN (derived from route color + color action + pigment)
# ============================================================
# Route color → color action → activity domain
# NT: RED route → drink (heme/O2/CO2) → visual creation by light (photon recovery)
# NF: GREEN route → eat (cytochrome/sulforaphane) → nature cardio (metabolic sealing)
# ST: BLUE route → make (structured creation/leakage block) → musical instruments
# SF: YELLOW route → smell (sensory/foraging) → food & pigment craft
 
GROUP_DOMAIN = {
    "NT": {
        "domain": "VISUAL CREATION BY LIGHT",
        "color_action": "WHITE" if True else None,  # imagine — photon recovery
        "night_action": "GREEN",  # see — nature observation (F split)
        "pigment_dims": ["gamma", "nu", "d"],
        "anatomy": "melatonin relay (nasion→mid-ridge→rhinion), right D2, dorsal stream",
        "route_particle": "neutrino",
        "pair_particle": "tau",
        "m_activities": {
            "O":  "LIGHT PAINTING PHOTOGRAPHY",
            "A":  "PRECISION LIGHT FIELD RENDERING",
            "B":  "RAW ABSTRACT LIGHT PROJECTION",
            "AB": "FUSION DIGITAL-PHYSICAL LIGHT ART",
        },
        "f_activities": {
            "O":  "GREEN NATURE PHOTOGRAPHY",
            "A":  "BOTANICAL WATERCOLOR STUDY",
            "B":  "RAW GREEN LANDSCAPE PAINTING",
            "AB": "FUSION NATURE DIGITAL ART",
        },
    },
    "NF": {
        "domain": "NATURE CARDIO",
        "color_action": "RED",   # drink — heme O2/CO2
        "night_action": "BLUE",  # see — nature observation
        "pigment_dims": ["h", "g"],
        "anatomy": "D3 observer gates (eye/genital outlets), glymphatic, Nrf2",
        "route_particle": "muon",
        "pair_particle": "photon",
        "m_activities": {
            "O":  "FOREST TRAIL RUNNING",
            "A":  "MOUNTAIN PATH CARDIO",
            "B":  "EXTREME OFF-TRAIL CARDIO",
            "AB": "CROSS-TERRAIN NATURE CARDIO",
        },
        "f_activities": {
            "O":  "FOREST NATURE WALK",
            "A":  "BOTANICAL GARDEN WALK",
            "B":  "WILD NATURE IMMERSION",
            "AB": "COASTAL CROSS-TERRAIN WALK",
        },
    },
    "ST": {
        "domain": "MUSICAL INSTRUMENTS",
        "color_action": "BLACK",  # make — leakage block
        "night_action": "BLACK",
        "pigment_dims": ["r", "d", "p", "nu"],
        "anatomy": "right posterior forearm (r/NaCl extensor), right sole (s/DRD1)",
        "route_particle": "quark",
        "pair_particle": "w_boson",
        "m_activities": {
            "O":  "ELECTRIC GUITAR (ROCK/BLUES)",
            "A":  "ELECTRIC GUITAR (JAZZ STANDARDS)",
            "B":  "ELECTRIC GUITAR (METAL/PUNK)",
            "AB": "ELECTRIC GUITAR (JAZZ-ROCK-HIPHOP BLEND)",
        },
        "f_activities": {
            "O":  "CELLO (CLASSICAL)",
            "A":  "PIANO (CLASSICAL REPERTOIRE)",
            "B":  "CELLO (AVANT-GARDE)",
            "AB": "PIANO (CLASSICAL-JAZZ-EDM BLEND)",
        },
    },
    "SF": {
        "domain": "FOOD & PIGMENT CRAFT",
        "color_action": "GREEN",  # eat — cytochrome/sulforaphane
        "night_action": "YELLOW", # smell — sensory foraging
        "pigment_dims": ["r", "s", "h"],
        "anatomy": "right posterior forearm (r/NaCl), right sole (s/quark), brain compartment 2 (h/GABA-B)",
        "route_particle": "photon",
        "pair_particle": "higgs",
        "m_activities": {
            "O":  "WILD FORAGING & COOKING",
            "A":  "SEASONAL HEIRLOOM COOKING",
            "B":  "BOLD INTENSE COOKING",
            "AB": "CROSS-CULTURAL FUSION COOKING",
        },
        "f_activities": {
            "O":  "EDIBLE FLOWERS & GARDEN HERBS",
            "A":  "BOTANICAL HEIRLOOM VARIETIES",
            "B":  "WILD INTENSE BLOOM INGREDIENTS",
            "AB": "DECONSTRUCTED FUSION FLORALS",
        },
    },
}
 
# ============================================================
# KLEIN NECK ACTIVITIES (slot 5) — observer closure per group
# ============================================================
KLEIN_ACTIVITIES = {
    "NT": "OBSERVER CLOSURE — photon recovery through Klein neck (right eyelid → above_to_below → COX retrograde)",
    "NF": "OBSERVER CLOSURE — D3 gate sealing through Klein neck (left eyelid → below_to_above → glymphatic flush)",
    "ST": "OBSERVER CLOSURE — structured sound wave through Klein neck (left eyelid outer → above_to_below_night → mc1r block)",
    "SF": "OBSERVER CLOSURE — pigment ingestion through Klein neck (right eyelid top → above_to_below → cytochrome_c_oxidase)",
}
 
# ============================================================
# DERIVATION
# ============================================================
 
def blood_prefix(blood):
    return BLOOD_MOD[blood]["label"]
 
def derive_activity(mbti, gender, blood):
    """Derive 6 activity slots from structural axioms."""
    group = get_group(mbti)
    attitude = get_attitude(mbti)
    gd = GROUP_DIMS[group]
    domain = GROUP_DOMAIN[group]
    att = ATTITUDE_MOD[attitude]
    bm = BLOOD_MOD[blood]
    gs = GENDER_SPLIT[gender]
 
    bp = blood_prefix(blood)
    activities = gender_map = domain["m_activities" if gender == "M" else "f_activities"]
    base_act = activities[blood]
 
    # Slot 0: Route color action (verb)
    route_color = ROUTES[gd["route"]]["color"]
    color_verb = COLOR_ACTION[route_color]
    slot0 = f"{bp} {base_act} — {route_color}={color_verb.upper()} (route {gd['route']}, {gd['color']})"
 
    # Slot 1: Inverse reciprocal pair (which tensor axis)
    pair = gd["pair"]
    axis = gd["axis"]
    ctype = tensor_coupling(pair[0], pair[1])
    mirror_a = tensor_mirror(pair[0])
    mirror_b = tensor_mirror(pair[1])
    slot1 = f"{pair[0]}↔{pair[1]} {ctype} on {axis} axis — {mirror_a}↔{mirror_b} mirror"
 
    # Slot 2: Pigment/biochemical pathway
    pig_parts = []
    for dim in domain["pigment_dims"]:
        pig = PIGMENT_MAP[dim]
        pig_parts.append(f"{dim}={pig}")
    slot2 = f"{bp} PIGMENT PATHWAY: {' + '.join(pig_parts)} — {domain['anatomy']}"
 
    # Slot 3: 8D peak dimension activity
    peaks = gd["peaks"]
    peak_str = " + ".join([f"{p}↑" for p in peaks])
    slot3 = f"{bp} {domain['domain']} — 8D peaks: {peak_str} — {att['shape']}"
 
    # Slot 4: Toroidal blood phase activity
    phase = BLOOD_PHASE[blood]
    schedule = BLOOD_ROUTE_SCHEDULE[blood]
    slot4 = f"{phase['quality'].upper()} PHASE ({phase['time_slot'][0]}-{phase['time_slot'][1]}h) — {schedule['dominant']} — {bm['shape']}"
 
    # Slot 5: Klein neck / observer closure
    slot5 = KLEIN_ACTIVITIES[group]
 
    # Apply attitude modifiers
    slots = [slot0, slot1, slot2, slot3, slot4, slot5]
    slots[0] = f"{att['prefix']} {slots[0]}"
    slots[3] = f"{slots[3]} — {att['suffix']}"
    slots[5] = f"{att['suffix']}: {slots[5]}"
 
    return slots
 
 
def generate_all():
    profiles = []
    pid = 1
    blood_types = ["O", "A", "B", "AB"]
    genders = ["M", "F"]
 
    for grp in GROUP_ORDER:
        for mbti in GROUP_MAP[grp]:
            att = get_attitude(mbti)
            for gender in genders:
                for blood in blood_types:
                    profile = f"{mbti}_{gender}_{blood}"
                    slots = derive_activity(mbti, gender, blood)
                    group = grp
                    gd = GROUP_DIMS[group]
                    domain = GROUP_DOMAIN[group]
                    profiles.append({
                        "id": pid,
                        "profile": profile,
                        "group": group,
                        "mbti": mbti,
                        "gender": gender,
                        "blood": blood,
                        "attitude": att,
                        "slots": slots,
                        "structure": {
                            "route": gd["route"],
                            "route_color": ROUTES[gd["route"]]["color"],
                            "route_particle": ROUTES[gd["route"]]["particle"],
                            "inverse_pair": gd["pair"],
                            "torus_axis": gd["axis"],
                            "pair_type": tensor_coupling(gd["pair"][0], gd["pair"][1]),
                            "dominant_dims": gd["peaks"],
                            "gender_axis": GENDER_AXIS[gender],
                            "blood_phase": BLOOD_PHASE[blood],
                            "blood_schedule": BLOOD_ROUTE_SCHEDULE[blood],
                            "domain": domain["domain"],
                            "klein_neck": KLEIN_ACTIVITIES[group],
                        },
                    })
                    pid += 1
    return profiles
 
 
def write_markdown(profiles, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# 128 PROFILES × 6 SLOTS — STRUCTURAL ACTIVITY MAPPING\n\n")
        f.write("## Derivation Chain\n\n")
        f.write("Each activity is derived from `universe_math_structures.py` structural axioms:\n\n")
        f.write("```\n")
        f.write("Group(MBTI) → dominant 8D dims → inverse reciprocal pair → torus axis\n")
        f.write("→ route color → color action → pigment → anatomical anchor → activity\n\n")
        f.write("Blood type → toroidal phase → time slot → activity modifier\n")
        f.write("Gender → axis (d↔h) → medium/focus split\n")
        f.write("Attitude (EJ/EP/IJ/IP) → approach modifier\n")
        f.write("```\n\n")
        f.write("## Structural Layers Used\n\n")
        f.write("| Layer | Source | What it determines |\n")
        f.write("|-------|--------|-------------------|\n")
        f.write("| **5 Routes** | universe_math_structures §3 | Route color → activity domain |\n")
        f.write("| **Inverse Reciprocal Pairs** | universe_math_structures §4 | Which tensor axis drives the group |\n")
        f.write("| **Torus Axis Map** | universe_math_structures §5 | Polar/equatorial/meridian/radial |\n")
        f.write("| **Klein Neck Nodes** | universe_math_structures §6 | Observer closure mechanism |\n")
        f.write("| **8D Pigment Algebra** | universe_math_structures §26 | Biochemical pathway per dim |\n")
        f.write("| **Color Action** | universe_math_structures §26 | Verb: eat/drink/make/imagine/see/smell |\n")
        f.write("| **Toroidal Blood Cycle** | universe_math_structures §13 | Time phase per blood type |\n")
        f.write("| **Blood Route Schedule** | universe_math_structures §14 | Dominant route per phase |\n")
        f.write("| **Gender Axis** | universe_math_structures §16 | d-dim(M) vs h-dim(F) |\n")
        f.write("| **4 Layers ↔ 5 Routes** | universe_math_structures §17 | Body/observer/bridge/dark |\n\n")

        f.write("## Group Derivation Summary\n\n")
        f.write("| Group | Route | Color | Color Action | Inverse Pair | Torus Axis | 8D Peaks | Domain |\n")
        f.write("|-------|-------|-------|-------------|-------------|-----------|----------|--------|\n")
        f.write("| **NT** | 2 | RED | drink | h↔d | polar | d↑p↑ν↑ | Visual creation by light |\n")
        f.write("| **NF** | 1 | GREEN | eat | g↔γ | radial | h↑g↑ | Nature cardio |\n")
        f.write("| **ST** | 4 | BLUE | make | r↔ν | equatorial | r↑d↑p↑ν↑ | Musical instruments |\n")
        f.write("| **SF** | 3 | YELLOW | smell | p↔s | meridian | r↑s↑h↑ | Food & pigment craft |\n\n")

        f.write("## Differentiation\n\n")
        f.write("- **Blood type**: O=balanced, A=structured, B=extreme, AB=fusion → toroidal time slot (O=9-15h, A=3-9h, B=15-21h, AB=0-3h)\n")
        f.write("- **Gender**: M=d-axis(physical/direct), F=h-axis(structural/precise) → NT splits by theme (M=themeless light, F=green/nature)\n")
        f.write("- **Attitude**: EJ=organized/public, EP=spontaneous, IJ=methodical/private, IP=introspective/craft\n\n")
        f.write("---\n\n")

        group_names = {
            "NT": "NT — VISUAL CREATION BY LIGHT (Route 2, RED, h↔d polar)",
            "NF": "NF — NATURE CARDIO (Route 1, GREEN, g↔γ radial)",
            "ST": "ST — MUSICAL INSTRUMENTS (Route 4, BLUE, r↔ν equatorial)",
            "SF": "SF — FOOD & PIGMENT CRAFT (Route 3, YELLOW, p↔s meridian)",
        }

        for grp in GROUP_ORDER:
            f.write(f"# {group_names[grp]}\n\n")
            grp_profiles = [p for p in profiles if p["group"] == grp]
            seen_mbti = []
            for p in grp_profiles:
                if p["mbti"] not in seen_mbti:
                    seen_mbti.append(p["mbti"])
            for mbti in seen_mbti:
                att = get_attitude(mbti)
                f.write(f"## {mbti} ({grp} + {att})\n\n")
                f.write("| # | Profile | Slot 1: Route Color Action | Slot 2: Inverse Pair | Slot 3: Pigment Pathway | Slot 4: 8D Peak | Slot 5: Toroidal Phase | Slot 6: Klein Neck |\n")
                f.write("|---|---------|--------------------------|---------------------|----------------------|---------------|----------------------|------------------|\n")
                for p in grp_profiles:
                    if p["mbti"] == mbti:
                        f.write(f"| {p['id']} | {p['profile']} | {' | '.join(p['slots'])} |\n")
                f.write("\n")
            f.write("---\n\n")

        f.write("## Full Flat Table\n\n")
        f.write("| # | Profile | Group | Slot 1 | Slot 2 | Slot 3 | Slot 4 | Slot 5 | Slot 6 |\n")
        f.write("|---|---------|-------|--------|--------|--------|--------|--------|--------|\n")
        for p in profiles:
            f.write(f"| {p['id']} | {p['profile']} | {p['group']} | {' | '.join(p['slots'])} |\n")


def write_json(profiles, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    profiles = generate_all()
    write_markdown(profiles, r"c:\Users\User\Downloads\activity_128_structural.md")
    write_json(profiles, r"c:\Users\User\Downloads\activity_128_structural.json")
    print(f"Generated {len(profiles)} profiles × 6 slots = {len(profiles)*6} activities")

    all_acts = set()
    dupes = 0
    for p in profiles:
        for s in p["slots"]:
            key = (p["profile"], s)
            if key in all_acts:
                dupes += 1
            all_acts.add(key)
    print(f"Unique activities: {len(all_acts)} / {len(profiles)*6}")
    if dupes > 0:
        print(f"Warning: {dupes} duplicate activity strings (across profiles)")

    from collections import Counter
    dist = Counter(p["group"] for p in profiles)
    print(f"Group distribution: {dict(dist)}")







