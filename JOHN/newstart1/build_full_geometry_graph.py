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
    label: str
    weight: float | None = None


def read_bridge_vectors(path: Path) -> list[Edge]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        out: list[Edge] = []
        for row in r:
            u = row.get("u") or ""
            v = row.get("v") or ""
            gap = row.get("gap_dist") or ""
            contact = row.get("contact_score") or ""
            drift = row.get("drift_factor_used") or ""
            label = f"gap={gap}, contact={contact}, drift={drift}"
            w = None
            try:
                w = float(row.get("contact_score") or "")
            except ValueError:
                w = None
            if u and v:
                out.append(Edge(u=u, v=v, label=label, weight=w))
        return out


def read_seam_glue_map(path: Path) -> list[Edge]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        out: list[Edge] = []
        for row in r:
            a = (row.get("patch_a") or row.get("seam_a") or "").strip()
            b = (row.get("patch_b") or row.get("seam_b") or "").strip()
            c = (row.get("patch_c") or "").strip()
            seam_type = (row.get("seam_type") or "").strip()
            seam_class = (row.get("seam_class") or "").strip()
            step = (row.get("step") or "").strip()
            red = (row.get("reduction") or "").strip()
            label = f"{seam_type}/{seam_class} step={step} red={red}"
            if a and b:
                out.append(Edge(u=a, v=b, label=label))
            if c and b:
                # represent relay third leg as dashed-ish label (still an edge)
                out.append(Edge(u=c, v=b, label=f"relay->{label}"))
        return out


def read_components_final(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_universal_map(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def parse_unresolved_gaps(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for ln in lines:
        if "NO UNRESOLVED GAPS REMAIN" in ln:
            return []
    gaps: list[str] = []
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("- "):
            gaps.append(s[2:].strip())
        else:
            gaps.append(s)
    # de-dup
    seen = set()
    out = []
    for g in gaps:
        if g in seen:
            continue
        seen.add(g)
        out.append(g)
    return out


def parse_missing_jobs(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return list(r)


def to_dot(
    *,
    nodes: set[str],
    edges: list[Edge],
    components: dict[str, Any],
    title: str,
) -> str:
    # color nodes by component territory if available
    female = set()
    male = set()
    try:
        female = set((components.get("female_territory") or components.get("component_a") or []))
        male = set((components.get("male_territory") or components.get("component_b") or []))
    except Exception:
        pass

    lines = [
        "digraph FULL_GEOMETRY {",
        '  graph [rankdir="LR", labelloc="t", fontsize=20];',
        f'  label="{title}";',
        '  node [shape="ellipse", style="filled", fontname="Consolas"];',
        '  edge [fontname="Consolas"];',
        "",
    ]
    for n in sorted(nodes):
        if n in female:
            color = "#ffdfef"
        elif n in male:
            color = "#dfefff"
        else:
            color = "#f2f2f2"
        safe = n.replace('"', '\\"')
        lines.append(f'  "{safe}" [fillcolor="{color}"];')

    lines.append("")
    for e in edges:
        u = e.u.replace('"', '\\"')
        v = e.v.replace('"', '\\"')
        lab = e.label.replace('"', '\\"')
        pen = 1.0
        if e.weight is not None:
            pen = 1.0 + 4.0 * max(0.0, min(1.0, e.weight))
        lines.append(f'  "{u}" -> "{v}" [label="{lab}", penwidth={pen:.2f}];')
    lines.append("}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Build a single full-geometry graph + missing-items report from current outputs.")
    ap.add_argument("--out-prefix", default="FULL_GEOMETRY")
    args = ap.parse_args(argv)

    bridges = read_bridge_vectors(Path("BRIDGE_VECTORS_FINAL.csv"))
    # If we have a seam glue map (the actual 12→1 closure trace), include it for a non-trivial graph.
    seam_edges = read_seam_glue_map(Path("_UNIVERSAL_GEOMETRY_FINAL_BUNDLE/SEAM_GLUE_MAP.csv"))
    if seam_edges:
        bridges = seam_edges + bridges
    comps = read_components_final(Path("COMPONENTS_FINAL.json"))
    uni = read_universal_map(Path("UNIVERSAL_GEOMETRY_COMPLETE_MAP.json"))
    gaps = parse_unresolved_gaps(Path("UNRESOLVED_FINAL_GAPS.md"))
    jobs = parse_missing_jobs(Path("missing_bridge_jobs.csv"))

    nodes = set()
    for e in bridges:
        nodes.add(e.u)
        nodes.add(e.v)

    # pull nodes from universal map if present
    for k in ("nodes", "node_list", "entities"):
        v = uni.get(k)
        if isinstance(v, list):
            for item in v:
                if isinstance(item, str):
                    nodes.add(item)

    # add any sheet_id:* tokens that appear in gap text
    for g in gaps:
        for m in re.findall(r"(sheet_id:\\d+|gateway_peak|flash:center_in|flash_bridge|mediator:[A-Za-z0-9_]+|core_center|right_branch)", g):
            nodes.add(m)

    title = "Full Geometry Graph (Current Locked Outputs)"
    dot = to_dot(nodes=nodes, edges=bridges, components=comps, title=title)
    dot_path = Path(f"{args.out_prefix}.dot")
    dot_path.write_text(dot, encoding="utf-8")

    report = {
        "nodes": sorted(nodes),
        "edges": [e.__dict__ for e in bridges],
        "unresolved_gaps_count": len(gaps),
        "unresolved_gaps": gaps,
        "missing_bridge_jobs_count": len(jobs),
        "missing_bridge_jobs": jobs,
    }
    json_path = Path(f"{args.out_prefix}_MISSING_AND_GRAPH.json")
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines = [
        "# Full Geometry — What is still missing",
        "",
        f"- Nodes in graph: `{len(nodes)}`",
        f"- Edges in `BRIDGE_VECTORS_FINAL.csv`: `{len(bridges)}`",
        f"- Unresolved gaps: `{len(gaps)}` (source: `UNRESOLVED_FINAL_GAPS.md`)",
        f"- Missing bridge jobs: `{len(jobs)}` (source: `missing_bridge_jobs.csv`)",
        "",
        "## Unresolved gaps",
    ]
    for g in gaps[:200]:
        md_lines.append(f"- {g}")
    md_lines.append("")
    md_lines.append("## Missing bridge jobs")
    if jobs:
        keys = list(jobs[0].keys())
        md_lines.append("")
        md_lines.append("| " + " | ".join(keys) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(keys)) + " |")
        for row in jobs[:200]:
            md_lines.append("| " + " | ".join((row.get(k) or "").replace("\n", " ") for k in keys) + " |")

    md_path = Path(f"{args.out_prefix}_MISSING.md")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(str(dot_path))
    print(str(md_path))
    print(str(json_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
