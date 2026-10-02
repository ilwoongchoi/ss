from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_DIR = ROOT / "analysis_results"
OUT_JSON = OUT_DIR / "pairwise_ownership_context.json"
OUT_MD = OUT_DIR / "pairwise_ownership_context.md"


CANONICAL_MOTIF_ORDER = [
    ("SM_SW", 4),
    ("BM_SW", 3),
    ("SM_BW", 3),
    ("BW_SW", 3),
    ("BM_BW", 2),
    ("BM_SM", 1),
]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pairwise_dirs = sorted([p for p in (ROOT / "out").glob("pairwise_topology*") if p.is_dir()])
    scanned = []
    feature_sets = {}
    for d in pairwise_dirs:
        s = d / "summary.json"
        if not s.exists():
            continue
        try:
            obj = json.loads(s.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        feats = obj.get("features", [])
        key = tuple(feats)
        feature_sets[key] = feature_sets.get(key, 0) + 1
        scanned.append(
            {
                "dir": str(d),
                "n_cells": obj.get("n_cells"),
                "features": feats,
                "h_dim_pairwise": obj.get("h_dim_pairwise"),
            }
        )

    # Ownership direct-inference needs 4 owner-aligned observed columns.
    has_owner_4col = any(len(x.get("features", [])) == 4 for x in scanned)
    report = {
        "canonical_motif_order": CANONICAL_MOTIF_ORDER,
        "scanned_pairwise_dirs": len(scanned),
        "feature_sets": [{"features": list(k), "count": v} for k, v in feature_sets.items()],
        "has_owner_4col_pairwise": has_owner_4col,
        "ownership_inference_status": (
            "direct_from_pairwise_possible" if has_owner_4col else "not_directly_possible_from_current_pairwise_outputs"
        ),
        "note": (
            "Current pairwise_topology outputs are mostly 7-feature geometry sweeps "
            "(amp_l2, ring1_frac, harm_ratio, broadband_frac, psi2, psi6, k_peak). "
            "They are valuable geometry diagnostics but not direct BM/BW/SM/SW owner columns."
        ),
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Pairwise Ownership Context",
        "",
        "## Canonical Motif Order",
        f"- `{CANONICAL_MOTIF_ORDER}`",
        "",
        "## Scan Result",
        f"- scanned_pairwise_dirs: `{len(scanned)}`",
        f"- has_owner_4col_pairwise: `{has_owner_4col}`",
        f"- ownership_inference_status: `{report['ownership_inference_status']}`",
        "",
        "## Feature Sets Found",
    ]
    for item in report["feature_sets"]:
        lines.append(f"- count=`{item['count']}` features=`{item['features']}`")
    lines += [
        "",
        "## Note",
        f"- {report['note']}",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

