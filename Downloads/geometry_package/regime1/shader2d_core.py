"""Regime-1 2D chart shader interface (geometry-only fields)."""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np

from . import core_constants as c
from .core_ops import in_sh_band_rq0, kappa_eff_rq0, plp_spine_gate_xy, w_gate_rq0


def xy_to_rq0(x: float, y: float, n_rows: int = 16, n_cols: int = 16) -> Tuple[float, float]:
    x_norm = float(x) / max(float(n_cols - 1), 1.0)
    y_norm = float(y) / max(float(n_rows - 1), 1.0)
    r = c.SH_R_BAND_MIN + x_norm * (c.SH_R_BAND_MAX - c.SH_R_BAND_MIN)
    q0 = c.SH_Q0_MIN + y_norm * (c.SH_Q0_MAX - c.SH_Q0_MIN)
    return float(r), float(q0)


def sample_core_fields_rq0(r: float, q0: float) -> Dict[str, float]:
    return {
        "r": float(r),
        "q0": float(q0),
        "w_gate": float(w_gate_rq0(r, q0)),
        "kappa_eff": float(kappa_eff_rq0(r, q0)),
        "in_sh_band": 1.0 if in_sh_band_rq0(r, q0) else 0.0,
        "plp_spine": 0.0,
    }


def sample_core_fields_xy(x: float, y: float, n_rows: int = 16, n_cols: int = 16) -> Dict[str, float]:
    r, q0 = xy_to_rq0(x, y, n_rows=n_rows, n_cols=n_cols)
    fields = sample_core_fields_rq0(r, q0)
    fields["plp_spine"] = float(plp_spine_gate_xy(x, y, n_rows=float(n_rows), n_cols=float(n_cols)))
    fields["x"] = float(x)
    fields["y"] = float(y)
    return fields


def compute_height_scalar(fields: Dict[str, float]) -> float:
    w = float(fields["w_gate"])
    k_eff = float(fields["kappa_eff"])
    in_band = float(fields["in_sh_band"])
    plp = float(fields.get("plp_spine", 0.0))

    base = c.TUNNEL_TENSION * w
    kappa_term = c.KAPPA_TDA_MID / max(k_eff, 1e-12)
    band_term = c.KAPPA_TDA_MID * in_band
    seam_term = c.LATTICE_3_32 * plp
    return float((base + kappa_term + band_term + seam_term) * c.MANIFOLD_CLOSURE)


def compute_color_scalar(height_scalar: float) -> float:
    denom = c.TUNNEL_TENSION + c.KAPPA_TDA_MAX + c.KAPPA_TDA_MID + c.LATTICE_3_32
    return float(np.clip(float(height_scalar) / float(denom), 0.0, 1.0))
