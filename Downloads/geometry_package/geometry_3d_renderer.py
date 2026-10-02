# geometry_package/geometry_3d_renderer.py
# This is the canonical Python renderer for the Unified Geometry.
# It is updated to use the single source of truth: absolute_constants.py
# This script is NOT a heightmap generator, but a composite object renderer.

import matplotlib
matplotlib.use('Agg') # Force headless so it can run on servers
import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D

# Use the canonical constants as the single source of truth
from . import absolute_constants as const

def render_unified_geometry(output_path="SYNTHESIS_UNIFIED_GEOMETRY.png"):
    """
    Renders the full composite geometry scene based on the python implementation.
    This function combines all the geometric objects into one scene.
    The most "terrain-like" part is the `_cristae_fractal_surface`.
    """
    fig = plt.figure(figsize=(18, 18), facecolor="#050510")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#050510")

    # BASE PARAMETERS from constants
    R_base = const.R_VOID * const.REALITY_TENSION * const.MANIFOLD_CLOSURE
    z_offset = 0.0
    phi_inv_local = const.PHI_INV

    # === Main Fractal Surface Generation (_cristae_fractal_surface) ===
    # This is the core generative geometry logic.
    u = np.linspace(0.0, 2.0 * math.pi, 160)
    v = np.linspace(0.0, math.pi, 80)
    U, V = np.meshgrid(u, v)

    modulation = np.zeros_like(U)
    for k in range(1, 8): # Loop 1 to 7
        amp = (const.KAPPA_1_32 * (phi_inv_local ** (k - 1))) / float(k)
        modulation += amp * np.sin(11.0 * float(k) * U) * np.sin(float(k) * V)
        modulation += (const.KAPPA_1_64 * (phi_inv_local ** (k - 1))) * np.cos(11.0 * float(k) * U) * np.sin(float(k + 1) * V)
    
    R_modulated = R_base * (1.0 + modulation)

    # Convert from spherical to cartesian coordinates to get the final shape
    X = R_modulated * np.cos(U) * np.sin(V)
    Y = R_modulated * np.sin(U) * np.sin(V)
    Z = R_modulated * np.cos(V) + z_offset

    ax.plot_wireframe(X, Y, Z, color="#ffd200", alpha=0.4, linewidth=0.7, rstride=3, cstride=3)
    
    # === Other Geometric Objects for context ===
    
    # Central Axis (ACh Spine)
    ax.plot([0, 0], [0, 0], [-R_base * 2, R_base * 2], color="#00ffcc", alpha=0.7, lw=3.0)

    # Torus Body (Mantle)
    R_torus_major = R_base * 4.0
    r_torus_minor = R_base * 1.5
    u_torus = np.linspace(0, 2 * np.pi, 128)
    v_torus = np.linspace(0, 2 * np.pi, 64)
    UT, VT = np.meshgrid(u_torus, v_torus)
    XT = (R_torus_major + r_torus_minor * np.cos(VT)) * np.cos(UT)
    YT = (R_torus_major + r_torus_minor * np.cos(VT)) * np.sin(UT)
    ZT = r_torus_minor * np.sin(VT)
    ax.plot_surface(XT, YT, ZT, color="#222233", alpha=0.1, linewidth=0, antialiased=True)

    # Styling
    ax.set_axis_off()
    ax.set_box_aspect([1.0, 1.0, 1.0])
    lim = R_torus_major + r_torus_minor
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    
    ax.text2D(0.05, 0.95, "Unified Geometry (Python Reference)", transform=ax.transAxes, color="white", fontsize=14)

    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="#050510")
    plt.close(fig)
    print(f"Rendered canonical python geometry to {output_path}")

if __name__ == "__main__":
    # Ensure the constants are loaded before rendering
    print("Executing Python renderer with canonical constants...")
    render_unified_geometry()
