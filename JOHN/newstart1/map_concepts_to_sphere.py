import csv
import hashlib
import json
import math
from pathlib import Path


def face_to_sphere(pt, r=1.0):
    x, y = pt
    lon = (x / 16.0) * 2.0 * math.pi - math.pi
    lat = (y / 16.0) * math.pi - (math.pi / 2.0)
    sx = r * math.cos(lat) * math.cos(lon)
    sy = r * math.cos(lat) * math.sin(lon)
    sz = r * math.sin(lat)
    return sx, sy, sz


def jitter_from_hash(key, scale=0.15):
    h = hashlib.md5(key.encode("utf-8")).hexdigest()
    a = int(h[:8], 16) / 0xFFFFFFFF
    b = int(h[8:16], 16) / 0xFFFFFFFF
    return (a - 0.5) * scale, (b - 0.5) * scale


def main():
    anchors_path = Path("AUTO_ANCHORS.json")
    if not anchors_path.exists():
        raise SystemExit("AUTO_ANCHORS.json not found")
    anchors = json.loads(anchors_path.read_text(encoding="utf-8"))

    # category → preferred anchor prefix (simple heuristic)
    category_anchor = {
        "physics": "COSMIC",
        "chemistry": "PLP",
        "biology": "VASOPRESSIN",
        "neurochem": "GABA_C",
        "systems": "IMPEDANCE",
    }

    concepts = []
    with open("CONCEPTS_LIST.csv", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            concepts.append((row["concept"], row["category"]))

    # pick anchor for category
    anchor_keys = list(anchors.keys())
    mapped = []
    for concept, cat in concepts:
        pref = category_anchor.get(cat, "")
        candidates = [k for k in anchor_keys if k.startswith(pref)]
        if not candidates:
            candidates = anchor_keys
        # pick deterministic anchor
        idx = int(hashlib.md5(concept.encode("utf-8")).hexdigest(), 16) % len(candidates)
        anchor = candidates[idx]
        ax, ay = anchors[anchor]
        jx, jy = jitter_from_hash(concept, scale=0.4)
        fx, fy = max(0.0, min(16.0, ax + jx)), max(0.0, min(16.0, ay + jy))
        sx, sy, sz = face_to_sphere((fx, fy), r=1.0)
        mapped.append((concept, cat, anchor, fx, fy, sx, sy, sz))

    with open("CONCEPTS_SPHERE_MAP.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["concept", "category", "anchor", "x_face", "y_face", "x_sphere", "y_sphere", "z_sphere"])
        for row in mapped:
            w.writerow(row)

    print(f"Wrote CONCEPTS_SPHERE_MAP.csv ({len(mapped)} concepts)")


if __name__ == "__main__":
    main()
