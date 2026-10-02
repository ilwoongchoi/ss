"""Extract LOCATION annotations from circuitfile-rewritten.md and dump a structured file.

Output 1: generated/body_locations.json  – per-node dict {node: {raw: str}}
Output 2: generated/earth_grid.csv       – starter 0.5° grid with column headers only

Run once; rerun after the markdown changes to refresh.
"""
from __future__ import annotations

import csv
import json
import math
import pathlib
import re
from typing import Dict

ROOT = pathlib.Path(__file__).parent.parent
MD_PATH = ROOT / "circuitfile-rewritten.md"
GEN_DIR = ROOT / "canonical_engine" / "generated"
GEN_DIR.mkdir(exist_ok=True)
BODY_LOC_FILE = GEN_DIR / "body_locations.json"
EARTH_GRID_FILE = GEN_DIR / "earth_grid.csv"

# ---------------------------------------------------------------------------
# 1. Extract LOCATION lines
# ---------------------------------------------------------------------------
loc_re = re.compile(r"^[#\s]*LOCATION[:=]?\s*(.+)$", re.IGNORECASE)
node_header_re = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\[")

body_map: Dict[str, Dict[str, str]] = {}
current_node: str | None = None

with MD_PATH.open(encoding="utf-8") as f:
    for line in f:
        m_head = node_header_re.match(line)
        if m_head:
            current_node = m_head.group(1)
            continue
        m_loc = loc_re.match(line)
        if m_loc and current_node:
            body_map[current_node] = {"raw": m_loc.group(1).strip()}

BODY_LOC_FILE.write_text(json.dumps(body_map, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Extracted {len(body_map)} LOCATION annotations → {BODY_LOC_FILE.relative_to(ROOT)}")

# ---------------------------------------------------------------------------
# 2. Create 0.5° earth grid scaffold (if not exists)
# ---------------------------------------------------------------------------
if not EARTH_GRID_FILE.exists():
    with EARTH_GRID_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["lat_deg", "lon_deg", "soil_code", "geology", "biome", "region_tag"])
        # do not populate rows yet – kept empty for manual/automated fill later
    print(f"Scaffolded earth grid → {EARTH_GRID_FILE.relative_to(ROOT)}")
else:
    print("earth_grid.csv already exists – skipped scaffold")
