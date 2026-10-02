# S5_MASTER_EQUATION

This file derives the **first canonical S^5 master law** in the required layered form:

`S_{n+1} = P_proj ∘ B_sep ∘ O_op ∘ G_gate ∘ T_ratio ∘ C_cont ∘ M_maxwell (S_n)`

Inputs used (core + TOTAL_*):

- `TOTAL_CONSTANT_TABLE.csv`
- `TOTAL_LAYER_ASSIGNMENT.md`
- `TOTAL_OPERATOR_ASSIGNMENT.md`
- `CONST_MAXWELL_F0_LOCK.csv`
- `MAXWELL_MAPPING_LOCK.json`
- `check_maxwell.py`
- `SEAM_GLUE_MAP.csv`

## A) Carrier (explicit choice + justification from current files)

Choose: **S^5 embedded in R^6**.

Justification from current files:

- The required system stack explicitly demands “Level 0 = 5-sphere carrier manifold”, and the current file set already uses real-valued constants and real-valued (pi_1, pi_2) observables (`MAXWELL_MAPPING_LOCK.json`).
- The repository’s operational laws (W7, tau/tension, kappa gates, branch/separatrix, renorm) are scalar/real and are already implemented in real-valued shader and python pipelines.
- Therefore, the minimal explicit carrier consistent with current files is the real embedding:
  - `S^5 = { x ∈ R^6 : ||x||^2 = 1 }`

Optional packaging into `C^3` is allowed as notation (see `S5_STATE_VARIABLES.md`), but **carrier is fixed as R^6** for explicitness.

## B) State (minimal, explicit)

Use:

`S_n = (x_n, A_n, tau_n, kappa_n, m_n, l_n, sigma_n, u_n, rho_n, g_n, f_n, p_n, q_n)`

All variables are kept (included); none are dropped. Domains and constant sources are pinned in `S5_STATE_VARIABLES.md`.

## C) Layered Update Law (explicit)

### 0) Maxwell pre-operator

`S^M_n = M_maxwell(S_n)`

`M_maxwell` is defined explicitly in `MAXWELL_INTEGRATION_IN_S5.md` using:

- `f0_lock = 2.1235e9 Hz` and `Q_lock = 11.85` (`CONST_MAXWELL_F0_LOCK.csv`)
- pi mapping `pi1=log10(f0)`, `pi2=log10(Q)` (`MAXWELL_MAPPING_LOCK.json`)
- cavity axes locks `Rmaj=17/8`, `Rmin=0.223550111...` (`check_maxwell.py`)

Outputs forwarded as scalars inside the next layers:

- `w_res` resonance weight
- `Z_fac` impedance factor
- `Δrho = w_res * RENORMALIZATION_BRIDGE`

### 1) C_cont: W7 / hysteresis continuous law

Inputs (locked constants):

- `W7_EXACT = π/20`
- `w7_raw ≈ 0.15697`
- `LUNAR_CYCLE = 1/28`

Define the continuous carrier advance on S^5 as a tangent update plus re-normalization:

1. Tangent field (minimal, file-supported dependencies only):

`V_cont(x; A, m, l, u, Z_fac) = Z_fac * [ (A - W7_EXACT) * V_A(x) + m * V_m(x) + l * V_l(x) + u * V_u(x) ]`

Where `V_A, V_m, V_l, V_u` are S^5-tangent vector fields (not yet given in closed form in current files; this is the minimal explicit placeholder required to avoid “vague words” while remaining derivable as structure).

2. Carrier update:

`x̃ = x + Δt * V_cont(x; ...)`

3. Projection back to S^5 (explicit):

`x' = x̃ / ||x̃||`

4. Hysteresis area update (explicit scalar relaxation toward `w7_raw` with Moebius torque):

`A' = A + α_A * (w7_raw - A) + β_A * sin(2π * n * LUNAR_CYCLE)`

No new constants are introduced; `α_A, β_A` are not numerically locked in the current files and are therefore left as unresolved scalars (recorded in `UNRESOLVED_FINAL_GAPS.md`).

### 2) T_ratio: discrete/continuous/real ratio law

Inputs (locked):

- `H2_W7 = 1/9`
- `DISCRETE_CLOSURE = 1.0000424`
- `REALITY_TENSION = 1.0100375`
- `mismatch_delta ≈ 3.513e-4`
- `analytic_closure_tension = 9π/(20π^2)` (as recorded)

Define:

`tau_target = analytic_closure_tension`

`tau' = tau + α_tau * (tau_target - tau) + mismatch_delta`

Then apply the two practical calibration coefficients as multiplicative tension factors carried forward:

- `tau'_disc = DISCRETE_CLOSURE * tau'`
- `tau'_real = REALITY_TENSION * tau'`

These appear downstream in gate/operator thresholds as the system’s “tension” scalars.

### 3) G_gate: gate law (fractions + verdict on 5/32)

Inputs (locked gate set):

- `KAPPA_1_16`, `KAPPA_1_32`, `KAPPA_1_64`, `KAPPA_1_128`
- `KAPPA_3_32`
- `GATE_5_32`

Define the canonical gate value family:

`kappa ∈ {1/16, 1/32, 1/64, 1/128, 3/32} ∪ (kappa_eff continuous)`

The codebase provides a dynamic `kappa_eff` and `w_gate` in the operator layer text, but not an explicit formula here; therefore we define gate update as:

`kappa' = GateSelect(kappa, tau'_disc, tau'_real, w_res)`

where `GateSelect` must satisfy the locked thresholds:

- stability center near `1/32`
- warning threshold near `1/64`
- collapse threshold at `1/128`
- compression gate at `3/32`

#### Forced verdict on 5/32 (no ambiguity)

`5/32` is **derivable and is a spark-leap discrete anchor**.

Basis (current files):

- `TOTAL_CONSTANT_TABLE.csv` contains `GATE_5_32 = 5/32` with description:
  - “Discrete anchor point for calculating Spark Leap distance”

Therefore in the master law:

- `5/32` is not a general gate like `1/32`; it is an **anchor used inside the operator law** to compute the Spark Leap distance/phase.

### 4) O_op: operator law

Inputs (locked):

- `SPARK_ANGLE_DEG = 138.88`
- `SPARK_LEAP_DIST = 2.5`
- `WAVELENGTH_6 = 6`
- `DELTA_4 = 4`
- `RENORMALIZATION_BRIDGE ≈ 42.368`

Define compression trigger:

`b_comp = 1{ kappa' >= 3/32 }`

Define spark action (as a map on `(x, l)`):

- if `b_comp = 1` then apply:
  - branch reset: `l' = -l`
  - a discontinuous refraction+leap operator on the carrier:
    - `x' = Spark(x; angle=138.88°, leap=2.5, anchor=5/32)`

Spark is the only place where `5/32` appears: as the discrete anchor for the leap computation.

Tunnel openness update (modulated by impedance factor from Maxwell):

`u' = clamp( u + α_u * (w_res - u) * Z_fac, 0, 1 )`

Renormalization bridge update:

`rho' = rho + w_res * RENORMALIZATION_BRIDGE`

Harmonic stabilizers:

- apply wavelength and delta operators as periodic corrections on the phase variables carried in `(A, tau)`:
  - `A' := A' + ε6 * sin(2π * A' / 6)`
  - `tau' := tau' + ε4 * sin(2π * tau' / 4)`

`ε6, ε4` are not numerically locked in current files; they are recorded as unresolved scalars.

### 5) B_sep: branch / separatrix / attractor law

Inputs (locked):

- attractors:
  - `LEFT_CORTISOL_R/Q0 = (0.1121475, 0.965)`
  - `RIGHT_CORTISOL_R/Q0 = (0.111900, 0.974879)`
- separatrix exists as boundary

Define separatrix side `sigma'` and basin update rule:

`(sigma', l') = B_sep( pi_n, tau'_real, kappa', l, sigma )`

Constraint: `sigma'` is a binary side label, and basin membership is decided by which attractor the projected coordinates are closer to.

Exact distance metric in pi-space is not explicitly defined in the current file set; recorded as missing term in `UNRESOLVED_FINAL_GAPS.md`.

### 6) P_proj: projected 13-patch / 128-grid skeleton

`(p_{n+1}, q_{n+1}, pi_{n+1}, e_{n+1}) = P_proj(S_{n+1}^{preproj})`

Projection terms and explicit missing terms are listed in `PATCH_AND_GRID_FROM_S5.md`.

### 7) Gluing (final constraint only)

After `P_proj`, enforce closure constraints using `SEAM_GLUE_MAP.csv` as a projection-only check:

- intrinsic closure bound: 2 components
- extended closure (after mediator patch `X`): 1 component
- barrier `(G,B)` forbidden intrinsically

This is specified in `GLUING_AS_PROJECTION_CONSTRAINT.md`.

## D) Full Compositional Master Law (final)

Let:

`S_{n+1} = P_proj( B_sep( O_op( G_gate( T_ratio( C_cont( M_maxwell(S_n) ) ) ) ) ) )`

with:

- `M_maxwell` explicit in `MAXWELL_INTEGRATION_IN_S5.md`
- `C_cont, T_ratio, G_gate, O_op, B_sep, P_proj` as defined above, with missing sub-terms enumerated in `UNRESOLVED_FINAL_GAPS.md`
- gluing imposed only as a final constraint on the projected skeleton outputs

