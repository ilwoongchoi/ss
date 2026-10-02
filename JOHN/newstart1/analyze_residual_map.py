import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def clamp01(v: float) -> float:
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return float(v)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def std_regress(y: np.ndarray, X: np.ndarray, feature_names: list[str]) -> dict:
    """
    Standardized linear regression: z(y) ~ 1 + z(X).
    Falls back to a tiny ridge solve if SVD/lstsq is unstable.
    """
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)
    y_z = (y - np.mean(y)) / (np.std(y) + 1e-12)
    X_z = (X - np.mean(X, axis=0)) / (np.std(X, axis=0) + 1e-12)
    X_design = np.column_stack([np.ones(len(X_z)), X_z])

    # Always use a tiny ridge solve to avoid platform-specific lstsq/SVD instability.
    lam = 1e-6
    A = X_design.T @ X_design + lam * np.eye(X_design.shape[1])
    b = X_design.T @ y_z
    beta = np.linalg.solve(A, b)

    y_hat = X_design @ beta
    ss_res = float(np.sum((y_z - y_hat) ** 2))
    ss_tot = float(np.sum((y_z - np.mean(y_z)) ** 2))
    r2 = 1.0 - ss_res / (ss_tot + 1e-12)
    return {
        "features": feature_names,
        "beta0": float(beta[0]),
        "betas": {feature_names[i]: float(beta[i + 1]) for i in range(len(feature_names))},
        "r2": float(r2),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Residual map + ablation report from out/h3_h4_d3_residuals artifacts")
    ap.add_argument(
        "--resdir",
        type=str,
        default=r"out\h3_h4_d3_residuals",
        help="Directory containing compute_h3_h4_d3_residuals outputs",
    )
    ap.add_argument(
        "--closure_summary",
        type=str,
        default=r"out\detune_closure_sweep_v4\summary.csv",
        help="4-point closure summary.csv used for separation check",
    )
    ap.add_argument(
        "--outdir",
        type=str,
        default=r"out\residual_map_report",
        help="Output directory for the report bundle",
    )
    ap.add_argument(
        "--ridge_csv",
        type=str,
        default=r"out\123\refine_lam10_det_ridge.csv",
        help="Optional ridge curve CSV (columns: q0,r) for hotspot proximity checks",
    )
    args = ap.parse_args()

    root = Path(__file__).resolve().parent
    resdir = (root / args.resdir).resolve()
    outdir = (root / args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    closure_path = (root / args.closure_summary).resolve()

    # ---------------------------------------------------------
    # 1) 4-point closure separation
    # ---------------------------------------------------------
    closure_df = pd.read_csv(closure_path)
    required_cols = {"point", "flash_rate"}
    missing = required_cols - set(closure_df.columns)
    if missing:
        raise ValueError(f"closure_summary missing columns: {sorted(missing)}")

    center_row = closure_df.loc[closure_df["point"] == "center_in"]
    if center_row.empty:
        raise ValueError("closure_summary missing point=center_in")
    center_flash_rate = float(center_row["flash_rate"].iloc[0])
    out_flash_rates = closure_df.loc[closure_df["point"] != "center_in", "flash_rate"].astype(float)
    out_flash_rate_mean = float(out_flash_rates.mean()) if len(out_flash_rates) else float("nan")

    closure_check = {
        "center_in_flash_rate": center_flash_rate,
        "out_band_flash_rate_mean": out_flash_rate_mean,
        "center_minus_out": center_flash_rate - out_flash_rate_mean,
        "separation_kept": bool(center_flash_rate > out_flash_rate_mean),
    }
    (outdir / "closure_check.json").write_text(json.dumps(closure_check, indent=2), encoding="utf-8")

    # ---------------------------------------------------------
    # 2) scalar residual summaries (angle, renorm)
    # ---------------------------------------------------------
    angle_summary_path = resdir / "flash_angle_summary.json"
    renorm_summary_path = resdir / "flash_renorm_summary.json"

    angle_summary = read_json(angle_summary_path) if angle_summary_path.exists() else {}
    renorm_summary = read_json(renorm_summary_path) if renorm_summary_path.exists() else {}

    scalar_summary = {
        "angle": angle_summary,
        "renorm": renorm_summary,
        "closure": closure_check,
    }
    (outdir / "scalar_residual_summary.json").write_text(json.dumps(scalar_summary, indent=2), encoding="utf-8")

    # ---------------------------------------------------------
    # 3) rate residual map (cell + per-turn)
    # ---------------------------------------------------------
    cell_rate_path = resdir / "cell_rate_residual_summary.csv"
    per_turn_path = resdir / "per_turn_with_rate_residuals.csv"

    if not cell_rate_path.exists():
        raise FileNotFoundError(f"Missing {cell_rate_path}")
    if not per_turn_path.exists():
        raise FileNotFoundError(f"Missing {per_turn_path}")

    cell = pd.read_csv(cell_rate_path)
    need_cell = {"r", "q0", "delta_rate_mean", "delta_rate_std"}
    missing = need_cell - set(cell.columns)
    if missing:
        raise ValueError(f"cell_rate_residual_summary missing columns: {sorted(missing)}")

    cell = cell.copy()
    cell["abs_delta_rate_mean"] = cell["delta_rate_mean"].abs()
    cell["delta_rate_z"] = cell["delta_rate_mean"] / cell["delta_rate_std"].replace(0, np.nan)
    cell.sort_values(["abs_delta_rate_mean"], ascending=False).to_csv(outdir / "rate_residual_map_sorted.csv", index=False)

    per_turn = pd.read_csv(per_turn_path)
    need_turn = {"r", "q0", "turn", "delta_rate", "w_gate_sim", "eligibleB_mean"}
    missing = need_turn - set(per_turn.columns)
    if missing:
        raise ValueError(f"per_turn_with_rate_residuals missing columns: {sorted(missing)}")

    # Alternative residuals that avoid rate_post pseudo-count behavior when eligible==0
    if {"sparksB_mean", "expectedB_mean"} <= set(per_turn.columns):
        per_turn["delta_sparks_mean"] = per_turn["sparksB_mean"] - per_turn["expectedB_mean"]
        per_turn["delta_sparks_per_eligible"] = per_turn["delta_sparks_mean"] / per_turn["eligibleB_mean"].replace(0, np.nan)

    # Axis decomposition (w_gate / eligible / kappa)
    axis_cols = ["w_gate_sim", "eligibleB_mean"]
    if "kappa_tda_H2" in per_turn.columns:
        axis_cols.append("kappa_tda_H2")
    axis_df = per_turn[["delta_rate", "turn"] + axis_cols].copy().replace([np.inf, -np.inf], np.nan).dropna()

    def corr(a: pd.Series, b: pd.Series) -> float:
        if len(a) < 3:
            return float("nan")
        return float(a.corr(b))

    axis_decomp = {
        "n_rows": int(len(axis_df)),
        "corr_delta_rate_vs_w_gate_sim": corr(axis_df["delta_rate"], axis_df["w_gate_sim"]),
        "corr_delta_rate_vs_eligibleB_mean": corr(axis_df["delta_rate"], axis_df["eligibleB_mean"]),
    }
    if "kappa_tda_H2" in axis_df.columns:
        axis_decomp["corr_delta_rate_vs_kappa_tda_H2"] = corr(axis_df["delta_rate"], axis_df["kappa_tda_H2"])

    # Standardized linear regression: z(delta_rate) ~ z(features)
    y = axis_df["delta_rate"].to_numpy(dtype=float)
    X_cols = [c for c in ["w_gate_sim", "eligibleB_mean", "kappa_tda_H2"] if c in axis_df.columns]
    X = axis_df[X_cols].to_numpy(dtype=float)
    axis_decomp["std_linear_regression"] = std_regress(y, X, X_cols)

    # Turn trend / sign pattern
    turn_stats = (
        per_turn.groupby("turn", as_index=False)
        .agg(
            n=("delta_rate", "count"),
            delta_rate_mean=("delta_rate", "mean"),
            delta_rate_abs_mean=("delta_rate", lambda s: float(np.mean(np.abs(s)))),
        )
        .sort_values("turn")
    )
    # simple linear fit: abs_mean ~ turn
    t = turn_stats["turn"].to_numpy(dtype=float)
    a = turn_stats["delta_rate_abs_mean"].to_numpy(dtype=float)
    if len(turn_stats) >= 2:
        slope = float(np.polyfit(t, a, deg=1)[0])
        mean_sign = float(np.mean(np.sign(turn_stats["delta_rate_mean"].to_numpy(dtype=float))))
        sign_changes = int(np.sum(np.sign(turn_stats["delta_rate_mean"].to_numpy(dtype=float))[1:] != np.sign(turn_stats["delta_rate_mean"].to_numpy(dtype=float))[:-1]))
    else:
        slope = float("nan")
        mean_sign = float("nan")
        sign_changes = 0
    axis_decomp["turn_pattern"] = {
        "abs_mean_slope_per_turn": slope,
        "mean_sign_over_turns": mean_sign,
        "sign_changes_over_turns": sign_changes,
        "turn_count": int(len(turn_stats)),
    }

    # Repeat decomposition with eligibility filters
    def filtered_block(min_eligible: float) -> dict:
        df = per_turn.copy()
        df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["delta_rate", "w_gate_sim", "eligibleB_mean"])
        df = df[df["eligibleB_mean"] >= float(min_eligible)]
        if "kappa_tda_H2" in df.columns:
            df = df.dropna(subset=["kappa_tda_H2"])
        if len(df) < 3:
            return {"n_rows": int(len(df))}
        y = df["delta_rate"].to_numpy(dtype=float)
        feats = [c for c in ["w_gate_sim", "eligibleB_mean", "kappa_tda_H2"] if c in df.columns]
        X = df[feats].to_numpy(dtype=float)
        out = {
            "n_rows": int(len(df)),
            "corr_delta_rate_vs_w_gate_sim": corr(df["delta_rate"], df["w_gate_sim"]),
            "corr_delta_rate_vs_eligibleB_mean": corr(df["delta_rate"], df["eligibleB_mean"]),
            "std_linear_regression": std_regress(y, X, feats),
            "delta_rate_abs_max": float(np.max(np.abs(y))),
        }
        if "kappa_tda_H2" in df.columns:
            out["corr_delta_rate_vs_kappa_tda_H2"] = corr(df["delta_rate"], df["kappa_tda_H2"])
        return out

    axis_decomp["filtered"] = {
        "eligible_ge_0p0001": filtered_block(1e-4),
        "eligible_ge_1": filtered_block(1.0),
        "eligible_ge_100": filtered_block(100.0),
    }

    # If available, add count-residual axis decomposition (sparks - expected)
    if "delta_sparks_per_eligible" in per_turn.columns:
        df2 = per_turn.replace([np.inf, -np.inf], np.nan).dropna(
            subset=["delta_sparks_per_eligible", "w_gate_sim", "eligibleB_mean", "kappa_tda_H2"]
            if "kappa_tda_H2" in per_turn.columns
            else ["delta_sparks_per_eligible", "w_gate_sim", "eligibleB_mean"]
        )
        df2 = df2[df2["eligibleB_mean"] > 0]
        feats2 = [c for c in ["w_gate_sim", "eligibleB_mean", "kappa_tda_H2"] if c in df2.columns]
        y2 = df2["delta_sparks_per_eligible"].to_numpy(dtype=float)
        X2 = df2[feats2].to_numpy(dtype=float)
        axis_decomp["delta_sparks_per_eligible_decomp"] = {
            "n_rows": int(len(df2)),
            "std_linear_regression": std_regress(y2, X2, feats2),
            "corr_vs_w_gate_sim": corr(df2["delta_sparks_per_eligible"], df2["w_gate_sim"]),
            "corr_vs_eligibleB_mean": corr(df2["delta_sparks_per_eligible"], df2["eligibleB_mean"]),
            "corr_vs_kappa_tda_H2": corr(df2["delta_sparks_per_eligible"], df2["kappa_tda_H2"]) if "kappa_tda_H2" in df2.columns else float("nan"),
        }

    (outdir / "rate_axis_decomposition.json").write_text(json.dumps(axis_decomp, indent=2), encoding="utf-8")

    # Binned summaries for quick visual inspection without plotting
    binned = per_turn.copy()
    binned = binned.replace([np.inf, -np.inf], np.nan).dropna(subset=["delta_rate", "w_gate_sim", "eligibleB_mean"])
    # Use integer bin labels to avoid pandas IntervalIndex edge cases.
    binned["w_gate_bin"] = pd.qcut(binned["w_gate_sim"], 10, labels=False, duplicates="drop")
    binned["eligible_bin"] = pd.qcut(binned["eligibleB_mean"], 10, labels=False, duplicates="drop")
    bin_agg = (
        binned.groupby(["w_gate_bin", "eligible_bin"], as_index=False, observed=True)
        .agg(
            n=("delta_rate", "count"),
            delta_rate_mean=("delta_rate", "mean"),
            delta_rate_abs_mean=("delta_rate", lambda s: float(np.mean(np.abs(s)))),
        )
        .sort_values("delta_rate_abs_mean", ascending=False)
    )
    bin_agg.to_csv(outdir / "rate_binned_wgate_eligible.csv", index=False)

    turn_agg = (
        per_turn.groupby(["turn"], as_index=False)
        .agg(
            n=("delta_rate", "count"),
            delta_rate_mean=("delta_rate", "mean"),
            delta_rate_std=("delta_rate", "std"),
            delta_rate_abs_mean=("delta_rate", lambda s: float(np.mean(np.abs(s)))),
        )
        .sort_values("delta_rate_abs_mean", ascending=False)
    )
    turn_agg.to_csv(outdir / "rate_residual_by_turn.csv", index=False)

    # Top hotspots with context fields for quick inspection
    hotspot_cols = [c for c in ["r", "q0", "turn", "delta_rate", "w_gate_sim", "eligibleB_mean", "kappa_tda_H2"] if c in per_turn.columns]
    per_turn_hot = per_turn.copy()
    per_turn_hot["abs_delta_rate"] = per_turn_hot["delta_rate"].abs()
    per_turn_hot.sort_values("abs_delta_rate", ascending=False).head(200)[hotspot_cols].to_csv(
        outdir / "rate_residual_hotspots_top200.csv", index=False
    )
    per_turn_hot_ge100 = per_turn_hot[per_turn_hot["eligibleB_mean"] >= 100].copy()
    if not per_turn_hot_ge100.empty:
        per_turn_hot_ge100.sort_values("abs_delta_rate", ascending=False).head(200)[hotspot_cols].to_csv(
            outdir / "rate_residual_hotspots_eligible_ge_100_top200.csv", index=False
        )

    # Ridge proximity for hotspots (optional)
    ridge_path = (root / args.ridge_csv).resolve()
    if ridge_path.exists():
        ridge = pd.read_csv(ridge_path)
        if {"q0", "r"} <= set(ridge.columns):
            ridge_pts = ridge[["r", "q0"]].to_numpy(dtype=float)
            cell_pts = cell[["r", "q0"]].to_numpy(dtype=float)

            r_span = float(np.nanmax(cell_pts[:, 0]) - np.nanmin(cell_pts[:, 0])) + 1e-12
            q_span = float(np.nanmax(cell_pts[:, 1]) - np.nanmin(cell_pts[:, 1])) + 1e-12

            def min_dist_norm(p: np.ndarray) -> float:
                dr = (ridge_pts[:, 0] - p[0]) / r_span
                dq = (ridge_pts[:, 1] - p[1]) / q_span
                return float(np.min(np.sqrt(dr * dr + dq * dq)))

            cell["ridge_dist_norm"] = [min_dist_norm(p) for p in cell_pts]
            cell.to_csv(outdir / "rate_residual_map_with_ridge_dist.csv", index=False)

            hot = cell.sort_values("abs_delta_rate_mean", ascending=False).head(200)
            ridge_report = {
                "ridge_csv": str(ridge_path),
                "hotspot200_ridge_dist_norm_median": float(hot["ridge_dist_norm"].median()),
                "all_cells_ridge_dist_norm_median": float(cell["ridge_dist_norm"].median()),
                "hotspot200_frac_within_0p05": float(np.mean(hot["ridge_dist_norm"] <= 0.05)),
                "hotspot200_frac_within_0p10": float(np.mean(hot["ridge_dist_norm"] <= 0.10)),
            }
            (outdir / "rate_hotspot_ridge_report.json").write_text(json.dumps(ridge_report, indent=2), encoding="utf-8")

    # ---------------------------------------------------------
    # 4) ablation: renorm terms
    # ---------------------------------------------------------
    term_events_path = resdir / "renorm_term_events.csv"
    if term_events_path.exists():
        ev = pd.read_csv(term_events_path)
        need_ev = {"renorm_before", "L_comp", "E_pole", "G_recover"}
        missing = need_ev - set(ev.columns)
        if missing:
            raise ValueError(f"renorm_term_events missing columns: {sorted(missing)}")

        # nominal (unclamped) and clamped deltas
        nominal_delta = -ev["L_comp"] + ev["E_pole"] + ev["G_recover"]
        clamped_after = (ev["renorm_before"] + nominal_delta).map(clamp01)
        delta_clamped = clamped_after - ev["renorm_before"]

        def ablate(which: str) -> dict:
            L = ev["L_comp"].copy()
            E = ev["E_pole"].copy()
            G = ev["G_recover"].copy()
            if which == "L_comp":
                L = 0.0
            elif which == "E_pole":
                E = 0.0
            elif which == "G_recover":
                G = 0.0
            else:
                raise ValueError(which)
            d = (-L + E + G).astype(float)
            after = (ev["renorm_before"] + d).map(clamp01)
            delta = (after - ev["renorm_before"]).astype(float)
            return {
                "delta_renorm_mean": float(delta.mean()),
                "delta_renorm_std": float(delta.std(ddof=1)) if len(delta) > 1 else 0.0,
            }

        ablation = {
            "n_flash_events": int(len(ev)),
            "nominal_delta_mean": float(nominal_delta.mean()),
            "nominal_delta_std": float(nominal_delta.std(ddof=1)) if len(ev) > 1 else 0.0,
            "delta_clamped_mean": float(delta_clamped.mean()),
            "delta_clamped_std": float(delta_clamped.std(ddof=1)) if len(ev) > 1 else 0.0,
            "ablate_L_comp": ablate("L_comp"),
            "ablate_E_pole": ablate("E_pole"),
            "ablate_G_recover": ablate("G_recover"),
        }
        (outdir / "renorm_ablation.json").write_text(json.dumps(ablation, indent=2), encoding="utf-8")

    # ---------------------------------------------------------
    # 5) single-line verdict helper
    # ---------------------------------------------------------
    delta_theta_mean = angle_summary.get("delta_theta_mean", None)
    delta_renorm_mean = renorm_summary.get("delta_renorm_mean", None)
    verdict = {
        "separation_kept": closure_check["separation_kept"],
        "delta_theta_mean": delta_theta_mean,
        "delta_renorm_mean": delta_renorm_mean,
        "rate_residual_abs_max": float(cell["abs_delta_rate_mean"].max()),
    }
    (outdir / "verdict.json").write_text(json.dumps(verdict, indent=2), encoding="utf-8")

    print("DONE")
    print(f"Report dir: {outdir}")


if __name__ == "__main__":
    main()
