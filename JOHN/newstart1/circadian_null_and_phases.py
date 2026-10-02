"""circadian_null_and_phases.py

Two follow-up analyses on literature_circadian_fit.py:

(A) NULL BENCHMARK
    Generate random AR(1)+sine curves and best-fit each against the 128-Z
    engine tensor.  Report 95-pct |r| — observed fits must beat this.

(B) PHASE RELATIONSHIPS
    The three hormones that collapsed onto Kr (Z=36) differ only in phase
    and sign.  Check whether their engine-fit shifts match the known
    physiological phase gaps.
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


def _circ_corr_all_shifts(X, y):
    """Vectorised Pearson across all circular shifts via FFT.
    X shape (n, N); y shape (N).  Returns (n, N) of r values (shift s = col).
    """
    X = X - X.mean(axis=1, keepdims=True)
    y = y - y.mean()
    Xn = np.linalg.norm(X, axis=1, keepdims=True)
    yn = np.linalg.norm(y)
    # cross-correlation via FFT: c[s] = sum_t X[t] * y[(t-s) mod N]
    FX = np.fft.fft(X, axis=1)
    Fy = np.fft.fft(y)
    C = np.real(np.fft.ifft(FX * np.conj(Fy)[None, :], axis=1))
    denom = Xn * yn + 1e-12
    return C / denom


def best_fit(y, arg, mag):
    feats = {"arg": arg, "mag": mag,
             "cos_arg": np.cos(np.radians(arg)),
             "sin_arg": np.sin(np.radians(arg))}
    best = {"Z": None, "feat": None, "shift_h": 0.0, "r": 0.0}
    for feat_name, X in feats.items():
        R = _circ_corr_all_shifts(X, y)        # (128, 128)
        idx = np.unravel_index(np.argmax(np.abs(R)), R.shape)
        r = float(R[idx])
        if abs(r) > abs(best["r"]):
            best = {"Z": int(idx[0] + 1), "feat": feat_name,
                    "shift_h": float(idx[1] * 24 / N_WIN), "r": r}
    return best


def null_benchmark(arg, mag, n_trials=100):
    rng = np.random.default_rng(42)
    null_rs = []
    for _ in range(n_trials):
        phi = rng.uniform(0, 2 * np.pi)
        t = np.linspace(0, 2 * np.pi, N_WIN, endpoint=False)
        noise = np.zeros(N_WIN); noise[0] = rng.normal()
        for i in range(1, N_WIN):
            noise[i] = 0.7 * noise[i - 1] + 0.3 * rng.normal()
        y = np.sin(t + phi) + 0.3 * noise
        b = best_fit(y, arg, mag)
        null_rs.append(abs(b["r"]))
    return np.array(null_rs)


def phase_analysis():
    """Observed vs literature phase gaps.

    Literature PEAK times:
      Melatonin:  02:00 — 03:00
      Cortisol :  08:00 — 09:00
      Core temp:  17:00 — 18:00
    Expected gaps (from melatonin peak):
      cortisol  - melatonin =  +6 h
      core_temp - melatonin = +15 h
      core_temp - cortisol  =  +9 h

    Engine-fit shifts (from literature_circadian_fit.py):
      melatonin = 16.69h (sin_arg, −)
      cortisol  = 22.50h (sin_arg, −)
      core_temp = 20.25h (sin_arg, +)

    But sign matters: sin_arg with − sign is phase-reversed vs +.  Effective
    phase = shift_h + (π if sign < 0)  in "equivalent-waveform" units.
    """
    engine_shifts = {
        "melatonin": (16.69, -1),
        "cortisol":  (22.50, -1),
        "core_temp": (20.25, +1),
    }
    # convert to effective phase (mod 24)
    def eff_phase(h, sign):
        return (h + (12 if sign < 0 else 0)) % 24
    print(f"{'hormone':<12} {'shift':>8} {'sign':>5} {'eff_phase':>10}")
    effs = {}
    for k, (h, s) in engine_shifts.items():
        e = eff_phase(h, s)
        effs[k] = e
        print(f"{k:<12} {h:>8.2f} {s:>5d} {e:>10.2f}")

    lit_peak = {"melatonin": 2.5, "cortisol": 8.5, "core_temp": 17.5}
    print("\nEngine effective phase vs literature peak time:")
    print(f"{'hormone':<12} {'engine':>8} {'lit_peak':>9} {'diff':>8}")
    for k in lit_peak:
        diff = (effs[k] - lit_peak[k]) % 24
        if diff > 12: diff -= 24
        print(f"{k:<12} {effs[k]:>8.2f} {lit_peak[k]:>9.2f} {diff:>+8.2f}h")

    print("\nPhase GAPS (engine vs literature):")
    pairs = [("cortisol", "melatonin"), ("core_temp", "melatonin"),
             ("core_temp", "cortisol")]
    for a, b in pairs:
        eng_gap = (effs[a] - effs[b]) % 24
        if eng_gap > 12: eng_gap -= 24
        lit_gap = (lit_peak[a] - lit_peak[b]) % 24
        if lit_gap > 12: lit_gap -= 24
        print(f"  {a} - {b:<10}:  engine={eng_gap:+6.2f}h   "
              f"literature={lit_gap:+6.2f}h   "
              f"err={eng_gap - lit_gap:+6.2f}h")


def main():
    print("Building engine tensor...")
    arg, mag = engine_tensor()

    print("\n" + "=" * 72)
    print("Null benchmark: 100 random AR(1)+sine curves best-fit to engine")
    print("=" * 72)
    null_rs = null_benchmark(arg, mag, n_trials=100)
    print(f"  null |r| mean    = {null_rs.mean():.3f}")
    print(f"  null |r| median  = {np.median(null_rs):.3f}")
    print(f"  null |r| 95-pct  = {np.percentile(null_rs, 95):.3f}")
    print(f"  null |r| max     = {null_rs.max():.3f}")
    observed = [0.914, 0.966, 0.917, 0.958, 0.976]
    print(f"\n  observed |r| range = {min(observed):.3f} — {max(observed):.3f}")
    n_beat = sum(o > np.percentile(null_rs, 95) for o in observed)
    print(f"  {n_beat}/5 observed fits beat null 95-pct "
          f"({'ALL STRONG ✓' if n_beat == 5 else 'partial'})")

    print("\n" + "=" * 72)
    print("Phase-gap analysis: engine-fit shifts vs known peak times")
    print("=" * 72)
    phase_analysis()


if __name__ == "__main__":
    main()
