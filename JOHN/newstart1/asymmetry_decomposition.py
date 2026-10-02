"""asymmetry_decomposition.py

User thesis: "angle is symmetric, magnitude is asymmetric."
This module quantifies *where the asymmetry comes from* by layering 3 physical
sources and measuring how much of the real NIST ionization-energy variance
each one explains.

Layer 1 — SYMMETRIC:         IE = R × Z² / n²                  (bare Coulomb)
Layer 2 — SHELL ASYMMETRY:   IE = R × (Z-S_slater)² / n_eff²   (Slater screen)
Layer 3 — EXCHANGE ASYMMETRY: +  half-fill/closed-shell correction
                                 (Hund's rule exchange energy)

For each layer we report:
  * Pearson r to NIST
  * MAPE (% error)
  * RMS [eV]
  * Explained variance (R²)

If Layer 3 explains >95% variance with residual <1 eV, the MAGNITUDE problem
is solved for the 72 elements we have NIST data for, and ΔS/state-vector
magnitudes can now be calibrated in eV.
"""
from __future__ import annotations
import numpy as np
from magnitude_engine import (IE_NIST, RYDBERG, N_EFF_TABLE,
                              _shell_occupations, _slater_screening,
                              predicted_ionization_energy)

# ───────────────────────── Layer 1: bare Coulomb ────────────────────────────
def ie_layer1(Z: int) -> float:
    groups = _shell_occupations(Z)
    n_out, _, _ = groups[-1]
    return RYDBERG * Z ** 2 / n_out ** 2


# ───────────────────────── Layer 2: Slater screening ───────────────────────
def ie_layer2(Z: int) -> float:
    return predicted_ionization_energy(Z)["IE_pred_eV"]


# ───────────────── Layer 3: exchange + shell-drop asymmetry ────────────────
# Empirical per-subshell calibration factor α(n, ell) fit from first 3 elements
# of that subshell, then applied to the rest — tests *extrapolation*.
def _fit_subshell_factors(train_frac: float = 0.4):
    """Group IE_NIST by (n_out, ell_out), fit multiplicative α from half the data."""
    by_group = {}
    for Z, real in IE_NIST.items():
        p = predicted_ionization_energy(Z)
        key = (p["n_out"], p["ell_out"])
        pred = p["IE_pred_eV"]
        by_group.setdefault(key, []).append((Z, pred, real))
    alpha = {}
    train_ids = set()
    for key, rows in by_group.items():
        rows.sort()
        n_train = max(1, int(len(rows) * train_frac))
        train = rows[:n_train]
        ratios = [real / pred for _, pred, real in train if pred > 0]
        alpha[key] = float(np.mean(ratios)) if ratios else 1.0
        for Z, _, _ in train:
            train_ids.add(Z)
    return alpha, train_ids


def ie_layer3(Z: int, alpha: dict) -> float:
    p = predicted_ionization_energy(Z)
    key = (p["n_out"], p["ell_out"])
    base = p["IE_pred_eV"]
    # Layer-3 exchange correction: half-filled subshell stability (Hund)
    # When subshell is *just past* half-fill, an extra electron destabilises
    # (e.g. N→O, P→S, Mn→Fe) — IE drops slightly.
    k_out = p["k_out"]
    cap = {"s": 2, "p": 6, "d": 10, "f": 14, "g": 18}[p["ell_out"]]
    half = cap / 2
    exchange = 0.0
    if k_out == half + 1:
        exchange = -0.08 * base   # 8% dip just past half-fill
    elif k_out == half:
        exchange = +0.03 * base   # 3% bump at exact half-fill
    return alpha.get(key, 1.0) * (base + exchange)


# ───────────────────────── scoring ──────────────────────────────────────────
def score(pred_fn, label, exclude_ids=None):
    preds, reals = [], []
    for Z, real in IE_NIST.items():
        if exclude_ids and Z not in exclude_ids:
            continue
        preds.append(pred_fn(Z)); reals.append(real)
    preds = np.array(preds); reals = np.array(reals)
    err = preds - reals
    rms  = float(np.sqrt(np.mean(err ** 2)))
    mape = float(np.mean(np.abs(err / reals)) * 100)
    r    = float(np.corrcoef(preds, reals)[0, 1])
    ss_res = float(np.sum(err ** 2))
    ss_tot = float(np.sum((reals - reals.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot
    return {"label": label, "n": len(preds), "pearson_r": r,
            "rms_eV": rms, "mape_pct": mape, "R2": r2}


def print_report():
    alpha, train_ids = _fit_subshell_factors(train_frac=0.4)
    test_ids = set(IE_NIST) - train_ids

    layers = [
        score(ie_layer1,                         "L1  Coulomb Z²/n² (symmetric)"),
        score(ie_layer2,                         "L2  Slater screening (shell asym.)"),
        score(lambda Z: ie_layer3(Z, alpha),     "L3  + subshell α + Hund exchange"),
        score(lambda Z: ie_layer3(Z, alpha), "L3 (test only)", exclude_ids=test_ids),
    ]
    print(f"{'layer':<40}  {'n':>4}  {'r':>6}  {'R²':>7}  {'RMS[eV]':>9}  {'MAPE%':>7}")
    print("-" * 88)
    for s in layers:
        print(f"{s['label']:<40}  {s['n']:>4}  {s['pearson_r']:>6.3f}  "
              f"{s['R2']:>7.3f}  {s['rms_eV']:>9.3f}  {s['mape_pct']:>7.2f}")
    print()
    print("Per-subshell calibration factors α(n, ell):")
    for (n, ell), a in sorted(alpha.items()):
        print(f"  ({n}{ell})  α = {a:.4f}")

    print("\nSample L3 predictions:")
    print(f"{'Z':>3}  {'sub':>4}  {'IE_pred':>8}  {'IE_NIST':>8}  {'err':>7}  {'err%':>7}  {'set':>5}")
    for Z in sorted(IE_NIST):
        if Z > 40 and Z not in (46, 54, 74, 79, 86): continue
        pred = ie_layer3(Z, alpha)
        real = IE_NIST[Z]
        p = predicted_ionization_energy(Z)
        tag = f"{p['n_out']}{p['ell_out']}"
        setname = "train" if Z in train_ids else "TEST"
        print(f"{Z:>3}  {tag:>4}  {pred:8.3f}  {real:8.3f}  "
              f"{pred-real:+7.3f}  {(pred-real)/real*100:+7.2f}  {setname:>5}")


if __name__ == "__main__":
    print_report()
