# geometry_package (Canonical)

This folder is the canonical, runnable "geometry package" snapshot rebuilt from the current repo state on **2026-03-10**.

## Scientific Core Documents

- `GEOMETRY_SCIENTIFIC_CORE.md` — **NEW**: Metabolic and physical foundation (ATP/ADP, NADH/NAD+, ETC coupling)
- `FINAL_ESCAPE_ROUTE.md` — **NEW**: RIGHT D2 traverse route with metabolic trajectory
- `EVOLUTIONARY_HISTORY.md` — **NEW**: SF/NF/NT progression and ISFJ A-type female electron flow
- `SKELETAL_CORE.md` — Mathematical invariants and operators (V2.3)
- `GEOMETRY_EQUATIONS.md` — Continuous-discrete tension physics
- `MOBIUS_CONTINUOUS_GEOMETRY.md` — Thermodynamic hysteresis loop
- `ADDENDUM_20260310_SCIENTIFIC.md` — Change summary with evolutionary analysis and PLP structure

## What's inside

## What’s inside

- `geometry_package/constants/TOTAL_CONSTANT_TABLE.csv` — canonical constant table (copied from repo root).
- `geometry_package/s5_executable_maps.py` — executable definitions for maps that were previously documented as missing:
  - `F_s5_to_f0Q`, `PatchClass`, `SeamAct`, `Phi_traits`, `Quant128`, `d_sep`
- `geometry_package/source_docs/` — source geometry documents copied from repo root:
  - `GEOMETRY_EQUATIONS.md`
  - `Universal Geometry Equation.md`
- `geometry_package/renderers/` — renderer/validation scripts copied from repo root:
  - `validate_geometry_3d_renderer.py`
- `geometry_package/lhd/` — LHD(Halpha+Bolometer) mapping outputs:
  - constants → LHD observables mapping (`*_TO_LHD.csv`, `*_KEEP_DISCARD.json`)
  - cluster → universal bridge-vector scale mapping (`LHD_QUANT_TO_UNIVERSAL_*`)
- `geometry_package/full_graph/` — locked full-geometry graph artifacts:
  - `FULL_GEOMETRY_LOCKED.png`
  - `FULL_GEOMETRY_LOCKED.dot`
  - `FULL_GEOMETRY_LOCKED_MISSING.md`

## Source-of-truth links (repo root)

Some large/active working files remain in the repo root; this package copies the canonical subsets but does not delete originals:
- `TOTAL_CONSTANT_TABLE.csv`
- `BRIDGE_VECTORS_FINAL.csv`
- `UNIVERSAL_GEOMETRY_COMPLETE_MAP.json`

## Notes / gaps

- `absolute_constants.py` was referenced in `TOTAL_CONSTANT_TABLE.csv` as a source, but a file with that exact name is not present in this repo snapshot. The constants are still present in the table; the original source file is missing/renamed.
