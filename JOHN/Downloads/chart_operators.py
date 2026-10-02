#!/usr/bin/env python3
"""
chart_operators.py
==================
Canonical, single-source implementations of the core geometric operators.

These functions were previously implicit in various shaders and grid generators.
Formalizing them here allows for consistent, verifiable use across all domains.
"""

from __future__ import annotations

import math
from typing import Tuple

from geometry_package.absolute_constants import SPARK_ANGLE_RAD

# Default chart shape (the canonical 16×16 grid).
DEFAULT_N_ROWS = 16.0
DEFAULT_N_COLS = 16.0


def solve_radial_psi(k: float) -> float:
    """Newton-Raphson solver for the cubic radial organizer equation: ψ³ - ψ - k = 0."""
    x = 1.0  # Initial guess
    # 3 iterations is the standard used in the reference shaders.
    for _ in range(3):
        # Avoid division by zero for x near sqrt(1/3)
        denominator = 3.0 * x * x - 1.0
        if abs(denominator) < 1e-9:
            # If the derivative is close to zero, nudge x slightly.
            x += 1e-6
            denominator = 3.0 * x * x - 1.0
        
        x = x - (x * x * x - x - k) / denominator
    return float(x)


def plp_spine_value(
    x: float,
    y: float,
    *,
    n_rows: float = DEFAULT_N_ROWS,
    n_cols: float = DEFAULT_N_COLS,
) -> float:
    """
    Normalized PLP spine seam value.

    Seam equation (normalized):
      x/n_cols + y/n_rows = 1

    Returns:
      value < 0  : below the seam
      value == 0 : on the seam
      value > 0  : on/above the seam
    """
    if n_rows <= 0 or n_cols <= 0:
        raise ValueError("n_rows and n_cols must be positive")
    return (x / n_cols) + (y / n_rows) - 1.0


def plp_spine_gate(
    x: float,
    y: float,
    *,
    n_rows: float = DEFAULT_N_ROWS,
    n_cols: float = DEFAULT_N_COLS,
    eps: float = 0.0,
) -> float:
    """Returns 1.0 if on/above the PLP spine seam, else 0.0."""
    return 1.0 if plp_spine_value(x, y, n_rows=n_rows, n_cols=n_cols) >= -float(eps) else 0.0


def plp_spine_manifold(
    pos: Tuple[float, float],
    *,
    n_rows: float = DEFAULT_N_ROWS,
    n_cols: float = DEFAULT_N_COLS,
) -> float:
    """Compatibility wrapper used by the shaders: pos=(x,y) -> {0.0,1.0}."""
    return plp_spine_gate(pos[0], pos[1], n_rows=n_rows, n_cols=n_cols)


def spark_refraction(vector: Tuple[float, float]) -> Tuple[float, float]:
    """
    Applies the spark refraction operator, rotating a 2D vector by the exact
    SPARK_ANGLE_RAD.
    """
    c = math.cos(SPARK_ANGLE_RAD)
    s = math.sin(SPARK_ANGLE_RAD)
    x, y = vector
    
    rotated_x = c * x - s * y
    rotated_y = s * x + c * y
    
    return (rotated_x, rotated_y)
