"""
cmb_v8_3rd_order.py — CMB 3-peak fit with HIGHER ORDER ODEs.

3rd-order ODE: d³T/dℓ³ + a d²T/dℓ² + b dT/dℓ + c T = F(ℓ)
4th-order ODE: 4 mode coupled oscillator
Both 3 acoustic peaks fixed at ℓ=220, 537, 810.
"""
import math, json
from pathlib import Path

PLANCK_TT = {
    2: 1064.5, 50: 1442.0, 100: 1860.0, 150: 3078.0, 200: 5320.0,
    220: 5769.0, 300: 3980.0, 400: 2480.0, 500: 2572.0, 537: 2542.0,
    700: 1880.0, 800: 1500.0, 810: 1450.0, 1000: 830.0, 1200: 420.0,
    1400: 230.0, 1490: 170.0, 2000: 65.0, 2500: 25.0,
}


# ============================================================
# 3rd-order ODE transfer function
# H(ω) = 1 / |P(iω)|² where P(s) = s³ + a s² + b s + c
# |P(iω)|² = (c - aω²)² + (bω - ω³)²
# 3 acoustic peaks = 3 roots of P(s) near s = i*220, i*537, i*810
# ============================================================
def cmb_3rd_order(ell, a, b, c, K, silk_d):
    denom2 = (c - a * ell ** 2) ** 2 + (b * ell - ell ** 3) ** 2 + 1e-10
    return K / denom2 * math.exp(-((ell / silk_d) ** 2))


# ============================================================
# 4th-order ODE: sum of 2 coupled 2nd-order oscillators (4 modes)
# ============================================================
def cmb_4th_order(ell, A1, A2, A3, A4, w1, w2, w3, w4, g1, g2, g3, g4, silk_d):
    s = 0.0
    for A, w, g in zip([A1, A2, A3, A4], [w1, w2, w3, w4], [g1, g2, g3, g4]):
        s += A / ((ell ** 2 - w ** 2) ** 2 + (g * ell) ** 2 + 1e-10)
    return s * math.exp(-((ell / silk_d) ** 2))


# ============================================================
# 5 coupled 2nd-order oscillators (1 extra for high-ℓ Silk damping)
# ============================================================
def cmb_5_coupled(ell, A1, A2, A3, A4, A5, g1, g2, g3, g4, g5, silk_d):
    L_PEAK = [220.0, 537.0, 810.0, 1200.0, 1500.0]
    s = 0.0
    for A, lpk, g in zip([A1, A2, A3, A4, A5], L_PEAK, [g1, g2, g3, g4, g5]):
        s += A / ((ell ** 2 - lpk ** 2) ** 2 + (g * ell) ** 2)
    return s * math.exp(-((ell / silk_d) ** 2))


def fit_3rd():
    ell_data = [ell for ell in sorted(PLANCK_TT.keys()) if 150 <= ell <= 1000]
    y_data = [PLANCK_TT[ell] for ell in ell_data]
    best_chi2 = float("inf")
    best = None
    # P(s) = s³ + a s² + b s + c
    # For 3 peaks at 220, 537, 810: roots are s = -γ_n ± i·ω_n
    # Approximation: a ≈ sum(γ), b ≈ sum(ω² + γ²), c ≈ product(ω)
    # Try grid around expected values
    for a in [200, 500, 1000, 2000, 5000]:
        for b in [1e5, 5e5, 1e6, 5e6, 1e7]:
            for c in [1e7, 1e8, 1e9, 1e10]:
                for K in [1e15, 1e17, 1e19, 1e21]:
                    for silk_d in [800, 1000, 1200, 1500, 2000]:
                        y_pred = [cmb_3rd_order(ell, a, b, c, K, silk_d) for ell in ell_data]
                        chi2 = sum((y_p - y_d) ** 2 / max(y_d, 1) for y_p, y_d in zip(y_pred, y_data))
                        chi2_n = chi2 / len(ell_data)
                        if chi2_n < best_chi2:
                            best_chi2 = chi2_n
                            best = (a, b, c, K, silk_d)
    return best_chi2, best


def fit_4th():
    ell_data = [ell for ell in sorted(PLANCK_TT.keys()) if 150 <= ell <= 1000]
    y_data = [PLANCK_TT[ell] for ell in ell_data]
    best_chi2 = float("inf")
    best = None
    for A1 in [1e10, 5e10, 1e11, 5e11]:
        for A2 in [1e8, 5e8, 1e9, 5e9]:
            for A3 in [1e7, 5e7, 1e8, 5e8]:
                for g1 in [50, 100, 200, 400]:
                    for g2 in [100, 200, 400, 800]:
                        g3 = g2 * 0.85
                        # 4th mode (Silk)
                        A4 = A3 * 0.3
                        g4 = 200
                        w4 = 1200
                        for silk_d in [800, 1000, 1200]:
                            y_pred = [cmb_4th_order(ell, A1, A2, A3, A4,
                                                    220, 537, 810, w4,
                                                    g1, g2, g3, g4, silk_d) for ell in ell_data]
                            chi2 = sum((y_p - y_d) ** 2 / max(y_d, 1) for y_p, y_d in zip(y_pred, y_data))
                            chi2_n = chi2 / len(ell_data)
                            if chi2_n < best_chi2:
                                best_chi2 = chi2_n
                                best = (A1, A2, A3, A4, g1, g2, g3, g4, silk_d)
    return best_chi2, best


if __name__ == "__main__":
    print("=" * 70)
    print("CMB v8 — Higher Order ODE")
    print("=" * 70)

    print("\n[1] 3rd-order ODE fit")
    chi2_3, p3 = fit_3rd()
    print(f"  chi2/n = {chi2_3:.4f}")
    print(f"  params: a={p3[0]}, b={p3[1]:.2e}, c={p3[2]:.2e}, K={p3[3]:.2e}, silk_d={p3[4]}")

    print("\n[2] 4th-order (4 coupled 2nd-order) fit")
    chi2_4, p4 = fit_4th()
    print(f"  chi2/n = {chi2_4:.4f}")
    print(f"  params: A1={p4[0]:.2e}, A2={p4[1]:.2e}, A3={p4[2]:.2e}, A4={p4[3]:.2e}")
    print(f"  γ1={p4[4]}, γ2={p4[5]}, γ3={p4[6]}, γ4={p4[7]}, silk={p4[8]}")

    # Save
    out = {
        "3rd_order_chi2_n": chi2_3,
        "4th_order_chi2_n": chi2_4,
        "best": "4th" if chi2_4 < chi2_3 else "3rd",
    }
    Path("cmb_v8.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote cmb_v8.json")
