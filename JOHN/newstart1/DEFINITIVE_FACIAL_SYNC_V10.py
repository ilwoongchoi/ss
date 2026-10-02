import numpy as np
import matplotlib.pyplot as plt
import math

def render_2d_facial_sovereign_sync():
    # --- 1. CONFIG & CONSTANTS ---
    N_TYPES = 128
    STEPS = 300
    DELTA_T_OBS = 0.2828
    SPARK_RAD = math.radians(138.88)
    
    # 128 Node Setup: 16x8 (M/F split)
    mbtis = ['ESTJ','ENTJ','ESFJ','ENFJ','ESTP','ENTP','ESFP','ENFP',
             'ISTJ','INTJ','ISFJ','INFJ','ISTP','INTP','ISFP','INFP']
    bloods = ['O', 'A', 'B', 'AB']
    genders = ['M', 'F']
    
    fig, ax = plt.subplots(figsize=(16, 16), facecolor='black')
    ax.set_facecolor('black')
    
    # Draw Facial Grid Background
    for i in range(17):
        ax.axhline(i, color='#222222', lw=0.5)
        ax.axvline(i, color='#222222', lw=0.5)
    
    # PLP Spine (The 16.0 Equilibrium)
    ax.plot([0, 16], [16, 0], color='#ff9900', ls='--', alpha=0.4, lw=2, label='PLP Spine')
    # Zero Point Midline (The Anchor)
    ax.axvline(8.0, color='gold', ls='-', alpha=0.6, lw=3, label='HUGE-LQG MIDLINE (X=8.0)')

    # --- 2. TRAJECTORY GENERATION (2D PROJECTION) ---
    trajectories = []
    
    print("Generating 128 Sovereign Facial Trajectories...")
    
    idx = 0
    for mbti in mbtis:
        for blood in bloods:
            for gender in genders:
                # Initial Position based on Topology
                is_m = gender == 'M'
                is_e = mbti[0] == 'E'
                
                # Starting X: M(Right), F(Left)
                x0 = 8.5 + (4.0 if is_e else 1.0) if is_m else 7.5 - (4.0 if is_e else 1.0)
                # Starting Y: Blood metabolic height
                blood_y = {'O': 2.0, 'A': 6.0, 'B': 10.0, 'AB': 14.0}[blood]
                y0 = blood_y + (1.0 if mbti[3] == 'J' else -1.0)
                
                pos = np.array([x0, y0], dtype=float)
                path = [pos.copy()]
                
                # Binary Physics (Betti 7 Bits)
                # 0: Gender Polarity, 1: MBTI E/I, 2: J/P, 3: Blood Phase
                bits = [1 if is_m else 0, 1 if is_e else 0, 1 if mbti[3]=='J' else 0, 0]
                
                # Recursive Seed C
                angle = (idx / N_TYPES) * 2 * np.pi
                C = complex(math.cos(angle) * DELTA_T_OBS, math.sin(angle) * DELTA_T_OBS)
                Z = complex(0, 0)
                
                for t_step in range(STEPS):
                    t = t_step * 0.1
                    
                    if t < DELTA_T_OBS:
                        continue
                    
                    # Ignition & Phase Counter-Rotation
                    # Night Window Effect (Gender Sync after half-time)
                    is_night = t_step > (STEPS // 2)
                    
                    # The Soliton Breath (Recursive)
                    damping = 0.02
                    Z = (Z**2 + C) * (1.0 - damping)
                    if abs(Z) > 3.0: Z = (Z / abs(Z)) * 3.0
                    
                    # Radial Distance from Start
                    radius = abs(Z) * 0.5
                    theta = math.atan2(Z.imag, Z.real)
                    
                    # Spark Clearing (138.88)
                    if t_step % 25 == 0:
                        theta += SPARK_RAD
                    
                    # Target Point (Midline Sync at Night)
                    target_x = 8.0 if is_night else (14.0 if is_m else 2.0)
                    
                    # Velocity Vectors
                    # vx: Towards target/midline
                    vx = (target_x - pos[0]) * 0.05
                    # vy: Towards metabolic equilibrium (Spine)
                    target_y = (16.0 - pos[0]) # Aim for PLP Spine
                    vy = (target_y - pos[1]) * 0.03 + (0.1 if mbti[3]=='J' else -0.1)
                    
                    pos[0] += vx + (radius * math.cos(theta)) * 0.1
                    pos[1] += vy + (radius * math.sin(theta)) * 0.1
                    
                    path.append(pos.copy())
                
                path_arr = np.array(path)
                trajectories.append(path_arr)
                
                # Plot the path
                color = '#00aaff' if is_m else '#ff33aa' # Blue(M), Pink(F)
                ax.plot(path_arr[:,0], path_arr[:,1], color=color, alpha=0.3, lw=0.6)
                
                # Mark initial node
                ax.scatter(x0, y0, color=color, s=20, edgecolors='white', lw=0.5)
                
                idx += 1

    # --- 3. THE GENDER SYNC MARKER ---
    # Show where they meet (X=8.0)
    ax.scatter([8.0]*16, np.linspace(2, 14, 16), color='gold', s=100, marker='*', label='GENDER SYNC NODES')

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_axis_off()
    ax.set_title("V10 FACIAL TOPOLOGY: GENDER SYNC BINARY TRAJECTORIES\n(Blue: Male, Pink: Female, Gold: Night Meeting Point)", color='white', fontsize=18)
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white', loc='upper right')
    
    output_fn = "V10_FACIAL_GENDER_SYNC.png"
    plt.savefig(output_fn, dpi=300, facecolor='black', bbox_inches='tight')
    print(f"--- SUCCESS: {output_fn} rendered ---")

if __name__ == "__main__":
    render_2d_facial_sovereign_sync()
