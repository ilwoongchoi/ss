import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from geometry_package.final_manifold_renderer import get_final_manifold_registry


def _load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    reg = get_final_manifold_registry()
    patches = reg["patches"]
    intrinsic = reg["intrinsic_seams"]
    extended = reg["extended_seams"]
    barrier = reg["barrier"]

    face_locks = _load_json("FINAL_GEOMETRY_LOCK_REGISTRY.json")
    corridor = face_locks["face_corridor"]
    choke = face_locks["face_choke_band"]
    zeros = face_locks.get("plp_zero_points", {})

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Normalize patch coordinates into face-grid space for a single-frame overlay
    xs = [info["pos"][0] for info in patches.values()]
    ys = [info["pos"][1] for info in patches.values()]
    zs = [info["pos"][2] for info in patches.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    face_x_min, face_x_max = 0.0, 16.0
    face_y_min, face_y_max = 0.0, 16.0
    face_z_min, face_z_max = 0.5, 6.0

    def _scale(v, vmin, vmax, tmin, tmax):
        if vmax == vmin:
            return (tmin + tmax) * 0.5
        return tmin + (v - vmin) * (tmax - tmin) / (vmax - vmin)

    def _tpos(pos):
        return (
            _scale(pos[0], min_x, max_x, face_x_min, face_x_max),
            _scale(pos[1], min_y, max_y, face_y_min, face_y_max),
            _scale(pos[2], min_z, max_z, face_z_min, face_z_max),
        )

    # Render 13-patch manifold
    for pid, info in patches.items():
        x, y, z = _tpos(info["pos"])
        ax.scatter([x], [y], [z], s=120, c="#66ccff", edgecolors="white")
        ax.text(x, y, z + 0.2, f"{pid}:{info['name']}", fontsize=7, color="white")

    # Optional bridge strengths
    bridge_strengths = {}
    strengths_path = Path("BRIDGE_FIELD_STRENGTHS.csv")
    if strengths_path.exists():
        for line in strengths_path.read_text(encoding="utf-8").splitlines()[1:]:
            parts = line.split(",")
            if len(parts) < 3:
                continue
            a, b, mean_v = parts[0], parts[1], float(parts[2])
            bridge_strengths[(a, b)] = mean_v
            bridge_strengths[(b, a)] = mean_v

    def _edge_width(a, b, base):
        if not bridge_strengths:
            return base
        vals = list(bridge_strengths.values())
        vmin, vmax = min(vals), max(vals)
        v = bridge_strengths.get((a, b), vmin)
        if vmax == vmin:
            return base
        return base + 3.0 * (v - vmin) / (vmax - vmin)

    def draw_edge(a, b, color, lw):
        pa, pb = _tpos(patches[a]["pos"]), _tpos(patches[b]["pos"])
        # Densify for smoother manifold lines
        steps = 50
        xs = [pa[0] + (pb[0] - pa[0]) * i / (steps - 1) for i in range(steps)]
        ys = [pa[1] + (pb[1] - pa[1]) * i / (steps - 1) for i in range(steps)]
        zs = [pa[2] + (pb[2] - pa[2]) * i / (steps - 1) for i in range(steps)]
        ax.plot(xs, ys, zs, color=color, lw=lw)

    for a, b, _ in intrinsic:
        draw_edge(a, b, "#888888", _edge_width(a, b, 1.2))
    for a, b, _ in extended:
        draw_edge(a, b, "#ffaa00", _edge_width(a, b, 2.0))
    draw_edge(barrier[0], barrier[1], "#ff4444", 2.5)

    # Face locks on z=0 plane scaled to 16x16 (rendered as separate overlay)
    def scatter_points(points, color, label):
        if not points:
            return
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [0.0 for _ in points]
        ax.scatter(xs, ys, zs, s=40, c=color, label=label)

    # Corridor polyline
    cp = corridor.get("corridor_points", [])
    if cp:
        ax.plot([p[0] for p in cp], [p[1] for p in cp], [0.0 for _ in cp], color="#ff8800", lw=2)

    # Choke ridge
    ridge = choke.get("ridge", [])
    if ridge:
        ax.plot([p[0] for p in ridge], [p[1] for p in ridge], [0.0 for _ in ridge], color="#00ffaa", lw=3)

    scatter_points([choke.get("primary")], "#ff0000", "primary")
    scatter_points(choke.get("secondary", []), "#ffaa00", "secondary")
    scatter_points(choke.get("tertiary", []), "#ffee00", "tertiary")

    scatter_points([corridor.get("loopstart_terminal")], "#00aaff", "right_dock")
    scatter_points([corridor.get("mirror_terminal")], "#4444ff", "left_mirror")

    zpts = []
    if "plp_zero" in zeros:
        zpts.append(zeros["plp_zero"])
    if "female_spare_vasopressin" in zeros:
        zpts.append(zeros["female_spare_vasopressin"])
    scatter_points(zpts, "#ffffff", "zero_points")

    # Unmapped face peaks (bio residuals)
    peaks_path = Path("UNMAPPED_FACE_PEAKS.csv")
    if peaks_path.exists():
        xs, ys = [], []
        for line in peaks_path.read_text(encoding="utf-8").splitlines()[1:]:
            parts = line.split(",")
            if len(parts) < 2:
                continue
            xs.append(float(parts[0]))
            ys.append(float(parts[1]))
        zs = [0.0 for _ in xs]
        ax.scatter(xs, ys, zs, s=8, c="#cccccc", alpha=0.25, label="unmapped_face_peaks")

    ax.set_title("Full Geometry: 13-Patch + Face Locks")
    ax.set_box_aspect([1, 1, 0.5])
    ax.legend(loc="upper right", fontsize=7)

    out = Path("FULL_GEOMETRY_3D.png")
    plt.savefig(out, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
