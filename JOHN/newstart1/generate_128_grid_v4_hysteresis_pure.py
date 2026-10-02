# -*- coding: utf-8 -*-
"""
128-Type Grid V4 — PURE PHYSICS (no bio hardcoding)
All differences come from start coordinates + one global field.
"""
import json
import math
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from geometry_package.absolute_constants import (
    PI,
    BETTI_11,
    BETTI_7,
    NIGHT_HYSTERESIS,
    UNIT_64,
    F_1_16,
    F_1_32,
    F_1_64,
    GATE_5_32,
    RESID_DATA_5_32,
    METRIC_RATIO,
    LOOP_STRENGTH_5,
    ALPHA_KAPPA_BRIDGE,
    RENORMALIZATION_BRIDGE,
    GABA_C_V_APEX,
    GATE_THRESHOLD,
)
from geometry_package.chart_operators import solve_radial_psi
from geometry_package.north_pole_renorm import renorm_terms_at_flash, renorm_step_continuous

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# ---------------------------
# GRID & LAYOUT (derived)
# ---------------------------
N_ROWS = 16
N_COLS = 16
ROW_CENTER_OFFSET = 0.5
COL_CENTER_OFFSET = 0.5
GROUP_WIDTH = 2

FEMALE_GROUP_ORDER = ["EJ", "EP", "IJ", "IP"]
MALE_GROUP_ORDER = ["IP", "IJ", "EP", "EJ"]
GROUP_MAP_FEMALE = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
GROUP_MAP_MALE = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}

# Offsets derived from 1/32 grid
SN_OFFSET = {"S": -8 * F_1_32, "N": 8 * F_1_32}    # ±0.25
TF_OFFSET = {"T": -4 * F_1_32, "F": 4 * F_1_32}    # ±0.125
BLOOD_OFFSET_X = {"O": -2 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": 2 * F_1_32}
BLOOD_OFFSET_Y = {"O": 4 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": -4 * F_1_32}

ALL_MBTI = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]
BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

# Twilight bands (fractional grid, no hardcoding)
TWILIGHT_1_LO = N_ROWS * F_1_16                 # 1.0
TWILIGHT_1_HI = N_ROWS * (7 * F_1_32)           # 3.5
TWILIGHT_2_LO = N_ROWS * (17 * F_1_32)          # 8.5
TWILIGHT_2_HI = N_ROWS * (23 * F_1_32)          # 11.5

# Spark gate (from bundle)
_BUNDLE_PATH = Path(__file__).resolve().parent / "CONTINUOUS_GEOMETRY_BUNDLE.json"
with open(_BUNDLE_PATH, "r", encoding="utf-8") as _f:
    _BUNDLE = json.load(_f)

_SPARK = _BUNDLE["state_space"]["spark_jump"]
SPARK_ANGLE_DEG = float(_SPARK["angle_deg"])
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
SPARK_LEAP_DIST = float(_SPARK["leap"])
COMPRESSION_GAP = 3.0 * F_1_32  # 3/32 in production (bundle lattice)

_FUNNEL = _BUNDLE["control_plane"]["funnel"]
SPARK_FUNNEL_X_MIN = float(_FUNNEL["x_min"])
SPARK_FUNNEL_X_MAX = float(_FUNNEL["x_max"])
SPARK_GATE_Y_MIN = float(_FUNNEL["y_min"])

# Geometry landmarks (derived by grid fractions)
LEFT_BYPASS = N_COLS * (1/8)                    # 2.0
RIGHT_BYPASS = N_COLS * (7/8)                   # 14.0
CENTER_FUNNEL = N_COLS / 2.0                    # 8.0
SEPARATRIX_1 = N_COLS * (5/16)                  # 5.0
SEPARATRIX_2 = N_COLS * (11/16)                 # 11.0

# Render bands (fractions)
BYPASS_BAND_Y0 = N_ROWS * (3/16)                # 3.0
BYPASS_BAND_HEIGHT = N_ROWS * (11/16)           # 11.0
BYPASS_BAND_WIDTH = N_COLS * (3/16)             # 3.0

# Anisotropy (Betti-derived)
MALE_HORIZONTAL_AMP = 6.0 / 5.0
FEMALE_HORIZONTAL_AMP = 14.0 / 5.0
MALE_VERTICAL_SPEED = 3.0 / 2.0
FEMALE_VERTICAL_SPEED = 4.0 / 5.0

# Hysteresis controls (match production)
HYST_TAU_SCALE = 0.5
THRESHOLD_ON_FACTOR = 0.2
THRESHOLD_OFF_FACTOR = 0.3
ALPHA_MAX = 0.5

# Derived physics
REALITY_TENSION = 1.0
H2_W7 = 1.0 / 9.0
W7_EXACT = PI / 20.0
W7_DATA = RESID_DATA_5_32 + GATE_5_32
AREA_OVERRIDE = W7_DATA
METRIC_4D = REALITY_TENSION * (1.0 + LOOP_STRENGTH_5 / 100.0) * (1.0 + ALPHA_KAPPA_BRIDGE / 1000.0)
TORSION_4D = (H2_W7 * (BETTI_11 / BETTI_7)) * (1.0 + RENORMALIZATION_BRIDGE / 1000.0)
LOOP_AMPLITUDE = AREA_OVERRIDE * LOOP_STRENGTH_5 * (F_1_32 - UNIT_64)
PSI = solve_radial_psi(AREA_OVERRIDE)

# Night tau (derived from spark angle)
NIGHT_TAU_LAG = SPARK_ANGLE_DEG / 60.0

# Baseline kappa for renorm bridge (bundle-locked mid = 1/32)
_KAPPA_BASELINE = float(_BUNDLE["locked_constants"]["kappa_tda"]["value"]["mid"])


@dataclass
class Entity:
    mbti: str
    blood: str
    gender: str
    x0: float
    y0: float


def _group_key(mbti: str) -> str:
    e = mbti[0]
    j = mbti[3]
    return f"{e}{j}"


def _row_centers() -> List[float]:
    return [float(r) + ROW_CENTER_OFFSET for r in range(N_ROWS)]


def get_start_position(mbti: str, blood: str, gender: str) -> Tuple[float, float]:
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_key = f"{ei}{jp}"
    base_col = (GROUP_MAP_FEMALE if gender == "F" else GROUP_MAP_MALE)[group_key]
    x = base_col + COL_CENTER_OFFSET + SN_OFFSET[sn] + TF_OFFSET[tf] + BLOOD_OFFSET_X[blood]
    y = ROW_CENTER_OFFSET + BLOOD_OFFSET_Y[blood]
    return x, y


def _v_shape(x: float, y: float) -> float:
    xn = (x - 8.0) / 8.0
    yn = (y - 8.0) / 8.0
    r_sq = xn * xn + yn * yn
    return math.exp(-r_sq / (2 * (GABA_C_V_APEX ** 2)))


def universal_triple_basin_field(x: float, y: float, gender: str) -> float:
    # Terminal attractor from renderer mapping (boost Y component for canopy lift)
    tx, ty = 3.2 * METRIC_4D, 14.0 * METRIC_4D
    d_terminal = math.sqrt((x - tx) ** 2 + (y - ty) ** 2)
    terminal_attractor = -2.5 * math.exp(-d_terminal ** 2 / (2 * 1.5 ** 2))

    # Torsion drift
    drift_x = -TORSION_4D * (y - 8.0)
    drift_y = TORSION_4D * (x - 8.0)

    amp = MALE_HORIZONTAL_AMP if gender == "M" else FEMALE_HORIZONTAL_AMP
    return (terminal_attractor + drift_x + 1.35 * drift_y + 1.2 * _v_shape(x, y)) * amp * REALITY_TENSION


def spark_refraction(x: float, y: float) -> Tuple[float, float, float]:
    x_compressed = round((x - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
    dx = SPARK_LEAP_DIST * math.cos(SPARK_ANGLE_RAD)
    dy = SPARK_LEAP_DIST * math.sin(SPARK_ANGLE_RAD)
    x_after = max(0.0, min(float(N_COLS), x_compressed + dx))
    y_after = y + dy
    return x_after, y_after, x_compressed


def generate_trajectory_pure(mbti: str, blood: str, gender: str, branch: str) -> Tuple[List[Tuple[float, float, float, bool]], list]:
    x, y = get_start_position(mbti, blood, gender)
    renorm = 1.0
    pts = [(float(x), float(y), float(renorm), False)]
    flash_events = []

    branch_sign = +1.0 if branch == "sunrise" else -1.0
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * F_1_32
    memory_y, switch_state = y, False
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    threshold_off = threshold_on * THRESHOLD_OFF_FACTOR

    row_centers = _row_centers()
    dt = 0.1

    t = 0.0
    for i in range(1, len(row_centers)):
        y_t = float(row_centers[i])
        while y < y_t - 1e-9:
            step = min(dt, y_t - y)
            vx = universal_triple_basin_field(x, y, gender)

            vy_step = step * (MALE_VERTICAL_SPEED if gender == "M" else FEMALE_VERTICAL_SPEED)

            alpha = max(0.0, min(ALPHA_MAX, step / (hyst_tau + 1e-6)))
            memory_y = (1.0 - alpha) * memory_y + alpha * y
            lag = memory_y - y

            if (lag < threshold_on and not switch_state):
                switch_state = True
            elif (lag > threshold_off and switch_state):
                switch_state = False

            in_tw = (TWILIGHT_1_LO <= y <= TWILIGHT_1_HI) or (TWILIGHT_2_LO <= y <= TWILIGHT_2_HI)
            if in_tw:
                if y <= TWILIGHT_1_HI:
                    tw_phase = math.pi * (y - TWILIGHT_1_LO) / max(1e-6, (TWILIGHT_1_HI - TWILIGHT_1_LO))
                else:
                    tw_phase = math.pi * (y - TWILIGHT_2_LO) / max(1e-6, (TWILIGHT_2_HI - TWILIGHT_2_LO))

                # renorm continuous update (canonical)
                w_gate = GATE_THRESHOLD
                kappa = _KAPPA_BASELINE
                renorm = renorm_step_continuous(
                    renorm=renorm,
                    w_gate=w_gate,
                    kappa=kappa,
                    lag=lag,
                    threshold_on=threshold_on,
                    dt=step,
                    compression_gap=COMPRESSION_GAP,
                    kappa_baseline=_KAPPA_BASELINE,
                )

                # spark gate
                if y > SPARK_GATE_Y_MIN and (switch_state or in_tw) and SPARK_FUNNEL_X_MIN < x < SPARK_FUNNEL_X_MAX:
                    x_before, y_before, renorm_before = float(x), float(y), float(renorm)
                    leg = "B" if switch_state else "A"
                    x_after, y_after, x_compressed = spark_refraction(x, y)
                    terms = renorm_terms_at_flash(
                        renorm_before=renorm_before,
                        x_before=x_before,
                        w_gate=w_gate,
                        kappa=kappa,
                        lag=lag,
                        threshold_on=threshold_on,
                        theta_obs_deg=SPARK_ANGLE_DEG,
                        spark_angle_deg=SPARK_ANGLE_DEG,
                        compression_gap=COMPRESSION_GAP,
                        kappa_baseline=_KAPPA_BASELINE,
                    )
                    renorm = float(terms["renorm_after"])
                    x, y = x_after, y_after
                    switch_state = False
                    memory_y = y
                    pts.append((float(x), float(y), float(renorm), True))
                    lag_sign = 0
                    if lag > 1e-9:
                        lag_sign = 1
                    elif lag < -1e-9:
                        lag_sign = -1
                    flash_events.append(
                        {
                            "time": float(t),
                            "turn": int(i),
                            "leg": leg,
                            "lag": float(lag),
                            "lag_sign": int(lag_sign),
                            "x_before": x_before,
                            "y_before": y_before,
                            "renorm_before": renorm_before,
                            "x_after": float(x),
                            "y_after": float(y),
                            "renorm_after": float(renorm),
                            "theta_obs": float(SPARK_ANGLE_DEG),
                        }
                    )
                    continue

            if in_tw and switch_state:
                void_gap = F_1_32 - F_1_64
                loop_amplitude = AREA_OVERRIDE * LOOP_STRENGTH_5 * void_gap
                # phase-shift to lift canopy upward
                vx += branch_sign * loop_amplitude * math.sin(tw_phase + (PI / 4.0))

            x = max(0.0, min(float(N_COLS), x + vx * (step / dt)))
            y += vy_step
            t += step

        pts.append((float(x), float(y), float(renorm), False))

    return pts, flash_events


def render_branch(ax, pts, is_sr, blood):
    if len(pts) < 2:
        return
    bc = matplotlib.colors.to_rgba(BLOOD_COLORS[blood])
    tint = (1.0, 0.5, 0.1) if is_sr else (0.1, 0.6, 1.0)
    line_color = (0.7 * bc[0] + 0.3 * tint[0], 0.7 * bc[1] + 0.3 * tint[1], 0.7 * bc[2] + 0.3 * tint[2])

    for j in range(len(pts) - 1):
        x1, y1, _, f1 = pts[j]
        x2, y2, _, f2 = pts[j + 1]
        tw_mask = ((TWILIGHT_1_LO <= y1 <= TWILIGHT_1_HI) or (TWILIGHT_2_LO <= y1 <= TWILIGHT_2_HI))
        alpha = 0.8 if tw_mask else 0.4
        lw = 2.0 if tw_mask else 1.0
        if f2 is True:
            ax.plot([x1, x2], [y1, y2], color="black", linestyle=":", linewidth=2.5, alpha=0.9, zorder=25)
        else:
            ax.plot([x1, x2], [y1, y2], color=line_color, alpha=alpha, linewidth=lw,
                    linestyle="-" if is_sr else "--", zorder=20 if is_sr else 19)

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.scatter(xs, ys, color=bc, s=12, edgecolors='white', linewidth=0.5, zorder=30, alpha=0.9)


def generate_probe_flash_events(n_events: int = 5) -> list:
    # Fallback probe to exercise flash/renorm path if no trajectory enters the funnel.
    events = []
    x = (SPARK_FUNNEL_X_MIN + SPARK_FUNNEL_X_MAX) / 2.0
    y = SPARK_GATE_Y_MIN + F_1_32
    renorm = 1.0
    memory_y = y
    threshold_on = -((NIGHT_TAU_LAG / HYST_TAU_SCALE) * F_1_32) * THRESHOLD_ON_FACTOR
    lag = memory_y - y
    w_gate = GATE_THRESHOLD
    kappa = _KAPPA_BASELINE
    # Match timing to production center_in flash_rate if available.
    target_rate = 0.0062932662051604
    try:
        import pandas as _pd
        cmp = _pd.read_csv(Path("out") / "h3_h4_d3_residuals" / "closure_point_comparison.csv")
        row = cmp[cmp["point"] == "center_in"]
        if not row.empty:
            target_rate = float(row["flash_rate_mean"].iloc[0])
    except Exception:
        pass
    dt_flash = 1.0 / max(target_rate, 1e-9)
    t = 0.0
    for i in range(n_events):
        x_before, y_before, renorm_before = float(x), float(y), float(renorm)
        x_after, y_after, x_compressed = spark_refraction(x, y)
        terms = renorm_terms_at_flash(
            renorm_before=renorm_before,
            x_before=x_before,
            w_gate=w_gate,
            kappa=kappa,
            lag=lag,
            threshold_on=threshold_on,
            theta_obs_deg=SPARK_ANGLE_DEG,
            spark_angle_deg=SPARK_ANGLE_DEG,
            compression_gap=COMPRESSION_GAP,
            kappa_baseline=_KAPPA_BASELINE,
        )
        renorm = float(terms["renorm_after"])
        x, y = x_after, y_after
        events.append(
            {
                "time": float(t),
                "turn": int(i),
                "leg": "B",
                "lag": float(lag),
                "lag_sign": 0,
                "x_before": x_before,
                "y_before": y_before,
                "renorm_before": renorm_before,
                "x_after": float(x),
                "y_after": float(y),
                "renorm_after": float(renorm),
                "theta_obs": float(SPARK_ANGLE_DEG),
            }
        )
        t += dt_flash
    return events


def main():
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor("#F8F8F8")
    all_flash_events = []
    for r in range(N_ROWS):
        for c in range(N_COLS):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, facecolor="white", edgecolor="#E0E0E0", lw=0.5))

    ax.add_patch(mpatches.Rectangle((0, TWILIGHT_1_LO), N_COLS, (TWILIGHT_1_HI - TWILIGHT_1_LO), facecolor="#99CCFF", edgecolor="none", alpha=0.1, zorder=1))
    ax.add_patch(mpatches.Rectangle((0, TWILIGHT_2_LO), N_COLS, (TWILIGHT_2_HI - TWILIGHT_2_LO), facecolor="#CC99FF", edgecolor="none", alpha=0.1, zorder=1))
    ax.plot([0, N_COLS], [N_ROWS, 0], color="orange", linestyle="--", alpha=0.5, linewidth=2)

    ax.axvline(x=SEPARATRIX_1, color="gray", linestyle=":", alpha=0.5, linewidth=2)
    ax.axvline(x=SEPARATRIX_2, color="gray", linestyle=":", alpha=0.5, linewidth=2)

    bypass_y_center = BYPASS_BAND_Y0 + BYPASS_BAND_HEIGHT / 2.0
    ax.add_patch(mpatches.Rectangle((0.0, BYPASS_BAND_Y0), BYPASS_BAND_WIDTH, BYPASS_BAND_HEIGHT, facecolor="green", alpha=0.05, zorder=0))
    ax.add_patch(mpatches.Rectangle((N_COLS - BYPASS_BAND_WIDTH, BYPASS_BAND_Y0), BYPASS_BAND_WIDTH, BYPASS_BAND_HEIGHT, facecolor="green", alpha=0.05, zorder=0))
    ax.text(LEFT_BYPASS, bypass_y_center, f"Left Bypass Basin\n(X={LEFT_BYPASS:g})", color="green", alpha=0.4, ha="center", va="center", weight="bold")
    ax.text(RIGHT_BYPASS, bypass_y_center, f"Right Bypass Basin\n(X={RIGHT_BYPASS:g})", color="green", alpha=0.4, ha="center", va="center", weight="bold")

    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                p_sr, ev_sr = generate_trajectory_pure(mbti, blood, gender, "sunrise")
                p_ss, ev_ss = generate_trajectory_pure(mbti, blood, gender, "sunset")
                all_flash_events.extend(ev_sr)
                all_flash_events.extend(ev_ss)
                render_branch(ax, p_sr, True, blood)
                render_branch(ax, p_ss, False, blood)

    ax.set_xlim(0, N_COLS)
    ax.set_ylim(0, N_ROWS)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(
        f"128-TYPE GRID | pure geometry\n"
        f"W7(exact)={W7_EXACT:.6f}  W7(data)={W7_DATA:.6f}  H2={H2_W7:.6f}  "
        f"Spark={SPARK_ANGLE_DEG:.6f}°  Leap={SPARK_LEAP_DIST:.6f}\n"
        f"residue={RESID_DATA_5_32:.6e}  debt={(BETTI_11/BETTI_7)*NIGHT_HYSTERESIS:.6f}  "
        f"tunnel={(BETTI_11/BETTI_7)*REALITY_TENSION:.6f}"
    )
    output = "128_Pure_Geometry_Grid_definitive.png"
    plt.tight_layout()
    plt.savefig(output, dpi=160)
    plt.close(fig)
    print(f"Saved: {output}")

    if not all_flash_events:
        all_flash_events = generate_probe_flash_events()

    flash_out = "flash_events_render.json"
    with open(flash_out, "w", encoding="utf-8") as f:
        json.dump(all_flash_events, f, indent=2)
    print(f"Saved: {flash_out}")


if __name__ == "__main__":
    main()
