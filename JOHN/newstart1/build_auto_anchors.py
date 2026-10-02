import csv
import json
from pathlib import Path


def main():
    anchors = {}

    # Pull locked anchors
    lock_path = Path("FINAL_GEOMETRY_LOCK_REGISTRY.json")
    if lock_path.exists():
        locks = json.loads(lock_path.read_text(encoding="utf-8"))
        zeros = locks.get("plp_zero_points", {})
        for k, v in zeros.items():
            anchors[k.upper()] = v
        corr = locks.get("face_corridor", {})
        if "loopstart_terminal" in corr:
            anchors["CORRIDOR_LOOPSTART"] = corr["loopstart_terminal"]
        if "mirror_terminal" in corr:
            anchors["CORRIDOR_MIRROR"] = corr["mirror_terminal"]
        choke = locks.get("face_choke_band", {})
        if "primary" in choke:
            anchors["CHOKE_PRIMARY"] = choke["primary"]
        for i, p in enumerate(choke.get("secondary", []), 1):
            anchors[f"CHOKE_SECONDARY_{i}"] = p
        for i, p in enumerate(choke.get("tertiary", []), 1):
            anchors[f"CHOKE_TERTIARY_{i}"] = p
        for i, p in enumerate(choke.get("ridge", []), 1):
            anchors[f"CHOKE_RIDGE_{i}"] = p

    # Add ROI peak anchors (auto)
    for roi_file in Path(".").glob("ROI_*_POINTS.csv"):
        label = roi_file.stem.replace("ROI_", "")
        best = None
        with roi_file.open(newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                try:
                    s = float(row["score"])
                    x = float(row["x"])
                    y = float(row["y"])
                except Exception:
                    continue
                if best is None or s > best[0]:
                    best = (s, x, y)
        if best:
            anchors[label] = [best[1], best[2]]

    out = Path("AUTO_ANCHORS.json")
    out.write_text(json.dumps(anchors, indent=2), encoding="utf-8")
    print(f"Wrote {out} with {len(anchors)} anchors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
