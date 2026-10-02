"""biochem_fit.py

Compare engine trajectories against the 128-step biochemistry schedule in
HOMEOSTASIS_24_SCHEDULE_128.csv.  For each (Z, channel) pair compute the
Pearson correlation over 128 windows (24h sampled).  Report the best
Z for each channel — does it match the D3/64-channel particle mapping?
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from universal_decoder import (
    UniversalDecoder, UniverseState, project_Z, C_CONST
)

ROOT = Path(__file__).parent
N_WIN = 128
DT = 24.0 / N_WIN     # 0.1875h per window


def engine_trajectories():
    """Run each Z's engine for 128 windows; record arg, |proton|, Re, Im."""
    dec = UniversalDecoder()
    trajs = {"arg": np.zeros((128, N_WIN)), "mag": np.zeros((128, N_WIN)),
             "re":  np.zeros((128, N_WIN)), "im":  np.zeros((128, N_WIN))}
    for Z in range(1, 129):
        es = project_Z(Z)
        st = UniverseState(z=np.array(es.state_vec, dtype=complex))
        for k in range(N_WIN):
            dec.step(st, gender="M")
            p = st.z[0] + C_CONST * st.z[1]
            trajs["arg"][Z - 1, k] = np.degrees(np.angle(p)) % 360
            trajs["mag"][Z - 1, k] = abs(p)
            trajs["re"][Z - 1, k]  = p.real
            trajs["im"][Z - 1, k]  = p.imag
    return trajs


def fit_channels(trajs):
    df = pd.read_csv(ROOT / "HOMEOSTASIS_24_SCHEDULE_128.csv")
    u_cols = [c for c in df.columns if c.startswith("u_")]
    results = []
    for ch in u_cols:
        y = df[ch].to_numpy(dtype=float)
        if np.std(y) < 1e-9:
            continue
        best = {"channel": ch, "best_Z": None, "best_feat": None,
                "best_r": 0.0}
        for feat_name in ("arg", "mag", "re", "im"):
            X = trajs[feat_name]
            for Z in range(1, 129):
                x = X[Z - 1]
                if np.std(x) < 1e-9: continue
                r = np.corrcoef(x, y)[0, 1]
                if abs(r) > abs(best["best_r"]):
                    best = {"channel": ch, "best_Z": Z,
                            "best_feat": feat_name, "best_r": float(r)}
        results.append(best)
    return pd.DataFrame(results)


def main():
    print("Running 128-parallel engine for 128 windows (24h, dt=0.1875h)...")
    trajs = engine_trajectories()
    print("Fitting each u_* channel to best (Z, feature)...")
    res = fit_channels(trajs)
    res = res.sort_values("best_r", key=lambda s: s.abs(), ascending=False)
    print("\n" + "=" * 78)
    print(f"Best engine fit for each of {len(res)} biochemistry channels")
    print("=" * 78)
    print(f"{'channel':<40} {'Z':>4} {'feat':>5} {'r':>7} {'subshell':>9}")
    for _, r in res.iterrows():
        sub = project_Z(r["best_Z"]).subshell if r["best_Z"] else "-"
        print(f"{r['channel']:<40} {r['best_Z']:>4} {r['best_feat']:>5} "
              f"{r['best_r']:>+7.3f} {sub:>9}")

    strong = res[res["best_r"].abs() > 0.9]
    medium = res[(res["best_r"].abs() > 0.7) & (res["best_r"].abs() <= 0.9)]
    weak   = res[res["best_r"].abs() <= 0.7]
    print("\n" + "=" * 78)
    print(f"Fit quality summary")
    print("=" * 78)
    print(f"  |r| > 0.9 (strong)  : {len(strong):2d} / {len(res)}")
    print(f"  0.7 < |r| ≤ 0.9     : {len(medium):2d} / {len(res)}")
    print(f"  |r| ≤ 0.7 (weak)    : {len(weak):2d} / {len(res)}")

    # save
    res.to_csv(ROOT / "BIOCHEM_Z_FIT.csv", index=False)
    print(f"\nFull fit table → BIOCHEM_Z_FIT.csv")

    # ── Specifically probe well-known circadian channels ──
    print("\n" + "=" * 78)
    print("Known circadian hormones: best Z and subshell assignment")
    print("=" * 78)
    known = ["u_glucocorticoid", "u_right_cortisol", "u_left_estrogen",
             "u_right_androgen", "u_male_oxytocin", "u_vasopressin_female",
             "u_right_dopamine", "u_male_left_5ht", "u_left_endorphin",
             "u_right_alpha_2", "u_left_acetyl_coa"]
    for ch in known:
        row = res[res["channel"] == ch]
        if not row.empty:
            r = row.iloc[0]
            sub = project_Z(r["best_Z"]).subshell
            print(f"  {ch:<32}  → Z={r['best_Z']:>3} ({sub})  feat={r['best_feat']}  r={r['best_r']:+.3f}")


if __name__ == "__main__":
    main()
