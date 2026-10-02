"""
Color Mapping Engine — 128 Personalities × Body Nodes × Time Slots
색깔 가산 논리로 성격-노드-시간대 매핑을 자동 계산

Node colors are assigned based on ACTUAL chemical/biochemical properties,
NOT element group mappings. Each node's color reflects the real-world color
of its underlying molecule, compound, or biological process.

4-Channel Blood Type → Particle → Color mapping (corrected):
  BW (AB) gluon:    day GREEN,  night YELLOW
  BM (O)  photon:   day YELLOW, night RED
  SW (A)  quark:    day BLUE,   night GREEN
  SM (B)  neutrino: day RED,    night BLUE

Personality color = base_channel_color (day/night) + MBTI_middle (NF/ST/SF/NT) + MBTI_end (EP/EJ/IJ/IP)
Node color = actual chemical/biochemical color of the node's function
Match = RGB distance between personality color and node color.

Sources:
  - CIRCUITFILE.MD  (node definitions, biochemical functions, circuit wiring)
  - prose.txt        (8D receptor map, day/night cycle logic, node roles)
"""

import itertools
import json
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


# ============================================================
# 1. BASE COLOR SYSTEM (RGB)
# ============================================================

# Primary colors as RGB tuples
RGB = {
    'RED':          (255,   0,   0),
    'GREEN':        (  0, 255,   0),
    'BLUE':         (  0,   0, 255),
    'YELLOW':       (255, 255,   0),
    'WHITE':        (255, 255, 255),
    'BLACK':        (  0,   0,   0),
    'CYAN':         (  0, 255, 255),
    'MAGENTA':      (255,   0, 255),
    'ORANGE':       (255, 165,   0),
    'RED-ORANGE':   (255,  69,   0),
    'BROWN':        (139,  69,  19),
    'DARK-BROWN':   (101,  67,  33),
    'DARK-GREEN':   (  0, 100,   0),
    'PALE-GREEN':   (152, 251, 152),
    'RED-BROWN':    (165,  42,  42),
    'YELLOW-ORANGE':(255, 200,   0),
    'BLUE-WHITE':   (224, 255, 255),
    'PALE-YELLOW':  (255, 255, 200),
    'DARK-VIOLET':  ( 48,   0,  80),
    'PURPLE':       (128,   0, 128),
    'RED-PURPLE':   (160,  32, 100),
    'PINK':         (255, 192, 203),
    'PALE-PINK':    (255, 218, 224),
    'GRAY':         (128, 128, 128),
    'DARK-GRAY':    ( 64,  64,  64),
    'SAND-YELLOW':  (238, 214, 122),
    'BLUE-GREY':    (106, 123, 155),
    'LILAC':        (200, 162, 200),
    'CRIMSON':      (220,  20,  60),
    'MAROON':       (128,   0,   0),
}


# ============================================================
# 2. 4-CHANNEL DAY/NIGHT COLOR LOGIC
# ============================================================

# Blood type → channel → particle → day/night colors
# BW = Blood type AB, Woman (gluon)
# BM = Blood type O, Man (photon)  
# SW = Blood type A, Woman (quark)
# SM = Blood type B, Man (neutrino)
CHANNEL_COLORS = {
    'BW': {  # AB, gluon
        'particle': 'gluon',
        'day':   RGB['GREEN'],
        'night': RGB['YELLOW'],
    },
    'BM': {  # O, photon
        'particle': 'photon',
        'day':   RGB['YELLOW'],
        'night': RGB['RED'],
    },
    'SW': {  # A, quark
        'particle': 'quark',
        'day':   RGB['BLUE'],
        'night': RGB['GREEN'],
    },
    'SM': {  # B, neutrino
        'particle': 'neutrino',
        'day':   RGB['RED'],
        'night': RGB['BLUE'],
    },
}

# Blood type → channel mapping
# AB → BW, O → BM, A → SW, B → SM
BLOOD_TYPE_CHANNEL = {
    'AB': 'BW',
    'O':  'BM',
    'A':  'SW',
    'B':  'SM',
}


# ============================================================
# 3. MBTI COLOR ADDITIONS
# ============================================================

# MBTI middle letters (function pair) → color addition (RGB delta)
# These are ADDED to the base channel color
MBTI_MIDDLE = {
    'NF': ( 20,   0,  20),   # violet shift — intuitive feeling
    'ST': ( 20,  20,   0),   # yellow shift — sensing thinking
    'SF': (  0,  20,   0),   # green shift — sensing feeling
    'NT': (  0,   0,  20),   # blue shift — intuitive thinking
}

# MBTI end letters (attitude) → color addition (RGB delta)
MBTI_END = {
    'EP': ( 15,  15,   0),   # extraverted perceiving — bright/warm
    'EJ': ( 15,   0,   0),   # extraverted judging — red/active
    'IJ': (  0,   0,  15),   # introverted judging — blue/structured
    'IP': (  0,  15,   0),   # introverted perceiving — green/receptive
}


# ============================================================
# 4. TIME SLOTS (Toroidal cycle)
# ============================================================

# Toroidal time slots: AB(0-3h), A(3-9h), O(9-15h), B(15-21h), AB(21-3h)
# Energy flows reverse: AB ← B ← O ← A ← AB
TIME_SLOTS = [
    {'hours': '0-3',   'blood': 'AB', 'phase': 'discharge',   'genre': 'release'},
    {'hours': '3-9',   'blood': 'A',  'phase': 'accumulate',  'genre': 'stress'},
    {'hours': '9-15',  'blood': 'O',  'phase': 'coulomb',     'genre': 'ambient'},
    {'hours': '15-21', 'blood': 'B',  'phase': 'compress',    'genre': 'extreme'},
    {'hours': '21-3',  'blood': 'AB', 'phase': 'integrate',   'genre': 'cinematic'},
]

# Day = 6:00-18:00, Night = 18:00-6:00
def is_daytime(hour: int) -> bool:
    return 6 <= hour < 18


# ============================================================
# 5. PERSONALITY COLOR CALCULATION
# ============================================================

@dataclass
class Personality:
    mbti: str           # e.g. "ENFP"
    gender: str         # "M" or "F"
    blood_type: str     # "O", "A", "B", "AB"
    element: str = ""   # associated element (e.g. "H(1)")
    
    @property
    def code(self) -> str:
        return f"{self.mbti}_{self.gender}_{self.blood_type}"
    
    @property
    def channel(self) -> str:
        return BLOOD_TYPE_CHANNEL[self.blood_type]
    
    @property
    def middle(self) -> str:
        return self.mbti[1:3]  # NF, ST, SF, NT
    
    @property
    def end(self) -> str:
        return self.mbti[2:4]  # EP, EJ, IJ, IP (last 2 chars)
    
    def base_color(self, hour: int) -> Tuple[int, int, int]:
        """Base channel color depends on day/night cycle."""
        ch = CHANNEL_COLORS[self.channel]
        return ch['day'] if is_daytime(hour) else ch['night']
    
    def color(self, hour: int = 12) -> Tuple[int, int, int]:
        """Full personality color = base + MBTI middle + MBTI end."""
        base = self.base_color(hour)
        mid = MBTI_MIDDLE.get(self.middle, (0, 0, 0))
        end = MBTI_END.get(self.end, (0, 0, 0))
        r = max(0, min(255, base[0] + mid[0] + end[0]))
        g = max(0, min(255, base[1] + mid[1] + end[1]))
        b = max(0, min(255, base[2] + mid[2] + end[2]))
        return (r, g, b)


# ============================================================
# 6. BODY NODES — ACTUAL CHEMICAL/BIOCHEMICAL COLORS
# ============================================================

@dataclass
class BodyNode:
    name: str               # circuit node name
    function: str           # biochemical function description
    location: str           # anatomical location
    color_name: str         # color name
    color_rgb: Tuple[int, int, int]  # RGB
    element: str = ""       # associated element if any
    particle: str = ""      # associated particle if any


# Node colors based on ACTUAL chemical/biochemical properties
# NOT element group mappings — real-world colors of the molecules/processes
NODES: List[BodyNode] = [
    # --- Heme / Iron nodes ---
    BodyNode('heme', 'Heme (Fe2+ porphyrin) — proton creation, O2 binding',
             'left nipple inner', 'RED', RGB['RED'],
             element='H(1)', particle='proton'),
    BodyNode('hemoglobin', 'Hemoglobin tetramer — O2-Fe2+ redox, Fe2+→Fe3+ charge transfer',
             'right nipple inner', 'RED-BROWN', RGB['RED-BROWN'],
             particle='proton_to_photon'),
    BodyNode('ferritin', 'Ferritin iron storage protein — Fe3+ oxyhydroxide core',
             'left upper abdomen', 'DARK-BROWN', RGB['DARK-BROWN'],
             element='Fe(26)', particle='muon_neutrino'),
    BodyNode('laterite', 'Iron sequestration D-latch — Fe3+ tropical duricrust',
             'left lateral thigh', 'RED-BROWN', RGB['RED-BROWN'],
             particle='right_testosterone'),
    BodyNode('steel', 'Structural iron oxidation — Fe2+/Fe3+ martensite/austenite',
             'right thumb toe', 'GRAY', RGB['GRAY'],
             element='Fe(26)', particle='muon_neutrino'),

    # --- Mitochondrial / ETC nodes ---
    BodyNode('cytochrome_c_oxidase', 'COX Complex IV — heme a/a3 + Cu centers, red-purple absorption',
             'left occipitalis inner top', 'RED-PURPLE', RGB['RED-PURPLE'],
             element='Be(4)', particle='z_boson'),
    BodyNode('succinate_dehydrogenase', 'SDH Complex II — FAD + Fe-S clusters, succinate→fumarate',
             'right axillary tendon', 'ORANGE', RGB['ORANGE'],
             element='Br(35)/Kr(36)', particle='muon_neutrino/photon'),
    BodyNode('lower_mantle', 'Mitochondrial matrix PMF — proton motive force, ΔΨm',
             'center torso', 'CYAN', RGB['CYAN'],
             element='W(74)/Re(75)', particle='muon'),
    BodyNode('outer_core_convection', 'PMF convection — proton pumping, ETC',
             'center torso deep', 'CYAN', RGB['CYAN'],
             particle='tau_neutrino'),
    BodyNode('plume', 'Ca2+ spark / mantle plume — mitochondrial calcium upwelling',
             'right lateral hip', 'WHITE', RGB['WHITE'],
             element='Pt(78)', particle='graviton'),

    # --- Krebs / TCA cycle ---
    BodyNode('citric_acid_cycle', 'TCA cycle — citrate (colorless), isocitrate, α-KG',
             'center abdomen', 'PALE-YELLOW', RGB['PALE-YELLOW'],
             particle='TCA'),
    BodyNode('methanogenesis', 'Methanogenesis — CH4 production, archaea, colorless gas',
             'gut / right 1st metatarsal', 'PALE-GREEN', RGB['PALE-GREEN'],
             element='Tb(65)/Dy(66)', particle='gluon'),
    BodyNode('nitrogenase_iron', 'Nitrogenase FeMo-co — N2 fixation, Fe-S + Mo',
             'left lateral thigh', 'DARK-BROWN', RGB['DARK-BROWN'],
             particle='electron_antineutrino'),

    # --- Pigment / Melanin nodes ---
    BodyNode('mc1r', 'MC1R — melanocortin receptor, eumelanin/pheomelanin switch',
             'skin / hair follicles', 'BROWN', RGB['BROWN'],
             element='Si(14)/Zn(30)', particle='graviton'),
    BodyNode('mycorradicin', 'AM symbiosis — C14 carotenoid glycoside, yellow root exudate',
             'right foot / Achilles', 'YELLOW', RGB['YELLOW'],
             particle='down_quark'),

    # --- Antioxidant / Detox nodes ---
    BodyNode('sulforaphane', 'Sulforaphane — isothiocyanate from cruciferous, Nrf2/ARE',
             'left hippocampus tail', 'DARK-GREEN', RGB['DARK-GREEN'],
             element='Ar(18)', particle='gluon'),
    BodyNode('pentose_phosphate', 'PPP — NADPH production, GSH recycling',
             'left lateral torso', 'PALE-YELLOW', RGB['PALE-YELLOW'],
             particle='neutron_star'),
    BodyNode('peonidine', 'Peonidine — anthocyanin, red/blue pH-dependent pigment',
             'left lateral thigh deep', 'RED-PURPLE', RGB['RED-PURPLE'],
             element='Sb(51)/Sn(50)', particle='energy/muon_antineutrino'),

    # --- Neurotransmitter nodes ---
    BodyNode('male_right_oxytocin', 'OXTR oxytocin — social bonding, Gq/11',
             'right temporalis / rSMG', 'PALE-PINK', RGB['PALE-PINK'],
             element='Pr(59)/Nd(60)', particle='up_quark/down_quark'),
    BodyNode('drd2_mpoa', 'D2/D3 MPOA — climax brake, Gi/o, reward threshold',
             'left genitalia projection', 'GRAY', RGB['GRAY'],
             element='Na(11)', particle='strange_quark'),
    BodyNode('drd2s_presynaptic', 'D2S autoreceptor — tonic DA, cAMP/PKA master bus',
             'outer left frontalis', 'GRAY', RGB['GRAY'],
             element='Na(11)', particle='strange_quark'),
    BodyNode('drd1_peripheral', 'D1/D5 peripheral — Gs, cAMP, motor drive',
             'center of right sole', 'RED', RGB['RED'],
             element='Pm(61)/Sm(62)', particle='down_quark'),
    BodyNode('right_sole_dopamine', 'D1/D5 right sole — somatic motor dopamine',
             'center of right sole', 'RED', RGB['RED'],
             element='Pm(61)/Sm(62)', particle='down_quark/muon'),
    BodyNode('right_d2', 'DRD2 postsynaptic indirect — Gi/o, NoGo pathway',
             'left frontalis outer strip', 'BLUE', RGB['BLUE'],
             element='E122', particle='dopamine'),
    BodyNode('right_cortisol', 'GR/NR3C1 — glucocorticoid nuclear receptor',
             'right posterior', 'YELLOW', RGB['YELLOW'],
             element='E123', particle='cortisol'),
    BodyNode('female_right_satisfaction', 'μ-opioid MOR — OPRM1 satisfaction, Gi',
             'left philtrum center', 'WHITE', RGB['WHITE'],
             element='E124', particle='satisfaction'),
    BodyNode('left_female_vasopressin', 'V1B vasopressin — stress arousal, Gq/11',
             'pituitary / left', 'RED', RGB['RED'],
             element='E125', particle='vasopressin'),
    BodyNode('male_gaba_a', 'GABA-A δ extrasynaptic — tonic inhibition, Cl- channel',
             'global / brainstem', 'PALE-GREEN', RGB['PALE-GREEN'],
             element='Al(13)', particle='GABA-A'),
    BodyNode('female_gaba_b', 'GABA-B postsynaptic — slow IPSP, GIRK K+',
             'left lat dorsi bottom', 'BLUE', RGB['BLUE'],
             element='E127', particle='GABA-B_2'),
    BodyNode('female_gaba_b_2', 'GABA-B secondary — hypoxic state confirmation',
             'left lat dorsi', 'BLUE', RGB['BLUE'],
             element='E127', particle='GABA-B_2'),
    BodyNode('5ht1a', '5-HT1A — Gi presynaptic autoreceptor, anti-anxiety',
             'left temporal region', 'GREEN', RGB['GREEN'],
             element='Ga(31)', particle='serotonin_1a'),
    BodyNode('5ht1b', '5-HT1B — Gi terminal autoreceptor, serotonin release control',
             'left temporal / hippocampus', 'WHITE', RGB['WHITE'],
             element='Rh(45)', particle='serotonin_1b'),
    BodyNode('right_acetylcholine', 'α7 nAChR — vagal cholinergic, Ca2+ permeable',
             'right temporalis', 'GREEN', RGB['GREEN'],
             element='Es(99)', particle='tau_neutrino'),
    BodyNode('male_left_noradrenaline', 'α2A-AR — noradrenergic, presynaptic autoreceptor',
             'left cervical', 'RED', RGB['RED'],
             element='E121', particle='noradrenaline'),
    BodyNode('choline', 'CHT1 choline transporter — ACh precursor synthesis',
             'left cervical', 'WHITE', RGB['WHITE'],
             element='E120', particle='precursor'),
    BodyNode('mor_presynaptic', 'MOR presynaptic — β-endorphin global analgesia',
             'left levator superioris', 'GREEN', RGB['GREEN'],
             element='Mg(12)', particle='electron_antineutrino'),
    BodyNode('mor_postsynaptic', 'MOR postsynaptic — reward spark, Mg2+',
             'left philtrum', 'GREEN', RGB['GREEN'],
             element='Mg(12)', particle='electron_antineutrino'),

    # --- Metabolic / Digestive nodes ---
    BodyNode('glp1', 'GLP-1 incretin — vagal satiety, D-flip-flop',
             'upper abdomen center', 'WHITE', RGB['WHITE'],
             element='Tb(65)/Dy(66)', particle='gluon'),
    BodyNode('cck', 'CCK cholecystokinin — postprandial satiety, MUX',
             'pancreas posterior', 'RED', RGB['RED'],
             element='Cf(98)', particle='w_boson'),
    BodyNode('NaCl', 'NaCl action potential — ionic reset, evaporite',
             'left ankle / right', 'WHITE', RGB['WHITE'],
             element='Pu(94)/Am(95)', particle='spark'),
    BodyNode('co2', 'CO2 / dark_energy — respiratory, time storage',
             'center / global', 'BLACK', RGB['BLACK'],
             element='Th(90)/Pa(91)', particle='dark_energy'),
    BodyNode('water', 'Water MUX — H2O, proton source, hydrological',
             'center torso', 'BLUE-WHITE', RGB['BLUE-WHITE'],
             element='Po(84)', particle='right_testosterone'),
    BodyNode('water_vapour', 'Water vapour — surface hydration, ECF osmosis',
             'skin surface', 'PALE-GREEN', RGB['PALE-GREEN'],
             particle='photon'),
    BodyNode('carbon', 'Carbon metabolic latch — anabolic/catabolic',
             'center abdomen', 'GRAY', RGB['GRAY'],
             element='C(6)', particle='photon'),
    BodyNode('carbonic_anhydrase', 'CA — CO2+H2O⇌HCO3-+H+, proton reflection',
             'blood / RBC', 'YELLOW', RGB['YELLOW'],
             particle='right_testosterone'),

    # --- Mineral / Structural nodes ---
    BodyNode('magnetite', 'Fe3O4 magnetite — intracellular magnetic sensor, MUX',
             'center torso', 'BLACK', RGB['BLACK'],
             element='Zn(30)', particle='gluon'),
    BodyNode('pyrite', 'FeS2 pyrite — Fe-S cluster, semiconductor, mineral buffer',
             'right 1st metatarsal', 'DARK-GRAY', RGB['DARK-GRAY'],
             element='Ni(28)/Cu(29)', particle='ego'),
    BodyNode('sulfur_iron_complex', 'Fe-S cluster — iron-sulfur, electron transfer',
             'right axillary tendon', 'DARK-BROWN', RGB['DARK-BROWN'],
             element='Fe(26)', particle='ego'),
    BodyNode('collagen', 'Collagen — triple helix, ECM structural protein',
             'connective tissue global', 'WHITE', RGB['WHITE'],
             element='Sr(38)', particle='tau'),
    BodyNode('actomyosin', 'Actomyosin — actin-myosin cross-bridge, ATP tension',
             'right thumb toe', 'PALE-PINK', RGB['PALE-PINK'],
             element='Ho(67)/Er(68)', particle='dark_energy'),
    BodyNode('caco3', 'CaCO3 carbonate buffer — pH homeostasis',
             'blood / bone', 'WHITE', RGB['WHITE'],
             element='Ac(89)/Th(90)', particle='dark_energy'),
    BodyNode('craton', 'Nuclear lamin scaffold — nuclear membrane stability',
             'right posterior pelvis', 'WHITE', RGB['WHITE'],
             element='Cd(48)/Hf(72)', particle='neutron'),
    BodyNode('basin', 'Foreland basin — metabolite sink, gravitational',
             'center lower torso', 'DARK-GRAY', RGB['DARK-GRAY'],
             particle='energy'),

    # --- Geological / Deep nodes ---
    BodyNode('large_igneous_province', 'LIP — ferroptotic ROS burst, iron-dependent death',
             'mid-thoracic spine', 'RED', RGB['RED'],
             element='Au(79)', particle='photon'),
    BodyNode('subduction_zone', 'Mitophagy — organelle recycling, lysosomal',
             'left lateral thigh', 'DARK-BROWN', RGB['DARK-BROWN'],
             element='Os(76)/Ir(77)', particle='Observer'),
    BodyNode('fold_belt', 'Fold belt — orogenic stress, structural compression',
             'right lateral torso', 'GRAY', RGB['GRAY'],
             particle='graviton'),
    BodyNode('gluon_orogen', 'Stress fiber — cytoskeletal, color confinement',
             'left inner bum', 'WHITE', RGB['WHITE'],
             element='Ar(18)', particle='gluon'),

    # --- Soil / Weathering nodes (metabolic analogs) ---
    BodyNode('cambisol', 'Cambisol — mature humus, autophagic vacuole',
             'right foot / Achilles', 'DARK-BROWN', RGB['DARK-BROWN'],
             element='U(92)/Np(93)', particle='dark_matter'),
    BodyNode('podzol', 'Podzol — acidic spodic horizon, lysosomal pH',
             'left foot', 'PALE-YELLOW', RGB['PALE-YELLOW'],
             element='Y(39)/Zr(40)', particle='neutron_star'),
    BodyNode('histosol', 'Histosol — organic peat, CO2/osmotic',
             'left lat dorsi', 'DARK-BROWN', RGB['DARK-BROWN'],
             element='S(16)', particle='muon_antineutrino'),
    BodyNode('andosol', 'Andosol — volcanic ash, amorphous',
             'left foot', 'BLACK', RGB['BLACK'],
             element='Nh(113)', particle='neutron'),
    BodyNode('gleysol', 'Gleysol — waterlogged, Fe2+ reduction, anaerobic',
             'left lateral malleolus', 'BLUE-GRAY', RGB['BLUE-GREY'],
             particle='neutron'),

    # --- Special nodes ---
    BodyNode('methylation', 'SAM-SAH cycle — DNA methylation, epigenetic',
             'left upper abdomen', 'PALE-GREEN', RGB['PALE-GREEN'],
             element='Yb(70)/Lu(71)', particle='charm_quark'),
    BodyNode('memory_entropy', 'Hippocampal novelty — CA1 mismatch, Shannon entropy',
             'left hippocampus', 'PALE-GREEN', RGB['PALE-GREEN'],
             element='Ca(20)', particle='electron'),
    BodyNode('hind_insula', 'Hind insula — interoceptive, posterior granular',
             'right posterior insula', 'WHITE', RGB['WHITE'],
             element='Sc(21)', particle='neutron'),
    BodyNode('adapter_protein', 'Signal transduction adapter — Grb2/SOS/Shc',
             'right cervical', 'YELLOW', RGB['YELLOW'],
             element='As(33)/Se(34)', particle='gluon'),
    BodyNode('thorium', 'Thorium — REE catalyst, nucleotide backbone',
             'center deep', 'BLACK', RGB['BLACK'],
             element='Th(90)', particle='dark_energy'),
    BodyNode('monazite', 'Monazite — REE phosphate, nucleotide routing',
             'center deep', 'YELLOW', RGB['YELLOW'],
             particle='photon'),
    BodyNode('manganese_oxygen_complex', 'Mn-OEC — Mn4CaO5, water-splitting, Kok cycle',
             'right temporal', 'DARK-VIOLET', RGB['DARK-VIOLET'],
             element='Mn(25)', particle='muon_neutrino'),
    BodyNode('oxidised_manganese', 'Mn(III)/Mn(IV) — oxidized manganese redox',
             'right temporal', 'DARK-VIOLET', RGB['DARK-VIOLET'],
             element='Tc(43)/Ru(44)', particle='unprotonic_spark'),
    BodyNode('pi_electron_cloud', 'Pi-electron — porphyrin/quinone, quantum tunneling',
             'anterior throat', 'PURPLE', RGB['PURPLE'],
             particle='up_quark'),
    BodyNode('hemoglobin', 'Hemoglobin — O2-Fe2+ redox hub',
             'right nipple inner', 'RED', RGB['RED'],
             particle='proton_to_photon'),
    BodyNode('iodine', 'Iodine-thyroid — T3/T4, photon-to-Higgs',
             'right posterior throat', 'BROWN', RGB['BROWN'],
             particle='photon_to_higgs'),
    BodyNode('axion_em_conversion', 'Axion→EM — body as transducer, piezoelectric',
             'entire body / vertex', 'WHITE', RGB['WHITE'],
             particle='axion'),
    BodyNode('electric_grid', 'Bio-electric grid — TEP, galvanotactic',
             'global', 'CYAN', RGB['CYAN'],
             particle='photon'),
    BodyNode('aurora', 'Aurora — EM field excitation, Na+ threshold',
             'skull / global', 'BLUE-WHITE', RGB['BLUE-WHITE'],
             element='Rb(37)', particle='muon'),
    BodyNode('sodium', 'Sodium osmotic — Na+ gradient, NaK-ATPase',
             'global / renal', 'YELLOW', RGB['YELLOW'],
             element='Na(11)', particle='w_boson'),
    BodyNode('chlorine_ion_pump', 'Cl- pump — chloride channel, GABA-A coupled',
             'global / neuronal', 'PALE-GREEN', RGB['PALE-GREEN'],
             element='Cl(17)', particle='electron'),
    BodyNode('heath_aerenchyma', 'Aerenchyma — O2 supply, plant tissue analog',
             'right foot', 'PALE-GREEN', RGB['PALE-GREEN'],
             particle='electron_neutrino'),
    BodyNode('nitrogenase', 'Nitrogenase — N2+8H+→2NH3, FeMo-co',
             'left lateral thigh', 'DARK-BROWN', RGB['DARK-BROWN'],
             particle='electron_antineutrino'),
    BodyNode('lactate_dehydrogenase', 'LDH — pyruvate↔lactate, anaerobic/aerobic',
             'muscle / heart', 'PALE-YELLOW', RGB['PALE-YELLOW'],
             particle='right_testosterone'),
    BodyNode('substance_p', 'Substance P — NK1 receptor, pain/inflammation',
             'left lateral thigh', 'RED', RGB['RED'],
             element='Ra(88)/Zn(30)', particle='tau_antineutrino'),
    BodyNode('autophagy', 'Autophagy — ULK1/Beclin-1/LC3-II, mTOR',
             'global', 'DARK-GRAY', RGB['DARK-GRAY'],
             particle='electron'),
    BodyNode('esr1_expression', 'ESR1 — estrogen receptor α, genomic',
             'right temporalis / frontalis', 'PINK', RGB['PINK'],
             particle='estrogen'),
    BodyNode('right_genital_male_vasopressin', 'V1B right genital — stress-reward sexual',
             'right genital', 'RED', RGB['RED'],
             element='Rh(45)', particle='vasopressin'),
    BodyNode('postsynaptic_pregnenenolone', 'Pregnenolone sulfate — NMDA+, GABA-A-',
             'right chin', 'PALE-YELLOW', RGB['PALE-YELLOW'],
             element='Pr(59)', particle='proton'),
    BodyNode('right_chin_excitatory_serotonin', '5-HT3 — ligand-gated, fast excitatory',
             'right chin', 'GREEN', RGB['GREEN'],
             element='Eu(63)', particle='serotonin_1a'),
    BodyNode('male_left_epinephrine_switch', 'Epinephrine — β-adrenergic, cAMP/PKA',
             'left fourth finger', 'RED', RGB['RED'],
             particle='epinephrine'),
    BodyNode('right_androgen', 'Androgen receptor — direction reversal, motor',
             'right fourth toe', 'DARK-BROWN', RGB['DARK-BROWN'],
             particle='testosterone'),
    BodyNode('drd2l_postsynaptic', 'D2L postsynaptic — GR-modulated, spatial clarity',
             'left frontalis outer strip lower', 'BLUE', RGB['BLUE'],
             particle='dopamine'),
    BodyNode('drd1_observer', 'D1 observer copy — mirror motor, pH buffer',
             'center right sole', 'RED', RGB['RED'],
             particle='down_quark'),
    BodyNode('observer_leftd2', 'DRD2 master permissive — outside left eye',
             'outside left eye', 'RED', RGB['RED'],
             element='Na(11)', particle='w_boson'),
    BodyNode('nonobserver_left_d2', 'DRD2/D3 non-observer — cortisol clarity switch',
             'left frontalis outer strip', 'BLUE', RGB['BLUE'],
             particle='dopamine'),
    BodyNode('observer_left_endorphin', 'MOR observer — electron antineutrino, night spark',
             'left philtrum', 'GREEN', RGB['GREEN'],
             element='Mg(12)', particle='electron_antineutrino'),
    BodyNode('left_endorphin_non_observer', 'MOR non-observer — electron neutrino, day spark',
             'left levator superioris', 'GREEN', RGB['GREEN'],
             particle='electron_neutrino'),
    BodyNode('clay_gouge', 'Clay gouge — anal sphincter, tight junction sealing',
             'anal sphincter', 'BROWN', RGB['BROWN'],
             particle='graviton'),
    BodyNode('magnetite_mux', 'Magnetite MUX — Fe3O4 directional sensor',
             'center torso', 'BLACK', RGB['BLACK'],
             element='Zn(30)', particle='gluon'),
    BodyNode('tff_autophagy', 'T flip-flop autophagy — inflammatory mode',
             'global', 'DARK-GRAY', RGB['DARK-GRAY'],
             particle='electron'),
]


# ============================================================
# 7. 128 PERSONALITIES
# ============================================================

# All 16 MBTI types
MBTI_TYPES = [
    'ENFP', 'ENFJ', 'ENTP', 'ENTJ',
    'ESFP', 'ESFJ', 'ESTP', 'ESTJ',
    'INFP', 'INFJ', 'INTP', 'INTJ',
    'ISFP', 'ISFJ', 'ISTP', 'ISTJ',
]

GENDERS = ['M', 'F']
BLOOD_TYPES = ['O', 'A', 'B', 'AB']


def generate_128_personalities() -> List[Personality]:
    """Generate all 128 personality types."""
    personalities = []
    for mbti in MBTI_TYPES:
        for gender in GENDERS:
            for blood in BLOOD_TYPES:
                personalities.append(Personality(
                    mbti=mbti, gender=gender, blood_type=blood
                ))
    return personalities


# ============================================================
# 8. COLOR MATCHING ENGINE
# ============================================================

def rgb_distance(c1: Tuple[int,int,int], c2: Tuple[int,int,int]) -> float:
    """Euclidean distance in RGB space."""
    return math.sqrt(
        (c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2
    )

def color_similarity(c1: Tuple[int,int,int], c2: Tuple[int,int,int]) -> float:
    """Similarity score 0-1 (1=identical)."""
    max_dist = math.sqrt(3 * 255**2)
    return 1.0 - (rgb_distance(c1, c2) / max_dist)


def match_personality_to_nodes(
    personality: Personality,
    nodes: List[BodyNode],
    hour: int,
    top_n: int = 10
) -> List[Tuple[BodyNode, float]]:
    """Match a personality to body nodes by color similarity.
    Returns list of (node, similarity_score) sorted by score descending."""
    p_color = personality.color(hour)
    scored = []
    for node in nodes:
        sim = color_similarity(p_color, node.color_rgb)
        scored.append((node, sim))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]


def match_node_to_personalities(
    node: BodyNode,
    personalities: List[Personality],
    hour: int,
    top_n: int = 10
) -> List[Tuple[Personality, float]]:
    """Match a body node to personalities by color similarity."""
    scored = []
    for p in personalities:
        sim = color_similarity(node.color_rgb, p.color(hour))
        scored.append((p, sim))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]


# ============================================================
# 9. TIME-SLOT AWARE MAPPING
# ============================================================

def get_time_slot(hour: int) -> dict:
    """Get the toroidal time slot for a given hour."""
    h = hour % 24
    if 0 <= h < 3:
        return TIME_SLOTS[0]
    elif 3 <= h < 9:
        return TIME_SLOTS[1]
    elif 9 <= h < 15:
        return TIME_SLOTS[2]
    elif 15 <= h < 21:
        return TIME_SLOTS[3]
    else:
        return TIME_SLOTS[4]


def full_mapping(
    personalities: List[Personality],
    nodes: List[BodyNode],
    hours: List[int],
    top_n: int = 5
) -> Dict:
    """Generate full mapping: personality × time_slot × top_nodes."""
    result = {}
    for p in personalities:
        result[p.code] = {}
        for h in hours:
            slot = get_time_slot(h)
            matches = match_personality_to_nodes(p, nodes, h, top_n)
            result[p.code][f"{h:02d}h"] = {
                'time_slot': slot['hours'],
                'phase': slot['phase'],
                'genre': slot['genre'],
                'day_night': 'day' if is_daytime(h) else 'night',
                'personality_rgb': p.color(h),
                'top_nodes': [
                    {
                        'node': n.name,
                        'function': n.function,
                        'location': n.location,
                        'node_color': n.color_name,
                        'node_rgb': n.color_rgb,
                        'similarity': round(sim, 4),
                    }
                    for n, sim in matches
                ]
            }
    return result


# ============================================================
# 10. MAIN
# ============================================================

def main():
    print("=" * 80)
    print("Color Mapping Engine — 128 Personalities × Body Nodes × Time Slots")
    print("Node colors: ACTUAL chemical/biochemical properties")
    print("=" * 80)
    
    personalities = generate_128_personalities()
    print(f"\nGenerated {len(personalities)} personalities")
    print(f"Loaded {len(NODES)} body nodes")
    
    # Example: ISTP_M_O at different hours
    print("\n" + "=" * 60)
    print("EXAMPLE: ISTP_M_O (Element: O(8))")
    print("=" * 60)
    
    istp = next(p for p in personalities if p.code == 'ISTP_M_O')
    for h in [2, 8, 12, 18, 22]:
        slot = get_time_slot(h)
        color = istp.color(h)
        dn = 'day' if is_daytime(h) else 'night'
        print(f"\n  {h:02d}h [{slot['hours']} | {slot['phase']} | {dn}]")
        print(f"  Channel: {istp.channel} | Base: {istp.base_color(h)} | Full: {color}")
        matches = match_personality_to_nodes(istp, NODES, h, top_n=5)
        for node, sim in matches:
            print(f"    → {node.name:30s} {node.color_name:15s} sim={sim:.3f}  ({node.function[:40]})")
    
    # Example: ENFP_F_AB at different hours
    print("\n" + "=" * 60)
    print("EXAMPLE: ENFP_F_AB (Element: Zn(30))")
    print("=" * 60)
    
    enfp = next(p for p in personalities if p.code == 'ENFP_F_AB')
    for h in [2, 8, 12, 18, 22]:
        slot = get_time_slot(h)
        color = enfp.color(h)
        dn = 'day' if is_daytime(h) else 'night'
        print(f"\n  {h:02d}h [{slot['hours']} | {slot['phase']} | {dn}]")
        print(f"  Channel: {enfp.channel} | Base: {enfp.base_color(h)} | Full: {color}")
        matches = match_personality_to_nodes(enfp, NODES, h, top_n=5)
        for node, sim in matches:
            print(f"    → {node.name:30s} {node.color_name:15s} sim={sim:.3f}  ({node.function[:40]})")
    
    # Full mapping to JSON
    print("\n" + "=" * 60)
    print("Generating full mapping (128 personalities × 5 time points)...")
    print("=" * 60)
    
    sample_hours = [2, 8, 12, 18, 22]
    mapping = full_mapping(personalities, NODES, sample_hours, top_n=5)
    
    output_file = "c:/Users/User/Downloads/color_mapping_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"\nFull mapping saved to: {output_file}")
    print(f"  {len(personalities)} personalities × {len(sample_hours)} time points × top-5 nodes")
    print(f"  {len(NODES)} body nodes with actual chemical/biochemical colors")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("NODE COLOR DISTRIBUTION (actual chemical colors)")
    print("=" * 60)
    color_counts = {}
    for node in NODES:
        color_counts[node.color_name] = color_counts.get(node.color_name, 0) + 1
    for color, count in sorted(color_counts.items(), key=lambda x: -x[1]):
        print(f"  {color:20s} : {count} nodes")


if __name__ == '__main__':
    main()
