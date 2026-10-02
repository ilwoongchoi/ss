"""Scalar spark gate function.
Implements g_spark = σ(α·(nor − θ) + β·plp + γ·noise)
Where:
  - `nor`  : NOR-default channel (normalized 0-1)
  - `plp`  : PLP-default channel (normalized 0-1)
  - `noise`: small gaussian noise term
Coefficients α,β,γ,θ are drawn from repository defaults; adjust later.
"""
from __future__ import annotations

import math
import random
from typing import Optional

# Coefficients (docs: gate fractions 1/32, 3/32, collapse 1/128)
_ALPHA = 32.0  # scale for NOR deviation
_BETA = 10.0   # plp sensitivity
_GAMMA = 0.1   # noise weight
_THETA = 1.0 / 32.0  # stable leakage threshold


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def spark_gate(nor: float, plp: float, *, noise: Optional[float] = None) -> float:
    """Return gate scalar in [0,1].  Inputs expected ∈[0,1]."""
    if noise is None:
        noise = random.gauss(0.0, 0.02)
    z = _ALPHA * (nor - _THETA) + _BETA * plp + _GAMMA * noise
    return _sigmoid(z)

__all__ = ["spark_gate"]
