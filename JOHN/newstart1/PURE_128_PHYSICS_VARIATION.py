import numpy as np
import matplotlib.pyplot as plt
import math

# --- 128-TYPE PHYSICAL PARAMETER TABLE ---
ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
BLOOD_TYPES = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]

# Constants
KAPPA_H2 = 1.0 / 32.0  # Darcy Flux Delay
SPARK_ANGLE = math.radians(138.88)
TORQUE_W = 11.0 / 7.0
TORQUE_M = 7.0 / 11.0

# Starting Slots (Y=0)
COL_W = {"EJ": 0.5, "EP": 2.5, "IJ": 4.5, "IP": 6.5}
COL_M = {"IP": 9.5, "IJ": 11.5, "EP": 13.5, "EJ": 15.5}

def run_128_physics():
    trajs = []
    dt = 0.05
    
    for mbti in ALL_MBTI:
        for blood in BLOOD_TYPES:
            for gender in GENDERS:
                ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
                
                # 1. Physical Profile Assignment
                mass = {"O": 1.3, "A": 1.0, "B": 0.7, "AB": 0.5}[blood]
                damping = 0.85 if jp == "J" else 0.98
                torsion_amp = 0.3 if tf == "F" else 0.0
                has_spark = (sn == "N")
                
                # Initial state
                grp = f"{ei}{jp}"
                x = COL_W[grp] if gender == "F" else COL_M[grp]
                y = 0.5
                vx, vy = 0.0, 0.0
                path = [(x, y)]
                mem_x, mem_y = x, y
                
                for step in range(800):
                    # --- DYNAMIC PHYSICS CALCULATION ---
                    
                    # 2. Torque Force (Gender specific)
                    # Women pull to Melatonin Ridge (8.0), Men push to extremes
                    target_x = 8.0 if gender == "F" else (15.5 if ei == "E" else 8.5)
                    t_ratio = TORQUE_W if gender == "F" else TORQUE_M
                    fx_torque = (target_x - x) * t_ratio * 0.1
                    
                    # 3. Torsion (Feeling based oscillation)
                    fx_torsion = math.sin(y * 2.0) * torsion_amp
                    
                    # 4. Hysteresis (1/32 Delay)
                    # Heavier blood (O) feels this drag more.
                    hx = (mem_x - x) * KAPPA_H2 * 4.0
                    hy = (mem_y - y) * KAPPA_H2 * 4.0
                    
                    # 5. Spark Leap (138.88 Deg)
                    # Occurs randomly for N-types, jump distance inversely proportional to mass
                    if has_spark and step % 100 == 0 and y > 3.0:
                        jump = 1.0 / mass
                        x += math.cos(SPARK_ANGLE) * jump
                        y += math.sin(SPARK_ANGLE) * (jump * 0.5)
                    
                    # 6. Summation
                    ax = (fx_torque + fx_torsion + hx) / mass
                    ay = (1.0 - hy) / mass # Gravity flow
                    
                    vx = (vx + ax * dt) * damping
                    vy = (vy + ay * dt) * damping
                    
                    x += vx * dt
                    y += vy * dt
                    
                    # 7. Memory Update (Hysteresis)
                    mem_x += (x - mem_x) * KAPPA_H2
                    mem_y += (y - mem_y) * KAPPA_H2
                    
                    path.append((x, y))
                    if y >= 16.0: break
                
                # Assign color by blood and gender polarity
                base_c = {"O": [1,0,0], "A": [0,0,1], "B": [0,1,0], "AB": [0.8,0,0.8]}[blood]
                trajs.append({'path': np.array(path), 'color': base_c, 'gender': gender})
                
    return trajs

def render(trajs):
    plt.figure(figsize=(20, 20), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Grid markers
    plt.axvline(8, color='#444444', lw=2, ls='--') # Melatonin
    plt.plot([0,16],[16,0], color='orange', lw=1, alpha=0.3) # PLP Spine
    
    for t in trajs:
        alpha = 0.6 if t['gender'] == 'F' else 0.4
        plt.plot(t['path'][:, 0], t['path'][:, 1], color=t['color'], alpha=alpha, lw=0.7)
        
    plt.xlim(0, 16)
    plt.ylim(16, 0) # Top down
    plt.axis('off')
    plt.savefig("PURE_128_PHYSICS_VARIATION.png", dpi=300, facecolor='black', bbox_inches='tight')
    print("--- SUCCESS: PURE_128_PHYSICS_VARIATION.png generated ---")

if __name__ == "__main__":
    render(run_128_physics())
