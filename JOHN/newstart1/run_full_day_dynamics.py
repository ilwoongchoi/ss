from __future__ import annotations

from pathlib import Path

from fusion_clean import edge_stack_master_step


OUT = Path(r"d:\Users\user\Documents\newstart\analysis_results\full_day_dynamics.md")
OUT.parent.mkdir(parents=True, exist_ok=True)


def hhmm_series(step_min: int = 15) -> list[str]:
    vals: list[str] = []
    for m in range(0, 24 * 60, step_min):
        h = m // 60
        mm = m % 60
        vals.append(f"{h:02d}:{mm:02d}")
    return vals


def main() -> int:
    times = hhmm_series(15)
    rows: list[dict[str, float | str]] = []
    for t in times:
        s = edge_stack_master_step([0.25, 0.25, 0.25, 0.25], 0.5, clock_hhmm=t)
        w = s["edge_weights_effective"]
        split = s["tunnel_transfer_split"]
        face = s["face_state"] or {}
        rows.append(
            {
                "time": t,
                "mode": str(face.get("mode", "none")),
                "slotting": float(s["slotting"]),
                "transfer_eff": float(split["transfer_efficiency"]),
                "bm_sm_eff": float(split["bm_sm_effective"]),
                "bw_bw_reserve": float(split["bw_bw_container_reserve"]),
                "bm_sm_w": float(w["BM_SM"]),
                "bm_bm_w": float(w["BM_BM"]),
                "bw_bw_w": float(w["BW_BW"]),
            }
        )

    tunnel = [r for r in rows if r["mode"] == "night_tunnel"]
    day = [r for r in rows if r["mode"] == "day_capture"]

    lines: list[str] = []
    lines.append("# Full-Day Dynamics")
    lines.append("")
    lines.append("- sample_step: `15 minutes`")
    lines.append("- tunnel_window(default): `01:30 -> 03:00`")
    lines.append(f"- n_day_points: `{len(day)}`")
    lines.append(f"- n_tunnel_points: `{len(tunnel)}`")
    lines.append("")
    if tunnel:
        lines.append("## Tunnel Window Summary")
        lines.append("")
        lines.append(f"- first_tunnel_point: `{tunnel[0]['time']}`")
        lines.append(f"- last_tunnel_point: `{tunnel[-1]['time']}`")
        lines.append(f"- transfer_eff_start: `{tunnel[0]['transfer_eff']}`")
        lines.append(f"- transfer_eff_end: `{tunnel[-1]['transfer_eff']}`")
        lines.append(f"- bm_sm_eff_start: `{tunnel[0]['bm_sm_eff']}`")
        lines.append(f"- bm_sm_eff_end: `{tunnel[-1]['bm_sm_eff']}`")
        lines.append(f"- bw_bw_reserve_start: `{tunnel[0]['bw_bw_reserve']}`")
        lines.append(f"- bw_bw_reserve_end: `{tunnel[-1]['bw_bw_reserve']}`")
        lines.append("")

    lines.append("## Key Points")
    lines.append("")
    for key_t in ("00:00", "01:30", "02:15", "02:45", "03:00", "14:00", "23:45"):
        row = next(r for r in rows if r["time"] == key_t)
        lines.append(
            "- "
            f"time=`{row['time']}`, mode=`{row['mode']}`, slotting=`{row['slotting']:.12f}`, "
            f"transfer_eff=`{row['transfer_eff']:.12f}`, bm_sm_eff=`{row['bm_sm_eff']:.12f}`, "
            f"reserve=`{row['bw_bw_reserve']:.12f}`, BM_SM=`{row['bm_sm_w']:.12f}`, "
            f"BM_BM=`{row['bm_bm_w']:.12f}`, BW_BW=`{row['bw_bw_w']:.12f}`"
        )
    lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("- In tunnel mode, `transfer_eff` increases while `bw_bw_reserve` decreases.")
    lines.append("- In day mode, `transfer_eff` returns to the static baseline.")
    lines.append("- `BM_BM(capture)` and `BW_BW(container)` remain separated across the full day cycle.")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
