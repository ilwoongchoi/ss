import argparse
import numpy as np
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", required=True)
    ap.add_argument("--out", default="out/grid_tensor_preview.png")
    ap.add_argument("--turns", type=int, default=6, help="how many turns to show")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    rs = d["r_axis"]
    qs = d["q0_axis"]
    turns = d["turns"]
    w = d["w_gate"]
    rate_turn = d["rate_turn"]  # (T,R,Q)

    T = rate_turn.shape[0]
    showT = min(args.turns, T)

    rate_mean = rate_turn.mean(axis=0)

    fig, axes = plt.subplots(2, 1 + showT, figsize=(4 * (1 + showT), 7), constrained_layout=True)

    extent = [qs.min(), qs.max(), rs.min(), rs.max()]

    ax = axes[0, 0]
    im = ax.imshow(w, origin="lower", aspect="auto", extent=extent)
    ax.set_title("w_gate")
    ax.set_xlabel("q0")
    ax.set_ylabel("r")
    fig.colorbar(im, ax=ax, fraction=0.046)

    ax = axes[1, 0]
    im = ax.imshow(rate_mean, origin="lower", aspect="auto", extent=extent)
    ax.set_title("rate_turn mean")
    ax.set_xlabel("q0")
    ax.set_ylabel("r")
    fig.colorbar(im, ax=ax, fraction=0.046)

    for i in range(showT):
        ax = axes[0, i + 1]
        im = ax.imshow(rate_turn[i], origin="lower", aspect="auto", extent=extent)
        ax.set_title(f"turn {int(turns[i])} rate")
        ax.set_xlabel("q0")
        ax.set_ylabel("r")
        fig.colorbar(im, ax=ax, fraction=0.046)

        ax = axes[1, i + 1]
        im = ax.imshow(rate_turn[i] - rate_mean, origin="lower", aspect="auto", extent=extent)
        ax.set_title(f"turn {int(turns[i])} (rate - mean)")
        ax.set_xlabel("q0")
        ax.set_ylabel("r")
        fig.colorbar(im, ax=ax, fraction=0.046)

    plt.savefig(args.out, dpi=200)
    print("[OK] saved", args.out)
    print("n_turns =", T)


if __name__ == "__main__":
    main()
