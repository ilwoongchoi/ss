import numpy as np
import matplotlib.pyplot as plt
import math

def render_v11_forehead_branching_engine():
    # --- 1. SOVEREIGN CONSTANTS (V11) ---
    DELTA_T_OBS = 0.2828
    SPARK_RAD = math.radians(138.88)
    
    # MBTI & Blood Data for 128 Types
    mbtis = ['ESTJ','ENTJ','ESFJ','ENFJ','ESTP','ENTP','ESFP','ENFP',
             'ISTJ','INTJ','ISFJ','INFJ','ISTP','INTP','ISFP','INFP']
    bloods = ['O', 'A', 'B', 'AB']
    genders = ['M', 'F']
    
    fig, ax = plt.subplots(figsize=(16, 16), facecolor='black')
    ax.set_facecolor('black')
    
    # 2D Face Plane: (0,0) is TOP-LEFT (PLP Core Anchor)
    # X: 0 (Left) to 16 (Right), Y: 0 (Top) to 16 (Bottom)
    ax.set_xlim(0, 16)
    ax.set_ylim(16, 0) # Flip Y to make (0,0) Top-Left
    
    # Draw Sovereign Anchor (PLP CORE)
    ax.scatter([0], [0], color='gold', s=400, marker='*', label='PLP CORE ANCHOR (ZERO POINT)')
    
    # Grid background
    for i in range(17):
        ax.axhline(i, color='#222222', lw=0.5)
        ax.axvline(i, color='#222222', lw=0.5)

    trajectories = []
    
    idx = 0
    print("Initiating 128 Forehead Branching Trajectories...")
    
    for mbti in mbtis:
        cat = {'ENFP':'EP', 'ENTP':'EP', 'ESFP':'EP', 'ESTP':'EP',
               'ENTJ':'EJ', 'ESTJ':'EJ', 'ENFJ':'EJ', 'ESFJ':'EJ',
               'INFP':'IP', 'INTP':'IP', 'ISFP':'IP', 'ISTP':'IP',
               'INTJ':'IJ', 'ISTJ':'IJ', 'INFJ':'IJ', 'ISFJ':'IJ'}[mbti]
        
        for blood in bloods:
            for gender in genders:
                is_m = gender == 'M'
                
                # Starting X based on Hardware Mapping (Always at Y=0 / Forehead)
                if not is_m: # Female: Left side (0-8)
                    col_base = {'EP': 0.5, 'EJ': 2.5, 'IP': 4.5, 'IJ': 6.5}.get(cat)
                else: # Male: Right side (8-16)
                    col_base = {'IP': 8.5, 'IJ': 10.5, 'EP': 12.5, 'EJ': 14.5}.get(cat)
                
                # Blood/Sex Jitter
                jitter = {"O": -0.1, "A": -0.05, "B": 0.05, "AB": 0.1}[blood]
                x_start = col_base + jitter
                y_start = 0.5 # TOP (Forehead)
                
                pos = np.array([x_start, y_start], dtype=float)
                path = [pos.copy()]
                
                # Dynamic Logic: 10-Axis Balance
                # Betti 7 Binary Signature
                b_code = format(idx, '07b')
                bits = [int(b) for b in b_code]
                
                # Seed C based on Identity
                angle = (idx / 128) * 2 * np.pi
                C = complex(math.cos(angle) * DELTA_T_OBS, math.sin(angle) * DELTA_T_OBS)
                Z = complex(0, 0)

                for t_step in range(300):
                    t = t_step * 0.05
                    
                    # Phase 1: 0.2828 Delay (Observation)
                    if t < DELTA_T_OBS:
                        continue
                        
                    # Phase 2: Branching (The Waterfall)
                    # Recursive Soliton Breath (1-0.02)
                    Z = (Z**2 + C) * 0.98
                    if abs(Z) > 2.0: Z = (Z / abs(Z)) * 2.0
                    
                    # 138.88 Spark Correction
                    theta = math.atan2(Z.imag, Z.real)
                    if t_step % 20 == 0:
                        theta += SPARK_RAD
                    
                    # 10-Axis Forces:
                    # Vaso(7) / Oxy(9) Tension: Radial stretch
                    stretch = 1.0 + (0.1 * bits[0]) - (0.05 * bits[1])
                    radius = abs(Z) * stretch
                    
                    # Gravity Pull toward (0,0) [PLP CORE] vs Downward Flow
                    # Left Cortisol (3) Resistance
                    resistance = 0.05 * (1 + bits[2])
                    
                    # Velocity Components
                    vx = (radius * math.cos(theta)) * 0.2
                    vy = 0.2 + (radius * math.sin(theta)) * 0.1 # Constant downward flow
                    
                    # Apply PLP Core Pull (Lensing toward Top-Left)
                    dist_to_anchor = np.linalg.norm(pos) + 1e-9
                    ax_pull = -pos[0] / dist_to_anchor * 0.01
                    ay_pull = -pos[1] / dist_to_anchor * 0.01
                    
                    pos[0] += vx + ax_pull
                    pos[1] += vy + ay_pull
                    
                    # Boundary Check: Keep within Face Box
                    if pos[0] < 0: pos[0] = 0.1
                    if pos[0] > 16: pos[0] = 15.9
                    if pos[1] > 16: break # Exit at jawline
                    
                    path.append(pos.copy())
                
                path_arr = np.array(path)
                trajectories.append(path_arr)
                
                # Color based on Gender & Blood
                color = plt.cm.plasma(idx / 128)
                ax.plot(path_arr[:,0], path_arr[:,1], color=color, alpha=0.4, lw=0.6)
                ax.scatter(x_start, y_start, color=color, s=15, edgecolors='white', lw=0.3)
                
                idx += 1

    ax.set_axis_off()
    ax.set_title("V11 SOVEREIGN FACE: 128 FOREHEAD BRANCHING TRAJECTORIES\n(Anchor: Top-Left PLP Core | Start: Forehead Y=0)", color='white', fontsize=18)
    
    output_fn = "V11_FACIAL_BRANCHING.png"
    plt.savefig(output_fn, dpi=300, facecolor='black', bbox_inches='tight')
    print(f"--- SUCCESS: {output_fn} rendered ---")

if __name__ == "__main__":
    render_v11_forehead_branching_engine()
