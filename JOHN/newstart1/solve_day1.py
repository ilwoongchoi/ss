"""solve_day1.py

Day-1 minimal homeostasis solver.

Pipeline
--------
1. Load 24 geometry nodes (MASTER_GEOMETRY_NODES.csv)
2. Load 451-spiral ROI (ROI_452_SPIRAL_SORTED.csv) -> Phi_A (expansion) seed
3. Load homeostasis requirement sample (HOMEOSTASIS_24_NODE_REQUIREMENTS_SAMPLE.json)
   -> Phi_B (binding) seed via required_u
4. Build 2D grid, place A/B point sources on nodes, diffuse (Gaussian kernel)
5. sigma(x) = |Phi_B * r - Phi_A / r| * sin(theta - 138.88 deg)
6. U(x)     = (sigma(x) - 7.4)^2
7. V(x)     = -grad U       (action vector field: "what every subject must do")
8. Per-node action vector table -> subject_actions.csv
9. Maps -> sigma_map.png, U_map.png, V_field.png
"""

from __future__ import annotations
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
THETA_SPARK_DEG = 138.88
SIGMA_STAR = 7.4                  # blood pH homeostasis target
GRID_N = 160
GRID_EXTENT = 8.0                 # model units, centered on origin
DIFFUSION_SIGMA = 0.6             # Gaussian kernel sigma for point sources


# ---------------------------------------------------------------------------
# 1. Load nodes
# ---------------------------------------------------------------------------
def load_nodes() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "MASTER_GEOMETRY_NODES.csv")
    df = df.dropna(subset=["x", "y", "z"]).reset_index(drop=True)
    # project to 2D (x, y) for day-1 solve
    return df[["node_id", "name", "x", "y", "z", "archetype"]]


# ---------------------------------------------------------------------------
# 2/3. Load Phi_A (ROI spiral) and Phi_B (homeostasis required_u)
# ---------------------------------------------------------------------------
def load_phi_seeds(nodes: pd.DataFrame):
    roi = pd.read_csv(ROOT / "ROI_452_SPIRAL_SORTED.csv")
    # Phi_A seed: mean radial spiral strength distributed on nodes via nearest ROI
    roi_xy = roi[["x", "y"]].to_numpy()
    # recenter ROI to origin (ROI is in image coords ~0..20)
    roi_xy = roi_xy - roi_xy.mean(axis=0)
    # scale ROI range to match model extent (~+-4)
    scale = 4.0 / np.max(np.abs(roi_xy))
    roi_xy = roi_xy * scale
    roi_r = roi["r"].to_numpy()
    # Phi_A at each node = inverse-distance weighted average of roi_r (expansion)
    phi_A = np.zeros(len(nodes))
    for i, (_, row) in enumerate(nodes.iterrows()):
        d = np.linalg.norm(roi_xy - np.array([row.x, row.y]), axis=1) + 1e-3
        w = 1.0 / d**2
        phi_A[i] = np.sum(w * roi_r) / np.sum(w)

    # Phi_B seed: homeostasis required_u sample
    hs = json.loads((ROOT / "HOMEOSTASIS_24_NODE_REQUIREMENTS_SAMPLE.json").read_text())
    u_vals = np.array(list(hs["required_u"].values()))
    # tile/truncate to match node count
    phi_B = np.resize(u_vals, len(nodes))

    # normalize to similar magnitude (~O(1))
    phi_A = phi_A / (phi_A.mean() + 1e-9)
    phi_B = phi_B / (phi_B.mean() + 1e-9)
    return phi_A, phi_B, roi_xy


# ---------------------------------------------------------------------------
# 4. Diffuse point sources onto 2D grid
# ---------------------------------------------------------------------------
def build_grid():
    ax = np.linspace(-GRID_EXTENT, GRID_EXTENT, GRID_N)
    X, Y = np.meshgrid(ax, ax)
    return ax, X, Y


def diffuse_field(nodes: pd.DataFrame, values: np.ndarray, X, Y) -> np.ndarray:
    field = np.zeros_like(X)
    s2 = 2.0 * DIFFUSION_SIGMA ** 2
    for (_, row), v in zip(nodes.iterrows(), values):
        d2 = (X - row.x) ** 2 + (Y - row.y) ** 2
        field += v * np.exp(-d2 / s2)
    return field


# ---------------------------------------------------------------------------
# 5/6/7. sigma -> U -> V
# ---------------------------------------------------------------------------
def compute_sigma(phi_A_field, phi_B_field, X, Y):
    """σ is the *imbalance* between expansion (Φ_A/r) and binding (Φ_B·r).
    NO hardcoded spark angle — the asymmetry emerges from Φ_A, Φ_B themselves.
    The dominant angular mode of |σ| is then measured to check whether it
    naturally coincides with 138.88° (spark), 69.44° (half-spark), or
    208.32° (D3 equilibrium). If yes, the angle is emergent, not imposed.
    """
    r = np.sqrt(X ** 2 + Y ** 2) + 1e-3
    # raw signed imbalance (no external gate)
    sigma_raw = phi_B_field * r - phi_A_field / r
    # rescale to biological pH band 6.8..7.8 centered on 7.4
    s_min, s_max = np.nanmin(sigma_raw), np.nanmax(sigma_raw)
    sigma = 6.8 + (sigma_raw - s_min) / (s_max - s_min + 1e-9) * 1.0
    return sigma


def measure_emergent_spark_angle(sigma, X, Y) -> dict:
    """Find the polar angle at which |sigma - 7.4| is maximal (spark direction)."""
    r = np.sqrt(X ** 2 + Y ** 2)
    theta = np.degrees(np.arctan2(Y, X)) % 360.0
    dev = np.abs(sigma - SIGMA_STAR)
    # only consider an annulus (ignore origin and far edges)
    mask = (r > 1.0) & (r < GRID_EXTENT * 0.7)
    theta_flat = theta[mask].ravel()
    dev_flat   = dev[mask].ravel()
    # angular histogram of deviation
    bins = np.linspace(0, 360, 73)  # 5° bins
    hist, edges = np.histogram(theta_flat, bins=bins, weights=dev_flat)
    counts, _   = np.histogram(theta_flat, bins=bins)
    mean_dev = hist / np.maximum(counts, 1)
    peak_idx = int(np.argmax(mean_dev))
    peak_angle = (edges[peak_idx] + edges[peak_idx + 1]) / 2.0
    canon = {"spark_138.88": 138.88, "half_69.44": 69.44, "D3_208.32": 208.32}
    distances = {k: min(abs(peak_angle - v), 360 - abs(peak_angle - v))
                 for k, v in canon.items()}
    nearest = min(distances.items(), key=lambda kv: kv[1])
    return {
        "peak_angle_deg": round(peak_angle, 2),
        "distances_to_canonical": {k: round(v, 2) for k, v in distances.items()},
        "nearest_canonical": nearest[0],
        "delta_deg": round(nearest[1], 2),
        "peak_deviation": round(float(mean_dev[peak_idx]), 4),
    }


def compute_U_and_V(sigma, ax):
    U = (sigma - SIGMA_STAR) ** 2
    dUdy, dUdx = np.gradient(U, ax, ax)          # note: gradient returns [d/row, d/col]
    Vx, Vy = -dUdx, -dUdy
    return U, Vx, Vy


# ---------------------------------------------------------------------------
# 8. Per-node action vectors
# ---------------------------------------------------------------------------
def sample_field_at_nodes(nodes, field, ax):
    out = []
    for _, row in nodes.iterrows():
        ix = np.clip(np.searchsorted(ax, row.x), 0, len(ax) - 1)
        iy = np.clip(np.searchsorted(ax, row.y), 0, len(ax) - 1)
        out.append(field[iy, ix])
    return np.array(out)


# ---------------------------------------------------------------------------
# 9. Plots
# ---------------------------------------------------------------------------
def plot_all(ax, X, Y, sigma, U, Vx, Vy, nodes, out_prefix: str):
    # sigma map
    fig, a = plt.subplots(figsize=(7, 6))
    im = a.pcolormesh(X, Y, sigma, cmap="RdBu_r", vmin=6.8, vmax=7.8)
    a.contour(X, Y, sigma, levels=[SIGMA_STAR], colors="k", linewidths=1.2)
    a.scatter(nodes.x, nodes.y, c="k", s=30, zorder=5)
    for _, r in nodes.iterrows():
        a.annotate(str(r.node_id), (r.x, r.y), fontsize=7, color="white")
    a.set_title(f"sigma field  (target sigma* = {SIGMA_STAR})")
    fig.colorbar(im, ax=a, label="sigma (pH-analog)")
    a.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(f"{out_prefix}_sigma_map.png", dpi=130)
    plt.close(fig)

    # U map
    fig, a = plt.subplots(figsize=(7, 6))
    im = a.pcolormesh(X, Y, U, cmap="magma")
    a.scatter(nodes.x, nodes.y, c="cyan", s=30, zorder=5)
    a.set_title("U(x) = (sigma - 7.4)^2   (homeostasis cost)")
    fig.colorbar(im, ax=a, label="U")
    a.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(f"{out_prefix}_U_map.png", dpi=130)
    plt.close(fig)

    # V field
    fig, a = plt.subplots(figsize=(7, 6))
    step = 8
    a.pcolormesh(X, Y, np.sqrt(Vx ** 2 + Vy ** 2), cmap="viridis", alpha=0.7)
    a.quiver(X[::step, ::step], Y[::step, ::step],
             Vx[::step, ::step], Vy[::step, ::step],
             color="white", scale=None, width=0.003)
    a.scatter(nodes.x, nodes.y, c="red", s=40, zorder=5)
    for _, r in nodes.iterrows():
        a.annotate(str(r.node_id), (r.x, r.y), fontsize=7, color="yellow")
    a.set_title("V(x) = -grad U   (action vector field toward pH 7.4)")
    a.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(f"{out_prefix}_V_field.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    nodes = load_nodes()
    print(f"[1] nodes loaded: {len(nodes)}")

    phi_A_vals, phi_B_vals, roi_xy = load_phi_seeds(nodes)
    print(f"[2] Phi_A seed range  {phi_A_vals.min():.3f} .. {phi_A_vals.max():.3f}")
    print(f"[3] Phi_B seed range  {phi_B_vals.min():.3f} .. {phi_B_vals.max():.3f}")

    ax, X, Y = build_grid()
    Phi_A = diffuse_field(nodes, phi_A_vals, X, Y)
    Phi_B = diffuse_field(nodes, phi_B_vals, X, Y)
    print(f"[4] fields diffused on grid {GRID_N}x{GRID_N}")

    sigma = compute_sigma(Phi_A, Phi_B, X, Y)
    U, Vx, Vy = compute_U_and_V(sigma, ax)
    print(f"[5-7] sigma range {sigma.min():.3f}..{sigma.max():.3f}   "
          f"|V| max {np.sqrt(Vx**2+Vy**2).max():.3f}")

    emergent = measure_emergent_spark_angle(sigma, X, Y)
    print(f"[VERIFY] emergent spark angle = {emergent['peak_angle_deg']}°")
    print(f"         nearest canonical = {emergent['nearest_canonical']}"
          f"  (Δ = {emergent['delta_deg']}°)")
    print(f"         distances: {emergent['distances_to_canonical']}")

    # per-node action vectors
    sig_n = sample_field_at_nodes(nodes, sigma, ax)
    U_n   = sample_field_at_nodes(nodes, U,   ax)
    Vx_n  = sample_field_at_nodes(nodes, Vx,  ax)
    Vy_n  = sample_field_at_nodes(nodes, Vy,  ax)
    out = nodes.copy()
    out["sigma"]     = sig_n
    out["deviation"] = sig_n - SIGMA_STAR
    out["U"]         = U_n
    out["Vx"]        = Vx_n
    out["Vy"]        = Vy_n
    out["V_mag"]     = np.sqrt(Vx_n ** 2 + Vy_n ** 2)
    out["V_angle_deg"] = np.degrees(np.arctan2(Vy_n, Vx_n))
    out["rebranch_flag"] = (np.abs(out["deviation"]) > 0.3).astype(int)
    out.to_csv(ROOT / "subject_actions.csv", index=False)
    print(f"[8] subject_actions.csv written  ({len(out)} rows)")

    plot_all(ax, X, Y, sigma, U, Vx, Vy, nodes, str(ROOT / "day1"))
    print("[9] PNGs written: day1_sigma_map.png, day1_U_map.png, day1_V_field.png")

    print("\n--- per-subject summary ---")
    print(out[["node_id", "name", "sigma", "deviation",
               "V_mag", "V_angle_deg", "rebranch_flag"]].to_string(index=False))


if __name__ == "__main__":
    main()
