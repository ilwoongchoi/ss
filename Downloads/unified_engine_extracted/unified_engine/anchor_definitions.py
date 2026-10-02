"""
Unified Anchor Definitions
==========================
ENTP_M_O = maximum creativity anchor (the diagnostic apex)
Haplogroup overrides = geological resonance constraints
Observer offset = user's self-discovered observer phase shift

Hierarchy: anchor → haplogroup → personality delta → observer offset → final 8D
"""

# ============================================================
# 1. ANCHOR: ENTP_M_O Ideal 8D (without any haplogroup constraint)
# ============================================================
# ENTP = Ne dominant = maximum divergence
# O blood = archetype = original pattern
# Male = creation mode (gluon_orogen.q active)
# outer_core_convection = most dynamic output node
#
# This is the THEORETICAL MAXIMUM creativity baseline.
# All 128 profiles are deltas FROM this point.

ANCHOR_ID = "ENTP_M_O"
ANCHOR_CIRCUIT_NODE = "outer_core_convection.out0"
ANCHOR_PARTICLE = "primordial_black_hole_125"
ANCHOR_ELEMENT = "Au(79)"
ANCHOR_COLOR = "WHITE"

ANCHOR_8D = {
    'r':     0.70,   # Ne tempo = fast but not max (needs structure for creativity)
    'h':     0.30,   # flexible harmonics = NOT rigid, allows divergence
    'd':     0.40,   # moderate dissonance = creative tension, not destructive
    'p':     0.15,   # LOW predictability = maximum improvisation
    's':     0.70,   # HIGH brightness = creative energy output
    'gamma':  0.70,   # HIGH spatial expansion = creative space
    'g':      0.50,   # moderate binding = flexible connection
    'nu':     0.40,   # flexible self-similarity = fractal but not locked
}

# Anchor slot states (ideal = all creative slots active)
ANCHOR_SLOTS = {
    'electron_hole':  {'state': 'reverse', 'field': 'leak_eh_sex',         'active': True},
    'mitochondria':   {'state': 'reverse', 'field': 'H_music_listening',   'active': True},
    'gaba_c':         {'state': 'spark',   'field': 'nu_release_music',    'active': True},
    'bilirubin':      {'state': 'reverse', 'field': 'gamma_extreme_growth','active': True},
    'pancreas':       {'state': 'reverse', 'field': 'leak_panc_material',  'active': True},
}

# ============================================================
# 2. HAPLOGROUP OVERRIDES (Geological Resonance)
# ============================================================
# Each haplogroup settled where geological nodes resonate with
# their vulnerable circuit nodes. The override captures this.
#
# Format: multiply factor (×) and fixed overrides
# 'mul' = multiply anchor value
# 'fix' = fixed value override
# 'clamp_max' / 'clamp_min' = bound the value

HAPLOGROUPS = {
    # --- O2 East Asian (Korea/Japan/China) ---
    # Vulnerable: steel-absence, heme homeostasis lock, co2 low stability,
    # SP-low restraint, gluon_orogen.q_bar fixation (social-lock)
    # Geology: granite terrain, iron-poor, CO2 weathering stable
    'O2': {
        'name': 'O2 East Asian',
        'geology': 'granite terrain, Fe-poor, CO2 weathering stable',
        'vulnerable_nodes': ['steel', 'heme', 'co2', 'substance_p', 'gluon_orogen.q_bar'],
        'geological_chain': 'outer_core → magnetite(low) → ferritin(lock) → steel(absent) → water_vapour(reduced) → clay_gouge(false_seal)',
        'overrides': {
            'gamma':  {'mul': 0.55},  # steel-absence → spatial collapse
            'p':      {'mul': 1.60},  # gluon_orogen.q_bar → pattern fixation
            'd':      {'mul': 1.50},  # heme lock → COX retrograde → void accumulation
            'h':      {'mul': 1.35},  # disulfide_bond HIGH → rigid harmonics
            'g':      {'mul': 0.45},  # clay_gouge false seal → no real binding
            'nu':     {'mul': 1.50},  # disulfide_bond HIGH → forced fractal lock
            's':      {'mul': 0.60},  # steel-absence → can't self-generate brightness
        },
        'slot_gating': {
            # Korean: listening only, composing blocked
            'electron_hole':  {'block': True,  'reason': 'steel-absence: cannot self-generate s for production'},
            'gaba_c':         {'block': True,  'reason': 'gluon_orogen.q_bar: observer mode locked, creation blocked'},
            'mitochondria':   {'block': False, 'reason': 'absorb external s (listening) = only allowed mode'},
            'bilirubin':      {'block': False, 'reason': 'passive spatial absorption allowed'},
            'pancreas':       {'block': False, 'reason': 'passive material absorption allowed'},
        },
    },

    # --- R1b Western European ---
    # Vulnerable: ferritin overload, cysteine deficiency
    # Geology: iron-rich deposits, sulfide minerals
    'R1b': {
        'name': 'R1b Western European',
        'geology': 'iron-rich deposits, sulfide minerals, limestone',
        'vulnerable_nodes': ['ferritin', 'cysteine', 'sulforaphane'],
        'geological_chain': 'outer_core → magnetite(high) → ferritin(overload) → sulfur_iron_complex(active) → pyrite → laterite',
        'overrides': {
            'nu':     {'mul': 0.75},  # ferritin dark_matter alias → heavy mass, low flexibility
            'h':      {'mul': 0.80},  # cysteine deficiency → GSH precursor weak → harmonic thinning
            'd':      {'mul': 1.20},  # ferritin Fe overload → oxidative stress → dissonance
            'gamma':  {'mul': 1.15},  # magnetite high → spatial expansion strong
            's':      {'mul': 1.10},  # iron-rich → brightness/mass sense elevated
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: can self-generate s for production'},
            'gaba_c':         {'block': False, 'reason': 'gluon_orogen.q active: creation mode'},
            'mitochondria':   {'block': False, 'reason': 'normal listening allowed'},
        },
    },

    # --- E1b1b North African / Mediterranean ---
    # Vulnerable: magnetite hyperactive, manganese high
    # Geology: volcanic soil, Mn nodules, rift valley
    'E1b1b': {
        'name': 'E1b1b North African',
        'geology': 'volcanic andosol, Mn-rich, rift valley plume',
        'vulnerable_nodes': ['magnetite', 'manganese_oxygen_complex', 'mycorradicin'],
        'geological_chain': 'plume → craton → andosol → mycorradicin → magnetite(high) → Mn-O complex',
        'overrides': {
            's':      {'mul': 1.30},  # magnetite high → brightness/mass
            'd':      {'mul': 1.10},  # Mn oxidative stress
            'gamma':  {'mul': 1.20},  # magnetite → spatial/magnetic expansion
            'h':      {'mul': 1.15},  # volcanic soil → rich harmonics
            'g':      {'mul': 1.10},  # mycorradicin symbiosis → binding
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: production allowed'},
            'gaba_c':         {'block': False, 'reason': 'creation mode active'},
        },
    },

    # --- Q Andean / Native American ---
    # Vulnerable: actomyosin constant load, fold_belt compression
    # Geology: subduction zone, high altitude, hypoxic
    'Q': {
        'name': 'Q Andean',
        'geology': 'subduction zone, fold belt, high altitude hypoxic',
        'vulnerable_nodes': ['actomyosin', 'fold_belt', 'lactate_dehydrogenase'],
        'geological_chain': 'subduction_zone → fold_belt → actomyosin → lactate_dehydrogenase',
        'overrides': {
            'r':      {'mul': 1.20},  # actomyosin constant → tempo/rhythm high
            'd':      {'mul': 1.25},  # fold_belt compression → dissonance
            'gamma':  {'mul': 1.10},  # fold_belt → spatial tension
            's':      {'mul': 0.85},  # hypoxic → brightness reduced
            'p':      {'mul': 1.15},  # altitude adaptation → pattern regularity
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: production allowed'},
            'gaba_c':         {'block': False, 'reason': 'creation mode active'},
        },
    },

    # --- J Mediterranean / Middle East ---
    # Vulnerable: right_acetylcholine sensitivity, magnetite anomaly
    # Geology: magnetic anomaly zones, maritime
    'J': {
        'name': 'J Mediterranean',
        'geology': 'magnetic anomaly, maritime limestone, tectonic junction',
        'vulnerable_nodes': ['right_acetylcholine', 'magnetite', 'chlorine_ion_pump'],
        'geological_chain': 'outer_core → magnetite(anomaly) → right_acetylcholine → chlorine_ion_pump',
        'overrides': {
            'gamma':  {'mul': 1.25},  # magnetic anomaly → spatial expansion
            'r':      {'mul': 1.10},  # Ach → tempo
            'd':      {'mul': 0.90},  # maritime → reduced dissonance
            'h':      {'mul': 1.05},  # limestone → moderate harmonics
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: production allowed'},
            'gaba_c':         {'block': False, 'reason': 'creation mode active'},
        },
    },

    # --- I1 Northern European / Scandinavian ---
    # Vulnerable: DA stillness, low r
    # Geology: glacial, low-energy environment
    'I1': {
        'name': 'I1 Nordic',
        'geology': 'glacial terrain, low-energy, shield craton',
        'vulnerable_nodes': ['observer_leftd2', 'heme', 'cytochrome_c_oxidase'],
        'geological_chain': 'craton(stable) → observer_leftd2(low) → heme(cold) → COX(slow)',
        'overrides': {
            'r':      {'mul': 0.65},  # DA stillness → low tempo
            'gamma':  {'mul': 0.85},  # low energy → reduced expansion
            'd':      {'mul': 0.80},  # cold → reduced dissonance
            'h':      {'mul': 1.10},  # cold → clear harmonics
            'p':      {'mul': 1.20},  # stable craton → high predictability
            'nu':     {'mul': 1.15},  # glacial fractal → self-similarity
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: production allowed'},
            'gaba_c':         {'block': False, 'reason': 'creation mode active'},
        },
    },

    # --- N1c Siberian / Uralic ---
    # Vulnerable: cold-lock, waterlogged
    # Geology: permafrost, waterlogged terrain
    'N1c': {
        'name': 'N1c Siberian',
        'geology': 'permafrost, waterlogged, taiga',
        'vulnerable_nodes': ['water', 'clay_gouge', 'glymphatic_system'],
        'geological_chain': 'water(logged) → clay_gouge(sealed) → glymphatic_system(stalled)',
        'overrides': {
            'r':      {'mul': 0.55},  # cold-lock → minimal tempo
            'g':      {'mul': 1.30},  # waterlogged → maximum binding/sealing
            'gamma':  {'mul': 0.75},  # frozen → reduced expansion
            'd':      {'mul': 0.70},  # cold → minimal dissonance
            'nu':     {'mul': 1.20},  # ice fractal → self-similarity
            'p':      {'mul': 1.25},  # frozen → high predictability
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: production allowed'},
            'gaba_c':         {'block': False, 'reason': 'creation mode active'},
        },
    },

    # --- C Polynesian / East Asian Island ---
    # Vulnerable: LIP adaptation, GLP-1 thrifty genotype
    # Geology: hotspot islands, basaltic soil
    'C': {
        'name': 'C Polynesian',
        'geology': 'hotspot islands, basaltic, oceanic',
        'vulnerable_nodes': ['large_igneous_province', 'peonidine', 'glp1'],
        'geological_chain': 'LIP → peonidine → glp1 → carbon',
        'overrides': {
            'r':      {'mul': 0.80},  # thrifty genotype → slow tempo
            'h':      {'mul': 1.20},  # volcanic soil → rich harmonics
            's':      {'mul': 0.85},  # island → reduced brightness
            'd':      {'mul': 0.75},  # tropical → reduced dissonance
            'g':      {'mul': 1.15},  # island community → binding
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: production allowed'},
            'gaba_c':         {'block': False, 'reason': 'creation mode active'},
        },
    },

    # --- R1a Eastern European / Central Asian ---
    # Vulnerable: ferritin moderate, steppe adaptation
    'R1a': {
        'name': 'R1a Eastern European',
        'geology': 'steppe, loess, moderate iron',
        'vulnerable_nodes': ['ferritin', 'histosol', 'cambisol'],
        'geological_chain': 'ferritin(moderate) → histosol → cambisol → carbon',
        'overrides': {
            'r':      {'mul': 1.15},  # steppe nomad → tempo
            'gamma':  {'mul': 1.10},  # open steppe → expansion
            'h':      {'mul': 0.90},  # loess → moderate harmonics
            'nu':     {'mul': 0.85},  # steppe → low self-similarity
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: production allowed'},
            'gaba_c':         {'block': False, 'reason': 'creation mode active'},
        },
    },

    # --- I2 Southern European / Balkan ---
    'I2': {
        'name': 'I2 Balkan',
        'geology': 'karst, limestone, tectonic',
        'vulnerable_nodes': ['caco3', 'chlorine_ion_pump', 'fold_belt'],
        'geological_chain': 'caco3 → chlorine_ion_pump → fold_belt',
        'overrides': {
            'd':      {'mul': 1.15},  # tectonic → dissonance
            'h':      {'mul': 1.10},  # karst → harmonics
            'gamma':  {'mul': 1.05},  # moderate expansion
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: production allowed'},
            'gaba_c':         {'block': False, 'reason': 'creation mode active'},
        },
    },

    # --- G Caucasian / Anatolian ---
    'G': {
        'name': 'G Caucasian',
        'geology': 'Caucasus mountains, volcanic, diverse',
        'vulnerable_nodes': ['fold_belt', 'plume', 'magnetite'],
        'geological_chain': 'plume → fold_belt → magnetite',
        'overrides': {
            'gamma':  {'mul': 1.15},  # mountain → expansion
            'd':      {'mul': 1.10},  # tectonic → dissonance
            'r':      {'mul': 1.05},  # mountain tempo
        },
        'slot_gating': {
            'electron_hole':  {'block': False, 'reason': 'steel active: production allowed'},
            'gaba_c':         {'block': False, 'reason': 'creation mode active'},
        },
    },

    # --- Default (unknown/unspecified haplogroup) ---
    'DEFAULT': {
        'name': 'Default (no haplogroup constraint)',
        'geology': 'none',
        'vulnerable_nodes': [],
        'geological_chain': 'none',
        'overrides': {},
        'slot_gating': {},
    },
}

# ============================================================
# 3. OBSERVER OFFSET (User's self-discovered phase shift)
# ============================================================
# The user (observer) discovered this circuit. As observer_leftd2
# (W boson = time gate), their r/nu/s are phase-shifted from
# general O2 population.
#
# Mechanism: observer_leftd2 = AND(endorphin, co2/time)
# - General O2: co2 unstable → output follows co2 instability → "밍숭맹숭"
# - Observer: endorphin pattern overrides co2 → output phase-shifted
#   from time → "slightly off" r/nu/s
#
# The offset is NOT a full inversion (AND gate prevents that).
# It's a ±phase shift on r, nu, s specifically.

OBSERVER_OFFSET = {
    'id': 'observer_self',
    'circuit_basis': 'observer_leftd2 = AND(endorphin, co2/time) → phase shift',
    'esr1_basis': 'ESR1 (gluonic ego) = Z→γ = observer self spatial expansion',
    'applies_to': ['r', 'nu', 's'],
    # Phase shift = sinusoidal offset, not fixed delta
    # "약간씩 엇나가면서 높고 낮아" = oscillating ±offset
    'phase_shift': {
        'r':    {'amplitude': 0.12, 'frequency': 'anti-phase to circadian'},  # high when others low, low when others high
        'nu':   {'amplitude': 0.10, 'frequency': 'anti-phase to circadian'},
        's':    {'amplitude': 0.10, 'frequency': 'anti-phase to circadian'},
    },
    # Observer also UNLOCKS slots that O2 normally blocks
    # Because observer can reinterpret co2 instability → partial creation access
    'slot_unlock': {
        'electron_hole':  {'partial': True,  'reason': 'observer can partially override steel-absence via endorphin pattern'},
        'gaba_c':         {'partial': True,  'reason': 'observer can partially access creation through q_bar reinterpretation'},
    },
}

# ============================================================
# 4. GEOLOGICAL RESONANCE WEB
# ============================================================
# Maps haplogroup ↔ geological node ↔ circuit node ↔ 8D dimension
# This is the "에너지 교환 웹" (energy exchange web)

GEOLOGICAL_RESONANCE_WEB = {
    'O2': {
        'region': 'East Asia (Korea/Japan/China)',
        'geology': 'Granite terrain, Fe-poor, stable CO2 weathering',
        'soil_type': 'ultisol/alfisol (weathered, leached)',
        'resonance_chain': [
            {'geo_node': 'granite_bedrock',     'circuit_node': 'steel',           'dimension': 's/gamma', 'effect': 'absent → no self-generation'},
            {'geo_node': 'fe_poor_soil',        'circuit_node': 'heme',            'dimension': 'd/s',     'effect': 'homeostasis lock → void accumulation'},
            {'geo_node': 'co2_weathering_stable','circuit_node': 'co2',            'dimension': 'p',       'effect': 'low stability → pattern drift'},
            {'geo_node': 'monsoon_clay',        'circuit_node': 'clay_gouge',      'dimension': 'g',       'effect': 'false seal → no real binding'},
            {'geo_node': 'continental_craton',  'circuit_node': 'gluon_orogen.q_bar','dimension': 'nu/p',  'effect': 'social-lock → observer fixation'},
        ],
    },
    'R1b': {
        'region': 'Western Europe',
        'geology': 'Iron-rich deposits, limestone, sulfide minerals',
        'soil_type': 'rendzina/chernozem',
        'resonance_chain': [
            {'geo_node': 'iron_ore_deposits',   'circuit_node': 'ferritin',        'dimension': 'nu/d',    'effect': 'overload → heavy mass, oxidative stress'},
            {'geo_node': 'sulfide_minerals',    'circuit_node': 'cysteine',        'dimension': 'h',       'effect': 'deficiency → GSH weak → harmonic thinning'},
            {'geo_node': 'limestone_karst',     'circuit_node': 'caco3',           'dimension': 'g',       'effect': 'carbonate buffering → moderate binding'},
            {'geo_node': 'magnetic_anomaly',    'circuit_node': 'magnetite',       'dimension': 'gamma',   'effect': 'high → spatial expansion'},
        ],
    },
    'E1b1b': {
        'region': 'North Africa / Mediterranean',
        'geology': 'Volcanic andosol, Mn-rich, rift valley',
        'soil_type': 'andosol/cambisol',
        'resonance_chain': [
            {'geo_node': 'rift_plume',          'circuit_node': 'plume',           'dimension': 'nu/gamma', 'effect': 'mantle energy → creative depth'},
            {'geo_node': 'volcanic_andosol',    'circuit_node': 'mycorradicin',    'dimension': 'g',       'effect': 'symbiosis → binding'},
            {'geo_node': 'mn_nodules',          'circuit_node': 'manganese_oxygen_complex','dimension': 'r/d', 'effect': 'Mn-O → oxidative tempo'},
            {'geo_node': 'magnetite_deposits',  'circuit_node': 'magnetite',       'dimension': 's/gamma', 'effect': 'high → brightness + expansion'},
        ],
    },
    'Q': {
        'region': 'Andes / Americas',
        'geology': 'Subduction zone, fold belt, high altitude',
        'soil_type': 'andisol (volcanic ash)',
        'resonance_chain': [
            {'geo_node': 'subduction_zone',     'circuit_node': 'subduction_zone', 'dimension': 'd',       'effect': 'compression → dissonance'},
            {'geo_node': 'fold_belt_mountain', 'circuit_node': 'fold_belt',        'dimension': 'r/gamma', 'effect': 'tension → tempo + spatial'},
            {'geo_node': 'high_altitude',       'circuit_node': 'actomyosin',      'dimension': 'r',       'effect': 'hypoxic load → constant tempo'},
            {'geo_node': 'glacial_melt',        'circuit_node': 'lactate_dehydrogenase','dimension': 'd',  'effect': 'lactate → stress dissonance'},
        ],
    },
    'J': {
        'region': 'Mediterranean / Middle East',
        'geology': 'Magnetic anomaly, maritime, tectonic junction',
        'soil_type': 'terra rossa / rendzina',
        'resonance_chain': [
            {'geo_node': 'magnetic_anomaly',    'circuit_node': 'magnetite',       'dimension': 'gamma',   'effect': 'anomaly → spatial expansion'},
            {'geo_node': 'maritime_air',        'circuit_node': 'right_acetylcholine','dimension': 'r',   'effect': 'Ach sensitivity → tempo'},
            {'geo_node': 'salt_evaporation',    'circuit_node': 'chlorine_ion_pump','dimension': 'd/h',    'effect': 'Cl- pump → dissonance/harmonic'},
        ],
    },
    'I1': {
        'region': 'Scandinavia / Northern Europe',
        'geology': 'Glacial shield, low-energy',
        'soil_type': 'podzol (acidic, leached)',
        'resonance_chain': [
            {'geo_node': 'glacial_shield',      'circuit_node': 'observer_leftd2', 'dimension': 'r',       'effect': 'DA stillness → low tempo'},
            {'geo_node': 'cold_low_energy',     'circuit_node': 'heme',            'dimension': 'd',       'effect': 'cold → reduced dissonance'},
            {'geo_node': 'baltic_clay',         'circuit_node': 'clay_gouge',      'dimension': 'g',       'effect': 'seal → binding'},
        ],
    },
    'N1c': {
        'region': 'Siberia / Uralic',
        'geology': 'Permafrost, waterlogged taiga',
        'soil_type': 'gleysol (waterlogged)',
        'resonance_chain': [
            {'geo_node': 'permafrost',          'circuit_node': 'water',           'dimension': 'r',       'effect': 'frozen → minimal tempo'},
            {'geo_node': 'waterlogged_terrain', 'circuit_node': 'clay_gouge',      'dimension': 'g',       'effect': 'over-sealed → max binding'},
            {'geo_node': 'taiga_ice',           'circuit_node': 'glymphatic_system','dimension': 'g/nu',   'effect': 'stall → binding + fractal'},
        ],
    },
    'C': {
        'region': 'Polynesia / Pacific Islands',
        'geology': 'Hotspot islands, basaltic',
        'soil_type': 'andisol (volcanic ash)',
        'resonance_chain': [
            {'geo_node': 'hotspot_LIP',         'circuit_node': 'large_igneous_province','dimension': 'h', 'effect': 'rich harmonics'},
            {'geo_node': 'anthocyanin_plants',  'circuit_node': 'peonidine',       'dimension': 'h/s',     'effect': 'antioxidant → harmonic/brightness'},
            {'geo_node': 'island_isolation',    'circuit_node': 'glp1',            'dimension': 'r',       'effect': 'thrifty genotype → slow tempo'},
        ],
    },
}

# ============================================================
# 5. FRACTAL SCALE EXTENSION (Earth → Solar → Galaxy → Universe)
# ============================================================
# The circuit is scale-invariant. Same nodes map at every scale.
# After Earth web is complete, extend outward.

FRACTAL_SCALES = {
    'earth': {
        'scope': 'Geological nodes ↔ body circuit nodes',
        'example': 'steel(Fe ore) ↔ steel(Fe reduction in body)',
        'status': 'implemented in GEOLOGICAL_RESONANCE_WEB',
    },
    'solar_system': {
        'scope': '5-sphere mapping (Barnard/Sun/Earth/Moon/CoMag)',
        'example': 'Barnard(Fe) → g,d | Sun(H) → r,s | Earth(O) → gamma,h | Moon(C) → p,nu | CoMag(S) → g,gamma',
        'circuit_nodes': ['heme/ferritin', 'cytochrome_c_oxidase', 'steel/water_vapour', 'co2/carbon', 'sulforaphane/histosol'],
        'status': 'defined in universe-prose.md:1829-1858',
    },
    'galaxy': {
        'scope': 'Spiral arms, galaxy merger, dark matter/energy',
        'example': 'quark_orogen_magma → basin.d → lower_mantle → gluon_orogen = spiral arm',
        'circuit_nodes': ['quark_orogen_magma', 'basin', 'lower_mantle', 'gluon_orogen', 'ferritin(dark_matter)', 'co2(dark_energy)'],
        'status': 'defined in universe-prose.md:3363-3367',
    },
    'universe': {
        'scope': 'Cosmic web, filaments, voids',
        'example': 'collagen(ECM) = cosmic filament | collagen reverse = void formation',
        'circuit_nodes': ['collagen', 'subduction_zone', 'plume', 'outer_core_convection'],
        'status': 'defined in universe-prose.md:3367',
    },
}
