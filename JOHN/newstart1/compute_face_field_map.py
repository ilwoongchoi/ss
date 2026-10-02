import csv
import math
from pathlib import Path

import importlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from geometry_package.regime1.shader2d_core import sample_core_fields_xy


def _mirror_x(x: float, center: float) -> float:
    return center + (center - x)


def _load_const():
    g = importlib.import_module("128GIRD_MBTI_PHYSICS")
    return g.CONST


def main():
    const = _load_const()
    n_rows = int(const.get("n_rows", 16))
    n_cols = int(const.get("n_cols", 16))
    center_x = n_cols / 2.0

    # Known anchors (from locked const + prior scans)
    right_d2 = (14.0, 6.0)
    left_d2 = (_mirror_x(right_d2[0], center_x), right_d2[1])
    left_cortisol = tuple(const.get("cortisol_center", [6.5, 5.0]))
    right_cortisol = (_mirror_x(left_cortisol[0], center_x), left_cortisol[1])
    ach_center = tuple(const.get("ach_center", [9.5, 5.0]))

    anchors = {
        "Right_D2": right_d2,
        "Left_D2": left_d2,
        "Right_Cortisol": right_cortisol,
        "Left_Cortisol": left_cortisol,
        "Right_ACh": ach_center,
    }

    step = 0.25
    rows = []
    for xi in range(int(n_cols / step) + 1):
        x = xi * step
        for yi in range(int(n_rows / step) + 1):
            y = yi * step
            core = sample_core_fields_xy(x, y, n_rows=n_rows, n_cols=n_cols)
            score = float(core["w_gate"]) * float(core["kappa_eff"])
            rows.append((x, y, score, core["kappa_eff"], core["w_gate"], core["in_sh_band"]))

    # Write full face field map
    out_csv = Path("FACE_FIELD_MAP.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "score", "kappa_eff", "w_gate", "in_sh_band"])
        for r in rows:
            w.writerow(r)

    # Label each point by nearest known anchor (partial mapping)
    out_labels = Path("FACE_NEUROCHEM_LABELS.csv")
    with out_labels.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "score", "nearest_anchor", "dist"])
        for x, y, score, *_ in rows:
            nearest = None
            best = None
            for name, (ax, ay) in anchors.items():
                d = math.hypot(x - ax, y - ay)
                if best is None or d < best:
                    best = d
                    nearest = name
            w.writerow([x, y, score, nearest, best])

    # Heatmap render (score)
    # Build grid
    grid = [[0.0 for _ in range(int(n_cols / step) + 1)] for __ in range(int(n_rows / step) + 1)]
    for x, y, score, *_ in rows:
        xi = int(round(x / step))
        yi = int(round(y / step))
        if 0 <= yi < len(grid) and 0 <= xi < len(grid[0]):
            grid[yi][xi] = score

    plt.figure(figsize=(8, 8))
    plt.imshow(grid, origin="lower", cmap="magma")
    plt.colorbar(label="score (w_gate * kappa_eff)")
    plt.title("FACE FIELD MAP (16x16, step=0.25)")
    plt.savefig("FACE_FIELD_MAP.png", dpi=220, bbox_inches="tight")
    plt.close()

    print("Wrote FACE_FIELD_MAP.csv, FACE_NEUROCHEM_LABELS.csv, FACE_FIELD_MAP.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
