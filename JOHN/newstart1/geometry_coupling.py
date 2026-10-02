#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geometry coupling layer: constants → gate features(u) → observable.

This is the missing "feature generator" bridge referenced in the geometry TODOs:
it turns discrete anchors (1/64, 1/32, 1/16, 3/32, 5/32) plus the spark angle
into a design matrix you can fit against any measured y.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from geometry_package.absolute_constants import F_1_16, F_1_32, F_1_64, F_3_32, GATE_5_32, SPARK_ANGLE_DEG
from geometry_package.tda_kappa import kappa_tda_from_p_h1
from geometry_package.universal_equation import coupling_scale, mismatch_delta, raw_tension, universal_latent


def _gaussian_gate(u: np.ndarray, *, center: float, sigma: float) -> np.ndarray:
    s = max(float(sigma), 1e-12)
    z = (u - float(center)) / s
    return np.exp(-0.5 * (z**2))


def _ridge_fit(X: np.ndarray, y: np.ndarray, l2: float) -> np.ndarray:
    lam = max(float(l2), 0.0)
    xtx = X.T @ X
    reg = lam * np.eye(X.shape[1], dtype=float)
    return np.linalg.solve(xtx + reg, X.T @ y)


def _r2(y: np.ndarray, y_hat: np.ndarray) -> float:
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - float(np.mean(y))) ** 2))
    if ss_tot <= 1e-18:
        return float("nan")
    return float(1.0 - (ss_res / ss_tot))


def build_features(
    u: np.ndarray,
    *,
    theta_deg: np.ndarray | None,
    sigma: float,
) -> tuple[np.ndarray, list[str]]:
    feature_cols: list[np.ndarray] = []
    feature_names: list[str] = []

    feature_cols.append(np.ones_like(u, dtype=float))
    feature_names.append("bias")

    gates = [
        (F_1_64, "gate_1_64"),
        (F_1_32, "gate_1_32"),
        (F_1_16, "gate_1_16"),
        (F_3_32, "gate_3_32"),
        (GATE_5_32, "gate_5_32"),
    ]
    for center, name in gates:
        feature_cols.append(_gaussian_gate(u, center=float(center), sigma=sigma))
        feature_names.append(name)

    if theta_deg is not None:
        # Spark alignment feature in degrees: cos(theta - spark)
        feature_cols.append(np.cos(np.deg2rad(theta_deg - float(SPARK_ANGLE_DEG))))
        feature_names.append("spark_align")

    X = np.column_stack(feature_cols).astype(float)
    return X, feature_names


def cmd_fit(args: argparse.Namespace) -> int:
    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    if args.u not in df.columns:
        raise SystemExit(f"Missing column for --u: {args.u}")
    if args.y not in df.columns:
        raise SystemExit(f"Missing column for --y: {args.y}")

    cols = [args.u, args.y]
    if args.theta is not None:
        if args.theta not in df.columns:
            raise SystemExit(f"Missing column for --theta: {args.theta}")
        cols.append(args.theta)

    work = df[cols].copy()
    work = work.dropna(axis=0, how="any")
    if len(work) < max(8, 2 * (6 if args.theta is None else 7)):
        raise SystemExit(f"Not enough rows after dropna: {len(work)}")

    u_raw = work[args.u].astype(float).to_numpy()
    y = work[args.y].astype(float).to_numpy()
    theta = work[args.theta].astype(float).to_numpy() if args.theta is not None else None

    if args.u_mode == "p_h1":
        if args.p_ref is None or args.p_max is None:
            raise SystemExit("--u-mode p_h1 requires --p-ref and --p-max")
        p_ref = float(args.p_ref)
        p_max = float(args.p_max)
        u = np.array([kappa_tda_from_p_h1(v, p_ref, p_max) for v in u_raw], dtype=float)
    else:
        u = u_raw

    sigma = float(args.sigma)
    X, feature_names = build_features(u, theta_deg=theta, sigma=sigma)

    w = _ridge_fit(X, y, l2=float(args.l2))
    y_hat = X @ w
    resid = y - y_hat

    print("=" * 80)
    print("GEOMETRY_COUPLING FIT")
    print("=" * 80)
    print(f"rows={len(work)} features={X.shape[1]} l2={args.l2} sigma={sigma} u_mode={args.u_mode}")
    print(f"raw_tension(analytic)={raw_tension():.12f} mismatch_delta={mismatch_delta():.12e}")
    print(f"coupling_scale(baseline)={coupling_scale():.6f} universal_latent(baseline)={universal_latent():.6f}")
    print(f"R2={_r2(y, y_hat):.6f}")
    print()
    for name, coef in zip(feature_names, w, strict=True):
        print(f"{name:>14s}  {coef:+.8e}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cert = work.copy()
    cert[f"{args.u}_kappa"] = u
    cert["y_hat"] = y_hat
    cert["residual"] = resid
    cert["abs_residual"] = np.abs(resid)
    cert.to_csv(out_path, index=False)
    print()
    print(f"[SAVED] residual certificate: {out_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="geometry_coupling.py")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fit = sub.add_parser("fit", help="Fit y from gate features along u")
    p_fit.add_argument("--csv", required=True, help="Input CSV path")
    p_fit.add_argument("--u", required=True, help="Continuous axis column (ideally κ_TDA)")
    p_fit.add_argument("--y", required=True, help="Observable column to predict")
    p_fit.add_argument("--u-mode", choices=["kappa", "p_h1"], default="kappa", help="Interpretation of --u column")
    p_fit.add_argument("--p-ref", type=float, help="Required when --u-mode p_h1: p_ref (reference H1 persistence)")
    p_fit.add_argument("--p-max", type=float, help="Required when --u-mode p_h1: p_max (max H1 persistence)")
    p_fit.add_argument("--theta", help="Optional angle column (degrees) for spark alignment feature")
    p_fit.add_argument("--sigma", type=float, default=0.01, help="Gate width for Gaussian bumps")
    p_fit.add_argument("--l2", type=float, default=1e-3, help="Ridge regularization strength")
    p_fit.add_argument(
        "--out",
        default=str(Path("out") / "geometry_coupling_residual_certificate.csv"),
        help="Output residual certificate CSV path",
    )
    p_fit.set_defaults(func=cmd_fit)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
