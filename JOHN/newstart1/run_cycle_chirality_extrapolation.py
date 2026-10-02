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


def branch_metrics(source: complex, rotated: complex) -> dict[str, float]:
    source_norm = abs(source)
    if source_norm <= 1.0e-12:
        return {
            "lensing_shadow": 0.0,
            "visible_transverse": 0.0,
        }
    radial_projection = (
        (source.real * rotated.real) + (source.imag * rotated.imag)
    ) / (source_norm * source_norm)
    transverse_projection = (
        (source.real * rotated.imag) - (source.imag * rotated.real)
    ) / (source_norm * source_norm)
    return {
        "lensing_shadow": float(max(0.0, -radial_projection) * source_norm),
        "visible_transverse": float(abs(transverse_projection) * source_norm),
    }


def wrap_angle(theta: float) -> float:
    return math.atan2(math.sin(theta), math.cos(theta))


def circular_distance(a: float, b: float) -> float:
    return abs(wrap_angle(a - b))


def seed_norm() -> float:
    return abs(complex(float(DELTA_T_OBS_DERIVED), float(OMEGA_KAPPA)))


def current_seed_angle() -> float:
    z0 = complex(float(DELTA_T_OBS_DERIVED), float(OMEGA_KAPPA))
    return math.atan2(z0.imag, z0.real)


def run_cycle(theta: float, levels: int) -> dict[str, float]:
    delta = float(DELTA_T_OBS_DERIVED)
    kappa = float(OMEGA_KAPPA)
    rho = seed_norm()
    u = complex(rho * math.cos(theta), rho * math.sin(theta))

    total_gap = 0.0
    total_lensing = 0.0
    total_visible = 0.0
    for level in range(1, int(levels) + 1):
        phi_scale = PHI ** (-(level - 1))
        c_level = complex(delta * phi_scale, kappa * phi_scale)
        raw = (u * u) + c_level
        cw = rotate_complex(raw, +SPARK_ANGLE_RAD)
        ccw = rotate_complex(raw, -SPARK_ANGLE_RAD)
        metrics = branch_metrics(raw, cw)
        total_gap += abs(cw.imag - ccw.imag)
        total_lensing += metrics["lensing_shadow"]
        total_visible += metrics["visible_transverse"]
        u = 0.5 * (cw + ccw)

    next_theta = math.atan2(u.imag, u.real)
    total_mass = total_gap + total_lensing + total_visible
    chirality_ratio = total_gap / max(total_mass, 1.0e-12)
    hidden_ratio = total_lensing / max(total_lensing + total_visible, 1.0e-12)
    return {
        "start_theta": float(theta),
        "end_theta": float(next_theta),
        "chirality_ratio": float(chirality_ratio),
        "hidden_ratio": float(hidden_ratio),
        "gap": float(total_gap),
        "lensing": float(total_lensing),
        "visible": float(total_visible),
    }


def build_inverse_lookup(levels: int, angle_samples: int) -> list[tuple[float, float]]:
    lookup: list[tuple[float, float]] = []
    for theta in np.linspace(-math.pi, math.pi, int(angle_samples), endpoint=False):
        row = run_cycle(float(theta), levels=levels)
        lookup.append((float(theta), float(row["end_theta"])))
    return lookup


def invert_cycle(target_theta: float, lookup: list[tuple[float, float]]) -> float:
    best_theta = lookup[0][0]
    best_dist = circular_distance(lookup[0][1], target_theta)
    for theta, end_theta in lookup[1:]:
        dist = circular_distance(end_theta, target_theta)
        if dist < best_dist:
            best_dist = dist
            best_theta = theta
    return float(best_theta)


def walk_future(start_theta: float, levels: int, cycles: int) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    theta = float(start_theta)
    for cycle_index in range(0, int(cycles) + 1):
        row = run_cycle(theta, levels=levels)
        row["cycle_index"] = int(cycle_index)
        rows.append(row)
        theta = float(row["end_theta"])
    return rows


def walk_past(start_theta: float, levels: int, cycles: int, angle_samples: int) -> list[dict[str, float]]:
    lookup = build_inverse_lookup(levels=levels, angle_samples=angle_samples)
    rows: list[dict[str, float]] = []
    theta = float(start_theta)
    for cycle_index in range(0, int(cycles) + 1):
        row = run_cycle(theta, levels=levels)
        row["cycle_index"] = -int(cycle_index)
        rows.append(row)
        theta = invert_cycle(theta, lookup=lookup)
    return rows


def summarize(rows: list[dict[str, float]], current_ratio: float) -> dict[str, float | str | bool]:
    ratios = np.asarray([row["chirality_ratio"] for row in rows], dtype=float)
    hidden = np.asarray([row["hidden_ratio"] for row in rows], dtype=float)
    theta_end = np.unwrap(np.asarray([row["end_theta"] for row in rows], dtype=float))
    idx = np.asarray([row["cycle_index"] for row in rows], dtype=float)
    slope = float(np.polyfit(idx, ratios, 1)[0]) if len(rows) >= 2 else 0.0
    max_dev = float(np.max(np.abs(ratios - current_ratio))) if len(rows) else 0.0
    ratio_diffs = np.diff(ratios)
    irregular = float(np.std(ratio_diffs)) if ratio_diffs.size else 0.0

    if max_dev < 1.0e-10:
        verdict = "exact_invariant"
    elif abs(slope) > irregular:
        verdict = "directional_drift"
    else:
        verdict = "bounded_irregular_drift"

    return {
        "ratio_min": float(np.min(ratios)),
        "ratio_max": float(np.max(ratios)),
        "hidden_min": float(np.min(hidden)),
        "hidden_max": float(np.max(hidden)),
        "max_abs_deviation_from_current": max_dev,
        "ratio_slope_per_cycle": slope,
        "ratio_diff_std": irregular,
        "net_end_theta_span": float(theta_end[-1] - theta_end[0]) if len(theta_end) else 0.0,
        "verdict": verdict,
        "exact_match_all_cycles": bool(max_dev < 1.0e-10),
    }


def build_report(levels: int, cycles: int, angle_samples: int) -> dict[str, object]:
    theta0 = current_seed_angle()
    current = run_cycle(theta0, levels=levels)
    future = walk_future(theta0, levels=levels, cycles=cycles)
    past = walk_past(theta0, levels=levels, cycles=cycles, angle_samples=angle_samples)

    return {
        "model": {
            "cycle_operator": "one full helix cascade followed by return-to-compaction amplitude normalization",
            "delta_phase": float(DELTA_T_OBS_DERIVED),
            "kappa": float(OMEGA_KAPPA),
            "spark_angle_deg": float(SPARK_ANGLE_DEG),
            "levels_per_cycle": int(levels),
            "cycles_scanned_each_direction": int(cycles),
        },
        "current_cycle": current,
        "future_summary": summarize(future, current_ratio=float(current["chirality_ratio"])),
        "past_summary": summarize(past, current_ratio=float(current["chirality_ratio"])),
        "future_cycles": future,
        "past_cycles": past,
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Cycle Chirality Extrapolation",
        "",
        "## Model",
        f"- cycle_operator: `{report['model']['cycle_operator']}`",
        f"- delta_phase: `{report['model']['delta_phase']}`",
        f"- kappa: `{report['model']['kappa']}`",
        f"- spark_angle_deg: `{report['model']['spark_angle_deg']}`",
        f"- levels_per_cycle: `{report['model']['levels_per_cycle']}`",
        f"- cycles_scanned_each_direction: `{report['model']['cycles_scanned_each_direction']}`",
        "",
        "## Current Cycle",
        f"- chirality_ratio: `{report['current_cycle']['chirality_ratio']}`",
        f"- hidden_ratio: `{report['current_cycle']['hidden_ratio']}`",
        f"- start_theta: `{report['current_cycle']['start_theta']}`",
        f"- end_theta: `{report['current_cycle']['end_theta']}`",
        "",
        "## Future Summary",
        f"- verdict: `{report['future_summary']['verdict']}`",
        f"- exact_match_all_cycles: `{report['future_summary']['exact_match_all_cycles']}`",
        f"- ratio_min: `{report['future_summary']['ratio_min']}`",
        f"- ratio_max: `{report['future_summary']['ratio_max']}`",
        f"- max_abs_deviation_from_current: `{report['future_summary']['max_abs_deviation_from_current']}`",
        f"- ratio_slope_per_cycle: `{report['future_summary']['ratio_slope_per_cycle']}`",
        "",
        "## Past Summary",
        f"- verdict: `{report['past_summary']['verdict']}`",
        f"- exact_match_all_cycles: `{report['past_summary']['exact_match_all_cycles']}`",
        f"- ratio_min: `{report['past_summary']['ratio_min']}`",
        f"- ratio_max: `{report['past_summary']['ratio_max']}`",
        f"- max_abs_deviation_from_current: `{report['past_summary']['max_abs_deviation_from_current']}`",
        f"- ratio_slope_per_cycle: `{report['past_summary']['ratio_slope_per_cycle']}`",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extrapolate repeated universe cycles and measure whether chirality stays fixed or drifts."
    )
    parser.add_argument("--levels", type=int, default=48)
    parser.add_argument("--cycles", type=int, default=32)
    parser.add_argument("--angle-samples", type=int, default=4096)
    parser.add_argument("--out-json", default="analysis_results/cycle_chirality_extrapolation.json")
    parser.add_argument("--out-md", default="analysis_results/cycle_chirality_extrapolation.md")
    args = parser.parse_args()

    report = build_report(levels=args.levels, cycles=args.cycles, angle_samples=args.angle_samples)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"current_ratio={report['current_cycle']['chirality_ratio']}")
    print(f"future_verdict={report['future_summary']['verdict']}")
    print(f"future_max_dev={report['future_summary']['max_abs_deviation_from_current']}")
    print(f"past_verdict={report['past_summary']['verdict']}")
    print(f"past_max_dev={report['past_summary']['max_abs_deviation_from_current']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
