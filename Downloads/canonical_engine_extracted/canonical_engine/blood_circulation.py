"""Blood-type specific energy circulation patterns on the canonical body loop.

Derived from universe-prose toroidal cycle:
    AB = spark/discharge    (complexity 4)
    A  = structured accumulate (complexity 2)
    O  = dark energy accumulate  (complexity 1)
    B  = extreme release    (complexity 3)
"""
from __future__ import annotations

import json
import pathlib
from typing import Dict, List, Tuple

from .canonical_body_loop import WAYPOINTS

GEN_DIR = pathlib.Path(__file__).parent / "generated"
BODY_FILE = GEN_DIR / "body_locations.json"
body_locs: Dict[str, Dict[str, str]] = json.loads(BODY_FILE.read_text(encoding="utf-8"))

LOOP = [w[0] for w in WAYPOINTS]


def _region(node: str) -> str:
    return body_locs.get(node, {}).get("raw", node)


def _subloop(start_idx: int, length: int, skip: int = 1) -> List[str]:
    out = []
    for i in range(length):
        out.append(LOOP[(start_idx + i * skip) % len(LOOP)])
    return out


def pattern(blood: str) -> Dict:
    blood = blood.upper()
    idx = LOOP.index("memory_entropy")
    if blood == "O":
        # complexity 1: single sequential loop, full cycle
        seq = _subloop(idx, len(LOOP), 1)
        return {
            "blood": blood,
            "complexity": 1,
            "mode": "single sequential loop",
            "paths": [{"name": "O-main", "nodes": seq}],
        }
    if blood == "A":
        # complexity 2: two antiphase half-cycles
        seq1 = _subloop(idx, len(LOOP) // 2, 1)
        seq2 = _subloop(idx + len(LOOP) // 2, len(LOOP) // 2, 1)
        return {
            "blood": blood,
            "complexity": 2,
            "mode": "two antiphase sequential streams",
            "paths": [
                {"name": "A-forward", "nodes": seq1},
                {"name": "A-return", "nodes": seq2},
            ],
        }
    if blood == "B":
        # complexity 3: triple spiral, every 3rd node
        paths = []
        for offset in range(3):
            seq = _subloop(idx + offset, len(LOOP) // 2 + 1, 3)
            paths.append({"name": f"B-spiral-{offset}", "nodes": seq})
        return {
            "blood": blood,
            "complexity": 3,
            "mode": "triple spiral / delayed branches",
            "paths": paths,
        }
    # AB
    # complexity 4: simultaneous 4-quadrant discharge
    paths = []
    for offset in range(4):
        seq = _subloop(idx + offset, len(LOOP) // 4 + 1, 4)
        paths.append({"name": f"AB-quadrant-{offset}", "nodes": seq})
    return {
        "blood": blood,
        "complexity": 4,
        "mode": "4-quadrant simultaneous spark discharge",
        "paths": paths,
    }


if __name__ == "__main__":
    lines = []
    for blood in ("O", "A", "B", "AB"):
        p = pattern(blood)
        lines.append(f"\nBLOOD {blood}  complexity={p['complexity']}  mode={p['mode']}")
        lines.append("=" * 60)
        for path in p["paths"]:
            lines.append(f"  {path['name']}:")
            for node in path["nodes"]:
                lines.append(f"    -> {node:35s} | {_region(node)[:55]}")
    text = "\n".join(lines)
    print(text)
    (GEN_DIR / "blood_circulation.txt").write_text(text, encoding="utf-8")
