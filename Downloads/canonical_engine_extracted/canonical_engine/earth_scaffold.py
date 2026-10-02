"""Generate a node→earth-region scaffold CSV from existing LOCATION data.

Output: generated/earth_node_map.csv
Columns:
    node, body_region, side, suggested_soil, suggested_geology, lat_est, lon_est
The last four columns are left blank for manual / external DB fill.
"""
from __future__ import annotations

import csv
import json
import pathlib
from typing import Dict

ROOT = pathlib.Path(__file__).parent
GEN_DIR = ROOT / "generated"
RAW_LOC = GEN_DIR / "body_locations_normalized.json"
OUT = GEN_DIR / "earth_node_map.csv"

data: Dict[str, Dict[str, str]] = json.loads(RAW_LOC.read_text(encoding="utf-8"))

with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "node",
        "body_region",
        "side",
        "suggested_soil",
        "suggested_geology",
        "lat_est_deg",
        "lon_est_deg",
    ])
    for node, meta in data.items():
        writer.writerow([
            node,
            meta.get("region", ""),
            meta.get("side", ""),
            "",
            "",
            "",
            "",
        ])
print(f"Scaffold {OUT.relative_to(ROOT.parent)} written ({len(data)} rows).")
