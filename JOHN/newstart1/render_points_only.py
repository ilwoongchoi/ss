"""
Render a 3D scatter of the face/sphere anchors only (no interpolated bridges, no surface mesh).
Uses SPHERE_POINT_LABELS.csv as source of anchors.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def main():
    csv_path = Path("SPHERE_POINT_LABELS.csv")
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    df = pd.read_csv(csv_path)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("black")

    # scatter points only
    ax.scatter(df["x_sphere"], df["y_sphere"], df["z_sphere"],
               c="cyan", s=14, alpha=0.8, edgecolors="none")

    # label a handful of anchors for orientation
    for lbl in ("PLP_ZERO", "FEMALE_SPARE_VASOPRESSIN", "TIME_SENSOR", "GABA-C V APEX"):
        rows = df[df["label"].str.lower() == lbl.lower()]
        if not rows.empty:
            r = rows.iloc[0]
            ax.text(r["x_sphere"], r["y_sphere"], r["z_sphere"], lbl,
                    color="yellow", fontsize=8)

    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    out = "POINTS_ONLY_SCATTER.png"
    plt.savefig(out, dpi=300, facecolor="black")
    plt.close()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
