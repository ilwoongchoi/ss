# -*- coding: utf-8 -*-
"""
DRAW_128_GRID.py - 128 Type Trajectory Grid Visualization
Generates the definitive 128-type grid showing all MBTI x Blood x Gender combinations.
"""

import math
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ============================================================================
# CONSTANTS (Standalone - No Imports)
# ============================================================================

SPARK_ANGLE_DEG = 138.88
SPARK_LEAP_DIST = 2.5
F_1_32 = 1.0 / 32.0
F_3_32 = 3.0 / 32.0

N_ROWS = 16
N_COLS = 16

# MBTI Groups
ALL_MBTI = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]

BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

# Grid layout
GROUP_MAP_FEMALE = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
GROUP_MAP_MALE = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}

SN_OFFSET = {"S": -8 * F_1_32, "N": 8 * F_1_32}
TF_OFFSET = {"T": -4 * F_1_32, "F": 4 * F_1_32}
BLOOD_OFFSET_X = {"O": -2 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": 2 * F_1_32}
BLOOD_OFFSET_Y = {"O": 4 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": -4 * F_1_32}

# ============================================================================
# POSITION CALCULATION
# ============================================================================

def get_position(mbti, blood, gender):
    """Calculate grid position for entity."""
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_key = f"{ei}{jp}"
    base_col = (GROUP_MAP_FEMALE if gender == "F" else GROUP_MAP_MALE)[group_key]
    
    x = base_col + 0.5 + SN_OFFSET[sn] + TF_OFFSET[tf] + BLOOD_OFFSET_X[blood]
    y = 0.5 + BLOOD_OFFSET_Y[blood]
    
    return x, y


def get_trajectory(x0, y0, mbti, blood, gender, branch="sunrise", steps=100):
    """Generate trajectory from start position."""
    points = [(x0, y0)]
    x, y = x0, y0
    
    # Simple trajectory physics
    angle = math.radians(SPARK_ANGLE_DEG) if branch == "sunrise" else math.radians(-SPARK_ANGLE_DEG)
    dx_base = math.cos(angle) * 0.05
    dy_base = math.sin(angle) * 0.05
    
    # Gender modifies trajectory
    speed = 1.2 if gender == "M" else 0.8
    
    for i in range(steps):
        # Spiral outward
        t = i / steps
        spiral_x = math.cos(t * 4 * math.pi) * 0.1 * speed
        spiral_y = math.sin(t * 4 * math.pi) * 0.1 * speed
        
        x += dx_base + spiral_x * 0.02
        y += dy_base + spiral_y * 0.02 + 0.02
        
        # Boundary check
        x = max(0.2, min(15.8, x))
        y = max(0.2, min(15.8, y))
        
        points.append((x, y))
    
    return points


# ============================================================================
# DRAW 128 GRID
# ============================================================================

def draw_128_grid(output_file="128_GRID_OUTPUT.png"):
    """Draw the complete 128-type trajectory grid."""
    
    fig, ax = plt.subplots(figsize=(20, 20), dpi=150)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_aspect('equal')
    ax.set_facecolor('#0a0a0a')
    fig.patch.set_facecolor('#0a0a0a')
    
    # Draw grid lines
    for i in range(17):
        ax.axhline(i, color='#1a1a1a', linewidth=0.5, alpha=0.8)
        ax.axvline(i, color='#1a1a1a', linewidth=0.5, alpha=0.8)
    
    # Draw group separators (thicker lines)
    for i in [2, 4, 6, 8, 10, 12, 14]:
        ax.axvline(i, color='#333333', linewidth=1.5, alpha=0.6)
    for i in [2, 4, 6, 8, 10, 12, 14]:
        ax.axhline(i, color='#333333', linewidth=1.5, alpha=0.6)
    
    # Generate and draw all 128 entities
    entity_count = 0
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                x0, y0 = get_position(mbti, blood, gender)
                color = BLOOD_COLORS[blood]
                
                # Draw trajectory
                traj = get_trajectory(x0, y0, mbti, blood, gender, "sunrise")
                xs = [p[0] for p in traj]
                ys = [p[1] for p in traj]
                
                # Line alpha based on gender
                alpha = 0.6 if gender == "M" else 0.4
                linewidth = 1.0 if gender == "M" else 0.8
                
                ax.plot(xs, ys, color=color, linewidth=linewidth, alpha=alpha)
                
                # Draw start point
                marker = 'o' if gender == "F" else 's'
                ax.scatter(x0, y0, c=color, s=30, marker=marker, 
                          edgecolors='white', linewidths=0.5, zorder=5)
                
                # Draw end point with spark effect
                ax.scatter(xs[-1], ys[-1], c='white', s=15, marker='*', zorder=4)
                
                entity_count += 1
    
    # Add MBTI group labels
    mbti_groups = ["EJ", "EP", "IJ", "IP"]
    for i, group in enumerate(mbti_groups):
        # Female groups (left side)
        ax.text(i * 2 + 1, 15.5, f"{group}\n(F)", ha='center', va='top',
                fontsize=9, color='#888888', fontweight='bold')
        # Male groups (right side)
        ax.text((i + 4) * 2 + 1, 15.5, f"{group}\n(M)", ha='center', va='top',
                fontsize=9, color='#888888', fontweight='bold')
    
    # Add blood type legend
    legend_elements = [
        mpatches.Patch(color=BLOOD_COLORS["O"], label='Type O'),
        mpatches.Patch(color=BLOOD_COLORS["A"], label='Type A'),
        mpatches.Patch(color=BLOOD_COLORS["B"], label='Type B'),
        mpatches.Patch(color=BLOOD_COLORS["AB"], label='Type AB'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='white', 
                   markersize=8, label='Female', linestyle='None'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='white',
                   markersize=8, label='Male', linestyle='None'),
    ]
    ax.legend(handles=legend_elements, loc='upper center', 
             bbox_to_anchor=(0.5, -0.02), ncol=6, fontsize=10,
             facecolor='#1a1a1a', edgecolor='#333333', labelcolor='white')
    
    # Title
    ax.set_title('128-Type Trajectory Grid\n' +
                 f'MBTI × Blood Type × Gender = 16 × 4 × 2 = {entity_count} Types\n' +
                 f'Spark Angle: {SPARK_ANGLE_DEG}° | Leap: {SPARK_LEAP_DIST} | Compression: 3/32',
                 fontsize=14, color='white', pad=20)
    
    # Remove axis
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add border
    for spine in ax.spines.values():
        spine.set_color('#333333')
        spine.set_linewidth(2)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, facecolor='#0a0a0a', edgecolor='none')
    print(f"Saved: {output_file}")
    print(f"Entities drawn: {entity_count}")
    
    return fig, ax


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DRAW_128_GRID - 128 Type Trajectory Visualization")
    print("=" * 60)
    print()
    print("Generating 128-Type Grid...")
    print()
    
    draw_128_grid("128_GRID_FINAL.png")
    
    print()
    print("Complete. Open 128_GRID_FINAL.png to view.")
