#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
export_viewer_data.py
---------------------
Exports the current master geometry tables + key constants to a single JSON
for the 128-grid + shader viewer.

Inputs:
  - MASTER_GEOMETRY_NODES.csv
  - MASTER_GEOMETRY_EDGES_WITH_METRICS.csv
  - geometry_package/absolute_constants.py (constants)

Output:
  - viewer/geometry_data.json
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


def _to_float(v: str) -> float | None:
    s = (v or "").strip()
    if not s or s.upper() in {"N/A", "NA", "NULL", "NONE"}:
        return None
    try:
        return float(s)
    except Exception:
        return None


def main() -> int:
    nodes_csv = ROOT / "MASTER_GEOMETRY_NODES.csv"
    edges_csv = ROOT / "MASTER_GEOMETRY_EDGES_WITH_METRICS.csv"
    if not nodes_csv.exists():
        raise SystemExit("Missing MASTER_GEOMETRY_NODES.csv (run generate_master_geometry_overlay.py)")
    if not edges_csv.exists():
        raise SystemExit("Missing MASTER_GEOMETRY_EDGES_WITH_METRICS.csv (run generate_master_geometry_overlay.py)")

    nodes_in = _read_csv(nodes_csv)
    edges_in = _read_csv(edges_csv)

    nodes: list[dict[str, Any]] = []
    for r in nodes_in:
        nodes.append(
            {
                "id": r["node_id"],
                "name": r["name"],
                "archetype": r.get("archetype", ""),
                "component_tag": r.get("component_tag", ""),
                "pos": [_to_float(r["x"]) or 0.0, _to_float(r["y"]) or 0.0, _to_float(r["z"]) or 0.0],
            }
        )

    edges: list[dict[str, Any]] = []
    for r in edges_in:
        edges.append(
            {
                "u": r.get("source_id", ""),
                "v": r.get("target_id", ""),
                "type": r.get("type", ""),
                "status": r.get("status", ""),
                "seam_step": _to_float(r.get("seam_step", "")),
                "score": _to_float(r.get("score", "")),
                "gap": _to_float(r.get("gap", "")),
                "canon_gap": _to_float(r.get("canon_gap", "")),
                "canon_contact": _to_float(r.get("canon_contact", "")),
                "canon_drift": _to_float(r.get("canon_drift", "")),
                "azimuth_deg": _to_float(r.get("azimuth_deg", "")),
                "elevation_deg": _to_float(r.get("elevation_deg", "")),
                "detune_1_32": _to_float(r.get("detune_1_32", "")),
                "detune_3_32": _to_float(r.get("detune_3_32", "")),
            }
        )

    from geometry_package.absolute_constants import (
        CALIBRATED_SKELETON,
        NIGHT_HYSTERESIS,
        VERTICAL_MOBIUS_TWIST,
        SPARK_ANGLE_DEG,
        LATTICE_3_32,
        TUNNEL_TENSION,
        BETTI_11,
        BETTI_7,
    )

    out = {
        "schema": "geometry_viewer_v1",
        "nodes": nodes,
        "edges": edges,
        "constants": {
            "NIGHT_HYSTERESIS": float(NIGHT_HYSTERESIS),
            "VERTICAL_MOBIUS_TWIST": float(VERTICAL_MOBIUS_TWIST),
            "SPARK_ANGLE_DEG": float(SPARK_ANGLE_DEG),
            "LATTICE_3_32": float(LATTICE_3_32),
            "TUNNEL_TENSION": float(TUNNEL_TENSION),
            "BETTI_11": float(BETTI_11),
            "BETTI_7": float(BETTI_7),
            "CALIBRATED_SKELETON": {k: (v[0] if isinstance(v, (list, tuple)) and v else v) for k, v in CALIBRATED_SKELETON.items()},
        },
    }

    viewer_dir = ROOT / "viewer"
    viewer_dir.mkdir(exist_ok=True)
    out_path = viewer_dir / "geometry_data.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

