"""literature_circadian_fit.py

Real-ish biochemistry comparison.  Circadian profiles below are APPROXIMATE
values typed from memory of standard physiology references (Brzezinski 1997,
Czeisler 1999, Van Cauter 1996, Kräuchi 2007, Diver 2003) — NOT extracted
from original figures.  Accurate to ±20%.  Use for *shape* and *phase*
verification; do not cite absolute pg/mL from here.

For each literature profile, find best (Z, feature, phase-shift) fit.  We
allow circular phase shift because the engine's t=0 need not be local
midnight.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.interpolate import CubicSpline
from element_projection import project_Z, C_CONST
from universal_decoder import UniversalDecoder, UniverseState

ROOT = Path(__file__).parent
N_WIN = 128


def literature_profiles():
    """Approximate daily profiles, hour → value."""
    profiles = {
        "melatonin_pg_mL":   {0:50, 2:70, 4:55, 6:30, 8:10, 10:5, 12:5,
                              14:5, 16:8, 18:12, 20:20, 22:40},
        "cortisol_ug_dL":    {0:6, 2:8, 4:12, 6:16, 8:18, 10:14, 12:10,
                              14:7, 16:5, 18:4, 20:3, 22:4},
        "GH_ng_mL":          {0:12, 2:15, 4:8, 6:3, 8:2, 10:1.5, 12:1.5,
                              14:2, 16:2, 18:2.5, 20:3, 22:6},
        "core_temp_C":       {0:36.8, 2:36.6, 4:36.4, 6:36.3, 8:36.5,
                              10:36.7, 12:36.9, 14:37.0, 16:37.05, 18:37.1,
                              20:37.0, 22:36.9},
        "testosterone_ng_dL":{0:650, 2:700, 4:720, 6:700, 8:700, 10:650,
                              12:600, 14:560, 16:530, 18:500, 20:460, 22:520},
    }
    out = {}
    for name, d in profiles.items():
        hrs = np.array(sorted(d.keys()), dtype=float)
        vals = np.array([d[h] for h in hrs])
        # wrap periodic
        hrs_ext = np.concatenate([hrs - 24, hrs, hrs + 24])
        vals_ext = np.tile(vals, 3)
        cs = CubicSpline(hrs_ext, vals_ext)
        t = np.linspace(0, 24, N_WIN, endpoint=False)
        out[name] = cs(t)
    return out


def engine_tensor():
    dec = UniversalDecoder()
    arg = np.zeros((128, N_WIN)); mag = np.zeros((128, N_WIN))
    for Z in range(1, 129):
        es = project_Z(Z)
        st = UniverseState(z=np.array(es.state_vec, dtype=complex))
        for k in range(N_WIN):
            dec.step(st, gender="M")
            p = st.z[0] + C_CONST * st.z[1]
            arg[Z - 1, k] = np.degrees(np.angle(p)) % 360
            mag[Z - 1, k] = abs(p)
    return arg, mag


def best_fit(y: np.ndarray, arg: np.ndarray, mag: np.ndarray):
    feats = {"arg": arg, "mag": mag,
             "cos_arg": np.cos(np.radians(arg)),
             "sin_arg": np.sin(np.radians(arg))}
    best = {"Z": None, "feat": None, "shift_h": 0.0, "r": 0.0}
    for feat_name, X in feats.items():
        for Z in range(128):
            x = X[Z]
            if np.std(x) < 1e-9: continue
            # vectorised circular shift + correlation
            for s in range(N_WIN):
                xs = np.roll(x, s)
                r = np.corrcoef(xs, y)[0, 1]
                if abs(r) > abs(best["r"]):
                    best = {"Z": Z + 1, "feat": feat_name,
                            "shift_h": s * 24 / N_WIN, "r": float(r)}
    return best


def main():
    print("Sampling literature profiles (128 windows)...")
    profiles = literature_profiles()
    print("Running 128-Z engine (128 windows)...")
    arg, mag = engine_tensor()

    print("\n" + "=" * 78)
    print("Best engine fit for literature profiles")
    print("=" * 78)
    print(f"{'profile':<22} {'Z':>4} {'subshell':>8} {'feat':>8} "
          f"{'shift[h]':>9} {'r':>7}")
    rows = []
    for name, y in profiles.items():
        b = best_fit(y, arg, mag)
        sub = project_Z(b["Z"]).subshell
        print(f"{name:<22} {b['Z']:>4} {sub:>8} {b['feat']:>8} "
              f"{b['shift_h']:>9.2f} {b['r']:>+7.3f}")
        rows.append({"profile": name, **b, "subshell": sub})
    pd.DataFrame(rows).to_csv(ROOT / "LITERATURE_BIOCHEM_FIT.csv", index=False)

    # Shuffle null: random-curve fits typically reach |r|=?
    print("\n" + "=" * 78)
    print("Null benchmark: fit random circadian-like curves (AR(1)+sine)")
    print("=" * 78)
    rng = np.random.default_rng(0)
    null_rs = []
    for trial in range(50):
        # random curve = sine at random phase + AR(1) noise
        phi = rng.uniform(0, 2 * np.pi)
        amp = 1.0
        noise = np.zeros(N_WIN); noise[0] = rng.normal()
        for i in range(1, N_WIN):
            noise[i] = 0.7 * noise[i-1] + 0.3 * rng.normal()
        t = np.linspace(0, 2*np.pi, N_WIN, endpoint=False)
        y_null = amp * np.sin(t + phi) + 0.3 * noise
        b = best_fit(y_null, arg, mag)
        null_rs.append(abs(b["r"]))
    print(f"  Null-fit |r| mean   = {np.mean(null_rs):.3f}")
    print(f"  Null-fit |r| 95-pct = {np.percentile(null_rs, 95):.3f}")
    print(f"  Null-fit |r| max    = {np.max(null_rs):.3f}")
    print("  → literature profiles should beat null 95-pct to be meaningful")


if __name__ == "__main__":
    main()
