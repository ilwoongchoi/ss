from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from geometry_package.absolute_constants import (
    DELTA_T_OBS_DERIVED,
    OMEGA_KAPPA,
    PHI,
    S_ELECTRON,
    S_GRAVITON,
    SPARK_ANGLE_DEG,
    SPARK_ANGLE_RAD,
)
from run_multiscale_universe_equation import rotate_complex


def branch_metrics(source: complex, rotated: complex) -> tuple[float, float]:
    source_norm = abs(source)
    if source_norm <= 1.0e-12:
        return 0.0, 0.0

    radial_projection = (
        (source.real * rotated.real) + (source.imag * rotated.imag)
    ) / (source_norm * source_norm)
    transverse_projection = (
        (source.real * rotated.imag) - (source.imag * rotated.real)
    ) / (source_norm * source_norm)
    lensing_shadow = max(0.0, -radial_projection) * source_norm
    visible_transverse = abs(transverse_projection) * source_norm
    return float(lensing_shadow), float(visible_transverse)


def scan_dimensionless_helix(levels: int) -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    kappa = float(OMEGA_KAPPA)
    u = complex(delta, kappa)
    rows: list[dict[str, float]] = []

    for level in range(1, int(levels) + 1):
        phi_scale = PHI ** (-(level - 1))
        c_level = complex(delta * phi_scale, kappa * phi_scale)
        raw = (u * u) + c_level
        cw = rotate_complex(raw, +SPARK_ANGLE_RAD)
        ccw = rotate_complex(raw, -SPARK_ANGLE_RAD)
        signed_lift = float(cw.imag - ccw.imag)
        lensing_shadow, visible_transverse = branch_metrics(raw, cw)

        rows.append(
            {
                "level": float(level),
                "phi_scale": float(phi_scale),
                "raw_norm": float(abs(raw)),
                "signed_lift": signed_lift,
                "lensing_shadow": lensing_shadow,
                "visible_transverse": visible_transverse,
            }
        )
        u = 0.5 * (cw + ccw)

    return {
        "delta": delta,
        "kappa": kappa,
        "spark_angle_deg": float(SPARK_ANGLE_DEG),
        "rows": rows,
    }


def build_continuous_report(levels: int, samples: int) -> dict[str, object]:
    profile = scan_dimensionless_helix(levels=levels)
    rows = profile["rows"]
    scale_min = float(S_GRAVITON)
    scale_max = float(S_ELECTRON)
    scan_scales = np.linspace(scale_min, scale_max, int(samples))

    base_min_signed_lift = min(float(row["signed_lift"]) for row in rows)
    base_min_lensing = min(float(row["lensing_shadow"]) for row in rows)
    base_min_visible = min(float(row["visible_transverse"]) for row in rows)

    break_count = 0
    first_break_scale = None
    first_break_level = None
    sampled = []
    probe_indices = {0, len(scan_scales) // 2, len(scan_scales) - 1}

    previous_total_gap = None
    monotone_total_gap = True

    for idx, scale in enumerate(scan_scales):
        min_signed_lift = scale * base_min_signed_lift
        min_lensing = scale * base_min_lensing
        min_visible = scale * base_min_visible
        total_gap = scale * sum(float(row["signed_lift"]) for row in rows)

        if previous_total_gap is not None and total_gap < previous_total_gap:
            monotone_total_gap = False
        previous_total_gap = total_gap

        if min_signed_lift <= 0.0 or min_lensing <= 0.0 or min_visible <= 0.0:
            break_count += 1
            if first_break_scale is None:
                first_break_scale = float(scale)
                if min_signed_lift <= 0.0:
                    first_break_level = int(min(rows, key=lambda row: row["signed_lift"])["level"])
                elif min_lensing <= 0.0:
                    first_break_level = int(min(rows, key=lambda row: row["lensing_shadow"])["level"])
                else:
                    first_break_level = int(min(rows, key=lambda row: row["visible_transverse"])["level"])

        if idx in probe_indices:
            sampled.append(
                {
                    "scale": float(scale),
                    "min_signed_lift": float(min_signed_lift),
                    "min_lensing_shadow": float(min_lensing),
                    "min_visible_transverse": float(min_visible),
                    "total_signed_lift": float(total_gap),
                }
            )

    return {
        "equation": "z_(n+1,pm)^(s) = s * R_(pm theta) (((z_n^(s))/s)^2 + phi^(-(n-1)) * (delta + i*kappa))",
        "interval": {
            "scale_min": scale_min,
            "scale_max": scale_max,
            "scale_samples": int(samples),
            "levels_checked": int(levels),
        },
        "locked_constants": {
            "delta": float(profile["delta"]),
            "kappa": float(profile["kappa"]),
            "spark_angle_deg": float(profile["spark_angle_deg"]),
        },
        "dimensionless_floor": {
            "min_signed_lift": float(base_min_signed_lift),
            "min_lensing_shadow": float(base_min_lensing),
            "min_visible_transverse": float(base_min_visible),
        },
        "continuity": {
            "helix_unbroken": break_count == 0,
            "break_count": int(break_count),
            "first_break_scale": first_break_scale,
            "first_break_level": first_break_level,
            "handedness_positive_all_levels": base_min_signed_lift > 0.0,
            "lensing_positive_all_levels": base_min_lensing > 0.0,
            "visible_positive_all_levels": base_min_visible > 0.0,
            "total_lift_monotone_in_scale": monotone_total_gap,
        },
        "sampled_scales": sampled,
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    interval = report["interval"]
    continuity = report["continuity"]
    floor = report["dimensionless_floor"]
    lines = [
        "# Continuous Helix Continuity",
        "",
        "## Equation",
        f"- `{report['equation']}`",
        "",
        "## Scan Interval",
        f"- scale_min: `{interval['scale_min']}`",
        f"- scale_max: `{interval['scale_max']}`",
        f"- scale_samples: `{interval['scale_samples']}`",
        f"- levels_checked: `{interval['levels_checked']}`",
        "",
        "## Dimensionless Floor",
        f"- min_signed_lift: `{floor['min_signed_lift']}`",
        f"- min_lensing_shadow: `{floor['min_lensing_shadow']}`",
        f"- min_visible_transverse: `{floor['min_visible_transverse']}`",
        "",
        "## Verdict",
        f"- helix_unbroken: `{continuity['helix_unbroken']}`",
        f"- handedness_positive_all_levels: `{continuity['handedness_positive_all_levels']}`",
        f"- lensing_positive_all_levels: `{continuity['lensing_positive_all_levels']}`",
        f"- visible_positive_all_levels: `{continuity['visible_positive_all_levels']}`",
        f"- total_lift_monotone_in_scale: `{continuity['total_lift_monotone_in_scale']}`",
        "",
        "## Probe Scales",
    ]

    for row in report["sampled_scales"]:
        lines.extend(
            [
                f"- scale `{row['scale']}`",
                f"- min_signed_lift `{row['min_signed_lift']}`",
                f"- min_lensing_shadow `{row['min_lensing_shadow']}`",
                f"- min_visible_transverse `{row['min_visible_transverse']}`",
                f"- total_signed_lift `{row['total_signed_lift']}`",
            ]
        )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether the 0.2828 chirality helix stays unbroken from the minimum locked scale to the maximum locked scale."
    )
    parser.add_argument("--levels", type=int, default=48)
    parser.add_argument("--samples", type=int, default=4097)
    parser.add_argument("--out-json", default="analysis_results/continuous_helix_continuity.json")
    parser.add_argument("--out-md", default="analysis_results/continuous_helix_continuity.md")
    args = parser.parse_args()

    report = build_continuous_report(levels=args.levels, samples=args.samples)

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    continuity = report["continuity"]
    print(f"levels={args.levels}")
    print(f"samples={args.samples}")
    print(f"helix_unbroken={continuity['helix_unbroken']}")
    print(f"break_count={continuity['break_count']}")
    print(f"first_break_scale={continuity['first_break_scale']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
