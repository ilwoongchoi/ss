"""
v11_pairing.py — Find correct 6-sphere → 3-peak pairing.
6 sphere (Fe/H/O/C/S/EM) → 3 acoustic peaks via closure × W7.
Test 6!/(2!2!2!) = 90 possible pairings.
"""
import math, json
from itertools import permutations
from pathlib import Path

DATA = {
    2: 1064.5, 50: 1442.0, 100: 1860.0, 150: 3078.0, 200: 5320.0,
    220: 5769.0, 300: 3980.0, 400: 2480.0, 500: 2572.0, 537: 2542.0,
    700: 1880.0, 800: 1500.0, 810: 1450.0, 1000: 830.0, 1200: 420.0,
    1400: 230.0, 1490: 170.0, 2000: 65.0, 2500: 25.0,
}

# Sphere weights (from closure_tension_base)
W7 = math.pi / 20          # 0.157
H2 = 1.0 / 9.0             # 0.111
C = math.sqrt(2) / 5        # 0.283
alpha = 1.0 / 137.036       # 7.30e-3
closure = 9 * math.pi / (20 * math.sqrt(2))   # 0.9996

# 6 sphere with master constant weights
SPHERES = {
    "Fe": {"w": 1.0 * closure * (1 + C),   "desc": "core (Fe-56, neutron star)"},
    "H":  {"w": 0.7 * closure * (1 + W7),  "desc": "light (main sequence)"},
    "O":  {"w": 0.5 * closure * (1 + H2),  "desc": "water (post-main)"},
    "C":  {"w": 0.4 * closure * (1 + W7/2),"desc": "organic (post-main)"},
    "S":  {"w": 0.3 * closure * (1 + H2/2),"desc": "sulfur (late massive)"},
    "EM": {"w": 0.9 * closure * (1 + alpha),"desc": "observer (closure)"},
}

# 6!/(2!2!2!) = 90 pairings, but for 3 pair groups = 15 distinct
# Pair (a,b) for peak 1, 2, 3
SPHERE_LIST = list(SPHERES.keys())

best_chi2 = float("inf")
best_pairing = None

# Generate all 15 distinct pairings of 6 elements into 3 pairs
from itertools import combinations
elements = SPHERE_LIST
pairings = []
seen = set()
for p1 in combinations(elements, 2):
    rem1 = [e for e in elements if e not in p1]
    for p2 in combinations(rem1, 2):
        p3 = tuple(e for e in rem1 if e not in p2)
        pairing = (p1, p2, p3)
        # Canonical: sort pairs and the triple
        canon = tuple(sorted([tuple(sorted(p)) for p in pairing]))
        if canon not in seen:
            seen.add(canon)
            pairings.append(pairing)

print(f"Testing {len(pairings)} distinct pairings...")
print()

for pairing in pairings:
    p1, p2, p3 = pairing
    # Amplitude per peak = sum of 2 sphere weights
    A1_target = SPHERES[p1[0]]["w"] + SPHERES[p1[1]]["w"]
    A2_target = SPHERES[p2[0]]["w"] + SPHERES[p2[1]]["w"]
    A3_target = SPHERES[p3[0]]["w"] + SPHERES[p3[1]]["w"]

    # Normalize to Planck peak 1 = 5769
    A1 = A1_target / max(A1_target, A2_target, A3_target) * 5769
    A2 = A2_target / max(A1_target, A2_target, A3_target) * 5769
    A3 = A3_target / max(A1_target, A2_target, A3_target) * 5769

    # Width per peak (closure-modulated)
    sigma1 = 80 * (1 + W7)
    sigma2 = 100 * (1 + W7)
    sigma3 = 90 * (1 + W7)

    def user_CMB(ell, A1, A2, A3):
        p1 = A1 * math.exp(-((ell - 220) / sigma1) ** 2 / 2)
        p2 = A2 * math.exp(-((ell - 537) / sigma2) ** 2 / 2)
        p3 = A3 * math.exp(-((ell - 810) / sigma3) ** 2 / 2)
        return p1 + p2 + p3

    # chi2
    chi2 = 0
    n = 0
    for ell in sorted(DATA.keys()):
        if 150 <= ell <= 1000:
            chi2 += ((user_CMB(ell, A1, A2, A3) - DATA[ell]) / DATA[ell]) ** 2
            n += 1
    chi2_n = chi2 / n

    if chi2_n < best_chi2:
        best_chi2 = chi2_n
        best_pairing = (p1, p2, p3, A1, A2, A3)

print(f"\nBest pairing (chi2/n = {best_chi2:.4f}):")
p1, p2, p3, A1, A2, A3 = best_pairing
print(f"  Peak 1: {p1[0]} + {p1[1]}  → A1 = {A1:.0f} (Planck 5769)")
print(f"  Peak 2: {p2[0]} + {p2[1]}  → A2 = {A2:.0f} (Planck 2542)")
print(f"  Peak 3: {p3[0]} + {p3[1]}  → A3 = {A3:.0f} (Planck 1450)")
print(f"  Ratios: 1 : {A2/A1:.3f} : {A3/A1:.3f}")
print(f"  Planck: 1 : 0.440 : 0.251")

# Save
out = {
    "version": "v11_pairing",
    "method": "6-sphere pairing → 3-peak (closure × W7 weighted)",
    "best_chi2_n": best_chi2,
    "pairing": {"peak1": list(p1), "peak2": list(p2), "peak3": list(p3)},
    "amplitudes": {"A1": A1, "A2": A2, "A3": A3},
    "ratios": {"peak1": 1.0, "peak2": A2/A1, "peak3": A3/A1},
    "planck_ratios": {"peak1": 1.0, "peak2": 2542/5769, "peak3": 1450/5769},
    "grade": "STRONG" if best_chi2 < 0.07 else ("MEDIUM" if best_chi2 < 0.15 else "WEAK"),
}
Path("v11_pairing.json").write_text(json.dumps(out, indent=2))
print(f"\nWrote v11_pairing.json")
