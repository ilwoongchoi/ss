# GEO/SEIS USGS Pilot — Closure Grammar Check

This pilot tests a concrete 'internal vs extended closure' mechanism on real earthquake catalog data:

- **Internal universe** = events above a stricter magnitude threshold (base).
- **Extended universe** = include lower-magnitude events (extended).
- **Mediator candidates** = added low-magnitude events that touch 2+ base components under the same edge rule.

## Query
- Date range (UTC): `2026-02-08` → `2026-03-08`
- BBox: lat `32.0`..`42.5`, lon `-125.0`..`-114.0`
- Edge rule: distance ≤ `35.0` km, time gap ≤ `10.0` days
- Base min magnitude: `3.0`
- Extended min magnitude: `1.0`
- API limit per query: `2000`

## Results (Connected Components)
- Base events: `33`; components: `17`
- Extended events: `1785` (+1752); components: `84`

### Component size snapshot
- Base top sizes: `[7, 5, 3, 3, 2, 2, 1, 1, 1, 1]`
- Extended top sizes: `[504, 451, 236, 135, 134, 67, 41, 23, 16, 13]`

## Mediator candidates
- Candidates found (touching ≥2 base components): `123`
- Output: `GEO_SEIS_USGS_CA30D_MEDIATOR_CANDIDATES.csv`

## What this does / does not claim
- If extended components < base components **under identical edge rules**, then lower-magnitude events behave like **mediators** that restore continuity lost by thresholding.
- This is **not** a proof of 'universal geometry'; it is a concrete reproducible check that the *closure-grammar mechanism* (projection trap via thresholding + extended closure via minimal mediators) occurs in a real sparse-observation geophysical dataset.
