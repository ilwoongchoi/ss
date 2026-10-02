# Seismic Wave State Model

## The Canonical State
The seismic traceability engine is uniquely defined by its continuous state vector, `S_wave`.

```text
S_wave = (
    event, 
    station_graph, 
    phase_graph, 
    residual_field, 
    polarization_field, 
    attenuation_field, 
    mediator_state, 
    barrier_state, 
    closure_state
)
```

## Variable Definitions & Physical Meanings

### 1. `event` (Observed / Inferred)
- **Meaning**: The physical source of the carrier wave (hypocenter, origin time, moment tensor).
- **Format**: 4D spatial-temporal coordinate + 6-component tensor.

### 2. `station_graph` (Observed)
- **Meaning**: The fixed spatial observation network.
- **Format**: Graph where nodes are stations, edges are physical distances, weighted by azimuth.

### 3. `phase_graph` (Observed / Latent)
- **Meaning**: The topological connectivity of wave arrivals.
- **Format**: DSU graph where nodes are waveform segments/picks. Edges are phase-consistent continuities (e.g., P-wave at STA1 connects to P-wave at STA2).

### 4. `residual_field` (Observed / Computed)
- **Meaning**: The divergence from a 1D/3D reference model.
- **Format**: Matrix of $\Delta t$ values across all stations and phases. Used for hidden lift in double-difference space.

### 5. `polarization_field` (Observed)
- **Meaning**: The 3D particle motion of the wavefield over time.
- **Format**: Eigenvectors and eigenvalues from moving-window 3C covariance matrices. Identifies trapped continuity.

### 6. `attenuation_field` (Latent / Reconstructed)
- **Meaning**: The energy dissipation landscape (path-averaged $Q$).
- **Format**: Spatial grid of t* values. 

### 7. `mediator_state` (Latent / Injected)
- **Meaning**: Synthesized structural corridors (e.g., low-velocity waveguides) or converted/scattered wave packets required to bridge isolated components.
- **Format**: Ordered list of active mediators and their geometric/kinematic parameters.

### 8. `barrier_state` (Latent / Confirmed)
- **Meaning**: True impedance discontinuities or tectonic boundaries that cleanly veto specific propagation paths.
- **Format**: Boolean masking matrix over the spatial domain.

### 9. `closure_state` (Computed)
- **Meaning**: The ultimate topological output. Tracks the number of disconnected sub-graphs within the wavefield.
- **Evolution**: 
  - $T_0$: $N$ isolated stations (high fragmentation).
  - $T_1$ (Internal Closure): Simple arrivals drop $N \rightarrow k$.
  - $T_2$ (Extended Closure): Transformed lift and mediators drop $k \rightarrow 1$ (or true barriers halt at $k=2$).
