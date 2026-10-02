# Geology/Seismology Pilot Experiment
## Fault Continuity Reconstruction Under Sparse Observation

---

## Selected Target: San Andreas Fault Step-Over with Seismic Gap

**Rationale**: 
- Well-studied system with known segmented structure
- Clear surface gaps (Pinto Mountain, San Gorgonio Pass)
- Extensive subsurface data (seismic profiles, microseismicity)
- Active research community for validation

**Alternative (smaller scale)**: Wasatch Fault segments with buried connection

---

## Experiment Design

### Research Question
Can closure grammar reconstruct fault continuity across surface gaps better than standard geological mapping while correctly identifying true structural barriers?

### Unit of Analysis
Individual fault segment pair with intervening gap

### Data Types
1. **Surface geology**: USGS Quaternary fault database, aerial imagery
2. **Seismology**: ANSS earthquake catalog, focal mechanisms
3. **Geodesy**: InSAR (Sentinel-1), GPS station velocities
4. **Geophysics**: Seismic reflection profiles, gravity/magnetic data

---

## Gap Definition

### Type 1: Projection Trap (Test Case)
- Surface gap < 5 km along strike
- Consistent kinematics on both sides
- Young (Quaternary) displacement on adjacent segments
- No cross-cutting relationships

### Type 2: True Barrier (Control Case)
- Structural offset > 10 km
- Opposing or inconsistent kinematics
- Cross-cutting relationships documented
- Different basement terranes

### Type 3: Ambiguous Gap (Validation Case)
- Intermediate geometry requiring interpretation
- Used to test predictive power

---

## Matched Controls

For each projection trap (Type 1):
- Select Type 2 true barrier with similar gap length
- Select Type 3 ambiguous gap for blind prediction
- Match on: gap length, cover type, tectonic setting

---

## Procedure

### Phase 1: Internal Closure (Standard Mapping)

1. Map all surface fault segments in study area
2. Build DSU with bridges based on:
   - Strike alignment (±15°)
   - Kinematic consistency
   - Gap length (< 5 km for initial bridge)
3. Count components after internal closure

**Expected**: 2+ components (connected clusters + isolated segments)

### Phase 2: Extended Closure (Mediator Insertion)

For each Type 1 gap:
1. Identify potential mediators:
   - Microseismicity clusters beneath gap
   - InSAR displacement gradients
   - Seismic velocity anomalies
2. Insert minimal mediator (strongest evidence)
3. Test bridge activation
4. Recompute components

**Expected**: Some 2→1 reductions (projection traps resolved)

### Phase 3: True Barrier Verification

For each Type 2 barrier:
1. Attempt mediator insertion
2. Verify that:
   - No microseismicity corridor exists
   - InSAR shows discontinuity
   - Structural evidence contradicts connection

**Expected**: 0 reductions (barriers remain)

---

## Primary Statistic

**Component Reduction Ratio (CRR)**:
```
CRR = (Components_internal - Components_extended) / Components_internal
```

**Prediction**:
- Projection traps (Type 1): CRR > 0 (reduction occurs)
- True barriers (Type 2): CRR = 0 (no reduction)
- Significance: Mann-Whitney U test comparing Type 1 vs. Type 2 CRR

---

## Artifact Checks

### Check 1: Over-connection Bias
- Blind test: Remove gap labels, have independent analyst classify
- Verify Type 2 barriers are never falsely connected

### Check 2: Data Snooping
- Split data: Use historical maps only for internal closure
- Reserve modern InSAR/seismic for extended closure validation

### Check 3: Tectonic Setting
- Ensure Type 1 and Type 2 gaps distributed across different settings
- Control for regional strain rate, lithology, cover thickness

### Check 4: Minimum Gap Size
- Exclude gaps < 1 km (may be erosional rather than structural)
- Exclude gaps > 15 km (unlikely to be projection traps)

---

## Success Criteria

### Primary Success
- Type 1 gaps show significantly higher CRR than Type 2 (p < 0.05)
- No Type 2 barriers incorrectly connected (false positive rate = 0)

### Secondary Success
- Predict Type 3 ambiguous gaps correctly (> 70% accuracy)
- Seismic corridor detection rate > 50% for Type 1 gaps

### Failure Modes
- No difference between Type 1 and Type 2 CRR → closure grammar not applicable
- High false positive rate → method over-connects
- Mediator evidence absent → projection traps may be true breaks

---

## Required Sample Size

**Power analysis**:
- Effect size: d = 0.8 (large difference in CRR)
- α = 0.05, β = 0.20
- Required: n = 21 per group (Type 1, Type 2)

**Practical target**:
- 25 projection trap candidates
- 25 true barrier controls
- 15 ambiguous validation cases

---

## Timeline

| Phase | Duration | Activity |
|-------|----------|----------|
| 1 | 2 months | Data compilation, segment mapping |
| 2 | 1 month | Internal closure analysis |
| 3 | 2 months | Mediator identification, extended closure |
| 4 | 1 month | Validation, blind testing |
| 5 | 1 month | Analysis, manuscript |

**Total**: 7 months for pilot study

---

*Pilot experiment: Fault continuity reconstruction via closure grammar*
