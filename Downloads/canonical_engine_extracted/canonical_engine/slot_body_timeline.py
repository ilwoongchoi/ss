"""Combine 128-slot timeline with body locations and 8D vectors.

For each slot:
  - circuit_entity → body location
  - canonical body loop position
  - 4-layer 8D vectors + genres
  - energy phase
"""
from __future__ import annotations

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
GEN_DIR = pathlib.Path(__file__).parent / "generated"

# load slot vectors
slots = json.loads((GEN_DIR / "slot_layer_vectors.json").read_text(encoding="utf-8"))

# load body locations
body_locs = json.loads((GEN_DIR / "body_locations.json").read_text(encoding="utf-8"))

# canonical loop nodes
from .canonical_body_loop import WAYPOINTS
LOOP_NODES = [w[0] for w in WAYPOINTS]


def _entity_to_node(entity: str) -> str:
    """heme.out1 -> heme, water_vapour.out1 -> water_vapour"""
    return entity.split(".")[0].replace("_out_", "").replace("_ctrl_", "")


def _loop_position(node: str) -> int | None:
    """Return index in canonical loop if node matches, else None"""
    for i, wn in enumerate(LOOP_NODES):
        if wn == node or wn in node or node in wn:
            return i
    return None


lines = []
lines.append("128-Slot Body Energy Timeline")
lines.append("=" * 80)
lines.append(f"{'Slot':>4} {'Phase':<16} {'Type':<12} {'Entity':<30} {'BodyLoc':<40} {'Loop#':>5}")
lines.append("-" * 80)

for s in slots:
    entity = s["circuit_entity"]
    node = _entity_to_node(entity)
    loc = body_locs.get(node, {}).get("raw", "")
    if not loc:
        # try partial match
        for bn, bv in body_locs.items():
            if bn in node or node in bn:
                loc = bv["raw"]
                node = bn
                break
    loop_idx = _loop_position(node)

    # 8D summary: release layer
    v = s["layer1_release"]["vec8d"]
    vec_str = f"P={v['P']:.2f} Z={v['Z']:.2f} Q={v['Q']:.2f} W={v['W']:.2f} H={v['H']:.2f}"

    lines.append(
        f"{s['slot']:>4} {s['energy_phase']:<16} {s['main_type']:<12} "
        f"{entity:<30} {loc[:40]:<40} {str(loop_idx):>5}"
    )
    lines.append(
        f"      L1 release:  {s['layer1_release']['genre']:<35} {vec_str}"
    )
    v2 = s["layer2_stress"]["vec8d"]
    lines.append(
        f"      L2 stress:   {s['layer2_stress']['genre']:<35} "
        f"P={v2['P']:.2f} Z={v2['Z']:.2f} Q={v2['Q']:.2f} W={v2['W']:.2f} H={v2['H']:.2f}"
    )
    v3 = s["layer3_extreme"]["vec8d"]
    lines.append(
        f"      L3 extreme:  {s['layer3_extreme']['genre']:<35} "
        f"P={v3['P']:.2f} Z={v3['Z']:.2f} Q={v3['Q']:.2f} W={v3['W']:.2f} H={v3['H']:.2f}"
    )
    # 512 layers A/B/C/D
    ref = s.get("layers_512_ref", {})
    layer_labels = {
        "A": "RH+ homo (main/release)",
        "B": "RH- homo (MBTI opp/stress)",
        "C": "RH+ hetero (blood+1/stress)",
        "D": "RH- hetero (opp+blood+1/extreme)",
    }
    for lk in ("A", "B", "C", "D"):
        lr = ref.get(lk)
        if lr:
            t = lr["tension_5d"]
            lines.append(
                f"      512-{lk} {layer_labels[lk]:<30} "
                f"{lr['genre']:<30} "
                f"r={t['Rhythm_Density']:.2f} h={t['Harmonic_Tension']:.2f} "
                f"d={t['Dynamic_Curve']:.2f} p={t['Predictability_Inv']:.2f} s={t['Spectral_Brightness']:.2f}"
            )
    lines.append("")

text = "\n".join(lines)
print(text[:3000])
(GEN_DIR / "slot_body_timeline.txt").write_text(text, encoding="utf-8")
print(f"\n... full output -> {GEN_DIR / 'slot_body_timeline.txt'}")
