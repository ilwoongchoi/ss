from __future__ import annotations

import argparse
import json
from pathlib import Path

from geometry_package.absolute_constants import (
    DELTA_T_OBS_DERIVED,
    GAMMA_COSMOS,
    LOOP_STRENGTH_5,
    WINDING_RATIO_11_7,
)


def build_report() -> dict[str, object]:
    delta_phase = float(DELTA_T_OBS_DERIVED)
    winding_ratio = float(WINDING_RATIO_11_7)
    loop_strength = float(LOOP_STRENGTH_5)
    observer_to_si = float(GAMMA_COSMOS)

    return {
        "verdict": {
            "delta_is_seconds": False,
            "delta_is_dimensionless_ratio": True,
            "observer_equals_big_bang": False,
            "safe_reading": "delta is a dimensionless phase threshold, not a literal SI-time delay",
        },
        "locked_identity": {
            "delta_phase": delta_phase,
            "definition": "delta_phase = (11/7) / loop_strength_5",
            "winding_ratio_11_7": winding_ratio,
            "loop_strength_5": loop_strength,
            "reconstructed_delta": float(winding_ratio / loop_strength),
        },
        "axis_separation": {
            "phase_axis": {
                "quantity": "delta_phase",
                "unit": "dimensionless",
                "meaning": "minimum internal phase-fill threshold before outward expression",
            },
            "time_axis": {
                "quantity": "t_si",
                "unit": "seconds",
                "meaning": "physical cosmology time",
            },
            "bridge_rule": {
                "quantity": "gamma_cosmos",
                "value": observer_to_si,
                "meaning": "observer-time to SI-seconds gear ratio",
                "status": "conversion gear only; not permission to reinterpret delta as literal Big Bang seconds",
            },
        },
        "invalid_readings": [
            "delta = 0.2828 seconds after observer birth",
            "energy first appears only after delta seconds",
            "observer birth is identical to the Big Bang event",
        ],
        "valid_readings": [
            "delta marks a phase threshold inside the model",
            "energy can exist before delta; delta marks outward emergence, not first existence",
            "Big Bang chronology must be handled on a separate physical time axis",
        ],
        "optional_conversion_check": {
            "delta_times_gamma_cosmos": float(delta_phase * observer_to_si),
            "interpretation": "algebraic conversion output only; not a validated cosmology timestamp",
        },
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    verdict = report["verdict"]
    ident = report["locked_identity"]
    axes = report["axis_separation"]
    lines = [
        "# Phase-Time Axis Separation",
        "",
        "## Verdict",
        f"- delta_is_seconds: `{verdict['delta_is_seconds']}`",
        f"- delta_is_dimensionless_ratio: `{verdict['delta_is_dimensionless_ratio']}`",
        f"- observer_equals_big_bang: `{verdict['observer_equals_big_bang']}`",
        f"- safe_reading: `{verdict['safe_reading']}`",
        "",
        "## Locked Identity",
        f"- delta_phase: `{ident['delta_phase']}`",
        f"- definition: `{ident['definition']}`",
        f"- winding_ratio_11_7: `{ident['winding_ratio_11_7']}`",
        f"- loop_strength_5: `{ident['loop_strength_5']}`",
        "",
        "## Axis Separation",
        f"- phase_axis: `{axes['phase_axis']['quantity']}` [{axes['phase_axis']['unit']}]",
        f"- phase_meaning: `{axes['phase_axis']['meaning']}`",
        f"- time_axis: `{axes['time_axis']['quantity']}` [{axes['time_axis']['unit']}]",
        f"- time_meaning: `{axes['time_axis']['meaning']}`",
        f"- bridge_rule: `{axes['bridge_rule']['quantity']} = {axes['bridge_rule']['value']}`",
        f"- bridge_status: `{axes['bridge_rule']['status']}`",
        "",
        "## Invalid Readings",
    ]

    for item in report["invalid_readings"]:
        lines.append(f"- `{item}`")

    lines.extend(["", "## Valid Readings"])
    for item in report["valid_readings"]:
        lines.append(f"- `{item}`")

    lines.extend(
        [
            "",
            "## Conversion Check",
            f"- delta_times_gamma_cosmos: `{report['optional_conversion_check']['delta_times_gamma_cosmos']}`",
            f"- interpretation: `{report['optional_conversion_check']['interpretation']}`",
            "",
        ]
    )
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Separate the 0.2828 phase threshold from physical cosmology time."
    )
    parser.add_argument("--out-json", default="analysis_results/phase_axis_separation.json")
    parser.add_argument("--out-md", default="analysis_results/phase_axis_separation.md")
    args = parser.parse_args()

    report = build_report()
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"delta_phase={report['locked_identity']['delta_phase']}")
    print(f"delta_is_seconds={report['verdict']['delta_is_seconds']}")
    print(f"delta_is_dimensionless_ratio={report['verdict']['delta_is_dimensionless_ratio']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
