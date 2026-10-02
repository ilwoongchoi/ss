"""Plot continuous stress-pair dynamics across 1000 vortex body nodes.

4 stress pairs → 8D dimension curves:
  CO2/O2      → (h, p)      — Earth/Moon
  Light/Dark  → (gamma, d)  — Earth/Barnard
  Cold/Heat   → (nu, r)     — Moon/Sun
  Matter/Non  → (s, g)      — Sun/Barnard

Nodes are reordered to TCA cycle flow:
  V2(OAA) → V1(αKG) → V4(succinyl-CoA) → V3(succinate) → [wrap to V2]

Outputs:
  generated/vortex_dynamics.png   — multi-panel dynamics figure
  generated/vortex_dynamics_data.json — raw curve data
"""
from __future__ import annotations

import json
import math
import pathlib
from typing import Dict, List, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

GEN_DIR = pathlib.Path(__file__).parent / "generated"

# ---------------------------------------------------------------------------
# Stress pair definitions
# ---------------------------------------------------------------------------
STRESS_PAIRS_DEF = {
    "o2_co2": {
        "name": "CO₂ / O₂",
        "name_kr": "CO2/O2",
        "dims": ("h", "p"),
        "color_a": "#2ca02c",   # green — O2
        "color_b": "#d62728",   # red — CO2
        "color_pair": "#8B4513",
    },
    "light_dark": {
        "name": "Light / Dark",
        "name_kr": "Light/Dark",
        "dims": ("gamma", "d"),
        "color_a": "#FFD700",   # gold — light
        "color_b": "#1a1a2e",   # dark
        "color_pair": "#9966CC",
    },
    "heat_cold": {
        "name": "Heat / Cold",
        "name_kr": "Heat/Cold",
        "dims": ("nu", "r"),
        "color_a": "#FF4500",   # orange-red — heat
        "color_b": "#00BFFF",   # deep sky blue — cold
        "color_pair": "#FF8C00",
    },
    "matter_nonmatter": {
        "name": "Matter / Non-matter",
        "name_kr": "Matter/Non-matter",
        "dims": ("s", "g"),
        "color_a": "#8B0000",   # dark red — matter/mass
        "color_b": "#E0E0E0",   # light grey — non-matter
        "color_pair": "#708090",
    },
}

ALL_DIMS = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]

# TCA flow order of vortices
TCA_FLOW_ORDER = ["V2_waist", "V1_brain", "V4_pelvis", "V3_chest"]

VORTEX_LABELS = {
    "V1_brain": "V1: α-Ketoglutarate\n(brain/head)",
    "V2_waist": "V2: Oxaloacetate\n(waist/abdomen)",
    "V3_chest": "V3: Succinate\n(chest/thorax)",
    "V4_pelvis": "V4: Succinyl-CoA\n(pelvis/legs)",
}

TCA_STAGES = {
    "V2_waist": "Oxaloacetate",
    "V1_brain": "α-Ketoglutarate",
    "V4_pelvis": "Succinyl-CoA",
    "V3_chest": "Succinate",
}


# ---------------------------------------------------------------------------
# Load and reorder nodes
# ---------------------------------------------------------------------------

def load_and_reorder() -> Tuple[List[Dict], List[int]]:
    """Load nodes and reorder to TCA flow."""
    data = json.loads(
        (GEN_DIR / "vortex_body_nodes.json").read_text(encoding="utf-8")
    )
    all_nodes = data["nodes"]

    # Group by vortex
    by_vortex: Dict[str, List[Dict]] = {}
    for n in all_nodes:
        vid = n["vortex_id"]
        by_vortex.setdefault(vid, []).append(n)

    # Sort each vortex by spiral_idx
    for vid in by_vortex:
        by_vortex[vid].sort(key=lambda x: x["spiral_idx"])

    # Concatenate in TCA flow order
    reordered: List[Dict] = []
    boundaries: List[int] = []
    for vid in TCA_FLOW_ORDER:
        boundaries.append(len(reordered))
        reordered.extend(by_vortex.get(vid, []))

    return reordered, boundaries


# ---------------------------------------------------------------------------
# Extract dimension arrays
# ---------------------------------------------------------------------------

def extract_arrays(nodes: List[Dict]) -> Dict[str, np.ndarray]:
    """Extract 8D vectors as numpy arrays."""
    arrays = {}
    for d in ALL_DIMS:
        arrays[d] = np.array([n["vec_8d"][d] for n in nodes])
    return arrays


def smooth_curve(y: np.ndarray, n_smooth: int = 2000) -> np.ndarray:
    """Smooth a curve using moving average + linear interpolation."""
    x = np.arange(len(y))
    x_smooth = np.linspace(0, len(y) - 1, n_smooth)
    # Moving average smoothing
    window = max(3, len(y) // 50)
    kernel = np.ones(window) / window
    y_padded = np.concatenate([np.full(window // 2, y[0]), y, np.full(window // 2, y[-1])])
    y_smoothed = np.convolve(y_padded, kernel, mode="valid")
    y_smoothed = y_smoothed[:len(y)]
    # Interpolate to smooth x
    return np.interp(x_smooth, x, y_smoothed)


# ---------------------------------------------------------------------------
# Compute dynamics
# ---------------------------------------------------------------------------

def compute_stress_intensity(arrays: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """Stress pair intensity = mean of the two active dims."""
    result = {}
    for sp, info in STRESS_PAIRS_DEF.items():
        d1, d2 = info["dims"]
        result[sp] = (arrays[d1] + arrays[d2]) / 2.0
    return result


def compute_stress_balance(arrays: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """Stress pair balance = dim_a - dim_b (polarity)."""
    result = {}
    for sp, info in STRESS_PAIRS_DEF.items():
        d1, d2 = info["dims"]
        result[sp] = arrays[d1] - arrays[d2]
    return result


def compute_rate_of_change(y: np.ndarray) -> np.ndarray:
    """Discrete derivative (rate of change)."""
    return np.gradient(y)


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_dynamics(
    nodes: List[Dict],
    boundaries: List[int],
    arrays: Dict[str, np.ndarray],
):
    """Create the multi-panel dynamics figure."""

    n_nodes = len(nodes)
    x = np.arange(n_nodes)
    x_smooth = np.linspace(0, n_nodes - 1, 2000)

    # Vortex boundary positions
    boundary_labels = [TCA_STAGES[TCA_FLOW_ORDER[i]] for i in range(len(boundaries))]

    fig = plt.figure(figsize=(24, 32), facecolor="#0a0a12")
    fig.suptitle(
        "4-Vortex Spiral Dynamics — Stress Pair Continuous Curves\n"
        "TCA Flow: OAA → αKG → Succinyl-CoA → Succinate → OAA",
        fontsize=18, color="white", fontweight="bold", y=0.98
    )

    # Color palette
    bg = "#0a0a12"
    grid_color = "#1a1a2e"
    text_color = "#E0E0E0"

    # ── Panel 1: All 8D dimensions as continuous curves ──
    ax1 = fig.add_subplot(5, 1, 1)
    ax1.set_facecolor(bg)
    dim_colors = {
        "r": "#00BFFF", "h": "#2ca02c", "d": "#1a1a2e", "p": "#FFD700",
        "s": "#8B0000", "gamma": "#FFD700", "g": "#E0E0E0", "nu": "#FF4500",
    }
    dim_labels = {
        "r": "r (tempo/cold)", "h": "h (harmonic)", "d": "d (dissonance/dark)",
        "p": "p (periodicity)", "s": "s (brightness/mass)", "gamma": "γ (reverb/light)",
        "g": "g (binding/non-matter)", "nu": "ν (fractal/heat)",
    }

    for d in ALL_DIMS:
        y_smooth = smooth_curve(arrays[d])
        lw = 2.5 if d in ["gamma", "d", "h", "p", "s", "g", "nu", "r"] else 1.5
        ax1.plot(x_smooth, y_smooth, label=dim_labels[d],
                 color=dim_colors[d], linewidth=lw, alpha=0.85)

    for i, b in enumerate(boundaries):
        ax1.axvline(b, color="#444466", linestyle="--", alpha=0.6, linewidth=1)
        if i < len(boundary_labels):
            ax1.text(b + n_nodes * 0.01, 0.95, boundary_labels[i],
                     color=text_color, fontsize=9, va="top", fontweight="bold")
    # Wrap-around boundary
    ax1.axvline(n_nodes, color="#444466", linestyle="--", alpha=0.4, linewidth=1)

    ax1.set_ylabel("8D Value", color=text_color, fontsize=12)
    ax1.set_title("■ 8D Music Dimension Curves (all 1000 nodes, TCA flow order)",
                  color=text_color, fontsize=14, fontweight="bold")
    ax1.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=9,
               facecolor=bg, edgecolor=grid_color, labelcolor=text_color)
    ax1.tick_params(colors=text_color)
    for spine in ax1.spines.values():
        spine.set_color(grid_color)
    ax1.grid(True, alpha=0.15, color=grid_color)
    ax1.set_xlim(0, n_nodes)
    ax1.set_ylim(0, 1.05)

    # ── Panel 2: Stress pair intensity (4 curves) ──
    ax2 = fig.add_subplot(5, 1, 2)
    ax2.set_facecolor(bg)

    intensities = compute_stress_intensity(arrays)
    for sp, info in STRESS_PAIRS_DEF.items():
        y_smooth = smooth_curve(intensities[sp])
        ax2.plot(x_smooth, y_smooth, label=f"{info['name']} ({info['name_kr']})",
                 color=info["color_pair"], linewidth=3, alpha=0.85)
        ax2.fill_between(x_smooth, 0.5, y_smooth, alpha=0.08, color=info["color_pair"])

    for i, b in enumerate(boundaries):
        ax2.axvline(b, color="#444466", linestyle="--", alpha=0.6, linewidth=1)
        if i < len(boundary_labels):
            ax2.text(b + n_nodes * 0.01, 0.95, boundary_labels[i],
                     color=text_color, fontsize=9, va="top", fontweight="bold")

    ax2.set_ylabel("Intensity", color=text_color, fontsize=12)
    ax2.set_title("■ Stress Pair Intensity (mean of active dims) -- Dynamics Strength",
                  color=text_color, fontsize=14, fontweight="bold")
    ax2.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=10,
               facecolor=bg, edgecolor=grid_color, labelcolor=text_color)
    ax2.tick_params(colors=text_color)
    for spine in ax2.spines.values():
        spine.set_color(grid_color)
    ax2.grid(True, alpha=0.15, color=grid_color)
    ax2.set_xlim(0, n_nodes)
    ax2.set_ylim(0.3, 0.9)

    # ── Panel 3: Stress pair balance / polarity ──
    ax3 = fig.add_subplot(5, 1, 3)
    ax3.set_facecolor(bg)

    balances = compute_stress_balance(arrays)
    for sp, info in STRESS_PAIRS_DEF.items():
        y_smooth = smooth_curve(balances[sp])
        ax3.plot(x_smooth, y_smooth, label=f"{info['name']} Δ({info['dims'][0]}−{info['dims'][1]})",
                 color=info["color_pair"], linewidth=2.5, alpha=0.85)

    ax3.axhline(0, color="#666680", linewidth=1, linestyle="-", alpha=0.5)

    for i, b in enumerate(boundaries):
        ax3.axvline(b, color="#444466", linestyle="--", alpha=0.6, linewidth=1)
        if i < len(boundary_labels):
            ax3.text(b + n_nodes * 0.01, 0.28, boundary_labels[i],
                     color=text_color, fontsize=9, va="top", fontweight="bold")

    ax3.set_ylabel("Balance (Δ)", color=text_color, fontsize=12)
    ax3.set_title("■ Stress Pair Polarity (dim_a - dim_b) -- Polarity Transition",
                  color=text_color, fontsize=14, fontweight="bold")
    ax3.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=10,
               facecolor=bg, edgecolor=grid_color, labelcolor=text_color)
    ax3.tick_params(colors=text_color)
    for spine in ax3.spines.values():
        spine.set_color(grid_color)
    ax3.grid(True, alpha=0.15, color=grid_color)
    ax3.set_xlim(0, n_nodes)

    # ── Panel 4: Rate of change (dynamics / acceleration) ──
    ax4 = fig.add_subplot(5, 1, 4)
    ax4.set_facecolor(bg)

    for sp, info in STRESS_PAIRS_DEF.items():
        roc = compute_rate_of_change(intensities[sp])
        y_smooth = smooth_curve(roc)
        ax4.plot(x_smooth, y_smooth, label=f"{info['name']}",
                 color=info["color_pair"], linewidth=2, alpha=0.8)

    ax4.axhline(0, color="#666680", linewidth=1, linestyle="-", alpha=0.5)

    for i, b in enumerate(boundaries):
        ax4.axvline(b, color="#444466", linestyle="--", alpha=0.6, linewidth=1)
        if i < len(boundary_labels):
            ax4.text(b + n_nodes * 0.01, 0.9, boundary_labels[i],
                     color=text_color, fontsize=9, va="top", fontweight="bold")

    ax4.set_ylabel("dI/dn", color=text_color, fontsize=12)
    ax4.set_title("■ Rate of Change (dynamics) -- Velocity / Acceleration",
                  color=text_color, fontsize=14, fontweight="bold")
    ax4.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=10,
               facecolor=bg, edgecolor=grid_color, labelcolor=text_color)
    ax4.tick_params(colors=text_color)
    for spine in ax4.spines.values():
        spine.set_color(grid_color)
    ax4.grid(True, alpha=0.15, color=grid_color)
    ax4.set_xlim(0, n_nodes)

    # ── Panel 5: Polar / circular TCA cycle plot ──
    ax5 = fig.add_subplot(5, 1, 5, projection="polar")
    ax5.set_facecolor(bg)

    # Compute mean intensity per vortex for each stress pair
    n_vortices = len(TCA_FLOW_ORDER)
    vortex_means: Dict[str, List[float]] = {}
    for sp in STRESS_PAIRS_DEF:
        means = []
        for vid in TCA_FLOW_ORDER:
            mask = [n["vortex_id"] == vid for n in nodes]
            vals = [intensities[sp][i] for i in range(n_nodes) if mask[i]]
            means.append(np.mean(vals) if vals else 0.5)
        # Close the loop
        means.append(means[0])
        vortex_means[sp] = means

    # Angular positions for 4 vortices + closing point
    angles = np.linspace(0, 2 * np.pi, n_vortices + 1)

    for sp, info in STRESS_PAIRS_DEF.items():
        vals = vortex_means[sp]
        ax5.plot(angles, vals, "o-", label=info["name"],
                 color=info["color_pair"], linewidth=2.5, markersize=8, alpha=0.85)
        ax5.fill(angles, vals, alpha=0.08, color=info["color_pair"])

    # Vortex labels on polar plot
    ax5.set_xticks(angles[:-1])
    ax5.set_xticklabels(
        [TCA_STAGES[vid] for vid in TCA_FLOW_ORDER],
        color=text_color, fontsize=11, fontweight="bold"
    )
    ax5.set_title("■ TCA Cycle Stress Pair Map (polar) -- 4 Vortex Circulation",
                  color=text_color, fontsize=14, fontweight="bold", pad=20)
    ax5.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=10,
               facecolor=bg, edgecolor=grid_color, labelcolor=text_color)
    ax5.tick_params(colors=text_color)
    ax5.grid(True, alpha=0.2, color=grid_color)
    ax5.set_ylim(0.3, 0.8)

    plt.tight_layout(rect=[0, 0, 0.88, 0.96])

    out_path = GEN_DIR / "vortex_dynamics.png"
    fig.savefig(out_path, dpi=150, facecolor=bg, bbox_inches="tight")
    plt.close(fig)
    print(f"→ {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# Export curve data as JSON
# ---------------------------------------------------------------------------

def export_curve_data(
    nodes: List[Dict],
    arrays: Dict[str, np.ndarray],
    intensities: Dict[str, np.ndarray],
    balances: Dict[str, np.ndarray],
):
    """Export raw curve data for further analysis."""
    n = len(nodes)
    data = {
        "n_nodes": n,
        "tca_flow_order": TCA_FLOW_ORDER,
        "boundaries": [],
        "dims": {},
        "stress_intensity": {},
        "stress_balance": {},
        "stress_rate_of_change": {},
    }

    # Boundaries
    by_vortex: Dict[str, int] = {}
    for i, node in enumerate(nodes):
        vid = node["vortex_id"]
        if vid not in by_vortex:
            by_vortex[vid] = i
    for vid in TCA_FLOW_ORDER:
        data["boundaries"].append({
            "vortex": vid,
            "tca_stage": TCA_STAGES[vid],
            "start_idx": by_vortex.get(vid, 0),
        })

    # Dimension curves
    for d in ALL_DIMS:
        data["dims"][d] = [round(float(v), 4) for v in arrays[d]]

    # Stress pair curves
    for sp in STRESS_PAIRS_DEF:
        data["stress_intensity"][sp] = [round(float(v), 4) for v in intensities[sp]]
        data["stress_balance"][sp] = [round(float(v), 4) for v in balances[sp]]
        roc = compute_rate_of_change(intensities[sp])
        data["stress_rate_of_change"][sp] = [round(float(v), 6) for v in roc]

    out = GEN_DIR / "vortex_dynamics_data.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"→ {out}")


# ---------------------------------------------------------------------------
# Print dynamics summary
# ---------------------------------------------------------------------------

def print_dynamics_summary(
    nodes: List[Dict],
    intensities: Dict[str, np.ndarray],
    balances: Dict[str, np.ndarray],
):
    """Print human-readable dynamics summary."""
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("4-VORTEX DYNAMICS SUMMARY")
    lines.append("=" * 80)
    lines.append("")
    lines.append("TCA Flow: V2(OAA) → V1(αKG) → V4(Succinyl-CoA) → V3(Succinate) → V2")
    lines.append("")

    # Per-vortex stress pair stats
    lines.append("■ Stress Pair Intensity by Vortex")
    lines.append("-" * 80)
    header = f"  {'Vortex':20s}"
    for sp in STRESS_PAIRS_DEF:
        header += f"  {STRESS_PAIRS_DEF[sp]['name']:18s}"
    lines.append(header)

    by_vortex: Dict[str, List[int]] = {}
    for i, node in enumerate(nodes):
        vid = node["vortex_id"]
        by_vortex.setdefault(vid, []).append(i)

    for vid in TCA_FLOW_ORDER:
        idxs = by_vortex.get(vid, [])
        row = f"  {TCA_STAGES[vid]:20s}"
        for sp in STRESS_PAIRS_DEF:
            vals = [intensities[sp][i] for i in idxs]
            mean_v = np.mean(vals) if vals else 0
            std_v = np.std(vals) if vals else 0
            row += f"  {mean_v:.3f}±{std_v:.3f}    "
        lines.append(row)

    lines.append("")
    lines.append("■ Stress Pair Balance (polarity) by Vortex")
    lines.append("-" * 80)
    lines.append(header)

    for vid in TCA_FLOW_ORDER:
        idxs = by_vortex.get(vid, [])
        row = f"  {TCA_STAGES[vid]:20s}"
        for sp in STRESS_PAIRS_DEF:
            vals = [balances[sp][i] for i in idxs]
            mean_v = np.mean(vals) if vals else 0
            row += f"  {mean_v:+.3f}            "
        lines.append(row)

    lines.append("")
    lines.append("■ Dominant Stress Pair per Vortex (highest mean intensity)")
    lines.append("-" * 80)
    for vid in TCA_FLOW_ORDER:
        idxs = by_vortex.get(vid, [])
        best_sp = None
        best_mean = 0
        for sp in STRESS_PAIRS_DEF:
            vals = [intensities[sp][i] for i in idxs]
            m = np.mean(vals) if vals else 0
            if m > best_mean:
                best_mean = m
                best_sp = sp
        info = STRESS_PAIRS_DEF[best_sp]
        lines.append(f"  {TCA_STAGES[vid]:20s} → {info['name']} ({info['name_kr']})  intensity={best_mean:.3f}")

    lines.append("")
    lines.append("■ Transition Dynamics (rate of change at vortex boundaries)")
    lines.append("-" * 80)
    for i, vid in enumerate(TCA_FLOW_ORDER):
        idxs = by_vortex.get(vid, [])
        if not idxs:
            continue
        start_i = idxs[0]
        end_i = idxs[-1]
        next_vid = TCA_FLOW_ORDER[(i + 1) % len(TCA_FLOW_ORDER)]
        next_idxs = by_vortex.get(next_vid, [])
        if not next_idxs:
            continue
        next_start = next_idxs[0]

        lines.append(f"  {TCA_STAGES[vid]} → {TCA_STAGES[next_vid]}:")
        for sp in STRESS_PAIRS_DEF:
            roc = intensities[sp][next_start] - intensities[sp][end_i]
            direction = "↑" if roc > 0 else "↓"
            lines.append(f"    {STRESS_PAIRS_DEF[sp]['name']:20s}  Δ={roc:+.4f} {direction}")

    lines.append("")
    text = "\n".join(lines)
    (GEN_DIR / "vortex_dynamics_summary.txt").write_text(text, encoding="utf-8")
    print(text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    nodes, boundaries = load_and_reorder()
    arrays = extract_arrays(nodes)
    intensities = compute_stress_intensity(arrays)
    balances = compute_stress_balance(arrays)

    print_dynamics_summary(nodes, intensities, balances)
    plot_dynamics(nodes, boundaries, arrays)
    export_curve_data(nodes, arrays, intensities, balances)
