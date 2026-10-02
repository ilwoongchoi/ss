# Archetype × Closure × Bridge Overlay (Clarified)

This overlay merges:
- the **2-component internal bound** and **extended 2→1 closure** seam trace (`SEAM_GLUE_MAP.csv`),
- the **bridge vector metrics** (`BRIDGE_VECTORS_FINAL.csv`),
- the **archetype labels** from `ARCHETYPE_BRIDGE_MAP.md` (best-effort parse).

## Nodes
| node | archetype | universe | role | barrier | internal | extended |
|---|---|---|---|---|---|---|
| core_center | Big Man |  |  |  |  |  |
| flash:center_in | Spark | Original | Flash complement | None | Main | Unified |
| flash_bridge | Spark | Original | A-B flash bridge | None | Main | Unified |
| gateway_peak | Boundary | Original | Isolated residual; Internal boundary | True barrier with B | Isolated | Unified |
| mediator:synthetic_alpha | Mediator | Extended | External mediator | Bypasses G-B barrier | N/A | Unified |
| right_branch | Small Man |  |  |  |  |  |
| sheet_id:1 | Big Woman | Original | Anchor node (A) | None | Main | Unified |
| sheet_id:10 | Small Woman | Original | Stage 2 repair; A-D bridge | None | Main | Unified |
| sheet_id:11 | Small Woman | Original | Lane B deprojection | None | Main | Unified |
| sheet_id:12 | Small Woman | Original | Stage 2 repair | None | Main | Unified |
| sheet_id:13 | Small Woman | Original | Lane C relay origin | None | Main | Unified |
| sheet_id:14 | Small Woman | Original | Lane B deprojection | None | Main | Unified |
| sheet_id:2 | Big Woman | Original | Gateway neighbor (B) | True barrier with G | Main | Unified |
| sheet_id:3 | Big Woman | Original | Flash anchor (C) | None | Main | Unified |
| sheet_id:4 | Big Woman | Original | Anchor node (D); Relay target | None | Main | Unified |

## Edges (closure trace + bridge vectors)
| kind | step | u | v | u_arch | v_arch | seam_type | class | phase | red | gap | contact | drift |
|---|---:|---|---|---|---|---|---|---|---:|---:|---:|---:|
| seam_glue | 1 | sheet_id:2 | sheet_id:4 | Big Woman | Big Woman | Direct | Local seam | Internal | 1 |  |  |  |
| seam_glue | 2 | sheet_id:11 | sheet_id:2 | Small Woman | Big Woman | Direct | Deprojection | Internal | 1 |  |  |  |
| seam_glue | 3 | sheet_id:14 | sheet_id:2 | Small Woman | Big Woman | Direct | Deprojection | Internal | 1 |  |  |  |
| seam_glue | 4 | sheet_id:13 | sheet_id:3 | Small Woman | Big Woman | Relay | Relay path | Internal | 2 |  |  |  |
| seam_glue_relay_leg | 4 | sheet_id:2 | sheet_id:3 | Big Woman | Big Woman | Relay | Relay path | Internal | 2 |  |  |  |
| seam_glue | 5 | sheet_id:10 | sheet_id:2 | Small Woman | Big Woman | Direct | Deprojection | Internal | 1 |  |  |  |
| seam_glue | 6 | sheet_id:12 | sheet_id:2 | Small Woman | Big Woman | Direct | Deprojection | Internal | 1 |  |  |  |
| seam_glue | 7 | sheet_id:10 | sheet_id:1 | Small Woman | Big Woman | Direct | Activation | Internal | 1 |  |  |  |
| seam_glue | 8 | flash_bridge | sheet_id:3 | Spark | Big Woman | Direct | Flash bridge | Internal | 1 |  |  |  |
| seam_glue | 9 | flash:center_in | sheet_id:3 | Spark | Big Woman | Direct | Flash complement | Internal | 1 |  |  |  |
| seam_glue | 10 | gateway_peak | mediator:synthetic_alpha | Boundary | Mediator | Direct | External expansion | External | 0 |  |  |  |
| seam_glue | 11 | mediator:synthetic_alpha | sheet_id:4 | Mediator | Big Woman | Direct | Relay connection | External | 1 |  |  |  |
| bridge_vector |  | mediator:synthetic_alpha | core_center | Mediator | Big Man |  |  |  |  | 7.6274 | 0.0169 | 2.147 |
| bridge_vector |  | gateway_peak | core_center | Boundary | Big Man |  |  |  |  | 8.1132 | 0.015 | 1.0 |
| bridge_vector |  | mediator:synthetic_alpha | right_branch | Mediator | Small Man |  |  |  |  | 15.2755 | 0.002 | 2.147 |
| bridge_vector |  | core_center | right_branch | Big Man | Small Man |  |  |  |  | 0.0 | 0.95 | 4.61 |
