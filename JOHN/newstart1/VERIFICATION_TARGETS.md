# Verification Targets (user-provided, NOT fit targets)

These are claims the engine should eventually be *tested against* once it
can produce the corresponding observables.  **Do NOT contort code to match
them.**  If the engine — built on its own physics — happens to reproduce
them, that is evidence.  If it doesn't, that is information.

## T1. 5-vertex geometry (2026-04-21)

- Each vertex carries ≥ 2 nodes: one particle-level, one element-level.
  → Engine should expose a per-vertex "particle slot" + "element slot"
    when the 5-vertex decomposition is extracted.
- Top-left vertex: LEAK
  - brems / lensing leak
  - 1/e (inverse natural constant)
  - W7 = π/20
- Right three vertices: HOMEOSTASIS, HIGGS-DISCRETE, COLLAPSE
- 5th vertex: OBSERVER / USER (D3 void, Right/Left Love router)

## T2. "Three ~1.4 constants" triangle (2026-04-21, LOW CONFIDENCE)

User hypothesises a right triangle made from three numbers that all
approximate 1.4:
  γ  = 7/5      = 1.4000          (diatomic adiabatic index, SLOTTING)
  √2 = 1.4142
  e^(1/e) = 1.4447

Claim: the coordinate differences between the 3 vertices of
{γ, √2, e^(1/e)} triangle and the 3 vertices of the original
right-triangle of (Homeostasis, Higgs, Collapse) residuals are in a
specific ratio.  User flagged this as uncertain — DO NOT fit to it.

Future test: once the Homeostasis/Higgs/Collapse residual triangle has
defined coordinates in eV-space (we have the residuals from
`pythagorean_residual_test.py`), compute pairwise distances of the 3
1.4-constants triangle vs the 3 residual norms and report ratios.
Accept/reject purely on data.

## T3. Mandelbrot shell-filling (CONFIRMED 2026-04-21)

Shell filling is a Mandelbrot-style iteration, not a table.
Signatures (i) |proton| contracts at noble gas and (ii) |c_step| peaks at
half-fill both verified in `mandelbrot_shell_iteration.py`.  arg(proton)
passes within 0.16° of 138.88° at Z=46 (Pd, 4d¹⁰).

## T4. LEAK ≟ (1/e) × W7 = 0.0578  (2026-04-21, UNDECIDED)

`pythagorean_residual_test.py` reported β(Z-Z_noble)/β(1/n) = +0.0081 vs
(1/e)×W7 = +0.0578.  Sign matches, magnitude 7× off.  This is a raw
coefficient ratio — NOT a normalised one, so the comparison is invalid as
stated.  Re-test after z-scoring features.

## T5. H ⊥ C orthogonality (CONFIRMED 2026-04-21)

ρ(Homeostasis, Collapse) = -0.065 in the 14-feature IE decomposition.
User claim that Homeostasis and Collapse are the two "linear equations"
producing independent axes is supported.

---

Rule of engagement: code runs on its own physics.  These are *targets*
the engine is allowed to hit or miss; missing is data too.
