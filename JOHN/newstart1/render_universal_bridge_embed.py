from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def main() -> int:
    ap = argparse.ArgumentParser(description="Render UNIVERSAL_BRIDGE_ALL_EMBED.json as a 3D scatter plot.")
    ap.add_argument("--embed", default="UNIVERSAL_BRIDGE_ALL_EMBED.json")
    ap.add_argument("--out", default="UNIVERSAL_BRIDGE_ALL_3D.png")
    args = ap.parse_args()

    obj = json.loads(Path(args.embed).read_text(encoding="utf-8"))
    nodes = obj.get("nodes", [])
    xs = [n["x"] for n in nodes]
    ys = [n["y"] for n in nodes]
    zs = [n["z"] for n in nodes]
    labels = [n["node"] for n in nodes]

    fig = plt.figure(figsize=(10, 8), dpi=180)
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(xs, ys, zs, s=40, c="#444", alpha=0.9)
    for x, y, z, lab in zip(xs, ys, zs, labels):
        ax.text(x, y, z, lab, fontsize=7)
    ax.set_title("UNIVERSAL_BRIDGE_ALL — 3D embedding (MDS)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.tight_layout()
    plt.savefig(args.out, bbox_inches="tight")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

