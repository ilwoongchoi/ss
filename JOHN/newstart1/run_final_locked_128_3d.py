from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from fusion_clean import sovereign_dynamics_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_DIR = ROOT / "analysis_results"
OUT_CSV = OUT_DIR / "final_locked_128_3d.csv"
OUT_MD = OUT_DIR / "final_locked_128_3d.md"


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
        rows.append(
            {
                "i": i,
                "clock": clock,
                "phase_fill": pf,
                "x_BM": float(state[0]),
                "y_BW": float(state[1]),
                "z_SM": float(state[2]),
                "sw": float(state[3]),
                "omega": omega,
            }
        )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    summary = {
        "points": n_points,
        "dt": dt,
        "omega_min": float(np.min(omegas)),
        "omega_max": float(np.max(omegas)),
        "omega_final": float(omegas[-1]),
        "final_state": [
            rows[-1]["x_BM"],
            rows[-1]["y_BW"],
            rows[-1]["z_SM"],
            rows[-1]["sw"],
        ],
        "csv": str(OUT_CSV),
    }

    lines = [
        "# Final Locked 128 (3D projection)",
        "",
        f"- points: `{summary['points']}`",
        f"- dt: `{summary['dt']}`",
        f"- omega_min: `{summary['omega_min']}`",
        f"- omega_max: `{summary['omega_max']}`",
        f"- omega_final: `{summary['omega_final']}`",
        f"- final [BM,BW,SM,SW]: `{summary['final_state']}`",
        f"- csv: `{summary['csv']}`",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
