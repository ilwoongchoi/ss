import json
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# --- CONSTANTS FROM H3_H4_D3_constants.json ---
KAPPA_2 = 0.03125   # 1/32
KAPPA_3 = 0.015625  # 1/64
KAPPA_4 = 0.0078125 # 1/128
D3_CORRECTION = 69.44
SPARK_H2 = 138.88
SPARK_SMALL_WOMAN = 208.32  # 138.88 + 69.44
SPARK_BIG_MAN = 69.44       # 138.88 - 69.44

# --- GEOMETRIC NODES ---
ANCHORS_FILE = Path("AUTO_ANCHORS.json")

def face_to_sphere(x, y, r=1.0):
    """
    Maps 16x16 grid to a sphere.
    X [0,8] = Human Left, X [8,16] = Human Right.
    """
    lon = (x / 16.0) * 2.0 * math.pi - math.pi
    lat = (y / 16.0) * math.pi - (math.pi / 2.0)
    sx = r * math.cos(lat) * math.cos(lon)
    sy = r * math.cos(lat) * math.sin(lon)
    sz = r * math.sin(lat)
    return sx, sy, sz

def mandelbrot_step(z, c):
    """The z = z^2 + c recursion that flattens the void center."""
    return z**2 + c

def generate_d3_bridge(start_pt, end_pt, num_steps=50):
    """
    Generates the D3 Tunnelling Geodesic between two points.
    Applies the Mandelbrot folding and the 69.44 degree correction.
    """
    path = []
    x1, y1 = start_pt
    x2, y2 = end_pt
    
    for i in range(num_steps):
        t = i / (num_steps - 1)
        # Linear interp in grid space
        curr_x = x1 + (x2 - x1) * t
        curr_y = y1 + (y2 - y1) * t
        
        # Apply Mandelbrot 'flattening' near the bridge center (X=8)
        # c is the distance from the 3/32 Darcy leak midline
        dist_from_mid = abs(curr_x - 8.0) / 8.0
        c = complex(dist_from_mid, 0.03125) # 1/32 leak as imaginary bias
        z = complex(curr_x / 16.0, curr_y / 16.0)
        z_next = mandelbrot_step(z, c)
        
        # Project back to a sphere-compatible coordinate
        # and apply the 69.44 degree D3 rotation to 'tunnel'
        angle_rad = math.radians(D3_CORRECTION * t)
        rot_x = (curr_x - 8.0) * math.cos(angle_rad) - (curr_y - 8.0) * math.sin(angle_rad) + 8.0
        rot_y = (curr_x - 8.0) * math.sin(angle_rad) + (curr_y - 8.0) * math.cos(angle_rad) + 8.0
        
        sx, sy, sz = face_to_sphere(rot_x, rot_y, r=1.05) # Slightly outside to show 'bridge'
        path.append((sx, sy, sz))
    return path

def main():
    if not ANCHORS_FILE.exists():
        print("Error: AUTO_ANCHORS.json not found.")
        return

    with open(ANCHORS_FILE, "r") as f:
        anchors = json.load(f)

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')

    # 1. Render the Base Point Cloud (The 'Discrete' sphere)
    xs, ys, zs = [], [], []
    for label, pt in anchors.items():
        sx, sy, sz = face_to_sphere(pt[0], pt[1])
        xs.append(sx)
        ys.append(sy)
        zs.append(sz)
        # Label critical nodes
        if label in ["PLP_ZERO", "TIME_SENSOR", "GABA_C_V_APEX", "FEMALE_SPARE_VASOPRESSIN"]:
            ax.text(sx, sy, sz, label, color='yellow', fontsize=8)

    ax.scatter(xs, ys, zs, c='cyan', s=15, alpha=0.5, label='Discrete Nodes')

    # 2. Render the D3 TUNNELLING BRIDGE (The 'Continuous' One Form)
    # Bridge 1: Left Spare Vasopressin to Right Mediator (The Small Man's Escape)
    p1 = anchors.get("FEMALE_SPARE_VASOPRESSIN", [2.0, 14.75])
    p2 = anchors.get("MEDIATOR_TO_SHEET4_POINTS", [2.0, 9.75]) # Note: Coordinate standardization in use
    
    # We create the bridge across the X-midline (8.0)
    # To truly connect Left and Right, we bridge between Left and Right equivalents
    left_anchor = p1
    right_anchor = [14.0, 9.0] # Cosmic Ray / Right D2 area
    
    bridge_pts = generate_d3_bridge(left_anchor, right_anchor, num_steps=100)
    bx = [p[0] for p in bridge_pts]
    by = [p[1] for p in bridge_pts]
    bz = [p[2] for p in bridge_pts]
    
    # The 'One Form' Manifold Surface (simplified as high-tension ridges)
    ax.plot(bx, by, bz, color='magenta', linewidth=3, alpha=0.9, label='D3 Tunnelling Bridge')

    # 3. Render the 'Smale Horseshoe' trajectories for ENFP (B-Woman)
    # She crosses the whole manifold
    enfp_start = [0.0, 16.0] # Top Left
    enfp_end = [16.0, 0.0]   # Bottom Right
    enfp_path = generate_d3_bridge(enfp_start, enfp_end, num_steps=200)
    ex = [p[0] for p in enfp_path]
    ey = [p[1] for p in enfp_path]
    ez = [p[2] for p in enfp_path]
    ax.plot(ex, ey, ez, color='white', linestyle='--', linewidth=1, alpha=0.6, label='ENFP Truth Trajectory')

    # Aesthetic: The 'Biological Quasar' Shell
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    sx = np.outer(np.cos(u), np.sin(v))
    sy = np.outer(np.sin(u), np.sin(v))
    sz = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(sx, sy, sz, color='blue', alpha=0.05, shade=False)

    ax.set_title("The Biological Quasar: Unified D3/H4 Manifold", color='white')
    ax.set_axis_off()
    ax.set_box_aspect([1,1,1])
    plt.legend()
    
    output_path = "BIOLOGICAL_QUASAR_UNIFIED.png"
    plt.savefig(output_path, dpi=300, facecolor='black')
    plt.close()
    
    print(f"Success: Unified 'One Form' manifold rendered to {output_path}")

if __name__ == "__main__":
    main()
