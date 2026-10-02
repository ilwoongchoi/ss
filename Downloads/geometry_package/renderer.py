# -*- coding: utf-8 -*-
"""
renderer.py
===========
Renders the absolute zero-error calibrated geometry.
Visualizes the collision between the Continuous Void (Pi) and the 
Discrete Structural Gates (Fractions), which forces the 138.88° Spark.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math
from .absolute_constants import CALIBRATED_SKELETON

def render_pure_geometry(output_path="pure_geometry_manifold.png"):
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect('equal')
    ax.set_facecolor('#050510')

    # Load perfectly calibrated constants
    w7_area = CALIBRATED_SKELETON["W7_AREA"]       # pi/20
    kappa_3_32 = CALIBRATED_SKELETON["COMPRESSION_GAP_3_32"] # 3/32
    kappa_1_32 = CALIBRATED_SKELETON["KAPPA_1_32"]           # 1/32
    spark_angle = CALIBRATED_SKELETON["SPARK_ANGLE_DEG"]     # 138.88
    
    # 1. Draw the Discrete Grid / Structural Gates (The rigid fractions)
    # These represent the exact topological cuts in the manifold
    ax.axhline(kappa_3_32, color='red', linestyle='--', linewidth=2, alpha=0.8, label='Darkness Stress (3/32)')
    ax.axhline(kappa_1_32, color='orange', linestyle=':', linewidth=2, alpha=0.8, label='Minimal Core (1/32)')
    ax.axhline(-kappa_3_32, color='red', linestyle='--', linewidth=2, alpha=0.8)
    ax.axvline(kappa_3_32, color='blue', linestyle='--', linewidth=2, alpha=0.8, label='Cortisol / Nile Delta (3/32)')
    ax.axvline(-kappa_3_32, color='blue', linestyle='--', linewidth=2, alpha=0.8)

    # 2. Draw the Continuous Energy Flow (The Pi component)
    # W7 Area = pi/20. Representing as a perfect circle/ellipse of equivalent area.
    # Area = pi * r^2  => r = sqrt(Area / pi) = sqrt((pi/20) / pi) = sqrt(1/20)
    radius = math.sqrt(w7_area / math.pi)
    
    theta = np.linspace(0, 2*math.pi, 300)
    x_cont = radius * np.cos(theta)
    y_cont = radius * np.sin(theta)
    ax.plot(x_cont, y_cont, color='cyan', linewidth=3, label=f'Continuous Void ($Area = \pi/20$)')
    ax.fill(x_cont, y_cont, color='cyan', alpha=0.1)

    # 3. The Collision and The Spark
    # The spark occurs where the continuous flow hits the rigid 3/32 compression gap.
    # At y = 3/32, x = sqrt(r^2 - y^2)
    try:
        spark_x = math.sqrt(radius**2 - kappa_3_32**2)
        spark_y = kappa_3_32
        
        # Calculate spark vector
        # 138.88 degrees converted to radians
        spark_rad = math.radians(spark_angle)
        dx = math.cos(spark_rad) * CALIBRATED_SKELETON["SPARK_LEAP_DIST"]
        dy = math.sin(spark_rad) * CALIBRATED_SKELETON["SPARK_LEAP_DIST"]

        ax.annotate(
            '', xy=(spark_x + dx, spark_y + dy), xytext=(spark_x, spark_y),
            arrowprops=dict(arrowstyle="->,head_width=0.8,head_length=1.2", 
                            color='yellow', lw=4, ls='-')
        )
        ax.plot(spark_x, spark_y, 'wo', markersize=10, markeredgecolor='yellow', markeredgewidth=2)
        ax.text(spark_x + 0.05, spark_y + 0.05, '138.88° Diagonal Reset Spark\n(Driven by Pi vs Fraction Tension)', 
                color='yellow', fontsize=12, fontweight='bold')
    except ValueError:
        pass # If radius is smaller than 3/32, no intersection (but math shows r ~0.223, 3/32 = 0.093, so it intersects)

    # Styling
    limit = 0.4
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.grid(color='#222233', linestyle='-', linewidth=0.5)
    
    # Information Box
    tension_val = CALIBRATED_SKELETON["MANIFOLD_CLOSURE"]
    info_text = (
        "ABSOLUTE ZERO-ERROR CALIBRATION\n"
        "-------------------------------\n"
        f"Continuous Area (W7): $\pi/20$ ({w7_area:.5f})\n"
        f"Discrete Topo Gap (H2): 1/9 ({CALIBRATED_SKELETON['H2_W7']:.5f})\n"
        f"Compression Gate: 3/32 ({kappa_3_32:.5f})\n"
        f"Structural Tension: {tension_val:.6f}\n\n"
        "The gap between Pi and Fractions\n"
        "forces the system to Spark (Leap)."
    )
    ax.text(0.05, 0.95, info_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='black', alpha=0.8, edgecolor='cyan'),
            color='white', family='monospace')

    plt.title("Geometry Manifold: Continuous vs Discrete Tension", color='white', pad=20, fontsize=16)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Rendered pure geometry to {output_path}")

if __name__ == "__main__":
    render_pure_geometry()
