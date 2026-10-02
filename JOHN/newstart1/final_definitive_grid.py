# -*- coding: utf-8 -*-
"""
FINAL DEFINITIVE 128-Type Grid Generator
This script generates the one true grid based on the user's core intuition and the latest universal physics.
- It uses the exact starting positions for each type group as specified by the user.
- It correctly implements the 2D vector field using the latest physics for both vx and vy.
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# --- LATEST UNIVERSAL CONSTANTS ---
# From generate_128_grid_v4_hysteresis_pure.py. These are not to be modified.
N_ROWS, N_COLS = 16, 16
REALITY_TENSION = 1.0
METRIC_4D = 1.0661
TORSION_4D = 0.1746
GABA_C_V_APEX = 0.85
MALE_HORIZONTAL_AMP = 6.0 / 5.0
FEMALE_HORIZONTAL_AMP = 14.0 / 5.0
MALE_VERTICAL_SPEED = 3.0 / 2.0
FEMALE_VERTICAL_SPEED = 4.0 / 5.0
DT = 0.1

ALL_MBTI = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
            "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]
BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

# --- USER INTUITION: EXACT STARTING POSITIONS ---
def get_start_position(mbti: str, blood: str, gender: str):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_key = f"{ei}{jp}"

    start_positions = {
        "F_EJ": (1.5, 15.5), "F_EP": (3.5, 15.5), "F_IJ": (5.5, 15.5), "F_IP": (7.5, 15.5),
        "M_IP": (8.5, 15.5), "M_IJ": (10.5, 15.5), "M_EP": (12.5, 15.5), "M_EJ": (14.5, 15.5),
    }

    key = f"{gender}_{group_key}"
    base_x, base_y = start_positions[key]

    sn_offset = {"S": -0.25, "N": 0.25}[sn]
    tf_offset = {"T": -0.125, "F": 0.125}[tf]
    blood_offset_x = {"O": -0.05, "A": 0.05, "B": -0.05, "AB": 0.05}[blood]

    x = base_x + sn_offset + tf_offset + blood_offset_x
    y = base_y
    return x, y

# --- LATEST UNIVERSAL PHYSICS FIELD (Correct 2D Implementation) ---
def _v_shape(x: float, y: float) -> float:
    xn = (x - 8.0) / 8.0
    yn = (y - 8.0) / 8.0
    r_sq = xn * xn + yn * yn
    return math.exp(-r_sq / (2 * (GABA_C_V_APEX ** 2)))

def get_velocity(x: float, y: float, gender: str) -> tuple[float, float]:
    """Returns the (vx, vy) vector using the latest universal physics.
    vx is from universal_triple_basin_field, vy is from vertical speed constants.
    """
    # Calculate vx (Horizontal Velocity)
    tx, ty = 3.2 * METRIC_4D, 14.0 * METRIC_4D
    d_terminal = math.sqrt((x - tx) ** 2 + (y - ty) ** 2)
    terminal_attractor = -2.5 * math.exp(-d_terminal ** 2 / (2 * 1.5 ** 2))
    drift_x = -TORSION_4D * (y - 8.0)
    drift_y = TORSION_4D * (x - 8.0)
    amp = MALE_HORIZONTAL_AMP if gender == "M" else FEMALE_HORIZONTAL_AMP
    vx = (terminal_attractor + drift_x + 1.35 * drift_y + 1.2 * _v_shape(x, y)) * amp * REALITY_TENSION

    # Calculate vy (Vertical Velocity)
    vy = -1 * (MALE_VERTICAL_SPEED if gender == "M" else FEMALE_VERTICAL_SPEED)

    return vx, vy

# --- TRAJECTORY GENERATION ---
def generate_trajectory(mbti, blood, gender):
    x, y = get_start_position(mbti, blood, gender)
    pts = [(x, y)]
    
    num_steps = 200
    for _ in range(num_steps):
        if y < 0.1: break
        vx, vy = get_velocity(x, y, gender)
        
        x_new = x + vx * DT
        y_new = y + vy * DT
        
        x = max(0.0, min(float(N_COLS), x_new))
        y = y_new
        pts.append((x, y))
    return pts

# --- MAIN & RENDERING ---
def main():
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#F8F8F8")
    ax.set_facecolor("#FFFFFF")

    for r in range(N_ROWS):
        for c in range(N_COLS):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, facecolor="white", edgecolor="#EAEAEA", lw=0.5))
    ax.add_patch(mpatches.Rectangle((0, 1.0), N_COLS, 2.5, facecolor="#E3F2FD", edgecolor="none", alpha=0.5, zorder=0))
    ax.add_patch(mpatches.Rectangle((0, 8.5), N_COLS, 3.0, facecolor="#F3E5F5", edgecolor="none", alpha=0.5, zorder=0))

    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                pts = generate_trajectory(mbti, blood, gender)
                xs, ys = zip(*pts)
                ax.plot(xs, ys, color=BLOOD_COLORS[blood], alpha=0.7, linewidth=1.8)
                ax.scatter([xs[0]], [ys[0]], color=BLOOD_COLORS[blood], s=25, zorder=10, edgecolor='white', linewidth=0.5)

    ax.set_xlim(0, N_COLS)
    ax.set_ylim(0, N_ROWS)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("FINAL DEFINITIVE 128-TYPE GRID | User Intuition + Latest Universal Physics", fontsize=24, pad=20)
    
    output_filename = "final_definitive_grid.png"
    plt.tight_layout()
    plt.savefig(output_filename, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved the FINAL definitive grid to: {output_filename}")

if __name__ == "__main__":
    main()
