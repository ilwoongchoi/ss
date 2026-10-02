import json
from datetime import datetime

import numpy as np
import pandas as pd

from sovereign_128 import get_channels
from fusion_pqn import OMEGA, integrate_window, pqn_potential, spark_scalar


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


def compute_recovery_windows(errors, trigger=0.18, recover=0.08):
    events = []
    i = 0
    n = len(errors)
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


def generate_pqn_grid():
    steps = 128
    elements = 128
    x = np.array([OMEGA / np.sqrt(3.0), OMEGA / np.sqrt(3.0), OMEGA / np.sqrt(3.0)], dtype=float)

    trajectory = []
    channels_by_window = []
    closure_errors = []
    spark_series = []
    vaso_spark = []
    non_vaso_spark = []

    print(" [STAGE 1] PQN trajectory integration...")
    for window_idx in range(steps):
        channels = get_channels(window_idx)
        z_driver = float(window_idx + 1)
        x = integrate_window(x, channels, z_driver, window_idx)
        trajectory.append(x.copy())
        channels_by_window.append(channels)

        err = abs(float(np.linalg.norm(x)) - OMEGA)
        closure_errors.append(err)

        spark_val = spark_scalar(channels, z_driver, window_idx)
        spark_series.append(spark_val)
        if channels.get("vasopressin_female") == "on":
            vaso_spark.append(spark_val)
        else:
            non_vaso_spark.append(spark_val)

    trajectory, periodic_before, periodic_after = apply_periodic_seam_lock(trajectory)

    print(" [STAGE 2] Building 128x128 PQN potential map...")
    z_map = np.zeros((steps, elements), dtype=float)
    for w in range(steps):
        channels = channels_by_window[w]
        state = trajectory[w]
        for z_idx in range(elements):
            z_atomic = float(z_idx + 1)
            z_map[w, z_idx] = pqn_potential(state, channels, z_atomic, w)

    print(" [STAGE 3] Writing outputs...")
    df = pd.DataFrame(z_map)
    output_csv = "SOVEREIGN_PQN_128x128_Z_MAP.csv"
    try:
        df.to_csv(output_csv, index=False, header=False)
    except PermissionError:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"SOVEREIGN_PQN_128x128_Z_MAP_{stamp}.csv"
        df.to_csv(output_csv, index=False, header=False)
        print(f" [WARN] Base CSV locked. Wrote fallback: {output_csv}")

    recovery = compute_recovery_windows(closure_errors)
    report = {
        "model": "PQN-only",
        "mean_closure_error": float(np.mean(closure_errors)),
        "max_closure_error": float(np.max(closure_errors)),
        "min_closure_error": float(np.min(closure_errors)),
        "periodic_error_l2_before_lock": periodic_before,
        "periodic_error_l2_after_lock": periodic_after,
        "spark_mean": float(np.mean(spark_series)),
        "spark_peak_window": int(np.argmax(spark_series)),
        "spark_peak_value": float(np.max(spark_series)),
        "spark_mean_when_vasopressin_on": float(np.mean(vaso_spark)) if vaso_spark else 0.0,
        "spark_mean_when_vasopressin_off": float(np.mean(non_vaso_spark)) if non_vaso_spark else 0.0,
        "spark_abs_mean_when_vasopressin_on": float(np.mean(np.abs(vaso_spark))) if vaso_spark else 0.0,
        "spark_abs_mean_when_vasopressin_off": float(np.mean(np.abs(non_vaso_spark))) if non_vaso_spark else 0.0,
        "spark_abs_peak_when_vasopressin_on": float(np.max(np.abs(vaso_spark))) if vaso_spark else 0.0,
        "spark_abs_peak_when_vasopressin_off": float(np.max(np.abs(non_vaso_spark))) if non_vaso_spark else 0.0,
        "recovery_event_count": int(len(recovery)),
        "recovery_avg_windows": float(np.mean(recovery)) if recovery else 0.0,
        "recovery_max_windows": int(max(recovery)) if recovery else 0,
    }
    with open("SOVEREIGN_PQN_CLOSURE_REPORT.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f" [SUCCESS] PQN map generated: {output_csv}")
    print(" [SUCCESS] Report: SOVEREIGN_PQN_CLOSURE_REPORT.json")


if __name__ == "__main__":
    generate_pqn_grid()
