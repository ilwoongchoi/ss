# Seismic Traceability Architecture

## System Overview
The Seismic Wave Traceability Engine is designed to ingest raw continuous waveform data and produce a rigorously verified topological closure graph. It explicitly rejects "lines drawn on maps" in favor of dynamically tracing the actual wave carrier across a heterogeneous medium.

## Core Modules

### 1. Ingestion & Pre-processing (The Projection Layer)
- **Inputs**: Continuous 3-component (3C) miniseed/mseed data, station metadata (XML), preliminary catalog events.
- **Function**: Standard bandpass filtering, instrument response removal, and basic STA/LTA triggering.
- **Output**: The baseline, often fragmented, *internal closure graph* (sparse nodes and seams).

### 2. Transformation Engine (The Hidden-Lift Layer)
This is the critical operational core. When the internal closure graph yields isolated components, the engine systematically transforms the data to hunt for "hidden lift":
- **Travel-time Residual Space (Double-Difference)**: Instead of absolute times, the engine lifts to differential times (hypoDD logic). Two apparently distinct source clusters may merge into a single continuous seam in relative residual space.
- **Frequency Domain (Spectral Coherence)**: Lifts waveform segments into the frequency domain using multi-taper methods. High-frequency scattering (a projection trap) might mask profound low-frequency continuity.
- **Polarization Domain (3C Eigen-decomposition)**: Lifts traces into covariance matrices to extract rectilinearity and planarity. A phase masked by noise (apparent gap) emerges clearly as a coherent P-wave polarization vector.
- **Station-Graph Topology (Interferometry)**: Lifts direct wave traces into the ambient noise cross-correlation space. Coda waves are correlated to bridge gaps between stations that lack direct phase associations.
- **Amplitude/Attenuation Residual Field (t* inversion)**: Maps energy decay. Apparent geometric gaps can be closed by demonstrating consistent $Q^{-1}$ profiles.

### 3. Mediator Insertion Engine
If transformation fails to bridge a component gap, the engine proposes an external structural/wave mediator:
- Synthesizes a "corridor" (e.g., a low-velocity fault-zone guided wave waveguide).
- Computes theoretical arrival times/amplitudes for this mediator.
- Tests if empirical data aligns with the mediator's required footprint.
- **Output**: A provisional *extended closure*.

### 4. Classification & DSU Engine
- Maintains the continuous `S_wave` state variables.
- Executes the rules in the `SEISMIC_MEDIATOR_AND_BARRIER_CLASSIFIER.md`.
- Evaluates the final graph. If 2 components become 1 via validated transformation or mediation, the marriage law is satisfied.

## Data Flow
`Raw Waveforms` → `Internal Phase Graph (Fragmented)` → `Transformed Domain Scans` → `Gap Classification` → `Mediator Proposal` → `Extended Closure Verification` → `Final State (S_wave)`
