from __future__ import annotations

import json
from pathlib import Path

from geometry_package import absolute_constants as ac
import fusion_clean as eq


OUT_JSON = Path(r"d:\Users\user\Documents\newstart\analysis_results\structure_crosscheck.json")
OUT_MD = Path(r"d:\Users\user\Documents\newstart\analysis_results\structure_crosscheck.md")


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    constant_checks = [
        {
            "name": "1/32",
            "domain": "discrete",
            "value": float(ac.F_1_32),
            "status": "wired_direct",
            "used_in": "discrete_stiffness",
            "meaning": "proton lattice anchor",
        },
        {
            "name": "3/32",
            "domain": "discrete",
            "value": float(ac.F_3_32),
            "status": "wired_direct",
            "used_in": "discrete_stiffness",
            "meaning": "debt/filter lattice anchor",
        },
        {
            "name": "1/28",
            "domain": "discrete",
            "value": float(ac.LUNAR_CYCLE),
            "status": "wired_direct",
            "used_in": "discrete_stiffness",
            "meaning": "lunar cycle bridge",
        },
        {
            "name": "1/9",
            "domain": "discrete",
            "value": 1.0 / 9.0,
            "status": "wired_direct",
            "used_in": "discrete_stiffness",
            "meaning": "H2/W7 scaffold term",
        },
        {
            "name": "1/64",
            "domain": "discrete",
            "value": float(ac.F_1_64),
            "status": "wired_direct",
            "used_in": "discrete_stiffness",
            "meaning": "user/neutron anchor",
        },
        {
            "name": "0.2828",
            "domain": "continuous",
            "value": float(eq.GDH_CONFINEMENT_02828),
            "status": "wired_direct",
            "used_in": "gate_02828 + confinement_bias",
            "meaning": "phase gate / confinement threshold",
        },
        {
            "name": "138.88",
            "domain": "continuous",
            "value": float(eq.SPARK_ANGLE_DEG_138_88),
            "status": "wired_direct",
            "used_in": "spark_phase",
            "meaning": "spark rotation phase",
        },
        {
            "name": "0.076",
            "domain": "continuous",
            "value": float(ac.OMEGA_SLOTTING_DELTA),
            "status": "wired_direct",
            "used_in": "slotting = 1.4 - 0.076 * phase_fill",
            "meaning": "drift / slotting leak",
        },
        {
            "name": "0.1569",
            "domain": "continuous",
            "value": float(eq.HIGGS_GABA_B_MASS),
            "status": "wired_conditional",
            "used_in": "mass anchor / higgs_13",
            "meaning": "continuous mass / hysteresis anchor",
            "note": "present in equation, but current node profile sets GABA-B channels OFF so injection is disabled",
        },
        {
            "name": "7.4",
            "domain": "real",
            "value": float(eq.OMEGA_TARGET),
            "status": "wired_direct",
            "used_in": "closure_err, physics_scale, brake_scale",
            "meaning": "homeostasis target",
        },
        {
            "name": "0.8009",
            "domain": "score",
            "value": float(eq.EFFICIENCY_TARGET_8009),
            "status": "not_a_structure_constant",
            "used_in": "unified correction / external scoring target",
            "meaning": "model score target, not a physics constant",
        },
    ]

    node_checks = [
        {
            "node": "left_acetyl_coa",
            "source": "latissimus dorsi / metabolic entrance",
            "status": "wired_active",
            "used_in": "slotting funnel tightening",
        },
        {
            "node": "male_oxytocin",
            "source": "LF inner bottom / BM-SM bond",
            "status": "wired_active",
            "used_in": "BM_SM restoring force",
        },
        {
            "node": "left_temporalis_5ht1a",
            "source": "temporalis LT-1/LT-3",
            "status": "wired_active",
            "used_in": "damping_release",
        },
        {
            "node": "right_occipitalis_gaba_a",
            "source": "RO inner top",
            "status": "wired_active",
            "used_in": "lensing_delta suppression",
        },
        {
            "node": "gaba_b",
            "source": "LO outer top / Higgs gate",
            "status": "wired_active_but_currently_disabled",
            "used_in": "mass_anchor_scale",
            "note": "wired, but current default OFF zeros mass injection",
        },
        {
            "node": "female_gaba_b_latdorsi",
            "source": "latissimus dorsi lower",
            "status": "wired_active_but_currently_disabled",
            "used_in": "mass_anchor_scale",
            "note": "wired, but current default OFF zeros mass injection",
        },
        {
            "node": "gdh_gluon",
            "source": "color confinement channel",
            "status": "wired_baseline_only",
            "used_in": "confinement_bias",
            "note": "appears as constant bias, not a controllable force term",
        },
        {
            "node": "left_estrogen",
            "source": "LF outer bottom",
            "status": "wired_active",
            "used_in": "window_boost",
        },
        {
            "node": "vasopressin_female",
            "source": "frontals swap logic",
            "status": "wired_active",
            "used_in": "window_boost + lensing tightening",
        },
        {
            "node": "left_frontalis_d2",
            "source": "LF outer top",
            "status": "wired_active",
            "used_in": "transfer_efficiency",
        },
        {
            "node": "right_androgen",
            "source": "drive / alpha2 family",
            "status": "wired_active",
            "used_in": "damping_release",
        },
        {
            "node": "left_endorphin",
            "source": "alpha2 family",
            "status": "wired_active",
            "used_in": "noise_quench",
        },
        {
            "node": "right_5ht1b_synchrotron",
            "source": "temporalis right bus",
            "status": "wired_passive",
            "used_in": "passive_synchrotron + lensing suppression + BM_to_SW bleed",
        },
        {
            "node": "male_left_5ht",
            "source": "left 5ht",
            "status": "wired_passive",
            "used_in": "passive_serotonin on interaction_total and stimulated_delta",
        },
        {
            "node": "female_left_noradrenaline",
            "source": "left noradrenaline",
            "status": "wired_passive",
            "used_in": "passive_noradrenaline on BW/container and quark lift",
        },
    ]

    coupling_terms = [
        {
            "term": "PHOTOELECTRIC gain",
            "formula": "(1 + gate-based node couplings) * q_scale * window_boost",
            "status": "structural",
            "risk": "no raw amplitude feedback",
        },
        {
            "term": "BREMSSTRAHLUNG gain",
            "formula": "(1 + gate-based node couplings) * e_scale * damping_release * noise_quench",
            "status": "structural",
            "risk": "no raw amplitude feedback",
        },
        {
            "term": "BETA_DECAY gain",
            "formula": "(1 + gate-based node couplings) * n_scale * lateral_bias",
            "status": "structural",
            "risk": "no raw amplitude feedback",
        },
    ]

    payload = {
        "summary": {
            "discrete_structure": "present",
            "continuous_structure": "present",
            "real_closure": "present",
            "score_structure_confusion": "0.8009 is score, not physics constant",
            "main_gap": "main operator now wires explicit passive no_control fields; remaining gaps are 16-window timing, full 6-state independence, and removing heuristic coefficients",
        },
        "constant_checks": constant_checks,
        "node_checks": node_checks,
        "coupling_terms": coupling_terms,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Structure Crosscheck",
        "",
        "## Summary",
        "- discrete / continuous / real split: `present in current sovereign_dynamics_step`",
        "- 0.8009: `score, not structure constant`",
        "- main issue: `explicit passive no_control fields are now wired; remaining gaps are timing granularity, full 6-state independence, and heuristic coefficients`",
        "",
        "## Constants",
    ]
    for row in constant_checks:
        note = f" | note: {row['note']}" if "note" in row else ""
        lines.append(
            f"- `{row['name']}` [{row['domain']}] -> `{row['status']}` via `{row['used_in']}` ({row['meaning']}){note}"
        )

    lines.extend(["", "## Nodes"])
    for row in node_checks:
        note = f" | note: {row['note']}" if "note" in row else ""
        lines.append(
            f"- `{row['node']}` -> `{row['status']}` via `{row['used_in']}` ({row['source']}){note}"
        )

    lines.extend(["", "## Coupling Terms"])
    for row in coupling_terms:
        lines.append(
            f"- `{row['term']}` -> `{row['formula']}` | `{row['status']}` | risk: `{row['risk']}`"
        )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
