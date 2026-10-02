# Local Earthquake CSV — Closure Grammar Check

- Input: `earthquake_data.csv`
- Base min magnitude: `6.5`
- Extended min magnitude: `5.5`
- Edge rule: distance ≤ `800.0` km, time gap ≤ `120.0` days

## Results
- Total rows: `782`
- Base events: `782` → components: `422`
- Extended events: `782` (+0) → components: `422`

## Interpretation (tight, not philosophical)
- If `extended_components < base_components` under the SAME edge rule, then lowering the magnitude threshold acts like an **extended-universe mediator expansion** that restores continuity lost by thresholding.
- If there is NO reduction, then either (a) the edge rule is too strict, (b) the dataset is too sparse/global, or (c) magnitude-thresholding is not the right projection trap for this file.

## Outputs
- `LOCAL_QUAKE_GLOBAL_2022_SUMMARY.json`
- `LOCAL_QUAKE_GLOBAL_2022_REPORT.md`
- `LOCAL_QUAKE_GLOBAL_2022_MEDIATOR_CANDIDATES.csv`
