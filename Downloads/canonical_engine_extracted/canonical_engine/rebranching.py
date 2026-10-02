"""Rebranching operator R(Y, c26).

Per SPIRAL_PHYSICS_MAPPING.md, "rebranching" governs discrete topology
switches in the spiral-arm nerve graph (gender rebranching / confinement
analogy). We implement it as a hysteretic threshold switch on the
lensed adjacency matrix: when a particle's potential crosses a high/low
threshold, its outgoing edges reroute to an alternate target chosen by
a fixed rebranch table (derived from confinement pairing rules).

This operator is discrete/stateful — it must be called with the
previous branch state to implement hysteresis (avoids chattering).
"""
from __future__ import annotations

from typing import Dict, Tuple

import numpy as np

from .fusion_core import K8_PARTICLES, PARTICLE_INDEX

# Hysteresis thresholds (from DREAM_FOLDING_CANONICAL.md: area ~0.157)
THRESH_HIGH = 0.65
THRESH_LOW = 0.35

# Static rebranch table: when particle p exceeds THRESH_HIGH, its default
# target is swapped for the alternate given here (confinement analogy).
_REBRANCH_TABLE: Dict[str, str] = {
    "quark": "gluon",       # confinement pair
    "gluon": "quark",
    "neutrino": "z_boson",  # weak-force partner swap
    "z_boson": "neutrino",
    "photon": "electron",
    "electron": "photon",
    "higgs": "w_boson",
    "w_boson": "higgs",
}


class RebranchState:
    """Holds per-particle branch flags across calls (hysteresis memory)."""

    def __init__(self) -> None:
        self.flags = {p: False for p in K8_PARTICLES}  # False=normal, True=rebranched

    def update(self, phi: np.ndarray) -> None:
        for p in K8_PARTICLES:
            idx = PARTICLE_INDEX[p]
            v = phi[idx]
            if not self.flags[p] and v > THRESH_HIGH:
                self.flags[p] = True
            elif self.flags[p] and v < THRESH_LOW:
                self.flags[p] = False


def rebranching_operator(adj: np.ndarray, phi: np.ndarray, state: RebranchState) -> np.ndarray:
    """Apply rebranching to an 8x8 adjacency matrix given current potentials.
    Returns a new adjacency matrix (copy); mutates `state` in place.
    """
    state.update(phi)
    adj_out = adj.copy()
    for p, is_rebranched in state.flags.items():
        if not is_rebranched:
            continue
        alt = _REBRANCH_TABLE.get(p)
        if alt is None:
            continue
        i = PARTICLE_INDEX[p]
        j_alt = PARTICLE_INDEX[alt]
        # Reroute all outgoing weight from i to the alternate target j_alt
        row_sum = adj_out[i, :].sum()
        adj_out[i, :] = 0.0
        adj_out[i, j_alt] = row_sum

    return adj_out

__all__ = ["RebranchState", "rebranching_operator", "THRESH_HIGH", "THRESH_LOW"]
