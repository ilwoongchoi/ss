# THE SOVEREIGN EQUATIONS: K6 GRAPH LAPLACIAN DYNAMICS

This document records the definitive physical equations of the 128-grid sovereign system. All fake derivations and filler are removed.

## 1. THE ENERGY POTENTIAL (E)
The potential energy is defined over the K6 complete graph.
Equation: E = 1/2 * Sum [ w_ab * (x_a - x_b)^2 ]
- w_ab: Binary state (1 or 0) of the 15 edges.
- x_a, x_b: Coordinates of the 6 vertices.

## 2. THE DYNAMICS (dx/dt)
The time evolution of the system is the negative gradient of the energy potential.
Equation: dx/dt = -L * x
- L: The Graph Laplacian matrix derived from weights w_ab.
- x: The state vector of the 6 core particles.
- Result: Energy flows via diffusion toward the sovereign stationary state.

## 3. THE FUSION OBSERVABLE (F)
The measurable fusion rate output.
Equation: F = BW^2 * spark * Z * SM
- Target Range: 14.0 to 19.0 (varies by phase).
- Closure Condition: System is closed when F remains within this stable limit over 128 steps.

## 4. THE COORDINATE TRANSFORMATION
Mapping physical observables to graph vertices using constant C.
- BW = pr + (C * g)
- SM = nu + (C * q)
- Constant C = 0.2828 (sqrt(2/5))

## 5. THE 24-NODE ARCHITECTURE (6 + 15 + 3)
- 6 Vertices: pr (proton), nu (neutrino), g (gluon), q (quark), e (electron), gamma (photon).
- 15 Edges: All possible connections between the 6 vertices (Binary 1/0).
- 3 Closure Slots: 
    - Node 22 (Inflow/Past)
    - Node 23 (Ignition/Present)
    - Node 24 (Sovereign Closure/Future)
    - These 3 slots adjust the Laplacian L to ensure dx/dt = 0 at the 138.88-degree convergence point.
