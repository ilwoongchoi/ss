import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from geometry_package import absolute_constants as const
from geometry_package.universal_equation import kappa_eff, w_gate, in_sh_band


def map_xy_to_rq0(x, y):
    # Map 16x16 face grid into SH band ranges (physics-only, no MBTI mapping)
    r = const.SH_R_BAND_MIN + (x / 16.0) * (const.SH_R_BAND_MAX - const.SH_R_BAND_MIN)
    q0 = const.SH_Q0_MIN + (y / 16.0) * (const.SH_Q0_MAX - const.SH_Q0_MIN)
    return r, q0


def step_field(x, y, dt=0.08):
    # Physics-only vector field driven by kappa gate + spark angle
    r, q0 = map_xy_to_rq0(x, y)
    k = kappa_eff(r, q0)
    wg = w_gate(r, q0)

    # radial pull toward center + spark-rotated drift
    cx, cy = 8.0, 8.0
    dx, dy = (cx - x), (cy - y)
    rad = math.hypot(dx, dy) + 1e-6
    ux, uy = dx / rad, dy / rad

    # rotate by spark angle
    theta = math.radians(const.SPARK_ANGLE_DEG)
    rx = ux * math.cos(theta) - uy * math.sin(theta)
    ry = ux * math.sin(theta) + uy * math.cos(theta)

    # blend: gate weight controls how much spark drift vs radial pull
    vx = (1 - wg) * ux + wg * rx
    vy = (1 - wg) * uy + wg * ry

    # speed scales with kappa (higher kappa -> faster drift)
    speed = 6.0 * k
    return x + vx * speed * dt, y + vy * speed * dt


def main():
    # 128 start points uniformly distributed (16x8 grid)
    starts = []
    for i in range(16):
        for j in range(8):
            x = i + 0.5
            y = j * 2 + 0.5
            starts.append((x, y))

    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.2)

    # draw trajectories
    for x0, y0 in starts:
        xs, ys = [x0], [y0]
        x, y = x0, y0
        for _ in range(120):
            x, y = step_field(x, y)
            xs.append(x)
            ys.append(y)
        ax.plot(xs, ys, linewidth=0.8, alpha=0.8)

    ax.set_title("128 Grid — Physics-Only (Universal Equation Field)")
    out = Path("128_GRID_PHYSICS_ONLY.png")
    plt.savefig(out, dpi=240, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
