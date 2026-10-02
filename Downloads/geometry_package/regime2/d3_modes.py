"""Regime-2 D3 mode classifier from Regime-1 snapshot patterns."""

from __future__ import annotations

from typing import Dict, Literal

from geometry_package.regime1 import core_constants as c


D3Mode = Literal["ideal_D3_grounded", "captured_D3", "sealed_D3"]


def classify_d3_mode(core_snapshot: Dict[str, float]) -> D3Mode:
    k_eff = float(core_snapshot.get("kappa_eff", c.KAPPA_TDA_MID))
    w = float(core_snapshot.get("w_gate", 0.0))
    occ = float(core_snapshot.get("funnel_occupancy", 0.0))
    in_band = bool(core_snapshot.get("in_sh_band", 0.0) >= 0.5)

    if in_band and abs(k_eff - c.KAPPA_TDA_MID) <= 1e-9 and occ <= 1e-12:
        return "sealed_D3"
    if w > 0.0 and (occ / (w + 1e-12)) < c.LATTICE_3_32:
        return "captured_D3"
    return "ideal_D3_grounded"
