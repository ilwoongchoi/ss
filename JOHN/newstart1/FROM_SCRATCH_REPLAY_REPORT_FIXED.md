# From-Scratch Replay Report (Fixed)

## Sources
- `out/closure_theorem_pack/run_closure_replay.py`
- `out/closure_theorem_pack/FROM_SCRATCH_REPLAY_REPORT.md`
- `CANONICAL_PROOF_TRACE_FIXED.csv`

## Bug Fixes Applied
1. Recomputed true pre/post component counts at each step.
2. Fixed internal boundary state after step 8.
3. Ensured `mediator:synthetic_alpha` appears only from step `9a`.
4. Distinguished internal theorem (`2` bound) from extended theorem (`2->1`).

## Baseline (Cold Start)
- Universe nodes at start: `12`
- Initial components: `11`
- Pre-linked baseline edge: `flash:center_in <-> flash_bridge`

## Correct Step Table
| Step | Bridge | Pre | Post | Delta | Scope |
|---|---|---:|---:|---:|---|
| 1 | `sheet_id:2__sheet_id:4` | 11 | 10 | -1 | internal |
| 2 | `sheet_id:11__sheet_id:2` | 10 | 9 | -1 | internal |
| 3 | `sheet_id:14__sheet_id:2` | 9 | 8 | -1 | internal |
| 4a | `sheet_id:13__sheet_id:3` | 8 | 7 | -1 | internal |
| 4b | `sheet_id:3__sheet_id:2` | 7 | 6 | -1 | internal |
| 5 | `sheet_id:10__sheet_id:2` | 6 | 5 | -1 | internal |
| 6 | `sheet_id:12__sheet_id:2` | 5 | 4 | -1 | internal |
| 7 | `sheet_id:10__sheet_id:1` | 4 | 3 | -1 | internal |
| 8 | `flash_bridge__sheet_id:3` | 3 | 2 | -1 | internal |
| 9a | `ADD mediator:synthetic_alpha` | 2 | 3 | +1 | extended |
| 9b | `gateway_peak__mediator:synthetic_alpha` | 3 | 2 | -1 | extended |
| 10 | `mediator:synthetic_alpha__sheet_id:4` | 2 | 1 | -1 | extended |

## Internal Boundary (After Step 8)
- Component 1 (main internal body):
  - `sheet_id:1, sheet_id:2, sheet_id:3, sheet_id:4, sheet_id:10, sheet_id:11, sheet_id:12, sheet_id:13, sheet_id:14, flash:center_in, flash_bridge`
- Component 2 (isolated residual):
  - `gateway_peak`
- `mediator:synthetic_alpha` is **absent** before step `9a`.

## Extended Closure (Steps 9a-10)
- Step `9a`: adds external node `mediator:synthetic_alpha`, producing temporary `2->3`.
- Step `9b`: binds `gateway_peak` to mediator, `3->2`.
- Step `10`: relays mediator into main body via `sheet_id:4`, `2->1`.

## Reproducibility
- Cold-start replay uses no inherited DSU state.
- Trace is deterministic and reproducible.
- No hidden-state leakage required to obtain final closure.
