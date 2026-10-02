import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    corridor = _load_json("FACE_CORRIDOR_LOCK.json")
    choke = _load_json("FACE_CHOKE_BAND_LOCK.json")
    zeros = _load_json("FINAL_GEOMETRY_LOCK_REGISTRY.json").get("plp_zero_points", {})

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Base face plane (16x16) at z=0
    ax.plot([0, 16, 16, 0, 0], [0, 0, 16, 16, 0], [0, 0, 0, 0, 0], color="#888888", lw=1)

    # Corridor points
    cp = corridor.get("corridor_points", [])
    if cp:
        xs = [p[0] for p in cp]
        ys = [p[1] for p in cp]
        zs = [0.0 for _ in cp]
        ax.plot(xs, ys, zs, color="#ff8800", lw=2, label="corridor")

    # Choke ridge
    ridge = choke.get("ridge", [])
    if ridge:
        xs = [p[0] for p in ridge]
        ys = [p[1] for p in ridge]
        zs = [0.0 for _ in ridge]
        ax.plot(xs, ys, zs, color="#00ffaa", lw=3, label="left_choke_ridge")

    # Primary/secondary/tertiary points
    def _scatter(points, color, label):
        if not points:
            return
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [0.0 for _ in points]
        ax.scatter(xs, ys, zs, s=50, c=color, label=label)

    _scatter([choke.get("primary")], "#ff0000", "primary")
    _scatter(choke.get("secondary", []), "#ffaa00", "secondary")
    _scatter(choke.get("tertiary", []), "#ffee00", "tertiary")

    # Dock points
    _scatter([corridor.get("loopstart_terminal")], "#00aaff", "right_dock")
    _scatter([corridor.get("mirror_terminal")], "#4444ff", "left_mirror")

    # Zero points
    if zeros:
        zpts = []
        if "plp_zero" in zeros:
            zpts.append(zeros["plp_zero"])
        if "female_spare_vasopressin" in zeros:
            zpts.append(zeros["female_spare_vasopressin"])
        _scatter(zpts, "#ffffff", "zero_points")

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_zlim(0, 1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title("Face Lock Geometry (3D overlay, z=0 plane)")

    out = Path("FACE_LOCKS_3D.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
