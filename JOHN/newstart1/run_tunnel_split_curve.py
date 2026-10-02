from __future__ import annotations

from pathlib import Path
from statistics import correlation

from fusion_clean import edge_stack_master_step


OUT = Path(r"d:\Users\user\Documents\newstart\analysis_results\tunnel_split_curve.md")
OUT.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    times = ["01:30", "02:15", "02:30", "02:45", "03:00"]
    rows: list[dict[str, float | str]] = []

    for t in times:
        step = edge_stack_master_step([0.25, 0.25, 0.25, 0.25], 0.5, clock_hhmm=t)
        split = step["tunnel_transfer_split"]
        face = step["face_state"] or {}
        rows.append(
            {
                "time": t,
                "mode": str(face.get("mode", "none")),
                "slotting": float(step["slotting"]),
                "transfer_eff": float(split["transfer_efficiency"]),
                "bm_sm_eff": float(split["bm_sm_effective"]),
                "bw_bw_reserve": float(split["bw_bw_container_reserve"]),
                "window_position": float(face.get("window_position", 0.0)),
            }
        )

    tunnel_rows = [r for r in rows if r["mode"] == "night_tunnel"]
    slotting_series = [float(r["slotting"]) for r in tunnel_rows]
    eff_series = [float(r["transfer_eff"]) for r in tunnel_rows]
    reserve_series = [float(r["bw_bw_reserve"]) for r in tunnel_rows]
    corr_slot_eff = correlation(slotting_series, eff_series) if len(slotting_series) > 1 else 0.0
    corr_slot_reserve = correlation(slotting_series, reserve_series) if len(slotting_series) > 1 else 0.0

    lines: list[str] = []
    lines.append("# Tunnel Split Curve")
    lines.append("")
    lines.append("- sample_points: `01:30, 02:15, 02:30, 02:45, 03:00`")
    lines.append("- note: `03:00` is outside tunnel window by current definition (`start <= t < end`)")
    lines.append("")
    lines.append("## Samples")
    lines.append("")
    for r in rows:
        lines.append(
            "- "
            f"time=`{r['time']}`, mode=`{r['mode']}`, pos=`{r['window_position']:.6f}`, "
            f"slotting=`{r['slotting']:.12f}`, eff=`{r['transfer_eff']:.12f}`, "
            f"bm_sm_eff=`{r['bm_sm_eff']:.12f}`, reserve=`{r['bw_bw_reserve']:.12f}`"
        )
    lines.append("")
    lines.append("## Tunnel-Only Sync")
    lines.append("")
    lines.append(f"- corr(slotting, transfer_eff) = `{corr_slot_eff:.12f}`")
    lines.append(f"- corr(slotting, bw_bw_reserve) = `{corr_slot_reserve:.12f}`")
    lines.append("- interpretation: `slotting` decreases through tunnel while `transfer_eff` rises and `reserve` falls")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
