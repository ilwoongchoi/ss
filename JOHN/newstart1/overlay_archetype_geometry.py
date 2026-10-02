from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Edge:
    u: str
    v: str
    attrs: dict[str, Any]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_bridge_vectors(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    if not path.exists():
        return {}
    rows = read_csv(path)
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for r in rows:
        u = (r.get("u") or "").strip()
        v = (r.get("v") or "").strip()
        if not u or not v:
            continue
        out[(u, v)] = r
        out[(v, u)] = r
    return out


def read_patch_table(path: Path) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    """
    Returns:
      id->name mapping (e.g., 'A' -> 'sheet_id:1')
      name->row attrs mapping
    """
    if not path.exists():
        return {}, {}
    rows = read_csv(path)
    id_to_name: dict[str, str] = {}
    name_to_row: dict[str, dict[str, str]] = {}
    for r in rows:
        pid = (r.get("patch_id") or "").strip()
        name = (r.get("patch_name") or "").strip()
        if pid and name:
            id_to_name[pid] = name
            name_to_row[name] = r
    return id_to_name, name_to_row


def read_seam_glue_edges(path: Path, id_to_name: dict[str, str]) -> list[Edge]:
    if not path.exists():
        return []
    rows = read_csv(path)
    out: list[Edge] = []
    for r in rows:
        a = (r.get("patch_a") or "").strip()
        b = (r.get("patch_b") or "").strip()
        c = (r.get("patch_c") or "").strip()
        # expand patch IDs to patch names if possible
        a_name = id_to_name.get(a, a)
        b_name = id_to_name.get(b, b)
        c_name = id_to_name.get(c, c) if c else ""

        attrs = {
            "step": r.get("step"),
            "seam_name": r.get("seam_name"),
            "seam_type": r.get("seam_type"),
            "seam_class": r.get("seam_class"),
            "pre_components": r.get("pre_components"),
            "post_components": r.get("post_components"),
            "reduction": r.get("reduction"),
            "universe_phase": r.get("universe_phase"),
            "mechanism": r.get("mechanism"),
            "kind": "seam_glue",
        }

        if a_name and b_name:
            out.append(Edge(u=a_name, v=b_name, attrs=attrs))
        if c_name and b_name:
            out.append(Edge(u=c_name, v=b_name, attrs={**attrs, "kind": "seam_glue_relay_leg"}))
    return out


def parse_archetype_bridge_map(path: Path) -> dict[str, str]:
    """
    Best-effort mapping node_name -> archetype label.
    Uses the user's canonical labels if present.
    """
    if not path.exists():
        return {}
    txt = path.read_text(encoding="utf-8", errors="replace")

    mapping: dict[str, str] = {}

    # Big Man / Small Man are explicit nodes in the corpus.
    if re.search(r"\bBig Man\b.*\bcore_center\b", txt, flags=re.IGNORECASE | re.DOTALL):
        mapping["core_center"] = "Big Man"
    if re.search(r"\bSmall Man\b.*\bright_branch\b", txt, flags=re.IGNORECASE | re.DOTALL):
        mapping["right_branch"] = "Small Man"

    # Female territory described as sheets 1-4 and 10-14 in user's summary.
    if re.search(r"Big Woman.*sheets\s+1-4", txt, flags=re.IGNORECASE):
        for i in (1, 2, 3, 4):
            mapping[f"sheet_id:{i}"] = "Big Woman"
    if re.search(r"Small Woman.*sheets\s+10-14", txt, flags=re.IGNORECASE):
        for i in (10, 11, 12, 13, 14):
            mapping[f"sheet_id:{i}"] = "Small Woman"

    # Spark system nodes
    if "flash:center_in" in txt:
        mapping["flash:center_in"] = "Spark"
    if "flash_bridge" in txt:
        mapping["flash_bridge"] = "Spark"

    # Gateway/mediator
    if "gateway_peak" in txt:
        mapping["gateway_peak"] = "Boundary"
    if "mediator:synthetic_alpha" in txt:
        mapping["mediator:synthetic_alpha"] = "Mediator"

    return mapping


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Overlay 2-component closure + seam glue trace + bridge vectors + archetype labels.")
    ap.add_argument("--bundle-dir", default="_UNIVERSAL_GEOMETRY_FINAL_BUNDLE")
    ap.add_argument("--bridge-vectors", default="BRIDGE_VECTORS_FINAL.csv")
    ap.add_argument("--archetype-map", default="ARCHETYPE_BRIDGE_MAP.md")
    ap.add_argument("--out-prefix", default="ARCHETYPE_GEOMETRY_OVERLAY")
    args = ap.parse_args(argv)

    bundle = Path(args.bundle_dir)
    patch_table = bundle / "MANIFOLD_PATCH_TABLE.csv"
    seam_glue = bundle / "SEAM_GLUE_MAP.csv"

    id_to_name, name_to_row = read_patch_table(patch_table)
    seam_edges = read_seam_glue_edges(seam_glue, id_to_name)
    bridge_vectors = read_bridge_vectors(Path(args.bridge_vectors))
    archetype = parse_archetype_bridge_map(Path(args.archetype_map))

    nodes: set[str] = set()
    edges: list[dict[str, Any]] = []

    for e in seam_edges:
        nodes.add(e.u)
        nodes.add(e.v)
        vec = bridge_vectors.get((e.u, e.v))
        edges.append(
            {
                "u": e.u,
                "v": e.v,
                **e.attrs,
                "bridge_vector_gap": vec.get("gap_dist") if vec else None,
                "bridge_vector_contact": vec.get("contact_score") if vec else None,
                "bridge_vector_drift": vec.get("drift_factor_used") if vec else None,
                "u_archetype": archetype.get(e.u, ""),
                "v_archetype": archetype.get(e.v, ""),
            }
        )

    # Add bridge-vector-only edges that aren't in seam glue (engine pair etc.)
    for (u, v), r in bridge_vectors.items():
        if (u, v) != (r.get("u"), r.get("v")):
            continue
        nodes.add(u)
        nodes.add(v)
        edges.append(
            {
                "u": u,
                "v": v,
                "kind": "bridge_vector",
                "step": None,
                "seam_name": None,
                "seam_type": None,
                "seam_class": None,
                "pre_components": None,
                "post_components": None,
                "reduction": None,
                "universe_phase": None,
                "mechanism": None,
                "bridge_vector_gap": r.get("gap_dist"),
                "bridge_vector_contact": r.get("contact_score"),
                "bridge_vector_drift": r.get("drift_factor_used"),
                "u_archetype": archetype.get(u, ""),
                "v_archetype": archetype.get(v, ""),
            }
        )

    node_rows: list[dict[str, Any]] = []
    for n in sorted(nodes):
        row = name_to_row.get(n, {})
        node_rows.append(
            {
                "node": n,
                "archetype": archetype.get(n, ""),
                "universe": row.get("universe"),
                "component_role": row.get("component_role"),
                "barrier_status": row.get("barrier_status"),
                "internal_component": row.get("internal_component"),
                "extended_component": row.get("extended_component"),
                "seam_count": row.get("seam_count"),
            }
        )

    out_json = Path(f"{args.out_prefix}.json")
    out_json.write_text(json.dumps({"nodes": node_rows, "edges": edges}, indent=2), encoding="utf-8")

    # Markdown clarity report
    md = []
    md.append("# Archetype × Closure × Bridge Overlay (Clarified)")
    md.append("")
    md.append("This overlay merges:")
    md.append("- the **2-component internal bound** and **extended 2→1 closure** seam trace (`SEAM_GLUE_MAP.csv`),")
    md.append("- the **bridge vector metrics** (`BRIDGE_VECTORS_FINAL.csv`),")
    md.append("- the **archetype labels** from `ARCHETYPE_BRIDGE_MAP.md` (best-effort parse).")
    md.append("")
    md.append("## Nodes")
    md.append("| node | archetype | universe | role | barrier | internal | extended |")
    md.append("|---|---|---|---|---|---|---|")
    for r in node_rows:
        md.append(
            "| "
            + " | ".join(
                [
                    str(r["node"]),
                    str(r["archetype"]),
                    str(r["universe"] or ""),
                    str(r["component_role"] or ""),
                    str(r["barrier_status"] or ""),
                    str(r["internal_component"] or ""),
                    str(r["extended_component"] or ""),
                ]
            )
            + " |"
        )
    md.append("")
    md.append("## Edges (closure trace + bridge vectors)")
    md.append("| kind | step | u | v | u_arch | v_arch | seam_type | class | phase | red | gap | contact | drift |")
    md.append("|---|---:|---|---|---|---|---|---|---|---:|---:|---:|---:|")
    for e in edges:
        md.append(
            "| "
            + " | ".join(
                [
                    str(e.get("kind") or ""),
                    str(e.get("step") or ""),
                    str(e["u"]),
                    str(e["v"]),
                    str(e.get("u_archetype") or ""),
                    str(e.get("v_archetype") or ""),
                    str(e.get("seam_type") or ""),
                    str(e.get("seam_class") or ""),
                    str(e.get("universe_phase") or ""),
                    str(e.get("reduction") or ""),
                    str(e.get("bridge_vector_gap") or ""),
                    str(e.get("bridge_vector_contact") or ""),
                    str(e.get("bridge_vector_drift") or ""),
                ]
            )
            + " |"
        )
    md.append("")
    out_md = Path(f"{args.out_prefix}.md")
    out_md.write_text("\n".join(md), encoding="utf-8")

    print(str(out_md))
    print(str(out_json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
