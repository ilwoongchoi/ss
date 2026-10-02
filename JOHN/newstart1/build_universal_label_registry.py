import json
from pathlib import Path

from geometry_package.final_manifold_renderer import get_final_manifold_registry


def main():
    registry = {}

    # Universe nodes (13-patch + mediator)
    reg = get_final_manifold_registry()
    nodes = []
    for pid, info in reg["patches"].items():
        nodes.append({
            "id": pid,
            "name": info["name"],
            "type": info["type"],
        })
    registry["universe_nodes"] = nodes

    # Archetype overlay
    overlay_path = Path("ARCHETYPE_GEOMETRY_OVERLAY.json")
    if overlay_path.exists():
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        registry["archetype_overlay"] = overlay

    # Face anchors
    lock_path = Path("FINAL_GEOMETRY_LOCK_REGISTRY.json")
    if lock_path.exists():
        registry["face_locks"] = json.loads(lock_path.read_text(encoding="utf-8"))

    # Auto anchors
    auto_path = Path("AUTO_ANCHORS.json")
    if auto_path.exists():
        registry["auto_anchors"] = json.loads(auto_path.read_text(encoding="utf-8"))

    out = Path("UNIVERSAL_LABEL_REGISTRY.json")
    out.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
