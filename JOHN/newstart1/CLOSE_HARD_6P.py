import json
from datetime import datetime
from itertools import product

import numpy as np
import pandas as pd

from fusion_clean import OMEGA, F_final, get_dynamics
from sovereign_128 import (
    get_channels,
    apply_channels,
    laplacian,
    day_target,
    night_target,
    init_state6_from_target4,
)


def adapt_controls(ts, x_state, base_ts):
    norm_x = float(np.linalg.norm(x_state))
    closure_error = abs(norm_x - OMEGA)
    alpha2 = float(ts.get("alpha2", 1.0))
    vasopressin = float(ts.get("vasopressin", 0.0))
    gaba_b = float(ts.get("gaba_b", 0.0))
    base_alpha2 = float(base_ts.get("alpha2", alpha2))
    base_vasopressin = float(base_ts.get("vasopressin", vasopressin))
    base_gaba_b = float(base_ts.get("gaba_b", gaba_b))

    error_drive = max(closure_error - 0.08, 0.0)
    emergency = closure_error > 0.30
    if emergency:
        alpha2_next = np.clip(alpha2 - 0.55 * np.tanh(error_drive), 0.0, 1.0)
        vasopressin_next = np.clip(vasopressin + 0.45 * np.tanh(error_drive), 0.0, 1.0)
        gaba_b_next = np.clip(gaba_b + 0.30 * np.tanh(error_drive), 0.0, 1.0)
    else:
        alpha2_next = np.clip(alpha2 - 0.28 * np.tanh(error_drive), 0.0, 1.0)
        vasopressin_next = np.clip(vasopressin + 0.22 * np.tanh(error_drive), 0.0, 1.0)
        gaba_b_next = np.clip(gaba_b + 0.14 * np.tanh(error_drive), 0.0, 1.0)

    if closure_error < 0.08:
        alpha2_next += 0.20 * (base_alpha2 - alpha2_next)
        vasopressin_next += 0.20 * (base_vasopressin - vasopressin_next)
        gaba_b_next += 0.20 * (base_gaba_b - gaba_b_next)

    ts_next = dict(ts)
    ts_next["alpha2"] = float(alpha2_next)
    ts_next["vasopressin"] = float(vasopressin_next)
    ts_next["gaba_b"] = float(gaba_b_next)
    ts_next["closure_error"] = float(closure_error)
    return ts_next


def apply_periodic_seam_lock(trajectory):
    if not trajectory:
        return trajectory, 0.0, 0.0
    n = len(trajectory)
    start = trajectory[0]
    end = trajectory[-1]
    delta = end - start
    before = float(np.linalg.norm(delta))
    if n == 1:
        return trajectory, before, before
    corrected = []
    for idx, state in enumerate(trajectory):
        alpha = idx / float(n - 1)
        corrected.append(state - alpha * delta)
    after = float(np.linalg.norm(corrected[-1] - corrected[0]))
    return corrected, before, after


def compute_recovery_windows(errors, trigger=0.16, recover=0.08):
    events = []
    n = len(errors)
    i = 0
    while i < n:
        if errors[i] <= trigger:
            i += 1
            continue
        j = i
        while j < n and errors[j] > recover:
            j += 1
        events.append(j - i if j < n else n - i)
        i = j + 1
    return events


def simulate(params, build_map=False):
    steps = 128
    elements = 128
    substeps = int(params["substeps"])
    dt = float(params["dt"])
    radial_lock = float(params["radial_lock"])
    emergency_gain = float(params["emergency_gain"])
    dx_norm_max = float(params["dx_norm_max"])
    omega_band = float(params["omega_band"])

    t4_day = day_target()
    t4_night = night_target()
    x = init_state6_from_target4(t4_day)

    trajectory = []
    ts_by_window = []
    closure_errors = []
    control_state = None

    for w in range(steps):
        ch = get_channels(w)
        wts = apply_channels(ch)
        L = laplacian(wts)
        is_night = (w < 36) or (w >= 104)
        x_att = init_state6_from_target4(t4_night if is_night else t4_day)
        gaba_b_female = 1.0 if ch.get("female_gaba_b_latdorsi") == "on" else 0.0
        gaba_b_male = 1.0 if ch.get("male_gaba_b") == "on" else 0.0
        vaso_state = ch.get("vasopressin_female", "off")

        base_ts = {
            "nu_p_coupling": wts.get(("neutrino", "proton"), 0.5),
            "nu_e_coupling": wts.get(("neutrino", "electron"), 0.5),
            "gamma_p_coupling": wts.get(("photon", "proton"), 0.5),
            "nu_q_coupling": wts.get(("neutrino", "quark"), 0.5),
            "vasopressin": 1.0 if vaso_state == "on" else (0.5 if vaso_state == "no_control" else 0.0),
            "glucocorticoid": 1.0 if ch.get("glucocorticoid") == "on" else 0.0,
            "right_cortisol": 1.0 if ch.get("right_cortisol") == "on" else 0.0,
            "right_extraversion": 1.0 if ch.get("right_extraversion") == "on" else 0.0,
            "alpha2": 0.0 if ch.get("right_alpha_2") == "off" else 1.0,
            "gaba_b_female": gaba_b_female,
            "gaba_b_male": gaba_b_male,
            "gaba_b": max(gaba_b_female, gaba_b_male),
            "time_window": w,
            "w_parameter": w / 127.0,
        }
        if control_state is None:
            control_state = {
                "alpha2": base_ts["alpha2"],
                "vasopressin": base_ts["vasopressin"],
                "gaba_b": base_ts["gaba_b"],
            }
        ts_in = dict(base_ts)
        ts_in.update(control_state)

        for _ in range(substeps):
            dx = get_dynamics(x, L, float(w + 1), ts_in)
            dx_norm = np.linalg.norm(dx)
            if dx_norm > dx_norm_max:
                dx = dx * (dx_norm_max / (dx_norm + 1e-9))
            x = x + dt * dx
            norm_x = np.linalg.norm(x)
            if norm_x > 1e-9:
                target = OMEGA * (x / norm_x)
                closure_error = abs(float(norm_x) - OMEGA)
                lock_strength = radial_lock + emergency_gain * np.tanh(max(closure_error - 0.10, 0.0))
                x = (1.0 - lock_strength) * x + lock_strength * target
                norm_post = np.linalg.norm(x)
                max_band = OMEGA + omega_band
                min_band = OMEGA - omega_band
                if norm_post > max_band:
                    x = x * (max_band / (norm_post + 1e-9))
                elif norm_post < min_band and norm_post > 1e-9:
                    x = x * (min_band / norm_post)
            x = np.clip(x, -50.0, 50.0)

        x = 0.92 * x + 0.08 * x_att
        ts_out = adapt_controls(ts_in, x, base_ts)
        control_state = {
            "alpha2": 0.75 * ts_out["alpha2"] + 0.25 * base_ts["alpha2"],
            "vasopressin": 0.75 * ts_out["vasopressin"] + 0.25 * base_ts["vasopressin"],
            "gaba_b": 0.75 * ts_out["gaba_b"] + 0.25 * base_ts["gaba_b"],
        }

        trajectory.append(x.copy())
        ts_by_window.append(ts_out)
        closure_errors.append(ts_out["closure_error"])

    trajectory, periodic_before, periodic_after = apply_periodic_seam_lock(trajectory)
    recovery = compute_recovery_windows(closure_errors)
    mean_err = float(np.mean(closure_errors))
    max_err = float(np.max(closure_errors))
    p95_err = float(np.percentile(closure_errors, 95))
    avg_recovery = float(np.mean(recovery)) if recovery else 0.0
    tail_risk = float(np.mean(np.array(closure_errors) > 0.28))
    score = (
        mean_err
        + 0.6 * max_err
        + 0.35 * p95_err
        + 0.08 * avg_recovery
        + 2.5 * tail_risk
        + 8.0 * periodic_after
    )

    result = {
        "score": float(score),
        "mean_closure_error": mean_err,
        "max_closure_error": max_err,
        "p95_closure_error": p95_err,
        "periodic_error_l2_before_lock": float(periodic_before),
        "periodic_error_l2_after_lock": float(periodic_after),
        "tail_risk_ratio": tail_risk,
        "avg_recovery_windows": avg_recovery,
        "max_recovery_windows": int(max(recovery)) if recovery else 0,
    }

    if not build_map:
        return result, None

    z_map = np.zeros((steps, elements), dtype=float)
    for w in range(steps):
        x_state = trajectory[w]
        ts = ts_by_window[w]
        for z_idx in range(elements):
            z_map[w, z_idx] = F_final(x_state, float(z_idx + 1), ts)
    return result, z_map


def main():
    param_grid = {
        "substeps": [22, 24, 26],
        "dt": [0.018, 0.020],
        "radial_lock": [0.08, 0.10, 0.12],
        "emergency_gain": [0.18, 0.22, 0.26],
        "dx_norm_max": [2.2, 2.5],
        "omega_band": [0.45, 0.55],
    }
    keys = list(param_grid.keys())
    best_params = None
    best_result = None

    print(" [SEARCH] Running hard-closure parameter search...")
    for values in product(*(param_grid[key] for key in keys)):
        params = dict(zip(keys, values))
        result, _ = simulate(params, build_map=False)
        if best_result is None or result["score"] < best_result["score"]:
            best_result = result
            best_params = params

    print(f" [SEARCH] Best params: {best_params}")
    final_result, z_map = simulate(best_params, build_map=True)

    df = pd.DataFrame(z_map)
    output_csv = "SOVEREIGN_128x128_Z_MAP_CLOSED.csv"
    try:
        df.to_csv(output_csv, index=False, header=False)
    except PermissionError:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"SOVEREIGN_128x128_Z_MAP_CLOSED_{stamp}.csv"
        df.to_csv(output_csv, index=False, header=False)
        print(f" [WARN] Base CSV locked. Wrote fallback: {output_csv}")

    report = {
        "model": "6P-hard-closure",
        "best_params": best_params,
        "metrics": final_result,
        "output_csv": output_csv,
    }
    with open("SOVEREIGN_HARD_CLOSURE_REPORT.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f" [SUCCESS] Output map: {output_csv}")
    print(" [SUCCESS] Report: SOVEREIGN_HARD_CLOSURE_REPORT.json")


if __name__ == "__main__":
    main()
