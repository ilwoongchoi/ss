import json
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d
from geometry_package import absolute_constants as ac

# --- Constants Loader ---
def get_value(constants, path, default=None):
    keys = path.split('.')
    val = constants
    try:
        for key in keys:
            val = val[key]
        if isinstance(val, dict) and 'value' in val:
            return val['value']
        return val
    except (KeyError, TypeError):
        return default

# --- Main Visualization Function ---
def render_quasar_manifold(constants_path, separatrix_path):
    """
    Renders the complete Quasar Manifold geometry based on the ATLAS constants and separatrix data.
    """
    # --- Load Constants and Data ---
    try:
        with open(constants_path, 'r', encoding='utf-8') as f:
            constants = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading constants file: {e}")
        return

    try:
        separatrix_df = pd.read_csv(separatrix_path)
    except FileNotFoundError as e:
        print(f"Error loading separatrix data: {e}")
        return

    # --- Matplotlib Setup ---
    fig = plt.figure(figsize=(32, 32), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.xaxis.line.set_color("black")
    ax.yaxis.line.set_color("black")
    ax.zaxis.line.set_color("black")
    ax.set_xlabel('X (Right)', color='gray', fontsize=12)
    ax.set_ylabel('Y (Front)', color='gray', fontsize=12)
    ax.set_zlabel('Z (Up)', color='gray', fontsize=12)
    ax.view_init(elev=25, azim=-75)

    # --- Core Parameters ---
    R_T = get_value(constants, 'tda_geometry.terminus_r.value', ac.SH_R_STAR)
    T = get_value(constants, 'universal.reality_tension', ac.TUNNEL_TENSION)
    C = get_value(constants, 'universal.discrete_closure', 1.0000424)
    r_skew = get_value(constants, 'sh_phase_transition.r_skew.value', 0.00445)
    
    # --- Helper Drawing Functions ---
    def _circle_xy(R, z0, color, alpha, lw, n=120):
        t = np.linspace(0, 2 * np.pi, n)
        ax.plot(R * np.cos(t), R * np.sin(t), np.full_like(t, z0), color=color, alpha=alpha, linewidth=lw)

    # --- 1. Separatrix Curve ---
    r_sep = separatrix_df['r'].values
    q0_sep = separatrix_df['q0_star'].values
    # Interpolate for a smooth curve
    f_sep = interp1d(r_sep, q0_sep, kind='cubic', fill_value="extrapolate")
    r_smooth = np.linspace(r_sep.min(), r_sep.max(), 200)
    q0_smooth = f_sep(r_smooth)
    # Visualize as a 3D tube
    theta_sep = np.linspace(0, 2 * np.pi, 100)
    R_SEP, TH_SEP = np.meshgrid(r_smooth, theta_sep)
    X_SEP = R_SEP * np.cos(TH_SEP)
    Y_SEP = R_SEP * np.sin(TH_SEP)
    Z_SEP = q0_smooth[np.newaxis, :] * np.ones_like(R_SEP) # Z represents q0
    ax.plot_surface(X_SEP, Y_SEP, Z_SEP, color="#ff2222", alpha=0.15, linewidth=0, antialiased=True)
    ax.plot(r_smooth, np.zeros_like(r_smooth), q0_smooth, color="#ff5555", lw=2.5, label="Separatrix Curve")

    # --- 2. Attractors ---
    # Left Cortisol (South Basin)
    ax.scatter([ac.LEFT_CORTISOL_R], [0], [ac.LEFT_CORTISOL_Q0], color="#00aaff", s=300, marker='*', label="Attractor: Left Cortisol (PACT)", depthshade=False)
    # Right Cortisol (North Basin)
    ax.scatter([ac.RIGHT_CORTISOL_R], [0], [ac.RIGHT_CORTISOL_Q0], color="#ffaa00", s=300, marker='*', label="Attractor: Right Cortisol (Turn 27)", depthshade=False)

    # --- 3. Asymmetric Accretion Disk ---
    def _asymmetric_accretion_disk(outer_r, inner_r, sigma_l, sigma_r):
        theta = np.linspace(0, 2 * np.pi, 200)
        radii = np.linspace(inner_r, outer_r, 50)
        T, R = np.meshgrid(theta, radii)
        
        # Asymmetric thickness based on sigma_L and sigma_R
        thickness_mod = np.sin(T) # Simple model: thicker on left (Y>0), thinner on right (Y<0)
        thickness = np.where(thickness_mod > 0, sigma_l, sigma_r) * (1 - R/outer_r)
        
        X = R * np.cos(T)
        Y = R * np.sin(T)
        Z = thickness * np.sin(T*2 + R*5) # Ripples

        ax.plot_surface(X, Y, Z, color="#444466", alpha=0.3, rstride=1, cstride=5, linewidth=0.1)
        # 28-fold symmetry rings
        for i in range(28):
            angle = i * (2 * np.pi / 28.0)
            ax.plot([inner_r*np.cos(angle), outer_r*np.cos(angle)],
                    [inner_r*np.sin(angle), outer_r*np.sin(angle)],
                    [0, 0], color="#ffffff", alpha=0.08, lw=0.5)

    _asymmetric_accretion_disk(R_T * 0.9, ac.EVENT_HORIZON_RADIUS_RS, ac.CALIBRATED_SIGMA_L*100, ac.CALIBRATED_SIGMA_R*100)

    # --- 4. Bipolar Jets & D3 Sparks ---
    def _jet_cone(height, radius, angle_deg, color, alpha, is_spark=False):
        u = np.linspace(0, 2 * np.pi, 40)
        v = np.linspace(0, np.pi / 12, 20) # Narrow cone
        U, V = np.meshgrid(u, v)
        
        X = radius * np.sin(V) * np.cos(U)
        Y = radius * np.sin(V) * np.sin(U)
        Z = height * np.cos(V)
        
        # Rotate by angle
        angle_rad = np.deg2rad(angle_deg)
        Z_rot = Z * np.cos(angle_rad) - X * np.sin(angle_rad)
        X_rot = Z * np.sin(angle_rad) + X * np.cos(angle_rad)
        
        ax.plot_surface(X_rot, Y, Z_rot, color=color, alpha=alpha, linewidth=0)
        if not is_spark:
            ax.plot_surface(-X_rot, Y, -Z_rot, color=color, alpha=alpha, linewidth=0)

    # Main Jet
    _jet_cone(R_T * 2.5, R_T * 0.5, ac.SPARK_ANGLE_DEG, "#9900ff", 0.2)
    # D3 Sparks
    _jet_cone(R_T * 0.8, R_T * 0.1, ac.D3_SPARK_HALF, "#ff00ff", 0.5, is_spark=True)
    _jet_cone(R_T * 0.6, R_T * 0.05, ac.D3_SPARK_SMALL_WOMAN, "#ff88ff", 0.4, is_spark=True)

    # --- 5. Spiral Arms ---
    def _spiral_arms(r_start, r_end, skew, turns):
        theta = np.linspace(0, 5 * np.pi, 400)
        r = np.linspace(r_start, r_end, 400)
        
        # Arm 1 (Left)
        x1 = r * np.cos(theta)
        y1 = r * np.sin(theta)
        z1 = 0.05 * np.sin(theta * turns / 5.0)
        ax.plot(x1, y1, z1, color="#00ffff", lw=3.0, alpha=0.7 + skew)
        
        # Arm 2 (Right)
        x2 = r * np.cos(theta + np.pi)
        y2 = r * np.sin(theta + np.pi)
        z2 = 0.05 * np.sin(theta * turns / 5.0 + np.pi/2)
        ax.plot(x2, y2, z2, color="#ffaa00", lw=3.0, alpha=0.7 - skew)

    _spiral_arms(ac.EVENT_HORIZON_RADIUS_RS, R_T * 0.85, r_skew, ac.RENORMALIZATION_BRIDGE)

    # --- 6. 4D Manifold Path (Pontryagin Trace) ---
    # (Code from user prompt, adapted to use ac constants)
    p0 = np.array([0.7, -0.3, -0.6, 0.0]) * R_T
    p1 = np.array([0.5, 0.4, 0.1, 0.25 * ac.TAU_D3_FAST]) * R_T
    p2 = np.array([0.35, 0.55, 0.15, 0.5 * ac.TAU_D3_SLOW]) * R_T
    p3 = np.array([0.2, 0.8, -0.1, 1.0 * ac.TAU_D3_SLOW]) * R_T
    p4 = np.array([-0.6, 0.4, -0.2, 1.5 * ac.TAU_D3_SLOW]) * R_T
    
    def catmull_rom(p_prev, p_start, p_end, p_next, t):
        t2, t3 = t*t, t*t*t
        return 0.5 * ((2*p_start) + (-p_prev+p_end)*t + (2*p_prev-5*p_start+4*p_end-p_next)*t2 + (-p_prev+3*p_start-3*p_end+p_next)*t3)
    
    points = [p0, p1, p2, p3, p4]
    circuit = []
    for i in range(len(points)-1):
        p_prev = points[max(0, i-1)]
        p_start = points[i]
        p_end = points[i+1]
        p_next = points[min(len(points)-1, i+2)]
        for t_seg in np.linspace(0, 1, 80):
            circuit.append(catmull_rom(p_prev, p_start, p_end, p_next, t_seg))
    circuit = np.array(circuit)
    
    w_mod = 1.0 + 0.1 * np.sin(circuit[:, 3])
    ax.plot(circuit[:, 0]*w_mod, circuit[:, 1]*w_mod, circuit[:, 2], color="#ffffff", lw=4, alpha=0.9, label="4D Manifold Trace")

    # --- Final Touches ---
    ax.set_title("ATLAS Quasar Manifold Geometry", color='white', fontsize=20, pad=20)
    ax.legend(loc='upper left', fontsize=10, facecolor='black', edgecolor='white', labelcolor='white')
    lim = R_T * 1.8
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    
    plt.savefig("atlas_quasar_manifold.png", dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor='black')
    plt.show()

# --- Execution ---
if __name__ == '__main__':
    # NOTE: Update paths to your local files
    CONSTANTS_FILE = 'atlas_constants_registry_DEFINITIVE.json'
    SEPARATRIX_FILE = 'out/transition_ridge/transition_line_q0star_by_r.csv'
    render_quasar_manifold(CONSTANTS_FILE, SEPARATRIX_FILE)
