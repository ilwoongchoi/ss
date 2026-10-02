# Seismic Traceability Pipeline

This pipeline details how the structural closure grammar is executed entirely in terms of seismic wavefield parameters.

## The Closure Grammar in Wave Terms

- **Node**: A discrete continuous entity in the wavefield. Specifically, a waveform segment (e.g., 2 seconds of 3C data) centered on a local energy packet, pick, or apparent arrival.
- **Seam**: A local, undeniable phase-consistent continuity. Example: The highly correlated P-wave first arrival across an array of stations with spacing less than half a wavelength ($\lambda/2$).
- **Bridge**: A cross-gap, wave-consistent link. This occurs when two distinct station arrays record the same source wavelet, but the intermediate stations failed to trigger.
- **Relay**: A multi-station or multi-phase propagation chain (e.g., Source $\rightarrow$ P $\rightarrow$ structural scatterer $\rightarrow$ P coda $\rightarrow$ Receiver).
- **Mediator**: A non-direct, externally injected structural or wave mechanism required to enforce closure. Examples: A converted phase (P-to-S conversion at Moho) or a low-velocity fault zone acting as a waveguide corridor.
- **Barrier**: A true physical shell. An extreme impedance discontinuity that reflects or completely attenuates the carrier, enforcing a hard topological boundary (e.g., the core-mantle boundary for certain high-frequency phases).
- **Projection Trap**: A false boundary. Examples include missing picks due to localized site noise, a sparse station network creating an artificial spatial gap, or a buried structure that creates a shadow zone in high frequencies but is fully continuous in low frequencies.
- **Hidden Lift**: The algorithmic mechanism of moving to a transformed domain (e.g., cross-correlation, double-difference, frequency, or polarization) to reveal that a projection trap is actually a continuous seam.
- **Internal Closure**: The standard operating procedure of seismology (e.g., HYPOELLIPSE / standard phase association) that groups clear, high-SNR arrivals into a single event component.
- **Extended Closure**: The advanced DSU operation where isolated graph components are forcefully united through mathematically valid transformations (hidden lift) or the explicit modeling of a scattered wavepacket (mediator insertion).

## Execution Pipeline

### Step 1: Initialize $S\_wave$ Base State
1. Load continuous data and standard catalog.
2. Initialize `station_graph`.
3. Detect absolute high-SNR nodes (internal picks).

### Step 2: Form Internal Seams (Standard DSU)
1. Execute basic travel-time association.
2. Form edges between nodes matching standard travel-time curves.
3. Calculate initial `closure_state` (typically fragmented into $k$ components).

### Step 3: Projection Trap Detection (The Lift)
1. For every unconnected spatial gap $G(A, B)$ between components $A$ and $B$:
2. **Execute Lift Protocols**:
   - *Frequency Lift*: Filter to 0.1-1.0 Hz. Re-evaluate coherence.
   - *Polarization Lift*: Apply rectilinearity filter. Hunt for sub-threshold nodes.
   - *Residual Lift*: Compute cross-correlations of waveforms.
3. If new nodes/seams emerge $\rightarrow$ Classify gap as `projection_trap` and union $A$ and $B$.

### Step 4: Mediator Insertion Scan
1. If components remain isolated, but metadata suggests geometric adjacency:
2. Propose mediator $M_x$ (e.g., `mediator:synthetic_scatterer`).
3. Synthesize theoretical waveform for $M_x$.
4. Check if observed data coda matches $M_x$.
5. If yes, union $A \rightarrow M_x \rightarrow B$.

### Step 5: Barrier Finalization
1. If $A$ and $B$ remain isolated despite all lifts and mediator attempts, and energy profiles show hard impedance drops:
2. Classify gap as `true_barrier`.
3. Freeze `closure_state`.

### Step 6: Verdict Generation
Output the final graph and log all structural claims strictly as derivatives of wave continuity.
