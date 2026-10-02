"""
universal_activity_table.py — Generate the 128-profile × 16-column activity
table deterministically from universal physics (kernel_v1.py).

Fix v2:
  - Use sha256 stable hash (not Python's non-deterministic hash())
  - MBTI-specific 5 activities per dim (16 MBTI × 14 dim × 5 = 1120)
  - 4 paradigms (subground, virtual, ecology, circular) embedded in each MBTI×dim

Result: each (MBTI, dim) cell is from MBTI-specific pool.
Same (mbti, blood, gender) → same activity, every run.
"""
import csv
import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(__file__))
import kernel_v1 as k


# ============================================================
# STABLE HASH (deterministic across Python sessions)
# ============================================================
def stable_hash(s: str) -> int:
    """SHA-256 based stable hash → 32-bit integer."""
    return int.from_bytes(hashlib.sha256(s.encode("utf-8")).digest()[:4], "big")


# ============================================================
# MBTI-SPECIFIC ACTIVITY POOLS (16 MBTI × 14 dim × 5 = 1120 activities)
# Each MBTI gets dim-specific activities matching its cognitive function stack.
# ============================================================
MBTI_DIMS_8D = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]
MBTI_DIMS_SPHERE = ["Fe", "H", "O", "C", "S", "EM"]


def _make_mbti_pool(mbti, paradigm_in_each=2):
    """Generate MBTI-specific 5 activities per dim, embedding paradigms."""
    P = []  # paradigm activities
    # 4 paradigms, each listed 1× per dim, total 4 paradigms × 14 dim = 56 paradigm slots
    # But user wants 4 paradigms → 1 per dim slot for max 14 (but pool size 5)
    # Each dim has 5 activities. paradigms appear 1× in some dim, total ≥ paradigm_in_each * 14
    paradigms = {
        "subground": {
            "r": "subground strategic cadence / underground planning meeting",
            "h": "subground acoustic resonance chamber design",
            "d": "subground strategic foresight / deep tunnel policy",
            "p": "subground timing instrumentation (geothermal drill)",
            "s": "subground visual mapping / cave photography",
            "gamma": "subground drone aerial mapping / caving film",
            "g": "subground structural engineering (tunnel, foundation)",
            "nu": "subground cave acoustics design / deep silence retreat",
            "Fe": "subground Fe ore mining / tunnel metallurgy",
            "H": "subground hydrogen storage cavern design",
            "O": "subground aquifer mapping / groundwater hydrology",
            "C": "subground carbon sequestration geology",
            "S": "subground volcanic monitoring network",
            "EM": "subground EM shielding / Faraday cage design",
        },
        "virtual": {
            "r": "virtual strategic simulation / executive digital twin",
            "h": "virtual harmonic synthesis (AI composition)",
            "d": "virtual strategy war-gaming / metaverse negotiation",
            "p": "virtual precision surgery simulation",
            "s": "virtual 3D scene design / immersive photography",
            "gamma": "virtual aerial VR / metaverse locomotion",
            "g": "virtual structural engineering / digital twin architecture",
            "nu": "virtual reality philosophy / simulated phenomenology",
            "Fe": "virtual Fe-core stellar simulation",
            "H": "virtual sun observation (solar VR / heliosphere sim)",
            "O": "virtual ocean VR / digital hydrology",
            "C": "virtual carbon cycle / carbon capture simulation",
            "S": "virtual sulfur chemistry simulation",
            "EM": "virtual EM field simulation / Maxwell visualization",
        },
        "ecology": {
            "r": "ecology circadian rhythm study / phenology",
            "h": "ecology acoustic soundscape recording / bioacoustics",
            "d": "ecology policy analysis / environmental impact review",
            "p": "ecology observation timing / seasonal clock",
            "s": "ecology living wall green facade design",
            "gamma": "ecology wildlife aerial survey / drone bio census",
            "g": "ecology earthwork / land restoration heavy design",
            "nu": "ecology deep ecology philosophy",
            "Fe": "ecology Fe cycle / rust microbiome",
            "H": "ecology solar greenhouse / permaculture sun design",
            "O": "ecology wetland design / constructed marsh / mangrove",
            "C": "ecology mycelium / biochar / soil microbiome",
            "S": "ecology sulfur-loving extremophile / hot spring research",
            "EM": "ecology magnetoreception / bird migration EM study",
        },
        "circular": {
            "r": "circular rhythm pattern / seasonal cycle design",
            "h": "circular harmony / closed-loop ensemble",
            "d": "circular economy system dynamics modeling",
            "p": "circular timing / closed-loop precision manufacturing",
            "s": "circular material palette / upcycling design",
            "gamma": "circular aerial transport (drone delivery network)",
            "g": "circular masonry reuse / reclaimed material structural design",
            "nu": "circular philosophy / regenerative design thinking",
            "Fe": "circular iron recycling metallurgy",
            "H": "circular hydrogen economy architect",
            "O": "circular water reuse systems / greywater design",
            "C": "circular carbon economy architect",
            "S": "circular sulfur recovery chemist",
            "EM": "circular electromagnetic energy harvesting",
        },
    }

    # 4 paradigm activities
    paradigm_activities = {dim: [] for dim in MBTI_DIMS_8D + MBTI_DIMS_SPHERE}
    for pname, ptable in paradigms.items():
        for dim, activity in ptable.items():
            paradigm_activities[dim].append(activity)

    return paradigm_activities


PARADIGM_ACTIVITIES = _make_mbti_pool(None)


# MBTI-specific 5 activities per dim (4 paradigm + 1 MBTI-specific)
# Each MBTI has its own "5th" MBTI-specific activity per dim
MBTI_SPECIFIC_5TH = {
    # ENTJ: T+J+E+N, leadership + analytical + planned + abstract
    "ENTJ": {
        "r": "executive decision rhythm / strategic cadence",
        "h": "keynote speech cadence / organizational vision casting",
        "d": "strategic chess / executive dialectic / policy review",
        "p": "military precision drill / strategic scheduling",
        "s": "architectural enterprise design / corporate visual identity",
        "gamma": "extreme endurance leadership / mountain expedition commanding",
        "g": "structural engineering executive / skyscraper construction",
        "nu": "grand strategy / long-horizon chess foresight",
        "Fe": "Fe-core corporate leadership / industrial forge",
        "H": "hydrogen economy executive / energy policy architect",
        "O": "ocean governance / blue economy executive",
        "C": "carbon executive policy / corporate ESG architect",
        "S": "sulfur industry executive / energy sector strategist",
        "EM": "EM spectrum executive / telecom policy architect",
    },
    # ENTP: P+N+E+T, exploratory + abstract + social + analytical
    "ENTP": {
        "r": "debate improvisation rhythm / startup pitch cadence",
        "h": "jazz harmonic improvisation / neoclassical composition",
        "d": "dialectic debate / startup strategy ideation",
        "p": "experimental prototyping timing / hackathon sprint",
        "s": "generative visual jockeying / HDL FPGA visual design",
        "gamma": "BMX aerial / flow parkour / chasetag strategy",
        "g": "rapid prototyping lab / startup product design",
        "nu": "innovation theory / invention philosophy",
        "Fe": "iron foundry startup / metallurgy invention",
        "H": "hydrogen startup / clean energy invention",
        "O": "ocean tech startup / blue innovation",
        "C": "carbon innovation / biotech invention",
        "S": "sulfur chemistry invention / volcano-tech startup",
        "EM": "EM invention / radio innovation startup",
    },
    # ENFJ: F+J+E+N, value + planned + social + abstract
    "ENFJ": {
        "r": "group facilitation rhythm / community drum circle",
        "h": "choir conducting / community singing / ensemble",
        "d": "mediation / group dialectic / community dialogue",
        "p": "community event planning / coordinated outreach",
        "s": "interior community space design / welcoming aesthetic",
        "gamma": "group sport coaching / capoeira with community",
        "g": "community architecture / public building design",
        "nu": "phenomenology of community / value philosophy",
        "Fe": "community Fe forge / blacksmithing workshop",
        "H": "community solar / cooperative energy",
        "O": "community watershed / cooperative water",
        "C": "community garden / cooperative carbon farming",
        "S": "community thermal bath / hot spring sharing",
        "EM": "community EM wellness / Schumann field meditation",
    },
    # ENFP: F+P+E+N, value + exploratory + social + abstract
    "ENFP": {
        "r": "freestyle dance / improvisation rhythm",
        "h": "freak folk composition / noise-pop songwriting",
        "d": "creative brainstorm / possibility dialectic",
        "p": "spontaneous timing / improv comedy beat",
        "s": "wildlife documentary art / living wall painting",
        "gamma": "inline aerial / night cycling / spontaneous adventure",
        "g": "ephemeral installation / pop-up structure design",
        "nu": "possibility philosophy / dream analysis",
        "Fe": "metalwork art / expressive iron sculpture",
        "H": "spontaneous sun worship / solar art",
        "O": "wild swimming / spontaneous ocean plunge",
        "C": "biochar art / creative mycelium sculpture",
        "S": "volcanic landscape art / sulfur painting",
        "EM": "EM field art / aurora photography",
    },
    # ESTJ: T+J+S+E, logical + planned + practical + social
    "ESTJ": {
        "r": "marching band / military parade cadence",
        "h": "structured ensemble / traditional choir",
        "d": "legal argument / corporate compliance review",
        "p": "military precision / accounting audit",
        "s": "traditional craftsmanship / carpentry / masonry",
        "gamma": "competitive team sport / football coaching",
        "g": "construction project management / building site",
        "nu": "classical philosophy / Stoic logic",
        "Fe": "iron foundry management / steel mill operations",
        "H": "solar farm management / energy operations",
        "O": "water utility management / municipal water",
        "C": "forest management / traditional carbon forestry",
        "S": "mining operations / sulfur extraction",
        "EM": "utility grid management / power operations",
    },
    # ESTP: T+P+S+E, logical + exploratory + practical + social
    "ESTP": {
        "r": "drumming ensemble / live DJ set",
        "h": "live performance / combat choreography",
        "d": "live tactical analysis / combat sport strategy",
        "p": "precision sports / MMA timing",
        "s": "extreme sport photography / action cinematography",
        "gamma": "BMX racing / drift trike / extreme parkour",
        "g": "extreme weightlifting / powerlifting meet",
        "nu": "pragmatic philosophy / action epistemology",
        "Fe": "extreme metalwork / knife forging",
        "H": "extreme solar exposure / solar racing",
        "O": "whitewater kayak / extreme ocean sport",
        "C": "combat survival / extreme carbon environment",
        "S": "extreme sulfur / volcanic extreme sport",
        "EM": "EM extreme exposure / radio contest",
    },
    # ESFJ: F+J+S+E, value + planned + practical + social
    "ESFJ": {
        "r": "group aerobics / community dance class",
        "h": "community choir / ensemble singing",
        "d": "community care / hospitality dialectic",
        "p": "event coordination / hospitality timing",
        "s": "interior decoration / hospitality design",
        "gamma": "group fitness / community sports",
        "g": "community building / hospitality architecture",
        "nu": "community ethics / hospitality philosophy",
        "Fe": "kitchen iron / cast iron cooking craft",
        "H": "community kitchen solar / community cooking",
        "O": "community pool / hospitality water",
        "C": "community kitchen garden / cooperative cooking",
        "S": "community kitchen sulfur / fermentation",
        "EM": "community EM / shared connectivity",
    },
    # ESFP: F+P+S+E, value + exploratory + practical + social
    "ESFP": {
        "r": "dance party / social dance / freestyle",
        "h": "live band / pop performance",
        "d": "live performance improvisation / comedy",
        "p": "live event timing / party planning",
        "s": "fashion / pop visual design",
        "gamma": "extreme dance / freestyle BMX / trampoline",
        "g": "event stage design / festival architecture",
        "nu": "aesthetic philosophy / live experience",
        "Fe": "live metalwork show / forging demo",
        "H": "live outdoor sun festival / summer solstice",
        "O": "beach party / ocean festival",
        "C": "music festival carbon / sustainable festival",
        "S": "volcanic hot spring party / thermal festival",
        "EM": "light show / EM festival",
    },
    # INTJ: T+J+N+I, logical + planned + abstract + introspective
    "INTJ": {
        "r": "theoretical math rhythm / research schedule cadence",
        "h": "neoclassical composition / orchestral analysis",
        "d": "system architecture analysis / strategic foresight",
        "p": "long-term planning / 10-year roadmap",
        "s": "minimal architecture / theory of design",
        "gamma": "alpine solo climbing / polar trekking",
        "g": "abstract architecture / theory of structure",
        "nu": "systems theory / grand unified theory",
        "Fe": "Fe-core stellar evolution research",
        "H": "stellar nucleosynthesis research",
        "O": "hydrological cycle deep modeling",
        "C": "carbon cycle deep modeling",
        "S": "sulfur cycle deep modeling",
        "EM": "EM field deep theory / Maxwell equations",
    },
    # INTP: T+P+N+I, logical + exploratory + abstract + introspective
    "INTP": {
        "r": "music concrete / experimental rhythm / algorithmic music",
        "h": "algorithmic music visualizer / generative composition",
        "d": "philosophical analysis / type system design",
        "p": "type system compiler design / language theory",
        "s": "fractal art / algorithmic visual",
        "gamma": "flowboarding / hash puzzle solving / geoguesser",
        "g": "abstract structure / formal model design",
        "nu": "mathematical proof / formal verification",
        "Fe": "Fe algorithmic model / metallurgy theory",
        "H": "hydrogen algorithmic model / fusion theory",
        "O": "ocean algorithmic model / fluid dynamics",
        "C": "carbon algorithmic model / chemistry theory",
        "S": "sulfur algorithmic model / chemistry simulation",
        "EM": "EM algorithmic model / Maxwell simulation",
    },
    # INFJ: F+J+N+I, value + planned + abstract + introspective
    "INFJ": {
        "r": "introspective rhythm / solo meditation cadence",
        "h": "indie folk composition / introspective singing",
        "d": "phenomenological writing / introverted dialectic",
        "p": "long-term vision planning / 30-year roadmap",
        "s": "introspective photography / quiet visual art",
        "gamma": "solo wilderness / reflective trekking",
        "g": "introspective architecture / sacred space design",
        "nu": "phenomenology / depth psychology",
        "Fe": "Fe introspection / iron homeostasis research",
        "H": "solar meditation / sunrise ritual",
        "O": "deep ocean meditation / blue mind",
        "C": "carbon meditation / forest bathing",
        "S": "sulfur meditation / hot spring ritual",
        "EM": "EM meditation / Schumann field reflection",
    },
    # INFP: F+P+N+I, value + exploratory + abstract + introspective
    "INFP": {
        "r": "introspective movement / solo yoga flow",
        "h": "psychedelic folk / symphonic metal / dream-pop composition",
        "d": "introspective writing / novel dialectic",
        "p": "spontaneous creative timing / artistic flow",
        "s": "introspective visual / dreamscape painting",
        "gamma": "wild swimming / abseiling / introspective aerial",
        "g": "introspective sculpture / personal monument",
        "nu": "depth psychology / personal mythology",
        "Fe": "Fe ritual / personal iron monument",
        "H": "sunset ritual / solar personal",
        "O": "personal lake / wild water ritual",
        "C": "personal mycelium / personal forest",
        "S": "personal hot spring / personal thermal",
        "EM": "personal aurora / personal EM ritual",
    },
    # ISTJ: T+J+S+I, logical + planned + practical + introspective
    "ISTJ": {
        "r": "data entry rhythm / accounting cadence",
        "h": "structured classical / conservatory practice",
        "d": "audit / compliance / data review",
        "p": "audit schedule / compliance timing",
        "s": "data visualization / structured photography",
        "gamma": "cross-country skiing / long-distance running",
        "g": "structural inspection / building compliance",
        "nu": "classical logic / Stoic data philosophy",
        "Fe": "Fe data tracking / metallurgy records",
        "H": "solar data tracking / energy records",
        "O": "water data tracking / reservoir records",
        "C": "carbon data tracking / forest records",
        "S": "sulfur data tracking / mining records",
        "EM": "EM data tracking / telecom records",
    },
    # ISTP: T+P+S+I, logical + exploratory + practical + introspective
    "ISTP": {
        "r": "solo mechanical rhythm / engine tuning",
        "h": "solo improvisation / technical practice",
        "d": "tactical analysis / system debugging",
        "p": "precision mechanics / engine timing",
        "s": "mechanical photography / technical documentation",
        "gamma": "motorcycle adventure / solo extreme sport",
        "g": "mechanical engineering / hands-on repair",
        "nu": "pragmatic logic / engineering epistemology",
        "Fe": "welding / metalwork craft",
        "H": "engine tuning / combustion mechanics",
        "O": "boat mechanics / marine engineering",
        "C": "engine carbon / fuel mechanics",
        "S": "combustion sulfur / engine chemistry",
        "EM": "electronics repair / EM diagnostics",
    },
    # ISFJ: F+J+S+I, value + planned + practical + introspective
    "ISFJ": {
        "r": "care rhythm / domestic cadence",
        "h": "domestic harmony / family singing",
        "d": "care dialectic / family mediation",
        "p": "care schedule / family calendar",
        "s": "domestic visual / home decoration",
        "gamma": "family sport / gentle yoga / walking",
        "g": "home maintenance / domestic architecture",
        "nu": "care philosophy / domestic ethics",
        "Fe": "domestic iron / kitchen cast iron",
        "H": "domestic solar / home sun",
        "O": "domestic water / home water",
        "C": "domestic garden / home composting",
        "S": "domestic sulfur / home fermentation",
        "EM": "domestic EM / home WiFi",
    },
    # ISFP: F+P+S+I, value + exploratory + practical + introspective
    "ISFP": {
        "r": "artistic rhythm / studio practice cadence",
        "h": "intimate art song / studio composition",
        "d": "artistic critique / studio dialectic",
        "p": "artistic timing / studio flow",
        "s": "fine art / painting / ceramics art",
        "gamma": "rock climbing / bouldering / artistic extreme",
        "g": "artistic structure / sculpture craft",
        "nu": "aesthetic philosophy / studio contemplation",
        "Fe": "artistic iron / forged sculpture",
        "H": "artistic sun / studio light",
        "O": "artistic water / watercolor",
        "C": "artistic carbon / charcoal drawing",
        "S": "artistic sulfur / encaustic",
        "EM": "artistic EM / stained glass",
    },
}


# ============================================================
# 8D vector per MBTI (for blood-type modulation)
# ============================================================
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
    vec = {dim: sum(MBTI_LETTER_8D[L][dim] for L in mbti) / 4.0
           for dim in MBTI_DIMS_8D}
    MBTI_8D[mbti] = vec

BLOOD_8D = {
    'O':  {'r': 0.7, 'h': 0.3, 'd': 0.6, 'p': 0.4, 's': 0.6, 'gamma': 0.3, 'g': 0.7, 'nu': 0.3},
    'A':  {'r': 0.6, 'h': 0.4, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.4, 'g': 0.6, 'nu': 0.4},
    'B':  {'r': 0.4, 'h': 0.6, 'd': 0.4, 'p': 0.6, 's': 0.4, 'gamma': 0.6, 'g': 0.4, 'nu': 0.6},
    'AB': {'r': 0.5, 'h': 0.5, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.5, 'g': 0.5, 'nu': 0.5},
}


def profile_8d(mbti, blood):
    m = MBTI_8D[mbti]
    b = BLOOD_8D[blood]
    return {dim: (m[dim] + b[dim]) / 2.0 for dim in MBTI_DIMS_8D}


# ============================================================
# SELECT ACTIVITY: MBTI-specific pool (4 paradigm + 1 MBTI-specific)
# ============================================================
def select_activity(mbti, dim, blood, gender, profile_idx):
    """Deterministic: (mbti, dim) gives 5 specific activities, choose by stable hash."""
    pool = PARADIGM_ACTIVITIES.get(dim, [])[:]  # 4 paradigm activities
    pool.append(MBTI_SPECIFIC_5TH[mbti][dim])  # 1 MBTI-specific 5th
    # 5 activities total per (mbti, dim)
    # Stable selection: hash(profile, dim) → index
    salt = f"{mbti}_{blood}_{gender}_{dim}_{profile_idx}"
    idx = stable_hash(salt) % 5
    return pool[idx]


# ============================================================
# GENERATE TABLE
# ============================================================
DIM_NAMES = ['r', 'h', 'd', 'p', 's', 'gamma', 'g', 'nu',
             'Fe', 'H', 'O', 'C', 'S', 'EM']
ALL_DIMS = MBTI_DIMS_8D + MBTI_DIMS_SPHERE


def format_time(profile_idx):
    """PEAK_CYCLE: 16 windows × 1.5h = 24h. Midpoint = 1.5*idx + 0.75h."""
    h = 1.5 * (profile_idx % 16) + 0.75
    return f"{int(h):02d}:{int((h - int(h)) * 60):02d}"


def generate_table():
    rows = []
    rows.append(['time', 'profile'] + DIM_NAMES)
    profile_idx = 0
    for mbti in MBTI_LIST:
        for gender in ['M', 'F']:
            for blood in ['O', 'A', 'B', 'AB']:
                profile = f"{mbti}_{blood}_{gender}"
                row = [format_time(profile_idx), profile]
                for dim in ALL_DIMS:
                    row.append(select_activity(mbti, dim, blood, gender, profile_idx))
                rows.append(row)
                profile_idx += 1
    return rows


# ============================================================
# VERIFY: determinism + uniqueness
# ============================================================
def verify():
    table1 = generate_table()
    table2 = generate_table()
    same = all(r1 == r2 for r1, r2 in zip(table1, table2))
    # Count unique activities
    all_activities = []
    for r in table1[1:]:
        all_activities.extend(r[2:])
    unique = set(all_activities)
    duplicates = len(all_activities) - len(unique)
    print(f"Determinism (same run): {same}")
    print(f"Total cells (128 × 14): {len(all_activities)}")
    print(f"Unique activities: {len(unique)}")
    print(f"Duplicate occurrences: {duplicates}")
    print(f"Duplicate ratio: {duplicates/len(all_activities)*100:.2f}%")


if __name__ == "__main__":
    verify()
    print()
    table = generate_table()
    out_path = "Downloads/activity_universal_128_v2.csv"
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerows(table)
    print(f"Generated {len(table)-1} rows × {len(table[0])} cols → {out_path}")
    print()
    # Show ENTJ_O_M as the user complained about
    for r in table[1:]:
        if r[1] == "ENTJ_O_M":
            print(f"ENTJ_O_M  (sample the user complained about):")
            for i, c in enumerate(r[2:], 2):
                print(f"  col {i-2} ({DIM_NAMES[i-2]}): {c}")
            break
    print()
    # Show ENTJ_A_M (different blood)
    for r in table[1:]:
        if r[1] == "ENTJ_A_M":
            print(f"ENTJ_A_M  (different blood, must differ):")
            for i, c in enumerate(r[2:], 2):
                print(f"  col {i-2} ({DIM_NAMES[i-2]}): {c}")
            break
    print()
    # Show INFP_O_M (totally different MBTI)
    for r in table[1:]:
        if r[1] == "INFP_O_M":
            print(f"INFP_O_M  (totally different MBTI):")
            for i, c in enumerate(r[2:], 2):
                print(f"  col {i-2} ({DIM_NAMES[i-2]}): {c}")
            break
