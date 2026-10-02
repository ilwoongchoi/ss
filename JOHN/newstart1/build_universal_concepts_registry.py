import json
from pathlib import Path

from geometry_package import absolute_constants as const
from geometry_package.final_manifold_renderer import get_final_manifold_registry


def main():
    registry = {}

    # Core constants
    registry["constants"] = {
        "PHI": const.PHI,
        "ALPHA": const.ALPHA,
        "PI": const.PI,
        "BETTI_0": const.BETTI_0,
        "BETTI_5": const.BETTI_5,
        "BETTI_7": const.BETTI_7,
        "BETTI_11": const.BETTI_11,
        "SPARK_ANGLE_DEG": const.SPARK_ANGLE_DEG,
        "SPARK_LEAP_DIST": const.SPARK_LEAP_DIST,
        "LATTICE_3_32": const.LATTICE_3_32,
        "F_1_32": const.F_1_32,
        "F_3_32": const.F_3_32,
        "KAPPA_TDA_MIN": const.KAPPA_TDA_MIN,
        "KAPPA_TDA_MID": const.KAPPA_TDA_MID,
        "KAPPA_TDA_MAX": const.KAPPA_TDA_MAX,
        "MANIFOLD_CLOSURE": const.CALIBRATED_SKELETON.get("MANIFOLD_CLOSURE"),
    }

    # Universe nodes
    reg = get_final_manifold_registry()
    registry["universe_nodes"] = [{
        "id": pid,
        "name": info["name"],
        "type": info["type"]
    } for pid, info in reg["patches"].items()]

    # Archetype overlay
    overlay_path = Path("ARCHETYPE_GEOMETRY_OVERLAY.json")
    if overlay_path.exists():
        registry["archetype_overlay"] = json.loads(overlay_path.read_text(encoding="utf-8"))

    # Face locks / anchors
    lock_path = Path("FINAL_GEOMETRY_LOCK_REGISTRY.json")
    if lock_path.exists():
        registry["face_locks"] = json.loads(lock_path.read_text(encoding="utf-8"))

    auto_path = Path("AUTO_ANCHORS.json")
    if auto_path.exists():
        registry["auto_anchors"] = json.loads(auto_path.read_text(encoding="utf-8"))

    # Master lock reference (bio mapping)
    master_path = Path("Master_Lock_Reference.md")
    if master_path.exists():
        registry["master_lock_reference_path"] = str(master_path)

    out = Path("UNIVERSAL_CONCEPTS_REGISTRY.json")
    out.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
