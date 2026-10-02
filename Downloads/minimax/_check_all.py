import kernel_v1 as k

all_closures = [
    'T_DISCREPANCY', 'CA1_CMB_TOPOLOGY', 'HUBBLE_TENSION', 'MUON_G2',
    'DYNAMICAL_STABILITY', 'PTA_NANOGRAV', 'JWST_Z14', 'KAPPA_LADDER',
    'MASTER_EQ_BOUNDED', 'PARTICLES_8_INTO_12', 'SPHERE_ATTRACTOR_BIJECTION',
    'LEAKAGE_CAVITY', 'UNSPARK_RECEPTOR', 'ESR1_SPLIT',
    'COMBINED_AND_GATES', 'PARTICLE_32', 'PEAK_CYCLE',
    'LAYER_ENTRIES_80', 'ENERGY_FLOW_5', 'D8_PARTICLE_OUTLET',
    'NODE_14_5HT1B_8ATTR',
    'CASCADE', 'COUPLING_ANALOGS', 'ARCHETYPE_BYPASS',
]
closed = 0
for n in all_closures:
    val = getattr(k, n + '_CLOSED', None)
    mark = "OK" if val else "FAIL"
    if val:
        closed += 1
    print(f"  [{mark}] {n:30s} = {val}")
print(f"\nCLOSED: {closed}/{len(all_closures)}")
