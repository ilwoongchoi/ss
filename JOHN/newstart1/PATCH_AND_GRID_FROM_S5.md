# PATCH_AND_GRID_FROM_S5

This file derives the **projected 13-patch / 128-grid skeleton outputs** as a projection `P_proj` from the S^5 state, and states exactly which terms are missing if any part is not derivable from current files.

Inputs used:

- `TOTAL_CONSTANT_TABLE.csv` (Level 7: 13-patch, 128-grid, offsets)
- `SEAM_GLUE_MAP.csv` (patch labels and closure trace)
- `MAXWELL_MAPPING_LOCK.json` (pi mapping definitions)

## 1) Projection Operator Signature

`P_proj : S_n -> (p_n, q_n, pi_n, e_n)`

where:

- `p_n` is the projected patch label (13-patch skeleton)
- `q_n` is the projected 128-grid coordinate
- `pi_n = (pi1_n, pi2_n)` is the internal pi-coordinate used across the repo
- `e_n` is evidence vector for seam activation used only by gluing constraints

## 2) pi-space from S^5 (what is derivable right now)

From `MAXWELL_MAPPING_LOCK.json`, pi axes are locked as:

- `pi1 = log10(f0 in Hz)`
- `pi2 = log10(Q)`

This gives a *type constraint* on `pi`, but not a full derivation from `x ∈ S^5`.

Therefore, the **missing term** is explicit:

- Missing: `F_s5_to_f0Q(x, A, tau, kappa, ...) -> (f0, Q)`

Without `F_s5_to_f0Q`, the best current derivation is:

- pi coordinates are computed by the already-existing pipeline on observed points (TrackA + Maxwell integration), and treated as an attached observable of `S_n`.

So we write:

- `pi_n := π_obs(S_n)` where `π_obs` is the repository’s existing mapping from data records to `(pi_1, pi_2)` fields.

## 3) 13-patch membership p_n (derivation constraint)

The 13-patch labels are:

`{A,B,C,D,10,11,12,13,14,F,F',G,X}`

Patch membership is defined as a deterministic classifier on the projected evidence coordinates:

`p_n = PatchClass(pi_n, branch_n, sep_n, receptor_n, shell_n, ...)`

Current files provide:

- existence of projected patch set (TOTAL constants)
- closure trace and minimal edge set (SEAM_GLUE_MAP)
- attractor basins and separatrix concepts (Level 5)
- receptor and fake-depth shell layer (Level 6)

But the exact `PatchClass` rule table is not fully specified in the files provided in this workspace snapshot.

Therefore:

- Missing: `PatchClass` explicit rule table linking `(pi, l, sigma, g, f, ...) -> patch`.

What is derivable now as constraints:

- `p_n` must lie in the 13-label set.
- closure constraints in `GLUING_AS_PROJECTION_CONSTRAINT.md` must hold for the projected edge evidence `e_n`.

## 4) 128-grid coordinate q_n (partial derivation)

From `TOTAL_CONSTANT_TABLE.csv`:

- `128-Grid` is the final projection of all laws as 128 trajectories.
- `SN_OFFSET = 8 * F_1_32`
- `TF_OFFSET = 4 * F_1_32`
- `BLOOD_OFFSET_X/Y` exist as offsets

The `F_1_32` symbol corresponds to the canonical stable leakage gate `KAPPA_1_32 = 1/32`.

Thus the **derivable part** is:

- grid offsets are linear multiples of `KAPPA_1_32`:
  - `SN_OFFSET = 8/32 = 1/4`
  - `TF_OFFSET = 4/32 = 1/8`

What is missing:

- the exact mapping from state observables to the “S/N”, “T/F”, and other axes used to place points on the 128 grid.
- the exact quantizer from continuous coordinates to `{0..127}` bins.

Therefore, define the grid projection as:

- `q_n = Quant128( Φ_traits(S_n) + offsets )`

with:

- `offsets = (SN_OFFSET, TF_OFFSET, BLOOD_OFFSET_X, BLOOD_OFFSET_Y, ...)`
- Missing: `Φ_traits` explicit feature extractor and `Quant128` quantizer definition.

## 5) Seam activation evidence e_n

The seam map is locked as a final output skeleton. We therefore define:

`e_n = Evidence(S_n)`

and constrain it only by the activated seam list:

- must support exactly the seams in `SEAM_GLUE_MAP.csv` as “on”
- must keep the intrinsic barrier `(G,B)` as “off”

Missing:

- explicit local geometry verification function from `x`/`pi` to seam evidence, because that logic lives in the earlier seam operator pipelines and is not yet expressed as a closed-form S^5 function.

## 6) Summary of Missing Terms (not a reclassification; explicit symbols)

The projection layer requires the following missing explicit definitions to become a fully derived map from S^5:

- `F_s5_to_f0Q` (carrier -> Maxwell observables)
- `PatchClass` (pi/branch/receptor/shell -> 13-patch membership)
- `Φ_traits` and `Quant128` (state -> 128-grid coordinate)
- `Evidence` (state -> seam activation evidence)

All other constraints and label sets are already locked by `TOTAL_CONSTANT_TABLE.csv` and `SEAM_GLUE_MAP.csv`.

