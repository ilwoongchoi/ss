"""Time → body energy path tracer.

Uses the toroidal cycle defined in universe-prose.md:
    AB spark      : 00-03 h
    A accumulate  : 03-09 h
    O accumulate  : 09-15 h
    B accumulate  : 15-21 h
    AB charge     : 21-24 h

For each phase a seed node set is activated; forward propagation through the
wiring graph yields the ordered list of body locations the energy visits.
"""
from __future__ import annotations

import json
import pathlib
from collections import deque
from typing import Dict, List, Tuple

from .circuit_loader import NODES

ROOT = pathlib.Path(__file__).parent.parent
GEN_DIR = pathlib.Path(__file__).parent / "generated"
BODY_LOC_FILE = GEN_DIR / "body_locations_normalized.json"

body_locs: Dict[str, Dict[str, str]] = json.loads(BODY_LOC_FILE.read_text(encoding="utf-8"))

PHASE_SEEDS: Dict[str, Tuple[str, ...]] = {
    "AB_spark":     ("co2", "memory_entropy"),
    "A_accumulate": ("laterite",),
    "O_accumulate": ("memory_entropy", "peonidine"),
    "B_accumulate": ("hind_insula", "co2"),
    "AB_charge":    ("co2", "memory_entropy"),
}


def _phase_from_hour(hour: float) -> str:
    if 0 <= hour < 3:
        return "AB_spark"
    if 3 <= hour < 9:
        return "A_accumulate"
    if 9 <= hour < 15:
        return "O_accumulate"
    if 15 <= hour < 21:
        return "B_accumulate"
    return "AB_charge"


def _reachable_anatomical(seed: str, max_depth: int = 12) -> List[str]:
    """BFS from seed, return only anatomical nodes (with LOCATION) in visit order."""
    if seed not in NODES:
        return []
    seen = {seed}
    order: List[str] = []
    if seed in body_locs:
        order.append(seed)
    q = deque([(seed, 0)])
    while q:
        cur, depth = q.popleft()
        if depth >= max_depth:
            continue
        node = NODES[cur]
        for port in node.ports:
            if port.kind != "out":
                continue
            nxt = port.link.split(".")[0]
            if nxt not in NODES or nxt in seen:
                continue
            seen.add(nxt)
            if nxt in body_locs:
                order.append(nxt)
            q.append((nxt, depth + 1))
    return order


def trace(hour: float, max_depth: int = 20) -> Dict[str, object]:
    phase = _phase_from_hour(hour)
    seeds = PHASE_SEEDS[phase]
    ordered: List[str] = []
    seen: set = set()
    for seed in seeds:
        for node in _reachable_anatomical(seed, max_depth):
            if node not in seen:
                seen.add(node)
                ordered.append(node)

    body_seq: List[Dict[str, str]] = []
    for node in ordered:
        loc = body_locs.get(node, {})
        body_seq.append({
            "node": node,
            "region": loc.get("region", ""),
            "side": loc.get("side", ""),
            "raw": loc.get("raw", ""),
        })

    return {
        "hour": hour,
        "phase": phase,
        "nodes": ordered,
        "body_path": body_seq,
    }


if __name__ == "__main__":
    out_lines = []
    for h in (1, 6, 12, 18, 23):
        r = trace(h)
        out_lines.append(f"{h:02d}:00 phase={r['phase']}")
        for step in r["body_path"][:20]:
            out_lines.append(f"  -> {step['node']:25s} | {step['side']:6s} {step['region']:10s} | {step['raw']}")
    text = "\n".join(out_lines)
    print(text)
    (GEN_DIR / "time_body_path_demo.txt").write_text(text, encoding="utf-8")
