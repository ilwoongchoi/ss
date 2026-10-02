import math

# 8D dims
DIMS = ['r','h','d','p','s','gamma','g','nu']

# MBTI 8D impedance
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

# 6 slot definitions
# Each slot: which dims boost, which dims suppress, special mods
SLOTS = {
    'AB_discharge': {
        'time': '21-3h',
        'boost': {'gamma': 0.3, 'nu': 0.3, 'd': 0.2},
        'suppress': {'r': 0.3, 's': 0.3, 'p': 0.2},
        'collapse': 0.7,
        'label': 'AB_DISCHARGE',
    },
    'A_awaken': {
        'time': '3-9h',
        'boost': {'h': 0.3, 'g': 0.2, 'r': 0.2},
        'suppress': {'d': 0.1, 'nu': 0.1},
        'collapse': 0.0,
        'label': 'A_AWAKEN',
    },
    'O_peak': {
        'time': '9-15h',
        'boost': {'s': 0.3, 'r': 0.2, 'p': 0.2},
        'suppress': {'d': 0.1, 'nu': 0.1},
        'collapse': 0.0,
        'label': 'O_PEAK',
    },
    'B_compress': {
        'time': '15-21h',
        'boost': {'d': 0.3, 'g': 0.2, 'gamma': 0.2},
        'suppress': {'s': 0.1, 'r': 0.1},
        'collapse': 0.0,
        'label': 'B_COMPRESS',
    },
    '3AM_random': {
        'time': '2-4h',
        'boost': {},
        'suppress': {},
        'collapse': 0.9,
        'random': ['p', 's', 'nu'],
        'label': '3AM_RANDOM',
    },
    '4:30AM_reset': {
        'time': '4-6h',
        'boost': {'s': 0.4, 'gamma': 0.3, 'nu': 0.2},
        'suppress': {'d': 0.2, 'g': 0.1},
        'collapse': 0.0,
        'label': '4:30AM_RESET',
    },
}

# 36 particles
PARTICLE_WEIGHTS = {
    'proton':    {'r': 0.7, 'p': 0.3},
    'gluon':     {'h': 0.6, 'r': 0.4},
    'muon':      {'g': 0.7, 's': 0.3},
    'electron':  {'s': 0.5, 'gamma': 0.5},
    'higgs':     {'p': 0.6, 's': 0.4},
    'w_boson':   {'nu': 0.6, 'd': 0.4},
    'z_boson':   {'d': 0.7, 'g': 0.3},
    'neutrino':  {'r': 0.6, 'gamma': 0.4},
    'tau':       {'d': 0.7, 'h': 0.3},
    'photon':    {'gamma': 0.7, 's': 0.3},
    'em':        {'gamma': 0.6, 's': 0.4},
    'up_quark':           {'s': 0.6, 'r': 0.4},
    'down_quark':         {'s': 0.5, 'h': 0.5},
    'charm_quark':        {'g': 0.6, 'nu': 0.4},
    'strange_quark':      {'d': 0.6, 's': 0.4},
    'top_quark':          {'g': 0.7, 'd': 0.3},
    'bottom_quark':       {'h': 0.6, 'g': 0.4},
    'tau_neutrino':       {'r': 0.5, 'd': 0.5},
    'electron_antineutrino': {'r': 0.6, 'gamma': 0.4},
    'muon_neutrino':      {'r': 0.5, 'g': 0.5},
    'muon_antineutrino':  {'r': 0.4, 'd': 0.6},
    'tau_antineutrino':   {'r': 0.4, 'p': 0.6},
    'neutron':            {'nu': 0.5, 'd': 0.5},
    'neutron_star':       {'g': 0.6, 'nu': 0.4},
    'dark_matter':        {'d': 0.6, 'nu': 0.4},
    'dark_energy':        {'gamma': 0.6, 'd': 0.4},
    'female_gaba':        {'h': 0.5, 'g': 0.5},
    'energy':             {'r': 0.6, 'p': 0.4},
    'clathrate_buffer':   {'g': 0.5, 'nu': 0.5},
    'malate_dehydrogenase': {'g': 0.5, 'd': 0.5},
    'ego_d2':             {'p': 0.6, 's': 0.4},
    'progesterone':       {'h': 0.6, 'gamma': 0.4},
    'testosterone':       {'r': 0.6, 'd': 0.4},
    'acetyl_coa':         {'g': 0.5, 'd': 0.5},
    'graviton':           {'g': 0.6, 'nu': 0.4},
    'axion':              {'nu': 0.6, 'gamma': 0.4},
}

# 118 personalities from PART V
# Format: (element_num, element_sym, mbti_idx, blood_idx, gender_idx)
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

def compute_slot_activity(m, b, g, slot_name):
    """Compute top 3 active particles for a given personality in a given slot."""
    vec = impedance_vector(m)
    fv = flow(g)
    ew = BLOOD_WEIGHT[b]
    
    slot = SLOTS[slot_name]
    
    # Apply slot boosts/suppressions
    for dim, val in slot.get('boost', {}).items():
        vec[dim] = min(1.0, vec[dim] + val)
    for dim, val in slot.get('suppress', {}).items():
        vec[dim] = max(0.0, vec[dim] - val)
    
    # Apply blood weight
    for k in vec:
        vec[k] *= ew
    # Apply gender flow
    for k in vec:
        vec[k] *= fv[k]
    
    # Apply collapse
    collapse = slot.get('collapse', 0.0)
    
    # Random dims (3AM)
    import random
    random.seed(42)  # deterministic
    if 'random' in slot:
        for dim in slot['random']:
            vec[dim] = random.random()
    
    # Compute particle values
    results = {}
    for particle, weights in PARTICLE_WEIGHTS.items():
        base = sum(vec[dim] * w for dim, w in weights.items())
        value = base
        if collapse > 0 and particle != 'neutrino':
            value *= (1.0 - collapse * 0.7)
        # 3AM special: neutrino boosts, axion boosts
        if slot_name == '3AM_random':
            if particle in ['neutrino', 'axion', 'dark_matter', 'graviton']:
                value *= 1.5
        # 4:30AM special: photon, em, z_boson boost
        if slot_name == '4:30AM_reset':
            if particle in ['photon', 'em', 'z_boson', 'electron_antineutrino']:
                value *= 1.3
        # AB special: gluon, axion, dark_energy active
        if slot_name == 'AB_discharge':
            if particle in ['gluon', 'axion', 'dark_energy', 'graviton', 'dark_matter']:
                value *= 1.2
        # A special: muon, charm_quark, testosterone active
        if slot_name == 'A_awaken':
            if particle in ['muon', 'charm_quark', 'testosterone', 'tau_antineutrino']:
                value *= 1.2
        # O special: proton, photon, up_quark, energy active
        if slot_name == 'O_peak':
            if particle in ['proton', 'photon', 'up_quark', 'energy', 'neutron', 'progesterone', 'acetyl_coa']:
                value *= 1.2
        # B special: tau, higgs, top_quark, ego_d2, dark_energy active
        if slot_name == 'B_compress':
            if particle in ['tau', 'higgs', 'top_quark', 'ego_d2', 'dark_energy', 'neutron_star', 'clathrate_buffer']:
                value *= 1.2
        
        value = max(0.0, min(1.0, value))
        results[particle] = round(value, 2)
    
    # Top 3 particles
    top3 = sorted(results.items(), key=lambda x: -x[1])[:3]
    return top3, results

# Generate mapping
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

output = []
def p(s=''):
    output.append(s)

p("# PART V-B: 118 PERSONALITIES × 6 SLOT ACTIVITY MAPPING")
p()
p("6 Slots: AB_DISCHARGE (21-3h) | A_AWAKEN (3-9h) | O_PEAK (9-15h) | B_COMPRESS (15-21h) | 3AM_RANDOM (2-4h) | 4:30AM_RESET (4-6h)")
p()
p("Each personality shows top 3 active particles per slot.")
p()
p("---")
p()

for num, sym, m, b, g in PERSONALITIES:
    mbti = MBTI_NAMES[m]
    blood = BLOOD_NAMES[b]
    gender = 'M' if g == 0 else 'F'
    profile = f"{mbti}_{gender}_{blood}"
    
    p(f"## {num}. {sym} ({profile})")
    p()
    
    slot_keys = ['AB_discharge', 'A_awaken', 'O_peak', 'B_compress', '3AM_random', '4:30AM_reset']
    slot_labels = ['AB_DISCHARGE', 'A_AWAKEN', 'O_PEAK', 'B_COMPRESS', '3AM_RANDOM', '4:30AM_RESET']
    slot_times = ['21-3h', '3-9h', '9-15h', '15-21h', '2-4h', '4-6h']
    
    for i, sn in enumerate(slot_keys):
        top3, _ = compute_slot_activity(m, b, g, sn)
        particles_str = ', '.join([f"{p_name}({v:.2f})" for p_name, v in top3])
        p(f"- **{slot_labels[i]} ({slot_times[i]})**: {particles_str}")
    
    p()

# Write to file
with open('_slot_final.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print(f'Written {len(output)} lines to _slot_final.md')
