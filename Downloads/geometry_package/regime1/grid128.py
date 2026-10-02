"""Regime-1 128-grid generation and 16x16 projection."""

from __future__ import annotations

import numpy as np

from .core_ops import emergent_nodes, plp_spine_gate_xy


def build_grid128(t_macro: float, resolution: int = 128) -> np.ndarray:
    return emergent_nodes(t_macro=t_macro, resolution=resolution)


def project_grid16x16(field128: np.ndarray) -> np.ndarray:
    field = np.asarray(field128, dtype=float).reshape(-1)
    if field.size == 0:
        raise ValueError("field128 must not be empty")
    sample_positions = np.linspace(0, field.size - 1, 16)
    sampled = np.interp(sample_positions, np.arange(field.size), field)
    chart = 0.5 * (sampled[:, None] + sampled[None, :])
    return chart


def plp_spine_mask_16x16() -> np.ndarray:
    mask = np.zeros((16, 16), dtype=float)
    for row in range(16):
        for col in range(16):
            mask[row, col] = plp_spine_gate_xy(col, row, n_rows=16.0, n_cols=16.0)
    return mask
