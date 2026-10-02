import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Check all 23 term values for ENTP_M_O day to see distribution
r = p.particles_to_dims('ENTP_M_O', 'day')
ueq = r.get('universe_equation', {})
terms = ueq.get('terms', {})
print("=== SIMPLE EQUATION TERM VALUES (ENTP_M_O day) ===")
for k in sorted(terms.keys()):
    v = terms[k]
    print(f"  {k}: {v:.6e}  abs={abs(v):.6e}")

print(f"\n  active: {ueq.get('active_constraint')}")
print(f"  homeostasis: {ueq.get('homeostasis_distance'):.6e}")

# Check closed equation terms
ceq = r.get('closed_universe_equation', {})
cterms = ceq.get('terms', {})
print("\n=== CLOSED EQUATION TERM VALUES (ENTP_M_O day) ===")
for k in sorted(cterms.keys()):
    v = cterms[k]
    print(f"  {k}: {v:.6e}  abs={abs(v):.6e}")
print(f"\n  active: {ceq.get('active_constraint')}")
print(f"  homeostasis: {ceq.get('homeostasis_distance'):.6e}")
