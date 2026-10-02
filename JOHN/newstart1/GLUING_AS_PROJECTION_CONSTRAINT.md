# GLUING_AS_PROJECTION_CONSTRAINT

This file demotes gluing to **final projection/closure constraints** only.
Primary law is the S^5 master operator stack; gluing is a check on the projected skeleton.

Inputs used (locked artifacts already in repo root):

- `SEAM_GLUE_MAP.csv` (11 seams + internal barrier + external mediator link)
- `FINAL_CONNECTED_MANIFOLD_ATLAS.md` (13 patches description)
- `MANIFOLD_PATCH_TABLE.csv` (patch list)

## 1) Projection Outputs (what gluing consumes)

The master law yields a continuous state `S_n` on S^5 plus continuous auxiliaries.
The projection operator `P_proj` (defined in `PATCH_AND_GRID_FROM_S5.md`) yields:

- `p_n` : patch label in `{A,B,C,D,10,11,12,13,14,F,F',G,X}`
- `q_n` : 128-grid coordinate
- `e_n` : seam-activation evidence vector (local, relay, mediator flags)

Gluing **does not feed back** into the continuous law. It only checks the projected outputs.

## 2) Closure Constraint Form (exact)

Define a discrete graph `Γ` on the 13 projected patches.

- Nodes: `V = {A,B,C,D,10,11,12,13,14,F,F',G,X}`
- Edges: `E` are exactly the activated seams in `SEAM_GLUE_MAP.csv`:
  - (B,D)   = `sheet_id:2__sheet_id:4`
  - (11,B)  = `sheet_id:11__sheet_id:2`
  - (14,B)  = `sheet_id:14__sheet_id:2`
  - (13,C) and (C,B) as relay edge bundle = `sheet_id:13__3__2`
  - (10,B)  = `sheet_id:10__sheet_id:2`
  - (12,B)  = `sheet_id:12__sheet_id:2`
  - (10,A)  = `sheet_id:10__sheet_id:1`
  - (F,C)   = `flash_bridge__sheet_id:3`
  - (F',C)  = `flash:center_in__sheet_id:3`
  - (G,X)   = `gateway_peak__mediator:synthetic_alpha`
  - (X,D)   = `mediator:synthetic_alpha__sheet_id:4`

Barrier constraint (intrinsic, never crossed):

- Forbidden edge: `(G,B)` = `gateway_peak ↔ sheet_id:2`

Closure check is then:

- Internal closure constraint (intrinsic universe): apply steps 1..9 from `SEAM_GLUE_MAP.csv` and compute `π0(Γ_internal)`.
  - Required locked result: `π0 = 2` (main component + isolated `G`).
- Extended closure constraint: after adding node `X` and edges (G,X) and (X,D), compute `π0(Γ_extended)`.
  - Required locked result: `π0 = 1`.

## 3) How Seam Activation Is Read From S5 Outputs (constraint only)

Each seam in `SEAM_GLUE_MAP.csv` is treated as a constraint predicate on the projection evidence vector `e_n`:

- Direct seam `(i,j)` is “active” iff `E_dir(i,j; S_n) = 1`.
- Relay seam `13__3__2` is “active” iff both hop predicates are true:
  - `E_dir(13,C; S_n) = 1` and `E_dir(C,B; S_n) = 1`.
- External mediator seam is “active” iff:
  - `E_ext(G,X; S_n) = 1` and `E_ext(X,D; S_n) = 1`.

No new seams are inferred here; only the locked list is accepted.

## 4) What Gluing Cannot Do (explicit)

Gluing cannot:

- modify `x_n` on S^5
- modify `A_n`, `tau_n`, `kappa_n`, `m_n`, `rho_n`, `g_n`, `f_n`
- generate new edges beyond `SEAM_GLUE_MAP.csv`

Gluing only asserts:

- the internal theorem bound `2` components in the intrinsic universe
- the extended theorem closure `1` component after adding the mediator patch `X`
- the barrier `(G,B)` remains forbidden (not “missing data”, not “projection trap”)

