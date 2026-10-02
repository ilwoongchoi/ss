# MAXWELL_INTEGRATION_IN_S5

This file pins *exactly* how Maxwell cavity/impedance/Q-factor enters the S^5 master operator stack using only quantities present in current files:

- `CONST_MAXWELL_F0_LOCK.csv`: `maxwell_f0 = 2.1235 GHz`, `maxwell_Q = 11.85`
- `MAXWELL_MAPPING_LOCK.json`: `pi1 = log10(f0 in Hz)`, `pi2 = log10(Q)`
- `check_maxwell.py`: cavity geometry locks
  - `MAXWELL_R_MAJOR = 17/8 = 2.125` (rational lock)
  - `MAXWELL_R_MINOR ≈ 0.2235501110` (minor axis; compared to `sqrt(1/20)` in-file)

## Maxwell State and Observables

Define Maxwell substate extracted from `S_n` (or appended if not present):

- `f0_n` : cavity resonance center frequency (Hz)
- `Q_n`  : cavity Q-factor (dimensionless)
- `Rmaj_n`, `Rmin_n` : cavity geometry axes (dimensionless in the codebase’s normalized units)

Locked values used when Maxwell is “in lock”:

- `f0_lock = 2.1235e9 Hz`
- `Q_lock = 11.85`
- `Rmaj_lock = 17/8`
- `Rmin_lock = 0.2235501110061347`

Pi mapping (locked):

- `pi1_maxwell = log10(f0_lock)`
- `pi2_maxwell = log10(Q_lock)`

## Where Maxwell Enters: Operator Classification (explicit)

Maxwell enters as **all of the below** (explicitly separated):

1. Boundary operator: *cavity acceptance / rejection*
2. Damping/resonance factor: *continuous weight applied to gates/operators*
3. Cavity constraint: *axes lock constraint*
4. Renorm recovery factor: *feeds `rho` / `RENORMALIZATION_BRIDGE` when in twilight-band*

No other roles are used.

## M_maxwell Definition (explicit operator)

Define `M_maxwell` as a map on the *continuous* part of state before discrete projection:

`M_maxwell : (x, A, tau, kappa, m, l, sigma, u, rho, g, f) -> (x', A', tau', kappa', m', l', sigma', u', rho', g', f')`

with the following steps:

### 1) Cavity acceptance gate (boundary operator)

Use the *only* Maxwell gate rule explicitly encoded in current pipeline logic (`maxwell_integration.py`):

- `Q_threshold = 2.0`
- `edge_margin_frac = 0.05` (range-edge truncation)

We do not import the frequency sweep range here; therefore in the S5 law we use only the Q-threshold as the acceptance boundary:

`b_Q = 1{ Q_n >= Q_threshold }`

When `b_Q = 0`, Maxwell contributes *no resonance weight*:

- `w_res = 0`

When `b_Q = 1`, proceed.

### 2) Resonance weight (damping/resonance factor)

Because the codebase’s locked Maxwell mapping is in pi-space (`MAXWELL_MAPPING_LOCK.json`), define resonance weight in pi-space:

- Let `π(S)` denote the system’s internal pi-coordinates computed by the projection operator that already exists in the pipeline (`pi_1`, `pi_2` are the canonical axes used throughout the repository).
- Let `π = (pi1, pi2)` be that internal coordinate for current state.

Then:

`Δπ = (pi1 - pi1_maxwell, pi2 - pi2_maxwell)`

Define a bounded resonance weight using only Q as sharpness (no new free parameters beyond what exists):

`w_res = b_Q * exp( - |Δπ1| * Q_lock ) * exp( - |Δπ2| * Q_lock )`

This uses only `Q_lock` (already locked) and the existing pi mapping; no new tuned constants are introduced.

### 3) Impedance modulation (explicit, minimal)

Impedance appears as a scalar modulation factor on the continuous evolution speed of the carrier and the tunnel openness.

Define the impedance factor:

`Z_fac = 1 / (1 + Q_lock * |Δπ1|)`

Again: only `Q_lock` and `Δπ1` appear.

Apply it to:

- carrier advance step size inside `C_cont` (the continuous W7/hysteresis operator)
- tunnel openness `u` inside operator layer `O_op`

### 4) Cavity geometry lock constraint

Enforce (as a constraint, not an invented dynamic):

- `Rmaj_n = Rmaj_lock`
- `Rmin_n = Rmin_lock`

Interpretation: the cavity geometry is a fixed boundary condition during the Maxwell-modulated update.

### 5) Renorm recovery coupling (to `RENORMALIZATION_BRIDGE`)

The repository’s operator layer includes `RENORMALIZATION_BRIDGE ~ 42.368` (Level 4) and the Maxwell integration pipeline is explicitly a “gate” that merges Maxwell points into canonical clouds. This is implemented as a bridge only when *gated OK* in the Maxwell pipeline.

Therefore, define:

`rho' = rho + w_res * RENORMALIZATION_BRIDGE`

with `RENORMALIZATION_BRIDGE` taken directly from `TOTAL_CONSTANT_TABLE.csv`.

## Output of M_maxwell

Within the master composition, `M_maxwell` contributes:

- a boundary acceptance bit `b_Q`
- a resonance weight `w_res`
- an impedance factor `Z_fac`
- a renorm increment `Δrho = w_res * RENORMALIZATION_BRIDGE`

These flow forward into the other layers:

- `C_cont` uses `Z_fac` to scale continuous carrier drift and hysteresis relaxation.
- `G_gate` uses `w_res` as a multiplier on gate weights (`kappa_eff`, `w_gate`) without changing the gate fractions themselves.
- `O_op` uses `Z_fac` to modulate tunnel openness `u` and spark triggering sensitivity.

