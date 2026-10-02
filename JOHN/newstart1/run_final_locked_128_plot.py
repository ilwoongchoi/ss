from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from fusion_clean import sovereign_dynamics_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_DIR = ROOT / "analysis_results"
OUT_CSV = OUT_DIR / "final_locked_128_plot.csv"
OUT_PNG = OUT_DIR / "final_locked_128_plot.png"
OUT_JSON = OUT_DIR / "final_locked_128_plot.json"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n_points = 128
    dt = 0.1
    state = np.array([1.0, 0.5, 0.5, 0.5], dtype=float)

    traj = []
    omega = []
    for i in range(n_points):
        pf = float(i / max(n_points - 1, 1))
        minute = (i % 96) * 15
        clock = f"{minute // 60:02d}:{minute % 60:02d}"
        out = sovereign_dynamics_step(state, phase_fill=pf, clock_hhmm=clock, dt=dt)
        state = np.asarray(out["state_next"], dtype=float)
        traj.append(state.copy())
        omega.append(float(np.linalg.norm(state)))

    traj = np.stack(traj, axis=0)
    np.savetxt(OUT_CSV, traj, delimiter=",")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], color="blue", linewidth=1.5)
    ax.set_xlabel("BM")
    ax.set_ylabel("BW")
    ax.set_zlabel("SM")
    ax.set_title("Final Locked 128 Trajectory (BM,BW,SM)")
    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=200)
    plt.close(fig)

    summary = {
        "points": n_points,
        "dt": dt,
        "omega_min": float(np.min(omega)),
        "omega_max": float(np.max(omega)),
        "omega_final": float(omega[-1]),
        "final_state": traj[-1].tolist(),
        "png": str(OUT_PNG),
        "csv": str(OUT_CSV),
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(OUT_PNG))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
