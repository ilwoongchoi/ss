import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def autocorr(x):
    x = np.asarray(x, dtype=float)
    x = x - np.nanmean(x)
    valid = np.isfinite(x)
    x = x[valid]
    if x.size == 0:
        return None
    corr = np.correlate(x, x, mode="full")
    corr = corr[corr.size // 2:]
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
    target = 0.25
    idx = int(np.argmin(np.abs(freqs - target)))
    peak = amp[idx]
    mask = freqs > 0
    if mask.sum() <= 1:
        return False, peak, np.nan
    ref = np.median(amp[mask])
    significant = peak > 2.0 * ref if ref > 0 else False
    return significant, peak, ref


def ridge_stats_from_path(ridge_q0, ridge_r):
    mask = np.isfinite(ridge_q0) & np.isfinite(ridge_r)
    if not np.any(mask):
        return np.nan, np.nan, np.nan
    q = ridge_q0[mask]
    r = ridge_r[mask]
    mean_r = np.mean(r)
    mean_q = np.mean(q)
    # length as sum of distances between consecutive points
    if len(r) < 2:
        length = 0.0
    else:
        dr = np.diff(r)
        dq = np.diff(q)
        length = float(np.sum(np.sqrt(dr * dr + dq * dq)))
    return mean_r, mean_q, length


def area_above_half_peak(grid, mask=None):
    g = np.array(grid, copy=True)
    if mask is not None and mask.size:
        g = np.where(mask, g, -np.inf)
    peak = np.nanmax(g)
    if not np.isfinite(peak) or peak <= 0:
        return peak, 0
    thr = 0.5 * peak
    area = int(np.sum(g >= thr))
    return peak, area


def main():
    ap = argparse.ArgumentParser(description="Per-turn ridge shape modulation analysis")
    ap.add_argument("--npz", required=True, help="grid_tensor npz")
    ap.add_argument("--out_png", default="out/turn_ridge_shape.png", help="output plot")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    turns = d["turns"]
    rate_turn = d["rate_turn"]
    mask_turn = d["mask_turn"] if "mask_turn" in d.files else np.array([])
    ridge_q0 = d["ridge_turn_q0"] if "ridge_turn_q0" in d.files else np.array([])
    ridge_r = d["ridge_turn_r"] if "ridge_turn_r" in d.files else np.array([])

    T = rate_turn.shape[0]

    peak_vals = np.full(T, np.nan)
    area_vals = np.full(T, np.nan)
    ridge_mean_r = np.full(T, np.nan)
    ridge_mean_q = np.full(T, np.nan)
    ridge_len = np.full(T, np.nan)

    for t in range(T):
        mask = mask_turn[t] if mask_turn.size else None
        peak, area = area_above_half_peak(rate_turn[t], mask)
        peak_vals[t] = peak
        area_vals[t] = area
        if ridge_q0.size and ridge_r.size:
            ridge_mean_r[t], ridge_mean_q[t], ridge_len[t] = ridge_stats_from_path(ridge_q0[t], ridge_r[t])

    metrics = {
        "peak": peak_vals,
        "area50": area_vals,
        "ridge_mean_r": ridge_mean_r,
        "ridge_mean_q": ridge_mean_q,
        "ridge_len": ridge_len,
    }

    # period-4 checks
    p4 = {}
    for k, v in metrics.items():
        fr, fa = fft_spectrum(v)
        sig, peak, ref = period4_significance(fr, fa)
        p4[k] = (sig, peak, ref)
        print(f"metric={k} p4_sig={sig} peak={peak} ref={ref}")

    # plot
    fig, axes = plt.subplots(len(metrics), 1, figsize=(10, 2.5 * len(metrics)), sharex=True)
    for ax, (k, v) in zip(np.ravel(axes), metrics.items()):
        ax.plot(turns, v, "o-", label=k)
        sig = p4[k][0]
        ax.set_ylabel(k)
        ax.grid(True, alpha=0.3)
        ax.legend()
        if sig:
            ax.set_title(f"{k} (period-4 signal)")
    axes[-1].set_xlabel("turn")
    plt.tight_layout()
    plt.savefig(args.out_png, dpi=200)
    print("[OK] saved", args.out_png)


if __name__ == "__main__":
    main()
