"""real_biochem_fit.py

Fit 128-Z engine trajectories to REAL_CIRCADIAN_REFERENCE.csv
(published peer-reviewed cosinor parameters + Forger99 model).

No hardcoded guesses — all targets come from real literature with PMIDs.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from element_projection import project_Z, C_CONST
from universal_decoder import UniversalDecoder, UniverseState

ROOT = Path(__file__).parent
N_WIN = 128
Z_RANGE = range(1, 129)


def engine_Z_trajectory(Z):
    """Propagate Z for 128 steps; return (arg°, magnitude) per step."""
    dec = UniversalDecoder()
    es = project_Z(Z)
    st = UniverseState(z=np.array(es.state_vec, dtype=complex))
    arg = np.zeros(N_WIN); mag = np.zeros(N_WIN)
    for k in range(N_WIN):
        dec.step(st, gender="M")
        p = st.z[0] + C_CONST * st.z[1]
        arg[k] = np.degrees(np.angle(p)) % 360
        mag[k] = abs(p)
    return arg, mag


def best_phase_fit(y, x):
    """FFT-based best circular shift + sign; returns (shift_h, r_signed)."""
    x = x - x.mean(); xn = np.linalg.norm(x)
    y = y - y.mean(); yn = np.linalg.norm(y)
    Fx = np.fft.fft(x); Fy = np.fft.fft(y)
    C = np.real(np.fft.ifft(Fx * np.conj(Fy))) / (xn * yn + 1e-12)
    s = int(np.argmax(np.abs(C)))
    return s * 24 / N_WIN, float(C[s])


def peak_hour(y):
    return float(np.argmax(y)) * 24 / N_WIN


def run():
    # ── 1. Load REAL reference ─────────────────────────────────────────────
    ref_csv = ROOT / "REAL_CIRCADIAN_REFERENCE.csv"
    if not ref_csv.exists():
        raise SystemExit("Run real_circadian_download.py first.")
    ref = pd.read_csv(ref_csv)
    # Resample to 128 timepoints
    t_ref = ref["t_hour"].values
    t_target = np.linspace(0, 24, N_WIN, endpoint=False)
    hormones = {}
    for col in ref.columns:
        if col == "t_hour": continue
        y = np.interp(t_target, t_ref, ref[col].values)
        hormones[col] = y

    print("=" * 78)
    print(f"Loaded {len(hormones)} hormones from REAL_CIRCADIAN_REFERENCE.csv")
    print("=" * 78)
    for name, y in hormones.items():
        print(f"  {name:24s}  peak at t = {peak_hour(y):5.2f} h   "
              f"range [{y.min():.2f}, {y.max():.2f}]")

    # ── 2. Scan all 128 Z, find best-fitting Z for each hormone ───────────
    print("\n" + "=" * 78)
    print("Scanning all 128 Z for best-fit (sign+phase allowed)")
    print("=" * 78)
    print("(computing engine trajectories for Z=1..128, this takes ~15s)")

    traj_cache = {}
    for Z in Z_RANGE:
        arg, mag = engine_Z_trajectory(Z)
        traj_cache[Z] = {
            "arg": arg, "mag": mag,
            "cos": np.cos(np.radians(arg)),
            "sin": np.sin(np.radians(arg)),
        }

    print(f"\n{'hormone':<24} {'best_Z':>6} {'feat':>5} {'|r|':>6} "
          f"{'shift':>6} {'eng_peak':>9} {'lit_peak':>9} {'Δpeak':>7}")
    print("-" * 78)
    results = []
    for name, y in hormones.items():
        best = {"Z": 0, "feat": "", "r": 0.0, "shift": 0.0}
        for Z, feats in traj_cache.items():
            for fname, x in feats.items():
                sh, r = best_phase_fit(y, x)
                if abs(r) > abs(best["r"]):
                    best = {"Z": Z, "feat": fname, "r": r, "shift": sh}
        x = traj_cache[best["Z"]][best["feat"]]
        s = int(round(best["shift"] * N_WIN / 24))
        shifted = np.roll(x, s)
        if best["r"] < 0: shifted = -shifted
        ep = peak_hour(shifted)
        lp = peak_hour(y)
        dp = (ep - lp + 12) % 24 - 12
        results.append({"name": name, **best, "eng_peak": ep, "lit_peak": lp, "dpeak": dp})
        print(f"{name:<24} {best['Z']:>6d} {best['feat']:>5} "
              f"{abs(best['r']):>6.3f} {best['shift']:>6.2f}h "
              f"{ep:>9.2f} {lp:>9.2f} {dp:>+7.2f}h")

    # ── 3. Null benchmark: AR(1) + sine random curves ─────────────────────
    print("\n" + "=" * 78)
    print("Null benchmark: 200× AR(1)+sine random targets, same scan")
    print("=" * 78)
    rng = np.random.default_rng(42)
    null_rs = []
    # Pre-flatten features for speed
    all_feats = []
    for Z, feats in traj_cache.items():
        for fname, x in feats.items():
            all_feats.append((Z, fname, x))
    for _ in range(200):
        phi = rng.uniform(0, 2 * np.pi)
        t = np.linspace(0, 2 * np.pi, N_WIN, endpoint=False)
        noise = np.zeros(N_WIN); noise[0] = rng.normal()
        for i in range(1, N_WIN):
            noise[i] = 0.7 * noise[i - 1] + 0.3 * rng.normal()
        y = np.sin(t + phi) + 0.3 * noise
        best_r = 0.0
        for _, _, x in all_feats:
            _, r = best_phase_fit(y, x)
            if abs(r) > abs(best_r): best_r = r
        null_rs.append(abs(best_r))
    null_rs = np.array(null_rs)
    p95 = np.percentile(null_rs, 95)
    print(f"  null |r|  mean={null_rs.mean():.3f}  median={np.median(null_rs):.3f}  "
          f"95-pct={p95:.3f}  max={null_rs.max():.3f}")

    # ── 4. Verdict ────────────────────────────────────────────────────────
    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    observed = [abs(r["r"]) for r in results]
    n_beat = sum(o > p95 for o in observed)
    peak_errs = [abs(r["dpeak"]) for r in results]
    print(f"  observed |r|    = {min(observed):.3f} — {max(observed):.3f}")
    print(f"  null 95-pct     = {p95:.3f}")
    print(f"  beat null       = {n_beat}/{len(results)}")
    print(f"  mean |Δpeak|    = {np.mean(peak_errs):.2f} h")
    print(f"  max  |Δpeak|    = {np.max(peak_errs):.2f} h")
    within1 = sum(e < 1 for e in peak_errs)
    within2 = sum(e < 2 for e in peak_errs)
    print(f"  peak-time within 1h: {within1}/{len(results)}")
    print(f"  peak-time within 2h: {within2}/{len(results)}")

    if n_beat >= 3 and np.mean(peak_errs) < 2:
        print("\n  → ENGINE FITS REAL CIRCADIAN DATA  (robust)")
    elif n_beat >= 1:
        print("\n  → PARTIAL FIT  (some hormones captured, not all)")
    else:
        print("\n  → ENGINE DOES NOT CAPTURE REAL DATA  (null-indistinguishable)")

    # Save table
    out = pd.DataFrame(results)
    out.to_csv(ROOT / "REAL_BIOCHEM_FIT_RESULTS.csv", index=False)
    print(f"\n  → Saved: REAL_BIOCHEM_FIT_RESULTS.csv")


if __name__ == "__main__":
    run()
