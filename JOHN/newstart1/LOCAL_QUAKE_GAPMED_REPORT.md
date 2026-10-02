# Local Earthquake CSV — Closure Grammar Check

- Input: `earthquake_1995-2023.csv`
- Base min magnitude: `6.5`
- Extended min magnitude: `6.5`
- Edge rule: distance ≤ `1200.0` km, time gap ≤ `365.0` days

## Results
- Total rows: `1000`
- Base events: `794` → components: `176`
- Extended events: `1000` (+206) → components: `189`

## Interpretation (tight, not philosophical)
- If `extended_components < base_components` under the SAME edge rule, then lowering the magnitude threshold acts like an **extended-universe mediator expansion** that restores continuity lost by thresholding.
- If there is NO reduction, then either (a) the edge rule is too strict, (b) the dataset is too sparse/global, or (c) magnitude-thresholding is not the right projection trap for this file.

## Outputs
- `LOCAL_QUAKE_GAPMED_SUMMARY.json`
- `LOCAL_QUAKE_GAPMED_REPORT.md`
- `LOCAL_QUAKE_GAPMED_MEDIATOR_CANDIDATES.csv`
