from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from fusion_clean import (
    C,
    OMEGA,
    ENTROPY_DEBT,
    CHANNEL_MAP,
    apply_channels,
    laplacian,
    project4,
    day_target,
    night_target,
    init_state6_from_target4,
    continuous_spark_gate,
)


N_WINDOWS = 128
MIN_PER_WIN = 24 * 60 / N_WINDOWS
SUBSTEPS = 30
DT = 0.015
ATTRACTOR_K = 0.0003

DEFAULT_SUBJECT_PROFILE = "general_user"
CONTROL_CAPABILITY = {
    "general_user": {"male_gaba_b": "indirect", "right_extraversion": "direct"},
    "john_subject": {"male_gaba_b": "direct", "right_extraversion": "direct"},
}

CHANNELS_ALL = list(CHANNEL_MAP.keys())


def window_to_hhmm(w: int) -> str:
    total = w * MIN_PER_WIN
    return f"{int(total // 60):02d}:{int(total % 60):02d}"


def get_channels(
    w: int,
    subject_profile: str | None = None,
    subject_overrides: dict[str, str] | None = None,
) -> dict[str, str]:
    profile = subject_profile or DEFAULT_SUBJECT_PROFILE
    ch: dict[str, str] = {key: "no_control" for key in CHANNELS_ALL}

    is_night = (w < 36) or (w >= 104)
    in_hysteresis = 12 <= w <= 24
    in_phase2 = 48 <= w <= 56
    in_phase1 = 80 <= w <= 88

    if in_phase1:
        ch["gdh_gluon"] = "on"
    elif in_hysteresis:
        ch["gdh_gluon"] = "off"

    ch["female_gaba_b_latdorsi"] = "on" if in_hysteresis else ("off" if not is_night else "no_control")
    ch["left_acetyl_coa"] = "on" if (in_phase1 or in_phase2) else ("off" if in_hysteresis else "no_control")
    ch["male_left_5ht"] = "on" if in_hysteresis else ("off" if not is_night else "no_control")
    ch["female_left_noradrenaline"] = "on" if in_phase1 else ("off" if is_night else "no_control")
    ch["left_temporalis_5ht1a"] = "on" if (not is_night and not in_phase1) else ("off" if is_night else "no_control")
    ch["left_estrogen"] = "on" if (in_hysteresis or w >= 104) else ("off" if not is_night else "no_control")
    ch["right_love"] = "on" if (w >= 96 or w < 24) else "off"
    ch["hypoxia"] = "off"
    ch["right_dopamine"] = "on" if (37 <= w <= 59) else ("off" if is_night else "no_control")
    ch["vasopressin_female"] = "on" if (in_phase1 or is_night) else ("off" if in_phase2 else "no_control")

    ch["male_oxytocin"] = "on" if (w >= 104 or w < 32) else "off"
    if ch["male_oxytocin"] == "on":
        ch["vasopressin_female"] = "on"
    elif ch["vasopressin_female"] == "no_control":
        ch["vasopressin_female"] = "no_control"

    ch["muscle_a"] = "on" if in_phase1 else ("off" if (in_phase2 or in_hysteresis) else "no_control")
    ch["muscle_b"] = "on" if in_phase2 else ("off" if in_phase1 else "no_control")
    ch["right_androgen"] = "on" if (in_phase2 or (64 <= w <= 104)) else ("off" if in_hysteresis else "no_control")
    ch["left_endorphin"] = "on" if (88 <= w <= 104) else ("off" if not is_night else "no_control")
    ch["left_frontalis_d2"] = "on" if (in_phase1 or in_phase2) else ("off" if in_hysteresis else "no_control")
    ch["right_occipitalis_gaba_a"] = "on" if in_hysteresis else ("off" if not is_night else "no_control")
    ch["right_acetylcholine"] = "on" if (in_phase2 or (24 <= w <= 36)) else ("off" if in_phase1 else "no_control")
    ch["left_extraversion"] = "off" if is_night else "on"
    ch["right_extraversion"] = "on" if (48 <= w <= 56 or 64 <= w <= 100) else "off"
    ch["glucocorticoid"] = "on" if (32 <= w <= 56) else ("off" if is_night else "no_control")
    ch["right_cortisol"] = "on" if (32 <= w <= 56 or in_phase1) else "off"
    ch["right_alpha_2"] = "off" if (in_phase2 or in_hysteresis or w >= 104 or w < 12) else "on"
    ch["male_gaba_b"] = "on" if (w < 32 or w >= 104) else "off"

    capabilities = CONTROL_CAPABILITY.get(profile, CONTROL_CAPABILITY["general_user"])
    if capabilities.get("male_gaba_b") != "direct":
        ch["male_gaba_b"] = "on" if in_hysteresis else "off"
    if subject_overrides:
        for key, value in subject_overrides.items():
            if capabilities.get(key) == "direct" and value in {"on", "off", "no_control"}:
                ch[key] = value
    return ch


def integrate_one_window(x: np.ndarray, L: np.ndarray, x_att: np.ndarray) -> np.ndarray:
    for _ in range(SUBSTEPS):
        dx = -(L @ x) + ATTRACTOR_K * (x_att - x)
        x = x + DT * dx
        x = np.clip(x, 1e-8, 50.0)
    return x


def spark_phase_gate(z_proxy: float, alpha2_state: str, ts: dict[str, Any]) -> tuple[float, float]:
    return continuous_spark_gate(z_proxy, alpha2_state, ts)


def run_sovereign(age: float = 25.0, verbose: bool = True) -> dict[str, Any]:
    schedule = [get_channels(w) for w in range(N_WINDOWS)]

    t4_day = day_target()
    t4_night = night_target()
    x = init_state6_from_target4(t4_day)
    x0 = x.copy()
    x4_t0 = project4(x0)
    omega0 = float(np.linalg.norm(x4_t0))

    history: list[dict[str, Any]] = []
    for w in range(N_WINDOWS):
        ch = schedule[w]
        wts = apply_channels(ch, age=age)
        L = laplacian(wts)
        is_night = (w < 36) or (w >= 104)
        x_att = init_state6_from_target4(t4_night if is_night else t4_day)
        x = integrate_one_window(x, L, x_att)

        x4 = project4(x)
        bm, bw, sm, sw = x4
        spark = wts.get(("photon", "proton"), 0.0) + wts.get(("photon", "electron"), 0.0)
        z_proxy = wts.get(("neutrino", "proton"), 0.0) + wts.get(("neutrino", "electron"), 0.0)
        phase, gate = spark_phase_gate(
            z_proxy,
            ch.get("right_alpha_2", "on"),
            {"noradrenaline": 5.0 / 32.0, "vasopressin": 3.0 / 32.0},
        )
        spark_eff = spark * gate
        fusion = float((bw**2) * spark_eff * z_proxy * sm * (1.0 - ENTROPY_DEBT))
        history.append(
            {
                "w": w,
                "time": window_to_hhmm(w),
                "BM": float(bm),
                "BW": float(bw),
                "SM": float(sm),
                "SW": float(sw),
                "omega4": float(np.linalg.norm(x4)),
                "spark": float(spark),
                "spark_phase": float(phase),
                "spark_gate": float(gate),
                "spark_eff": float(spark_eff),
                "z_proxy": float(z_proxy),
                "fusion": float(fusion),
            }
        )

    x4_final = project4(x)
    err_6d = float(np.linalg.norm(x - x0))
    err_4d = float(np.linalg.norm(x4_final - x4_t0))
    omega_fin = float(np.linalg.norm(x4_final))
    omega_err = float(omega_fin - OMEGA)

    def avg(key: str, lo: int, hi: int) -> float:
        pts = [h[key] for h in history if lo <= h["w"] <= hi]
        return float(np.mean(pts)) if pts else 0.0

    metrics = {
        "omega_start": omega0,
        "omega_end": omega_fin,
        "omega_err": omega_err,
        "periodic_err_6d": err_6d,
        "periodic_err_4d": err_4d,
        "phase2_spark_eff": avg("spark_eff", 48, 56),
        "phase2_z_proxy": avg("z_proxy", 48, 56),
        "phase1_bw": avg("BW", 80, 88),
        "hysteresis_sm": avg("SM", 12, 24),
    }
    out = {"metrics": metrics, "history": history, "age": float(age), "n_windows": N_WINDOWS}
    if verbose:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return out


def main() -> None:
    result = run_sovereign(age=25.0, verbose=True)
    out_path = Path("analysis_results") / "sovereign_128_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result["metrics"], ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()

