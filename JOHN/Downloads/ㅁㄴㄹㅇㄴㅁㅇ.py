# -*- coding: utf-8 -*-
"""
generate_128_grid_v4_hysteresis_pure.py
======================================
128-Type trajectory grid driven only by the canonical geometry package:
- single-source constants: `geometry_package/absolute_constants.py`
- canonical operators: `geometry_package/chart_operators.py`
- renormalization / closure scalars: `geometry_package/universal_equation.py`

No registry JSON loading. No domain-specific auxiliary laws.
Type differences are expressed as chart-address initial conditions.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from geometry_package.absolute_constants import (
    BETTI_11,
    BETTI_7,
    CHIRALITY_CONSTANT,
    DRIFT_DELTA,
    F_1_32,
    GABA_C_R_CAB,
    GABA_C_R_CA,
    GABA_C_V_APEX,
    GATE_5_32,
    H2_W7,
    LOOP_STRENGTH_5,
    METRIC_RATIO,
    NIGHT_HYSTERESIS,
    PI,
    REALITY_TENSION,
    RENORMALIZATION_BRIDGE,
    RESID_DATA_5_32,
    SH_R_FWHM_L,
    SH_R_FWHM_R,
    SH_R_STAR,
    SPARK_ANGLE_DEG,
    SPARK_LEAP_DIST,
    TOTAL_DEBT_AREA,
    TUNNEL_TENSION,
    UNIT_64,
    W7_EXACT,
)
from geometry_package.chart_operators import plp_spine_manifold, solve_radial_psi, spark_refraction
from geometry_package.universal_equation import coupling_scale, mismatch_delta, universal_latent


matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False


N_ROWS = 16
N_COLS = 16
ROW_CENTER_OFFSET = 0.5
COL_CENTER_OFFSET = 0.5

DT = 0.10

# 16 MBTI × 4 blood × 2 gender = 128
ALL_MBTI = [
    "INTJ",
    "INTP",
    "ENTJ",
    "ENTP",
    "INFJ",
    "INFP",
    "ENFJ",
    "ENFP",
    "ISTJ",
    "ISFJ",
    "ESTJ",
    "ESFJ",
    "ISTP",
    "ISFP",
    "ESTP",
    "ESFP",
]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]


# Chart address mapping (coordinateization, not a physics law)
GROUP_WIDTH = 2
FEMALE_GROUP_ORDER = ["EJ", "EP", "IJ", "IP"]
MALE_GROUP_ORDER = ["IP", "IJ", "EP", "EJ"]
GROUP_MAP_FEMALE = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
GROUP_MAP_MALE = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}

SN_OFFSET = {"S": -0.25, "N": 0.25}
TF_OFFSET = {"T": -0.125, "F": 0.125}
BLOOD_OFFSET_X = {"O": -0.03, "A": 0.03, "B": -0.03, "AB": 0.03}
BLOOD_OFFSET_Y = {"O": 0.06, "A": 0.03, "B": -0.03, "AB": -0.06}


@dataclass(frozen=True)
class Trajectory:
    mbti: str
    blood: str
    gender: str
    branch: str
    pts: list[tuple[float, float, object]]


def _clamp(v: float, lo: float, hi: float) -> float:
    return float(max(lo, min(v, hi)))


def _row_centers() -> list[float]:
    return [r + ROW_CENTER_OFFSET for r in range(N_ROWS)]


def get_start_position(mbti: str, blood: str, gender: str) -> tuple[float, float]:
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_key = f"{ei}{jp}"
    group_map = GROUP_MAP_FEMALE if gender == "F" else GROUP_MAP_MALE
    base_col = float(group_map[group_key])
    x = base_col + COL_CENTER_OFFSET + SN_OFFSET[sn] + TF_OFFSET[tf] + BLOOD_OFFSET_X[blood]
    y = ROW_CENTER_OFFSET + BLOOD_OFFSET_Y[blood]
    return float(x), float(y)


def _twilight_bands() -> tuple[float, float, float, float]:
    """
    Derive twilight transition bands from the SH peak FWHM extents and scale to 16 rows.
    This is renderer-only; it just defines where hysteresis switching is sampled.
    """
    tw1_lo = float((SH_R_STAR - SH_R_FWHM_L) * (N_ROWS / (SH_R_STAR * 2.0)))
    tw1_hi = float((SH_R_STAR + SH_R_FWHM_R) * (N_ROWS / (SH_R_STAR * 2.0)))
    tw2_lo = float(N_ROWS - tw1_hi)
    tw2_hi = float(N_ROWS - tw1_lo)
    return tw1_lo, tw1_hi, tw2_lo, tw2_hi


def _universal_field_scale() -> tuple[float, float, float]:
    """
    Renormalized scalars used by the engine, sourced from the canonical universal equation.
    """
    u_scale = float(coupling_scale())
    u_latent = float(universal_latent())
    mis = float(mismatch_delta())
    return u_scale, u_latent, mis


def generate_trajectory_pure(
    mbti: str,
    blood: str,
    gender: str,
    *,
    branch: str,
    area_override: float,
) -> list[tuple[float, float, object]]:
    """
    Deterministic trajectory for one type.
    Returns a list of (x,y,flag) where flag is:
    - False: normal point
    - True: spark leap (diagonal reset)
    """
    x, y = get_start_position(mbti, blood, gender)
    pts: list[tuple[float, float, object]] = [(x, y, False)]

    branch_sign = 1.0 if branch == "sunrise" else -1.0
    tw1_lo, tw1_hi, tw2_lo, tw2_hi = _twilight_bands()

    u_scale, u_latent, mis = _universal_field_scale()

    # Canonical 4D metric & torsion (same scaffold as the renderer, driven by universal scalars).
    metric_4d = float(REALITY_TENSION) * (1.0 + LOOP_STRENGTH_5 / 100.0) * u_scale
    torsion_4d = float(H2_W7 * (BETTI_11 / BETTI_7)) * (1.0 + mis) * (1.0 + RENORMALIZATION_BRIDGE / 1000.0)
    torsion_4d *= 1.0 + (u_latent - 1.0) * 0.05

    # Hysteresis memory (bounded by the 1/32 gate scale).
    # Use the empirically locked NIGHT_HYSTERESIS as the only amplitude scale.
    hyst_tau = float((NIGHT_HYSTERESIS * 2.317382542906709) * F_1_32)
    memory_y = float(y)
    switch_state = False
    threshold_on = float(-hyst_tau * 0.60)
    threshold_off = float(threshold_on * 0.30)

    row_centers = _row_centers()
    for i in range(1, len(row_centers)):
        y_target = float(row_centers[i])
        while y < y_target - 1e-9:
            step = min(DT, y_target - y)

            # 1) Radial operator ψ from k, quantized on the 1/64 grid.
            k_raw = math.hypot(x - 8.0, y - 8.0) * F_1_32
            k = float(math.floor(k_raw / UNIT_64 + 0.5) * UNIT_64)
            psi = float(solve_radial_psi(k))

            # 2) Base rotational field around (8,8).
            base_vx = -torsion_4d * (y - 8.0) * psi
            vx = float(base_vx)
            # y is the chart's time/phase axis; advance monotonically.
            vy_step = float(step)

            # 3) Hysteresis window: only inside the twilight bands.
            in_tw = (tw1_lo <= y <= tw1_hi) or (tw2_lo <= y <= tw2_hi)
            if in_tw:
                if y <= tw1_hi:
                    tw_phase = PI * (y - tw1_lo) / max(1e-9, (tw1_hi - tw1_lo))
                else:
                    tw_phase = PI * (y - tw2_lo) / max(1e-9, (tw2_hi - tw2_lo))

                alpha = _clamp(step / (hyst_tau + 1e-9), 0.0, 0.50)
                memory_y = (1.0 - alpha) * memory_y + alpha * y
                lag = float(memory_y - y)

                if lag < threshold_on and not switch_state:
                    switch_state = True
                elif lag > threshold_off and switch_state:
                    switch_state = False

                # Spark: diagonal reset, only on the PLP seam.
                if (
                    plp_spine_manifold((x, y), n_rows=float(N_ROWS), n_cols=float(N_COLS)) > 0.0
                    and switch_state
                ):
                    dx_leap, dy_leap = spark_refraction((float(SPARK_LEAP_DIST), 0.0))
                    x = _clamp(x + dx_leap, 0.0, float(N_COLS))
                    y = y + dy_leap
                    switch_state = False
                    memory_y = y
                    pts.append((float(x), float(y), True))
                    continue

                # Hysteresis lateral separation (area calibration knob).
                void_gap = float(F_1_32 - UNIT_64)
                vx += float(branch_sign * area_override * metric_4d * void_gap * math.sin(tw_phase))

            x = _clamp(x + vx * step, 0.0, float(N_COLS))
            y = float(y + vy_step)

        pts.append((float(x), float(y), False))

    return pts


def _pts_xy_sorted(pts: list[tuple[float, float, object]]) -> np.ndarray:
    arr = np.array([[p[0], p[1]] for p in pts], dtype=float)
    return arr[np.argsort(arr[:, 1])]


def compute_loop_area(area_override: float, *, samples: int = 600) -> float:
    """
    Computes mean hysteresis area between sunrise/sunset branches, sampled only inside twilight bands.
    Uses representative types (engine is universal).
    """
    tw1_lo, tw1_hi, tw2_lo, tw2_hi = _twilight_bands()
    y_grid = np.linspace(ROW_CENTER_OFFSET, float(N_ROWS) - ROW_CENTER_OFFSET, int(samples))

    total_area = 0.0
    count = 0
    for mbti in ("ENTJ", "ISFP"):
        for gender in ("M", "F"):
            p_sr = generate_trajectory_pure(mbti, "O", gender, branch="sunrise", area_override=area_override)
            p_ss = generate_trajectory_pure(mbti, "O", gender, branch="sunset", area_override=area_override)

            sr = _pts_xy_sorted(p_sr)
            ss = _pts_xy_sorted(p_ss)
            x_sr = np.interp(y_grid, sr[:, 1], sr[:, 0])
            x_ss = np.interp(y_grid, ss[:, 1], ss[:, 0])

            mask = ((y_grid >= tw1_lo) & (y_grid <= tw1_hi)) | ((y_grid >= tw2_lo) & (y_grid <= tw2_hi))
            area = float(np.trapezoid(np.abs(x_sr - x_ss)[mask], y_grid[mask]))
            total_area += area
            count += 1

    return float(total_area / max(1, count))


def find_area_for_target(target_area: float, *, max_iter: int = 24) -> float:
    low = 0.0
    high = max(0.5, target_area * 5.0)
    while compute_loop_area(high) < target_area:
        high *= 1.7

    for _ in range(int(max_iter)):
        mid = 0.5 * (low + high)
        if compute_loop_area(mid) < target_area:
            low = mid
        else:
            high = mid

    return float(0.5 * (low + high))


def _draw_background(ax: plt.Axes) -> None:
    tw1_lo, tw1_hi, tw2_lo, tw2_hi = _twilight_bands()

    for r in range(N_ROWS):
        for c in range(N_COLS):
            ax.add_patch(
                mpatches.Rectangle(
                    (c, r),
                    1.0,
                    1.0,
                    facecolor="white",
                    edgecolor="#E0E0E0",
                    linewidth=0.5,
                    zorder=0,
                )
            )

    ax.add_patch(
        mpatches.Rectangle(
            (0.0, tw1_lo),
            float(N_COLS),
            float(tw1_hi - tw1_lo),
            facecolor="#99CCFF",
            edgecolor="none",
            alpha=0.10,
            zorder=1,
        )
    )
    ax.add_patch(
        mpatches.Rectangle(
            (0.0, tw2_lo),
            float(N_COLS),
            float(tw2_hi - tw2_lo),
            facecolor="#CC99FF",
            edgecolor="none",
            alpha=0.10,
            zorder=1,
        )
    )

    # PLP spine seam: x+y = 16 (diagonal chart seam)
    ax.plot([0.0, float(N_COLS)], [float(N_ROWS), 0.0], color="orange", linestyle="--", alpha=0.5, linewidth=2.0)

    ax.text(8.0, -1.2, "PLP_SPINE: x+y=16 (chart seam)", ha="center", va="center", fontsize=11, color="#aa5500")


def render_grid(trajectories: Iterable[Trajectory], *, output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#F8F8F8")

    _draw_background(ax)

    # Color by blood (renderer-only)
    blood_colors = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

    for tr in trajectories:
        pts = tr.pts
        for j in range(len(pts) - 1):
            x1, y1, f1 = pts[j]
            x2, y2, f2 = pts[j + 1]
            if f2 is True:
                ax.plot([x1, x2], [y1, y2], color="black", linestyle=":", linewidth=2.2, alpha=0.9, zorder=10)
            else:
                ax.plot(
                    [x1, x2],
                    [y1, y2],
                    color=blood_colors[tr.blood],
                    alpha=0.18,
                    linewidth=0.8,
                    linestyle="-" if tr.branch == "sunrise" else "--",
                    zorder=5,
                )

    u_scale, u_latent, mis = _universal_field_scale()
    title = (
        "128-TYPE GRID | pure geometry\n"
        f"W7={W7_EXACT:.6f}  H2={H2_W7:.6f}  Spark={SPARK_ANGLE_DEG:.6f}°  Leap={SPARK_LEAP_DIST:.6f}\n"
        f"Δmismatch={mis:.6e}  coupling={u_scale:.6f}  latent={u_latent:.6f}  residue={RESID_DATA_5_32:.6e}\n"
        f"GABA-C(avg)={(GABA_C_R_CAB+GABA_C_R_CA+GABA_C_V_APEX)/3.0:.6f}  debt={TOTAL_DEBT_AREA:.6f}  tunnel={TUNNEL_TENSION:.6f}"
    )
    ax.set_title(title, fontsize=16, pad=20, weight="bold")

    ax.set_xlim(-2.0, float(N_COLS) + 2.0)
    ax.set_ylim(float(N_ROWS) + 2.0, -2.0)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="128_Pure_Geometry_Grid_definitive.png")
    parser.add_argument("--area-override", type=float, default=None)
    parser.add_argument("--target-area", type=float, default=float(W7_EXACT))
    parser.add_argument("--calibrate", action="store_true", help="Solve for area_override to match --target-area.")
    parser.add_argument("--quick", action="store_true", help="Render only representative types (fast).")
    args = parser.parse_args()

    if args.calibrate:
        print("Calibrating hysteresis area...")
        final_area = find_area_for_target(float(args.target_area))
        print(f"Calibration complete. area_override={final_area:.8f}")
    elif args.area_override is not None:
        final_area = float(args.area_override)
        print(f"Using provided area_override={final_area:.8f}")
    else:
        final_area = float(W7_EXACT)
        print(f"Using core area_override=W7_EXACT={final_area:.8f}")

    if args.quick:
        mbti_list = ["ENTJ", "ISFP"]
        blood_list = ["O"]
        gender_list = ["M", "F"]
    else:
        mbti_list = ALL_MBTI
        blood_list = BLOODS
        gender_list = GENDERS

    print("Generating trajectories...")
    trajectories: list[Trajectory] = []
    for mbti in mbti_list:
        for blood in blood_list:
            for gender in gender_list:
                for branch in ("sunrise", "sunset"):
                    pts = generate_trajectory_pure(
                        mbti,
                        blood,
                        gender,
                        branch=branch,
                        area_override=final_area,
                    )
                    trajectories.append(Trajectory(mbti=mbti, blood=blood, gender=gender, branch=branch, pts=pts))

    print("Rendering...")
    render_grid(trajectories, output_path=str(args.output))
    print(f"Saved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
