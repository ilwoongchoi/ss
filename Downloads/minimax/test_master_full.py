"""Test full master equation"""
import sys
sys.path.insert(0, '.')
import kernel_v1 as k
import math

print("=" * 60)
print("FULL MASTER EQUATION TEST")
print("=" * 60)

# Test master_equation_full
print("\n[Master equation full]")
for obs in [0.0, 0.5, 1.0]:
    psi = k.master_equation_full(0, 0, 0, 12.0, obs, 0.5, 0.5, 0.5, 1.0, 1.0)
    print(f"  obs={obs}: Ψ = {psi:.4f}")

# Test F_final
print("\n[F_final]")
for obs in [0.0, 0.5, 1.0]:
    f = k.F_final(obs, 10, 1.5, 1.0, 1.0)
    print(f"  obs={obs}: F = {f:.4f}")

# Test L1 mandelbrot
print("\n[L1 Mandelbrot depth]")
for mbti in ["INTJ", "ENFP", "ISFP"]:
    d = k.L1_mandelbrot_depth(mbti, "M", "O")
    print(f"  {mbti}: depth = {d}")

# Test L2 clifford
print("\n[L2 Clifford constraint]")
c = k.L2_clifford_constraint(0.5, 0.5, 0.5, 0.5)
print(f"  lss=0.5, rss=0.5, le=0.5, re=0.5: {c:.4f}")

# Test Cosmic scenarios
print("\n[Cosmic scenarios]")
for scen, desc in k.COSMIC_SCENARIOS.items():
    print(f"  {scen}: {desc}")

# Test L3 spacetime, L4 rebranch
print("\n[L3 SPACETIME]")
for kk, vv in k.L3_SPACETIME.items():
    print(f"  {kk}: {vv}")
print("\n[L4 REBRANCH]")
for kk, vv in k.L4_REBRANCH.items():
    print(f"  {kk}: {vv}")

# Test 16-window peak cycle (full 24h)
print("\n[16-WINDOW PEAK CYCLE (24h)]")
for t in range(24):
    pd = k.peak_dim(t)
    if t % 4 == 0:
        print(f"  t={t:2d}h: {pd} (window {(t*2)//3})")
