"""Canonical Regime-1 operators (geometry-only)."""

from __future__ import annotations

from typing import Dict

import numpy as np

from geometry_package.chart_operators import plp_spine_manifold, plp_spine_value
from geometry_package.universal_equation import (
    get_emergent_128_nodes,
    get_macro_micro_time,
    in_sh_band,
    kappa_eff,
    kappa_tda,
    w_gate,
)


def kappa_tda_from_persistence(persistence: float) -> float:
    return float(kappa_tda(float(persistence)))


def in_sh_band_rq0(r: float, q0: float) -> bool:
    return bool(in_sh_band(float(r), float(q0)))


def kappa_eff_rq0(r: float, q0: float, use_lookup: bool = True) -> float:
    return float(kappa_eff(float(r), float(q0), use_lookup=use_lookup))


def w_gate_rq0(r: float, q0: float) -> float:
    return float(w_gate(float(r), float(q0)))


def plp_spine_xy(x: float, y: float, n_rows: float = 16.0, n_cols: float = 16.0) -> float:
    return float(plp_spine_value(float(x), float(y), n_rows=n_rows, n_cols=n_cols))


def plp_spine_gate_xy(x: float, y: float, n_rows: float = 16.0, n_cols: float = 16.0) -> float:
    return float(plp_spine_manifold((float(x), float(y)), n_rows=n_rows, n_cols=n_cols))


def macro_micro_time(t_macro: float) -> tuple[float, bool]:
    t_micro, is_reverse = get_macro_micro_time(float(t_macro))
    return float(t_micro), bool(is_reverse)


def emergent_nodes(t_macro: float, resolution: int = 128) -> np.ndarray:
    return np.asarray(get_emergent_128_nodes(float(t_macro), resolution=int(resolution)), dtype=float)


def core_snapshot(r: float, q0: float, t_macro: float, resolution: int = 128) -> Dict[str, float]:
    nodes = emergent_nodes(t_macro=t_macro, resolution=resolution)
    t_micro, is_reverse = macro_micro_time(t_macro)
    return {
        "r": float(r),
        "q0": float(q0),
        "kappa_eff": kappa_eff_rq0(r, q0),
        "w_gate": w_gate_rq0(r, q0),
        "in_sh_band": 1.0 if in_sh_band_rq0(r, q0) else 0.0,
        "t_micro": float(t_micro),
        "is_reverse": 1.0 if is_reverse else 0.0,
        "funnel_occupancy": float(np.mean(np.abs(nodes))),
        "node_activation_sum": float(np.sum(nodes > 0.0)),
        "node_activation_ratio": float(np.mean(nodes > 0.0)),
    }
