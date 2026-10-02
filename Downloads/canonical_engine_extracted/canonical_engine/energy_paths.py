"""High-level path enumerator.

API:
    list_paths(phase: str, profile_key: str, max_depth: int = 6) -> List[Dict]

• phase              – "release" | "stress" | "extreme"
• profile_key        – matches music_map.json key, used here only for placeholder Vec8D lookup
• returns path dicts: {"nodes": [...], "vec8d": (r,h,d,p,s,gamma,g,nu)}

NOTE: placeholder implementation – no earth/sky mapping yet, no latch state save.
"""
from __future__ import annotations

from collections import deque
from typing import Dict, List, Tuple

from .circuit_loader import NODES

Vec8 = Tuple[float, float, float, float, float, float, float, float]

# ---------------------------------------------------------------------------
# minimal Vec8D placeholder (loads zeros) – to be replaced by CSV reader
# ---------------------------------------------------------------------------
_zero: Vec8 = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

# ---------------------------------------------------------------------------
# path enumeration
# ---------------------------------------------------------------------------

def list_paths(phase: str, profile_key: str, max_depth: int = 6) -> List[Dict]:
    results: List[Dict] = []
    visited = set()
    # simplistic source set: all nodes with no incoming links
    sources = [n for n in NODES.values() if not any(p.kind == "in" for p in n.ports)]
    for src in sources:
        stack = deque([(src.name, [src.name])])
        while stack:
            node_name, path = stack.pop()
            if len(path) > max_depth:
                continue
            node = NODES[node_name]
            outs = [p.link.split(".")[0] for p in node.ports if p.kind == "out"]
            if not outs:
                # sink reached
                results.append({
                    "nodes": path,
                    "vec8d": _zero,
                })
                continue
            for nxt in outs:
                if nxt not in NODES:
                    continue
                edge = (node_name, nxt)
                if edge in visited:
                    continue
                visited.add(edge)
                stack.append((nxt, path + [nxt]))
    return results

if __name__ == "__main__":
    demo = list_paths("release", "ENFP_F_O", max_depth=4)
    print(f"demo paths: {len(demo)} (depth<=4)")
