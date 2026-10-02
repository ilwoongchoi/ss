"""Extract per-slot 4-layer 8D vectors + genre 8D vectors.

For each of 128 slots:
  - main type (from 128_UNIFIED_MASTER_8D_fixed.csv)
  - layer 1 (A) = release: 8D vector + genre
  - layer 2 (B) = stress_growth: 8D vector + genre
  - layer 3 (C) = extreme_growth: 8D vector + genre
  - layer 4 (D) = 512 layer D: 8D vector + genre (from 512_WITH_MUSIC_FIXED.csv)

8D = [P, Z, Q, W, H, Gamma, G, Nu]
"""
from __future__ import annotations

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
GEN_DIR = pathlib.Path(__file__).parent / "generated"
MASTER_128 = ROOT / "128_UNIFIED_MASTER_8D_fixed.csv"
MASTER_512 = ROOT / "512_WITH_MUSIC_FIXED.csv"

# --- read 128 master ---
rows128 = []
with MASTER_128.open(encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows128.append(r)

# --- read 512 master: element -> 4 layers ---
layers512 = {}  # element_symbol -> {A,B,C,D -> row}
with MASTER_512.open(encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for r in reader:
        elem = r["Element"]
        layer = r["Layer"]
        layers512.setdefault(elem, {})[layer] = r

# 5D tension columns in 512
TENSION_5D = ["Rhythm_Density", "Harmonic_Tension", "Dynamic_Curve",
              "Predictability_Inv", "Spectral_Brightness"]

# 8D column names in 128
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

output = []
for r in rows128:
    slot = r["Reverse_Order"]
    elem = r["Element"]  # e.g. "Rf(104)"
    main_type = r["Type"]
    profile = r["Profile_Key"]
    circuit_entity = r["Circuit_Entity"]

    # 3 phases from 128 master (release/stress/extreme)
    phases = []
    for pi, pname in enumerate(PHASE_NAMES):
        vec = {}
        for dim, cols in VEC8_COLS.items():
            vec[dim] = float(r[cols[pi]])
        vec["Gamma"] = float(r[GAMMA_COL])
        vec["G"] = float(r[G_COL])
        vec["Nu"] = float(r[NU_COL])
        genre = r[GENRE_COLS[pi]]
        phases.append({"phase": pname, "genre": genre, "vec8d": vec})

    # 4th layer from 512 (layer D = extreme = opposite+blood+1)
    layer_d = layers512.get(elem, {}).get("D", {})
    vec_d = {}
    if layer_d:
        for t in TENSION_5D:
            vec_d[t] = float(layer_d.get(t, 0))
        vec_d["genre"] = layer_d.get("Music_Genre", "")
        vec_d["profile"] = layer_d.get("Profile_Transformed", "")
        vec_d["music_category"] = layer_d.get("Music_Category", "")

    # also get layer A/B/C from 512 for cross-reference
    layers_ref = {}
    for lk in ("A", "B", "C", "D"):
        lr = layers512.get(elem, {}).get(lk, {})
        if lr:
            layers_ref[lk] = {
                "profile": lr.get("Profile_Transformed", ""),
                "music_category": lr.get("Music_Category", ""),
                "genre": lr.get("Music_Genre", ""),
                "tension_5d": {t: float(lr.get(t, 0)) for t in TENSION_5D},
            }

    output.append({
        "slot": int(slot),
        "main_type": main_type,
        "profile": profile,
        "element": elem,
        "circuit_entity": circuit_entity,
        "energy_phase": r["Energy_Phase"],
        "slot_start": r["Slot_Start"],
        "slot_end": r["Slot_End"],
        "layer1_release": phases[0],
        "layer2_stress": phases[1],
        "layer3_extreme": phases[2],
        "layer4_512D": vec_d,
        "layers_512_ref": layers_ref,
    })

OUT_JSON = GEN_DIR / "slot_layer_vectors.json"
OUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

# also write a compact CSV
OUT_CSV = GEN_DIR / "slot_layer_vectors.csv"
csv_lines = ["slot,main_type,profile,element,circuit_entity,phase,genre,P,Z,Q,W,H,Gamma,G,Nu"]
for o in output:
    for lk in ("layer1_release", "layer2_stress", "layer3_extreme"):
        p = o[lk]
        v = p["vec8d"]
        csv_lines.append(
            f"{o['slot']},{o['main_type']},{o['profile']},{o['element']},{o['circuit_entity']},"
            f"{p['phase']},{p['genre']},"
            f"{v['P']},{v['Z']},{v['Q']},{v['W']},{v['H']},{v['Gamma']},{v['G']},{v['Nu']}"
        )
    # layer 4 from 512
    d = o["layer4_512D"]
    if d:
        csv_lines.append(
            f"{o['slot']},{o['main_type']},{o['profile']},{o['element']},{o['circuit_entity']},"
            f"layer4_512D,{d.get('genre','')},"
            f"{d.get('Rhythm_Density','')},{d.get('Harmonic_Tension','')},{d.get('Dynamic_Curve','')},"
            f"{d.get('Predictability_Inv','')},{d.get('Spectral_Brightness','')},,,"
        )
OUT_CSV.write_text("\n".join(csv_lines), encoding="utf-8")

print(f"Wrote {len(output)} slots -> {OUT_JSON}")
print(f"Wrote compact CSV -> {OUT_CSV}")
