import json
from datetime import datetime

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


def build_ts(ch, wts, window_idx):
    gaba_b_female = 1.0 if ch.get("female_gaba_b_latdorsi") == "on" else 0.0
    gaba_b_male = 1.0 if ch.get("male_gaba_b") == "on" else 0.0
    vaso_state = ch.get("vasopressin_female", "off")
    return {
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
        "time_window": int(window_idx),
        "w_parameter": float(window_idx) / 127.0,
    }


def simulate_period(
    x0,
    dt=0.018,
    substeps=24,
    k_anchor=0.5,
    attractor_k=0.0003,
):
    steps = 128
    t4_day = day_target()
    t4_night = night_target()
    x = np.array(x0, dtype=float)
    trajectory = []
    ts_windows = []
    closure_errors = []

    for w in range(steps):
        ch = get_channels(w)
        wts = apply_channels(ch)
        L = laplacian(wts)
        is_night = (w < 36) or (w >= 104)
        x_att = init_state6_from_target4(t4_night if is_night else t4_day)
        ts = build_ts(ch, wts, w)

        for _ in range(substeps):
            dx = get_dynamics(x, L, float(w + 1), ts, k=k_anchor)
            dx += attractor_k * (x_att - x)
            x = x + dt * dx
            if not np.all(np.isfinite(x)):
                return None, None, None
            x = np.clip(x, -1e3, 1e3)

        trajectory.append(x.copy())
        ts_windows.append(ts)
        closure_errors.append(abs(float(np.linalg.norm(x)) - OMEGA))

    return trajectory, ts_windows, closure_errors


def find_periodic_orbit(
    init_x0,
    dt=0.018,
    substeps=24,
    k_anchor=0.5,
    attractor_k=0.0003,
    relax=0.55,
    max_iters=36,
    tol=1e-4,
):
    x0 = np.array(init_x0, dtype=float)
    history = []
    best = None

    for i in range(max_iters):
        traj, ts_windows, errs = simulate_period(
            x0, dt=dt, substeps=substeps, k_anchor=k_anchor, attractor_k=attractor_k
        )
        if traj is None:
            break
        x_end = traj[-1]
        delta = x_end - x0
        periodic_error = float(np.linalg.norm(delta))
        mean_err = float(np.mean(errs))
        max_err = float(np.max(errs))
        score = periodic_error + 0.35 * mean_err + 0.10 * max_err
        history.append(
            {
                "iter": i,
                "score": score,
                "periodic_error": periodic_error,
                "mean_err": mean_err,
                "max_err": max_err,
            }
        )
        if best is None or score < best["score"]:
            best = {
                "score": score,
                "x0": x0.copy(),
                "traj": traj,
                "ts_windows": ts_windows,
                "errs": errs,
                "periodic_error": periodic_error,
                "mean_err": mean_err,
                "max_err": max_err,
            }

        if periodic_error < tol:
            break
        x0 = x0 + relax * delta

    return best, history


def build_z_map(trajectory, ts_windows):
    steps = 128
    elements = 128
    z_map = np.zeros((steps, elements), dtype=float)
    for w in range(steps):
        x_state = trajectory[w]
        ts = ts_windows[w]
        for z_idx in range(elements):
            z_map[w, z_idx] = F_final(x_state, float(z_idx + 1), ts)
    return z_map


def main():
    init_x0 = init_state6_from_target4(day_target())
    params = {
        "dt": 0.006,
        "substeps": 32,
        "k_anchor": 3.0,
        "attractor_k": 0.05,
        "relax": 0.55,
        "max_iters": 30,
        "tol": 1e-5,
    }
    best, history = find_periodic_orbit(
        init_x0=init_x0,
        dt=params["dt"],
        substeps=params["substeps"],
        k_anchor=params["k_anchor"],
        attractor_k=params["attractor_k"],
        relax=params["relax"],
        max_iters=params["max_iters"],
        tol=params["tol"],
    )
    if best is None:
        raise RuntimeError("Autonomous closure search failed (unstable trajectory).")

    z_map = build_z_map(best["traj"], best["ts_windows"])
    df = pd.DataFrame(z_map)
    output_csv = "SOVEREIGN_128x128_Z_MAP_AUTOCLOSE.csv"
    try:
        df.to_csv(output_csv, index=False, header=False)
    except PermissionError:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"SOVEREIGN_128x128_Z_MAP_AUTOCLOSE_{stamp}.csv"
        df.to_csv(output_csv, index=False, header=False)

    report = {
        "model": "6P-autonomous-closure",
        "params": params,
        "periodic_error_l2": best["periodic_error"],
        "mean_closure_error": best["mean_err"],
        "max_closure_error": best["max_err"],
        "iterations": len(history),
        "score": best["score"],
        "output_csv": output_csv,
        "iter_history_tail": history[-5:],
    }
    with open("SOVEREIGN_AUTOCLOSE_REPORT.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f" [SUCCESS] AUTONOMOUS OUTPUT: {output_csv}")
    print(" [SUCCESS] REPORT: SOVEREIGN_AUTOCLOSE_REPORT.json")


if __name__ == "__main__":
    main()
