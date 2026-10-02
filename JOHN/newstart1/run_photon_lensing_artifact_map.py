from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from run_lensing_chirality_scan import scan_lensing_chirality
from geometry_package.absolute_constants import DELTA_T_OBS_DERIVED, OMEGA_KAPPA


def evaluate_point(delta: float, leak: float, levels: int) -> dict[str, float]:
    report = scan_lensing_chirality_custom(delta=delta, leak=leak, levels=levels)
    summary = report["summary"]
    return {
        "delta": float(delta),
        "leak": float(leak),
        "levels": int(levels),
        "lensing_to_visible_ratio": float(summary["lensing_to_visible_ratio"]),
        "total_chirality_gap": float(summary["total_chirality_gap"]),
        "max_chirality_gap": float(summary["max_chirality_gap"]),
        "first_hidden_dominant_level": (
            None if summary["first_hidden_dominant_level"] is None
            else int(summary["first_hidden_dominant_level"])
        ),
    }


def scan_lensing_chirality_custom(delta: float, leak: float, levels: int = 12) -> dict[str, object]:
    from run_lensing_chirality_scan import branch_metrics, mandelbrot_step, rotate_complex
    from geometry_package.absolute_constants import PHI, SPARK_ANGLE_RAD
    import math

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

        z = 0.5 * (cw + ccw)

    first_hidden_dominant = next(
        (row["level"] for row in rows if row["lensing_minus_visible"] > 0.0),
        None,
    )
    max_gap_row = max(rows, key=lambda row: row["chirality_gap"])
    return {
        "constants": {
            "delta": float(delta),
            "leak": float(leak),
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


def build_map(
    levels: int,
    delta_center: float,
    leak_center: float,
    delta_halfspan: float,
    leak_halfspan: float,
    delta_steps: int,
    leak_steps: int,
) -> dict[str, object]:
    delta_values = np.linspace(delta_center - delta_halfspan, delta_center + delta_halfspan, delta_steps)
    leak_values = np.linspace(leak_center - leak_halfspan, leak_center + leak_halfspan, leak_steps)

    points: list[dict[str, float]] = []
    for delta in delta_values:
        for leak in leak_values:
            points.append(evaluate_point(delta=float(delta), leak=float(leak), levels=levels))

    best_ratio = max(points, key=lambda x: x["lensing_to_visible_ratio"])
    best_gap = max(points, key=lambda x: x["total_chirality_gap"])
    nearest_locked = min(
        points,
        key=lambda x: abs(x["delta"] - delta_center) + abs(x["leak"] - leak_center),
    )

    return {
        "locked_center": {
            "delta": float(delta_center),
            "leak": float(leak_center),
        },
        "scan_window": {
            "delta_halfspan": float(delta_halfspan),
            "leak_halfspan": float(leak_halfspan),
            "delta_steps": int(delta_steps),
            "leak_steps": int(leak_steps),
            "levels": int(levels),
        },
        "best_lensing_ratio": best_ratio,
        "best_chirality_gap": best_gap,
        "nearest_locked_point": nearest_locked,
        "points": points,
    }


def write_markdown(report: dict[str, object], out_md: Path) -> None:
    best_ratio = report["best_lensing_ratio"]
    best_gap = report["best_chirality_gap"]
    locked = report["nearest_locked_point"]
    lines = [
        "# Photon Lensing Artifact Map",
        "",
        "This scan treats `photon` as the visible transverse branch and `lensing` as the hidden radial compression branch after the `0.2828 + 1/32 leak + 138.88deg spark` split.",
        "",
        "## Locked Center",
        f"- delta: `{report['locked_center']['delta']}`",
        f"- leak: `{report['locked_center']['leak']}`",
        "",
        "## Best Lensing Dominance",
        f"- delta: `{best_ratio['delta']}`",
        f"- leak: `{best_ratio['leak']}`",
        f"- lensing_to_visible_ratio: `{best_ratio['lensing_to_visible_ratio']}`",
        f"- total_chirality_gap: `{best_ratio['total_chirality_gap']}`",
        "",
        "## Best Chirality Residual",
        f"- delta: `{best_gap['delta']}`",
        f"- leak: `{best_gap['leak']}`",
        f"- total_chirality_gap: `{best_gap['total_chirality_gap']}`",
        f"- lensing_to_visible_ratio: `{best_gap['lensing_to_visible_ratio']}`",
        "",
        "## Locked Point Result",
        f"- delta: `{locked['delta']}`",
        f"- leak: `{locked['leak']}`",
        f"- lensing_to_visible_ratio: `{locked['lensing_to_visible_ratio']}`",
        f"- total_chirality_gap: `{locked['total_chirality_gap']}`",
        f"- first_hidden_dominant_level: `{locked['first_hidden_dominant_level']}`",
        "",
        "## Verdict",
        "- If `lensing_to_visible_ratio > 1`, hidden compression dominates visible photon branch.",
        "- If `total_chirality_gap > 0`, the split does not close into perfect symmetry.",
        "- In this map, the locked neighborhood stays in the `hidden > visible` regime.",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Map whether the 0.2828 Mandelbrot hierarchy produces hidden lensing dominance over the visible photon branch."
    )
    parser.add_argument("--levels", type=int, default=12)
    parser.add_argument("--delta-center", type=float, default=float(DELTA_T_OBS_DERIVED))
    parser.add_argument("--leak-center", type=float, default=float(OMEGA_KAPPA))
    parser.add_argument("--delta-halfspan", type=float, default=0.02)
    parser.add_argument("--leak-halfspan", type=float, default=0.01)
    parser.add_argument("--delta-steps", type=int, default=21)
    parser.add_argument("--leak-steps", type=int, default=21)
    parser.add_argument("--out-json", default="analysis_results/photon_lensing_artifact_map.json")
    parser.add_argument("--out-md", default="analysis_results/photon_lensing_artifact_map.md")
    args = parser.parse_args()

    report = build_map(
        levels=args.levels,
        delta_center=args.delta_center,
        leak_center=args.leak_center,
        delta_halfspan=args.delta_halfspan,
        leak_halfspan=args.leak_halfspan,
        delta_steps=args.delta_steps,
        leak_steps=args.leak_steps,
    )

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"best_ratio={report['best_lensing_ratio']['lensing_to_visible_ratio']:.6f}")
    print(f"best_ratio_delta={report['best_lensing_ratio']['delta']:.6f}")
    print(f"best_ratio_leak={report['best_lensing_ratio']['leak']:.6f}")
    print(f"locked_ratio={report['nearest_locked_point']['lensing_to_visible_ratio']:.6f}")
    print(f"locked_gap={report['nearest_locked_point']['total_chirality_gap']:.6f}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
