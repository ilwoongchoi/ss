from __future__ import annotations

from pathlib import Path

from geometry_package.ownership_bridge_model import closure_sequence, ownership_rows


OUT = Path("analysis_results/ownership_bridge_model.md")
OUT.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    lines: list[str] = []
    lines.append("# Ownership Bridge Model")
    lines.append("")
    lines.append("## Canonical Ledger")
    lines.append("")
    for row in ownership_rows():
        lines.append(
            f"- `{row['edge']}` {row['pair']}: "
            f"domain=`{row['domain']}`, ownership=`{row['ownership']}`, "
            f"role=`{row['role']}`"
        )
        if "strength" in row:
            lines.append(f"  strength=`{row['strength']}`")
        if "processes" in row:
            lines.append(f"  processes=`{row['processes']}`")
    lines.append("")
    lines.append("## Closure Sequence")
    lines.append("")
    for step in closure_sequence():
        lines.append(f"- {step}")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
