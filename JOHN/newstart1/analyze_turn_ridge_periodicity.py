import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def autocorr(x):
    x = np.asarray(x, dtype=float)
    x = x - np.nanmean(x)
    valid = np.isfinite(x)
    if not np.any(valid):
        return None
    x = x[valid]
    n = len(x)
    if n == 0:
        return None
    corr = np.correlate(x, x, mode="full")
    corr = corr[corr.size // 2:]  # non-negative lags
    corr /= corr[0] if corr[0] != 0 else 1.0
    return corr


def fft_spectrum(x):
    x = np.asarray(x, dtype=float)
    x = x - np.nanmean(x)
    valid = np.isfinite(x)
    x = x[valid]
    n = len(x)
    if n == 0:
        return None, None
    freqs = np.fft.rfftfreq(n)
    amp = np.abs(np.fft.rfft(x)) / max(n, 1)
    return freqs, amp


def period4_significance(freqs, amp):
    if freqs is None or amp is None:
        return False, np.nan, np.nan
    # target frequency near 1/4 (cycles per turn unit)
    target = 0.25
    idx = int(np.argmin(np.abs(freqs - target)))
    peak = amp[idx]
    # reference: median of non-DC, excluding target bin
    mask = freqs > 0
    if mask.sum() <= 1:
        return False, peak, np.nan
    ref = np.median(amp[mask])
    significant = peak > 2.0 * ref if ref > 0 else False
    return significant, peak, ref


def extract_centers(rate_turn, mask_turn, r_axis, q0_axis):
    T, R, Q = rate_turn.shape
    centers_r = np.full(T, np.nan)
    centers_q = np.full(T, np.nan)
    for t in range(T):
        grid = rate_turn[t]
        if mask_turn.size == 0:
            mask = np.ones_like(grid, dtype=bool)
        else:
            mask = mask_turn[t].astype(bool)
        masked = np.where(mask, grid, -np.inf)
        idx = np.argmax(masked)
        if not np.isfinite(masked.flat[idx]):
            continue
        i, j = divmod(idx, Q)
        centers_r[t] = r_axis[i]
        centers_q[t] = q0_axis[j]
    return centers_r, centers_q


def main():
    ap = argparse.ArgumentParser(description="Analyze per-turn ridge periodicity from grid tensor NPZ")
    ap.add_argument("--npz", required=True, help="Path to grid_tensor npz")
    ap.add_argument("--out_png", default="out/turn_ridge_timeseries.png", help="Output plot path")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    r_axis = d["r_axis"]
    q0_axis = d["q0_axis"]
    turns = d["turns"]
    rate_turn = d["rate_turn"]
    mask_turn = d["mask_turn"] if "mask_turn" in d.files else np.array([])

    centers_r, centers_q = extract_centers(rate_turn, mask_turn, r_axis, q0_axis)

    # Autocorr & FFT
    ac_r = autocorr(centers_r)
    ac_q = autocorr(centers_q)
    fr_r, fa_r = fft_spectrum(centers_r)
    fr_q, fa_q = fft_spectrum(centers_q)

    sig_r, peak_r, ref_r = period4_significance(fr_r, fa_r)
    sig_q, peak_q, ref_q = period4_significance(fr_q, fa_q)

    print("r* period-4 significant:", sig_r, "peak=", peak_r, "ref=", ref_r)
    print("q0* period-4 significant:", sig_q, "peak=", peak_q, "ref=", ref_q)

    # Plot timeseries
    plt.figure(figsize=(10, 6))
    plt.plot(turns, centers_r, "o-", label="r*(t)")
    plt.plot(turns, centers_q, "s-", label="q0*(t)")
    plt.xlabel("turn")
    plt.ylabel("value")
    title = "turn ridge centers"\
        + (" | r*:p4 sig" if sig_r else "")\
        + (" | q0*:p4 sig" if sig_q else "")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.out_png, dpi=200)
    print("[OK] saved", args.out_png)


if __name__ == "__main__":
    main()
