# Synthetic Alpha Activation Report

## Test Parameters
- **Base State**: 2 components (Main + gateway_peak)
- **Mediator**: mediator:synthetic_alpha
- **Activation Path**: gateway_peak <-> mediator:synthetic_alpha <-> sheet_id:4

## Step-by-Step Trace

| Step | Action | Nodes | Components |
|------|--------|-------|------------|
| 0 | initial_locked_state | 12 | 2 |
| 1 | add_synthetic_alpha | 13 | 3 |
| 2 | activate_gateway_peak_seam | 13 | 2 |
| 3 | activate_sheet_id_4_relay | 13 | 1 |

## Verification
- Initial components: 2
- Final components: 1
- Reduction: 1

## Conclusion
The activation arithmetic confirms that adding a mediator with seams to both the isolated node and the main component's sheet_id:4 results in a single connected component.
