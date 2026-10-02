# FINAL GEOMETRY RECEPTOR MAP

**Version:** 2.3 (Updated 2026-03-09)
**Coordinate Standard:** Grid X (0~8) = Human Left, Grid X (8~16) = Human Right

## Bio-Neurochemical Layer Integration

---

## RECEPTOR PLACEMENT SUMMARY

**Principle:** Every neurochemical receptor type maps to a specific geometric locus on the final manifold.

| Chemical | Receptor | Geometric Locus | Coordinates | Classification |
|----------|----------|----------------|-------------|----------------|
| **GABA** | GABA-C | V-Apex Convergence | (3.232, 14.14) | **SHELL / CONVERGENCE POINT** |
| **Glutamate** | NMDA/AMPA | Spark Trigger Zone | x∈[6,10], y≥8 | **OPERATOR ZONE** |
| **Dopamine** | D1/D2 | Left Attractor Basin | r<0.1117, q0<0.972 | **BASIN** |
| **Serotonin** | 5-HT | Right Attractor Basin | r>0.1117, q0>0.972 | **BASIN** |
| **Histamine** | H1 | Twilight Band Boundaries | y=1,3.5,8.5,11.5 | **BOUNDARY** |
| **Cortisol** | Glucocorticoid | Right Cortisol Shell | r=0.112, q0=0.975 | **FAKE 3D SHELL** |

---

## 1. GABA-C V-CONVERGENCE

**Classification:** FINAL GEOMETRY NODE / CONVERGENCE SHELL

**Location:**
- Cartesian: (3.2 × TUNNEL_TENSION, 14.0 × TUNNEL_TENSION)
- Exact: **(3.23212, 14.140525)**
- Grid: Approximately (3.2, 14.1) on 16×16 grid

**Geometric Form:**
```
V-Apex = {
  shape: Conical convergence,
  apex: (3.232, 14.14),
  opening_angle: 2 × arctan(1/9),
  depth: 1/32,
  base_radius: 3/32
}
```

**Role in Closure:**
- **Inhibitory Brake:** Terminates excitatory glutamate flow
- **Convergence Point:** All trajectories approach here
- **GABA-C specifically:** The "C" subtype (distinct from A and B)
- **V-shape:** Creates potential well for final settling

**Integration with Physics:**
```
V_shape(x, y) = exp(-r² / (2 × GABA_C_V_APEX²))
where:
  - r² = ((x-3.232)/8)² + ((y-14.14)/8)²
  - GABA_C_V_APEX = 1.40488 / 10 = 0.140488
```

**Visual Representation:**
- Red octagon at convergence point
- Red shaded cone showing potential well
- Label: "GABA-C V-CONVERGENCE / INHIBITORY BRAKE"

**Neurochemical Function:**
- Receives excitatory input from glutamate spark zones
- Provides negative feedback to prevent runaway excitation
- Enables loop closure by "stopping" the forward trajectory

---

## 2. GLUTAMATE SPARK ZONE

**Classification:** OPERATOR ZONE / TRIGGER REGION

**Location:**
- Grid Region: Funnel (x ∈ [6, 10], y ≥ 8)
- Gate: w_gate > 0.5
- Switch: Hysteresis state = True

**Geometric Form:**
```
Spark_Zone = {
  shape: Rectangular funnel,
  x_range: [6.0, 10.0],
  y_min: 8.0,
  y_max: 16.0,
  trigger: switch_state AND in_funnel
}
```

**Receptor Types:**
- **NMDA:** Voltage-gated, requires depolarization
- **AMPA:** Fast excitatory, primary current

**Role in Geometry:**
- **Excitatory Drive:** Powers the 138.88° spark leap
- **Production:** Drives sunrise branch forward
- **Trigger:** Initiates state transition (spark operator)

**Integration with Physics:**
```
Glutamate_activation = {
  angle: 138.88°,
  leap: 2.5 units,
  compression: 3/32 grid,
  result: Phase transition to new position
}
```

**Visual Representation:**
- Yellow lightning bolt icons at trigger points
- Yellow shaded funnel region
- Arrows showing 138.88° direction
- Label: "GLUTAMATE / NMDA-AMPA / SPARK TRIGGER"

**Neurochemical Function:**
- Fast excitatory neurotransmitter
- Drives production and approach behaviors
- Coupled to spark refraction mechanism

---

## 3. DOPAMINE LEFT BASIN

**Classification:** BASIN / ATTRACTOR REGION

**Location:**
- Center: (0.1121475, 0.965)
- Basin: P_L1, P_L2, P_L3 (left patches)
- r < R_C (left of barrier beta)
- q0 < Q0* (below resonance)

**Geometric Form:**
```
Left_Basin = {
  center: LEFT_CORTISOL_R = 0.1121475,
  q0: LEFT_CORTISOL_Q0 = 0.965,
  extent: sigma_L = 0.003717,
  shape: Asymmetric Gaussian (left-skewed),
  receptor: D1/D2
}
```

**Receptor Types:**
- **D1:** Excitatory, reward expectation
- **D2:** Inhibitory, reward prediction error

**Role in Geometry:**
- **Reward/Approach:** PACT mechanism (Production, Approach, Consummation, Termination)
- **Left Attractor:** Pulls trajectories toward (0.112, 0.965)
- **Sunrise Origin:** Primary source of sunrise branch trajectories

**Integration with Physics:**
```
Dopamine_drive = {
  w_gate_weight: High (0.7 - 1.0),
  kappa: Near 1/32 (stable),
  flow: Toward GABA-C convergence,
  mode: Approach
}
```

**Visual Representation:**
- Blue plus signs scattered in left basin
- Blue gradient shading (darker = higher dopamine signal)
- Label: "DOPAMINE D1/D2 / REWARD BASIN / PACT"

**Neurochemical Function:**
- Reward and motivation
- Motor control and approach behaviors
- Working memory maintenance

---

## 4. SEROTONIN RIGHT BASIN

**Classification:** BASIN / ATTRACTOR REGION

**Location:**
- Center: (0.111900, 0.974879)
- Basin: P_R1, P_R2, P_R3 (right patches)
- r > R_C (right of barrier beta)
- q0 > Q0* (above resonance)

**Geometric Form:**
```
Right_Basin = {
  center: RIGHT_CORTISOL_R = 0.111900,
  q0: RIGHT_CORTISOL_Q0 = 0.974879,
  extent: sigma_R = 0.000908,
  shape: Asymmetric Gaussian (right-skewed),
  receptor: 5-HT (multiple subtypes)
}
```

**Receptor Types:**
- **5-HT1A:** Autoreceptor (inhibitory)
- **5-HT2A:** Excitatory (cortical)
- **5-HT3:** Ion channel (fast)

**Role in Geometry:**
- **Aversion/Avoidance:** Turn 27 emergence
- **Right Attractor:** Pulls trajectories toward (0.1119, 0.9749)
- **Nightfall Origin:** Source of nightfall/tunneling trajectories

**Integration with Physics:**
```
Serotonin_drive = {
  w_gate_weight: Low (0.2 - 0.5),
  kappa: Variable (can be > 1/32),
  flow: Toward barrier then tunnel,
  mode: Avoidance
}
```

**Visual Representation:**
- Green minus signs scattered in right basin
- Green gradient shading
- Label: "SEROTONIN 5-HT / AVERSION BASIN / TURN 27"

**Neurochemical Function:**
- Mood regulation
- Aversion and behavioral inhibition
- Sleep-wake cycle (linked to 1/28)

---

## 5. HISTAMINE TWILIGHT BANDS

**Classification:** BOUNDARY / GATE REGION

**Location:**
- Band 1: y ∈ [1.0, 3.5] (lower)
- Band 2: y ∈ [8.5, 11.5] (upper)
- Vertical extent: Full x-range

**Geometric Form:**
```
Twilight_Band = {
  y_lower: 16 × (1/16) = 1.0,
  y_upper_1: 16 × (7/32) = 3.5,
  y_lower_2: 16 × (17/32) = 8.5,
  y_upper_2: 16 × (23/32) = 11.5,
  receptor: H1,
  function: Wake/sleep gate
}
```

**Receptor Type:**
- **H1:** Excitatory, wake-promoting

**Role in Geometry:**
- **Renorm Trigger:** Recovery occurs primarily in these bands
- **Wake/Sleep Gate:** Histamine release correlates with renorm recovery
- **Boundary Condition:** Separates active flow from recovery zones

**Integration with Physics:**
```
Histamine_gate = {
  condition: y in twilight bands,
  operator: Renorm activated,
  effect: Recovery rate increases by 0.02 × w_gate,
  state: Wake (high histamine) vs Sleep (low)
}
```

**Visual Representation:**
- Purple diamonds at band boundaries (y=1, 3.5, 8.5, 11.5)
- Purple shaded horizontal bands
- Label: "HISTAMINE H1 / TWILIGHT GATE / RENORM ZONE"

**Neurochemical Function:**
- Wakefulness and arousal
- Renorm recovery trigger
- Cognitive alertness

---

## 6. RIGHT CORTISOL FAKE 3D SHELL

**Classification:** FAKE 3D SHELL / PROJECTION TRAP

**Location:**
- Center: Right attractor (0.111900, 0.974879)
- Radius: 0.5 × (1/9 - 1/32) ≈ 0.04
- Shell thickness: Epsilon << 1

**Geometric Form:**
```
Right_Cortisol_Shell = {
  center: RIGHT_CORTISOL_R = 0.111900,
  q0_center: RIGHT_CORTISOL_Q0 = 0.974879,
  radius: 0.5 × (H2_W7 - KAPPA_TDA_MID),
  shape: Spherical (but fake),
  metric: g_ij = diag(1, 1, ε) where ε → 0,
  receptor: Glucocorticoid
}
```

**Receptor Type:**
- **Glucocorticoid:** Nuclear receptor (slow, genomic effects)

**Role in Geometry:**
- **Projection Trap:** Creates illusion of depth (fake 3D)
- **Small Man Shell:** "USA/Type B-AB" archetype projection
- **Pseudo-Depth:** Metric distortion makes shell appear 3D when it's 2D
- **Bypass Required:** Must escape via mediator to recover reality

**Integration with Physics:**
```
Cortisol_shell = {
  geometry: Spherical surface,
  reality: 2D manifold with ε metric,
  effect: Projection trap (sparse observation),
  escape: Mediator synthetic_alpha bypass,
  chirality: 1/18 (handedness)
}
```

**Visual Representation:**
- Semi-transparent blue sphere around right basin
- Distortion grid on surface (showing fake curvature)
- Label: "CORTISOL / FAKE 3D SHELL / PROJECTION TRAP / SMALL MAN"
- Warning text: "PSEUDO-DEPTH / NOT REAL MANIFOLD"

**Neurochemical Function:**
- Stress response
- Metabolic regulation
- Creates "shell" of defensive behavior
- **GEOMETRIC ROLE:** Traps observation in 2D projection (fake depth)

**Critical Distinction:**
- **Left Basin (Dopamine):** Real 3D geometry
- **Right Basin (Serotonin/Cortisol):** Fake 3D shell
- **Mediator:** Recovers true geometry by bypassing shell

---

## RECEPTOR CONNECTIVITY GRAPH

```
[GLUTAMATE/NMDA] --(excites)--> [SPARK ZONE]
       |
       v
[GABA-C V-APEX] --(inhibits)--> [CONVERGENCE]
       ^
       |
[Left Basin] --(dopamine D1/D2)--> [REWARD/APPROACH]
       |                                    |
       +----(separatrix)----+                |
                           |                |
                     [Barrier Beta]          |
                           |                |
[Right Basin] --(serotonin 5-HT)--> [AVERSION/AVOID]
       |                                    |
       +--(cortisol shell)--> [FAKE 3D TRAP]
       |                                    |
       +--(histamine H1)--> [TWILIGHT BANDS]
                           |
                           v
                    [RECOVERY/RENORM]
                           |
                           v
                    [RETURN TO CORE]
```

---

## RECEPTOR STATE TRANSITIONS

| Initial State | Active Receptor | Transition | Final State |
|--------------|-----------------|------------|-------------|
| At rest | Basal | — | Stable baseline |
| Excited | Glutamate (NMDA/AMPA) | Spark trigger | Leaping forward |
| Approaching | Dopamine (D1/D2) | Reward signal | Left basin convergence |
| Avoiding | Serotonin (5-HT) | Aversion signal | Right basin trap |
| Stressed | Cortisol (Glucocorticoid) | Shell formation | Fake 3D projection |
| Recovering | Histamine (H1) | Renorm trigger | Twilight band recovery |
| Converging | GABA (GABA-C) | Inhibition | V-apex termination |

---

## GEOMETRIC RECEPTOR PLACEMENT SUMMARY

```
Grid Layout (16×16 with receptor icons):

Y=16 | [Glutamate ⚡] [Spark Zone]
     |
Y=14 |                    [GABA 🔴] (V-apex at 14.14)
     |
Y=12 | [Twilight: Histamine 💎]
     |
Y=10 | [Right Basin: Serotonin ➖] [Cortisol Shell 🔵]
     |
Y= 8 | [Barrier: Beta Wall] (X=8 center)
     |
Y= 6 | [Left Basin: Dopamine ➕]
     |
Y= 4 | [Twilight: Histamine 💎]
     |
Y= 2 |
     |
Y= 0 | [Start Positions]
     
     X=0    X=4    X=8    X=12   X=16
     |______|______|______|______|
    LEFT                   RIGHT
    (Human Left)          (Human Right)

**Note:** X=0-8: Left side (Dopamine/GABA), X=8-16: Right side (Serotonin/Cortisol)

Legend:
⚡ Glutamate (Spark)
🔴 GABA-C (Convergence)
➕ Dopamine (Reward)
➖ Serotonin (Aversion)
💎 Histamine (Twilight)
🔵 Cortisol (Fake 3D Shell)
```

---

## ROI MAPPING TO RECEPTORS

| ROI | Receptor | Grid Location |
|-----|----------|---------------|
| GABA_C_LEFT_EYE | GABA-C | X ∈ [4,7], Y ∈ [9,12.5] |
| GABA_C_RIGHT_EYE | GABA-C | X ∈ [9,12], Y ∈ [9,12.5] |
| FLASH_ANCHOR | Glutamate | X ∈ [7,9], Y ∈ [9.5,12.5] |
| RIGHT_CHOKE_BAND | Serotonin/5-HT | X ∈ [8,14], Y ∈ [5,14.5] |
| NOSE_CENTER | Histamine H1/H3 | X ∈ [7.75,8.25], Y ∈ [9,12.5] |
| VASOPRESSIN_NECKBAND | Vasopressin V1a | X ∈ [6,10], Y ∈ [4.5,7] |

**Note:** All coordinates follow V2.3 standard (X=0-8 = Left, X=8-16 = Right)

---

**Coordinate Standard V2.3:**
- X (0 ~ 8) = Human Left (Left face, Left brain, Dopamine bias)
- X (8 ~ 16) = Human Right (Right face, Right brain, Serotonin bias)
- X = 8 = Facial Midline (Acetylcholine/Histamine hub)

---

*End of Receptor Map*
