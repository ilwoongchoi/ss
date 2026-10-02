from __future__ import annotations

import json
from pathlib import Path

from geometry_package.trilateral_compatibility_15 import compatibility_report


OUT_DIR = Path(r"d:\Users\user\Documents\newstart\analysis_results")
OUT_JSON = OUT_DIR / "trilateral_compatibility_15.json"
OUT_MD = OUT_DIR / "trilateral_compatibility_15.md"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = compatibility_report()
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Trilateral Compatibility (15-Slot / 15-Edge / Scale Ladder)",
        "",
        f"- all_checks_pass: `{report['all_checks_pass']}`",
        "",
        "## Checks",
    ]
    for k, v in report["checks"].items():
        lines.append(f"- {k}: `{v}`")
    lines += ["", "## Subject -> Particle", ""]
    for k, v in report["subject_to_particle"].items():
        lines.append(f"- `{k}` -> `{v}`")
    lines += ["", "## Pair Edges (15)", ""]
    for e in report["pair_edges_15"]:
        lines.append(
            f"- `{e['index']}. {e['key']}`: slot=`{e['mapped_slot']}`, domain=`{e['process_domain']}`"
        )
    lines += ["", "## Scale Ladder", ""]
    for s in report["scale_ladder"]:
        lines.append(f"- `{s['label']}` = `{s['value']}`")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"all_checks_pass={report['all_checks_pass']}")
    print(f"json={OUT_JSON}")
    print(f"md={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

