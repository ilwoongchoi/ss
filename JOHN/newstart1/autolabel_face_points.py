import csv
import json
import math
from pathlib import Path


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def main():
    field_path = Path("FACE_FIELD_MAP.csv")
    lock_path = Path("FINAL_GEOMETRY_LOCK_REGISTRY.json")
    if not field_path.exists() or not lock_path.exists():
        raise SystemExit("Missing FACE_FIELD_MAP.csv or FINAL_GEOMETRY_LOCK_REGISTRY.json")

    # Use fixed anchor points only (no ROI overlap, nearest-anchor labeling)
    anchors = {}
    auto_path = Path("AUTO_ANCHORS.json")
    if auto_path.exists():
        anchors = json.loads(auto_path.read_text(encoding="utf-8"))
    else:
        locks = json.loads(lock_path.read_text(encoding="utf-8"))
        zeros = locks.get("plp_zero_points", {})
        if "plp_zero" in zeros:
            anchors["PLP_ZERO"] = tuple(zeros["plp_zero"])
        if "female_spare_vasopressin" in zeros:
            anchors["VASOPRESSIN_SPARE"] = tuple(zeros["female_spare_vasopressin"])
        if "time_sensor" in zeros:
            anchors["TIME_SENSOR"] = tuple(zeros["time_sensor"])

    if not anchors:
        raise SystemExit("No anchors available for autolabel.")

    # Label every point by nearest anchor in X only (user rule: x-coordinate separation)
    out_csv = Path("FACE_FIELD_AUTOLABEL.csv")
    if out_csv.exists():
        out_csv = Path("FACE_FIELD_AUTOLABEL_v2.csv")
    with field_path.open(newline="", encoding="utf-8") as f_in, out_csv.open("w", newline="", encoding="utf-8") as f_out:
        r = csv.DictReader(f_in)
        w = csv.writer(f_out)
        w.writerow(["x", "y", "score", "label", "dist"])
        for row in r:
            x = float(row["x"])
            y = float(row["y"])
            score = float(row["score"])
            best_label = None
            best_dist = None
            for lbl, pt in anchors.items():
                d = abs(x - float(pt[0]))
                if best_dist is None or d < best_dist:
                    best_dist = d
                    best_label = lbl
            w.writerow([x, y, score, best_label, best_dist])

    print(f"Wrote {out_csv}")


if __name__ == "__main__":
    raise SystemExit(main())
