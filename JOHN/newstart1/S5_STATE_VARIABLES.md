# S5_STATE_VARIABLES

Carrier choice (explicit): **S^5 embedded in R^6**.

- Carrier coordinate: `x ∈ R^6`, constrained by `||x||^2 = 1`.
- Optional complex packaging (notation only, no extra degrees): define
  - `z = (z1, z2, z3) ∈ C^3`
  - `z1 = x1 + i x2`, `z2 = x3 + i x4`, `z3 = x5 + i x6`
  - Then `||x||^2 = 1` is equivalent to `|z1|^2 + |z2|^2 + |z3|^2 = 1`.

State at step `n`:

`S_n = (x_n, A_n, tau_n, kappa_n, m_n, l_n, sigma_n, u_n, rho_n, g_n, f_n, p_n, q_n)`

Mandatory variables (include/reject verdict from current files):

- `z` (complex carrier state): **included as packaging of `x`** (no new physics), because the system needs an explicit S^5 carrier; complex form is available via the R^6 embedding.
- `A` (continuous area / W7-hysteresis state): **included**. Source: `TOTAL_CONSTANT_TABLE.csv` has `W7_EXACT = π/20` and `w7 raw / night_hysteresis_area ≈ 0.15697`.
- `tau` (ratio/tension): **included**. Source: `TOTAL_CONSTANT_TABLE.csv` has `H2_W7 = 1/9`, `DISCRETE_CLOSURE = 1.0000424`, `REALITY_TENSION = 1.0100375`, `mismatch_delta ≈ 3.513e-4`, `analytic_closure_tension = 9π/(20π^2)`.
- `kappa` (gate): **included**. Source: `TOTAL_CONSTANT_TABLE.csv` has `KAPPA_1_16`, `KAPPA_1_32`, `KAPPA_1_64`, `KAPPA_1_128`, `KAPPA_3_32`, `LUNAR_CYCLE = 1/28`, `GATE_5_32`.
- `m` (hysteresis memory): **included**. Source: W7 raw hysteresis is explicit, and `TOTAL_OPERATOR_ASSIGNMENT.md` defines hysteresis as a system capacitor driven by global twist.
- `l` (branch leg ascending/descending): **included**. Source: `TOTAL_CONSTANT_TABLE.csv` includes `Ascending Branch`, `Descending Branch`; `TOTAL_OPERATOR_ASSIGNMENT.md` describes branch reset via Spark.
- `sigma` (separatrix side): **included**. Source: `TOTAL_LAYER_ASSIGNMENT.md` includes Separatrix under Level 5.
- `u` (tunnel state): **included**. Source: tunnel/spark appears in the canonical law path used in `terrain.html` / `geometry_truth_probe_shader.html` and the operator layer text treats tunnel-like gating via kappa_eff/w_gate.
- `rho` (renorm state): **included**. Source: `TOTAL_CONSTANT_TABLE.csv` includes `RENORMALIZATION_BRIDGE ~ 42.368`; `TOTAL_OPERATOR_ASSIGNMENT.md` defines renorm triggering and recovery.
- `g` (GABA-C / receptor anchor): **included**. Source: `TOTAL_CONSTANT_TABLE.csv` includes `GABA_C_V_APEX = 0.140488`.
- `f` (fake-3D shell state): **included**. Source: `TOTAL_LAYER_ASSIGNMENT.md` includes “Right Cortisol Fake 3D”.
- `p` (projected patch index): **included**. Source: `TOTAL_CONSTANT_TABLE.csv` and atlas docs define “13-patch skeleton” as Level 7 projection output.
- `q` (projected grid coordinate): **included**. Source: `TOTAL_CONSTANT_TABLE.csv` defines “128-Grid” and grid offsets; Level 7 projection output.

Typed domains:

- `x_n ∈ S^5 ⊂ R^6`
- `A_n ∈ R` (W7 area/hysteresis scalar)
- `tau_n ∈ R` (tension/ratio scalar)
- `kappa_n ∈ [0, 1]` (gate fraction; canonically around 1/32 with bounds)
- `m_n ∈ [0, 1]` (memory weight)
- `l_n ∈ {+1, -1}` (ascending / descending)
- `sigma_n ∈ {L, R}` (separatrix side)
- `u_n ∈ [0, 1]` (tunnel openness)
- `rho_n ∈ R` (renorm step or bridge magnitude)
- `g_n ∈ R` (receptor anchor scalar; includes GABA-C apex constant)
- `f_n ∈ [0, 1]` (fake-depth shell strength)
- `p_n ∈ {A,B,C,D,10,11,12,13,14,F,F',G,X}` for 13-patch projection outputs (see `SEAM_GLUE_MAP.csv`)
- `q_n ∈ {0..127}×{0..127}` (128-grid coordinate; exact mapping terms below in `PATCH_AND_GRID_FROM_S5.md`)

Locked numeric constants used by the master law layers (as currently present in files):

- `W7_EXACT = π/20 ≈ 0.1570796327`
- `w7_raw ≈ 0.15697` (night hysteresis area)
- `H2_W7 = 1/9`
- `DISCRETE_CLOSURE = 1.0000424`
- `REALITY_TENSION = 1.0100375`
- `mismatch_delta ≈ 3.513e-4`
- `KAPPA_1_32 = 1/32 = 0.03125`
- `KAPPA_1_128 = 1/128 = 0.0078125`
- `GATE_5_32 = 5/32 = 0.15625` (verdict forced in `S5_MASTER_EQUATION.md`)
- `SPARK_ANGLE_DEG = 138.88`, `SPARK_LEAP_DIST = 2.5`
- `LUNAR_CYCLE = 1/28`
- `WAVELENGTH_6 = 6`, `DELTA_4 = 4`
- `RENORMALIZATION_BRIDGE ≈ 42.368`
- `GABA_C_V_APEX = 0.140488`

