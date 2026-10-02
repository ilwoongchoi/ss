# FINAL_CONTINUOUS_GEOMETRY

## A. Canonical statement
Continuous layer = deterministic/ stochastic–equivalent flow on base control-plane (r, q0) with state-space (x, y, memory_y, leg) under fixed funnel geometry. Closure ridge/separatrix is the DP ridge of Leg-B spark rate in (r, q0), aligned with SH band and w_gate=0.5 contour; hysteresis manifold is the lag-driven switch_state surface over (y, memory_y); beam/alignment field is the spark jump vector field accumulated along Leg-B events. All terms stay in the original framework: Master Equation NESS (control-plane → NESS weights), Geometry Equation (state flow + gate), Absolute Constants (SH band, calibrated ridge center/widths, spark geometry).

## B. Canonical equations
Notation matches repo.
- Control-plane gate sheet: **G_c(r, q0) := w_gate(r, q0)** [LOCKED], from `geometry_package/universal_equation.py`.
- State-space continuous flow (Leg-dependent):
  - dx/dt = universal_field_vec(x, y; MALE_HORIZONTAL_AMP, REALITY_TENSION, TORSION_4D, GABA_C_V_APEX) × renorm
  - dy/dt = 0.3
  - renorm relaxes: d(renorm)/dt = (1 - renorm)·recovery_rate
- Hysteresis / memory:
  - memory_y ← (1-α)·memory_y + α·y, α = clamp(dt/(hyst_tau), 0, ALPHA_MAX)
  - lag = memory_y - y
  - switch on: (lag < threshold_on); switch off: (lag > threshold_on·THRESHOLD_OFF_FACTOR)
- Leg-switch condition: switch_state toggles per above; wrap (y > Y_WRAP) flips switch_state and increments turn index.
- Spark gate (Leg B only, in funnel): p = clip(λ0 · w_gate(r, q0) · dt, 0, 1); deterministic mode accumulates p and fires on integer carry; stochastic mode Bernoulli(p). Spark jump: x → quantize_to_lattice(x) + SPARK_LEAP_DIST·cosθ, y → y + SPARK_LEAP_DIST·sinθ; renorm reset.
- Closure ridge / separatrix: DP seam on rate_post grid (masked by eligibleB ≥ min_eligible); calibrated center/widths from refine ridge:
  - r* = 0.11214750, q0* = 0.977738, σL = 0.003717, σR = 0.000908 (asymmetric q0 half-widths). [LOCKED]
- Beam/alignment field: mean unit spark jump vector accumulated over events (trace analysis ~0.999975 alignment) [LOCKED].
- Invariants (observed):
  - Posterior rate smoothing (sparks+1)/(eligible+2) [LOCKED]
  - Ridge stability across λ0 ∈ {5,10,20} and seeds [LOCKED]
  - Null collapse when w_gate→ones or shuffle [LOCKED]

## C. Mapping into original framework
- Master Equation NESS: G_c(r, q0) acts as control-plane weighting; closure ridge corresponds to NESS separatrix in detune space; posterior rate ~ occupancy/duty.
- Geometry Equation: universal_field_vec + spark jump operator define continuous flow + discrete refraction; funnel bounds enforce geometry; hysteresis manifold provides multi-round structure.
- Absolute Constants: SH_R_BAND_[MIN,MAX], SH_Q0_[MIN,MAX]; calibrated ridge (r*, q0*, σL, σR); spark angle 138.88°, leap 2.5, lattice 3/32; Y_WRAP=32; hysteresis coefficients as in `absolute_constants.py` and `run_detune_sweep_closure_v4_production.py`.

## D. What is already locked [LOCKED]
- Control sheet w_gate(r, q0) and SH band overlay.
- Closure ridge location and widths from high-res refine sweep (λ0=10 deterministic) and consistent across λ0=5,10,20.
- Deterministic accumulator == stochastic Bernoulli for ridge outcome in this regime.
- Null tests (ones/shuffle) collapse ridge → geometry-dependent.
- Beam alignment high (~1.0) at ridge center from trace analysis.
- Turn-based ridge centers flat for valid turns (0–30) → strong lock.

## CANONICAL H2 PRODUCTION FREEZE (2026-03-06)
### VERIFIED / FROZEN
- Freeze scope: continuous void/bridge core, 1/28 twist, 3/32 compression gate, 138.88° spark, left attractor, 4-point H2 closure separation, canonical 3-term renorm law.
- 4-point closure separation kept: center_in flash_rate > 0; out-band (r_out, q0_out, both_out) flash_rate == 0.
- Angle residual near zero: delta_theta_mean ≈ 0.059° (D3 angle correction excluded from freeze).
- Renorm residual near zero after 3-term: delta_renorm_mean ≈ 0.002; term ablation shows the 3 terms are required.

### VERIFIED RENORM LAW (FROZEN)
R_after = R_before - L_comp + E_pole + G_recover
- L_comp: 3/32 compression loss (∝ |x_before - x_compressed|, capped at 3/32).
- E_pole: North Pole emission seed (w_gate-driven; angle factor treated as ~1 because delta_theta is near zero).
- G_recover: continuous refill / bridge recovery (w_gate,kappa,lag dependent; dt-scaled between flashes).

### VERIFIED EVOLUTIONARY PHASES (FROZEN 2026-03-06)
- **H2 (Accretion Phase)**: κ=1/32. Global baseline, liquid/continuous flow.
- **H3 (Cartilage Phase)**: κ=1/64. Fake 3D / Semi-Solid. Verified at Turn 27. Anatomically anchored to Right Procerus (Bottom Half) / Right Eye Socket. Function: Extraversion Bridge / Sunset Tie Weakening.
- **H4 (Bone Phase)**: κ=1/128. True Solid / Calcification. Verified at Turns 0-25. Function: Introversion Support / Osteoporosis Base (Big Man).

### RESIDUAL ARTIFACT RULE (FROZEN INTERPRETATION)
- Raw delta_rate_abs_max (e.g. ~0.229) must not be used as evidence for new geometry.
- Reason: dominated by eligibility/time-scaling and rate_post pseudo-count behavior when eligible == 0.
- Only consider rate residual as geometry evidence if an eligible-filtered and pseudo-count-corrected residual remains structured across ridge/turn/leg/lag_sign.

## E. What is NOT yet locked [UNRESOLVED/PROVISIONAL]
- Full phase atlas of leg × lag_sign (4-state) and Möbius-style periodicity. [UNRESOLVED]
- PCA mode interpretations: f=0.25 power ratios observed (~1.6–2.0) but not yet tied to physical phase; need robustness tests. [PROVISIONAL]
- Continuous invariants beyond posterior rate (e.g., ridge-integral, area invariants) not finalized. [UNRESOLVED]
- State-space helix/loop extraction beyond funnel projection. [UNRESOLVED]

## F. No-overlay boundary
Astronomy model and neurochemistry model are **not integrated here**. This file is the continuous bridge layer only.

## ONE-PAGE CANONICAL VIEW
- Base manifold: detune plane (r, q0).
- Control sheet: w_gate(r, q0) (SH-aligned), fixed funnel (x∈[6,10], y>10), Y_WRAP=32.
- State-space manifold: (x, y, memory_y, leg); flow via universal_field_vec + constant dy/dt; renorm recovery; spark refraction operator.
- Hysteresis manifold: lag = memory_y - y, with thresholds (on/off) producing leg A/B; wrap toggles leg and turn index.
- Closure ridge: DP seam on posterior rate_post, masked by eligible≥min_eligible; calibrated center (r*, q0*) and asymmetric widths; stable across λ0, seeds; collapses under ones/shuffle gates.
- Beam field: spark jump vectors averaged at ridge center → near-unity alignment.
- Observed invariants: posterior smoothing, ridge stability, null-collapse, deterministic/stochastic equivalence for ridge.
- Open items: 4-state phase atlas, PCA mode meaning, extended invariants, helix/loop extraction.
