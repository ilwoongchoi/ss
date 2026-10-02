#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_128_personality_trajectories.py
-------------------------------------
Renders 128 *trajectories* (not just a single 128-field texture).

Interpretation used (repo-consistent, no tuning):
  - Each "personality" i in [0..127] is an initial state vector x_i in R^6 on S5.
  - Time evolution uses geometry_package.universal_equation.get_straightened_flow()
    plus damping_term() hooks, with t_macro as the driver.
  - Each time step maps state -> traits -> Quant128 coordinates using s5_executable_maps.

Outputs:
  - out/personality_128_trajectories.png
  - out/personality_128_trajectories.csv
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _unit(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v)) or 1.0
    return v / n


def _seed_vec6(i: int, *, phi: float, chirality: float) -> np.ndarray:
    """
    Deterministic S5 seed: golden-angle spiral embedded into 6D with chirality bias.
    """
    # golden-angle phase
    ga = math.pi * (3.0 - math.sqrt(5.0))
    th = (i + 1) * ga
    # 6D components with alternating chirality skew
    v = np.array(
        [
            math.cos(th),
            math.sin(th),
            math.cos(2 * th) * (1.0 + chirality),
            math.sin(2 * th) * (1.0 - chirality),
            math.cos(3 * th),
            math.sin(3 * th),
        ],
        dtype=float,
    )
    # mild phi scaling to spread directions deterministically
    v[0] *= 1.0 / phi
    v[5] *= phi
    return _unit(v)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--t0", type=float, default=0.0)
    ap.add_argument("--t1", type=float, default=200.0)
    ap.add_argument("--dt", type=float, default=1.0)
    ap.add_argument("--outdir", type=str, default="out")
    args = ap.parse_args()

    from geometry_package.universal_equation import get_straightened_flow
    from geometry_package.universal_equation import DynamicsHooks
    from geometry_package.universal_equation import (
        get_macro_micro_time,
        get_south_pole_pressure,
        get_north_pole_jet,
        get_flash_probability,
    )
    from geometry_package.absolute_constants import (
        PHI,
        PHI_PB,
        OMEGA_LA,
        TOTAL_DEBT_AREA,
        NIGHT_HYSTERESIS,
        CHIRALITY_CONSTANT,
        LATTICE_3_32,
        TUNNEL_TENSION,
        BETTI_11,
        BETTI_7,
        SH_R_STAR,
        SH_Q0_STAR,
        CALIBRATED_SKELETON,
    )
    from geometry_package.universal_equation import kappa_eff

    from s5_executable_maps import Phi_traits, Quant128

    t0 = float(args.t0)
    t1 = float(args.t1)
    dt = float(args.dt)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    times = np.arange(t0, t1 + 1e-9, dt, dtype=float)
    nT = times.size

    # Use a stable kappa anchor (SH band center); personalities differ by initial x only
    kap = float(kappa_eff(float(SH_R_STAR), float(SH_Q0_STAR), use_lookup=False))

    # Initialize 128 personalities
    X = np.stack([_seed_vec6(i, phi=float(PHI), chirality=float(CHIRALITY_CONSTANT)) for i in range(128)], axis=0)
    drive_dir = np.stack(
        [_seed_vec6((i * 17) % 128, phi=float(PHI), chirality=-float(CHIRALITY_CONSTANT)) for i in range(128)], axis=0
    )

    # Storage: quant coords (4 dims) and first 2 dims for plotting
    qcoords = np.zeros((128, nT, 4), dtype=int)
    traj2 = np.zeros((128, nT, 2), dtype=float)

    # Evolve
    for ti, t in enumerate(times):
        # TIME operator (macro->micro + reversal) + engine drives + spark probability
        _t_micro, is_reverse = get_macro_micro_time(float(t))
        south_pressure = float(get_south_pole_pressure(float(t)))  # Big Man proxy
        north_jet = float(get_north_pole_jet(float(t)))            # Small Man proxy
        u_raw = (north_jet * float(PHI_PB)) / (abs(south_pressure) + float(OMEGA_LA))
        u = float(np.tanh(u_raw))
        flash_p = float(get_flash_probability(south_pressure, kappa_noise=0.02))

        # Flow + damping (no tuning; uses hooks)
        flow = get_straightened_flow(X, float(t))
        damp = DynamicsHooks.damping_term(X, kap, use_sw_calibration=False)

        # Drive injection using locked constants (pi/20 vs 1/9 mismatch, 3/32 gate, tension)
        w7_area = float(CALIBRATED_SKELETON.get("W7_AREA", math.pi / 20.0))
        mismatch = float((w7_area / (1.0 / 9.0)) - 1.0)
        gate = float(TUNNEL_TENSION - LATTICE_3_32)
        drive_scale = (mismatch + gate) * (1.0 + 0.5 * flash_p) * (1.0 if not is_reverse else -1.0)
        drive = (u * drive_scale) * drive_dir

        # Hysteresis as a memory-lag on the update magnitude (use NIGHT_HYSTERESIS directly)
        # Update: X <- X + (1-h)*dt*(flow + damp + drive)
        h = float(NIGHT_HYSTERESIS)
        X = X + (1.0 - h) * dt * (flow + damp + drive)
        # Re-project to S5
        X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)

        # Map each personality to traits -> 128-grid coordinate
        for i in range(128):
            traits = Phi_traits(x=X[i], A=float(TOTAL_DEBT_AREA), tau=float(NIGHT_HYSTERESIS), kappa=kap, u=u)
            q = Quant128(traits)
            qcoords[i, ti, :] = np.array(q, dtype=int)
            # plot first two dims as 2D trajectory on [0,127]
            traj2[i, ti, 0] = q[0]
            traj2[i, ti, 1] = q[1]

    # Export CSV (long format)
    csv_path = outdir / "personality_128_trajectories_v2.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["personality", "t_macro", "q0", "q1", "q2", "q3"])
        for i in range(128):
            for ti, t in enumerate(times):
                q0, q1, q2, q3 = qcoords[i, ti, :].tolist()
                w.writerow([i, float(t), q0, q1, q2, q3])

    # Render PNG
    fig = plt.figure(figsize=(10, 10), facecolor="#0a0a15")
    ax = fig.add_subplot(111)
    ax.set_facecolor("#0a0a15")
    ax.set_xlim(-1, 128)
    ax.set_ylim(-1, 128)
    ax.set_xticks([0, 32, 64, 96, 127])
    ax.set_yticks([0, 32, 64, 96, 127])
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("#333344")
    ax.grid(color="#222233", linewidth=0.6, alpha=0.8)

    # Color by personality index with a cyclic colormap
    cmap = plt.get_cmap("hsv")
    for i in range(128):
        col = cmap(i / 128.0)
        ax.plot(traj2[i, :, 0], traj2[i, :, 1], color=col, lw=0.8, alpha=0.65)
        ax.scatter(traj2[i, 0, 0], traj2[i, 0, 1], color=col, s=6, alpha=0.9)

    ax.set_title("128 PERSONALITY TRAJECTORIES on Quant128 Grid (q0 vs q1)", color="white", fontsize=12, pad=10)
    ax.text(
        0.01,
        0.01,
        f"t∈[{t0:.1f},{t1:.1f}] dt={dt:.1f} | kappa_eff(SH*)={kap:.6f} | uses TOTAL_DEBT_AREA, CHIRALITY, HYSTERESIS, Mobius(time reversal in flow)",
        transform=ax.transAxes,
        color="#ccccdd",
        fontsize=9,
        family="monospace",
        va="bottom",
    )

    png_path = outdir / "personality_128_trajectories_v2.png"
    plt.savefig(png_path, dpi=240, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)

    print(f"Wrote {png_path}")
    print(f"Wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
