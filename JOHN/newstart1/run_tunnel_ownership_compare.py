from __future__ import annotations

from pathlib import Path

from geometry_package.interaction_64 import edge_strengths_6
from geometry_package.interaction_motifs import PAIR_MACRO_GEOMETRY
from geometry_package.process_ownership_state_model import process_table_for_time


OUT = Path("analysis_results/tunnel_ownership_compare.md")
OUT.parent.mkdir(parents=True, exist_ok=True)


PAIR_TO_EDGE = {
    frozenset({"p", "e"}): "BW_SW",
    frozenset({"p", "gamma"}): "BM_BW",
    frozenset({"p", "nu"}): "SM_BW",
    frozenset({"e", "gamma"}): "BM_SW",
    frozenset({"e", "nu"}): "SM_SW",
    frozenset({"gamma", "nu"}): "BM_SM",
}


def summarize(clock: str) -> tuple[dict[str, float], dict[str, float]]:
    edges = edge_strengths_6()
    counts = {PAIR_TO_EDGE[k]: len(v) for k, v in PAIR_MACRO_GEOMETRY.items()}
    base_share = {edge: edges[edge] / counts[edge] for edge in counts}
    own: dict[str, float] = {}
    edge_sum: dict[str, float] = {}
    for row in process_table_for_time(clock):
        edge = str(row["edge"])
        if edge == "FACE":
            continue
        val = base_share[edge] * float(row["weight"])
        ownership = str(row["ownership"])
        own[ownership] = own.get(ownership, 0.0) + val
        edge_sum[edge] = edge_sum.get(edge, 0.0) + val
    return own, edge_sum


def main() -> int:
    day_own, day_edge = summarize("14:00")
    night_own, night_edge = summarize("02:20")

    lines: list[str] = []
    lines.append("# Tunnel Ownership Compare")
    lines.append("")
    lines.append("## Ownership Totals")
    lines.append("")
    for key in sorted(set(day_own) | set(night_own)):
        d = day_own.get(key, 0.0)
        n = night_own.get(key, 0.0)
        lines.append(f"- `{key}`: day=`{d}`, night=`{n}`, delta=`{n-d}`")
    lines.append("")
    lines.append("## Edge Totals")
    lines.append("")
    for key in sorted(set(day_edge) | set(night_edge)):
        d = day_edge.get(key, 0.0)
        n = night_edge.get(key, 0.0)
        lines.append(f"- `{key}`: day=`{d}`, night=`{n}`, delta=`{n-d}`")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
