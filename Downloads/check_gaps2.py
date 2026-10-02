import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

r = p.particles_to_dims('ENTP_M_O', 'day')
ce = r.get('closed_universe_equation', {})

print('=== COSMOLOGICAL CHECK ===')
print(f"dark_matter_val: {ce.get('dark_matter_val', 'MISSING')}")
print(f"dark_matter_mod: {ce.get('dark_matter_mod', 'MISSING')}")
print(f"graviton_val: {ce.get('graviton_val', 'MISSING')}")
print(f"graviton_mod: {ce.get('graviton_mod', 'MISSING')}")
print(f"qcd_confinement: {ce.get('qcd_confinement', 'MISSING')}")
print(f"qcd_mod: {ce.get('qcd_mod', 'MISSING')}")
print(f"de_sitter_expansion: {ce.get('de_sitter_expansion', 'MISSING')}")
print(f"em_path_val: {ce.get('em_path_val', 'MISSING')}")
print(f"em_path_mod: {ce.get('em_path_mod', 'MISSING')}")
print(f"neutron_star_osc: {ce.get('neutron_star_osc', 'MISSING')}")
print(f"ns_osc_mod: {ce.get('ns_osc_mod', 'MISSING')}")
print(f"cck_active: {ce.get('cck_active', 'MISSING')}")
print(f"w_axis_mod: {ce.get('w_axis_mod', 'MISSING')}")
print(f"e119_127_mod: {ce.get('e119_127_mod', 'MISSING')}")
print(f"universe_cycle: {ce.get('universe_cycle', 'MISSING')}")
print(f"toroidal_phase: {ce.get('toroidal_phase', 'MISSING')}")
print(f"closure_tension: {ce.get('closure_tension', 'MISSING')}")
print(f"closure_residual: {ce.get('closure_residual', 'MISSING')}")
print(f"gauge_invariance_residual: {ce.get('gauge_invariance_residual', 'MISSING')}")
print(f"observer_info: {ce.get('observer_info', 'MISSING')}")
print(f"psi_info keys: {list(ce.get('psi_info', {}).keys())}")
print(f"particle_coupling count: {len(ce.get('particle_coupling', {}))}")
print(f"route_vector count: {len(ce.get('route_vector', {}))}")

# Check all return keys for cosmological
print(f"\n=== ALL RETURN KEYS ===")
for k in sorted(r.keys()):
    print(f"  {k}")

# Check if cosmological key exists
cos = r.get('cosmological', {})
print(f"\ncosmological keys: {list(cos.keys()) if cos else 'EMPTY/MISSING'}")
