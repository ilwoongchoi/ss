from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from geometry_package.absolute_constants import DELTA_T_OBS_DERIVED, OMEGA_KAPPA, PHI, SPARK_ANGLE_DEG, SPARK_ANGLE_RAD


def rotate_complex(z: complex, angle_rad: float) -> complex:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return complex((c * z.real) - (s * z.imag), (s * z.real) + (c * z.imag))


def build_rows(levels: int) -> list[dict[str, float]]:
    delta = float(DELTA_T_OBS_DERIVED)
    kappa = float(OMEGA_KAPPA)
    seed = complex(delta, kappa)
    u = seed
    rows: list[dict[str, float]] = []

    for level in range(1, int(levels) + 1):
        c_level = complex(delta * (PHI ** (-(level - 1))), kappa * (PHI ** (-(level - 1))))
        raw = (u * u) + c_level
        cw = rotate_complex(raw, +SPARK_ANGLE_RAD)
        ccw = rotate_complex(raw, -SPARK_ANGLE_RAD)
        nxt = 0.5 * (cw + ccw)
        rows.append(
            {
                "level": float(level),
                "radius_in": float(abs(u)),
                "radius_raw": float(abs(raw)),
                "radius_out": float(abs(nxt)),
                "gain_out_over_in": float(abs(nxt) / max(abs(u), 1.0e-12)),
                "gain_raw_over_in": float(abs(raw) / max(abs(u), 1.0e-12)),
            }
        )
        u = nxt
    return rows


def build_report(levels: int) -> dict[str, object]:
    rows = build_rows(levels=levels)
    gains = np.asarray([row["gain_out_over_in"] for row in rows], dtype=float)
    radii = np.asarray([row["radius_out"] for row in rows], dtype=float)
    levels_arr = np.asarray([row["level"] for row in rows], dtype=float)
    phi_inv = 1.0 / PHI

    tail_start = max(0, len(rows) // 2)
    tail_gains = gains[tail_start:]
    tail_mean = float(np.mean(tail_gains))
    tail_max_dev = float(np.max(np.abs(tail_gains - phi_inv)))
    tail_levels = levels_arr[tail_start:]
    tail_radii = radii[tail_start:]
    tail_slope, tail_intercept = np.polyfit(tail_levels, np.log(np.maximum(tail_radii, 1.0e-300)), 1)
    tail_base = float(math.exp(tail_slope))

    log_r = np.log(np.maximum(radii, 1.0e-300))
    slope, intercept = np.polyfit(levels_arr, log_r, 1)
    predicted = np.exp(intercept + slope * levels_arr)
    rel_err = np.max(np.abs((radii - predicted) / np.maximum(radii, 1.0e-300)))

    return {
        "locked_constants": {
            "delta": float(DELTA_T_OBS_DERIVED),
            "kappa": float(OMEGA_KAPPA),
            "spark_angle_deg": float(SPARK_ANGLE_DEG),
            "phi_inv": float(phi_inv),
            "cos_theta_abs": float(abs(math.cos(SPARK_ANGLE_RAD))),
        },
        "law": {
            "measured_statement": "radius decreases each level and converges to a geometric decay ratio",
            "asymptotic_gain": tail_mean,
            "asymptotic_target_phi_inv": float(phi_inv),
            "asymptotic_max_abs_error_vs_phi_inv": tail_max_dev,
            "closed_form_best_fit": "r_n ~= A * phi^(-n)",
            "log_fit_slope": float(slope),
            "log_fit_equivalent_base": float(math.exp(slope)),
            "log_fit_max_relative_error": float(rel_err),
            "tail_log_fit_equivalent_base": tail_base,
            "verdict": (
                "phi_inverse_decay"
                if tail_max_dev < 1.0e-5 and abs(tail_base - phi_inv) < 1.0e-5
                else "non_phi_decay"
            ),
        },
        "rows": rows,
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    law = report["law"]
    const = report["locked_constants"]
    lines = [
        "# Radius Amplification Law",
        "",
        "## Constants",
        f"- delta: `{const['delta']}`",
        f"- kappa: `{const['kappa']}`",
        f"- spark_angle_deg: `{const['spark_angle_deg']}`",
        f"- phi_inv: `{const['phi_inv']}`",
        f"- abs_cos_theta: `{const['cos_theta_abs']}`",
        "",
        "## Law",
        f"- measured_statement: `{law['measured_statement']}`",
        f"- asymptotic_gain: `{law['asymptotic_gain']}`",
        f"- asymptotic_target_phi_inv: `{law['asymptotic_target_phi_inv']}`",
        f"- asymptotic_max_abs_error_vs_phi_inv: `{law['asymptotic_max_abs_error_vs_phi_inv']}`",
        f"- closed_form_best_fit: `{law['closed_form_best_fit']}`",
        f"- log_fit_slope: `{law['log_fit_slope']}`",
        f"- log_fit_equivalent_base: `{law['log_fit_equivalent_base']}`",
        f"- log_fit_max_relative_error: `{law['log_fit_max_relative_error']}`",
        f"- verdict: `{law['verdict']}`",
        "",
        "## First Rows",
    ]

    for row in report["rows"][:12]:
        lines.append(
            f"- L{int(row['level'])}: rin={row['radius_in']}, rout={row['radius_out']}, gain={row['gain_out_over_in']}"
        )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure the actual helix radius amplification law across levels.")
    parser.add_argument("--levels", type=int, default=48)
    parser.add_argument("--out-json", default="analysis_results/radius_amplification_law.json")
    parser.add_argument("--out-md", default="analysis_results/radius_amplification_law.md")
    args = parser.parse_args()

    report = build_report(levels=args.levels)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    law = report["law"]
    print(f"asymptotic_gain={law['asymptotic_gain']}")
    print(f"phi_inv={report['locked_constants']['phi_inv']}")
    print(f"fit_base={law['log_fit_equivalent_base']}")
    print(f"verdict={law['verdict']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
