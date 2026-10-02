from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass(frozen=True)
class Node:
    name: str
    feats: np.ndarray  # fixed-length feature vector


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_archetype_bridge_map(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    txt = path.read_text(encoding="utf-8", errors="replace")
    mapping: dict[str, str] = {}
    if re.search(r"\bBig Man\b.*\bcore_center\b", txt, flags=re.IGNORECASE | re.DOTALL):
        mapping["core_center"] = "Big Man"
    if re.search(r"\bSmall Man\b.*\bright_branch\b", txt, flags=re.IGNORECASE | re.DOTALL):
        mapping["right_branch"] = "Small Man"
    if re.search(r"Big Woman.*sheets\\s+1-4", txt, flags=re.IGNORECASE):
        for i in (1, 2, 3, 4):
            mapping[f"sheet_id:{i}"] = "Big Woman"
    if re.search(r"Small Woman.*sheets\\s+10-14", txt, flags=re.IGNORECASE):
        for i in (10, 11, 12, 13, 14):
            mapping[f"sheet_id:{i}"] = "Small Woman"
    if "flash:center_in" in txt:
        mapping["flash:center_in"] = "Spark"
    if "flash_bridge" in txt:
        mapping["flash_bridge"] = "Spark"
    if "gateway_peak" in txt:
        mapping["gateway_peak"] = "Boundary"
    if "mediator:synthetic_alpha" in txt:
        mapping["mediator:synthetic_alpha"] = "Mediator"
    return mapping


def build_node_list(bundle_dir: Path) -> list[str]:
    patch_table = bundle_dir / "MANIFOLD_PATCH_TABLE.csv"
    nodes: list[str] = []
    if patch_table.exists():
        for r in read_csv(patch_table):
            name = (r.get("patch_name") or "").strip()
            if name:
                nodes.append(name)
    # engine pair always present in your model
    for extra in ("core_center", "right_branch"):
        if extra not in nodes:
            nodes.append(extra)
    return sorted(dict.fromkeys(nodes))


def node_feature_vector(
    *,
    name: str,
    patch_row: dict[str, str] | None,
    archetype_label: str | None,
) -> np.ndarray:
    """
    Single fixed feature schema for ALL nodes. No external references required.

    Features (all numeric):
    - type one-hot-ish: [is_sheet, is_flash, is_gateway, is_mediator, is_engine]
    - sheet index bucket (0..1 normalized)
    - component: internal_main (0/1), internal_isolated(0/1)
    - barrier flag (0/1)
    - seam_count normalized
    - archetype code (BigWoman/SmallWoman/BigMan/SmallMan/Spark/Boundary/Mediator/Other) as 0..1 bins
    """
    n = name
    is_sheet = 1.0 if n.startswith("sheet_id:") else 0.0
    is_flash = 1.0 if n.startswith("flash:") or n == "flash_bridge" else 0.0
    is_gateway = 1.0 if n == "gateway_peak" else 0.0
    is_mediator = 1.0 if n.startswith("mediator:") else 0.0
    is_engine = 1.0 if n in ("core_center", "right_branch") else 0.0

    sheet_idx = 0.0
    m = re.match(r"sheet_id:(\\d+)$", n)
    if m:
        sheet_idx = float(int(m.group(1)))
    sheet_norm = min(1.0, sheet_idx / 14.0) if sheet_idx else 0.0

    internal_comp = (patch_row or {}).get("internal_component", "")
    internal_main = 1.0 if internal_comp == "Main" else 0.0
    internal_iso = 1.0 if internal_comp == "Isolated" else 0.0
    barrier = 1.0 if "True barrier" in ((patch_row or {}).get("barrier_status", "") or "") else 0.0

    seam_count = 0.0
    try:
        seam_count = float((patch_row or {}).get("seam_count") or 0.0)
    except ValueError:
        seam_count = 0.0
    seam_norm = min(1.0, seam_count / 6.0)

    arch = (archetype_label or "Other").strip()
    arch_bins = {
        "Big Woman": 0.10,
        "Small Woman": 0.25,
        "Big Man": 0.45,
        "Small Man": 0.55,
        "Spark": 0.70,
        "Boundary": 0.80,
        "Mediator": 0.90,
        "Other": 0.00,
    }
    arch_code = arch_bins.get(arch, 0.0)

    return np.array(
        [
            is_sheet,
            is_flash,
            is_gateway,
            is_mediator,
            is_engine,
            sheet_norm,
            internal_main,
            internal_iso,
            barrier,
            seam_norm,
            arch_code,
        ],
        dtype=np.float32,
    )


def bridge_strength(u: Node, v: Node) -> tuple[float, float, float]:
    """
    Canonical (gap, contact, drift) function.

    - gap: weighted L2 in feature space (geometry distance proxy)
    - contact: 1/(1+gap^2)
    - drift: penalty from barrier mismatch + archetype mismatch
    """
    w = np.array([1, 1, 1, 1, 1, 0.8, 1, 1, 2.0, 0.6, 0.7], dtype=np.float32)
    d = (u.feats - v.feats) * w
    gap = float(np.linalg.norm(d))

    contact = 1.0 / (1.0 + gap * gap)

    # drift: barriers amplify drift; different archetype codes add drift
    barrier_pen = 1.0 + 3.0 * max(float(u.feats[8]), float(v.feats[8]))
    arch_pen = 1.0 + 2.0 * abs(float(u.feats[10]) - float(v.feats[10]))
    drift = float((barrier_pen * arch_pen) / 5.0)

    # contact drift-adjusted (store drift separately; keep raw contact here)
    return gap, contact, drift


def mds_embed(dist: np.ndarray, dim: int = 3) -> np.ndarray:
    """
    Classical MDS embedding from a distance matrix.
    """
    n = dist.shape[0]
    D2 = dist ** 2
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ D2 @ J
    # eigendecompose
    vals, vecs = np.linalg.eigh(B)
    idx = np.argsort(vals)[::-1]
    vals = vals[idx]
    vecs = vecs[:, idx]
    vals = np.maximum(vals[:dim], 0.0)
    X = vecs[:, :dim] * np.sqrt(vals[None, :])
    return X.astype(np.float32)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Compute full universal bridge matrix (gap/contact/drift) over all nodes.")
    ap.add_argument("--bundle-dir", default="_UNIVERSAL_GEOMETRY_FINAL_BUNDLE")
    ap.add_argument("--archetype-map", default="ARCHETYPE_BRIDGE_MAP.md")
    ap.add_argument("--out-prefix", default="UNIVERSAL_BRIDGE_ALL")
    args = ap.parse_args(argv)

    bundle = Path(args.bundle_dir)
    nodes = build_node_list(bundle)
    patch_rows = {r["patch_name"]: r for r in read_csv(bundle / "MANIFOLD_PATCH_TABLE.csv")} if (bundle / "MANIFOLD_PATCH_TABLE.csv").exists() else {}
    arch = parse_archetype_bridge_map(Path(args.archetype_map))

    node_objs: list[Node] = []
    for n in nodes:
        feats = node_feature_vector(name=n, patch_row=patch_rows.get(n), archetype_label=arch.get(n))
        node_objs.append(Node(name=n, feats=feats))

    n = len(node_objs)
    dist = np.zeros((n, n), dtype=np.float32)
    out_rows: list[dict[str, Any]] = []
    for i in range(n):
        for j in range(i + 1, n):
            gap, contact, drift = bridge_strength(node_objs[i], node_objs[j])
            dist[i, j] = dist[j, i] = gap
            out_rows.append(
                {
                    "u": node_objs[i].name,
                    "v": node_objs[j].name,
                    "gap_dist": gap,
                    "contact_score": contact,
                    "drift_factor_used": drift,
                }
            )

    out_csv = Path(f"{args.out_prefix}.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["u", "v", "gap_dist", "contact_score", "drift_factor_used"])
        w.writeheader()
        w.writerows(out_rows)

    # embedding
    X = mds_embed(dist, dim=3)
    out_embed = Path(f"{args.out_prefix}_EMBED.json")
    out_embed.write_text(
        json.dumps(
            {
                "nodes": [{"node": node_objs[i].name, "x": float(X[i, 0]), "y": float(X[i, 1]), "z": float(X[i, 2])} for i in range(n)],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(str(out_csv))
    print(str(out_embed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
