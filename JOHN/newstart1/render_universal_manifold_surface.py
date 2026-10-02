import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from geometry_package.final_manifold_renderer import get_final_manifold_registry


def _scale(v, vmin, vmax, tmin, tmax):
    if vmax == vmin:
        return (tmin + tmax) * 0.5
    return tmin + (v - vmin) * (tmax - tmin) / (vmax - vmin)


def _normalize_positions(patches):
    xs = [info["pos"][0] for info in patches.values()]
    ys = [info["pos"][1] for info in patches.values()]
    zs = [info["pos"][2] for info in patches.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    face_x_min, face_x_max = 0.0, 16.0
    face_y_min, face_y_max = 0.0, 16.0
    face_z_min, face_z_max = 0.5, 6.0

    def tpos(pos):
        return (
            _scale(pos[0], min_x, max_x, face_x_min, face_x_max),
            _scale(pos[1], min_y, max_y, face_y_min, face_y_max),
            _scale(pos[2], min_z, max_z, face_z_min, face_z_max),
        )

    return {pid: tpos(info["pos"]) for pid, info in patches.items()}


def main():
    field_path = Path("FACE_FIELD_MAP.csv")
    if not field_path.exists():
        raise SystemExit("FACE_FIELD_MAP.csv not found. Run compute_face_field_map.py first.")

    # Load field into grid
    xs, ys, zs = [], [], []
    with field_path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            xs.append(float(row["x"]))
            ys.append(float(row["y"]))
            zs.append(float(row["score"]))

    xs_u = sorted(set(xs))
    ys_u = sorted(set(ys))
    x_index = {v: i for i, v in enumerate(xs_u)}
    y_index = {v: i for i, v in enumerate(ys_u)}
    grid = np.zeros((len(ys_u), len(xs_u)))
    for x, y, z in zip(xs, ys, zs):
        grid[y_index[y], x_index[x]] = z

    X, Y = np.meshgrid(xs_u, ys_u)

    # Scale score to height for manifold
    z_min, z_max = float(np.min(grid)), float(np.max(grid))
    Z = 0.2 + 3.0 * (grid - z_min) / (z_max - z_min + 1e-9)

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Render surface manifold
    ax.plot_surface(X, Y, Z, cmap="magma", linewidth=0, antialiased=True, alpha=0.9)

    # Overlay 13-patch manifold edges in same coordinate frame
    reg = get_final_manifold_registry()
    patches = reg["patches"]
    intrinsic = reg["intrinsic_seams"]
    extended = reg["extended_seams"]
    barrier = reg["barrier"]
    pos2d = _normalize_positions(patches)

    def draw_edge(a, b, color, lw):
        pa, pb = pos2d[a], pos2d[b]
        steps = 50
        xs = [pa[0] + (pb[0] - pa[0]) * i / (steps - 1) for i in range(steps)]
        ys = [pa[1] + (pb[1] - pa[1]) * i / (steps - 1) for i in range(steps)]
        # sample surface height beneath edge for better embedding
        zs = []
        for x, y in zip(xs, ys):
            xi = min(range(len(xs_u)), key=lambda i: abs(xs_u[i] - x))
            yi = min(range(len(ys_u)), key=lambda i: abs(ys_u[i] - y))
            zs.append(Z[yi, xi] + 0.2)
        ax.plot(xs, ys, zs, color=color, lw=lw)

    for a, b, _ in intrinsic:
        draw_edge(a, b, "#bbbbbb", 1.2)
    for a, b, _ in extended:
        draw_edge(a, b, "#ffaa00", 2.0)
    draw_edge(barrier[0], barrier[1], "#ff4444", 2.5)

    ax.set_title("Universal Manifold Surface (Face Field + 13-Patch Overlay)")
    ax.set_box_aspect([1, 1, 0.5])
    ax.set_axis_off()

    out = Path("UNIVERSAL_MANIFOLD_SURFACE_3D.png")
    plt.savefig(out, dpi=240, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
