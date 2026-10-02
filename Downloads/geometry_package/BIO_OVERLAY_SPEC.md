# BIO OVERLAY SPEC (Regime-2)

## 1) Overview
- Regime-2 is an interpretation layer over Regime-1 scalar fields.
- Allowed: Möbius loop narrative, 7+1 nodes, jawless→jawed transition framing, social/neuro labels.
- Not allowed: redefining Regime-1 constants/operators/primitives.
- Regime-2 only reads Regime-1 API outputs and maps them to states.

## 2) Mapping table (concept -> Regime-1 field)

| Overlay concept | Regime-1 reference |
|---|---|
| Left/Right volume balance | `w_gate(r,q0)`, `kappa_eff(r,q0)` gradient |
| Core stability | `in_sh_band(r,q0)` + `kappa_eff≈1/32` condition |
| Funnel occupancy | stats from `get_emergent_128_nodes(t_macro)` |
| Structural seam activation | `PLP_SPINE(x,y)` on `16x16` chart |
| Sink/source asymmetry | `Betti-5 / Betti-11` ring occupancy and flux annotation |
| Temporal reversal phase | `get_macro_micro_time(t_macro)` |
| Epoch forcing | macro-time schedule over `LUNAR_CYCLE` |

## 3) D3 modes (overlay-only classification)
- **ideal_D3_grounded**
  - Grounded to Betti-0, productive exhaust pattern.
  - Core signature: stable gate + non-collapsed funnel occupancy.
- **captured_D3 (fake sink)**
  - Energy circulation without effective transport.
  - Core signature: gate present but low occupancy efficiency pattern.
- **sealed_D3**
  - Symmetric lock with practical AND-gate closure.
  - Core signature: near-anchor kappa with near-zero occupancy dynamics.

Regime-2 must never modify core to force these modes; it only classifies snapshots.

## 4) Temporal/Epoch mapping
- Epoch narrative (`E(t)` phases, jawless→jawed, branch changes) must be encoded as overlay metadata.
- The only numeric clock references are Regime-1 time outputs:
  - `t_micro`
  - `is_reverse`
  - `emergent_128_nodes`
- “Post-appearance branch” annotations must stay metadata-only and must not mutate core constants.

## 5) Usage rules (strict)
- Regime-2 calls Regime-1 as black-box API.
- Allowed: call/query, aggregate, label, classify.
- Forbidden:
  - changing SH band definition
  - changing kappa map
  - changing 128-grid emergence logic
  - changing renderer primitive geometry constants
