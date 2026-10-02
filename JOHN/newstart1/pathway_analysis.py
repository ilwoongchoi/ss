"""
pathway_analysis.py
===================
30-channel pathway map for all 6 archetypes.

For each archetype:
  - Track z[i] amplitude for all 8 K8 particles over 128 steps
  - Show which channels drive which particle at each phase
  - Output: table + plot per archetype
"""

import numpy as np
import matplotlib.pyplot as plt
import os

from fusion_core import (
    SUBJECTS, IDX, laplacian, apply_channels,
    PHASE_TABLE, C, OMEGA, CHANNEL_MAP, CHANNEL_ORDER,
)
from universe_sim import primordial_z
from archetypes import ARCHETYPE_CHANNEL_STATES, ARCHETYPE_PARAMS, BLOOD_TYPE_COORDS

E_INV        = 1.0 / np.e
ENTROPY_DEBT = 1/64 + 1/256
DT           = 0.03
NAMED        = list(ARCHETYPE_CHANNEL_STATES.keys())

PHASE_CYCLE = ["phase1","phase2","proton_landing","night_spark","hysteresis"]

def phase_at(t):
    hour = t * 24.0 / 128
    if 2.25 <= hour < 4.50:
        if 3.00 <= hour < 3.25:
            return "night_spark"
        return "hysteresis"
    if 9.75 <= hour < 15.75:
        return "phase2"
    if 15.75 <= hour < 16.50:
        return "phase1"
    if 16.50 <= hour < 16.75:
        return "proton_landing"
    return "phase1"

def rebranch(z):
    q = z[IDX["quark"]]
    g = z[IDX["gluon"]]
    h = z[IDX["higgs"]]
    z[IDX["photon"]]   = q * g
    z[IDX["electron"]] = g ** 2
    z[IDX["neutrino"]] = g * h ** 2
    z[IDX["w_boson"]]  = q * h
    z[IDX["z_boson"]]  = g * h
    return z

def make_z0(arch_name):
    params = ARCHETYPE_PARAMS[arch_name]
    blood  = params.get("blood", params.get("blood_type", "AB"))
    coords = BLOOD_TYPE_COORDS.get(blood, {"BW": OMEGA/2, "SM": OMEGA/2})
    z      = primordial_z(C).copy()
    scale  = 0.08
    z[IDX["quark"]]  = (coords["BW"] / (OMEGA + 1e-9)) * scale * (1.0 + 0j)
    z[IDX["gluon"]]  = (coords["SM"] / (OMEGA + 1e-9)) * scale * 1j
    z[IDX["higgs"]]  = C + 0j
    return rebranch(z)


def run_archetype_trace(arch_name):
    """
    Returns:
      traj:     (128, 8) float  — |z[particle]| at each t
      ch_active:(128, 30) float — channel activation level at each t
    """
    z        = make_z0(arch_name)
    base_ch  = dict(ARCHETYPE_CHANNEL_STATES[arch_name])
    post_reset = False

    traj      = np.zeros((128, 8))
    ch_active = np.zeros((128, len(CHANNEL_ORDER)))

    for t in range(128):
        phase = phase_at(t)
        ch    = dict(base_ch)
        if post_reset:
            ch["vasopressin_female"] = "on"
            ch["right_love"]         = "no_control"

        # Record channel activation
        for k, name in enumerate(CHANNEL_ORDER):
            st = ch.get(name, "no_control")
            ch_active[t, k] = 1.0 if st == "on" else (0.5 if st == "no_control" else 0.0)

        w = apply_channels(ch)
        L = laplacian(w)
        h = -L @ z * DT

        z = z ** 2 - z + h

        norms   = np.abs(z)
        escaped = norms > 10.0
        if escaped.any():
            z[escaped] = 10.0 * z[escaped] / (norms[escaped] + 1e-15)

        if t == 88:
            z = rebranch(z)
            post_reset = True

        z -= ENTROPY_DEBT * z

        traj[t] = np.abs(z)

    return traj, ch_active


def channel_influence_matrix(arch_name, traj):
    """
    For each channel: compute correlation with each particle trajectory.
    Returns (30, 8) correlation matrix.
    """
    _, ch_active = run_archetype_trace(arch_name)

    corr = np.zeros((len(CHANNEL_ORDER), 8))
    for k in range(len(CHANNEL_ORDER)):
        ch_sig = ch_active[:, k]
        if ch_sig.std() < 1e-9:
            continue
        for p in range(8):
            p_sig = traj[:, p]
            if p_sig.std() < 1e-9:
                continue
            c = np.corrcoef(ch_sig, p_sig)[0, 1]
            corr[k, p] = c if not np.isnan(c) else 0.0
    return corr


def print_pathway_table(arch_name, traj, corr):
    params = ARCHETYPE_PARAMS[arch_name]
    blood  = params.get("blood", params.get("blood_type", "?"))
    print(f"\n{'='*72}")
    print(f"ARCHETYPE: {arch_name}  ({blood}-type, {params.get('mbti','?')})")
    print(f"{'='*72}")

    # Dominant particle at t=0, t=88, t=127
    for label, t_idx in [("t=0  ", 0), ("t=88 ", 88), ("t=127", 127)]:
        amps = traj[t_idx]
        dominant = SUBJECTS[int(np.argmax(amps))]
        bw = amps[IDX["w_boson"]]
        sm = amps[IDX["z_boson"]]
        tot = bw + sm + 1e-15
        print(f"  {label}  dominant={dominant:8s}  "
              f"BW={bw/(tot)*OMEGA:.3f}  SM={sm/(tot)*OMEGA:.3f}  "
              f"|q|={amps[IDX['quark']]:.3f}  |g|={amps[IDX['gluon']]:.3f}  "
              f"|h|={amps[IDX['higgs']]:.3f}")

    # Top 5 channel→particle pathways
    print(f"\n  Top channel→particle pathways (|corr| > 0.3):")
    paths = []
    for k, ch_name in enumerate(CHANNEL_ORDER):
        for p, p_name in enumerate(SUBJECTS):
            r = corr[k, p]
            if abs(r) > 0.3:
                paths.append((abs(r), r, ch_name, p_name))
    paths.sort(reverse=True)
    for rank, (ar, r, ch, par) in enumerate(paths[:10]):
        sign = "+" if r > 0 else "-"
        print(f"    {rank+1:2d}. {ch:35s} -> {par:10s}  r={sign}{ar:.3f}")


def plot_archetype(arch_name, traj, outdir):
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), facecolor="black")

    # Panel 1: 8 particle amplitudes over time
    ax = axes[0]
    ax.set_facecolor("black")
    colors = plt.cm.tab10(np.linspace(0, 1, 8))
    for p, name in enumerate(SUBJECTS):
        ax.plot(traj[:, p], color=colors[p], lw=1.2, label=name)
    ax.axvline(x=88, color="white", ls="--", lw=0.8, alpha=0.6)
    ax.set_title(f"{arch_name} — particle amplitudes |z[i]|", color="white")
    ax.legend(facecolor="#111", labelcolor="white", fontsize=7,
              ncol=4, loc="upper left")
    ax.tick_params(colors="white")
    ax.set_ylabel("|z|", color="white")

    # Panel 2: BW and SM trajectories
    ax2 = axes[1]
    ax2.set_facecolor("black")
    bw_traj = traj[:, IDX["w_boson"]]
    sm_traj = traj[:, IDX["z_boson"]]
    tot     = bw_traj + sm_traj + 1e-15
    bw_norm = bw_traj / tot * OMEGA
    sm_norm = sm_traj / tot * OMEGA
    ax2.plot(bw_norm, color="orange",  lw=1.5, label="BW")
    ax2.plot(sm_norm, color="skyblue", lw=1.5, label="SM")
    ax2.axhline(y=OMEGA/2, color="gray", ls=":", lw=0.8, alpha=0.6,
                label=f"OMEGA/2={OMEGA/2}")
    ax2.axvline(x=88, color="white", ls="--", lw=0.8, alpha=0.6)
    ax2.set_title("BW / SM balance", color="white")
    ax2.legend(facecolor="#111", labelcolor="white", fontsize=8)
    ax2.tick_params(colors="white")
    ax2.set_ylabel("normalised", color="white")

    # Panel 3: 3 primitives (quark, gluon, higgs)
    ax3 = axes[2]
    ax3.set_facecolor("black")
    ax3.plot(traj[:, IDX["quark"]],  color="red",   lw=1.5, label="quark (real)")
    ax3.plot(traj[:, IDX["gluon"]],  color="green", lw=1.5, label="gluon (imag)")
    ax3.plot(traj[:, IDX["higgs"]],  color="gold",  lw=1.5, label="higgs (C)")
    ax3.axvline(x=88, color="white", ls="--", lw=0.8, alpha=0.6,
                label="rebranch t=88")
    ax3.set_title("3 Primitives", color="white")
    ax3.legend(facecolor="#111", labelcolor="white", fontsize=8)
    ax3.tick_params(colors="white")
    ax3.set_ylabel("|primitive|", color="white")
    ax3.set_xlabel("t (128 windows)", color="white")

    plt.tight_layout()
    fname = os.path.join(outdir, f"pathway_{arch_name}.png")
    plt.savefig(fname, dpi=150, bbox_inches="tight", facecolor="black")
    plt.close()
    print(f"  -> {fname}")


def main():
    outdir = "analysis_results/pathways"
    os.makedirs(outdir, exist_ok=True)

    print("30-CHANNEL PATHWAY ANALYSIS")
    print(f"K8 particles: {SUBJECTS}")
    print(f"Channels: {len(CHANNEL_ORDER)}")

    all_corr = {}
    for arch_name in NAMED:
        traj, _ = run_archetype_trace(arch_name)
        corr     = channel_influence_matrix(arch_name, traj)
        all_corr[arch_name] = corr
        print_pathway_table(arch_name, traj, corr)
        plot_archetype(arch_name, traj, outdir)

    # Summary: which channels are UNIVERSAL (high corr across all archetypes)
    print(f"\n{'='*72}")
    print("UNIVERSAL PATHWAYS (consistent across all 6 archetypes):")
    mean_corr = np.mean([np.abs(v) for v in all_corr.values()], axis=0)  # (30,8)
    for k, ch_name in enumerate(CHANNEL_ORDER):
        for p, p_name in enumerate(SUBJECTS):
            r = mean_corr[k, p]
            if r > 0.4:
                print(f"  {ch_name:35s} -> {p_name:10s}  mean|r|={r:.3f}")

    print("\n[DONE] analysis_results/pathways/")


if __name__ == "__main__":
    main()
