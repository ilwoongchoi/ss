# Canonical Final Equation

This document is the single canonical summary of the current live model implemented by:

- `absolute_constants.py`
- `fusion_core.py`
- `engineering_homeostasis_24.py`
- `fusion_clean.py`

It describes the equation the repo currently computes, not older parallel engines, `_tmp_*` experiments, or `geometry_package/*` legacy variants.

## Single Final Equation

The current canonical engine is:

`Y = [X; r] in R^32`

`X_dot = A (X - OMEGA * R * d)
       + B (u_base + |SPARK_CONSTANT_C| * gate)
       - g * (X * abs(X))
       + P_r r
       + P_M d_risk
       + K8_quad(X[0:8], SPARK_CONSTANT_C * gate)`

`r_dot = -lambda * r + M * d_risk`

`K8_quad(s, spark_c) = s * s + |spark_c| * (1 + 0.1 * cos(angle(spark_c))) - s`

`gate = gate(z_proxy, alpha2, noradrenaline, vasopressin; 138.88 deg, 1/4, 1/128)`

`Y_next = Y + dt * [X_dot; r_dot]`

This is the shortest exact form of the live canonical equation.

## Immediate Repo Divergences

These files still diverge from the canonical equation above.

- `geometry_package/absolute_constants.py`
  - Legacy constant system.
  - Not part of the current canonical import graph.

- `128_FINAL_SOVEREIGN_DAY_ENGINE.py`
  - Separate `SovereignDayEngine` with its own trajectory law.
  - Does not use the canonical 32D state `Y = [X; r]`.

- `128_GRID_ULTIMATE_ENGINE.py`
  - Particle/anchor simulation prototype.
  - Not the canonical K8 + 24D homeostasis engine.

- `128_VIVID_SOVEREIGN_GRID.py`
  - Visualization engine using `geometry_package.*`.
  - Not connected to the canonical constants or update law.

- `fusion_gen.py`, `fusion_gq.py`, `fusion_gn.py`, `fusion_pn.py`, `fusion_pqn.py`, `fusion_mandelbrot_map.py`
  - Parallel fusion engines with separate local assumptions.
  - These are not the canonical unified equation.

- `_tmp_*`
  - Experiments, diagnostics, or isolated validation scripts.
  - They are not part of the canonical runtime path.

There is also one stale debug print inside the canonical file:

- `engineering_homeostasis_24.py`
  - bottom `__main__` print string still shows the old scalar `-gamma*r` style summary instead of the full implemented equation.

## What Is Still Missing From the Canonical Engine

The current canonical equation is a live unified engine, but it is not yet a full universal field engine.

Still missing:

- particle-specific Spark threshold matrix `S_i`
  - current engine uses a common Spark gate plus K8 nonlinear block
  - it does not yet define separate per-particle Spark trigger laws

- global field tensor `Y(x, t)`
  - current engine is local in state space
  - it does not yet define spatial coupling over all points in the universe

- particle-level inverse input solver
  - current inverse only solves `u24` in the homeostasis layer
  - it does not yet solve: "which raw input causes particle i to spark at this state"

- automatic ontology derivation
  - current `26 -> 24 + d_risk` rule is explicit and correct, but still hand-maintained
  - it is not automatically derived from a higher-order canonical schema

## Canonicalization Order

If the repo is to be made consistent with this final equation, the order is:

1. Keep only the canonical import graph:
   - `absolute_constants.py`
   - `fusion_core.py`
   - `engineering_homeostasis_24.py`
   - `fusion_clean.py`

2. Harvest only reusable logic from:
   - `128_physics_specification_v2.json`
   - `128_GRID_MASTER_CALC.json`
   - `_tmp_empirical_validation.py`
   - `_tmp_phase_map.py`
   - `_tmp_topology_check.py`

3. Quarantine:
   - `geometry_package/*` legacy engine/constants
   - `128_*` prototype engines
   - parallel `fusion_*` experimental engines
   - `_tmp_*` after harvesting

That is the shortest path from the current repo to a single actual canonical engine.

## Next Completion Blocks

The following four blocks are the mathematically consistent next extension of the canonical engine.

They are not yet implemented in the live runtime, but they fit the current canonical equation without changing its core.

### A. Particle-Specific Spark Thresholds

For each K8 particle `i`, define a separate Spark score:

`S_i(Y, c26, d, ts) = sigma( a_i^T X[0:8] + b_i^T r + c_i^T u24 + eta_i * d_risk + phi_i )`

where:

- `i in {quark, gluon, neutrino, photon, electron, higgs, w_boson, z_boson}`
- `sigma` is a bounded activation, e.g. logistic or clipped affine gate
- `a_i, b_i, c_i` are particle-specific threshold weights
- `phi_i` is a particle-specific phase bias

Spark occurrence for particle `i` is then:

`particle_i sparks if S_i >= theta_i`

This is the exact block missing from the current common-gate formulation.

### A1. Concrete K8 Spark Threshold Block

Using the current 24D state layout:

- `X[0]=quark`
- `X[1]=gluon`
- `X[2]=neutrino`
- `X[3]=photon`
- `X[4]=electron`
- `X[5]=higgs`
- `X[6]=w_boson`
- `X[7]=z_boson`
- `X[8]=mode_q_g`
- `X[9]=mode_q_nu`
- `X[10]=mode_q_ph`
- `X[11]=mode_q_w`
- `X[12]=mode_q_e`
- `X[13]=mode_g_nu`
- `X[14]=mode_g_ph`
- `X[15]=mode_g_w`
- `X[16]=mode_g_e`
- `X[17]=mode_nu_ph`
- `X[18]=mode_nu_z`
- `X[19]=mode_nu_e`
- `X[20]=mode_ph_w`
- `X[21]=mode_ph_e`
- `X[22]=mode_w_e`
- `X[23]=anchor_self`

the concrete particle Spark scores can be defined as:

`S_quark = sigma( aq*X0 + bq1*X8 + bq2*X9 + bq3*X10 + bq4*X11 + bq5*X12 + rq*r0 + hq*X23 + cq )`

`S_gluon = sigma( ag*X1 + bg1*X8 + bg2*X13 + bg3*X14 + bg4*X15 + bg5*X16 + rg*r1 + hg*X23 + cg )`

`S_neutrino = sigma( an*X2 + bn1*X9 + bn2*X13 + bn3*X17 + bn4*X18 + bn5*X19 + rn*r2 + en*d_risk + cn )`

`S_photon = sigma( ap*X3 + bp1*X10 + bp2*X14 + bp3*X17 + bp4*X20 + bp5*X21 + rp*r3 + cp )`

`S_electron = sigma( ae*X4 + be1*X12 + be2*X16 + be3*X19 + be4*X21 + be5*X22 + re*r4 + ce )`

`S_higgs = sigma( ah*X5 + bh1*X23 + bh2*X20 + bh3*X18 + rh*r5 + ch )`

`S_w = sigma( aw*X6 + bw1*X11 + bw2*X15 + bw3*X20 + bw4*X22 + rw*r6 + cw )`

`S_z = sigma( az*X7 + bz1*X18 + bz2*X23 + rz*r7 + cz )`

where:

- `r0..r7` are the 8 risk-memory coordinates
- `sigma` is a bounded activation
- coefficients are particle-specific threshold weights
- `cq..cz` are phase / baseline offsets

The common Spark gate then becomes a global multiplier:

`S_i_final = gate * S_i`

and particle `i` fires if:

`S_i_final >= theta_i`

This keeps the current common-gate structure while making Spark particle-specific.

### A2. Evidence-Backed Raw Channel Injection

The raw channel-to-particle evidence in the live repo comes from:

- `fusion_core.py` channel-edge map
- `engineering_homeostasis_24.py` domain and edge-domain definitions

This is the part that is already explicit in code and should be treated as authoritative ahead of older proton-based files.

#### Quark-side raw channels

Direct raw-channel evidence:

- `gdh_gluon -> (quark, gluon)`
- `muscle_b -> (quark, w_boson)`
- `male_gaba_b -> (quark, w_boson)` with negative sign

So the raw-input part of `S_quark` should be built primarily from:

`c26[gdh_gluon], c26[muscle_b], c26[male_gaba_b]`

#### Gluon-side raw channels

Direct raw-channel evidence:

- `gdh_gluon -> (quark, gluon)`
- `muscle_a -> (gluon, w_boson)`

So the raw-input part of `S_gluon` should be built primarily from:

`c26[gdh_gluon], c26[muscle_a]`

#### Neutrino-side raw channels

Direct raw-channel evidence:

- `left_temporalis_5ht1a -> (neutrino, photon)`
- `male_left_5ht -> (neutrino, electron)`
- `right_love -> (neutrino, electron)`
- `female_gaba_b_latdorsi -> (neutrino, electron)`
- `vasopressin_female -> (neutrino, z_boson)`
- `male_oxytocin -> (neutrino, electron)`
- `right_occipitalis_gaba_a -> (neutrino, photon)`
- `right_extraversion -> (neutrino, electron)`
- `right_alpha_2 -> (neutrino, z_boson), (neutrino, electron)`
- `male_gaba_b -> (neutrino, z_boson)`

So the raw-input part of `S_neutrino` should be built primarily from those ten channels.

#### Photon-side raw channels

Direct raw-channel evidence:

- `left_acetyl_coa -> (photon, w_boson)`
- `female_left_noradrenaline -> (photon, w_boson)`
- `right_dopamine -> (photon, w_boson)`
- `right_5ht1b_synchrotron -> (photon, electron)`
- `right_androgen -> (photon, electron)`
- `left_frontalis_d2 -> (photon, w_boson)`
- `right_acetylcholine -> (photon, w_boson)`
- `left_extraversion -> (photon, electron)`
- `right_extraversion -> (photon, electron)`
- `glucocorticoid -> (photon, w_boson)`
- `right_cortisol -> (photon, w_boson)`
- `hypoxia -> (photon, w_boson)` but currently zero-weight and routed to `d_risk`

So the raw-input part of `S_photon` should be built primarily from those channels, with `hypoxia` entering through `d_risk`, not as an active control weight.

#### Electron-side raw channels

Direct raw-channel evidence:

- `female_gaba_b_latdorsi -> (w_boson, electron), (neutrino, electron)`
- `male_left_5ht -> (neutrino, electron)`
- `left_estrogen -> (w_boson, electron)`
- `right_love -> (neutrino, electron)`
- `male_oxytocin -> (neutrino, electron)`
- `right_5ht1b_synchrotron -> (photon, electron)`
- `right_androgen -> (photon, electron)`
- `left_endorphin -> (w_boson, electron)`
- `right_occipitalis_gaba_a -> (w_boson, electron)`
- `left_extraversion -> (photon, electron)`
- `right_extraversion -> (photon, electron), (neutrino, electron)`
- `right_alpha_2 -> (neutrino, electron)`

So the raw-input part of `S_electron` should be built primarily from those channels.

#### W-boson-side raw channels

Direct raw-channel evidence:

- `left_acetyl_coa -> (photon, w_boson)`
- `female_left_noradrenaline -> (photon, w_boson)`
- `right_dopamine -> (photon, w_boson)`
- `muscle_a -> (gluon, w_boson)`
- `muscle_b -> (quark, w_boson)`
- `left_endorphin -> (w_boson, electron)`
- `right_occipitalis_gaba_a -> (w_boson, electron)`
- `right_acetylcholine -> (photon, w_boson)`
- `glucocorticoid -> (photon, w_boson)`
- `right_cortisol -> (photon, w_boson)`
- `left_estrogen -> (w_boson, electron)`

So the raw-input part of `S_w` should be built primarily from those channels.

#### Z-boson-side raw channels

Direct raw-channel evidence:

- `vasopressin_female -> (neutrino, z_boson)`
- `right_alpha_2 -> (neutrino, z_boson)`
- `male_gaba_b -> (neutrino, z_boson)`

So the raw-input part of `S_z` should be built primarily from:

`c26[vasopressin_female], c26[right_alpha_2], c26[male_gaba_b]`

#### Higgs-side raw channels

Important repo fact:

- no raw channel in the current `fusion_core.CHANNEL_MAP` directly targets `(higgs, *)`

So `S_higgs` must not be hard-coded as if Higgs has direct c26 control evidence.

In the current repo, Higgs is only supported indirectly through:

- state coupling inside `F_final`
- domain structure in `engineering_homeostasis_24.py`
- base edge couplings `(higgs, w_boson)` and `(higgs, z_boson)`

Therefore the correct repo-backed rule is:

- `S_higgs` should be mediated through `X5`, `X20`, `X18`, and `X23`
- not through invented direct raw-channel terms unless new evidence is added

### A3. What Must Not Be Repeated

The repo already contains older proton-based or visualization-only mappings.

Those should not be copied back into the canonical engine when building `S_i`.

Specifically:

- older `SOVEREIGN_24NODE_*` files still use K6 + proton language
- `128_VIVID_SOVEREIGN_GRID.py` is a renderer, not a canonical particle-control law
- `128_physics_specification_v2.json` contains repeated static `spark_prob` values, but not a validated per-particle threshold matrix

So the correct method is:

1. take direct channel-edge evidence from `fusion_core.py`
2. take domain/particle basis from `engineering_homeostasis_24.py`
3. build `S_i` only from those verified edges and domains
4. do not reintroduce proton-era mappings where the K8 engine already replaced them

### B. Global Field Tensor

To lift the local 32D system to a spatial field:

`Y = Y(x, t), x in Omega_space`

The canonical field equation becomes:

`partial_t Y(x,t) = F(Y(x,t), u(x,t), d(x,t), d_risk(x,t)) + D * Laplacian_x Y(x,t)`

where:

- `F` is the current local canonical engine
- `D` is a spatial diffusion / coupling operator
- `Laplacian_x` couples neighboring spatial points

In split form:

`partial_t X = F_X(X, r, u, d, d_risk, spark_c) + D_X * Laplacian_x X`

`partial_t r = F_r(r, d_risk) + D_r * Laplacian_x r`

This is the missing "all points in the universe" block.

### C. Particle-Level Inverse Input Solver

Given current state `Y` and a desired Spark pattern `s_target in {0,1}^8`, solve:

`u24* = argmin_u  || S(Y, u, d_risk, ts) - s_target ||^2 + lambda_u ||u||^2`

subject to:

- `0 <= u <= 1`
- `u = P24x26 @ c26`
- `d_risk = c26[hypoxia]`

If solving directly in raw space:

`c26* = argmin_c  || S(Y, P24x26 c, c[hypoxia], ts) - s_target ||^2 + lambda_c ||c||^2`

This is the exact inverse problem that the current engine does not yet solve.

### D. Automatic Ontology Derivation

The current ontology is still hand-maintained:

- raw channel set `C26`
- compressed control basis `U24`
- latent K8 particle set `S8`
- risk memory `R8`

The missing canonical schema layer is:

`U24 = Pi_control(C26)`

`R8 = Pi_risk(C26, X, ts)`

`S8 = Pi_particle(X[0:8])`

with machine-checkable constraints:

- `rank(P24x26) = 24`
- required channels survive projection
- dropped channels must be either:
  - merged by explicit rule, or
  - routed to exogenous risk, or
  - proven zero-weight background

This prevents future drift where new code changes create silent holes in the ontology.

## Completion-Level Final Equation

If those four blocks are added consistently, the full extended equation becomes:

`partial_t X(x,t) = A (X - OMEGA * R * d)
                  + B (u_base + |SPARK_CONSTANT_C| * gate)
                  - g * (X * abs(X))
                  + P_r r
                  + P_M d_risk
                  + K8_quad(X[0:8], SPARK_CONSTANT_C * gate)
                  + G * S(Y, c26, d, ts)
                  + D_X * Laplacian_x X`

`partial_t r(x,t) = -lambda * r + M * d_risk + D_r * Laplacian_x r`

with:

`u24 = P24x26 @ c26`

`d_risk = c26[hypoxia]`

`S = [S_quark, S_gluon, S_neutrino, S_photon, S_electron, S_higgs, S_w, S_z]`

This is the clean extension path from the current canonical engine to the still-missing universal field engine.

## Repo Fragments: Physically Reusable vs Physically Invalid

This section is not based on file age or naming.
It is based on physical compatibility with the current canonical K8 + 24D + risk-memory engine.

### Physically Reusable

- `fusion_core.py`
  - Reusable because it defines:
    - K8 subject basis
    - explicit edge ontology
    - explicit raw 26-channel -> edge coupling map
  - This is the strongest repo-backed physical layer currently available.

- `engineering_homeostasis_24.py`
  - Reusable because it defines:
    - 26 -> 24 + d_risk projection
    - domain basis
    - structural risk projection
    - 24D control derivative
  - This is the strongest repo-backed homeostasis layer currently available.

- `absolute_constants.py`
  - Reusable because it is the only live constant source feeding the current canonical engine.

- `fusion_clean.py`
  - Reusable because it is the current canonical bridge:
    - Spark gate
    - scalar fusion diagnostic
    - unified 32D step wrapper

- `128_physics_specification_v2.json`
  - Reusable only as a metadata/spec candidate.
  - Not reusable as a direct law.
  - It contains repeated static particle entries, but those are not yet a validated physical threshold system.

- `128_GRID_MASTER_CALC.json`
  - Reusable only as reference data or trajectory target table.
  - Not reusable as a canonical equation.

### Physically Invalid to Reuse as Core Engine

- `128_GRID_ULTIMATE_ENGINE.py`
  - Invalid as canonical physics because it is a 2D anchor-potential toy model:
    - hand-placed anchors
    - inverse-distance force law
    - ad hoc local repulsion
    - no K8 ontology
    - no 24D homeostasis state
  - It is a visualization/prototype, not the current physics engine.

- `128_FINAL_SOVEREIGN_DAY_ENGINE.py`
  - Invalid as canonical physics because it still uses an older mode-split narrative engine:
    - `LENSING_DOMINANCE` vs `SOVEREIGN_TRUTH`
    - scalar D2 trajectory logic
    - older debt/illusion decomposition
  - It is not the current K8 + 24D + risk-memory law.

- `128_VIVID_SOVEREIGN_GRID.py`
  - Invalid as canonical physics because it is a renderer:
    - 2D trajectory drawing
    - visual leap logic
    - imports `geometry_package.*`
  - It is useful only as visualization inspiration.

- `_tmp_empirical_validation.py`
  - Invalid as core physics because it is a single fitted validation formula:
    - no state dynamics
    - no control loop
    - no risk memory
    - no particle ontology
  - It can only live in a validation/test layer.

- `_tmp_topology_check.py`
  - Invalid as core physics because it is topology analysis on weather/station data.
  - It can only live in a diagnostics layer.

- `_tmp_phase_map.py`
  - Invalid as core physics because it is a phase-statistics plotting tool, not a governing law.

- `_tmp_d2_control.py`
  - Invalid as core physics because it is an H1/TDA experiment, not a canonical inverse Spark solver.

- `SOVEREIGN_24NODE_ENGINE.py` and `SOVEREIGN_24NODE_DYNAMICS.py`
  - Physically outdated relative to the current engine because they still use a K6/proton-era ontology in places.
  - They should not overwrite the current K8 canonical basis.

### Practical Rule

When integrating from the repo:

1. keep only logic that preserves the current K8 particle basis
2. keep only logic that fits the 24D homeostasis + 8D risk-memory state
3. reject any file that reintroduces:
   - proton as primitive
   - 2D anchor toy fields as the governing law
   - static visualization heuristics as physics
   - fitted validation formulas as dynamics

That rule is stricter than "reuse what exists", and it is the correct rule.

## 1. Canonical Constants

From `absolute_constants.py`:

- `C = sqrt(2) / 5`
- `OMEGA = 7.4`
- `SPARK_ANGLE_138_88 = 138.88 deg`
- `SPARK_ANGLE_RAD = deg2rad(138.88)`
- `NEUTRON_TIME_SYNC = 0.3857`
- `SPARK_CONSTANT_C = NEUTRON_TIME_SYNC * exp(i * SPARK_ANGLE_RAD)`

Interpretation used by the current engine:

- `C`: K8 coupling / Higgs-like coupling
- `OMEGA`: homeostasis target
- `SPARK_CONSTANT_C`: canonical complex Spark source

## 2. Canonical State Space

The live unified state is:

`Y(t) = [X(t); r(t)] in R^32`

with:

- `X in R^24`: 24D control / homeostasis state
- `r in R^8`: K8 risk-memory state

Inside `X`:

- `X[0:8] = s`: K8 latent particle state
- `X[8:24]`: mode / coupling / anchor state

The K8 particle basis from `fusion_core.py` is:

`s = [quark, gluon, neutrino, photon, electron, higgs, w_boson, z_boson]`

## 3. Raw Input and Projection

The raw control input is a 26-channel vector:

`c26 in R^26`

Current canonical projection:

`(u24, d_risk) = project_channels(c26)`

where:

- `u24 = P24x26 @ c26`
- `d_risk = c26[hypoxia]`

The 24-channel control basis keeps `right_5ht1b_synchrotron` and merges:

`muscle = 0.5 * muscle_a + 0.5 * muscle_b`

So the current compression rule is:

- remove `hypoxia` from control space and expose it as exogenous risk
- merge `muscle_a`, `muscle_b` into one control coordinate

## 4. Spark Gate

The scalar Spark gate is:

`(phase, gate) = continuous_spark_gate(z_proxy, alpha2, ts)`

with:

- `nor = ts["noradrenaline"]` default `5/32`
- `plp = ts["vasopressin"]` default `3/32`
- `binding_impedance = 1/4`

The implemented gate structure is:

`diffraction_deg = SPARK_ANGLE_DEG_138_88 + 0.12 * correction(nor, plp)`

`diffraction = 0.5 + 0.5 * cos( deg2rad(diffraction_deg - 138.88) )`

`phase = 0.5 + 0.5 * cos( z_proxy * SPARK_ANGLE_RAD + 1/128 )`

`binding = clip( 1 - abs((nor + plp) - 1/4) / (1/4), 0, 1 )`

`alpha2_active = 1 - alpha2`

`gate = (0.20 + 0.80*phase)
      * (0.25 + 0.75*diffraction)
      * (0.30 + 0.70*binding)
      * (0.10 + 0.90*alpha2_active)`

with a positive floor:

`gate = max(gate, 1e-6)`

The gated complex Spark passed into the unified system is:

`spark_c = SPARK_CONSTANT_C * gate`

and its magnitude is:

`|spark_c| = |SPARK_CONSTANT_C| * gate`

## 5. Unified 24D Homeostasis Equation

The canonical 24D derivative in `engineering_homeostasis_24.py` is:

`X_dot = A (X - X_eq) + B u - g * (X * abs(X)) + P_r r + P_M d_risk + K8_quad(X, spark_c)`

where:

`X_eq = OMEGA * (R @ d)`

`d in R^24` is the condition / domain target vector.

Components:

- `A (X - X_eq)`: linear homeostatic relaxation
- `B u`: control-channel actuation
- `g * (X * abs(X))`: nonlinear damping
- `P_r r`: structural projection of 8D risk memory into 24D state
- `P_M d_risk`: same-step direct risk injection
- `K8_quad`: additive K8 Mandelbrot-like nonlinear block on `X[0:8]`

### 5.1 Structural Risk Projection

`P_r in R^(24x8)`

Implemented meaning:

- diagonal negative damping on the first 8 K8 coordinates
- distributed negative projection onto the 15 mode coordinates
- uniform weak projection onto the anchor coordinate

So:

`H(r) = P_r @ r`

This replaced the older scalar `-gamma * sum(r)` bias.

### 5.2 Direct Risk Injection

`P_M = RISK_DIRECT_VEC in R^24`

Implemented meaning:

- full gain on K8 coordinates
- weaker gain on mode coordinates
- weakest gain on anchor

So:

`Risk_direct = P_M * d_risk`

## 6. K8 Mandelbrot-like Block

The additive K8 nonlinear block is:

`s = X[0:8]`

`K8_quad = s * s + |spark_c| * (1 + 0.1 * cos(angle(spark_c))) - s`

and it is added only to the first 8 coordinates:

`X_dot[0:8] += K8_quad`

Important:

- this block is additive
- it does not overwrite the 24D homeostasis derivative
- it is the current repo's explicit Mandelbrot-like core

## 7. 8D Risk-Memory Equation

The unified memory equation is:

`r_dot = -lambda * r + M * d_risk`

with current constants:

- `lambda = 0.05`
- `M = 0.20`

This is the current automatic closure loop for exogenous risk:

`hypoxia -> d_risk -> r_dot and X_dot`

## 8. Final Unified Time Step

The live step function in `fusion_clean.py` computes:

`Y(t + dt) = Y(t) + dt * [X_dot; r_dot]`

with:

`u = u_base + |spark_c|`

So the current canonical one-step system is:

`X_dot = A (X - OMEGA * R d)
       + B (u_base + |spark_c|)
       - g * (X * abs(X))
       + P_r r
       + P_M d_risk
       + K8_quad(X[0:8], spark_c)`

`r_dot = -lambda * r + M * d_risk`

`spark_c = SPARK_CONSTANT_C * gate(z_proxy, alpha2, nor, plp)`

`Y_next = Y + dt * [X_dot; r_dot]`

This is the current canonical final equation of the repo.

## 9. Scalar Fusion Diagnostic

The scalar fusion diagnostic in `fusion_clean.py` is:

`BW = q + 2*C*g`

`SM = nu + C*q`

`spark = |SPARK_CONSTANT_C| * gate * 0.5 * (clip(ph) + clip(el))`

`Z_full = z_proxy * (1 + C * (clip(z) + clip(el)))`

`H = 1 + C * clip(hi)`

`W = 1 + C * clip(w)`

`leak = exp(-z_atomic / 64)`

`fusion = (BW * W)^2 * spark * Z_full * SM * H * leak * hierarchy_gain * (1 - ENTROPY_DEBT)`

`F_final = fusion + scalar_anchor(x)`

This is a diagnostic scalar, not the primary 32D state equation.

## 10. Current Inverse Component

The current inverse component is only partial:

`u24, states = solve_required_nodes(x_target, d_now, desired_dx)`

This solves a control inverse in the 24D homeostasis layer.

It does **not** yet solve the stronger inverse problem:

- which particle should spark
- at which threshold
- under which full `c26` and state configuration

So the current system has:

- forward unified dynamics: yes
- control inverse for `u24`: yes
- particle-specific Spark inverse: not yet
- global field `Y(x,t)`: not yet

## 11. What This Document Excludes

This document intentionally excludes:

- `geometry_package/*` legacy constants/engines
- `_tmp_*` experiments
- `128_*` visualization or prototype engines
- parallel `fusion_*` prototype engines outside the canonical import path

Those files are not the canonical equation, even when they contain related ideas.

## 12. Canonical Minimal Summary

If reduced to the shortest exact form currently implemented:

`Y = [X; r]`

`X_dot = A (X - OMEGA R d)
       + B (u_base + |SPARK_CONSTANT_C| * gate)
       - g (X * abs(X))
       + P_r r
       + P_M d_risk
       + [s * s + |SPARK_CONSTANT_C|*gate*(1 + 0.1*cos(angle(SPARK_CONSTANT_C))) - s] on first 8 dims`

`r_dot = -lambda r + M d_risk`

`Y_next = Y + dt [X_dot; r_dot]`

with:

`gate = gate(z_proxy, alpha2, noradrenaline, vasopressin; 138.88, 1/4, 1/128)`

This is the single current final equation of the live canonical engine.

## 13. What Is Still Missing Structurally

The current canonical engine has:

- a common Spark gate
- a 24D homeostasis operator
- an 8D risk-memory loop
- an additive K8 quadratic block

It does **not** yet have true structural:

- lensing
- rebranching
- proton foreground / shadow membership

That distinction matters.

Right now the live engine mainly does **state reweighting**:

- `gate(...)` scales the K8 nonlinearity
- `P_r @ r` projects memory into the 24D control state
- `P_M * d_risk` injects same-step risk
- `d` changes the equilibrium target manifold

Those are real modulations, but they are **not yet topology-changing operators**.

So the correct statement is:

- current repo has Spark gating and control modulation
- current repo does **not** yet have true lensing / rebranching in the structural sense

## 14. Structural Lensing Operator

The physically coherent place to define lensing is not with a hardcoded mode label.
It should be an operator induced by the raw channels that already act on the electroweak / neutral-current edges in `fusion_core.py`.

Use the raw channel coordinates:

- `c_gluco = c26[glucocorticoid]`
- `c_cort  = c26[right_cortisol]`
- `c_vaso  = c26[vasopressin_female]`
- `c_a2    = c26[right_alpha_2]`
- `c_syn   = c26[right_5ht1b_synchrotron]`

Use the K8 state:

- `s = X[0:8] = [q, g, nu, ph, el, hi, w, z]`

Define the electroweak / neutral-current field amplitudes:

`E_EM = ph + el + w`

`E_NC = nu + z`

`alpha2_active = 1 - c_a2`

Then define a scalar lensing strength:

`ell = sigma( k_l * gate * (c_gluco + c_cort + c_vaso + c_syn) * (E_EM + C * E_NC) - b_l * (1 - alpha2_active) - h_l * d_risk - theta_l )`

Interpretation:

- glucocorticoid / right_cortisol act through the existing `photon <-> w_boson` edge family
- vasopressin_female / right_alpha_2 act through the existing `neutrino <-> z_boson` family
- right_5ht1b_synchrotron acts through the existing `photon <-> electron` family
- risk suppresses foregrounding

This gives a genuine **state-and-input dependent lensing coefficient** instead of a named mode.

Turn that scalar into a 24D operator:

`L(Y, c26) = ell * P_L @ X`

where `P_L` is a sparse matrix that:

- foregrounds the photon / electron / w_boson / z_boson-related coordinates
- weakly suppresses unrelated mode coordinates
- leaves anchors bounded

Minimal K8 foreground mask:

`P_L^K8 = diag([0, 0, 1, 1, 1, 0, 1, 1])`

So the K8 part of lensing is:

`L_K8 = ell * P_L^K8 @ s`

## 15. Structural Rebranching Operator

Rebranching should not be a second hardcoded mode.
It should be a channel-induced graph rewrite that redistributes flow across the already-defined K8 sectors.

Use the raw branching channels:

- `c_male_gaba_b = c26[male_gaba_b]`
- `c_gaba_a      = c26[right_occipitalis_gaba_a]`
- `c_oxy         = c26[male_oxytocin]`
- `c_vaso        = c26[vasopressin_female]`
- `c_extrav      = c26[right_extraversion]`

Define a rebranching intensity:

`rho = sigma( k_r * gate * (c_male_gaba_b + c_gaba_a + c_oxy + c_vaso + c_extrav) + a_r * ell - h_r * d_risk - theta_r )`

Then define a K8 redistribution operator:

`R(Y, c26) = rho * T_R @ s`

with a conservative K8 transport matrix `T_R` such that:

- quark / gluon can feed into w_boson under strong-to-weak bridge
- neutrino can feed into z_boson / electron under neutral-current activation
- photon can feed into electron / w_boson under synchrotron / electroweak activation

Minimal physically consistent transport:

`T_R s = [`

`  -a_qw * q,`

`  -a_gw * g,`

`  -a_nz * nu - a_ne * nu,`

`  -a_pe * ph - a_pw * ph,`

`   a_pe * ph + a_ne * nu,`

`   0,`

`   a_qw * q + a_gw * g + a_pw * ph,`

`   a_nz * nu`

`]`

with all `a_* >= 0`.

That is the first operator in this repo that would make "rebranching" mean actual pathway redistribution rather than weight relabeling.

## 16. Proton Membership Operator

The current canonical engine fixes proton as derived:

`p_comp = q + C * g`

`BW = q + 2 * C * g`

What is still missing is the rule that decides when proton should be treated as:

- shadow composite
- foreground effective observable

without changing the latent K8 basis itself.

The clean operator is:

`chi_p(Y, c26) = sigma( k_p * gate * (1 + ell + rho) * |BW| - h_p * d_risk - m_p * ||r||_2 - theta_p )`

Interpretation:

- high Spark gate promotes proton emergence
- strong lensing / rebranching promote proton foregrounding
- strong risk-memory suppresses proton foregrounding

Then define the effective proton observable:

`p_eff = chi_p * BW`

and inject it back into the live 24D/K8 system without creating a new primitive basis:

`G_p(Y, c26) = p_eff * [1, C, 0, 0, 0, 0, C, 0, 0, ..., 0]^T`

So:

- `chi_p -> 0`: proton remains a background composite
- `chi_p -> 1`: proton becomes a foreground effective degree of freedom

This matches the theory better than either:

- "proton is always primitive"
- "proton is always excluded"

## 17. Structural Extension of the Canonical Equation

With the three missing structural operators added, the canonical 32D equation becomes:

`X_dot = A (X - OMEGA * R * d)`

`      + B (u_base + |SPARK_CONSTANT_C| * gate)`

`      - g * (X * abs(X))`

`      + P_r r`

`      + P_M d_risk`

`      + K8_quad(X[0:8], SPARK_CONSTANT_C * gate)`

`      + L(Y, c26)`

`      + R(Y, c26)`

`      + G_p(Y, c26)`

`r_dot = -lambda * r + M * d_risk`

and:

`Y_next = Y + dt * [X_dot; r_dot]`

This is the smallest structural extension that turns the current engine from:

- Spark-gated homeostasis with additive K8 nonlinearity

into:

- Spark-gated homeostasis
- plus lensing
- plus rebranching
- plus proton foreground/shadow selection

without reverting to old K6 / proton-primitive / 2D toy-field engines.
