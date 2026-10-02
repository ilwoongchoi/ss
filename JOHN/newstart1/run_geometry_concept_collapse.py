from __future__ import annotations

import argparse
import json
from pathlib import Path

from geometry_package import absolute_constants as ac


def build_report() -> dict[str, object]:
    primitive = {
        "shape_seed": {
            "phi": ac.PHI,
            "alpha": ac.ALPHA,
            "betti_0": ac.BETTI_0,
            "betti_5": ac.BETTI_5,
            "betti_7": ac.BETTI_7,
            "betti_11": ac.BETTI_11,
        },
        "chirality_gate": {
            "spark_angle_deg": ac.SPARK_ANGLE_DEG,
            "kappa": ac.OMEGA_KAPPA,
            "lattice_3_32": ac.LATTICE_3_32,
            "gate_5_32": ac.GATE_5_32,
        },
        "time_engine": {
            "slotting_start": ac.OMEGA_SLOTTING_START,
            "slotting_delta": ac.OMEGA_SLOTTING_DELTA,
            "omega_phi": ac.OMEGA_PHI,
            "omega_w7": ac.OMEGA_W7,
            "omega_h2": ac.OMEGA_H2,
            "omega_duality": ac.OMEGA_DUALITY,
            "lunar_cycle": ac.LUNAR_CYCLE,
        },
        "4d_hardware": {
            "metric_4d": ac.METRIC_4D,
            "torsion_4d": ac.TORSION_4D,
            "maxwell_r_major": ac.MAXWELL_R_MAJOR,
            "maxwell_r_minor": ac.MAXWELL_R_MINOR,
            "maxwell_q_factor": ac.MAXWELL_Q_FACTOR,
        },
        "particle_scales": {
            "electron": ac.S_ELECTRON,
            "photon": ac.S_PHOTON,
            "proton": ac.S_PROTON,
            "sentinel": ac.S_SENTINEL,
            "neutrino": ac.S_NEUTRINO,
            "graviton": ac.S_GRAVITON,
        },
    }

    derived = {
        "chirality_constant": ac.CHIRALITY_CONSTANT,
        "loop_strength_5": ac.LOOP_STRENGTH_5,
        "winding_ratio_11_7": ac.WINDING_RATIO_11_7,
        "delta_phase": ac.DELTA_T_OBS_DERIVED,
        "drift_from_gap_11_over_8": ac.DRIFT_FROM_GAP_11_OVER_8,
        "closure_12_over_12": ac.CLOSURE_12_OVER_12,
        "renormalization_bridge": ac.RENORMALIZATION_BRIDGE,
        "alpha_kappa_bridge": ac.ALPHA_KAPPA_BRIDGE,
        "omega_la": ac.OMEGA_LA,
        "phi_pb": ac.PHI_PB,
        "flash_bridge_angle": ac.FLASH_BRIDGE_ANGLE,
        "d3_equilibrium_angle": ac.D3_EQUILIBRIUM_ANGLE,
    }

    operators = {
        "mandelbrot_core": "z_next = z^2 + c",
        "spark_rotation": "R_theta with theta = 138.88 deg",
        "omega_law": "Omega(t) = ((slotting_start - slotting_delta*t)/(kappa*duality)) * (omega_phi/(omega_w7+omega_h2)) * schedule(t) * comag(maxwell)",
        "schedule": "schedule(t) = 1 + 0.5*lunar_cycle*sin(2*pi*(28*t mod 1))",
        "comag": "comag = 1 + gate_5_32/(1 + z_maxwell), z_maxwell=(Q*R_major)/R_minor",
        "edge_projection": "particle edges from interaction_64 edge_strengths_6",
        "domain_projection": "observable_y = Projection_domain(state, domain)",
    }

    overlap_collapse = {
        "phi_family": {
            "primitive": ["phi"],
            "derived_or_operator_forms": [
                "phi_decay",
                "phi_decay2",
                "phi_decay3",
                "metric_phi",
                "kappa_phi",
                "gate_phi",
                "lattice_phi",
                "chirality_phi",
            ],
            "rule": "do not fit these as independent constants; they are phi-governed operator descendants",
        },
        "omega_family": {
            "primitive": ["slotting_start", "slotting_delta", "omega_phi", "omega_w7", "omega_h2", "omega_duality", "lunar_cycle", "maxwell_*"],
            "derived_or_operator_forms": [
                "omega",
                "engine",
                "reservoir",
                "schedule",
                "comag",
                "torsion_omega",
            ],
            "rule": "fit only the primitive engine; all other omega terms are operator outputs",
        },
        "spark_family": {
            "primitive": ["spark_angle_deg", "torsion_4d"],
            "derived_or_operator_forms": [
                "half_spark_angle",
                "flash_bridge_angle",
                "d3_delta_theta_cw",
                "d3_delta_theta_ccw",
                "cos_theta",
                "sin_theta",
                "cos_half_theta",
                "sin_half_theta",
            ],
            "rule": "spark harmonics are projection bases, not new constants",
        },
        "kappa_family": {
            "primitive": ["kappa", "lattice_3_32", "gate_5_32"],
            "derived_or_operator_forms": [
                "kappa_h2",
                "kappa_h3",
                "kappa_h4",
                "kappa_tda_min",
                "kappa_tda_mid",
                "kappa_tda_max",
            ],
            "rule": "all kappa descendants must be represented as level-specific resolutions of one quantization family",
        },
        "particle_family": {
            "primitive": ["particle_scales", "edge_strengths_6"],
            "derived_or_operator_forms": [
                "scale_i_cos",
                "scale_i_sin",
                "edge_i_cos",
                "edge_i_sin",
            ],
            "rule": "use particle scales and interaction edges once; harmonic projections are not independent constants",
        },
    }

    collapsed_skeleton = {
        "state_equation": (
            "z_(n+1,d) = Projection_d( R_(theta + torsion_4d*Omega(t_n)) "
            "[ metric_4d * z_n^2 + phi^(-(n-1)) * (delta_phase + i*kappa) + Edge(s_n) ], domain_d )"
        ),
        "delta_definition": "delta_phase = (11/7) / loop_strength_5, loop_strength_5 = 100 * chirality_constant, chirality_constant = 1/(11+7)",
        "omega_definition": (
            "Omega(t) = ((slotting_start - slotting_delta*t)/(kappa*duality)) * "
            "(omega_phi/(omega_w7+omega_h2)) * schedule(t) * comag(maxwell)"
        ),
        "residual_rule": "residual_w = observed - 3D_projection; introduce new term only after primitive/operator overlap is exhausted",
    }

    return {
        "primitive": primitive,
        "derived": derived,
        "operators": operators,
        "overlap_collapse": overlap_collapse,
        "collapsed_skeleton": collapsed_skeleton,
    }


def write_markdown(report: dict[str, object], out_path: Path) -> None:
    lines = [
        "# Geometry Concept Collapse",
        "",
        "## Primitive",
    ]
    for group, values in report["primitive"].items():
        lines.append(f"- `{group}`")
        for key, value in values.items():
            lines.append(f"- `{key}` = `{value}`")

    lines.extend(["", "## Derived"])
    for key, value in report["derived"].items():
        lines.append(f"- `{key}` = `{value}`")

    lines.extend(["", "## Operators"])
    for key, value in report["operators"].items():
        lines.append(f"- `{key}` -> `{value}`")

    lines.extend(["", "## Overlap Collapse"])
    for family, payload in report["overlap_collapse"].items():
        lines.append(f"- `{family}`")
        lines.append(f"- primitive: `{payload['primitive']}`")
        lines.append(f"- descendants: `{payload['derived_or_operator_forms']}`")
        lines.append(f"- rule: `{payload['rule']}`")

    lines.extend(["", "## Collapsed Skeleton"])
    for key, value in report["collapsed_skeleton"].items():
        lines.append(f"- `{key}`: `{value}`")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Collapse geometry constants into primitive/derived/operator/projection families.")
    parser.add_argument("--out-json", default="analysis_results/geometry_concept_collapse.json")
    parser.add_argument("--out-md", default="analysis_results/geometry_concept_collapse.md")
    args = parser.parse_args()

    report = build_report()
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    write_markdown(report, out_md)

    print(f"primitive_groups={len(report['primitive'])}")
    print(f"derived_count={len(report['derived'])}")
    print(f"overlap_families={len(report['overlap_collapse'])}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
