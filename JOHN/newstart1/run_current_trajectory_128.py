from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from fusion_clean import sovereign_dynamics_step


OUT_DIR = Path(r"d:\Users\user\Documents\newstart\analysis_results")
OUT_TRAJ_CSV = OUT_DIR / "current_trajectory_128.csv"
OUT_GRID_CSV = OUT_DIR / "current_grid_128.csv"
OUT_JSON = OUT_DIR / "current_trajectory_128.json"
OUT_MD = OUT_DIR / "current_trajectory_128.md"

N = 128
DT = 0.1
INIT = np.array([1.0, 0.5, 0.5, 0.5], dtype=float)


def minute_to_clock(minute: int) -> str:
    minute = int(minute) % (24 * 60)
    return f"{minute // 60:02d}:{minute % 60:02d}"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    state = INIT.copy()
    rows: list[dict[str, float | int | str]] = []
    grid_rows: list[dict[str, float | int | str]] = []

    for idx in range(N):
        pf = float(idx / max(N - 1, 1))
        minute = int(round(idx * (24.0 * 60.0) / N)) % (24 * 60)
        clock = minute_to_clock(minute)
        step = sovereign_dynamics_step(state, phase_fill=pf, clock_hhmm=clock, dt=DT)
        base = dict(step["base"])
        state_in = np.asarray(step["state_in"], dtype=float)
        state_next = np.asarray(step["state_next"], dtype=float)
        dstate = np.asarray(step["dstate"], dtype=float)

        rows.append(
            {
                "idx": idx,
                "pf": pf,
                "minute": minute,
                "clock": clock,
                "bm": float(state_in[0]),
                "bw": float(state_in[1]),
                "sm": float(state_in[2]),
                "sw": float(state_in[3]),
                "dbm": float(dstate[0]),
                "dbw": float(dstate[1]),
                "dsm": float(dstate[2]),
                "dsw": float(dstate[3]),
                "omega_in": float(step["omega_in"]),
                "omega_out": float(np.linalg.norm(state_next)),
                "gate": float(base["gate"]),
                "slotting": float(base["slotting"]),
                "spark": float(step["spark"]),
                "phase_gate": float(step["phase_gate"]),
                "closure_err": float(step["closure_err"]),
                "q_scale": float(base["q_scale"]),
                "n_scale": float(base["n_scale"]),
                "g_scale": float(base["g_scale"]),
                "e_scale": float(base["e_scale"]),
                "quark_9": float(base["quark_9"]),
                "gluon_10": float(base["gluon_10"]),
                "muon_11": float(base["muon_11"]),
                "tau_12": float(base["tau_12"]),
                "higgs_13": float(base["higgs_13"]),
                "overlay_norm": float(base["tunnel_transfer_split"].get("overlay_norm", 0.0)),
                "particle_backbone_norm": float(base["tunnel_transfer_split"].get("particle_backbone_norm", 0.0)),
                "node_relation_norm": float(base["tunnel_transfer_split"].get("node_relation_norm", 0.0)),
                "p_axis": float(base["tunnel_transfer_split"].get("p_axis", 0.0)),
            }
        )

        grid_rows.append(
            {
                "idx": idx,
                "clock": clock,
                "quark": float(base["quark_9"]),
                "gluon": float(base["gluon_10"]),
                "neutrino": float(state_in[2]),
                "photon": float(state_in[0]),
                "proton": float(state_in[1]),
                "electron": float(state_in[3]),
                "omega": float(step["omega_in"]),
            }
        )

        state = state_next

    with OUT_TRAJ_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with OUT_GRID_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
        writer.writeheader()
        writer.writerows(grid_rows)

    omegas = np.array([float(r["omega_in"]) for r in rows], dtype=float)
    payload = {
        "n_points": N,
        "dt": DT,
        "initial_state": INIT.tolist(),
        "omega_min": float(np.min(omegas)),
        "omega_max": float(np.max(omegas)),
        "omega_final": float(rows[-1]["omega_out"]),
        "trajectory_csv": str(OUT_TRAJ_CSV),
        "grid_csv": str(OUT_GRID_CSV),
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Current Trajectory 128",
        "",
        f"- points: `{N}`",
        f"- dt: `{DT}`",
        f"- initial_state: `{INIT.tolist()}`",
        f"- omega_min: `{payload['omega_min']}`",
        f"- omega_max: `{payload['omega_max']}`",
        f"- omega_final: `{payload['omega_final']}`",
        f"- trajectory_csv: `{OUT_TRAJ_CSV}`",
        f"- grid_csv: `{OUT_GRID_CSV}`",
        "",
        "## Final State",
        f"- BM/BW/SM/SW: `{[rows[-1]['bm'], rows[-1]['bw'], rows[-1]['sm'], rows[-1]['sw']]}`",
        f"- quark/gluon/neutrino/photon/proton/electron: `{[grid_rows[-1]['quark'], grid_rows[-1]['gluon'], grid_rows[-1]['neutrino'], grid_rows[-1]['photon'], grid_rows[-1]['proton'], grid_rows[-1]['electron']]}`",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
