import argparse
import numpy as np
import matplotlib.pyplot as plt


def fft_power_ratio_at(freqs, amp, target=0.25):
    if freqs is None or amp is None or len(freqs) == 0:
        return np.nan
    idx = int(np.argmin(np.abs(freqs - target)))
    target_power = amp[idx]
    mask = freqs > 0
    if mask.sum() <= 1:
        return np.nan
    median_power = np.median(amp[mask])
    return target_power / median_power if median_power > 0 else np.nan


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


def main():
    ap = argparse.ArgumentParser(description="PCA/SVD on turn-wise rate maps to detect hidden period-4 modulation")
    ap.add_argument("--npz", required=True, help="grid_tensor npz path")
    ap.add_argument("--k", type=int, default=6, help="number of modes to show")
    ap.add_argument("--min_valid_cells", type=int, default=50, help="min mask-true cells per turn to keep turn")
    ap.add_argument("--min_pixel_coverage", type=float, default=0.8, help="fraction of valid turns a pixel must be unmasked to keep")
    ap.add_argument("--out_png", default="out/turn_pca_modes.png", help="output plot path")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    rate_turn = d["rate_turn"]  # (T,R,Q)
    mask_turn = d["mask_turn"] if "mask_turn" in d.files else np.ones_like(rate_turn, dtype=bool)
    r_axis = d["r_axis"]
    q0_axis = d["q0_axis"]
    turns = d["turns"]

    T, R, Q = rate_turn.shape

    # turn validity
    turn_valid = mask_turn.reshape(T, -1).sum(axis=1) >= args.min_valid_cells
    rate_turn = rate_turn[turn_valid]
    mask_turn = mask_turn[turn_valid]
    turns = turns[turn_valid]

    if rate_turn.size == 0:
        raise ValueError("No valid turns after filtering")

    T, R, Q = rate_turn.shape
    P = R * Q

    # pixel coverage filter
    pixel_coverage = mask_turn.reshape(T, P).mean(axis=0)
    keep_pixels = pixel_coverage >= args.min_pixel_coverage
    if not np.any(keep_pixels):
        raise ValueError("No pixels meet coverage threshold")

    X = rate_turn.reshape(T, P)[:, keep_pixels]
    M = np.nanmean(X, axis=0)
    Xc = X - M

    # SVD
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    V = Vt  # modes x pixels
    k = min(args.k, V.shape[0])

    # mode coeffs (time series)
    coeffs = U[:, :k] * S[:k]

    # FFT power ratio for each mode
    ratios = []
    for i in range(k):
        freqs, amp = fft_spectrum(coeffs[:, i])
        ratio = fft_power_ratio_at(freqs, amp, target=0.25)
        ratios.append(ratio)
        print(f"mode {i}: f=0.25 power_ratio={ratio}")

    # Prepare spatial maps with masked pixels
    maps = []
    template = np.full(P, np.nan)
    for i in range(k):
        vec = template.copy()
        vec[keep_pixels] = V[i]
        maps.append(vec.reshape(R, Q))

    # Plot
    fig, axes = plt.subplots(k, 2, figsize=(10, 3 * k), constrained_layout=True)
    extent = [q0_axis.min(), q0_axis.max(), r_axis.min(), r_axis.max()]
    for i in range(k):
        ax_map = axes[i, 0]
        im = ax_map.imshow(maps[i], origin="lower", aspect="auto", extent=extent, cmap="coolwarm")
        ax_map.set_title(f"mode {i} spatial (f0.25 ratio={ratios[i]:.2f})")
        ax_map.set_xlabel("q0")
        ax_map.set_ylabel("r")
        fig.colorbar(im, ax=ax_map, fraction=0.046)

        ax_ts = axes[i, 1]
        ax_ts.plot(turns, coeffs[:, i], "o-", label=f"mode {i} coeff")
        ax_ts.axhline(0, color="gray", lw=0.8)
        ax_ts.set_xlabel("turn")
        ax_ts.set_ylabel("coeff")
        ax_ts.grid(True, alpha=0.3)
        ax_ts.legend()

    plt.savefig(args.out_png, dpi=200)
    print(f"[OK] saved {args.out_png}")


if __name__ == "__main__":
    main()
