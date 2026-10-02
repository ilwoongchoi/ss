"""Unified slot query: given slot number, return complete energy state.

Combines:
  - 128_UNIFIED_MASTER_8D_fixed.csv (slot → type, entity, 8D vectors, genres)
  - 512_WITH_MUSIC_FIXED.csv (element → 4 layers A/B/C/D, 5D tension, genre)
  - circuit.json (circuit node topology)
  - body_locations.json (entity → body location)
  - canonical_body_loop.py (16-waypoint body loop)

8D = [P, Z, Q, W, H, Gamma, G, Nu]
5D = [r, h, d, p, s]  (from 512)
"""
from __future__ import annotations

import csv
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).parent.parent
GEN_DIR = pathlib.Path(__file__).parent / "generated"

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

# 128 master
_rows128: list[dict[str, str]] = []
with (ROOT / "128_UNIFIED_MASTER_8D_fixed.csv").open(encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        _rows128.append(r)

# 512 master: element → {A,B,C,D → row}
_layers512: dict[str, dict[str, dict[str, str]]] = {}
with (ROOT / "512_WITH_MUSIC_FIXED.csv").open(encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        _layers512.setdefault(r["Element"], {})[r["Layer"]] = r

# circuit nodes
_circuit: dict[str, Any] = {
    n["name"]: n for n in json.loads((GEN_DIR / "circuit.json").read_text(encoding="utf-8"))
}

# body locations
_body_locs: dict[str, Any] = json.loads(
    (GEN_DIR / "body_locations.json").read_text(encoding="utf-8")
)

# canonical body loop waypoints
try:
    from .canonical_body_loop import WAYPOINTS
    _loop_nodes = [w[0] for w in WAYPOINTS]
except Exception:
    _loop_nodes = []

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VEC8_COLS = {
    "P": ["Vector_8D_P_Release", "Vector_8D_P_Stress", "Vector_8D_P_Extreme"],
    "Z": ["Vector_8D_Z_Release", "Vector_8D_Z_Stress", "Vector_8D_Z_Extreme"],
    "Q": ["Vector_8D_Q_Release", "Vector_8D_Q_Stress", "Vector_8D_Q_Extreme"],
    "W": ["Vector_8D_W_Release", "Vector_8D_W_Stress", "Vector_8D_W_Extreme"],
    "H": ["Vector_8D_H_Release", "Vector_8D_H_Stress", "Vector_8D_H_Extreme"],
}
GAMMA_COL = "Vector_8D_Gamma"
G_COL = "Vector_8D_G"
NU_COL = "Vector_8D_Nu"
GENRE_COLS = ["Genre_Release", "Genre_Stress_Growth", "Genre_Extreme_Growth"]
PHASE_NAMES = ["release", "stress_growth", "extreme_growth"]
TENSION_5D = ["Rhythm_Density", "Harmonic_Tension", "Dynamic_Curve",
              "Predictability_Inv", "Spectral_Brightness"]

LAYER_META = {
    "A": {"rh": "RH+ homozygous", "category": "release",       "label": "Self-preservation"},
    "B": {"rh": "RH- homozygous", "category": "stress_growth", "label": "Temperament flip"},
    "C": {"rh": "RH+ heterozygous","category": "stress_growth", "label": "Complexity shift"},
    "D": {"rh": "RH- heterozygous","category": "extreme_growth","label": "Entropy / 3AM breakdown"},
}


def _entity_to_node(entity: str) -> str:
    return entity.split(".")[0].replace("_out_", "").replace("_ctrl_", "")


def _loop_position(node: str) -> int | None:
    for i, wn in enumerate(_loop_nodes):
        if wn == node or wn in node or node in wn:
            return i
    return None


def _vec8d_from_128(row: dict, phase_idx: int) -> dict[str, float]:
    v = {}
    for dim, cols in VEC8_COLS.items():
        v[dim] = float(row[cols[phase_idx]])
    v["Gamma"] = float(row[GAMMA_COL])
    v["G"] = float(row[G_COL])
    v["Nu"] = float(row[NU_COL])
    return v


def _tension5d_from_512(row: dict) -> dict[str, float]:
    return {t: float(row.get(t, 0)) for t in TENSION_5D}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def query_slot(slot: int) -> dict[str, Any]:
    """Return complete energy state for a given slot (1-128)."""
    row = _rows128[slot - 1]
    entity = row["Circuit_Entity"]
    node_name = _entity_to_node(entity)
    elem = row["Element"]

    # circuit node info
    cnode = _circuit.get(node_name, {})

    # body location
    bloc = _body_locs.get(node_name, {})
    if not bloc:
        for bn, bv in _body_locs.items():
            if bn in node_name or node_name in bn:
                bloc = bv
                break

    # loop position
    loop_idx = _loop_position(node_name)

    # 3 phases from 128 master (8D)
    phases = []
    for pi, pname in enumerate(PHASE_NAMES):
        phases.append({
            "phase": pname,
            "genre": row[GENRE_COLS[pi]],
            "vec8d": _vec8d_from_128(row, pi),
        })

    # 4 layers from 512 (5D tension + genre + profile)
    layers = {}
    for lk in ("A", "B", "C", "D"):
        lr = _layers512.get(elem, {}).get(lk)
        if lr:
            layers[lk] = {
                "rh": LAYER_META[lk]["rh"],
                "category": LAYER_META[lk]["category"],
                "label": LAYER_META[lk]["label"],
                "profile_original": lr.get("Profile_Original", ""),
                "profile_transformed": lr.get("Profile_Transformed", ""),
                "genre": lr.get("Music_Genre", ""),
                "key": lr.get("Key", ""),
                "tempo_bpm": lr.get("Tempo_BPM", ""),
                "time_sig": lr.get("Time_Sig", ""),
                "tension_5d": _tension5d_from_512(lr),
            }

    return {
        "slot": slot,
        "time_start": row["Slot_Start"],
        "time_end": row["Slot_End"],
        "energy_phase": row["Energy_Phase"],
        "phase_start": row["Phase_Start"],
        "phase_end": row["Phase_End"],
        "main_type": row["Type"],
        "mbti": row["MBTI"],
        "blood": row["Blood"],
        "gender": row["Gender"],
        "profile_key": row["Profile_Key"],
        "element": elem,
        "element_symbol": row["Element_Symbol"],
        "element_number": int(row["Element_Number"]) if row["Element_Number"] else 0,
        "circuit_entity": entity,
        "circuit_node": node_name,
        "circuit_node_info": {
            "element": cnode.get("element", ""),
            "particle": cnode.get("particle", ""),
            "group": cnode.get("group", ""),
            "color": cnode.get("color", ""),
            "music_dims": cnode.get("music_dims", []),
            "location": cnode.get("location", ""),
        },
        "body_location": bloc.get("raw", ""),
        "body_region": bloc.get("region", ""),
        "canonical_loop_index": loop_idx,
        "receptor": row["Receptor"],
        "neurochem": row["Reverse_Energy_Neurochem"],
        "spark_condition": row["Reverse_Energy_Spark_Condition"],
        "potential": float(row["Reverse_Energy_Potential"]),
        "z_index": int(row["Reverse_Energy_Z_Index"]),
        "primary_vector": row["Reverse_Energy_Primary_Vector"],
        "linear_window": row["Reverse_Energy_Linear_Window"],
        "phases_128": phases,
        "layers_512": layers,
    }


def query_all() -> list[dict[str, Any]]:
    return [query_slot(i) for i in range(1, 129)]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        slot = int(sys.argv[1])
        result = query_slot(slot)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        all_slots = query_all()
        out = GEN_DIR / "unified_slot_data.json"
        out.write_text(json.dumps(all_slots, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote 128 slots -> {out}")
        # demo slot 1
        print("\n--- Slot 1 demo ---")
        s1 = all_slots[0]
        print(f"Slot {s1['slot']} ({s1['time_start']}-{s1['time_end']}) {s1['energy_phase']}")
        print(f"  Type: {s1['main_type']}  Entity: {s1['circuit_entity']}")
        print(f"  Body: {s1['body_location']}")
        print(f"  Loop#: {s1['canonical_loop_index']}")
        for p in s1["phases_128"]:
            v = p["vec8d"]
            print(f"  {p['phase']:<16} {p['genre']:<35} "
                  f"P={v['P']:.2f} Z={v['Z']:.2f} Q={v['Q']:.2f} W={v['W']:.2f} H={v['H']:.2f} "
                  f"γ={v['Gamma']:.2f} g={v['G']:.2f} ν={v['Nu']:.2f}")
        for lk in ("A", "B", "C", "D"):
            lr = s1["layers_512"].get(lk)
            if lr:
                t = lr["tension_5d"]
                print(f"  512-{lk} {lr['label']:<22} {lr['genre']:<30} "
                      f"r={t['Rhythm_Density']:.2f} h={t['Harmonic_Tension']:.2f} "
                      f"d={t['Dynamic_Curve']:.2f} p={t['Predictability_Inv']:.2f} "
                      f"s={t['Spectral_Brightness']:.2f}")
