"""
128 성격 × 4 창의적 활동 모양 v3
8D 벡터에서 장르+운동+기술+형용사/루프모양을 생성 규칙으로 만듦
2.csv 스타일이지만 복사가 아닌 생성. 128개 전부 유일.
음식 없음. 활동만.
"""

import json
import math
from typing import Dict, List, Tuple

# ============================================================
# 1. 8D IMPEDANCE (from _slot_mapping.py)
# ============================================================

MBTI_8D = {
    0:  ('r', 1.0, 's', 0.6, 'nu', 0.3),
    1:  ('h', 1.0, 'gamma', 0.6, 'nu', 0.3),
    2:  ('d', 1.0, 'h', 0.6, 'g', 0.3),
    3:  ('p', 1.0, 'nu', 0.6, 'h', 0.3),
    4:  ('s', 1.0, 'r', 0.6, 'nu', 0.3),
    5:  ('gamma', 1.0, 'h', 0.6, 'p', 0.3),
    6:  ('g', 1.0, 's', 0.6, 'r', 0.3),
    7:  ('nu', 1.0, 'p', 0.6, 'd', 0.3),
    8:  ('r', 0.8, 'h', 0.8, 'gamma', 0.4),
    9:  ('h', 1.0, 'p', 0.6, 'nu', 0.3),
    10: ('s', 1.0, 'gamma', 0.6, 'r', 0.3),
    11: ('d', 1.0, 'g', 0.6, 'p', 0.3),
    12: ('g', 1.0, 'd', 0.6, 'p', 0.3),
    13: ('h', 1.0, 'gamma', 0.6, 'nu', 0.3),
    14: ('g', 1.0, 'gamma', 0.6, 'h', 0.3),
    15: ('d', 1.0, 'gamma', 0.6, 'g', 0.3),
}

MBTI_NAMES = {0:'ENFP',1:'ISFP',2:'ESFJ',3:'INTP',4:'ENTP',5:'INFJ',6:'ESTP',7:'ISTP',
              8:'ENFJ',9:'INTJ',10:'ESFP',11:'ISTJ',12:'ESTJ',13:'INFP',14:'ISFJ',15:'ENTJ'}

BLOOD_WEIGHT = {0: 1.0, 1: 0.75, 2: 0.60, 3: 0.50}
BLOOD_NAMES = {0:'O',1:'A',2:'B',3:'AB'}

def flow(g):
    if g == 0:
        return {'r': 0.8, 'h': 0.5, 'd': 1.0, 'p': 0.5, 's': 0.6, 'gamma': 0.9, 'g': 0.4, 'nu': 0.5}
    else:
        return {'r': 0.6, 'h': 0.9, 'd': 0.4, 'p': 0.5, 's': 0.7, 'gamma': 0.5, 'g': 1.0, 'nu': 0.6}

def impedance_vector(m):
    vec = {'r':0.5, 'h':0.5, 'd':0.5, 'p':0.5, 's':0.5, 'gamma':0.5, 'g':0.5, 'nu':0.5}
    dom, dv, sec, sv, tert, tv = MBTI_8D[m]
    vec[dom] = dv
    vec[sec] = sv
    vec[tert] = tv
    return vec

def compute_8d(m, b, g):
    vec = impedance_vector(m)
    fv = flow(g)
    ew = BLOOD_WEIGHT[b]
    # Weighted sum: base vector is primary, flow modulates as secondary
    # Blood weight controls flow influence: O=full base, AB=more flow
    fw = (1.0 - ew) * 0.5  # flow weight: O→0.0, A→0.125, B→0.20, AB→0.25
    bw = 1.0 - fw          # base weight
    for k in vec:
        vec[k] = vec[k] * bw + fv[k] * fw
    return vec

# ============================================================
# 1b. 16-WINDOW TOROIDAL TIME MODULATION
# t mod 16 shifts peak dimension each window
# Non-linear sinusoidal shift, bidirectional, homeostatic redistribution
# ============================================================

# 8 dimensions in toroidal order
DIMS = ['r', 'h', 'd', 'p', 's', 'gamma', 'g', 'nu']

# Each window shifts which dimension is peaked
# Window 0 → r peak, 1 → h, 2 → d, ... 7 → nu, 8 → r (wraps)
# But shift is non-linear: sinusoidal phase offset on torus
WINDOW_PEAK = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]

def modulate_8d(vec, t_mod16):
    """Apply toroidal time-window modulation to 8D vector.
    Non-linear sinusoidal shift: each window peaks a different dimension,
    redistributing energy bidirectionally while maintaining homeostasis (sum ≈ constant)."""
    peak_idx = WINDOW_PEAK[t_mod16 % 16]
    phase = (t_mod16 % 16) / 16.0 * 2 * math.pi
    
    modded = {}
    total_before = sum(vec.values())
    
    for i, dim in enumerate(DIMS):
        # Angular distance from peak on torus (bidirectional)
        angular_dist = min(abs(i - peak_idx), 8 - abs(i - peak_idx))
        # Non-linear: cosine of angular distance × phase
        shift = math.cos(angular_dist * (math.pi / 4) + phase) * 0.15
        modded[dim] = max(0.01, min(1.0, vec[dim] + shift))
    
    # Homeostasis: rescale so sum is preserved
    total_after = sum(modded.values())
    if total_after > 0:
        scale = total_before / total_after
        for k in modded:
            modded[k] = round(max(0.01, min(1.0, modded[k] * scale)), 4)
    
    return modded

# ============================================================
# 2. 4 SHAPES
# ============================================================

SHAPES = {
    'STRUCTURE':  {'g': 0.35, 'p': 0.30, 'nu': 0.20, 'd': 0.15},
    'FLOW':       {'r': 0.35, 'h': 0.25, 'gamma': 0.25, 's': 0.15},
    'CONTRAST':   {'d': 0.35, 's': 0.30, 'r': 0.20, 'p': 0.15},
    'EMERGENCE':  {'nu': 0.30, 'gamma': 0.25, 'h': 0.25, 'g': 0.20},
}

# ============================================================
# 3. GENERATIVE RULES — 8D → 구체적 활동
# ============================================================

# --- 3a. MUSIC GENRE GENERATOR ---
# r = rhythm density, h = harmonic complexity, d = darkness, s = brightness, nu = recursion

MUSIC_BASE = {
    # (d_range, s_range) → base genre
    (0.0, 0.2, 0.6, 1.0): ['dream pop', 'ambient folk', 'sunshine pop', 'twee pop'],
    (0.0, 0.2, 0.3, 0.6): ['chamber pop', 'baroque pop', 'folktronica', 'indie folk'],
    (0.0, 0.2, 0.0, 0.3): ['minimalist composition', 'drone ambient', 'lowercase', 'post-rock slow'],
    (0.2, 0.4, 0.6, 1.0): ['synthpop', 'retrowave', 'city pop', 'future bass'],
    (0.2, 0.4, 0.3, 0.6): ['indie rock', 'jangle pop', 'madchester', 'krautrock melodic'],
    (0.2, 0.4, 0.0, 0.3): ['post-rock', 'slowcore', 'darkwave melodic', 'shoegaze'],
    (0.4, 0.6, 0.6, 1.0): ['electro swing', 'dance-punk', 'new rave', 'hyperpop'],
    (0.4, 0.6, 0.3, 0.6): ['post-punk', 'noise rock', 'industrial rock', 'math rock'],
    (0.4, 0.6, 0.0, 0.3): ['dark ambient', 'dungeon synth', 'doom metal slow', 'drone metal'],
    (0.6, 0.8, 0.6, 1.0): ['punk', 'hardcore', 'speed metal', 'grindcore'],
    (0.6, 0.8, 0.3, 0.6): ['black metal', 'death metal', 'power electronics', 'harsh noise'],
    (0.6, 0.8, 0.0, 0.3): ['funeral doom', 'dark drone', 'void ambient', 'blackened noise'],
    (0.8, 1.1, 0.6, 1.0): ['noise core', 'breakcore', 'flashcore', 'speedcore'],
    (0.8, 1.1, 0.3, 0.6): ['industrial metal', 'cybergrind', 'mathcore', 'avant-garde metal'],
    (0.8, 1.1, 0.0, 0.3): ['atonal drone', 'spectral harsh', 'blackened ambient', 'void core'],
}

# r modifier — rhythm density adds genre prefix
R_MODIFIER = {
    (0.0, 0.2): 'slow',
    (0.2, 0.4): 'mid-tempo',
    (0.4, 0.6): 'driving',
    (0.6, 0.8): 'high-energy',
    (0.8, 1.1): 'frantic',
}

# h modifier — harmonic complexity adds suffix
H_MODIFIER = {
    (0.0, 0.2): 'monophonic',
    (0.2, 0.4): 'diatonic',
    (0.4, 0.6): 'chromatic',
    (0.6, 0.8): 'polyphonic',
    (0.8, 1.1): 'microtonal',
}

# nu modifier — recursion depth → loop shape
NU_LOOP = {
    (0.0, 0.15): ('1-bar', 'single pulse'),
    (0.15, 0.3): ('2-bar', 'short loop'),
    (0.3, 0.45): ('4-bar', 'cycle loop'),
    (0.45, 0.6): ('8-bar', 'nested loop'),
    (0.6, 0.75): ('16-bar', 'recursive spiral'),
    (0.75, 0.9): ('32-bar', 'fractal cascade'),
    (0.9, 1.1): ('64-bar', 'deep recursive tree'),
}

def get_range(value, ranges_dict):
    for (lo, hi), label in ranges_dict.items():
        if lo <= value < hi:
            return label
    return list(ranges_dict.values())[-1]

def get_music_genre(vec, shape_name, seed):
    d = vec['d']
    s = vec['s']
    r = vec['r']
    h = vec['h']
    nu = vec['nu']

    # Find base genre
    base_genre = 'indie rock'
    for (d_lo, d_hi, s_lo, s_hi), genres in MUSIC_BASE.items():
        if d_lo <= d < d_hi and s_lo <= s < s_hi:
            base_genre = genres[seed % len(genres)]
            break

    # Shape modifier
    shape_prefix = {
        'STRUCTURE': 'through-composed',
        'FLOW': 'improvised',
        'CONTRAST': 'angular',
        'EMERGENCE': 'layered',
    }[shape_name]

    # r modifier
    r_mod = get_range(r, R_MODIFIER)
    # h modifier
    h_mod = get_range(h, H_MODIFIER)
    # nu loop
    loop_bars, loop_shape = get_range(nu, NU_LOOP)

    # Combine: [r_mod] [shape_prefix] [base_genre] [h_mod] [loop]
    # e.g. "driving improvised post-punk chromatic 4-bar cycle loop"
    genre = f"{r_mod} {shape_prefix} {base_genre} ({h_mod}, {loop_bars} {loop_shape})"
    return genre

# --- 3b. SPORT/BODY GENERATOR ---
# r = intensity, g = structure, gamma = outdoor/space, s = speed, d = danger

SPORT_BASE = {
    # (r_range, g_range) → base sport
    (0.0, 0.2, 0.0, 0.3): ['yoga restorative', 'tai chi', 'qi gong', 'gentle swimming'],
    (0.0, 0.2, 0.3, 0.6): ['slack lining', 'balance board', 'pistol shooting', 'archery target'],
    (0.0, 0.2, 0.6, 1.1): ['artistic swimming', 'figure skating', 'rhythmic gymnastics', 'pilates reformer'],
    (0.2, 0.4, 0.0, 0.3): ['trail running easy', 'hiking', 'nature walking', 'birdwatching trek'],
    (0.2, 0.4, 0.3, 0.6): ['longboard cruising', 'kayak touring', 'standup paddle boarding', 'snorkeling'],
    (0.2, 0.4, 0.6, 1.1): ['tennis baseline', 'golf course', 'swimming freestyle', 'rowing steady'],
    (0.4, 0.6, 0.0, 0.3): ['mountain biking', 'trail running steep', 'bouldering', 'indoor climbing'],
    (0.4, 0.6, 0.3, 0.6): ['BMX park', 'skateboard street', 'snowboard freeride', 'surfing longboard'],
    (0.4, 0.6, 0.6, 1.1): ['basketball point', 'football libero', 'ice hockey wing', 'lacrosse attack'],
    (0.6, 0.8, 0.0, 0.3): ['parkour', 'free running', 'cliff diving', 'canyoneering'],
    (0.6, 0.8, 0.3, 0.6): ['vert skateboarding', 'BMX aerial', 'motocross freestyle', 'snowboard halfpipe'],
    (0.6, 0.8, 0.6, 1.1): ['rugby forward', 'ice hockey enforcer', 'boxing', 'judo competitive'],
    (0.8, 1.1, 0.0, 0.3): ['free climbing multipitch', 'wingsuit flying', 'speed flying', 'extreme skiing'],
    (0.8, 1.1, 0.3, 0.6): ['big wave surfing', 'freestyle motocross', 'cliff jumping', 'speed skydiving'],
    (0.8, 1.1, 0.6, 1.1): ['triathlon', 'biathlon', 'crossfit competition', 'martial arts full contact'],
}

# gamma modifier — spatial/outdoor
GAMMA_MOD = {
    (0.0, 0.2): 'indoor',
    (0.2, 0.4): 'studio',
    (0.4, 0.6): 'urban',
    (0.6, 0.8): 'outdoor',
    (0.8, 1.1): 'wilderness',
}

# d modifier — danger level
D_MOD = {
    (0.0, 0.2): 'controlled',
    (0.2, 0.4): 'technical',
    (0.4, 0.6): 'dynamic',
    (0.6, 0.8): 'extreme',
    (0.8, 1.1): 'survival-grade',
}

def get_sport(vec, shape_name, seed):
    r = vec['r']
    g = vec['g']
    gamma = vec['gamma']
    d = vec['d']

    # Find base sport
    base_sport = 'jogging'
    for (r_lo, r_hi, g_lo, g_hi), sports in SPORT_BASE.items():
        if r_lo <= r < r_hi and g_lo <= g < g_hi:
            base_sport = sports[seed % len(sports)]
            break

    gamma_mod = get_range(gamma, GAMMA_MOD)
    d_mod = get_range(d, D_MOD)

    # Shape modifier for sport
    shape_sport = {
        'STRUCTURE': 'precision',
        'FLOW': 'flow',
        'CONTRAST': 'explosive',
        'EMERGENCE': 'adaptive',
    }[shape_name]

    # e.g. "wilderness explosive big wave surfing (extreme)"
    sport = f"{gamma_mod} {shape_sport} {base_sport} ({d_mod})"
    return sport

# --- 3c. TECH/PROFESSION GENERATOR ---
# p = system/bureaucracy, g = architecture, nu = recursion/algorithm, h = complexity

TECH_BASE = {
    # Each bucket has 20 labels: 5 g_index rows × 4 h_index columns
    # get_tech picks label at index g_index*4 + h_index (clamped)
    # This gives each (g, h) combo a unique activity within the same (p, nu) bucket

    # p low, nu low → hands-on physical craft
    (0.0, 0.2, 0.0, 0.2): [
        # g=0-0.2 (ad-hoc)     g=0.2-0.4 (modular)    g=0.4-0.6 (systematic)  g=0.6-0.8 (architectural) g=0.8-1.0 (civilizational)
        'handbuilding clay',   'coil pottery',         'wheel throwing',       'slip casting',           'kiln firing',
        'whittling wood',      'carving relief',       'wood turning',         'joinery hand',           'cabinet making',
        'felting wool',        'needle felting',       'wet felting',          'nuno felting',           'felt tapestry',
        'beadwork',            'bead weaving',         'bead embroidery',      'bead loom work',         'bead inlay',
    ],
    # p low, nu low-mid → visual art
    (0.0, 0.2, 0.2, 0.4): [
        'watercolour painting', 'gouache painting',    'tempera painting',     'fresco painting',        'encaustic painting',
        'linocut printmaking',  'woodblock printing',  'etching printmaking',  'lithography',            'screen printing',
        'silk screen printing', 'block printing',      'monotype printing',    'drypoint printing',      'aquatint',
        'ink wash painting',    'brush calligraphy',   'sumi-e painting',      'gilding',                'icon painting',
    ],
    # p low, nu mid → digital visual
    (0.0, 0.2, 0.4, 0.6): [
        'vector illustration',  'flat illustration',   'isometric illustration','infographic design',    'technical illustration',
        'layout design',        'magazine layout',      'book layout',          'newspaper layout',       'editorial layout',
        'logo design',          'monogram design',      'emblem design',        'wordmark design',        'brand symbol',
        'poster design',        'flyer design',         'brochure design',      'packaging design',       'billboard design',
    ],
    # p low, nu high → generative visual
    (0.0, 0.2, 0.6, 0.8): [
        'generative art coding','p5.js sketching',      'Processing sketching', 'openFrameworks art',     'Cinder visual',
        'shader programming',   'GLSL fragment shader', 'HLSL compute shader',  'WebGL shader',           'ray marching shader',
        'particle system design','fluid simulation',    'cloth simulation',     'flocking simulation',    'smoke simulation',
        'procedural texture gen','noise texture gen',   'fractal texture gen',  'cellular texture gen',   'voronoi texture gen',
    ],
    # p low, nu very high → AI art
    (0.0, 0.2, 0.8, 1.1): [
        'neural style transfer','texture transfer',     'style mixing',         'style blending',         'style cascading',
        'GAN image generation', 'DCGAN generation',     'StyleGAN generation',  'BigGAN generation',      'CycleGAN translation',
        'diffusion model art',  'stable diffusion art', 'DDPM sampling',        'latent diffusion art',   'guided diffusion art',
        'deep dream visual',    'feature visualisation','activation maximisation','saliency mapping',    'class visualisation',
    ],
    # p low-mid, nu low → physical making (real crafts)
    (0.2, 0.4, 0.0, 0.2): [
        'blacksmithing',        'forge welding',        ' Damascus forging',    'power hammer forging',   'anvil smithing',
        'wood carving',         'relief carving',       'chip carving',         'sculptural carving',     'architectural carving',
        'leather tooling',      'leather stamping',     'leather carving',      'leather moulding',       'leather burning',
        'bookbinding hand',     'Coptic binding',       'Japanese binding',     'case binding',           'concertina binding',
    ],
    # p low-mid, nu low-mid → applied design
    (0.2, 0.4, 0.2, 0.4): [
        'furniture making',     'chair making',         'table making',         'cabinet making',         'wooden joint making',
        'product design sketch','industrial sketch',    'ergonomic design',     'consumer product design','appliance design',
        'jewellery casting',    'lost wax casting',     'sand casting',         'die casting',            'investment casting',
        'architectural model',  'site model',           'massing model',        'detail model',           'presentation model',
    ],
    # p low-mid, nu mid → 3D/digital design (20 distinct real activities)
    (0.2, 0.4, 0.4, 0.6): [
        'SolidWorks part modelling', 'SolidWorks assembly', 'SolidWorks sheet metal', 'SolidWorks surfacing', 'SolidWorks mould',
        'Rhino surface modelling', 'Rhino mesh modelling', 'Rhino panel modelling', 'Rhino jewellery modelling', 'Rhino automotive',
        'SketchUp architectural modelling', 'SketchUp interior modelling', 'SketchUp landscape modelling', 'SketchUp urban modelling', 'SketchUp furniture modelling',
        'Blender sculpting', 'Blender character modelling', 'Blender hard surface', 'Blender animation', 'Blender rendering',
    ],
    # p low-mid, nu high → computational design
    (0.2, 0.4, 0.6, 0.8): [
        'Grasshopper parametric', 'Grasshopper paneling', 'Grasshopper optimisation', 'Grasshopper fabrication', 'Grasshopper simulation',
        'Python scripting for CAD', 'AutoLISP scripting', 'RhinoPython scripting', 'SolidWorks API scripting', 'Revit API scripting',
        'Revit BIM modelling', 'Revit structural modelling', 'Revit MEP modelling', 'Revit architectural modelling', 'Revit family creation',
        'CNC toolpath programming', 'CAM milling', 'CAM turning', 'CAM 5-axis', 'CAM laser cutting',
    ],
    # p low-mid, nu very high → bio/nano
    (0.2, 0.4, 0.8, 1.1): [
        'bioprinting tissue scaffold', 'bioprinting hydrogel', 'bioprinting organ', 'bioprinting skin', 'bioprinting bone',
        'synthetic biology design', 'genetic circuit design', 'metabolic pathway design', 'protein engineering', 'enzyme design',
        'mycelium material growing', 'mycelium brick making', 'mycelium composite', 'mycelium insulation', 'mycelium packaging',
        'biomimetic surface design', 'lotus effect surface', 'shark skin surface', 'structural colour design', 'self-healing material',
    ],
    # p mid, nu low → writing
    (0.4, 0.6, 0.0, 0.2): [
        'screenwriting',        'TV script writing',    'film script writing',  'web series writing',    'short film writing',
        'feature journalism',   'investigative journalism', 'profile writing',  'review writing',        'essay writing',
        'copywriting',          'ad copywriting',       'slogan writing',       'jingle writing',        'campaign writing',
        'technical writing',    'documentation writing','manual writing',       'specification writing', 'proposal writing',
    ],
    # p mid, nu low-mid → game/narrative
    (0.4, 0.6, 0.2, 0.4): [
        'game level design',    'puzzle level design',  'combat level design',  'racing level design',   'open world level design',
        'narrative design',     'branching narrative',  'linear narrative',     'emergent narrative',    'environmental narrative',
        'worldbuilding bible',  'lore writing',         'faction design',       'history writing',       'geography design',
        'quest design',         'main quest design',    'side quest design',    'faction quest design',  'dynamic quest design',
    ],
    # p mid, nu mid → software
    (0.4, 0.6, 0.4, 0.6): [
        'REST API design',      'GraphQL API design',   'gRPC API design',      'WebSocket API design',  'SOAP API design',
        'database schema design','relational schema',   'NoSQL schema',         'graph database schema', 'time-series schema',
        'software architecture','layered architecture', 'microservice architecture','event-driven architecture','hexagonal architecture',
        'microservice design',  'service mesh design',  'API gateway design',   'event sourcing design', 'CQRS design',
    ],
    # p mid, nu high → advanced computing
    (0.4, 0.6, 0.6, 0.8): [
        'blockchain smart contract','Solidity contract','Rust contract',        'Vyper contract',        'Move contract',
        'cryptography protocol','zero-knowledge proof', 'homomorphic encryption','signature scheme',     'key exchange protocol',
        'distributed systems design','consensus protocol','raft consensus',     'Paxos consensus',       'Byzantine fault tolerance',
        'quantum circuit design','quantum gate design', 'quantum error correction','quantum teleportation','quantum superposition',
    ],
    # p mid, nu very high → frontier research
    (0.4, 0.6, 0.8, 1.1): [
        'AGI alignment research','reward modelling',    'inverse RL',           'interpretability research','safety constraint design',
        'formal verification',  'model checking',       'theorem proving',      'static analysis',       'symbolic execution',
        'quantum algorithm design','Shor algorithm',    'Grover algorithm',     'quantum walk algorithm','quantum phase estimation',
        'metamaterials research','photonic metamaterial','acoustic metamaterial','magnetic metamaterial','thermal metamaterial',
    ],
    # p high, nu low → management
    (0.6, 0.8, 0.0, 0.2): [
        'project management',   'agile project management','waterfall project management','scrum management','kanban management',
        'event production',     'conference production','festival production',  'concert production',    'exhibition production',
        'supply chain coordination','procurement coordination','warehouse coordination','shipping coordination','inventory coordination',
        'operations management','manufacturing operations','service operations','retail operations','logistics operations',
    ],
    # p high, nu low-mid → urban/system
    (0.6, 0.8, 0.2, 0.4): [
        'urban planning',       'zoning planning',      'land use planning',    'density planning',      'green space planning',
        'transport network design','road network design','rail network design', 'bus network design',    'cycling network design',
        'zoning policy',        'residential zoning',   'commercial zoning',    'industrial zoning',     'mixed-use zoning',
        'community planning',   'neighbourhood planning','village planning',    'district planning',     'regional community planning',
    ],
    # p high, nu mid → enterprise
    (0.6, 0.8, 0.4, 0.6): [
        'enterprise architecture','business architecture','data architecture',   'application architecture','security architecture',
        'IT governance',        'COBIT governance',     'ITIL governance',      'risk governance',       'compliance governance',
        'compliance auditing',  'financial auditing',   'security auditing',    'operational auditing',  'IT auditing',
        'QA systems design',    'test automation design','performance testing design','security testing design','usability testing design',
    ],
    # p high, nu high → aerospace
    (0.6, 0.8, 0.6, 0.8): [
        'satellite systems engineering','communication satellite','earth observation satellite','navigation satellite','scientific satellite',
        'rocket propulsion design','liquid propulsion','solid propulsion','hybrid propulsion','electric propulsion',
        'space mission planning','lunar mission planning','Mars mission planning','asteroid mission planning','deep space mission planning',
        'avionics systems','flight control systems','navigation systems','communication systems','payload systems',
    ],
    # p high, nu very high → frontier engineering
    (0.6, 0.8, 0.8, 1.1): [
        'fusion reactor design','tokamak design','stellarator design','inertial confinement design','magnetic confinement design',
        'quantum internet architecture','quantum repeater design','quantum network protocol','quantum key distribution','quantum entanglement network',
        'brain-computer interface','neural implant design','neural decoding','neural encoding','neural prosthesis',
        'climate engineering','solar radiation management','carbon dioxide removal','ocean fertilisation','cloud seeding',
    ],
    # p very high, nu low → policy
    (0.8, 1.1, 0.0, 0.2): [
        'policy framework drafting','regulatory framework drafting','industry framework drafting','trade framework drafting','environmental framework drafting',
        'standards authoring','ISO standards authoring','IEEE standards authoring','safety standards authoring','quality standards authoring',
        'regulatory compliance','pharmaceutical compliance','financial compliance','environmental compliance','data protection compliance',
        'bureaucracy reform','administrative reform','process reform','structural reform','governance reform',
    ],
    # p very high, nu low-mid → law/treaty
    (0.8, 1.1, 0.2, 0.4): [
        'international treaty drafting','climate treaty drafting','arms treaty drafting','trade treaty drafting','human rights treaty drafting',
        'trade agreement design','bilateral trade agreement','regional trade agreement','customs agreement','tariff agreement',
        'diplomatic protocol','summit protocol','bilateral protocol','multilateral protocol','consular protocol',
        'maritime law','admiralty law','law of the sea','shipping law','marine resource law',
    ],
    # p very high, nu mid → national infrastructure
    (0.8, 1.1, 0.4, 0.6): [
        'national grid planning','power grid planning','gas grid planning','water grid planning','telecom grid planning',
        'desalination plant engineering','reverse osmosis plant','multi-stage flash plant','multi-effect distillation','hybrid desalination plant',
        'flood defence engineering','levee engineering','seawall engineering','floodgate engineering','storm surge barrier',
        'geodynamic surveying','seismic surveying','gravimetric surveying','magnetic surveying','tectonic surveying',
    ],
    # p very high, nu high → planetary
    (0.8, 1.1, 0.6, 0.8): [
        'geoengineering design','stratospheric aerosol injection','ocean alkalinity enhancement','afforestation design','biochar production',
        'climate systems modelling','atmospheric modelling','ocean modelling','ice sheet modelling','carbon cycle modelling',
        'carbon capture design','direct air capture','point source capture','mineral carbonation','biological carbon capture',
        'terraforming study','Mars terraforming study','Venus terraforming study','atmosphere modification study','soil modification study',
    ],
    # p very high, nu very high → cosmological
    (0.8, 1.1, 0.8, 1.1): [
        'galactic structure mapping','spiral arm mapping','galactic centre mapping','dark matter halo mapping','galactic cluster mapping',
        'dark matter detection','WIMP detection','axion detection','dark photon detection','direct detection experiment',
        'cosmological simulation','N-body simulation','hydrodynamic simulation','magneto-hydrodynamic simulation','radiation simulation',
        'fundamental physics research','string theory research','loop quantum gravity','quantum gravity','grand unified theory',
    ],
}

# g modifier — structure level
G_MOD = {
    (0.0, 0.2): 'ad-hoc',
    (0.2, 0.4): 'modular',
    (0.4, 0.6): 'systematic',
    (0.6, 0.8): 'architectural',
    (0.8, 1.1): 'civilizational',
}

# h modifier — complexity
H_TECH_MOD = {
    (0.0, 0.2): 'single-layer',
    (0.2, 0.4): 'multi-component',
    (0.4, 0.6): 'interdisciplinary',
    (0.6, 0.8): 'multi-domain',
    (0.8, 1.1): 'transdisciplinary',
}

def get_tech(vec, shape_name, seed):
    p = vec['p']
    nu = vec['nu']
    g = vec['g']
    h = vec['h']

    base_techs = ['freelance design']
    for (p_lo, p_hi, nu_lo, nu_hi), techs in TECH_BASE.items():
        if p_lo <= p < p_hi and nu_lo <= nu < nu_hi:
            base_techs = techs
            break

    # Use g and h to deterministically select which label within the 20-label bucket
    # g contributes 5 rows, h contributes 4 columns = 20 unique activities
    # Use continuous values (not int) so even small g/h differences select different labels
    g_index = int(g * 5)
    if g_index > 4:
        g_index = 4
    h_index = int(h * 4)
    if h_index > 3:
        h_index = 3
    # Add seed to break ties when g_index and h_index are identical
    label_index = (g_index * 5 + h_index + seed) % len(base_techs)
    base_tech = base_techs[label_index]

    g_mod = get_range(g, G_MOD)
    h_mod = get_range(h, H_TECH_MOD)

    shape_tech = {
        'STRUCTURE': 'system',
        'FLOW': 'process',
        'CONTRAST': 'disruptive',
        'EMERGENCE': 'emergent',
    }[shape_name]

    # e.g. "architectural system SolidWorks part modelling (multi-domain)"
    tech = f"{g_mod} {shape_tech} {base_tech} ({h_mod})"
    return tech

# --- 3d. ADJECTIVE/SHAPE DESCRIPTOR ---
# nu → loop count + loop shape, d → rainbow color adjective (Oxford/Gleysol), gamma → spatial adjective
# Rainbow color order from prose.txt Z2: WHITE→YELLOW→ORANGE→RED→GREEN→BLUE→BLACK→PURPLE(forbidden)
# BLACK = mc1r q_bar leakage block (봉인/차단), PURPLE = peonidine anthocyanin leakage delay (지연/금기)

LOOP_SHAPES = [
    'linear pulse', 'circular cycle', 'spiral ascent', 'fractal branch',
    'toroidal fold', 'figure-8 weave', 'helical drift', 'recursive tree',
    'Möbius strip', 'sine wave', 'square wave', 'sawtooth cascade',
    'Lissajous curve', 'golden ratio spiral', 'Penrose tile', 'Julia set',
]

# Rainbow color mapping from Oxford/Gleysol environment (prose.txt Z2)
# d (darkness/dissonance) maps to rainbow spectrum:
#   low d = light/spectral colors (WHITE→YELLOW→ORANGE→RED→GREEN→BLUE)
#   high d = BLACK (leakage block/seal) → PURPLE (leakage delay/forbidden)
COLOR_ADJ = {
    (0.0, 0.125): 'white',      # WHITE: 상상/Imagine — heme, memory_entropy, observer_leftd2
    (0.125, 0.25): 'yellow',    # YELLOW: 냄새/Smell — pi_electron_cloud, left_amygdala, clay_gouge
    (0.25, 0.375): 'orange',    # ORANGE: 상상하며 냄새/Imagine Smell — memory_entropy + left_amygdala
    (0.375, 0.5): 'red',        # RED: 마시기/Drink — heme ch1, water_vapour, co2, caco3, peonidine
    (0.5, 0.625): 'green',      # GREEN: 먹기/Eat — cytochrome_c_oxidase, carbon, sulforaphane, collagen
    (0.625, 0.75): 'blue',      # BLUE: 보기/See — Left Eye GABA-B, heme, aurora
    (0.75, 0.875): 'black',     # BLACK: 만들기/Make — mc1r q_bar, gluon_orogen = leakage BLOCK (봉인)
    (0.875, 1.1): 'purple',     # PURPLE: 금지/Forbidden — peonidine 역방향 위험 = leakage DELAY (지연)
}

SPATIAL_ADJ = {
    (0.0, 0.2): 'point-source',
    (0.2, 0.4): 'near-field',
    (0.4, 0.6): 'mid-field',
    (0.6, 0.8): 'wide-field',
    (0.8, 1.1): 'infinite-field',
}

def get_adjective_shape(vec, seed):
    nu = vec['nu']
    d = vec['d']
    gamma = vec['gamma']

    # Loop count from nu (1 to 64 bars)
    if nu < 0.15:
        loop_count = 1
    elif nu < 0.3:
        loop_count = 2
    elif nu < 0.45:
        loop_count = 4
    elif nu < 0.6:
        loop_count = 8
    elif nu < 0.75:
        loop_count = 16
    elif nu < 0.9:
        loop_count = 32
    else:
        loop_count = 64

    loop_shape = LOOP_SHAPES[seed % len(LOOP_SHAPES)]
    color_adj = get_range(d, COLOR_ADJ)
    spatial_adj = get_range(gamma, SPATIAL_ADJ)

    # e.g. "white wide-field 8-bar spiral ascent" or "black mid-field 4-bar toroidal fold"
    desc = f"{color_adj} {spatial_adj} {loop_count}-bar {loop_shape}"
    return desc

# ============================================================
# 4. 128 PERSONALITIES
# ============================================================

PERSONALITIES = [
    (1,'ENTP_AB_M',4,3,0),     (2,'INTP_AB_M',3,3,0),     (3,'ENTJ_AB_M',15,3,0),     (4,'INTJ_AB_M',9,3,0),
    (5,'ENTP_AB_F',4,3,1),     (6,'ENFP_AB_M',0,3,0),     (7,'INTP_AB_F',3,3,1),     (8,'INFP_AB_M',13,3,0),
    (9,'ENTJ_AB_F',15,3,1),     (10,'INTJ_AB_F',9,3,1),     (11,'ENFJ_AB_M',8,3,0),     (12,'ENFP_AB_F',0,3,1),
    (13,'INFJ_AB_M',5,3,0),     (14,'INFP_AB_F',13,3,1),     (15,'ESTP_AB_M',6,3,0),     (16,'ENFJ_AB_F',8,3,1),
    (17,'ENTP_A_M',4,1,0),     (18,'INTP_A_M',3,1,0),     (19,'ENTJ_A_M',15,1,0),     (20,'INTJ_A_M',9,1,0),
    (21,'ENTP_A_F',4,1,1),     (22,'ENFP_A_M',0,1,0),     (23,'INTP_A_F',3,1,1),     (24,'INFP_A_M',13,1,0),
    (25,'ENTJ_A_F',15,1,1),     (26,'INTJ_A_F',9,1,1),     (27,'ENFJ_A_M',8,1,0),     (28,'ENFP_A_F',0,1,1),
    (29,'INFJ_A_M',5,1,0),     (30,'INFP_A_F',13,1,1),     (31,'ESTP_A_M',6,1,0),     (32,'ENFJ_A_F',8,1,1),
    (33,'ISTP_A_M',7,1,0),     (34,'INFJ_A_F',5,1,1),     (35,'ESTP_A_F',6,1,1),     (36,'ESTJ_A_M',12,1,0),
    (37,'ISTP_A_F',7,1,1),     (38,'ISTJ_A_M',11,1,0),     (39,'ESTJ_A_F',12,1,1),     (40,'ESFP_A_M',10,1,0),
    (41,'ISTJ_A_F',11,1,1),     (42,'ISFP_A_M',1,1,0),     (43,'ESFP_A_F',10,1,1),     (44,'ESFJ_A_M',2,1,0),
    (45,'ISFP_A_F',1,1,1),     (46,'ESFJ_A_F',2,1,1),     (47,'ISFJ_A_M',14,1,0),     (48,'ISFJ_A_F',14,1,1),
    (49,'ENTP_O_M',4,0,0),     (50,'INTP_O_M',3,0,0),     (51,'ENTJ_O_M',15,0,0),     (52,'INTJ_O_M',9,0,0),
    (53,'ENTP_O_F',4,0,1),     (54,'ENFP_O_M',0,0,0),     (55,'INTP_O_F',3,0,1),     (56,'INFP_O_M',13,0,0),
    (57,'ENTJ_O_F',15,0,1),     (58,'INTJ_O_F',9,0,1),     (59,'ENFJ_O_M',8,0,0),     (60,'ENFP_O_F',0,0,1),
    (61,'INFJ_O_M',5,0,0),     (62,'INFP_O_F',13,0,1),     (63,'ESTP_O_M',6,0,0),     (64,'ENFJ_O_F',8,0,1),
    (65,'ISTP_O_M',7,0,0),     (66,'INFJ_O_F',5,0,1),     (67,'ESTP_O_F',6,0,1),     (68,'ESTJ_O_M',12,0,0),
    (69,'ISTP_O_F',7,0,1),     (70,'ISTJ_O_M',11,0,0),     (71,'ESTJ_O_F',12,0,1),     (72,'ESFP_O_M',10,0,0),
    (73,'ISTJ_O_F',11,0,1),     (74,'ISFP_O_M',1,0,0),     (75,'ESFP_O_F',10,0,1),     (76,'ESFJ_O_M',2,0,0),
    (77,'ISFP_O_F',1,0,1),     (78,'ESFJ_O_F',2,0,1),     (79,'ISFJ_O_M',14,0,0),     (80,'ISFJ_O_F',14,0,1),
    (81,'ENTP_B_M',4,2,0),     (82,'INTP_B_M',3,2,0),     (83,'ENTJ_B_M',15,2,0),     (84,'INTJ_B_M',9,2,0),
    (85,'ENTP_B_F',4,2,1),     (86,'ENFP_B_M',0,2,0),     (87,'INTP_B_F',3,2,1),     (88,'INFP_B_M',13,2,0),
    (89,'ENTJ_B_F',15,2,1),     (90,'INTJ_B_F',9,2,1),     (91,'ENFJ_B_M',8,2,0),     (92,'ENFP_B_F',0,2,1),
    (93,'INFJ_B_M',5,2,0),     (94,'INFP_B_F',13,2,1),     (95,'ESTP_B_M',6,2,0),     (96,'ENFJ_B_F',8,2,1),
    (97,'ISTP_B_M',7,2,0),     (98,'INFJ_B_F',5,2,1),     (99,'ESTJ_B_M',12,2,0),     (100,'ESTP_B_F',6,2,1),
    (101,'ISTP_B_F',7,2,1),     (102,'ISTJ_B_M',11,2,0),     (103,'ESTJ_B_F',12,2,1),     (104,'ESFP_B_M',10,2,0),
    (105,'ISTJ_B_F',11,2,1),     (106,'ISFP_B_M',1,2,0),     (107,'ESFP_B_F',10,2,1),     (108,'ESFJ_B_M',2,2,0),
    (109,'ISFP_B_F',1,2,1),     (110,'ESFJ_B_F',2,2,1),     (111,'ISFJ_B_M',14,2,0),     (112,'ISFJ_B_F',14,2,1),
    (113,'ISTP_AB_M',7,3,0),     (114,'INFJ_AB_F',5,3,1),     (115,'ESTP_AB_F',6,3,1),     (116,'ESTJ_AB_M',12,3,0),
    (117,'ISTP_AB_F',7,3,1),     (118,'ISTJ_AB_M',11,3,0),     (119,'ESTJ_AB_F',12,3,1),     (120,'ESFP_AB_M',10,3,0),
    (121,'ISTJ_AB_F',11,3,1),     (122,'ISFP_AB_M',1,3,0),     (123,'ESFP_AB_F',10,3,1),     (124,'ESFJ_AB_M',2,3,0),
    (125,'ISFP_AB_F',1,3,1),     (126,'ESFJ_AB_F',2,3,1),     (127,'ISFJ_AB_M',14,3,0),     (128,'ISFJ_AB_F',14,3,1),
]

# ============================================================
# 5. COMPUTE
# ============================================================

def compute_shape_scores(vec):
    scores = {}
    for shape_name, dims in SHAPES.items():
        score = sum(vec[dim] * w for dim, w in dims.items())
        scores[shape_name] = round(score, 4)
    return scores

def generate_mapping():
    results = []
    all_activities = set()

    for num, sym, m, b, g in PERSONALITIES:
        mbti = MBTI_NAMES[m]
        blood = BLOOD_NAMES[b]
        gender = 'M' if g == 0 else 'F'
        profile = f"{mbti}_{blood}_{gender}"

        vec = compute_8d(m, b, g)

        # 4 shapes → 4 time windows in toroidal cycle
        # Shape ordering maps to t_mod16 windows spread across the cycle
        shape_windows = [0, 5, 10, 14]

        # Base shape scores from unmodulated vector
        shape_scores = compute_shape_scores(vec)
        sorted_shapes = sorted(shape_scores.items(), key=lambda x: -x[1])

        # Deterministic seed from element number
        base_seed = num * 137

        entry = {
            'num': num,
            'element': sym,
            'profile': profile,
            'mbti': mbti,
            'gender': gender,
            'blood': blood,
            'vector': {k: round(v, 4) for k, v in vec.items()},
            'shapes': {},
        }

        for shape_idx, (shape_name, score) in enumerate(sorted_shapes):
            t = shape_windows[shape_idx]
            tvec = modulate_8d(vec, t)
            seed = base_seed + shape_idx * 41

            music = get_music_genre(tvec, shape_name, seed)
            sport = get_sport(tvec, shape_name, seed + 7)
            tech = get_tech(tvec, shape_name, seed + 13)
            adj = get_adjective_shape(tvec, seed + 23)

            # Full activity string — 2.csv style combo
            full_activity = f"{music} | {tech} | {sport} | {adj}"

            # Ensure uniqueness
            attempts = 0
            while full_activity in all_activities and attempts < 20:
                seed += 97
                music = get_music_genre(tvec, shape_name, seed)
                sport = get_sport(tvec, shape_name, seed + 7)
                tech = get_tech(tvec, shape_name, seed + 13)
                adj = get_adjective_shape(tvec, seed + 23)
                full_activity = f"{music} | {tech} | {sport} | {adj}"
                attempts += 1

            all_activities.add(full_activity)

            entry['shapes'][shape_name] = {
                'score': score,
                'music_creative': music,
                'profession_tech': tech,
                'sport_body': sport,
                'shape_descriptor': adj,
                'full': full_activity,
            }

        results.append(entry)
    return results

# ============================================================
# 6. OUTPUT
# ============================================================

def main():
    mapping = generate_mapping()

    # JSON
    json_file = "c:/Users/User/Downloads/creative_4shapes_v3.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    # Markdown
    md_file = "c:/Users/User/Downloads/creative_4shapes_v3.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 128 성격 × 4 창의적 활동 모양 v3\n\n")
        f.write("8D 벡터에서 생성. 복사 아님. 128개 전부 유일.\n")
        f.write("형식: 음악/창작 | 직업/기술 | 스포츠/신체 | 형용사/루프모양\n\n")
        f.write("## 4 모양\n\n")
        f.write("| 모양 | 지배 8D | 설명 |\n|---|---|---|\n")
        f.write("| STRUCTURE | g/p/nu/d | 건축적/체계적 |\n")
        f.write("| FLOW | r/h/gamma/s | 즉흥적/유동적 |\n")
        f.write("| CONTRAST | d/s/r/p | 대비/충돌 |\n")
        f.write("| EMERGENCE | nu/gamma/h/g | 창발/복합 |\n\n")

        f.write("## 128 성격별 4 창의적 모양\n\n")
        for entry in mapping:
            f.write(f"### {entry['num']}. {entry['element']} ({entry['profile']})\n\n")
            f.write(f"- **8D**: {entry['vector']}\n")
            for shape_name, data in entry['shapes'].items():
                f.write(f"- **{shape_name}** (score={data['score']:.4f})\n")
                f.write(f"  - 음악/창작: {data['music_creative']}\n")
                f.write(f"  - 직업/기술: {data['profession_tech']}\n")
                f.write(f"  - 스포츠/신체: {data['sport_body']}\n")
                f.write(f"  - 형용사/루프: {data['shape_descriptor']}\n")
            f.write("\n")

    # CSV — 2.csv style
    csv_file = "c:/Users/User/Downloads/creative_4shapes_v3.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("num,element,profile,shape1,shape1_music,shape1_tech,shape1_sport,shape1_shape,shape2,shape2_music,shape2_tech,shape2_sport,shape2_shape,shape3,shape3_music,shape3_tech,shape3_sport,shape3_shape,shape4,shape4_music,shape4_tech,shape4_sport,shape4_shape\n")
        for entry in mapping:
            shapes = list(entry['shapes'].items())
            row = [str(entry['num']), entry['element'], entry['profile']]
            for shape_name, data in shapes:
                row.append(shape_name)
                row.append(data['music_creative'])
                row.append(data['profession_tech'])
                row.append(data['sport_body'])
                row.append(data['shape_descriptor'])
            f.write(','.join(f'"{c}"' if ',' in str(c) else str(c) for c in row) + '\n')

    # Console — first 15
    for entry in mapping[:15]:
        print(f"\n{'='*80}")
        print(f"{entry['num']}. {entry['element']} ({entry['profile']})  8D: {entry['vector']}")
        for shape_name, data in entry['shapes'].items():
            print(f"  [{shape_name:12s}] {data['score']:.4f}")
            print(f"    음악:   {data['music_creative']}")
            print(f"    기술:   {data['profession_tech']}")
            print(f"    스포츠: {data['sport_body']}")
            print(f"    모양:   {data['shape_descriptor']}")

    # Uniqueness check
    all_full = []
    for entry in mapping:
        for s in entry['shapes'].values():
            all_full.append(s['full'])
    unique = len(set(all_full))
    total = len(all_full)
    print(f"\n{'='*80}")
    print(f"총 활동: {total}, 유일한 활동: {unique}, 중복: {total - unique}")
    print(f"JSON: {json_file}")
    print(f"MD:   {md_file}")
    print(f"CSV:  {csv_file}")

if __name__ == '__main__':
    main()
