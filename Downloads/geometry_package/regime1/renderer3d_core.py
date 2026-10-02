"""Regime-1 3D geometry renderer core (no bio/narrative labels)."""

from __future__ import annotations

import math
from typing import Dict

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from . import core_constants as c
from .core_ops import emergent_nodes


def _polygon_ring(n_nodes: int, radius: float, z0: float) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * math.pi, n_nodes + 1)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.full_like(x, z0)
    return np.column_stack([x, y, z])


def build_geometry_scene(t_macro: float, terminus_radius: float = 10.0) -> Dict[str, object]:
    r_void = math.sqrt(c.W7_AREA / math.pi)
    r_major = c.MAXWELL_R_MAJOR * r_void
    r_minor = c.MAXWELL_R_MINOR * r_void

    shells = {
        "shell_1_64": terminus_radius * (1.0 - c.KAPPA_TDA_MIN),
        "shell_1_32": terminus_radius * (1.0 - c.KAPPA_TDA_MID),
        "shell_1_16": terminus_radius * (1.0 - c.KAPPA_TDA_MAX),
        "shell_3_32": terminus_radius * (1.0 - c.LATTICE_3_32),
    }

    betti5 = _polygon_ring(5, r_void * 1.5, -terminus_radius * 0.2)
    betti11 = _polygon_ring(11, r_void * 1.8, terminus_radius * 0.2)

    nodes = emergent_nodes(t_macro=t_macro, resolution=128)
    z_funnel = np.linspace(r_void, terminus_radius * 0.9, nodes.size)
    r_funnel = r_void + np.abs(nodes) * (terminus_radius * 0.25)

    return {
        "terminus_radius": float(terminus_radius),
        "r_void": float(r_void),
        "maxwell_torus_major": float(r_major),
        "maxwell_torus_minor": float(r_minor),
        "shells": shells,
        "betti5_ring": betti5,
        "betti11_ring": betti11,
        "funnel_r": r_funnel,
        "funnel_z": z_funnel,
    }


def render_geometry_scene(scene: Dict[str, object], output_path: str = "REGIME1_GEOMETRY_3D.png") -> str:
    fig = plt.figure(figsize=(14, 12), facecolor="#060612")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#060612")

    r_major = float(scene["maxwell_torus_major"])
    r_minor = float(scene["maxwell_torus_minor"])

    u = np.linspace(0, 2 * np.pi, 96)
    v = np.linspace(0, 2 * np.pi, 64)
    U, V = np.meshgrid(u, v)
    XT = (r_major + r_minor * np.cos(V)) * np.cos(U)
    YT = (r_major + r_minor * np.cos(V)) * np.sin(U)
    ZT = r_minor * np.sin(V)
    ax.plot_wireframe(XT, YT, ZT, color="#8888aa", alpha=0.25, rstride=4, cstride=4)

    ring5 = np.asarray(scene["betti5_ring"])
    ring11 = np.asarray(scene["betti11_ring"])
    ax.plot(ring5[:, 0], ring5[:, 1], ring5[:, 2], color="#ff8800", linewidth=2.0, label="Betti-5 Ring")
    ax.plot(ring11[:, 0], ring11[:, 1], ring11[:, 2], color="#aa66ff", linewidth=1.8, label="Betti-11 Ring")

    r_funnel = np.asarray(scene["funnel_r"])
    z_funnel = np.asarray(scene["funnel_z"])
    theta = np.linspace(0.0, 2.0 * np.pi, r_funnel.size)
    ax.plot(r_funnel * np.cos(theta), r_funnel * np.sin(theta), z_funnel, color="#22ddaa", alpha=0.85, linewidth=1.2)

    lim = float(scene["terminus_radius"])
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_axis_off()
    ax.legend(loc="upper left")
    ax.text2D(0.02, 0.98, "Regime-1 Geometry Core", transform=ax.transAxes, color="white")

    plt.savefig(output_path, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path
