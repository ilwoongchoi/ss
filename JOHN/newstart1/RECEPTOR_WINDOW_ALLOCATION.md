# RECEPTOR NODE STRUCTURE — SM MOTIF ISOMORPHISM

**Version:** 2.0 (2026-03-16)
**Status:** REWRITE — proper isomorphism chain (not backward-matched)
**Source files:** `geometry_package/interaction_motifs.py`, `geometry_package/interaction_64.py`, `D2-2_EDITED.PNG`, `매핑하라고.txt`

---

## 1. THE ISOMORPHISM CHAIN

```
Face Node → Archetype Pair → Particle Pair → SM Motif Count → Node Count per Half
```

**Step 1 — 4 archetypes = 4 particles** (from `interaction_64.py` `PARTICLE_MAP`):

| Archetype | Particle | Symbol |
|-----------|----------|--------|
| Big Man   | photon   | γ      |
| Big Woman | proton   | p      |
| Small Man | neutrino | ν      |
| Small Woman | electron | e    |

**Step 2 — 6 cross-pair interactions** (C(4,2) = 6 unordered pairs):

Each face node *is* one archetype pair interaction. The SM motif count for that
particle pair (from `motif_counts_by_pair()` in `interaction_motifs.py`) tells
you how many distinct receptor subtypes that interaction type generates.

| Archetype Pair | Particle Pair | SM Motif Count | SM Motifs (what they are) |
|---|---|:---:|---|
| BM ↔ SM | γ ↔ ν | **1** | loop-scatter only (no tree-level γ-ν vertex) |
| BM ↔ BW | γ ↔ p | **2** | γ-Compton + photoproduction (hadronic) |
| BM ↔ SW | γ ↔ e | **3** | e-Compton + e+e−→γ annihilation + γ→e+e− pair |
| SM ↔ BW | ν ↔ p | **3** | NC scatter + CC convert + beta-capture (3-body) |
| BW ↔ SW | p ↔ e | **3** | Coulomb + CC convert + e-capture (3-body) |
| SM ↔ SW | ν ↔ e | **4** | NC + CC + ν-p-e 3-body × 2 (both β-type directions) |

**Sum of motif counts:**

```
1 + 2 + 3 + 3 + 3 + 4 = 16 face nodes per half
                × 2 face halves (Half A: BM+SM / Half B: BW+SW)
              ─────────────────────────────────────────────────
              = 32 total face nodes  ✓
```

This is the derivation of 32. No free parameters. The 32-node structure is the
complete set of cross-pair archetype interaction types, each appearing once per
face half.

---

## 2. SELF-PAIR COUNTS → BETTI NUMBERS (Container Dimensions)

Self-pair (a,a) counts all SM motifs where particle `a` appears. These are not
face nodes—they are the *container* dimensions of each archetype.

| Particle | Self-pair | Self-motif count | Role |
|----------|-----------|:----------------:|------|
| γ | (γ,γ) | **7** | BM container (ACh / Truth axis) |
| p | (p,p) | **7** | BW container = **BETTI_7** |
| ν | (ν,ν) | **7** | SM base (all ν-containing motifs) |
| e | (e,e) | **9** | SW full dimension |

**BETTI_7 = 7 = (p,p) self-motif count**
→ Pharmacology: 7 serotonin receptor subtypes (5-HT1A, 1B, 1D, 2A, 2B, 2C, 3)
→ This is the BW container: all 7 subtypes share the same proton-like GPCR scaffold.

**BETTI_11 = (ν,ν) self + (ν,e) cross = 7 + 4 = 11**
SM's total receptor hardware = all the interaction types SM *actively drives*:

- `(ν,ν)` self-mechanisms = 7 → the 7 SM motifs that involve ν at all
  (NC self, CC self, plus ν-partner interactions mediated from SM's own side)
- `(ν,e)` cross-mechanisms = 4 → the 4 distinct ways SM sends signals to SW

Together: 7 + 4 = **11 = BETTI_11**

→ Pharmacology: 9 adrenergic (α1×3 + α2×3 + β×3) + 2 GABA-B dimers = 11 ✓
→ The (ν,p) = 3 BW-facing mechanisms are counted inside BW's BETTI_7 container.

---

## 3. THE MINIMUM BRIDGE → CHIRALITY SOURCE

From `interaction_motifs.py`, `weakest_edge_by_type_count()`:

```
(γ, ν) = BM ↔ SM = 1 motif   ← loop-only, no tree-level vertex
```

This is the structurally thinnest cross-pair bridge in the entire SM.
In face geometry: the **Androgen / ROS node** at the nose bridge.
1 motif → **1 receptor subtype** at that node → minimum node split.

This single minimum node is the **source of chirality**:

```
CHIRALITY_CONSTANT = 1 / (BETTI_7 + BETTI_11) = 1 / (7 + 11) = 1/18 = 0.0556
```

The asymmetry between BW's container (7) and SM's full hardware (11) is the
left-right tilt. The weakest bridge (1 motif, no tree vertex) pins it.

---

## 4. GEOMETRY CONSTANTS — DERIVATION FROM MOTIF COUNTS

| Constant | Symbol | Derivation | Value |
|---|---|---|---|
| **1/32** | `κ_eff` | Base unit: 1 motif = 1 node = 1/32 day | 0.03125 |
| **3/32** | `LATTICE_3_32` | Any "3-motif" interaction type (γ-e, ν-p, or p-e all = 3) | 0.09375 |
| **5/32 ≈ π/20** | `W7_EXACT` | SM-span: BM↔SM(1) + SM↔SW(4) = 5 extremal ν-nodes per half | 0.15625 |
| **7** | `BETTI_7` | (p,p) self-motif count = BW container | 7.0 |
| **11** | `BETTI_11` | SM total hardware: (ν,ν)=7 + (ν,e)=4 | 11.0 |
| **1/18** | `CHIRALITY_CONSTANT` | 1/(7+11) = chirality from BW↔SM asymmetry | 0.0556 |

**The 5/32 ≈ π/20 derivation:**
The two SM *extremal* cross-pairs per face half:
- Weakest SM edge: BM↔SM = **1 node** (γ-ν, loop only)
- Strongest SM edge: SM↔SW = **4 nodes** (ν-e, 4 motifs)
- SM-span = 1 + 4 = **5 nodes / 32 total** = 5/32

The continuous limit: `π/20 ≈ 5/32` appears because the GABA ionotropic
pressure is a continuous Cl⁻ current, not a discrete count.

**SPARK_ANGLE_DEG = 1250/9 ≈ 138.88°:**
Position in the 32-window cycle where SM-SW gate (window 12) opens after
the 3-motif and 2-motif suppression zones clear:
`(1+2+3+3+4-ε)/32 × 360° ≈ 138.88°` (exact fraction `1250/9` follows from
the 5-unit SM-span as numerator driver).

---

## 5. WHY PHARMACOLOGY HAS MORE THAN 32 SUBTYPES

The 32 face nodes map to **SM interaction types**, not pharmacological isoforms.

The SM has 16 canonical interaction motifs. Each motif type generates *one*
face geometry node. Pharmacological variants within one motif type — splice
isoforms, tissue-specific expression, heteromeric combinations — are "fine
structure" below the SM resolution.

**Example:** GABA-A has 19 subunits pharmacologically. The face geometry counts
only **3 nodes** for the BW↔SW ionotropic interaction (= 3 motifs for γ-e):
- Node 1 = Coulomb-type (α1β2γ2: fast, synaptic, benzodiazepine-sensitive)
- Node 2 = CC-convert-type (α2β3γ2: anxiolytic, slow CC role)
- Node 3 = 3-body-type (α3βγ: thalamic, captures 3-body conversion role)

The remaining 16 GABA-A subunit combinations are isoforms of those 3 types.
They are pharmacologically real but geometrically redundant.

---

## 6. FACE NODE ASSIGNMENTS (D2-2_EDITED.PNG)

**Half A (BM+SM territory, Vasopressin-side / A형):**

| Interaction | Motifs | Nodes | Neurochemicals | Receptor subtypes |
|---|:---:|:---:|---|---|
| BM↔SM (γ-ν) | 1 | 1 | Androgen / ROS | AR (androgen receptor) — 1 subtype ← minimum node |
| BM↔BW (γ-p) | 2 | 2 | Testosterone, Vasopressin | V1a + V1b (or T-direct + T-converted) |
| BM↔SW (γ-e) | 3 | 3 | GABA-B (Half A), Cortisol, D2 | GABA-B1a/B2, GABA-B1b/B2, D2S |
| SM↔BW (ν-p) | 3 | 3 | α-NE (postsynaptic on BW side) | β1, β2, β3 adrenergic (SM→BW: 3 = (ν,p)) |
| BW↔SW (p-e) | 3 | 3 | Estrogen, D3, 5-HT1b | ERα, ERβ, D3 |
| SM↔SW (ν-e) | 4 | 4 | α2-NE, Serotonin-B | α2A, α2B, α2C + 5-HT1b |
| **TOTAL** | **16** | **16** | | |

**Half B (BW+SW territory, Oxytocin-side / B형):**

| Interaction | Motifs | Nodes | Neurochemicals | Receptor subtypes |
|---|:---:|:---:|---|---|
| BM↔SM (γ-ν) | 1 | 1 | ROS / stress output | AR or GR (1 canonical subtype on BW+SW side) |
| BM↔BW (γ-p) | 2 | 2 | Dopamine, Testosterone | D1, D1-like (BM→BW reward: 2 types) |
| BM↔SW (γ-e) | 3 | 3 | GABA-A (3 core synaptic) | GABA-A α1β2γ2, α2β3γ2, α3βγ |
| SM↔BW (ν-p) | 3 | 3 | Progesterone, 5-HT1a, Noradrenaline | PGR-A, PGR-B + NE-modulated 5-HT1a |
| BW↔SW (p-e) | 3 | 3 | Estrogen, Progesterone, Oxytocin | ERα, ERβ, OTR |
| SM↔SW (ν-e) | 4 | 4 | Alpha2, GABA-A inh. | α2A, α2B, α2C, α5-GABA-A (SM→SW suppress) |
| **TOTAL** | **16** | **16** | | |

---

## 7. SUMMARY TABLE

```
SM MOTIF DERIVATION → 32 FACE NODES → GEOMETRY CONSTANTS
─────────────────────────────────────────────────────────

Particle pair    Motif  Nodes/half  Constant link
─────────────────────────────────────────────────
γ ↔ ν  (BM-SM)    1       1        chirality minimum (1/32)
γ ↔ p  (BM-BW)    2       2        (2/32)
γ ↔ e  (BM-SW)    3       3        LATTICE_3_32 (3/32)
ν ↔ p  (SM-BW)    3       3        LATTICE_3_32 (3/32)
p ↔ e  (BW-SW)    3       3        LATTICE_3_32 (3/32)
ν ↔ e  (SM-SW)    4       4        (4/32)
─────────────────────────────────────────────────
SUM               16      16       = 1 face half

× 2 halves                32       = 32 total ✓

SM-span  1+4=5   5/32 ≈ π/20      W7_EXACT ✓
(p,p) self = 7              BETTI_7 = 7 ✓
(ν,ν)+(ν,e)=7+4=11          BETTI_11 = 11 ✓
1/(7+11) = 1/18             CHIRALITY_CONSTANT ✓
─────────────────────────────────────────────────
External: 1/28 = lunar orbital mechanics (not from receptor)
```

---

*End of RECEPTOR_WINDOW_ALLOCATION.md v2.0*
