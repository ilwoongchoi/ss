## Master Equation NESS mapping (control plane)
- Control sheet: G_c(r,q0)=w_gate(r,q0). Use directly as control-plane weight. SH band constants bound the admissible detune region.
- Closure separatrix: use calibrated ridge center/widths (r*=0.11214750, q0*=0.977738, σL=0.003717, σR=0.000908) as NESS separatrix prior.
- Posterior rate smoothing: rate_post=(sparks+1)/(eligible+2); treat as duty/occupancy estimator.
- Null tests: ones/shuffle collapse ridge → geometry-dependent; keep as sanity check.

## Geometry Equation mapping (state space)
- State variables: (x, y, memory_y, leg, renorm).
- Flow: universal_field_vec; dy/dt=0.3; renorm relaxes to 1 with recovery_rate; spark refraction is discrete jump operator (angle 138.88°, leap 2.5, lattice 3/32).
- Funnel constraints: x∈[6,10], y>10; wrap at Y_WRAP=32 toggles leg and turn.
- Hysteresis: memory_y low-pass with α=clamp(dt/(hyst_tau), 0, ALPHA_MAX); lag=memory_y-y; leg on/off thresholds from run_detune_sweep_closure_v4_production.py.
- Spark gate: only when leg B and funnel; p=clip(λ0·w_gate·dt,0,1); deterministic accumulator ≡ Bernoulli for ridge stats in tested regime.

## Absolute Constants usage
- SH band: SH_R_BAND_MIN/MAX, SH_Q0_MIN/MAX.
- Ridge calibration: r*, q0*, σL, σR as above; constants_bundle.json already written.
- Spark geometry: SPARK_ANGLE_DEG=138.88, SPARK_LEAP_DIST=2.5, COMPRESSION_GAP=3/32.
- Hysteresis parameters: HYST_TAU_SCALE, THRESHOLD_ON_FACTOR, THRESHOLD_OFF_FACTOR, ALPHA_MAX, NIGHT_TAU_LAG; Y_WRAP=32.

## Implementation notes
- For any solver using NESS weights, feed w_gate and mask outside SH band; use ridge prior for initialization.
- For simulation, keep deterministic accumulator mode available to verify stochastic equivalence.
- When extracting ridges, mask by eligible ≥ min_eligible and apply DP seam; persist ridge to *_ridge.csv and constants_bundle.json.
- When analyzing periodicity, filter turns with mask coverage (e.g., ≥50 cells) and pixels with ≥0.8 coverage before PCA.
- Keep astronomy/neurochem overlays separate; this memo is continuous geometry only.

## CANONICAL H2 PRODUCTION FREEZE (2026-03-06)
### VERIFIED / FROZEN
- H2 closure separation kept (4-point): center_in flash_rate > 0; out-band flash_rate == 0.
- Angle residual near zero: delta_theta_mean ≈ 0.059° (exclude angle correction from current freeze).
- Renorm residual near zero after canonical 3-term law: delta_renorm_mean ≈ 0.002.
- Raw rate residual max (~0.229) is a measurement artifact from eligibility/time-scaling and rate_post pseudo-count when eligible == 0.

### FROZEN RENORM LAW
R_after = R_before - L_comp + E_pole + G_recover
- L_comp: 3/32 compression loss.
- E_pole: North Pole emission seed (w_gate-driven; angle factor ~1 under near-zero delta_theta).
- G_recover: continuous refill / bridge recovery (w_gate,kappa,lag dependent; dt-scaled between flashes).

### VERIFIED EVOLUTIONARY PHASES (FROZEN 2026-03-06)
- **H2 (Accretion Phase)**: κ=1/32. Global baseline.
- **H3 (Cartilage Phase)**: κ=1/64. Fake 3D / Semi-Solid. Verified at Turn 27. Anatomical Anchor: Right Procerus (Bottom Half).
- **H4 (Bone Phase)**: κ=1/128. True Solid / Calcification. Verified at Turns 0-25. Anatomical Anchor: Big Man Base.

### ARTIFACT RULE (FROZEN INTERPRETATION)
- Do not use raw delta_rate_abs_max as evidence for new geometry unless eligible-filtered and pseudo-count-corrected residual remains structured across ridge/turn/leg/lag_sign.
