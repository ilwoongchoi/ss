from __future__ import annotations

from pathlib import Path

from geometry_package.interaction_64 import edge_strengths_6
from geometry_package.interaction_motifs import PAIR_MACRO_GEOMETRY


OUT_DIR = Path("analysis_results")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MD = OUT_DIR / "process_level_unveil.md"


PAIR_TO_EDGE = {
    frozenset({"p", "gamma"}): "BM_BW",
    frozenset({"e", "gamma"}): "BM_SW",
    frozenset({"p", "nu"}): "SM_BW",
    frozenset({"e", "nu"}): "SM_SW",
    frozenset({"p", "e"}): "BW_SW",
    frozenset({"gamma", "nu"}): "BM_SM",
}


def build_report() -> str:
    edges = edge_strengths_6()

    lines: list[str] = []
    lines.append("# Process-Level Unveil")
    lines.append("")
    lines.append("## Strict Rule")
    lines.append("")
    lines.append("- Use only process lists explicitly encoded in `interaction_motifs.py`.")
    lines.append("- Split each bridge total equally across its listed processes.")
    lines.append("- Remove only the process explicitly named `gravitational_lensing`.")
    lines.append("- Do not subtract hidden lensing from other bridges unless separately proven.")
    lines.append("")

    lensing_share = 0.0
    process_rows: list[tuple[str, str, float, bool]] = []
    pruned_totals = dict(edges)

    for pair, processes in PAIR_MACRO_GEOMETRY.items():
        edge = PAIR_TO_EDGE[frozenset(pair)]
        total = edges[edge]
        share = total / len(processes)
        for proc in processes:
            is_lensing = proc == "gravitational_lensing"
            process_rows.append((edge, proc, share, is_lensing))
            if is_lensing:
                lensing_share += share
                pruned_totals[edge] = pruned_totals[edge] - share

    lines.append("## Process Shares")
    lines.append("")
    for edge, proc, share, is_lensing in process_rows:
        suffix = "  <-- removed" if is_lensing else ""
        lines.append(f"- `{edge} :: {proc} = {share:.17f}`{suffix}")
    lines.append("")

    lines.append("## Bridge Totals")
    lines.append("")
    for edge in ("BM_BW", "BM_SW", "SM_BW", "SM_SW", "BW_SW", "BM_SM"):
        lines.append(
            f"- `{edge}: raw={edges[edge]:.17f}, pruned={pruned_totals[edge]:.17f}`"
        )
    lines.append("")

    lines.append("## Key Results")
    lines.append("")
    lines.append(f"- `strict_lensing_share = {lensing_share:.17f}`")
    lines.append(f"- `BM_SM_direct_raw = {edges['BM_SM']:.17f}`")
    lines.append(f"- `BM_SM_direct_pruned = {pruned_totals['BM_SM']:.17f}`")
    lines.append("- `BM_SM` itself does not change under strict process-level unveiling, because its listed process is `gravitational_interaction`, not `gravitational_lensing`.")
    lines.append("")

    residual_like = edges["BW_SW"] - pruned_totals["BM_SW"] - pruned_totals["SM_BW"] - pruned_totals["SM_SW"] - pruned_totals["BM_SM"]
    lines.append("## Residual-Like Leftover")
    lines.append("")
    lines.append(f"- `BW_SW - BM_SW(pruned) - SM_BW(pruned) - SM_SW(pruned) - BM_SM(pruned) = {residual_like:.17f}`")
    lines.append("- This number is a bookkeeping leftover, not a direct BM_SM measurement.")
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    OUT_MD.write_text(build_report(), encoding="utf-8")
    print(str(OUT_MD))
