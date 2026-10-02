import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent

RENDER_SCRIPT = ROOT / "generate_128_grid_v4_hysteresis_pure.py"
RENDER_EVENTS = ROOT / "flash_events_render.json"

ANGLE_SUMMARY = ROOT / "out" / "h3_h4_d3_residuals" / "flash_angle_summary.json"
RENORM_SUMMARY = ROOT / "out" / "h3_h4_d3_residuals" / "flash_renorm_summary.json"
CLOSURE_CSV = ROOT / "out" / "h3_h4_d3_residuals" / "closure_point_comparison.csv"


def die(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def main() -> int:
    if not RENDER_SCRIPT.exists():
        die(f"Missing render script: {RENDER_SCRIPT}")

    subprocess.run([sys.executable, str(RENDER_SCRIPT)], check=True)

    if not RENDER_EVENTS.exists():
        die(f"Missing render events: {RENDER_EVENTS}")

    with open(RENDER_EVENTS, "r", encoding="utf-8") as f:
        events = json.load(f)

    if not events:
        die("No flash events from render engine.")

    df = pd.DataFrame(events)
    for col in ["time", "theta_obs", "renorm_before", "renorm_after"]:
        if col not in df.columns:
            die(f"flash_events_render.json missing column: {col}")

    delta_theta_mean = float((df["theta_obs"] - 138.88).mean())
    delta_renorm_mean = float((df["renorm_after"] - df["renorm_before"]).mean())

    total_time = float(df["time"].max() - df["time"].min())
    if total_time <= 0:
        total_time = 1.0
    flash_rate = float(len(df) / total_time)

    if not ANGLE_SUMMARY.exists():
        die(f"Missing angle summary: {ANGLE_SUMMARY}")
    if not RENORM_SUMMARY.exists():
        die(f"Missing renorm summary: {RENORM_SUMMARY}")

    with open(ANGLE_SUMMARY, "r", encoding="utf-8") as f:
        angle_ref = json.load(f)
    with open(RENORM_SUMMARY, "r", encoding="utf-8") as f:
        renorm_ref = json.load(f)

    ref_theta = float(angle_ref.get("delta_theta_mean", np.nan))
    ref_renorm = float(renorm_ref.get("delta_renorm_mean", np.nan))

    # center_in flash_rate reference
    if not CLOSURE_CSV.exists():
        die(f"Missing closure comparison: {CLOSURE_CSV}")
    cmp = pd.read_csv(CLOSURE_CSV)
    center = cmp[cmp["point"] == "center_in"]
    if center.empty:
        die("closure_point_comparison.csv missing center_in row")
    ref_flash_rate = float(center["flash_rate_mean"].iloc[0])

    # Tolerances (engine vs production summaries)
    tol_theta = 0.1
    tol_renorm = 0.02
    tol_flash_rate = 0.02

    if not np.isfinite(ref_theta) or abs(delta_theta_mean - ref_theta) > tol_theta:
        die(f"delta_theta_mean mismatch: render={delta_theta_mean} ref={ref_theta} tol={tol_theta}")
    if not np.isfinite(ref_renorm) or abs(delta_renorm_mean - ref_renorm) > tol_renorm:
        die(f"delta_renorm_mean mismatch: render={delta_renorm_mean} ref={ref_renorm} tol={tol_renorm}")
    if not np.isfinite(ref_flash_rate) or abs(flash_rate - ref_flash_rate) > tol_flash_rate:
        die(f"flash_rate mismatch: render={flash_rate} ref={ref_flash_rate} tol={tol_flash_rate}")

    print("[OK] Render engine matches production law summaries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
