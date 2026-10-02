from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from geometry_package.absolute_constants import DELTA_T_OBS_DERIVED, OMEGA_KAPPA, PHI, SPARK_ANGLE_RAD


def rotate_complex(z: complex, angle_rad: float) -> complex:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return complex((c * z.real) - (s * z.imag), (s * z.real) + (c * z.imag))


def mandelbrot_step(z: complex, c: complex) -> complex:
    return (z * z) + c


def branch_metrics(source: complex, rotated: complex) -> dict[str, float]:
    base_norm = abs(source)
    rot_norm = abs(rotated)
    if base_norm <= 1.0e-12:
        return {
            "base_norm": base_norm,
            "rot_norm": rot_norm,
            "radial_projection": 0.0,
            "lensing_shadow": 0.0,
            "visible_transverse": 0.0,
        }

    radial_projection = (
        (source.real * rotated.real) + (source.imag * rotated.imag)
    ) / (base_norm * base_norm)
    transverse_projection = (
        (source.real * rotated.imag) - (source.imag * rotated.real)
    ) / (base_norm * base_norm)
    return {
        "base_norm": float(base_norm),
        "rot_norm": float(rot_norm),
        "radial_projection": float(radial_projection),
        "lensing_shadow": float(max(0.0, -radial_projection) * base_norm),
        "visible_transverse": float(abs(transverse_projection) * base_norm),
    }


def scan_lensing_chirality(levels: int = 12) -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    leak = float(OMEGA_KAPPA)

    rows: list[dict[str, object]] = []
    z = complex(delta, leak)
    total_chirality_gap = 0.0
    total_lensing_shadow = 0.0
    total_visible_transverse = 0.0

    for level in range(1, int(levels) + 1):
        scale = PHI ** (-(level - 1))
        c_level = complex(delta * scale, leak * scale)
        raw = mandelbrot_step(z, c_level)
        cw = rotate_complex(raw, +SPARK_ANGLE_RAD)
        ccw = rotate_complex(raw, -SPARK_ANGLE_RAD)

        cw_metrics = branch_metrics(raw, cw)
        ccw_metrics = branch_metrics(raw, ccw)
        chirality_gap = abs(cw.imag - ccw.imag)
        symmetry_fill_ratio = min(abs(cw), abs(ccw)) / max(abs(cw), abs(ccw), 1.0e-12)
        lensing_minus_visible = cw_metrics["lensing_shadow"] - cw_metrics["visible_transverse"]

        total_chirality_gap += chirality_gap
        total_lensing_shadow += cw_metrics["lensing_shadow"]
        total_visible_transverse += cw_metrics["visible_transverse"]

        rows.append(
            {
                "level": level,
                "scale_phi": float(scale),
                "c_real_delta": float(c_level.real),
                "c_imag_leak": float(c_level.imag),
                "raw_real": float(raw.real),
                "raw_imag": float(raw.imag),
                "raw_norm": float(abs(raw)),
                "cw_real": float(cw.real),
                "cw_imag": float(cw.imag),
                "ccw_real": float(ccw.real),
                "ccw_imag": float(ccw.imag),
                "lensing_shadow": float(cw_metrics["lensing_shadow"]),
                "visible_transverse": float(cw_metrics["visible_transverse"]),
                "lensing_minus_visible": float(lensing_minus_visible),
                "chirality_gap": float(chirality_gap),
                "symmetry_fill_ratio": float(symmetry_fill_ratio),
            }
        )

        # Feed the next layer with the mean of the two spark branches.
        z = 0.5 * (cw + ccw)

    first_hidden_dominant = next(
        (row["level"] for row in rows if row["lensing_minus_visible"] > 0.0),
        None,
    )
    max_gap_row = max(rows, key=lambda row: row["chirality_gap"])

    return {
        "constants": {
            "delta_quoted": 0.2828,
            "delta_derived": delta,
            "kappa_1_32": leak,
            "spark_angle_deg": math.degrees(SPARK_ANGLE_RAD),
            "spark_cos": math.cos(SPARK_ANGLE_RAD),
            "spark_sin": math.sin(SPARK_ANGLE_RAD),
        },
        "summary": {
            "levels_scanned": int(levels),
            "first_hidden_dominant_level": first_hidden_dominant,
            "total_chirality_gap": float(total_chirality_gap),
            "total_lensing_shadow": float(total_lensing_shadow),
            "total_visible_transverse": float(total_visible_transverse),
            "lensing_to_visible_ratio": float(
                total_lensing_shadow / max(total_visible_transverse, 1.0e-12)
            ),
            "max_chirality_gap_level": int(max_gap_row["level"]),
            "max_chirality_gap": float(max_gap_row["chirality_gap"]),
        },
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan lensing/chirality residuals across Mandelbrot hierarchy at the 0.2828 minimum structure."
    )
    parser.add_argument("--levels", type=int, default=12)
    parser.add_argument(
        "--out-json",
        default="analysis_results/lensing_chirality_scan.json",
    )
    args = parser.parse_args()

    report = scan_lensing_chirality(levels=args.levels)
    out_path = Path(args.out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = report["summary"]
    print(f"levels_scanned={summary['levels_scanned']}")
    print(f"first_hidden_dominant_level={summary['first_hidden_dominant_level']}")
    print(f"lensing_to_visible_ratio={summary['lensing_to_visible_ratio']:.6f}")
    print(f"max_chirality_gap_level={summary['max_chirality_gap_level']}")
    print(f"max_chirality_gap={summary['max_chirality_gap']:.6f}")
    print(f"report={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
