"""Test master equation computation"""
import sys
sys.path.insert(0, '.')
import kernel_v1 as k

psi_terms = k.compute_psi_static()
print("Ψ_static computation (10 terms):")
for name, val in psi_terms.items():
    print(f"  {name:15s} = {val:.6f}")
print()
print(f"5-stage energy flow: {len(k.ENERGY_FLOW_5)} phases")
print(f"4 archetypes: {list(k.ARCHETYPES_4.keys())}")
print(f"8D param mapping: {len(k.D8_PARTICLE_OUTLET)} dims")
print(f"4 cosmic objects: {list(k.COSMIC_OBJECTS_4.keys())}")
print(f"3-tier mapping: {len(k.TIER3_MAPPING)} nodes")
print(f"24 master constants: {len(k.MASTER_CONSTANTS)}")
print(f"6 spheres: {list(k.SIX_SPHERES.keys())}")
print(f"8 base particles: {k.PARTICLES_8}")
print(f"12 particles: {k.PARTICLES_12}")
print(f"6 quark flavors: {list(k.QUARK_6.keys())}")
print(f"3 neutrinos + 3 antineutrinos: {list(k.NEUTRINO_6.keys())}")
print(f"3 derived baryons: {list(k.DERIVED_BARYONS.keys())}")
print(f"5 hidden: {list(k.HIDDEN_PARTICLES.keys())}")
print(f"Total particles: {k.TOTAL_PARTICLES}")
