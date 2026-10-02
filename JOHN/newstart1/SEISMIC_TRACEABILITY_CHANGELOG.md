# Seismic Traceability Changelog

## [1.0.0] - 2026-03-07

### Added
- **SEISMIC_TRACEABILITY_MASTER.md**: Established the overarching philosophy of the seismic traceability branch, defining seismic waves as the primary carrier and explicitly linking to the generalized framework (Big Man, Big Woman, etc.).
- **SEISMIC_TRACEABILITY_ARCHITECTURE.md**: Defined the structural flow of the system, including the Ingestion layer, Transformation Engine, and Mediator Insertion core.
- **SEISMIC_WAVE_STATE_MODEL.md**: Formalized the canonical `S_wave` continuous state vector, establishing variables from `event` to `closure_state`.
- **SEISMIC_TRACEABILITY_PIPELINE.md**: Translated the core closure grammar (node, seam, bridge, relay, mediator, barrier, projection trap) into explicit, mathematical wavefield procedures.
- **SEISMIC_MEDIATOR_AND_BARRIER_CLASSIFIER.md**: Created the rigorous decision matrix for classifying any disconnected component gap in the phase graph into one of 6 strict states.
- **SEISMIC_TRACEABILITY_TEST_PLAN.md**: Designed a pilot, falsifiable experiment focused on sub-threshold wave continuity across an apparent structural fault gap.

### Changed
- Shifted analytical paradigm from descriptive geological map-drawing (lines and proxy structures) to dynamic, mathematical Disjoint Set Union (DSU) phase-graph continuity evaluation.
- Redefined "Deprojection" from a vague concept into explicit transformed-domain algorithmic lifts (Frequency, Polarization, Residuals, Interferometry).

### Removed
- Removed reliance on secondary proxy data (fault maps, lineaments) as the primary determinant of system connectivity.
