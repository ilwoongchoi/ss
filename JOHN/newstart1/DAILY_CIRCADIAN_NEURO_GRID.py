# -*- coding: utf-8 -*-
"""
DAILY_CIRCADIAN_NEURO_GRID.py
The 24-Hour Circadian Rhythm Grid for 128 Types.
Y-axis: 0 to 16 represents the 24 hours of a single day.
Physics: Brain Ratio (-0.5:1:0.5:1.5), Circadian D2 Toggles, Hormonal Tension.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from geometry_package.absolute_constants import *
from geometry_package import universal_equation as unieq

# 1. BRAIN POTENTIAL RATIO (-0.5 : 1 : 0.5 : 1.5)
# Left to Right Hemisphere mapping
def get_brain_potential(x):
    if x < 4: return -0.5  # GABA Zone
    if x < 8: return 1.0   # ACh Zone
    if x < 12: return 0.5  # Glu Zone
    return 1.5             # 5HT Zone

# 2. NEUROCHEMICAL METABOLISM
def get_metabolism(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Blood Type = Daily Energy Engine
    v_thrust = {"O": 1.6, "A": 0.9, "B": 1.3, "AB": 1.1}[blood]
    h_damping = {"O": 0.4, "A": 1.6, "B": 0.7, "AB": 1.0}[blood]
    
    # Hormonal Baseline
    is_T = (tf == "T") # Testosterone: Resistance
    is_F = (tf == "F") # Estrogen/Progesterone: Amity
    
    return {
        "thrust": v_thrust, "damping": h_damping,
        "is_T": is_T, "is_F": is_F,
        "ei": ei, "sn": sn, "jp": jp, "gender": gender, "blood": blood
    }

# 3. CIRCADIAN FIELD OPERATOR
def calculate_daily_velocity(x, y, c, d2_side):
    # Base 31:1 Daily Flow
    # A. Brain Potential Force (Hemispheric pull)
    potential_grad = get_brain_potential(x)
    if c["gender"] == "F":
        v_potential = -potential_grad * 0.2 if x > 8 else potential_grad * 0.1
    else:
        v_potential = potential_grad * 0.2 if x < 8 else -potential_grad * 0.1
        
    # B. Circadian D2 Toggle (Lie/Extraversion Muscle)
    v_d2 = 0.0
    if d2_side == "L": # Left D2 ON
        v_d2 = (4.0 - x) * 0.3 
    else: # Right D2 ON
        v_d2 = (12.0 - x) * 0.3 
        
    # C. Social/Hormonal Tension
    v_hormone = 0.0
    if c["is_T"]: v_hormone -= np.sign(x - 8.0) * 0.15 # Push away from center
    if c["is_F"]: v_hormone += np.sign(8.0 - x) * 0.1  # Pull to center
        
    # Total Hourly Flow
    vx = (v_potential + v_d2 + v_hormone) * c["thrust"]
    vy = (1.5 if c["gender"] == "M" else 0.8) * c["thrust"]
    
    return np.array([vx, vy])

# 4. DAILY CYCLE GENERATOR
def generate_daily_cycle(mbti, blood, gender):
    c = get_metabolism(mbti, blood, gender)
    
    # Morning Wake-up State (Seed)
    group_map_f = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    group_map_m = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    base_x = group_map_f[mbti[0]+mbti[3]] if gender == "F" else group_map_m[mbti[0]+mbti[3]]
    
    x = base_x + 1.0 + (np.random.uniform(-0.1, 0.1))
    y = 0.5
    start_pos = np.array([x, y])
    pts = [start_pos.copy()]
    
    dt = 0.1
    # 24 Hours modeled in steps
    for step in range(160):
        if y >= 16.0: break
        
        # Circadian Toggle: D2 switches states periodically throughout the day
        d2_side = "L" if (step // 20) % 2 == 0 else "R"
        
        V = calculate_daily_velocity(x, y, c, d2_side)
        
        x += V[0] * dt / c["damping"]
        y += V[1] * dt
        
        # SLEEP RESET (The 45-min Dream Folding Rule)
        # Men: Deep sleep reset at 1:30 AM (y=13)
        # Women: Deep sleep reset at 3:00 AM (y=14)
        is_rem_sleep = (y >= 13.0 and y < 13.5) if gender == "M" else (y >= 13.5 and y < 14.0)
        
        if is_rem_sleep:
            pts.append(start_pos.copy()) # Wake up reset
            break
            
        pts.append(np.array([x, y]))
        
    return pts

# 5. RENDERING
def main():
    print("Simulating 24-Hour Circadian Grid for 128 Types...")
    fig, ax = plt.subplots(figsize=(32, 20))
    fig.patch.set_facecolor("#FFFFFF")
    
    # Pure 16x16 Grid representing hours
    for i in range(17):
        ax.axhline(i, color="#F0F0F0", lw=0.5, zorder=0)
        ax.axvline(i, color="#F0F0F0", lw=0.5, zorder=0)

    MBTI_16 = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
    BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    for m in MBTI_16:
        for b in ["O", "A", "B", "AB"]:
            for g in ["M", "F"]:
                pts = generate_daily_cycle(m, b, g)
                xs, ys = zip(*pts)
                
                bc = np.array(plt.cm.colors.to_rgba(BLOOD_COLORS[b]))[:3]
                color = 0.8 * bc + 0.2 * (np.array([1,0.5,0]) if g=="F" else np.array([0,0.5,1]))
                ax.plot(xs, ys, color=color, alpha=0.3, lw=0.7, zorder=10)

    labels = ["EJ WOMEN", "EP WOMEN", "IJ WOMEN", "IP WOMEN", "IP MEN", "IJ MEN", "EP MEN", "EJ MEN"]
    for i, label in enumerate(labels):
        ax.text(i*2 + 1, -0.8, label, ha="center", weight="bold", size=14)

    ax.set_title("128-TYPE DAILY CIRCADIAN GRID | 24-Hour Neurochemical Cycle", 
                 fontsize=28, pad=60, weight="bold")
    ax.set_xlim(-1, 17); ax.set_ylim(17, -2); ax.axis("off")
    
    output = "128_DAILY_CIRCADIAN_GRID.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Success: {output} rendered as a single day's cycle.")

if __name__ == "__main__":
    main()
