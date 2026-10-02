# Canonical Origin Equation (K8 → Origin Field → D3 Leak)

This file defines the **origin-side** equation implied by the *current* K8 graph code (`fusion_core.py`), in a form that the other agents can implement and cross-check.

It does **not** claim real-world physics; it is a consistent “origin kernel” inside this repo’s model.

## 1) Canonical Constants (from code)

- `C = sqrt(2)/5 ≈ 0.2828427125`  (`fusion_core.py:17`, `absolute_constants.py:67`)
- `C2 = C*C = 0.08`               (`fusion_core.py:18`)
- `θ = SPARK_ANGLE = 138.88°`     (`absolute_constants.py:69`, `SPARK_ANGLE_RAD`)
- `|C_spark| = 0.3857`            (`absolute_constants.py:70`..`72`, `SPARK_CONSTANT_C`)
- `Δt_obs = 99/350 ≈ 0.2828571429 rad` (derived from `11/7` and `100/18` in `simulate_cyclic_universe.py:26`..`28`)

## 2) Tier-4 Residuals in `fusion_core.py` (the “Origin is not empty” proof)

In the live K8 graph, the sub-leading (“Tier-4”) edge weights are:

- `w(q,ph) = C2/64`
- `w(q,nu) = C2/128`
- `w(g,ph) = C2/128`
- `w(q,el) = C2/128`
- `w(g,nu) = C2/256`
- `w(g,el) = C2/256`

These are literally present in `fusion_core.py:55`..`60`.

Define the **origin residual coupling** as the mean of these 6 weights:

`ε0 = (1/6) * Σ Tier4(w) = C2/128 = 0.000625`

This is the key identity:

- `ε0 = C2/128`
- equivalently `ε0 = S_NEUTRINO * C2` if `S_NEUTRINO = 1/128`.

## 3) D3 Leak Rate derived from ε0 (and how to hit 0.076)

Let:

- number of Tier-4 edges: `N4 = 6`
- electron scale: `S_ELECTRON = 1/8`
- topology factor: `B11 = 11` (your “BETTI_11”)
- correction: `β = 4/3` (the minimal scalar you used to close to `~0.076`)

Then the **raw origin leak** from Tier-4 edges is:

`L_raw = β * B11 * S_ELECTRON * (N4 * ε0)`

Numerically:

- `N4 * ε0 = 6 * (0.000625) = 0.00375`
- `S_ELECTRON * (N4*ε0) = 0.125 * 0.00375 = 0.00046875`
- `B11 * (...) = 11 * 0.00046875 = 0.00515625`
- `β * (...) = (4/3) * 0.00515625 = 0.006875`

So **with one `B11`**, you get `L_raw = 0.006875` (not `0.076`).

If you require the repo’s canonical drift/leak constant

- `OMEGA_SLOTTING_DELTA ≈ 0.076` (`geometry_package/absolute_constants.py:307`)

then the **smallest single-factor closure** that matches the number is multiplying by `B11` one more time:

`L_076 = B11 * L_raw = β * (B11^2) * S_ELECTRON * (N4 * ε0)`

Numerically:

- `L_076 = 11 * 0.006875 = 0.075625 ≈ 0.076`

Interpretation inside the model: one `B11` factor counts “where leak is generated”, the second `B11` counts “how many independent loops/sheets amplify it”.

## 4) The Origin Kernel in Complex Space (validation-only)

We keep complex space as a **validator**, not the primary geometry.

Define a complex “origin state” `z_n`:

`z_(n+1) = (z_n^2 * exp(i Δt_obs) + C_spark) * (1 - C) + ε0 - i * L(t)`

Where:

- `Δt_obs = 99/350` (rad)
- `C_spark = SPARK_CONSTANT_C = 0.3857 * exp(i θ)`
- damping `(1 - C)` is the same bounded recursion pattern we already use in validation scripts
- `ε0 = C2/128`
- `L(t)` is the D3 leak term; use either `L_raw` or `L_076` depending on which closure you are matching.

This equation is the **single “origin equation”** that the INTJ/complex-validator can check against the real-space vortex via Hilbert analytic signal (see `run_real_vortex_contract_expand_validation.py`).

## 5) How each “attack axis” uses the same origin equation (inputs only)

All four axes share the same origin equation and differ only by inputs / constraints:

- Photon-side (ENTJ): modulate `C_spark` phase toward `θ/2` when “collapse” is detected:
  - `θ_eff(t) = θ * (1 - D3_CORRECTION_FACTOR)` with `D3_CORRECTION_FACTOR = 0.5` ⇒ `θ_eff = 69.44°`
- Drug-side complement (INFP): set `L(t)=0` (complement set “no D3”) and see whether the orbit still closes.
- Outside-complex real-part missing (ENTP): compare `Re(z_n)` from the recursion to the real-geometry projection residual.
- Complex validation (INTJ): check invariants (`handedness`, `phase_turns`, continuity) and the drift match (`L_076 ~ 0.076`).

The particle-side explorer (Claude) expands `ε0` into a full **K8 state-vector** update, but the origin scalar `ε0 = C2/128` remains the shared bottom-floor constant.

