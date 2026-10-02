"""
128 성격 × 먹을거(Food) 노드 매핑
CIRCUITFILE.MD의 모든 먹을거/대사/소화/영양 관련 노드만 추출하여
128 성격에 대해 색상 매칭 수행

먹을거 노드 = 음식 섭취, 소화, 대사, 영양소, 포만/허기, 미생물 발효 관련 노드
"""

import json
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

# ============================================================
# 1. BASE COLOR SYSTEM (RGB)
# ============================================================

RGB = {
    'RED':          (255,   0,   0),
    'GREEN':        (  0, 255,   0),
    'BLUE':         (  0,   0, 255),
    'YELLOW':       (255, 255,   0),
    'WHITE':        (255, 255, 255),
    'BLACK':        (  0,   0,   0),
    'CYAN':         (  0, 255, 255),
    'ORANGE':       (255, 165,   0),
    'RED-ORANGE':   (255,  69,   0),
    'BROWN':        (139,  69,  19),
    'DARK-BROWN':   (101,  67,  33),
    'DARK-GREEN':   (  0, 100,   0),
    'PALE-GREEN':   (152, 251, 152),
    'RED-BROWN':    (165,  42,  42),
    'BLUE-WHITE':   (224, 255, 255),
    'PALE-YELLOW':  (255, 255, 200),
    'PURPLE':       (128,   0, 128),
    'RED-PURPLE':   (160,  32, 100),
    'PINK':         (255, 192, 203),
    'GRAY':         (128, 128, 128),
    'DARK-GRAY':    ( 64,  64,  64),
    'SAND-YELLOW':  (238, 214, 122),
    'LILAC':        (200, 162, 200),
    'CRIMSON':      (220,  20,  60),
    'MAROON':       (128,   0,   0),
    'MAGENTA':      (255,   0, 255),
}

# ============================================================
# 2. 4-CHANNEL DAY/NIGHT
# ============================================================

CHANNEL_COLORS = {
    'BW': {'particle': 'gluon',    'day': RGB['GREEN'],  'night': RGB['YELLOW']},
    'BM': {'particle': 'photon',   'day': RGB['YELLOW'], 'night': RGB['RED']},
    'SW': {'particle': 'quark',    'day': RGB['BLUE'],   'night': RGB['GREEN']},
    'SM': {'particle': 'neutrino', 'day': RGB['RED'],    'night': RGB['BLUE']},
}

BLOOD_TYPE_CHANNEL = {'AB': 'BW', 'O': 'BM', 'A': 'SW', 'B': 'SM'}

MBTI_MIDDLE = {
    'NF': ( 20,   0,  20),
    'ST': ( 20,  20,   0),
    'SF': (  0,  20,   0),
    'NT': (  0,   0,  20),
}

MBTI_END = {
    'EP': ( 15,  15,   0),
    'EJ': ( 15,   0,   0),
    'IJ': (  0,   0,  15),
    'IP': (  0,  15,   0),
}

# ============================================================
# 3. PERSONALITY
# ============================================================

@dataclass
class Personality:
    mbti: str
    gender: str
    blood_type: str
    element: str = ""

    @property
    def code(self) -> str:
        return f"{self.mbti}_{self.gender}_{self.blood_type}"

    @property
    def channel(self) -> str:
        return BLOOD_TYPE_CHANNEL[self.blood_type]

    @property
    def middle(self) -> str:
        return self.mbti[1:3]

    @property
    def end(self) -> str:
        # last 2 chars: FP, FJ, TP, TJ → map to EP/EJ/IJ/IP
        last = self.mbti[2:4]
        # E/I from first char, P/J from last char
        ei = self.mbti[0]  # E or I
        pj = self.mbti[3]  # P or J
        return f"{ei}{pj}"  # EP, EJ, IP, IJ

    def base_color(self, hour: int) -> Tuple[int,int,int]:
        dn = 'day' if 6 <= hour < 18 else 'night'
        return CHANNEL_COLORS[self.channel][dn]

    def color(self, hour: int) -> Tuple[int,int,int]:
        base = self.base_color(hour)
        mid = MBTI_MIDDLE[self.middle]
        end = MBTI_END[self.end]
        r = max(0, min(255, base[0] + mid[0] + end[0]))
        g = max(0, min(255, base[1] + mid[1] + end[1]))
        b = max(0, min(255, base[2] + mid[2] + end[2]))
        return (r, g, b)


# ============================================================
# 4. FOOD NODES — 먹을거 관련 노드만
# ============================================================

@dataclass
class FoodNode:
    name: str
    food_function: str        # 음식/영양 관점에서의 기능
    location: str
    color_name: str
    color_rgb: Tuple[int,int,int]
    element: str = ""
    particle: str = ""
    food_category: str = ""   # 음식 카테고리


FOOD_NODES: List[FoodNode] = [
    # --- 포만/허기 호르몬 (Satiety/Hunger Hormones) ---
    FoodNode('glp1', 'GLP-1 인크레틴 — 식후 포만감, 장-뇌 축',
             'upper abdomen center', 'WHITE', RGB['WHITE'],
             element='Tb(65)/Dy(66)', particle='gluon',
             food_category='포만호르몬'),
    FoodNode('cck', 'CCK 콜레시스토키닌 — 식후 포만감, 담낭수축',
             'pancreas posterior', 'RED', RGB['RED'],
             element='Cf(98)', particle='w_boson',
             food_category='포만호르몬'),
    FoodNode('opioid_and', '포만-보상-치유 완전 일치 — 식사 만족감',
             'left levator superioris', 'WHITE', RGB['WHITE'],
             food_category='포만허기'),
    FoodNode('opioid_nor', '절대 허기 — 대사 진공 상태',
             'left levator superioris', 'BLACK', RGB['BLACK'],
             food_category='포만허기'),
    FoodNode('opioid_xnor_or', '포만/허기 위상 안정 — 식사 주기 균형',
             'left levator superioris', 'WHITE', RGB['WHITE'],
             food_category='포만허기'),
    FoodNode('bioenergetic_drive_and', '대사 구동 — 음식→에너지 변환 허락',
             'center torso', 'YELLOW', RGB['YELLOW'],
             food_category='대사구동'),

    # --- 아미노산/단백질 (Amino Acids / Proteins) ---
    FoodNode('methionine', '메티오닌 — 단백질 합성 시작 코돈, 황 아미노산',
             'right exterior hip', 'YELLOW', RGB['YELLOW'],
             element='Ge(32)', particle='z_boson',
             food_category='아미노산'),
    FoodNode('cysteine', '시스테인 — 글루타티온 전구체, 황 아미노산',
             'right medial canthus', 'RED', RGB['RED'],
             element='Fr(87)', particle='energy',
             food_category='아미노산'),
    FoodNode('glutathione', '글루타티온 — GSH 항산화 버퍼, 간 합성',
             'right entorhinal cortex', 'PALE-YELLOW', RGB['PALE-YELLOW'],
             food_category='항산화영양소'),
    FoodNode('collagen', '콜라겐 — 삼중 나선 구조 단백질, 결합조직',
             'connective tissue global', 'WHITE', RGB['WHITE'],
             element='Sr(38)', particle='tau',
             food_category='단백질'),
    FoodNode('disulfide_bond', '이황화 결합 — S-S 브릿지, 단백질 구조 안정화',
             'right medial canthus', 'YELLOW', RGB['YELLOW'],
             food_category='단백질구조'),
    FoodNode('substance_p', '서브스턴스 P — 신경펩타이드, 통증/염증',
             'left lumbar paraspinal', 'GREEN', RGB['GREEN'],
             element='Ra(88)', particle='bottom_quark',
             food_category='신경펩타이드'),

    # --- TCA 회로 / 에너지 대사 (TCA Cycle / Energy Metabolism) ---
    FoodNode('citric_acid_cycle', 'TCA 회로 — 시트르산 회로, 식품→ATP',
             'center abdomen', 'PALE-YELLOW', RGB['PALE-YELLOW'],
             particle='TCA',
             food_category='에너지대사'),
    FoodNode('succinate_dehydrogenase', 'SDH Complex II — 숙신산→푸마르산',
             'right axillary tendon', 'ORANGE', RGB['ORANGE'],
             element='Br(35)/Kr(36)', particle='muon_neutrino',
             food_category='에너지대사'),
    FoodNode('lactate_dehydrogenase', 'LDH — 피루브이트↔락테이트, 무산소/유산소',
             'muscle / heart', 'PALE-YELLOW', RGB['PALE-YELLOW'],
             particle='right_testosterone',
             food_category='에너지대사'),
    FoodNode('cytochrome_c_oxidase', 'COX Complex IV — O2→H2O, 최종 전자수용체',
             'left occipitalis inner top', 'RED-PURPLE', RGB['RED-PURPLE'],
             element='Be(4)', particle='z_boson',
             food_category='에너지대사'),
    FoodNode('pentose_phosphate', 'PPP — NADPH 생산, GSH 재활용',
             'left lateral torso', 'PALE-YELLOW', RGB['PALE-YELLOW'],
             particle='neutron_star',
             food_category='에너지대사'),
    FoodNode('proton_pump', '프로톤 펌프 — H+ 펌프, 위산/미토콘드리아',
             'left occipitalis', 'RED', RGB['RED'],
             food_category='소화'),
    FoodNode('heme', '헴 — Fe2+ 포르피린, 철 흡수/이용',
             'left nipple inner', 'RED', RGB['RED'],
             element='H(1)', particle='proton',
             food_category='미네랄'),
    FoodNode('hemoglobin', '헤모글로빈 — O2 운반, Fe2+→Fe3+ 전하 이동',
             'right nipple inner', 'RED-BROWN', RGB['RED-BROWN'],
             element='Rf(104)', particle='proton_to_photon',
             food_category='미네랄'),
    FoodNode('ferritin', '페리틴 — 철 저장, Fe 나노케이지',
             'left lat dorsi', 'DARK-BROWN', RGB['DARK-BROWN'],
             element='Mn(25)', particle='muon_antineutrino',
             food_category='미네랄'),

    # --- 미네랄/이온 (Minerals / Ions) ---
    FoodNode('NaCl', '소금 — NaCl 활동전위, 이온 리셋',
             'left ankle / right', 'WHITE', RGB['WHITE'],
             element='Pu(94)/Am(95)', particle='spark',
             food_category='미네랄'),
    FoodNode('sodium', '나트륨 — Na+ 삼투, NaK-ATPase',
             'global / renal', 'YELLOW', RGB['YELLOW'],
             element='Na(11)', particle='w_boson',
             food_category='미네랄'),
    FoodNode('chlorine_ion_pump', '염소 이온 펌프 — Cl- 채널, GABA-A 결합',
             'global / neuronal', 'PALE-GREEN', RGB['PALE-GREEN'],
             element='Cl(17)', particle='electron',
             food_category='미네랄'),
    FoodNode('carbonic_anhydrase', '탄산 탈수효소 — CO2+H2O⇌HCO3-+H+, 산-염기 평형',
             'blood / RBC', 'YELLOW', RGB['YELLOW'],
             particle='right_testosterone',
             food_category='소화'),
    FoodNode('copper_iron_complex', 'Cu-Fe 복합체 — 혼합 원가족속 산화환원',
             'left inner bum', 'GREEN', RGB['GREEN'],
             element='Ba(56)', particle='charm_quark',
             food_category='미네랄'),
    FoodNode('manganese_nodule', '망간 노듈 — Mn 산화물 침적, 미네랄 저장',
             'left lateral malleolus', 'DARK-BROWN', RGB['DARK-BROWN'],
             particle='gluon',
             food_category='미네랄'),
    FoodNode('iodine', '요오드 — 갑상선 T3/T4 합성, 요오드화',
             'right posterior throat', 'BLUE-WHITE', RGB['BLUE-WHITE'],
             particle='photon_to_higgs',
             food_category='미네랄'),

    # --- 항산화/식물영양소 (Antioxidants / Phytonutrients) ---
    FoodNode('sulforaphane', '술포라판 — 십자화과 채소, Nrf2/ARE 경로',
             'left hippocampus tail', 'DARK-GREEN', RGB['DARK-GREEN'],
             element='Ar(18)', particle='gluon',
             food_category='식물영양소'),
    FoodNode('peonidine', '페오니딘 — 안토시아닌, 적/청 pH 의존 색소',
             'right thumb toe', 'RED', RGB['RED'],
             element='Sb(51)', particle='energy',
             food_category='식물영양소'),

    # --- 미생물/발효 (Microbiome / Fermentation) ---
    FoodNode('methanogenesis', '메탄생성 — 장내 고세균 CH4 생산',
             'gut / right 1st metatarsal', 'PALE-GREEN', RGB['PALE-GREEN'],
             element='Tb(65)/Dy(66)', particle='gluon',
             food_category='장내미생물'),
    FoodNode('nitrogenase', '질소고정효소 — N2+8H+→2NH3, 단백질 합성 원료',
             'left lateral thigh', 'DARK-BROWN', RGB['DARK-BROWN'],
             particle='electron_antineutrino',
             food_category='장내미생물'),
    FoodNode('chrna7_vagal', 'α7 nAChR — 미주신경 콜린성 항염 경로',
             'right temporalis', 'GREEN', RGB['GREEN'],
             element='Es(99)', particle='tau_neutrino',
             food_category='장내미생물'),

    # --- 소화/흡수 (Digestion / Absorption) ---
    FoodNode('choline', '콜린 — ACh 전구체, 뇌-장 축',
             'left cervical', 'WHITE', RGB['WHITE'],
             element='E120', particle='precursor',
             food_category='소화'),
    FoodNode('right_acetylcholine', '아세틸콜린 — 콜린성 미주신경, 소화 구동',
             'right temporalis', 'GREEN', RGB['GREEN'],
             element='Es(99)', particle='tau_neutrino',
             food_category='소화'),
    FoodNode('water', '물 — H2O, 수분 공급, 용매',
             'center torso', 'BLUE-WHITE', RGB['BLUE-WHITE'],
             element='Po(84)', particle='right_testosterone',
             food_category='수분'),
    FoodNode('water_vapour', '수증기 — 수분 보존, 호흡 수분',
             'right posterior pelvis', 'BLUE-WHITE', RGB['BLUE-WHITE'],
             element='Bk(97)', particle='neutrino',
             food_category='수분'),

    # --- 탄수화물/탄소 대사 (Carbohydrate / Carbon Metabolism) ---
    FoodNode('carbon', '탄소 대사 래치 — 동화/이화, 식품 탄소 흐름',
             'center abdomen', 'GRAY', RGB['GRAY'],
             element='C(6)', particle='photon',
             food_category='탄수화물'),
    FoodNode('co2', 'CO2 — 호흡, TCA 회로 최종 산물',
             'center / global', 'BLACK', RGB['BLACK'],
             element='Th(90)/Pa(91)', particle='dark_energy',
             food_category='탄수화물'),

    # --- 자가포식/재활용 (Autophagy / Recycling) ---
    FoodNode('autophagy', '자가포식 — 세포 자가 분해, 영양 재활용',
             'left lat dorsi', 'DARK-GREEN', RGB['DARK-GREEN'],
             element='Rh(45)', particle='gluon',
             food_category='자가포식'),

    # --- Maillard 반응 (Maillard Reaction) ---
    FoodNode('maillard', 'Maillard 반응 — 당+아미노산 축합, AGE 축적',
             'right entorhinal cortex', 'BROWN', RGB['BROWN'],
             food_category='조리반응'),

    # --- 기타 식품 관련 (Other Food-Related) ---
    FoodNode('mangrove_aerenchyma', '망그로브 통기조직 — O2 공급, 산소 전달',
             'right upper rib cage', 'PALE-GREEN', RGB['PALE-GREEN'],
             particle='female_gaba',
             food_category='산소공급'),
    FoodNode('caco3', '탄산칼슘 — CaCO3 완충, pH 안정화',
             'left fourth finger', 'WHITE', RGB['WHITE'],
             element='K(19)', particle='up_quark',
             food_category='미네랄'),
]


# ============================================================
# 5. COLOR MATCHING
# ============================================================

def rgb_distance(c1, c2):
    return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)

def color_similarity(c1, c2):
    max_dist = math.sqrt(3 * 255**2)
    return 1.0 - (rgb_distance(c1, c2) / max_dist)


# ============================================================
# 6. 128 PERSONALITIES
# ============================================================

MBTI_TYPES = [
    'ENFP', 'ENFJ', 'ENTP', 'ENTJ',
    'ESFP', 'ESFJ', 'ESTP', 'ESTJ',
    'INFP', 'INFJ', 'INTP', 'INTJ',
    'ISFP', 'ISFJ', 'ISTP', 'ISTJ',
]

GENDERS = ['M', 'F']
BLOOD_TYPES = ['O', 'A', 'B', 'AB']


# Element assignment for 128 personalities (1-118 periodic + 10 beyond)
ELEMENT_MAP = {
    'ENFP_M_O': 'H(1)',    'ISFP_F_A': 'He(2)',   'ESFJ_M_A': 'Li(3)',   'INTP_M_A': 'Be(4)',
    'ENTP_F_A': 'B(5)',    'ESTP_M_O': 'C(6)',    'INTP_M_AB': 'N(7)',   'ISTP_M_A': 'O(8)',
    'ESTJ_F_AB': 'F(9)',   'ENFP_F_A': 'Ne(10)',  'INFJ_F_A': 'Na(11)',  'ESFP_M_B': 'Mg(12)',
    'ESFP_M_O': 'Al(13)',  'ISTP_M_O': 'Si(14)',  'ISTP_M_B': 'P(15)',   'INFJ_F_B': 'S(16)',
    'ESTJ_M_B': 'Cl(17)',  'ENFJ_M_O': 'Ar(18)',  'ENFJ_F_B': 'K(19)',   'ENTJ_M_O': 'Ca(20)',
    'ENFP_M_A': 'Sc(21)',  'ESTJ_F_A': 'Ti(22)',  'ESFP_M_AB': 'V(23)',  'ENFP_F_B': 'Cr(24)',
    'INFJ_M_AB': 'Mn(25)', 'ISTJ_F_A': 'Fe(26)',  'ENTJ_F_AB': 'Co(27)', 'ESFJ_F_A': 'Ni(28)',
    'ESTJ_M_O': 'Cu(29)',  'ENFP_F_AB': 'Zn(30)', 'ISTJ_F_B': 'Ga(31)',  'ESTJ_M_AB': 'Ge(32)',
    'ESTP_F_O': 'As(33)',  'ISTJ_F_O': 'Se(34)',  'ISTJ_M_A': 'Br(35)',  'ISFJ_F_AB': 'Kr(36)',
    'INFJ_M_A': 'Rb(37)',  'ENTJ_M_A': 'Sr(38)',  'ENTJ_M_AB': 'Y(39)',  'INFJ_F_B_2': 'Zr(40)',
    'INTP_F_O': 'Nb(41)',  'ISTJ_F_AB': 'Mo(42)', 'INTP_F_AB': 'Tc(43)', 'INFP_M_B': 'Ru(44)',
    'ISFJ_M_AB': 'Rh(45)', 'INTJ_F_O': 'Pd(46)',  'ESFP_M_A': 'Ag(47)',  'ESFP_F_B': 'Cd(48)',
    'ESFP_F_O': 'In(49)',  'ENFJ_M_AB': 'Sn(50)', 'ESFP_F_AB': 'Sb(51)', 'ENFJ_F_AB': 'Te(52)',
    'ISFP_M_AB': 'I(53)',  'ESFJ_F_B': 'Xe(54)',  'ENFJ_M_A': 'Cs(55)',  'INTJ_M_A': 'Ba(56)',
    'ISFP_M_O': 'La(57)',  'INFP_M_A': 'Ce(58)',  'ENTJ_M_B': 'Pr(59)',  'ESTP_M_B': 'Nd(60)',
    'INTJ_F_A': 'Pm(61)',  'ESTP_F_AB': 'Sm(62)', 'INTP_M_B': 'Eu(63)',  'ENFJ_M_B': 'Gd(64)',
    'ENFP_M_B': 'Tb(65)',  'INTJ_F_AB': 'Dy(66)', 'ENTP_F_B': 'Ho(67)',  'ESTJ_F_B': 'Er(68)',
    'ESTP_F_A': 'Tm(69)',  'ESFJ_M_O': 'Yb(70)',  'INFP_M_AB': 'Lu(71)', 'ISFJ_F_A': 'Hf(72)',
    'ESFP_F_A': 'Ta(73)',  'ISTP_F_B': 'W(74)',   'INTJ_M_AB': 'Re(75)', 'ENFJ_F_O': 'Os(76)',
    'INTP_F_A': 'Ir(77)',  'ESFJ_F_AB': 'Pt(78)', 'ISFJ_F_B': 'Au(79)',  'INFJ_F_O': 'Hg(80)',
    'ISFJ_M_B': 'Tl(81)',  'ENFJ_F_A': 'Pb(82)',  'ISTP_F_O': 'Bi(83)',  'ESTP_F_B_2': 'Po(84)',
    'ISTJ_M_B': 'At(85)',  'ENTP_M_A': 'Rn(86)',  'INFJ_M_O': 'Fr(87)',  'INTJ_M_B': 'Ra(88)',
    'INTP_M_O': 'Ac(89)',  'ESTP_M_A': 'Th(90)',  'INFP_F_B': 'Pa(91)',  'ISTP_F_AB': 'U(92)',
    'ISFP_F_AB': 'Np(93)', 'ISFP_M_A': 'Pu(94)',  'INFP_F_AB': 'Am(95)', 'ISFP_F_B': 'Cm(96)',
    'ISTJ_M_O': 'Bk(97)',  'ENTP_F_O': 'Cf(98)',  'ESFJ_F_O': 'Es(99)',  'INTP_F_B': 'Fm(100)',
    'ENFP_M_AB': 'Md(101)','ISFJ_F_O': 'No(102)', 'ESTP_M_AB': 'Lr(103)', 'ENTP_M_AB': 'Rf(104)',
    'ENTJ_F_O': 'Db(105)', 'INFP_M_O': 'Sg(106)', 'ISFP_F_O': 'Bh(107)', 'ISTP_M_A_2': 'Hs(108)',
    'ISTJ_M_AB': 'Mt(109)','ENTJ_F_A': 'Ds(110)', 'ENTP_F_AB': 'Rg(111)','ISTP_M_AB': 'Cn(112)',
    'INFJ_F_AB': 'Nh(113)','ISFP_M_B_2': 'Fl(114)','ISFJ_M_O': 'Mc(115)','ENTJ_F_B': 'Lv(116)',
    'ISFJ_M_A': 'Ts(117)','INTJ_F_B': 'Og(118)',
}


def generate_128_personalities():
    personalities = []
    for mbti in MBTI_TYPES:
        for gender in GENDERS:
            for blood in BLOOD_TYPES:
                code = f"{mbti}_{gender}_{blood}"
                elem = ELEMENT_MAP.get(code, '')
                personalities.append(Personality(
                    mbti=mbti, gender=gender, blood_type=blood, element=elem
                ))
    return personalities


# ============================================================
# 7. FOOD MAPPING — 128 성격 × 먹을거 노드
# ============================================================

def match_personality_to_food_nodes(personality, nodes, hour, top_n=10):
    p_color = personality.color(hour)
    scored = []
    for node in nodes:
        sim = color_similarity(p_color, node.color_rgb)
        scored.append((node, sim))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]


def full_food_mapping(personalities, nodes, hours, top_n=5):
    result = {}
    for p in personalities:
        result[p.code] = {
            'element': p.element,
            'mbti': p.mbti,
            'gender': p.gender,
            'blood_type': p.blood_type,
            'channel': p.channel,
            'time_slots': {}
        }
        for h in hours:
            dn = 'day' if 6 <= h < 18 else 'night'
            p_color = p.color(h)
            matches = match_personality_to_food_nodes(p, nodes, h, top_n)
            result[p.code]['time_slots'][f"{h:02d}h"] = {
                'day_night': dn,
                'personality_rgb': list(p_color),
                'top_food_nodes': [
                    {
                        'node': n.name,
                        'food_function': n.food_function,
                        'food_category': n.food_category,
                        'location': n.location,
                        'node_color': n.color_name,
                        'node_rgb': list(n.color_rgb),
                        'similarity': round(sim, 4),
                    }
                    for n, sim in matches
                ]
            }
    return result


# ============================================================
# 8. MAIN
# ============================================================

def main():
    print("=" * 80)
    print("128 성격 × 먹을거(Food) 노드 매핑")
    print("CIRCUITFILE.MD 먹을거/대사/소화/영양 관련 노드만")
    print("=" * 80)

    personalities = generate_128_personalities()
    print(f"\n128 성격 생성: {len(personalities)}")
    print(f"먹을거 노드 수: {len(FOOD_NODES)}")

    # 카테고리별 노드 수
    print("\n먹을거 카테고리별 노드 수:")
    cats = {}
    for n in FOOD_NODES:
        cats[n.food_category] = cats.get(n.food_category, 0) + 1
    for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat:15s} : {cnt}개")

    # 색상별 노드 수
    print("\n먹을거 노드 색상 분포:")
    color_counts = {}
    for n in FOOD_NODES:
        color_counts[n.color_name] = color_counts.get(n.color_name, 0) + 1
    for color, cnt in sorted(color_counts.items(), key=lambda x: -x[1]):
        print(f"  {color:15s} : {cnt}개")

    # 예시: ENFP_M_O (H(1) — proton)
    print("\n" + "=" * 60)
    print("예시: ENFP_M_O (H(1) — proton, RED)")
    print("=" * 60)
    enfp = next(p for p in personalities if p.code == 'ENFP_M_O')
    for h in [2, 8, 12, 18, 22]:
        dn = 'day' if 6 <= h < 18 else 'night'
        color = enfp.color(h)
        print(f"\n  {h:02d}h [{dn}]")
        matches = match_personality_to_food_nodes(enfp, FOOD_NODES, h, top_n=5)
        for node, sim in matches:
            print(f"    → {node.name:25s} [{node.food_category:10s}] {node.color_name:15s} sim={sim:.3f}  {node.food_function[:35]}")

    # 예시: ISTP_M_O (O(8) — Nonmetal, YELLOW)
    print("\n" + "=" * 60)
    print("예시: ISTP_M_O (O(8) — Nonmetal, YELLOW)")
    print("=" * 60)
    istp = next(p for p in personalities if p.code == 'ISTP_M_O')
    for h in [2, 8, 12, 18, 22]:
        dn = 'day' if 6 <= h < 18 else 'night'
        color = istp.color(h)
        print(f"\n  {h:02d}h [{dn}]")
        matches = match_personality_to_food_nodes(istp, FOOD_NODES, h, top_n=5)
        for node, sim in matches:
            print(f"    → {node.name:25s} [{node.food_category:10s}] {node.color_name:15s} sim={sim:.3f}  {node.food_function[:35]}")

    # 전체 매핑 JSON 저장
    print("\n" + "=" * 60)
    print("전체 매핑 생성 중... (128 성격 × 5 시간대 × top-5 먹을거 노드)")
    print("=" * 60)

    sample_hours = [2, 8, 12, 18, 22]
    mapping = full_food_mapping(personalities, FOOD_NODES, sample_hours, top_n=5)

    output_file = "c:/Users/User/Downloads/food_128_mapping.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"\n저장: {output_file}")
    print(f"  {len(personalities)} 성격 × {len(sample_hours)} 시간대 × top-5 먹을거 노드")
    print(f"  {len(FOOD_NODES)} 먹을거 노드 (먹을거/대사/소화/영양 관련만)")

    # Markdown 테이블 저장
    md_file = "c:/Users/User/Downloads/food_128_mapping.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 128 성격 × 먹을거(Food) 노드 매핑\n\n")
        f.write("CIRCUITFILE.MD의 먹을거/대사/소화/영양 관련 노드만 추출하여 128 성격에 매핑.\n\n")
        f.write(f"총 먹을거 노드: {len(FOOD_NODES)}개\n\n")

        f.write("## 먹을거 카테고리\n\n")
        f.write("| 카테고리 | 노드 수 | 노드 목록 |\n|---|---|---|\n")
        cat_nodes = {}
        for n in FOOD_NODES:
            cat_nodes.setdefault(n.food_category, []).append(n.name)
        for cat in sorted(cat_nodes.keys()):
            nodes_str = ', '.join(cat_nodes[cat])
            f.write(f"| {cat} | {len(cat_nodes[cat])} | {nodes_str} |\n")

        f.write("\n## 먹을거 노드 색상 분포\n\n")
        f.write("| 색상 | Hex | 노드 수 |\n|---|---|---|\n")
        hex_map = {
            'RED': '#FF0000', 'GREEN': '#00FF00', 'BLUE': '#0000FF',
            'YELLOW': '#FFFF00', 'WHITE': '#FFFFFF', 'BLACK': '#000000',
            'ORANGE': '#FFA500', 'DARK-BROWN': '#654321', 'BROWN': '#8B4513',
            'PALE-YELLOW': '#FFFFC8', 'PALE-GREEN': '#98FB98',
            'DARK-GREEN': '#006400', 'RED-BROWN': '#A52A2A',
            'BLUE-WHITE': '#E0FFFF', 'GRAY': '#808080',
            'RED-PURPLE': '#A02060',
        }
        for color, cnt in sorted(color_counts.items(), key=lambda x: -x[1]):
            hex_val = hex_map.get(color, '#FFFFFF')
            f.write(f"| {color} | `{hex_val}` | {cnt} |\n")

        f.write("\n## 128 성격별 top-3 먹을거 노드 (12h 낮 기준)\n\n")
        f.write("| # | 성격 | 원소 | 채널 | 색상 | top-1 먹을거 | top-2 | top-3 |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for i, p in enumerate(personalities, 1):
            p_color = p.color(12)
            matches = match_personality_to_food_nodes(p, FOOD_NODES, 12, top_n=3)
            hex_c = f"#{p_color[0]:02X}{p_color[1]:02X}{p_color[2]:02X}"
            top1 = f"{matches[0][0].name}({matches[0][1]:.2f})" if matches else "-"
            top2 = f"{matches[1][0].name}({matches[1][1]:.2f})" if len(matches) > 1 else "-"
            top3 = f"{matches[2][0].name}({matches[2][1]:.2f})" if len(matches) > 2 else "-"
            f.write(f"| {i} | {p.code} | {p.element} | {p.channel} | `{hex_c}` | {top1} | {top2} | {top3} |\n")

        f.write("\n## 시간대별 먹을거 매핑 (선택 성격)\n\n")
        for sample_code in ['ENFP_M_O', 'ISTP_M_O', 'ENTJ_M_O', 'INFJ_F_A', 'ESFP_M_B']:
            sp = next((p for p in personalities if p.code == sample_code), None)
            if not sp:
                continue
            f.write(f"### {sample_code} ({sp.element})\n\n")
            f.write("| 시간 | 낮/밤 | 성격색 | top-1 | top-2 | top-3 |\n")
            f.write("|---|---|---|---|---|---|\n")
            for h in [2, 8, 12, 18, 22]:
                dn = '낮' if 6 <= h < 18 else '밤'
                p_color = sp.color(h)
                hex_c = f"#{p_color[0]:02X}{p_color[1]:02X}{p_color[2]:02X}"
                matches = match_personality_to_food_nodes(sp, FOOD_NODES, h, top_n=3)
                cells = []
                for n, sim in matches:
                    cells.append(f"{n.name}({sim:.2f})")
                while len(cells) < 3:
                    cells.append("-")
                f.write(f"| {h:02d}h | {dn} | `{hex_c}` | {cells[0]} | {cells[1]} | {cells[2]} |\n")
            f.write("\n")

    print(f"Markdown 저장: {md_file}")


if __name__ == '__main__':
    main()
