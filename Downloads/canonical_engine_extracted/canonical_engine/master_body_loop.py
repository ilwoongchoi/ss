"""Trace the master body energy loop starting from observer_leftd2.

The canonical loop (read from the wiring + body locations):
  face/center -> down central axis -> back/pelvis -> legs/feet -> up spine -> scalp/brain
"""
from __future__ import annotations

import json
import pathlib
from collections import deque
from typing import Dict, List

from .circuit_loader import NODES

GEN_DIR = pathlib.Path(__file__).parent / "generated"
BODY_LOC_FILE = GEN_DIR / "body_locations.json"
body_locs: Dict[str, Dict[str, str]] = json.loads(
    BODY_LOC_FILE.read_text(encoding="utf-8")
)


def _reachable(seed: str, max_depth: int = 25) -> List[str]:
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
        for port in NODES[cur].ports:
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


if __name__ == "__main__":
    path = _reachable("observer_leftd2", max_depth=25)
    lines = []
    for i, node in enumerate(path, 1):
        raw = body_locs[node]["raw"]
        lines.append(f"{i:02d}. {node:30s} | {raw}")
    text = "\n".join(lines)
    print(text)
    (GEN_DIR / "master_body_loop.txt").write_text(text, encoding="utf-8")
