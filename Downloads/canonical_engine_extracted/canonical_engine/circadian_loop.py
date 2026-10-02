"""Circadian modulation of the canonical body energy loop.

For each hour we report:
  - phase (AB_spark / A_accumulate / O_accumulate / B_accumulate / AB_charge)
  - active node on the canonical loop
  - body position
  - next 3 waypoints in the loop
"""
from __future__ import annotations

import json
import pathlib
from typing import Dict, List, Tuple

from .canonical_body_loop import WAYPOINTS

GEN_DIR = pathlib.Path(__file__).parent / "generated"
BODY_FILE = GEN_DIR / "body_locations.json"
body_locs: Dict[str, Dict[str, str]] = json.loads(BODY_FILE.read_text(encoding="utf-8"))

LOOP_NODES = [w[0] for w in WAYPOINTS]


def _phase(hour: float) -> str:
    if 0 <= hour < 3:
        return "AB_spark"
    if 3 <= hour < 9:
        return "A_accumulate"
    if 9 <= hour < 15:
        return "O_accumulate"
    if 15 <= hour < 21:
        return "B_accumulate"
    return "AB_charge"


def _active_index(phase: str) -> int:
    """Map phase to the canonical-loop node that receives the primary spark."""
    return {
        "AB_spark":     LOOP_NODES.index("memory_entropy"),
        "A_accumulate": LOOP_NODES.index("laterite"),
        "O_accumulate": LOOP_NODES.index("memory_entropy"),
        "B_accumulate": LOOP_NODES.index("co2"),
        "AB_charge":    LOOP_NODES.index("memory_entropy"),
    }[phase]


if __name__ == "__main__":
    lines = []
    for hour in range(24):
        phase = _phase(hour)
        idx = _active_index(phase)
        node = LOOP_NODES[idx]
        raw = body_locs.get(node, {}).get("raw", "")
        region = WAYPOINTS[idx][1]
        next_nodes = [LOOP_NODES[(idx + i) % len(LOOP_NODES)] for i in range(1, 4)]
        lines.append(
            f"{hour:02d}:00  phase={phase:14s}  focus={node:25s}  region={region:14s}  next={next_nodes}"
        )
    text = "\n".join(lines)
    print(text)
    (GEN_DIR / "circadian_loop.txt").write_text(text, encoding="utf-8")
