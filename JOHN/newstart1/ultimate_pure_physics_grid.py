# -*- coding: utf-8 -*-
"""
ULTIMATE 128-Type Grid - PURE GEOMETRY ENGINE
This script generates the definitive 128-type grid based on the user's core intuition.
- It uses the exact starting positions for each type group as specified.
- It applies the universal, unmodified physics laws to generate trajectories.
- All hardcoded values and logic are designed to match the user's provided images and schema.
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json
import os

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# --- Core Constants (Derived from 128GIRD_MBTI_PHYSICS.py) ---
# These are the universal constants and should not be modified.
CONST = {
    "w5": 5.555492104,
    "w7": 0.15697685963482133,
    "male_horizontal_amp": 1.2,
    "female_horizontal_amp": 2.8,
    "male_vertical_speed": 1.5,
    "female_vertical_speed": 0.8,
    "n_rows": 16,
    "n_cols": 16,
    "row_center_offset": 0.5,
    "col_center_offset": 0.5,
    "dt": 0.1,
    "reality_tension": 1.0100375,
    "metric_4d": 1.0661,
    "torsion_4d": 0.1746,
    "twilight_1_lo": 1.0,
    "twilight_1_hi": 3.5,
    "twilight_2_lo": 8.5,
    "twilight_2_hi": 11.5,
}

ALL_MBTI = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
            "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]
BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

# --- USER INTUITION: STARTING POSITIONS ---
# This section explicitly implements the starting grid from the user's spreadsheet image.
# These are the *exact* starting points and are not subject to other physics.

def get_start_position(mbti: str, blood: str, gender: str):
    """
    Returns the exact starting (x, y) coordinate based on the user's specified grid.
    This logic overrides all other start position calculations.
    """
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_key = f"{ei}{jp}"

    # Base coordinates from user's spreadsheet layout
    start_positions = {
        # WOMEN (Left Side)
        "F_EJ": (1, 15), "F_EP": (3, 15), "F_IJ": (5, 15), "F_IP": (7, 15),
        # MEN (Right Side)
        "M_IP": (9, 15), "M_IJ": (11, 15), "M_EP": (13, 15), "M_EJ": (15, 15),
    }

    key = f"{gender}_{group_key}"
    base_x, base_y = start_positions[key]

    # Micro-offsets for visual separation (from 128GIRD_MBTI_PHYSICS)
    sn_offset = {"S": -0.25, "N": 0.25}[sn]
    tf_offset = {"T": -0.125, "F": 0.125}[tf]
    blood_offset_x = {"O": -0.1, "A": 0.1, "B": -0.1, "AB": 0.1}[blood]

    # Apply offsets to the base position
    x = base_x + sn_offset + tf_offset + blood_offset_x
    y = base_y # Y starts at the top row for all

    return x, y

# --- UNIVERSAL PHYSICS FIELD ---
# This is the unmodified physics engine from 128GIRD_MBTI_PHYSICS.py.

def universal_physical_mbti_field(x, y, mbti, gender):
    """
    4D DETERMINISTIC CIRCUIT FIELD. This is the universal law.
    """
    e_i, s_n, t_f, j_p = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # 1. Base Torsion & Tension
    drift_x = -CONST["torsion_4d"] * (y - 8.0)
    
    # T vs F: ACh Truth Logic (T) straightens, Serotonin Buffer (F) yields
    drift_x *= 0.3 if t_f == 'T' else 1.3
        
    # 2. Alpha-2 Adrenergic Margins (S vs N)
    alpha2_left, alpha2_right = 6.0, 10.0
    damp_l = np.exp(-((x - alpha2_left)**2) / 0.8)
    damp_r = np.exp(-((x - alpha2_right)**2) / 0.8)
    if gender == "M": damp_r *= 1.5 
        
    if s_n == "S":
        margin_resistance = max(0.1, 1.0 - (damp_l * 0.8) - (damp_r * 0.8))
        pull_to_margin_x = 0.0
        if abs(x - alpha2_left) < 2.0: pull_to_margin_x = (alpha2_left - x) * 0.5
        elif abs(x - alpha2_right) < 2.0: pull_to_margin_x = (alpha2_right - x) * 0.5
        vx = (drift_x + pull_to_margin_x) * margin_resistance
    else:
        vx = drift_x * 1.5
        
    # 3. J vs P: GABA-B Fixation vs GABA-A Spiral
    if j_p == "J":
        target_x = 16.0 - y
        vx += (target_x - x) * 0.05
    else:
        vx += np.sign(x - 8.0) * 0.1
        
    # 4. Melatonin Smoothing
    dist_nose = abs(x - 8.0)
    smoothing = np.exp(-(dist_nose**2) / 0.083)
    vx *= (1.0 - smoothing)
    
    # 5. Gender & E/I Anisotropy
    amp = CONST["male_horizontal_amp"] if gender == "M" else CONST["female_horizontal_amp"]
    if e_i == "I": amp *= 0.6
        
    # 6. Terminal Attractors
    tx_l, ty_l = 3.2 * CONST["metric_4d"], 11.2 * CONST["metric_4d"]
    term_attr_l = -2.5 * np.exp(-((x - tx_l)**2 + (y - ty_l)**2) / (2 * 1.5**2))
    tx_r, ty_r = (16.0 - 3.2) * CONST["metric_4d"], 11.2 * CONST["metric_4d"]
    term_attr_r = -2.5 * np.exp(-((x - tx_r)**2 + (y - ty_r)**2) / (2 * 1.5**2))
    
    vx_final = (vx + term_attr_l + term_attr_r) * amp * CONST["reality_tension"]
    return vx_final

# --- TRAJECTORY GENERATION ---

def generate_trajectory(mbti, blood, gender):
    x, y = get_start_position(mbti, blood, gender)
    pts = [(x, y)]
    
    row_centers = [r + CONST["row_center_offset"] for r in range(CONST["n_rows"])][::-1] # Top to bottom
    
    for i in range(len(row_centers) - 1):
        y_t = row_centers[i+1]
        while y > y_t + 1e-9:
            step = min(CONST["dt"], y - y_t)
            vx = universal_physical_mbti_field(x, y, mbti, gender)
            vy_step = -step * (CONST["male_vertical_speed"] if gender == "M" else CONST["female_vertical_speed"])
            
            x = max(0.0, min(float(CONST["n_cols"]), x + vx * (step / CONST["dt"])))
            y += vy_step
        
        pts.append((x, y_t))
    return pts

# --- MAIN & RENDERING ---

def main():
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#F0F0F0")
    ax.set_facecolor("#FFFFFF")

    # Grid and bands
    for r in range(CONST["n_rows"]):
        for c in range(CONST["n_cols"]):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, facecolor="white", edgecolor="#E0E0E0", lw=0.5))
    ax.add_patch(mpatches.Rectangle((0, CONST["twilight_1_lo"]), CONST["n_cols"], (CONST["twilight_1_hi"] - CONST["twilight_1_lo"]), facecolor="#E3F2FD", edgecolor="none", alpha=0.6, zorder=0))
    ax.add_patch(mpatches.Rectangle((0, CONST["twilight_2_lo"]), CONST["n_cols"], (CONST["twilight_2_hi"] - CONST["twilight_2_lo"]), facecolor="#F3E5F5", edgecolor="none", alpha=0.6, zorder=0))

    # Generate and plot all trajectories
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                pts = generate_trajectory(mbti, blood, gender)
                xs, ys = zip(*pts)
                ax.plot(xs, ys, color=BLOOD_COLORS[blood], alpha=0.6, linewidth=1.5)
                ax.scatter([xs[0]], [ys[0]], color=BLOOD_COLORS[blood], s=20, zorder=10)

    # Final plot setup
    ax.set_xlim(0, CONST["n_cols"])
    ax.set_ylim(0, CONST["n_rows"])
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("ULTIMATE 128-TYPE GRID | User Intuition & Pure Physics", fontsize=24, pad=20)
    
    output_filename = "ultimate_pure_physics_grid.png"
    plt.tight_layout()
    plt.savefig(output_filename, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved definitive grid to: {output_filename}")

if __name__ == "__main__":
    main()
