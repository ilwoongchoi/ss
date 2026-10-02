import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Debug: trace iteration for INTJ_M_A (A blood type, failing)
dims = {'r': 0.5, 'h': 0.5, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.5, 'g': 0.5, 'nu': 0.5}
# Get actual dims from particles_to_dims
r = p.particles_to_dims('INTJ_M_A', 'day')
dims = r['dims']
print(f"Initial dims: {dims}")
print(f"Blood type: A → alpha=-1.5, beta=0.15")

adjusted = dict(dims)
for i in range(8):
    eq = p.compute_universe_equation(adjusted, blood_type='A')
    active = eq['active_constraint']
    homeo = eq['homeostasis_distance']
    t8_val = eq['terms'].get('t8_p_ag_b', 0)
    t5_val = eq['terms'].get('t5_gamma_rg', 0)
    print(f"  iter={i} active={active} homeo={homeo:.6e} t5={t5_val:.6e} t8={t8_val:.6e}")
    
    adjusted2, active_i, eq_i = p._solve_one_step(adjusted, 'A')
    eq_after = p.compute_universe_equation(adjusted2, blood_type='A')
    print(f"    → adjusted_key={eq_i.get('active_constraint','')} homeo_after={eq_after['homeostasis_distance']:.6e}")
    adjusted = adjusted2

print(f"\nFinal dims: {adjusted}")
print(f"Final equation_after: {eq_after['equation_value']:.6e}")
