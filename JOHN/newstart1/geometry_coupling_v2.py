#!/usr/bin/env python3
"""
Fit a data-driven coupling model over a sweep parameter u and target y.
Uses gate-centered basis functions (RBF + logistic step) with ridge regression.
Constant-like physics terms are excluded from fit features and reported only
in the residual certificate.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from geometry_package.absolute_constants import (
    CHIRALITY_CONSTANT,
    DISCRETE_CLOSURE,
    LUNAR_CYCLE,
)


GATES = (1.0 / 64.0, 1.0 / 32.0, 1.0 / 16.0, 3.0 / 32.0)


@dataclass(frozen=True)
class ModelSpec:
    ridge: float
    sigma: float
    step_k: float
    gates: tuple[float, ...]
    with_theta: bool
    feature_names: list[str]
    coef: list[float]
    intercept: float


def _rbf(u: np.ndarray, gate: float, sigma: float) -> np.ndarray:
    return np.exp(-((u - gate) / max(sigma, 1e-12)) ** 2)


def _step(u: np.ndarray, gate: float, k: float) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-(u - gate) / max(k, 1e-12)))


def _theta_features(theta_deg: np.ndarray) -> list[tuple[str, np.ndarray]]:
    theta_rad = np.deg2rad(theta_deg)
    return [
        ("theta_sin", np.sin(theta_rad)),
        ("theta_cos", np.cos(theta_rad)),
    ]


def _build_features(u: np.ndarray, sigma: float, step_k: float, theta_deg: np.ndarray | None) -> tuple[np.ndarray, list[str]]:
    cols: list[np.ndarray] = []
    names: list[str] = []

    for gate in GATES:
        cols.append(_rbf(u, gate, sigma))
        names.append(f"gate_{gate:.6f}_rbf")
        cols.append(_step(u, gate, step_k))
        names.append(f"gate_{gate:.6f}_step")

    cols.append(u)
    names.append("u_linear")

    if theta_deg is not None:
        for name, col in _theta_features(theta_deg):
            cols.append(col)
            names.append(name)

    X = np.column_stack(cols) if cols else np.empty((u.size, 0))
    return X, names


def _fit_ridge(X: np.ndarray, y: np.ndarray, ridge: float) -> tuple[np.ndarray, float]:
    n = X.shape[0]
    X_design = np.column_stack([np.ones(n), X])
    ridge_mat = np.eye(X_design.shape[1])
    ridge_mat[0, 0] = 0.0  # do not penalize intercept
    lhs = X_design.T @ X_design + ridge * ridge_mat
    rhs = X_design.T @ y
    coef_full = np.linalg.solve(lhs, rhs)
    intercept = float(coef_full[0])
    coef = coef_full[1:]
    return coef, intercept


def _prepare_series(df: pd.DataFrame, col: str) -> np.ndarray:
    if col not in df.columns:
        raise KeyError(f"Missing column: {col}")
    series = pd.to_numeric(df[col], errors="coerce")
    return series.to_numpy()


def fit_model(csv_path: Path, u_col: str, y_col: str, theta_col: str | None, ridge: float, sigma: float, step_k: float) -> ModelSpec:
    df = pd.read_csv(csv_path)
    u_raw = _prepare_series(df, u_col)
    y_raw = _prepare_series(df, y_col)

    mask = np.isfinite(u_raw) & np.isfinite(y_raw)
    theta_vals = None
    if theta_col is not None:
        theta_raw = _prepare_series(df, theta_col)
        mask &= np.isfinite(theta_raw)
        theta_vals = theta_raw[mask]

    u_vals = u_raw[mask]
    y_vals = y_raw[mask]

    X, names = _build_features(u_vals, sigma, step_k, theta_vals)
    coef, intercept = _fit_ridge(X, y_vals, ridge)

    return ModelSpec(
        ridge=float(ridge),
        sigma=float(sigma),
        step_k=float(step_k),
        gates=tuple(GATES),
        with_theta=theta_vals is not None,
        feature_names=names,
        coef=[float(c) for c in coef],
        intercept=float(intercept),
    )


def _predict(spec: ModelSpec, df: pd.DataFrame, u_col: str, theta_col: str | None) -> np.ndarray:
    u_vals = _prepare_series(df, u_col)
    theta_vals = None
    if theta_col is not None:
        theta_vals = _prepare_series(df, theta_col)
    X, _ = _build_features(u_vals, spec.sigma, spec.step_k, theta_vals if spec.with_theta else None)
    yhat = spec.intercept + X @ np.array(spec.coef)
    return yhat


def _nearest_gate(u_vals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    gates = np.array(GATES)
    diffs = np.abs(u_vals[:, None] - gates[None, :])
    idx = np.argmin(diffs, axis=1)
    nearest = gates[idx]
    dist = diffs[np.arange(diffs.shape[0]), idx]
    return nearest, dist


def _write_model(spec: ModelSpec, path: Path) -> None:
    data = asdict(spec)
    data["gates"] = list(spec.gates)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _read_model(path: Path) -> ModelSpec:
    data = json.loads(path.read_text(encoding="utf-8"))
    return ModelSpec(
        ridge=float(data["ridge"]),
        sigma=float(data["sigma"]),
        step_k=float(data["step_k"]),
        gates=tuple(float(x) for x in data["gates"]),
        with_theta=bool(data["with_theta"]),
        feature_names=list(data["feature_names"]),
        coef=[float(c) for c in data["coef"]],
        intercept=float(data["intercept"]),
    )


def _add_certificate_fields(df: pd.DataFrame) -> None:
    df["closure_residual"] = float(DISCRETE_CLOSURE - 1.0)
    df["lunar_cycle"] = float(LUNAR_CYCLE)
    df["chirality_constant"] = float(CHIRALITY_CONSTANT)


def cmd_fit(args: argparse.Namespace) -> int:
    spec = fit_model(
        csv_path=Path(args.csv),
        u_col=args.u,
        y_col=args.y,
        theta_col=args.theta_col,
        ridge=args.ridge,
        sigma=args.sigma,
        step_k=args.step_k,
    )
    _write_model(spec, Path(args.model))
    print(f"Saved model to {args.model}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    csv_path = Path(args.csv)
    model_path = Path(args.model)

    if model_path.exists():
        spec = _read_model(model_path)
    else:
        spec = fit_model(
            csv_path=csv_path,
            u_col=args.u,
            y_col=args.y,
            theta_col=args.theta_col,
            ridge=args.ridge,
            sigma=args.sigma,
            step_k=args.step_k,
        )
        _write_model(spec, model_path)

    df = pd.read_csv(csv_path)
    yhat = _predict(spec, df, args.u, args.theta_col)

    out = pd.DataFrame()
    out[args.u] = df[args.u]
    out[args.y] = df[args.y]
    out["y_hat"] = yhat
    out["residual"] = df[args.y] - yhat

    nearest_gate, gate_dist = _nearest_gate(pd.to_numeric(df[args.u], errors="coerce").to_numpy())
    out["nearest_gate"] = nearest_gate
    out["gate_distance"] = gate_dist

    _add_certificate_fields(out)
    out.to_csv(args.out, index=False)
    print(f"Wrote residual certificate to {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Geometry coupling fit/report.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    fit_p = sub.add_parser("fit", help="Fit ridge model and save coefficients.")
    fit_p.add_argument("--csv", required=True)
    fit_p.add_argument("--u", required=True)
    fit_p.add_argument("--y", required=True)
    fit_p.add_argument("--theta_col", default=None)
    fit_p.add_argument("--ridge", type=float, default=1e-3)
    fit_p.add_argument("--sigma", type=float, default=0.02)
    fit_p.add_argument("--step_k", type=float, default=0.01)
    fit_p.add_argument("--model", default="coupling_model.json")
    fit_p.set_defaults(func=cmd_fit)

    rep_p = sub.add_parser("report", help="Generate residual certificate.")
    rep_p.add_argument("--csv", required=True)
    rep_p.add_argument("--u", required=True)
    rep_p.add_argument("--y", required=True)
    rep_p.add_argument("--theta_col", default=None)
    rep_p.add_argument("--ridge", type=float, default=1e-3)
    rep_p.add_argument("--sigma", type=float, default=0.02)
    rep_p.add_argument("--step_k", type=float, default=0.01)
    rep_p.add_argument("--model", default="coupling_model.json")
    rep_p.add_argument("--out", default="residual_certificate.csv")
    rep_p.set_defaults(func=cmd_report)

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
