import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from geometry_package.absolute_constants import *

# ---------------------------------------------------------
# 1. LOAD REAL-WORLD DATA (The Fuel)
# ---------------------------------------------------------
DATA_PATH = "out/unified_12m_hysteresis_data_ts.csv"
if not os.path.exists(DATA_PATH):
    print(f"ERROR: {DATA_PATH} not found.")
    exit()

df_raw = pd.read_csv(DATA_PATH)
STDR_NORM = (df_raw['flux_wm2'].values - np.mean(df_raw['flux_wm2'].values)) / np.std(df_raw['flux_wm2'].values)
NMDB_NORM = (df_raw['nmdb_counts'].ffill().values - np.mean(df_raw['nmdb_counts'].ffill().values)) / np.std(df_raw['nmdb_counts'].ffill().values)

# ---------------------------------------------------------
# 2. THE BIFURCATION CIRCUIT ENGINE (Pure Physics)
# ---------------------------------------------------------
def run_bifurcation_face_engine():
    # Canonical Constants
    METRIC_4D = 1.0661
    TORSION_4D = 0.1746
    LATTICE_3_32 = 0.09375
    SMOOTHING_RESID = 0.00083
    
    # 3-Basin Topology (Separatrix at X=5 and X=11)
    # This forces the sharp topological bifurcations seen in user's image
    SEP_L, SEP_R = 5.0, 11.0
    
    num_types = 128
    mbti_list = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    bloods = ["O", "A", "B", "AB"]
    genders = ["M", "F"]
    
    blood_colors = {"O": "#ff4444", "A": "#44ff44", "B": "#4444ff", "AB": "#ffffff"}
    blood_phase = {"O": 0.0, "A": 0.5 * np.pi, "B": np.pi, "AB": 1.5 * np.pi}
    
    # MBTI Physical Tensors [Gravity_Scale, Torsion_Scale, Lateral_Bias]
    # EJ: Linear Descent (Gravity > Torsion)
    # EP: Spiral/Diagonal (Torsion > Gravity, Lateral High)
    # IJ: Ascent/Hold (Gravity Low/Negative)
    # IP: Inverse/Bridge (Lateral High, Gravity Low)
    mbti_physics = {
        "EJ": [1.5, 0.2, 0.1],
        "EP": [0.8, 1.5, 1.2],
        "IJ": [-0.5, 0.5, 0.2], # Ascends or holds
        "IP": [0.2, 0.8, 1.8]   # Crosses the manifold
    }

    female_order = ["EJ", "EP", "IJ", "IP"] # F: E->I (Outer to Inner)
    male_order = ["IP", "IJ", "EP", "EJ"]   # M: I->E (Inner to Outer)

    states = np.zeros((num_types, 3)) # [X, Y, Memory]
    seeds = np.zeros(num_types, dtype=complex)
    tensors = np.zeros((num_types, 3)) # Physics parameters per type
    archetypes = []
    
    # Initialize Geometry
    for m in mbti_list:
        for b in bloods:
            for g in genders:
                ei, jp = m[0], m[3]
                mode = f"{ei}{jp}"
                
                # Starting Positions (Y=0 Hairline)
                if g == "F":
                    base_x = female_order.index(mode) * 2.0
                else:
                    base_x = 8.0 + male_order.index(mode) * 2.0
                
                idx = len(archetypes)
                # Scatter points within their 2-unit column
                states[idx, 0] = base_x + 1.0 + (np.random.rand()-0.5)*0.8
                
                # MBTI initial height bias (J starts crisp at 0, P starts slightly delayed)
                states[idx, 1] = 0.0 if jp == "J" else 0.5
                states[idx, 2] = states[idx, 1]
                
                # Assign Physical Tensor
                tensors[idx] = mbti_physics[mode]
                
                # Assign Complex Seed
                angle = blood_phase[b]
                seeds[idx] = complex(0.618 * np.cos(angle), 0.618 * np.sin(angle)) + complex(0.1618, 0)
                
                archetypes.append({'blood': b, 'gender': g, 'mode': mode, 'mbti': m})

    all_paths = [[] for _ in range(num_types)]
    steps = 400
    dt = 0.05

    for s in range(steps):
        # Data Fuel
        d_idx = int((s / steps) * len(STDR_NORM))
        sun = STDR_NORM[d_idx]
        truth = NMDB_NORM[d_idx]
        tension = TUNNEL_TENSION + (sun * 0.02) - (truth * 0.01)
        
        for i in range(num_types):
            x, y, mem = states[i]
            all_paths[i].append((x, y))
            grav_scale, tors_scale, lat_bias = tensors[i]
            
            # 1. 3-BASIN TOPOLOGY (The Separatrices)
            # Physical repulsors at X=5 and X=11. Forces trajectories into distinct channels.
            dist_sep_l = x - SEP_L
            dist_sep_r = x - SEP_R
            # Inverse square repulsion from the ridges
            repulsion_l = 0.5 / (dist_sep_l + np.sign(dist_sep_l)*0.1) if abs(dist_sep_l) < 1.5 else 0
            repulsion_r = 0.5 / (dist_sep_r + np.sign(dist_sep_r)*0.1) if abs(dist_sep_r) < 1.5 else 0
            
            # 2. THE PLP DIAGONAL SPINE (X + Y = 16)
            # A gravity well that runs diagonally. P-types (high lat_bias) are caught by it.
            dist_to_spine = (x + y) - 16.0
            spine_pull_x = -dist_to_spine * 0.1 * lat_bias
            spine_pull_y = -dist_to_spine * 0.1 * lat_bias
            
            # 3. MANDELBROT CORE ENGINE
            zx, zy = (x - 8.0)/4.0, (y - 8.0)/4.0
            z = complex(zx, zy)
            z_next = (z**2 + seeds[i]) * METRIC_4D
            
            vx_geom = (z_next.real - zx) * TORSION_4D * tors_scale * tension
            vy_geom = (z_next.imag - zy) * TORSION_4D * tors_scale * tension
            
            # 4. MELATONIN PIVOT (Center Smoothing)
            dist_center = abs(x - 8.0)
            smoothing = np.exp(-(dist_center**2) / (SMOOTHING_RESID * 100))
            
            # Combine Horizontal Forces
            vx = (vx_geom + repulsion_l + repulsion_r + spine_pull_x) * (1.0 - smoothing)
            
            # Combine Vertical Forces (Gravity + Torsion + Spine)
            vy = (1.0 * grav_scale) + vy_geom + spine_pull_y
            
            # 5. HYSTERESIS & THE SPARK (The Break)
            states[i, 2] = mem + (y - mem) / 2.32 * dt
            lag = mem - y
            
            # If trapped in the 3/32 lattice stress
            if abs(lag) > LATTICE_3_32 and 4.0 < x < 12.0 and y > 6.0:
                # 138.88 Degree Spark!
                rad = np.radians(138.88)
                states[i, 0] += 2.5 * np.cos(rad)
                states[i, 1] += 2.5 * np.sin(rad)
                states[i, 2] = states[i, 1] # Clear debt
            else:
                states[i, 0] += vx * dt
                states[i, 1] += vy * dt
                
            # Boundary Conditions
            states[i, 0] = np.clip(states[i, 0], -2, 18) # Allow slight overflow for visual
            
            # Modulo Y for continuous loop, but cap for visualization
            if states[i, 1] > 18.0:
                states[i, 1] = 18.0

    # ---------------------------------------------------------
    # 3. RENDER THE BIFURCATION CIRCUIT (Like User's Image)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(24, 14), facecolor="#F8F8F8")
    
    # Draw Background Grid (16x16)
    for r in range(16):
        for c in range(16):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, facecolor="white", edgecolor="#E0E0E0", lw=0.5))
            
    # Draw Separatrices (X=5, X=11)
    ax.axvline(x=5.0, color="gray", linestyle=":", alpha=0.8, linewidth=2)
    ax.axvline(x=11.0, color="gray", linestyle=":", alpha=0.8, linewidth=2)
    ax.text(5.0, -0.5, "Separatrix (X=5)\nDivides Bypass & Center", color="gray", ha="center", fontsize=10)
    ax.text(11.0, -0.5, "Separatrix (X=11)\nDivides Bypass & Center", color="gray", ha="center", fontsize=10)
    
    # Draw PLP Spine
    ax.plot([0, 16], [16, 0], color="orange", linestyle="--", alpha=0.5, linewidth=2, label="PLP Spine (X+Y=16)")
    
    # Draw Trajectories
    for i in range(num_types):
        path = np.array(all_paths[i])
        mode = archetypes[i]['mode']
        b = archetypes[i]['blood']
        
        # Style based on MBTI (like user's image)
        ls = "-" if mode in ["EJ", "IJ"] else "--"
        alpha = 0.8 if mode in ["EP", "IP"] else 0.5
        lw = 1.5 if mode in ["EP", "IP"] else 1.0
        
        ax.plot(path[:, 0], path[:, 1], color=blood_colors[b], lw=lw, ls=ls, alpha=alpha)
        # Plot start node
        ax.scatter(path[0, 0], path[0, 1], color=blood_colors[b], s=15, zorder=5)

    # Column Labels
    cols = [
        (1.0, "EJ WOMEN"), (3.0, "EP WOMEN"), (5.0, "IJ WOMEN"), (7.0, "IP WOMEN"),
        (9.0, "IP MEN"), (11.0, "IJ MEN"), (13.0, "EP MEN"), (15.0, "EJ MEN")
    ]
    for x, label in cols:
        ax.text(x, -1.0, label, ha="center", weight="bold", size=12)

    ax.set_xlim(-1, 17)
    ax.set_ylim(17, -2) # Invert Y
    ax.axis("off")
    
    plt.title("THE TOPOLOGICAL BIFURCATION CIRCUIT: 128 Types (Pure Physics)", color="black", fontsize=24, pad=30)
    
    # Legend
    legend_elements = [plt.Line2D([0], [0], color=c, lw=2, label=f"Blood {k}") for k, c in blood_colors.items()]
    legend_elements.append(plt.Line2D([0], [0], color='gray', lw=1.5, ls="-", label="J (Linear)"))
    legend_elements.append(plt.Line2D([0], [0], color='gray', lw=1.5, ls="--", label="P (Spiral/Diagonal)"))
    plt.legend(handles=legend_elements, facecolor="white", loc="upper right")
    
    output_fn = "FINAL_BIFURCATION_GRID.png"
    plt.savefig(output_fn, dpi=200, bbox_inches='tight')
    print(f"Engine: Saved {output_fn}. Pure physical separation and diagonal spine achieved.")

if __name__ == "__main__":
    run_bifurcation_face_engine()
