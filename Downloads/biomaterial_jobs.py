#!/usr/bin/env python3
from particle_to_8d import particles_to_dims, MBTI_TYPES, BLOOD_TYPES, GENDERS

profiles = [f'{mbti}_{g}_{b}' for mbti in MBTI_TYPES for g in GENDERS for b in BLOOD_TYPES]

jobs = {
    '1_Biomaterials_Scientist': {
        'desc': 'microbe->biomass->material discovery, broad bio+materials',
        'w': {'p':3, 's':2, 'h':2, 'd':3, 'r':3, 'gamma':2, 'g':2, 'nu':3},
    },
    '2_Biopolymer_Scientist': {
        'desc': 'PLA/PHA polymer design, chemistry+structure',
        'w': {'p':4, 's':2, 'h':1, 'd':3, 'r':3, 'gamma':1, 'g':2, 'nu':2},
    },
    '3_Mycelium_Materials_Scientist': {
        'desc': 'fungal strain+growth+density+composite, biology+hands-on',
        'w': {'p':3, 's':3, 'h':2, 'd':2, 'r':2, 'gamma':2, 'g':2, 'nu':3},
    },
    '4_Biomaterials_Formulation_Scientist': {
        'desc': 'mix materials for target properties, chemistry+precision',
        'w': {'p':4, 's':2, 'h':2, 'd':3, 'r':3, 'gamma':1, 'g':2, 'nu':2},
    },
    '5_BioComposite_Materials_Engineer': {
        'desc': 'fibre/interface/microstructure+industrial architecture',
        'w': {'p':3, 's':2, 'h':1, 'd':3, 'r':4, 'gamma':2, 'g':3, 'nu':1},
    },
    '6_Bioprocess_Engineer': {
        'desc': 'fermentation->separation->scale-up, systems+industrial',
        'w': {'p':4, 's':1, 'h':0, 'd':3, 'r':4, 'gamma':2, 'g':3, 'nu':1},
    },
    '7_Fermentation_Engineer_Materials': {
        'desc': 'microbe as chemical factory, fermentation optimization',
        'w': {'p':3, 's':1, 'h':1, 'd':3, 'r':4, 'gamma':2, 'g':2, 'nu':2},
    },
    '8_Microbial_Materials_Engineer': {
        'desc': 'microorganism as material producer, microbiology+materials',
        'w': {'p':3, 's':2, 'h':2, 'd':2, 'r':3, 'gamma':2, 'g':2, 'nu':3},
    },
    '9_Algal_Biomaterials_Scientist': {
        'desc': 'algae->material, biological properties+ecosystem',
        'w': {'p':2, 's':3, 'h':3, 'd':2, 'r':2, 'gamma':3, 'g':2, 'nu':3},
    },
    '10_Biofabrication_Engineer': {
        'desc': 'biology->material formation, 3D printing+grown material',
        'w': {'p':3, 's':3, 'h':3, 'd':2, 'r':2, 'gamma':3, 'g':2, 'nu':2},
    },
    '11_Living_Materials_Engineer': {
        'desc': 'living cells in material, self-healing/biosensing, frontier',
        'w': {'p':2, 's':2, 'h':3, 'd':2, 'r':2, 'gamma':3, 'g':2, 'nu':4},
    },
    '12_Biomaterials_Manufacturing_Engineer': {
        'desc': 'R&D->factory, extrusion/moulding/scale-up',
        'w': {'p':4, 's':2, 'h':0, 'd':2, 'r':4, 'gamma':2, 'g':3, 'nu':1},
    },
    '13_BioBased_Product_Designer': {
        'desc': 'material->product design, aesthetics+function',
        'w': {'p':3, 's':4, 'h':3, 'd':1, 'r':2, 'gamma':3, 'g':2, 'nu':2},
    },
    '14_Biomaterials_Process_Dev_Scientist': {
        'desc': 'cheaper+stable production, optimization+efficiency',
        'w': {'p':4, 's':2, 'h':1, 'd':3, 'r':4, 'gamma':1, 'g':2, 'nu':1},
    },
    '15_Biomass_to_Materials_Engineer': {
        'desc': 'waste->feedstock->biomaterial, circular+industrial',
        'w': {'p':3, 's':2, 'h':1, 'd':3, 'r':3, 'gamma':2, 'g':3, 'nu':2},
    },
    '16_Circular_Biomaterials_Engineer': {
        'desc': 'full lifecycle design, production->use->recovery->reuse',
        'w': {'p':3, 's':2, 'h':2, 'd':2, 'r':3, 'gamma':3, 'g':3, 'nu':3},
    },
    '17_Biomaterials_LCA_Sustainability': {
        'desc': 'LCA calculation, data+analysis+systems thinking',
        'w': {'p':3, 's':2, 'h':1, 'd':4, 'r':3, 'gamma':2, 'g':2, 'nu':2},
    },
}

for job_name, info in jobs.items():
    weights = info['w']
    scored = []
    for label in profiles:
        d = particles_to_dims(label, 'day')['dims']
        score = sum(d[dim] * w for dim, w in weights.items())
        scored.append((label, round(score, 4)))
    scored.sort(key=lambda x: x[1], reverse=True)
    print(f'\n=== {job_name} ===')
    print(f'  {info["desc"]}')
    for s in scored[:3]:
        d = particles_to_dims(s[0], 'day')['dims']
        dims_str = f"p={d['p']:.2f} s={d['s']:.2f} h={d['h']:.2f} r={d['r']:.2f} g={d['g']:.2f} gam={d['gamma']:.2f} nu={d['nu']:.2f} d={d['d']:.2f}"
        print(f"  {s[0]}: score={s[1]} {dims_str}")
