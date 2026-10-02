# Seismic-Wave Falsifiable Tests
## Three Predictions Distinguishing Closure-Grammar from Standard Seismology

---

## Core Hypothesis (Recap)

> **Seismic wave fields are continuous carriers of connectivity. Apparent phase discontinuities are projection traps (sparse observation), not true barriers. Minimal mediator phases (converted, scattered, low-amplitude) recover continuity beyond standard phase association, while true impedance barriers remain uncrossable.**

---

## Prediction 1: Converted Phase Continuity Across Structural Gaps

### Statement
In regions with mapped fault gaps or structural discontinuities, P-to-S converted phases (receiver functions, Ps phases) will reveal continuous impedance boundaries where standard P- and S-wave arrivals suggest breaks.

### Standard View
Structural gaps represent true discontinuities. Wave propagation across gaps requires complex path deviations; no simple phase continuity expected.

### Closure-Grammar View
Gaps are projection traps in surface mapping. Converted phases act as mediators revealing continuous deep structure beneath apparent breaks.

### Falsifiable Test

**Setup**:
- Select 15 fault segments with mapped 1-5 km gaps (no surface expression)
- Select 15 true barrier controls (cross-cutting faults, different ages)
- Deploy temporary seismic stations across gaps (or use existing dense arrays)

**Measurement**:
1. Compute receiver functions at stations on both sides of each gap
2. Measure Ps delay time (indicates Moho depth)
3. Correlate receiver functions across gap
4. Test for continuous layering beneath gap

**Statistic**:
```
C_gap = Correlation(receiver_function_left, receiver_function_right)
C_barrier = Correlation(receiver_function_across_true_barrier)
```

**Prediction comparison**:

| View | Expected |
|------|----------|
| **Standard** | C_gap ≈ C_barrier (no continuous structure beneath gaps) |
| **Closure-grammar** | C_gap > C_barrier × 2 (continuous Moho beneath projection traps) |

**Success criterion**: Receiver function correlation significantly higher across gaps than across true barriers (t-test, p < 0.05)

**Failure mode**: No correlation difference → gaps are true structural breaks

---

## Prediction 2: Low-Amplitude Phase Corridors in Station Shadows

### Statement
In station gaps (shadow zones), weak but coherent seismic phases will be detectable via beamforming or matched filtering, revealing wave-field continuity invisible to standard picking algorithms.

### Standard View
Station gaps create data voids. No reliable seismic information without receiver coverage.

### Closure-Grammar View
Wave field continuous through gap; low-amplitude phases (mediators) carry connectivity information recoverable via processing.

### Falsifiable Test

**Setup**:
- Identify 10 events with azimuthal station gaps (>30° gap in coverage)
- Select 10 control events with complete azimuthal coverage
- Use dense array data (USArray, AlpArray, or similar)

**Measurement**:
1. Standard processing: Pick phases at stations (internal closure)
2. Extended processing: Beamform into gap azimuth; matched filter for weak phases
3. Measure signal coherence in gap direction
4. Compare apparent wave-field continuity

**Statistic**:
```
S_gap = Beamformed amplitude in gap direction / Noise level
S_control = Beamformed amplitude in covered direction / Noise level
Continuity_index = S_gap / S_control
```

**Prediction comparison**:

| View | Expected |
|------|----------|
| **Standard** | Continuity_index ≈ 1.0 (no excess signal in gaps) |
| **Closure-grammar** | Continuity_index > 1.5 (coherent wave field in gaps) |

**Success criterion**: Significant coherent energy in beamformed gap direction (SNR > 3)

**Failure mode**: No coherent signal in gaps → wave field truly discontinuous

---

## Prediction 3: True Barriers Resist Mediator Penetration

### Statement
True impedance boundaries (fluid bodies, core-mantle boundary, subduction slabs) will remain wave barriers even with aggressive mediator phase detection, while projection traps yield to mediator insertion.

### Standard View
All wave discontinuities are physical; no distinction between observation gaps and true barriers.

### Closure-Grammar View
Explicit distinction: projection traps yield to mediators; true barriers resist all phases.

### Falsifiable Test

**Setup**:
- Select 10 projection trap candidates (fault gaps with kinematic consistency)
- Select 10 true barrier candidates (fluid bodies, S-wave shadows, core reflections)
- Apply identical mediator detection protocol to both

**Measurement**:
1. Detect all possible phases: direct P, S, converted (Ps, Sp), coda, scattered
2. Count phases that successfully bridge each discontinuity
3. Measure phase amplitude relative to source

**Statistic**:
```
Bridgeability_trap = Number of mediator phases bridging gap / Total attempts
Bridgeability_barrier = Number of phases crossing barrier / Total attempts
Discrimination_ratio = Bridgeability_trap / Bridgeability_barrier
```

**Prediction comparison**:

| View | Expected |
|------|----------|
| **Standard** | No systematic difference between traps and barriers |
| **Closure-grammar** | Discrimination_ratio > 10 (traps bridgeable, barriers resist) |

**Success criterion**: Bridgeability significantly higher for traps than barriers (χ² test, p < 0.01)

**Failure mode**: Barriers bridgeable → no true distinction; method over-connects

---

## Smallest Falsifiable Wave Experiment

### Selected: Converted Phase Continuity Test (Prediction 1)

**Rationale**:
- Uses existing receiver function methodology
- Requires minimal new data (can use temporary deployments or existing arrays)
- Clear binary outcome (correlated vs. uncorrelated)
- Directly tests wave-field continuity beneath structural gaps

### Experiment: Ps Phase Correlation Across Fault Gaps

**Data requirements**:
- 3-component broadband seismic stations
- Stations positioned on both sides of mapped fault gaps
- Minimum 5 stations per gap crossing
- Recording duration: 6 months (teleseismic events)

**Procedure**:
1. Identify 10 candidate fault gaps (1-5 km, kinematic consistency)
2. Identify 5 true barrier controls (cross-cutting, opposing kinematics)
3. Compute receiver functions for all stations (Ps phase from Moho)
4. Cross-correlate receiver functions:
   - Within segments (baseline)
   - Across gaps (test)
   - Across barriers (control)
5. Measure correlation coefficient for each pair type

**Primary statistic**:
```
R_gap = Mean correlation across gaps
R_barrier = Mean correlation across barriers
Effect_size = (R_gap - R_barrier) / σ_pooled
```

**Prediction**:
| View | Expected |
|------|----------|
| **Standard** | R_gap ≈ R_barrier (no continuity beneath gaps) |
| **Closure-grammar** | R_gap > R_barrier + 0.3 (continuous Moho beneath gaps) |

**Success criteria**:
- Effect size > 0.8 (large effect)
- p < 0.05 (significant)
- Zero false positives (no barriers misclassified as bridgeable)

**Required sample**: 10 gaps, 5 barriers, 50 teleseismic events per station

**Timeline**: 6 months data + 2 months analysis

**Why this is smallest**:
- Standard receiver function methodology
- Existing station infrastructure (or small temporary deployment)
- Single statistical comparison
- Clear binary outcome
- Directly transferable to electron domain

---

## Validation Framework

### Joint Success Criteria

| Prediction | Success Metric | Threshold |
|------------|---------------|-----------|
| P1: Converted phase continuity | R_gap - R_barrier | > 0.3 |
| P2: Low-amplitude corridors | Continuity_index | > 1.5 |
| P3: Barrier resistance | Discrimination_ratio | > 10 |

### Outcome Interpretation

| P1 | P2 | P3 | Interpretation |
|----|----|----|----------------|
| ✓ | ✓ | ✓ | Closure grammar validated for seismic waves |
| ✓ | ✓ | ✗ | Method over-connects; barriers not discriminated |
| ✗ | ✓ | ✓ | Converted phases not primary mediators |
| ✗ | ✗ | ✓ | No wave-mediated continuity; gaps are true |

---

*Falsifiable wave tests: Closure grammar as operational seismology method*
