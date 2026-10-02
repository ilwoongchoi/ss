#!/usr/bin/env python3
from particle_to_8d import particles_to_dims, MBTI_TYPES, BLOOD_TYPES, GENDERS

profiles = [f'{mbti}_{g}_{b}' for mbti in MBTI_TYPES for g in GENDERS for b in BLOOD_TYPES]

jobs = {
    '1_Surface_Minimalism_Curator': {'p':3, 's':4, 'h':3, 'd':1, 'r':1, 'gamma':3, 'g':2, 'nu':2},
    '2_Subterranean_Biourbanist': {'p':4, 's':2, 'h':1, 'd':2, 'r':3, 'gamma':3, 'g':3, 'nu':1},
    '3_Lithic_Acoustic_Architect': {'p':2, 's':3, 'h':3, 'd':2, 'r':1, 'gamma':4, 'g':2, 'nu':3},
    '4_Vertical_Luminescence_Agronomist': {'p':3, 's':4, 'h':2, 'd':2, 'r':3, 'gamma':2, 'g':2, 'nu':2},
    '5_Sub_Surface_Logistics_Operator': {'p':4, 's':2, 'h':0, 'd':2, 'r':4, 'gamma':2, 'g':3, 'nu':0},
}

for job_name, weights in jobs.items():
    scored = []
    for label in profiles:
        d = particles_to_dims(label, 'day')['dims']
        score = sum(d[dim] * w for dim, w in weights.items())
        scored.append((label, round(score, 4)))
    scored.sort(key=lambda x: x[1], reverse=True)
    print(f'\n=== {job_name} ===')
    for s in scored[:5]:
        d = particles_to_dims(s[0], 'day')['dims']
        dims_str = f"p={d['p']:.2f} s={d['s']:.2f} h={d['h']:.2f} r={d['r']:.2f} g={d['g']:.2f} gamma={d['gamma']:.2f} nu={d['nu']:.2f} d={d['d']:.2f}"
        print(f"  {s[0]}: score={s[1]} {dims_str}")
