# Seismic-Wave Observable Map
## Wave-Centric Measurement Framework

---

## Observable: PHASE PICK (Node)

**Closure mapping**: Primary node in wave-field DSU

**Measurement**:
- Arrival time t (absolute or relative)
- Phase type (P, S, PP, SS, PcP, ScS, etc.)
- Amplitude A (peak or integrated)
- Frequency content f (dominant period)
- Polarization (for 3-component stations)

**Component role**: Discrete observation of continuous wave field

**Closure condition**: Pick qualifies as node when SNR > threshold and phase identifiable

---

## Observable: TRAVEL-TIME RESIDUAL (Bridge Saddle)

**Closure mapping**: Geometric compatibility metric

**Measurement**:
```
δt = t_observed - t_predicted (1D reference model)
```

**Properties**:
- δt ≈ 0: Phase consistent with direct path
- δt > 0: Delayed arrival (slow structure, longer path)
- δt < 0: Early arrival (fast structure, upper mantle)

**Component role**: Determines bridge saddle quality

**Closure condition**: |δt| < 3σ (within model uncertainty)

---

## Observable: AMPLITUDE RATIO (Bridge Contact)

**Closure mapping**: Wave coherence metric

**Measurement**:
- P/S amplitude ratio
- Site amplification (relative to reference)
- Spectral amplitude at dominant frequency

**Component role**: Strong amplitude → high contact (reliable bridge)

**Closure condition**: Amplitude above detection threshold; consistent with attenuation model

---

## Observable: CONVERTED PHASE (External Mediator)

**Closure mapping**: Minimal mediator phase

**Measurement**:
- P-to-S conversion at impedance boundary (Ps phase)
- S-to-P conversion at free surface (Sp phase)
- Converted amplitude relative to primary
- Delay time (indicates conversion depth)

**Component role**: Mediator enabling 2→1 closure across structural gap

**Falsifiable signature**:
- Converted phase present where direct phase absent
- Delay time consistent with structure depth
- Amplitude pattern matches impedance contrast

---

## Observable: CODA WAVE (Scattered Mediator)

**Closure mapping**: Scattered wave packet mediator

**Measurement**:
- Coda duration Qc
- Coda shape (single scattering vs. multiple scattering)
- Frequency-dependent decay
- Correlation with primary phase

**Component role**: Scattering relay connecting source and receiver through medium heterogeneity

**Closure condition**: Coda coherence indicates continuous wave path despite complex structure

---

## Observable: AMBIENT NOISE CORRELATION (Virtual Mediator)

**Closure mapping**: Cross-correlation mediator

**Measurement**:
- Green's function extracted from noise correlation
- Surface wave dispersion from ambient field
- Body wave emergence from long-term stacking

**Component role**: Virtual source creates mediator phase between station pairs

**Closure condition**: Correlation converges to causal+acausal wavelet

---

## Observable: RECEIVER FUNCTION (Hidden Lift)

**Closure mapping**: Deprojection in delay-time domain

**Measurement**:
- P-to-S conversion at Moho (Ps delay ~3-4s for crust)
- Crustal multiples (PpPs, PsPs)
- Lithosphere-asthenosphere boundary (LAB) conversion

**Component role**: Reveals continuous layering beneath projection trap

**Closure condition**: Receiver function peaks indicate continuous impedance boundaries

---

## Observable: TRAVEL-TIME TOMOGRAPHY RESIDUAL CORRIDOR (Hidden Lift)

**Closure mapping**: Continuity in residual space

**Measurement**:
- Spatial pattern of δt across station network
- Correlation with mapped structure
- Low-velocity corridor signature

**Component role**: Residual continuity reveals wave-speed structure continuous beneath apparent gaps

---

## Observable: STATION GAP (Projection Trap)

**Closure mapping**: Observation shadow

**Measurement**:
- Distance between stations along wave path
- Azimuthal gap in station coverage
- Depth penetration of gap (sensitive to different phases)

**Component role**: No direct observation; mediator phase may reveal continuity

---

## Observable: PHASE MISIDENTIFICATION (Projection Trap)

**Closure mapping**: Erroneous node classification

**Measurement**:
- Secondary phase labeled as primary
- Converted phase missed entirely
- Multiple phase interference

**Component role**: Trap resolved by reclassification or mediator insertion

---

## Observable: IMPEDANCE CONTRAST (True Barrier)

**Closure mapping**: Uncrossable boundary

**Measurement**:
- Reflection coefficient (amplitude ratio)
- Transmission coefficient
- Mode conversion efficiency
- Critical angle for refraction

**Component role**: Big Woman (shell) — wave field fundamentally changes

---

## Observable: LOW-VELOCITY CORRIDOR (Mediator Structure)

**Closure mapping**: Structural mediator enabling wave continuity

**Measurement**:
- Reduced wave speed relative to surroundings
- High attenuation (low Q)
- Guiding of wave energy
- Anomalous dispersion

**Component role**: Channel for wave propagation where direct path blocked

---

## Summary Table: Wave-Centric Elements

| Closure Element | Wave Physics Equivalent | Primary Observable | Secondary Observable |
|-----------------|------------------------|-------------------|---------------------|
| Node | Phase pick | Arrival time t | Amplitude A, frequency f |
| Bridge | Phase-consistent path | Travel-time residual δt | Amplitude ratio |
| Relay | Multi-station/phase path | Station pair correlation | Phase conversion chain |
| Mediator | Converted/scattered phase | Ps delay time | Conversion amplitude |
| Barrier | Impedance boundary | Reflection coefficient | Mode conversion |
| Projection trap | Station gap / threshold | Azimuthal gap | Detection threshold |
| Hidden lift | Receiver function | Ps delay ~3-4s | Crustal multiples |
| Big Man | Deep propagation drive | Energy flux conservation | Focal mechanism |
| Big Woman | Impedance shell | Reflection polarity | Transmission cutoff |
| Small Man | Local coherent seam | Single-station phase | Particle motion |
| Small Woman | Sparse observation | Missing phase pick | SNR < threshold |

---

*Wave-centric observable map: Every closure element grounded in seismic measurement*
