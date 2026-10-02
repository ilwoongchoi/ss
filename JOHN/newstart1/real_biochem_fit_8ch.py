"""real_biochem_fit_8ch.py

FIX: previous `real_biochem_fit.py` used only ONE channel (proton = z[0]+C·z[1]).
The engine carries EIGHT particles: quark, gluon, neutrino, photon, electron,
higgs, w_boson, z_boson — each with its own phase.

This script expands the search to the full 8-particle × 4-feature grid
(128 Z × 8 particles × 4 features = 4096 candidate channels) and tests:

  1. Which (Z, particle) reproduces each hormone's peak time WITHOUT any
     phase shift — a strict prediction.
  2. Null benchmark: same scan against AR(1)+sine random targets.
  3. Can the engine simultaneously cover all 5 hormone phases?
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from element_projection import project_Z
from universal_decoder import UniversalDecoder, UniverseState

ROOT = Path(__file__).parent
N_WIN = 128
PARTICLES = ["quark", "gluon", "neutrino", "photon",
             "electron", "higgs", "w_boson", "z_boson"]


def engine_trajectory_8ch(Z):
    """Return dict particle -> dict feature -> array[N_WIN].

    Each particle p exposes:
        arg  = angle (degrees) of z[p]
        mag  = |z[p]|
        cos  = cos(arg)
        sin  = sin(arg)
    """
    dec = UniversalDecoder()
    es = project_Z(Z)
    st = UniverseState(z=np.array(es.state_vec, dtype=complex))
    arg = np.zeros((8, N_WIN))
    mag = np.zeros((8, N_WIN))
    for k in range(N_WIN):
        dec.step(st, gender="M")
        for p in range(8):
            arg[p, k] = np.degrees(np.angle(st.z[p])) % 360
            mag[p, k] = abs(st.z[p])
    out = {}
    for p, name in enumerate(PARTICLES):
        out[name] = {
            "arg": arg[p], "mag": mag[p],
            "cos": np.cos(np.radians(arg[p])),
            "sin": np.sin(np.radians(arg[p])),
        }
    return out


def peak_hour(y):
    return float(np.argmax(y)) * 24 / N_WIN


def corr_no_shift(x, y):
    """Pearson r with NO circular shift allowed — strict test."""
    x = x - x.mean()
    y = y - y.mean()
    xn = np.linalg.norm(x); yn = np.linalg.norm(y)
    if xn < 1e-12 or yn < 1e-12: return 0.0
    return float(np.dot(x, y) / (xn * yn))


def run():
    # ── 1. Load REAL data ─────────────────────────────────────────────
    ref = pd.read_csv(ROOT / "REAL_CIRCADIAN_REFERENCE.csv")
    t_target = np.linspace(0, 24, N_WIN, endpoint=False)
    hormones = {}
    for col in ref.columns:
        if col == "t_hour": continue
        hormones[col] = np.interp(t_target, ref["t_hour"].values, ref[col].values)

    # ── 2. Compute all engine trajectories (128 × 8 particles) ────────
    print("Computing 128 Z × 8 particles × 4 features = 4096 channels...")
    all_traj = {}
    for Z in range(1, 129):
        all_traj[Z] = engine_trajectory_8ch(Z)
    print(f"  Done. {128*8*4} candidate channels.\n")

    # ── 3. STRICT test: no shift, no sign flip, find best (Z, part, feat) ──
    print("=" * 90)
    print("STRICT FIT (no circular shift, no sign flip)")
    print("=" * 90)
    print(f"{'hormone':<22} {'best_Z':>6} {'particle':>9} {'feat':>5} "
          f"{'r':>7} {'eng_peak':>9} {'lit_peak':>9} {'Δpeak':>7}")
    print("-" * 90)
    strict_rows = []
    for name, y in hormones.items():
        best = {"Z": 0, "part": "", "feat": "", "r": 0.0, "peak": 0.0}
        for Z in range(1, 129):
            for part in PARTICLES:
                for feat in ("arg", "mag", "cos", "sin"):
                    x = all_traj[Z][part][feat]
                    r = corr_no_shift(x, y)
                    if abs(r) > abs(best["r"]):
                        x_eff = x if r > 0 else -x
                        best = {"Z": Z, "part": part, "feat": feat, "r": r,
                                "peak": peak_hour(x_eff)}
        lp = peak_hour(y)
        dp = (best["peak"] - lp + 12) % 24 - 12
        strict_rows.append({**best, "name": name, "lit_peak": lp, "dpeak": dp})
        print(f"{name:<22} {best['Z']:>6d} {best['part']:>9} {best['feat']:>5} "
              f"{best['r']:>+7.3f} {best['peak']:>9.2f} {lp:>9.2f} {dp:>+7.2f}h")

    # ── 4. Joint simultaneous fit: single Z for all 5 hormones ────────
    print("\n" + "=" * 90)
    print("JOINT FIT — single Z, map each hormone to best particle")
    print("(tests: can ONE Z simultaneously produce all 5 acrophases?)")
    print("=" * 90)
    best_joint = {"Z": 0, "sum_abs_dp": 1e9, "details": []}
    for Z in range(1, 129):
        details = []
        sum_dp = 0.0
        for name, y in hormones.items():
            lp = peak_hour(y)
            # find best particle for this hormone at this Z
            br, bp, bpart, bfeat = 0.0, 0.0, "", ""
            for part in PARTICLES:
                for feat in ("arg", "mag", "cos", "sin"):
                    x = all_traj[Z][part][feat]
                    r = corr_no_shift(x, y)
                    if abs(r) > abs(br):
                        x_eff = x if r > 0 else -x
                        br, bp, bpart, bfeat = r, peak_hour(x_eff), part, feat
            dp = (bp - lp + 12) % 24 - 12
            details.append({"name": name, "part": bpart, "feat": bfeat,
                            "r": br, "peak": bp, "lit": lp, "dp": dp})
            sum_dp += abs(dp)
        if sum_dp < best_joint["sum_abs_dp"]:
            best_joint = {"Z": Z, "sum_abs_dp": sum_dp, "details": details}

    print(f"\nBest joint Z = {best_joint['Z']}  "
          f"(Σ|Δpeak| = {best_joint['sum_abs_dp']:.2f}h across 5 hormones)")
    print(f"{'hormone':<22} {'particle':>9} {'feat':>5} {'r':>7} "
          f"{'eng_peak':>9} {'lit_peak':>9} {'Δpeak':>7}")
    print("-" * 90)
    for d in best_joint["details"]:
        print(f"{d['name']:<22} {d['part']:>9} {d['feat']:>5} "
              f"{d['r']:>+7.3f} {d['peak']:>9.2f} {d['lit']:>9.2f} "
              f"{d['dp']:>+7.2f}h")

    # ── 5. Null benchmark (strict, 4096-channel scan) ─────────────────
    print("\n" + "=" * 90)
    print("NULL BENCHMARK — 100× random AR(1)+sine, same 4096-channel scan")
    print("=" * 90)
    rng = np.random.default_rng(42)
    null_peak_errs = []
    null_rs = []
    flat_channels = [(Z, p, f, all_traj[Z][p][f])
                     for Z in range(1, 129) for p in PARTICLES
                     for f in ("arg", "mag", "cos", "sin")]
    for trial in range(100):
        phi = rng.uniform(0, 2*np.pi)
        t = np.linspace(0, 2*np.pi, N_WIN, endpoint=False)
        noise = np.zeros(N_WIN); noise[0] = rng.normal()
        for i in range(1, N_WIN):
            noise[i] = 0.7*noise[i-1] + 0.3*rng.normal()
        y = np.sin(t + phi) + 0.3*noise
        lp = peak_hour(y)
        br, bp = 0.0, 0.0
        for _, _, _, x in flat_channels:
            r = corr_no_shift(x, y)
            if abs(r) > abs(br):
                x_eff = x if r > 0 else -x
                br, bp = r, peak_hour(x_eff)
        dp = (bp - lp + 12) % 24 - 12
        null_rs.append(abs(br))
        null_peak_errs.append(abs(dp))
    null_rs = np.array(null_rs); null_peak_errs = np.array(null_peak_errs)
    print(f"  null |r|          mean={null_rs.mean():.3f}  95-pct={np.percentile(null_rs,95):.3f}")
    print(f"  null |Δpeak| (h)  mean={null_peak_errs.mean():.2f}   95-pct={np.percentile(null_peak_errs,95):.2f}")

    # ── 6. Verdict ────────────────────────────────────────────────────
    print("\n" + "=" * 90)
    print("VERDICT")
    print("=" * 90)
    obs_dps = [abs(r["dpeak"]) for r in strict_rows]
    obs_rs = [abs(r["r"]) for r in strict_rows]
    joint_dps = [abs(d["dp"]) for d in best_joint["details"]]

    print(f"  PER-HORMONE (best Z+particle each):")
    print(f"    |r|          {min(obs_rs):.3f} — {max(obs_rs):.3f}")
    print(f"    |Δpeak| (h)  mean={np.mean(obs_dps):.2f}  max={np.max(obs_dps):.2f}")
    print(f"    within 1h: {sum(e<1 for e in obs_dps)}/5    "
          f"within 2h: {sum(e<2 for e in obs_dps)}/5")
    print(f"\n  JOINT (single Z={best_joint['Z']}, 8-particle channels):")
    print(f"    |Δpeak| (h)  mean={np.mean(joint_dps):.2f}  max={np.max(joint_dps):.2f}")
    print(f"    within 1h: {sum(e<1 for e in joint_dps)}/5    "
          f"within 2h: {sum(e<2 for e in joint_dps)}/5")
    print(f"\n  NULL (random targets):")
    print(f"    |Δpeak| (h)  mean={null_peak_errs.mean():.2f}  95-pct={np.percentile(null_peak_errs,95):.2f}")

    # Save
    pd.DataFrame(strict_rows).to_csv(ROOT/"REAL_BIOCHEM_STRICT_RESULTS.csv", index=False)
    pd.DataFrame(best_joint["details"]).to_csv(
        ROOT/f"REAL_BIOCHEM_JOINT_Z{best_joint['Z']}.csv", index=False)
    print(f"\n  → Saved: REAL_BIOCHEM_STRICT_RESULTS.csv  "
          f"REAL_BIOCHEM_JOINT_Z{best_joint['Z']}.csv")


if __name__ == "__main__":
    run()
