"""pythagorean_residual_test.py

User thesis: the 3 fixed-point axes {Homeostasis, Higgs-discrete, Collapse}
produce residuals whose squares obey Pythagoras — i.e. they are orthogonal
in the engine's 14-dim feature space.  If true, the iteration is unitary
(energy-conserving), and the 5-vertex geometry is a real constraint, not a
metaphor.

Test procedure
--------------
1. Fit IE(Z) with 14 features (see magnitude_structure.py).
2. Group features into 4 axes:
     Homeostasis : 1/n, 1/n², fill_frac
     Higgs       : is_noble, block_d, block_f
     Collapse    : bifurc_risk, is_halogen, block_p
     LEAK        : Z-Z_noble, (Z-Z_noble)², block_s
   (intercept + constant absorbed into OBSERVER 5th vertex)
3. Per element compute partial contribution of each axis:
     y_H(Z) = Σ β_i x_i(Z)   for i in Homeostasis
     y_G(Z) = Σ β_i x_i(Z)   for i in Higgs
     y_C(Z) = Σ β_i x_i(Z)   for i in Collapse
     y_L(Z) = Σ β_i x_i(Z)   for i in Leak
4. Residual of each axis relative to the full prediction:
     Δ_H(Z) = y_H(Z) - mean(y_H)      (deviation from that axis's mean)
     similarly Δ_G, Δ_C, Δ_L
5. Check: Σ_Z Δ_H·Δ_C  ≈ 0        (orthogonality)
          Σ_Z Δ_H·Δ_G  ≈ 0
          Σ_Z Δ_C·Δ_G  ≈ 0
   and  Σ_Z Δ_G²  ≈  Σ_Z Δ_H²  +  Σ_Z Δ_C²    (Pythagorean global)
6. Also check LEAK axis: this should capture the brems-like gradient.
"""
from __future__ import annotations
import numpy as np
from magnitude_structure import features, fit, IE_NIST

FEATURE_NAMES = ["intercept", "1/n", "1/n²", "fill_frac", "bifurc_risk",
                 "Z-Z_noble", "(Z-Z_noble)²",
                 "is_noble", "is_alkali", "is_halogen",
                 "block_s", "block_p", "block_d", "block_f"]

AXIS_GROUPS = {
    "Homeostasis": ["1/n", "1/n²", "fill_frac"],
    "Higgs":       ["is_noble", "block_d", "block_f"],
    "Collapse":    ["bifurc_risk", "is_halogen", "block_p"],
    "LEAK":        ["Z-Z_noble", "(Z-Z_noble)²", "block_s"],
    "Observer":    ["intercept", "is_alkali"],
}

def main():
    beta, rms, mape, r2, Zs, y, y_hat = fit()
    X = np.array([features(Z) for Z in Zs])
    # contributions per feature per Z
    C = X * beta[None, :]           # shape (n_Z, 14)

    # axis contributions
    axis_y = {}
    for axis, names in AXIS_GROUPS.items():
        idx = [FEATURE_NAMES.index(n) for n in names]
        axis_y[axis] = C[:, idx].sum(axis=1)

    print("=" * 72)
    print("Per-axis mean contribution to IE [eV]")
    print("=" * 72)
    for axis, yv in axis_y.items():
        print(f"  {axis:<12}  mean={yv.mean():+7.3f}  std={yv.std():6.3f}  "
              f"range=[{yv.min():+.2f}, {yv.max():+.2f}]")

    # residuals = deviation from mean (what each axis adds beyond baseline)
    R = {axis: yv - yv.mean() for axis, yv in axis_y.items()}

    print("\n" + "=" * 72)
    print("Inner products <Δ_i, Δ_j> (should be ≈0 for orthogonal axes)")
    print("=" * 72)
    axes = ["Homeostasis", "Higgs", "Collapse", "LEAK"]
    print(f"{'':<13}" + "".join(f"{a:>13}" for a in axes))
    for a in axes:
        row = f"{a:<13}"
        for b in axes:
            ip = float(np.dot(R[a], R[b]))
            row += f"{ip:>13.3f}"
        print(row)

    # normalised correlation matrix
    print("\n" + "=" * 72)
    print("Correlation matrix ρ(Δ_i, Δ_j)   |ρ| small ⇒ orthogonal")
    print("=" * 72)
    print(f"{'':<13}" + "".join(f"{a:>13}" for a in axes))
    for a in axes:
        row = f"{a:<13}"
        for b in axes:
            if R[a].std() < 1e-9 or R[b].std() < 1e-9:
                rho = 0.0
            else:
                rho = float(np.corrcoef(R[a], R[b])[0, 1])
            row += f"{rho:>13.4f}"
        print(row)

    # Pythagorean test: ||Δ_Higgs||² ≈ ||Δ_H||² + ||Δ_C||² ?
    print("\n" + "=" * 72)
    print("Pythagorean condition on axis norms  (||Δ||² = Σ_Z Δ(Z)²)")
    print("=" * 72)
    nH = float(np.sum(R["Homeostasis"] ** 2))
    nG = float(np.sum(R["Higgs"] ** 2))
    nC = float(np.sum(R["Collapse"] ** 2))
    nL = float(np.sum(R["LEAK"] ** 2))
    print(f"  ||Δ_Homeostasis||²  = {nH:8.3f}")
    print(f"  ||Δ_Higgs||²        = {nG:8.3f}")
    print(f"  ||Δ_Collapse||²     = {nC:8.3f}")
    print(f"  ||Δ_LEAK||²         = {nL:8.3f}")
    print(f"  ||Δ_H||² + ||Δ_C||² = {nH + nC:8.3f}    (claimed = ||Δ_G||²)")
    ratio = (nH + nC) / nG if nG > 0 else float("nan")
    print(f"  ratio (Δ_H²+Δ_C²)/Δ_G²  = {ratio:.3f}   (=1.0 ⇒ Pythagoras exact)")

    # Also: can LEAK be reconstructed from brems + 1/e + W7 constants?
    #   brems intensity ∝ Z² × 1/n  (our feature basis), so β_(1/n) × β_(Z-Z_noble) ratio
    #   should match 1/e × W7
    print("\n" + "=" * 72)
    print("LEAK axis physical check")
    print("=" * 72)
    W7 = np.pi / 20.0
    inv_e = 1.0 / np.e
    leak_ratio = beta[FEATURE_NAMES.index("Z-Z_noble")] / (
        beta[FEATURE_NAMES.index("1/n")] + 1e-9)
    predicted = inv_e * W7
    print(f"  β(Z-Z_noble)/β(1/n)  = {leak_ratio:+.4f}")
    print(f"  (1/e) × W7           = {predicted:+.4f}")
    print(f"  ratio                = {leak_ratio / predicted:+.2f}  "
          f"(=1.0 ⇒ LEAK constant matches user claim)")

if __name__ == "__main__":
    main()
