# Geology/Seismology Falsifiable Predictions

## Core Hypothesis

> **Apparent geological discontinuities are not always true breaks; some are projection-trapped gaps whose continuity can be recovered by minimal mediator insertion, while true barriers remain uncrossable even under extended closure.**

---

## Prediction 1: Projection Traps Show Latent Corridor Signal

### Statement
Surface gaps classified as projection traps (consistent kinematics, no cross-cutting) will show subsurface structural evidence (seismic corridor, microseismicity, InSAR gradient) significantly more often than matched control gaps in non-faulted terrain.

### Standard View
Surface gaps represent true fault terminations or complex distributed deformation. Subsurface structure beneath gaps will be indistinguishable from background.

### Closure-Grammar View
Projection traps mask through-going structure. Subsurface corridors (latent mediators) will be detectable beneath gaps.

### Falsifiable Test

**Setup**:
- Select 20 fault segment pairs with 1-5 km gaps and kinematic consistency
- Select 20 matched control locations in non-faulted terrain with similar cover

**Measurement**:
- Microseismicity density within 2 km of gap centerline
- InSAR strain rate across gap
- Seismic velocity anomaly beneath gap

**Statistic**:
```
S_gap = Σ(microseismic events along trend) / (gap length × observation time)
S_control = matched calculation for control locations
```

**Prediction comparison**:

| View | Expected Result |
|------|-----------------|
| **Standard** | S_gap ≈ S_control (no excess structure) |
| **Closure-grammar** | S_gap > S_control × 2 (latent corridor present) |

**Success criterion**: Mann-Whitney U test, p < 0.05 for S_gap > S_control

**Failure mode**: No significant difference → gaps are true terminations

---

## Prediction 2: Mediator-Assisted Reconstruction Reduces Component Count

### Statement
Extended closure (including subsurface mediators) will achieve significantly greater component reduction (more gaps bridged) than internal closure (surface mapping only), while true barriers remain resistant.

### Standard View
Additional subsurface data may fill gaps but will not systematically reduce component count beyond what careful surface mapping achieves.

### Closure-Grammar View
Systematic mediator insertion will specifically target projection traps and achieve measurable reduction in disconnected components.

### Falsifiable Test

**Setup**:
- Define study region with N known fault segments
- Classify gaps as: Type 1 (projection trap), Type 2 (true barrier), Type 3 (ambiguous)

**Phase 1 (Internal)**:
- Map using surface geology only
- Build DSU with strike-alignment bridges
- Count components C_internal

**Phase 2 (Extended)**:
- Add seismic/InSAR mediators for Type 1 gaps
- Recompute DSU
- Count components C_extended

**Statistic**:
```
Reduction_internal = (N_initial - C_internal) / N_initial
Reduction_extended = (N_initial - C_extended) / N_initial
ΔReduction = Reduction_extended - Reduction_internal
```

**Prediction comparison**:

| View | Expected Result |
|------|-----------------|
| **Standard** | ΔReduction ≈ 0 (subsurface adds no new connections) |
| **Closure-grammar** | ΔReduction > 0.15 (15% more reduction via mediators) |

**Success criterion**: ΔReduction > 0.15 with p < 0.05 (bootstrap resampling)

**Failure mode**: ΔReduction ≈ 0 → subsurface structure does not enable new connections

---

## Prediction 3: True Barriers Remain Resistant to Over-Connection

### Statement
True structural barriers (cross-cutting relationships, opposing kinematics) will show zero component reduction even under aggressive mediator insertion, preventing false over-connection that would invalidate the method.

### Standard View
Any continuity method risks over-connecting truly separate structures. Validation requires independent evidence.

### Closure-Grammar View
The method explicitly distinguishes projection traps (bridgeable) from true barriers (uncrossable). True barriers will resist all bridge attempts.

### Falsifiable Test

**Setup**:
- Identify 15 true barrier locations (cross-cutting faults, opposing kinematics)
- Apply identical mediator insertion protocol as for projection traps

**Measurement**:
- Attempt bridge formation for each barrier
- Record bridge success/failure
- Verify with independent structural evidence

**Statistic**:
```
False_positive_rate = (barriers incorrectly connected) / (total barriers)
```

**Prediction comparison**:

| View | Expected Result |
|------|-----------------|
| **Standard** | False positives possible without careful validation |
| **Closure-grammar** | False_positive_rate = 0 (barriers uncrossable) |

**Success criterion**: Zero false positives in 15 barrier tests

**Failure mode**: Any false positive → method lacks discrimination power

---

## Combined Validation Framework

### Joint Prediction
Closure grammar will simultaneously achieve:
1. **Sensitivity**: > 50% of projection traps show mediator evidence
2. **Specificity**: 100% of true barriers remain unconnected
3. **Efficiency**: Component reduction exceeds standard mapping by > 15%

### Decision Matrix

| Result | Interpretation |
|--------|----------------|
| P1 + P2 + P3 all pass | Closure grammar validated as general method |
| P1 + P2 pass, P3 fails | Method over-connects; lacks barrier discrimination |
| P1 fails, P2 + P3 pass | Subsurface structure present but not mediator-like |
| All fail | Closure grammar not applicable to geology |

---

## Minimal Falsifiable Experiment Summary

**Smallest test**: Prediction 1 (Latent corridor signal)

**Requirements**:
- 20 fault gaps (1-5 km, kinematically consistent)
- 20 matched controls
- Earthquake catalog (ANSS or regional network)
- 2 weeks analysis time

**Outcome**:
- **Positive**: S_gap > 2× S_control → Supports closure grammar
- **Negative**: S_gap ≈ S_control → Projection traps are true breaks

**Why this is minimal**:
- Uses existing public data (no fieldwork)
- Single statistical test
- Clear binary outcome
- Extends directly to full pilot if successful

---

*Falsifiable predictions: Closure grammar as testable geological method*
