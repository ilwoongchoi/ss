#!/usr/bin/env python3
from particle_to_8d import particles_to_dims, MBTI_TYPES, BLOOD_TYPES, GENDERS

profiles = [f'{mbti}_{g}_{b}' for mbti in MBTI_TYPES for g in GENDERS for b in BLOOD_TYPES]

jobs = {
    '1_Subterranean_Spatial_Ecologist': {
        'desc': 'underground ecosystem design, air/water/microbe/plant cycle',
        'w': {'p':3, 's':2, 'h':2, 'd':2, 'r':2, 'gamma':3, 'g':3, 'nu':4},
    },
    '2_Subterranean_Resource_Geologist': {
        'desc': 'rock strength/fracture/water/gas/stability for permanent space',
        'w': {'p':4, 's':2, 'h':0, 'd':4, 'r':3, 'gamma':2, 'g':3, 'nu':1},
    },
    '3_Underground_Climate_Architect': {
        'desc': 'temp/humidity/CO2/light/sound/smell microclimate design',
        'w': {'p':3, 's':3, 'h':2, 'd':2, 'r':2, 'gamma':4, 'g':3, 'nu':2},
    },
    '4_Subterranean_Hydrological_Architect': {
        'desc': 'groundwater->purify->drink->agri->industrial->treat->recover',
        'w': {'p':4, 's':2, 'h':1, 'd':3, 'r':3, 'gamma':3, 'g':3, 'nu':2},
    },
    '5_Geothermal_Habitat_Engineer': {
        'desc': 'geothermal heating/cooling/energy/thermal storage',
        'w': {'p':3, 's':1, 'h':0, 'd':3, 'r':4, 'gamma':2, 'g':3, 'nu':1},
    },
    '6_Underground_Lightscape_Architect': {
        'desc': 'light as building material, spectrum/dawn/noon/sunset/night',
        'w': {'p':3, 's':4, 'h':3, 'd':1, 'r':2, 'gamma':3, 'g':2, 'nu':2},
    },
    '7_Subterranean_Biophilic_Architect': {
        'desc': 'water/wind/plants/rock/sound/humidity/season underground',
        'w': {'p':2, 's':3, 'h':3, 'd':1, 'r':1, 'gamma':4, 'g':2, 'nu':3},
    },
    '8_Underground_Food_System_Architect': {
        'desc': 'algae->fungi->crops->insects->fermentation->protein->waste->recover',
        'w': {'p':3, 's':2, 'h':2, 'd':2, 'r':3, 'gamma':2, 'g':3, 'nu':3},
    },
    '9_Subterranean_Fermentation_Engineer': {
        'desc': 'underground stable temp/dark for fermentation biomanufacturing',
        'w': {'p':3, 's':1, 'h':1, 'd':3, 'r':4, 'gamma':2, 'g':2, 'nu':3},
    },
    '10_Underground_Circularity_Architect': {
        'desc': 'resource->production->consumption->recovery->transformation->resource',
        'w': {'p':3, 's':2, 'h':2, 'd':2, 'r':3, 'gamma':3, 'g':3, 'nu':3},
    },
    '11_Subsurface_Waste_Bioconversion_Engineer': {
        'desc': 'waste->feedstock, food/cellulose/CO2/wastewater->biomass',
        'w': {'p':3, 's':2, 'h':1, 'd':3, 'r':3, 'gamma':2, 'g':2, 'nu':3},
    },
    '12_Underground_Manufacturing_Architect': {
        'desc': 'raw->process->fabricate->assemble->store->distribute underground',
        'w': {'p':4, 's':2, 'h':0, 'd':2, 'r':4, 'gamma':2, 'g':4, 'nu':1},
    },
    '13_Subterranean_Logistics_Network_Architect': {
        'desc': '3D transport: autonomous/pneumatic/rail/elevator/pipeline/robot',
        'w': {'p':4, 's':2, 'h':0, 'd':2, 'r':4, 'gamma':2, 'g':4, 'nu':1},
    },
    '14_Surface_Subsurface_Interface_Architect': {
        'desc': 'entrance/vent/exit/lightshaft/elevator/water/energy interface',
        'w': {'p':3, 's':3, 'h':2, 'd':2, 'r':3, 'gamma':3, 'g':3, 'nu':1},
    },
    '15_Surface_Wilderness_Architect': {
        'desc': 'rewilding/invasive removal/river restore/forest succession',
        'w': {'p':2, 's':2, 'h':2, 'd':1, 'r':2, 'gamma':4, 'g':2, 'nu':4},
    },
    '16_Surface_Silence_Designer': {
        'desc': 'noise removal, preserve natural sound, acoustic ecology',
        'w': {'p':2, 's':3, 'h':3, 'd':2, 'r':1, 'gamma':4, 'g':2, 'nu':3},
    },
    '17_Surface_Void_Curator': {
        'desc': 'empty space as value, why NOT to build, art+philosophy',
        'w': {'p':2, 's':3, 'h':4, 'd':1, 'r':1, 'gamma':3, 'g':1, 'nu':3},
    },
    '18_Planetary_Surface_Preservation_Planner': {
        'desc': 'planetary scale conservation, wilderness/corridor/access/preservation',
        'w': {'p':3, 's':2, 'h':2, 'd':2, 'r':2, 'gamma':3, 'g':3, 'nu':3},
    },
    '19_Subterranean_Psychology_Architect': {
        'desc': 'claustrophobia/horizon/daylight/season/spatial disorientation',
        'w': {'p':2, 's':3, 'h':4, 'd':2, 'r':1, 'gamma':4, 'g':2, 'nu':3},
    },
    '20_Underground_Culture_Architect': {
        'desc': 'plazas/theatres/galleries/music/libraries/gardens/ritual/silence',
        'w': {'p':2, 's':3, 'h':4, 'd':1, 'r':2, 'gamma':4, 'g':2, 'nu':3},
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
