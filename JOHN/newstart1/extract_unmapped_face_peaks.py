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

    locks = json.loads(lock_path.read_text(encoding="utf-8"))
    locked_points = []

    # corridor terminals
    corr = locks.get("face_corridor", {})
    for key in ("loopstart_terminal", "mirror_terminal"):
        pt = corr.get(key)
        if pt:
            locked_points.append(tuple(pt))

    # choke ridge + primary/secondary/tertiary
    choke = locks.get("face_choke_band", {})
    if choke.get("primary"):
        locked_points.append(tuple(choke["primary"]))
    for arr in choke.get("secondary", []):
        locked_points.append(tuple(arr))
    for arr in choke.get("tertiary", []):
        locked_points.append(tuple(arr))
    for arr in choke.get("ridge", []):
        locked_points.append(tuple(arr))

    # plp zeros
    zeros = locks.get("plp_zero_points", {})
    for k in ("plp_zero", "female_spare_vasopressin"):
        if k in zeros:
            locked_points.append(tuple(zeros[k]))

    # Load field map
    rows = []
    with field_path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row["x"]), float(row["y"]), float(row["score"])))

    # Filter: score threshold, and far from locked points
    score_threshold = 0.02
    min_dist = 0.0  # no exclusion; keep all
    candidates = []
    for x, y, s in rows:
        if s < score_threshold:
            continue
        if locked_points:
            if min(_dist((x, y), p) for p in locked_points) < min_dist:
                continue
        candidates.append((x, y, s))

    # Keep all candidates by score (no cap)
    candidates.sort(key=lambda t: t[2], reverse=True)
    top = candidates

    out_csv = Path("UNMAPPED_FACE_PEAKS.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "score"])
        for x, y, s in top:
            w.writerow([x, y, s])

    out_json = Path("UNMAPPED_FACE_PEAKS.json")
    out_json.write_text(json.dumps({
        "score_threshold": score_threshold,
        "min_dist_from_locked": min_dist,
        "count": len(top),
        "points": top
    }, indent=2), encoding="utf-8")

    print(f"Wrote {out_csv} and {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
