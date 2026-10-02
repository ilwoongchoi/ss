"""Very simple normaliser: try to extract body side (left/right/central), coarse region, and tissue type from raw LOCATION strings.
This is heuristic and meant as a starter; manual curation will still be required.

Output: generated/body_locations_normalized.json
"""
from __future__ import annotations

import json
import pathlib
import re
from typing import Dict

ROOT = pathlib.Path(__file__).parent.parent
RAW_FILE = ROOT / "canonical_engine" / "generated" / "body_locations.json"
OUT_FILE = ROOT / "canonical_engine" / "generated" / "body_locations_normalized.json"

raw: Dict[str, Dict[str, str]] = json.loads(RAW_FILE.read_text(encoding="utf-8"))

side_kw = {
    "left": "left",
    "right": "right",
    "bilateral": "bilateral",
    "midline": "center",
    "center": "center",
}

region_kw = {
    "foot": "foot",
    "toe": "foot",
    "ankle": "ankle",
    "knee": "knee",
    "hip": "hip",
    "calf": "calf",
    "abdomen": "abdomen",
    "chest": "chest",
    "rib": "chest",
    "waist": "waist",
    "back": "back",
    "spine": "back",
    "shoulder": "shoulder",
    "arm": "arm",
    "wrist": "wrist",
    "hand": "hand",
    "finger": "hand",
    "neck": "neck",
    "head": "head",
    "scalp": "head",
    "ear": "head",
    "lip": "face",
    "nose": "face",
    "eye": "face",
    "brain": "brain",
}

norm: Dict[str, Dict[str, str]] = {}
for node, data in raw.items():
    txt = data["raw"].lower()
    side = next((v for k, v in side_kw.items() if k in txt), "unspecified")
    region = next((v for k, v in region_kw.items() if k in txt), "other")
    norm[node] = {
        "raw": data["raw"],
        "side": side,
        "region": region,
    }

OUT_FILE.write_text(json.dumps(norm, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Normalized {len(norm)} body locations → {OUT_FILE.relative_to(ROOT)}")
