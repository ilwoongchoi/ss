"""Body Energy Flow — unified temporal→spatial body circulation engine.

Merges 6 scripts into one dynamic stem:
  1. canonical_body_loop  — 16 anatomical waypoints, path verification
  2. master_body_loop     — BFS from observer_leftd2
  3. circadian_loop       — 24h phase modulation
  4. time_body_path       — phase seed → BFS body path
  5. blood_circulation    — blood-type patterns on the loop
  6. slot_body_timeline   — 128-slot × body × 8D vectors

All 6 trace the same toroidal energy through the body at different
time scales and granularities. The stem flows:
  time → phase → seed node → BFS propagation → body path → blood variation → 128-slot timeline

Outputs:
  generated/body_energy_flow.txt   (consolidated report)
  generated/body_energy_flow.json  (structured data)
"""
from __future__ import annotations

import csv
import json
import pathlib
from collections import deque
from typing import Dict, List, Optional, Tuple

from .circuit_loader import NODES

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)

BODY_FILE = GEN_DIR / "body_locations.json"
BODY_NORM_FILE = GEN_DIR / "body_locations_normalized.json"
DOMAIN_FILE = GEN_DIR / "domain_map.json"
SLOT_FILE = GEN_DIR / "slot_layer_vectors.json"

body_locs: Dict[str, Dict[str, str]] = json.loads(BODY_FILE.read_text(encoding="utf-8"))
body_locs_norm: Dict[str, Dict[str, str]] = json.loads(BODY_NORM_FILE.read_text(encoding="utf-8"))
domains: Dict[str, Dict[str, str]] = json.loads(DOMAIN_FILE.read_text(encoding="utf-8"))

# ===========================================================================
# 1. CANONICAL BODY LOOP — 16 anatomical waypoints
# ===========================================================================

WAYPOINTS: List[Tuple[str, str, str]] = [
    ("observer_leftd2",            "frontalis",        "neuro/math"),
    ("observer_left_endorphin_electron_antineutrino", "philtrum/face", "neuro/biochem"),
    ("pi_electron_cloud",          "throat",           "biochem/particle"),
    ("heme",                       "chest",            "biochem"),
    ("left_genital_d2",            "pelvis",           "neuro"),
    ("gluon_orogen",               "left glute/pelvis", "geology/mantle"),
    ("laterite",                   "left calf",        "geology"),
    ("oxidised_manganese",         "left 4th toe",     "geology"),
    ("right_sole_dopamine",        "right sole",       "biology/neuro"),
    ("copper_iron_complex",        "right foot",       "geology/biochem"),
    ("collagen",                   "right Achilles",   "biology"),
    ("subduction_zone",            "left thigh",       "geology"),
    ("water_vapour",               "thoracic spine",   "atmosphere"),
    ("aurora",                     "scalp",            "astronomy"),
    ("co2",                        "occiput",          "atmosphere/time"),
    ("memory_entropy",             "right brain",      "math/neuro"),
]

LOOP_NODES = [w[0] for w in WAYPOINTS]


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


def _reachable(seed: str, max_depth: int = 25) -> List[str]:
    """BFS from seed, return only anatomical nodes in visit order."""
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


# ===========================================================================
# 2. CIRCADIAN PHASES
# ===========================================================================

PHASE_SEEDS: Dict[str, Tuple[str, ...]] = {
    "AB_spark":     ("co2", "memory_entropy"),
    "A_accumulate": ("laterite",),
    "O_accumulate": ("memory_entropy", "peonidine"),
    "B_accumulate": ("hind_insula", "co2"),
    "AB_charge":    ("co2", "memory_entropy"),
}


def phase_from_hour(hour: float) -> str:
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
    return {
        "AB_spark":     LOOP_NODES.index("memory_entropy"),
        "A_accumulate": LOOP_NODES.index("laterite"),
        "O_accumulate": LOOP_NODES.index("memory_entropy"),
        "B_accumulate": LOOP_NODES.index("co2"),
        "AB_charge":    LOOP_NODES.index("memory_entropy"),
    }[phase]


# ===========================================================================
# 3. BLOOD TYPE PATTERNS
# ===========================================================================

def _subloop(start_idx: int, length: int, skip: int = 1) -> List[str]:
    return [LOOP[(start_idx + i * skip) % len(LOOP)] for i in range(length)]

LOOP = LOOP_NODES


def blood_pattern(blood: str) -> Dict:
    blood = blood.upper()
    idx = LOOP.index("memory_entropy")
    if blood == "O":
        seq = _subloop(idx, len(LOOP), 1)
        return {"blood": blood, "complexity": 1, "mode": "single sequential loop",
                "paths": [{"name": "O-main", "nodes": seq}]}
    if blood == "A":
        seq1 = _subloop(idx, len(LOOP) // 2, 1)
        seq2 = _subloop(idx + len(LOOP) // 2, len(LOOP) // 2, 1)
        return {"blood": blood, "complexity": 2, "mode": "two antiphase streams",
                "paths": [{"name": "A-forward", "nodes": seq1},
                          {"name": "A-return", "nodes": seq2}]}
    if blood == "B":
        paths = [{"name": f"B-spiral-{o}", "nodes": _subloop(idx + o, len(LOOP) // 2 + 1, 3)}
                 for o in range(3)]
        return {"blood": blood, "complexity": 3, "mode": "triple spiral", "paths": paths}
    # AB
    paths = [{"name": f"AB-quadrant-{o}", "nodes": _subloop(idx + o, len(LOOP) // 4 + 1, 4)}
             for o in range(4)]
    return {"blood": blood, "complexity": 4, "mode": "4-quadrant spark discharge", "paths": paths}


# ===========================================================================
# 4. TIME → BODY PATH
# ===========================================================================

def trace_body_path(hour: float, max_depth: int = 20) -> Dict:
    phase = phase_from_hour(hour)
    seeds = PHASE_SEEDS[phase]
    ordered: List[str] = []
    seen: set = set()
    for seed in seeds:
        for node in _reachable(seed, max_depth):
            if node not in seen:
                seen.add(node)
                ordered.append(node)
    body_seq = []
    for node in ordered:
        loc = body_locs_norm.get(node, {})
        body_seq.append({"node": node, "region": loc.get("region", ""),
                         "side": loc.get("side", ""), "raw": loc.get("raw", "")})
    return {"hour": hour, "phase": phase, "nodes": ordered, "body_path": body_seq}


# ===========================================================================
# 5. SLOT BODY TIMELINE (128-slot × body × 8D)
# ===========================================================================

def _entity_to_node(entity: str) -> str:
    return entity.split(".")[0].replace("_out_", "").replace("_ctrl_", "")


def _loop_position(node: str) -> int | None:
    for i, wn in enumerate(LOOP_NODES):
        if wn == node or wn in node or node in wn:
            return i
    return None


def build_slot_timeline() -> List[Dict]:
    if not SLOT_FILE.exists():
        return []
    slots = json.loads(SLOT_FILE.read_text(encoding="utf-8"))
    result = []
    for s in slots:
        entity = s["circuit_entity"]
        node = _entity_to_node(entity)
        loc = body_locs.get(node, {}).get("raw", "")
        if not loc:
            for bn, bv in body_locs.items():
                if bn in node or node in bn:
                    loc = bv["raw"]
                    node = bn
                    break
        loop_idx = _loop_position(node)
        v = s["layer1_release"]["vec8d"]
        result.append({
            "slot": s["slot"], "phase": s["energy_phase"], "type": s["main_type"],
            "entity": entity, "body_loc": loc, "loop_idx": loop_idx,
            "release_genre": s["layer1_release"]["genre"],
            "release_vec": f"P={v['P']:.2f} Z={v['Z']:.2f} Q={v['Q']:.2f} W={v['W']:.2f} H={v['H']:.2f}",
            "stress_genre": s["layer2_stress"]["genre"],
            "extreme_genre": s["layer3_extreme"]["genre"],
        })
    return result


# ===========================================================================
# 6. CONSOLIDATED REPORT
# ===========================================================================

def generate_report() -> Tuple[str, Dict]:
    lines: List[str] = []
    data: Dict = {}

    # --- Section 1: Canonical loop waypoints ---
    lines.append("=" * 80)
    lines.append("  BODY ENERGY FLOW — Unified Temporal→Spatial Circulation")
    lines.append("  Stem: time → phase → seed → BFS → body path → blood → 128-slot")
    lines.append("=" * 80)
    lines.append("")

    lines.append("  [1] CANONICAL BODY LOOP — 16 Waypoints")
    lines.append("-" * 80)
    loop_data = []
    for i, (node, region, domain) in enumerate(WAYPOINTS, 1):
        raw = body_locs.get(node, {}).get("raw", "")
        dom = domains.get(node, {}).get("domain", "")
        lines.append(f"  {i:02d}. {node:35s} | {region:18s} | domain={dom:16s} | {raw}")
        loop_data.append({"index": i, "node": node, "region": region, "domain": dom, "raw": raw})
    lines.append("")

    # Path verification
    lines.append("  Segment verification:")
    seg_data = []
    for i in range(len(WAYPOINTS) - 1):
        a, _, _ = WAYPOINTS[i]
        b, _, _ = WAYPOINTS[i + 1]
        ok = _has_path(a, b)
        status = "OK" if ok else "MANUAL/GAP"
        lines.append(f"    {a} -> {b}: {status}")
        seg_data.append({"from": a, "to": b, "ok": ok})
    close_ok = _has_path(WAYPOINTS[-1][0], "observer_leftd2")
    lines.append(f"    Close loop: {WAYPOINTS[-1][0]} -> observer_leftd2: {'OK' if close_ok else 'GAP'}")
    lines.append("")
    data["canonical_loop"] = {"waypoints": loop_data, "segments": seg_data, "closed": close_ok}

    # --- Section 2: Master BFS loop ---
    lines.append("  [2] MASTER BFS LOOP — from observer_leftd2")
    lines.append("-" * 80)
    master_path = _reachable("observer_leftd2", max_depth=25)
    master_data = []
    for i, node in enumerate(master_path, 1):
        raw = body_locs.get(node, {}).get("raw", "")
        lines.append(f"  {i:02d}. {node:30s} | {raw}")
        master_data.append({"index": i, "node": node, "raw": raw})
    lines.append("")
    data["master_loop"] = master_data

    # --- Section 3: Circadian 24h ---
    lines.append("  [3] CIRCADIAN 24h — phase × active node × region")
    lines.append("-" * 80)
    circadian_data = []
    for hour in range(24):
        phase = phase_from_hour(hour)
        idx = _active_index(phase)
        node = LOOP_NODES[idx]
        raw = body_locs.get(node, {}).get("raw", "")
        region = WAYPOINTS[idx][1]
        next_nodes = [LOOP_NODES[(idx + i) % len(LOOP_NODES)] for i in range(1, 4)]
        lines.append(f"  {hour:02d}:00  phase={phase:14s}  focus={node:25s}  region={region:14s}  next={next_nodes}")
        circadian_data.append({"hour": hour, "phase": phase, "focus": node, "region": region})
    lines.append("")
    data["circadian"] = circadian_data

    # --- Section 4: Time → body path ---
    lines.append("  [4] TIME → BODY PATH — 5 representative hours")
    lines.append("-" * 80)
    path_data = {}
    for h in (1, 6, 12, 18, 23):
        r = trace_body_path(h)
        lines.append(f"  {h:02d}:00 phase={r['phase']}")
        for step in r["body_path"][:15]:
            lines.append(f"    -> {step['node']:25s} | {step['side']:6s} {step['region']:10s} | {step['raw']}")
        path_data[str(h)] = r
    lines.append("")
    data["time_paths"] = path_data

    # --- Section 5: Blood type patterns ---
    lines.append("  [5] BLOOD TYPE CIRCULATION PATTERNS")
    lines.append("-" * 80)
    blood_data = {}
    for blood in ("O", "A", "B", "AB"):
        p = blood_pattern(blood)
        lines.append(f"\n  BLOOD {blood}  complexity={p['complexity']}  mode={p['mode']}")
        for path in p["paths"]:
            lines.append(f"    {path['name']}:")
            for node in path["nodes"]:
                raw = body_locs.get(node, {}).get("raw", node)
                lines.append(f"      -> {node:35s} | {raw[:55]}")
        blood_data[blood] = p
    lines.append("")
    data["blood_patterns"] = blood_data

    # --- Section 6: 128-slot timeline ---
    lines.append("  [6] 128-SLOT BODY TIMELINE")
    lines.append("-" * 80)
    slot_data = build_slot_timeline()
    if slot_data:
        lines.append(f"  {'Slot':>4} {'Phase':<16} {'Type':<12} {'Entity':<30} {'BodyLoc':<40} {'Loop#':>5}")
        lines.append("  " + "-" * 78)
        for s in slot_data:
            lines.append(
                f"  {s['slot']:>4} {s['phase']:<16} {s['type']:<12} "
                f"{s['entity']:<30} {s['body_loc'][:40]:<40} {str(s['loop_idx']):>5}"
            )
            lines.append(f"        release: {s['release_genre']:<35} {s['release_vec']}")
            lines.append(f"        stress:  {s['stress_genre']:<35}")
            lines.append(f"        extreme: {s['extreme_genre']:<35}")
    else:
        lines.append("  (slot_layer_vectors.json not found — run slot_layer_vectors first)")
    lines.append("")
    data["slot_timeline"] = slot_data

    text = "\n".join(lines)
    return text, data


# ===========================================================================
# MAIN
# ===========================================================================

if __name__ == "__main__":
    text, data = generate_report()
    (GEN_DIR / "body_energy_flow.txt").write_text(text, encoding="utf-8")
    (GEN_DIR / "body_energy_flow.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(text[:4000])
    print(f"\n... full report -> {GEN_DIR / 'body_energy_flow.txt'}")
    print(f"... structured  -> {GEN_DIR / 'body_energy_flow.json'}")
