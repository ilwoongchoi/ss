#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
geometry_coupling_v3.py
======================

Adds the missing *validation loop* for your coupling hypothesis:

- Ablation: remove gates and/or spark features and refit.
- Holdout: fit on a u-range and evaluate on a disjoint u-range.
- Permutation: shuffle y to build a null distribution for a statistic
  (near-vs-far residual improvement).

Outputs:
- model JSON (coefficients + feature names + metrics)
- residual certificate CSV (u, y, yhat, resid, abs_resid, gate_distance, etc.)
- validation summary CSV (ablation/holdout/permutation results)

Dependencies: numpy, pandas (no sklearn).
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


# -----------------------------
# 0) Load your exact constants
# -----------------------------
def load_constants() -> Dict[str, float]:
    """
    Tries to load constants from your repo layout.
    """
    try:
        from geometry_package.absolute_constants import CALIBRATED_SKELETON  # type: ignore
        return {k: float(v) for k, v in CALIBRATED_SKELETON.items()}
    except Exception as e:
        raise RuntimeError(
            "Could not import geometry_package.absolute_constants.CALIBRATED_SKELETON. "
            "Run from your project root where geometry_package is importable."
        ) from e


@dataclass(frozen=True)
class CoreConsts:
    spark_angle_deg: float
    kappa_1_64: float
    kappa_1_32: float
    kappa_1_16: float
    kappa_3_32: float

    @staticmethod
    def from_constants(C: Dict[str, float]) -> "CoreConsts":
        return CoreConsts(
            spark_angle_deg=float(C["SPARK_ANGLE_DEG"]),
            kappa_1_64=float(C["KAPPA_1_64"]),
            kappa_1_32=float(C["KAPPA_1_32"]),
            kappa_1_16=float(C["SPACING_1_16"]),
            kappa_3_32=float(C["COMPRESSION_GAP_3_32"]),
        )


# -----------------------------------------
# 1) Feature generators (coupling features)
# -----------------------------------------
def gaussian_gate(u: np.ndarray, g: float, width: float) -> np.ndarray:
    z = (u - g) / max(width, 1e-12)
    return np.exp(-(z * z))


def step_gate(u: np.ndarray, g: float, sharpness: float = 200.0) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-sharpness * (u - g)))


def spark_alignment(theta_deg: np.ndarray, spark_angle_deg: float) -> np.ndarray:
    return np.cos(np.deg2rad(theta_deg - spark_angle_deg))


def gate_distance(u: np.ndarray, gates: List[float]) -> np.ndarray:
    """Distance from u to nearest gate center."""
    G = np.vstack([np.abs(u - g) for g in gates])
    return np.min(G, axis=0)


def build_features(
    df: pd.DataFrame,
    u_col: str,
    core: CoreConsts,
    theta_col: Optional[str],
    gate_width: Optional[float],
    use_gates: bool,
    use_spark: bool,
) -> Tuple[np.ndarray, List[str], np.ndarray]:
    if u_col not in df.columns:
        raise KeyError(f"u_col='{u_col}' not found. Available: {list(df.columns)[:40]}")

    u = df[u_col].to_numpy(dtype=float)

    # width default: 2% of u-range
    if gate_width is None:
        ur = float(np.nanmax(u) - np.nanmin(u))
        gate_width = max(ur * 0.02, 1e-6)

    feats: List[np.ndarray] = [np.ones_like(u)]
    names: List[str] = ["bias"]

    gates = [
        ("gate_1_64", core.kappa_1_64),
        ("gate_1_32", core.kappa_1_32),
        ("gate_1_16", core.kappa_1_16),
        ("gate_3_32", core.kappa_3_32),
    ]

    if use_gates:
        for nm, g in gates:
            feats.append(gaussian_gate(u, g, gate_width))
            names.append(f"{nm}_gauss_w{gate_width:g}")
        for nm, g in gates:
            feats.append(step_gate(u, g))
            names.append(f"{nm}_step")

    if use_spark:
        if theta_col is not None and theta_col in df.columns:
            theta = df[theta_col].to_numpy(dtype=float)
        else:
            theta = np.zeros_like(u)
        feats.append(spark_alignment(theta, core.spark_angle_deg))
        names.append("spark_align_cos")

    X = np.vstack(feats).T
    gd = gate_distance(u, [g for _, g in gates])
    return X, names, gd


# -----------------------------
# 2) Ridge regression
# -----------------------------
def ridge_fit(X: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    n, p = X.shape
    A = (X.T @ X) + lam * np.eye(p)
    b = X.T @ y
    return np.linalg.solve(A, b)


@dataclass
class FitResult:
    coef: List[float]
    feature_names: List[str]
    u_col: str
    y_col: str
    theta_col: Optional[str]
    lam: float
    rmse: float
    r2: float
    n_train: int
    use_gates: bool
    use_spark: bool
    gate_width: float


def fit_and_score(
    df: pd.DataFrame,
    u_col: str,
    y_col: str,
    core: CoreConsts,
    theta_col: Optional[str],
    lam: float,
    gate_width: Optional[float],
    use_gates: bool,
    use_spark: bool,
    mask: Optional[np.ndarray] = None,
) -> Tuple[FitResult, np.ndarray, np.ndarray, np.ndarray]:
    if y_col not in df.columns:
        raise KeyError(f"y_col='{y_col}' not found. Available: {list(df.columns)[:40]}")

    X, names, gd = build_features(df, u_col, core, theta_col, gate_width, use_gates, use_spark)
    y = df[y_col].to_numpy(dtype=float)

    valid = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    if mask is not None:
        valid = valid & mask

    Xv, yv, gdv = X[valid], y[valid], gd[valid]
    if Xv.shape[0] < 5:
        raise RuntimeError(f"Too few valid rows: {Xv.shape[0]}")

    # Fix gate_width in result
    gw = float(gate_width if gate_width is not None else max((np.nanmax(df[u_col]) - np.nanmin(df[u_col])) * 0.02, 1e-6))

    w = ridge_fit(Xv, yv, lam)
    yhat = Xv @ w
    resid = yv - yhat

    rmse = float(np.sqrt(np.mean(resid ** 2)))
    ss_tot = float(np.sum((yv - np.mean(yv)) ** 2))
    ss_res = float(np.sum(resid ** 2))
    r2 = float(1.0 - ss_res / max(ss_tot, 1e-12))

    fr = FitResult(
        coef=[float(x) for x in w],
        feature_names=names,
        u_col=u_col,
        y_col=y_col,
        theta_col=theta_col,
        lam=lam,
        rmse=rmse,
        r2=r2,
        n_train=int(Xv.shape[0]),
        use_gates=use_gates,
        use_spark=use_spark,
        gate_width=gw,
    )
    return fr, yv, yhat, gdv


def make_certificate(df: pd.DataFrame, fit: FitResult, core: CoreConsts, gate_width: Optional[float], near_thr: float) -> pd.DataFrame:
    X, names, gd = build_features(df, fit.u_col, core, fit.theta_col, gate_width, fit.use_gates, fit.use_spark)
    y = df[fit.y_col].to_numpy(dtype=float)
    w = np.array(fit.coef, dtype=float)
    yhat = X @ w
    resid = y - yhat
    out = pd.DataFrame({
        fit.u_col: df[fit.u_col].to_numpy(),
        fit.y_col: y,
        "yhat": yhat,
        "resid": resid,
        "abs_resid": np.abs(resid),
        "gate_distance": gd,
        "is_near_gate": gd <= near_thr,
    })
    # include select activations
    for j, nm in enumerate(names):
        if nm.startswith("gate_") or nm == "spark_align_cos":
            out[nm] = X[:, j]
    return out


# -----------------------------
# 3) Validation statistics
# -----------------------------
def near_far_stat(abs_resid: np.ndarray, gd: np.ndarray, near_thr: float) -> Dict[str, float]:
    near = abs_resid[gd <= near_thr]
    far = abs_resid[gd > near_thr]
    return {
        "near_n": float(near.size),
        "far_n": float(far.size),
        "near_mean_abs": float(np.mean(near)) if near.size else float("nan"),
        "far_mean_abs": float(np.mean(far)) if far.size else float("nan"),
        "ratio_near_over_far": float(np.mean(near) / max(np.mean(far), 1e-12)) if (near.size and far.size) else float("nan"),
        "delta_far_minus_near": float((np.mean(far) - np.mean(near))) if (near.size and far.size) else float("nan"),
    }


def permutation_pvalue(
    df: pd.DataFrame,
    u_col: str,
    y_col: str,
    core: CoreConsts,
    theta_col: Optional[str],
    lam: float,
    gate_width: Optional[float],
    use_gates: bool,
    use_spark: bool,
    near_thr: float,
    n_perm: int,
    rng_seed: int = 0,
) -> Dict[str, float]:
    rng = np.random.default_rng(rng_seed)

    # observed
    fit_obs, yv, yhatv, gdv = fit_and_score(df, u_col, y_col, core, theta_col, lam, gate_width, use_gates, use_spark)
    stat_obs = near_far_stat(np.abs(yv - yhatv), gdv, near_thr)["delta_far_minus_near"]

    # null distribution by shuffling y within valid rows (target permutation)
    Xfull, _, gdfull = build_features(df, u_col, core, theta_col, gate_width, use_gates, use_spark)
    yfull = df[y_col].to_numpy(dtype=float)
    valid = np.isfinite(yfull) & np.all(np.isfinite(Xfull), axis=1)

    Xv = Xfull[valid]
    yv0 = yfull[valid]
    gd0 = gdfull[valid]

    # precompute XtX once for speed? not with ridge because y changes only -> solve each time
    # keep it simple; n_perm should be modest (e.g., 200-1000)

    null_stats = []
    for _ in range(n_perm):
        yperm = rng.permutation(yv0)
        w = ridge_fit(Xv, yperm, lam)
        resid = yperm - (Xv @ w)
        s = near_far_stat(np.abs(resid), gd0, near_thr)["delta_far_minus_near"]
        null_stats.append(s)

    null_stats = np.array(null_stats, dtype=float)
    # one-sided: observed should be large positive (far - near > 0)
    p = float((np.sum(null_stats >= stat_obs) + 1.0) / (n_perm + 1.0))

    return {
        "perm_n": float(n_perm),
        "perm_stat_obs": float(stat_obs),
        "perm_stat_null_mean": float(np.mean(null_stats)),
        "perm_stat_null_std": float(np.std(null_stats)),
        "perm_p_one_sided": p,
    }


def parse_range(s: str) -> Tuple[float, float]:
    a, b = s.split(",")
    return float(a), float(b)


def stratified_holdout_masks(u: np.ndarray, n_bins: int, start: str) -> Tuple[np.ndarray, np.ndarray]:
    if n_bins < 2:
        raise ValueError("holdout_strat_bins must be >= 2")
    if start not in ("train", "test"):
        raise ValueError("holdout_strat_start must be 'train' or 'test'")

    umin = float(np.nanmin(u))
    umax = float(np.nanmax(u))
    bins = np.linspace(umin, umax, n_bins + 1)
    bin_idx = np.digitize(u, bins, right=False)
    # bins numbered 1..n_bins, alternate assignment by bin index
    if start == "train":
        train_bins = (bin_idx % 2) == 1
    else:
        train_bins = (bin_idx % 2) == 0
    train_mask = train_bins
    test_mask = ~train_bins
    return train_mask, test_mask


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    # report
    ap_r = sub.add_parser("report")
    ap_r.add_argument("--csv", required=True)
    ap_r.add_argument("--u", required=True)
    ap_r.add_argument("--y", required=True)
    ap_r.add_argument("--theta_col", default=None)
    ap_r.add_argument("--lam", type=float, default=1e-2)
    ap_r.add_argument("--gate_width", type=float, default=None)
    ap_r.add_argument("--near_thr", type=float, default=0.007)
    ap_r.add_argument("--out", default="residual_certificate.csv")
    ap_r.add_argument("--model", default="coupling_model.json")
    ap_r.add_argument("--ablate", choices=["none", "gates", "spark", "all"], default="none")

    # validate
    ap_v = sub.add_parser("validate")
    ap_v.add_argument("--csv", required=True)
    ap_v.add_argument("--u", required=True)
    ap_v.add_argument("--y", required=True)
    ap_v.add_argument("--theta_col", default=None)
    ap_v.add_argument("--lam", type=float, default=1e-2)
    ap_v.add_argument("--gate_width", type=float, default=None)
    ap_v.add_argument("--near_thr", type=float, default=0.007)
    ap_v.add_argument("--permute_y", type=int, default=0)
    ap_v.add_argument("--seed", type=int, default=0)

    ap_v.add_argument("--holdout_train", default=None, help="train range 'a,b' on u")
    ap_v.add_argument("--holdout_test", default=None, help="test range 'a,b' on u")
    ap_v.add_argument("--holdout_strat_bins", type=int, default=None, help="stratified holdout bins on u")
    ap_v.add_argument("--holdout_strat_start", default="train", choices=["train", "test"])

    ap_v.add_argument("--summary_out", default="validation_summary.csv")

    args = ap.parse_args()

    C = load_constants()
    core = CoreConsts.from_constants(C)

    df = pd.read_csv(args.csv)

    def ablation_flags(mode: str) -> Tuple[bool, bool]:
        if mode == "none":
            return True, True
        if mode == "gates":
            return False, True
        if mode == "spark":
            return True, False
        if mode == "all":
            return False, False
        raise ValueError(mode)

    # ---------------- report ----------------
    if args.cmd == "report":
        use_gates, use_spark = ablation_flags(args.ablate)

        fit, _, _, _ = fit_and_score(
            df, args.u, args.y, core, args.theta_col, args.lam, args.gate_width, use_gates, use_spark
        )
        cert = make_certificate(df, fit, core, args.gate_width, args.near_thr)
        cert.to_csv(args.out, index=False)

        with open(args.model, "w", encoding="utf-8") as f:
            json.dump(asdict(fit), f, indent=2)

        # quick print
        nf = near_far_stat(cert["abs_resid"].to_numpy(dtype=float), cert["gate_distance"].to_numpy(dtype=float), args.near_thr)
        print("[Report]")
        print("model:", args.model)
        print("certificate:", args.out)
        print("rmse:", fit.rmse, "r2:", fit.r2, "n_train:", fit.n_train)
        print("near_mean_abs:", nf["near_mean_abs"], "far_mean_abs:", nf["far_mean_abs"], "delta_far_minus_near:", nf["delta_far_minus_near"])
        return

    # ---------------- validate ----------------
    rows = []

    # baseline
    for ab in ["none", "gates", "spark", "all"]:
        use_gates, use_spark = ablation_flags(ab)
        fit, yv, yhatv, gdv = fit_and_score(df, args.u, args.y, core, args.theta_col, args.lam, args.gate_width, use_gates, use_spark)
        nf = near_far_stat(np.abs(yv - yhatv), gdv, args.near_thr)
        row = {
            "mode": f"ablate_{ab}",
            "rmse": fit.rmse,
            "r2": fit.r2,
            **nf,
        }
        rows.append(row)

    # holdout
    if args.holdout_strat_bins:
        u = df[args.u].to_numpy(dtype=float)
        train_mask, test_mask = stratified_holdout_masks(u, int(args.holdout_strat_bins), args.holdout_strat_start)
    elif args.holdout_train and args.holdout_test:
        tr0, tr1 = parse_range(args.holdout_train)
        te0, te1 = parse_range(args.holdout_test)

        u = df[args.u].to_numpy(dtype=float)
        train_mask = (u >= tr0) & (u <= tr1)
        test_mask = (u >= te0) & (u <= te1)
    else:
        train_mask = None
        test_mask = None

    if train_mask is not None and test_mask is not None:
        # fit on train
        fit_tr, ytr, yhat_tr, gd_tr = fit_and_score(
            df, args.u, args.y, core, args.theta_col, args.lam, args.gate_width, True, True, mask=train_mask
        )
        nf_tr = near_far_stat(np.abs(ytr - yhat_tr), gd_tr, args.near_thr)
        rows.append({"mode": "holdout_train", "rmse": fit_tr.rmse, "r2": fit_tr.r2, **nf_tr})

        # evaluate on test using train coefficients
        Xte, _, gd_te = build_features(df, args.u, core, args.theta_col, args.gate_width, True, True)
        yte = df[args.y].to_numpy(dtype=float)

        valid = np.isfinite(yte) & np.all(np.isfinite(Xte), axis=1) & test_mask
        Xtev = Xte[valid]
        ytev = yte[valid]
        gdtev = gd_te[valid]
        w = np.array(fit_tr.coef, dtype=float)
        yhat = Xtev @ w
        resid = ytev - yhat

        rmse = float(np.sqrt(np.mean(resid ** 2)))
        ss_tot = float(np.sum((ytev - np.mean(ytev)) ** 2))
        ss_res = float(np.sum(resid ** 2))
        r2 = float(1.0 - ss_res / max(ss_tot, 1e-12))

        nf_te = near_far_stat(np.abs(resid), gdtev, args.near_thr)
        rows.append({"mode": "holdout_test", "rmse": rmse, "r2": r2, **nf_te})

    # permutation
    if args.permute_y and args.permute_y > 0:
        perm = permutation_pvalue(
            df, args.u, args.y, core, args.theta_col, args.lam, args.gate_width,
            use_gates=True, use_spark=True, near_thr=args.near_thr, n_perm=int(args.permute_y), rng_seed=int(args.seed)
        )
        rows.append({"mode": "permute_y", **perm})

    out = pd.DataFrame(rows)
    out.to_csv(args.summary_out, index=False)
    print("[Validate] wrote:", args.summary_out)


if __name__ == "__main__":
    main()
