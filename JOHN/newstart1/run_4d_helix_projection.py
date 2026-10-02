from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from geometry_package.absolute_constants import DELTA_T_OBS_DERIVED, OMEGA_KAPPA, SPARK_ANGLE_DEG, SPARK_ANGLE_RAD


def intrinsic_radius() -> float:
    return float(DELTA_T_OBS_DERIVED)


def y_gap_schedule(level: int, total_levels: int, y0: float, y_floor: float) -> float:
    # Shrinking pitch toward the upper levels.
    alpha = (int(level) - 1) / max(int(total_levels) - 1, 1)
    return float(y_floor + (y0 - y_floor) * math.exp(-3.0 * alpha))


def build_rows(levels: int, y0: float, y_floor: float) -> list[dict[str, float]]:
    r4 = intrinsic_radius()
    theta = float(SPARK_ANGLE_RAD)
    rows: list[dict[str, float]] = []

    # Start with zero hidden torsion, then let shrinking dy force torsion growth.
    w_abs = 0.0
    phase = 0.0
    y_pos = 0.0

    for level in range(1, int(levels) + 1):
        dy = y_gap_schedule(level=level, total_levels=levels, y0=y0, y_floor=y_floor)
        phase += theta
        y_pos += dy

        # The hidden torsion absorbs the mismatch created by shrinking vertical pitch.
        # Keep the full 4D norm fixed at r4.
        w_target = math.sqrt(max(r4 * r4 - dy * dy, 0.0))
        if w_target < w_abs:
            w_abs = w_abs
        else:
            w_abs = w_target

        r_xyz = math.sqrt(max(r4 * r4 - w_abs * w_abs, 0.0))
        x = r_xyz * math.cos(phase)
        z = r_xyz * math.sin(phase)

        rows.append(
            {
                "level": float(level),
                "phase_deg": float(math.degrees(phase)),
                "dy": float(dy),
                "y": float(y_pos),
                "r4": float(r4),
                "w_hidden": float(w_abs),
                "r_xyz": float(r_xyz),
                "x": float(x),
                "z": float(z),
            }
        )

    return rows


def build_report(levels: int, y0: float, y_floor: float) -> dict[str, object]:
    rows = build_rows(levels=levels, y0=y0, y_floor=y_floor)
    r4_values = np.asarray([row["r4"] for row in rows], dtype=float)
    rxyz_values = np.asarray([row["r_xyz"] for row in rows], dtype=float)
    w_values = np.asarray([row["w_hidden"] for row in rows], dtype=float)
    dy_values = np.asarray([row["dy"] for row in rows], dtype=float)

    dr = np.diff(rxyz_values)
    dw = np.diff(w_values)
    ddy = np.diff(dy_values)

    return {
        "model": {
            "intrinsic_claim": "true chirality radius is locked in 4D, while 3D widening is a projection effect",
            "r4_lock": float(intrinsic_radius()),
            "spark_angle_deg": float(SPARK_ANGLE_DEG),
            "levels": int(levels),
            "y0": float(y0),
            "y_floor": float(y_floor),
        },
        "summary": {
            "r4_constant_min": float(np.min(r4_values)),
            "r4_constant_max": float(np.max(r4_values)),
            "r4_spread": float(np.max(r4_values) - np.min(r4_values)),
            "rxyz_min": float(np.min(rxyz_values)),
            "rxyz_max": float(np.max(rxyz_values)),
            "w_min": float(np.min(w_values)),
            "w_max": float(np.max(w_values)),
            "dy_min": float(np.min(dy_values)),
            "dy_max": float(np.max(dy_values)),
            "dy_monotone_down": bool(np.all(ddy <= 1.0e-12)),
            "w_monotone_up": bool(np.all(dw >= -1.0e-12)),
            "rxyz_monotone_down": bool(np.all(dr <= 1.0e-12)),
        },
        "rows": rows,
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    model = report["model"]
    summary = report["summary"]
    lines = [
        "# 4D Helix Projection",
        "",
        "## Model",
        f"- intrinsic_claim: `{model['intrinsic_claim']}`",
        f"- r4_lock: `{model['r4_lock']}`",
        f"- spark_angle_deg: `{model['spark_angle_deg']}`",
        f"- levels: `{model['levels']}`",
        f"- y0: `{model['y0']}`",
        f"- y_floor: `{model['y_floor']}`",
        "",
        "## Summary",
        f"- r4_spread: `{summary['r4_spread']}`",
        f"- dy_monotone_down: `{summary['dy_monotone_down']}`",
        f"- w_monotone_up: `{summary['w_monotone_up']}`",
        f"- rxyz_monotone_down: `{summary['rxyz_monotone_down']}`",
        f"- rxyz_min: `{summary['rxyz_min']}`",
        f"- rxyz_max: `{summary['rxyz_max']}`",
        f"- w_min: `{summary['w_min']}`",
        f"- w_max: `{summary['w_max']}`",
        "",
        "## Rows",
    ]

    for row in report["rows"]:
        lines.append(
            f"- L{int(row['level'])}: dy={row['dy']}, r4={row['r4']}, w={row['w_hidden']}, r_xyz={row['r_xyz']}"
        )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Project a 4D fixed-radius chirality helix into 3D under shrinking y-gap and growing hidden torsion."
    )
    parser.add_argument("--levels", type=int, default=10)
    parser.add_argument("--y0", type=float, default=0.20)
    parser.add_argument("--y-floor", type=float, default=0.01)
    parser.add_argument("--out-json", default="analysis_results/4d_helix_projection.json")
    parser.add_argument("--out-md", default="analysis_results/4d_helix_projection.md")
    args = parser.parse_args()

    report = build_report(levels=args.levels, y0=args.y0, y_floor=args.y_floor)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    summary = report["summary"]
    print(f"r4_spread={summary['r4_spread']}")
    print(f"dy_monotone_down={summary['dy_monotone_down']}")
    print(f"w_monotone_up={summary['w_monotone_up']}")
    print(f"rxyz_monotone_down={summary['rxyz_monotone_down']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
