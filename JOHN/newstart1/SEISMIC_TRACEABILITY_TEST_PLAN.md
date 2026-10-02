# Seismic Traceability Test Plan

## Pilot Experiment: Sub-Threshold Fault-Zone Continuity

### Objective
Operationalize the traceability engine by testing whether an apparent structural gap (a fault zone) acts as a `true_barrier` or a `projection_trap` using sub-threshold wave continuity.

### 1. Data Source
- **Dataset**: Continuous 3-component (3C) data from a dense nodal seismic array (e.g., Large-N deployment) traversing a known active fault zone (e.g., San Jacinto Fault).
- **Event**: A single, high-SNR regional teleseism (magnitude 5.0+, distance 10-30 degrees) providing a coherent, deep plane-wave illumination (The "Big Man" external drive).

### 2. Unit of Analysis
- **Temporal Window**: A continuous 1-hour waveform window containing the pre-event noise, main arrival ($P$, $S$), and extended coda.
- **Spatial Unit**: The sequence of nodes perpendicular to the fault strike.

### 3. Gap Definition
- **The Apparent Gap**: The geographical swath directly above the fault core.
- **Internal Closure Failure**: Standard STA/LTA triggering fails to pick distinct arrivals in this swath due to severe scattering, attenuation, and local site noise. Standard catalogs show this as a "broken" phase graph (2 isolated components: West of fault, East of fault).

### 4. Matched Controls
- **Control Group**: A parallel linear transect of identical nodal stations deployed 5 km away from the fault, in intact, homogeneous bedrock.

### 5. Primary Statistic
- **Metric**: Peak cross-correlation coefficient ($CC_{max}$) and lag-time ($\tau$) between adjacent stations.
- **Transformed Domains**: Computed in:
  1. Raw time domain (0.5 - 20 Hz).
  2. Low-frequency domain (0.1 - 1.0 Hz).
  3. Polarization-filtered domain (rectilinearity > 0.8).

### 6. Pipeline Execution
1. Ingest continuous wave data.
2. Confirm the 2-component isolated state across the fault using standard internal closure.
3. Apply transformations (Hidden Lift).
4. Attempt to identify a Fault Zone Guided Wave (Mediator Insertion).

### 7. Artifact Checks
- **Clock Drift**: Verify GPS lock on all nodes; reject nodes with $>5$ ms drift.
- **Filter Ringing**: Run identical CC operations on 1-hour pure noise windows to establish the null-hypothesis CC distribution.

### 8. Success Criterion (Marriage Law Achieved)
- The raw data shows $CC_{max} < 0.3$ across the gap (Projection Trap confirmed).
- The low-frequency or polarization-filtered data yields $CC_{max} > 0.75$ with travel-time lags matching structural models.
- The state officially reduces from `2 components $\rightarrow$ 1 component`. The fault is classified as a mediator/projection trap, not a true barrier to the carrier.

### 9. Failure Criterion (Barrier Maintained)
- $CC_{max}$ remains $< 0.3$ across all tested transformed domains and mediator insertions.
- The state remains locked at `2 components`. The fault is classified as a `true_barrier` to that specific wavelength.
