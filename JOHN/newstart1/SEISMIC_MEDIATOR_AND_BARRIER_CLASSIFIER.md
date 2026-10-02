# Seismic Mediator and Barrier Classifier

This module serves as the primary decision engine for evaluating topological gaps in the `phase_graph`. For any unconnected boundary $G_{AB}$ between component $A$ and component $B$, the classifier strictly assigns one of six states.

## 1. True Barrier (`true_barrier`)
- **Observables**: Sudden, catastrophic drop in amplitude (energy ratio $E_B / E_A < 0.05$); complete loss of spectral coherence; distinct shift in dominant frequency; total lack of phase continuity.
- **Decision Rule**: Fails all Hidden Lift attempts across all transformed domains. Attenuation field shows extreme gradient.
- **Failure Mode**: Mistaking a severe but traversable highly-attenuating basin for a hard tectonic boundary.
- **Falsification Path**: If ambient noise interferometry eventually retrieves a cross-correlation function $> 0.3$ between $A$ and $B$, the true barrier is falsified.

## 2. Projection Trap (`projection_trap`)
- **Observables**: Apparent absence of an arrival pick in the standard time-domain catalog; spatial gap between valid stations.
- **Decision Rule**: Waveform continuity is entirely recovered when lifted into a transformed domain (e.g., applying a rectilinearity filter reveals a coherent P-wave buried in ambient noise, or array beaming reconstructs the signal).
- **Failure Mode**: Beaming local coherent noise instead of the true carrier wave.
- **Falsification Path**: If the recovered waveform has an anomalous slowness vector inconsistent with the primary event, the trap recovery is false.

## 3. Hidden Lift (`hidden_lift`)
- **Observables**: (This is the *action* and *state* of recovering a projection trap). Coherent phase or amplitude vectors that exist *only* in transformed spaces (e.g., Double-Difference residual space).
- **Decision Rule**: Cross-correlation coefficient (CC) in the filtered/transformed domain exceeds $0.6$, whereas raw time-domain CC is $< 0.2$.
- **Failure Mode**: Over-filtering data (e.g., narrow-bandpass) to force sine waves to correlate.
- **Falsification Path**: Apply the exact same filter to a matched control noise window; if the control also yields $CC > 0.6$, the hidden lift is an artifact.

## 4. Relay Available (`relay_available`)
- **Observables**: Multiple disparate phases (e.g., $Pg$, $Pn$, $PmP$) connecting sequentially across the network.
- **Decision Rule**: An unbroken kinematic chain of arrivals can be traced from $A$ to $B$ passing through intermediate node sets without requiring a synthetic structural insertion.
- **Failure Mode**: Misidentifying a depth-phase as a continuous refracted phase.
- **Falsification Path**: Travel-time residuals for the relay chain exceed standard deviations ($> 3\sigma$).

## 5. Mediator Required (`mediator_required`)
- **Observables**: A hard gap exists in direct phases, but localized trapped energy, intense coda waves, or highly specific phase conversions are observed.
- **Decision Rule**: Gap can only be closed by mathematically inserting an external structural parameter (e.g., a "Fault Zone Guided Wave" corridor or a "Moho scatterer") that perfectly predicts the delayed/coda energy. 
- **Failure Mode**: The mediator is non-unique (multiple different structural geometries could produce the same scattered wavefield).
- **Falsification Path**: The proposed mediator fails to predict secondary observables (e.g., it predicts travel times but completely fails to predict 3C polarization angles).

## 6. Irrecoverable Gap (`irrecoverable_gap`)
- **Observables**: Missing data, stations offline, or noise levels exceeding the physical limits of the 24-bit digitizer.
- **Decision Rule**: No physical data exists to compute transformations; gap must be accepted as unverified.
- **Failure Mode**: Assuming it is a true barrier.
- **Falsification Path**: Future deployment of a denser array across the same spatial coordinates.
