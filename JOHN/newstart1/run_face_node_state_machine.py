from __future__ import annotations

from pathlib import Path

from geometry_package.face_node_state_machine import (
    TUNNEL_WINDOW,
    COMMON_NODES,
    DAY_BINARY_NODES,
    NIGHT_BINARY_NODES,
    day_node_labels,
    day_vector,
    face_state_at_time,
    night_node_labels,
    night_vector,
    ownership_summary,
    tunnel_paths,
    transition_rules,
)


OUT = Path("analysis_results/face_node_state_machine.md")
OUT.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    lines: list[str] = []
    lines.append("# Face Node State Machine")
    lines.append("")
    lines.append("## Fixed Structure")
    lines.append("")
    lines.append(f"- common_nodes: `{len(COMMON_NODES)}`")
    lines.append(f"- binary_slots: `{len(DAY_BINARY_NODES)}`")
    lines.append(f"- tunnel_window: `{TUNNEL_WINDOW[0]} -> {TUNNEL_WINDOW[1]}`")
    lines.append("")
    lines.append("## Common Backbone")
    lines.append("")
    for node in COMMON_NODES:
        lines.append(f"- `{node.index}. {node.name}` ownership=`{node.ownership}`, gate=`{node.gate_role}`")
    lines.append("")
    lines.append("## Day State")
    lines.append("")
    for i, label in enumerate(day_node_labels(), start=1):
        lines.append(f"- `{i}: {label}` = `1`")
    lines.append(f"- day_state_vector: `{day_vector()}`")
    lines.append("")
    lines.append("## Night State")
    lines.append("")
    for i, label in enumerate(night_node_labels(), start=1):
        lines.append(f"- `{i}: {label}` = `1`")
    lines.append(f"- night_state_vector: `{night_vector()}`")
    lines.append("")
    lines.append("## Tunnel Paths")
    lines.append("")
    for name, path in tunnel_paths().items():
        lines.append(f"- `{name}`: `{path}`")
    lines.append("")
    lines.append("## Face-State Controllers")
    lines.append("")
    for clock in ("14:00", "02:20"):
        state = face_state_at_time(clock)
        lines.append(
            f"- `{clock}`: mode=`{state['mode']}`, trigger=`{state['trigger']}`, "
            f"tunnel_open=`{state['tunnel_open_controller']}`, rail=`{state['rail']}`, exit=`{state['exit_controller']}`"
        )
    lines.append("")
    lines.append("## Ownership Derivations")
    lines.append("")
    for key, values in ownership_summary().items():
        lines.append(f"- `{key}`: `{values}`")
    lines.append("")
    lines.append("## Transition Rules")
    lines.append("")
    for rule in transition_rules():
        lines.append(f"- {rule}")
    lines.append("")
    lines.append("## Direct Consequences")
    lines.append("")
    lines.append("- `capture_mode(day)` is supported by `R_temporalis_front_AChR_and_R_occipitalis_GABAA`.")
    lines.append("- `escape_mode(night)` is supported by `L_temporalis_back_5HT1A`.")
    lines.append("- `impedance_day` and `impedance_night` are not symmetric; this creates deterministic ownership asymmetry.")
    lines.append("- `slotting` should be attached to tunnel/capture/escape scheduling, not treated as a free scalar.")
    lines.append("- The 10-node layout is enough to define a deterministic two-state machine with a tunnel window.")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
