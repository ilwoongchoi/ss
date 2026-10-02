# Skeletal Core (Single Source-of-Truth)

This file is the **geometry-only core**: invariants + operators that should survive **any** domain swap (bio/cosmo/finance/etc.) and any renderer swap (Python/HTML/WebGL).

If something is only needed to make a visualization stable (camera radius, point size, prime indexing, arbitrary thresholds), it is **not** core.

## 1) Core Constants (Invariants)

Implemented in `geometry_package/absolute_constants.py`.

### Mathematical roots
- `PI`
- `SQRT2`
- `PHI`
- `ALPHA`

### Continuous core
- **Void area:** `W7_EXACT = PI/20`

### Discrete skeleton
- **H2 gap:** `H2_W7 = 1/9`
- **Fraction gates:** `1/64`, `1/32`, `3/32`, `1/16`
- **Anchor:** `GATE_5_32 = 5/32` (nearest discrete point to `W7`)

### Spark (diagonal reset)
- **Angle:** `SPARK_ANGLE_DEG = 1250/9` and `SPARK_ANGLE_RAD = radians(SPARK_ANGLE_DEG)`
- **Leap (derived):** `SPARK_LEAP_DIST = 16 * (5/32) = 2.5` (canonical 16×16 chart)

### Canonical dipole ratios
- `DIPOLE_11_7 = 11/7`
- `DIPOLE_7_11 = 7/11`

## 2) Core Operators (Structures)

### PLP spine (coordinate seam)
Defined in `geometry_package/chart_operators.py`.

- Seam equation (normalized): `x/n_cols + y/n_rows = 1`
- Canonical 16×16 form: `x + y = 16`
- Shader form: `step(16.0, x+y)`

This is a **coordinateization operator**, not a biological overlay. It is what prevents “spark gating” from degenerating into arbitrary `y > threshold` hacks.

### Continuous→Discrete bridge from data (TDA)
Defined in `geometry_package/tda_kappa.py` and consumed by `geometry_package/universal_equation.py`.

Pipeline:
`p_H1` → `kappa_TDA` → gate weights → `coupling_scale(kappa=...)` / `universal_latent(kappa=...)`

## 3) Non-Core (Renderer / Tuning)

These appear in HTML engines but should **not** be promoted into the skeleton:
- `R_PHASE_LOCK`, `IDENTITY_HORIZON`
- Mersenne/prime indexing schemes (e.g., `/127.0`)
- Camera orbit radii, point size formulas, fog coefficients
- Day/night toggles, “dreamfolding” toggles
- Arbitrary refraction thresholds (e.g., `step(5.0, length(p))`)

Use `tools/audit_html_geometry_constants.py` to see which shader constants match the skeleton and which are unmatched (likely renderer-only).
