"""
iso_8base_with_leakage.py — 8 base cascade WITH leakage to 17 cavity.
Each transition has a KAPPA gap rate that leaks mass to the cavity.
Mass conservation in UNIVERSE (particles + cavity) = 1.0, but in cascade < 1.0.
"""
import math, json
from pathlib import Path

# Real BASE_W_7 rates (gap between transitions = leakage)
K_TRANS = {
    "HG":  math.sqrt(0.08),   # 0.2828 (H → G transition)
    "GM":  1.0,                # 0 → 1 (G → M)
    "MP":  2.0 / 16.0,         # 0.125 (M → P)
    "PT":  3.0 / 16.0,         # 0.1875 (P → T)
    "TW":  math.sqrt(0.08),    # 0.2828 (T → W)
    "WZ":  4.0 / 16.0,         # 0.25 (W → Z)
    "Znu": 1.0 / 28.0,         # 0.0357 (Z → νμ, LUNAR)
}

# KAPPA_LADDER leakage rates (gap to 17 cavity)
# 7 rungs: 1/2, 1/32, 1/64, 1/128, 1/256, 3/32, D3_angle(69.44°)
K_LEAK = {
    "HG":  1.0 / 32.0,    # κ_2: H → G transition leaks to cavity_2
    "GM":  1.0 / 64.0,    # κ_3: G → M leaks to cavity_3
    "MP":  1.0 / 128.0,   # κ_4: M → P leaks to cavity_4
    "PT":  1.0 / 256.0,   # κ_5: P → T leaks to cavity_5
    "TW":  3.0 / 32.0,    # κ_gate: T → W leaks to compression_gate
    "WZ":  1.0 / 2.0,     # κ_1: W → Z leaks to cavity_1 (largest leakage)
    "Znu": 1.0 / 32.0,    # κ_2: Z → νμ leaks to cavity_2
}

# Cavity mapping: 17 cavity, 7 leak pathways
CAVITY_MAP = {
    "HG":  "D3_observer_gate_left_eye_outer",  # cavity 1
    "GM":  "D3_observer_gate_right_eye_outer",  # cavity 2
    "MP":  "transform_gate_right_levator_scap",  # cavity 3
    "PT":  "structural_anchor_fold_belt_sternum",  # cavity 4
    "TW":  "structural_anchor_right_ribs_jesus",  # cavity 5
    "WZ":  "physiological_excretion_lungs_exhalation",  # cavity 6
    "Znu": "physiological_excretion_kidney_urine",  # cavity 7
}


def cascade_with_leak(t, x, K_trans, K_leak):
    """8 state + 7 cavity = 15 state.
    dstate/dt = transition_in - transition_out - leak_out
    dcavity/dt = leak_in"""
    H, G, M, P, T_, W, Z, N = x[:8]
    L1, L2, L3, L4, L5, L6, L7 = x[8:15]  # 7 leak cavities

    # Particle transitions
    dH = -K_trans["HG"] * H - K_leak["HG"] * H
    dG = +K_trans["HG"] * H - K_trans["GM"] * G - K_leak["GM"] * G
    dM = +K_trans["GM"] * G - K_trans["MP"] * M - K_leak["MP"] * M
    dP = +K_trans["MP"] * M - K_trans["PT"] * P - K_leak["PT"] * P
    dT = +K_trans["PT"] * P - K_trans["TW"] * T_ - K_leak["TW"] * T_
    dW = +K_trans["TW"] * T_ - K_trans["WZ"] * W - K_leak["WZ"] * W
    dZ = +K_trans["WZ"] * W - K_trans["Znu"] * Z - K_leak["Znu"] * Z
    dN = +K_trans["Znu"] * Z  # νμ: ghost sink, no further leak

    # Cavity leak-in
    dL1 = K_leak["HG"] * H
    dL2 = K_leak["GM"] * G
    dL3 = K_leak["MP"] * M
    dL4 = K_leak["PT"] * P
    dL5 = K_leak["TW"] * T_
    dL6 = K_leak["WZ"] * W
    dL7 = K_leak["Znu"] * Z

    return [dH, dG, dM, dP, dT, dW, dZ, dN,
            dL1, dL2, dL3, dL4, dL5, dL6, dL7]


def rk4(f, t, x, h, K_trans, K_leak):
    k1 = f(t, x, K_trans, K_leak)
    k2 = f(t+h/2, [x[i]+h*k1[i]/2 for i in range(15)], K_trans, K_leak)
    k3 = f(t+h/2, [x[i]+h*k2[i]/2 for i in range(15)], K_trans, K_leak)
    k4 = f(t+h, [x[i]+h*k3[i] for i in range(15)], K_trans, K_leak)
    return [x[i]+h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(15)], t+h


def main():
    print("=" * 70)
    print("CASCADE WITH KAPPA LEAKAGE to 17 CAVITY")
    print("=" * 70)
    print(f"\nK_TRANS = {K_TRANS}")
    print(f"\nK_LEAK (KAPPA ladder, gap to 17 cavity) = {K_LEAK}")

    x0 = [1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ts, xs = [], [x0[:]]
    t, x = 0.0, x0[:]
    dt = 0.05
    for _ in range(int(2000/dt)):
        x, t = rk4(cascade_with_leak, t, x, dt, K_TRANS, K_LEAK)
        ts.append(t)
        xs.append(x[:])

    print(f"\n  {'t':>6s}  {'H':>6s}  {'G':>6s}  {'M':>6s}  {'P':>6s}  "
          f"{'T':>6s}  {'W':>6s}  {'Z':>6s}  {'N':>6s}  "
          f"{'Σ_part':>6s}  {'Σ_leak':>6s}  {'Σ_uni':>6s}")

    for i in [0, 5, 10, 20, 30, 50, 100, 200, 500, 1000, 1999]:
        if i < len(ts):
            x = xs[i]
            part = sum(x[:8])
            leak = sum(x[8:15])
            uni = part + leak
            print(f"  {ts[i]:5.1f}  {x[0]:6.4f}  {x[1]:6.4f}  {x[2]:6.4f}  {x[3]:6.4f}  "
                  f"{x[4]:6.4f}  {x[5]:6.4f}  {x[6]:6.4f}  {x[7]:6.4f}  "
                  f"{part:6.4f}  {leak:6.4f}  {uni:6.4f}")

    final = xs[-1]
    print(f"\nFinal particle sum: {sum(final[:8]):.6f} (NOT 1.0 — leakage)")
    print(f"Final cavity sum: {sum(final[8:15]):.6f}")
    print(f"Final universe sum: {sum(final):.6f} (SHOULD be 1.0)")
    print(f"Final ghost sink (νμ): {final[7]:.6f}")
    print(f"Final Z retained: {final[6]:.6f}")
    print(f"Total leakage to 17 cavity: {sum(final[8:15]):.6f}")

    # Save
    out = {
        "version": "iso_8base_with_leakage",
        "method": "Cascade with KAPPA_LADDER leakage to 17 cavity",
        "K_TRANS": K_TRANS,
        "K_LEAK": K_LEAK,
        "cavity_map": CAVITY_MAP,
        "final_particle_sum": sum(final[:8]),
        "final_leakage_sum": sum(final[8:15]),
        "final_universe_sum": sum(final),
        "final_nu_mu": final[7],
        "final_Z": final[6],
    }
    Path("iso_8base_with_leakage.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote iso_8base_with_leakage.json")


if __name__ == "__main__":
    main()
