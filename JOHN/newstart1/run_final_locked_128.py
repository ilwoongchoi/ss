from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from fusion_clean import MOTIF_TARGET_4, sovereign_dynamics_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_DIR = ROOT / "analysis_results"
OUT_CSV = OUT_DIR / "final_locked_128.csv"
OUT_GRID = OUT_DIR / "final_locked_grid_128.csv"
OUT_JSON = OUT_DIR / "final_locked_128.json"
OUT_MD = OUT_DIR / "final_locked_128.md"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    n_points = 128
    dt = 0.1
    state = np.array([1.0, 0.5, 0.5, 0.5], dtype=float)

    rows = []
    omegas = []
    for i in range(n_points):
        pf = float(i / max(n_points - 1, 1))
        minute = (i % 96) * 15
        clock = f"{minute // 60:02d}:{minute % 60:02d}"
        out = sovereign_dynamics_step(state, phase_fill=pf, clock_hhmm=clock, dt=dt)
        state = np.asarray(out["state_next"], dtype=float)
        omega = float(np.linalg.norm(state))
        omegas.append(omega)
        s6 = np.asarray(out["semantic_state6"], dtype=float)
        rows.append(
            {
                "i": i,
                "clock": clock,
                "phase_fill": pf,
                "BM": float(state[0]),
                "BW": float(state[1]),
                "SM": float(state[2]),
                "SW": float(state[3]),
                "omega": omega,
                "self": float(s6[0]),
                "origin": float(s6[1]),
                "discrete": float(s6[2]),
                "continuous": float(s6[3]),
                "will": float(s6[4]),
                "collapse": float(s6[5]),
            }
        )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # 128-grid projection payload (index + 4D state + 6-state semantics)
    with OUT_GRID.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["idx", "BM", "BW", "SM", "SW", "self", "origin", "discrete", "continuous", "will", "collapse"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(
                {
                    "idx": r["i"],
                    "BM": r["BM"],
                    "BW": r["BW"],
                    "SM": r["SM"],
                    "SW": r["SW"],
                    "self": r["self"],
                    "origin": r["origin"],
                    "discrete": r["discrete"],
                    "continuous": r["continuous"],
                    "will": r["will"],
                    "collapse": r["collapse"],
                }
            )

    final_state = np.array([rows[-1]["BM"], rows[-1]["BW"], rows[-1]["SM"], rows[-1]["SW"]], dtype=float)
    summary = {
        "points": n_points,
        "dt": dt,
        "initial_state": [1.0, 0.5, 0.5, 0.5],
        "omega_min": float(np.min(omegas)),
        "omega_max": float(np.max(omegas)),
        "omega_final": float(omegas[-1]),
        "final_state": final_state.tolist(),
        "target_state": np.asarray(MOTIF_TARGET_4, dtype=float).tolist(),
        "dist_to_target": float(np.linalg.norm(final_state - np.asarray(MOTIF_TARGET_4, dtype=float))),
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Final Locked 128",
        "",
        f"- points: `{summary['points']}`",
        f"- dt: `{summary['dt']}`",
        f"- omega_min: `{summary['omega_min']}`",
        f"- omega_max: `{summary['omega_max']}`",
        f"- omega_final: `{summary['omega_final']}`",
        f"- final BM/BW/SM/SW: `{summary['final_state']}`",
        f"- target BM/BW/SM/SW: `{summary['target_state']}`",
        f"- dist_to_target: `{summary['dist_to_target']}`",
        "",
        f"- csv: `{OUT_CSV}`",
        f"- grid: `{OUT_GRID}`",
        f"- json: `{OUT_JSON}`",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
