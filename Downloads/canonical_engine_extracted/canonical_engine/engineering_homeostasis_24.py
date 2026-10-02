"""24-dimensional homeostasis subsystem + 8-dim risk-memory.
Implements
    Ẋ = A (X − Ω R d) + B (u_base + |C_spark|·gate) − g (X ⊙ |X|) + P_r r + P_M d_risk
    ṙ = −λ r + M d_risk
Numbers A, B, g, P_r, P_M are placeholders for now; tune later.

Usage:
    from canonical_engine.engineering_homeostasis_24 import step_homeostasis
    X_next, r_next = step_homeostasis(X, r, u26, d_risk, dt)
"""
from __future__ import annotations

from typing import Tuple

import numpy as np

from .absolute_constants import (
    OMEGA,
    LAMBDA_RISK_DECAY as _LAM,
    M_RISK_GAIN as _MGAIN,
    SPARK_MAGNITUDE as _CS,
)
from .fusion_core import RAW_COUNT, CHANNEL_INDEX

# --- Projection P24 (identity) ----------------------------------------------
# Ground-truth CSV data (HOMEOSTASIS_24_SCHEDULE_128.csv, u_* vs state_*
# columns) confirms a direct 1:1 correspondence between each raw channel
# and its homeostasis state dimension -- no cross-channel mixing.
assert RAW_COUNT == 24, "fusion_core channel list must have exactly 24 entries"
P24 = np.eye(24, dtype=float)

# Parameter matrices (placeholders – diagonal unity)
# NOTE: A is the *restoring* gain, applied with a leading minus sign in
# step_homeostasis (i.e. dX contains -A(X - eq)) so the system relaxes
# toward the driven equilibrium Ω·u24 instead of diverging.
A = np.eye(24) * 0.3
B = np.eye(24)
g_diag = np.ones(24) * 0.1  # cubic damping coefficient
P_r = np.zeros((24, 8))
np.fill_diagonal(P_r, 0.05)  # couples first 8 homeostasis dims to risk-memory
P_M = np.eye(24) * 0.02

# ---------------------------------------------------------------------------

def project_channels(c24: np.ndarray) -> np.ndarray:
    """u24 = P24 x c24 (identity projection; see module docstring)."""
    return P24 @ c24


def three_forces_coupling(
    V: float,          # Vasopressin force (depth / inward binding)
    alpha2: float,     # Alpha-2 phase/topology switch force
    C_r: float,        # Right-cortisol stress-curvature / spark drive force
    c24: np.ndarray,   # shape (24,) raw control channels
    *,
    k_V: float = 0.5,
    k_a2: float = 0.3,
    k_C: float = 0.5,
) -> np.ndarray:
    """Convert the three effective forces into a 24-dim coupling vector.

    The forces are EM-effective couplings on the raw control graph, written
    in the form Δw = k · signal · M · c24:

      - V (vasopressin)     : depth/inward bias on the (ν, p) edge.
                              proxy channel = water_vapour.
      - alpha2              : phase gate on the (ν, p) and (ν, e) edges.
                              The gate factor is (1 - alpha2^2):
                              alpha2 = 0 -> gate fully open,
                              alpha2 -> ±1 -> gate closed.
                              proxy channels = observer_leftd2 / nonobserver_left_d2.
      - C_r (right cortisol): stress-curvature / spark drive on (γ, p) and (γ, e).
                              proxy channels = right_sole_dopamine and mc1r.
    """
    coupling = np.zeros(RAW_COUNT)

    # V : ν-p inward binding
    if V != 0.0:
        nu = CHANNEL_INDEX["water_vapour"]
        coupling[nu] += k_V * V * c24[nu]

    # alpha2 : phase/topology gate, open when alpha2 -> 0
    if alpha2 != 0.0:
        gate = 1.0 - (alpha2 * alpha2)
        nu_p = CHANNEL_INDEX["observer_leftd2"]
        nu_e = CHANNEL_INDEX["nonobserver_left_d2"]
        coupling[nu_p] += k_a2 * gate * c24[nu_e]
        coupling[nu_e] += k_a2 * gate * c24[nu_p]

    # C_r : right-cortisol stress-curvature / spark drive on (γ, p/e)
    if C_r != 0.0:
        gamma = CHANNEL_INDEX["mc1r"]
        p = CHANNEL_INDEX["right_sole_dopamine"]
        coupling[p] += k_C * C_r * c24[gamma]
        coupling[gamma] += k_C * C_r * c24[p]

    return coupling


def step_homeostasis(
    X: np.ndarray,   # shape (24,)
    r: np.ndarray,   # shape (8,)
    c24: np.ndarray, # shape (24,) raw control channels
    d_risk: float,
    gate_scalar: float,
    dt: float = 1.0,
    coupling24: np.ndarray | None = None,  # optional structural feedback term
) -> Tuple[np.ndarray, np.ndarray]:
    """Single Euler step for homeostasis + risk memory.

    `coupling24`, if provided, is an additive (24,) term coming from the
    lensing/rebranching structural operators (see fusion_clean.py). This
    closes the loop so structural K8-graph state actually influences the
    scalar homeostasis dynamics instead of being diagnostic-only.
    """
    if X.shape != (24,) or r.shape != (8,) or c24.shape != (RAW_COUNT,):
        raise ValueError("Dimension mismatch on inputs")

    u24 = project_channels(c24)
    # raw control after spark gate influence
    u_eff = u24 + _CS * gate_scalar

    # Homeostasis derivative (note leading minus on restoring term A)
    dX = (
        -A @ (X - OMEGA * u24)
        + B @ u_eff
        - g_diag * (X * np.abs(X))
        + P_r @ r
        + P_M @ (d_risk * np.ones(24))
    )

    if coupling24 is not None:
        if coupling24.shape != (24,):
            raise ValueError("coupling24 must have shape (24,)")
        dX = dX + coupling24

    # Risk memory derivative
    dr = -_LAM * r + _MGAIN * d_risk

    X_next = X + dt * dX
    r_next = r + dt * dr
    return X_next, r_next

__all__ = ["project_channels", "step_homeostasis", "three_forces_coupling", "P24"]
