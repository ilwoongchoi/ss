import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    map_path = Path("CONCEPTS_SPHERE_MAP.csv")
    if not map_path.exists():
        raise SystemExit("CONCEPTS_SPHERE_MAP.csv not found")

    xs, ys, zs, cats = [], [], [], []
    with map_path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            xs.append(float(row["x_sphere"]))
            ys.append(float(row["y_sphere"]))
            zs.append(float(row["z_sphere"]))
            cats.append(row["category"])

    color_map = {
        "physics": "#66ccff",
        "chemistry": "#ffcc66",
        "biology": "#66ff99",
        "neurochem": "#ff6699",
        "systems": "#ccccff",
    }
    colors = [color_map.get(c, "#aaaaaa") for c in cats]

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(xs, ys, zs, s=6, c=colors, alpha=0.6)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    plt.savefig("CONCEPTS_SPHERE_3D.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Wrote CONCEPTS_SPHERE_3D.png")


if __name__ == "__main__":
    main()
