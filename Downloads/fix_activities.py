#!/usr/bin/env python3
"""
Fix activity_corrected.csv:
- Cross-reference with 128_UNIFIED_MASTER_8D_fixed.csv
- Fill empty slots and correct wrong activities
- Output: activity_corrected_full.csv

Activity derivation logic from gen_activity_128.py:
  Group(MBTI) → dominant 8D dims → inverse reciprocal pair → torus axis
  → route color → color action → pigment → anatomical anchor → activity
  Blood type → toroidal phase → time slot → activity modifier
  Gender → axis (d↔h) → medium/focus split
  Attitude (EJ/EP/IJ/IP) → approach modifier

6 slots per profile:
  0: Music composition (genre from master CSV)
  1: Solo physical / recreational activity
  2: Creative/artistic activity
  3: Professional/technical activity
  4: Sport/physical activity
  5: Puzzle/game/cognitive activity
"""

import csv
import re
import os

# ============================================================
# MASTER DATA: Parse 128_UNIFIED_MASTER_8D_fixed.csv
# ============================================================
MASTER_PATH = r"c:\Users\User\Downloads\128_UNIFIED_MASTER_8D_fixed.csv"
INPUT_PATH  = r"c:\Users\User\Downloads\activity_corrected.csv"
OUTPUT_PATH = r"c:\Users\User\Downloads\activity_corrected_full.csv"

def parse_master():
    """Parse master CSV into dict keyed by profile key like ENTP_AB_M"""
    master = {}
    with open(MASTER_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get('Type', '').strip()
            if not key:
                continue
            master[key] = row
    return master

# ============================================================
# GROUP / ATTITUDE / BLOOD / GENDER MAPPING
# ============================================================
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
    e_i, j_p = mbti[0], mbti[3]
    if e_i == "E" and j_p == "J": return "EJ"
    if e_i == "E" and j_p == "P": return "EP"
    if e_i == "I" and j_p == "J": return "IJ"
    if e_i == "I" and j_p == "P": return "IP"

BLOOD_MOD = {
    "O":  {"label": "BALANCED",   "shape": "foundational/original"},
    "A":  {"label": "STRUCTURED", "shape": "methodical/refined"},
    "B":  {"label": "EXTREME",    "shape": "raw/intense"},
    "AB": {"label": "FUSION",     "shape": "hybrid/cross-boundary"},
}

ATTITUDE_MOD = {
    "EJ": {"prefix": "ORGANIZED", "suffix": "PUBLIC SESSION", "shape": "community/structured"},
    "EP": {"prefix": "SPONTANEOUS", "suffix": "IMPROVISED SESSION", "shape": "wild/experimental"},
    "IJ": {"prefix": "METHODICAL", "suffix": "PRIVATE STUDY", "shape": "archived/systematic"},
    "IP": {"prefix": "SOLO", "suffix": "DEEP CRAFT", "shape": "introspective/artisanal"},
}

# ============================================================
# ACTIVITY GENERATION PER GROUP
# Based on gen_activity_128.py GROUP_DOMAIN but expanded
# with concrete activities per blood type and gender
# ============================================================

# NT: VISUAL CREATION BY LIGHT (Route 2, RED, h↔d polar)
# Peaks: d↑ p↑ nu↑ — photon recovery, light-based creation
NT_ACTIVITIES = {
    "M": {
        "O": {
            "music": "Ebm composition",
            "solo": "vert bowl skateboarding",
            "creative": "Light Painting Photography",
            "tech": "Thermal energy systems engineer",
            "sport": "skim boarding",
            "game": "match squash",
        },
        "A": {
            "music": "Autechre adjacent composition",
            "solo": "Urban heat island dynamic visualization",
            "creative": "Precision Light Field Rendering / VR AR environment design",
            "tech": "Type System Compiler designer",
            "sport": "road cycle breakout",
            "game": "geoguesser (Hashiwokakero)",
        },
        "B": {
            "music": "Doom metal composition",
            "solo": "writing mystery novels",
            "creative": "Parametric 3D printing light sculpture",
            "tech": "Simulation Game Multiplayer networking engineer",
            "sport": "epee fencing",
            "game": "Nurikabe logic puzzle",
        },
        "AB": {
            "music": "Hyperpop-adjacent composition",
            "solo": "FLOW PARKOUR",
            "creative": "Real-time generative visual jockeying",
            "tech": "HDL FPGA design",
            "sport": "BMX aerial / chasetag",
            "game": "FLOWBOARDING",
        },
    },
    "F": {
        "O": {
            "music": "Baroque guitar composition",
            "solo": "lutherie",
            "creative": "Green nature photography",
            "tech": "열약학 engineer (pharmacology)",
            "sport": "longboard surfing",
            "game": "composting",
        },
        "A": {
            "music": "House dance composition",
            "solo": "diorama craft",
            "creative": "Botanical watercolor study / simulation game development",
            "tech": "simulation game dev",
            "sport": "rink roller skate",
            "game": "ecological volunteering",
        },
        "B": {
            "music": "Mac DeMarco adjacent composition",
            "solo": "sandboarding",
            "creative": "Raw abstract light projection / photogrammetry 3D scanning",
            "tech": "Climate tech Drone Mapping startup",
            "sport": "kite MTB freestyle",
            "game": "number theory hobby",
        },
        "AB": {
            "music": "New wave / IDM composition",
            "solo": "VR AR environment design",
            "creative": "Fusion digital-physical light art / utility network systems design",
            "tech": "Utility network systems designer",
            "sport": "korfball attack (indoor wavepool surf)",
            "game": "trampoline",
        },
    },
}

# NF: NATURE CARDIO (Route 1, GREEN, g↔γ radial)
# Peaks: h↑ g↑ — metabolic sealing, nature immersion
NF_ACTIVITIES = {
    "M": {
        "O": {
            "music": "EBM composition",
            "solo": "Light Painting",
            "creative": "Eco-acoustic soundscape recording",
            "tech": "Padel Tennis / mobile indie game design",
            "sport": "Kendra flow art",
            "game": "forest trail running",
        },
        "A": {
            "music": "Hauntology composition",
            "solo": "snowblading",
            "creative": "Microbial Biomaterials engineering / Algae Materials Fermentation",
            "tech": "Vehicle simulation sound system engineer",
            "sport": "underwater hockey",
            "game": "soundscape archiving",
        },
        "B": {
            "music": "Stoner rock composition",
            "solo": "Comic book graphic novel writing",
            "creative": "Zimmer style cinematic sound design",
            "tech": "Biomimetic furniture design",
            "sport": "kite MTB freestyle",
            "game": "Permaculture",
        },
        "AB": {
            "music": "Noise pop composition",
            "solo": "night time cycling",
            "creative": "Eco-acoustic soundscape recording / Living wall green facade system design",
            "tech": "wildlife documentary",
            "sport": "inline aerial",
            "game": "pogostick",
        },
    },
    "F": {
        "O": {
            "music": "Ambient electronica composition",
            "solo": "standup paddle boarding",
            "creative": "Ecological sketch from imagination",
            "tech": "Schumann resonance DLL (nature healing resonance designer)",
            "sport": "forest trail running",
            "game": "solo hiking in falklands",
        },
        "A": {
            "music": "Space rock composition",
            "solo": "Underground flow/thermal simulation 3D visualization",
            "creative": "Motion graphic design",
            "tech": "shortboard aerial surfing",
            "sport": "drift car",
            "game": "yoga restorative",
        },
        "B": {
            "music": "Singer songwriter composition",
            "solo": "cyanotype sun printing",
            "creative": "Epic fantasy writing",
            "tech": "independent fashion designer",
            "sport": "vivarium building",
            "game": "web design for her business",
        },
        "AB": {
            "music": "Freak folk composition",
            "solo": "rollerskating park recreation",
            "creative": "Regional watershed flow visualization / Green roof network deployment planner",
            "tech": "regional designer",
            "sport": "surfing",
            "game": "yoga vinyasa afterwork",
        },
    },
}

# ST: MUSICAL INSTRUMENTS / STRUCTURED CREATION (Route 4, BLUE, r↔ν equatorial)
# Peaks: r↑ d↑ p↑ nu↑ — leakage block, structured creation
ST_ACTIVITIES = {
    "M": {
        "O": {
            "music": "Experimental rock composition",
            "solo": "feet toe midi player designer",
            "creative": "BIM modelling",
            "tech": "Ice climbing / coasteering",
            "sport": "BMX street/flatland",
            "game": "Sumgrid mobile game",
        },
        "A": {
            "music": "Aero ambient frutigal composition",
            "solo": "botanical illustration",
            "creative": "geological surveyor",
            "tech": "soil piezoenergy engineer",
            "sport": "Adam Ondra style free climb",
            "game": "gardening",
        },
        "B": {
            "music": "Death metal composition",
            "solo": "snowkiting",
            "creative": "generative cnc machining",
            "tech": "3d snow kiting",
            "sport": "3d rogaining",
            "game": "airsoft",
        },
        "AB": {
            "music": "Berliner Schule composition",
            "solo": "Contemporary dance choreography",
            "creative": "IOT Engineer",
            "tech": "textile designer",
            "sport": "park/bowls skateboarding",
            "game": "bouldering",
        },
    },
    "F": {
        "O": {
            "music": "Weird pop composition",
            "solo": "freestyle swimming",
            "creative": "fantasy screen writer",
            "tech": "water colour painting",
            "sport": "open water swimming",
            "game": "field archery",
        },
        "A": {
            "music": "Glitch opera composition",
            "solo": "circuit bending",
            "creative": "soil piezoenergy engineer",
            "tech": "DIGITAL PROCESSING",
            "sport": "via ferrata",
            "game": "geocaching",
        },
        "B": {
            "music": "No wave / orchestral composition",
            "solo": "Street Skateboarding",
            "creative": "kinetic art",
            "tech": "acrylic/paint pour",
            "sport": "open water swimming",
            "game": "strategy board game",
        },
        "AB": {
            "music": "Experimental pop composition",
            "solo": "night time longboard",
            "creative": "Installation artist",
            "tech": "Darkroom photography",
            "sport": "aggressive inline",
            "game": "interactive media designer",
        },
    },
}

# SF: FOOD & PIGMENT CRAFT (Route 3, YELLOW, p↔s meridian)
# Peaks: r↑ s↑ h↑ — sensory foraging, pigment craft
SF_ACTIVITIES = {
    "M": {
        "O": {
            "music": "Electropop composition",
            "solo": "Kinetic Performance Art",
            "creative": "Agriculture waste product to materials engineer",
            "tech": "live sound engineer",
            "sport": "kitesurfing",
            "game": "generative art",
        },
        "A": {
            "music": "Glam rock composition",
            "solo": "clay modelling with hand",
            "creative": "Biofabrication engineer",
            "tech": "hydraulics engineer",
            "sport": "urban vegetable community gardening",
            "game": "3 cushion billiards",
        },
        "B": {
            "music": "Technical instrumental metal composition",
            "solo": "special forces agent",
            "creative": "geometric shape woodblock print",
            "tech": "taebo class",
            "sport": "obstacle course racing",
            "game": "b-boying",
        },
        "AB": {
            "music": "Exp. pop composition",
            "solo": "Installation Artist",
            "creative": "colourgel photography",
            "tech": "Professional Audax/randonneur",
            "sport": "night longboard",
            "game": "tobogganing",
        },
    },
    "F": {
        "O": {
            "music": "Chillwave composition",
            "solo": "tango",
            "creative": "Interface designer",
            "tech": "beach volleyball",
            "sport": "freestyle scooter",
            "game": "theme park ride designer",
        },
        "A": {
            "music": "Noise rock composition",
            "solo": "지역지리색채 소설 (regional geography novel)",
            "creative": "mixed media digital analogue collage",
            "tech": "rhythm roller skating",
            "sport": "upcycling",
            "game": "Freeride snowboard",
        },
        "B": {
            "music": "Ethereal composition",
            "solo": "Montessori",
            "creative": "marbling art ebru",
            "tech": "walking netball",
            "sport": "alps hiking",
            "game": "art gallery curator",
        },
        "AB": {
            "music": "Krautrock composition",
            "solo": "tennis doubles forward",
            "creative": "art gallery curator",
            "tech": "tent and trees puzzle",
            "sport": "tennis doubles forward",
            "game": "Historical Reenactment Designer",
        },
    },
}

GROUP_ACTIVITIES = {
    "NT": NT_ACTIVITIES,
    "NF": NF_ACTIVITIES,
    "ST": ST_ACTIVITIES,
    "SF": SF_ACTIVITIES,
}

# ============================================================
# MUSIC GENRES FROM MASTER CSV
# Use Genre_Release as primary music activity
# ============================================================

def get_music_from_master(master_row):
    """Extract music genre from master CSV row"""
    genre = master_row.get('Genre_Release', '').strip()
    if not genre:
        genre = master_row.get('Genre_Stress_Growth', '').strip()
    if not genre:
        genre = master_row.get('Genre_Extreme_Growth', '').strip()
    return genre

# ============================================================
# CIRCUIT ENTITY → ACTIVITY MAPPING
# Map circuit entities to concrete activities
# ============================================================
CIRCUIT_ACTIVITY_MAP = {
    # Geological nodes → earth science / engineering
    'podzol': 'soil science / podzol mapping',
    'fold_belt': 'geological fold belt survey',
    'laterite': 'laterite soil engineering',
    'laterite.q': 'laterite iron sequestration',
    'laterite.q_bar': 'laterite weathering analysis',
    'cambisol': 'cambisol soil classification',
    'cambisol.out1': 'cambisol maturity mapping',
    'craton': 'craton geological survey',
    'craton.out0': 'craton stability analysis',
    'craton.out1': 'craton core sampling',
    'subduction_zone': 'subduction zone modelling',
    'subduction_zone.out0': 'subduction dynamics simulation',
    'subduction_zone.out1': 'subduction seismic analysis',
    'basin': 'basin hydrology',
    'basin.q': 'basin sediment analysis',
    'basin.q_bar': 'basin drainage modelling',
    'plume': 'mantle plume modelling',
    'magnetite': 'magnetite geophysics',
    'magnetite.out0': 'magnetite survey',
    'pyrite': 'pyrite mineral analysis',
    'pyrite.out1': 'pyrite oxidation study',
    'monazite': 'monazite rare earth extraction',
    'monazite_thorium_and': 'monazite thorium processing',
    'large_igneous_province': 'igneous province mapping',
    'large_igneous_province.out0': 'LIP volcanic analysis',
    'lower_mantle': 'lower mantle geodynamics',
    'lower_mantle.q': 'lower mantle convection',
    'lower_mantle.q_bar': 'lower mantle state analysis',
    'outer_core_convection': 'outer core convection modelling',
    'outer_core_convection.out0': 'core convection simulation',
    'andosol.out0': 'volcanic ash soil mapping',
    'fold_belt.out1': 'fold belt structural analysis',
    'manganese_nodule': 'manganese nodule deep sea mining',
    'manganese_nodule.q': 'manganese nodule extraction',
    'manganese_nodule.q_bar': 'manganese nodule survey',
    'manganese_oxygen_complex': 'Mn oxidation engineering',
    'manganese_oxygen_complex.out1': 'Mn-O complex analysis',
    'oxidised_manganese': 'oxidised manganese processing',
    'oxidised_manganese.out0': 'Mn oxidation product',
    'oxidised_manganese.node': 'Mn oxidation node',
    'methionine': 'methionine metabolism study',
    'clay_gouge': 'clay gouge fault analysis',
    'methanogenesis': 'methanogenesis engineering',
    'methanogenesis.node': 'methane bioreactor',

    # Biochemical nodes → bio engineering
    'heme': 'heme synthesis research',
    'heme.out1': 'heme oxygenase study',
    'heme.node': 'heme protein engineering',
    'carbon': 'carbon cycle engineering',
    'carbon.q': 'carbon sequestration',
    'carbon.q_bar': 'carbon catabolism analysis',
    'co2': 'CO2 capture engineering',
    'co2.out0': 'CO2 dark energy release',
    'co2.out1': 'CO2 time energy storage',
    'water_vapour': 'water vapour cycle modelling',
    'water_vapour.out0': 'evapotranspiration modelling',
    'water_vapour.out1': 'water vapour photosynthesis',
    'water': 'water resource engineering',
    'water.out0': 'water purification',
    'sodium': 'sodium ion channel study',
    'sodium.out1': 'sodium pump research',
    'NaCl': 'NaCl electrolyte engineering',
    'NaCl.out1': 'NaCl proton pump study',
    'sulforaphane': 'sulforaphane Nrf2 activation',
    'sulforaphane.out0': 'Nrf2 pathway engineering',
    'sulforaphane.node': 'sulforaphane extraction',
    'histosol': 'histosol peatland restoration',
    'histosol.out1': 'peatland sulfur cycle',
    'histosol.node': 'peat soil engineering',
    'cysteine': 'cysteine redox engineering',
    'cysteine.node': 'cysteine synthesis',
    'ferritin': 'ferritin iron storage',
    'ferritin.out0': 'ferritin iron release',
    'ferritin.out1': 'ferritin iron sequestration',
    'ferritin.node': 'ferritin nanoparticle',
    'sulfur_iron_complex': 'Fe-S cluster engineering',
    'sulfur_iron_complex.out1': 'Fe-S electron transfer',
    'sulfur_iron_complex.node': 'Fe-S biogenesis',
    'nitrogenase': 'nitrogenase N2 fixation',
    'nitrogenase.out_2': 'nitrogenase MoFe analysis',
    'nitrogenase.out_3': 'nitrogenase Fe protein',
    'nitrogenase.node': 'biological nitrogen fixation',
    'pentose_phosphate': 'pentose phosphate pathway',
    'pentose_phosphate.out_2': 'PPP NADPH production',
    'pentose_phosphate.node': 'PPP metabolic engineering',
    'disulfide_bond': 'disulfide bond engineering',
    'disulfide_bond.node': 'protein folding study',
    'collagen': 'collagen biomaterials',
    'collagen.node': 'collagen tissue engineering',
    'actomyosin': 'actomyosin motor study',
    'actomyosin.out1': 'actomyosin contraction',
    'actomyosin_ctrl.out': 'actomyosin control',
    'actomyosin.node': 'actomyosin dynamics',
    'actomyosin.out0': 'actomyosin force',
    'mycorradicin': 'mycorradicin AM symbiosis',
    'mycorradicin.out0': 'mycorradicin C-stress',
    'mycorradicin.node': 'mycorrhizal signalling',
    'peonidine': 'peonidine anthocyanin study',
    'peonidine.out1': 'peonidine antioxidant',
    'peonidine.node': 'peonidine pigment',
    'methylation': 'DNA methylation study',
    'methylation.out1': 'methylation epigenetics',
    'methylation.node': 'methyltransferase',
    'glp1': 'GLP-1 metabolic study',
    'glp1.q_bar': 'GLP-1 receptor analysis',
    'glp1.node': 'GLP-1 agonist research',
    'glymphatic_system': 'glymphatic clearance',
    'glymphatic_system.node': 'glymphatic flow modelling',
    'aurora': 'aurora geophysics',
    'aurora.out0': 'aurora EM emission',
    'aurora.node': 'aurora plasma study',
    'cytochrome_c_oxidase': 'COX enzyme engineering',
    'cytochrome_c_oxidase.out1': 'COX proton pump',
    'cytochrome_c_oxidase.node': 'COX electron transfer',
    'succinate_dehydrogenase': 'succinate dehydrogenase study',
    'succinate_dehydrogenase.node': 'TCA cycle complex II',
    'lactate_dehydrogenase': 'lactate metabolism',
    'lactate_dehydrogenase.out1': 'LDH anaerobic study',
    'lactate_dehydrogenase.node': 'LDH enzyme',
    'memory_entropy': 'memory entropy computation',
    'memory_entropy.out_co2': 'memory entropy CO2',
    'memory_entropy.out_hind_insula': 'memory entropy insula',
    'memory_entropy.node': 'memory entropy modelling',
    'mc1r': 'MC1R melanin study',
    'mc1r.q_bar': 'MC1R seal release',
    'mc1r.node': 'MC1R pigmentation',
    'gluon_orogen': 'gluon orogeny',
    'gluon_orogen.q_bar': 'gluon orogen seal',
    'gluon_orogen.node': 'gluon field modelling',
    'chlorine_ion_pump': 'chlorine ion pump',
    'chlorine_ion_pump.out1': 'Cl- cryptobiosis',
    'chlorine_ion_pump.node': 'Cl- transport',
    'adapter_protein': 'adapter protein signalling',
    'adapter_protein.q_bar': 'adapter protein state',
    'adapter_protein.node': 'pattern recognition',
    'substance_p': 'substance P neurokinin',
    'substance_p.out_autophagy': 'SP autophagy signal',
    'substance_p.node': 'SP receptor study',
    'autophagy': 'autophagy research',
    'autophagy.out0': 'autophagy flux',
    'autophagy.node': 'autophagy pathway',
    'cck': 'CCK cholecystokinin',
    'cck.node': 'CCK satiety study',
    'male_right_oxytocin': 'oxytocin signalling',
    'male_right_oxytocin.q_bar': 'oxytocin receptor',
    'male_right_oxytocin.node': 'oxytocin study',
    'right_sole_dopamine': 'sole dopamine',
    'right_sole_dopamine.q_bar': 'sole DA receptor',
    'right_sole_dopamine.node': 'peripheral dopamine',
    'LeftD2': 'D2 receptor study',
    'LeftD2.node': 'dopamine D2',
    'none_observer': 'non-observer baseline',
    'none_observer.node': 'non-observer study',
    'right_acetylcholine': 'acetylcholine study',
    'right_acetylcholine.node': 'ACh signalling',
    'pi_electron_cloud': 'pi electron cloud',
    'pi_electron_cloud.node': 'aromatic system',
    'hind_insula': 'hind insula study',
    'hind_insula.node': 'insula processing',
    'heath_aerenchyma': 'aerenchyma oxygen',
    'heath_aerenchyma.out0': 'aerenchyma flooding',
    'heath_aerenchyma.node': 'plant oxygen transport',
    'steel': 'steel metallurgy',
    'steel.out1': 'steel alloy',
    'steel.node': 'steel engineering',
    'caco3': 'calcium carbonate',
    'caco3.node': 'CaCO3 biomineral',
    'thorium': 'thorium nuclear',
    'thorium.node': 'thorium fuel cycle',
    'plume_out0_nand': 'plume NAND gate',
    'monazite_thorium_and': 'monazite AND gate',

    # Placeholder/exotic
    'neutron_star_matter_121': 'neutron star matter',
    'gravitational_wave_126': 'gravitational wave',
    'dark_matter_119': 'dark matter',
    'dark_energy_124': 'dark energy',
    'primordial_black_hole_125': 'primordial black hole',
    'exotic_matter_120': 'exotic matter',
    'cosmic_ray_123': 'cosmic ray',
    'black_hole_accretion_122': 'black hole accretion',
    'gold_197_placeholder': 'gold-197',
    'oxygen_16_placeholder': 'oxygen-16',
}

# ============================================================
# MAIN: Parse input CSV, fix activities, write output
# ============================================================

def parse_profile_key(profile_str):
    """Parse 'ENTP_AB_M' → ('ENTP', 'AB', 'M')"""
    parts = profile_str.split('_')
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    return None, None, None

def is_empty_or_wrong(val):
    """Check if a slot is empty or clearly wrong"""
    if not val or val.strip() == '':
        return True
    v = val.strip()
    # Single characters, placeholder values
    if v in ('d', '9', '?', 'x', '-', 'drum, piano, cello, guitar'):
        return True
    # Very short meaningless entries
    if len(v) <= 2 and not v.isupper():
        return True
    return False

def generate_activity_for_slot(slot_idx, mbti, blood, gender, group, master_row, existing_val):
    """Generate corrected activity for a given slot"""
    attitude = get_attitude(mbti)
    att = ATTITUDE_MOD[attitude]
    bm = BLOOD_MOD[blood]
    ga = GROUP_ACTIVITIES[group]

    # Get the activity set for this profile
    if gender in ga and blood in ga[gender]:
        act_set = ga[gender][blood]
    else:
        act_set = {}

    # Slot mapping:
    # 0: time_slot (keep from CSV)
    # 1: profile (keep from CSV)
    # 2: music composition
    # 3: solo/recreational
    # 4: creative/artistic
    # 5: professional/technical
    # 6: sport
    # 7: game/puzzle
    # (CSV columns: 0=time, 1=profile, 2=music, 3=solo, 4=creative, 5=tech, 6=sport, 7=game, 8+=extra)

    # Map slot indices to activity keys
    slot_map = {
        2: 'music',
        3: 'solo',
        4: 'creative',
        5: 'tech',
        6: 'sport',
        7: 'game',
    }

    # If existing value is valid, keep it
    if existing_val and not is_empty_or_wrong(existing_val):
        return existing_val.strip()

    # Generate from activity set
    key = slot_map.get(slot_idx)
    if key and key in act_set:
        return act_set[key]

    # Fallback: use circuit entity from master
    circuit = master_row.get('Circuit_Entity', '').strip() if master_row else ''
    if circuit in CIRCUIT_ACTIVITY_MAP:
        return CIRCUIT_ACTIVITY_MAP[circuit]

    # Ultimate fallback
    return f"{bm['label']} {group} activity"

def main():
    master = parse_master()
    print(f"Loaded {len(master)} master profiles")

    # Parse input CSV
    rows = []
    # Try utf-8 first, fall back to euc-kr (Korean encoding)
    # NOTE: This CSV has NO header row — first row is data (ENTP_AB_M)
    try:
        with open(INPUT_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
    except UnicodeDecodeError:
        with open(INPUT_PATH, 'r', encoding='euc-kr') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)

    # Build header from max row length
    max_cols = max(len(r) for r in rows) if rows else 0
    header = ['TimeSlot', 'Profile', 'Music', 'Solo', 'Creative', 'Tech', 'Sport', 'Game'] + [f'Extra{i}' for i in range(8, max_cols)]

    print(f"Loaded {len(rows)} activity rows")

    # Deduplicate: keep first occurrence of each profile
    seen_profiles = set()
    deduped_rows = []
    for row in rows:
        if len(row) >= 2:
            prof = row[1].strip()
            if prof in seen_profiles:
                print(f"  Skipping duplicate: {prof}")
                continue
            seen_profiles.add(prof)
        deduped_rows.append(row)
    rows = deduped_rows

    # Find missing profiles and insert them with empty slots
    master_order = list(master.keys())
    missing = [k for k in master_order if k not in seen_profiles]
    if missing:
        print(f"Missing profiles to add: {missing}")
        for prof in missing:
            mrow = master[prof]
            time_slot = f"{mrow.get('Slot_Start','')}-{mrow.get('Slot_End','')}"
            empty_row = [time_slot, prof, '', '', '', '', '', '']
            rows.append(empty_row)

    # Sort rows by master CSV order
    master_idx = {k: i for i, k in enumerate(master_order)}
    rows.sort(key=lambda r: master_idx.get(r[1].strip() if len(r) > 1 else '', 999))

    print(f"Final row count: {len(rows)}")

    # Process each row
    output_rows = []
    fixes = 0
    empties_filled = 0

    for row in rows:
        if len(row) < 2:
            output_rows.append(row)
            continue

        time_slot = row[0] if len(row) > 0 else ''
        profile = row[1] if len(row) > 1 else ''

        mbti, blood, gender = parse_profile_key(profile)
        if not mbti:
            output_rows.append(row)
            continue

        group = get_group(mbti)
        if not group:
            output_rows.append(row)
            continue

        master_key = f"{mbti}_{blood}_{gender}"
        master_row = master.get(master_key, {})

        # Build corrected row
        new_row = [time_slot, profile]

        # Process slots 2-7 (indices 2-7 in the row)
        for slot_idx in range(2, min(8, len(row))):
            existing = row[slot_idx] if slot_idx < len(row) else ''
            was_empty = is_empty_or_wrong(existing)
            corrected = generate_activity_for_slot(slot_idx, mbti, blood, gender, group, master_row, existing)
            new_row.append(corrected)
            if was_empty:
                empties_filled += 1
            elif corrected != existing.strip():
                fixes += 1

        # Preserve any extra columns beyond slot 7
        for i in range(8, len(row)):
            new_row.append(row[i])

        # Pad if original was shorter
        while len(new_row) < len(header):
            new_row.append('')

        output_rows.append(new_row)

    # Write output
    with open(OUTPUT_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in output_rows:
            writer.writerow(row)

    print(f"Fixed {fixes} wrong activities, filled {empties_filled} empty slots")
    print(f"Output: {OUTPUT_PATH}")

    # Verify all 128 profiles present
    profiles_seen = set()
    for row in output_rows:
        if len(row) >= 2:
            profiles_seen.add(row[1])
    print(f"Profiles in output: {len(profiles_seen)}")

    # Check for any remaining empties
    remaining_empties = 0
    for row in output_rows:
        for i in range(2, min(8, len(row))):
            if is_empty_or_wrong(row[i]):
                remaining_empties += 1
                print(f"  EMPTY: {row[1]} slot {i}")
    if remaining_empties == 0:
        print("All slots filled!")
    else:
        print(f"Remaining empties: {remaining_empties}")

if __name__ == "__main__":
    main()
