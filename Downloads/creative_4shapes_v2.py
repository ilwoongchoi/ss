"""
128 성격 × 4 창의적 활동 모양 v2
2.csv 스타일: 구체적 장르명 + 스포츠 + 기술 + 형용사/루프모양
음식 관련 없음. 활동만.
8D 임피던스 → 4 모양 → 구체적 활동 매핑
"""

import math
import json
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ============================================================
# 1. 8D IMPEDANCE
# ============================================================

MBTI_8D = {
    0:  ('r', 1.0, 's', 0.6, 'nu', 0.3),   # ENFP
    1:  ('h', 1.0, 'gamma', 0.6, 'nu', 0.3), # ISFP
    2:  ('d', 1.0, 'h', 0.6, 'g', 0.3),     # ESFJ
    3:  ('p', 1.0, 'nu', 0.6, 'h', 0.3),    # INTP
    4:  ('s', 1.0, 'r', 0.6, 'nu', 0.3),    # ENTP
    5:  ('gamma', 1.0, 'h', 0.6, 'p', 0.3), # INFJ
    6:  ('g', 1.0, 's', 0.6, 'r', 0.3),     # ESTP
    7:  ('nu', 1.0, 'p', 0.6, 'd', 0.3),    # ISTP
    8:  ('r', 0.8, 'h', 0.8, 'gamma', 0.4), # ENFJ
    9:  ('h', 1.0, 'p', 0.6, 'nu', 0.3),    # INTJ
    10: ('s', 1.0, 'gamma', 0.6, 'r', 0.3), # ESFP
    11: ('d', 1.0, 'g', 0.6, 'p', 0.3),     # ISTJ
    12: ('g', 1.0, 'd', 0.6, 'p', 0.3),     # ESTJ
    13: ('h', 1.0, 'gamma', 0.6, 'nu', 0.3),# INFP
    14: ('g', 1.0, 'gamma', 0.6, 'h', 0.3), # ISFJ
    15: ('d', 1.0, 'gamma', 0.6, 'g', 0.3), # ENTJ
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

# ============================================================
# 2. 4 SHAPES — 8D 기반
# ============================================================

SHAPES = {
    'STRUCTURE': {
        'dims': {'g': 0.35, 'p': 0.30, 'nu': 0.20, 'd': 0.15},
    },
    'FLOW': {
        'dims': {'r': 0.35, 'h': 0.25, 'gamma': 0.25, 's': 0.15},
    },
    'CONTRAST': {
        'dims': {'d': 0.35, 's': 0.30, 'r': 0.20, 'p': 0.15},
    },
    'EMERGENCE': {
        'dims': {'nu': 0.30, 'gamma': 0.25, 'h': 0.25, 'g': 0.20},
    },
}

# ============================================================
# 3. ACTIVITY POOLS — 2.csv 스타일 구체적 활동
# 음식 없음. 활동만.
# ============================================================

# 각 모양별 활동 풀: (음악/창작, 직업/기술, 스포츠/신체)
# 8D 세부 값으로 세분화

# STRUCTURE: g/p/nu/d 지배 → 건축적, 체계적, 조립적
STRUCTURE_ACTIVITIES = {
    # high g (구조) + high p (예측) → 정밀 조립, 설계
    'high_gp': [
        ('NEOCLASSICAL composition', '3D GRAPHICS DEVELOPER', 'tennis baseline strategy'),
        ('MINIMALIST PHOTOGRAPHY', 'INTERNATIONAL PUBLIC BANK BUREAUCRAT', 'ALPINE SKI carving'),
        ('Baroque guitar', 'lutherie', 'fencing epee precision'),
        ('MECCANO HOBBY', 'EMBEDDED SYSTEMS FIRMWARE', 'SINGLE SCULL ROWING'),
        ('scale model building (lost wax casting)', 'horologist', 'free climbing route setting'),
        ('cryptographer', 'DESALINATION ENGINEER', 'Go joseki analysis'),
        ('photogrammetry 3d scanning', 'algorhythm designer', 'pacing strategy distance swim'),
        ('dynamic diorama (KITBASHING)', 'CTO', 'KORFBALL defence'),
    ],
    # high nu (재귀) + high p → 프랙탈, 중첩 구조
    'high_nup': [
        ('fractal art', 'white hacker', 'polar trekking'),
        ('recurrence relation solving', 'CRYPTOGRAPHY EXERCISE', 'bouldering graded route'),
        ('topology problem set', 'number theory hobby', 'chess puzzle composition'),
        ('formal logic proof writing', 'quantum computing researcher', '3m springboard dive'),
        ('constraint satisfaction puzzle', 'software product manager (technical)', 'artistic swimming routine'),
        ('nonogram puzzle', 'data warehouse ETL pipeline engineer', 'tent and trees puzzle'),
    ],
    # high d (어둠) + high g → 무거운 구조, 심층
    'high_dg': [
        ('SF worldbuilding', 'vbeer brewing hobby', 'free climbing multipitch'),
        ('dark textile weaving', 'special forces agent', 'SERE training'),
        ('Free jazz composition (through-composed)', 'independent sw architect (hobby)', 'biathlon'),
        ('Berliner schule composition', 'IOT Engineer', 'ice climbing waterfall'),
        ('glitch opera (structured)', 'Car cpu developer', 'marksmanship precision'),
    ],
    # mid values → 일반 구조
    'mid': [
        ('traditional music transcription', 'archival research', 'racketball'),
        ('bookbinding', 'tax planner (coordinator)', '3 cushion billiards'),
        ('precision pen drawing', 'INTERIOR DESIGN RENDER', 'inline skating slalom'),
        ('clay modelling with hand', 'GIS professional', 'urban vegetable community gardening'),
        ('felt making', 'soil scientist', 'cart racing precision'),
        ('watchmaking', 'precision instrument calibration', 'competitive rubiks cube'),
    ],
}

# FLOW: r/h/gamma/s 지배 → 즉흥, 유동, 리듬
FLOW_ACTIVITIES = {
    # high r (리듬) + high h (화성) → 음악적 플로우
    'high_rh': [
        ('FLOW PARKOUR', 'game systems design', 'BMX AERIAL'),
        ('FLOWBOARDING / MUSIC CONCRETE', 'creative tools developer', 'FLOORBALL'),
        ('NEW WAVE / site specific atmospheric dance', 'VR AR ENVIRONMENT DESIGN', 'KORFBALL ATTACK (indoor wavepool surf)'),
        ('capoeira', 'festival director', 'acrobatic yoga'),
        (' rollerskating park recreational', 'regional designer', 'surfing'),
        ('Contemporary dance music / spontaneous edm djing', 'Real Time databoard visualisation', 'icehockey wing'),
        ('j turntablist / Indie rock comp', 'stunt performer', 'rhythmic fencing'),
        ('DJ turntablist binaural beat composition', 'game sound designer', 'BMX street'),
    ],
    # high gamma (공간) + high s (밝기) → 공간적 플로우, 야외
    'high_gammas': [
        ('SPACE ROCK', 'motion graphic designer', 'shortboard aerial surfing'),
        ('standup paddle boarding', 'ecological sketch from imagination', 'forest trail running'),
        ('nighttime cycling', 'wildlife documentary', 'inline aerial'),
        ('solo touring kayak / retrowave', 'light artist', 'paddleboard'),
        ('longboard surfing', 'schumann resonance dll designer', 'WINDSURFING'),
        ('longboard cruising', 'cinematic visual concept artist', 'snowboard downhill'),
        ('night time longboard', 'Installation artist', 'Darkroom photography'),
    ],
    # high r + high s → 고에너지 플로우
    'high_rs': [
        ('NOISEPOP', 'graffiti', 'ultimate frisbee creative role'),
        ('vert bowl skateboarding Ebm composition', 'match squash', 'longboard surfing'),
        ('SYNTHWAVE swimming butterfly 200m', 'game systems design', 'table tennis'),
        ('Karate synth pop', 'Gundam model kit', 'korfball defence'),
        ('aggressive inline', 'textile design', 'interactive media designer'),
        ('Street Skateboarding', 'kinetic art', 'strategy board game'),
        ('b boying', 'twitch arena fps', 'korfball defence'),
        ('Judo Clean and Jerk', 'vfx motion graphic artist', 'EXPERIMENTAL POP COMP'),
    ],
    # mid → 일반 플로우
    'mid': [
        ('indie folk', 'cartographic illustration', 'NORDIC SKIING'),
        ('rollerskating park recreational', 'independent fashion designer', 'yoga vinyasa afterwork'),
        ('gentle swimming', 'childrens book illustrator', 'slack lining'),
        ('tango', 'Interface designer', 'beach volleyball'),
        ('Play electric guitar, avant pop', 'light artist', 'paddleboard'),
        ('progressive rock', 'roller skating (park recreational)', 'taebo class'),
        ('Amb folk composition', 'software product manager (technical)', 'artistic swimming'),
        ('roller derby avant pop (city pop synth)', 'urban planning', 'trail running'),
    ],
}

# CONTRAST: d/s/r/p 지배 → 대비, 충돌, 파괴
CONTRAST_ACTIVITIES = {
    # high d (어둠) + high s (밝기) → 극단 대비
    'high_ds': [
        ('Noise pop composition', 'Conservation architect', 'Freeride snowboard'),
        ('noise ambient / yin yoga', 'taichi', 'Swimming'),
        ('noise rock', 'tactical training', 'rugby'),
        ('glitch opera', 'circuit bending', 'soil piezoenergy engineer'),
        ('no wave', 'canyoneering', 'open water swimming'),
        ('HAUNTOLOGY COMPOSITION', 'dark textile', 'abseiling'),
        ('noise ambient', 'salt paint art', 'nature photography'),
        ('minimal / deep techno', 'tax planner (coordinator)', '3 cushion'),
    ],
    # high d + high r → 파괴적 리듬
    'high_dr': [
        ('SMOKE JUMPER', 'graffiti', 'triathlon'),
        ('EXTREME SPORTS EVENT CREATOR', 'airsoft', 'BMX racing individual pursuit'),
        ('motorcross freestyle', 'motorcycle engine rebuild', 'metal alloy recycle grid operator'),
        ('muay thai', 'TV journalist', 'tactical precision fps'),
        ('mittwork shadow boxing', 'Wood carving', 'marksmanship'),
        ('Judo Clean and Jerk', 'vfx motion graphic artist', 'obstacle course racing'),
        ('Free jazz composition', 'horologist', 'free climbing'),
    ],
    # high s + high r → 밝은 충돌
    'high_sr': [
        ('EXPERIMENTAL POP COMP', 'Installation Artist', 'korfball defence'),
        ('mixed media digital analogue collage', 'rhythm roller skating', 'up cycling'),
        ('avant pop', 'light artist', 'board game competitive'),
        ('EXP. POP', 'Installation Artist', 'futsal'),
        ('Karate synth pop', 'Gundam model kit', 'korfball defence'),
        ('Judo Clean and Jerk', 'vfx motion graphic artist', 'EXPERIMENTAL POP COMP'),
    ],
    # mid → 일반 대비
    'mid': [
        ('shoegaze / longboard downhill', 'SEISMOLOGIST', 'SURFING FREERIDE'),
        ('mountain biking downhill', 'acrylic/paint pour', 'trail running steep'),
        ('drum machine sampler', 'cryptologist', 'inline skating aggressive'),
        ('noise rock', 'tactical training', 'rugby'),
        ('progressive techno', 'cryptographer', 'fjord coastal trekking'),
        ('Black Pottery', 'strategy board game', 'Street Skateboarding'),
        ('cliff diving', 'industrial graphic design', 'postrock / Hammock'),
    ],
}

# EMERGENCE: nu/gamma/h/g 지배 → 창발, 복합, 층위
EMERGENCE_ACTIVITIES = {
    # high nu (재귀) + high gamma (공간) → 프랙탈 창발
    'high_nugamma': [
        ('Experimental ambient composition', 'minimalistic architecture', 'indoor climbing'),
        ('Electronica composition', 'fractal art', 'polar trekking'),
        ('Berliner schule composition', 'textile designer', 'park/bowls skateboarding'),
        ('Ghibli adjacent / nighttime drone photography', 'cinematic visual concept artist', 'snowboard downhill'),
        ('CELLO SOLO', 'BIOSYSTEMS 3D PRINTING', 'Database Engineer'),
        ('zimmer style cinematic sound designer', 'Comic book graphic novel writing', 'breakdancing'),
        ('Triphop composition / splitboarding snowboard', 'hydrological engineer', 'fjord coastal trekking'),
    ],
    # high h (화성) + high g (구조) → 복합 구조 창발
    'high_hg': [
        ('symphonic prog', 'Distributed system architecture developer', 'lacrosse'),
        ('Folktronica composition Adventure racing', 'Biophillic architectural design', 'biathlon'),
        ('Contemporary classical / writing mystery novels', 'Leader who leads through debate and persuasion', 'EPEE FENCING'),
        ('Chamber pop', 'precision pen drawing', 'Digital forensics'),
        ('Lofi', 'quantum computing researcher', '4d printing'),
        ('Contemporary dance choreography', 'IOT Engineer', 'bouldering'),
        ('improvisational pianist', 'battleship shooting games', 'CLAY PIGEON SHOOTING'),
    ],
    # high nu + high h → 중첩 창작
    'high_nuh': [
        ('Comic book graphic novel writing', 'zimmer style cinematic sound designer', 'breakdancing'),
        ('feature film screenwriter', 'abseiling', 'cyanotype sun printing'),
        ('Epic Fantasy Writing', 'fantasy film screenwriter', 'solo hiking in falklands'),
        ('wetfolding origami', 'musicologist', 'Long distance swimming'),
        ('silver gelatin printing', 'peatland restoration professional', 'origami'),
        ('Letter press printing', 'water colour painting', 'open water swimming'),
    ],
    # mid → 일반 창발
    'mid': [
        ('acoustic arrangement', 'acoustic arrangement', 'yoga restorative'),
        ('ecological sketch from imagination', 'biomaterials engineer', 'forest trail running'),
        ('planatary stargazing', 'Landscape painting after work from memory or sunset', 'Freeride snowboard'),
        ('drone aerial photography', 'vr visual programming', 'ice dance'),
        ('ceramic art', 'Computer art', 'flyboarding hover'),
        ('marbling art ebru', 'netball wing attack', 'alps hiking'),
        ('needlepoint canvas work', 'tufting', 'running in the nature'),
        ('vivarium building', 'web design for her business', 'independent fashion designer'),
    ],
}

# ============================================================
# 4. 128 PERSONALITIES
# ============================================================

PERSONALITIES = [
    (1,'H',0,0,0),(2,'He',1,1,1),(3,'Li',2,0,0),(4,'Be',3,0,0),(5,'B',4,1,1),
    (6,'C',6,0,0),(7,'N',3,3,0),(8,'O',7,0,0),(9,'F',12,3,1),(10,'Ne',0,1,1),
    (11,'Na',5,1,1),(12,'Mg',10,0,2),(13,'Al',10,0,0),(14,'Si',7,0,0),(15,'P',7,0,2),
    (16,'S',5,1,2),(17,'Cl',12,0,2),(18,'Ar',8,0,0),(19,'K',8,1,1),(20,'Ca',15,0,0),
    (21,'Sc',0,0,0),(22,'Ti',12,1,1),(23,'V',10,0,3),(24,'Cr',0,1,2),(25,'Mn',5,0,3),
    (26,'Fe',11,1,1),(27,'Co',15,1,3),(28,'Ni',2,1,1),(29,'Cu',12,0,0),(30,'Zn',0,1,3),
    (31,'Ga',11,1,2),(32,'Ge',12,0,3),(33,'As',6,1,0),(34,'Se',11,1,0),(35,'Br',11,0,0),
    (36,'Kr',14,1,3),(37,'Rb',5,0,0),(38,'Sr',15,0,0),(39,'Y',15,0,3),(40,'Zr',5,1,2),
    (41,'Nb',3,1,0),(42,'Mo',11,1,3),(43,'Tc',3,1,3),(44,'Ru',13,0,2),(45,'Rh',14,0,3),
    (46,'Pd',9,1,0),(47,'Ag',10,0,0),(48,'Cd',10,1,2),(49,'In',10,1,0),(50,'Sn',8,0,3),
    (51,'Sb',10,1,3),(52,'Te',8,1,3),(53,'I',1,0,3),(54,'Xe',2,1,2),(55,'Cs',8,0,0),
    (56,'Ba',9,0,0),(57,'La',1,0,0),(58,'Ce',13,0,0),(59,'Pr',15,0,2),(60,'Nd',6,0,2),
    (61,'Pm',9,1,0),(62,'Sm',6,1,3),(63,'Eu',3,0,2),(64,'Gd',8,0,2),(65,'Tb',0,0,2),
    (66,'Dy',9,1,3),(67,'Ho',4,1,2),(68,'Er',12,1,2),(69,'Tm',6,1,0),(70,'Yb',2,0,0),
    (71,'Lu',13,0,3),(72,'Hf',14,1,0),(73,'Ta',10,1,1),(74,'W',7,1,2),(75,'Re',9,0,3),
    (76,'Os',8,1,0),(77,'Ir',3,1,0),(78,'Pt',2,1,3),(79,'Au',14,1,2),(80,'Hg',5,1,0),
    (81,'Tl',14,0,2),(82,'Pb',8,1,0),(83,'Bi',7,1,0),(84,'Po',6,1,2),(85,'At',11,0,2),
    (86,'Rn',4,0,0),(87,'Fr',5,0,0),(88,'Ra',9,0,2),(89,'Ac',3,0,0),(90,'Th',6,0,0),
    (91,'Pa',13,1,2),(92,'U',7,1,3),(93,'Np',1,1,3),(94,'Pu',1,0,0),(95,'Am',13,1,3),
    (96,'Cm',1,1,2),(97,'Bk',11,0,0),(98,'Cf',4,1,0),(99,'Es',2,1,0),(100,'Fm',3,1,2),
    (101,'Md',0,0,3),(102,'No',14,1,0),(103,'Lr',6,0,3),(104,'Rf',4,0,3),(105,'Db',15,1,0),
    (106,'Sg',13,0,0),(107,'Bh',1,1,0),(108,'Hs',7,0,0),(109,'Mt',11,0,3),(110,'Ds',15,1,0),
    (111,'Rg',4,1,3),(112,'Cn',7,0,3),(113,'Nh',5,1,3),(114,'Fl',1,0,2),(115,'Mc',14,0,0),
    (116,'Lv',15,1,2),(117,'Ts',14,0,0),(118,'Og',9,1,2),
]

# ============================================================
# 5. COMPUTE
# ============================================================

def compute_8d_vector(m, b, g):
    vec = impedance_vector(m)
    fv = flow(g)
    ew = BLOOD_WEIGHT[b]
    for k in vec:
        vec[k] *= ew
    for k in vec:
        vec[k] *= fv[k]
    return vec

def compute_shape_scores(vec):
    scores = {}
    for shape_name, shape_def in SHAPES.items():
        score = sum(vec[dim] * w for dim, w in shape_def['dims'].items())
        scores[shape_name] = round(score, 3)
    return scores

def classify_subshape(shape_name, vec):
    """8D 세부 값으로 서브카테고리 분류"""
    if shape_name == 'STRUCTURE':
        g, p, nu, d = vec['g'], vec['p'], vec['nu'], vec['d']
        if g > 0.3 and p > 0.3:
            return 'high_gp'
        elif nu > 0.25 and p > 0.25:
            return 'high_nup'
        elif d > 0.3 and g > 0.25:
            return 'high_dg'
        else:
            return 'mid'
    elif shape_name == 'FLOW':
        r, h, gamma, s = vec['r'], vec['h'], vec['gamma'], vec['s']
        if r > 0.3 and h > 0.3:
            return 'high_rh'
        elif gamma > 0.3 and s > 0.3:
            return 'high_gammas'
        elif r > 0.3 and s > 0.3:
            return 'high_rs'
        else:
            return 'mid'
    elif shape_name == 'CONTRAST':
        d, s, r, p = vec['d'], vec['s'], vec['r'], vec['p']
        if d > 0.3 and s > 0.3:
            return 'high_ds'
        elif d > 0.3 and r > 0.3:
            return 'high_dr'
        elif s > 0.3 and r > 0.3:
            return 'high_sr'
        else:
            return 'mid'
    elif shape_name == 'EMERGENCE':
        nu, gamma, h, g = vec['nu'], vec['gamma'], vec['h'], vec['g']
        if nu > 0.25 and gamma > 0.25:
            return 'high_nugamma'
        elif h > 0.3 and g > 0.3:
            return 'high_hg'
        elif nu > 0.25 and h > 0.3:
            return 'high_nuh'
        else:
            return 'mid'
    return 'mid'

def get_activities_for_shape(shape_name, subshape, vec, profile_hash):
    """서브카테고리에서 활동 선택 — 해시로 결정적 선택"""
    pools = {
        'STRUCTURE': STRUCTURE_ACTIVITIES,
        'FLOW': FLOW_ACTIVITIES,
        'CONTRAST': CONTRAST_ACTIVITIES,
        'EMERGENCE': EMERGENCE_ACTIVITIES,
    }
    pool = pools[shape_name].get(subshape, pools[shape_name]['mid'])
    idx = profile_hash % len(pool)
    return pool[idx]

def generate_mapping():
    results = []
    for num, sym, m, b, g in PERSONALITIES:
        mbti = MBTI_NAMES[m]
        blood = BLOOD_NAMES[b]
        gender = 'M' if g == 0 else 'F'
        profile = f"{mbti}_{gender}_{blood}"

        vec = compute_8d_vector(m, b, g)
        shape_scores = compute_shape_scores(vec)

        # Sort shapes by score descending
        sorted_shapes = sorted(shape_scores.items(), key=lambda x: -x[1])

        # Deterministic hash from profile
        profile_hash = hash(f"{num}_{sym}_{profile}") % 10000

        entry = {
            'num': num,
            'element': sym,
            'profile': profile,
            'mbti': mbti,
            'gender': gender,
            'blood': blood,
            'vector': {k: round(v, 3) for k, v in vec.items()},
            'shapes': {},
        }

        for shape_name, score in sorted_shapes:
            subshape = classify_subshape(shape_name, vec)
            activities = get_activities_for_shape(shape_name, subshape, vec, profile_hash + ord(shape_name[0]))
            entry['shapes'][shape_name] = {
                'score': score,
                'subshape': subshape,
                'music_creative': activities[0],
                'profession_tech': activities[1],
                'sport_body': activities[2],
            }

        results.append(entry)
    return results

# ============================================================
# 6. OUTPUT
# ============================================================

def main():
    mapping = generate_mapping()

    # JSON
    json_file = "c:/Users/User/Downloads/creative_4shapes_v2.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    # Markdown — 2.csv 스타일
    md_file = "c:/Users/User/Downloads/creative_4shapes_v2.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 128 성격 × 4 창의적 활동 모양 v2\n\n")
        f.write("2.csv 스타일: 구체적 장르 + 직업/기술 + 스포츠. 음식 없음.\n\n")
        f.write("## 4 모양\n\n")
        f.write("| 모양 | 지배 8D | 설명 |\n|---|---|---|\n")
        f.write("| STRUCTURE | g/p/nu/d | 건축적/체계적 — 조립, 설계, 정밀 |\n")
        f.write("| FLOW | r/h/gamma/s | 즉흥적/유동적 — 리듬, 공간, 흐름 |\n")
        f.write("| CONTRAST | d/s/r/p | 대비/충돌 — 파괴, 극단, 엣지 |\n")
        f.write("| EMERGENCE | nu/gamma/h/g | 창발/복합 — 층위, 프랙탈, 중첩 |\n\n")

        f.write("## 128 성격별 4 창의적 모양\n\n")
        f.write("| # | 원소 | 성격 | SHAPE_1 음악/창작 | 직업/기술 | 스포츠/신체 | SHAPE_2 음악/창작 | 직업/기술 | 스포츠/신체 | SHAPE_3 음악/창작 | 직업/기술 | 스포츠/신체 | SHAPE_4 음악/창작 | 직업/기술 | 스포츠/신체 |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")

        for entry in mapping:
            shapes = list(entry['shapes'].items())
            cells = []
            for shape_name, data in shapes:
                cells.append(data['music_creative'])
                cells.append(data['profession_tech'])
                cells.append(data['sport_body'])
            while len(cells) < 12:
                cells.append("-")
            f.write(f"| {entry['num']} | {entry['element']} | {entry['profile']} | "
                    f"{' | '.join(cells[:3])} | {' | '.join(cells[3:6])} | "
                    f"{' | '.join(cells[6:9])} | {' | '.join(cells[9:12])} |\n")

        f.write("\n## 상세\n\n")
        for entry in mapping:
            f.write(f"### {entry['num']}. {entry['element']} ({entry['profile']})\n\n")
            f.write(f"- **8D**: {entry['vector']}\n")
            for shape_name, data in entry['shapes'].items():
                f.write(f"- **{shape_name}** (score={data['score']:.3f}, sub={data['subshape']}): "
                        f"음악/창작={data['music_creative']} | "
                        f"직업/기술={data['profession_tech']} | "
                        f"스포츠/신체={data['sport_body']}\n")
            f.write("\n")

    # CSV — 2.csv 동일 포맷
    csv_file = "c:/Users/User/Downloads/creative_4shapes_v2.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("num,element,profile,shape1_music,shape1_tech,shape1_sport,shape2_music,shape2_tech,shape2_sport,shape3_music,shape3_tech,shape3_sport,shape4_music,shape4_tech,shape4_sport\n")
        for entry in mapping:
            shapes = list(entry['shapes'].items())
            row = [str(entry['num']), entry['element'], entry['profile']]
            for shape_name, data in shapes:
                row.append(data['music_creative'])
                row.append(data['profession_tech'])
                row.append(data['sport_body'])
            while len(row) < 15:
                row.append("")
            f.write(','.join(f'"{c}"' if ',' in str(c) else str(c) for c in row) + '\n')

    # 콘솔 출력 (처음 10개)
    for entry in mapping[:10]:
        print(f"\n{'='*70}")
        print(f"{entry['num']}. {entry['element']} ({entry['profile']})")
        print(f"8D: {entry['vector']}")
        for shape_name, data in entry['shapes'].items():
            print(f"  [{shape_name:12s}] {data['subshape']:15s} | "
                  f"{data['music_creative']:45s} | "
                  f"{data['profession_tech']:40s} | "
                  f"{data['sport_body']}")

    print(f"\nJSON: {json_file}")
    print(f"MD:   {md_file}")
    print(f"CSV:  {csv_file}")
    print(f"\n총 {len(mapping)} 성격 × 4 모양 × 3 활동 = {len(mapping)*4*3} 활동")

if __name__ == '__main__':
    main()
