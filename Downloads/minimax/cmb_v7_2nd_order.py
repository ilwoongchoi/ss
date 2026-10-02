"""
cmb_v7_2nd_order.py — CMB 3-peak fit with 2nd-order damped driven oscillator.
Each acoustic peak is a damped driven harmonic oscillator.

T(ℓ) = Σ A_n / ((ℓ² - ℓ_n²)² + (γ_n · ℓ)²) × exp(-(ℓ/ℓ_silk)²)

9 parameters (3 amp + 3 width + 3 damping) + Silk damping scale.
3 peak positions FIXED at 220, 537, 810 (Planck 2018).
"""
import math, json
from pathlib import Path

PLANCK_TT = {
    2: 1064.5, 50: 1442.0, 100: 1860.0, 150: 3078.0, 200: 5320.0,
    220: 5769.0, 300: 3980.0, 400: 2480.0, 500: 2572.0, 537: 2542.0,
    700: 1880.0, 800: 1500.0, 810: 1450.0, 1000: 830.0, 1200: 420.0,
    1400: 230.0, 1490: 170.0, 2000: 65.0, 2500: 25.0,
}

L_PEAK = [220.0, 537.0, 810.0]


def cmb_2nd_order(ell_array, A1, A2, A3, gamma1, gamma2, gamma3, silk_d):
    """Damped driven oscillator transfer function for each peak."""
    out = []
    for ell in ell_array:
        s = 0.0
        for A, lpk, g in zip([A1, A2, A3], L_PEAK, [gamma1, gamma2, gamma3]):
            # 2nd-order resonance profile
            s += A / ((ell ** 2 - lpk ** 2) ** 2 + (g * ell) ** 2)
        s *= math.exp(-((ell / silk_d) ** 2))
        out.append(s)
    return out


def fit():
    ell_data = [ell for ell in sorted(PLANCK_TT.keys()) if 150 <= ell <= 1000]
    y_data = [PLANCK_TT[ell] for ell in ell_data]

    best_chi2 = float("inf")
    best_params = None
    for A1 in [1e9, 5e9, 1e10, 5e10, 1e11]:
        for A2 in [1e8, 5e8, 1e9, 5e9]:
            for A3 in [1e7, 5e7, 1e8, 5e8]:
                for g1 in [50, 100, 200, 400]:
                    for g2 in [100, 200, 400, 800]:
                        g3 = g2 * 0.85
                        for silk_d in [800, 1000, 1200, 1500]:
                            y_pred = cmb_2nd_order(ell_data, A1, A2, A3, g1, g2, g3, silk_d)
                            chi2 = sum((y_p - y_d) ** 2 / max(y_d, 1) for y_p, y_d in zip(y_pred, y_data))
                            chi2_n = chi2 / len(ell_data)
                            if chi2_n < best_chi2:
                                best_chi2 = chi2_n
                                best_params = (A1, A2, A3, g1, g2, g3, silk_d)
    return best_chi2, best_params


if __name__ == "__main__":
    chi2, params = fit()
    A1, A2, A3, g1, g2, g3, silk_d = params
    print("=" * 70)
    print("CMB v7 — 2nd-order Damped Driven Oscillator")
    print("=" * 70)
    print(f"\nBest fit:")
    print(f"  A1 = {A1:.4e}, A2 = {A2:.4e}, A3 = {A3:.4e}")
    print(f"  γ1 = {g1}, γ2 = {g2}, γ3 = {g3:.0f}")
    print(f"  silk_d = {silk_d}")
    print(f"\nchi2/n = {chi2:.4f}")
    grade = "STRONG" if chi2 < 0.07 else ("MEDIUM" if chi2 < 0.15 else "WEAK")
    print(f"Grade: {grade}")
    out = {
        "version": "v7_2nd_order",
        "method": "2nd-order damped driven oscillator (3 peaks fixed at 220, 537, 810)",
        "params": {"A1": A1, "A2": A2, "A3": A3, "gamma1": g1, "gamma2": g2, "gamma3": g3, "silk_d": silk_d},
        "chi2_n": chi2,
        "grade": grade,
    }
    Path("cmb_v7_2nd_order.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote cmb_v7_2nd_order.json")
