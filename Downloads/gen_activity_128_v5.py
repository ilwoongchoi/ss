#!/usr/bin/env python3
"""Generate 128-profile × 6-slot activity mapping based on leakage-resolution framework.

SF = food/pigment (block STRESS leakage from quarks+peonidine)
NT = visual creation by light (night energy leakage between sexes)
  - M: themeless pure creation, differentiated by medium/specificity only
  - F: imagine/portray green or nature
ST = musical instruments (darcy leakage from water)
NF = nature cardio (self-harm risk)
"""

import json

# 16 MBTI types × 2 genders × 4 blood types = 128
MBTI_TYPES = [
    "ENTP","INTP","ENTJ","INTJ",  # NT
    "ENFP","INFP","ENFJ","INFJ",  # NF
    "ESTP","ISTP","ESTJ","ISTJ",  # ST
    "ESFP","ISFP","ESFJ","ISFJ",  # SF
]
GENDERS = ["M","F"]
BLOODS = ["O","A","B","AB"]

# Group classification
def get_group(mbti):
    mid = mbti[1:3]
    if mid in ("NF",): return "NF"
    if mid in ("NT",): return "NT"
    if mid in ("SF",): return "SF"
    if mid in ("ST",): return "ST"

# Attitude
def get_attitude(mbti):
    ends = mbti[0] + mbti[3]
    if ends == "EJ": return "EJ"
    if ends == "EP": return "EP"
    if ends == "IJ": return "IJ"
    if ends == "IP": return "IP"

# Blood modifier
BLOOD_MOD = {
    "O":  {"intensity": "balanced",     "style": "foundational"},
    "A":  {"intensity": "structured",   "style": "methodical"},
    "B":  {"intensity": "extreme",      "style": "improvisational"},
    "AB": {"intensity": "hybrid",       "style": "interdisciplinary"},
}

# Gender modifier
GENDER_MOD = {
    "M": {"focus": "physical",   "energy": "high-risk"},
    "F": {"focus": "structural", "energy": "complex"},
}

# Attitude modifier
ATTITUDE_MOD = {
    "EJ": {"approach": "organized",       "setting": "public"},
    "EP": {"approach": "improvisational", "setting": "spontaneous"},
    "IJ": {"approach": "methodical",      "setting": "private"},
    "IP": {"approach": "exploratory",     "setting": "introspective"},
}

# ============================================================
# SF GROUP — Food & Pigment Activities
# ============================================================
SF_ACTIVITIES = {
    # attitude -> [slot1, slot2, slot3, slot4, slot5, slot6]
    # Each is a template; blood/gender modifies the descriptor
    "EP": [  # Spontaneous food/pigment exploration
        ("IMPROVISED COOKING WITH {ingr}", "PIGMENT EXTRACTION FROM {source}", "FERMENTATION EXPERIMENT ({adj})", "{foraging} FORAGING WALK", "EXTREME TASTING MENU DESIGN", "{craft} CRAFT"),
        ("VIBRANT {dish} WITH EDIBLE FLOWERS", "NATURAL FOOD COLORING CRAFT", "YOGURT FERMENTATION", "KITCHEN HERB GARDEN TENDING", "ARTISANAL JAM & PRESERVE MAKING", "FLOWER SYRUP CRAFT"),  # F template
    ],
    "IP": [  # Introspective food/pigment craft
        ("SLOW COOKING WITH {ingr}", "EARTH PIGMENT GRINDING & PAINTING", "SOURDOUGH STARTER MAINTENANCE", "SOLO FORAGING HIKE", "ARTISANAL CHARCUTERIE CRAFT", "WILD MUSHROOM PREPARATION"),
        ("AESTHETIC PLATING WITH EDIBLE FLOWERS", "BOTANICAL DYE FOR FOOD", "SLOW JAM MAKING", "FLOWER GARDEN CULTIVATION", "ARTISANAL ICE CREAM CRAFT", "HERBAL TEA BLENDING"),
    ],
    "EJ": [  # Organized food/pigment events
        ("COMMUNITY COOKING EVENT WITH {ingr}", "PIGMENT WORKSHOP FOR GROUP", "ORGANIZED FERMENTATION PARTY", "GROUP FORAGING WALK", "LARGE-SCALE TASTING EVENT ORGANIZATION", "COMMUNITY FEAST PREPARATION"),
        ("COMMUNITY BAKING GATHERING", "EDIBLE FLOWER ARRANGEMENT WORKSHOP", "ORGANIZED PRESERVE-MAKING SESSION", "COMMUNITY HERB GARDEN PROJECT", "HIGH-TEA EVENT ORGANIZATION", "SEASONAL FOOD CELEBRATION PLANNING"),
    ],
    "IJ": [  # Methodical food/pigment preservation
        ("TRADITIONAL RECIPE PRESERVATION & COOKING", "HISTORICAL PIGMENT RESEARCH & REPLICATION", "METHODICAL FERMENTATION (SAUERKRAUT)", "HOME GARDEN HARVEST & COOKING", "HEIRLOOM RECIPE RESTORATION", "SEASONAL PRESERVATION CYCLE"),
        ("SEASONAL JAM & PRESERVE MAKING", "BOTANICAL DYE RESEARCH & APPLICATION", "TRADITIONAL PICKLING (FAMILY RECIPE)", "HERB DRYING & STORAGE CRAFT", "HEIRLOOM DESSERT RECREATION", "FLOWER SYRUP & CORDIAL CRAFT"),
    ],
}

SF_BLOOD_INGR = {
    "O": "WILD INGREDIENTS",
    "A": "SEASONAL INGREDIENTS",
    "B": "BOLD INGREDIENTS",
    "AB": "FUSION INGREDIENTS",
}
SF_BLOOD_SOURCE = {
    "O": "WILD BERRIES",
    "A": "BOTANICAL SOURCES",
    "B": "CHILI PEPPERS",
    "AB": "MULTI-SOURCE",
}
SF_BLOOD_ADJ = {
    "O": "SPONTANEOUS",
    "A": "METHODICAL",
    "B": "WILD",
    "AB": "CROSS-CULTURAL",
}
SF_BLOOD_FORAGE = {
    "O": "TRAIL",
    "A": "GARDEN",
    "B": "URBAN EDGE",
    "AB": "ETHNIC MARKET",
}
SF_BLOOD_CRAFT = {
    "O": "WILD HERB PESTO",
    "A": "ARTISANAL BREAD",
    "B": "SMOKED MEAT",
    "AB": "CROSS-CULTURAL FERMENT",
}
SF_BLOOD_DISH = {
    "O": "SALAD",
    "A": "TART",
    "B": "STREET FOOD",
    "AB": "DECONSTRUCTED CUISINE",
}

def gen_sf(profile, gender, blood, attitude):
    templates = SF_ACTIVITIES[attitude]
    g_idx = 0 if gender == "M" else 1
    slots = templates[g_idx]
    ingr = SF_BLOOD_INGR[blood]
    source = SF_BLOOD_SOURCE[blood]
    adj = SF_BLOOD_ADJ[blood]
    forage = SF_BLOOD_FORAGE[blood]
    craft = SF_BLOOD_CRAFT[blood]
    dish = SF_BLOOD_DISH[blood]
    result = []
    for s in slots:
        result.append(s.format(ingr=ingr, source=source, adj=adj, foraging=forage, craft=craft, dish=dish))
    return result

# ============================================================
# NT GROUP — Visual Creation by Light
# ============================================================
NT_ACTIVITIES_M = {  # Men: themeless pure creation, medium-specific
    "EP": [
        "ABSTRACT LIGHT PAINTING PHOTOGRAPHY", "EXPERIMENTAL VIDEO PROJECTION ART", "SPONTANEOUS DIGITAL ART (NO THEME)",
        "LIGHT BOX SCULPTURE PROTOTYPE", "EXTREME LIGHT INSTALLATION (LARGE-SCALE)", "HOLOGRAPHIC PROJECTION EXPERIMENT",
    ],
    "IP": [
        "SOLO ABSTRACT DIGITAL PAINTING (THEMELESS)", "LIGHT RAY TRACING ART", "FRACTAL VISUALIZATION (NO SUBJECT)",
        "CODE-BASED GENERATIVE ART", "DEEP PARAMETRIC COMPOSITION", "ALGORITHMIC LIGHT ART",
    ],
    "EJ": [
        "LARGE-SCALE LIGHT INSTALLATION (PUBLIC)", "ABSTRACT VIDEO ART PRODUCTION", "ORGANIZED DIGITAL ART EXHIBITION",
        "LIGHT SCULPTURE COMMISSION", "MONUMENTAL PROJECTION MAPPING", "PUBLIC LIGHT ART COMMISSION",
    ],
    "IJ": [
        "SYSTEMATIC ABSTRACT ART SERIES (THEMELESS)", "PRECISION LIGHT FIELD RENDERING", "METHODICAL DIGITAL COMPOSITION STUDY",
        "ALGORITHMIC ART GENERATION SYSTEM", "HIGH-DETAIL PARAMETRIC ART SERIES", "LONG-TERM DIGITAL ART ARCHITECTURE",
    ],
}

NT_ACTIVITIES_F = {  # Women: imagine/portray green or nature
    "EP": [
        "GREEN NATURE PHOTOGRAPHY (VIVID)", "BOTANICAL ILLUSTRATION (DIGITAL)", "IMAGINED GREEN LANDSCAPE PAINTING",
        "NATURE WALK PHOTOGRAPHY", "VIBRANT GREEN COMPOSITION ART", "FLORAL LIGHT PAINTING",
    ],
    "IP": [
        "SOLO GREEN NATURE PAINTING (TRADITIONAL)", "BOTANICAL WATERCOLOR STUDY", "IMAGINED ECOSYSTEM ILLUSTRATION",
        "NATURE OBSERVATION SKETCHING", "DETAILED LEAF STRUCTURE ART", "FOREST CANOPY VISUAL STUDY",
    ],
    "EJ": [
        "ORGANIZED GREEN NATURE EXHIBITION", "BOTANICAL ART SHOW CURATION", "PUBLIC NATURE MURAL PROJECT",
        "COMMUNITY GARDEN VISUAL DESIGN", "LARGE-SCALE NATURE INSTALLATION", "ENVIRONMENTAL ART COMMISSION",
    ],
    "IJ": [
        "SYSTEMATIC BOTANICAL ART SERIES (GREEN)", "PRECISION NATURE ILLUSTRATION STUDY", "METHODICAL GREEN COMPOSITION ARCHIVE",
        "ALGORITHMIC NATURE ART SYSTEM", "FINE BOTANICAL ART COLLECTION", "LONG-TERM NATURE VISUAL ARCHITECTURE",
    ],
}

NT_BLOOD_PREFIX = {
    "O": "",
    "A": "STRUCTURED ",
    "B": "RAW ",
    "AB": "FUSION ",
}

def gen_nt(profile, gender, blood, attitude):
    if gender == "M":
        base = NT_ACTIVITIES_M[attitude]
    else:
        base = NT_ACTIVITIES_F[attitude]
    prefix = NT_BLOOD_PREFIX[blood]
    # Apply blood modifier as prefix to first 3 slots (core activities)
    result = []
    for i, s in enumerate(base):
        if i < 3 and prefix:
            # Don't double-prefix if already starts with modifier
            if not s.startswith(prefix.strip()):
                result.append(prefix + s)
            else:
                result.append(s)
        else:
            result.append(s)
    return result

# ============================================================
# ST GROUP — Musical Instrument Activities
# ============================================================
ST_ACTIVITIES_M = {  # Men: guitar, drums, DJ, beats
    "EP": [
        "IMPROVISED ELECTRIC GUITAR SOLO ({genre})", "LIVE DRUM SAMPLING BEAT MAKING", "SPONTANEOUS DJ SET ({genre})",
        "IMPROMPTU JAM SESSION", "EXTREME LIVE GUITAR PERFORMANCE", "ON-THE-SPOT BEAT PRODUCTION",
    ],
    "IP": [
        "SOLO GUITAR EXPLORATION ({genre})", "MODULAR SYNTH PATCH DESIGN", "PRIVATE BEAT MAKING ({genre})",
        "LUTHIER WORK (GUITAR SETUP)", "DEEP GUITAR TONE CRAFT", "ANALOG SYNTH CALIBRATION",
    ],
    "EJ": [
        "ORGANIZED BAND REHEARSAL ({genre})", "STRUCTURED DRUM SAMPLING SESSION", "DJ SET PLANNING & EXECUTION ({genre})",
        "MUSIC PRODUCTION PROJECT MANAGEMENT", "LARGE-SCALE LIVE PERFORMANCE ORGANIZATION", "STUDIO RECORDING SESSION",
    ],
    "IJ": [
        "SYSTEMATIC GUITAR PRACTICE ({genre})", "METHODICAL DRUM SAMPLING ARCHIVE", "STRUCTURED DJ MIX LIBRARY ({genre})",
        "MUSIC THEORY STUDY (HARMONY/COUNTERPOINT)", "FINE GUITAR REPERTOIRE BUILDING", "LONG-TERM MUSIC COLLECTION ARCHIVING",
    ],
}

ST_ACTIVITIES_F = {  # Women: cello, piano, DJ, synths
    "EP": [
        "IMPROVISED CELLO PERFORMANCE ({genre})", "LIVE PIANO IMPROVISATION ({genre})", "SPONTANEOUS DJ SET ({genre})",
        "IMPROMPTU CHAMBER MUSIC JAM", "EXTREME CELLO PERFORMANCE (SOLO)", "ON-THE-SPOT PIANO COMPOSITION",
    ],
    "IP": [
        "SOLO CELLO EXPLORATION ({genre})", "PRIVATE PIANO IMPROVISATION ({genre})", "MODULAR SYNTH EXPLORATION (AMBIENT)",
        "INSTRUMENT MAINTENANCE & TUNING", "DEEP CELLO TONE CRAFT", "PIANO TECHNIQUE STUDY",
    ],
    "EJ": [
        "ORGANIZED ORCHESTRA REHEARSAL ({genre})", "STRUCTURED PIANO RECITAL PREPARATION", "DJ SET PLANNING ({genre})",
        "CHAMBER MUSIC PROJECT MANAGEMENT", "LARGE-SCALE RECITAL ORGANIZATION", "STUDIO RECORDING ({genre})",
    ],
    "IJ": [
        "SYSTEMATIC CELLO PRACTICE ({genre})", "METHODICAL PIANO STUDY (REPERTOIRE)", "STRUCTURED DJ MIX LIBRARY ({genre})",
        "MUSIC THEORY STUDY (CLASSICAL HARMONY)", "FINE CELLO REPERTOIRE BUILDING", "LONG-TERM CLASSICAL MUSIC ARCHIVING",
    ],
}

ST_BLOOD_GENRE_M = {
    "O": "ROCK/BLUES",
    "A": "JAZZ STANDARDS",
    "B": "METAL/PUNK",
    "AB": "JAZZ-ROCK-HIPHOP BLEND",
}
ST_BLOOD_GENRE_F = {
    "O": "CLASSICAL",
    "A": "CLASSICAL REPERTOIRE",
    "B": "AVANT-GARDE",
    "AB": "CLASSICAL-JAZZ-EDM BLEND",
}

def gen_st(profile, gender, blood, attitude):
    if gender == "M":
        base = ST_ACTIVITIES_M[attitude]
        genre = ST_BLOOD_GENRE_M[blood]
    else:
        base = ST_ACTIVITIES_F[attitude]
        genre = ST_BLOOD_GENRE_F[blood]
    result = [s.format(genre=genre) for s in base]
    return result

# ============================================================
# NF GROUP — Nature Cardio Activities
# ============================================================
NF_ACTIVITIES_M = {  # Men: trail running, conservation, cardio in nature
    "EP": [
        "TRAIL RUNNING (FOREST, SPONTANEOUS ROUTE)", "CONSERVATION VOLUNTEERING (OUTDOOR)", "IMPROMPTU OUTDOOR CARDIO SESSION",
        "WILDLIFE TRAIL EXPLORATION", "EXTREME TRAIL RUNNING CHALLENGE", "OUTDOOR SURVIVAL CARDIO",
    ],
    "IP": [
        "SOLO TRAIL RUNNING (FOREST, INTROSPECTIVE)", "PRIVATE NATURE CONSERVATION WORK", "SOLO OUTDOOR CARDIO (MEDITATIVE)",
        "WILDLIFE OBSERVATION HIKE", "DEEP FOREST RUNNING (LONG DISTANCE)", "NATURE PHOTOGRAPHY WALK",
    ],
    "EJ": [
        "ORGANIZED TRAIL RUNNING EVENT", "CONSERVATION PROJECT LEADERSHIP", "GROUP OUTDOOR CARDIO SESSION",
        "WILDLIFE TRAIL GROUP EXPLORATION", "EXTREME TRAIL RACING EVENT ORGANIZATION", "COMMUNITY OUTDOOR FITNESS EVENT",
    ],
    "IJ": [
        "SYSTEMATIC TRAIL RUNNING TRAINING PLAN", "METHODICAL CONSERVATION WORK (SCHEDULED)", "STRUCTURED OUTDOOR CARDIO PROGRAM",
        "WILDLIFE TRAIL MAPPING & DOCUMENTATION", "FINE TRAIL RUNNING TECHNIQUE STUDY", "LONG-TERM NATURE FITNESS ARCHIVING",
    ],
}

NF_ACTIVITIES_F = {  # Women: trail running, conservation, nature immersion
    "EP": [
        "FOREST TRAIL RUNNING (VIVID NATURE)", "CONSERVATION VOLUNTEERING (COMMUNITY GARDEN)", "SPONTANEOUS NATURE WALK CARDIO",
        "WILDLIFE GARDEN TENDING", "EXTREME COASTAL TRAIL RUNNING", "NATURE IMMERSION CARDIO",
    ],
    "IP": [
        "SOLO FOREST RUNNING (MEDITATIVE)", "PRIVATE CONSERVATION GARDENING", "SOLO NATURE CARDIO (CONTEMPLATIVE)",
        "BOTANICAL TRAIL OBSERVATION", "DEEP NATURE WALKING (MINDFUL)", "WILDFLOWER MEADOW WALKING",
    ],
    "EJ": [
        "ORGANIZED NATURE WALK EVENT", "COMMUNITY CONSERVATION PROJECT LEADERSHIP", "GROUP FOREST CARDIO SESSION",
        "WILDLIFE GARDEN COMMUNITY PROJECT", "EXTREME NATURE RETREAT ORGANIZATION", "COMMUNITY FOREST FITNESS EVENT",
    ],
    "IJ": [
        "SYSTEMATIC NATURE WALKING PROGRAM", "METHODICAL CONSERVATION STUDY (BOTANICAL)", "STRUCTURED FOREST CARDIO ROUTINE",
        "WILDLIFE TRAIL BOTANICAL DOCUMENTATION", "FINE NATURE WALKING TECHNIQUE STUDY", "LONG-TERM NATURE IMMERSION JOURNAL",
    ],
}

NF_BLOOD_PREFIX = {
    "O": "",
    "A": "STRUCTURED ",
    "B": "EXTREME ",
    "AB": "CROSS-TERRAIN ",
}

def gen_nf(profile, gender, blood, attitude):
    if gender == "M":
        base = NF_ACTIVITIES_M[attitude]
    else:
        base = NF_ACTIVITIES_F[attitude]
    prefix = NF_BLOOD_PREFIX[blood]
    result = []
    for i, s in enumerate(base):
        if i < 3 and prefix and not s.startswith(prefix.strip()):
            result.append(prefix + s)
        else:
            result.append(s)
    return result

# ============================================================
# MAIN GENERATOR
# ============================================================
def generate_all():
    profiles = []
    idx = 1
    for mbti in MBTI_TYPES:
        group = get_group(mbti)
        attitude = get_attitude(mbti)
        for gender in GENDERS:
            for blood in BLOODS:
                profile_name = f"{mbti}_{gender}_{blood}"
                if group == "SF":
                    slots = gen_sf(profile_name, gender, blood, attitude)
                elif group == "NT":
                    slots = gen_nt(profile_name, gender, blood, attitude)
                elif group == "ST":
                    slots = gen_st(profile_name, gender, blood, attitude)
                elif group == "NF":
                    slots = gen_nf(profile_name, gender, blood, attitude)
                else:
                    slots = ["UNKNOWN"] * 6

                profiles.append({
                    "id": idx,
                    "profile": profile_name,
                    "group": group,
                    "gender": gender,
                    "blood": blood,
                    "attitude": attitude,
                    "slots": slots,
                })
                idx += 1
    return profiles

def write_markdown(profiles, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# 128 PROFILES × 6 SLOTS — LEAKAGE-RESOLUTION ACTIVITY MAPPING v5\n\n")
        f.write("## Framework\n\n")
        f.write("| Group | Leakage Type | Resolution | Activity Domain |\n")
        f.write("|-------|-------------|-----------|-----------------|\n")
        f.write("| **SF** | STRESS leakage (quarks + peonidine) | Eat food and pigments | Cooking, foraging, pigment craft, fermentation |\n")
        f.write("| **NT** | Night energy leakage between sexes | Visual creation by light | M: themeless pure creation; F: green/nature portrayal |\n")
        f.write("| **ST** | Darcy leakage (water) | Musical instruments | Guitar, drums, synths, piano, cello, DJing, beat making |\n")
        f.write("| **NF** | Self-harm risk | Nature cardio | Trail running, conservation, outdoor cardio |\n\n")
        f.write("## Differentiation\n\n")
        f.write("- **O** = balanced/foundational | **A** = structured/methodical | **B** = extreme/improvisational | **AB** = hybrid/interdisciplinary\n")
        f.write("- **M** = physical/high-risk | **F** = structural/complex\n")
        f.write("- **EJ** = organized/public | **EP** = improvisational/spontaneous | **IJ** = methodical/private | **IP** = exploratory/introspective\n\n")
        f.write("---\n\n")

        group_names = {"NT": "NT — VISUAL CREATION BY LIGHT", "NF": "NF — NATURE CARDIO",
                       "ST": "ST — MUSICAL INSTRUMENTS", "SF": "SF — FOOD & PIGMENT"}
        group_order = ["NT","NF","ST","SF"]

        for grp in group_order:
            f.write(f"# {group_names[grp]}\n\n")
            grp_profiles = [p for p in profiles if p["group"] == grp]
            # Sub-group by MBTI type, write each section once
            seen_mbti = []
            for p in grp_profiles:
                mbti = p["profile"].split("_")[0]
                if mbti not in seen_mbti:
                    seen_mbti.append(mbti)
            for mbti in seen_mbti:
                att = get_attitude(mbti)
                f.write(f"## {mbti} ({grp} + {att})\n\n")
                f.write("| # | Profile | Slot 1 | Slot 2 | Slot 3 | Slot 4 | Slot 5 | Slot 6 |\n")
                f.write("|---|---------|--------|--------|--------|--------|--------|--------|\n")
                for p2 in grp_profiles:
                    if p2["profile"].split("_")[0] == mbti:
                        f.write(f"| {p2['id']} | {p2['profile']} | {' | '.join(p2['slots'])} |\n")
                f.write("\n")
            f.write("---\n\n")

        # Also write flat table
        f.write("\n## Full Flat Table\n\n")
        f.write("| # | Profile | Group | Slot 1 | Slot 2 | Slot 3 | Slot 4 | Slot 5 | Slot 6 |\n")
        f.write("|---|---------|-------|--------|--------|--------|--------|--------|--------|\n")
        for p in profiles:
            f.write(f"| {p['id']} | {p['profile']} | {p['group']} | {' | '.join(p['slots'])} |\n")

def write_json(profiles, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    profiles = generate_all()
    write_markdown(profiles, r"c:\Users\User\Downloads\activity_128_v5.md")
    write_json(profiles, r"c:\Users\User\Downloads\activity_128_v5.json")
    print(f"Generated {len(profiles)} profiles × 6 slots = {len(profiles)*6} activities")
    # Uniqueness check
    all_acts = set()
    dupes = 0
    for p in profiles:
        for s in p["slots"]:
            key = (p["profile"], s)
            if s in all_acts:
                dupes += 1
            all_acts.add(s)
    print(f"Unique activities: {len(all_acts)} / {len(profiles)*6}")
    if dupes > 0:
        print(f"Warning: {dupes} duplicate activity strings (across profiles)")
    # Group distribution
    from collections import Counter
    groups = Counter(p["group"] for p in profiles)
    print(f"Group distribution: {dict(groups)}")
