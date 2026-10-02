# Electron Observable Map: Closure Grammar Elements

## Observable: HIT

**Closure mapping**: Node

**Measurement**:
- Position (x, y, z) in detector coordinates
- Energy deposition dE/dx
- Timing t relative to trigger

**Component role**: Primary node in DSU

**Closure condition**: Hit qualifies as node when dE/dx > threshold and timing within window

---

## Observable: CHARGE DEPOSITION

**Closure mapping**: Bridge weight / Contact metric

**Measurement**:
- Integrated charge Q in drift cell
- Pulse shape parameters (rise time, width)
- Cluster size in pixel/strip detectors

**Component role**: Determines bridge viability

**Closure condition**: 
- High charge → strong contact (bridge likely valid)
- Low charge → weak contact (bridge may be projection trap)

---

## Observable: TIMING

**Closure mapping**: Synchronization constraint / Shell boundary

**Measurement**:
- Drift time in gaseous detectors
- Time-over-threshold in silicon
- Coincidence windows between layers

**Component role**: Big Woman (shell veto) — timing inconsistent with trajectory breaks bridge

**Closure condition**: |t_expected - t_observed| < Δt_resolution

---

## Observable: SCATTERING ANGLE

**Closure mapping**: Geometric compatibility / Saddle metric

**Measurement**:
- Deflection angle θ between track segments
- Multiple Coulomb scattering deviation
- Kink angle at vertex candidates

**Component role**: Determines saddle quality of bridge

**Closure condition**: θ < θ_max(energy, material) for continuous track

---

## Observable: LATENT MEDIATOR

**Closure mapping**: External mediator (synthetic_alpha equivalent)

**Measurement**:
- Low-amplitude signal below standard threshold
- Secondary vertex from scattering
- Cross-detector correlation (e.g., calorimeter energy deposit matching missing momentum)

**Component role**: Extended universe node enabling 2→1 closure

**Closure condition**: Mediator must connect two otherwise disconnected components

**Falsifiable signature**:
- Presence of sub-threshold signal in gap region
- Timing correlation with track endpoints
- Scattering angle consistency with material budget

---

## Observable: PROJECTION GAP

**Closure mapping**: Barrier / gateway_peak isolation

**Measurement**:
- Distance between last hit and next candidate
- Material thickness in gap region
- Expected hit density vs. observed

**Component role**: Internal boundary where local reconstruction fails

**Closure condition**: Gap distance > reconstruction search window

**Critical distinction**:
- Standard view: Gap = "no electron passed here"
- Closure view: Gap = "projection trap — mediator may exist"

---

## Observable: RELAY PATH

**Closure mapping**: Multi-layer connection

**Measurement**:
- Hit in intermediate detector layer
- Consistent trajectory through three or more points
- Reduced χ² for track fit

**Component role**: Lane C relay — indirect connection via intermediate

**Closure condition**: χ²/n_dof < threshold AND timing consistent

---

## Observable: DETECTOR SHELL

**Closure mapping**: Big Woman (boundary condition)

**Measurement**:
- Active volume boundaries
- Material budget distribution
- Magnetic field uniformity

**Component role**: Veto on impossible trajectories, enables deprojection

---

## Observable: MEDIATOR DRIVE

**Closure mapping**: Big Man (bridge drive)

**Measurement**:
- Energy momentum conservation at gap
- Calorimeter deposition matching track energy loss
- Bremsstrahlung photon conversion point

**Component role**: Forces bridge activation when conservation laws demand connection

---

## Observable: LOCAL SEAM

**Closure mapping**: Small Man

**Measurement**:
- Adjacent hits in same detector layer
- Small-angle scattering within single volume
- Continuous charge deposition in drift chamber

**Component role**: Direct bridge without need for external mediator

---

## Observable: PROJECTION TRAP

**Closure mapping**: Small Woman

**Measurement**:
- Missing hit in expected trajectory extrapolation
- Energy loss without corresponding hit
- Timing window with no associated signal

**Component role**: Local evidence insufficient; deprojection or external mediator required

---

## Summary Table

| Closure Element | Primary Observable | Secondary Observable |
|-----------------|-------------------|---------------------|
| Node | Hit position | Charge deposition |
| Bridge | Track segment | Scattering angle |
| Relay | Multi-hit chain | Reduced χ² |
| Barrier | Projection gap | Missing hit |
| Big Man | Energy conservation | Calorimeter deposit |
| Big Woman | Timing window | Detector boundary |
| Small Man | Local seam | Adjacent hits |
| Small Woman | Projection trap | Missing signal |
| External mediator | Latent hit | Sub-threshold signal |

---

*Observable map: Every closure element grounded in detector measurement*
