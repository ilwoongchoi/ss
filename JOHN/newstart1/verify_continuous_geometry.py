import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent

BUNDLE_PATH = ROOT / "CONTINUOUS_GEOMETRY_BUNDLE.json"
DIST_ALL = ROOT / "analysis_results" / "iter3_tda_v2" / "dist_all.csv"
RIDGE_CSV = ROOT / "out" / "refine_lam10_det_ridge.csv"

ANGLE_SUMMARY = ROOT / "out" / "h3_h4_d3_residuals" / "flash_angle_summary.json"
ANGLE_SWEEP = ROOT / "out" / "h3_h4_d3_residuals" / "lambda_sweep_angle_all.json"

RENORM_SUMMARY = ROOT / "out" / "h3_h4_d3_residuals" / "flash_renorm_summary.json"
RENORM_ABLATION = ROOT / "out" / "residual_map_report" / "renorm_ablation.json"

RATE_DECOMP = ROOT / "out" / "residual_map_report" / "rate_axis_decomposition.json"

HYST_SCRIPT = ROOT / "scripts" / "run_hysteresis_loop.py"
HYST_METRICS = ROOT / "out" / "strd_nmdb_hysteresis_metrics.json"


def die(errors: list[str]) -> None:
    for msg in errors:
        print(f"[FAIL] {msg}")
    sys.exit(1)


def check_close(errors: list[str], name: str, val: float, ref: float, tol: float) -> None:
    if not (np.isfinite(val) and np.isfinite(ref)):
        errors.append(f"{name}: non-finite value (val={val}, ref={ref})")
        return
    if abs(val - ref) > tol:
        errors.append(f"{name}: {val} vs {ref} (tol={tol})")


def kappa_piecewise_from_persistence(p: float, p_ref: float, p_max: float) -> float:
    k_min = 1.0 / 64.0
    k_mid = 1.0 / 32.0
    k_max = 1.0 / 16.0

    if not np.isfinite(p):
        return np.nan

    if p_max <= p_ref:
        return k_mid

    mid = p_ref + 0.5 * (p_max - p_ref)

    if p <= p_ref:
        return k_min
    if p <= mid:
        t = (p - p_ref) / (mid - p_ref)
        return k_min + t * (k_mid - k_min)
    if p <= p_max:
        t = (p - mid) / (p_max - mid)
        return k_mid + t * (k_max - k_mid)
    return k_max


def load_bundle() -> dict:
    if not BUNDLE_PATH.exists():
        die([f"Missing bundle: {BUNDLE_PATH}"])
    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def recompute_ref_cell(dist: pd.DataFrame) -> tuple[float, float, float, float]:
    ref_idx = dist["wasserstein_H1"].idxmin()
    ref_row = dist.loc[ref_idx]
    r_ref = float(ref_row["r"])
    q0_ref = float(ref_row["q0"])
    p_ref = float(ref_row["max_persistence"])
    p_max = float(dist["max_persistence"].max())
    return r_ref, q0_ref, p_ref, p_max


def recompute_sh_band(dist: pd.DataFrame, p_ref: float, p_max: float) -> tuple[float, float, float, float]:
    dist = dist.copy()
    dist["kappa_tda"] = dist["max_persistence"].apply(
        lambda p: kappa_piecewise_from_persistence(p, p_ref, p_max)
    )
    k_mid = 1.0 / 32.0
    diff = (dist["kappa_tda"] - k_mid).abs()
    if not np.isfinite(diff).any():
        return np.nan, np.nan, np.nan, np.nan
    cut = np.nanpercentile(diff, 5)
    band = dist[diff <= cut]
    if band.empty:
        return np.nan, np.nan, np.nan, np.nan
    return (
        float(band["r"].min()),
        float(band["r"].max()),
        float(band["q0"].min()),
        float(band["q0"].max()),
    )


def recompute_ridge_stats(ridge: pd.DataFrame) -> tuple[float, float, float, float]:
    # Center: rate_post-weighted mean over ridge points.
    w = ridge["rate_post"].to_numpy()
    r_star = float(np.average(ridge["r"].to_numpy(), weights=w))
    q0_star = float(np.average(ridge["q0"].to_numpy(), weights=w))

    # Widths: half-max band in q0 around the half-max mean.
    peak = float(ridge["rate_post"].max())
    half = 0.5 * peak
    q_half = ridge[ridge["rate_post"] >= half]["q0"]
    if q_half.empty:
        return r_star, q0_star, np.nan, np.nan
    q0_mean = float(q_half.mean())
    sigma_l = float(q0_mean - q_half.min())
    sigma_r = float(q_half.max() - q0_mean)
    return r_star, q0_star, sigma_l, sigma_r


def run_hysteresis_script(errors: list[str]) -> dict:
    if not HYST_SCRIPT.exists():
        errors.append(f"Missing hysteresis script: {HYST_SCRIPT}")
        return {}
    try:
        subprocess.run([sys.executable, str(HYST_SCRIPT)], check=True)
    except subprocess.CalledProcessError as exc:
        errors.append(f"Hysteresis script failed: {HYST_SCRIPT} (exit={exc.returncode})")
        return {}
    if not HYST_METRICS.exists():
        errors.append(f"Missing hysteresis metrics output: {HYST_METRICS}")
        return {}
    with open(HYST_METRICS, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    errors: list[str] = []

    bundle = load_bundle()
    locked = bundle.get("locked_constants", {})

    # A) TDA bridge / SH ridge
    if not DIST_ALL.exists():
        errors.append(f"Missing dist_all.csv: {DIST_ALL}")
    else:
        dist = pd.read_csv(DIST_ALL)
        for c in ["r", "q0", "wasserstein_H1", "max_persistence"]:
            if c not in dist.columns:
                errors.append(f"dist_all.csv missing column: {c}")
        if not errors:
            r_ref, q0_ref, p_ref, p_max = recompute_ref_cell(dist)
            ref_lock = locked.get("ref_cell", {})
            ref_val = ref_lock.get("value", {})
            ref_tol = ref_lock.get("tolerance", {})
            check_close(errors, "ref_cell.r_ref", r_ref, ref_val.get("r_ref", np.nan), ref_tol.get("r_ref", 0.0))
            check_close(errors, "ref_cell.q0_ref", q0_ref, ref_val.get("q0_ref", np.nan), ref_tol.get("q0_ref", 0.0))
            check_close(errors, "ref_cell.p_ref", p_ref, ref_val.get("p_ref", np.nan), ref_tol.get("p_ref", 0.0))
            check_close(errors, "ref_cell.p_max", p_max, ref_val.get("p_max", np.nan), ref_tol.get("p_max", 0.0))

            r_min, r_max, q0_min, q0_max = recompute_sh_band(dist, p_ref, p_max)
            sh_lock = locked.get("sh_band", {})
            sh_val = sh_lock.get("value", {})
            sh_tol = sh_lock.get("tolerance", {})
            check_close(errors, "sh_band.r_min", r_min, sh_val.get("r_min", np.nan), sh_tol.get("r_min", 0.0))
            check_close(errors, "sh_band.r_max", r_max, sh_val.get("r_max", np.nan), sh_tol.get("r_max", 0.0))
            check_close(errors, "sh_band.q0_min", q0_min, sh_val.get("q0_min", np.nan), sh_tol.get("q0_min", 0.0))
            check_close(errors, "sh_band.q0_max", q0_max, sh_val.get("q0_max", np.nan), sh_tol.get("q0_max", 0.0))

    if not RIDGE_CSV.exists():
        errors.append(f"Missing refine_lam10_det_ridge.csv: {RIDGE_CSV}")
    else:
        ridge = pd.read_csv(RIDGE_CSV)
        for c in ["q0", "r", "rate_post"]:
            if c not in ridge.columns:
                errors.append(f"refine_lam10_det_ridge.csv missing column: {c}")
        if not errors:
            r_star, q0_star, sigma_l, sigma_r = recompute_ridge_stats(ridge)
            ridge_lock = locked.get("ridge_center", {})
            ridge_val = ridge_lock.get("value", {})
            ridge_tol = ridge_lock.get("tolerance", {})
            check_close(errors, "ridge.r_star", r_star, ridge_val.get("r_star", np.nan), ridge_tol.get("r_star", 0.0))
            check_close(errors, "ridge.q0_star", q0_star, ridge_val.get("q0_star", np.nan), ridge_tol.get("q0_star", 0.0))
            check_close(errors, "ridge.sigma_L", sigma_l, ridge_val.get("sigma_L", np.nan), ridge_tol.get("sigma_L", 0.0))
            check_close(errors, "ridge.sigma_R", sigma_r, ridge_val.get("sigma_R", np.nan), ridge_tol.get("sigma_R", 0.0))

    # B) Spark angle / D3 residual
    if not ANGLE_SUMMARY.exists():
        errors.append(f"Missing flash_angle_summary.json: {ANGLE_SUMMARY}")
    else:
        with open(ANGLE_SUMMARY, "r", encoding="utf-8") as f:
            angle = json.load(f)
        delta = float(angle.get("delta_theta_mean", np.nan))
        if not np.isfinite(delta):
            errors.append("flash_angle_summary.json missing delta_theta_mean")
        else:
            if abs(delta) >= 0.1:
                errors.append(f"delta_theta_mean too large: {delta}")
            spark_val = locked.get("spark", {}).get("value", {})
            spark_angle = float(spark_val.get("angle_deg", np.nan))
            if np.isfinite(spark_angle):
                mean_obs = spark_angle + delta
                if abs(mean_obs - spark_angle) >= 0.1:
                    errors.append(f"mean observed angle drift: {mean_obs} vs {spark_angle}")

        if ANGLE_SWEEP.exists():
            with open(ANGLE_SWEEP, "r", encoding="utf-8") as f:
                sweep = json.load(f)
            delta_all = sweep.get("delta_theta_mean_all")
            if delta_all is not None and abs(float(delta_all)) >= 0.1:
                errors.append(f"delta_theta_mean_all too large: {delta_all}")

    # C) Renorm bridge (North Pole)
    if not RENORM_SUMMARY.exists():
        errors.append(f"Missing flash_renorm_summary.json: {RENORM_SUMMARY}")
    else:
        with open(RENORM_SUMMARY, "r", encoding="utf-8") as f:
            ren = json.load(f)
        delta_ren = float(ren.get("delta_renorm_mean", np.nan))
        if not np.isfinite(delta_ren) or abs(delta_ren) >= 0.01:
            errors.append(f"delta_renorm_mean too large: {delta_ren}")

    if not RENORM_ABLATION.exists():
        errors.append(f"Missing renorm_ablation.json: {RENORM_ABLATION}")
    else:
        with open(RENORM_ABLATION, "r", encoding="utf-8") as f:
            abl = json.load(f)
        nominal = float(abl.get("nominal_delta_mean", np.nan))
        for key in ["ablate_L_comp", "ablate_E_pole", "ablate_G_recover"]:
            if key not in abl:
                errors.append(f"renorm_ablation.json missing {key}")
                continue
            val = float(abl[key].get("delta_renorm_mean", np.nan))
            if not np.isfinite(val) or not np.isfinite(nominal):
                errors.append(f"{key} delta_renorm_mean missing")
                continue
            if abs(val) <= abs(nominal):
                errors.append(f"{key} does not increase |delta_renorm_mean| (nominal={nominal}, ablated={val})")

    # D) Rate residual / eligibility
    if not RATE_DECOMP.exists():
        errors.append(f"Missing rate_axis_decomposition.json: {RATE_DECOMP}")
    else:
        with open(RATE_DECOMP, "r", encoding="utf-8") as f:
            rate = json.load(f)
        corr = float(rate.get("corr_delta_rate_vs_eligibleB_mean", np.nan))
        if not np.isfinite(corr) or corr > -0.9:
            errors.append(f"corr(delta_rate, eligibleB_mean) not strongly negative: {corr}")
        filtered = rate.get("filtered", {})
        delta_max = None
        for key in ["eligible_ge_100", "eligible_ge_1", "eligible_ge_0p0001"]:
            if key in filtered and "delta_rate_abs_max" in filtered[key]:
                delta_max = float(filtered[key]["delta_rate_abs_max"])
                break
        if delta_max is None:
            errors.append("filtered delta_rate_abs_max missing in rate_axis_decomposition.json")
        elif delta_max > 0.005:
            errors.append(f"filtered delta_rate_abs_max too large: {delta_max}")

    # E) Hysteresis / TOTAL_DEBT
    metrics = run_hysteresis_script(errors)
    if metrics:
        loop_area = float(metrics.get("loop_area_flux_nmdb_norm", np.nan))
        w7_area = float(locked.get("w7_area", {}).get("value", np.nan))
        nh_area = locked.get("night_hysteresis_area", {})
        if np.isfinite(loop_area) and np.isfinite(w7_area):
            if nh_area:
                nh_val = float(nh_area.get("value", np.nan))
                nh_tol = float(nh_area.get("tolerance", 0.0))
                if np.isfinite(nh_val):
                    target = w7_area / nh_val
                    if abs(loop_area - target) > nh_tol:
                        errors.append(
                            f"hysteresis area mismatch: loop_area={loop_area} vs W7_AREA/night_hysteresis_area={target}"
                        )
            else:
                night_hyst = float(locked.get("night_hysteresis", {}).get("value", np.nan))
                if np.isfinite(night_hyst):
                    target = w7_area / night_hyst
                    if abs(loop_area - target) > 1e-3:
                        errors.append(
                            f"hysteresis area mismatch: loop_area={loop_area} vs W7_AREA/night_hysteresis={target}"
                        )

    # TOTAL_DEBT_AREA relationship (from absolute constants)
    try:
        from geometry_package import absolute_constants as ac
        total_debt = float(ac.TOTAL_DEBT_AREA)
        night_hyst = float(ac.NIGHT_HYSTERESIS)
        expected = (11.0 / 7.0) * night_hyst
        if abs(total_debt - expected) > 1e-6:
            errors.append(
                f"TOTAL_DEBT_AREA mismatch: {total_debt} vs (11/7)*NIGHT_HYSTERESIS={expected}"
            )
    except Exception as exc:
        errors.append(f"Failed to load absolute_constants for TOTAL_DEBT check: {exc}")

    if errors:
        die(errors)

    print("[OK] Continuous geometry verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
