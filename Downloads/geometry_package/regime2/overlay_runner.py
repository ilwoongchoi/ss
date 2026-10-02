"""Regime-2 runtime: reads Regime-1 API and produces overlay state."""

from __future__ import annotations

from typing import Dict

from geometry_package.regime1.core_ops import core_snapshot, plp_spine_gate_xy
from geometry_package.regime1.shader2d_core import xy_to_rq0

from .overlay_mapping import map_overlay_state


def run_overlay(
    *,
    t_macro: float,
    x: float | None = None,
    y: float | None = None,
    r: float | None = None,
    q0: float | None = None,
    epoch_state: Dict[str, float] | None = None,
) -> Dict[str, object]:
    if r is None or q0 is None:
        if x is None or y is None:
            raise ValueError("Provide either (r, q0) or (x, y).")
        r, q0 = xy_to_rq0(x, y)

    snapshot = core_snapshot(r=float(r), q0=float(q0), t_macro=float(t_macro), resolution=128)
    if x is not None and y is not None:
        snapshot["plp_spine"] = float(plp_spine_gate_xy(float(x), float(y)))
    else:
        snapshot["plp_spine"] = 0.0
    return map_overlay_state(snapshot, epoch_state=epoch_state)
