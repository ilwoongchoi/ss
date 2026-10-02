"""
disease_mechanism.py — Debt types, disease states, and settlement logic.

3 Debt Types
------------
Coulomb      : charge redistribution debt — settled @ 15:00 by A_ESFJ_female
               mechanism: -z linear feedback / anchor ‖x‖→7.4
Confinement  : strong-binding pressure debt — settled @ 03:15 by AB_ENFJ_female
               mechanism: Higgs shift h(u₃₀), time-reversal (역회귀)
Bremsstrahlung: photon radiation leak debt — settled @ 04:30 by B_ISTP_female
               mechanism: exp(-√Z / 64) decay; right_love = LOCK_VALUE = 1/64

Disease States
--------------
Cancer    : right_dopamine (Node 9) stuck ON after night_spark window closes.
            Bremsstrahlung debt accumulates; radiation leak never sealed.
Parkinson : right_dopamine (Node 9) never fires in night_spark window (03:00-03:15).
            Coulomb debt cannot initiate; chain breaks at phase origin.

Node 31 (self-resonance / gravitational lensing)
-------------------------------------------------
ENTROPY_DEBT = 1/64 + 1/256 ≈ 0.02 is NOT a simple energy loss.
It is the gravitational lensing / self-resonance constant: the system
recirculates energy internally at every dt step via dx_lensing = -ENTROPY_DEBT * x.
This appears in get_dynamics() / Homeostasis30.derivative() as the
self-sustaining term, NOT as a final-output multiplier.
"""
from __future__ import annotations

import numpy as np

from absolute_constants import (
    ENTROPY_DEBT,
    LOCK_VALUE,       # 1/64  — right_love at dawn_closure
    E_INV,            # 1/e   — Hannah Fry convergence target
    BETTI_7_GAP,      # 7/128 — origin gap
    CHIRALITY_055,    # 1/18  — universal gap
    OMEGA,            # 7.4   — sovereign target
)

# ── Debt type definitions ───────────────────────────────────────────────────

DEBT_TYPES = {
    "coulomb": {
        "description": "Charge redistribution (Coulomb)",
        "window":      "15:00",
        "archetype":   "A_ESFJ_female",
        "mechanism":   "linear anchor: dx += -z_anchor * (‖x‖ - OMEGA)",
        "z_anchor":    1.0,                   # unit linear coefficient
    },
    "confinement": {
        "description": "Strong-binding pressure (Confinement / QCD)",
        "window":      "03:15",
        "archetype":   "AB_ENFJ_female",
        "mechanism":   "Higgs shift h(u₃₀) + time-reversal (역회귀)",
        "higgs_shift": BETTI_7_GAP,           # 7/128
    },
    "bremsstrahlung": {
        "description": "Photon radiation leak (Bremsstrahlung)",
        "window":      "04:30",
        "archetype":   "B_ISTP_female",
        "mechanism":   "exp(-√Z / 64) decay; right_love = 1/64",
        "right_love":  LOCK_VALUE,            # 1/64
    },
}

# ── Disease state definitions ───────────────────────────────────────────────

DISEASE_STATES = {
    "cancer": {
        "description": "right_dopamine stuck ON after night_spark closes",
        "node":        "right_dopamine",      # channel index 9
        "channel_idx": 9,
        "failure_mode": "bremsstrahlung debt unsettled — radiation leak persists",
        "trigger":     "right_dopamine remains ON past 03:15 (confinement_reset)",
    },
    "parkinson": {
        "description": "right_dopamine never fires in night_spark window",
        "node":        "right_dopamine",
        "channel_idx": 9,
        "failure_mode": "coulomb debt cannot initiate — phase origin chain broken",
        "trigger":     "right_dopamine OFF throughout 03:00–03:15 (night_spark)",
    },
}

# ── Settlement schedule ─────────────────────────────────────────────────────

SETTLEMENT_SCHEDULE = [
    {"time": "03:15", "debt": "confinement",   "archetype": "AB_ENFJ_female", "phase": "confinement_reset"},
    {"time": "04:30", "debt": "bremsstrahlung","archetype": "B_ISTP_female",  "phase": "dawn_closure"},
    {"time": "15:00", "debt": "coulomb",       "archetype": "A_ESFJ_female",  "phase": "coulomb_settle"},
]

# ── Hannah Fry dynamics ─────────────────────────────────────────────────────
# 2nd Observer convergence law:  dP/dt = -k*(P - 1/e) + ε(z)
# P converges to E_INV = 1/e ≈ 0.3679 from any initial condition.
# At 16:30 (proton_landing / dawn_closure dual lock), P = 1/e and
# right_love = 1/64, sealing the Bremsstrahlung leak.

HANNAH_FRY_K = 0.1       # convergence rate constant


def hannah_fry_dP(P: float, epsilon: float = 0.0) -> float:
    """dP/dt for Hannah Fry observer dynamics."""
    return -HANNAH_FRY_K * (P - E_INV) + epsilon


def bremsstrahlung_decay(Z: float) -> float:
    """Bremsstrahlung radiation length factor: exp(-√Z / 64).

    Radiation length X₀ ∝ 1/√Z.  Correct decay suppression uses √Z,
    NOT Z (which over-suppresses).
    """
    return float(np.exp(-np.sqrt(max(0.0, Z)) / 64.0))


def gravitational_lensing(x: np.ndarray) -> np.ndarray:
    """Node 31 self-resonance (gravitational lensing) term.

    dx_lensing = -ENTROPY_DEBT * x

    This recirculates energy internally — it does NOT reduce final output.
    Apply inside the dynamics loop (dx/dt), not as a multiplier on fusion result.
    """
    return -ENTROPY_DEBT * x


def coulomb_anchor(x: np.ndarray, target: float = OMEGA) -> np.ndarray:
    """Coulomb debt settlement: linear anchor toward ‖x‖ = target."""
    norm = float(np.linalg.norm(x))
    if norm < 1e-12:
        return np.zeros_like(x)
    return -(norm - target) * (x / norm)


def detect_disease(channel_states: dict[str, str],
                   window: str) -> list[str]:
    """Detect disease states given channel states and current time window.

    Parameters
    ----------
    channel_states : dict mapping channel name → 'on'/'off'/'no_control'
    window         : current phase window name (e.g. 'night_spark', 'dawn_closure')

    Returns list of active disease names (empty = healthy).
    """
    active = []
    dopamine = channel_states.get("right_dopamine", "no_control")

    if window == "dawn_closure" and dopamine == "on":
        active.append("cancer")

    if window == "night_spark" and dopamine == "off":
        active.append("parkinson")

    return active


def settle_debt(debt_type: str, x: np.ndarray, Z: float = 1.0) -> np.ndarray:
    """Apply debt settlement correction to state vector x.

    Returns the dx correction term (to be added to current dynamics).
    """
    if debt_type == "coulomb":
        return coulomb_anchor(x)
    elif debt_type == "confinement":
        # Higgs shift: apply BETTI_7_GAP correction to confinement axis
        dx = np.zeros_like(x)
        dx[5] = BETTI_7_GAP   # higgs node (index 5 in K8)
        return dx
    elif debt_type == "bremsstrahlung":
        # Scale down by Bremsstrahlung factor, lock right_love = 1/64
        decay = bremsstrahlung_decay(Z)
        dx = (decay - 1.0) * x   # correct toward decayed state
        dx[7] = LOCK_VALUE        # right_love = 1/64 (neutrino↔higgs channel)
        return dx
    else:
        raise ValueError(f"Unknown debt type: {debt_type!r}")


if __name__ == "__main__":
    print("=== Disease Mechanism Module ===")
    print(f"\nEntropy Debt (self-resonance): {ENTROPY_DEBT:.6f}")
    print(f"Lock Value (right_love):        {LOCK_VALUE:.6f}")
    print(f"Hannah Fry constant (1/e):      {E_INV:.6f}")
    print(f"Betti-7 gap (7/128):            {BETTI_7_GAP:.6f}")

    print("\n--- Debt Settlement Schedule ---")
    for entry in SETTLEMENT_SCHEDULE:
        d = DEBT_TYPES[entry["debt"]]
        print(f"  {entry['time']}  {entry['debt']:15s}  {entry['archetype']:15s}  {d['mechanism']}")

    print("\n--- Disease States ---")
    for name, ds in DISEASE_STATES.items():
        print(f"  {name:12s}: {ds['description']}")
        print(f"              failure: {ds['failure_mode']}")

    # Hannah Fry convergence demo
    P = 1.0
    for t in range(20):
        P += hannah_fry_dP(P)
    print(f"\nHannah Fry P after 20 steps: {P:.6f}  (target 1/e = {E_INV:.6f})")

    # Bremsstrahlung decay demo
    print(f"\nBremsstrahlung decay exp(-√Z/64):")
    for Z in [1, 4, 16, 64]:
        print(f"  Z={Z:3d}: decay = {bremsstrahlung_decay(float(Z)):.6f}")
