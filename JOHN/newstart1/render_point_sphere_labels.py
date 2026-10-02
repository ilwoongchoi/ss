import csv
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


def load_points():
    points = []
    # locked points
    lock_path = Path("FINAL_GEOMETRY_LOCK_REGISTRY.json")
    if lock_path.exists():
        locks = json.loads(lock_path.read_text(encoding="utf-8"))
        corr = locks.get("face_corridor", {})
        choke = locks.get("face_choke_band", {})
        zeros = locks.get("plp_zero_points", {})

        def add(label, pt):
            if pt:
                points.append((label, float(pt[0]), float(pt[1])))

        add("corridor_loopstart", corr.get("loopstart_terminal"))
        add("corridor_mirror", corr.get("mirror_terminal"))
        add("choke_primary", choke.get("primary"))
        for i, p in enumerate(choke.get("secondary", []), 1):
            add(f"choke_secondary_{i}", p)
        for i, p in enumerate(choke.get("tertiary", []), 1):
            add(f"choke_tertiary_{i}", p)
        for i, p in enumerate(choke.get("ridge", []), 1):
            add(f"choke_ridge_{i}", p)
        if "plp_zero" in zeros:
            add("plp_zero", zeros["plp_zero"])
        if "female_spare_vasopressin" in zeros:
            add("vasopressin_spare", zeros["female_spare_vasopressin"])

    # unmapped peaks
    peaks_path = Path("UNMAPPED_FACE_PEAKS.csv")
    if peaks_path.exists():
        with peaks_path.open(newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for i, row in enumerate(r, 1):
                points.append((f"peak_{i}", float(row["x"]), float(row["y"])))

    return points


def main():
    points = load_points()
    if not points:
        raise SystemExit("No points found.")

    # Map to sphere
    mapped = []
    for label, x, y in points:
        sx, sy, sz = face_to_sphere((x, y), r=1.0)
        mapped.append((label, x, y, sx, sy, sz))

    # Write full label list
    out_csv = Path("SPHERE_POINT_LABELS.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["label", "x_face", "y_face", "x_sphere", "y_sphere", "z_sphere"])
        for row in mapped:
            w.writerow(row)

    # Render sphere points (no text to avoid clutter)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    xs = [m[3] for m in mapped]
    ys = [m[4] for m in mapped]
    zs = [m[5] for m in mapped]
    ax.scatter(xs, ys, zs, s=6, c="#cccccc", alpha=0.6)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    plt.savefig("SPHERE_POINT_CLOUD.png", dpi=240, bbox_inches="tight")
    plt.close(fig)

    print("Wrote SPHERE_POINT_LABELS.csv and SPHERE_POINT_CLOUD.png")


if __name__ == "__main__":
    raise SystemExit(main())
