# GEO/SEIS USGS Pilot — Closure Grammar Check

This pilot tests a concrete 'internal vs extended closure' mechanism on real earthquake catalog data:

- **Internal universe** = events above a stricter magnitude threshold (base).
- **Extended universe** = include lower-magnitude events (extended).
- **Mediator candidates** = added low-magnitude events that touch 2+ base components under the same edge rule.

## Query
- Date range (UTC): `2025-03-08` → `2026-03-08`
- BBox: lat `5.0`..`35.0`, lon `60.0`..`100.0`
- Edge rule: distance ≤ `150.0` km, time gap ≤ `3.0` days
- Base min magnitude: `5.0`
- Extended min magnitude: `4.0`
- API limit per query: `5000`

## Results (Connected Components)
- Base events: `56`; components: `43`
- Extended events: `512` (+456); components: `292`
- Base components *inside extended graph*: `42` (lower means 'mediator' actually merges base components)

### Component size snapshot
- Base top sizes: `[7, 3, 2, 2, 2, 2, 2, 1, 1, 1]`
- Extended top sizes: `[48, 40, 30, 10, 10, 9, 7, 7, 6, 5]`

## Mediator candidates
- Candidates found (touching ≥2 base components): `2`
- Output: `USGS_SOUTH_ASIA_1Y_MEDIATOR_CANDIDATES.csv`

## What this does / does not claim
- If extended components < base components **under identical edge rules**, then lower-magnitude events behave like **mediators** that restore continuity lost by thresholding.
- This is **not** a proof of 'universal geometry'; it is a concrete reproducible check that the *closure-grammar mechanism* (projection trap via thresholding + extended closure via minimal mediators) occurs in a real sparse-observation geophysical dataset.
