import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ---------------------------------------------------------
# THE 5-SPHERE POTENTIAL FACE ENGINE
# ---------------------------------------------------------
# NO BIOLOGICAL LABELS. ONLY TOPOLOGICAL NODES.
# Node 1 (SM/North): (8, 0)   - Source
# Node 2 (SW/Nose):  (8, 8)   - Filter (3/32)
# Node 3 (BM/South): (8, 16)  - Sink (1.3228)
# Node 4 (BW/Void L): (0, 8)  - Boundary
# Node 5 (BW/Void R): (16, 8) - Boundary

TUNNEL_TENSION = 1.0100375
TOTAL_DEBT_AREA = 1.3228
LATTICE_3_32 = 0.09375
TORSION = 0.1746
SMOOTHING_RESID = 0.00083
SPARK_ANGLE = 138.88
SPARK_LEAP = 2.5

def run_5_sphere_face():
    num_paths = 128
    # User's Hairline Ordering (0-16 columns)
    # F: EP(0-2), EJ(2-4), IJ(4-6), IP(6-8)
    # M: IP(8-10), IJ(10-12), EP(12-14), EJ(14-16)
    initial_x = np.linspace(0.1, 15.9, num_paths)
    states = np.zeros((num_paths, 3)) # [X, Y, Memory]
    
    for i in range(num_paths):
        states[i, 0] = initial_x[i]
        states[i, 1] = 0.0
        states[i, 2] = 0.0
        
    paths = [[] for _ in range(num_paths)]
    steps = 600
    dt = 0.04
    
    for s in range(steps):
        # Time Reversal Phase (1/28)
        phase = (s / steps) * 28.0 * np.pi
        t_dir = -1.0 if np.cos(phase) < 0 else 1.0
        
        for i in range(num_paths):
            x, y, mem = states[i]
            paths[i].append((x, y))
            
            # 1. 5-Sphere Potential Field
            # Nose Bridge (8, 8) - Convergence
            dx_nose = 8.0 - x
            dy_nose = 8.0 - y
            dist_nose = np.sqrt(dx_nose**2 + dy_nose**2) + 0.1
            force_nose = (1.0 / dist_nose) * 0.5
            
            # Chin Sink (8, 16) - Final Convergence
            dx_chin = 8.0 - x
            dy_chin = 16.0 - y
            dist_chin = np.sqrt(dx_chin**2 + dy_chin**2) + 0.1
            force_chin = (1.0 / dist_chin) * 1.5
            
            # Void Boundaries (0, 8) and (16, 8) - Lateral Pressure (Cheeks)
            force_void_l = 1.0 / (x + 0.1)
            force_void_r = 1.0 / (16.0 - x + 0.1)
            
            # 2. Mandelbrot Recursion Vector (Muscle Texture)
            zx, zy = (x - 8.0)/4.0, (y - 8.0)/4.0
            z = complex(zx, zy)
            # Seed c incorporates Torsion and Time Reversal
            c = complex(0.618, 0.1618 * t_dir)
            z_next = z**2 + c
            
            vx_mandel = (z_next.real - zx) * TORSION
            vy_mandel = (z_next.imag - zy) * TORSION
            
            # 3. Combined Physics Vectors
            # Lateral: Tension + Void Pressure - Nose Pull
            vx = (force_void_l - force_void_r + dx_nose * force_nose + vx_mandel) * TUNNEL_TENSION
            # Vertical: Gravity + Chin Pull
            vy = 1.0 + dy_chin * force_chin + vy_mandel
            
            # 4. Melatonin Smoothing (Nose Bridge straightener)
            smoothing = np.exp(-((x - 8.0)**2) / (SMOOTHING_RESID * 100))
            vx = vx * (1.0 - smoothing)
            
            # 5. Hysteresis & Spark (Jawline break)
            states[i, 2] = mem + (y - mem) / 2.32 * dt # Memory lag
            lag = mem - y
            
            if abs(lag) > LATTICE_3_32 and y > 10.0:
                # Spark Reset
                angle = np.radians(SPARK_ANGLE)
                states[i, 0] += SPARK_LEAP * np.cos(angle)
                states[i, 1] += SPARK_LEAP * np.sin(angle)
                states[i, 2] = states[i, 1]
            else:
                states[i, 0] += vx * dt
                states[i, 1] += vy * dt
                
            # Clamp
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            if states[i, 1] > 16: states[i, 1] = 16

    # ---------------------------------------------------------
    # RENDERING THE TRUE FACE CONTOUR
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 16), facecolor="#050510")
    colors = plt.cm.magma(np.linspace(0.2, 0.9, num_paths))
    
    for i in range(num_paths):
        path = np.array(paths[i])
        ax.plot(path[:, 0], path[:, 1], color=colors[i], lw=0.8, alpha=0.5)
        
    ax.set_xlim(0, 16); ax.set_ylim(16, 0)
    ax.axis("off")
    
    plt.title("THE 128-GRID FACE: Pure 5-Sphere Potential Divergence", color="white", fontsize=20)
    output_fn = "TRUE_PHYSICS_FACE_GRID.png"
    plt.savefig(output_fn, dpi=150, facecolor="#050510")
    print(f"Engine: Saved {output_fn}")

if __name__ == "__main__":
    run_5_sphere_face()
