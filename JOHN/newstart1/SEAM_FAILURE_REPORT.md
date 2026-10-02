# SEAM_FAILURE_REPORT

## Proven facts
- True connected components remain `11`.
- Main hard block is `gateway_peak -> sheet_id:2` (`TRUE_DISCONNECTION` in tunnel verification).
- Right branch verdict is `corridor` (corridor, not attractor).
- Projection-only overlaps exist (`9` seam rows flagged), including `dist_xy==0` pairs.
- Solenoid root-cause document states 1D-only handling and explicit non-integration into 2D PASS.
- Mersenne report is diagnostics-only and not a direct gluing proof.

## Seam failure diagnosis
- Main hard block: `gateway_peak <-> sheet_id:2` is tunnel-blocked and cannot be upgraded by Barnard.
- Fake center overlaps: any seam with `projection_overlap_flag=true` is treated as rendered coincidence, not a bridge.
- Solenoid incompatibility: seam-level direct solenoid bridge evidence is absent; solenoid is flagged as conflict source if used for 2D gluing claims.
- Mersenne conflict: candidate seams stay multi-component while Mersenne checks are diagnostics-only; this is compatibility pressure, not a bridge operator.
- Percolation candidates found in events: `sheet0_subsheets_vs_1to4, subsheet10_13_vs_14, subsheet10_vs_13` (candidate only, not true gluing).

## Barnard-linked reweighting plan (selector only)
- Barnard is applied only as candidate seam ranking, never as teleportation/bridge creation.
- Excluded from amplification: tunnel-blocked seams, projection-only overlaps, and corridor-only links.
- Best next candidate seam under current evidence: `sheet_id:1 <-> sheet_id:10`.

## Why corridor still does not glue
Global gluing fails because the dominant seam to `sheet_id:2` is a verified tunnel block, while many center overlaps are projection artifacts (`dist_xy==0`) and right-branch behavior is corridor drift rather than attractor capture.
