import numpy as np
import matplotlib.pyplot as plt
import math

# =============================================================================
# DEFINITIVE_128_QUASAR_INTEGRATION.py
# =============================================================================
# INTEGRATED TRUTHS:
# 1. Small Man = Both GABAs = AKG = Female (Left Side Sink).
# 2. Male = Glutamate (AKG + Nitrogen) -> Serotonin (Right Side Competition).
# 3. 4x4 Fractal Time: Macro Forward (0->16) / Micro Reverse (3->0) ALWAYS.
# 4. Hysteresis (1/32), Spark (138.88), Torque (11/7), PLP Spine (X+Y=16).
# 5. The Narrative: Men borrow energy, lose Nitrogen, and surrender to the Female AKG Sink.
# =============================================================================

# --- LOCKED CONSTANTS ---
KAPPA_H2 = 1.0 / 32.0
SPARK_ANGLE = math.radians(138.88)
TORQUE_RATIO = 11.0 / 7.0
PLP_LEVEL = 16.0

ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
BLOOD_TYPES = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]

# Starting Columns (Dawn: Y=0.5)
COL_W = {"EJ": 0.5, "EP": 2.5, "IJ": 4.5, "IP": 6.5}
COL_M = {"IP": 9.5, "IJ": 11.5, "EP": 13.5, "EJ": 15.5}

BLOOD_MASS = {"O": 1.3, "A": 1.0, "B": 0.7, "AB": 0.5}

def get_fractal_time(y):
    # Macro flow (0 to 16)
    macro_idx = int(y) 
    # Micro flow (Reverse within each macro unit)
    # Each 1.0 Y unit is one Macro window containing 1 Micro cycle
    # For a 4x4 system over 16 units, each 4 units is a major Macro window.
    # But for trajectory resolution, we treat each unit as a pulse.
    micro_prog = y % 1.0
    is_reverse = micro_prog > 0.7 # Suction phase
    return is_reverse

def simulate_quasar():
    results = []
    dt = 0.05
    
    for mbti in ALL_MBTI:
        for blood in BLOOD_TYPES:
            for gender in GENDERS:
                ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
                
                # Initial Position
                grp = f"{ei}{jp}"
                x = COL_W[grp] if gender == "F" else COL_M[grp]
                y = 0.5
                
                # Add blood/type jitter
                x += (0.2 if blood in ["A", "AB"] else -0.2)
                
                vx, vy = 0.0, 0.0
                path = [(x, y)]
                mem_x, mem_y = x, y
                
                # Nitrogen Fuel (Male only starts with it)
                nitrogen_fuel = 1.0 if gender == "M" else 0.0
                
                for _ in range(1200):
                    # 1. Fractal Time Pulse
                    is_rev = get_fractal_time(y)
                    
                    # 2. AKG Sink (Left Side Gravity)
                    # The AKG Sink is the Female essence (Small Man).
                    # It pulls harder as Male Nitrogen drops.
                    akg_target_x = 3.0 
                    akg_pull = 0.4 if is_rev else 0.1
                    
                    # Male Exhaustion (Glutamate -> AKG)
                    # As Y increases, Nitrogen is lost to competition.
                    exhaustion = math.pow(y / 16.0, 1.5) if gender == "M" else 0.0
                    
                    # 3. Forces
                    # Torque (11/7) - Men outward, Women inward
                    if gender == "M":
                        # Competition drive (Rightwards) vs Suction (Leftwards)
                        drive_x = 14.5 * (1.0 - exhaustion) + akg_target_x * exhaustion
                        fx = (drive_x - x) * (7.0/11.0) * (0.8 if not is_rev else 0.2)
                    else:
                        # Women stay in the AKG/GABA zone
                        fx = (akg_target_x - x) * (11.0/7.0) * 0.2

                    # 4. PLP Spine (x+y=16) Seam
                    spine_dist = (x + y) - 16.0
                    fx_spine = -np.sign(spine_dist) * 0.3 * (1.0 - exhaustion)
                    
                    # 5. Hysteresis (1/32)
                    hx = (mem_x - x) * KAPPA_H2 * 5.0
                    hy = (mem_y - y) * KAPPA_H2 * 5.0
                    
                    # 6. Spark Leap (138.88)
                    # Triggered by N-type tension or Suction phase
                    if sn == "N" and is_rev and y > 4.0:
                        vx += math.cos(SPARK_ANGLE) * 1.2 * (-1 if gender == "M" else 1)
                        vy += math.sin(SPARK_ANGLE) * 0.5
                    
                    # Integration
                    ax = (fx + fx_spine + hx) / BLOOD_MASS[blood]
                    ay = (1.2 - hy) / BLOOD_MASS[blood] # Constant time fall
                    
                    # Damping (J=controlled, P=loose)
                    damping = 0.88 if jp == "J" else 0.96
                    vx = (vx + ax * dt) * damping
                    vy = (vy + ay * dt) * damping
                    
                    x += vx * dt
                    y += vy * dt
                    
                    # Boundary
                    x = max(0.1, min(15.9, x))
                    
                    # Update Hysteresis Memory
                    mem_x += (x - mem_x) * KAPPA_H2
                    mem_y += (y - mem_y) * KAPPA_H2
                    
                    path.append((x, y))
                    if y >= 16.0: break
                
                # Color logic: Red (Glutamate/Hot) -> Blue/Dark (AKG/Cold/Female)
                color_map = {"O": "#FF0000", "A": "#0000FF", "B": "#00FF00", "AB": "#FF00FF"}
                c = np.array(plt.cm.colors.to_rgb(color_map[blood]))
                if gender == "M":
                    # Fade to AKG-darkness as nitrogen drops
                    c = c * (1.0 - exhaustion) + np.array([0.1, 0.1, 0.3]) * exhaustion
                
                results.append({'path': np.array(path), 'color': c, 'alpha': 0.5})
                
    return results

def render(trajs):
    plt.figure(figsize=(20, 20), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Melatonin Bridge
    plt.axvline(8, color='#333333', lw=2, ls='--')
    # PLP Spine
    plt.plot([0, 16], [16, 0], color='orange', lw=1, alpha=0.4)
    
    for t in trajs:
        plt.plot(t['path'][:, 0], t['path'][:, 1], color=t['color'], alpha=t['alpha'], lw=0.8)
    
    plt.xlim(0, 16)
    plt.ylim(16, 0)
    plt.axis('off')
    
    plt.title("THE DEFINITIVE 128 QUASAR: AKG SINK & NITROGEN EXHAUSTION", color='white', fontsize=24)
    plt.savefig("FINAL_128_QUASAR_INTEGRATED.png", dpi=300, facecolor='black', bbox_inches='tight')
    print("--- SUCCESS: FINAL_128_QUASAR_INTEGRATED.png generated. ---")

if __name__ == "__main__":
    render(simulate_quasar())
