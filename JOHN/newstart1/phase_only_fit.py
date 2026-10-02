"""phase_only_fit.py

Constrained prediction: LOCK every hormone to Z=36 (Kr) and ONLY fit the
phase shift.  Null degrees of freedom drop from 65,536 → 128.

If the 5 hormones still land at their literature peak times (within ±1h)
with this constrained model, the finding is robust.
"""
from __future__ import annotations
import numpy as np
from pathlib import Path
from scipy.interpolate import CubicSpline
from element_projection import project_Z, C_CONST
from universal_decoder import UniversalDecoder, UniverseState

ROOT = Path(__file__).parent
N_WIN = 128
LOCK_Z = 36                # Kr, 4p⁶  — attractor for all circadian hormones


def literature_profiles():
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
        hrs_ext = np.concatenate([hrs - 24, hrs, hrs + 24])
        vals_ext = np.tile(vals, 3)
        cs = CubicSpline(hrs_ext, vals_ext)
        t = np.linspace(0, 24, N_WIN, endpoint=False)
        out[name] = cs(t)
    return out


def engine_Z_trajectory(Z):
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


def best_phase_fit(y, x, sign_allowed=True):
    x = x - x.mean(); xn = np.linalg.norm(x)
    y = y - y.mean(); yn = np.linalg.norm(y)
    Fx = np.fft.fft(x); Fy = np.fft.fft(y)
    C = np.real(np.fft.ifft(Fx * np.conj(Fy))) / (xn * yn + 1e-12)
    if sign_allowed:
        s = int(np.argmax(np.abs(C))); return s * 24 / N_WIN, float(C[s])
    s = int(np.argmax(C)); return s * 24 / N_WIN, float(C[s])


def lit_peak_time(y):
    return float(np.argmax(y)) * 24 / N_WIN


def engine_peak_time(x, shift_h, sign):
    s = int(round(shift_h * N_WIN / 24))
    shifted = np.roll(x, s)
    if sign < 0:
        shifted = -shifted
    return float(np.argmax(shifted)) * 24 / N_WIN


def null_phase_only(arg, mag, n_trials=200):
    """Null: for random AR(1)+sine, how well does Kr alone fit?"""
    rng = np.random.default_rng(7)
    feats = {"arg": arg, "mag": mag,
             "cos": np.cos(np.radians(arg)),
             "sin": np.sin(np.radians(arg))}
    null_rs = []
    for _ in range(n_trials):
        phi = rng.uniform(0, 2 * np.pi)
        t = np.linspace(0, 2 * np.pi, N_WIN, endpoint=False)
        noise = np.zeros(N_WIN); noise[0] = rng.normal()
        for i in range(1, N_WIN):
            noise[i] = 0.7 * noise[i - 1] + 0.3 * rng.normal()
        y = np.sin(t + phi) + 0.3 * noise
        best = 0.0
        for fname, x in feats.items():
            _, r = best_phase_fit(y, x)
            if abs(r) > abs(best): best = r
        null_rs.append(abs(best))
    return np.array(null_rs)


def main():
    print(f"Locking all hormones to Z={LOCK_Z} (Kr, 4p⁶)\n")
    arg_kr, mag_kr = engine_Z_trajectory(LOCK_Z)
    feats = {"arg": arg_kr, "mag": mag_kr,
             "cos": np.cos(np.radians(arg_kr)),
             "sin": np.sin(np.radians(arg_kr))}
    profiles = literature_profiles()

    print("=" * 80)
    print("Phase-only fit, Z locked to Kr (4 features × 128 shifts = 512 DOF)")
    print("=" * 80)
    print(f"{'hormone':<22} {'feat':>5} {'shift':>8} {'sign':>5} "
          f"{'|r|':>6} {'eng_peak':>9} {'lit_peak':>9} {'Δpeak':>7}")
    rows = []
    for name, y in profiles.items():
        best = {"feat": None, "shift": 0.0, "sign": +1, "r": 0.0}
        for fname, x in feats.items():
            sh, r = best_phase_fit(y, x)
            if abs(r) > abs(best["r"]):
                best = {"feat": fname, "shift": sh,
                        "sign": +1 if r > 0 else -1, "r": r}
        x = feats[best["feat"]]
        ep = engine_peak_time(x, best["shift"], best["sign"])
        lp = lit_peak_time(y)
        dp = (ep - lp + 12) % 24 - 12
        rows.append((name, best, ep, lp, dp))
        print(f"{name:<22} {best['feat']:>5} {best['shift']:>8.2f} "
              f"{best['sign']:>+5d} {abs(best['r']):>6.3f} "
              f"{ep:>9.2f} {lp:>9.2f} {dp:>+7.2f}h")

    print("\n" + "=" * 80)
    print("Null benchmark (Kr-only, phase-only)")
    print("=" * 80)
    null_rs = null_phase_only(arg_kr, mag_kr, n_trials=200)
    print(f"  null |r| mean    = {null_rs.mean():.3f}")
    print(f"  null |r| median  = {np.median(null_rs):.3f}")
    print(f"  null |r| 95-pct  = {np.percentile(null_rs, 95):.3f}")
    print(f"  null |r| max     = {null_rs.max():.3f}")
    observed = [abs(r[1]["r"]) for r in rows]
    n_beat = sum(o > np.percentile(null_rs, 95) for o in observed)
    print(f"\n  observed |r| range = {min(observed):.3f} — {max(observed):.3f}")
    print(f"  {n_beat}/5 observed beat Kr-only null 95-pct")

    print("\n" + "=" * 80)
    print("Peak-time joint test: err vs literature for all 5 hormones")
    print("=" * 80)
    peak_errs = [abs(dp) for _, _, _, _, dp in rows]
    print(f"  mean |Δpeak|  = {np.mean(peak_errs):.2f} h")
    print(f"  max  |Δpeak|  = {np.max(peak_errs):.2f} h")
    print(f"  all within 1h? {'YES ✓' if all(e < 1 for e in peak_errs) else 'NO'}")
    print(f"  all within 2h? {'YES ✓' if all(e < 2 for e in peak_errs) else 'NO'}")


if __name__ == "__main__":
    main()
