from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def parse_archetype_bridge_map(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    txt = path.read_text(encoding="utf-8", errors="replace")
    mapping: dict[str, str] = {}
    if re.search(r"\bBig Man\b.*\bcore_center\b", txt, flags=re.IGNORECASE | re.DOTALL):
        mapping["core_center"] = "Big Man"
    if re.search(r"\bSmall Man\b.*\bright_branch\b", txt, flags=re.IGNORECASE | re.DOTALL):
        mapping["right_branch"] = "Small Man"
    if re.search(r"Big Woman.*sheets\s+1-4", txt, flags=re.IGNORECASE):
        for i in (1, 2, 3, 4):
            mapping[f"sheet_id:{i}"] = "Big Woman"
    if re.search(r"Small Woman.*sheets\s+10-14", txt, flags=re.IGNORECASE):
        for i in (10, 11, 12, 13, 14):
            mapping[f"sheet_id:{i}"] = "Small Woman"
    if "flash:center_in" in txt:
        mapping["flash:center_in"] = "Spark"
    if "flash_bridge" in txt:
        mapping["flash_bridge"] = "Spark"
    if "gateway_peak" in txt:
        mapping["gateway_peak"] = "Boundary"
    if "mediator:synthetic_alpha" in txt:
        mapping["mediator:synthetic_alpha"] = "Mediator"
    return mapping


def main() -> int:
    ap = argparse.ArgumentParser(description="Render UNIVERSAL_GEOMETRY_COMPLETE_MAP.json as a readable graph.")
    ap.add_argument("--map", default="UNIVERSAL_GEOMETRY_COMPLETE_MAP.json")
    ap.add_argument("--archetype", default="ARCHETYPE_BRIDGE_MAP.md")
    ap.add_argument("--out", default="UNIVERSAL_GEOMETRY_COMPLETE_MAP.png")
    args = ap.parse_args()

    obj = json.loads(Path(args.map).read_text(encoding="utf-8"))
    nodes = obj.get("nodes") or []
    bridges = obj.get("bridges") or []
    arch = parse_archetype_bridge_map(Path(args.archetype))

    id_to_name = {n["id"]: n.get("name", n["id"]) for n in nodes if isinstance(n, dict) and "id" in n}
    g = nx.DiGraph()
    for n in nodes:
        if not isinstance(n, dict):
            continue
        nid = n.get("id")
        name = n.get("name", nid)
        if not nid or not name:
            continue
        g.add_node(name, role=n.get("role", ""), archetype=arch.get(name, ""))

    for b in bridges:
        if not isinstance(b, dict):
            continue
        s = b.get("source")
        t = b.get("target")
        if not s or not t:
            continue
        u = id_to_name.get(s, s)
        v = id_to_name.get(t, t)
        score = b.get("score")
        gap = b.get("gap")
        typ = b.get("type", "")
        status = b.get("status", "")
        try:
            score_f = float(score)
        except Exception:
            score_f = 0.0
        try:
            gap_f = float(gap)
        except Exception:
            gap_f = 0.0
        g.add_edge(u, v, score=score_f, gap=gap_f, type=typ, status=status)

    colors = []
    for n, d in g.nodes(data=True):
        a = (d.get("archetype") or "").strip()
        if a == "Big Woman":
            colors.append("#ffdfef")
        elif a == "Small Woman":
            colors.append("#ffd7c8")
        elif a == "Big Man":
            colors.append("#dfefff")
        elif a == "Small Man":
            colors.append("#cfe3ff")
        elif a == "Spark":
            colors.append("#fff2b2")
        elif a == "Mediator":
            colors.append("#d6ffd6")
        elif a == "Boundary":
            colors.append("#e6e6e6")
        else:
            colors.append("#f2f2f2")

    plt.figure(figsize=(16, 10), dpi=200)
    pos = nx.spring_layout(g, seed=0, k=1.0 / max(1, math.sqrt(g.number_of_nodes())))
    widths = []
    for _u, _v, d in g.edges(data=True):
        widths.append(0.5 + 3.0 * max(0.0, min(1.0, float(d.get("score", 0.0)))))

    nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=1400, edgecolors="#333", linewidths=0.7)
    nx.draw_networkx_edges(g, pos, width=widths, arrows=False, edge_color="#666", alpha=0.9)
    nx.draw_networkx_labels(g, pos, font_size=8)

    plt.title(f"UNIVERSAL_GEOMETRY_COMPLETE_MAP (nodes={g.number_of_nodes()}, bridges={g.number_of_edges()})")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(args.out, bbox_inches="tight")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

