#!/usr/bin/env python
import argparse, json, math
import numpy as np
import pandas as pd

GATES = np.array([1/64, 1/32, 1/16, 3/32], dtype=float)

def gate_distance(u):
    u = np.asarray(u, dtype=float)
    return np.min(np.abs(u[:, None] - GATES[None, :]), axis=1)

def stratified_holdout(df, u_col, bins=10, start=0):
    u = df[u_col].to_numpy()
    order = np.argsort(u)
    bins_idx = np.array_split(order, bins)
    train_idx, test_idx = [], []
    toggle = start % 2
    for i, idx in enumerate(bins_idx):
        if (i + toggle) % 2 == 0:
            train_idx.extend(idx.tolist())
        else:
            test_idx.extend(idx.tolist())
    return np.array(train_idx), np.array(test_idx)

def fit_bias(X, y):
    # simple ridge on bias only (or linear). Here just mean.
    mu = float(np.mean(y))
    return mu

def predict_bias(mu, n):
    return np.full(n, mu, dtype=float)

def eval_delta(df, u_col, y_col, near_thr):
    u = df[u_col].to_numpy()
    y = df[y_col].to_numpy()
    gd = gate_distance(u)
    near = gd <= near_thr
    if near.sum() == 0 or (~near).sum() == 0:
        return dict(delta_far_minus_near=np.nan, near_n=int(near.sum()), far_n=int((~near).sum()))
    # simple baseline: absolute residual vs mean
    mu = np.mean(y)
    resid = np.abs(y - mu)
    near_mean = resid[near].mean()
    far_mean = resid[~near].mean()
    return dict(delta_far_minus_near=float(far_mean - near_mean), near_n=int(near.sum()), far_n=int((~near).sum()))

def perm_pvalue(df, u_col, y_col, near_thr, n_perm=300):
    base = eval_delta(df, u_col, y_col, near_thr)["delta_far_minus_near"]
    if not np.isfinite(base):
        return np.nan
    y = df[y_col].to_numpy()
    count = 0
    for _ in range(n_perm):
        y_perm = np.random.permutation(y)
        tmp = df.copy()
        tmp[y_col] = y_perm
        d = eval_delta(tmp, u_col, y_col, near_thr)["delta_far_minus_near"]
        if d >= base:
            count += 1
    return float((count + 1) / (n_perm + 1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["validate"])
    ap.add_argument("--csv", required=True)
    ap.add_argument("--u", required=True)
    ap.add_argument("--y", required=True)
    ap.add_argument("--near_thr", type=float, required=True)
    ap.add_argument("--holdout_strat_bins", type=int, default=10)
    ap.add_argument("--permute_y", type=int, default=300)
    ap.add_argument("--summary_out", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    df = df.dropna(subset=[args.u, args.y]).copy()

    tr_idx, te_idx = stratified_holdout(df, args.u, bins=args.holdout_strat_bins)
    df_train = df.iloc[tr_idx].copy()
    df_test = df.iloc[te_idx].copy()

    rows = []
    for name, d in [("train", df_train), ("test", df_test)]:
        ed = eval_delta(d, args.u, args.y, args.near_thr)
        mu = float(np.mean(d[args.y]))
        resid = d[args.y] - mu
        ss_res = float(np.sum(resid**2))
        ss_tot = float(np.sum((d[args.y]-np.mean(d[args.y]))**2)) + 1e-12
        r2 = 1.0 - ss_res/ss_tot
        rows.append({
            "split": name,
            "delta_far_minus_near": ed["delta_far_minus_near"],
            "near_n": ed["near_n"],
            "far_n": ed["far_n"],
            "r2": r2,
        })

    perm_p = perm_pvalue(df, args.u, args.y, args.near_thr, n_perm=args.permute_y)
    rows.append({"split":"permute_y", "perm_p_one_sided": perm_p})

    out = pd.DataFrame(rows)
    out.to_csv(args.summary_out, index=False)
    print(out)

if __name__ == "__main__":
    main()
