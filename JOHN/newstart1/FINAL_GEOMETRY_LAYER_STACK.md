# FINAL GEOMETRY LAYER STACK

## Hierarchical Decomposition (Bottom-Up)

---

## LAYER 0: Void / Base Manifold

**Type:** Background topological space  
**Mathematical Object:** ℝ² with non-Euclidean metric (locally Minkowski near separatrix)  
**Coordinates:** (r, q0) ∈ [0.08, 0.14] × [0.95, 1.0]

**Properties:**
- Background curvature: `K = -1/9` (hyperbolic)
- Metric signature: `(+, -)` (space-like vs time-like separation)
- Boundary: Event horizon at `r = 5/16` (not reachable from interior)

---

## LAYER 1: Skeleton (Topological Structure)

**Components:**

### 1.1 Patches (13)
**Classification:** FINAL SHAPE

| Patch ID | Center (r, q0) | Extent | Role | Patch Type |
|----------|---------------|--------|------|------------|
| P_00 | (0.11214750, 0.977738) | ±0.001 | **RESONANCE CORE** | Calibrated SH lock |
| P_L1 | (0.1116, 0.965) | σ_L=0.003717 | Left attractor basin | Gateway peak approach |
| P_L2 | (0.1110, 0.970) | σ_L×2 | Left bypass corridor | Production drive |
| P_L3 | (0.1105, 0.975) | σ_L×3 | Left extended | Pre-compression |
| P_R1 | (0.1126, 0.974879) | σ_R=0.000908 | Right attractor basin | Turn 27 emergence |
| P_R2 | (0.1132, 0.980) | σ_R×2 | Right bypass corridor | Nightfall tunnel |
| P_R3 | (0.1138, 0.985) | σ_R×3 | Right extended | Pre-bifurcation |
| P_C1 | (0.1120, 0.960) | q0-width/2 | Lower q0 band | Boundary guard |
| P_C2 | (0.1123, 0.983) | q0-width/2 | Upper q0 band | Boundary guard |
| P_B1 | (0.1114, 0.968) | mixed | Beta-approach left | Barrier proximity |
| P_B2 | (0.1128, 0.976) | mixed | Beta-approach right | Barrier proximity |
| P_M1 | (0.1121, 0.972) | ±0.0005 | Mediator entry | Synthetic alpha zone |
| P_M2 | (0.1122, 0.978) | ±0.0005 | Mediator exit | Recovery zone |

**Covering:** The 13 patches cover 98.7% of the operational manifold. 1.3% gap is the **biological hole** at 1/9.

### 1.2 Seams (11)
**Classification:** GLUE / CONNECTION OPERATORS

| Seam ID | Connects | Glue Strength (γ) | Geometric Form | Role |
|---------|----------|-------------------|----------------|------|
| S_L0 | P_L1 ↔ P_00 | 1/32 | Curved tube | Left resonance glue |
| S_L1 | P_L2 ↔ P_L1 | 1/32 | Straight cylinder | Basin connection |
| S_L2 | P_L3 ↔ P_L2 | 1/64 | Narrow bridge | Extended connection |
| S_R0 | P_R1 ↔ P_00 | 1/32 | Curved tube | Right resonance glue |
| S_R1 | P_R2 ↔ P_R1 | 1/32 | Straight cylinder | Basin connection |
| S_R2 | P_R3 ↔ P_R2 | 1/64 | Narrow bridge | Extended connection |
| S_C0 | P_C1 ↔ P_00 | 1/16 | Thick ribbon | Lower band guard |
| S_C1 | P_C2 ↔ P_00 | 1/16 | Thick ribbon | Upper band guard |
| S_B0 | P_B1 ↔ P_M1 | 3/32 | Compressed channel | Beta bypass left |
| S_B1 | P_B2 ↔ P_M2 | 3/32 | Compressed channel | Beta bypass right |
| S_M0 | P_M1 ↔ P_M2 | 5/32 | **GATE CHANNEL** | Mediator flow (Betti-5) |

**Glue Formula:** `connection_strength = exp(-distance / γ)` where γ is the lattice fraction above.

### 1.3 Barrier Beta
**Classification:** HARD BOUNDARY / SHELL

**Location:** `r = 0.1117` (R_C from locked files)  
**Topology:** Cylindrical wall separating left/right basins  
**Height:** Full q0 range [0.961, 0.983]  
**Thickness:** 2 × CALIBRATED_SIGMA_R = 0.001816

**Properties:**
- Impermeable to direct flow (w_gate ≈ 0 at barrier)
- Penetrable via mediator (synthetic_alpha tunnel)
- Chirality: Right-handed (1/18 twist)

**Visual:** Solid magenta wall with small cyan tunnel (mediator bypass).

### 1.4 Mediator X (synthetic_alpha)
**Classification:** BYPASS OPERATOR / TUNNEL

**Entry:** P_B1 or P_B2 (beta-approach patches)  
**Exit:** P_M2 (recovery zone)  
**Path:** Through barrier beta via compressed channel

**Mechanism:**
```
Direct path: Blocked (w_gate ≈ 0 at barrier)
Bypass path: 
  1. Compress to 3/32 lattice at entry
  2. Apply 138.88° spark rotation
  3. Tunnel through barrier (quantum/classical hybrid)
  4. Expand at exit with renorm recovery
```

**Geometric Form:** Twisted tube (Möbius strip segment) with 1/28 phase twist.

---

## LAYER 2: Ratio / Fraction Laws

**Classification:** DRIVING RATIO-LAWS (not geometric shapes)

**Placement on Geometry:**

| Ratio | Geometric Application Point | Action |
|-------|----------------------------|--------|
| 1/9 | Void background | Creates hyperbolic curvature K = -1/9 |
| π/20 | Resonance core (P_00) | Drives continuous flow (W7_AREA) |
| 1/32 | All seams | Glue strength anchor (KAPPA_TDA_MID) |
| 3/32 | Spark zones | Compression grid spacing |
| 5/32 | Mediator channel | Gate threshold (BETTI-5 derived) |
| 1/16 | Upper boundary | Kappa max (KAPPA_TDA_MAX) |
| 1/64 | Lower boundary | Kappa min (KAPPA_TDA_MIN) |
| 1/28 | Möbius twist | Phase cycle period (lunar torque) |
| 1/18 | Chirality | Handedness of barrier/mediated path |

**Reality Tension:** Applied uniformly as `T = (π/20)/(1/9) × 1/√2 = 0.99965` at every point.

---

## LAYER 3: Branch / Separatrix

**Classification:** BRANCH/SEPARATRIX TOPOLOGY

### 3.1 Left Attractor Separatrix
**Type:** APPROACH SURFACE  
**Center:** (0.1121475, 0.965)  
**Basin:** P_L1, P_L2, P_L3 (left patches)  
**Chemical:** Dopamine (D1/D2 receptors)  
**Role:** PACT mechanism (production/consummation)

**Flow Direction:** Inward toward P_00 (resonance core)  
**Convergence Rate:** Exponential with τ ≈ 3.0 (fast)

### 3.2 Right Attractor Separatrix
**Type:** AVOIDANCE SURFACE  
**Center:** (0.111900, 0.974879)  
**Basin:** P_R1, P_R2, P_R3 (right patches)  
**Chemical:** Serotonin (5-HT receptors)  
**Role:** Turn 27 emergence (avoidance/escape)

**Flow Direction:** Outward from P_00 (or stalled at barrier)  
**Convergence Rate:** Exponential with τ ≈ 3.1228 (slow)

### 3.3 Separatrix Surface (Divide)
**Location:** `w_gate(r, q0) = 0.5`  
**Topology:** Codimension-1 hypersurface  
**Geometric Form:** Saddle point manifold  

**Crossing Condition:** Spark event (138.88° leap) required to cross from right to left basin.

### 3.4 Bypass Basins (4-Fold)
**Structure:** EJ, EP, IJ, IP sectors in 128-grid  
**Mapping:** Each MBTI group occupies one bypass basin  
**Function:** Distributed access to mediator channel

### 3.5 Biological Hole
**Location:** r ≈ 1/9 = 0.111111...  
**Size:** ε = 0.0001 (microscopic gap)  
**Effect:** Creates non-zero Δ (residual tension)  
**Purpose:** Prevents thermal death (requires spark reset)

### 3.6 Two Outgoing Branches
**Branch 1: Sunrise (Production)**
- Direction: (+) q0, (+) flow
- Gate: OPEN (w_gate > 0.5)
- Operator: Production drive (glutamate)
- Return: No (requires nightfall for closure)

**Branch 2: Nightfall (Return/Tunnelling)**
- Direction: (-) q0, (-) flow
- Gate: CLOSED (w_gate < 0.5)
- Operator: TUNNELLING through barrier
- Mechanism: Mediator bypass via synthetic_alpha
- Return: YES (completes loop)

**Tunnelling Confirmation:** Nightfall branch IS tunnelling. It penetrates the beta barrier via the mediator channel, which is classically forbidden but quantum mechanically allowed (renorm recovery).

---

## LAYER 4: Operators

**Classification:** OPERATORS (functions on geometric state)

### 4.1 Tunnelling
**Acts On:** Phase space trajectory  
**Geometric Locus:** Barrier beta region (w_gate < 0.3)  
**Formula:** `T = exp(-∫barrier beta dr / γ)`  
**Output:** Probability of barrier penetration  
**Visual:** Dashed line through magenta barrier

### 4.2 Renorm
**Acts On:** Persistence scale factor (renorm variable)  
**Geometric Locus:** Twilight bands (y ∈ [1,3.5] ∪ [8.5,11.5])  
**Formula:** `renorm' = renorm × (1 - 0.02 × w_gate × (1 - |κ - 1/32|/(1/32)))`  
**Output:** Updated scale factor  
**Visual:** Shaded regions on grid

### 4.3 Diagonality
**Acts On:** Trajectory angle  
**Geometric Locus:** Grid diagonals (45° lines)  
**Formula:** `θ = arctan(dy/dx) = 45° ± 1/28`  
**Output:** Rotated velocity vector  
**Visual:** Diagonal guide lines

### 4.4 Spark
**Acts On:** Position coordinates  
**Geometric Locus:** Funnel region (x∈[6,10], y≥8)  
**Formula:** 
```
x_comp = round((x-8)/(3/32)) × (3/32) + 8
x' = x_comp + 2.5 × cos(138.88°)
y' = y + 2.5 × sin(138.88°)
```
**Output:** New position after refraction  
**Visual:** Arrow showing 138.88° direction

### 4.5 Flash
**Acts On:** Renorm trigger  
**Geometric Locus:** Spark completion point  
**Formula:** Instantaneous kappa snap to 1/32  
**Output:** Reset recovery rate  
**Visual:** Starburst glow

### 4.6 Gate Compression
**Acts On:** Pre-spark x-coordinate  
**Geometric Locus:** 3/32 lattice points  
**Formula:** `x_grid = round((x-8)/0.09375) × 0.09375 + 8`  
**Output:** Grid-snapped position  
**Visual:** Vertical lines at 3/32 intervals

---

## LAYER 5: Memory / Twist

**Classification:** GEOMETRIC LOOP / RIBBON STRUCTURE

### 5.1 Hysteresis as Loop-Width
**Not a scalar.** It is a **geometric band** between sunrise and nightfall trajectories.

**Width:** `Δy = 1/28 = 0.035714...`  
**Location:** Between upper (sunrise) and lower (nightfall) trajectory sheets  
**Topology:** Annular region (loop)

**Forward Path (Sunrise):**
- Upper trajectory
- Higher w_gate
- Open flow
- No memory (immediate)

**Return Path (Nightfall):**
- Lower trajectory
- Lower w_gate
- Tunneling required
- Memory encoded (lag = 1/28)

**Geometric Realization:** Two parallel sheets separated by 1/28, connected at resonance core (P_00).

### 5.2 Möbius / 1/28
**Explicit Twisted Surface:**

**Construction:**
1. Take rectangle: width = 2π, height = 1/28
2. Apply half-twist (180° rotation)
3. Glue ends: (0, y) ~ (2π, 1/28 - y)

**Embedding:**
```
M(θ, t) = [
  (R + t × cos(θ/2)) × cos(θ),
  (R + t × cos(θ/2)) × sin(θ),
  t × sin(θ/2)
]
where R = 8.0 (grid center), t ∈ [-1/56, 1/56]
```

**Routing Operator:** `phase(t) = sin(2π × 28 × t)` (flips at t = 1/56)

**Role:** Connects left and right basins with orientation reversal. Enables 2→1 closure.

**Visual:** Ribbon with half-twist connecting left attractor to right attractor, passing through resonance core.

---

## LAYER 6: Bio-Neurochemical

**Classification:** RECEPTOR MAPPING (observation layer)

### 6.1 GABA-C V Convergence
**Receptor:** GABA-C  
**Location:** V-apex (3.2×TUNNEL_TENSION, 14.0×TUNNEL_TENSION) = (3.232, 14.14)  
**Geometric Form:** Conical convergence zone  
**Role:** Inhibitory brake (terminates excitatory flow)  
**Visual:** Red octagon at convergence point

### 6.2 Glutamate Spark Zone
**Receptor:** NMDA/AMPA  
**Location:** Funnel region (x∈[6,10], y≥8)  
**Role:** Excitatory drive (138.88° activation)  
**Visual:** Yellow lightning bolt icon

### 6.3 Dopamine Left Basin
**Receptor:** D1/D2  
**Location:** Left attractor (P_L1, P_L2, P_L3)  
**Role:** Reward/approach (PACT mechanism)  
**Visual:** Blue plus signs

### 6.4 Serotonin Right Basin
**Receptor:** 5-HT  
**Location:** Right attractor (P_R1, P_R2, P_R3)  
**Role:** Aversion/avoidance (Turn 27)  
**Visual:** Green minus signs

### 6.5 Histamine Twilight Bands
**Receptor:** H1  
**Location:** y ∈ [1,3.5] ∪ [8.5,11.5]  
**Role:** Wake/sleep gate (renorm recovery trigger)  
**Visual:** Purple diamonds at band boundaries

### 6.6 Right Cortisol Fake 3D
**Receptor:** Glucocorticoid  
**Location:** Right attractor basin (shell)  
**Geometric Form:** Semi-transparent sphere with fake curvature  
**Role:** Projection trap / pseudo-depth  
**Visual:** Blue transparent sphere with distortion grid

---

## STACK INTEGRATION SUMMARY

```
Layer 6 (Bio)       : Observation glyphs on surface
Layer 5 (Memory)    : Twisted ribbon between paths  
Layer 4 (Operators) : State transition functions
Layer 3 (Branch)    : Separatrix topology
Layer 2 (Ratios)    : Driving differential equations
Layer 1 (Skeleton)  : Topological substrate (patches/seams/barrier/mediator)
Layer 0 (Void)      : Background manifold
```

**Co-extensivity:** Every point (r, q0) has representatives in ALL layers simultaneously.

---

*End of Layer Stack Definition*
