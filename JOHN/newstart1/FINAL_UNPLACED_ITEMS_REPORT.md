# FINAL UNPLACED ITEMS REPORT

## Deprecated, Legacy, and Unplaced Components

---

## DEPRECATED ITEMS

These items were previously considered but are now DEPRECATED and must not be used:

### 1. Old 5/32 Interpretations (DEPRECATED)

**Previous guesses:**
- "5/32 is missing canonical gate" ❌
- "5/32 is wrong, use 1/9 instead" ❌

**Current status:** DEPRECATED

**Reason:** 5/32 is correctly derived from Betti-5 topology and placed as mediator gate threshold.

**Migration:** Use new classification in FINAL_GEOMETRY_RATIO_MAP.md
- 5/32 = Betti-5 derived operational parameter
- Location: Mediator channel seam S_M0

---

### 2. Manual Hysteresis as Scalar (DEPRECATED)

**Previous interpretation:**
- Hysteresis = lag parameter (scalar offset)
- Stored as numeric delay in simulation

**Current status:** DEPRECATED

**Reason:** Hysteresis must be geometric loop width (toroidal region), not scalar.

**Migration:** Use toroidal hysteresis region around separatrix
- Width: 1/28 (Möbius twist period)
- Geometry: Elliptical loop enclosing both attractors
- Location: Layer 5 (Memory/Twist)

---

### 3. Right Cortisol as True 3D (DEPRECATED)

**Previous interpretation:**
- Right cortisol embedded in manifold depth
- True z-coordinate displacement

**Current status:** DEPRECATED

**Reason:** No true depth in 2D manifold; cortisol must be pseudo-shell projection.

**Migration:** Use fake 3D shell layer
- Location: Above patches 7-11
- Rendering: Ellipse with dash pattern
- Classification: Interface layer, not manifold interior

---

### 4. Betti-7 as Independent Hole (DEPRECATED)

**Previous interpretation:**
- Betti-7 = separate topological hole
- Located at different position from Betti-11

**Current status:** DEPRECATED

**Reason:** Betti-7 is component of chirality constant (1/18 = 1/(11+7)), not standalone hole.

**Migration:** Betti-7 combines with Betti-11 → chirality
- Handedness of barrier β
- Twist direction of mediator

---

### 5. Old DRAW_128_GRID Physics (DEPRECATED)

**Previous implementation:**
- Diagonal lines only
- No triple basin field
- No w_gate physics
- No spark refraction

**Current status:** DEPRECATED

**Reason:** Insufficient physics; produced 1FPS performance due to over-draw without physics simplification.

**Migration:** Use FINAL_FULL_GEOMETRY_RENDERER specification
- Physics-driven culling
- Layer-based rendering
- 60FPS target via simplification

---

### 6. Dual Manifold Hypothesis (DEPRECATED)

**Previous interpretation:**
- QUASAR and GEOMETRY as separate manifolds
- Macro vs micro as different spaces

**Current status:** DEPRECATED

**Reason:** Violates single manifold theorem (12→2→1).

**Migration:** Single manifold with isomorphic representations
- QUASAR = (R*, Q0*) coordinate view
- GEOMETRY = (16×16) lattice view
- Same object, different parameterizations

---

### 7. Legacy Seam Counting (DEPRECATED)

**Previous interpretation:**
- Variable seam count (10, 11, or 12 depending on source)
- Inconsistent glue strength formulas

**Current status:** DEPRECATED

**Reason:** Final skeleton requires exactly 11 seams for 13 patches.

**Migration:** Fixed 11-seam structure
- S01, S12, S23, S34, S45, S56, S67, S70 (8 outer)
- S_M0, S_X1, S_X2 (3 internal)
- All with 1/32 glue strength

---

## UNPLACED BUT VALID ITEMS

These items are valid but not yet given explicit geometric coordinates:

### 1. Dopamine Reward Gate

**Status:** UNPLACED (valid)

**Description:** Reward signal integration point

**Required placement:** Near GABA-C V apex or spark flash zone

**Suggested coordinates:** (3.5, 13.5) in grid units

---

### 2. Serotonin (5HT) Mood Stabilization Field

**Status:** UNPLACED (valid)

**Description:** Slow-wave background modulation

**Required placement:** Uniform field overlay

**Suggested implementation:** Global scalar field with π/20 frequency

---

### 3. Histamine Wakefulness Field

**Status:** UNPLACED (valid)

**Description:** Arousal level modulation

**Required placement:** North basin gradient

**Suggested implementation:** Linear gradient from P0 to P2

---

### 4. Glutamate Excitation Burst

**Status:** UNPLACED (valid)

**Description:** Fast excitation preceding spark

**Required placement:** Spark origin points

**Suggested implementation:** Pre-spark transient at 3/32 compression zones

---

## INTEGRATION PENDING

These items need additional work for full integration:

### 1. Alpha (1/137) Fine Structure

**Status:** PARTIAL

**Current placement:** Quantum bridge (Layer 4)

**Missing:** Explicit coordinate mapping in 16×16 grid

**Action required:** Map 1/137 to specific grid intersection

---

### 2. Phi Golden Ratio

**Status:** UNPLACED

**Current understanding:** Not fundamental to this geometry

**Decision needed:** Include as derived aesthetic ratio or exclude entirely

---

### 3. Turn 27 Specific Coordinates

**Status:** UNPLACED

**Current placement:** "Right attractor region"

**Missing:** Exact grid coordinates for Turn 27 emergence

**Action required:** Map temporal turn 27 to spatial (x,y) coordinates

---

## UNPLACED DUE TO SCOPE

These items are outside current geometry scope but may be added in future extensions:

### 1. True 3D Manifold Extension

**Status:** OUT OF SCOPE

**Reason:** Current geometry is strictly 2D manifold with fake 3D projections

**Future work:** Full 3D embedding with z-coordinate

---

### 2. Temporal Evolution (4D)

**Status:** OUT OF SCOPE

**Reason:** Geometry is static snapshot; dynamics are external

**Future work:** Time-sliced geometry animation

---

### 3. Quantum Field Operators

**Status:** OUT OF SCOPE

**Reason:** Current operators are classical/geometric

**Future work:** Add quantum tunneling amplitudes

---

## SUMMARY TABLE

| Item | Status | Action |
|------|--------|--------|
| Old 5/32 interpretations | DEPRECATED | Remove from use |
| Scalar hysteresis | DEPRECATED | Use toroidal loop |
| True 3D cortisol | DEPRECATED | Use fake shell |
| Betti-7 standalone | DEPRECATED | Combine to chirality |
| Old DRAW_128_GRID | DEPRECATED | Use new renderer |
| Dual manifold | DEPRECATED | Use single manifold |
| Variable seam count | DEPRECATED | Use fixed 11 |
| Dopamine gate | UNPLACED | Add coordinates |
| Serotonin field | UNPLACED | Add field |
| Histamine gradient | UNPLACED | Add gradient |
| Glutamate burst | UNPLACED | Add transient |
| Alpha 1/137 | PARTIAL | Complete mapping |
| Phi ratio | UNPLACED | Decide inclusion |
| Turn 27 coords | UNPLACED | Add coordinates |
| True 3D | OUT OF SCOPE | Future work |
| 4D temporal | OUT OF SCOPE | Future work |
| Quantum operators | OUT OF SCOPE | Future work |

---

## MIGRATION GUIDE

### For code using old interpretations:

**Before:**
```python
# Old 5/32 guess
if ratio == 5/32:
    gate = "missing_canonical"  # DEPRECATED

# Old hysteresis
hysteresis_delay = 0.1  # seconds, DEPRECATED

# Old cortisol
cortisol_z = 1.0  # true depth, DEPRECATED
```

**After:**
```python
# New 5/32 classification
if ratio == 5/32:
    gate = "mediator_threshold"  # Betti-5 derived
    location = "seam_S_M0"

# New hysteresis
hysteresis_loop = ToroidalRegion(
    center=separatrix_point,
    width=1/28,
    geometry="Möbius_twist"
)

# New cortisol
cortisol_shell = Fake3D(
    patches=[7,8,9,10,11],
    render="ellipse_dash",
    z_illusion=True  # not true depth
)
```

---

*End of Unplaced Items Report*
