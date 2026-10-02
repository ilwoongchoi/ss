import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def face_to_sphere(pt, r=1.0):
    x, y = pt
    lon = (x / 16.0) * 2.0 * math.pi - math.pi
    lat = (y / 16.0) * math.pi - (math.pi / 2.0)
    sx = r * math.cos(lat) * math.cos(lon)
    sy = r * math.cos(lat) * math.sin(lon)
    sz = r * math.sin(lat)
    return sx, sy, sz


def main():
    auto_path = Path("AUTO_ANCHORS.json")
    if not auto_path.exists():
        raise SystemExit("AUTO_ANCHORS.json not found. Run build_auto_anchors.py first.")

    anchors = json.loads(auto_path.read_text(encoding="utf-8"))
    mapped = []
    for label, pt in anchors.items():
        sx, sy, sz = face_to_sphere(pt, r=1.0)
        mapped.append((label, sx, sy, sz))

    # Write labels list
    out_csv = Path("AUTO_ANCHOR_LABELS.csv")
    if out_csv.exists():
        out_csv = Path("AUTO_ANCHOR_LABELS_v2.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        f.write("label,x_sphere,y_sphere,z_sphere\n")
        for label, sx, sy, sz in mapped:
            f.write(f"{label},{sx},{sy},{sz}\n")

    # Render points with labels
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    xs = [m[1] for m in mapped]
    ys = [m[2] for m in mapped]
    zs = [m[3] for m in mapped]
    ax.scatter(xs, ys, zs, s=10, c="#66ccff", alpha=0.7)
    for label, sx, sy, sz in mapped:
        ax.text(sx, sy, sz + 0.02, label, color="white", fontsize=6, ha="center")
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    plt.savefig("AUTO_ANCHOR_SPHERE_LABELED.png", dpi=240, bbox_inches="tight")
    plt.close(fig)

    print("Wrote AUTO_ANCHOR_LABELS.csv and AUTO_ANCHOR_SPHERE.png")


if __name__ == "__main__":
    raise SystemExit(main())
