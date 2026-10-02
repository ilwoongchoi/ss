#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_time_geometry.py
-----------------------
Renders how TIME enters the geometry package via universal_equation.py:
  - macro/micro time + reversal flag (1/28 lunar twist)
  - south pole pressure (Big Man drive proxy)
  - north pole jet (Small Man voltage/jet proxy)
  - flash probability (spark closure proxy)

Output:
  - TIME_GEOMETRY_DYNAMICS.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main() -> int:
    from geometry_package.universal_equation import (
        get_macro_micro_time,
        get_south_pole_pressure,
        get_north_pole_jet,
        get_flash_probability,
        kappa_eff,
    )
    from geometry_package.absolute_constants import (
        SH_R_STAR,
        SH_Q0_STAR,
        TUNNEL_TENSION,
    )

    # Time axis (macro-time)
    t = np.linspace(0.0, 200.0, 2400, dtype=float)

    t_micro = np.zeros_like(t)
    is_reverse = np.zeros_like(t, dtype=bool)
    for i, tt in enumerate(t):
        tm, rev = get_macro_micro_time(float(tt))
        t_micro[i] = float(tm)
        is_reverse[i] = bool(rev)

    # Use a representative kappa_eff at the SH attractor (stable band)
    kap = float(kappa_eff(float(SH_R_STAR), float(SH_Q0_STAR), use_lookup=False))

    south = np.array([float(get_south_pole_pressure(float(tt))) for tt in t], dtype=float)
    north = np.array([float(get_north_pole_jet(float(tt))) for tt in t], dtype=float)

    # Flash probability depends on current_tension; we model "current_tension" here as south pole pressure
    flash = np.array([float(get_flash_probability(float(s), kappa_noise=0.02)) for s in south], dtype=float)

    # Normalize north/south for shared plotting
    def zscore(x: np.ndarray) -> np.ndarray:
        mu = float(np.mean(x))
        sd = float(np.std(x)) or 1.0
        return (x - mu) / sd

    south_z = zscore(south)
    north_z = zscore(north)

    fig = plt.figure(figsize=(18, 10), facecolor="#0a0a15")
    gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 1.1, 1.1], hspace=0.28)

    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[1, 0], sharex=ax0)
    ax2 = fig.add_subplot(gs[2, 0], sharex=ax0)

    for ax in (ax0, ax1, ax2):
        ax.set_facecolor("#0a0a15")
        ax.grid(color="#222233", linewidth=0.6, alpha=0.8)
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("#333344")

    # Panel 0: micro-time and reversal regions
    ax0.plot(t, t_micro, color="#66ddff", lw=1.5, label="t_micro = sin(2π * t_macro / 28) (1/28 twist)")
    ax0.fill_between(
        t,
        -1.05,
        1.05,
        where=is_reverse,
        color="#ff8844",
        alpha=0.12,
        label="time reversal half-cycle (cos < 0)",
    )
    ax0.set_ylabel("t_micro", color="white")
    ax0.set_ylim(-1.1, 1.1)
    ax0.legend(loc="upper right", fontsize=9, facecolor="#0a0a15", edgecolor="#333344", labelcolor="white")

    # Panel 1: Big Man / Small Man proxies
    ax1.plot(t, south_z, color="#ff3366", lw=1.1, label="South pole pressure (Big Man drive proxy)")
    ax1.plot(t, north_z, color="#ffaa00", lw=1.1, label="North pole jet (Small Man voltage proxy)")
    ax1.set_ylabel("z-score", color="white")
    ax1.legend(loc="upper right", fontsize=9, facecolor="#0a0a15", edgecolor="#333344", labelcolor="white")

    # Panel 2: Spark/closure proxy
    ax2.plot(t, flash, color="#ffff55", lw=1.2, label="Flash probability (spark closure proxy)")
    ax2.axhline(0.5, color="#9999aa", lw=0.8, ls="--", alpha=0.6)
    ax2.set_ylabel("P(flash)", color="white")
    ax2.set_xlabel("t_macro", color="white")
    ax2.set_ylim(0.0, 1.02)
    ax2.legend(loc="upper right", fontsize=9, facecolor="#0a0a15", edgecolor="#333344", labelcolor="white")

    fig.suptitle(
        "TIME in Geometry Package: macro→micro (1/28) + drive/jet + spark probability",
        color="white",
        fontsize=14,
        y=0.98,
    )

    # Small info block
    fig.text(
        0.01,
        0.01,
        f"Using kappa_eff(SH_R*,SH_Q0*)≈{kap:.6f} | TUNNEL_TENSION={float(TUNNEL_TENSION):.7f}",
        color="#ccccdd",
        fontsize=9,
        family="monospace",
    )

    out = Path("TIME_GEOMETRY_DYNAMICS.png")
    plt.savefig(out, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

