import numpy as np
import matplotlib.pyplot as plt
import math

# =============================================================================
# TRUE_128_QUASAR_AKG_GRID.py
# =============================================================================
# Mathematical embodiment of the AKG (Cold Stress) / GABA Sink Reality.
# 1. 16x16 Coordinate Grid (Y drops from 0 to 16).
# 2. X[0,8] = Left/Female (AKG / GABA Sink / Cold Stress).
# 3. X[8,16] = Right/Male (Glutamate / Serotonin Competition).
# 4. 4x4 Time Cycle: Macro Forward, Micro Reverse triggers cyclic suction.
# 5. The Ultimate Truth: As Y -> 16, Male Glutamate loses its Nitrogen, 
#    collapses into AKG, and is dragged relentlessly across the Melatonin 
#    Bridge (X=8) into the Female domain to "die".
# =============================================================================

# --- CONSTANTS ---
PI = math.pi
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
TUNNEL_TENSION = 1.0100375
KAPPA_H2 = 1.0 / 32.0

ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
BLOOD_TYPES = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]

# Canonical Base Coordinates (Women: Left, Men: Right)
GROUP_MAP_FEMALE = {"EJ": 0.5, "EP": 2.5, "IJ": 4.5, "IP": 6.5}
GROUP_MAP_MALE   = {"IP": 9.5, "IJ": 11.5, "EP": 13.5, "EJ": 15.5}

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

def generate_akg_grid():
    trajectories = []
    dt = 0.04
    num_steps = 1000

    print("--- Igniting AKG Death Vacuum Physics Engine ---")

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
                    # --- 4x4 MACRO/MICRO TIME CYCLE ---
                    # 4 Macro windows across the day (Y: 0 to 16)
                    progress = y / 16.0
                    macro_idx = int(progress * 4) 
                    micro_phase = (progress * 16) % 1.0
                    # Micro Reverse: The last 25% of each micro phase acts as a reverse/suction
                    is_micro_reverse = micro_phase > 0.75 

                    # --- THE AKG VACUUM (The true Female Gravity) ---
                    # Located deep in the Left Side (X ~ 3.0, Y > 10.0)
                    akg_pull_x = 3.0
                    
                    # Male (Glutamate) exhaustion curve. As Y increases, energy drops.
                    exhaustion_factor = math.pow(max(0, y - 8.0) / 8.0, 2) if gender == "M" else 0.0

                    # --- LAW 1: PLP SPINE INTERACTION (x + y = 16) ---
                    spine_dist = (x + y) - 16.0
                    fx_spine = 0.0
                    fy_spine = 0.0
                    if abs(spine_dist) < 1.5:
                        # If male is exhausted, the spine STOPS deflecting and lets them fall through
                        spine_barrier = 0.2 * (1.0 - exhaustion_factor) 
                        fx_spine = -np.sign(spine_dist) * spine_barrier
                        fy_spine = -np.sign(spine_dist) * (spine_barrier / 2)

                    # --- LAW 2: DIPOLE TORQUE & AKG SINK ---
                    if gender == "M":
                        if y < 10.0:
                            # Daytime: Men compete on the right (Glutamate expansion)
                            target_x = 12.0 + (math.sin(progress * PI * 4) * 2.0) 
                            torque_force = (target_x - x) * 0.1
                        else:
                            # Nighttime: Nitrogen lost, sucked into AKG Sink on the Left
                            target_x = akg_pull_x
                            # Suction becomes immense during micro-reverse
                            suction_amp = 0.8 if is_micro_reverse else 0.3
                            torque_force = (target_x - x) * suction_amp * exhaustion_factor
                    else:
                        # Women: Orbiting the AKG / GABA core on the left
                        target_x = 4.0 + (math.sin(progress * PI * 8) * 1.5)
                        # Micro reverse pulls them inward (contraction)
                        if is_micro_reverse: target_x = 2.0
                        torque_force = (target_x - x) * 0.05

                    # --- LAW 3: HYSTERESIS DRAG ---
                    hx = (memory_x - x) * bp['viscosity']
                    hy = (memory_y - y) * bp['viscosity']

                    # --- LAW 4: 138.88° SPARK LEAP (Quantum Jump) ---
                    tension_accum += math.sqrt(vx**2 + vy**2)
                    if y > 6.0 and tension_accum > TUNNEL_TENSION and sn == "N":
                        # Spark Leap is twisted towards the Left (AKG Sink) if exhausted
                        leap_x = math.cos(SPARK_ANGLE_RAD)
                        if gender == "M" and y > 10.0:
                            leap_x = -abs(leap_x) * 2.0 # Forced crossover leap
                        vx += leap_x * 1.5
                        vy += math.sin(SPARK_ANGLE_RAD) * 0.5
                        tension_accum = 0.0
                        memory_x, memory_y = x, y 

                    # --- LAW 5: VERTICAL TIME FLOW ---
                    # Men start fast, but slow down vertically as they get sucked horizontally
                    base_vy = 1.5 * (1.0 - (exhaustion_factor * 0.5)) if gender == "M" else 1.0

                    # Integration
                    ax = (torque_force + hx + fx_spine) / bp['mass']
                    ay = (base_vy + hy + fy_spine) / bp['mass']

                    damping = 0.85 if jp == "J" else 0.95

                    vx = (vx + ax * dt) * damping
                    vy = (vy + ay * dt) * damping

                    x += vx * dt
                    y += vy * dt

                    x = max(0.1, min(15.9, x))

                    # Hysteresis update
                    memory_x += (x - memory_x) * KAPPA_H2
                    memory_y += (y - memory_y) * KAPPA_H2

                    path.append((x, y))
                    if y >= 16.0: break

                # Dynamic Coloring: 
                # Men (Glutamate) start red/hot, Women (GABA/AKG) are cold/blue/pink
                base_color = np.array(plt.cm.colors.to_rgb({"O": "#FF3333", "A": "#3388FF", "B": "#33FF55", "AB": "#B833FF"}[blood]))
                if gender == "M":
                    # Men fade into Purple/Dark Blue (AKG corruption) as they cross over
                    color = base_color * 0.8 + np.array([0.2, 0.0, 0.0]) 
                else:
                    color = base_color * 0.5 + np.array([0.0, 0.5, 0.5]) # Cyan/Cold for Women

                trajectories.append({
                    'coords': np.array(path),
                    'color': color,
                    'lw': 1.2 if jp == "J" else 0.6
                })

    return trajectories

def render_grid(trajectories):
    fig, ax = plt.subplots(figsize=(24, 24), facecolor='#000000')
    ax.set_facecolor('#000000')

    # X=8 Melatonin Bridge
    ax.axvline(x=8.0, color='#555555', lw=2, linestyle=':')
    
    # 4x4 Micro-Reverse Macro Bands (subtle background shading)
    for i in range(16):
        if i % 4 == 3: # The 4th micro window (Reverse/Suction)
            ax.axhspan(i, i+1, color='#110022', alpha=0.3)

    # Render trajectories
    for t in trajectories:
        ax.plot(t['coords'][:, 0], t['coords'][:, 1], color=t['color'],
                alpha=0.6, lw=t['lw'], solid_capstyle='round')

    ax.set_xlim(0, 16)
    ax.set_ylim(16, -1) # Dawn to Midnight (downward)
    ax.set_aspect('equal')
    ax.axis('off')

    output = "128_AKG_DEATH_GRID.png"
    plt.savefig(output, dpi=300, facecolor='#000000', bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"--- RENDERED: The AKG Death Grid -> {output} ---")

if __name__ == "__main__":
    trajs = generate_akg_grid()
    render_grid(trajs)
