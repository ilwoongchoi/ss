import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import math
import time

# =============================================================================
# NEW_128_TRAJECTORY_GRID_FINAL.py
# =============================================================================
# Pure, clean 128-trajectory 2D grid based on the advanced physics engine.
# No sensor/stress overlays. Exactly 128 distinct trajectory paths
# organized into the 8 canonical columns.
# =============================================================================

# --- CONSTANTS ---
F_3_32 = 3.0 / 32.0
F_1_64 = 1.0 / 64.0
SPARK_ANGLE_RAD = math.radians(138.88)
N_SPARK_ANGLE = math.radians(69.44)

NEURO_ZONES = {
    'GABA':  {'x_range': (0, 4),   'potential': -0.5, 'charge': -1},
    'ACh':   {'x_range': (4, 8),   'potential': 1.0,  'charge': +1},
    'Glu':   {'x_range': (8, 12),  'potential': 0.5,  'charge': +1},
    '5HT':   {'x_range': (12, 16), 'potential': 1.5,  'charge': +2}
}

FEMALE = {'Vy': 0.8, 'Vx_amp': 2.8, 'loop_start': 13.5, 'loop_end': 14.0, 'zone_sensitivity': {'GABA': 1.5, 'ACh': 1.3, 'Glu': 0.5, '5HT': 0.3}, 'color_tint': (1.0, 0.2, 0.8)}
MALE = {'Vy': 1.5, 'Vx_amp': 1.2, 'loop_start': 13.0, 'loop_end': 13.5, 'zone_sensitivity': {'GABA': 0.3, 'ACh': 0.5, 'Glu': 1.3, '5HT': 1.5}, 'color_tint': (0.2, 0.8, 1.0)}

MBTI_DIM = {
    'E': {'radial_bias': 1.0, 'expansion': 0.3, 'target_x': 'outer'},
    'I': {'radial_bias': -1.0, 'contraction': 0.4, 'target_x': 'center'},
    'S': {'freq': 0.5, 'harmonic': 1, 'grid_coupling': 0.2, 'spark_prob': 0.0},
    'N': {'freq': 2.0, 'harmonic': 3, 'grid_coupling': 1.0, 'spark_prob': 0.3},
    'T': {'phase': 0, 'torsion': 0.2, 'swirl': 'minimal', 'straightness': 0.9},
    'F': {'phase': math.pi/4, 'torsion': 1.5, 'swirl': 'maximal', 'straightness': 0.3},
    'J': {'damping': 0.9, 'snap': 0.8, 'continuity': 'discrete', 'lattice_k': 1.0},
    'P': {'damping': 0.2, 'snap': 0.1, 'continuity': 'continuous', 'lattice_k': 0.1}
}

BLOOD = {
    'O':  {'mass': 1.3, 'decay': 0.92, 'momentum': 1.4, 'chaos': 0.0, 'curvature': 0.2, 'color': '#C62828'},
    'A':  {'mass': 1.0, 'decay': 0.98, 'momentum': 1.0, 'chaos': 0.0, 'curvature': 0.1, 'color': '#1565C0'},
    'B':  {'mass': 0.7, 'decay': 0.88, 'momentum': 0.8, 'chaos': 0.4, 'curvature': 0.8, 'color': '#2E7D32'},
    'AB': {'mass': 0.5, 'decay': 0.94, 'momentum': 0.6, 'chaos': 0.1, 'curvature': 0.5, 'color': '#6A1B9A'}
}

GROUP_F = {'EJ': 0, 'EP': 2, 'IJ': 4, 'IP': 6}
GROUP_M = {'IP': 8, 'IJ': 10, 'EP': 12, 'EJ': 14}
ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
GENDERS = ['F', 'M']

def get_initial_state(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    gp = FEMALE if gender == 'F' else MALE
    bp = BLOOD[blood]
    
    group_key = f"{ei}{jp}"
    base_x = GROUP_F[group_key] if gender == 'F' else GROUP_M[group_key]
    
    sn_off = 0.4 if sn == 'N' else 0.15
    sn_dir = 1 if ei == 'E' else -1
    x_offset_sn = sn_off * sn_dir
    
    tf_off = 0.2 if tf == 'F' else 0.1
    tf_dir = 1 if ei == 'E' else -1
    x_offset_tf = tf_off * tf_dir
    
    blood_offsets = {'O': -0.4, 'A': -0.15, 'B': 0.15, 'AB': 0.4}
    
    y_base = 0.5
    y_offset_mass = (1.0 - bp['mass']) * 0.3
    y_offset_jp = 0.1 if jp == 'J' else 0.0
    
    x = base_x + 1.0 + x_offset_sn + x_offset_tf + blood_offsets[blood]
    y = y_base + y_offset_mass + y_offset_jp
    
    vx_init = MBTI_DIM[ei]['radial_bias'] * 0.2 * gp['Vx_amp']
    vy_init = gp['Vy'] * bp['momentum'] * 0.5
    
    if sn == 'N':
        vx_init += math.cos(N_SPARK_ANGLE) * 0.3
        vy_init += math.sin(N_SPARK_ANGLE) * 0.2
        
    return np.array([x, y]), np.array([vx_init, vy_init])

def compute_forces(pos, vel, mbti, blood, gender, step):
    x, y = pos
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    gp = FEMALE if gender == 'F' else MALE
    bp = BLOOD[blood]
    
    fx, fy = 0.0, gp['Vy'] / bp['mass']
    
    target = (2.0 if gender == 'F' else 14.0) if MBTI_DIM[ei]['target_x'] == 'outer' else (6.0 if gender == 'F' else 10.0)
    fx += (target - x) * 0.08 * MBTI_DIM[ei].get('expansion', 0.3)
    
    for neuro, props in NEURO_ZONES.items():
        if props['x_range'][0] <= x < props['x_range'][1]:
            fx += props['potential'] * gp['zone_sensitivity'][neuro] * 0.15
            break
            
    if tf == 'F':
        dx_c, dy_c = x - 8.0, y - 8.0
        dist = math.sqrt(dx_c**2 + dy_c**2) + 0.001
        ts = MBTI_DIM['F']['torsion'] * bp['curvature']
        fx += -dy_c / dist * ts
        fy += dx_c / dist * ts * 0.5
    else:
        tgt_x = 2.0 if (gender=='F' and ei=='E') else (14.0 if (gender=='M' and ei=='E') else (6.0 if (gender=='F' and ei=='I') else 10.0))
        fx += (tgt_x - x) * 0.05 * MBTI_DIM['T']['straightness']
        
    if sn == 'N' and y > 6:
        grid_y = y / F_3_32
        if abs(grid_y - round(grid_y)) < 0.15 and np.random.random() < MBTI_DIM['N']['spark_prob']:
            fx += math.cos(N_SPARK_ANGLE) * 0.8
            fy += math.sin(N_SPARK_ANGLE) * 0.5
            
    if jp == 'J':
        lattice_x = round(x / F_1_64) * F_1_64
        fx += (lattice_x - x) * MBTI_DIM['J']['damping'] * 0.3
        
    if blood == 'B' and bp['chaos'] > 0:
        np.random.seed((hash(mbti) + step) % 2**31)
        fx += (np.random.random() - 0.5) * bp['chaos'] * 0.5
        fy += (np.random.random() - 0.5) * bp['chaos'] * 0.3
        
    if blood == 'AB':
        fx += math.sin(step * 0.3) * 0.1
        
    fx *= gp['Vx_amp'] * bp['momentum']
    fy *= bp['momentum']
    return fx, fy

def generate_trajectory(mbti, blood, gender):
    pos, vel = get_initial_state(mbti, blood, gender)
    positions = [pos.copy()]
    bp = BLOOD[blood]
    dt = 0.06
    
    for step in range(600):
        fx, fy = compute_forces(pos, vel, mbti, blood, gender, step)
        vel[0] = (vel[0] + fx * dt) * bp['decay']
        vel[1] = (vel[1] + fy * dt) * bp['decay']
        
        speed = np.linalg.norm(vel)
        if speed > 2.0: vel = vel / speed * 2.0
            
        pos += vel * dt
        pos[0] = max(0.2, min(15.8, pos[0]))
        pos[1] = max(0.2, min(15.8, pos[1]))
        positions.append(pos.copy())
        
        if pos[1] >= 15.5: break
            
    return np.array(positions)

def render_grid():
    fig, ax = plt.subplots(figsize=(28, 22), facecolor='#000000')
    ax.set_facecolor('#000000')
    
    for x in [2, 4, 6, 8, 10, 12, 14]:
        ax.axvline(x, color='#333333', linewidth=1.5, linestyle=':', alpha=0.5, zorder=1)
        
    count = 0
    for mbti in ALL_MBTI:
        for blood in BLOOD.keys():
            for gender in GENDERS:
                traj = generate_trajectory(mbti, blood, gender)
                if len(traj) < 2: continue
                
                base_rgb = plt.cm.colors.to_rgb(BLOOD[blood]['color'])
                tint = FEMALE['color_tint'] if gender == 'F' else MALE['color_tint']
                color = (base_rgb[0]*0.5 + tint[0]*0.5, base_rgb[1]*0.5 + tint[1]*0.5, base_rgb[2]*0.5 + tint[2]*0.5)
                
                lw = 1.5 if mbti[3] == 'J' else 0.8
                alpha = 0.4 + (BLOOD[blood]['mass'] - 0.5) * 0.2
                
                ax.plot(traj[:, 0], traj[:, 1], color=color, linewidth=lw, alpha=alpha, solid_capstyle='round', zorder=10)
                count += 1
                
    labels = ['EJ WOMEN', 'EP WOMEN', 'IJ WOMEN', 'IP WOMEN', 'IP MEN', 'IJ MEN', 'EP MEN', 'EJ MEN']
    for i, label in enumerate(labels):
        ax.text(i * 2 + 1, -0.7, label, ha='center', va='top', fontsize=14, fontweight='bold', color='#AAAAAA', zorder=20)
        
    title = ax.set_title(f'NEW 128-TYPE PURE TRAJECTORY GRID (N={count})', fontsize=28, fontweight='bold', color='white', pad=30)
    
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(16.5, -2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    output = "NEW_128_TRAJECTORY_GRID_FINAL.png"
    plt.savefig(output, dpi=300, facecolor='#000000', bbox_inches='tight', pad_inches=0.3)
    print(f"--- SUCCESS: Rendered {count} trajectories to {output} ---")

if __name__ == "__main__":
    render_grid()