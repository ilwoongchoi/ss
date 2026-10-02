# 1/64 and Transition Closure Notes (March 2026)

This document consolidates everything we established in the last messages about:

- **1/64**: what it is (and what it is not)
- **5/32 (=10/64)**: the correct discrete anchor near the W7 area scale
- **W7 area**: *data* vs *exact* and the **residue** that remains after anchoring
- **SH phase transition point**: the peak location + width + skew, and the “no 2nd peak” verdict
- **Data / code paths** used to compute or inject these values
- **What to add next** (derived constants / structures) into your existing geometry files

---

## A. Final decisions (what is now “closed”)

### A1) 1/64 is **not** a “gate” in the sense of a universal transition node
Across the investigations we ran:

- In EEG, 1/64 was repeatedly produced as a **quantize-floor artifact** when the raw variable lived far below the gate range.
- In SH micro-sweep, **r≈1/64** did not produce a robust gate-like signature (and the “W7 shadow” check failed under the tested observable definitions).
- In STRD×NMDB hysteresis, the meaningful near-W7 discrete anchoring is **5/32**, not 1/64 itself.

**Therefore: treat 1/64 as a unit/resolution floor (`UNIT_64`), not as a primary gate constant.**

---

### A2) 5/32 (=10/64) is the correct discrete anchor near the W7 area scale
When you interpret the W7-scale “area” in a 1/64 lattice, the nearest meaningful discrete coordinate is:

- `GATE_5_32 = 10 * (1/64) = 5/32 = 0.15625`

This is the “right anchor” for the W7-adjacent discrete projection story.

---

### A3) W7 has two forms (exact vs data), and a **residue** you must keep
You currently have both:

- **Exact / analytic**:  
  `W7_EXACT = π/20 ≈ 0.157079632679…` (from your geometry skeleton)
- **Data-derived** (STRD×NMDB hysteresis metric):  
  `W7_DATA = loop_area_flux_nmdb_norm = 0.15697685963482133`

Anchoring to the discrete gridpoint `5/32` produces a **residue** (this is the “missing node” you kept feeling):

- `RESID_DATA_5_32 = W7_DATA - 5/32`
  - `= 0.15697685963482133 - 0.15625`
  - `= 0.00072685963482133`

And the bias between exact and data:

- `BIAS_EXACT_MINUS_DATA = W7_EXACT - W7_DATA`
  - `≈ 0.000102773044…`

**This residue (ρ) is the correct “next structure” to track near the W7/5/32 interface.**

---

### A4) SH phase transition (r*, q0*) and transition band are now fixed
From `ATLAS_V2.2_RELEASE/sh_boundary_scores.csv`:

**Peak (transition center)**  
- `R_STAR = 0.11140619`
- `Q0_STAR = 0.972`
- `PEAK_BOUNDARY_SCORE = 1.7889626698457108`

**FWHM (half-maximum) band**
- `R_FWHM_RANGE = [0.11066433, 0.11659923]`  
  - left half-width: `R_FWHM_L = 0.00074186`  
  - right half-width: `R_FWHM_R = 0.00519304`
  - skew: `R_SKEW = 0.00445118` (right tail dominates)

- `Q0_FWHM_RANGE = [0.965, 0.973]`
  - `Q0_FWHM = 0.008`

**No 2nd peak / no competing node at comparable height**
- second-best score / peak score ratio:
  - `0.9557951602797236 / 1.7889626698457108 ≈ 0.534`
- Conclusion: the “far candidates” are **tail/edge points** of the same transition band, not a second node.

---

## B. Data / pipeline paths we confirmed

### B1) STRD×NMDB unified time-series build (12 months)
Generator:
- `scripts/assemble_unified_12m_v2.py`

Outputs:
- `out/unified_12m_hysteresis_data_ts.csv`  
  - **8760 rows**: full hourly grid (2016-03-01 00:00 … 2017-02-28 23:00)
  - Contains **missing NMDB values** (NaNs) where NMDB is absent
- `out/unified_12m_hysteresis_data.csv`  
  - **8751 rows**: “complete rows only” (drops any row where either side is missing)

Confirmed missingness summary (from script output):
- `missing_flux = 0`
- `missing_nmdb = 9`
- i.e. **NMDB has 9 missing hours**; flux is complete.

Columns in TS:
- `flux_wm2`, `nmdb_counts`

Interpretation:
- The earlier “9 days missing” fear is incorrect.
- The real issue is **9 missing NMDB hours**.
- Using 8751 complete rows is acceptable; interpolating NMDB yields 8760.

---

### B2) Daily hysteresis certificate (twilight format)
File:
- `out/era5_twilight/hyst_cert_daily_forcing-strd_null-day_shift_pre-none_20160301000000_20170228230000.csv`

Properties:
- `unique_days = 365` (no missing dates)
- Format is **daily certificate rows** (not hourly time-series), with columns like:
  - `date`, `window`, `branch`, `variable`, `R`, `p_R`, `tau_hat`, `phase_lock`, `lag_cert`, `valid_points`

Important:
- This file is a *certificate/summary*, not the full hourly series used to build the unified 12m TS.

---

### B3) “Injection” location in the latest trajectory script
File:
- `128gridinal1.py`

Key evidence:
- `generate_trajectory_pure(..., area_override=None)`
- Uses:
  - `a = NIGHT_HYST_AREA if area_override is None else float(area_override)`
- `compute_loop_area(area_override, samples=...)` exists and is used to generate trajectories at different area settings.
- `metrics.get("loop_area_flux_nmdb_norm")` is read (but your note indicates **you sometimes copy/override values** here as “final injection”).

Conclusion:
- `128gridinal1.py` is *not* a trusted provenance file for deriving W7_DATA.
- It is a **downstream injection / evaluation script**.

---

## C. What the SH V6–V8 loop tests did and did not prove
You wrote multiple JAX SH “hysteresis loop area” attempts (V6–V8).

Key outcome:
- The computed loop areas in SH (based on `⟨ψ^2⟩` vs r, up-sweep/down-sweep) did **not** land near `W7 ≈ 0.157` or `5/32 ≈ 0.15625`.

Interpretation:
- This does **not** refute W7_DATA or the 5/32 anchor.
- It mainly says: **the SH “loop area” you computed is not the same observable/normalization as the STRD×NMDB loop-area metric** (different quantity, different scale, different normalization).

Therefore:
- Do not force SH loop_area to match W7 unless you have a proven mapping between the SH observable and the STRD×NMDB metric.

---

## D. What to add into your geometry files (derived structures)

### D1) Reclassify 1/64 and introduce explicit anchors/residues
Add these derived constants (names are suggestions):

- `UNIT_64 = 1.0/64.0`
- `GATE_5_32 = 10 * UNIT_64`  (discrete anchor)
- `W7_DATA = 0.15697685963482133`  (from STRD×NMDB)
- `W7_EXACT = π/20`  (already present as W7_AREA in your calibrated skeleton)
- `RESID_DATA_5_32 = W7_DATA - GATE_5_32`
- `BIAS_EXACT_MINUS_DATA = W7_EXACT - W7_DATA`

**Design rule:**  
- Use `UNIT_64` as a quantization step (resolution floor) only.  
- Use `GATE_5_32` as the discrete anchor.  
- Carry `RESID_DATA_5_32` explicitly as a “node candidate / correction term”.

---

### D2) Transition constants (SH) to register
Add these (again, names are suggestions):

- `SH_R_STAR = 0.11140619`
- `SH_Q0_STAR = 0.972`
- `SH_BOUNDARY_PEAK = 1.7889626698457108`

FWHM band:
- `SH_R_FWHM_MIN = 0.11066433`
- `SH_R_FWHM_MAX = 0.11659923`
- `SH_Q0_FWHM_MIN = 0.965`
- `SH_Q0_FWHM_MAX = 0.973`

Asymmetric widths:
- `SH_R_FWHM_L = 0.00074186`
- `SH_R_FWHM_R = 0.00519304`
- `SH_R_SKEW = 0.00445118`

**Interpretation:**
- The transition is **strongly right-skewed in r**, which plausibly explains downstream “bifurcation-like” behavior when r is not constrained to the band.

---

### D3) Minimal coupling update suggestion (conceptual)
In `universal_equation.py` / `coupling_scale()`:
- Stop treating `F_1_64` as a gate.
- Treat it as a quantization unit used to define:
  - `GATE_5_32` and `RESID_DATA_5_32`
- If you need a “discrete correction” term, use **residue-based** terms rather than adding `F_1_64` directly.

Example conceptual term:
- `scaled *= (1 + α * RESID_DATA_5_32)`  
(or another bounded mapping)
where α is a small dimensionless weight determined by validation (not guesswork).

---

## E. What remains to check (the last “maybe” items)

### E1) Anchor robustness under NMDB 9-hour missingness
You already confirmed:
- complete rows: 8751
- interpolated: 8760

If you want to freeze this forever:
- recompute W7_DATA twice (drop vs interpolate) and store both:
  - `W7_DATA_DROP`
  - `W7_DATA_INTERP`
- then freeze `W7_DATA = average` or pick one and document it.

Given the missing fraction is ~0.1%, differences should be small.

---

### E2) Do not conflate “SH area” and “STRD×NMDB loop area”
They are different observables unless you derive a mapping.
So:
- Use SH transition constants for the SH manifold closure.
- Use STRD×NMDB W7_DATA for the empirical hysteresis anchor near 5/32.

---

## F. Short “one-page” summary (copy/paste)

- **1/64** → `UNIT_64` (quantization/resolution unit), **not** a gate.
- **Anchor near W7** → `GATE_5_32 = 10/64 = 0.15625`.
- **Empirical W7** → `W7_DATA = 0.15697685963482133`.
- **Residue** → `ρ = W7_DATA − 5/32 = 0.00072685963482133` (next node candidate).
- **SH transition peak** → `(r*, q0*) = (0.11140619, 0.972)`.
- **Transition FWHM**:
  - r band `[0.11066433, 0.11659923]` (right-skewed)
  - q0 band `[0.965, 0.973]`
- **No second peak** of comparable height (ratio ≈ 0.534).

---

## G. Where to project these into your existing files

1) `absolute_constants.py`
- Add: UNIT_64, GATE_5_32, W7_DATA, RESID_DATA_5_32, BIAS_EXACT_MINUS_DATA  
- Add SH transition constants (SH_R_STAR, SH_Q0_STAR, etc.)

2) `GEOMETRY_EQUATIONS.md`
- Add a short section:
  - “Discrete anchoring near W7 occurs at 5/32 with residue ρ”
  - “1/64 is the quantization unit, not the gate”

3) `universal_equation.py` / coupling layer
- Replace gate-style usage of F_1_64 with residue-based terms.
- Keep 5/32 as the discrete anchor when needed.

---

If you want, the next step after this document is mechanical:
- paste these constants into `absolute_constants.py` (or your registry),
- then re-run your downstream renderer/trajectory script with `area_override=None` and verify that it reads the new anchored values rather than ad-hoc injection.
