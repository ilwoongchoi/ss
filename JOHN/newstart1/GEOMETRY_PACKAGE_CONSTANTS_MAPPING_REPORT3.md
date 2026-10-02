# Geometry Package Constants — LHD Mapping Summary

- Mapping input: `GEOMETRY_PACKAGE_CONSTANTS_TO_LHD3.csv`
- Keep/discard: `GEOMETRY_PACKAGE_CONSTANTS_TO_LHD3_KEEP_DISCARD.json`
- Keep count: `24`
- Discard count: `18`
- Duplicate numeric-value groups: `1`

## Headline constants

| Constant | Value_raw | Status | Mapping | DupGroup |
|---|---:|---|---|---|
| W7_EXACT | π/20 | phase_snap_candidate | phase_mean_rad ~= k*const (radians); detuning=observed/snapped |  |
| H2_W7 | 1/9 | phase_snap_candidate | phase_mean_rad ~= k*const (radians); detuning=observed/snapped |  |
| KAPPA_3_32 | 3/32 | phase_snap_candidate | phase_mean_rad ~= k*const (radians); detuning=observed/snapped |  |
| GATE_5_32 | 5/32 | phase_snap_candidate | phase_mean_rad ~= k*const (radians); detuning=observed/snapped |  |
| SPARK_ANGLE_DEG | 138.88 | phase_snap_candidate_deg | phase_mean_rad ~= k*rad(const_deg) |  |
| DISCRETE_CLOSURE | 1.0000424 | phase_snap_candidate | phase_mean_rad ~= k*const (radians); detuning=observed/snapped |  |
| REALITY_TENSION | 1.0100375 | phase_snap_candidate | phase_mean_rad ~= k*const (radians); detuning=observed/snapped |  |
| CHIRALITY_CONSTANT | 1/18 | phase_snap_candidate | phase_mean_rad ~= k*const (radians); detuning=observed/snapped |  |
| LUNAR_CYCLE | 1/28 | phase_snap_candidate | phase_mean_rad ~= k*const (radians); detuning=observed/snapped | LUNAR_CYCLE;Möbius Twist |

## Discarded constants (this LHD run)

Discard here means: not numeric or not mapped to the chosen LHD edge observables (phase/stability/bias/score) in this run.

| Constant | Reason |
|---|---|
| analytic_closure_tension | non_numeric |
| loop_strength_5 | out_of_lhd_range |
| WAVELENGTH_6 | out_of_lhd_range |
| DELTA_4 | out_of_lhd_range |
| Betti-5 (Metabolic Debt) | out_of_lhd_range |
| Ascending Branch | non_numeric |
| Descending Branch | non_numeric |
| LEFT_CORTISOL_R / Q0 | non_numeric |
| RIGHT_CORTISOL_R / Q0 | non_numeric |
| 7+1 Node Cycle | non_numeric |
| Right Cortisol Fake 3D | non_numeric |
| Receptor Mappings | non_numeric |
| 13-patch skeleton | non_numeric |
| 128-Grid | non_numeric |
| SN_OFFSET | non_numeric |
| TF_OFFSET | non_numeric |
| BLOOD_OFFSET_X/Y | non_numeric |
| 1.001375 | non_numeric |

## Duplicate numeric values

If two names share the same numeric value, keep the *canonical* name and treat the others as aliases unless the descriptions differ materially.

- `0.035714285714`: LUNAR_CYCLE, Möbius Twist
