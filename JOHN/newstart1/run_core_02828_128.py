from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from geometry_package.core_02828_operator import core_02828_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_DIR = ROOT / "analysis_results"
OUT_CSV = OUT_DIR / "core_02828_128.csv"
OUT_JSON = OUT_DIR / "core_02828_128.json"
OUT_MD = OUT_DIR / "core_02828_128.md"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    state6 = np.array([1.0, 1.0, 0.5, 0.5, 0.5, 0.5], dtype=float)
    rows = []

    for idx in range(128):
        out = core_02828_step(state6, dt=0.05)
        state6 = np.asarray(out["state6_out"], dtype=float)
        state4 = np.asarray(out["state4_out"], dtype=float)
        rows.append(
            {
                "idx": idx,
                "quark": float(state6[0]),
                "gluon": float(state6[1]),
                "neutrino": float(state6[2]),
                "photon": float(state6[3]),
                "proton": float(state6[4]),
                "electron": float(state6[5]),
                "BM": float(state4[0]),
                "BW": float(state4[1]),
                "SM": float(state4[2]),
                "SW": float(state4[3]),
                "omega4": float(out["omega4"]),
            }
        )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    final_row = rows[-1]
    summary = {
        "points": 128,
        "dt": 0.05,
        "retained_structure": ["6_subjects", "4_coordinates", "15_edges", "0.2828"],
        "final_state6": [final_row[k] for k in ("quark", "gluon", "neutrino", "photon", "proton", "electron")],
        "final_state4": [final_row[k] for k in ("BM", "BW", "SM", "SW")],
        "omega4_final": float(final_row["omega4"]),
        "omega4_min": float(min(r["omega4"] for r in rows)),
        "omega4_max": float(max(r["omega4"] for r in rows)),
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Core 0.2828 / 6-subject / 15-edge / 4-coordinate",
        "",
        f"- points: `{summary['points']}`",
        f"- dt: `{summary['dt']}`",
        f"- retained_structure: `{summary['retained_structure']}`",
        f"- omega4_min: `{summary['omega4_min']}`",
        f"- omega4_max: `{summary['omega4_max']}`",
        f"- omega4_final: `{summary['omega4_final']}`",
        f"- final_state6: `{summary['final_state6']}`",
        f"- final_state4: `{summary['final_state4']}`",
        "",
        f"- csv: `{OUT_CSV}`",
        f"- json: `{OUT_JSON}`",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
