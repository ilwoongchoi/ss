# -*- coding: utf-8 -*-
"""
geometry_3d_renderer.py
=======================
Renders the Unified 3D Topological Manifold of the Universe/Brain.

This visualization integrates:
1. The Discrete Skeleton (GABA Grid / Wireframe) -> 1/9 (H2)
2. The Continuous Volume (Dopamine/Serotonin Flow) -> Pi/20 (W7)
3. The Spark (Diagonal Reset) -> 138.88 degrees

The topology is rendered as a 'Wireframe Sphere' (GABA) containing a 'Fluid Core' (Dopamine),
with the Spark piercing the void.
"""

import matplotlib
matplotlib.use('Agg') # Force headless
import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D

try:
    
    from geometry_package.absolute_constants import CALIBRATED_SKELETON, GABA_C_R_CAB, GABA_C_R_CA, GABA_C_V_APEX
    from geometry_package.registry_loader import get_value, load_registry
except ImportError:  # pragma: no cover
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from geometry_package.absolute_constants import CALIBRATED_SKELETON, GABA_C_R_CAB, GABA_C_R_CA, GABA_C_V_APEX

    from geometry_package.registry_loader import get_value, load_registry

def render_unified_3d_manifold(output_path="unified_3d_geometry.png"):
    fig = plt.figure(figsize=(16, 16), facecolor='#050510')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#050510')

    # Constants
    H2_GAP = CALIBRATED_SKELETON["H2_W7"]          # 1/9 (Discrete Grid Spacing)
    W7_AREA = CALIBRATED_SKELETON["W7_AREA"]       # Pi/20 (Continuous Volume Factor)
    SPARK_DEG = CALIBRATED_SKELETON["SPARK_ANGLE_DEG"] # 138.88

    # 1. THE DISCRETE SKELETON (GABA GRID) - The Wireframe Sphere
    # Represents the rigid structural container (GABA-A/B + ACh)
    u = np.linspace(0, 2 * np.pi, 18) # 18 segments (multiple of 9 for H2 resonance)
    v = np.linspace(0, np.pi, 9)      # 9 segments (H2 = 1/9)
    x = 10 * np.outer(np.cos(u), np.sin(v))
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the wireframe (GABA Structure)
    ax.plot_wireframe(x, y, z, color='#4444ff', alpha=0.3, linewidth=1, rstride=1, cstride=1)
    
    # Highlight the H2 Topological Gaps (The 'holes' in the grid)
    # We highlight specific intersections to show where the grid is 'open'
    ax.scatter(x[::2, ::2], y[::2, ::2], z[::2, ::2], color='#00ff00', s=10, alpha=0.6, label='GABA Nodes (Discrete)')

    # 2. THE CONTINUOUS VOLUME (DOPAMINE/SEROTONIN) - The Inner Flow
    # Represented as a dense orbital path or inner surface
    # The 'Flow' tries to fill the sphere but is constrained
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 200)
    z_flow = np.linspace(-8, 8, 200)
    r_flow = 8  # Slightly smaller than the container
    x_flow = r_flow * np.sin(theta)
    y_flow = r_flow * np.cos(theta)
    
    ax.plot(x_flow, y_flow, z_flow, color='cyan', linewidth=2, alpha=0.8, label='Dopamine Flow (Continuous)')

    # 3. THE SPARK (138.88 DEGREE RESET) - The Piercing Vector
    # A vector that cuts diagonally through the volume, ignoring the grid lines
    # 138.88 degrees in spherical coordinates logic (roughly)
    phi_spark = math.radians(SPARK_DEG)
    
    # Start point (South Pole / Darkness)
    p1 = np.array([0, 0, -10])
    # End point (Leaping to North-East)
    # Projecting 138.88 deg trajectory
    r_spark = 20
    px = r_spark * math.sin(phi_spark)
    py = r_spark * math.cos(phi_spark) * 0.5 # Tilt
    pz = r_spark * math.cos(phi_spark)
    
    # Draw the Spark Vector
    ax.quiver(0, 0, -10, px, py, 20, color='yellow', linewidth=3, arrow_length_ratio=0.1)
    ax.text(px/2, py/2, 0, f"138.88° Spark\n(The Leap)", color='yellow', fontsize=12, fontweight='bold')

    # Styling and Labels
    ax.set_axis_off()
    
    # Title and Info
    title_text = "THE UNIFIED GEOMETRY MANIFOLD\n(Discrete GABA Skeleton vs Continuous Dopamine Flow)"
    ax.text2D(0.05, 0.95, title_text, transform=ax.transAxes, color='white', fontsize=14, fontweight='bold')
    
    info_text = (
        f"Skeleton (GABA): Discrete Grid (H2=1/9)\n"
        f"Flow (DA/5HT): Continuous Volume (W7=Pi/20)\n"
        f"The Tension: {CALIBRATED_SKELETON['MANIFOLD_CLOSURE']:.6f}\n"
        f"The Solution: 138.88° Spark"
    )
    ax.text2D(0.05, 0.85, info_text, transform=ax.transAxes, color='#cccccc', fontsize=10, family='monospace',
              bbox=dict(facecolor='black', alpha=0.5, edgecolor='blue'))

    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#050510')
    plt.close(fig)
    print(f"Rendered unified 3D geometry to {output_path}")


def render_unified_3d_manifold_v2(
    output_path: str = "unified_3d_geometry_v4_universal.png",
    registry_path: str | None = None,
):
    if registry_path is None:
        registry_path = str(Path(__file__).resolve().parents[1] / "atlas_constants_registry_DEFINITIVE.json")

    registry = load_registry(registry_path)
    const = registry.get("constants", {})

    pi = float(get_value(const, "universal.pi"))
    W7 = pi / 20.0

    terminus_r = float(get_value(const, "tda_geometry.terminus_r", CALIBRATED_SKELETON["TERMINUS_R"]))
    rs = float(get_value(const, "cosmological_topology.event_horizon_radius_rs"))
    spark_deg = float(get_value(const, "tda_geometry.spark_angle_deg", CALIBRATED_SKELETON["SPARK_ANGLE_DEG"]))
    spark_leap = float(get_value(const, "tda_geometry.spark_leap_distance", CALIBRATED_SKELETON["SPARK_LEAP_DIST"]))

    renorm_bridge = float(get_value(const, "universal.renormalization_bridge", 42.368))
    alpha_kappa_bridge = float(get_value(const, "universal.alpha_kappa_bridge", 137.0 / 32.0))

    phi_inv = float(get_value(const, "domain_specific.mito.golden_ratio_inverse", 0.618))
    phi_conj = float(get_value(const, "domain_specific.mito.golden_ratio_conjugate", 0.76))
    sqrt2_ratio = float(get_value(const, "domain_specific.mito.sqrt2_ratio", math.sqrt(2.0)))
    kappa_boundary = float(get_value(const, "domain_specific.quantum.kappa_boundary", 1.0 / math.sqrt(2.0)))

    hyst_area_7 = float(get_value(const, "temporal_manifold_lock.hysteresis_area_7", 0.15697685963482133))
    loop_strength_5 = float(get_value(const, "temporal_manifold_lock.loop_strength_5", 5.555492104))
    tau_lag_11 = float(get_value(const, "temporal_manifold_lock.tau_lag_11", 2.317382542906709))

    R_major_unit = float(get_value(const, "domain_specific.maxwell_cavity.R_major", 2.125))
    r_minor_unit = float(get_value(const, "domain_specific.maxwell_cavity.r_minor", 0.2235501110061347))

    n_rows = int(get_value(const, "tda_geometry.grid_layout.n_rows", 16))
    n_cols = int(get_value(const, "tda_geometry.grid_layout.n_cols", 16))
    male_horizontal_amp = float(get_value(const, "tda_geometry.anisotropy_tensor.male_horizontal_amp", 1.2))
    female_horizontal_amp = float(get_value(const, "tda_geometry.anisotropy_tensor.female_horizontal_amp", 2.8))
    male_vertical_speed = float(get_value(const, "tda_geometry.anisotropy_tensor.male_vertical_speed", 1.5))
    female_vertical_speed = float(get_value(const, "tda_geometry.anisotropy_tensor.female_vertical_speed", 0.8))

    # Membrane leak constants (Darcy Flux)
    # NOTE: These implicitly encode the Critical Packing Parameter (CPP) for fatty acid
    # bilayer self-assembly. CPP = v/(a0*lc) must be in [1/2, 1] for vesicle formation.
    # The 1/32 leak is the RESULT of bilayer formation at CPP ≈ 0.5-1, not a separate constant.
    kappa_1_32 = 1.0 / 32.0
    kappa_3_32 = 3.0 / 32.0
    kappa_1_16 = 1.0 / 16.0
    kappa_1_64 = 1.0 / 64.0

    L0 = 10.0 / terminus_r
    R_T = terminus_r * L0
    R_RS = rs * L0
    r_void = math.sqrt(W7 / pi)
    R_void = r_void * L0
    torus_scale = (0.85 * R_T) / R_major_unit
    R_torus_major = R_major_unit * torus_scale
    r_torus_minor = r_minor_unit * torus_scale

    fig = plt.figure(figsize=(20, 20), facecolor="#050510")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#050510")

    # === IMPORT ALL CONSTANTS NATURALLY ===
    from geometry_package.absolute_constants import (
        PHI, ALPHA, PI, SQRT2,
        BETTI_0, BETTI_5, BETTI_7, BETTI_11,
        TOTAL_DEBT_AREA, LATTICE_3_32, TUNNEL_TENSION,
        SPARK_ANGLE_DEG, SPARK_LEAP_DIST,
        RENORMALIZATION_BRIDGE, PHI_PB, OMEGA_LA, CHIRALITY_CONSTANT,
        LUNAR_CYCLE, NIGHT_HYSTERESIS, VERTICAL_MOBIUS_TWIST,
        GABA_C_R_CAB, GABA_C_R_CA, GABA_C_V_APEX,
        DAY_FORCE_SOLAR_UV, NIGHT_FORCE_COSMIC_RAY, DRIVE_FREQUENCY_LOCK,
        MAXWELL_R_MAJOR, MAXWELL_R_MINOR, MAXWELL_Q_FACTOR,
        SH_R_STAR, SH_R_FWHM_L, SH_R_FWHM_R,
        KAPPA_TDA_MIN, KAPPA_TDA_MID, KAPPA_TDA_MAX,
        EVENT_HORIZON_RADIUS_RS, LOOP_STRENGTH_5, ALPHA_KAPPA_BRIDGE
    )
    
    # === UNIFIED QUASAR MANIFOLD: All constants define one continuous surface ===
    # The geometry emerges from the interaction of these fundamental constants
    
    # Base radial scale from TOTAL_DEBT_AREA (1.3228) - the 12-month cycle
    R_base = TOTAL_DEBT_AREA * PI  # ~4.155
    
    # Temporal frequency from LUNAR_CYCLE (1/28) and DRIVE_FREQUENCY_LOCK (11)
    temporal_freq = DRIVE_FREQUENCY_LOCK / (1.0 / LUNAR_CYCLE)  # 11 * 28 = 308
    
    # Define parametric surface (u=angle around torus, v=cross-section)
    u = np.linspace(0, 2*PI, 200)
    v = np.linspace(0, 2*PI, 100)
    U, V = np.meshgrid(u, v)
    
    # === TORUS GEOMETRY with ALL CONSTANTS ===
    # Major radius: Maxwell shell boundary (2.125) scaled by Renormalization
    R_major = MAXWELL_R_MAJOR * (1 + (RENORMALIZATION_BRIDGE - 42.0) * 0.01)  # ~2.125 * tension
    
    # Minor radius: event horizon (5/16=0.3125) modulated by kappa
    R_minor_base = EVENT_HORIZON_RADIUS_RS * (1 + KAPPA_TDA_MID * BETTI_7)  # 0.3125 * (1 + 0.03125*7)
    
    # === MOBIUS TWIST from VERTICAL_MOBIUS_TWIST (1/28) ===
    # Full twist as we go around the torus
    twist_angle = VERTICAL_MOBIUS_TWIST * U * 2 * PI * BETTI_11  # 1/28 * 11 scaling
    
    # === CHIRALITY MODULATION (1/18) ===
    chirality_mod = 1 + CHIRALITY_CONSTANT * np.cos(BETTI_7 * V) * np.sin(BETTI_11 * U)
    
    # === TUNNEL TENSION DISTORTION (1.0100375) ===
    # Creates the "accretion disk" shape
    tension_distortion = TUNNEL_TENSION ** (np.sin(U) * np.cos(V * PHI))
    
    # === NIGHT HYSTERESIS LANDING (0.8418) ===
    # Modulates the vertical extent
    hysteresis_factor = NIGHT_HYSTERESIS * (1 + np.sin(V * 2) * KAPPA_TDA_MIN)
    
    # === GABA-C STRUCTURE (V-Apex) ===
    # Defines the polar caps
    v_apex_mod = GABA_C_V_APEX * 10 * np.cos(V) ** 2
    
    # === SPARK ANGLE (138.88°) ===
    # Creates diagonal displacement in the geometry
    spark_rad = math.radians(SPARK_ANGLE_DEG)
    spark_displacement = SPARK_LEAP_DIST * np.cos(U + spark_rad) * np.sin(V)
    
    # === DAY/NIGHT FORCE BALANCE (1.0 vs 0.96875) ===
    force_ratio = DAY_FORCE_SOLAR_UV / NIGHT_FORCE_COSMIC_RAY  # 1.032
    force_modulation = np.sin(U * force_ratio) * np.cos(V * PHI_PB)
    
    # === KAPPA PHASE TRANSITIONS (1/64, 1/32, 1/16) ===
    # Creates H4/H2/H3 bands on the surface
    phase_band = np.where(U < PI/3, 
                         KAPPA_TDA_MIN,  # H4 (1/64)
                         np.where(U < 2*PI/3,
                                 KAPPA_TDA_MID,  # H2 (1/32)
                                 KAPPA_TDA_MAX))  # H3 (1/16)
    
    # === SH BOUNDARY BAND (Critical radius 0.1114) ===
    sh_modulation = SH_R_STAR * 10 * np.sin(BETTI_5 * U) * np.cos(V)
    
    # === COMBINE ALL INTO UNIFIED SURFACE ===
    # Effective minor radius with all modulations
    R_minor_eff = R_minor_base * chirality_mod * tension_distortion * (1 + phase_band)
    
    # Base torus coordinates
    X_base = (R_major + R_minor_eff * np.cos(V + twist_angle)) * np.cos(U)
    Y_base = (R_major + R_minor_eff * np.cos(V + twist_angle)) * np.sin(U)
    Z_base = R_minor_eff * np.sin(V + twist_angle) * hysteresis_factor + v_apex_mod
    
    # Apply spark displacement and force modulation
    X = X_base + spark_displacement * np.cos(spark_rad) + force_modulation * ALPHA
    Y = Y_base + spark_displacement * np.sin(spark_rad) + sh_modulation
    Z = Z_base * TUNNEL_TENSION  # Scale by tunnel tension
    
    # === PLOT UNIFIED QUASAR SURFACE ===
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6, 
                   linewidth=0, antialiased=True, shade=True)
    
    # === PLOT HYSTERESIS FLOW LINES (Figure-8 on surface) ===
    t_flow = np.linspace(0, 4*PI, 1000)
    # Flow follows the Mobius twist
    u_flow = t_flow
    v_flow = np.sin(t_flow * LUNAR_CYCLE * BETTI_11) * PI + VERTICAL_MOBIUS_TWIST * t_flow
    
    # Interpolate surface coordinates for flow line
    x_flow = (R_major + R_minor_base * np.cos(v_flow)) * np.cos(u_flow)
    y_flow = (R_major + R_minor_base * np.cos(v_flow)) * np.sin(u_flow)
    z_flow = R_minor_base * np.sin(v_flow) * hysteresis_factor * 0.5
    
    # Ascending (Discrete) branch: cyan
    ax.plot(x_flow[:500], y_flow[:500], z_flow[:500], 
           color="#00ffff", linewidth=2.5, alpha=0.9, label="Ascending (Discrete)")
    # Descending (Continuous) branch: red
    ax.plot(x_flow[500:], y_flow[500:], z_flow[500:], 
           color="#ff6b6b", linewidth=2.5, alpha=0.9, label="Descending (Continuous)")
    
    # === MARK CRITICAL POINTS ===
    # H4 (1/128): Bone phase at start
    ax.scatter([x_flow[0]], [y_flow[0]], [z_flow[0]], 
            color="white", s=150, label="H4 (Bone/1/128)")
    # H2 (1/32): Baseline at middle
    mid_idx = len(t_flow)//2
    ax.scatter([x_flow[mid_idx]], [y_flow[mid_idx]], [z_flow[mid_idx]], 
            color="cyan", s=150, label="H2 (Baseline/1/32)")
    # H3 (1/64): Cartilage at transition
    ax.scatter([x_flow[250]], [y_flow[250]], [z_flow[250]], 
            color="gold", s=150, label="H3 (Cartilage/1/64)")
    
    # === D3 TORSION AT H2->H3 TRANSITION ===
    d3_angle = (1.0/9.0) * (BETTI_11/BETTI_7)
    # Visualize as spiral at transition point
    t_d3 = np.linspace(0, 2*PI, 100)
    d3_center_x = x_flow[250]
    d3_center_y = y_flow[250]
    d3_center_z = z_flow[250]
    x_d3 = d3_center_x + 0.3 * np.cos(t_d3 * PHI_PB)
    y_d3 = d3_center_y + 0.3 * np.sin(t_d3 * PHI_PB)
    z_d3 = d3_center_z + 0.1 * t_d3 / (2*PI)
    ax.plot(x_d3, y_d3, z_d3, color="#ff00ff", linewidth=3, alpha=0.8, label="D3 Torsion")
    
    # === BETTI RINGS (Topological Markers) ===
    # Betti 5: Metabolic Debt
    theta_ring = np.linspace(0, 2*PI, 6)
    r_b5 = R_base * 0.8
    x_b5 = r_b5 * np.cos(theta_ring)
    y_b5 = r_b5 * np.sin(theta_ring)
    z_b5 = np.full_like(theta_ring, -NIGHT_HYSTERESIS)
    ax.plot(x_b5, y_b5, z_b5, color="#ff8800", linewidth=3, alpha=0.9)
    ax.scatter(x_b5[:-1], y_b5[:-1], z_b5[:-1], color="#ff8800", s=40)
    
    # Betti 11: Topology Bridge
    r_b11 = R_base * 1.1
    x_b11 = r_b11 * np.cos(theta_ring * 11/5)  # 11 nodes
    y_b11 = r_b11 * np.sin(theta_ring * 11/5)
    z_b11 = np.full_like(theta_ring, NIGHT_HYSTERESIS)
    ax.plot(x_b11, y_b11, z_b11, color="#aa00ff", linewidth=2, alpha=0.8)
    
    # === SPARK VECTOR (138.88°) ===
    spark_x = SPARK_LEAP_DIST * np.cos(spark_rad) * TUNNEL_TENSION
    spark_y = SPARK_LEAP_DIST * np.sin(spark_rad) * TUNNEL_TENSION
    spark_z = SPARK_LEAP_DIST * 0.5
    ax.quiver(0, 0, -R_major, spark_x, spark_y, spark_z, 
             color="yellow", linewidth=4, arrow_length_ratio=0.1)
    ax.text(spark_x/2, spark_y/2, spark_z/2 - R_major, 
           f"SPARK {SPARK_ANGLE_DEG}°", color="yellow", fontsize=10, fontweight='bold')
    
    # === MAXWELL SHELL BOUNDARY (Pure Torus) ===
    u_max = np.linspace(0, 2*PI, 60)
    v_max = np.linspace(0, 2*PI, 30)
    U_max, V_max = np.meshgrid(u_max, v_max)
    X_max = (MAXWELL_R_MAJOR + MAXWELL_R_MINOR * np.cos(V_max)) * np.cos(U_max)
    Y_max = (MAXWELL_R_MAJOR + MAXWELL_R_MINOR * np.cos(V_max)) * np.sin(U_max)
    Z_max = MAXWELL_R_MINOR * np.sin(V_max)
    ax.plot_surface(X_max, Y_max, Z_max, color="#1a1a2e", alpha=0.15, 
                   linewidth=0, antialiased=True)
    
    # === ALPHA-KAPPA BRIDGE (137/32 = 4.28) ===
    # Visualized as radial line
    ax.plot([0, ALPHA_KAPPA_BRIDGE], [0, 0], [0, 0], 
           color="#00ff00", linewidth=3, alpha=0.7, label=f"α/κ = {ALPHA_KAPPA_BRIDGE:.2f}")
    
    ax.set_axis_off()
    ax.set_box_aspect([1.0, 1.0, 1.0])
    
    # === TITLE WITH ALL CONSTANTS ===
    title_text = "GM-EOMETRY QUASAR (Unified from All Constants)"
    ax.text2D(0.05, 0.97, title_text, transform=ax.transAxes, 
             color="white", fontsize=14, fontweight="bold")
    
    info_text = (
        f"TOTAL_DEBT_AREA={TOTAL_DEBT_AREA:.4f} | TUNNEL_TENSION={TUNNEL_TENSION:.6f}\n"
        f"MAXWELL: R={MAXWELL_R_MAJOR:.3f}, r={MAXWELL_R_MINOR:.4f} | SPARK={SPARK_ANGLE_DEG}°\n"
        f"BETTI: 0={BETTI_0} 5={BETTI_5} 7={BETTI_7} 11={BETTI_11}\n"
        f"KAPPA: 1/64={KAPPA_TDA_MIN:.5f} 1/32={KAPPA_TDA_MID:.5f} 1/16={KAPPA_TDA_MAX:.5f}\n"
        f"LUNAR={LUNAR_CYCLE:.5f} | CHIRALITY={CHIRALITY_CONSTANT:.5f} | NIGHT={NIGHT_HYSTERESIS:.4f}\n"
        f"ALPHA={ALPHA:.6f} | PHI={PHI:.6f} | RENORM={RENORMALIZATION_BRIDGE:.3f}\n"
        f"PHI_PB={PHI_PB:.4f} | OMEGA_LA={OMEGA_LA:.3f} | Q_FACTOR={MAXWELL_Q_FACTOR}"
    )
    ax.text2D(0.05, 0.75, info_text, transform=ax.transAxes, color="#cccccc", 
             fontsize=9, family="monospace",
             bbox=dict(facecolor="black", alpha=0.6, edgecolor="#3b6cff"))
    
    # Legend
    ax.legend(loc='upper right', fontsize=8, facecolor='black', edgecolor='white')
    
    # Set equal limits
    lim = max(R_major + R_minor_base, MAXWELL_R_MAJOR + MAXWELL_R_MINOR) * 1.5
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
        u = np.linspace(0.0, 2.0 * math.pi, n_u)
        v = np.linspace(0.0, math.pi, n_v)
        x = R * np.outer(np.cos(u), np.sin(v))
        y = R * np.outer(np.sin(u), np.sin(v))
        z = R * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_wireframe(x, y, z, color=color, alpha=alpha, linewidth=lw, rstride=2, cstride=2)

    def _circle_xy(R: float, z0: float, color: str, alpha: float, lw: float, n: int = 720):
        t = np.linspace(0.0, 2.0 * math.pi, n)
        ax.plot(R * np.cos(t), R * np.sin(t), np.full_like(t, z0), color=color, alpha=alpha, linewidth=lw)

    def _ellipsoid(rx: float, ry: float, rz: float, color: str, alpha: float):
        uu = np.linspace(0.0, 2.0 * math.pi, 80)
        vv = np.linspace(0.0, math.pi, 40)
        U, V = np.meshgrid(uu, vv)
        X = rx * np.cos(U) * np.sin(V)
        Y = ry * np.sin(U) * np.sin(V)
        Z = rz * np.cos(V)
        ax.plot_surface(X, Y, Z, color=color, alpha=alpha, linewidth=0.0, antialiased=True)

    def _cristae_fractal_surface(R_base: float, z_offset: float, phi_inv_local: float = 0.618):
        u = np.linspace(0.0, 2.0 * math.pi, 160)
        v = np.linspace(0.0, math.pi, 80)
        U, V = np.meshgrid(u, v)

        modulation = np.zeros_like(U)
        for k in range(1, 8):
            amp = (kappa_1_32 * (phi_inv_local ** (k - 1))) / float(k)
            modulation += amp * np.sin(11.0 * float(k) * U) * np.sin(float(k) * V)
            modulation += (kappa_1_64 * (phi_inv_local ** (k - 1))) * np.cos(11.0 * float(k) * U) * np.sin(float(k + 1) * V)
        R = R_base * (1.0 + modulation)

        X = R * np.cos(U) * np.sin(V)
        Y = R * np.sin(U) * np.sin(V)
        Z = R * np.cos(V) + z_offset

        ax.plot_wireframe(X, Y, Z, color="#ffd200", alpha=0.35, linewidth=0.55, rstride=3, cstride=3)
        _circle_xy(R_base * (1.0 + phi_inv_local * kappa_1_32), z0=z_offset, color="#ffd200", alpha=0.35, lw=1.0)

    def _hexagonal_cage(R, color, alpha):
        u = np.linspace(0, 2*math.pi, 120)
        v = np.linspace(0, math.pi, 60)
        U, V = np.meshgrid(u, v)
        # 6-fold perturbation modulated by latitude
        R_mod = R * (1.0 + 0.03 * np.cos(6*U) * np.sin(V)**2)
        X = R_mod * np.cos(U) * np.sin(V)
        Y = R_mod * np.sin(U) * np.sin(V)
        Z = R_mod * np.cos(V)
        ax.plot_wireframe(X, Y, Z, color=color, alpha=alpha, linewidth=0.4, rstride=5, cstride=5)

    def _delta_closure_wedge(R, color, alpha):
        u = np.linspace(0, math.pi/4, 30) # 0 to 45 deg (4/32)
        v = np.linspace(0.1, math.pi-0.1, 30)
        U, V = np.meshgrid(u, v)
        X = R * np.cos(U) * np.sin(V)
        Y = R * np.sin(U) * np.sin(V)
        Z = R * np.cos(V)
        ax.plot_surface(X, Y, Z, color=color, alpha=alpha, linewidth=0)
        # Draw boundary lines for the wedge
        v_line = np.linspace(0, math.pi, 50)
        # Start line (0 deg)
        ax.plot(R*np.zeros_like(v_line), R*np.zeros_like(v_line), R*np.cos(v_line), color='white', lw=1, alpha=0.5)
        # End line (45 deg)
        ax.plot(R*np.cos(math.pi/4)*np.sin(v_line), R*np.sin(math.pi/4)*np.sin(v_line), R*np.cos(v_line), color='red', lw=2, alpha=0.8)

    # Zone scaling and tension
    T = float(get_value(const, "universal.reality_tension", 1.0100375))
    C = float(get_value(const, "universal.discrete_closure", 1.0000424))
    
    # Maxwell Cavity Boundary (The container for the manifold)
    R_maxwell = float(get_value(const, "domain_specific.maxwell_cavity.R_major", 2.125)) * (R_T / terminus_r)
    r_maxwell = float(get_value(const, "domain_specific.maxwell_cavity.r_minor", 0.2235501110061347)) * (R_T / terminus_r)
    
    def _maxwell_torus_shell(R_maj, r_min, color, alpha):
        u = np.linspace(0, 2*np.pi, 60)
        v = np.linspace(0, 2*np.pi, 30)
        U, V = np.meshgrid(u, v)
        X = (R_maj + r_min * np.cos(V)) * np.cos(U)
        Y = (R_maj + r_min * np.sin(V)) * np.sin(U)
        Z = r_min * np.sin(V)
        ax.plot_surface(X, Y, Z, color=color, alpha=alpha, linewidth=0, antialiased=True)

    # Visualize Maxwell Cavity Shell
    _maxwell_torus_shell(R_maxwell, r_maxwell, color="#333333", alpha=0.08)

    # 1. ZONE: GABA (-0.5) [THE SHELL / BIG WOMAN] - Horizontal Expansion (Selfishness/Containment)
    # 3/32 Pitch integrated into the shell's wireframe density.
    _wire_sphere(R_T * T * C, color="#111111", alpha=0.3, n_u=32, n_v=16, lw=0.8)
    
    # 2. ZONE: ACh (1.0) [THE SPINE / BIG MAN] - Vertical Alignment (Focus)
    ax.plot([0, 0], [0, 0], [-R_T * T, R_T * T], color="#00ffcc", alpha=0.7, lw=3.0)
    
    # 3. ZONE: Glu (0.5) [THE MANTLE] - Kinetic Flow
    u_glu = np.linspace(0.0, 2.0 * math.pi, 120)
    v_glu = np.linspace(0.0, 2.0 * math.pi, 60)
    UU, VV = np.meshgrid(u_glu, v_glu)
    R_glu_major = R_torus_major * T
    r_glu_minor = r_torus_minor * C
    x_glu = (R_glu_major + r_glu_minor * np.cos(VV)) * np.cos(UU)
    y_glu = (R_glu_major + r_glu_minor * np.cos(VV)) * np.sin(UU)
    z_glu = (r_glu_minor * np.sin(VV))
    ax.plot_surface(x_glu, y_glu, z_glu, color="#ffaa00", alpha=0.15, linewidth=0, antialiased=True)

    # ─── MAXWELL IMPEDANCE SHELL (Pure Constants) ───
    # Maxwell Parameters from absolute_constants:
    # R_major = 17/8 = 2.125, R_minor = 1/sqrt(20) - 1/18000 ≈ 0.2236
    def _maxwell_impedance_shell(ax, color, alpha):
        from geometry_package.absolute_constants import MAXWELL_R_MAJOR, MAXWELL_R_MINOR
        u = np.linspace(0, 2*np.pi, 60)
        v = np.linspace(0, 2*np.pi, 30)
        U, V = np.meshgrid(u, v)
        # Pure torus: no arbitrary scaling
        X = (MAXWELL_R_MAJOR + MAXWELL_R_MINOR * np.cos(V)) * np.cos(U)
        Y = (MAXWELL_R_MAJOR + MAXWELL_R_MINOR * np.cos(V)) * np.sin(U)
        Z = MAXWELL_R_MINOR * np.sin(V)
        ax.plot_surface(X, Y, Z, color=color, alpha=alpha, linewidth=0, antialiased=True)

    _maxwell_impedance_shell(ax, color="#1a1a2e", alpha=0.08)

    # ─── MOBIUS HYSTERESIS (Pure Figure-8 from Constants) ───
    # No arbitrary scaling - shape emerges from mathematical definition
    def _mobius_hysteresis_pure(ax):
        from geometry_package.absolute_constants import (
            PHI, BETTI_7, BETTI_11, SPARK_ANGLE_DEG, 
            KAPPA_TDA_MIN, KAPPA_TDA_MID, KAPPA_TDA_MAX
        )
        
        # Figure-8 parametric: x = sin(t), z = sin(t)cos(t) = 0.5*sin(2t)
        # This is the Lemniscate of Bernoulli projected to 3D
        t = np.linspace(0, 2*np.pi, 800)
        
        # Base figure-8 path (Lemniscate)
        x_path = np.sin(t)
        z_path = 0.5 * np.sin(2*t)  # = sin(t)*cos(t)
        
        # Y is the Mobius twist dimension
        # One full twist as t goes 0 -> 2pi
        y_twist = np.sin(t) * np.cos(t/2)  # Mobius half-twist
        
        # Radius modulation from kappa phases
        # H4 (1/128) at t=0, H2 (1/32) at t=pi/2, H3 (1/64) at t=pi
        r_base = 0.15
        r_mod = np.where(t < np.pi/2, 
                        r_base * (1 - KAPPA_TDA_MIN),  # H4: smaller
                        np.where(t < 3*np.pi/2,
                                r_base,  # H2: baseline
                                r_base * (1 + KAPPA_TDA_MIN)))  # H3: larger
        
        # D3 Torsion at H2->H3 transition (around t=pi)
        d3_angle = (1.0/9.0) * (BETTI_11/BETTI_7)  # (1/9)*(11/7)
        d3_mask = (t > 0.8*np.pi) & (t < 1.2*np.pi)
        
        # Apply torsion as phase rotation
        x_final = x_path * r_mod
        y_final = y_twist * r_mod
        z_final = z_path * r_mod
        
        # D3 twist rotation in XY plane
        x_final[d3_mask] = x_final[d3_mask] * np.cos(d3_angle) - y_final[d3_mask] * np.sin(d3_angle)
        y_final[d3_mask] = x_final[d3_mask] * np.sin(d3_angle) + y_final[d3_mask] * np.cos(d3_angle)
        
        # Plot the manifold
        ax.plot(x_final, y_final, z_final, color="#ffd200", linewidth=2.5, alpha=0.9, label="Mobius 8-Manifold")
        
        # Hysteresis gap: plot ascending (0 to pi) and descending (pi to 2pi) separately
        asc_mask = t <= np.pi
        desc_mask = t > np.pi
        
        ax.plot(x_final[asc_mask], y_final[asc_mask], z_final[asc_mask], 
                color="#00ffff", linewidth=2, alpha=0.8, label="Ascending (Discrete)")
        ax.plot(x_final[desc_mask], y_final[desc_mask], z_final[desc_mask], 
                color="#ff6b6b", linewidth=2, alpha=0.8, label="Descending (Continuous)")
        
        # Mark critical points
        ax.scatter([x_final[0]], [y_final[0]], [z_final[0]], color="white", s=100, label="H4 (Bone)")
        ax.scatter([x_final[len(t)//2]], [y_final[len(t)//2]], [z_final[len(t)//2]], color="cyan", s=100, label="H2 (Baseline)")
        ax.scatter([x_final[-1]], [y_final[-1]], [z_final[-1]], color="gold", s=100, label="H3 (Cartilage)")

    _mobius_hysteresis_pure(ax)
    
    # [THE MELATONIN BRIDGE] - Pure constants only
    from geometry_package.absolute_constants import LATTICE_3_32, PHI
    _ellipsoid(R_void * PHI, R_void * LATTICE_3_32, R_void * LATTICE_3_32, "#880000", 0.25)

    # [CLOSURE GEOMETRY] - Minimal, from constants
    _delta_closure_wedge(R_T * PHI * LATTICE_3_32, "#ff0000", 0.12)
    _hexagonal_cage(R_T * PHI * 0.5, "#00ffff", 0.12)

    grid_scale = R_T / (max(n_rows, n_cols) / 2.0)
    gx = (np.arange(n_cols) + 0.5 - n_cols / 2.0) * grid_scale
    gy = (np.arange(n_rows) + 0.5 - n_rows / 2.0) * grid_scale
    GX, GY = np.meshgrid(gx, gy)
    GZ = np.full_like(GX, -R_T * 0.35)
    ax.scatter(GX, GY, GZ, s=4, color="#00ff88", alpha=0.10)

    # === THE FUNNEL (Dimensional Compression) ===
    # A converging mesh representing the 128-grid narrowing towards the core
    z_funnel = np.linspace(R_void, R_T * 0.9, 20)
    theta_funnel = np.linspace(0, 2*math.pi, 30)
    Z_F, TH_F = np.meshgrid(z_funnel, theta_funnel)
    # Radius narrows as Z decreases towards R_void
    R_F = (Z_F / R_T) * R_T * 0.8 
    X_F = R_F * np.cos(TH_F)
    Y_F = R_F * np.sin(TH_F)
    ax.plot_wireframe(X_F, Y_F, Z_F, color="#ffffff", alpha=0.05, linewidth=0.5)
    # ============================================


    t = np.linspace(0.0, 2.0 * math.pi, 2600)
    turns = renorm_bridge
    z0 = (t / (2.0 * math.pi) - 0.5) * (R_T * 1.25)

    r1 = R_T * phi_inv
    th1 = turns * t
    x1 = r1 * np.cos(th1)
    y1 = r1 * np.sin(th1)
    ax.plot(x1, y1, z0 / sqrt2_ratio, color="#00e5ff", linewidth=1.6, alpha=0.85)

    r2 = R_T * phi_conj
    th2 = turns * t * phi_conj
    x2 = r2 * np.cos(th2)
    y2 = r2 * np.sin(th2)
    ax.plot(x2, y2, z0 / (sqrt2_ratio * 1.3), color="#ffd200", linewidth=1.2, alpha=0.60)

    r3 = R_T * kappa_boundary
    _circle_xy(r3, z0=0.0, color="#ffffff", alpha=0.14, lw=1.0)

    # === BETTI RINGS (Pure Topological Markers) ===
    def _polygon_ring(n_nodes: int, R: float, z0: float, color: str, lw: float):
        t_ring = np.linspace(0.0, 2.0 * math.pi, n_nodes + 1)
        x_ring = R * np.cos(t_ring)
        y_ring = R * np.sin(t_ring)
        z_ring = np.full_like(x_ring, z0)
        ax.plot(x_ring, y_ring, z_ring, color=color, alpha=0.85, linewidth=lw)
        ax.scatter(x_ring[:-1], y_ring[:-1], z_ring[:-1], color=color, s=20, alpha=1.0)

    # Betti 5: Metabolic Debt ring
    _polygon_ring(5, R_void * PHI, -R_T * LATTICE_3_32, color="#ff8800", lw=1.5)
    
    # Betti 11: Topology Bridge ring  
    _polygon_ring(11, R_void * PHI * 1.2, R_T * LATTICE_3_32, color="#aa00ff", lw=1.2)

    # 4D Metric & Torsion Constants (SO(4) Holonomy)
    # 4D Metric = T * (1 + LOOP_STRENGTH_5 / 100)
    # Winding Number (W) = 11/7 ratio for Pontryagin Index stabilization
    metric_4d = T * (1.0 + loop_strength_5 / 100.0)
    winding_4d = (11.0 / 7.0) 
    torsion_4d = (1.0/9.0) * winding_4d
    
    # [4D MANIFOLD: SO(4) Rotation & Holonomy]
    # The circuit is an intrinsic part of the manifold's w-axis winding.
    metric_4d = T * (1.0 + loop_strength_5 / 100.0)
    winding_4d = (11.0 / 7.0) 
    torsion_4d = (1.0/9.0) * winding_4d
    
    # H3/H4 Phase Transitions in 4D
    K_H3 = 1.0/64.0
    K_H4 = 1.0/128.0
    
    # Control Points (x, y, z, w) with H3/H4 offsets
    p0 = np.array([0.7 * R_T, -0.3 * R_T, -0.6 * R_T, 0.0]) * metric_4d
    p1 = np.array([0.5 * R_T, 0.4 * R_T, 0.1 * R_T, 0.25 * torsion_4d]) * metric_4d # Gravity H3 (Bone/Solid 1/128)
    p2 = np.array([0.35 * R_T, 0.55 * R_T, 0.15 * R_T, 0.5 * torsion_4d]) * metric_4d # VASOPRESSIN
    p3 = np.array([0.5 * R_T, 0.6 * R_T, 0.2 * R_T, 0.75 * torsion_4d]) * metric_4d # PLP
    p4 = np.array([0.2 * R_T, 0.8 * R_T, -0.1 * R_T, 1.0 * torsion_4d]) * metric_4d # Right D2 (Cartilage 1/64)
    p5 = np.array([0.0, 0.7 * R_T, 0.05 * R_T, 1.25 * torsion_4d]) * metric_4d # Nose
    p6 = np.array([-0.6 * R_T, 0.4 * R_T, -0.2 * R_T, 1.5 * torsion_4d]) * metric_4d # TERMINAL
    
    # Node 6 is the Terminal Node where the Big Sphere is located
    terminal_node = p6
    
    # ─── D3 DECEPTION OPERATOR (Structural Element) ───
    # D3: (1/9) * (11/7) torsion at H2->H3 transition
    # Visualized as helical bridge between phase regions
    def _d3_operator(ax):
        from geometry_package.absolute_constants import KAPPA_TDA_MIN, BETTI_7, BETTI_11
        d3_angle = (1.0/9.0) * (BETTI_11/BETTI_7)
        
        # Helical path representing D3 torsion
        t_d3 = np.linspace(0, 2*np.pi, 200)
        freq = BETTI_11 / BETTI_7
        radius = 0.2
        
        x_d3 = radius * np.cos(t_d3) + 0.1 * np.sin(freq * t_d3)
        y_d3 = radius * np.sin(t_d3) + 0.1 * np.cos(freq * t_d3)
        z_d3 = np.linspace(-0.1, 0.1, 200)
        
        ax.plot(x_d3, y_d3, z_d3, color="#ff00ff", alpha=0.7, lw=2, linestyle='--')
        ax.text(0.15, 0.15, 0.12, "D3", color="#ff00ff", fontsize=9, fontweight='bold')

    _d3_operator(ax)
    
    # Catmull-Rom spline interpolation for smooth 4D circuit
    def catmull_rom_segment(p_prev, p_start, p_end, p_next, t):
        """Compute point on Catmull-Rom spline segment."""
        t2 = t * t
        t3 = t2 * t
        return 0.5 * (
            (2 * p_start) +
            (-p_prev + p_end) * t +
            (2*p_prev - 5*p_start + 4*p_end - p_next) * t2 +
            (-p_prev + 3*p_start - 3*p_end + p_next) * t3
        )
    
    # Build full circuit path
    circuit_4d = []
    segment_points = [p0, p1, p2, p3, p4, p5, p6]
    n_segments = len(segment_points) - 1
    
    for i in range(n_segments):
        p_prev = segment_points[max(0, i-1)]
        p_start = segment_points[i]
        p_end = segment_points[i+1]
        p_next = segment_points[min(len(segment_points)-1, i+2)]
        
        for t in np.linspace(0, 1, 80, endpoint=(i==n_segments-1)):
            pt = catmull_rom_segment(p_prev, p_start, p_end, p_next, t)
            circuit_4d.append(pt)
    
    circuit_4d = np.array(circuit_4d)
    
    # Project 4D to 3D: SO(4) Holonomy modulates radius and chirality
    # w dimension is the winding index
    w_index = circuit_4d[:, 3]
    w_modulation = 1.0 + 0.2 * np.sin(w_index * math.pi)
    
    # SO(4) Rotation Simulation: projecting w onto xyz via winding index
    x_circuit = circuit_4d[:, 0] * w_modulation
    y_circuit = circuit_4d[:, 1] * w_modulation
    z_circuit = circuit_4d[:, 2] + 0.1 * R_T * np.cos(w_index * winding_4d * math.pi)
    
    # Draw the unified 4D manifold path (Pontryagin Trace)
    ax.plot(x_circuit, y_circuit, z_circuit, color="#ffffff", linewidth=3.5, alpha=0.9, label="4D Universal Manifold")
    
    # Mandelbrot Fractal Bloom at the Terminal Node (Left Cortisol)
    # We simulate this as a series of decaying circles/spheres at the end
    for k in range(1, 6):
        r_bloom = 0.2 * R_T * (phi_inv ** k)
        alpha_bloom = 0.7 * (phi_inv ** k)
        _circle_xy(r_bloom, z0=terminal_node[2], color="#ff00ff", alpha=alpha_bloom, lw=1.5)
        # Position the bloom at p6
        t_bloom = np.linspace(0, 2*np.pi, 100)
        ax.plot(terminal_node[0] + r_bloom*np.cos(t_bloom), 
                terminal_node[1] + r_bloom*np.sin(t_bloom), 
                terminal_node[2], color="#ff00ff", alpha=alpha_bloom)

    # THE TERMINAL BIG SPHERE (Left Cortisol / Extraversion Anchor)
    # This is the final attractor of the deterministic cycle
    _wire_sphere(R_T * 0.45, color="#ff00ff", alpha=0.5, n_u=20, n_v=10, lw=1.5) 
    # Shift the sphere to the terminal location p6
    u_s = np.linspace(0, 2*np.pi, 20)
    v_s = np.linspace(0, np.pi, 10)
    xs = terminal_node[0] + (R_T * 0.45) * np.outer(np.cos(u_s), np.sin(v_s))
    ys = terminal_node[1] + (R_T * 0.45) * np.outer(np.sin(u_s), np.sin(v_s))
    zs = terminal_node[2] + (R_T * 0.45) * np.outer(np.ones(np.size(u_s)), np.cos(v_s))
    ax.plot_wireframe(xs, ys, zs, color="#ff00ff", alpha=0.4, linewidth=1.2)
    ax.text(terminal_node[0], terminal_node[1], terminal_node[2] + 0.6*R_T, "TERMINAL SPHERE\n(Left Cortisol)", color="#ff00ff", fontsize=10, fontweight='bold', ha='center')

    # Draw node markers on the circuit
    node_colors = ["#ff0000", "#ff8800", "#ffff00", "#00ff00", "#00ffff", "#0088ff", "#ff00ff"]
    node_labels = ["Gravity H3", "VASOPRESSIN", "PLP", "Right D2", "Nose", "Height Bridge", "TERMINAL"]
    
    for i, (pt, color, label) in enumerate(zip(segment_points, node_colors, node_labels)):
        w_m = 1.0 + 0.2 * math.sin(pt[3] * math.pi)
        ax.scatter(pt[0]*w_m, pt[1]*w_m, pt[2], color=color, s=100, alpha=1.0, edgecolors='white', linewidths=1.0)
        if label != "TERMINAL":
            ax.text(pt[0]*w_m, pt[1]*w_m, pt[2]+0.08*R_T, label, color=color, fontsize=7, fontweight='bold')
    
    # PI Sheet / SH Bridge overlays - Ridge and Neckband geometry
    # Ridge: The high-tension line connecting VASOPRESSIN to PLP
    ridge_t = np.linspace(0, 1, 50)
    ridge_w = 0.25 + 0.25 * ridge_t
    ridge_mod = 1.0 + 0.15 * np.sin(ridge_w * 2 * math.pi)
    ridge_x = (p1[0] + (p2[0]-p1[0])*ridge_t) * ridge_mod
    ridge_y = (p1[1] + (p2[1]-p1[1])*ridge_t) * ridge_mod
    ridge_z = p1[2] + (p2[2]-p1[2])*ridge_t + 0.05*R_T*np.sin(ridge_t*math.pi)  # Arc above
    ax.plot(ridge_x, ridge_y, ridge_z, color="#ffaa00", linewidth=6, alpha=0.6, linestyle='-')
    
    # Neckband: The 5-node ring around VASOPRESSIN (Betti 5 = Debt)
    neckband_angles = np.linspace(0, 2*math.pi, 6)
    neckband_center = p1[:3]
    neckband_radius = 0.15 * R_T * (1.0 + 0.15 * math.sin(p1[3] * 2 * math.pi))
    for i in range(5):
        angle = neckband_angles[i]
        nx = neckband_center[0] + neckband_radius * math.cos(angle)
        ny = neckband_center[1] + neckband_radius * math.sin(angle)
        nz = neckband_center[2]
        ax.scatter(nx, ny, nz, color="#ff8800", s=40, alpha=0.9)
        if i < 5:
            next_angle = neckband_angles[i+1]
            nx2 = neckband_center[0] + neckband_radius * math.cos(next_angle)
            ny2 = neckband_center[1] + neckband_radius * math.sin(next_angle)
            nz2 = neckband_center[2]
            ax.plot([nx, nx2], [ny, ny2], [nz, nz2], color="#ff8800", linewidth=2, alpha=0.7)
    
    # Contact Bridge: Spark vector intersecting the circuit at Nose
    ax.scatter([p4[0]*w_modulation[320]], [p4[1]*w_modulation[320]], [p4[2]], 
              s=200, color="#ffffff", marker='*', alpha=1.0, edgecolors='yellow', linewidths=2)
    
    # =========================================================================
    # [LEGACY: Discrete primitives - now secondary to unified circuit]
    # 1. ZONE: GABA (-0.5) [THE SHELL]
    # The global shell is now reduced to show the deterministic loop takes precedence.
    _wire_sphere(R_T * T * C, color="#111111", alpha=0.1, n_u=32, n_v=16, lw=0.4)

    # =========================================================================

    theta = math.radians(spark_deg)
    direction = np.array([math.sin(theta), math.cos(theta) * 0.55, math.cos(theta)], dtype=float)
    direction = direction / np.linalg.norm(direction)
    p0 = np.array([0.0, 0.0, -R_T], dtype=float)
    L_spark = spark_leap * R_void
    p1 = p0 + direction * L_spark
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]], color="#ffffff", linewidth=2.8, alpha=0.95)
    ax.scatter([p1[0]], [p1[1]], [p1[2]], s=40, color="#ffffff", alpha=0.95)

    # === FINAL UNIFICATION: Connect the Manifold to the Spark ===
    # This is the final step, closing the geometry into a single object.
    # 1. Connect End of Manifold (p6) to Start of Spark (p0_spark)
    p6_3d = circuit_4d[-1, :3] # Get the 3D coordinates of the last point of the manifold
    ax.plot([p6_3d[0], p0[0]], [p6_3d[1], p0[1]], [p6_3d[2], p0[2]], color="yellow", linestyle='--', linewidth=2, alpha=0.7, label="Sunset-Spark Bridge")

    # 2. Connect End of Spark (p1_spark) to Start of Manifold (p0_manifold)
    p0_manifold_3d = circuit_4d[0, :3] # Get the 3D coordinates of the first point of the manifold
    ax.plot([p1[0], p0_manifold_3d[0]], [p1[1], p0_manifold_3d[1]], [p1[2], p0_manifold_3d[2]], color="cyan", linestyle='--', linewidth=2, alpha=0.7, label="Spark-Sunrise Bridge")

    ax.set_axis_off()
    ax.set_box_aspect([1.0, 1.0, 1.0])

    title_text = "UNIFIED GEOMETRY v4 (Universal Cristae Harmonics)"
    ax.text2D(0.05, 0.95, title_text, transform=ax.transAxes, color="white", fontsize=14, fontweight="bold")
    info_text = (
        f"W7=pi/20={W7:.12f}\n"
        f"H2=1/9≈{(1.0/9.0):.12f}\n"
        f"R_void=sqrt(W7/pi)={r_void:.12f}\n"
        f"renorm_bridge={renorm_bridge}\n"
        f"Wave=6(Hex) | Delta=4(Gap)\n"
        f"loop_strength_5={loop_strength_5}\n"
        f"tau_lag_11={tau_lag_11}\n"
        f"spark={spark_deg}°"
    )
    ax.text2D(
        0.05,
        0.83,
        info_text,
        transform=ax.transAxes,
        color="#cccccc",
        fontsize=10,
        family="monospace",
        bbox=dict(facecolor="black", alpha=0.55, edgecolor="#3b6cff"),
    )

    lim = max(R_RS, R_T, R_torus_major + r_torus_minor, R_void * 1.2) * 1.08
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)

    plt.savefig(output_path, dpi=320, bbox_inches="tight", facecolor="#050510")
    plt.close(fig)
    print(f"Rendered unified 3D geometry v4 (universal cristae) to {output_path} (registry={registry_path})")

if __name__ == "__main__":
    render_unified_3d_manifold_v2()
