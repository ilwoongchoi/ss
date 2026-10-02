from __future__ import annotations

import argparse
import cmath
import json
from pathlib import Path

from geometry_package.absolute_constants import (
    DELTA_T_OBS_DERIVED,
    GAMMA_COSMOS,
    OMEGA_DUALITY,
    OMEGA_H2,
    OMEGA_KAPPA,
    OMEGA_PHI,
    OMEGA_SLOTTING_DELTA,
    OMEGA_SLOTTING_START,
    OMEGA_TARGET,
    OMEGA_W7,
    PHI,
    SPARK_ANGLE_DEG,
    SPARK_ANGLE_RAD,
)
from geometry_package.interaction_64 import PARTICLE_MAP
from run_multiscale_universe_equation import SCALE_LOCKS


PHYSICAL_TO_PARTICLE = {
    "electron": "e",
    "photon": "gamma",
    "proton": "p",
    "neutrino": "nu",
}


def omega_prefactor() -> float:
    return (1.0 / (OMEGA_KAPPA * OMEGA_DUALITY)) * (OMEGA_PHI / (OMEGA_W7 + OMEGA_H2))


def omega_natural(t: float) -> float:
    return (OMEGA_SLOTTING_START - (OMEGA_SLOTTING_DELTA * t)) * omega_prefactor()


def omega_natural_dt() -> float:
    return -OMEGA_SLOTTING_DELTA * omega_prefactor()


def build_scale_row(scale_name: str, scale_value: float) -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    kappa = float(OMEGA_KAPPA)
    theta = float(SPARK_ANGLE_RAD)
    phase_seed = complex(delta, kappa)
    z0 = scale_value * phase_seed

    c0 = phase_seed
    rotation_plus = cmath.exp(1j * theta)
    rotation_minus = cmath.exp(-1j * theta)

    z1_plus = scale_value * rotation_plus * (((z0 / scale_value) ** 2) + c0)
    z1_minus = scale_value * rotation_minus * (((z0 / scale_value) ** 2) + c0)

    delta_plus = z1_plus - z0
    delta_minus = z1_minus - z0

    jacobian_plus = 2.0 * rotation_plus * (z0 / scale_value)
    jacobian_minus = 2.0 * rotation_minus * (z0 / scale_value)
    hessian_plus = (2.0 / scale_value) * rotation_plus
    hessian_minus = (2.0 / scale_value) * rotation_minus

    particle = PHYSICAL_TO_PARTICLE.get(scale_name)
    archetype = PARTICLE_MAP.get(particle, {}).get("symbol", "N/A")
    node = PARTICLE_MAP.get(particle, {}).get("node", "N/A")

    return {
        "scale_name": scale_name,
        "scale_value": float(scale_value),
        "particle": particle if particle is not None else "N/A",
        "archetype": archetype,
        "node": node,
        "z0": {"real": float(z0.real), "imag": float(z0.imag), "norm": float(abs(z0))},
        "z1_plus": {"real": float(z1_plus.real), "imag": float(z1_plus.imag), "norm": float(abs(z1_plus))},
        "z1_minus": {"real": float(z1_minus.real), "imag": float(z1_minus.imag), "norm": float(abs(z1_minus))},
        "delta_plus": {"real": float(delta_plus.real), "imag": float(delta_plus.imag), "norm": float(abs(delta_plus))},
        "delta_minus": {"real": float(delta_minus.real), "imag": float(delta_minus.imag), "norm": float(abs(delta_minus))},
        "jacobian_plus": {
            "real": float(jacobian_plus.real),
            "imag": float(jacobian_plus.imag),
            "norm": float(abs(jacobian_plus)),
        },
        "jacobian_minus": {
            "real": float(jacobian_minus.real),
            "imag": float(jacobian_minus.imag),
            "norm": float(abs(jacobian_minus)),
        },
        "hessian_plus": {
            "real": float(hessian_plus.real),
            "imag": float(hessian_plus.imag),
            "norm": float(abs(hessian_plus)),
        },
        "hessian_minus": {
            "real": float(hessian_minus.real),
            "imag": float(hessian_minus.imag),
            "norm": float(abs(hessian_minus)),
        },
    }


def build_report() -> dict[str, object]:
    delta = float(DELTA_T_OBS_DERIVED)
    kappa = float(OMEGA_KAPPA)
    theta = float(SPARK_ANGLE_RAD)
    forced_seconds = delta * float(GAMMA_COSMOS)
    prefactor = omega_prefactor()
    seed = complex(delta, kappa)
    rotation_plus = cmath.exp(1j * theta)
    rotation_minus = cmath.exp(-1j * theta)

    scales = [build_scale_row(name, value) for name, value in SCALE_LOCKS.items()]
    jacobian_norms = {row["scale_name"]: row["jacobian_plus"]["norm"] for row in scales}

    return {
        "forced_time_conversion": {
            "delta_phase": delta,
            "gamma_cosmos": float(GAMMA_COSMOS),
            "seconds_if_forced": float(forced_seconds),
            "status": "forced algebraic conversion only",
        },
        "final_equations": {
            "phase_threshold": "delta_phase = (11/7) / loop_strength_5",
            "omega_top": "Omega_natural(t) = ((1.4 - 0.076 t) / (kappa * 2)) * (phi / (W7 + H2))",
            "omega_locked": "Omega_final(t) = max(Omega_natural(t), 7.4)",
            "geometry_top": "z_(n+1,pm)^(s) = s * exp(pm i theta) * (((z_n^(s))/s)^2 + phi^(-(n-1)) * (delta + i*kappa))",
            "first_difference": "Delta z_n^(s,pm) = z_(n+1,pm)^(s) - z_n^(s)",
        },
        "derivatives": {
            "d_omega_natural_dt": float(omega_natural_dt()),
            "d_omega_final_dt_before_lock": float(omega_natural_dt()),
            "d_omega_final_dt_after_lock": 0.0,
            "geometry_jacobian": "d z_(n+1,pm)^(s) / d z_n^(s) = exp(pm i theta) * 2 z_n^(s) / s",
            "geometry_hessian": "d^2 z_(n+1,pm)^(s) / d (z_n^(s))^2 = 2 exp(pm i theta) / s",
            "forcing_decay": "d c_n / d n = -(ln phi) phi^(-(n-1)) (delta + i*kappa)",
        },
        "seed_dynamics": {
            "seed_phase": {"real": float(seed.real), "imag": float(seed.imag), "norm": float(abs(seed))},
            "rotation_plus": {"real": float(rotation_plus.real), "imag": float(rotation_plus.imag)},
            "rotation_minus": {"real": float(rotation_minus.real), "imag": float(rotation_minus.imag)},
            "jacobian_norm_all_scales_equal": len(set(round(v, 15) for v in jacobian_norms.values())) == 1,
            "jacobian_norm_value": float(next(iter(jacobian_norms.values()))),
            "omega_prefactor": float(prefactor),
            "omega_at_t0": float(omega_natural(0.0)),
            "omega_at_lock_threshold_13_5": float(omega_natural(13.5)),
            "omega_target": float(OMEGA_TARGET),
        },
        "scale_dynamics": scales,
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Universe Derivative Report",
        "",
        "## Forced Time Conversion",
        f"- delta_phase: `{report['forced_time_conversion']['delta_phase']}`",
        f"- gamma_cosmos: `{report['forced_time_conversion']['gamma_cosmos']}`",
        f"- seconds_if_forced: `{report['forced_time_conversion']['seconds_if_forced']}`",
        f"- status: `{report['forced_time_conversion']['status']}`",
        "",
        "## Final Equations",
        f"- phase_threshold: `{report['final_equations']['phase_threshold']}`",
        f"- omega_top: `{report['final_equations']['omega_top']}`",
        f"- omega_locked: `{report['final_equations']['omega_locked']}`",
        f"- geometry_top: `{report['final_equations']['geometry_top']}`",
        f"- first_difference: `{report['final_equations']['first_difference']}`",
        "",
        "## Derivatives",
        f"- d_omega_natural_dt: `{report['derivatives']['d_omega_natural_dt']}`",
        f"- d_omega_final_dt_before_lock: `{report['derivatives']['d_omega_final_dt_before_lock']}`",
        f"- d_omega_final_dt_after_lock: `{report['derivatives']['d_omega_final_dt_after_lock']}`",
        f"- geometry_jacobian: `{report['derivatives']['geometry_jacobian']}`",
        f"- geometry_hessian: `{report['derivatives']['geometry_hessian']}`",
        f"- forcing_decay: `{report['derivatives']['forcing_decay']}`",
        "",
        "## Seed Dynamics",
        f"- seed_norm: `{report['seed_dynamics']['seed_phase']['norm']}`",
        f"- jacobian_norm_all_scales_equal: `{report['seed_dynamics']['jacobian_norm_all_scales_equal']}`",
        f"- jacobian_norm_value: `{report['seed_dynamics']['jacobian_norm_value']}`",
        f"- omega_at_t0: `{report['seed_dynamics']['omega_at_t0']}`",
        f"- omega_at_lock_threshold_13_5: `{report['seed_dynamics']['omega_at_lock_threshold_13_5']}`",
        f"- omega_target: `{report['seed_dynamics']['omega_target']}`",
        "",
        "## Scale Dynamics",
    ]

    for row in report["scale_dynamics"]:
        lines.extend(
            [
                f"- scale `{row['scale_name']}`",
                f"- s `{row['scale_value']}`",
                f"- particle `{row['particle']}`",
                f"- archetype `{row['archetype']}`",
                f"- node `{row['node']}`",
                f"- z0_norm `{row['z0']['norm']}`",
                f"- delta_plus_norm `{row['delta_plus']['norm']}`",
                f"- delta_minus_norm `{row['delta_minus']['norm']}`",
                f"- jacobian_plus_norm `{row['jacobian_plus']['norm']}`",
                f"- hessian_plus_norm `{row['hessian_plus']['norm']}`",
            ]
        )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Emit the final universe equation, its derivatives, and the scale-by-scale dynamics."
    )
    parser.add_argument("--out-json", default="analysis_results/universe_derivative_report.json")
    parser.add_argument("--out-md", default="analysis_results/universe_derivative_report.md")
    args = parser.parse_args()

    report = build_report()
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"seconds_if_forced={report['forced_time_conversion']['seconds_if_forced']}")
    print(f"jacobian_norm={report['seed_dynamics']['jacobian_norm_value']}")
    print(f"d_omega_natural_dt={report['derivatives']['d_omega_natural_dt']}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
