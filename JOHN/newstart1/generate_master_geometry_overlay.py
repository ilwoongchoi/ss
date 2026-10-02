#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generate_master_geometry_overlay.py
----------------------------------
Builds a single "latest master overlay" from:
  - geometry_package.final_manifold_renderer.get_final_manifold_registry()
  - _UNIVERSAL_GEOMETRY_FINAL_BUNDLE/UNIVERSAL_GEOMETRY_COMPLETE_MAP.json
  - _UNIVERSAL_GEOMETRY_FINAL_BUNDLE/SEAM_GLUE_MAP.csv
  - ARCHETYPE_BRIDGE_MAP.md (archetype labels)

Outputs:
  - MASTER_GEOMETRY_NODES.csv
  - MASTER_GEOMETRY_EDGES.csv
  - MASTER_GEOMETRY_OVERLAY.md
  - MASTER_GEOMETRY_3D.png
"""

from __future__ import annotations

import csv
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "_UNIVERSAL_GEOMETRY_FINAL_BUNDLE"


@dataclass(frozen=True)
class NodeRec:
    node_id: str
    name: str
    x: float
    y: float
    z: float
    sh_r: float
    sh_q0: float
    sh_w_gate: float
    sh_kappa_eff: float
    sh_in_band: int
    archetype: str
    territory_component: str
    notes: str


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_seam_glue_map(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({k: (v or "").strip() for k, v in row.items()})
    return rows


def _normalize_patch_id(patch_id: str) -> str:
    return patch_id.strip()


def _pair_key(a: str, b: str) -> tuple[str, str]:
    a2 = _normalize_patch_id(a)
    b2 = _normalize_patch_id(b)
    return (a2, b2) if a2 <= b2 else (b2, a2)


def _read_bridge_vectors(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    """
    Loads BRIDGE_VECTORS_FINAL.csv (if present) and indexes by unordered name-pair.

    Columns expected:
      u,v,gap_dist,contact_score,drift_factor_used,source
    """
    if not path.exists():
        return {}
    rows: dict[tuple[str, str], dict[str, str]] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = (row.get("u") or "").strip()
            v = (row.get("v") or "").strip()
            if not u or not v:
                continue
            k = _pair_key(u, v)
            rows[k] = {k2: (v2 or "").strip() for k2, v2 in row.items()}
    return rows


def _resolve_bridge_endpoint(
    token: Any,
    patches: dict[str, dict[str, Any]],
    patch_id_by_name: dict[str, str],
) -> tuple[str, str, str]:
    """
    Resolves a bridge endpoint from the COMPLETE_MAP into:
      (patch_id, canonical_name, raw_token_string)

    COMPLETE_MAP is not consistent: sometimes it uses patch ids (A,B,C,...),
    sometimes node names (sheet_id:3, gateway_peak, core_center), sometimes
    numeric sheet indices ("3"). This function normalizes those into the
    patch ids used by the canonical manifold registry.
    """
    raw = "" if token is None else str(token).strip()
    if not raw:
        return "", "", raw

    # 1) already a canonical patch id
    if raw in patches:
        return raw, str(patches[raw].get("name", raw)), raw

    # 2) already a canonical node name
    if raw in patch_id_by_name:
        pid = patch_id_by_name[raw]
        name = str(patches.get(pid, {}).get("name", raw))
        return pid, name, raw

    # 3) numeric sheet index -> "sheet_id:{n}"
    if raw.isdigit():
        name_key = f"sheet_id:{int(raw)}"
        if name_key in patch_id_by_name:
            pid = patch_id_by_name[name_key]
            name = str(patches.get(pid, {}).get("name", name_key))
            return pid, name, raw

    # 4) unknown; keep raw so the row is still visible for debugging
    return raw, raw, raw


def _parse_archetype_bridge_map(md_path: Path) -> dict[str, str]:
    """
    Minimal extractor: assigns archetype labels to node *names* when they appear.
    Falls back to heuristic territory ranges used in ARCHETYPE_BRIDGE_MAP.md.
    """
    text = md_path.read_text(encoding="utf-8", errors="replace")

    explicit: dict[str, str] = {}

    patterns = [
        (r"Big Woman.*?:\s*(.+)", "Big Woman"),
        (r"Small Woman.*?:\s*(.+)", "Small Woman"),
        (r"Big Man.*?:\s*(.+)", "Big Man"),
        (r"Small Man.*?:\s*(.+)", "Small Man"),
    ]
    for pat, label in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if not m:
            continue
        chunk = m.group(1)
        # pull identifiers like sheet_id:12, core_center, right_branch, flash:center_in, flash_bridge, gateway_peak, mediator:synthetic_alpha
        for tok in re.findall(r"(sheet_id:\d+|core_center|right_branch|flash:center_in|flash_bridge|gateway_peak|mediator:synthetic_alpha)", chunk):
            explicit[tok] = label

    # Territory heuristics (what the user has been using consistently)
    for i in range(1, 5):
        explicit.setdefault(f"sheet_id:{i}", "Big Woman")
    for i in range(10, 15):
        explicit.setdefault(f"sheet_id:{i}", "Small Woman")
    explicit.setdefault("core_center", "Big Man")
    explicit.setdefault("right_branch", "Small Man")
    explicit.setdefault("flash:center_in", "Spark")
    explicit.setdefault("flash_bridge", "Spark")
    explicit.setdefault("gateway_peak", "Boundary")
    explicit.setdefault("mediator:synthetic_alpha", "Mediator")

    return explicit


def _component_boundary_tags(seam_rows: list[dict[str, str]]) -> dict[str, str]:
    """
    Tags nodes as:
      - internal_main (in MAIN component at internal bound)
      - internal_isolated (isolated at internal bound)
      - extended (connected after mediator expansion)

    We infer using the seam rows' last internal step where post_components==2.
    """
    # Find the last row with universe_phase == Internal and post_components == 2
    internal_bound_idx: Optional[int] = None
    for idx, row in enumerate(seam_rows):
        phase = (row.get("universe_phase") or row.get("universe_p") or row.get("universe_phase".upper()) or "").lower()
        if not phase:
            phase = (row.get("universe_p") or "").lower()
        post = row.get("post_components", "")
        if ("internal" in phase) and post == "2":
            internal_bound_idx = idx

    tags: dict[str, str] = {}
    if internal_bound_idx is None:
        return tags

    # The seam_glue_map itself doesn't contain explicit membership sets, but the locked theorem does:
    # MAIN = sheet_id:1,2,3,4,10,11,12,13,14 + flash:center_in + flash_bridge
    # ISOLATED = gateway_peak
    # We'll apply those as tags.
    for name in [
        "sheet_id:1",
        "sheet_id:2",
        "sheet_id:3",
        "sheet_id:4",
        "sheet_id:10",
        "sheet_id:11",
        "sheet_id:12",
        "sheet_id:13",
        "sheet_id:14",
        "flash:center_in",
        "flash_bridge",
    ]:
        tags[name] = "internal_main"
    tags["gateway_peak"] = "internal_isolated"
    tags["mediator:synthetic_alpha"] = "extended_only"
    return tags


def _ensure_engine_pair_positions(patches: dict[str, dict[str, Any]]) -> None:
    """
    Injects the engine-pair nodes into the coordinate registry using the canonical
    axis convention from geometry_package.geometry_3d_renderer (central Z axis).

    This does NOT change the intrinsic/extended closure proof; it only makes the
    archetype engine pair visible in the same 3D frame as the manifold embedding.
    """
    # Avoid overwriting if already present in future versions
    if "O" in patches or "BM" in patches:
        return
    try:
        from geometry_package.absolute_constants import CALIBRATED_SKELETON

        r0 = float(CALIBRATED_SKELETON.get("TERMINUS_R", 1.0))
    except Exception:
        r0 = 1.0

    # Place on Z axis: South pole (Big Man) and North jet (Small Man)
    z_span = max(6.0, 6.0 * r0)
    patches["O"] = {"pos": (0.0, 0.0, -z_span), "name": "core_center", "type": "engine_big_man"}
    patches["B_man"] = {"pos": (0.0, 0.0, z_span), "name": "right_branch", "type": "engine_small_man"}


def _node_color(archetype: str) -> str:
    return {
        "Big Woman": "#00ff88",
        "Small Woman": "#4466ff",
        "Big Man": "#ff3366",
        "Small Man": "#ffaa00",
        "Spark": "#ffff55",
        "Mediator": "#ff8800",
        "Boundary": "#ff4444",
    }.get(archetype, "#cccccc")


def _edge_color(kind: str) -> str:
    if kind == "barrier":
        return "#ff4444"
    if kind == "extended":
        return "#ffaa00"
    if kind == "intrinsic":
        return "#dddddd"
    return "#888888"


def _load_external_bridge_weights(path: Path) -> dict[tuple[str, str], float]:
    """
    Optionally load external bridge weights (e.g., LHD sensor evidence).
    CSV columns expected: nearest_bridge, count
    nearest_bridge formatted as "nodeA__nodeB".
    """
    if not path.exists():
        return {}
    try:
        import csv

        weights: dict[tuple[str, str], float] = {}
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nb = (row.get("nearest_bridge") or "").strip()
                if "__" not in nb:
                    continue
                a, b = nb.split("__", 1)
                try:
                    cnt = float(row.get("count", "") or 0.0)
                except Exception:
                    cnt = 0.0
                if cnt <= 0:
                    continue
                k = (a, b) if a <= b else (b, a)
                weights[k] = cnt
        return weights
    except Exception:
        return {}


def main() -> int:
    from geometry_package.final_manifold_renderer import get_final_manifold_registry
    from geometry_package.absolute_constants import (
        CALIBRATED_Q0_MAX,
        CALIBRATED_Q0_MIN,
        CALIBRATED_SKELETON,
        SH_R_BAND_MAX,
        SH_R_BAND_MIN,
    )
    from geometry_package.universal_metrics import gap_contact_drift
    from geometry_package.universal_equation import in_sh_band, kappa_eff, w_gate

    bundle_map = BUNDLE / "UNIVERSAL_GEOMETRY_COMPLETE_MAP.json"
    bundle_seams = BUNDLE / "SEAM_GLUE_MAP.csv"
    archetype_md = ROOT / "ARCHETYPE_BRIDGE_MAP.md"

    if not bundle_map.exists():
        raise SystemExit(f"Missing {bundle_map}")
    if not bundle_seams.exists():
        raise SystemExit(f"Missing {bundle_seams}")
    if not archetype_md.exists():
        raise SystemExit(f"Missing {archetype_md}")

    registry = get_final_manifold_registry()
    patches: dict[str, dict[str, Any]] = dict(registry["patches"])
    intrinsic_seams: list[tuple[str, str, str]] = list(registry["intrinsic_seams"])
    extended_seams: list[tuple[str, str, str]] = list(registry["extended_seams"])
    barrier = tuple(registry["barrier"])

    _ensure_engine_pair_positions(patches)

    # -----------------------------
    # SH chart mapping (deterministic)
    #
    # The closure manifold embedding uses a small integer coordinate system.
    # Regime-1 (SH/TDA) operates on (r, q0). To overlay SH on the same registry,
    # we use a deterministic affine map from the canonical embedding's XY bounds
    # to the calibrated (r, q0) domain.
    # -----------------------------
    xs = [float(info["pos"][0]) for info in patches.values() if "pos" in info]
    ys = [float(info["pos"][1]) for info in patches.values() if "pos" in info]
    min_x = min(xs) if xs else 0.0
    max_x = max(xs) if xs else 1.0
    min_y = min(ys) if ys else 0.0
    max_y = max(ys) if ys else 1.0

    def _map_xy_to_rq0(x: float, y: float) -> tuple[float, float]:
        dx = max(max_x - min_x, 1e-9)
        dy = max(max_y - min_y, 1e-9)
        x_norm = (float(x) - min_x) / dx
        y_norm = (float(y) - min_y) / dy
        r = float(SH_R_BAND_MIN + x_norm * (SH_R_BAND_MAX - SH_R_BAND_MIN))
        q0 = float(CALIBRATED_Q0_MIN + y_norm * (CALIBRATED_Q0_MAX - CALIBRATED_Q0_MIN))
        return r, q0

    # Alias compatibility: some pipelines use F_prime instead of "F'"
    if "F'" in patches and "F_prime" not in patches:
        patches["F_prime"] = dict(patches["F'"])

    complete = _read_json(bundle_map)
    seam_rows = _read_seam_glue_map(bundle_seams)
    bridge_vectors = _read_bridge_vectors(ROOT / "BRIDGE_VECTORS_FINAL.csv")
    external_weights = _load_external_bridge_weights(ROOT / "LHD_UNIFIED_BRIDGES_AGGREGATED.csv")
    max_ext_weight = max(external_weights.values()) if external_weights else 0.0

    archetype_by_name = _parse_archetype_bridge_map(archetype_md)
    component_tags = _component_boundary_tags(seam_rows)

    # Build node registry keyed by node name
    nodes: list[NodeRec] = []
    for patch_id, info in patches.items():
        x, y, z = info["pos"]
        name = str(info["name"])
        sh_r, sh_q0 = _map_xy_to_rq0(float(x), float(y))
        sh_w = float(w_gate(sh_r, sh_q0))
        sh_k = float(kappa_eff(sh_r, sh_q0, use_lookup=True))
        sh_in = 1 if in_sh_band(sh_r, sh_q0) else 0
        archetype = archetype_by_name.get(name, "Unknown")
        territory = component_tags.get(name, "")
        notes = str(info.get("type", ""))
        nodes.append(
            NodeRec(
                patch_id,
                name,
                float(x),
                float(y),
                float(z),
                sh_r,
                sh_q0,
                sh_w,
                sh_k,
                sh_in,
                archetype,
                territory,
                notes,
            )
        )

    # Build seam step lookup from seam_glue_map
    seam_step_by_pair: dict[tuple[str, str], str] = {}
    seam_mech_by_pair: dict[tuple[str, str], str] = {}
    for row in seam_rows:
        a = row.get("patch_a") or row.get("patch1") or row.get("u") or ""
        b = row.get("patch_b") or row.get("patch2") or row.get("v") or ""
        if not a or not b:
            continue
        step = row.get("step", "")
        mech = row.get("mechanism", "") or row.get("seam_class", "") or row.get("seam_type", "")
        seam_step_by_pair[_pair_key(a, b)] = step
        seam_mech_by_pair[_pair_key(a, b)] = mech

    # Build node-id lookup for bridge mapping
    patch_id_by_name = {n.name: n.node_id for n in nodes}

    # Build edge table from complete-map bridges + seam registry
    edge_rows: list[dict[str, Any]] = []
    bridges = complete.get("bridges", [])
    for br in bridges:
        src = br.get("source")
        tgt = br.get("target")
        if not src or not tgt:
            continue

        src_id, src_name, src_raw = _resolve_bridge_endpoint(src, patches, patch_id_by_name)
        tgt_id, tgt_name, tgt_raw = _resolve_bridge_endpoint(tgt, patches, patch_id_by_name)
        if not src_id or not tgt_id:
            continue

        # Compute geometry from coords if available
        src_node = next((n for n in nodes if n.node_id == src_id), None)
        tgt_node = next((n for n in nodes if n.node_id == tgt_id), None)
        if src_node and tgt_node:
            dx = tgt_node.x - src_node.x
            dy = tgt_node.y - src_node.y
            dz = tgt_node.z - src_node.z
            length = float(math.sqrt(dx * dx + dy * dy + dz * dz))
            azimuth = float(math.degrees(math.atan2(dy, dx)))  # XY plane
            elevation = float(math.degrees(math.atan2(dz, math.sqrt(dx * dx + dy * dy))))  # above XY plane
        else:
            length = float("nan")
            azimuth = float("nan")
            elevation = float("nan")

        score = br.get("score")
        gap = br.get("gap")
        status = br.get("status", "")
        kind = br.get("type", "")

        step = seam_step_by_pair.get(_pair_key(src_id, tgt_id), "")
        mech = seam_mech_by_pair.get(_pair_key(src_id, tgt_id), "")

        def _to_float_or_blank(v: Any) -> Any:
            if v is None:
                return ""
            if isinstance(v, (int, float)):
                return float(v)
            s = str(v).strip()
            if not s or s.upper() in {"N/A", "NA", "NONE", "NULL"}:
                return ""
            try:
                return float(s)
            except Exception:
                return ""

        # Attach explicit bridge-vector metrics (if present) keyed by node *names*.
        bv = bridge_vectors.get(_pair_key(str(src_name), str(tgt_name)))
        if isinstance(bv, dict):
            bv_gap = _to_float_or_blank(bv.get("gap_dist"))
            bv_contact = _to_float_or_blank(bv.get("contact_score"))
            bv_drift_factor = _to_float_or_blank(bv.get("drift_factor_used"))
            bv_source = str(bv.get("source") or "")
        else:
            bv_gap = ""
            bv_contact = ""
            bv_drift_factor = ""
            bv_source = ""

        edge_rows.append(
            {
                "source_id": src_id,
                "source_name": src_name,
                "target_id": tgt_id,
                "target_name": tgt_name,
                "type": kind,
                "status": status,
                "score": _to_float_or_blank(score),
                "gap": _to_float_or_blank(gap),
                "seam_step": step,
                "seam_mechanism": mech,
                "length_3d": length,
                "azimuth_deg": azimuth,
                "elevation_deg": elevation,
                "raw_source": src_raw,
                "raw_target": tgt_raw,
                "bridge_gap_dist": bv_gap,
                "bridge_contact_score": bv_contact,
                "bridge_drift_factor_used": bv_drift_factor,
                "bridge_source": bv_source,
            }
        )

    # Add seams that are in closure registry but not in bridges list
    existing_pairs = {_pair_key(r["source_id"], r["target_id"]) for r in edge_rows}
    for a, b, _lbl in intrinsic_seams + extended_seams:
        k = _pair_key(a, b)
        if k in existing_pairs:
            continue
        a_name = patches.get(a, {}).get("name", a)
        b_name = patches.get(b, {}).get("name", b)
        edge_rows.append(
            {
                "source_id": a,
                "source_name": a_name,
                "target_id": b,
                "target_name": b_name,
                "type": "seam_only",
                "status": "active",
                "score": "",
                "gap": "",
                "seam_step": seam_step_by_pair.get(k, ""),
                "seam_mechanism": seam_mech_by_pair.get(k, ""),
                "length_3d": "",
                "azimuth_deg": "",
                "elevation_deg": "",
            }
        )

    # Export nodes
    nodes_csv = ROOT / "MASTER_GEOMETRY_NODES.csv"
    with nodes_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "node_id",
                "name",
                "x",
                "y",
                "z",
                "sh_r",
                "sh_q0",
                "sh_w_gate",
                "sh_kappa_eff",
                "sh_in_band",
                "archetype",
                "component_tag",
                "notes",
            ]
        )
        for n in sorted(nodes, key=lambda r: (str(r.archetype), str(r.node_id))):
            w.writerow(
                [
                    n.node_id,
                    n.name,
                    n.x,
                    n.y,
                    n.z,
                    n.sh_r,
                    n.sh_q0,
                    n.sh_w_gate,
                    n.sh_kappa_eff,
                    n.sh_in_band,
                    n.archetype,
                    n.territory_component,
                    n.notes,
                ]
            )

    # Export edges
    edges_csv = ROOT / "MASTER_GEOMETRY_EDGES.csv"
    fieldnames = [
        "source_id",
        "source_name",
        "target_id",
        "target_name",
        "type",
        "status",
        "score",
        "gap",
        "seam_step",
        "seam_mechanism",
        "length_3d",
        "azimuth_deg",
        "elevation_deg",
        "raw_source",
        "raw_target",
    ]
    with edges_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in edge_rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})

    # Export canonical gap/contact/drift for all node pairs using the canonical 3D embedding
    node_pos = {n.node_id: (n.x, n.y, n.z) for n in nodes}
    node_sh = {
        n.node_id: {
            "sh_r": n.sh_r,
            "sh_q0": n.sh_q0,
            "sh_w_gate": n.sh_w_gate,
            "sh_kappa_eff": n.sh_kappa_eff,
            "sh_in_band": n.sh_in_band,
        }
        for n in nodes
    }
    metrics_csv = ROOT / "MASTER_GEOMETRY_METRICS_ALL_PAIRS.csv"
    all_ids = sorted(node_pos.keys())
    with metrics_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "u",
                "v",
                "gap",
                "contact",
                "drift",
                "length_3d",
                "azimuth_deg",
                "elevation_deg",
                "detune_1_32",
                "detune_3_32",
                "sh_w_gate_mean",
                "sh_kappa_eff_mean",
                "sh_in_band_both",
                "contact_gated",
                "drift_kappa_scaled",
            ]
        )
        for i, u in enumerate(all_ids):
            for v in all_ids[i + 1 :]:
                m = gap_contact_drift(node_pos[u], node_pos[v])
                sh_u = node_sh.get(u, {})
                sh_v = node_sh.get(v, {})
                w_mean = 0.5 * (float(sh_u.get("sh_w_gate", 0.0)) + float(sh_v.get("sh_w_gate", 0.0)))
                k_mean = 0.5 * (float(sh_u.get("sh_kappa_eff", 0.0)) + float(sh_v.get("sh_kappa_eff", 0.0)))
                in_both = 1 if (int(sh_u.get("sh_in_band", 0)) == 1 and int(sh_v.get("sh_in_band", 0)) == 1) else 0
                contact_gated = float(m.contact) * float(w_mean)
                drift_kappa_scaled = float(m.drift) * (float(k_mean) / (1.0 / 32.0)) if float(k_mean) > 0 else float(m.drift)
                w.writerow(
                    [
                        u,
                        v,
                        m.gap,
                        m.contact,
                        m.drift,
                        m.length_3d,
                        m.azimuth_deg,
                        m.elevation_deg,
                        m.detune_1_32,
                        m.detune_3_32,
                        w_mean,
                        k_mean,
                        in_both,
                        contact_gated,
                        drift_kappa_scaled,
                    ]
                )

    # Attach canonical metrics to the existing edge list (for the bridges/seams people actually look at)
    edges_with_metrics_csv = ROOT / "MASTER_GEOMETRY_EDGES_WITH_METRICS.csv"
    metrics_by_pair = {}
    for i, u in enumerate(all_ids):
        for v in all_ids[i + 1 :]:
            metrics_by_pair[(u, v)] = gap_contact_drift(node_pos[u], node_pos[v])

    extra_fields = [
        "canon_gap",
        "canon_contact",
        "canon_drift",
        "detune_1_32",
        "detune_3_32",
        "sh_r_u",
        "sh_q0_u",
        "sh_w_gate_u",
        "sh_kappa_eff_u",
        "sh_in_band_u",
        "sh_r_v",
        "sh_q0_v",
        "sh_w_gate_v",
        "sh_kappa_eff_v",
        "sh_in_band_v",
        "sh_w_gate_mean",
        "sh_kappa_eff_mean",
        "sh_in_band_both",
        "canon_contact_gated",
        "canon_drift_kappa_scaled",
        "bridge_gap_dist",
        "bridge_contact_score",
        "bridge_drift_factor_used",
        "bridge_source",
    ]
    out_fields = fieldnames + extra_fields
    with edges_with_metrics_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        for r in edge_rows:
            a = str(r.get("source_id", ""))
            b = str(r.get("target_id", ""))
            u, v = (a, b) if a <= b else (b, a)
            m = metrics_by_pair.get((u, v))
            row_out = {k: r.get(k, "") for k in fieldnames}
            if m is None:
                row_out.update({k: "" for k in extra_fields})
            else:
                row_out.update(
                    {
                        "canon_gap": m.gap,
                        "canon_contact": m.contact,
                        "canon_drift": m.drift,
                        "detune_1_32": m.detune_1_32,
                        "detune_3_32": m.detune_3_32,
                    }
                )

            sh_a = node_sh.get(a, {})
            sh_b = node_sh.get(b, {})
            row_out.update(
                {
                    "sh_r_u": sh_a.get("sh_r", ""),
                    "sh_q0_u": sh_a.get("sh_q0", ""),
                    "sh_w_gate_u": sh_a.get("sh_w_gate", ""),
                    "sh_kappa_eff_u": sh_a.get("sh_kappa_eff", ""),
                    "sh_in_band_u": sh_a.get("sh_in_band", ""),
                    "sh_r_v": sh_b.get("sh_r", ""),
                    "sh_q0_v": sh_b.get("sh_q0", ""),
                    "sh_w_gate_v": sh_b.get("sh_w_gate", ""),
                    "sh_kappa_eff_v": sh_b.get("sh_kappa_eff", ""),
                    "sh_in_band_v": sh_b.get("sh_in_band", ""),
                }
            )
            try:
                row_out["sh_w_gate_mean"] = 0.5 * (float(sh_a.get("sh_w_gate", 0.0)) + float(sh_b.get("sh_w_gate", 0.0)))
            except Exception:
                row_out["sh_w_gate_mean"] = ""
            try:
                row_out["sh_kappa_eff_mean"] = 0.5 * (float(sh_a.get("sh_kappa_eff", 0.0)) + float(sh_b.get("sh_kappa_eff", 0.0)))
            except Exception:
                row_out["sh_kappa_eff_mean"] = ""
            try:
                row_out["sh_in_band_both"] = (
                    1 if int(sh_a.get("sh_in_band", 0)) == 1 and int(sh_b.get("sh_in_band", 0)) == 1 else 0
                )
            except Exception:
                row_out["sh_in_band_both"] = ""

            # Derived SH-gated metrics (keep canon_* untouched; provide explicit gated columns)
            try:
                row_out["canon_contact_gated"] = float(row_out.get("canon_contact", 0.0)) * float(row_out.get("sh_w_gate_mean", 0.0))
            except Exception:
                row_out["canon_contact_gated"] = ""
            try:
                k_mean = float(row_out.get("sh_kappa_eff_mean", 0.0))
                row_out["canon_drift_kappa_scaled"] = (
                    float(row_out.get("canon_drift", 0.0)) * (k_mean / (1.0 / 32.0)) if k_mean > 0 else float(row_out.get("canon_drift", 0.0))
                )
            except Exception:
                row_out["canon_drift_kappa_scaled"] = ""

            # Always preserve explicit bridge-vector scan values (if present on the edge row).
            for k in ["bridge_gap_dist", "bridge_contact_score", "bridge_drift_factor_used", "bridge_source"]:
                row_out[k] = r.get(k, "")
            writer.writerow(row_out)

    # Render 3D overlay
    fig = plt.figure(figsize=(18, 14), facecolor="#0a0a15")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0a0a15")

    # nodes
    for n in nodes:
        ax.scatter(n.x, n.y, n.z, s=220, c=_node_color(n.archetype), edgecolors="white", linewidths=1.2, alpha=0.95)
        ax.text(n.x, n.y, n.z + 0.35, f"{n.node_id}\n{n.name}", color="white", fontsize=7, ha="center")

    # edges (thin + overlay for intrinsic/extended)
    def _draw_edge(a: str, b: str, color: str, lw: float, alpha: float) -> None:
        na = next((n for n in nodes if n.node_id == a), None)
        nb = next((n for n in nodes if n.node_id == b), None)
        if not na or not nb:
            return
        ax.plot([na.x, nb.x], [na.y, nb.y], [na.z, nb.z], color=color, lw=lw, alpha=alpha)

    for r in edge_rows:
        a = str(r["source_id"])
        b = str(r["target_id"])
        name_a = str(r.get("source_name", ""))
        name_b = str(r.get("target_name", ""))
        ext_key = (name_a, name_b) if name_a <= name_b else (name_b, name_a)
        ext_w = external_weights.get(ext_key, 0.0)
        ext_lw = 0.0
        if max_ext_weight > 0 and ext_w > 0:
            # Normalize to [0.5, 4.0] thickness boost
            ext_lw = 0.5 + 3.5 * (ext_w / max_ext_weight)

        if _pair_key(a, b) == _pair_key(barrier[0], barrier[1]):
            _draw_edge(a, b, _edge_color("barrier"), 2.5 + ext_lw, 0.9)
            continue
        # classify by whether seam_step exists and its universe_phase (from seam map text)
        step = str(r.get("seam_step") or "")
        if step:
            # step 10+ treated as extended in this proof
            try:
                step_i = int(float(step))
            except Exception:
                step_i = -1
            if step_i >= 10:
                _draw_edge(a, b, _edge_color("extended"), 2.2 + ext_lw, 0.85)
            else:
                _draw_edge(a, b, _edge_color("intrinsic"), 1.6 + ext_lw, 0.55)
        else:
            # background candidate bridges
            sc = r.get("bridge_contact_score") or r.get("score")
            try:
                scv = float(sc) if sc not in ("", None) else 0.0
            except Exception:
                scv = 0.0

            kind = str(r.get("type") or "")
            if kind == "calculated_missing_vector":
                # These are long-range bridges; their scores are intentionally small.
                lw = 0.8 + 2.8 * max(0.0, min(1.0, scv / 0.02)) + ext_lw
                _draw_edge(a, b, "#ffaa00", lw, 0.28)
            elif kind == "corridor":
                lw = 0.8 + 3.2 * max(0.0, min(1.0, scv)) + ext_lw
                _draw_edge(a, b, "#ff3366", lw, 0.35)
            else:
                lw = 0.4 + 2.0 * max(0.0, min(1.0, scv)) + ext_lw
                _draw_edge(a, b, "#666677", lw, 0.18)

    ax.set_axis_off()
    ax.set_box_aspect([1.0, 1.0, 1.0])

    # Title + constants overlay (the ones the user keeps asking about)
    spark = float(CALIBRATED_SKELETON.get("SPARK_ANGLE_DEG", 138.88))
    w7 = float(CALIBRATED_SKELETON.get("W7_AREA", math.pi / 20.0))
    k_1_32 = float(CALIBRATED_SKELETON.get("KAPPA_1_32", 1.0 / 32.0))
    k_3_32 = float(CALIBRATED_SKELETON.get("COMPRESSION_GAP_3_32", 3.0 / 32.0))
    h2_w7 = float(CALIBRATED_SKELETON.get("H2_W7", 1.0 / 9.0))
    # Quick SH summary (to make sure the band is actually reflected)
    try:
        w_mean = sum(float(n.sh_w_gate) for n in nodes) / max(len(nodes), 1)
        in_band_n = sum(int(n.sh_in_band) for n in nodes)
    except Exception:
        w_mean = 0.0
        in_band_n = 0
    ax.text2D(
        0.02,
        0.98,
        "MASTER OVERLAY (canonical patch embedding)\n"
        f"Constants: W7=pi/20={w7:.6f}, 1/32={k_1_32:.6f}, 3/32={k_3_32:.6f}, H2={h2_w7:.6f}, Spark={spark:.2f} deg\n"
        f"SH: w_gate_mean={w_mean:.4f}, in_band_nodes={in_band_n}/{len(nodes)}\n"
        "Colors: BigWoman/SmallWoman/BigMan/SmallMan/Spark/Mediator/Boundary",
        transform=ax.transAxes,
        color="white",
        fontsize=10,
        family="monospace",
    )

    out_png = ROOT / "MASTER_GEOMETRY_3D.png"
    plt.savefig(out_png, dpi=240, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)

    # Markdown summary (single place to look)
    md = ROOT / "MASTER_GEOMETRY_OVERLAY.md"
    md.write_text(
        "\n".join(
            [
                "# MASTER GEOMETRY OVERLAY (Latest)",
                "",
                "This overlay is built from the canonical patch embedding in `geometry_package/final_manifold_renderer.py`",
                "and the latest closure trace + bridge list in `_UNIVERSAL_GEOMETRY_FINAL_BUNDLE/`.",
                "",
                "## Outputs",
                f"- `MASTER_GEOMETRY_NODES.csv`",
                f"- `MASTER_GEOMETRY_EDGES.csv`",
                f"- `MASTER_GEOMETRY_EDGES_WITH_METRICS.csv` (bridges/seams + canon_* + bridge_* metrics)",
                f"- `MASTER_GEOMETRY_METRICS_ALL_PAIRS.csv` (gap/contact/drift for any node pair)",
                f"- `MASTER_GEOMETRY_3D.png`",
                "",
                "## What this fixes (your complaint)",
                "- Keeps the 2-component internal bound (gateway_peak isolated) and shows the extended mediator bypass.",
                "- Keeps 4 archetypes visible as labels/colors (Big Woman / Small Woman / Big Man / Small Man) instead of collapsing to anonymous points.",
                "- Keeps the constants in-frame (pi/20, 1/32, 3/32, 1/9, spark 138.88°) from `absolute_constants.py`.",
                "",
                "## Angle meaning (in this artifact)",
                "- `azimuth_deg`: edge direction in XY plane of the canonical embedding.",
                "- `elevation_deg`: tilt above XY plane.",
                "- These angles are computed from the *canonical patch coordinates* (not a spring layout).",
                "",
                "## Canonical edge function (requested)",
                "- `gap/contact/drift(u,v)` is implemented in `geometry_package/universal_metrics.py` on the canonical 3D embedding.",
                "- All-pairs results are exported to `MASTER_GEOMETRY_METRICS_ALL_PAIRS.csv`.",
                "",
                "## Note on engine pair visibility",
                "- `core_center` (Big Man) and `right_branch` (Small Man) are injected on the canonical Z-axis so they are visible in the same 3D frame.",
                "  This does not change closure steps; it is a coordinate overlay for archetype visibility.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        f"Wrote {nodes_csv.name}, {edges_csv.name}, {edges_with_metrics_csv.name}, "
        f"{metrics_csv.name}, {out_png.name}, {md.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
