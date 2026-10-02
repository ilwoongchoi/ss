"""Declare and verify the canonical closed body energy loop.

The loop shape is fixed by anatomy/domain mapping:
  center -> face -> throat -> chest/abdomen -> pelvis -> left leg -> feet -> right leg -> spine -> brain -> center

For each consecutive waypoint pair we check whether a directed path exists in
the circuit graph; if not, the link is marked MANUAL.
"""
from __future__ import annotations

import json
import pathlib
from collections import deque
from typing import Dict, List, Tuple

from .circuit_loader import NODES

GEN_DIR = pathlib.Path(__file__).parent / "generated"
DOMAIN_FILE = GEN_DIR / "domain_map.json"
BODY_FILE = GEN_DIR / "body_locations.json"

domains: Dict[str, Dict[str, str]] = json.loads(DOMAIN_FILE.read_text(encoding="utf-8"))
body_locs: Dict[str, Dict[str, str]] = json.loads(BODY_FILE.read_text(encoding="utf-8"))

# Canonical anatomical/disciplinary waypoints
WAYPOINTS: List[Tuple[str, str, str]] = [
    ("observer_leftd2",            "frontalis",        "neuro/math"),
    ("observer_left_endorphin_electron_antineutrino", "philtrum/face", "neuro/biochem"),
    ("pi_electron_cloud",          "throat",           "biochem/particle"),
    ("heme",                       "chest",            "biochem"),
    ("left_genital_d2",            "pelvis",           "neuro"),
    ("gluon_orogen",               "left glute/pelvis", "geology/mantle"),
    ("laterite",                   "left calf",        "geology"),
    ("oxidised_manganese",       "left 4th toe",     "geology"),
    ("right_sole_dopamine",        "right sole",       "biology/neuro"),
    ("copper_iron_complex",        "right foot",       "geology/biochem"),
    ("collagen",                   "right Achilles",   "biology"),
    ("subduction_zone",            "left thigh",       "geology"),
    ("water_vapour",               "thoracic spine",   "atmosphere"),
    ("aurora",                     "scalp",            "astronomy"),
    ("co2",                        "occiput",          "atmosphere/time"),
    ("memory_entropy",             "right brain",      "math/neuro"),
]


def _has_path(src: str, dst: str, max_depth: int = 12) -> bool:
    if src not in NODES or dst not in NODES:
        return False
    seen = {src}
    q = deque([(src, 0)])
    while q:
        cur, d = q.popleft()
        if cur == dst:
            return True
        if d >= max_depth:
            continue
        for port in NODES[cur].ports:
            if port.kind != "out":
                continue
            nxt = port.link.split(".")[0]
            if nxt in NODES and nxt not in seen:
                seen.add(nxt)
                q.append((nxt, d + 1))
    return False


if __name__ == "__main__":
    lines = []
    lines.append("Canonical closed body loop")
    lines.append("=" * 60)
    for i, (node, region, domain) in enumerate(WAYPOINTS, 1):
        raw = body_locs.get(node, {}).get("raw", "")
        dom = domains.get(node, {}).get("domain", "")
        lines.append(f"{i:02d}. {node:35s} | {region:18s} | domain={dom:16s}")
    # close loop back to observer_leftd2
    last_node, last_region, last_domain = WAYPOINTS[-1]
    ok = _has_path(last_node, "observer_leftd2")
    lines.append("-" * 60)
    lines.append(f"Close loop: {last_node} -> observer_leftd2  path_exists={ok}")
    lines.append("")
    lines.append("Segment verification:")
    for i in range(len(WAYPOINTS) - 1):
        a, _, _ = WAYPOINTS[i]
        b, _, _ = WAYPOINTS[i + 1]
        ok = _has_path(a, b)
        status = "OK" if ok else "MANUAL/GAP"
        lines.append(f"  {a} -> {b}: {status}")

    text = "\n".join(lines)
    print(text)
    (GEN_DIR / "canonical_body_loop.txt").write_text(text, encoding="utf-8")
