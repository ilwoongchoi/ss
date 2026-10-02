import argparse
import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd


def _infer_grid_axes(df: pd.DataFrame):
    rs = np.sort(df["r"].unique())
    qs = np.sort(df["q0"].unique())
    return rs, qs


def _pivot_grid(df: pd.DataFrame, rs, qs, value_col: str, fill=0.0):
    """
    Pivot (r,q0)->value into (len(rs), len(qs)) grid.
    Assumes df has one row per (r,q0) for the requested value_col.
    """
    g = df.pivot(index="r", columns="q0", values=value_col).reindex(index=rs, columns=qs)
    return g.fillna(fill).values.astype(float)


def _load_turn_ridges(pattern: str):
    ridges = []
    for fn in sorted(glob.glob(pattern)):
        m = Path(fn).stem
        # expects ..._turn{n}_ridge.csv
        # parse the last "turn" occurrence
        tidx = None
        for token in m.split("_"):
            if token.startswith("turn"):
                try:
                    tidx = int(token.replace("turn", ""))
                except Exception:
                    pass
        if tidx is None:
            continue
        rdf = pd.read_csv(fn)
        ridges.append((tidx, rdf))
    ridges.sort(key=lambda x: x[0])
    return ridges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per_turn_csv", required=True, help="*_per_turn.csv produced by --per_turn")
    ap.add_argument("--out", required=True, help="Output .npz path")
    ap.add_argument("--base_csv", default=None, help="Optional overall map CSV (non-turn)")
    ap.add_argument("--turn_ridge_glob", default=None, help="Optional glob for turn ridge CSVs")
    ap.add_argument("--min_eligible", type=float, default=None, help="Optional mask threshold (set values to 0 where eligible < thr)")
    args = ap.parse_args()

    per_df = pd.read_csv(args.per_turn_csv)

    # Expected per-turn columns (flexible):
    # required: turn or turn_idx, r, q0
    # typical: eligibleB_mean, sparksB_mean, expectedB_mean, rate_post_mean, w_gate_sim
    turn_col = "turn" if "turn" in per_df.columns else "turn_idx"
    required = {turn_col, "r", "q0"}
    if not required.issubset(per_df.columns):
        raise ValueError(f"per_turn_csv missing required columns: {required - set(per_df.columns)}")

    rs, qs = _infer_grid_axes(per_df)

    # Turns
    turns = np.sort(per_df[turn_col].unique()).astype(int)
    T = len(turns)
    R = len(rs)
    Q = len(qs)

    def col_or_fallback(cands):
        for c in cands:
            if c in per_df.columns:
                return c
        return None

    col_elig = col_or_fallback(["eligibleB_mean", "eligibleB", "eligible_mean", "eligible"])
    col_rate = col_or_fallback(["rate_post_mean", "rate_mean", "rate_post", "rate"])
    col_exp = col_or_fallback(["expectedB_mean", "expectedB", "expected_mean", "expected"])
    col_sparks = col_or_fallback(["sparksB_mean", "sparksB", "sparks_mean", "sparks"])
    col_w = col_or_fallback(["w_gate_sim", "w_gate", "w"])

    if col_rate is None:
        raise ValueError("No rate column found in per_turn_csv (expected rate_post_mean or similar).")
    if col_w is None:
        raise ValueError("No w_gate column found in per_turn_csv (expected w_gate_sim or similar).")

    # Allocate tensors
    rate_turn = np.zeros((T, R, Q), dtype=float)
    elig_turn = np.zeros((T, R, Q), dtype=float) if col_elig else None
    exp_turn = np.zeros((T, R, Q), dtype=float) if col_exp else None
    sparks_turn = np.zeros((T, R, Q), dtype=float) if col_sparks else None

    # w_gate is constant across turns (should be); take from any subset (turn 0)
    w_df = per_df[per_df[turn_col] == turns[0]][["r", "q0", col_w]].copy()
    w_gate_grid = _pivot_grid(w_df.rename(columns={col_w: "val"}), rs, qs, "val", fill=0.0)

    # Fill per-turn grids
    for ti, t in enumerate(turns):
        sdf = per_df[per_df[turn_col] == t]

        tmp = sdf[["r", "q0", col_rate]].rename(columns={col_rate: "val"})
        rate_turn[ti] = _pivot_grid(tmp, rs, qs, "val", fill=0.0)

        if col_elig:
            tmp = sdf[["r", "q0", col_elig]].rename(columns={col_elig: "val"})
            elig_turn[ti] = _pivot_grid(tmp, rs, qs, "val", fill=0.0)

        if col_exp:
            tmp = sdf[["r", "q0", col_exp]].rename(columns={col_exp: "val"})
            exp_turn[ti] = _pivot_grid(tmp, rs, qs, "val", fill=0.0)

        if col_sparks:
            tmp = sdf[["r", "q0", col_sparks]].rename(columns={col_sparks: "val"})
            sparks_turn[ti] = _pivot_grid(tmp, rs, qs, "val", fill=0.0)

    # Optional masking
    mask_turn = None
    if args.min_eligible is not None and elig_turn is not None:
        mask_turn = elig_turn >= float(args.min_eligible)
        rate_turn = np.where(mask_turn, rate_turn, 0.0)
        if exp_turn is not None:
            exp_turn = np.where(mask_turn, exp_turn, 0.0)
        if sparks_turn is not None:
            sparks_turn = np.where(mask_turn, sparks_turn, 0.0)

    # Optional overall grids (non-turn)
    rate = None
    elig = None
    exp = None
    sparks = None
    if args.base_csv:
        base = pd.read_csv(args.base_csv)
        if {"r", "q0"}.issubset(base.columns):
            def bcol_or_fallback(cands):
                for c in cands:
                    if c in base.columns:
                        return c
                return None

            b_col_rate = bcol_or_fallback(["rate_post_mean", "rate_mean", "rate_post", "rate"])
            b_col_elig = bcol_or_fallback(["eligibleB_mean", "eligibleB", "eligible_mean", "eligible"])
            b_col_exp = bcol_or_fallback(["expectedB_mean", "expectedB", "expected_mean", "expected"])
            b_col_sparks = bcol_or_fallback(["sparksB_mean", "sparksB", "sparks_mean", "sparks"])

            if b_col_rate:
                rate = _pivot_grid(base[["r", "q0", b_col_rate]].rename(columns={b_col_rate: "val"}), rs, qs, "val", fill=0.0)
            if b_col_elig:
                elig = _pivot_grid(base[["r", "q0", b_col_elig]].rename(columns={b_col_elig: "val"}), rs, qs, "val", fill=0.0)
            if b_col_exp:
                exp = _pivot_grid(base[["r", "q0", b_col_exp]].rename(columns={b_col_exp: "val"}), rs, qs, "val", fill=0.0)
            if b_col_sparks:
                sparks = _pivot_grid(base[["r", "q0", b_col_sparks]].rename(columns={b_col_sparks: "val"}), rs, qs, "val", fill=0.0)

            # base mask
            if args.min_eligible is not None and elig is not None:
                m = elig >= float(args.min_eligible)
                if rate is not None:
                    rate = np.where(m, rate, 0.0)
                if exp is not None:
                    exp = np.where(m, exp, 0.0)
                if sparks is not None:
                    sparks = np.where(m, sparks, 0.0)

    # Optional ridge paths (turn-wise)
    ridge_turn_q0 = None
    ridge_turn_r = None
    if args.turn_ridge_glob:
        ridges = _load_turn_ridges(args.turn_ridge_glob)
        if ridges:
            # store as ragged arrays via object, or pad to max length
            maxlen = max(len(df) for _, df in ridges)
            ridge_turn_q0 = np.full((T, maxlen), np.nan, dtype=float)
            ridge_turn_r = np.full((T, maxlen), np.nan, dtype=float)
            for tidx, rdf in ridges:
                if tidx in turns:
                    ti = int(np.where(turns == tidx)[0][0])
                    L = len(rdf)
                    if "q0" in rdf.columns and "r" in rdf.columns:
                        ridge_turn_q0[ti, :L] = rdf["q0"].values
                        ridge_turn_r[ti, :L] = rdf["r"].values

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Save bundle
    np.savez_compressed(
        out_path,
        r_axis=rs,
        q0_axis=qs,
        turns=turns,
        w_gate=w_gate_grid,
        rate_turn=rate_turn,
        eligible_turn=elig_turn if elig_turn is not None else np.array([]),
        expected_turn=exp_turn if exp_turn is not None else np.array([]),
        sparks_turn=sparks_turn if sparks_turn is not None else np.array([]),
        mask_turn=mask_turn if mask_turn is not None else np.array([]),
        rate=rate if rate is not None else np.array([]),
        eligible=elig if elig is not None else np.array([]),
        expected=exp if exp is not None else np.array([]),
        sparks=sparks if sparks is not None else np.array([]),
        ridge_turn_q0=ridge_turn_q0 if ridge_turn_q0 is not None else np.array([]),
        ridge_turn_r=ridge_turn_r if ridge_turn_r is not None else np.array([]),
        meta=json.dumps(
            {
                "per_turn_csv": str(args.per_turn_csv),
                "base_csv": str(args.base_csv) if args.base_csv else None,
                "turn_ridge_glob": str(args.turn_ridge_glob) if args.turn_ridge_glob else None,
                "min_eligible": args.min_eligible,
                "columns": {
                    "rate": col_rate,
                    "eligible": col_elig,
                    "expected": col_exp,
                    "sparks": col_sparks,
                    "w_gate": col_w,
                    "turn": turn_col,
                },
            },
            ensure_ascii=False,
        ),
    )

    print(f"[OK] Saved grid tensor: {out_path}")
    print(f"  axes: R={len(rs)} Q={len(qs)} turns={len(turns)}")
    if args.min_eligible is not None:
        print(f"  mask: min_eligible={args.min_eligible}")
    if args.turn_ridge_glob:
        print(f"  ridge turn paths: {args.turn_ridge_glob}")


if __name__ == "__main__":
    main()
