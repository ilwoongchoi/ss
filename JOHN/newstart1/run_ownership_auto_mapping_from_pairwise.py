from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Iterable

import pandas as pd


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_DIR = ROOT / "analysis_results"
OUT_JSON = OUT_DIR / "ownership_auto_mapping_from_pairwise.json"
OUT_MD = OUT_DIR / "ownership_auto_mapping_from_pairwise.md"

# Canonical motif order locked from interaction_motifs.py
MOTIF_ORDER = ["SM_SW", "BM_SW", "SM_BW", "BW_SW", "BM_BW", "BM_SM"]

# Preferred columns when more than 4 are available.
PREFERRED_COLS = [
    "amp_l2",
    "ring1_frac",
    "harm_ratio",
    "broadband_frac",
    "psi2",
    "psi6",
    "k_peak",
]


def numeric_columns(df: pd.DataFrame) -> list[str]:
    cols: list[str] = []
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            cols.append(c)
    return cols


def pick_four_columns(cols: list[str]) -> list[str]:
    chosen: list[str] = []
    for p in PREFERRED_COLS:
        if p in cols:
            chosen.append(p)
        if len(chosen) == 4:
            return chosen
    if len(cols) >= 4:
        return cols[:4]
    return cols


def pairwise_abs_corr(df: pd.DataFrame, cols: Iterable[str]) -> list[dict[str, object]]:
    cols = list(cols)
    corr = df[cols].corr(method="pearson").abs()
    rows: list[dict[str, object]] = []
    for a, b in combinations(cols, 2):
        v = float(corr.loc[a, b])
        rows.append({"pair": [a, b], "abs_corr": v})
    rows.sort(key=lambda x: x["abs_corr"], reverse=True)
    return rows


def assign_motif(pairs_sorted: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for i, row in enumerate(pairs_sorted):
        if i >= len(MOTIF_ORDER):
            break
        out.append(
            {
                "motif_edge": MOTIF_ORDER[i],
                "observed_pair": row["pair"],
                "score_abs_corr": row["abs_corr"],
            }
        )
    return out


def resolve_feature_cloud(summary_path: Path, csv_field: str) -> Path | None:
    p = Path(csv_field)
    if p.is_absolute() and p.exists():
        return p
    # Try relative to summary directory first.
    p1 = summary_path.parent / p
    if p1.exists():
        return p1
    # Try repo root.
    p2 = ROOT / p
    if p2.exists():
        return p2
    # Common location for quick runs.
    p3 = ROOT / "out" / "geometry_sweep_cpu_quick" / "feature_cloud.csv"
    if p3.exists():
        return p3
    return None


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pairwise_dirs = sorted([p for p in (ROOT / "out").glob("pairwise_topology*") if p.is_dir()])
    reports: list[dict[str, object]] = []

    for d in pairwise_dirs:
        s = d / "summary.json"
        if not s.exists():
            continue
        try:
            summary = json.loads(s.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            reports.append({"dir": str(d), "status": "summary_parse_failed"})
            continue

        csv_field = str(summary.get("csv", "")).strip()
        if not csv_field:
            reports.append({"dir": str(d), "status": "csv_field_missing"})
            continue

        csv_path = resolve_feature_cloud(s, csv_field)
        if csv_path is None:
            reports.append({"dir": str(d), "status": "feature_cloud_not_found", "csv_field": csv_field})
            continue

        try:
            df = pd.read_csv(csv_path)
        except Exception:
            reports.append({"dir": str(d), "status": "feature_cloud_parse_failed", "csv_path": str(csv_path)})
            continue

        cols = numeric_columns(df)
        if len(cols) < 4:
            reports.append({"dir": str(d), "status": "not_enough_numeric_cols", "csv_path": str(csv_path), "cols": cols})
            continue

        used = pick_four_columns(cols)
        pairs = pairwise_abs_corr(df, used)
        assigned = assign_motif(pairs)
        reports.append(
            {
                "dir": str(d),
                "status": "ok",
                "csv_path": str(csv_path),
                "used_columns": used,
                "pairs_sorted": pairs,
                "ownership_assignment": assigned,
            }
        )

    payload = {"canonical_motif_order": MOTIF_ORDER, "reports": reports}
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Ownership Auto Mapping From Pairwise",
        "",
        f"- canonical_motif_order: `{MOTIF_ORDER}`",
        "",
    ]
    for r in reports:
        lines.append(f"## {r['dir']}")
        lines.append("")
        lines.append(f"- status: `{r['status']}`")
        if r["status"] != "ok":
            if "csv_field" in r:
                lines.append(f"- csv_field: `{r['csv_field']}`")
            if "csv_path" in r:
                lines.append(f"- csv_path: `{r['csv_path']}`")
            if "cols" in r:
                lines.append(f"- cols: `{r['cols']}`")
            lines.append("")
            continue
        lines.append(f"- csv_path: `{r['csv_path']}`")
        lines.append(f"- used_columns: `{r['used_columns']}`")
        lines.append("- ownership_assignment:")
        for a in r["ownership_assignment"]:
            lines.append(
                f"  - `{a['motif_edge']}` <= `{a['observed_pair']}` (abs_corr=`{a['score_abs_corr']}`)"
            )
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

