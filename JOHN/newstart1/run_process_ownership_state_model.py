from __future__ import annotations

from pathlib import Path

from geometry_package.process_ownership_state_model import grouped_summary, process_table_for_time


OUT = Path("analysis_results/process_ownership_state_model.md")
OUT.parent.mkdir(parents=True, exist_ok=True)


def _write_mode(lines: list[str], clock: str, title: str) -> None:
    rows = process_table_for_time(clock)
    lines.append(f"## {title}")
    lines.append("")
    lines.append(f"- clock: `{clock}`")
    lines.append("")
    for row in rows:
        lines.append(
            f"- `{row['edge']}::{row['process']}` ownership=`{row['ownership']}`, "
            f"weight=`{row['weight']}`, role=`{row['role']}`"
        )
    lines.append("")
    lines.append("### Grouped")
    lines.append("")
    grouped = grouped_summary(clock)
    for key, values in grouped.items():
        lines.append(f"- `{key}`: `{values}`")
    lines.append("")


def main() -> int:
    lines: list[str] = []
    lines.append("# Process Ownership State Model")
    lines.append("")
    lines.append("- `14:00` is treated as day/capture mode.")
    lines.append("- `02:20` is treated as night/female tunnel mode.")
    lines.append("- Tunnel window default is `01:30 -> 03:00`.")
    lines.append("")
    _write_mode(lines, "14:00", "Day Capture")
    _write_mode(lines, "02:20", "Night Tunnel")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
