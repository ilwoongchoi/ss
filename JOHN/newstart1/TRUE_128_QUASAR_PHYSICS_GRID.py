import numpy as np
import matplotlib.pyplot as plt
import math

# =============================================================================
# TRUE_128_QUASAR_PHYSICS_GRID.py
# =============================================================================
# Absolute conformity to the SKELETAL CORE and TDA Physics:
# 1. 16x16 Coordinate Grid (Y drops from 0 to 16).
# 2. X[0,8] = Left/Female, X[8,16] = Right/Male.
# 3. Trajectories Start at top columns (Y=0.5).
# 4. PLP Spine (X+Y=16) acts as a physical seam, not a start point.
# 5. Core Engine incorporates 11/7 Torque, 138.88° Spark Leap, and H2 lag.
# =============================================================================

# --- CONSTANTS ---
PI = math.pi
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
TUNNEL_TENSION = 1.0100375
KAPPA_H2 = 1.0 / 32.0
LATTICE_3_32 = 3.0 / 32.0

ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
BLOOD_TYPES = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]

# Canonical Base Coordinates (Women: Left to Center, Men: Center to Right)
GROUP_MAP_FEMALE = {"EJ": 0.5, "EP": 2.5, "IJ": 4.5, "IP": 6.5}
GROUP_MAP_MALE   = {"IP": 8.5, "IJ": 10.5, "EP": 12.5, "EJ": 14.5}

BLOOD_OFFSET_X = {"O": -0.2, "A": 0.2, "B": -0.2, "AB": 0.2}
BLOOD_OFFSET_Y = {"O": 0.1,  "A": 0.1, "B": -0.1, "AB": -0.1}
SN_OFFSET = {"S": -0.15, "N": 0.15}
TF_OFFSET = {"T": -0.05, "F": 0.05}

# Physics Parameters by Blood
BLOOD_PHYSICS = {
    'O':  {'mass': 1.3, 'viscosity': 0.15},
    'A':  {'mass': 1.0, 'viscosity': 0.10},
    'B':  {'mass': 0.7, 'viscosity': 0.05},
    'AB': {'mass': 0.5, 'viscosity': 0.02}
}

def generate_true_grid():
    trajectories = []
    dt = 0.04
    num_steps = 800
    
    print("--- Igniting True 128-Type Physics Engine ---")
    
    for mbti in ALL_MBTI:
        for blood in BLOOD_TYPES:
            for gender in GENDERS:
                ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
                
                # 1. INITIAL SEEDING (Top of the Grid)
                grp = f"{ei}{jp}"
                base_x = GROUP_MAP_FEMALE[grp] if gender == "F" else GROUP_MAP_MALE[grp]
                
                x = base_x + BLOOD_OFFSET_X[blood] + SN_OFFSET[sn] + TF_OFFSET[tf]
                y = 0.5 + BLOOD_OFFSET_Y[blood]
                
                vx, vy = 0.0, 0.0
                path = [(x, y)]
                memory_x, memory_y = x, y
                tension_accum = 0.0
                bp = BLOOD_PHYSICS[blood]
                
                for step in range(num_steps):
                    # --- LAW 1: PLP SPINE INTERACTION (x + y = 16) ---
                    # The seam generates a restorative/deflective force when crossed.
                    spine_dist = (x + y) - 16.0
                    fx_spine = 0.0
                    fy_spine = 0.0
                    if abs(spine_dist) < 1.5:
                        fx_spine = -np.sign(spine_dist) * 0.2
                        fy_spine = -np.sign(spine_dist) * 0.1
                        
                    # --- LAW 2: DIPOLE TORQUE (11/7 Polarity) ---
                    # Pulls toward Center (8.0) or Outward depending on E/I and Gender
                    target_x = 8.0 if ei == "I" else (2.0 if gender == "F" else 14.0)
                    torque_force = (target_x - x) * (11.0/7.0 if gender == "F" else 7.0/11.0) * 0.05
                    
                    # --- LAW 3: HYSTERESIS DRAG ---
                    hx = (memory_x - x) * bp['viscosity']
                    hy = (memory_y - y) * bp['viscosity']
                    
                    # --- LAW 4: 138.88° SPARK LEAP (Quantum Jump) ---
                    # N-types and certain thresholds trigger discrete leaps
                    tension_accum += math.sqrt(vx**2 + vy**2)
                    if y > 6.0 and tension_accum > TUNNEL_TENSION and sn == "N":
                        vx += math.cos(SPARK_ANGLE_RAD) * 1.5
                        vy += math.sin(SPARK_ANGLE_RAD) * 0.5
                        tension_accum = 0.0
                        memory_x, memory_y = x, y # Anchor reset
                        
                    # --- LAW 5: BASE DESCENDING TIME FLOW (1D) ---
                    # Men drop vertically faster, Women experience more horizontal drag
                    base_vy = 1.2 if gender == "M" else 0.8
                    
                    # Integration
                    ax = (torque_force + hx + fx_spine) / bp['mass']
                    ay = (base_vy + hy + fy_spine) / bp['mass']
                    
                    # J-types maintain tight control (high damping), P-types spiral (low damping)
                    damping = 0.85 if jp == "J" else 0.96
                    
                    vx = (vx + ax * dt) * damping
                    vy = (vy + ay * dt) * damping
                    
                    # T/F Torsion Shift
                    if tf == "F":
                        vx += math.sin(y * 0.5) * 0.2
                        
                    x += vx * dt
                    y += vy * dt
                    
                    x = max(0.1, min(15.9, x))
                    
                    # Hysteresis update
                    memory_x += (x - memory_x) * KAPPA_H2
                    memory_y += (y - memory_y) * KAPPA_H2
                    
                    path.append((x, y))
                    if y >= 16.0: break
                
                # Dynamic Coloring
                base_color = np.array(plt.cm.colors.to_rgb({"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}[blood]))
                tint = np.array([1, 0.4, 0]) if gender == "F" else np.array([0, 0.4, 1])
                color = 0.6 * base_color + 0.4 * tint
                
                trajectories.append({
                    'coords': np.array(path),
                    'color': color,
                    'lw': 1.5 if jp == "J" else 0.8
                })

    return trajectories

def render_true_grid(trajectories):
    fig, ax = plt.subplots(figsize=(24, 24), facecolor='#000000')
    ax.set_facecolor('#000000')
    
    # 1. THE PLP SPINE (The Master Seam X + Y = 16)
    # Rendered as the crucial structural boundary
    ax.plot([0, 16], [16, 0], color='orange', lw=2, linestyle='--', alpha=0.5)
    
    # 2. SEPTUM / MELATONIN AXIS
    ax.axvline(x=8.0, color='#333333', lw=2, linestyle=':')
    
    # 3. RENDER 128 DYNAMIC FLOWS
    for t in trajectories:
        ax.plot(t['coords'][:, 0], t['coords'][:, 1], color=t['color'], 
                alpha=0.5, lw=t['lw'], solid_capstyle='round')
        
    # 4. FORMATTING
    labels = ["EJ W", "EP W", "IJ W", "IP W", "IP M", "IJ M", "EP M", "EJ M"]
    for i, label in enumerate(labels):
        ax.text(i * 2 + 1, -0.5, label, ha='center', va='top', fontsize=18, fontweight='bold', color='#AAAAAA')
    
    ax.set_xlim(0, 16)
    # VITAL FIX: Y-axis flows from Dawn (0) to Midnight (16) downwards
    ax.set_ylim(16, -1) 
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title("TRUE 128-TYPE PHYSICS GRID\nVertical Descent | PLP Spine Seam | 11/7 Torque | Spark Leap", 
              color='white', fontsize=32, fontweight='bold', pad=40)

    output = "TRUE_128_QUASAR_PHYSICS_GRID.png"
    plt.savefig(output, dpi=300, facecolor='#000000', bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"--- SUCCESS: Rendered exactly {len(trajectories)} physical flows to {output} ---")

if __name__ == "__main__":
    trajs = generate_true_grid()
    render_true_grid(trajs)
