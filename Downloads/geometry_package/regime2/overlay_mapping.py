"""Regime-2 concept mapping table over Regime-1 fields."""

from __future__ import annotations

from typing import Dict

from .d3_modes import classify_d3_mode


def map_overlay_state(core_snapshot: Dict[str, float], epoch_state: Dict[str, float] | None = None) -> Dict[str, object]:
    epoch = epoch_state or {}
    d3_mode = classify_d3_mode(core_snapshot)

    return {
        "d3_mode": d3_mode,
        "mobius_loop_phase": {
            "t_micro": float(core_snapshot.get("t_micro", 0.0)),
            "is_reverse": bool(core_snapshot.get("is_reverse", 0.0) >= 0.5),
        },
        "jawless_to_jawed_marker": {
            "epoch_id": epoch.get("epoch_id", "unspecified"),
            "epoch_weight": float(epoch.get("epoch_weight", 0.0)),
        },
        "neuro_social_mapping": {
            "left_right_volume_balance": float(core_snapshot.get("w_gate", 0.0)),
            "stability_gate": float(core_snapshot.get("kappa_eff", 0.0)),
            "funnel_occupancy": float(core_snapshot.get("funnel_occupancy", 0.0)),
            "plp_seam_influence": float(core_snapshot.get("plp_spine", 0.0)),
        },
    }
