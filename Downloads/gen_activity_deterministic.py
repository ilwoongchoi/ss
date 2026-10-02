#!/usr/bin/env python3
"""
Deterministic Activity Mapping — Full System Stack Derivation

Chain: Leakage Cavity → Attractor → Rainbow Color Action → Pigment/Biochemical → 8D → Anatomical Anchor → Activity

NOT 8D numbers → activity.
Instead: the full system stack determines what activity each profile MUST do.

4 MBTI groups × 4 leakage types × 6 attractors × 8 color actions × 8 pigments × 8D params × anatomical anchors
"""

import json

# ============================================================
# SYSTEM LAYER 1: LEAKAGE CAVITIES (which leakage each group resolves)
# ============================================================
LEAKAGE = {
    "SF": {
        "type": "STRESS leakage",
        "cause": "quarks + peonidine → STRESS leakage from 5th unmapped column",
        "cavity_sites": ["gluon (0,+46,+7) philtrum — color confinement fails", "fold_belt — tau-z_boson collision"],
        "resolution": "Eat food and pigments — GREEN action (cytochrome_c_oxidase, sulforaphane, collagen)",
        "color_action": "GREEN = 먹기/Eat",
        "pigment_path": "s=phycocyanin(cytochrome_c_oxidase) + h=peonidine(disulfide_bond) + r=NaCl(electrolyte) → ingest pigments to block stress leakage",
    },
    "NT": {
        "type": "Night energy leakage between sexes",
        "cause": "energy leakage during night between male/female — photon/w_boson dissipation",
        "cavity_sites": ["heme (-8.2,+4.1,+7.3) — Fe2+ cannot recharge", "neutron (-8,+32,-2) — w_boson decay uncontrolled"],
        "resolution": "Visual creation by light — recover leaked photons through deliberate light generation",
        "color_action": "WHITE = 상상/Imagine (M: themeless) / GREEN = 먹기 (F: nature/green portrayal)",
        "pigment_path": "M: gamma=delphinidine(photon emission) + nu=w_boson(dark_energy→light) → create light without subject. F: s=phycocyanin(green/cytochrome) + gamma=delphinidine(blue-purple) → portray green/nature",
    },
    "ST": {
        "type": "Darcy leakage (water)",
        "cause": "water-mediated leakage — solenoid resistance threshold 3/32 = 0.09375 Darcy-style",
        "cavity_sites": ["LIP_water_node — left iliac crest phosphorus-water", "right_foot_outer_edge — peripheral reverse flow"],
        "resolution": "Musical instruments — structured sound waves counter water-mediated darcy leakage",
        "color_action": "BLACK = 만들기/Make (leakage BLOCK through structured creation)",
        "pigment_path": "r=neutrino(NaCl/proton_pump rhythm) + d=tau/z_boson(actomyosin/collagen tension) + p=higgs(form/predictability) + nu=w_boson(recursive motif) → instrument playing blocks darcy flow",
    },
    "NF": {
        "type": "Self-harm risk",
        "cause": "observer leak through D3 gates — left_eye/right_eye/left_genital/right_genital outlets",
        "cavity_sites": ["D3 observer gates — 4 outlets", "aurora — skull piezoelectric field night mode"],
        "resolution": "Pure non-spatial nature activities — cardio in nature to close observer gates through physical exertion",
        "color_action": "RED = 마시기/Drink (heme ch1, water_vapour, co2) + BLUE = 보기/See (nature observation)",
        "pigment_path": "h=gluon(cyanidine/complexity) + g=muon(sulforaphane/sealing) → nature cardio seals observer gates through metabolic exertion",
    },
}

# ============================================================
# SYSTEM LAYER 2: ATTRACTORS (which phase each group operates in)
# ============================================================
ATTRACTORS = {
    "SF": {
        "primary": "Information (Earth→Moon)",
        "particle_triplet": "neutrino, quark, photon",
        "phase": "clean signal-to-noise — foraging requires clean sensory information",
        "secondary": "Energy (Sun→Earth)",
        "secondary_triplet": "proton, gluon, w_boson",
        "secondary_phase": "metabolic ATP production — cooking/fermentation = energy transformation",
    },
    "NT": {
        "primary": "COX Retrograde (observer closure)",
        "particle_triplet": "electron, neutrino, photon",
        "phase": "observer closure = heme 5-step EM path complete — visual creation = deliberate photon recovery",
        "secondary": "GaN Bulkhead (Barnard→Sun)",
        "secondary_triplet": "gluon, higgs, z_boson",
        "secondary_phase": "cortical sealing intact — structured visual output prevents bulkhead breach",
    },
    "ST": {
        "primary": "Repair (Moon→CoMag)",
        "particle_triplet": "tau, gluon, w_boson",
        "phase": "autophagy T-flip-flop — musical practice = repair cycle through structured sound",
        "secondary": "GaN Bulkhead (Barnard→Sun)",
        "secondary_triplet": "gluon, higgs, z_boson",
        "secondary_phase": "cortical sealing — instrument playing seals auditory cortex",
    },
    "NF": {
        "primary": "Opioid Landau (CoMag→Barnard)",
        "particle_triplet": "muon, electron, photon",
        "phase": "reward homeostasis — nature cardio restores opioid balance, prevents self-harm",
        "secondary": "COX Retrograde (observer closure)",
        "secondary_triplet": "electron, neutrino, photon",
        "secondary_phase": "observer closure — nature immersion closes D3 observer gates",
    },
}

# ============================================================
# SYSTEM LAYER 3: RAINBOW COLOR ACTION GUIDE
# ============================================================
COLOR_ACTIONS = {
    "GREEN": {"action": "먹기/Eat", "biochemical": "cytochrome_c_oxidase, carbon, sulforaphane, collagen", "dimension": "s+d"},
    "RED": {"action": "마시기/Drink", "biochemical": "heme ch1, water_vapour, co2, caco3, peonidine", "dimension": "d+g"},
    "BLACK": {"action": "만들기/Make", "biochemical": "mc1r q_bar, gluon_orogen = leakage BLOCK", "dimension": "nu+h"},
    "WHITE": {"action": "상상/Imagine", "biochemical": "heme, memory_entropy, observer_leftd2", "dimension": "r+p"},
    "YELLOW": {"action": "냄새/Smell", "biochemical": "pi_electron_cloud, left_amygdala, clay_gouge", "dimension": "r+gamma"},
    "BLUE": {"action": "보기/See", "biochemical": "Left Eye GABA-B(640 cytochrome), heme, aurora", "dimension": "s+gamma"},
    "ORANGE": {"action": "상상하며 냄새/Imagine Smell", "biochemical": "memory_entropy + left_amygdala, hind_insula", "dimension": "p+h"},
    "PURPLE": {"action": "금지/Forbidden", "biochemical": "peonidine(역방향 위험), caco3(과부하) = leakage DELAY", "dimension": "h+gamma"},
}

# ============================================================
# SYSTEM LAYER 4: 8D PIGMENT ALGEBRA
# ============================================================
PIGMENTS = {
    "r": {"particle": "neutrino", "pigment": "Na+/K+/Mg2+ electrolyte", "color_day": "YELLOW", "color_night": "WHITE", "biochemical": "NaCl → proton_pump", "anatomy": "right posterior forearm (extensor compartment)"},
    "h": {"particle": "gluon", "pigment": "Cyanidine (적자색)", "color_day": "RED-PURPLE", "color_night": "RED-PURPLE", "biochemical": "peonidine ch0 → disulfide_bond → pentose_phosphate", "anatomy": "brain compartment 2, GABA-B female 0.2828 Higgs gate"},
    "d": {"particle": "tau/z_boson", "pigment": "Astaxanthin (적색)", "color_day": "RED", "color_night": "GREEN", "biochemical": "mycorradicin → actomyosin → collagen", "anatomy": "aortic arch / left carotid / melatonin relay (nasion→mid-ridge→rhinion)"},
    "p": {"particle": "higgs", "pigment": "Phosphatidylcholine (인지질)", "color_day": "YELLOW", "color_night": "WHITE", "biochemical": "carbon_q_or → methionine → substance_P → MC1R", "anatomy": "observer_leftd2 4-5nm, frontal eye field"},
    "s": {"particle": "quark", "pigment": "Phycocyanin (청색)", "color_day": "BLUE", "color_night": "BLUE", "biochemical": "aurora → heme → cytochrome_c_oxidase", "anatomy": "right sole DRD1/DRD5 4-5nm, s-axis origin"},
    "gamma": {"particle": "photon", "pigment": "Delphinidine (청자색)", "color_day": "BLUE-PURPLE", "color_night": "BLUE-PURPLE", "biochemical": "peonidine ch1 → co2 → male_right_oxytocin", "anatomy": "right D2, GaN bulkhead, dorsal stream"},
    "g": {"particle": "muon", "pigment": "Sulforaphane/Allicin (황화합물)", "color_day": "RED (aurora Rb37)", "color_night": "CYAN (lower_mantle W74/Re75)", "biochemical": "sulforaphane → glymphatic_system → cysteine → Nrf2", "anatomy": "clathrin 100-200nm, tight junction 500-2000nm"},
    "nu": {"particle": "w_boson", "pigment": "발효 대사물/프로바이오틱스", "color_day": "YELLOW", "color_night": "BLACK (dark_energy)", "biochemical": "cysteine → memory_entropy → glymphatic feedback", "anatomy": "clathrin-coated pit 100-200nm, fracton nesting"},
}

# ============================================================
# SYSTEM LAYER 5: 8D PARAMETER TRENDS PER GROUP
# From Update Particle Map Locations.md analysis
# ============================================================
GROUP_8D = {
    "NT": {"peaks": ["d↑", "p↑", "ν↑"], "description": "위험·계획·재귀 — 분석가", "dominant_dims": ["d", "p", "nu"]},
    "NF": {"peaks": ["h↑", "g↑"], "description": "복잡도·구조 — 외교관", "dominant_dims": ["h", "g"]},
    "SF": {"peaks": ["r↑", "s↑", "h↑"], "description": "실행·관측·복잡도 — 탐험가", "dominant_dims": ["r", "s", "h"]},
    "ST": {"peaks": ["r↑", "d↑", "p↑", "ν↑"], "description": "실행·위험·계획·재귀 — 관리자", "dominant_dims": ["r", "d", "p", "nu"]},
}

# ============================================================
# SYSTEM LAYER 6: ATTITUDE (EJ/EP/IJ/IP) — 8D trends
# ============================================================
ATTITUDE_8D = {
    "EJ": {"peaks": ["r↑↑", "p↑", "γ↑", "g↑"], "description": "organized/public", "shape": "이끌고 기획하고 공적으로 실행"},
    "EP": {"peaks": ["r↑", "h↑", "s↑", "γ↑"], "description": "improvisational/spontaneous", "shape": "그 자리에서 만들고 던지고 시도"},
    "IJ": {"peaks": ["d↑", "p↑↑", "g↑", "ν↑"], "description": "methodical/private", "shape": "혼자 연구하고 정리하고 아카이브"},
    "IP": {"peaks": ["h↑", "ν↑", "d↑"], "description": "exploratory/introspective", "shape": "깊이 파고들고 만지고 조율"},
}

# ============================================================
# SYSTEM LAYER 7: BLOOD TYPE — 8D trends
# ============================================================
BLOOD_8D = {
    "O": {"description": "balanced/foundational", "modifier": "", "shape": "기초형 — 원형 그대로"},
    "A": {"description": "structured/methodical", "modifier": "STRUCTURED", "shape": "구조형 — 정교하게 다듬음"},
    "B": {"description": "extreme/improvisational", "modifier": "EXTREME", "shape": "극단형 — 날것으로 밀어붙임"},
    "AB": {"description": "hybrid/interdisciplinary", "modifier": "FUSION", "shape": "융합형 — 경계를 넘나듦"},
}

# ============================================================
# SYSTEM LAYER 8: GENDER — 8D trends + NT theme split
# ============================================================
GENDER_8D = {
    "M": {"description": "physical/high-risk", "shape": "물리적 · 고위험 · 직접적"},
    "F": {"description": "structural/complex", "shape": "구조적 · 복잡 · 정밀함"},
}

# ============================================================
# SYSTEM LAYER 9: TOROIDAL TIME SLOTS
# AB(0-3h) → A(3-9h) → O(9-15h) → B(15-21h)
# ============================================================
TOROIDAL_SLOTS = {
    "AB": {"time": "0-3h", "phase": "RELEASE", "description": "midnight release — AB toroidal position"},
    "A": {"time": "3-9h", "phase": "STRESS GROWTH", "description": "morning stress growth — A toroidal position"},
    "O": {"time": "9-15h", "phase": "PRESENT", "description": "day present moment — O toroidal position"},
    "B": {"time": "15-21h", "phase": "EXTREME GROWTH", "description": "evening extreme growth — B toroidal position"},
}

# ============================================================
# DETERMINISTIC ACTIVITY DERIVATION
# ============================================================

# 16 MBTI types
MBTI_TYPES = [
    "ENTP", "INTP", "ENTJ", "INTJ",  # NT
    "ENFP", "INFP", "ENFJ", "INFJ",  # NF
    "ESTP", "ISTP", "ESTJ", "ISTJ",  # ST
    "ESFP", "ISFP", "ESFJ", "ISFJ",  # SF
]

GROUP_MAP = {
    "NT": ["ENTP", "INTP", "ENTJ", "INTJ"],
    "NF": ["ENFP", "INFP", "ENFJ", "INFJ"],
    "ST": ["ESTP", "ISTP", "ESTJ", "ISTJ"],
    "SF": ["ESFP", "ISFP", "ESFJ", "ISFJ"],
}

def get_group(mbti):
    for grp, types in GROUP_MAP.items():
        if mbti in types:
            return grp
    return None

def get_attitude(mbti):
    e_i = mbti[0]
    j_p = mbti[3]
    if e_i == "E" and j_p == "J": return "EJ"
    if e_i == "E" and j_p == "P": return "EP"
    if e_i == "I" and j_p == "J": return "IJ"
    if e_i == "I" and j_p == "P": return "IP"

# ============================================================
# ACTIVITY GENERATION — derived from full system stack
# ============================================================

def derive_activity(group, gender, blood, attitude, slot_idx):
    """
    Deterministic activity derivation:
    group → leakage → attractor → color action → pigment → 8D → anatomy → activity
    slot_idx (0-5) → which aspect of the derivation chain to emphasize
    """
    leak = LEAKAGE[group]
    attr = ATTRACTORS[group]
    g8d = GROUP_8D[group]
    a8d = ATTITUDE_8D[attitude]
    b8d = BLOOD_8D[blood]
    gen = GENDER_8D[gender]

    # 6 slots = 6 aspects of the derivation chain
    # Slot 0: leakage resolution (primary action)
    # Slot 1: attractor phase (which cycle)
    # Slot 2: color action (which verb)
    # Slot 3: pigment/biochemical (which substance)
    # Slot 4: 8D peak dimension (which parameter drives)
    # Slot 5: toroidal slot (which time phase)

    blood_mod = b8d["modifier"]

    if group == "SF":
        # SF: STRESS leakage → Eat food and pigments
        # GREEN action: cytochrome_c_oxidase, sulforaphane, collagen
        # Pigments: s=phycocyanin + h=peonidine + r=NaCl
        # Attractor: Information (clean signal) + Energy (ATP)
        # Anatomy: right posterior forearm (r/NaCl), right sole (s/quark)

        m_dishes = {
            "O": "WILD FORAGED INGREDIENTS",
            "A": "SEASONAL HEIRLOOM INGREDIENTS",
            "B": "BOLD INTENSE INGREDIENTS",
            "AB": "CROSS-CULTURAL FUSION INGREDIENTS",
        }
        f_dishes = {
            "O": "EDIBLE FLOWERS & GARDEN HERBS",
            "A": "BOTANICAL HEIRLOOM VARIETIES",
            "B": "WILD INTENSE BLOOM INGREDIENTS",
            "AB": "DECONSTRUCTED FUSION FLORALS",
        }

        if gender == "M":
            slots = [
                # Slot 0: leakage resolution — eat to block stress
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}WILD FORAGING & COOKING ({m_dishes[blood]})",
                # Slot 1: attractor — Information (clean signal) + Energy (ATP)
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}PIGMENT EXTRACTION CRAFT (phycocyanin/peonidine → stress block)",
                # Slot 2: GREEN action — eat
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}FERMENTATION (sulforaphane → glymphatic → Nrf2 activation)",
                # Slot 3: pigment/biochemical — s=phycocyanin + h=peonidine + r=NaCl
                f"NaCl ELECTROLYTE RESTORATION (r-dim: right posterior forearm → proton_pump reset)",
                # Slot 4: 8D peak — r↑s↑h↑
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}TASTING MENU DESIGN (r↑ rhythm + s↑ observation + h↑ complexity)",
                # Slot 5: toroidal — blood type determines slot
                f"{TOROIDAL_SLOTS[blood]['phase']} COOKING SESSION ({TOROIDAL_SLOTS[blood]['time']} toroidal slot)",
            ]
        else:
            slots = [
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}AESTHETIC CULINARY CRAFT ({f_dishes[blood]})",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}BOTANICAL DYE & NATURAL COLORING (peonidine → disulfide_bond → pigment craft)",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}SLOW FERMENTATION (yogurt/kimchi → probiotic → nu=발효대사물)",
                f"HERB GARDEN CULTIVATION (s=phycocyanin → cytochrome_c_oxidase → chlorophyll pathway)",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}PRESERVE & JAM CRAFT (h↑ complexity + s↑ observation + r↑ execution)",
                f"{TOROIDAL_SLOTS[blood]['phase']} BOTANICAL CRAFT ({TOROIDAL_SLOTS[blood]['time']} toroidal slot)",
            ]

        # Attitude modifies the approach
        att_mods = {
            "EJ": ("COMMUNITY ", " GROUP EVENT", " ORGANIZED SESSION", " PUBLIC WORKSHOP"),
            "EP": ("SPONTANEOUS ", " WILD EXPERIMENT", " IMPROVISED SESSION", " ON-THE-SPOT CRAFT"),
            "IJ": ("METHODICAL ", " ARCHIVE STUDY", " SCHEDULED SESSION", " PRIVATE RESEARCH"),
            "IP": ("SOLO ", " DEEP CRAFT", " INTROSPECTIVE SESSION", " ARTISANAL WORK"),
        }
        am = att_mods[attitude]
        slots[0] = am[0] + slots[0]
        slots[1] = slots[1] + am[1]
        slots[2] = slots[2] + am[2]
        slots[5] = am[3] + " — " + slots[5]

        return slots

    elif group == "NT":
        # NT: Night energy leakage → Visual creation by light
        # M: WHITE action (themeless pure creation) / F: GREEN action (nature/green portrayal)
        # Pigments: M: gamma=delphinidine(photon) + nu=w_boson(dark_energy→light)
        #           F: s=phycocyanin(green) + gamma=delphinidine(blue-purple)
        # Attractor: COX Retrograde (observer closure) + GaN Bulkhead (cortical sealing)
        # Anatomy: melatonin relay (nasion→mid-ridge→rhinion) for d→gamma transition

        if gender == "M":
            m_media = {
                "O": "LIGHT PAINTING PHOTOGRAPHY",
                "A": "PRECISION LIGHT FIELD RENDERING",
                "B": "RAW ABSTRACT LIGHT PROJECTION",
                "AB": "FUSION DIGITAL-PHYSICAL LIGHT ART",
            }
            slots = [
                # Slot 0: leakage resolution — create light to recover leaked photons
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}THEMELESS {m_media[blood]} (photon recovery → COX retrograde closure)",
                # Slot 1: attractor — COX Retrograde (observer closure)
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}GENERATIVE CODE ART (electron→neutrino→photon 5-step EM path)",
                # Slot 2: WHITE action — imagine (themeless)
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}ABSTRACT DIGITAL COMPOSITION (WHITE=상상, no subject, medium-only differentiation)",
                # Slot 3: pigment — gamma=delphinidine + nu=w_boson(dark_energy→light)
                f"LIGHT EMISSION CRAFT (gamma=delphinidine photon + nu=w_boson dark_energy→light conversion)",
                # Slot 4: 8D peak — d↑p↑ν↑
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}PARAMETRIC LIGHT SCULPTURE (d↑ darkness + p↑ form + ν↑ recursion)",
                # Slot 5: toroidal
                f"{TOROIDAL_SLOTS[blood]['phase']} VISUAL CREATION ({TOROIDAL_SLOTS[blood]['time']} toroidal slot)",
            ]
        else:
            f_media = {
                "O": "GREEN NATURE PHOTOGRAPHY",
                "A": "BOTANICAL WATERCOLOR STUDY",
                "B": "RAW GREEN LANDSCAPE PAINTING",
                "AB": "FUSION NATURE DIGITAL ART",
            }
            slots = [
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}{f_media[blood]} (GREEN=먹기 → cytochrome_c_oxidase → nature pigment ingestion through vision)",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}BOTANICAL ILLUSTRATION (s=phycocyanin green + gamma=delphinidine blue-purple → nature spectrum)",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}IMAGINED GREEN ECOSYSTEM PAINTING (WHITE=상상 + GREEN=자연 → imagined nature)",
                f"NATURE PIGMENT STUDY (s=phycocyanin chlorophyll pathway + h=peonidine plant pigment)",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}GREEN COMPOSITION ARCHIVE (d↑ + p↑ + ν↑ → structured nature visual series)",
                f"{TOROIDAL_SLOTS[blood]['phase']} NATURE VISUAL CRAFT ({TOROIDAL_SLOTS[blood]['time']} toroidal slot)",
            ]

        att_mods = {
            "EJ": ("LARGE-SCALE PUBLIC ", " EXHIBITION", " COMMISSION", " ORGANIZED SHOW"),
            "EP": ("SPONTANEOUS ", " EXPERIMENT", " IMPROVISED PIECE", " ON-THE-SPOT CREATION"),
            "IJ": ("SYSTEMATIC ", " ARCHIVE SERIES", " STUDY", " PRIVATE RESEARCH"),
            "IP": ("SOLO ", " DEEP EXPLORATION", " INTROSPECTIVE PIECE", " ARTISANAL CRAFT"),
        }
        am = att_mods[attitude]
        slots[0] = am[0] + slots[0]
        slots[1] = slots[1] + am[1]
        slots[2] = slots[2] + am[2]
        slots[5] = am[3] + " — " + slots[5]

        return slots

    elif group == "ST":
        # ST: Darcy leakage (water) → Musical instruments
        # BLACK action: 만들기/Make (leakage BLOCK through structured creation)
        # Pigments: r=NaCl(rhythm) + d=tau/z_boson(tension) + p=higgs(form) + nu=w_boson(recursion)
        # Attractor: Repair (autophagy T-flip-flop) + GaN Bulkhead (cortical sealing)
        # Anatomy: right posterior forearm (r/NaCl) → instrument playing uses forearm extensors

        m_genres = {
            "O": "ROCK/BLUES",
            "A": "JAZZ STANDARDS",
            "B": "METAL/PUNK",
            "AB": "JAZZ-ROCK-HIPHOP BLEND",
        }
        f_genres = {
            "O": "CLASSICAL",
            "A": "CLASSICAL REPERTOIRE",
            "B": "AVANT-GARDE",
            "AB": "CLASSICAL-JAZZ-EDM BLEND",
        }

        if gender == "M":
            # M: electric guitar, drum sampling, beat making, DJ
            # r=NaCl → right posterior forearm → guitar picking/drumming uses extensor muscles
            slots = [
                # Slot 0: leakage resolution — play instrument to block darcy
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}ELECTRIC GUITAR ({m_genres[blood]}) — r=NaCl right forearm extensor → darcy block",
                # Slot 1: attractor — Repair (autophagy T-flip-flop)
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}DRUM SAMPLING & BEAT MAKING ({m_genres[blood]}) — tau/gluon/w_boson repair cycle",
                # Slot 2: BLACK action — make (leakage BLOCK)
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}MODULAR SYNTH PATCH DESIGN — BLACK=만들기, mc1r q_bar leakage BLOCK",
                # Slot 3: pigment — r=NaCl + d=actomyosin/collagen + p=higgs + nu=w_boson
                f"LUTHIER WORK & INSTRUMENT MAINTENANCE (r+d+p+ν → physical instrument = structured sound wave)",
                # Slot 4: 8D peak — r↑d↑p↑ν↑
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}DJ SET ({m_genres[blood]}) — r↑ rhythm + d↑ darkness + p↑ form + ν↑ recursion",
                # Slot 5: toroidal
                f"{TOROIDAL_SLOTS[blood]['phase']} MUSIC SESSION ({TOROIDAL_SLOTS[blood]['time']} toroidal slot)",
            ]
        else:
            # F: cello, piano, DJ, synths
            slots = [
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}CELLO PERFORMANCE ({f_genres[blood]}) — d=actomyosin/collagen → bowing tension blocks darcy",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}PIANO IMPROVISATION ({f_genres[blood]}) — tau/gluon/w_boson repair cycle",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}SYNTH EXPLORATION — BLACK=만들기, mc1r q_bar leakage BLOCK",
                f"INSTRUMENT TUNING & TECHNIQUE STUDY (r+d+p+ν → structured sound wave craft)",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'FUSION ' if blood=='AB' else ''}DJ SET ({f_genres[blood]}) — r↑ + d↑ + p↑ + ν↑",
                f"{TOROIDAL_SLOTS[blood]['phase']} MUSIC SESSION ({TOROIDAL_SLOTS[blood]['time']} toroidal slot)",
            ]

        att_mods = {
            "EJ": ("ORGANIZED BAND ", " REHEARSAL", " STUDIO RECORDING", " LIVE PERFORMANCE"),
            "EP": ("IMPROVISED ", " JAM SESSION", " ON-THE-SPOT BEAT", " SPONTANEOUS DJ SET"),
            "IJ": ("SYSTEMATIC ", " PRACTICE ARCHIVE", " MUSIC THEORY STUDY", " REPERTOIRE BUILDING"),
            "IP": ("SOLO ", " DEEP TONE CRAFT", " ANALOG CALIBRATION", " ARTISANAL EXPLORATION"),
        }
        am = att_mods[attitude]
        slots[0] = am[0] + slots[0]
        slots[1] = slots[1] + am[1]
        slots[2] = slots[2] + am[2]
        slots[5] = am[3] + " — " + slots[5]

        return slots

    elif group == "NF":
        # NF: Self-harm risk → Nature cardio
        # RED action: 마시기/Drink (heme, water_vapour, co2) + BLUE action: 보기/See (nature)
        # Pigments: h=gluon(cyanidine/complexity) + g=muon(sulforaphane/sealing)
        # Attractor: Opioid Landau (reward homeostasis) + COX Retrograde (observer closure)
        # Anatomy: D3 observer gates (eye/genital outlets) → cardio closes them

        m_terrains = {
            "O": "FOREST TRAIL",
            "A": "MOUNTAIN PATH",
            "B": "EXTREME OFF-TRAIL",
            "AB": "CROSS-TERRAIN",
        }
        f_terrains = {
            "O": "FOREST NATURE WALK",
            "A": "BOTANICAL GARDEN WALK",
            "B": "WILD NATURE IMMERSION",
            "AB": "COASTAL CROSS-TERRAIN",
        }

        if gender == "M":
            slots = [
                # Slot 0: leakage resolution — cardio to close D3 observer gates
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'CROSS-TERRAIN ' if blood=='AB' else ''}TRAIL RUNNING ({m_terrains[blood]}) — RED=마시기, heme O2/CO2 → D3 gate closure",
                # Slot 1: attractor — Opioid Landau (reward homeostasis)
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'CROSS-TERRAIN ' if blood=='AB' else ''}CONSERVATION VOLUNTEERING — muon/electron/photon reward restoration",
                # Slot 2: RED + BLUE action — drink (heme) + see (nature)
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'CROSS-TERRAIN ' if blood=='AB' else ''}OUTDOOR CARDIO — RED=마시기(heme ch1, water_vapour) + BLUE=보기(nature observation)",
                # Slot 3: pigment — h=gluon(cyanidine) + g=muon(sulforaphane/sealing)
                f"WILDLIFE TRAIL EXPLORATION (h↑ complexity + g↑ sealing → glymphatic → Nrf2 activation)",
                # Slot 4: 8D peak — h↑g↑
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'CROSS-TERRAIN ' if blood=='AB' else ''}EXTREME NATURE CARDIO (h↑ complexity + g↑ sealing → observer gate forced closure)",
                # Slot 5: toroidal
                f"{TOROIDAL_SLOTS[blood]['phase']} NATURE CARDIO ({TOROIDAL_SLOTS[blood]['time']} toroidal slot)",
            ]
        else:
            slots = [
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'CROSS-TERRAIN ' if blood=='AB' else ''}{f_terrains[blood]} — RED=마시기 + BLUE=보기 → D3 gate closure",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'CROSS-TERRAIN ' if blood=='AB' else ''}CONSERVATION GARDENING — muon/electron/photon reward restoration",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'CROSS-TERRAIN ' if blood=='AB' else ''}MINDFUL NATURE CARDIO — RED+BLUE → heme O2 + nature vision",
                f"BOTANICAL TRAIL OBSERVATION (h↑ + g↑ → glymphatic → Nrf2)",
                f"{'STRUCTURED ' if blood=='A' else 'EXTREME ' if blood=='B' else 'CROSS-TERRAIN ' if blood=='AB' else ''}NATURE IMMERSION CARDIO (h↑ + g↑ → observer gate closure)",
                f"{TOROIDAL_SLOTS[blood]['phase']} NATURE ACTIVITY ({TOROIDAL_SLOTS[blood]['time']} toroidal slot)",
            ]

        att_mods = {
            "EJ": ("ORGANIZED GROUP ", " EVENT", " COMMUNITY SESSION", " PUBLIC FITNESS"),
            "EP": ("SPONTANEOUS ", " EXPLORATION", " IMPROMPTU SESSION", " WILD ADVENTURE"),
            "IJ": ("SYSTEMATIC ", " TRAINING PLAN", " SCHEDULED PROGRAM", " PRIVATE PRACTICE"),
            "IP": ("SOLO ", " DEEP IMMERSION", " MEDITATIVE SESSION", " INTROSPECTIVE WALK"),
        }
        am = att_mods[attitude]
        slots[0] = am[0] + slots[0]
        slots[1] = slots[1] + am[1]
        slots[2] = slots[2] + am[2]
        slots[5] = am[3] + " — " + slots[5]

        return slots


def generate_all():
    profiles = []
    pid = 1
    blood_types = ["O", "A", "B", "AB"]
    genders = ["M", "F"]

    for grp in ["NT", "NF", "ST", "SF"]:
        for mbti in GROUP_MAP[grp]:
            att = get_attitude(mbti)
            for gender in genders:
                for blood in blood_types:
                    profile = f"{mbti}_{gender}_{blood}"
                    slots = derive_activity(grp, gender, blood, att, 0)
                    profiles.append({
                        "id": pid,
                        "profile": profile,
                        "group": grp,
                        "mbti": mbti,
                        "gender": gender,
                        "blood": blood,
                        "attitude": att,
                        "slots": slots,
                        "derivation": {
                            "leakage": LEAKAGE[grp],
                            "attractor": ATTRACTORS[grp],
                            "group_8d": GROUP_8D[grp],
                            "attitude_8d": ATTITUDE_8D[att],
                            "blood_8d": BLOOD_8D[blood],
                            "gender_8d": GENDER_8D[gender],
                            "toroidal_slot": TOROIDAL_SLOTS[blood],
                        }
                    })
                    pid += 1
    return profiles


def write_markdown(profiles, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# 128 PROFILES × 6 SLOTS — DETERMINISTIC ACTIVITY MAPPING v6\n\n")
        f.write("## Derivation Chain\n\n")
        f.write("Each activity is derived from the FULL SYSTEM STACK, not just 8D numbers:\n\n")
        f.write("```\n")
        f.write("Leakage Cavity → Attractor → Rainbow Color Action → Pigment/Biochemical → 8D → Anatomical Anchor → Activity\n")
        f.write("```\n\n")
        f.write("## System Layers Used\n\n")
        f.write("| Layer | Source | What it determines |\n")
        f.write("|-------|--------|-------------------|\n")
        f.write("| **Leakage Cavities** | nm_body_particle_map_v4 PART IX | Which leakage each group resolves |\n")
        f.write("| **6 Attractors** | nm_body_particle_map_v4 PART VI | Which phase/cycle the activity operates in |\n")
        f.write("| **Rainbow Color Action** | nm_body_particle_map_v4 PART XIV | Which verb (eat/drink/make/imagine/see) |\n")
        f.write("| **8D Pigment Algebra** | nm_body_particle_map_v4 PART XIV | Which biochemical substance/pathway |\n")
        f.write("| **8D Parameter Trends** | Update Particle Map Locations.md | Which dimensions peak per group/attitude |\n")
        f.write("| **Anatomical Anchors** | nm_body_particle_map_v4 PART I + XIII | Where in body the activity acts |\n")
        f.write("| **Toroidal Time Slots** | AB→A→O→B cycle | Which time phase per blood type |\n")
        f.write("| **Melatonin Relay** | CIRCUITFILE.MD (3-node) | d→gamma transition for NT visual creation |\n")
        f.write("| **NaCl Location** | CIRCUITFILE.MD (right posterior forearm) | r-dim anatomical anchor for ST/SF |\n\n")

        f.write("## Group Derivation Summary\n\n")
        f.write("| Group | Leakage | Attractor | Color Action | Key Pigments | 8D Peaks | Activity Domain |\n")
        f.write("|-------|---------|-----------|-------------|-------------|----------|----------------|\n")
        f.write("| **SF** | STRESS (quarks+peonidine) | Information + Energy | GREEN=먹기 | s=phycocyanin, h=peonidine, r=NaCl | r↑s↑h↑ | Foraging, cooking, pigment craft, fermentation |\n")
        f.write("| **NT** | Night energy (sexes) | COX Retrograde + GaN Bulkhead | M: WHITE=상상 / F: GREEN=자연 | M: gamma+nu / F: s+gamma | d↑p↑ν↑ | Visual creation by light (themeless M / green F) |\n")
        f.write("| **ST** | Darcy (water) | Repair + GaN Bulkhead | BLACK=만들기 | r=NaCl, d=actomyosin, p=higgs, nu=w_boson | r↑d↑p↑ν↑ | Musical instruments (guitar/drums/synths/piano/cello/DJ) |\n")
        f.write("| **NF** | Self-harm (D3 gates) | Opioid Landau + COX Retrograde | RED=마시기 + BLUE=보기 | h=gluon, g=muon(sulforaphane) | h↑g↑ | Nature cardio, trail running, conservation |\n\n")

        f.write("## Differentiation\n\n")
        f.write("- **Blood type**: O=balanced, A=structured, B=extreme, AB=fusion → also determines toroidal time slot (O=9-15h, A=3-9h, B=15-21h, AB=0-3h)\n")
        f.write("- **Gender**: M=physical/direct, F=structural/complex → NT splits by theme (M=themeless, F=green/nature)\n")
        f.write("- **Attitude**: EJ=organized/public, EP=spontaneous, IJ=methodical/private, IP=introspective/craft\n\n")
        f.write("---\n\n")

        group_names = {
            "NT": "NT — VISUAL CREATION BY LIGHT (COX Retrograde + GaN Bulkhead)",
            "NF": "NF — NATURE CARDIO (Opioid Landau + COX Retrograde)",
            "ST": "ST — MUSICAL INSTRUMENTS (Repair + GaN Bulkhead)",
            "SF": "SF — FOOD & PIGMENT (Information + Energy)"
        }
        group_order = ["NT", "NF", "ST", "SF"]

        for grp in group_order:
            f.write(f"# {group_names[grp]}\n\n")
            grp_profiles = [p for p in profiles if p["group"] == grp]
            seen_mbti = []
            for p in grp_profiles:
                mbti = p["mbti"]
                if mbti not in seen_mbti:
                    seen_mbti.append(mbti)
            for mbti in seen_mbti:
                att = get_attitude(mbti)
                f.write(f"## {mbti} ({grp} + {att})\n\n")
                f.write("| # | Profile | Slot 1: Leakage Resolution | Slot 2: Attractor Phase | Slot 3: Color Action | Slot 4: Pigment/Anatomy | Slot 5: 8D Peak | Slot 6: Toroidal |\n")
                f.write("|---|---------|---------------------------|------------------------|---------------------|------------------------|----------------|-----------------|\n")
                for p in grp_profiles:
                    if p["mbti"] == mbti:
                        f.write(f"| {p['id']} | {p['profile']} | {' | '.join(p['slots'])} |\n")
                f.write("\n")
            f.write("---\n\n")

        # Flat table
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
    write_markdown(profiles, r"c:\Users\User\Downloads\activity_128_v6.md")
    write_json(profiles, r"c:\Users\User\Downloads\activity_128_v6.json")
    print(f"Generated {len(profiles)} profiles × 6 slots = {len(profiles)*6} activities")
    # Uniqueness check
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
    # Group distribution
    from collections import Counter
    dist = Counter(p["group"] for p in profiles)
    print(f"Group distribution: {dict(dist)}")
