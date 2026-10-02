from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np

from absolute_constants import C as COUPLING_C_SQRT2_OVER_5
from absolute_constants import NEUTRON_TIME_SYNC
from absolute_constants import SPARK_ANGLE_RAD
from absolute_constants import SPARK_CONSTANT_C


def derived_delta_t_obs() -> float:
    # Canonical "clover/observer gap" used across repo:
    #   W = 11/7, L = 100/18 (= 5.555...)
    #   Δt = W/L = (11/7)/(100/18) = 99/350
    return float(99.0 / 350.0)


PHI = (1.0 + math.sqrt(5.0)) / 2.0


def analytic_signal(x: np.ndarray) -> np.ndarray:
    """Hilbert-transform analytic signal (FFT method), matching repo conventions."""
    x = np.asarray(x, dtype=float)
    n = int(x.size)
    if n == 0:
        return np.asarray([], dtype=np.complex128)
    X = np.fft.fft(x)
    h = np.zeros(n, dtype=float)
    if n % 2 == 0:
        h[0] = 1.0
        h[n // 2] = 1.0
        h[1 : n // 2] = 2.0
    else:
        h[0] = 1.0
        h[1 : (n + 1) // 2] = 2.0
    return np.fft.ifft(X * h)


def helix_metrics(z: np.ndarray) -> dict[str, float | int | bool]:
    z = np.asarray(z, dtype=np.complex128)
    if z.size == 0:
        return {
            "n": 0,
            "min_amplitude": 0.0,
            "mean_amplitude": 0.0,
            "phase_span": 0.0,
            "phase_turns": 0.0,
            "handedness": 0.0,
            "opposite_fraction": 0.0,
            "helix_continuous": False,
        }

    amp = np.abs(z)
    phase = np.unwrap(np.angle(z))
    dphi = np.diff(phase)
    nonzero = dphi[np.abs(dphi) > 1.0e-9]
    handedness = 0.0 if nonzero.size == 0 else float(np.sign(np.median(nonzero)))
    opposite_fraction = 0.0 if nonzero.size == 0 else float(np.mean(np.sign(nonzero) != handedness))
    phase_span = float(phase[-1] - phase[0])
    min_amp = float(np.min(amp))

    return {
        "n": int(z.size),
        "min_amplitude": min_amp,
        "mean_amplitude": float(np.mean(amp)),
        "phase_span": phase_span,
        "phase_turns": float(abs(phase_span) / (2.0 * math.pi)),
        "handedness": handedness,
        "opposite_fraction": opposite_fraction,
        "helix_continuous": bool(min_amp > 0.0 and abs(phase_span) > math.pi and handedness != 0.0),
    }


def count_turning_points(x: np.ndarray) -> int:
    x = np.asarray(x, dtype=float)
    if x.size < 3:
        return 0
    dx = np.diff(x)
    signs = np.sign(dx)
    # ignore zero slopes
    signs = signs[np.abs(signs) > 1.0e-12]
    if signs.size < 2:
        return 0
    return int(np.sum(signs[1:] != signs[:-1]))


def corr(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.size != b.size or a.size < 2:
        return float("nan")
    a0 = a - float(np.mean(a))
    b0 = b - float(np.mean(b))
    denom = float(np.linalg.norm(a0) * np.linalg.norm(b0))
    if denom <= 1.0e-12:
        return float("nan")
    return float(np.dot(a0, b0) / denom)


DyMode = Literal["shrink", "grow", "const"]


def dy_schedule(mode: DyMode, u: float, y0: float, y_floor: float, k: float) -> float:
    u = float(max(0.0, min(1.0, u)))
    if mode == "const":
        return float(y0)
    if mode == "shrink":
        return float(y_floor + (y0 - y_floor) * math.exp(-k * u))
    if mode == "grow":
        return float(y_floor + (y0 - y_floor) * (1.0 - math.exp(-k * u)))
    raise ValueError(f"Unknown dy mode: {mode}")


@dataclass(frozen=True)
class RealVortexConfig:
    steps_per_cycle: int
    cycles: int
    r_min: float
    r_max: float
    r4_lock: float
    theta_rad: float
    delta_t_rad: float
    dy_mode: DyMode
    y0: float
    y_floor: float
    dy_k: float
    clover_twist: bool


def generate_real_vortex(cfg: RealVortexConfig) -> dict[str, object]:
    steps = int(cfg.steps_per_cycle)
    cycles = int(cfg.cycles)
    total = steps * cycles
    if steps < 3:
        raise ValueError("steps_per_cycle must be >= 3")
    if cycles < 1:
        raise ValueError("cycles must be >= 1")
    if cfg.r_max < cfg.r_min:
        raise ValueError("r_max must be >= r_min")

    y = 0.0
    rows: list[dict[str, float]] = []
    z_complex = np.zeros(total, dtype=np.complex128)
    amp = np.zeros(total, dtype=float)
    w_hidden = np.zeros(total, dtype=float)
    dy_arr = np.zeros(total, dtype=float)

    for i in range(total):
        u = (i % steps) / float(steps - 1)
        r = float(cfg.r_min + (cfg.r_max - cfg.r_min) * math.sin(math.pi * u))
        base_phase = float(i) * float(cfg.theta_rad)

        # Optional clover twist: a smooth inner/outer leaf phase shear driven by Δt.
        if cfg.clover_twist:
            shear = float(cfg.delta_t_rad) * math.sin(2.0 * math.pi * u)
        else:
            shear = 0.0
        phase = base_phase + shear

        x = r * math.cos(phase)
        z = r * math.sin(phase)

        dy = dy_schedule(cfg.dy_mode, u=u, y0=cfg.y0, y_floor=cfg.y_floor, k=cfg.dy_k)
        y += dy

        # Hidden folding: keep transverse+hidden norm bounded by r4_lock.
        w = math.sqrt(max(float(cfg.r4_lock * cfg.r4_lock - r * r), 0.0))

        rows.append(
            {
                "step": float(i),
                "u_cycle": float(u),
                "r_xyz": float(r),
                "phase_rad": float(phase),
                "x": float(x),
                "y": float(y),
                "z": float(z),
                "w_hidden": float(w),
                "dy": float(dy),
            }
        )
        z_complex[i] = complex(x, z)
        amp[i] = r
        w_hidden[i] = w
        dy_arr[i] = dy

    return {
        "rows": rows,
        "z_complex": z_complex,
        "amplitude": amp,
        "w_hidden": w_hidden,
        "dy": dy_arr,
    }


def generate_complex_validator(
    steps: int,
    cycles: int,
    *,
    delta_t_rad: float,
    damping: float,
    c_spark: complex,
) -> np.ndarray:
    total = int(steps) * int(cycles)
    rot = complex(math.cos(delta_t_rad), math.sin(delta_t_rad))
    z = complex(0.0, 0.0)
    out = np.zeros(total, dtype=np.complex128)
    for i in range(total):
        z = (z * z * rot + c_spark) * damping
        out[i] = z
    return out


def score_match(z_real: np.ndarray, z_val: np.ndarray) -> dict[str, object]:
    z_real = np.asarray(z_real, dtype=np.complex128)
    z_val = np.asarray(z_val, dtype=np.complex128)
    n = int(min(z_real.size, z_val.size))
    z_real = z_real[:n]
    z_val = z_val[:n]

    amp_real = np.abs(z_real)
    amp_val = np.abs(z_val)
    phase_real = np.unwrap(np.angle(z_real))
    phase_val = np.unwrap(np.angle(z_val))

    dphi_real = np.diff(phase_real)
    dphi_val = np.diff(phase_val)

    metrics_real = helix_metrics(z_real)
    metrics_val = helix_metrics(z_val)

    handedness_match = bool(metrics_real["handedness"] == metrics_val["handedness"])
    amp_corr = corr(amp_real, amp_val)
    dphi_corr = corr(dphi_real, dphi_val) if dphi_real.size and dphi_val.size else float("nan")
    amp_turns = {
        "real": count_turning_points(amp_real),
        "validator": count_turning_points(amp_val),
    }

    # A simple score: reward correlation and handedness agreement.
    # Keep it transparent (no magic); caller can inspect components.
    score = 0.0
    if not math.isnan(amp_corr):
        score += max(-1.0, min(1.0, amp_corr))
    if not math.isnan(dphi_corr):
        score += 0.5 * max(-1.0, min(1.0, dphi_corr))
    score += 0.5 if handedness_match else 0.0

    return {
        "n": n,
        "metrics_real": metrics_real,
        "metrics_validator": metrics_val,
        "handedness_match": handedness_match,
        "amp_corr": float(amp_corr),
        "dphi_corr": float(dphi_corr),
        "amplitude_turning_points": amp_turns,
        "score": float(score),
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    cfg = report["config"]
    lines = [
        "# Real Vortex Contract/Expand Validation",
        "",
        "Goal: build a **real-space** contract/expand vortex and use the **complex plane only as validation**.",
        "",
        "## Constants",
        f"- coupling_C_sqrt2_over_5: `{report['constants']['coupling_C_sqrt2_over_5']}`",
        f"- delta_t_obs_derived_rad: `{report['constants']['delta_t_obs_derived_rad']}`",
        f"- spark_angle_rad: `{report['constants']['spark_angle_rad']}`",
        f"- neutron_time_sync: `{report['constants']['neutron_time_sync']}`",
        f"- validator_damping: `{report['constants']['validator_damping']}`",
        "",
        "## Real-Space Config",
        f"- steps_per_cycle: `{cfg['steps_per_cycle']}`",
        f"- cycles: `{cfg['cycles']}`",
        f"- r_min: `{cfg['r_min']}`",
        f"- r_max: `{cfg['r_max']}`",
        f"- r4_lock: `{cfg['r4_lock']}`",
        f"- dy_mode: `{cfg['dy_mode']}`",
        f"- y0: `{cfg['y0']}`",
        f"- y_floor: `{cfg['y_floor']}`",
        f"- dy_k: `{cfg['dy_k']}`",
        f"- clover_twist: `{cfg['clover_twist']}`",
        "",
        "## Results",
        f"- trace_csv: `{report['artifacts']['trace_csv']}`",
        "",
    ]

    lines.append("## Real-Space Cycle Summary")
    for row in report.get("real_summary", {}).get("per_cycle", []):
        lines.extend(
            [
                f"- cycle `{row['cycle_index']}`",
                f"- dy_min `{row['dy_min']}`",
                f"- dy_max `{row['dy_max']}`",
                f"- dy_monotone_up `{row['dy_monotone_up']}`",
                f"- dy_monotone_down `{row['dy_monotone_down']}`",
                f"- w_monotone_up `{row['w_monotone_up']}`",
                f"- w_monotone_down `{row['w_monotone_down']}`",
                f"- r_turning_points `{row['r_turning_points']}`",
            ]
        )
    lines.append("")

    for name, payload in report["matches"].items():
        lines.extend(
            [
                f"### Match: `{name}`",
                f"- score: `{payload['score']}`",
                f"- handedness_match: `{payload['handedness_match']}`",
                f"- amp_corr: `{payload['amp_corr']}`",
                f"- dphi_corr: `{payload['dphi_corr']}`",
                f"- real_phase_turns: `{payload['metrics_real']['phase_turns']}`",
                f"- validator_phase_turns: `{payload['metrics_validator']['phase_turns']}`",
                f"- real_min_amp: `{payload['metrics_real']['min_amplitude']}`",
                f"- validator_min_amp: `{payload['metrics_validator']['min_amplitude']}`",
                f"- amp_turning_points_real: `{payload['amplitude_turning_points']['real']}`",
                f"- amp_turning_points_validator: `{payload['amplitude_turning_points']['validator']}`",
                "",
            ]
        )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a real-space contract/expand vortex (primary) and validate against a bounded complex recursion (secondary)."
    )
    parser.add_argument("--steps-per-cycle", type=int, default=256)
    parser.add_argument("--cycles", type=int, default=4)
    parser.add_argument("--r-min", type=float, default=float(COUPLING_C_SQRT2_OVER_5))
    parser.add_argument("--r-max", type=float, default=float(NEUTRON_TIME_SYNC))
    parser.add_argument("--r4-lock", type=float, default=float(NEUTRON_TIME_SYNC))
    parser.add_argument("--dy-mode", choices=("shrink", "grow", "const"), default="shrink")
    parser.add_argument("--y0", type=float, default=0.20)
    parser.add_argument("--y-floor", type=float, default=0.01)
    parser.add_argument("--dy-k", type=float, default=3.0)
    parser.add_argument("--clover-twist", action="store_true")
    parser.add_argument("--validator-damping", type=float, default=float(1.0 - COUPLING_C_SQRT2_OVER_5))
    parser.add_argument(
        "--hilbert-source",
        choices=("x", "radius"),
        default="x",
        help="Which real series to convert into a complex analytic signal for validation.",
    )
    parser.add_argument("--out-json", default="analysis_results/real_vortex_contract_expand_validation.json")
    parser.add_argument("--out-md", default="analysis_results/real_vortex_contract_expand_validation.md")
    parser.add_argument("--out-csv", default="analysis_results/real_vortex_contract_expand_validation_trace.csv")
    args = parser.parse_args()

    delta_t = derived_delta_t_obs()
    cfg = RealVortexConfig(
        steps_per_cycle=int(args.steps_per_cycle),
        cycles=int(args.cycles),
        r_min=float(args.r_min),
        r_max=float(args.r_max),
        r4_lock=float(args.r4_lock),
        theta_rad=float(SPARK_ANGLE_RAD),
        delta_t_rad=float(delta_t),
        dy_mode=str(args.dy_mode),  # type: ignore[arg-type]
        y0=float(args.y0),
        y_floor=float(args.y_floor),
        dy_k=float(args.dy_k),
        clover_twist=bool(args.clover_twist),
    )

    real = generate_real_vortex(cfg)
    z_real = np.asarray(real["z_complex"], dtype=np.complex128)
    amp_real = np.asarray(real["amplitude"], dtype=float)
    x_real = np.asarray([row["x"] for row in real["rows"]], dtype=float)

    # Complex-from-real validation: reconstruct a complex signal from a single real series via Hilbert transform.
    hilbert_input = x_real if str(args.hilbert_source) == "x" else amp_real
    z_hilbert = analytic_signal(hilbert_input)

    # Complex validator: bounded clover recursion with damping and canonical spark constant.
    z_validator = generate_complex_validator(
        steps=cfg.steps_per_cycle,
        cycles=cfg.cycles,
        delta_t_rad=cfg.delta_t_rad,
        damping=float(args.validator_damping),
        c_spark=complex(SPARK_CONSTANT_C),
    )

    matches: dict[str, object] = {
        "geom_vs_hilbert": score_match(z_real, z_hilbert),
        "geom_vs_validator": score_match(z_real, z_validator),
    }

    # Write trace CSV (step-aligned).
    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "step",
                "u_cycle",
                "x",
                "y",
                "z",
                "w_hidden",
                "dy",
                "z_real_re",
                "z_real_im",
                "z_val_re",
                "z_val_im",
                "z_hilbert_re",
                "z_hilbert_im",
                "amp_real",
                "amp_val",
                "amp_hilbert",
            ],
        )
        writer.writeheader()
        rows = real["rows"]
        for i in range(min(len(rows), int(z_validator.size))):
            zr = z_real[i]
            zv = z_validator[i]
            zh = z_hilbert[i] if i < z_hilbert.size else complex(float("nan"), float("nan"))
            writer.writerow(
                {
                    "step": int(rows[i]["step"]),
                    "u_cycle": rows[i]["u_cycle"],
                    "x": rows[i]["x"],
                    "y": rows[i]["y"],
                    "z": rows[i]["z"],
                    "w_hidden": rows[i]["w_hidden"],
                    "dy": rows[i]["dy"],
                    "z_real_re": float(zr.real),
                    "z_real_im": float(zr.imag),
                    "z_val_re": float(zv.real),
                    "z_val_im": float(zv.imag),
                    "z_hilbert_re": float(zh.real),
                    "z_hilbert_im": float(zh.imag),
                    "amp_real": float(abs(zr)),
                    "amp_val": float(abs(zv)),
                    "amp_hilbert": float(abs(zh)),
                }
            )

    report: dict[str, object] = {
        "constants": {
            "coupling_C_sqrt2_over_5": float(COUPLING_C_SQRT2_OVER_5),
            "delta_t_obs_derived_rad": float(delta_t),
            "spark_angle_rad": float(SPARK_ANGLE_RAD),
            "neutron_time_sync": float(NEUTRON_TIME_SYNC),
            "validator_damping": float(args.validator_damping),
            "spark_constant_c_re": float(complex(SPARK_CONSTANT_C).real),
            "spark_constant_c_im": float(complex(SPARK_CONSTANT_C).imag),
        },
        "config": {
            "steps_per_cycle": cfg.steps_per_cycle,
            "cycles": cfg.cycles,
            "r_min": cfg.r_min,
            "r_max": cfg.r_max,
            "r4_lock": cfg.r4_lock,
            "theta_rad": cfg.theta_rad,
            "delta_t_rad": cfg.delta_t_rad,
            "dy_mode": cfg.dy_mode,
            "y0": cfg.y0,
            "y_floor": cfg.y_floor,
            "dy_k": cfg.dy_k,
            "clover_twist": cfg.clover_twist,
            "hilbert_source": str(args.hilbert_source),
        },
        "real_summary": {
            "per_cycle": [],
        },
        "matches": matches,
        "artifacts": {
            "trace_csv": str(out_csv),
        },
    }

    # Cycle-wise summaries (monotonicity only makes sense within a cycle because u resets each cycle).
    per_cycle: list[dict[str, object]] = []
    for c in range(cfg.cycles):
        start = c * cfg.steps_per_cycle
        end = start + cfg.steps_per_cycle
        dy_c = np.asarray(real["dy"][start:end], dtype=float)
        w_c = np.asarray(real["w_hidden"][start:end], dtype=float)
        r_c = np.asarray(real["amplitude"][start:end], dtype=float)
        per_cycle.append(
            {
                "cycle_index": int(c),
                "dy_min": float(np.min(dy_c)) if dy_c.size else 0.0,
                "dy_max": float(np.max(dy_c)) if dy_c.size else 0.0,
                "dy_monotone_up": bool(np.all(np.diff(dy_c) >= -1.0e-12)),
                "dy_monotone_down": bool(np.all(np.diff(dy_c) <= 1.0e-12)),
                "w_monotone_up": bool(np.all(np.diff(w_c) >= -1.0e-12)),
                "w_monotone_down": bool(np.all(np.diff(w_c) <= 1.0e-12)),
                "r_turning_points": int(count_turning_points(r_c)),
            }
        )
    report["real_summary"]["per_cycle"] = per_cycle

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"json={out_json}")
    print(f"md={out_md}")
    print(f"trace_csv={out_csv}")
    print(f"score_geom_vs_hilbert={matches['geom_vs_hilbert']['score']}")
    print(f"score_geom_vs_validator={matches['geom_vs_validator']['score']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
