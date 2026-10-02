import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

profiles = ['ENTP_M_O', 'INFJ_F_O', 'ISTJ_M_A', 'ENFP_F_AB', 'INTP_M_B', 'ESFJ_F_A']
for prof in profiles:
    for phase in ['day', 'night']:
        r = p.particles_to_dims(prof, phase)
        eqd = r.get('equation_derived', {})
        ueq = r.get('universe_equation', {})
        ceq = r.get('closed_universe_equation', {})
        
        active = ueq.get('active_constraint', '')
        eq_before = eqd.get('equation_before', 0)
        eq_after = eqd.get('equation_after', 0)
        homeo_before = eqd.get('homeostasis_before', 0)
        homeo_after = eqd.get('homeostasis_after', 0)
        adjusted_key = eqd.get('adjusted_key', '')
        branch = eqd.get('active_branch', '')
        
        closed_val = ceq.get('equation_value', 0)
        closed_active = ceq.get('active_constraint', '')
        closed_homeo = ceq.get('homeostasis_distance', 0)
        gauge = ceq.get('gauge_invariance_residual', 0)
        
        print(f"{prof} {phase}:")
        print(f"  simple_eq: active={active} before={eq_before:.4e} after={eq_after:.4e} homeo={homeo_before:.4e}->{homeo_after:.4e} adjust={adjusted_key}")
        print(f"  closed_eq: active={closed_active} value={closed_val:.4e} homeo={closed_homeo:.4e} gauge={gauge:.4e}")
        print()
