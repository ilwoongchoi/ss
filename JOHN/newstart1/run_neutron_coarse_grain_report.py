from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from fusion_clean import sovereign_dynamics_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_DIR = ROOT / "analysis_results"
OUT_CSV = OUT_DIR / "neutron_coarse_grain_128.csv"
OUT_JSON = OUT_DIR / "neutron_coarse_grain_128.json"
OUT_MD = OUT_DIR / "neutron_coarse_grain_128.md"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    n_points = 128
    dt = 0.1
    state = np.array([1.0, 0.5, 0.5, 0.5], dtype=float)
    rows: list[dict[str, float | int | str]] = []

    for i in range(n_points):
        phase_fill = float(i / max(n_points - 1, 1))
        minute = (i % 96) * 15
        clock = f"{minute // 60:02d}:{minute % 60:02d}"
        out = sovereign_dynamics_step(state, phase_fill=phase_fill, clock_hhmm=clock, dt=dt)
        state = np.asarray(out["state_next"], dtype=float)
        nc = dict(out["neutron_coarse"])
        comp = dict(nc["components"])
        rows.append(
            {
                "i": i,
                "clock": clock,
                "phase_fill": phase_fill,
                "BM": float(state[0]),
                "BW": float(state[1]),
                "SM": float(state[2]),
                "SW": float(state[3]),
                "omega": float(np.linalg.norm(state)),
                "neutron_observable": float(nc["observable"]),
                "anchor_seed": float(nc["anchor_seed"]),
                "bridge_bundle": float(nc["bridge_bundle"]),
                "string_release": float(nc["string_release"]),
                "sm_seed": float(comp["sm_seed"]),
                "nam_nam_flux": float(comp["nam_nam_flux"]),
                "neutron_electron_flux": float(comp["neutron_electron_flux"]),
                "beta_decay_flux": float(comp["beta_decay_flux"]),
                "higgs_trapezius_flux": float(comp["higgs_trapezius_flux"]),
            }
        )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    neutron_vals = np.array([float(r["neutron_observable"]) for r in rows], dtype=float)
    anchor_vals = np.array([float(r["anchor_seed"]) for r in rows], dtype=float)
    bundle_vals = np.array([float(r["bridge_bundle"]) for r in rows], dtype=float)
    string_vals = np.array([float(r["string_release"]) for r in rows], dtype=float)
    peak_idx = int(np.argmax(neutron_vals))
    peak_row = rows[peak_idx]
    final_row = rows[-1]

    summary = {
        "points": n_points,
        "dt": dt,
        "formula": "neutron = (1/64)*|SM| + weighted_incident_bridge_bundle + spark_string_break",
        "initial_state": [1.0, 0.5, 0.5, 0.5],
        "observable_min": float(np.min(neutron_vals)),
        "observable_max": float(np.max(neutron_vals)),
        "observable_mean": float(np.mean(neutron_vals)),
        "anchor_seed_mean": float(np.mean(anchor_vals)),
        "bridge_bundle_mean": float(np.mean(bundle_vals)),
        "string_release_mean": float(np.mean(string_vals)),
        "peak_index": peak_idx,
        "peak_clock": str(peak_row["clock"]),
        "peak_phase_fill": float(peak_row["phase_fill"]),
        "peak_observable": float(peak_row["neutron_observable"]),
        "final_index": int(final_row["i"]),
        "final_clock": str(final_row["clock"]),
        "final_phase_fill": float(final_row["phase_fill"]),
        "final_observable": float(final_row["neutron_observable"]),
        "final_state": [
            float(final_row["BM"]),
            float(final_row["BW"]),
            float(final_row["SM"]),
            float(final_row["SW"]),
        ],
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Neutron Coarse Grain 128",
        "",
        "## Formula",
        "- `neutron = (1/64)*|SM| + weighted incident bridge bundle + spark string break`",
        "- incident bundle uses only the four bridges touching `SM_USER_NEUTRON`: `NAM_NAM_BRIDGE`, `NEUTRON_ELECTRON`, `BETA_DECAY`, `HIGGS_TRAPEZIUS`",
        "",
        "## Summary",
        f"- points: `{summary['points']}`",
        f"- dt: `{summary['dt']}`",
        f"- observable_min: `{summary['observable_min']}`",
        f"- observable_max: `{summary['observable_max']}`",
        f"- observable_mean: `{summary['observable_mean']}`",
        f"- anchor_seed_mean: `{summary['anchor_seed_mean']}`",
        f"- bridge_bundle_mean: `{summary['bridge_bundle_mean']}`",
        f"- string_release_mean: `{summary['string_release_mean']}`",
        "",
        "## Peak",
        f"- idx: `{summary['peak_index']}`",
        f"- clock: `{summary['peak_clock']}`",
        f"- phase_fill: `{summary['peak_phase_fill']}`",
        f"- neutron_observable: `{summary['peak_observable']}`",
        "",
        "## Final",
        f"- idx: `{summary['final_index']}`",
        f"- clock: `{summary['final_clock']}`",
        f"- phase_fill: `{summary['final_phase_fill']}`",
        f"- neutron_observable: `{summary['final_observable']}`",
        f"- final BM/BW/SM/SW: `{summary['final_state']}`",
        "",
        f"- csv: `{OUT_CSV}`",
        f"- json: `{OUT_JSON}`",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
