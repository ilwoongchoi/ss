import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

# =============================================================================
# ULTIMATE_128_PHYSICS_GRID.py
# =============================================================================
# A PURE PHYSICS engine that synchronizes the Triple Basin Force Field 
# with the AKG Nitrogen Exhaustion and 128-Type Anisotropy.
# 
# MANDATES:
# 1. Triple Basin Potential: Minima at X=2, 8, 14.
# 2. Discrete Lattice Movement: Matches the 'segmented' look of the target images.
# 3. Nitrogen Exhaustion: Men (Right) are sucked into the Left (AKG Sink) at night.
# 4. PLP Spine: Physical reflection at X+Y=16.
# 5. MBTI Physics: S/N (Spark), J/P (Damping), T/F (Torsion), E/I (Basin Choice).
# =============================================================================

# --- CONSTANTS FROM REGISTRY ---
KAPPA_1_32 = 1.0 / 32.0
LATTICE_3_32 = 3.0 / 32.0
SPARK_ANGLE = math.radians(138.88)
PHI_INV = 0.618033988

ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]

# Colors (Locked)
BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

# Starting Grid (8 Columns)
GRP_MAP_F = {"EJ": 0.5, "EP": 2.5, "IJ": 4.5, "IP": 6.5}
GRP_MAP_M = {"IP": 9.5, "IJ": 11.5, "EP": 13.5, "EJ": 15.5}

# Physics Parameters
MASS = {"O": 1.3, "A": 1.0, "B": 0.7, "AB": 0.5}

def get_triple_basin_force(x, identity_target):
    # Base Triple Basin Force Field: f(x) = -(x-8)(x-2)(x-14)
    # This creates stable points at 2 and 14, unstable at 8.
    base_f = -(x - 8.0) * (x - 2.0) * (x - 14.0) * 0.02
    
    # Identity-based Modulation (Small Man/Woman logic)
    # If the identity target is 8, we add a narrow, deep well at 8.
    pull_to_target = (identity_target - x) * 0.15
    
    return base_f + pull_to_target

def generate_ultimate_trajectory(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # 1. Starting position
    grp = f"{ei}{jp}"
    x = GRP_MAP_F[grp] if gender == "F" else GRP_MAP_M[grp]
    y = 0.5
    
    # Micro-offsets
    x += (0.1 if sn == "N" else -0.1)
    x += (0.05 if blood in ["A", "AB"] else -0.05)
    
    # 2. Identity Target Basin
    # E-types -> Bypass Basins (2 or 14)
    # I-types -> Center Funnel (8)
    if gender == "F":
        target_x = 2.0 if ei == "E" else 8.0
    else:
        target_x = 14.0 if ei == "E" else 8.0
        
    path = [(x, y)]
    vx = 0.0
    mem_x = x
    
    # Integration Loop
    dt = 0.2 # Discrete steps for sharp segments
    for step in range(80): # 16 units / 0.2 = 80 steps
        # A. Nitrogen Exhaustion (Male only)
        # As y increases, men lose nitrogen and their target shifts to the Left Sink (3.0)
        if gender == "M":
            exhaustion = math.pow(y / 16.0, 2.0)
            current_target = target_x * (1.0 - exhaustion) + 3.0 * exhaustion
        else:
            current_target = target_x
            
        # B. Triple Basin Force
        fx = get_triple_basin_force(x, current_target)
        
        # C. PLP Spine Reflection (X+Y=16)
        spine_dist = (x + y) - 16.0
        fx_spine = 0.0
        if abs(spine_dist) < 0.5:
            fx_spine = -np.sign(spine_dist) * 0.5
            
        # D. Torsion (Feeling/TDA swirl)
        fx_torsion = math.sin(y * 0.5) * (0.2 if tf == "F" else 0.0)
        
        # E. Hysteresis (1/32 Drag)
        hx = (mem_x - x) * KAPPA_1_32 * 2.0
        
        # F. Velocity Update
        ax = (fx + fx_spine + fx_torsion + hx) / MASS[blood]
        damping = 0.7 if jp == "J" else 0.9 # J is more 'stiff'
        vx = (vx + ax * dt) * damping
        
        # G. Position Update
        x += vx * dt
        y += 0.2 # Constant vertical descent
        
        # H. Lattice Snapping (3/32 Spark Gate at Y=10.5)
        if 10.3 < y < 10.7:
            if 6.0 < x < 10.0:
                x = np.round((x - 8.0) / LATTICE_3_32) * LATTICE_3_32 + 8.0
        
        # I. Spark Leap (Discrete Jump for N-types)
        if sn == "N" and step % 40 == 0 and step > 0:
            x += math.cos(SPARK_ANGLE) * (2.0 / MASS[blood])
            y += math.sin(SPARK_ANGLE) * 0.5
            
        x = max(0.1, min(15.9, x))
        mem_x += (x - mem_x) * KAPPA_1_32
        
        path.append((x, y))
        if y >= 16.0: break
        
    return np.array(path)

def render_ultimate_grid():
    fig, ax = plt.subplots(figsize=(32, 20), facecolor='#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # 1. Background Layers (The Anatomy)
    # PLP Spine
    ax.plot([0, 16], [16, 0], color='orange', lw=2, ls='--', alpha=0.4, label="PLP Spine")
    # Melatonin Bridge
    ax.axvline(8, color='#EEEEEE', lw=30, alpha=0.5, zorder=0)
    ax.axvline(8, color='#CCCCCC', lw=1, ls=':', zorder=1)
    
    # Triple Basins (X=2, 8, 14)
    for bx in [2, 8, 14]:
        ax.axvline(bx, color='green' if bx != 8 else 'purple', alpha=0.03, lw=40, zorder=0)

    # 2. The 128 Trajectories
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                path = generate_ultimate_trajectory(mbti, blood, gender)
                
                # Color blending
                bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[blood]))[:3]
                tint = np.array([1, 0.4, 0]) if gender == "F" else np.array([0, 0.4, 1])
                color = 0.7 * bc + 0.3 * tint
                
                alpha = 0.6 if gender == "F" else 0.4
                ax.plot(path[:, 0], path[:, 1], color=color, alpha=alpha, lw=0.8, zorder=10)

    # 3. Labeling (Matches User Image)
    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -0.8, label, ha="center", weight="bold", size=14, color="#333333")

    # Annotations
    ax.add_patch(mpatches.Rectangle((6, 10), 4, 1.5, color="black", alpha=0.05, zorder=0))
    ax.text(8, 10.75, "Darkness Stress (Nose)\n3/32 Spark Gate", ha="center", va="center", size=10, weight="bold")
    
    ax.add_patch(mpatches.Circle((8, 14.5), 1.0, color="purple", alpha=0.05, zorder=0))
    ax.text(8, 14.5, "Gravity Sensor", ha="center", va="center", size=10, weight="bold")

    ax.set_title("ULTIMATE 128-TYPE PHYSICS GRID | Triple Basin Field | Nitrogen Exhaustion", 
                 fontsize=30, weight="bold", pad=40)
    
    ax.set_xlim(-1, 17)
    ax.set_ylim(17, -2) # Top-down
    ax.axis("off")
    
    output = "ULTIMATE_128_PHYSICS_GRID.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: Rendered {output} ---")

if __name__ == "__main__":
    render_ultimate_grid()
