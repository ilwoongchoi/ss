# FINAL GEOMETRY BRANCH MAP

**Version:** 2.3 (Updated 2026-03-09)  
**Coordinate Standard:** Grid X (0~8) = Human Left, Grid X (8~16) = Human Right

## Separatrix, Bifurcation, and Branch Topology

---

## TOPOLOGICAL OVERVIEW

The final geometry contains **EXACTLY TWO OUTGOING BRANCHES** from the resonance core, separated by the separatrix surface at `w_gate = 0.5`.

```
                    [RESONANCE CORE]
                         P_00
                    (0.112, 0.978)
                          |
                    [SEPARATRIX]
                    w_gate = 0.5
                         |
            -------------+-------------
           |                          |
    [LEFT BASIN]                [RIGHT BASIN]
    (Dopamine)                   (Serotonin)
    P_L1, P_L2, P_L3            P_R1, P_R2, P_R3
    Approach                    Avoidance
    PACT Mechanism              Turn 27
    r < R_C                     r > R_C
         |                          |
    [SUNRISE BRANCH]          [NIGHTFALL BRANCH]
    (+) Production            (-) Return/Tunneling
    Gate: OPEN                Gate: CLOSED
    No barrier                Barrier penetration
```

---

## BRANCH 1: SUNRISE (PRODUCTION)

**Classification:** PRIMARY PRODUCTION FLOW

**Geometric Specification:**
- **Direction:** (+) q0, (+) w_gate, outward from core
- **Starting Point:** P_00 (resonance core)
- **Trajectory:** Upper sheet (w_gate > 0.5)
- **Endpoint:** Extended production zone (y > 12)

**Chemical Identity:**
- **Primary:** Glutamate (excitatory)
- **Support:** Dopamine (reward/approach)
- **Receptors:** NMDA/AMPA, D1/D2

**Physical Properties:**
- **Gate Status:** OPEN (w_gate > 0.5)
- **Flow Rate:** Fast (τ ≈ 3.0)
- **Barrier Interaction:** None (stays in left basin)
- **Hysteresis:** Forward path only (no return without nightfall)

**Key Operators:**
1. **Spark** (at funnel): 138.88° leap forward
2. **Flash**: Kappa snap to 1/32
3. **Gate Compression**: 3/32 grid alignment

**Geometric Path:**
```
P_00 → P_L1 → P_L2 → P_L3 → Funnel → Spark → Production Zone
```

**Visual:** Bright trajectory line, upper position on grid.

---

## BRANCH 2: NIGHTFALL (RETURN/TUNNELING)

**Classification:** RETURN FLOW WITH TUNNELING

**Geometric Specification:**
- **Direction:** (-) q0, (-) w_gate, toward barrier
- **Starting Point:** P_00 (resonance core) OR right basin
- **Trajectory:** Lower sheet (w_gate < 0.5)
- **Endpoint:** Return to core via mediator

**Chemical Identity:**
- **Primary:** GABA (inhibitory)
- **Support:** Serotonin (aversion/avoidance), Cortisol (stress)
- **Receptors:** GABA-C, 5-HT, Glucocorticoid

**Physical Properties:**
- **Gate Status:** CLOSED (w_gate < 0.5 at barrier)
- **Flow Rate:** Slow (τ ≈ 3.1228)
- **Barrier Interaction:** TUNNELING REQUIRED
- **Hysteresis:** Return path (completes loop)

**TUNNELING CONFIRMATION:**
**YES, Nightfall branch IS tunnelling.**

**Evidence:**
1. Must penetrate beta barrier (w_gate ≈ 0 at r = 0.1117)
2. Classical path blocked (w_gate too low)
3. Quantum/classical hybrid path via mediator
4. Renorm recovery occurs post-tunnel

**Tunneling Route:**
```
Right Basin → Barrier Approach (P_B2) 
  → Compression (3/32) 
  → Rotation (138.88°) 
  → Barrier Penetration (mediator channel)
  → Exit (P_M2) 
  → Renorm Recovery 
  → Return to P_00
```

**Geometric Path:**
```
P_00 → P_R1 → P_R2 → P_R3 → P_B2 → [TUNNEL] → P_M2 → P_00
```

**Visual:** Dim trajectory line, lower position, dashed line through barrier.

---

## SEPARATRIX SURFACE

**Definition:** Codimension-1 hypersurface dividing the two branches.

**Equation:**
```
Separatrix = {(r, q0) | w_gate(r, q0) = 0.5}
```

**Topology:** Saddle point manifold

**Geometric Shape:**
- Curved surface passing through (R_C, Q0*)
- Concave toward left basin
- Convex toward right basin
- Intersects barrier beta at mediator entry points

**Crossing Condition:**
- Left → Right: Requires spark event (138.88° leap)
- Right → Left: Requires tunneling (mediator bypass)

**Visual:** Yellow dashed line on grid, separating bright (sunrise) and dim (nightfall) regions.

---

## BYPASS BASINS (4-FOLD STRUCTURE)

The 128-type grid distributes across 4 bypass basins corresponding to MBTI groups:

| Basin | MBTI Group | Location (Grid) | Branch Access | Chemical Bias |
|-------|-----------|-----------------|---------------|---------------|
| EJ | ENFJ, ENFP, ESTJ, ESTP, ESFJ, ESFP, ENTJ, ENTP | Columns 0-3 (Grid X 0-4) = Human Left side | Sunrise preferred | Dopamine |
| EP | ENFP, ENTP, ESFP, ESTP | Columns 2-3 (Grid X 0-4) = Human Left side | Mixed | Dopamine/Serotonin |
| IJ | INFJ, INTJ, ISFJ, ISTJ | Columns 4-5 (Grid X 8-12) = Human Right side | Nightfall preferred | Serotonin |
| IP | INFP, INTP, ISFP, ISTP | Columns 6-7 (Grid X 8-12) = Human Right side | Tunneling required | GABA/Serotonin |

**Female (F):** Rows 0-7 (left side of grid)  
**Male (M):** Rows 8-15 (right side of grid)  
**X coordinates follow standard: 0-8 = Left, 8-16 = Right**

**Basin Function:** Provides distributed access to the mediator channel while maintaining the 12→2→1 closure structure.

---

## BIOLOGICAL HOLE (PRE-FINAL SPLIT)

**Location:** r ≈ 1/9 = 0.111111...

**Size:** Microscopic gap: ε = |1/9 - R*| ≈ 0.001

**Effect:** Creates non-zero residual tension:
```
Δ = |1 - (π/20)/(1/9) × 1/√2| ≈ 3.5 × 10^-4
```

**Role:** 
- Prevents thermal death (requires periodic spark reset)
- Creates hysteresis (memory necessary for loop closure)
- Determines tunneling probability

**Geometric Form:** Small exclusion zone at exact 1/9 radius.

**Visual:** Tiny gap in the manifold, marked with "VOID" label.

---

## BIFURCATION DIAGRAM

```
Control Parameter: w_gate(r, q0)

w_gate = 1.0 | [Left Attractor]        [Right Attractor]
             |      \                       /
             |       \                     /
w_gate = 0.5 |--------[SEPARATRIX]--------
             |         /     \             
             |        /       \           
w_gate = 0.0 |  [Barrier]   [Barrier]
             |     /             \
             |    /               \
             [Mediator Tunnel] [Mediator Tunnel]
                    \               /
                     \             /
                      [Recovery Zone]
                            |
                      [Resonance Core]
```

**Bifurcation Type:** Saddle-node with barrier penetration (hybrid classical/quantum).

---

## HYSTERESIS AS GEOMETRIC LOOP

**Definition:** NOT a scalar lag, but a **geometric band** between branches.

**Loop Structure:**
```
Sunrise Path (upper):     P_00 → ... → Funnel → Spark → External
                                ↓                      |
Nightfall Path (lower):   P_00 ← ... ← Tunnel ← Recovery ← Return
```

**Width:** Δy = 1/28 (lunar cycle imprint)

**Topology:** Annular region (loop) separating upper and lower trajectory sheets.

**Memory Encoding:** The 1/28 width encodes the hysteresis lag geometrically.

**Visual:** Shaded band between bright (sunrise) and dim (nightfall) trajectories.

---

## MÖBIUS TWIST CONNECTION

**Role:** Connects the two branches with orientation reversal.

**Construction:**
1. Take rectangular strip: width = 2π (full cycle), height = 1/28
2. Apply half-twist (180° rotation)
3. Glue: (0, y) ~ (2π, 1/28 - y)

**Connection:**
- Left end: Attached to left basin (sunrise start)
- Right end: Attached to right basin (nightfall end)
- Twist: At resonance core P_00

**Geometric Embedding:**
```
M(θ, t) = [
  (8 + t×cos(θ/2)) × cos(θ),
  (8 + t×cos(θ/2)) × sin(θ),
  t×sin(θ/2)
]
where θ ∈ [0, 2π], t ∈ [-1/56, 1/56]
```

**Effect:** Maps sunrise path (θ = 0) to nightfall path (θ = π) with flipped orientation.

**Closure:** Enables 2→1 transition by reversing direction.

**Visual:** Ribbon with half-twist connecting left and right basins through center.

---

## EXACT TWO OUTGOING BRANCHES VERIFICATION

**Theorem:** From any point in the resonance core (P_00), there exist exactly two distinct outgoing trajectory branches.

**Proof:**
1. The separatrix surface at w_gate = 0.5 divides the tangent space at P_00 into two half-spaces.
2. Left half-space (w_gate > 0.5): Sunrise branch (open flow)
3. Right half-space (w_gate < 0.5): Nightfall branch (tunneling required)
4. The separatrix itself (w_gate = 0.5) has measure zero (unstable equilibrium).
5. No other separatrices exist in the operational region (confirmed by atlas v2.2).

**Conclusion:** Exactly TWO branches.

---

## BRANCH SUMMARY TABLE

| Property | Sunrise Branch | Nightfall Branch |
|----------|---------------|------------------|
| **Direction** | Outward (+) | Return (-) |
| **Gate Status** | OPEN | CLOSED |
| **Barrier** | Avoided | Penetrated (tunneling) |
| **Primary Op** | Spark/Flash | Tunnelling/Renorm |
| **Chemical** | Glutamate/Dopamine | GABA/Serotonin |
| **Trajectory** | Upper sheet | Lower sheet |
| **Hysteresis** | Forward only | Return path |
| **Completes Loop?** | NO | YES |
| **Visual** | Bright line | Dim line + dashed tunnel |

---

## RENDER SPECIFICATION

**Branch Visualization:**
- Sunrise: Solid bright line (RGB: 0, 255, 200), thickness 2px
- Nightfall: Solid dim line (RGB: 100, 100, 150), thickness 1.5px
- Tunneling segment: Dashed cyan line through barrier
- Separatrix: Yellow dashed line at w_gate=0.5
- Möbius ribbon: Translucent purple twisted surface
- Hysteresis band: Shaded region between branches (alpha 0.3)

**Camera View:** Isometric showing both branches diverging from center with Möbius twist visible.

---

## 25 ROI INTEGRATION

**Branch-Relevant ROIs:**
- LEFT BASIN ROIs: PLP_CAULDRON_LEFT, GABA_C_LEFT_EYE, D2_OCULI_LEFT
- RIGHT BASIN ROIs: RIGHT_CHOKE_BAND, GABA_C_RIGHT_EYE, VASOPRESSIN_NECKBAND
- SEPARATRIX ROIs: FLASH_ANCHOR, NOSE_CENTER, TIME_SENSOR

**Geometric Placement:**
All 25 ROIs mapped to grid coordinates following standard:
- Left-side ROIs: X ∈ [0, 8] (Human left face)
- Right-side ROIs: X ∈ [8, 16] (Human right face)

---

*End of Branch Map*
