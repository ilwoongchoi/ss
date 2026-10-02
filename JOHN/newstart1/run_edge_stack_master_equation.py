from __future__ import annotations

from pathlib import Path

import numpy as np

from geometry_package.absolute_constants import DELTA_T_OBS_DERIVED
from fusion_clean import (
    BW_BW_VOID_PROJECTION,
    EDGE_DOMAIN_STACK,
    DEFAULT_EDGE_WEIGHTS,
    edge_stack_master_step,
    master_equation_string,
)


OUT_DIR = Path("analysis_results")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MD = OUT_DIR / "edge_stack_master_equation.md"


def _fmt(vec: np.ndarray) -> str:
    return "[" + ", ".join(f"{float(x):.6f}" for x in vec) + "]"


def _norm(vec: np.ndarray) -> float:
    return float(np.linalg.norm(vec))


def build_report() -> str:
    state = np.array([0.25, 0.25, 0.25, 0.25], dtype=float)
    residual_gap = 0.01973885682129521
    bw_bw_void = DEFAULT_EDGE_WEIGHTS["BW_BW"] * BW_BW_VOID_PROJECTION
    fills = [
        ("pre_gate", 0.20, 0.0, None),
        ("day_capture", DELTA_T_OBS_DERIVED, 1.0, "14:00"),
        ("night_tunnel", 1.0 - DELTA_T_OBS_DERIVED, None, "02:20"),
    ]

    lines = []
    lines.append("# Edge Stack Master Equation")
    lines.append("")
    lines.append("## Equation")
    lines.append("")
    lines.append(f"`{master_equation_string()}`")
    lines.append("")
    lines.append("## Fixed Roles")
    lines.append("")
    lines.append(f"- `0.2828 gate = {DELTA_T_OBS_DERIVED:.15f}`")
    lines.append("- `slotting(t) = 1.4 - 0.076 t`")
    lines.append("- `138.88 = spark rotation operator`")
    lines.append("- `4D torsion = hidden twist term`")
    lines.append("- `cancel pair = lensing - PLP`")
    lines.append("- `slotting itself is the D3 envelope`")
    lines.append(f"- `BW_BW_void projection = {BW_BW_VOID_PROJECTION:.15f}`")
    lines.append("")
    lines.append("## 10 Edge Stack")
    lines.append("")
    for item in EDGE_DOMAIN_STACK:
        lines.append(
            f"- `{item.index}. {item.edge}`: {item.domain} "
            f"(weight={DEFAULT_EDGE_WEIGHTS[item.edge]:.6f})"
        )
    lines.append("")
    lines.append("## Residual Closure")
    lines.append("")
    lines.append(f"- `residual_gap = {residual_gap:.17f}`")
    lines.append(f"- `BW_BW_void = BW_BW * projection = {bw_bw_void:.17f}`")
    lines.append(f"- `closure_difference = {residual_gap - bw_bw_void:.17f}`")
    lines.append("")
    lines.append("## Sample Decomposition")
    lines.append("")
    lines.append(f"- `state_in = {_fmt(state)}`")
    lines.append("")

    for name, phase_fill, time_like, clock_hhmm in fills:
        step = edge_stack_master_step(state, phase_fill, time_like=time_like, clock_hhmm=clock_hhmm)
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"- `phase_fill = {phase_fill:.15f}`")
        if clock_hhmm is not None:
            lines.append(f"- `clock = {clock_hhmm}`")
            lines.append(f"- `face_mode = {step['face_state']['mode']}`")
            lines.append(f"- `capture_gate = {step['capture_gate']:.6f}`")
            lines.append(f"- `escape_gate = {step['escape_gate']:.6f}`")
        lines.append(f"- `time_like = {float(step['time_like']):.6f}`")
        lines.append(f"- `gate = {float(step['gate']):.6f}`")
        lines.append(f"- `slotting = {float(step['slotting']):.6f}`")
        lines.append(f"- `observer_only_norm = {_norm(step['observer_only']):.6f}`")
        lines.append(f"- `mandelbrot_core_norm = {_norm(step['mandelbrot_core']):.6f}`")
        lines.append(f"- `edge_total_norm = {_norm(step['edge_total']):.6f}`")
        lines.append(f"- `cancel_pair_norm = {_norm(step['cancel_pair']):.6f}`")
        lines.append(f"- `bw_bw_void_norm = {_norm(step['bw_bw_void']):.6f}`")
        lines.append(f"- `gated_branch_norm = {_norm(step['gated_branch']):.6f}`")
        lines.append(f"- `state_out = {_fmt(step['state_out'])}`")
        lines.append("")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    OUT_MD.write_text(build_report(), encoding="utf-8")
    print(str(OUT_MD))
