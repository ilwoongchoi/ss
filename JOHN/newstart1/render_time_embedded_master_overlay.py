#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_time_embedded_master_overlay.py
-------------------------------------
Produces a TIME-embedded overlay of the master geometry without tuning constants.

What it does (pure visualization/operator overlay):
  - Loads canonical node positions from MASTER_GEOMETRY_NODES.csv.
  - Uses the existing time operator from geometry_package.universal_equation:
      get_macro_micro_time(t_macro) -> (t_micro, is_reverse)
  - Applies a Möbius-twist phase operator using the already-locked constant:
      VERTICAL_MOBIUS_TWIST = 1/28
    as a rotation in the XY plane.
  - Applies hysteresis as a *memory filter* using the already-locked constant:
      NIGHT_HYSTERESIS
    to create lag between raw phase and applied phase (no parameter fitting).

Outputs:
  - TIME_EMBEDDED_MASTER_OVERLAY.png
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class Node:
    node_id: str
    name: str
    archetype: str
    component_tag: str
    pos: np.ndarray  # (3,)


def _rot_xy(theta_rad: float) -> np.ndarray:
    c = math.cos(theta_rad)
    s = math.sin(theta_rad)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]], dtype=float)


def _node_color(archetype: str) -> str:
    return {
        "Big Woman": "#00ff88",
        "Small Woman": "#4466ff",
        "Big Man": "#ff3366",
        "Small Man": "#ffaa00",
        "Spark": "#ffff55",
        "Mediator": "#ff8800",
        "Boundary": "#ff4444",
    }.get(archetype, "#cccccc")


def main() -> int:
    import pandas as pd

    from geometry_package.universal_equation import get_macro_micro_time
    from geometry_package.absolute_constants import (
        NIGHT_HYSTERESIS,
        VERTICAL_MOBIUS_TWIST,
        SPARK_ANGLE_DEG,
    )

    nodes_path = Path("MASTER_GEOMETRY_NODES.csv")
    if not nodes_path.exists():
        raise SystemExit("Missing MASTER_GEOMETRY_NODES.csv (run generate_master_geometry_overlay.py first)")

    df = pd.read_csv(nodes_path)
    nodes: list[Node] = []
    for _, r in df.iterrows():
        pos = np.array([float(r["x"]), float(r["y"]), float(r["z"])], dtype=float)
        nodes.append(
            Node(
                node_id=str(r["node_id"]),
                name=str(r["name"]),
                archetype=str(r["archetype"]),
                component_tag=str(r.get("component_tag", "")),
                pos=pos,
            )
        )

    # Time samples: one full 28-cycle shown as 5 slices
    t_samples = np.array([0.0, 7.0, 14.0, 21.0, 28.0], dtype=float)

    # Raw Möbius phase: θ_raw(t) = 2π * (t * 1/28)
    theta_raw = 2.0 * math.pi * (t_samples * float(VERTICAL_MOBIUS_TWIST))

    # Hysteresis memory: θ_mem[n] = h*θ_mem[n-1] + (1-h)*θ_raw[n]
    h = float(NIGHT_HYSTERESIS)
    theta_mem = np.zeros_like(theta_raw)
    for i in range(len(theta_raw)):
        if i == 0:
            theta_mem[i] = theta_raw[i]
        else:
            theta_mem[i] = h * theta_mem[i - 1] + (1.0 - h) * theta_raw[i]

    # Reversal flags from the canonical time operator (this is the "time 정순/역순" switch)
    reversals = np.array([bool(get_macro_micro_time(float(t))[1]) for t in t_samples], dtype=bool)

    # Plot
    fig = plt.figure(figsize=(22, 12), facecolor="#0a0a15")
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.0], wspace=0.18, hspace=0.18)

    axes = []
    for i in range(5):
        ax = fig.add_subplot(gs[i // 3, i % 3], projection="3d")
        ax.set_facecolor("#0a0a15")
        ax.set_axis_off()
        axes.append(ax)

    # Legend panel
    axl = fig.add_subplot(gs[1, 2])
    axl.set_facecolor("#0a0a15")
    axl.set_axis_off()

    for i, t in enumerate(t_samples):
        ax = axes[i]
        theta = float(theta_mem[i])
        R = _rot_xy(theta)

        # Apply reversal as a mirrored twist (sign flip) for visualization
        if reversals[i]:
            R = _rot_xy(-theta)

        # Node positions at time slice
        pts = []
        cols = []
        for n in nodes:
            p = (R @ n.pos.reshape(3, 1)).reshape(3)
            pts.append(p)
            cols.append(_node_color(n.archetype))

        P = np.stack(pts, axis=0)
        ax.scatter(P[:, 0], P[:, 1], P[:, 2], s=220, c=cols, edgecolors="white", linewidths=1.0, alpha=0.95)

        for j, n in enumerate(nodes):
            ax.text(P[j, 0], P[j, 1], P[j, 2] + 0.35, f"{n.node_id}", color="white", fontsize=8, ha="center")

        # Keep consistent limits
        lim = float(np.max(np.abs(P))) + 0.8
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-lim, lim)

        direction = "REVERSE" if reversals[i] else "FORWARD"
        ax.set_title(
            f"t_macro={t:.0f}  θ_mem={math.degrees(theta):.1f}°  {direction}",
            color="white",
            fontsize=11,
            pad=10,
        )

    # Legend / explanation
    axl.text(
        0.02,
        0.95,
        "TIME-EMBEDDED OVERLAY (no tuning)\n"
        "--------------------------------\n"
        "Positions = canonical patch embedding rotated by Möbius phase.\n"
        "θ_raw(t) = 2π * (t * VERTICAL_MOBIUS_TWIST)  (twist=1/28)\n"
        "θ_mem = hysteresis memory using NIGHT_HYSTERESIS\n"
        "Reverse/Forward = get_macro_micro_time(t).is_reverse\n"
        "\n"
        f"SPARK_ANGLE_DEG = {float(SPARK_ANGLE_DEG):.2f}° (spark is an event, not a steady rotation)\n",
        color="white",
        fontsize=10,
        family="monospace",
        va="top",
    )

    # Color key
    key = [
        ("Big Woman", "#00ff88"),
        ("Small Woman", "#4466ff"),
        ("Big Man", "#ff3366"),
        ("Small Man", "#ffaa00"),
        ("Spark", "#ffff55"),
        ("Mediator", "#ff8800"),
        ("Boundary", "#ff4444"),
    ]
    y = 0.52
    for label, c in key:
        axl.add_patch(plt.Rectangle((0.04, y), 0.04, 0.03, color=c, transform=axl.transAxes, clip_on=False))
        axl.text(0.10, y + 0.015, label, color="white", fontsize=10, va="center")
        y -= 0.05

    fig.suptitle("TIME in Universal Geometry: Möbius twist + Hysteresis memory + Forward/Reverse operator", color="white", fontsize=15)

    out = Path("TIME_EMBEDDED_MASTER_OVERLAY.png")
    plt.savefig(out, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

