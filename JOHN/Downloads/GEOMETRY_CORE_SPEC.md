# GEOMETRY CORE SPEC (Regime-1)

## 1) Overview
- Regime-1 is the geometry/physics core only.
- Core tension is the collision between:
  - Continuous reservoir: `W7 = π/20`
  - Discrete gates: `H2 = 1/9`, `kappa = {1/64, 1/32, 1/16}`, and `3/32` compression gate.
- `128` nodes are treated as an emergent scalar field from interference (`Reality_Tension` vs `LATTICE_3_32`) via `get_emergent_128_nodes`.
- Regime-1 never uses biology/social labels and never redefines overlay semantics.

## 2) Constants (single source)
Primary source: `geometry_package/absolute_constants.py`

- **Topological and area locks**
  - `H2_W7 = 1/9`
  - `W7_AREA = π/20`
  - `BETTI_0, BETTI_5, BETTI_7, BETTI_11`
- **Kappa ladder**
  - `KAPPA_TDA_MIN = 1/64`
  - `KAPPA_TDA_MID = 1/32` (anchor)
  - `KAPPA_TDA_MAX = 1/16`
  - `LATTICE_3_32 = 3/32`
- **SH band**
  - `CALIBRATED_SH_R_STAR`, `CALIBRATED_SH_Q0_STAR`
  - `CALIBRATED_SIGMA_L`, `CALIBRATED_SIGMA_R`
  - `CALIBRATED_Q0_MIN/MAX`
  - `SH_R_BAND_MIN/MAX`, `SH_Q0_MIN/MAX`
- **Global dynamics/closure**
  - `TUNNEL_TENSION`, `RENORMALIZATION_BRIDGE`, `MANIFOLD_CLOSURE`
- **Maxwell cavity**
  - `MAXWELL_R_MAJOR`, `MAXWELL_R_MINOR`, `MAXWELL_Q_FACTOR`
- **Temporal**
  - `LUNAR_CYCLE = 1/28`

## 3) Operators (canonical API)
Primary source: `geometry_package/universal_equation.py` and `geometry_package/chart_operators.py`

- `kappa_tda(p)`  
  Piecewise mapping from persistence to kappa gate (`1/64 -> 1/32 -> 1/16`).
- `in_sh_band(r, q0)`  
  Membership in calibrated SH band.
- `kappa_eff(r, q0, use_lookup=True)`  
  In-band snap to `1/32`; out-band from nearest-cell persistence lookup.
- `w_gate(r, q0, alpha=GATE_ALPHA, eps_kappa=GATE_EPS_KAPPA)`  
  Unified gate weight: `w_atlas^alpha * w_kappa^(1-alpha)`.
- `get_macro_micro_time(t_macro)`  
  Macro/micro conversion by `LUNAR_CYCLE`.
- `get_emergent_128_nodes(t_macro, resolution=128)`  
  Interference-based emergent scalar field.
- `PLP_SPINE` (16x16 seam)
  - `plp_spine_value(x,y,n_rows=16,n_cols=16)`
  - `plp_spine_gate(...)`
  - seam condition equivalent: `x/n_cols + y/n_rows = 1`.

## 4) 2D Shader Interface

### Inputs
- Coordinate form A: `(r, q0)`  
- Coordinate form B: `(x, y)` on `16x16` chart
- Required fields:
  - `w_gate`
  - `kappa_eff`
  - `in_sh_band`
  - `plp_spine` value/gate

### Outputs
- `height_scalar`: scalar field composed only from Regime-1 operators/constants
- `color_scalar`: normalized scalar derived from `height_scalar`

### Hard constraints
- No D3 naming/logic in core shader path.
- No biology/social labels.
- No arbitrary thresholds outside Regime-1 constants.

## 5) 3D Renderer Interface

### Required primitives
- Maxwell Torus (`MAXWELL_R_MAJOR`, `MAXWELL_R_MINOR`)
- Void Sphere (`R_void = sqrt(W7_AREA / π)`)
- Discrete shells (`1/64`, `1/32`, `1/16`, `3/32`)
- Betti rings (`polygon_ring(5)`, `polygon_ring(11)`)
- 128-node funnel (built from emergent node field)

### Naming constraints
- Use geometry-only labels:
  - `Zone-1`, `Zone-2`
  - `Betti-5 Ring`, `Betti-11 Ring`
  - `Maxwell Cavity`, `Void Core`

## 6) D3/epoch separation rule
- Regime-1 assumes `D3_enforcement(E) ≡ 0` for core runs.
- Future/discrete branch handling in Regime-1 must treat D3 terms as non-existent.
- Any D3 interpretation or mode classification is delegated to Regime-2 overlay only.
