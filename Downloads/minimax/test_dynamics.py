"""Test dynamical functions"""
import sys
sys.path.insert(0, '.')
import kernel_v1 as k
import math

print("=" * 60)
print("DYNAMICAL FUNCTIONS TEST")
print("=" * 60)

# Test 1: closure_tension
T = k.closure_tension_base()
print(f"closure_tension_base: {T:.6f}  (prose: 0.9996, my T_closure earlier: 0.9228)")

# Test 2: dark_energy_release
for obs_d2 in [0, 0.5, 1.0]:
    de = k.dark_energy_release(obs_d2, co2_time=1.0)
    print(f"DE release (obs={obs_d2}): {de:.4f}")

# Test 3: universe expansion rate (using full universe DE release)
for obs_d2 in [0, 0.5, 1.0]:
    de = k.dark_energy_release_full(obs_d2)
    H = k.HUBBLE_H0 * math.sqrt(k.OMEGA_M + k.OMEGA_L * de)
    print(f"H(t) (obs={obs_d2}): DE={de:.4f}, H={H:.4f}  regime: {'dark_energy' if H>0.07 else ('matter' if H>0.05 else 'contraction')}")

# Test 4: dark matter density
print(f"DM density: {k.dark_matter_density(observer_d2=1.0):.4f}  (obs=1, q=1)")

# Test 5: CP violation
print(f"CP violation (obs=0): {k.cp_violation(0.0):.4f}")
print(f"CP violation (obs=1): {k.cp_violation(1.0):.4f}")

# Test 6: matter-antimatter
print(f"Matter/anti (obs=1): {k.matter_antimatter_balance(1.0):.2e}")

# Test 7: mandelbrot
z0 = 0+0j
h0 = 0.1+0j
n_iter = k.mandelbrot_iterate(z0, h0, max_iter=128)
print(f"Mandelbrot iterate (z0=0, h=0.1): {n_iter} iter (escape=2.0)")

# Test 8: master eq static
psi = k.compute_psi_static()
print(f"\nΨ_static: {psi['Psi_static']:.4f}  (prose: 67.77, my v2: 73.79)")

# Test 9: Proton pump
for obs in [0, 0.5, 1.0]:
    pp = k.proton_pump_output(obs, laterite_q=1.0)
    print(f"proton_pump (obs={obs}, q=1): {pp}")

# Test 10: peak_dim cycle (16 windows)
for t in [0, 4, 8, 12, 16, 20, 23]:
    print(f"t={t}h: peak_dim = {k.peak_dim(t)}")
