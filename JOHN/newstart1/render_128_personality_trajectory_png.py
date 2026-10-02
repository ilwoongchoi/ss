#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_128_personality_trajectory_png.py
---------------------------------------
Renders the "128 PERSONALITY TRAJECTORY" grid as a PNG artifact (offline).

This is a 2D grid texture meant to be used as input to a separate shader viewer.

How it's built (no tuning):
  - Uses geometry_package.universal_equation.get_emergent_128_nodes(t_macro, resolution=128)
    which returns a 128-sample emergent field for the given macro-time.
  - Converts the 1D field into a 128x128 texture by a deterministic tiling rule:
      row i uses field rolled by i (circulant embedding)
    This preserves "trajectory" continuity across both axes without inventing new parameters.

Outputs:
  - out/trajectory_128_tXXXX.png
  - out/trajectory_128_latest.png (copy)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def build_grid(field_1d: np.ndarray) -> np.ndarray:
    field_1d = np.asarray(field_1d, dtype=float).reshape(-1)
    if field_1d.size != 128:
        raise ValueError(f"Expected 128 field values, got {field_1d.size}")
    grid = np.zeros((128, 128), dtype=float)
    for i in range(128):
        grid[i, :] = np.roll(field_1d, i)
    return grid


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--t", type=float, default=0.0, help="macro time t_macro")
    ap.add_argument("--outdir", type=str, default="out", help="output directory")
    args = ap.parse_args()

    from geometry_package.universal_equation import get_emergent_128_nodes

    t = float(args.t)
    field = get_emergent_128_nodes(t, resolution=128)
    grid = build_grid(field)

    # Normalize to [-1,1]
    m = float(np.max(np.abs(grid))) or 1.0
    gridn = grid / m

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    out_path = outdir / f"trajectory_128_t{int(round(t * 10)):04d}.png"
    latest = outdir / "trajectory_128_latest.png"

    fig = plt.figure(figsize=(8, 8), facecolor="#0a0a15")
    ax = fig.add_subplot(111)
    ax.set_facecolor("#0a0a15")
    im = ax.imshow(gridn, cmap="turbo", vmin=-1.0, vmax=1.0, interpolation="nearest")
    ax.set_title(f"128 PERSONALITY TRAJECTORY GRID (t_macro={t:.1f})", color="white", fontsize=12, pad=10)
    ax.set_xticks([])
    ax.set_yticks([])

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(colors="white", labelsize=9)

    plt.savefig(out_path, dpi=240, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)

    # Copy to latest
    latest.write_bytes(out_path.read_bytes())

    print(f"Wrote {out_path}")
    print(f"Wrote {latest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

