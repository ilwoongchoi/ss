"""Lensing operator L(Y, c26).

Per CANONICAL_FINAL_EQUATION.md, lensing bends the effective K8 particle
graph based on the current 32-dim state Y=[X;r] and raw channel vector.
This is a structural extension that was previously *missing*; the
implementation below is a first, minimal, testable version:

    L(Y, c26)_{ij} = base_weight_{ij} * (1 + κ * tanh(X_i - X_j))

where κ is a lensing-strength constant and base_weight comes from the
static edge ontology in fusion_core.EDGE_MAP (edge presence → 1.0).

This produces a *modulated* adjacency matrix over the K8 basis that can
be used to reweight coupling before it's fed into homeostasis
projection, without altering the raw channel semantics.
"""
from __future__ import annotations

import numpy as np

from .fusion_core import K8_PARTICLES, PARTICLE_INDEX, EDGE_MAP

KAPPA_LENS = 0.15  # lensing strength, tuned conservatively

N_K8 = len(K8_PARTICLES)

# Static base adjacency (1.0 where an edge exists in EDGE_MAP, else 0.0)
_BASE_ADJ = np.zeros((N_K8, N_K8), dtype=float)
for (src, dst) in EDGE_MAP.keys():
    i, j = PARTICLE_INDEX[src], PARTICLE_INDEX[dst]
    _BASE_ADJ[i, j] = 1.0


def particle_potentials(X24: np.ndarray) -> np.ndarray:
    """Reduce 24D homeostasis state to an 8D K8 potential proxy.
    Simple scheme: average consecutive 3-blocks of X24 → 8 potentials.
    (24 = 8 particles * 3 homeostasis channels each, matching K8 grouping
    order in fusion_core.C26_CHANNELS layout.)
    """
    if X24.shape != (24,):
        raise ValueError("X24 must be shape (24,)")
    return X24.reshape(8, 3).mean(axis=1)


def lensing_operator(X24: np.ndarray) -> np.ndarray:
    """Return the lensed adjacency matrix L (8x8) given current state."""
    phi = particle_potentials(X24)  # shape (8,)
    diff = phi[:, None] - phi[None, :]
    modulation = 1.0 + KAPPA_LENS * np.tanh(diff)
    return _BASE_ADJ * modulation

def graph_diffusion_delta(adj: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """Graph-Laplacian diffusion term over K8 potentials.
    delta_i = sum_j adj[i,j] * (phi_j - phi_i)
    Returns shape (8,).
    """
    deg = adj.sum(axis=1)
    return (adj @ phi) - deg * phi


def expand_to_24(delta8: np.ndarray) -> np.ndarray:
    """Broadcast an 8D particle-level delta back to the 24D homeostasis
    space, matching the (8 particles x 3 channels) grouping used in
    particle_potentials(). Each particle's delta is repeated 3x.
    """
    if delta8.shape != (8,):
        raise ValueError("delta8 must have shape (8,)")
    return np.repeat(delta8, 3)


__all__ = [
    "lensing_operator",
    "particle_potentials",
    "graph_diffusion_delta",
    "expand_to_24",
    "KAPPA_LENS",
]
