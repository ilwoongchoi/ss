from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def main() -> int:
    ap = argparse.ArgumentParser(description="Render FULL_GEOMETRY_*_MISSING_AND_GRAPH.json as a PNG.")
    ap.add_argument("--json", default="FULL_GEOMETRY_LOCKED_MISSING_AND_GRAPH.json")
    ap.add_argument("--out", default="FULL_GEOMETRY_LOCKED.png")
    args = ap.parse_args()

    obj = json.loads(Path(args.json).read_text(encoding="utf-8"))
    nodes = obj.get("nodes") or []
    edges = obj.get("edges") or []

    g = nx.DiGraph()
    for n in nodes:
        g.add_node(n)
    for e in edges:
        g.add_edge(e["u"], e["v"], label=e.get("label", ""), weight=e.get("weight"))

    plt.figure(figsize=(16, 10), dpi=180)
    # spring layout for small graphs
    pos = nx.spring_layout(g, seed=0, k=1.2 / max(1, g.number_of_nodes() ** 0.5))
    weights = []
    for _u, _v, d in g.edges(data=True):
        w = d.get("weight")
        try:
            weights.append(1.0 + 4.0 * float(w))
        except Exception:
            weights.append(1.0)

    nx.draw_networkx_nodes(g, pos, node_size=900, node_color="#f2f2f2", edgecolors="#444", linewidths=0.6)
    # Matplotlib can error on some arrow paths for certain layouts; render edges without arrows for robustness.
    nx.draw_networkx_edges(g, pos, width=weights, arrows=False, edge_color="#555", alpha=0.9)
    nx.draw_networkx_labels(g, pos, font_size=7)

    # edge labels are usually unreadable; keep off by default
    plt.axis("off")
    plt.tight_layout()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.out, bbox_inches="tight")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
