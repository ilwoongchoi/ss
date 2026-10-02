import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Check what the equation gap analysis says
r = p.particles_to_dims('ENTP_M_O', 'day')
eqg = r.get('equation_gaps', {})
print('=== SIMPLE EQUATION GAP ANALYSIS ===')
print(f"covered_pairs: {eqg.get('covered_pairs', 0)}/{eqg.get('total_pairs', 28)}")
print(f"uncovered_pairs: {eqg.get('uncovered_pairs', 0)}")
print(f"uncovered_pair_names: {eqg.get('uncovered_pair_names', [])}")
print(f"structural_gaps:")
for sg in eqg.get('structural_gaps', []):
    print(f"  {sg['gap']}: {sg['desc']}")

# Check closed universe equation keys
ce = r.get('closed_universe_equation', {})
print(f"\n=== CLOSED UNIVERSE EQUATION KEYS ({len(ce.keys())}) ===")
for k in sorted(ce.keys()):
    v = ce[k]
    if isinstance(v, dict):
        print(f"  {k}: dict({len(v)} keys)")
    elif isinstance(v, list):
        print(f"  {k}: list({len(v)})")
    elif isinstance(v, (int, float, str, bool)):
        print(f"  {k}: {v}")
    else:
        print(f"  {k}: {type(v).__name__}")

# Check cosmological completeness
cos = r.get('cosmological', {})
print(f"\n=== COSMOLOGICAL COMPLETENESS ({len(cos)} keys) ===")
for k, v in sorted(cos.items()):
    print(f"  {k}: {v}")

# Check all return keys
print(f"\n=== ALL RETURN KEYS ({len(r.keys())}) ===")
for k in sorted(r.keys()):
    v = r[k]
    if isinstance(v, dict):
        print(f"  {k}: dict({len(v)})")
    elif isinstance(v, list):
        print(f"  {k}: list({len(v)})")
    else:
        print(f"  {k}: {type(v).__name__}")
