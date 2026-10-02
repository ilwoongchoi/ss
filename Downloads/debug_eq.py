import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Test equation convergence for several profiles
test_profiles = ['ENTP_M_O', 'INTP_M_AB', 'ENTJ_F_A', 'INFJ_M_B', 'ESFP_F_O']

for prof in test_profiles:
    result = p.particles_to_dims(prof, 'day')
    eq = result.get('equation_derived', {})
    eq_gaps = result.get('equation_gaps', {})
    dims = result.get('dims', {})
    
    print(f"\n=== {prof} ===")
    print(f"  dims: {dims}")
    print(f"  active_branch: {eq.get('active_branch','')}")
    print(f"  homeo_before: {eq.get('homeostasis_before',0):.6f}")
    print(f"  homeo_after:  {eq.get('homeostasis_after',0):.6f}")
    print(f"  eq_before: {eq.get('equation_before',0):.2e}")
    print(f"  eq_after:  {eq.get('equation_after',0):.2e}")
    
    # Check which terms are far from zero
    ueq = result.get('universe_equation', {})
    terms = ueq.get('terms', {})
    far_terms = [(k, v) for k, v in terms.items() if abs(v) > 0.3]
    far_terms.sort(key=lambda x: -abs(x[1]))
    print(f"  terms far from 0 (|t|>0.3):")
    for k, v in far_terms[:5]:
        print(f"    {k}: {v:.4f}")
    
    # Check clamp issue
    print(f"  reciprocal terms (x*y=1 type):")
    for k in ['t4_gammad','t5_gamma_rg','t6_hrg','t7_dnu','t9_sgamma','t10_hd','t11_rs']:
        print(f"    {k}: {terms.get(k,0):.4f}")
