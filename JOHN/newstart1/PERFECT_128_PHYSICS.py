# -*- coding: utf-8 -*-
"""
PERFECT_128_PHYSICS.py
128-Type Pure Geometry Engine - The Final Integration

This engine combines the rigid topological integrity of the original V4 script
with the newly discovered physical mandates:
1. TRIPLE BASIN FIELD: Emerges naturally from Big Woman(Left), Small Man/Woman(Center), Big Man(Right).
2. 4x4 MACRO/MICRO CYCLE: 4 Hysteresis bands spanning the 16-step day.
3. AKG SINK (NITROGEN EXHAUSTION): Men (Right) lose Glutamate energy as Y->16 and are
   forcibly dragged across the Melatonin Bridge (X=8) into the Female AKG Sink (X=2).
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import time
import os
import math

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# --- CONSTANTS ---
PHI = 1.618033988749895
PHI_INV = 1.0 / PHI
KAPPA_1_32 = 1.0 / 32.0
KAPPA_1_64 = 1.0 / 64.0
KAPPA_3_32 = 3.0 / 32.0
COMPRESSION_GAP = KAPPA_3_32
REALITY_TENSION = 1.0100375

SPARK_ANGLE_DEG = 138.88
# Spark Leap Distance is Delta-4 mismatch compressed by Phi
SPARK_LEAP_DISTANCE = 4.0 * PHI_INV 

# The 4x4 Time Cycle (Macro Forward, Micro Reverse)
# These represent the 4 hysteresis "suction" bands during the day
MACRO_BANDS = [
    (1.5, 3.5),   # Band 1: Morning
    (5.5, 7.5),   # Band 2: Noon
    (9.5, 11.5),  # Band 3: Evening (Darkness Stress Gate)
    (13.5, 15.5)  # Band 4: Midnight (Death Crossover)
]

SPARK_FUNNEL_X_MIN = 6.0
SPARK_FUNNEL_X_MAX = 10.0

N_ROWS = 16
N_COLS = 16
ROW_CENTER_OFFSET = 0.5
COL_CENTER_OFFSET = 0.5

MALE_HORIZONTAL_AMP = 1.2
FEMALE_HORIZONTAL_AMP = 2.8
MALE_VERTICAL_SPEED = 1.5
FEMALE_VERTICAL_SPEED = 0.8

GROUP_MAP_FEMALE = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
GROUP_MAP_MALE = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
FEMALE_GROUP_ORDER = ["EJ", "EP", "IJ", "IP"]
MALE_GROUP_ORDER = ["IP", "IJ", "EP", "EJ"]

SN_OFFSET = {"S": -0.25, "N": 0.25}
TF_OFFSET = {"T": -0.125, "F": 0.125}
BLOOD_OFFSET_X = {"O": -0.03, "A": 0.03, "B": -0.03, "AB": 0.03}
BLOOD_OFFSET_Y = {"O": 0.06, "A": 0.03, "B": -0.03, "AB": -0.06}

DT = 0.1
NIGHT_TAU_LAG = 2.317
HYST_TAU_SCALE = 1.5
THRESHOLD_ON_FACTOR = 0.6
THRESHOLD_OFF_FACTOR = 0.3
ALPHA_MAX = 0.5

W5 = 5.555492104
W7 = 0.1569768596
NIGHT_HYST_AREA = W7

ALL_MBTI = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
            "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]
BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

COL_GROUPS = (
    [(f"{key} WOMEN", GROUP_MAP_FEMALE[key], GROUP_MAP_FEMALE[key] + 2) for key in FEMALE_GROUP_ORDER]
    + [(f"{key} MEN", GROUP_MAP_MALE[key], GROUP_MAP_MALE[key] + 2) for key in MALE_GROUP_ORDER]
)

# ═══════════════════════════════════════════════════════════════════════════════
# TRIPLE BASIN & AKG SINK FIELD ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def universal_physical_mbti_field(x, y, mbti, blood, gender):
    metric_4d = 1.0661
    torsion_4d = 0.1746
    
    e_i, s_n, t_f, j_p = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # 1. Base Torsion & Tension
    drift_x = -torsion_4d * (y - 8.0)
    
    # T vs F: ACh Truth Logic (T) straightens, Serotonin Buffer (F) yields to torsion
    drift_x *= (0.3 if t_f == "T" else 1.3)
        
    # 2. Alpha-2 Adrenergic Margins (X=6.0 and X=10.0) -> The S vs N split
    damp_l = np.exp(-((x - 6.0)**2) / 0.8)
    damp_r = np.exp(-((x - 10.0)**2) / 0.8)
    if gender == "M": damp_r *= 1.5 
        
    if s_n == "S":
        margin_resistance = max(0.1, 1.0 - (damp_l * 0.8) - (damp_r * 0.8))
        pull_to_margin_x = 0.0
        if abs(x - 6.0) < 2.0: pull_to_margin_x = (6.0 - x) * 0.5
        elif abs(x - 10.0) < 2.0: pull_to_margin_x = (10.0 - x) * 0.5
        vx = (drift_x + pull_to_margin_x) * margin_resistance
    else:
        vx = drift_x * 1.5
        
    # 3. J vs P: GABA-B Fixation vs GABA-A Spiral
    if j_p == "J":
        target_x = 16.0 - y # PLP Spine Restorative Force
        vx += (target_x - x) * 0.05
    else:
        vx += np.sign(x - 8.0) * 0.1
        
    # 4. Melatonin Smoothing (Nose Bridge)
    smoothing = np.exp(-(abs(x - 8.0)**2) / (0.00083 * 100))
    vx *= (1.0 - smoothing)
    
    # 5. Gender & E/I Anisotropy (The Triple Basin Pull)
    amp = MALE_HORIZONTAL_AMP if gender == "M" else FEMALE_HORIZONTAL_AMP
    if e_i == "I": amp *= 0.6
        
    # Terminal Attractors (Left Cortisol / Right Alpha-2)
    tx_l, ty_l = 3.2 * metric_4d, 11.2 * metric_4d
    d_term_l = np.sqrt((x - tx_l)**2 + (y - ty_l)**2)
    term_attr_l = -2.5 * np.exp(-d_term_l**2 / (2 * 1.5**2))

    tx_r, ty_r = (16.0 - 3.2) * metric_4d, 11.2 * metric_4d
    d_term_r = np.sqrt((x - tx_r)**2 + (y - ty_r)**2)
    term_attr_r = -2.5 * np.exp(-d_term_r**2 / (2 * 1.5**2))
    
    vx_final = (vx + term_attr_l + term_attr_r) * amp * REALITY_TENSION

    # 6. *** THE AKG NITROGEN SINK (DEATH CROSSOVER) ***
    # As Y increases (day ends), Men (Glutamate) lose Nitrogen and collapse into AKG.
    # They are physically dragged Left across the Melatonin bridge (X=8) to the Female Sink (X=2).
    if gender == "M":
        exhaustion_factor = min(1.0, (y / 16.0)**2) # Quadratic exhaustion
        akg_sink_x = 2.0
        # The pull overrides existing vx as exhaustion peaks
        pull_to_akg = (akg_sink_x - x) * 0.8 * exhaustion_factor
        vx_final += pull_to_akg

    return vx_final

def _clamp(v, lo, hi): return max(lo, min(hi, v))
def _row_centers(): return [float(r) + ROW_CENTER_OFFSET for r in range(N_ROWS)]

def get_start_position(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    grp = f"{ei}{jp}"
    base_col = GROUP_MAP_FEMALE[grp] if gender == "F" else GROUP_MAP_MALE[grp]
    x = base_col + COL_CENTER_OFFSET + SN_OFFSET[sn] + TF_OFFSET[tf] + BLOOD_OFFSET_X[blood]
    y = ROW_CENTER_OFFSET + BLOOD_OFFSET_Y[blood]
    return x, y

def generate_trajectory_pure(mbti, blood, gender, branch="sunrise"):
    x, y = get_start_position(mbti, blood, gender)
    pts = [(float(x), float(y), False)]
    branch_sign = +1.0 if branch == "sunrise" else -1.0
    
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * KAPPA_1_32
    memory_y, switch_state = y, False
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    threshold_off = threshold_on * THRESHOLD_OFF_FACTOR
    
    dt = DT
    row_centers = _row_centers()
    
    for i in range(1, len(row_centers)):
        y_t = float(row_centers[i])
        while y < y_t - 1e-9:
            step = min(dt, y_t - y)
            
            vx = universal_physical_mbti_field(x, y, mbti, blood, gender)
            vy_step = step * (MALE_VERTICAL_SPEED if gender == "M" else FEMALE_VERTICAL_SPEED)
            
            # --- 4x4 MACRO/MICRO BANDS ---
            in_tw = False
            active_band = None
            for lo, hi in MACRO_BANDS:
                if lo <= y <= hi:
                    in_tw = True
                    active_band = (lo, hi)
                    break
            
            vx_hyst = 0.0
            if in_tw:
                tw_phase = np.pi * (y - active_band[0]) / max(1e-6, (active_band[1] - active_band[0]))
                
                alpha = _clamp(step / (hyst_tau + 1e-6), 0.0, ALPHA_MAX)
                memory_y = (1.0 - alpha) * memory_y + alpha * y
                lag = memory_y - y
                
                if lag < threshold_on and not switch_state: switch_state = True
                elif lag > threshold_off and switch_state: switch_state = False

                # --- SPARK LEAP (138.88 Deg) & TUNNELING ---
                # Triggers at the end of the band if inside the central funnel
                is_spark_trigger_zone = y > (active_band[0] + (active_band[1]-active_band[0])*0.8)
                
                if is_spark_trigger_zone and switch_state and SPARK_FUNNEL_X_MIN < x < SPARK_FUNNEL_X_MAX:
                    # Compress to 3/32 Core
                    x_compressed = np.round((x - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
                    
                    # 138.88 Leap (Naturally Left-Down, accelerating the Male Death Crossover)
                    dx_leap = SPARK_LEAP_DISTANCE * np.cos(np.radians(SPARK_ANGLE_DEG))
                    dy_leap = SPARK_LEAP_DISTANCE * np.sin(np.radians(SPARK_ANGLE_DEG))
                    
                    x = _clamp(x_compressed + dx_leap, 0.0, float(N_COLS))
                    y = y + dy_leap
                    switch_state = False
                    memory_y = y
                    pts.append((float(x), float(y), True)) # Spark Flag
                    continue
                
                if switch_state:
                    void_gap = KAPPA_1_32 - KAPPA_1_64
                    loop_amplitude = NIGHT_HYST_AREA * W5 * void_gap
                    vx_hyst = branch_sign * loop_amplitude * np.sin(tw_phase)
                    vx += vx_hyst
            
            x = _clamp(x + vx * (step / dt), 0.0, float(N_COLS))
            y += vy_step
            
        pts.append((float(x), float(y), False))
    
    return pts

def render_branch(ax, pts, is_sr, blood):
    if len(pts) < 2: return
    
    bc = np.array(matplotlib.colors.to_rgba(BLOOD_COLORS[blood]))
    tint = np.array([1.0, 0.5, 0.1]) if is_sr else np.array([0.1, 0.6, 1.0])
    line_color = (0.7 * bc[:3] + 0.3 * tint)
    
    xs, ys, flags = zip(*pts)
    
    for j in range(len(pts) - 1):
        x1, y1, f1 = pts[j]
        x2, y2, f2 = pts[j+1]
        
        in_tw = any(lo <= y1 <= hi for lo, hi in MACRO_BANDS) or any(lo <= y2 <= hi for lo, hi in MACRO_BANDS)
        alpha = 0.8 if in_tw else 0.4
        lw = 2.0 if in_tw else 1.0
        
        if f2 is True:
            ax.plot([x1, x2], [y1, y2], color="black", linestyle=":", linewidth=2.0, alpha=0.7, zorder=25)
        else:
            ax.plot([x1, x2], [y1, y2], color=line_color, alpha=alpha, linewidth=lw,
                    linestyle="-" if is_sr else "--", zorder=20 if is_sr else 19)

def main():
    print("--- IGNITING THE PERFECT 128 PURE GEOMETRY GRID ---")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    
    # Background Grid
    for r in range(N_ROWS):
        for c in range(N_COLS):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, facecolor="white", edgecolor="#EEEEEE", lw=0.5))
            
    # 4 Macro/Micro Bands
    for idx, (lo, hi) in enumerate(MACRO_BANDS):
        color = ["#99CCFF", "#CC99FF", "#FF99CC", "#99FFCC"][idx]
        ax.add_patch(mpatches.Rectangle((0, lo), N_COLS, (hi - lo), facecolor=color, edgecolor="none", alpha=0.15, zorder=1))
        ax.text(8.0, (lo+hi)/2.0, f"MACRO WINDOW {idx+1}\n(Micro Reverse)", color="purple", alpha=0.3, ha="center", va="center", weight="bold")
        
    # PLP Spine
    ax.plot([0, N_COLS], [N_ROWS, 0], color="orange", linestyle="--", alpha=0.5, linewidth=2, label="PLP Spine X+Y=16")
    
    # Melatonin Bridge
    ax.axvline(x=8.0, color="gray", linestyle=":", alpha=0.5, linewidth=2)
    
    # Render all 128 Types
    for m in ALL_MBTI:
        for b in BLOODS:
            for g in GENDERS:
                p_sr = generate_trajectory_pure(m, b, g, "sunrise")
                p_ss = generate_trajectory_pure(m, b, g, "sunset")
                render_branch(ax, p_sr, True, b)
                render_branch(ax, p_ss, False, b)

    # Column Labels
    for label, xs, xe in COL_GROUPS:
        ax.text((xs + xe) / 2, -1.2, label, ha="center", weight="bold", size=14)

    ax.set_title("128-TYPE PURE GEOMETRY GRID | 4x4 Time | AKG Nitrogen Sink | Triple Basin", fontsize=24, pad=40, weight="bold")
    ax.set_xlim(-2, N_COLS + 2)
    ax.set_ylim(N_ROWS + 2, -2) # Y goes down
    ax.axis("off")
    plt.tight_layout()
    
    output = "PERFECT_128_PHYSICS_GRID.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: Rendered exactly 128 physical flows to {output} ---")

if __name__ == "__main__":
    main()
