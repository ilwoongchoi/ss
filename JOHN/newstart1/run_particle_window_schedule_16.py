from __future__ import annotations

"""
run_particle_window_schedule_16.py

Create a human-readable 16-window (90min) schedule from the CURRENT operator.

This does NOT claim "the Standard Model has a daily clock".
It answers the user's framework question:
  "If we slice a day into 16 windows, which window is strong/confinement,
   which window is Z/weak (nu-proton), which window is spark/string-breaking, etc?"
"""

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from geometry_package import absolute_constants as ac
from fusion_clean import sovereign_dynamics_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_DIR = ROOT / "analysis_results"
OUT_MD = OUT_DIR / "particle_window_schedule_16.md"


def minute_to_clock(minute: int) -> str:
    minute = int(minute) % (24 * 60)
    return f"{minute // 60:02d}:{minute % 60:02d}"


def motif_target_state4() -> np.ndarray:
    deg = np.array([6.0, 8.0, 8.0, 10.0], dtype=float)  # BM,BW,SM,SW
    return (deg / float(np.linalg.norm(deg))) * float(ac.OMEGA_TARGET)


@dataclass(frozen=True)
class StepRow:
    minute: int
    clock: str
    state: np.ndarray
    is_tunnel: bool
    capture: float
    escape: float
    spark: float
    sigma: float
    string_break: float
    em: float
    weak_z: float
    e_loss: float
    higgs: float
    quark: float
    gluon: float


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--persona", choices=["user", "people"], default="user")
    ap.add_argument("--anchor", default="15:00", help="window0 start (HH:MM), default 15:00 = p-window start")
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--phase-fill", type=float, default=0.5)
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        ah, am = str(args.anchor).split(":", 1)
        anchor_start_min = (int(ah) % 24) * 60 + (int(am) % 60)
    except Exception:
        anchor_start_min = 15 * 60

    state = motif_target_state4()
    phase_fill = float(np.clip(float(getattr(args, "phase_fill", 0.5)), 0.0, 1.0))

    # Evaluate at the CENTER of each 90min window (simple, deterministic).
    windows = []
    for i in range(16):
        start = (anchor_start_min + i * 90) % (24 * 60)
        end = (start + 90) % (24 * 60)
        center = (start + 45) % (24 * 60)
        clock = minute_to_clock(center)

        out = sovereign_dynamics_step(
            state,
            phase_fill=phase_fill,
            clock_hhmm=clock,
            dt=float(args.dt),
            control_override={"__persona__": str(args.persona)},
        )
        base = out["base"]
        split = base["tunnel_transfer_split"]
        gains = base["gains"]
        edge = base["edge_terms"]

        # Edge magnitudes
        sm_bw = float(np.linalg.norm(edge["SM_BW"]))
        sm_sw = float(np.linalg.norm(edge["SM_SW"]))
        bm_bw = float(np.linalg.norm(edge["BM_BW"]))
        bm_sw = float(np.linalg.norm(edge["BM_SW"]))
        bw_sw = float(np.linalg.norm(edge["BW_SW"]))

        weak_z = float(gains["BETA_DECAY"] * (sm_bw + sm_sw))
        em = float(gains["PHOTOELECTRIC"] * (bm_bw + bm_sw))
        e_loss = float(gains["BREMSSTRAHLUNG"] * bw_sw)

        windows.append(
            StepRow(
                minute=int(center),
                clock=clock,
                state=np.asarray(out["state_in"], dtype=float).reshape(4),
                is_tunnel=bool(base["is_tunnel"]),
                capture=float(base["capture_gate"]),
                escape=float(base["escape_gate"]),
                spark=float(out["spark"]),
                sigma=float(split["effective_string_tension"]),
                string_break=float(split["spark_string_break"]),
                em=em,
                weak_z=weak_z,
                e_loss=e_loss,
                higgs=float(base.get("higgs_13", 0.0)),
                quark=float(base.get("quark_9", 0.0)),
                gluon=float(base.get("gluon_10", 0.0)),
            )
        )

    # Render markdown in plain language.
    lines: list[str] = []
    lines.append("# 16-Window Particle Schedule (90min) from Current Operator")
    lines.append("")
    lines.append("This is the operator's **mapping** of windows to interaction dominance.")
    lines.append("It is not claiming the Standard Model has a daily clock; it's your framework's day-slice view.")
    lines.append("")
    lines.append("Legend (plain):")
    lines.append("- `sigma` : confinement strength (gluon/quark grip). High = locked; low = released.")
    lines.append("- `break` : spark-induced string breaking (5/32 aperture). High = confinement suppressed.")
    lines.append("- `weak_Z`: weak neutral-current proxy (nu with proton/electron).")
    lines.append("- `EM`    : photon/charge proxy (photon with proton/electron).")
    lines.append("- `E_loss`: electron-side radiative loss proxy (bremsstrahlung side).")
    lines.append("- `capture/escape`: operator regime flags (1/0) used internally.")
    lines.append("")
    lines.append(f"- persona: `{args.persona}`")
    lines.append(f"- anchor window0 start: `{minute_to_clock(anchor_start_min)}`")
    lines.append(f"- phase_fill: `{phase_fill}` (gate_0.2828 is {'OPEN' if phase_fill>=0.2828 else 'CLOSED'})")
    lines.append("")

    lines.append("## Table")
    lines.append("")
    lines.append("| idx | window | center | tunnel | cap | esc | spark | break | sigma | weak_Z | EM | E_loss | quark | gluon | higgs |")
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for i, r in enumerate(windows):
        start = (anchor_start_min + i * 90) % (24 * 60)
        end = (start + 90) % (24 * 60)
        lines.append(
            "| "
            + " | ".join(
                [
                    str(i),
                    f"{minute_to_clock(start)}-{minute_to_clock(end)}",
                    r.clock,
                    "1" if r.is_tunnel else "0",
                    f"{r.capture:.0f}",
                    f"{r.escape:.0f}",
                    f"{r.spark:+.3f}",
                    f"{r.string_break:.4f}",
                    f"{r.sigma:.4f}",
                    f"{r.weak_z:.4f}",
                    f"{r.em:.4f}",
                    f"{r.e_loss:.4f}",
                    f"{r.quark:.4f}",
                    f"{r.gluon:.4f}",
                    f"{r.higgs:.4f}",
                ]
            )
            + " |"
        )

    # Identify decisive peaks.
    i_z = int(max(range(16), key=lambda k: windows[k].weak_z))
    i_break = int(max(range(16), key=lambda k: windows[k].string_break))
    i_sigma = int(max(range(16), key=lambda k: windows[k].sigma))

    def win_span(i: int) -> str:
        s = (anchor_start_min + i * 90) % (24 * 60)
        e = (s + 90) % (24 * 60)
        return f"{minute_to_clock(s)}-{minute_to_clock(e)}"

    lines.append("")
    lines.append("## Decisive Windows (in this operator run)")
    lines.append("")
    lines.append(f"- Z/weak peak (nu-proton neutral-current proxy): `idx {i_z}` = `{win_span(i_z)}` (center `{windows[i_z].clock}`)")
    lines.append(f"- Spark string-breaking peak (confinement suppression): `idx {i_break}` = `{win_span(i_break)}` (center `{windows[i_break].clock}`)")
    lines.append(f"- Confinement max (sigma highest): `idx {i_sigma}` = `{win_span(i_sigma)}` (center `{windows[i_sigma].clock}`)")
    lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
