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
    reg_path = Path("UNIVERSAL_LABEL_REGISTRY.json")
    if not reg_path.exists():
        raise SystemExit("UNIVERSAL_LABEL_REGISTRY.json not found")
    reg = json.loads(reg_path.read_text(encoding="utf-8"))

    # Render all anchors on a sphere
    anchors = {}
    for k, v in reg.get("auto_anchors", {}).items():
        anchors[k] = v
    for k, v in reg.get("face_locks", {}).get("plp_zero_points", {}).items():
        anchors[k] = v

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Sphere surface (visible shape)
    import numpy as np
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 30)
    U, V = np.meshgrid(u, v)
    X = np.cos(U) * np.sin(V)
    Y = np.sin(U) * np.sin(V)
    Z = np.cos(V)
    ax.plot_wireframe(X, Y, Z, color="#444466", alpha=0.3, linewidth=0.4, rstride=2, cstride=2)

    # Point cloud with numeric labels to reduce overlap (larger font)
    label_list = []
    for idx, (label, pt) in enumerate(sorted(anchors.items()), 1):
        sx, sy, sz = face_to_sphere(pt, r=1.02)
        ax.scatter([sx], [sy], [sz], s=40, c="#66ccff", alpha=0.95)
        ax.text(sx, sy, sz + 0.04, str(idx), color="white", fontsize=9, ha="center")
        label_list.append((idx, label, pt[0], pt[1], sx, sy, sz))

    # Write label list for lookup
    out_list = Path("UNIVERSAL_LABELS_LIST.csv")
    with out_list.open("w", newline="", encoding="utf-8") as f:
        f.write("id,label,x_face,y_face,x_sphere,y_sphere,z_sphere\n")
        for row in label_list:
            f.write(",".join(map(str, row)) + "\n")

    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    plt.savefig("UNIVERSAL_LABELS_3D.png", dpi=320, bbox_inches="tight")
    plt.close(fig)
    print("Wrote UNIVERSAL_LABELS_3D.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
