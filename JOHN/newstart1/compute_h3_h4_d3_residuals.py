import json
from pathlib import Path

import numpy as np
import pandas as pd

# =========================================================
# PATHS
# =========================================================
ROOT = Path(r"d:\Users\user\Documents\newstart")

DIST_ALL = ROOT / r"analysis_results\iter3_tda_v2\dist_all.csv"
PER_TURN = ROOT / r"out\refine_lam10_det_per_turn.csv"
SUMMARY = ROOT / r"out\detune_closure_sweep_v4\summary.csv"
FLASH_JSON = ROOT / r"out\detune_closure_sweep_v4\flash_events_center_in.json"

OUTDIR = ROOT / r"out\h3_h4_d3_residuals"
OUTDIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# HELPERS
# =========================================================
def kappa_piecewise_from_persistence(p: float, p_ref: float, p_max: float) -> float:
    """
    H2 baseline piecewise map:
      low  -> 1/64
      mid  -> 1/32
      high -> 1/16

    Linear ramp from p_ref -> p_max with midpoint at half-range.
    """
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
    elif p <= mid:
        # ramp k_min -> k_mid
        t = (p - p_ref) / (mid - p_ref)
        return k_min + t * (k_mid - k_min)
    elif p <= p_max:
        # ramp k_mid -> k_max
        t = (p - mid) / (p_max - mid)
        return k_mid + t * (k_max - k_mid)
    else:
        return k_max


def ensure_columns(df: pd.DataFrame, cols: list[str], name: str):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"{name} missing columns: {missing}")


# =========================================================
# 1) H2 BASELINE FROM dist_all.csv
# =========================================================
dist = pd.read_csv(DIST_ALL)
ensure_columns(
    dist,
    ["r", "q0", "wasserstein_H1", "max_persistence"],
    "dist_all.csv",
)

# reference cell = min wasserstein_H1
ref_idx = dist["wasserstein_H1"].idxmin()
ref_row = dist.loc[ref_idx].copy()

r_ref = ref_row["r"]
q0_ref = ref_row["q0"]
p_ref = ref_row["max_persistence"]
p_max = dist["max_persistence"].max()

dist["kappa_tda_H2"] = dist["max_persistence"].apply(
    lambda p: kappa_piecewise_from_persistence(p, p_ref, p_max)
)

# save baseline map
dist.to_csv(OUTDIR / "dist_all_with_kappa_tda_H2.csv", index=False)

baseline_meta = {
    "r_ref": float(r_ref),
    "q0_ref": float(q0_ref),
    "p_ref": float(p_ref),
    "p_max": float(p_max),
    "kappa_min": 1.0 / 64.0,
    "kappa_mid": 1.0 / 32.0,
    "kappa_max": 1.0 / 16.0,
}
with open(OUTDIR / "h2_baseline_meta.json", "w", encoding="utf-8") as f:
    json.dump(baseline_meta, f, indent=2)


# =========================================================
# 2) RATE RESIDUAL FROM refine_lam10_det_per_turn.csv
# =========================================================
per_turn = pd.read_csv(PER_TURN)
ensure_columns(
    per_turn,
    ["rate_post_mean", "rateB_eligible_mean", "w_gate_sim", "eligibleB_mean", "turn", "r", "q0"],
    "refine_lam10_det_per_turn.csv",
)

# attach H2 baseline kappa by (r, q0)
kappa_map = dist[["r", "q0", "kappa_tda_H2"]].drop_duplicates()
per_turn = per_turn.merge(kappa_map, on=["r", "q0"], how="left")

# Use production H2 expected rate directly from sweep output.
# rateB_eligible_mean is expectedB / eligibleB under the production lambda0 and gate.
per_turn["rate_H2_pred"] = per_turn["rateB_eligible_mean"]
per_turn["delta_rate"] = per_turn["rate_post_mean"] - per_turn["rate_H2_pred"]
per_turn["delta_rate_alt"] = per_turn["delta_rate"]

per_turn.to_csv(OUTDIR / "per_turn_with_rate_residuals.csv", index=False)

# aggregate by cell
cell_rate = (
    per_turn.groupby(["r", "q0"], as_index=False)
    .agg(
        n_turns=("turn", "count"),
        kappa_tda_H2=("kappa_tda_H2", "first"),
        w_gate_sim_mean=("w_gate_sim", "mean"),
        eligibleB_mean_mean=("eligibleB_mean", "mean"),
        rate_post_mean_mean=("rate_post_mean", "mean"),
        rate_H2_pred_mean=("rate_H2_pred", "mean"),
        rateB_eligible_mean_mean=("rateB_eligible_mean", "mean"),
        delta_rate_mean=("delta_rate", "mean"),
        delta_rate_std=("delta_rate", "std"),
        delta_rate_alt_mean=("delta_rate_alt", "mean"),
        delta_rate_alt_std=("delta_rate_alt", "std"),
    )
)
cell_rate.to_csv(OUTDIR / "cell_rate_residual_summary.csv", index=False)

# Quick diagnostic to identify dominant source of residual variation.
diag = {
    "corr_delta_rate_vs_kappa_tda_H2": float(cell_rate["delta_rate_mean"].corr(cell_rate["kappa_tda_H2"])),
    "corr_delta_rate_vs_w_gate_sim": float(cell_rate["delta_rate_mean"].corr(cell_rate["w_gate_sim_mean"])),
    "corr_delta_rate_vs_eligibleB_mean": float(cell_rate["delta_rate_mean"].corr(cell_rate["eligibleB_mean_mean"])),
}
with open(OUTDIR / "rate_residual_diagnostic.json", "w", encoding="utf-8") as f:
    json.dump(diag, f, indent=2)


# =========================================================
# 3) CLOSURE SEPARATION FROM summary.csv
# =========================================================
summary = pd.read_csv(SUMMARY)
ensure_columns(
    summary,
    [
        "point",
        "r",
        "q0",
        "w_gate",
        "kappa",
        "in_band",
        "flash_count",
        "flash_rate",
        "total_time",
        "contact_count",
        "eligible_time",
        "expected_sparks",
        "conditional_prob",
        "p_per_dt",
    ],
    "summary.csv",
)

summary["flash_count_residual"] = summary["flash_count"] - summary["expected_sparks"]
summary["flash_rate_minus_pdt"] = summary["flash_rate"] - summary["p_per_dt"]

summary.to_csv(OUTDIR / "closure_summary_with_residuals.csv", index=False)

# point-level comparison
point_cmp = (
    summary.groupby("point", as_index=False)
    .agg(
        n=("point", "count"),
        flash_rate_mean=("flash_rate", "mean"),
        flash_rate_std=("flash_rate", "std"),
        expected_sparks_mean=("expected_sparks", "mean"),
        flash_count_mean=("flash_count", "mean"),
        flash_count_residual_mean=("flash_count_residual", "mean"),
        flash_count_residual_std=("flash_count_residual", "std"),
        conditional_prob_mean=("conditional_prob", "mean"),
        p_per_dt_mean=("p_per_dt", "mean"),
        flash_rate_minus_pdt_mean=("flash_rate_minus_pdt", "mean"),
    )
)
point_cmp.to_csv(OUTDIR / "closure_point_comparison.csv", index=False)

# explicit center_in vs out-band
point_lookup = {}
for _, row in point_cmp.iterrows():
    point_lookup[row["point"]] = row.to_dict()

center = point_lookup.get("center_in", {})
r_out = point_lookup.get("r_out", {})
q0_out = point_lookup.get("q0_out", {})
both_out = point_lookup.get("both_out", {})

closure_report = {
    "center_in_flash_rate_mean": center.get("flash_rate_mean"),
    "r_out_flash_rate_mean": r_out.get("flash_rate_mean"),
    "q0_out_flash_rate_mean": q0_out.get("flash_rate_mean"),
    "both_out_flash_rate_mean": both_out.get("flash_rate_mean"),
    "center_minus_r_out": None if not center or not r_out else center["flash_rate_mean"] - r_out["flash_rate_mean"],
    "center_minus_q0_out": None if not center or not q0_out else center["flash_rate_mean"] - q0_out["flash_rate_mean"],
    "center_minus_both_out": None if not center or not both_out else center["flash_rate_mean"] - both_out["flash_rate_mean"],
}
with open(OUTDIR / "closure_separation_report.json", "w", encoding="utf-8") as f:
    json.dump(closure_report, f, indent=2)


# =========================================================
# 4) FLASH EVENT RENORM RESIDUAL
# =========================================================
with open(FLASH_JSON, "r", encoding="utf-8") as f:
    flash_payload = json.load(f)

if isinstance(flash_payload, dict) and "flash_events" in flash_payload:
    flash_events = flash_payload["flash_events"]
else:
    flash_events = flash_payload

flash_df = pd.DataFrame(flash_events)
ensure_columns(
    flash_df,
    [
        "time",
        "tension_before",
        "state_before",
        "renorm_before",
        "renorm_after",
        "kappa_at_flash",
        "w_gate",
        "p_spark",
        "in_band",
    ],
    "flash_events_center_in.json",
)

flash_df["delta_renorm"] = flash_df["renorm_after"] - flash_df["renorm_before"]
has_terms = all(c in flash_df.columns for c in ["L_comp", "E_pole", "G_recover"])

# estimate H2 kappa at flash from center reference cell if available
# fallback: use median kappa_tda_H2
ref_match = dist[(dist["r"] == r_ref) & (dist["q0"] == q0_ref)]
if len(ref_match) > 0:
    kappa_h2_center = float(ref_match["kappa_tda_H2"].iloc[0])
else:
    kappa_h2_center = float(dist["kappa_tda_H2"].median())

flash_df["kappa_H2_center"] = kappa_h2_center
flash_df["delta_kappa_flash"] = flash_df["kappa_at_flash"] - flash_df["kappa_H2_center"]

flash_df.to_csv(OUTDIR / "flash_events_with_renorm_residuals.csv", index=False)

flash_summary = {
    "n_flash_events": int(len(flash_df)),
    "delta_renorm_mean": float(flash_df["delta_renorm"].mean()),
    "delta_renorm_std": float(flash_df["delta_renorm"].std(ddof=1)) if len(flash_df) > 1 else 0.0,
    "kappa_H2_center": float(kappa_h2_center),
    "delta_kappa_flash_mean": float(flash_df["delta_kappa_flash"].mean()),
    "delta_kappa_flash_std": float(flash_df["delta_kappa_flash"].std(ddof=1)) if len(flash_df) > 1 else 0.0,
}
if has_terms:
    flash_summary["L_comp_mean"] = float(flash_df["L_comp"].mean())
    flash_summary["L_comp_std"] = float(flash_df["L_comp"].std(ddof=1)) if len(flash_df) > 1 else 0.0
    flash_summary["E_pole_mean"] = float(flash_df["E_pole"].mean())
    flash_summary["E_pole_std"] = float(flash_df["E_pole"].std(ddof=1)) if len(flash_df) > 1 else 0.0
    flash_summary["G_recover_mean"] = float(flash_df["G_recover"].mean())
    flash_summary["G_recover_std"] = float(flash_df["G_recover"].std(ddof=1)) if len(flash_df) > 1 else 0.0
with open(OUTDIR / "flash_renorm_summary.json", "w", encoding="utf-8") as f:
    json.dump(flash_summary, f, indent=2)

if has_terms:
    term_events = flash_df[
        [
            "time",
            "renorm_before",
            "renorm_after",
            "delta_renorm",
            "L_comp",
            "E_pole",
            "G_recover",
            "x_compressed",
            "w_gate",
            "kappa_at_flash",
            "lag",
            "theta_obs",
            "turn",
            "leg",
            "lag_sign",
        ]
    ].copy()
    term_events.to_csv(OUTDIR / "renorm_term_events.csv", index=False)

    term_summary = {
        "n_flash_events": int(len(flash_df)),
        "delta_renorm_mean": float(flash_df["delta_renorm"].mean()),
        "delta_renorm_std": float(flash_df["delta_renorm"].std(ddof=1)) if len(flash_df) > 1 else 0.0,
        "L_comp_mean": float(flash_df["L_comp"].mean()),
        "L_comp_std": float(flash_df["L_comp"].std(ddof=1)) if len(flash_df) > 1 else 0.0,
        "E_pole_mean": float(flash_df["E_pole"].mean()),
        "E_pole_std": float(flash_df["E_pole"].std(ddof=1)) if len(flash_df) > 1 else 0.0,
        "G_recover_mean": float(flash_df["G_recover"].mean()),
        "G_recover_std": float(flash_df["G_recover"].std(ddof=1)) if len(flash_df) > 1 else 0.0,
    }
    with open(OUTDIR / "renorm_term_summary.json", "w", encoding="utf-8") as f:
        json.dump(term_summary, f, indent=2)


# =========================================================
# Angle residual if logger fields exist
angle_required = ["x_before", "y_before", "x_after", "y_after", "theta_obs"]
has_angle = all(c in flash_df.columns for c in angle_required)
if has_angle:
    flash_df["delta_theta"] = flash_df["theta_obs"] - 138.88
    angle_summary = {
        "angle_residual_possible": True,
        "n_flash_events_with_theta": int(flash_df["delta_theta"].notna().sum()),
        "delta_theta_mean": float(flash_df["delta_theta"].mean()),
        "delta_theta_std": float(flash_df["delta_theta"].std(ddof=1)) if len(flash_df) > 1 else 0.0,
    }
    with open(OUTDIR / "flash_angle_summary.json", "w", encoding="utf-8") as f:
        json.dump(angle_summary, f, indent=2)
    missing_report = {
        "angle_residual_possible": True,
        "reason": None,
        "needed_fields": angle_required,
        "formula": "delta_theta = theta_obs - 138.88",
    }
else:
    missing_report = {
        "angle_residual_possible": False,
        "reason": "flash_events_center_in.json does not contain theta/vector coordinates",
        "needed_fields": angle_required,
        "formula_when_available": "delta_theta = theta_obs - 138.88",
    }

with open(OUTDIR / "missing_angle_residual_report.json", "w", encoding="utf-8") as f:
    json.dump(missing_report, f, indent=2)

# Save flash table after optional angle residuals are added.
flash_df.to_csv(OUTDIR / "flash_events_with_renorm_residuals.csv", index=False)

print("DONE")
print(f"Output folder: {OUTDIR}")
print(f"reference cell: r_ref={r_ref}, q0_ref={q0_ref}, p_ref={p_ref}, p_max={p_max}")
print("Generated:")
for p in sorted(OUTDIR.glob("*")):
    print(" -", p.name)
