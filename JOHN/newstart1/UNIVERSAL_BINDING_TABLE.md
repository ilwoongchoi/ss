# UNIVERSAL BINDING TABLE (LOCKED)

This table locks one-to-one bindings between equation symbols, particle layer, archetype layer, biology layer, and geometry layer.

## 1) Core 4 entities

| Symbol | Particle | Archetype | Biology Node | Scale | Geometry Anchor |
|---|---|---|---|---|---|
| BW | Proton (p) | Big Woman | Vasopressin | 1/32 | VASO lock axis |
| SW | Electron (e) | Small Woman | PLP | 1/8 | PLP core pull |
| BM | Photon (gamma) | Big Man | Right Acetylcholine | 1/16 | Propagation/radiative axis |
| SM | Neutrino (nu) | Small Man | Right Cortisol | 1/128 | Observer/weak-stress axis |

## 1B) Dark matter (modifier, not a state)

| Name | Meaning | Scale | Execution rule |
|---|---|---|---|
| DM | Gravitational lensing only (no emission/absorption) | 1/64 | Acts inside the 5/32 gate as a curvature/deflection modifier on photon paths; not a separate state variable |

## 2) Core geometry anchors

| Name | Coordinates | Role in equation |
|---|---|---|
| PLP_CORE | (8.0, 0.4) | Singular pull term |
| VASO_LOCK | (14.0, 6.0) | Compression/locking term |
| SPINE_16_10 | (8.0, 10.0) | Transition/spark gate |

## 3) Interaction layer (64 channels)

Definition:
- Ordered pairs: 4x4 = 16
- Matter/antimatter configs: 4
- Total channels: 16x4 = 64

Channel tensor:
- K_ij^c where i,j in {nu,p,e,gamma}, c in {pp,p_ap,ap_p,ap_ap}

## 4) Dynamic update operator

Single-step update:

S_{t+1} = F(S_t; K64, V_core, R_state)

Expanded:
- Interaction drive: K64-weighted pair forces
- Core potential: V_core = V_PLP + V_VASO
- State rule: R_state over 5 states

## 5) 5-state rule

| State | Meaning |
|---|---|
| DISCRETE_IDEAL | Locked equilibrium |
| GABAERGIC_SELFISH | Bounded selfish mode |
| CRUNCH | Collapse mode |
| CREATIVE_ASCENT | Upward constructive mode |
| TRANSCENDENT | Stable high-order recurrence |

## 6) Non-negotiable execution rule

No free remapping during runtime:
- Each symbol must map to exactly one row in section (1)
- Any code path violating this table is invalid
