# Final Domain-Neutral Closure Grammar

## Extracted from Geology/Seismology Pilot

---

## Core Structure

The closure grammar is a **reproducible, state-leakage-free method** for reconstructing hidden continuity in sparse observation systems.

### Fundamental Theorem

> **Internal Closure Theorem**: In any observation universe with nodes and candidate bridges, there exists a hard bound on component reduction achievable using only internal evidence.

> **Extended Closure Theorem**: A minimal external mediator can reduce the residual state beyond the internal bound, achieving full closure.

---

## Domain-Neutral Element Definitions

### NODE
**Definition**: Discrete evidence element with spatial/temporal coordinates

**Properties**:
- Observable above threshold
- Has identity (can be tracked)
- Carries attributes (strength, timing, quality)

**Domain examples**:
- Geology: Fault segment endpoint
- Seismology: Earthquake hypocenter
- Electron: Detector hit
- Network: Router/node

---

### BRIDGE
**Definition**: Hypothesis linking two nodes via continuity

**Properties**:
- Has contact (strength of evidence for connection)
- Has saddle (geometric/kinematic compatibility)
- Can be active or inactive

**Domain examples**:
- Geology: Fault trace projection
- Seismology: Event cluster alignment
- Electron: Track segment hypothesis
- Network: Link existence probability

---

### RELAY
**Definition**: Multi-step bridge via intermediate nodes

**Properties**:
- Chain of bridges: A → B → C
- Indirect connection when direct bridge invalid
- Cumulative contact/saddle constraints

**Domain examples**:
- Geology: Multi-segment fault chain
- Seismology: Event migration path
- Electron: Multi-point track fit
- Network: Multi-hop path

---

### MEDIATOR
**Definition**: Minimal external element enabling 2→1 closure

**Properties**:
- Not present in original observation universe
- Added via universe expansion
- Connects otherwise disconnected components
- Sufficient but not necessary (minimal)

**Domain examples**:
- Geology: Subsurface seismic corridor
- Seismology: Microseismicity cluster
- Electron: Sub-threshold signal
- Network: Latent relay node

---

### BARRIER
**Definition**: True structural discontinuity uncrossable by any mediator

**Properties**:
- Absolute veto on bridge formation
- Independent of observation quality
- Reflects fundamental system structure

**Domain examples**:
- Geology: Cross-cutting fault of different age
- Seismology: Stress regime boundary
- Electron: Detector material gap (true dead zone)
- Network: Air-gapped partition

---

### PROJECTION TRAP
**Definition**: Apparent discontinuity caused by observation limitations, not true barrier

**Properties**:
- No evidence for connection (locally)
- No evidence against connection
- May yield to deprojection or mediator insertion

**Domain examples**:
- Geology: Buried fault trace
- Seismology: Seismic network gap
- Electron: Sub-threshold hit region
- Network: Unmonitored network segment

---

### HIDDEN LIFT
**Definition**: Continuity evidence revealed by deprojection or coordinate transformation

**Properties**:
- Invisible in original projection
- Revealed by altered perspective
- Does not require new data (unlike mediator)

**Domain examples**:
- Geology: Fault plane intersection in 3D
- Seismology: Focal mechanism similarity in moment tensor space
- Electron: Track segment in drift time vs. position
- Network: Hidden path in latency space

---

### INTERNAL CLOSURE
**Definition**: Maximum component reduction achievable within original observation universe

**Properties**:
- Hard bound exists (usually > 1 component)
- Uses only local evidence
- Reproducible from scratch

**State**: N components (N ≥ 2)

---

### EXTENDED CLOSURE
**Definition**: Component reduction beyond internal bound via minimal mediator insertion

**Properties**:
- Requires universe expansion
- Each mediator is minimal (sufficient, not necessary)
- Achieves full closure (1 component) if sufficient mediators exist

**State**: 1 component (full connectivity)

---

## Framework Roles (The "Family")

### BIG MAN
**Role**: Mediator drive / Bridge forcing

**Function**: Conservation laws or strong constraints demand connection

**Domain examples**:
- Geology: Tectonic strain compatibility
- Seismology: Moment tensor sum
- Electron: Energy-momentum conservation
- Network: Traffic flow conservation

---

### BIG WOMAN
**Role**: Hard shell / True barrier enforcement

**Function**: Absolute constraints veto impossible connections

**Domain examples**:
- Geology: Cross-cutting relationships
- Seismology: Incompatible stress regimes
- Electron: Detector boundary conditions
- Network: Security policy partitions

---

### SMALL MAN
**Role**: Local seam substrate

**Function**: Direct connection without mediator

**Domain examples**:
- Geology: Continuous fault scarp
- Seismology: Immediate aftershock
- Electron: Adjacent hits
- Network: Direct link

---

### SMALL WOMAN
**Role**: Projection trap / Sparse observation

**Function**: Local evidence insufficient; requires deprojection or mediator

**Domain examples**:
- Geology: Alluvial cover
- Seismology: Station gap
- Electron: Missing hit region
- Network: Unmonitored hop

---

### MARRIAGE LAW
**Role**: Lifted continuity / Recovered connection

**Function**: Continuity restored across projection trap via mediator or deprojection

**Domain examples**:
- Geology: Fault continuity beneath cover
- Seismology: Hidden fault connection
- Electron: Track segment recovery
- Network: Path restoration

---

## Operational Procedure (Domain-Neutral)

### Phase 1: Internal Closure

1. **Enumerate nodes**: All discrete evidence elements above threshold
2. **Score bridges**: Contact (evidence strength) and saddle (compatibility)
3. **Build DSU**: Activate bridges above thresholds
4. **Count components**: Record C_internal
5. **Identify isolated components**: Candidates for extended closure

### Phase 2: Extended Closure

1. **Classify gaps**: Projection trap vs. true barrier
2. **Identify mediators**: Minimal external elements connecting isolated components
3. **Insert mediators**: Expand universe
4. **Recompute closure**: Build new DSU with mediators
5. **Count components**: Record C_extended

### Phase 3: Validation

1. **Verify barrier resistance**: True barriers remain unconnected
2. **Measure reduction**: C_internal → C_extended
3. **Test reproducibility**: Replay from scratch

---

## Reuse Contract

```python
def closure_reconstruction(nodes, bridges, mediators=None):
    """
    Domain-neutral closure grammar implementation.
    
    Args:
        nodes: List of evidence elements
        bridges: List of (node_a, node_b, contact, saddle)
        mediators: Optional list of external nodes for extended closure
    
    Returns:
        components: DSU component count
        component_map: Node -> component assignment
        classification: Gap classifications (barrier, trap, connected)
    """
    dsu = DSU(nodes)
    
    # Phase 1: Internal closure
    for a, b, contact, saddle in bridges:
        if contact > contact_threshold and saddle > saddle_threshold:
            dsu.union(a, b)
    
    C_internal = dsu.components()
    
    # Phase 2: Extended closure (if mediators provided)
    if mediators:
        for m in mediators:
            dsu.add_node(m)
            # Connect mediator to compatible components
            for node in nodes:
                if compatible(m, node):
                    dsu.union(m, node)
    
    C_extended = dsu.components()
    
    return {
        'C_internal': C_internal,
        'C_extended': C_extended,
        'reduction': C_internal - C_extended,
        'component_map': dsu.get_components()
    }
```

---

*Domain-neutral closure grammar: Validated in geology, ready for transfer*
