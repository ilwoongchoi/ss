from __future__ import annotations

import argparse
import json
from pathlib import Path

from geometry_package.universal_equation import aggregate_geometry_overlay_reports


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate CSV overlays and report geometry holes for 16-slot/10-edge minimum structure."
    )
    parser.add_argument(
        "--glob",
        dest="glob_pattern",
        default="observations-*.csv",
        help="CSV glob pattern relative to --base-dir",
    )
    parser.add_argument(
        "--base-dir",
        default=".",
        help="Base directory for glob search",
    )
    parser.add_argument(
        "--out-json",
        default="analysis_results/geometry_overlay_aggregate_report.json",
        help="Output JSON report path",
    )
    parser.add_argument("--time-col", default=None)
    parser.add_argument("--x-col", default=None)
    parser.add_argument("--y-col", default=None)
    parser.add_argument("--min-valid-rows", type=int, default=1)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail immediately when one CSV cannot be parsed",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    csv_paths = sorted(str(p) for p in base_dir.glob(args.glob_pattern) if p.is_file())
    if not csv_paths:
        raise SystemExit(f"No files matched: base_dir={base_dir} glob={args.glob_pattern}")

    report = aggregate_geometry_overlay_reports(
        csv_paths=csv_paths,
        time_col=args.time_col,
        x_col=args.x_col,
        y_col=args.y_col,
        min_valid_rows=args.min_valid_rows,
        strict=bool(args.strict),
    )

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"input_files={len(csv_paths)}")
    print(f"pass={report['pass']}")
    print(f"slots_observed={report['coverage']['slots_observed']}")
    print(f"missing_slots={len(report['holes']['missing_slots'])}")
    print(f"missing_edges_active={len(report['holes']['missing_edges_active'])}")
    print(f"slot_edge_pair_coverage_ratio={report['summary']['slot_edge_pair_coverage_ratio']:.6f}")
    print(f"report={out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

