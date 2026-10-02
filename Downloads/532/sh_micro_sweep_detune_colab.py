#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, math, subprocess
from pathlib import Path
import numpy as np
import pandas as pd

GATES = np.array([1/64, 1/32, 1/16, 3/32], dtype=float)

def build_r_values(start=0.0096, end=0.0216, step=0.00025):
    n = int(round((end-start)/step)) + 1
    vals = [start + i*step for i in range(n)]
    return [v for v in vals if v >= start-1e-12 and v <= end+1e-12]

def fmt(vals):
    return ",".join(f"{v:.6g}" for v in vals)

def choose_near_thr(u_vals, start=0.001, stop=0.01, step=0.001, min_near=10):
    u = np.asarray(u_vals, dtype=float)
    for thr in np.arange(start, stop + 1e-12, step):
        gd = np.min(np.abs(u[:, None] - GATES[None, :]), axis=1)
        if int((gd <= thr).sum()) >= min_near:
            return float(thr)
    return float(stop)

def aggregate_feature_cloud(fc_csv):
    df = pd.read_csv(fc_csv)
    if "status" in df.columns:
        df = df[df["status"] == "finite"]
    grp = df.groupby(["r", "q0"], as_index=False)
    agg = grp.agg(
        psi2_mean=("psi2", "mean"),
        psi2_std=("psi2", "std"),
        n_seed=("psi2", "count"),
    )
    for col in ["amp_l2","k_peak","ring1_frac","harm_ratio","broadband_frac","psi6"]:
        if col in df.columns:
            m = df.groupby(["r","q0"])[col].mean().reset_index(name=f"{col}_mean")
            agg = agg.merge(m, on=["r","q0"], how="left")
    agg["hysteresis_area"] = np.nan
    agg["residual"] = np.nan
    return agg

def add_quant_features(df):
    psi2 = df["psi2_mean"].to_numpy(float)
    u64 = np.round(psi2 / (1/64.0)) * (1/64.0)
    err64 = psi2 - u64
    dist64 = np.abs(err64)
    err_W7 = psi2 - (math.pi/20.0)
    err_grid = psi2 - (10/64.0)
    delta_quant = (math.pi/20.0) - (10/64.0)
    df = df.copy()
    df["u64"] = u64
    df["err64"] = err64
    df["dist64"] = dist64
    df["err_W7"] = err_W7
    df["err_grid"] = err_grid
    df["delta_quant"] = delta_quant
    return df

def quant_diagnostics(df):
    err64 = df["err64"].to_numpy(float)
    dist64 = df["dist64"].to_numpy(float)
    q = np.quantile(err64, [0.1, 0.5, 0.9])
    qd = np.quantile(dist64, [0.1, 0.5, 0.9])
    return pd.DataFrame([{
        "n": len(err64),
        "err64_mean": float(np.mean(err64)),
        "err64_std": float(np.std(err64)),
        "err64_q10": float(q[0]),
        "err64_q50": float(q[1]),
        "err64_q90": float(q[2]),
        "dist64_mean": float(np.mean(dist64)),
        "dist64_std": float(np.std(dist64)),
        "dist64_q10": float(qd[0]),
        "dist64_q50": float(qd[1]),
        "dist64_q90": float(qd[2]),
        "delta_quant": float((math.pi/20.0) - (10/64.0)),
    }])

def main():
    outdir = Path("out/geometry_sweep_2d")
    outdir.mkdir(parents=True, exist_ok=True)

    r_vals = build_r_values()
    q0_vals = [0.971, 0.972, 0.973]

    run_cmd = [
        sys.executable, "runsh_detune_feature_sweep_jax.py",
        "--outdir", str(outdir),
        "--r-values", fmt(r_vals),
        "--q0-values", fmt(q0_vals),
        "--grid", "256",
        "--domain", "200.0",
        "--dt", "0.1",
        "--steps", "2000",
        "--ring-rel-width", "0.08",
        "--batch", "2",
        "--n-seeds", "40",
        "--seed-start", "0",
        "--resume",
        "--dealias",
    ]
    print("RUN:", " ".join(run_cmd))
    subprocess.check_call(run_cmd)

    fc = outdir / "feature_cloud.csv"
    agg = aggregate_feature_cloud(fc)
    agg = add_quant_features(agg)
    out_csv = outdir / "sh_micro_sweep_r_1over64.csv"
    agg.to_csv(out_csv, index=False)

    qdiag = quant_diagnostics(agg)
    qdiag.to_csv(outdir / "quantization_diagnostics_sh_micro.csv", index=False)

    near_thr = choose_near_thr(agg["r"].to_numpy(), start=0.001, stop=0.01, step=0.001, min_near=10)
    vcmd = [
        sys.executable, "geometry_coupling_v3.py", "validate",
        "--csv", str(out_csv),
        "--u", "r",
        "--y", "psi2_mean",
        "--near_thr", f"{near_thr:.6g}",
        "--holdout_strat_bins", "10",
        "--permute_y", "300",
        "--summary_out", str(outdir / "validation_sh_micro_r_1over64.csv"),
    ]
    print("VALIDATE:", " ".join(vcmd))
    subprocess.check_call(vcmd)

    print("DONE")
    print(out_csv)
    print(outdir / "validation_sh_micro_r_1over64.csv")
    print(outdir / "quantization_diagnostics_sh_micro.csv")

if __name__ == "__main__":
    main()
