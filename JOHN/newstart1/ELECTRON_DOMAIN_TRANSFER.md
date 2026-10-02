# Electron Domain Transfer: Closure Grammar → Detector Physics

## Source Method (Locked Closure Theorem)

The closure grammar provides a reproducible, state-leakage-free framework for connectivity reconstruction:
- **Internal closure**: Hard bound at 2 components within original universe
- **Extended closure**: 2→1 reduction via minimal external mediator
- **Mechanism**: Bridge activation sequence with relay paths through latent structure

## Domain Mapping: Closure Grammar → Electron Tracking

| Closure Element | Electron Physics Equivalent | Operational Definition |
|-----------------|----------------------------|------------------------|
| **Node** | Hit / Charge cluster | Energy deposition above threshold in detector cell |
| **Bridge** | Track segment connection | Hypothesis linking two hits via particle trajectory |
| **Relay** | Multi-point track link | Chain of bridges forming extended track hypothesis |
| **Barrier** | Tracking gap / Dead region | Volume where standard reconstruction loses continuity |
| **Internal boundary** | Projection trap boundary | Region where local evidence is insufficient for connection |
| **External mediator** | Latent hit / Scattering vertex | Unobserved or weakly-observed intermediate point enabling connection |

## Phase Mapping

### Phase 1: Internal Closure (Standard Tracking)

```
Universe: Detector hits within active volume
Nodes: All hits above threshold
Bridges: Kalman-filter or Hough-transform connections
Relay: Full track candidates

Hard bound: 2 components
- Component A: Main track cluster (connected hits)
- Component B: Isolated hits / Gap region (projection trap)
```

**Barrier**: A↔C equivalent — the gap region where local reconstruction fails.

### Phase 2: Extended Closure (Mediator-Assisted)

```
Universe expansion: Add latent mediator candidates
- Scattering vertices in material
- Low-energy depositions below standard threshold
- Timing-correlated signals from adjacent detectors

External mediator: Minimal node enabling 2→1 reduction
Relay: hit → mediator → hit (skipping the gap)
```

## Structural Isomorphism

| Closure Structure | Electron Tracking Structure |
|-------------------|----------------------------|
| Sheet cluster (main component) | Track segment with dense hits |
| gateway_peak (isolated) | Gap region with no observable hits |
| sheet_id:2 (neighbor) | Last hit before gap |
| A↔C barrier | Trajectory discontinuity in projection |
| mediator:synthetic_alpha | Latent scattering point or drift-time extension |
| Relay 13→3→2 | Multi-point link through intermediate detector layer |

## Method Transfer Principles

1. **No textbook assumptions first**: Start from closure grammar, derive tracking behavior
2. **Observable grounding**: Every mapped element must have detector-level signature
3. **Falsifiability**: Predictions must distinguish closure-grammar from standard reconstruction
4. **Minimal mediator**: External expansion uses smallest possible addition to universe

---

*Domain transfer: Closure grammar as generative method for electron tracking*
