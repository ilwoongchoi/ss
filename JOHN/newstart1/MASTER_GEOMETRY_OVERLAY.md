# MASTER GEOMETRY OVERLAY (Latest)

This overlay is built from the canonical patch embedding in `geometry_package/final_manifold_renderer.py`
and the latest closure trace + bridge list in `_UNIVERSAL_GEOMETRY_FINAL_BUNDLE/`.

## Outputs
- `MASTER_GEOMETRY_NODES.csv`
- `MASTER_GEOMETRY_EDGES.csv`
- `MASTER_GEOMETRY_EDGES_WITH_METRICS.csv` (bridges/seams + canon_* + bridge_* metrics)
- `MASTER_GEOMETRY_METRICS_ALL_PAIRS.csv` (gap/contact/drift for any node pair)
- `MASTER_GEOMETRY_3D.png`
- `FINAL_GEOMETRY_LOCK_REGISTRY.json` (merged face corridor + left choke band + PLP zero points)

## What this fixes (your complaint)
- Keeps the 2-component internal bound (gateway_peak isolated) and shows the extended mediator bypass.
- Keeps 4 archetypes visible as labels/colors (Big Woman / Small Woman / Big Man / Small Man) instead of collapsing to anonymous points.
- Keeps the constants in-frame (pi/20, 1/32, 3/32, 1/9, spark 138.88°) from `absolute_constants.py`.

## Angle meaning (in this artifact)
- `azimuth_deg`: edge direction in XY plane of the canonical embedding.
- `elevation_deg`: tilt above XY plane.
- These angles are computed from the *canonical patch coordinates* (not a spring layout).

## Canonical edge function (requested)
- `gap/contact/drift(u,v)` is implemented in `geometry_package/universal_metrics.py` on the canonical 3D embedding.
- All-pairs results are exported to `MASTER_GEOMETRY_METRICS_ALL_PAIRS.csv`.

## Note on engine pair visibility
- `core_center` (Big Man) and `right_branch` (Small Man) are injected on the canonical Z-axis so they are visible in the same 3D frame.
  This does not change closure steps; it is a coordinate overlay for archetype visibility.
