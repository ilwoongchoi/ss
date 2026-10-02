"""Test all dynamical functions"""
import sys
sys.path.insert(0, '.')
import kernel_v1 as k
import math

print("=" * 60)
print("EXTENDED DYNAMICAL FUNCTIONS TEST")
print("=" * 60)

# Test 16-window peak cycle
print("\n[16-WINDOW PEAK CYCLE]")
for t in range(0, 24, 1):
    pd = k.peak_dim(t)
    print(f"  t={t:2d}h: {pd:5s} | 1.5h window", end="\r")

# Test kappa ladder
print("\n\n[KAPPA LADDER]")
for name, val in k.KAPPA_LADDER.items():
    print(f"  {name:25s} = {val}")

# Test homeostasis direction
print("\n[HOMEOSTASIS DIRECTION]")
for p in [0.2, 0.5, 0.8]:
    d = k.homeostasis_direction(1.0, p)
    print(f"  p={p}: direction={d}")

# Test 4:30 PM transition
print("\n[4:30 PM TRANSITION]")
for kk, vv in k.PM_430_TRANSITION.items():
    print(f"  {kk}: {vv}")

# Test 3 AM hysteresis
print("\n[3 AM HYSTERESIS]")
for kk, vv in k.AM_3_HYSTERESIS.items():
    print(f"  {kk}: {vv}")

# Test cognitive functions
print("\n[8 COGNITIVE FUNCTIONS]")
for fn, desc in k.COGNITIVE_FUNCTIONS_8.items():
    print(f"  {fn}: {desc}")

# Test 8D → 12D
print("\n[8D → 12D MAPPING]")
v8 = [0.5, 0.6, 0.7, 0.8, 0.3, 0.4, 0.2, 0.1]
v12 = k.v8_to_v12(v8, 0.5, 0.5, 0.5, 0.5)
print(f"  8D:  {v8}")
print(f"  12D: {v12}")

# Test PLP spine / Barnard
print("\n[PLP SPINE]")
for kk, vv in k.PLP_SPINE.items():
    print(f"  {kk}: {vv}")
print("\n[BARNARD 5-BODY]")
for kk, vv in k.BARNARD_5_BODY.items():
    print(f"  {kk}: {vv}")
