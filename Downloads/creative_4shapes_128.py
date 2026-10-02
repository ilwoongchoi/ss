"""
128 성격 × 4 창의적 활동 모양 (Creative Activity Shapes)
기존 _activity_128x6.md와 다르게:
- 6슬롯이 아니라 4개의 창의적 "모양(shape)"을 정확하게 계산
- 8D 임피던스 벡터 + 입자 가중치 + 혈액형/성별 플로우로 결정
- 각 모양은 실제 8D 파라미터 조합에서 나옴 — 멍청하게 반복하지 않음

4 창의적 모양:
  SHAPE_1: STRUCTURE (g/p/nu 지배) — 건축적, 체계적 창작
  SHAPE_2: FLOW (r/h/gamma 지배) — 즉흥적, 유동적 창작  
  SHAPE_3: CONTRAST (d/s 지배) — 대비, 갈등, 파괴적 창작
  SHAPE_4: EMERGENCE (nu/gamma/h 지배) — 복합, 층위, 창발적 창작
"""

import math
import json
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ============================================================
# 1. 8D IMPEDANCE (from _slot_mapping.py)
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
# 2. 4 CREATIVE SHAPES — 8D 파라미터 기반
# ============================================================

# 각 모양은 8D 파라미터의 특정 조합이 지배할 때 발현
# 모양 점수 = 해당 파라미터들의 가중 합
SHAPES = {
    'STRUCTURE': {
        'dims': {'g': 0.35, 'p': 0.30, 'nu': 0.20, 'd': 0.15},
        'desc': '건축적/체계적 — 구조를 세우는 창작',
        'keywords': ['설계', '프레임워크', '조립', '시스템', '아키텍처'],
    },
    'FLOW': {
        'dims': {'r': 0.35, 'h': 0.25, 'gamma': 0.25, 's': 0.15},
        'desc': '즉흥적/유동적 — 흐르는 창작',
        'keywords': ['즉흥', '리듬', '연속', '스윙', '브릿지'],
    },
    'CONTRAST': {
        'dims': {'d': 0.35, 's': 0.30, 'r': 0.20, 'p': 0.15},
        'desc': '대비/갈등 — 충돌에서 나오는 창작',
        'keywords': ['파괴', '대비', '충돌', '엣지', '역동'],
    },
    'EMERGENCE': {
        'dims': {'nu': 0.30, 'gamma': 0.25, 'h': 0.25, 'g': 0.20},
        'desc': '창발/복합 — 층위가 겹쳐 새로운 것이 나오는 창작',
        'keywords': ['층위', '프랙탈', '창발', '중첩', '재귀'],
    },
}

# ============================================================
# 3. ACTIVITY DATABASE — 모양×입자 매핑
# ============================================================

# 각 (shape, dominant_particle) 조합에 대한 구체적 활동
# 입자 = 해당 shape에서 가장 활성화된 입자
ACTIVITIES = {
    'STRUCTURE': {
        'proton':      '기둥/아치 구조 설계 — 물리적 부지킴 창작',
        'gluon':       '모듈러 건축 조립 — 결합력 기반 구조 창작',
        'w_boson':     '게임 룰 시스템 설계 — 상호작용 규칙 창작',
        'photon':      '광학 설치 계획 — 빛 경로 구조 설계',
        'higgs':       '세계관 틀 구축 — 질량 부여 구조 창작',
        'neutrino':    '관통형 구조 — 투명한 층위 설계',
        'tau':         '무거운 기반 구축 — 심층 토대 창작',
        'z_boson':     '양자 게이트 설계 — 붕괴 경로 구조',
        'electron':    '회로 기판 레이아웃 — 전자 경로 설계',
        'muon':        '피라미드 구조 — 중심축 기반 창작',
        'up_quark':    '스캐폴딩 설계 — 상향 지지 구조',
        'down_quark':  '레일 시스템 구축 — 하향 레일 창작',
        'charm_quark': '분자 모델 조립 — 매력적 결합 구조',
        'strange_quark': '비정형 구조 설계 — 기하학적 변형',
        'top_quark':   '캐논 형식 작곡 — 최위계 구조',
        'bottom_quark':'기반 공사 설계 — 하부 구조 창작',
        'neutron':     '중성 프레임 — 관찰자 구조 설계',
        'neutron_star':'밀도 구조 — 압축 형태 창작',
        'dark_matter': '보이지 않는 뼈대 — 암묵적 구조',
        'dark_energy': '팽창 구조 — 확장 시스템 설계',
        'energy':      '에너지 그리드 설계 — 동력 분배 구조',
        'ego_d2':      '자아 구조 — 주체적 프레임 구축',
        'testosterone':'힘 구조 — 강도 기반 설계',
        'progesterone':'회복 구조 — 치유 프레임 설계',
        'acetyl_coa':  '대사 공정 설계 — 변환 라인 구축',
        'graviton':    '중력 구조 — 질량 분배 설계',
        'axion':       '숨겨진 축 — 비가시적 구조 창작',
        'female_gaba': '인비저닝 구조 — 포용적 프레임',
        'clathrate_buffer': '격자 구조 — 클라스레이트 설계',
        'malate_dehydrogenase': 'TCA 회로 설계 — 대사 사이클 구조',
        'tau_neutrino':   '시그마 구조 — 변환 게이트 설계',
        'electron_antineutrino': '역방향 구조 — 반전 프레임',
        'muon_neutrino':  '피로 구조 — 하중 분산 설계',
        'muon_antineutrino': '재귀 구조 — 자기참조 프레임',
        'tau_antineutrino': '붕괴 구조 — 해체 경로 설계',
        'em':            'EM 스펙트럼 설계 — 파동 구조',
    },
    'FLOW': {
        'proton':      '리듬 시퀀스 즉흥 — 박자 창작',
        'gluon':       '접착 플로우 — 붙였다 떼는 즉흥',
        'w_boson':     '상호작용 플로우 — 교류 리듬 창작',
        'photon':      '빛 흐름 — 광선 시퀀스 즉흥',
        'higgs':       '질량 플로우 — 무게감 있는 흐름',
        'neutrino':    '관통 플로우 — 통과하는 리듬',
        'tau':         '무거운 흐름 — 느린 파도 창작',
        'z_boson':     '양자 플로우 — 붕괴 리듬 즉흥',
        'electron':    '전자 플로우 — 점프 시퀀스 창작',
        'muon':        '우주선 플로우 — 고에너지 흐름',
        'up_quark':    '상향 플로우 — 상승 리듬 창작',
        'down_quark':  '하향 플로우 — 하강 리듬 창작',
        'charm_quark': '매력 플로우 — 끌림 리듬 즉흥',
        'strange_quark': '기묘한 흐름 — 비틀린 리듬',
        'top_quark':   '정점 플로우 — 클라이맥스 흐름',
        'bottom_quark':'바닥 플로우 — 그루브 창작',
        'neutron':     '중성 플로우 — 균형 흐름',
        'neutron_star':'압축 플로우 — 밀도 리듬',
        'dark_matter': '암흑 흐름 — 보이지 않는 리듬',
        'dark_energy': '팽창 플로우 — 확장 흐름 창작',
        'energy':      '에너지 플로우 — 동력 리듬 즉흥',
        'ego_d2':      '자아 플로우 — 주체적 흐름',
        'testosterone':'폭발 플로우 — 힘 리듬 창작',
        'progesterone':'회복 플로우 — 치유 흐름',
        'acetyl_coa':  '대사 플로우 — 변환 리듬',
        'graviton':    '중력 플로우 — 끌림 흐름 창작',
        'axion':       '숨겨진 흐름 — 암시적 리듬',
        'female_gaba': '포용 플로우 — 감싸는 흐름',
        'clathrate_buffer': '버퍼 플로우 — 완충 리듬',
        'malate_dehydrogenase': '사이클 플로우 — 회전 흐름',
        'tau_neutrino':   '변환 플로우 — 전환 리듬',
        'electron_antineutrino': '역플로우 — 반전 흐름',
        'muon_neutrino':  '피로 플로우 — 하강 리듬',
        'muon_antineutrino': '재귀 플로우 — 되돌림 흐름',
        'tau_antineutrino': '붕괴 플로우 — 해체 리듬',
        'em':            'EM 플로우 — 파동 흐름 즉흥',
    },
    'CONTRAST': {
        'proton':      '충돌 리듬 — 박자 파괴 창작',
        'gluon':       '결합/분해 대비 — 붙임/떼임 충돌',
        'w_boson':     '교류 충돌 — 상호작용 파괴',
        'photon':      '빛/그림자 대비 — 광학 충돌 창작',
        'higgs':       '질량/무질량 대비 — 무게 충돌',
        'neutrino':    '관통/차단 대비 — 투과 충돌',
        'tau':         '무거움/가벼움 — 질량 대비 창작',
        'z_boson':     '양자 붕괴 대비 — 상태 충돌',
        'electron':    '점프/정지 대비 — 전자 충돌',
        'muon':        '고에너지/피로 대비 — 우주선 충돌',
        'up_quark':    '상승/하강 대비 — 방향 충돌',
        'down_quark':  '레일/이탈 대비 — 궤도 충돌',
        'charm_quark': '끌림/밀침 대비 — 매력 충돌',
        'strange_quark': '정상/기묘 대비 — 변형 충돌',
        'top_quark':   '정점/바닥 대비 — 극단 충돌',
        'bottom_quark':'바닥/정상 대비 — 역전 충돌',
        'neutron':     '중성/편향 대비 — 균형 충돌',
        'neutron_star':'압축/팽창 대비 — 밀도 충돌',
        'dark_matter': '보임/숨김 대비 — 암흑 충돌',
        'dark_energy': '수축/팽창 대비 — 우주 충돌',
        'energy':      '폭발/정지 대비 — 동력 충돌',
        'ego_d2':      '자아/비자아 대비 — 주체 충돌',
        'testosterone':'공격/방어 대비 — 힘 충돌',
        'progesterone':'회복/파괴 대비 — 치유 충돌',
        'acetyl_coa':  '합성/분해 대비 — 대사 충돌',
        'graviton':    '중력/반중력 대비 — 끌림 충돌',
        'axion':       '가시/비가시 대비 — 숨김 충돌',
        'female_gaba': '억제/흥분 대비 — GABA 충돌',
        'clathrate_buffer': '봉쇄/개방 대비 — 격자 충돌',
        'malate_dehydrogenase': '산화/환원 대비 — TCA 충돌',
        'tau_neutrino':   '변환/유지 대비 — 전환 충돌',
        'electron_antineutrino': '정방향/역방향 대비 — 반전 충돌',
        'muon_neutrino':  '활성/피로 대비 — 하중 충돌',
        'muon_antineutrino': '전진/후퇴 대비 — 재귀 충돌',
        'tau_antineutrino': '생성/붕괴 대비 — 해체 충돌',
        'em':            '간섭/소멸 대비 — 파동 충돌',
    },
    'EMERGENCE': {
        'proton':      '프랙탈 리듬 — 중첩 박자 창작',
        'gluon':       '결합 창발 — 다중 결합 층위',
        'w_boson':     '교환 창발 — 다차원 상호작용',
        'photon':      '광학 창발 — 간섭 패턴 창작',
        'higgs':       '질량 창발 — 다층 질량 부여',
        'neutrino':    '관통 창발 — 다차원 투과',
        'tau':         '무거움 창발 — 심층 파도',
        'z_boson':     '양자 창발 — 다상태 중첩',
        'electron':    '전자 창발 — 다층 궤도 창작',
        'muon':        '우주선 창발 — 다단계 피로',
        'up_quark':    '상승 창발 — 다층 상승',
        'down_quark':  '레일 창발 — 다중 궤도',
        'charm_quark': '매력 창발 — 다차원 끌림',
        'strange_quark': '기묘함 창발 — 비선형 변형',
        'top_quark':   '정점 창발 — 다단 클라이맥스',
        'bottom_quark':'바닥 창발 — 다층 그루브',
        'neutron':     '중성 창발 — 다차원 균형',
        'neutron_star':'밀도 창발 — 다단 압축',
        'dark_matter': '암흑 창발 — 보이지 않는 층위',
        'dark_energy': '팽창 창발 — 다단 확장',
        'energy':      '에너지 창발 — 다층 동력',
        'ego_d2':      '자아 창발 — 다차원 주체',
        'testosterone':'힘 창발 — 다단 폭발',
        'progesterone':'회복 창발 — 다층 치유',
        'acetyl_coa':  '대사 창발 — 다단 변환',
        'graviton':    '중력 창발 — 다차원 끌림',
        'axion':       '숨겨진 창발 — 다층 암시',
        'female_gaba': '포용 창발 — 다차원 감쌈',
        'clathrate_buffer': '봉쇄 창발 — 다층 격자',
        'malate_dehydrogenase': 'TCA 창발 — 다단 회전',
        'tau_neutrino':   '변환 창발 — 다차원 전환',
        'electron_antineutrino': '역창발 — 다층 반전',
        'muon_neutrino':  '피로 창발 — 다단 하중',
        'muon_antineutrino': '재귀 창발 — 다층 되돌림',
        'tau_antineutrino': '붕괴 창발 — 다단 해체',
        'em':            'EM 창발 — 다차원 파동',
    },
}

# ============================================================
# 4. PARTICLE WEIGHTS (from _slot_mapping.py)
# ============================================================

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

# ============================================================
# 5. 128 PERSONALITIES
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
# 6. COMPUTE 4 SHAPES PER PERSONALITY
# ============================================================

def compute_8d_vector(m, b, g):
    """Compute the 8D impedance vector for a personality."""
    vec = impedance_vector(m)
    fv = flow(g)
    ew = BLOOD_WEIGHT[b]
    for k in vec:
        vec[k] *= ew
    for k in vec:
        vec[k] *= fv[k]
    return vec

def compute_shape_scores(vec):
    """Compute 4 shape scores from 8D vector."""
    scores = {}
    for shape_name, shape_def in SHAPES.items():
        score = sum(vec[dim] * w for dim, w in shape_def['dims'].items())
        scores[shape_name] = round(score, 3)
    return scores

def compute_particle_values(vec):
    """Compute particle activation values."""
    results = {}
    for particle, weights in PARTICLE_WEIGHTS.items():
        value = sum(vec[dim] * w for dim, w in weights.items())
        results[particle] = round(value, 3)
    return results

def get_top_particle(particle_values, shape_name, vec):
    """Get the most relevant particle for a given shape."""
    shape_dims = SHAPES[shape_name]['dims']
    # Score each particle by how well it aligns with this shape's dominant dims
    # AND its overall activation
    best_particle = None
    best_score = -1
    for particle, weights in PARTICLE_WEIGHTS.items():
        # How much this particle's weights overlap with shape dims
        shape_alignment = sum(w * shape_dims.get(dim, 0) for dim, w in weights.items())
        activation = particle_values[particle]
        combined = shape_alignment * activation
        if combined > best_score:
            best_score = combined
            best_particle = particle
    return best_particle, round(best_score, 3)

def get_activity(shape_name, particle):
    """Get the specific activity for a shape+particle combination."""
    activities = ACTIVITIES.get(shape_name, {})
    return activities.get(particle, f'{particle} 기반 {SHAPES[shape_name]["desc"]}')

# ============================================================
# 7. GENERATE MAPPING
# ============================================================

def generate_mapping():
    results = []
    for num, sym, m, b, g in PERSONALITIES:
        mbti = MBTI_NAMES[m]
        blood = BLOOD_NAMES[b]
        gender = 'M' if g == 0 else 'F'
        profile = f"{mbti}_{gender}_{blood}"
        
        vec = compute_8d_vector(m, b, g)
        shape_scores = compute_shape_scores(vec)
        particle_values = compute_particle_values(vec)
        
        # Sort shapes by score descending
        sorted_shapes = sorted(shape_scores.items(), key=lambda x: -x[1])
        
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
            particle, p_score = get_top_particle(particle_values, shape_name, vec)
            activity = get_activity(shape_name, particle)
            entry['shapes'][shape_name] = {
                'score': score,
                'dominant_particle': particle,
                'particle_score': p_score,
                'activity': activity,
                'desc': SHAPES[shape_name]['desc'],
            }
        
        results.append(entry)
    return results

# ============================================================
# 8. OUTPUT
# ============================================================

def main():
    mapping = generate_mapping()
    
    print("=" * 80)
    print("128 성격 × 4 창의적 활동 모양 (Creative Activity Shapes)")
    print("8D 임피던스 + 입자 가중치 + 혈액형/성별 플로우 기반")
    print("=" * 80)
    
    # 예시 출력
    for entry in mapping[:5]:
        print(f"\n{'='*60}")
        print(f"{entry['num']}. {entry['element']} ({entry['profile']})")
        print(f"8D: {entry['vector']}")
        print(f"{'='*60}")
        for shape_name, data in entry['shapes'].items():
            print(f"  [{shape_name:12s}] score={data['score']:.3f} | "
                  f"particle={data['dominant_particle']:20s} | "
                  f"{data['activity']}")
    
    # JSON 저장
    json_file = "c:/Users/User/Downloads/creative_4shapes_128.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"\nJSON 저장: {json_file}")
    
    # Markdown 저장
    md_file = "c:/Users/User/Downloads/creative_4shapes_128.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 128 성격 × 4 창의적 활동 모양\n\n")
        f.write("8D 임피던스 벡터 + 입자 가중치 + 혈액형/성별 플로우로 계산.\n\n")
        f.write("## 4 모양 정의\n\n")
        f.write("| 모양 | 지배 8D | 설명 |\n|---|---|---|\n")
        for name, defn in SHAPES.items():
            dims_str = ', '.join(f"{k}({v})" for k, v in defn['dims'].items())
            f.write(f"| {name} | {dims_str} | {defn['desc']} |\n")
        
        f.write("\n## 128 성격별 4 창의적 모양\n\n")
        f.write("| # | 원소 | 성격 | SHAPE_1 (최강) | SHAPE_2 | SHAPE_3 | SHAPE_4 (최약) |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        
        for entry in mapping:
            shapes = list(entry['shapes'].items())
            cells = []
            for shape_name, data in shapes:
                cells.append(f"**{shape_name}** ({data['score']:.2f}) {data['dominant_particle']} → {data['activity']}")
            while len(cells) < 4:
                cells.append("-")
            f.write(f"| {entry['num']} | {entry['element']} | {entry['profile']} | {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} |\n")
        
        f.write("\n## 상세: 8D 벡터 + 모양 점수\n\n")
        for entry in mapping:
            f.write(f"### {entry['num']}. {entry['element']} ({entry['profile']})\n\n")
            f.write(f"- **8D 벡터**: {entry['vector']}\n")
            for shape_name, data in entry['shapes'].items():
                f.write(f"- **{shape_name}** (score={data['score']:.3f}): "
                        f"particle={data['dominant_particle']} (p_score={data['particle_score']:.3f}) "
                        f"→ {data['activity']}\n")
            f.write("\n")
    
    print(f"Markdown 저장: {md_file}")
    
    # 통계
    print(f"\n총 {len(mapping)} 성격 × 4 모양 = {len(mapping)*4} 창의적 활동")
    
    # 모양별 빈도
    shape_count = {}
    for entry in mapping:
        for shape_name in entry['shapes']:
            shape_count[shape_name] = shape_count.get(shape_name, 0) + 1
    print("\n모양별 빈도 (1순위):")
    for shape_name in SHAPES:
        count = sum(1 for e in mapping if list(e['shapes'].keys())[0] == shape_name)
        print(f"  {shape_name:12s} : {count}개")


if __name__ == '__main__':
    main()
