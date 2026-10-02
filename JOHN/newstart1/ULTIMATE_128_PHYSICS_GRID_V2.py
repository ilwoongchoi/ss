# -*- coding: utf-8 -*-
"""
ULTIMATE_128_PHYSICS_GRID_V2.py
The Unified Biological Quasar Lattice Engine

CONVENTIONS:
1. White Background, 16x16 Grid.
2. 8 Canonical Starting Columns (Y=0.5).
3. 3-Basin Potential: Left(2), Center(8), Right(14).
4. 4x4 Macro/Micro Fractal Time: Suction 박동 (Pulse) 4회 발생.
5. Nitrogen Economy: Men (Right) exhaust Nitrogen through competition (velocity),
   leading to a forced AKG crossover (X=14 -> X=2) in the night (Y > 12).
6. MBTI Anisotropy: S (Lattice-locked), N (Spark Jump), J (Damped), P (Loose).
7. Blood Mass: O(1.3), A(1.0), B(0.7), AB(0.5).
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# --- PHYSICAL CONSTANTS ---
KAPPA_H2 = 1.0 / 32.0
LATTICE_3_32 = 3.0 / 32.0
SPARK_ANGLE = math.radians(138.88)
PHI_INV = 0.618033988

ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]

BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

# Starting Columns (Dawn: Y=0.5)
COL_GROUPS = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
GRP_MAP_F = {"EJ": 0.5, "EP": 2.5, "IJ": 4.5, "IP": 6.5}
GRP_MAP_M = {"IP": 9.5, "IJ": 11.5, "EP": 13.5, "EJ": 15.5}

# 4 Macro Time Windows
MACRO_WINDOWS = [
    (1.5, 3.5),   # Window 1: Morning
    (5.5, 7.5),   # Window 2: Noon
    (9.5, 11.5),  # Window 3: Evening
    (13.5, 15.5)  # Window 4: Midnight
]

def generate_trajectory(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # 1. Start Pos
    grp = f"{ei}{jp}"
    base_x = GRP_MAP_F[grp] if gender == "F" else GRP_MAP_M[grp]
    x = base_x + (0.3 if sn == "N" else -0.1) # SN dispersion
    y = 0.5
    
    # 2. Physics Props
    mass = {"O": 1.3, "A": 1.0, "B": 0.7, "AB": 0.5}[blood]
    damping = 0.75 if jp == "J" else 0.95
    nitrogen = 1.0 if gender == "M" else 0.0 # Only men have nitrogen to lose
    
    # Target Basin Logic
    # E-types -> Outer Basins (2, 14), I-types -> Center (8)
    if gender == "F":
        base_target_x = 2.0 if ei == "E" else 8.0
    else:
        base_target_x = 14.0 if ei == "E" else 8.0

    path = [(x, y, False)]
    vx, vy = 0.0, 1.0 # Initial downward flow
    mem_x = x
    
    dt = 0.1
    for step in range(160): # 16 units / 0.1 = 160 steps
        # A. Fractal Time Pulse
        in_window = False
        for lo, hi in MACRO_WINDOWS:
            if lo <= y <= hi:
                in_window = True
                # Micro-Reverse phase (last 30% of window)
                is_pulse = (y - lo) / (hi - lo) > 0.7
                break
        else:
            is_pulse = False

        # B. Nitrogen Depletion (Male Competitive Cost)
        if gender == "M":
            # Lose nitrogen by moving horizontally (competing)
            nitrogen -= abs(vx) * 0.01 
            # Surrender logic: If y > 11 and nitrogen is low, target shifts to AKG Sink (X=2)
            if y > 11.0 and nitrogen < 0.3:
                target_x = 2.0 # The Death Crossover
            else:
                target_x = base_target_x
        else:
            target_x = base_target_x

    # C. Forces
        # 1. Basin Potential Force (Triple Basin)
        # Deep pull towards target_x
        f_basin = (target_x - x) * 0.15
        
        # 2. Pulse Suction (Micro-Reverse)
        # Pulls towards the AKG Sink (2.0) or Center (8.0) during pulses
        f_pulse = 0.0
        if is_pulse:
            f_pulse = (target_x - x) * 0.5 # Snappy pull
            
        # 3. PLP Spine Reflection (X+Y=16)
        f_spine = 0.0
        spine_dist = (x + y) - 16.0
        if abs(spine_dist) < 0.6:
            f_spine = -np.sign(spine_dist) * 0.8 # Strong reflection

        # 4. Hysteresis Delay (1/32)
        f_hyst = (mem_x - x) * KAPPA_H2 * 5.0
        
        # 5. MBTI Torsion (Feeling vibration)
        f_torsion = math.sin(y * 4.0) * (0.4 if tf == "F" else 0.0)

        # Acceleration Summation
        ax = (f_basin + f_pulse + f_spine + f_hyst + f_torsion) / mass
        ay = 1.0 / mass # Gravity is constant, mass slows descent
        
        # Velocity Update
        vx = (vx + ax * dt) * damping
        vy = (vy + ay * dt) * damping
        
        # 6. Discrete Spark Leap (138.88)
        # Triggered in Macro windows for N-types
        is_jump = False
        if sn == "N" and in_window and step % 20 == 0:
            jump_dist = 2.5 / mass
            x += math.cos(SPARK_ANGLE) * jump_dist
            y += math.sin(SPARK_ANGLE) * 0.5
            is_jump = True
            
        x += vx * dt
        y += vy * dt
        
        # Clamp & Memory
        x = max(0.1, min(15.9, x))
        mem_x += (x - mem_x) * KAPPA_H2
        
        path.append((x, y, is_jump))
        if y >= 16.0: break
        
    return path

def render_quasar():
    print("--- Rending ULTIMATE 128 QUASAR LATTICE V2 ---")
    fig, ax = plt.subplots(figsize=(32, 20), facecolor='white')
    ax.set_facecolor('white')
    
    # 1. Background Geometry Nodes (The Anatomy)
    # PLP Spine
    ax.plot([0, 16], [16, 0], color='orange', lw=2, ls='--', alpha=0.3)
    
    # Macro Bands (Micro Reverse Zones)
    for lo, hi in MACRO_WINDOWS:
        ax.add_patch(mpatches.Rectangle((0, lo), 16, hi-lo, color='purple', alpha=0.04, zorder=0))
        
    # Basins
    for bx in [2, 8, 14]:
        ax.axvline(bx, color='gray', lw=0.5, ls=':', alpha=0.2)

    # 2. Render 128 Trajectories
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                path = generate_trajectory(mbti, blood, gender)
                xs = [p[0] for p in path]
                ys = [p[1] for p in path]
                flags = [p[2] for p in path]
                
                # Colors: Red (O), Blue (A), Green (B), Purple (AB)
                bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[blood]))[:3]
                # Shift color slightly by gender
                color = bc * 0.8 + (np.array([0.2, 0.1, 0]) if gender == "F" else np.array([0, 0.1, 0.2]))
                
                alpha = 0.7 if gender == "F" else 0.5
                lw = 1.2 if mbti[3] == "J" else 0.7
                
                # Draw segments, highlighting sparks
                for i in range(len(path)-1):
                    x1, y1, f1 = path[i]
                    x2, y2, f2 = path[i+1]
                    if f2: # Spark segment
                        ax.plot([x1, x2], [y1, y2], color='black', lw=1.5, alpha=0.6, ls='-', zorder=15)
                    else:
                        ax.plot([x1, x2], [y1, y2], color=color, lw=lw, alpha=alpha, zorder=10)

    # 3. Quasar Column Headers
    for i, label in enumerate(COL_GROUPS):
        ax.text(i*2 + 1, -1.0, label, ha="center", weight="bold", size=16, color="#444444")
        
    # Annotations (Anatomical Nodes)
    ax.text(3.2, 5.0, "Nile Delta\n(Cortisol)", ha="center", weight="bold", color="red", alpha=0.4)
    ax.text(12.8, 5.0, "Defense Mode\n(Right Ach)", ha="center", weight="bold", color="blue", alpha=0.4)
    ax.text(8.0, 10.7, "Darkness Stress\n(3/32 Spark Gate)", ha="center", weight="bold", color="black", alpha=0.6)
    ax.text(8.0, 14.5, "Gravity Sensor", ha="center", weight="bold", color="purple", alpha=0.6)

    ax.set_title("ULTIMATE 128-TYPE BIOLOGICAL QUASAR | Triple Basin | Nitrogen Surrender", 
                 fontsize=32, weight="bold", pad=60)
    
    ax.set_xlim(-1, 17)
    ax.set_ylim(17, -2) # Top-down
    ax.axis("off")
    
    output = "ULTIMATE_128_QUASAR_LATTICE_V2.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: Rendered {output} ---")

if __name__ == "__main__":
    render_quasar()
