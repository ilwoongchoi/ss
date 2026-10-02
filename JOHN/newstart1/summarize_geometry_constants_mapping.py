from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mapping-csv", default="GEOMETRY_PACKAGE_CONSTANTS_TO_LHD.csv")
    ap.add_argument("--keep-json", default="GEOMETRY_PACKAGE_CONSTANTS_TO_LHD_KEEP_DISCARD.json")
    ap.add_argument("--out", default="GEOMETRY_PACKAGE_CONSTANTS_MAPPING_REPORT.md")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.mapping_csv, "r", encoding="utf-8")))
    kd = json.load(open(args.keep_json, "r", encoding="utf-8"))

    keep = set(kd.get("keep", []))
    discard = kd.get("discard", [])
    dupes = kd.get("dupes", {})

    def pick(names: list[str]) -> list[dict[str, str]]:
        by = {r["Constant"]: r for r in rows}
        return [by[n] for n in names if n in by]

    # high-signal constants to show first (if present)
    headline = [
        "W7_EXACT",
        "H2_W7",
        "KAPPA_1_32 (觀)",
        "KAPPA_3_32",
        "GATE_5_32",
        "SPARK_ANGLE_DEG",
        "DISCRETE_CLOSURE",
        "REALITY_TENSION",
        "CHIRALITY_CONSTANT",
        "LUNAR_CYCLE",
    ]

    md = []
    md.append("# Geometry Package Constants — LHD Mapping Summary")
    md.append("")
    md.append(f"- Mapping input: `{Path(args.mapping_csv).name}`")
    md.append(f"- Keep/discard: `{Path(args.keep_json).name}`")
    md.append(f"- Keep count: `{len(keep)}`")
    md.append(f"- Discard count: `{len(discard)}`")
    md.append(f"- Duplicate numeric-value groups: `{len(dupes)}`")
    md.append("")
    md.append("## Headline constants")
    md.append("")
    md.append("| Constant | Value_raw | Status | Mapping | DupGroup |")
    md.append("|---|---:|---|---|---|")
    for r in pick(headline):
        md.append(
            "| "
            + " | ".join(
                [
                    r["Constant"],
                    r["Value_raw"],
                    r["Status"],
                    r["Mapping"],
                    r.get("DupGroup", ""),
                ]
            )
            + " |"
        )
    md.append("")

    md.append("## Discarded constants (this LHD run)")
    md.append("")
    md.append("Discard here means: not numeric or not mapped to the chosen LHD edge observables (phase/stability/bias/score) in this run.")
    md.append("")
    md.append("| Constant | Reason |")
    md.append("|---|---|")
    for d in discard:
        md.append(f"| {d.get('Constant','')} | {d.get('Reason','')} |")
    md.append("")

    if dupes:
        md.append("## Duplicate numeric values")
        md.append("")
        md.append("If two names share the same numeric value, keep the *canonical* name and treat the others as aliases unless the descriptions differ materially.")
        md.append("")
        for v, names in dupes.items():
            md.append(f"- `{v}`: {', '.join(names)}")
        md.append("")

    Path(args.out).write_text("\n".join(md), encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

