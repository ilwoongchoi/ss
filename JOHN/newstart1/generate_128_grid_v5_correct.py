# -*- coding: utf-8 -*-
"""
128-Type Grid V5 — CORRECT DISCRETE GRID (Not Complex Plane Fractal)

Based on V4 pattern:
- 16x16 Grid layout (not complex plane trajectories)
- Female Left [0,8], Male Right [8,16]
- Y-axis = Time Windows (16 steps)
- Discrete scatter + line connections (sharp vectors, not fluid)
- Spark leap = heavy black dotted line

Axiom: z_{n+1} = z_n^2 + c + G(z_n, t) with seed c = exp(i·138.88°)
"""

import json
import math
from pathlib import Path
from typing import List, Tuple, Dict
from dataclasses import dataclass

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# =============================================================================
# 1. CONSTANTS & AXIOMS (From Observer Derivation)
# =============================================================================

PI = math.pi
PHI = (1 + math.sqrt(5)) / 2
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
GOLDEN_ANGLE_DEG = 137.507764
GAP_DEG = SPARK_ANGLE_DEG - GOLDEN_ANGLE_DEG  # 1.372236...
CHIRALITY = 1.0 / 18.0
UNIVERSAL_DRIFT = GAP_DEG * CHIRALITY  # ~0.0762

# Grid Layout
N_ROWS = 16
N_COLS = 16

# Grid fractions
F_1_32 = 1.0 / 32.0
F_1_16 = 1.0 / 16.0

# Group mappings (Female/Male opposite)
FEMALE_GROUP_ORDER = ["EJ", "EP", "IJ", "IP"]
MALE_GROUP_ORDER = ["IP", "IJ", "EP", "EJ"]
GROUP_MAP_FEMALE = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
GROUP_MAP_MALE = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}

# Offsets (1/32 grid units)
SN_OFFSET = {"S": -8 * F_1_32, "N": 8 * F_1_32}      # ±0.25
TF_OFFSET = {"T": -4 * F_1_32, "F": 4 * F_1_32}      # ±0.125
BLOOD_OFFSET_X = {"O": -2 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": 2 * F_1_32}
BLOOD_OFFSET_Y = {"O": 4 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": -4 * F_1_32}

# Blood colors
BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

# MBTI list
ALL_MBTI = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]

# Physics Coefficients for G operator
COULOMB_K = 0.5
WEAK_G = 0.1
GATE_5_32 = 5.0 / 32.0
HYSTERESIS_MEM = 0.8

# Seed c (from axiom)
SEED_MAGNITUDE = UNIVERSAL_DRIFT
C_SEED = complex(math.cos(SPARK_ANGLE_RAD) * SEED_MAGNITUDE,
                 math.sin(SPARK_ANGLE_RAD) * SEED_MAGNITUDE)

# =============================================================================
# 2. INITIALIZATION (z_0 mapping to Grid Coordinates)
# =============================================================================

def get_z0_grid(mbti: str, blood: str, gender: str) -> Tuple[float, float]:
    """
    Maps Type Identity to Initial Grid Position (x, y in [0,16]).
    NOT complex plane - actual grid coordinates.
    """
    ei = mbti[0]  # E/I
    sn = mbti[1]  # S/N
    tf = mbti[2]  # T/F
    jp = mbti[3]  # J/P
    group_key = f"{ei}{jp}"
    
    base_col = GROUP_MAP_FEMALE[group_key] if gender == "F" else GROUP_MAP_MALE[group_key]
    
    # Calculate grid position
    off_sn = SN_OFFSET[sn]
    off_tf = TF_OFFSET[tf]
    bx = BLOOD_OFFSET_X[blood]
    by = BLOOD_OFFSET_Y[blood]
    
    # Grid coordinates (0..16) - START FROM TOP (row 16)
    gx = base_col + 0.5 + off_sn + off_tf + bx
    gy = 15.5 + by  # Start near TOP (row 15-16), flow downward
    
    return (gx, gy)

# =============================================================================
# 3. PHYSICS OPERATOR G (for grid-based evolution)
# =============================================================================

def compute_G_grid(x: float, y: float, z_complex: complex, history: complex, t: float) -> Tuple[float, float]:
    """
    G(x, y, z, t) = Coulomb + Weak + 5/32 Gate + Hysteresis
    Returns (dx, dy) in grid coordinates.
    """
    # Coulomb attraction to center (x=8, y varies)
    r = math.sqrt((x - 8)**2 + (y - 8)**2) + 1e-6
    fx_coulomb = -COULOMB_K * (x - 8) / (r * (r + 0.1))
    fy_coulomb = -COULOMB_K * (y - 8) / (r * (r + 0.1))
    
    # Weak force - phase rotation (chirality)
    phase_rot = WEAK_G * CHIRALITY * r
    fx_weak = phase_rot * (y - 8) / r
    fy_weak = -phase_rot * (x - 8) / r
    
    # 5/32 Gate - spatial modulation
    gate_val = math.sin(10 * (x / 16)) * math.sin(10 * (y / 16))
    fx_gate = fx_coulomb * (GATE_5_32 * gate_val)
    fy_gate = fy_coulomb * (GATE_5_32 * gate_val)
    
    # Hysteresis - memory
    fx_hyst = (history.real - x) * HYSTERESIS_MEM * 0.01
    fy_hyst = (history.imag - y) * HYSTERESIS_MEM * 0.01
    
    # Universal drift (upward in time/rows)
    fy_drift = UNIVERSAL_DRIFT * 0.5
    
    dx = fx_coulomb + fx_weak + fx_gate + fx_hyst
    dy = fy_coulomb + fy_weak + fy_gate + fy_hyst + fy_drift
    
    return (dx, dy)

# =============================================================================
# 4. SINGLE ITERATION ENGINE (Grid-based, not complex plane)
# =============================================================================

def iterate_grid_trajectory(mbti: str, blood: str, gender: str, 
                              steps: int = 16, dt: float = 0.5) -> List[Tuple[float, float, bool]]:
    """
    Generate trajectory in GRID coordinates [0,16] x [0,16].
    Returns list of (x, y, is_spark_flash).
    """
    x, y = get_z0_grid(mbti, blood, gender)
    
    # Convert to complex for z^2 calculation
    z = complex((x - 8) / 8, (y - 8) / 8)  # Normalize to [-1,1] for math
    z_prev = z
    
    trajectory = [(x, y, False)]
    
    for step in range(steps):
        # Calculate physics G
        dx, dy = compute_G_grid(x, y, z, z_prev, step * dt)
        
        # Mandelbrot self-interaction (z^2 term)
        # Scale down to avoid explosion
        z2_effect = (z * z) * 0.05
        
        # Seed c contribution
        c_effect = C_SEED * 0.1
        
        # Update complex z
        z_new = z + z2_effect + c_effect + complex(dx * 0.01, dy * 0.01)
        
        # Check for spark condition (Gap compression)
        is_spark = False
        angle = math.atan2(z_new.imag, z_new.real) * 180 / PI
        if angle > SPARK_ANGLE_DEG - 5 and angle < SPARK_ANGLE_DEG + 5:
            if abs(z_new) > 0.5:  # Threshold for spark
                is_spark = True
                # Spark leap - diagonal reset
                x = x + (8 - x) * 0.3  # Move toward center
                y = y + (16 - y) * 0.2  # Move upward
        
        # Update grid coordinates
        x = max(0, min(16, x + dx * dt))
        y = max(0, min(16, y + dy * dt))
        
        # Convert back from complex
        if not is_spark:
            x = 8 + z_new.real * 8
            y = 8 + z_new.imag * 8
            x = max(0, min(16, x))
            y = max(0, min(16, y))
        
        trajectory.append((float(x), float(y), is_spark))
        z_prev = z
        z = z_new
    
    return trajectory

# =============================================================================
# 5. RENDERING (16x16 Grid with Discrete Scatter + Lines)
# =============================================================================

def render_grid_v5(trajectories: Dict[str, List[Tuple[float, float, bool]]], output_path: str):
    """
    Render 128-Type Grid with:
    - 16x16 grid cells
    - Twilight bands
    - Scatter points + connecting lines
    - Spark leaps as black dotted lines
    - Diagonal reference line
    """
    fig, ax = plt.subplots(figsize=(16, 16))
    fig.patch.set_facecolor("#F8F8F8")
    ax.set_facecolor("#FAFAFA")
    
    # Draw grid cells (16x16)
    for r in range(N_ROWS):
        for c in range(N_COLS):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, 
                                          facecolor="white", 
                                          edgecolor="#E0E0E0", 
                                          lw=0.5, zorder=1))
    
    # Twilight bands (shaded regions)
    TWILIGHT_1_LO = N_ROWS * F_1_16      # 1.0
    TWILIGHT_1_HI = N_ROWS * (7 * F_1_32)  # 3.5
    TWILIGHT_2_LO = N_ROWS * (17 * F_1_32) # 8.5
    TWILIGHT_2_HI = N_ROWS * (23 * F_1_32) # 11.5
    
    ax.add_patch(mpatches.Rectangle((0, TWILIGHT_1_LO), N_COLS, 
                                  (TWILIGHT_1_HI - TWILIGHT_1_LO),
                                  facecolor="#99CCFF", edgecolor="none", 
                                  alpha=0.15, zorder=2))
    ax.add_patch(mpatches.Rectangle((0, TWILIGHT_2_LO), N_COLS, 
                                  (TWILIGHT_2_HI - TWILIGHT_2_LO),
                                  facecolor="#CC99FF", edgecolor="none", 
                                  alpha=0.15, zorder=2))
    
    # Separatrix lines
    SEPARATRIX_1 = N_COLS * (5/16)   # 5.0
    SEPARATRIX_2 = N_COLS * (11/16) # 11.0
    ax.axvline(x=SEPARATRIX_1, color="gray", linestyle=":", alpha=0.5, linewidth=2, zorder=3)
    ax.axvline(x=SEPARATRIX_2, color="gray", linestyle=":", alpha=0.5, linewidth=2, zorder=3)
    
    # Diagonal line (corner to corner)
    ax.plot([0, N_COLS], [0, N_ROWS], color="orange", linestyle="--", 
            alpha=0.4, linewidth=2, zorder=4)
    
    # Draw trajectories
    for key, points in trajectories.items():
        parts = key.split("_")
        blood = parts[1]
        gender = parts[2]
        
        color = BLOOD_COLORS.get(blood, "black")
        
        # Extract coordinates
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        sparks = [p[2] for p in points]
        
        # Draw connecting lines
        for i in range(len(points) - 1):
            x1, y1, spark1 = points[i]
            x2, y2, spark2 = points[i + 1]
            
            if spark2:  # Spark leap - heavy black dotted
                ax.plot([x1, x2], [y1, y2], color="black", linestyle=":", 
                       linewidth=2.5, alpha=0.9, zorder=25)
            else:  # Normal line
                alpha = 0.6 if gender == "F" else 0.5
                lw = 1.2 if gender == "F" else 1.0
                ax.plot([x1, x2], [y1, y2], color=color, alpha=alpha, 
                       linewidth=lw, zorder=20)
        
        # Draw scatter points
        ax.scatter(xs, ys, color=color, s=20, edgecolors='white', 
                  linewidth=0.5, zorder=30, alpha=0.9)
        
        # Mark start point
        ax.scatter(xs[0], ys[0], color=color, s=50, marker='o', 
                  edgecolors='black', linewidth=1, zorder=35)
    
    # Labels and info
    ax.set_xlim(0, N_COLS)
    ax.set_ylim(0, N_ROWS)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Grid X (Left=Female, Right=Male)", fontsize=12)
    ax.set_ylabel("Time Windows (0=Dawn, 16=Midnight)", fontsize=12)
    
    info_text = (
        f"V5: Single Iteration Axiom\n"
        f"z' = z² + c + G(z,t)\n"
        f"Seed: {SPARK_ANGLE_DEG}° | Gap: {GAP_DEG:.3f}°\n"
        f"Drift: {UNIVERSAL_DRIFT:.4f} | Chirality: 1/18"
    )
    ax.text(0.5, 15.5, info_text, fontsize=10, 
           bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'),
           verticalalignment='top')
    
    # Legend for blood types
    legend_elements = [mpatches.Patch(color=color, label=blood) 
                      for blood, color in BLOOD_COLORS.items()]
    ax.legend(handles=legend_elements, loc='upper right', title='Blood Type')
    
    ax.set_title("128-Type Grid V5: Observer Axiom (Discrete 16×16 Grid)", fontsize=14, pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")

# =============================================================================
# 6. MAIN
# =============================================================================

def main():
    print("V5 Grid Generator — Single Iteration Axiom")
    print(f"Gap: {GAP_DEG:.4f}° | Drift: {UNIVERSAL_DRIFT:.4f}")
    print(f"Seed c: {C_SEED}")
    
    trajectories = {}
    
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                key = f"{mbti}_{blood}_{gender}"
                traj = iterate_grid_trajectory(mbti, blood, gender, steps=20, dt=0.3)
                trajectories[key] = traj
                if len(trajectories) % 50 == 0:
                    print(f"  Generated {len(trajectories)}/128 trajectories...")
    
    output_file = "out/128_Grid_V5_Single_Iteration.png"
    render_grid_v5(trajectories, output_file)
    
    # Verification log
    log_path = "out/V5_verification_log.txt"
    with open(log_path, "w") as f:
        f.write("V5 Grid Verification\n")
        f.write("=" * 50 + "\n")
        f.write(f"Formula: Grid-based z' = z² + c + G\n")
        f.write(f"Seed c: {C_SEED} (|c|={SEED_MAGNITUDE:.6f})\n")
        f.write(f"Spark Angle: {SPARK_ANGLE_DEG}°\n")
        f.write(f"Gap: {GAP_DEG:.6f}°\n")
        f.write(f"Universal Drift: {UNIVERSAL_DRIFT:.6f}\n")
        f.write(f"Grid: {N_ROWS}×{N_COLS} discrete cells\n")
        f.write(f"Types: {len(trajectories)} trajectories generated\n")
        f.write("Status: DETERMINISTIC (fixed seeds and physics)\n")
    print(f"Saved: {log_path}")
    print("Done.")

if __name__ == "__main__":
    main()
