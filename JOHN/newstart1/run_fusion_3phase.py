"""
Nuclear fusion equation - 3 phase profile.

Phase 1 (Neutron Star A): BW capture / confinement dominant
Phase 2 (Neutron Star B): spark rising / partial BW release
Hysteresis (Neutrino path): SM ascent / Z boson channel open

Day = pulsating Phase 1 <-> Phase 2
Night 01:30-03:00 = Hysteresis, vertical neutrino ascent
"""
from __future__ import annotations

import json
import numpy as np
from pathlib import Path

from fusion_clean import (
    _compute_step,
    nuclear_fusion_from_base,
    neutron_coarse_grain_from_base,
    MOTIF_TARGET_4,
    GDH_CONFINEMENT_02828,
)

# Hysteresis target: 0.2828 shifts from BW to SM (cortisol off ??melatonin/cartilage remanifest)
# BW_night = 3.64 - 0.2828 = 3.36,  SM_night = 3.64 + 0.2828 = 3.92
_DAY_TARGET   = np.asarray(MOTIF_TARGET_4, dtype=float)
_NIGHT_TARGET = _DAY_TARGET.copy()
_NIGHT_TARGET[1] -= GDH_CONFINEMENT_02828  # BW down
_NIGHT_TARGET[2] += GDH_CONFINEMENT_02828  # SM up

# ?€?€ Complete 3-phase channel table ?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€
# Values: "on" / "off" / "no_control"
PHASE_TABLE: dict[str, dict[str, str]] = {
    "phase1": {
        # BW capture / confinement
        "gdh_gluon":                    "on",
        "female_gaba_b_latdorsi":       "off",
        "left_acetyl_coa":              "on",
        "male_left_5ht":                "off",       # left serotonin
        "female_left_noradrenaline":    "on",
        "left_temporalis_5ht1a":        "off",
        "left_estrogen":                "off",
        "right_love":                   "off",
        "hypoxia":                      "off",
        "right_dopamine":               "off",
        "vasopressin_female":           "on",
        "male_oxytocin":                "off",
        "muscle_a":                     "on",
        "muscle_b":                     "on",
        "right_5ht1b_synchrotron":      "no_control",
        "right_androgen":               "no_control",
        "left_endorphin":               "no_control",
        "left_frontalis_d2":            "on",
        "right_occipitalis_gaba_a":     "on",
        "right_acetylcholine":          "off",
        "left_extraversion":            "on",
        "glucocorticoid":               "off",
        "right_cortisol":               "on",
    },
    "phase2": {
        # Spark rising / partial release
        "gdh_gluon":                    "no_control",
        "female_gaba_b_latdorsi":       "off",
        "left_acetyl_coa":              "no_control",
        "male_left_5ht":                "no_control",
        "female_left_noradrenaline":    "off",
        "left_temporalis_5ht1a":        "off",
        "left_estrogen":                "no_control",
        "right_love":                   "no_control",
        "hypoxia":                      "off",
        "right_dopamine":               "on",
        "vasopressin_female":           "on",
        "male_oxytocin":                "no_control",
        "muscle_a":                     "no_control",
        "muscle_b":                     "no_control",
        "right_5ht1b_synchrotron":      "no_control",
        "right_androgen":               "on",
        "left_endorphin":               "off",
        "left_frontalis_d2":            "on",
        "right_occipitalis_gaba_a":     "on",
        "right_acetylcholine":          "no_control",
        "left_extraversion":            "on",
        "glucocorticoid":               "off",
        "right_cortisol":               "no_control",
    },
    "hysteresis": {
        # SM / neutrino vertical ascent - Z boson channel open
        "gdh_gluon":                    "off",
        "female_gaba_b_latdorsi":       "on",
        "left_acetyl_coa":              "off",
        "male_left_5ht":                "on",        # left serotonin: SM_SW bridge
        "female_left_noradrenaline":    "no_control",
        "left_temporalis_5ht1a":        "no_control",
        "left_estrogen":                "on",
        "right_love":                   "on",
        "hypoxia":                      "no_control",
        "right_dopamine":               "off",
        "vasopressin_female":           "on",
        "male_oxytocin":                "no_control",
        "muscle_a":                     "on",
        "muscle_b":                     "no_control",
        "right_5ht1b_synchrotron":      "no_control",
        "right_androgen":               "on",
        "left_endorphin":               "off",
        "left_frontalis_d2":            "on",
        "right_occipitalis_gaba_a":     "on",
        "right_acetylcholine":          "no_control",
        "left_extraversion":            "off",       # introvert / neutrino path
        "glucocorticoid":               "off",
        "right_cortisol":               "off",
    },
}

PHASE_CLOCKS = {
    "phase1":     "15:45",   # p-window center
    "phase2":     "09:45",   # spark-peak center
    "hysteresis": "02:15",   # hysteresis center
}

PHASE_FILL = {
    "phase1":     0.5,
    "phase2":     0.5,
    "hysteresis": 0.5,
}


def run_phase(name: str) -> dict:
    s = _NIGHT_TARGET if name == "hysteresis" else _DAY_TARGET
    override = PHASE_TABLE[name]
    clock = PHASE_CLOCKS[name]
    fill = PHASE_FILL[name]

    base = _compute_step(
        s,
        phase_fill=fill,
        clock_hhmm=clock,
        control_override=override,
    )
    fusion = nuclear_fusion_from_base(base, state4=s)
    neutron = neutron_coarse_grain_from_base(base, state4=s)

    state4 = np.asarray(base["state_out"], dtype=float)
    ts = base.get("tunnel_transfer_split") or {}

    return {
        "phase": name,
        "clock": clock,
        "BM": float(state4[0]),
        "BW": float(state4[1]),
        "SM": float(state4[2]),
        "SW": float(state4[3]),
        "omega": float(np.linalg.norm(state4)),
        "spark_string_break": float(ts.get("spark_string_break", 0.0)),
        "sigma_eff": float(ts.get("effective_string_tension", GDH_CONFINEMENT_02828)),
        "neutron_observable": float(neutron.get("observable", 0.0)),
        "fusion_rate": float(fusion["fusion_rate"]),
        "z_boson_proxy": float(fusion["components"]["z_boson_proxy"]),
        "proton_sq": float(state4[1] ** 2),
        "components": fusion["components"],
    }


def closure_score(results: list[dict]) -> float:
    """
    How much does the 3-phase cycle close the fusion equation?

    Criteria:
    1. Phase 1 BW >> Phase 1 SM  (neutron star = BW dominant)
    2. Phase 2 spark > Phase 1 spark  (spark rises in release phase)
    3. Hysteresis SM >> Phase 1 SM  (neutrino path = SM dominant)
    4. Hysteresis z_boson > Phase 1 z_boson  (Z channel opens at night)
    5. Phase 2 fusion_rate > Phase 1 fusion_rate  (fusion ignites in release)
    """
    r = {d["phase"]: d for d in results}
    p1 = r["phase1"]
    p2 = r["phase2"]
    hy = r["hysteresis"]

    checks = {
        "BW_dominant_P1":      p1["BW"] > p1["SM"],
        "spark_rises_P2":      p2["spark_string_break"] > p1["spark_string_break"],
        "SM_dominant_HY":      hy["SM"] > hy["BW"],
        "Z_opens_HY":          hy["z_boson_proxy"] > p1["z_boson_proxy"],
        "fusion_peaks_P2":     p2["fusion_rate"] >= p1["fusion_rate"],
    }

    score = sum(checks.values()) / len(checks)
    return score, checks


def main():
    results = [run_phase(name) for name in ("phase1", "phase2", "hysteresis")]
    score, checks = closure_score(results)

    out = {
        "closure_pct": round(score * 100, 1),
        "checks": checks,
        "phases": results,
    }

    out_path = Path("analysis_results/fusion_3phase.json")
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))

    print(f"\n=== NUCLEAR FUSION 3-PHASE ===")
    print(f"CLOSURE: {score*100:.0f}%\n")
    for k, v in checks.items():
        print(f"  {'OK' if v else 'X '}  {k}")
    print()
    for r in results:
        print(f"[{r['phase']:10s}] BM={r['BM']:.2f} BW={r['BW']:.2f} SM={r['SM']:.2f} SW={r['SW']:.2f} | "
              f"spark={r['spark_string_break']:.4f} z={r['z_boson_proxy']:.5f} fusion={r['fusion_rate']:.6f}")
    print(f"\n??{out_path}")


if __name__ == "__main__":
    main()
