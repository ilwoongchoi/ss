"""Test state space"""
import sys
sys.path.insert(0, '.')
import kernel_v1 as k
import math

print("=" * 60)
print("STATE SPACE NUMBERS")
print("=" * 60)

# Verify state space counts
N_8 = 8
N_12 = 12
N_6_S = 6
N_6_A = 6
N_16_W = 16
N_4_L = 4
N_2_G = 2
N_4_B = 4
N_16_M = 16
N_5_T = 5
N_24_H = 24

# Total possible state combinations (theoretical)
N_TOTAL_FULL = (N_8 * N_12 * N_6_S * N_6_A * N_16_W * N_4_L
                * N_2_G * N_4_B * N_16_M)
print(f"  Full state space: {N_TOTAL_FULL:,}")

# Practical per-day per-profile
N_DAILY_PRACTICAL = N_8 * N_16_W * N_4_L * N_5_T  # 2560
print(f"  Practical daily cells: {N_DAILY_PRACTICAL:,}")

# All MBTI × blood × gender × layer combinations
N_PROFILES_TOTAL = N_16_M * N_2_G * N_4_B * N_4_L
print(f"  Profile state space: {N_PROFILES_TOTAL}")

# Daily cells per MBTI profile
N_DAILY_PROFILE = N_DAILY_PRACTICAL * N_PROFILES_TOTAL
print(f"  Daily cells × all profiles: {N_DAILY_PROFILE:,}")

# Verify some key constants
print(f"\n  Hubble H0 = {k.HUBBLE_H0} Gyr^-1")
print(f"  Omega_m = {k.OMEGA_M}")
print(f"  Omega_L = {k.OMEGA_L}")
print(f"  alpha_em = {k.MASTER_CONSTANTS['alpha_em']:.6f}  (1/137.036 = {1/137.036:.6f})")
print(f"  Phi (golden ratio) = {k.MASTER_CONSTANTS['phi']:.6f}  (1.618)")
print(f"  C nucleon = {k.MASTER_CONSTANTS['C_nucleon']:.6f}  (sqrt(2)/5 = {math.sqrt(2)/5:.6f})")
print(f"  W7 = {k.MASTER_CONSTANTS['W7']:.6f}  (pi/20 = {math.pi/20:.6f})")
print(f"  H2 = {k.MASTER_CONSTANTS['H2']:.6f}  (1/9 = {1/9:.6f})")

# Verify Betti numbers
print(f"\n  Betti: b0={k.BETTI['b0']}, b5={k.BETTI['b5']}, b7={k.BETTI['b7']}, b11={k.BETTI['b11']}")

# Verify particle counts
print(f"\n  8 base: {len(k.PARTICLES_8)}")
print(f"  12 core: {len(k.PARTICLES_12)}")
print(f"  6 quark: {len(k.QUARK_6)}")
print(f"  6 neutrino: {len(k.NEUTRINO_6)}")
print(f"  3 baryon: {len(k.DERIVED_BARYONS)}")
print(f"  5 hidden: {len(k.HIDDEN_PARTICLES)}")
print(f"  Total: {k.TOTAL_PARTICLES}")

# Compute full master equation
psi_full = k.master_equation_full(0, 0, 0, 12.0, 1.0, 0.5, 0.5, 0.5, 1.0, 1.0)
print(f"\n  Master equation (obs=1): Ψ = {psi_full:.4f}")

# Test 6 sphere mapping
print("\n  6 SPHERES (element → particle → attractor):")
for sphere, info in k.SIX_SPHERES.items():
    print(f"    {sphere:8s} | {info['element']:3s} | {info['particle']:25s} | {info['attractor']:18s}")
