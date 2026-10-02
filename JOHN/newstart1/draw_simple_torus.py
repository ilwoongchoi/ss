import matplotlib
matplotlib.use('Agg') # Force headless
import matplotlib.pyplot as plt
import numpy as np
import math

def render_simple_torus(output_path="simple_torus.png"):
    fig = plt.figure(figsize=(12, 12), facecolor='#e0e0e0')
    ax = fig.add_subplot(111, projection='3d')

    # Simple, clean torus parameters, ignoring all constants.
    major_R = 3.0
    minor_r = 1.0

    u = np.linspace(0, 2 * np.pi, 128)
    v = np.linspace(0, 2 * np.pi, 64)
    U, V = np.meshgrid(u, v)
    X = (major_R + minor_r * np.cos(V)) * np.cos(U)
    Y = (major_R + minor_r * np.cos(V)) * np.sin(U)
    Z = minor_r * np.sin(V)

    ax.plot_wireframe(X, Y, Z, color="#4a90e2", alpha=0.3, linewidth=1.0, rstride=8, cstride=8)

    # Add Betti rings to the poles
    def _draw_betti_ring(n_nodes, major_R, minor_r, z_offset, color, lw):
        theta = np.linspace(0, 2 * np.pi, n_nodes + 1)
        # The ring lies on the surface of the torus tube
        ring_radius = major_R
        x = ring_radius * np.cos(theta)
        y = ring_radius * np.sin(theta)
        z = np.full_like(theta, z_offset)
        ax.plot(x, y, z, color=color, alpha=0.9, linewidth=lw)
        ax.scatter(x[:-1], y[:-1], z[:-1], color=color, s=45, alpha=1.0, edgecolors='white', linewidths=0.5)

    # Betti-11 (North Pole / Bridge)
    _draw_betti_ring(11, major_R, minor_r, minor_r, color="#aa00ff", lw=2.0)

    # Betti-5 (South Pole / Debt)
    _draw_betti_ring(5, major_R, minor_r, -minor_r, color="#ff8800", lw=2.5)

    # Add the Uroboros Path (Spark)
    p_start_spark = np.array([0, 0, -minor_r]) # Center of Betti-5 ring
    p_end_spark = np.array([0, 0, minor_r])   # Center of Betti-11 ring
    ax.plot([p_start_spark[0], p_end_spark[0]], [p_start_spark[1], p_end_spark[1]], [p_start_spark[2], p_end_spark[2]], color="#ff0000", linewidth=2.5, alpha=1.0, linestyle='-')

    # Add the Path of Consciousness
    def _draw_consciousness_path(major_R, minor_r, num_winds=11.0/7.0):
        path_points = []
        # Generate points for a smooth spline from North Pole to South Pole
        for i in range(200):
            t = i / 199.0  # t from 0 to 1
            u = 2 * np.pi * num_winds * t # Winding angle
            v = np.pi * t # Vertical angle from top (0) to bottom (pi)

            # Parametric equation for a path on a torus surface
            x = (major_R + minor_r * np.cos(v)) * np.cos(u)
            y = (major_R + minor_r * np.cos(v)) * np.sin(u)
            z = minor_r * np.sin(v)
            path_points.append([x, y, z])
        path = np.array(path_points)
        ax.plot(path[:,0], path[:,1], path[:,2], color="#ffffff", linewidth=3.0, alpha=0.95)

    _draw_consciousness_path(major_R, minor_r)
    ax.set_box_aspect([1.0, 1.0, 1.0])
    ax.set_axis_off()

    lim = major_R + minor_r + 0.5
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)

    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#e0e0e0')
    plt.close(fig)
    print(f"Rendered simple torus to {output_path}")

if __name__ == "__main__":
    render_simple_torus()
