import csv
from pathlib import Path

from geometry_package.final_manifold_renderer import get_final_manifold_registry
from geometry_package.regime1.shader2d_core import sample_core_fields_xy


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


def _bridge_field_score(a_xy, b_xy, samples=24):
    ax, ay = a_xy
    bx, by = b_xy
    vals = []
    for i in range(samples):
        t = i / (samples - 1) if samples > 1 else 0.0
        x = ax + (bx - ax) * t
        y = ay + (by - ay) * t
        core = sample_core_fields_xy(x, y, n_rows=16, n_cols=16)
        vals.append(float(core["w_gate"]) * float(core["kappa_eff"]))
    mean_v = sum(vals) / len(vals) if vals else 0.0
    return mean_v, min(vals) if vals else 0.0, max(vals) if vals else 0.0


def main():
    reg = get_final_manifold_registry()
    patches = reg["patches"]
    pos2d = _normalize_positions(patches)

    ids = list(patches.keys())
    out = Path("BRIDGE_FIELD_STRENGTHS.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target", "mean_strength", "min_strength", "max_strength"])
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a = ids[i]
                b = ids[j]
                mean_v, min_v, max_v = _bridge_field_score(pos2d[a][:2], pos2d[b][:2], samples=64)
                w.writerow([a, b, mean_v, min_v, max_v])

    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
