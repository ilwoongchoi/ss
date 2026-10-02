"""Unified canonical engine step function.

Combines:
  1. Spark gate (spark_gate.py)
  2. Lensing operator (lensing.py)
  3. Rebranching operator (rebranching.py)
  4. 24D homeostasis + 8D risk memory (engineering_homeostasis_24.py)

State representation
---------------------
Y = (X24, r8)  — the 32D canonical state vector, split as two arrays
    X24 : np.ndarray shape (24,)
    r8  : np.ndarray shape (8,)

Inputs per step
---------------
c24     : np.ndarray shape (24,)  raw control-channel vector (ground truth
          order per HOMEOSTASIS_24_SCHEDULE_128.csv)
d_risk  : float, exogenous risk scalar (independent of c24)
nor,plp : floats in [0,1] driving the spark gate
dt      : float time step

Returns
-------
(X24_next, r8_next, diagnostics: dict)
"""
from __future__ import annotations

from typing import Dict, Tuple

import numpy as np

from .fusion_core import RAW_COUNT
from .spark_gate import spark_gate
from .lensing import (
    lensing_operator,
    particle_potentials,
    graph_diffusion_delta,
    expand_to_24,
)
from .rebranching import RebranchState, rebranching_operator
from .engineering_homeostasis_24 import step_homeostasis


KAPPA_COUPLE = 0.05  # structural-graph → homeostasis feedback gain


class CanonicalEngine:
    """Stateful wrapper holding rebranch hysteresis across steps."""

    def __init__(self) -> None:
        self.rebranch_state = RebranchState()

    def step(
        self,
        X24: np.ndarray,
        r8: np.ndarray,
        c24: np.ndarray,
        d_risk: float,
        *,
        nor: float,
        plp: float,
        dt: float = 1.0,
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, object]]:
        if c24.shape != (RAW_COUNT,):
            raise ValueError(f"c24 must have shape ({RAW_COUNT},)")

        # 1. Spark gate scalar
        gate = spark_gate(nor, plp)

        # 2. Structural operators (lensing + rebranching): produce an 8x8
        #    K8 adjacency, then close the loop by converting it into a
        #    graph-diffusion delta that feeds back into the 24D
        #    homeostasis derivative (see engineering_homeostasis_24.py).
        phi = particle_potentials(X24)
        adj_lensed = lensing_operator(X24)
        adj_final = rebranching_operator(adj_lensed, phi, self.rebranch_state)

        delta8 = graph_diffusion_delta(adj_final, phi)
        coupling24 = KAPPA_COUPLE * expand_to_24(delta8)

        # 3. Homeostasis + risk-memory Euler step (structural feedback included)
        X24_next, r8_next = step_homeostasis(
            X24, r8, c24, d_risk, gate, dt=dt, coupling24=coupling24
        )

        diagnostics = {
            "gate": gate,
            "d_risk": d_risk,
            "phi": phi,
            "adj_final": adj_final,
            "rebranch_flags": dict(self.rebranch_state.flags),
        }
        return X24_next, r8_next, diagnostics


__all__ = ["CanonicalEngine"]
