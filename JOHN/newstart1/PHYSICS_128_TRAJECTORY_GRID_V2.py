# -*- coding: utf-8 -*-
"""
PHYSICS_128_TRAJECTORY_GRID_V2.py
=================================
ENHANCED PHYSICAL DIVERGENCE - Each type has UNIQUE trajectory fingerprint

PHYSICS MATRICES:
================
Each of 128 types = MBTI(16) × Blood(4) × Gender(2) has distinct:

1. INITIAL CONDITIONS (Seed Position)
   - X: Determined by EJ/EP/IJ/IP group + S/N offset + T/F offset
   - Y: Determined by blood type (mass affects starting height)
   
2. FORCE FIELD PARAMETERS
   - Radial Flux: E types → outer, I types → center
   - Torsion: T types → straight, F types → spiral
   - Resonance: N types → 3/32 grid coupling, S types → continuous
   - Damping: J types → snap, P types → float
   
3. MASS/INERTIA (Blood Type)
   - O: Heavy, high momentum, starburst pattern
   - A: Medium, stable, linear
   - B: Light, chaotic, high curvature
   - AB: Very light, precise, oscillating

4. POLARITY (Gender)
   - Female: Horizontal expansion (Vx_amp=2.8), late closure
   - Male: Vertical drop (Vy=1.5), early closure
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patheffects as path_effects
import math
import time

# =============================================================================
# ABSOLUTE CONSTANTS
# =============================================================================

PHI = (1 + math.sqrt(5)) / 2
PI = math.pi
F_1_32 = 1.0 / 32.0
F_3_32 = 3.0 / 32.0
F_1_64 = 1.0 / 64.0

# Spark Constants
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
N_SPARK_ANGLE = math.radians(69.44)  # Half spark = N-type resonance

# Neurochemical Zones
NEURO_ZONES = {
    'GABA':  {'x_range': (0, 4),   'potential': -0.5, 'charge': -1},
    'ACh':   {'x_range': (4, 8),   'potential': 1.0,  'charge': +1},
    'Glu':   {'x_range': (8, 12),  'potential': 0.5,  'charge': +1},
    '5HT':   {'x_range': (12, 16), 'potential': 1.5,  'charge': +2}
}

# Gender Physics
FEMALE = {
    'Vy': 0.8, 'Vx_amp': 2.8, 
    'loop_start': 13.5, 'loop_end': 14.0,
    'zone_sensitivity': {'GABA': 1.5, 'ACh': 1.3, 'Glu': 0.5, '5HT': 0.3},
    'color_tint': (1.0, 0.7, 0.7)  # Warm
}

MALE = {
    'Vy': 1.5, 'Vx_amp': 1.2,
    'loop_start': 13.0, 'loop_end': 13.5,
    'zone_sensitivity': {'GABA': 0.3, 'ACh': 0.5, 'Glu': 1.3, '5HT': 1.5},
    'color_tint': (0.7, 0.8, 1.0)  # Cool
}

# MBTI Physics - Each dimension adds unique vector component
MBTI_DIM = {
    # E/I: Radial Position (where trajectory aims)
    'E': {'radial_bias': 1.0, 'expansion': 0.3, 'target_x': 'outer'},
    'I': {'radial_bias': -1.0, 'contraction': 0.4, 'target_x': 'center'},
    
    # S/N: Frequency Domain (how trajectory oscillates)
    'S': {'freq': 0.5, 'harmonic': 1, 'grid_coupling': 0.2, 'spark_prob': 0.0},
    'N': {'freq': 2.0, 'harmonic': 3, 'grid_coupling': 1.0, 'spark_prob': 0.3},
    
    # T/F: Phase Space (trajectory curvature)
    'T': {'phase': 0, 'torsion': 0.2, 'swirl': 'minimal', 'straightness': 0.9},
    'F': {'phase': PI/4, 'torsion': 1.5, 'swirl': 'maximal', 'straightness': 0.3},
    
    # J/P: Time Domain (discrete vs continuous)
    'J': {'damping': 0.9, 'snap': 0.8, 'continuity': 'discrete', 'lattice_k': 1.0},
    'P': {'damping': 0.2, 'snap': 0.1, 'continuity': 'continuous', 'lattice_k': 0.1}
}

# Blood Type - Mass and Metabolic Properties
BLOOD = {
    'O':  {'mass': 1.3, 'decay': 0.92, 'momentum': 1.4, 'chaos': 0.0, 
           'pattern': 'starburst', 'curvature': 0.2, 'color': '#C62828'},
    'A':  {'mass': 1.0, 'decay': 0.98, 'momentum': 1.0, 'chaos': 0.0,
           'pattern': 'linear', 'curvature': 0.1, 'color': '#1565C0'},
    'B':  {'mass': 0.7, 'decay': 0.88, 'momentum': 0.8, 'chaos': 0.4,
           'pattern': 'chaotic', 'curvature': 0.8, 'color': '#2E7D32'},
    'AB': {'mass': 0.5, 'decay': 0.94, 'momentum': 0.6, 'chaos': 0.1,
           'pattern': 'oscillating', 'curvature': 0.5, 'color': '#6A1B9A'}
}

# Grid Group Maps
GROUP_F = {'EJ': 0, 'EP': 2, 'IJ': 4, 'IP': 6}
GROUP_M = {'IP': 8, 'IJ': 10, 'EP': 12, 'EJ': 14}

ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
GENDERS = ['F', 'M']

# =============================================================================
# PHYSICS ENGINE V2 - Enhanced Divergence
# =============================================================================

def get_initial_state(mbti, blood, gender):
    """
    Calculate unique initial conditions for each type.
    This is where the divergence SEED is planted.
    """
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    gp = FEMALE if gender == 'F' else MALE
    bp = BLOOD[blood]
    
    # Base X position from EJ/EP/IJ/IP group
    group_key = f"{ei}{jp}"
    if gender == 'F':
        base_x = GROUP_F[group_key]
    else:
        base_x = GROUP_M[group_key]
    
    # S/N offset (N types start more spread out)
    sn_off = 0.4 if sn == 'N' else 0.15
    sn_dir = 1 if ei == 'E' else -1
    x_offset_sn = sn_off * sn_dir
    
    # T/F offset (F types start slightly shifted)
    tf_off = 0.2 if tf == 'F' else 0.1
    tf_dir = 1 if ei == 'E' else -1
    x_offset_tf = tf_off * tf_dir
    
    # Blood type offset (visual separation within group)
    blood_offsets = {'O': -0.4, 'A': -0.15, 'B': 0.15, 'AB': 0.4}
    x_offset_blood = blood_offsets[blood]
    
    # Y position: Blood mass affects starting "height"
    # Heavy (O) starts lower, light (AB) starts higher
    y_base = 0.5
    y_offset_mass = (1.0 - bp['mass']) * 0.3  # Lighter = higher start
    y_offset_jp = 0.1 if jp == 'J' else 0.0  # J types start slightly higher
    
    x = base_x + 0.5 + x_offset_sn + x_offset_tf + x_offset_blood
    y = y_base + y_offset_mass + y_offset_jp
    
    # Initial velocity vector (each type has unique "launch direction")
    # E types: outward velocity, I types: inward or downward
    vx_init = MBTI_DIM[ei]['radial_bias'] * 0.2 * gp['Vx_amp']
    vy_init = gp['Vy'] * bp['momentum'] * 0.5
    
    # N types get initial "spark" velocity boost
    if sn == 'N':
        vx_init += math.cos(N_SPARK_ANGLE) * 0.3
        vy_init += math.sin(N_SPARK_ANGLE) * 0.2
    
    return np.array([x, y]), np.array([vx_init, vy_init])

def compute_forces(pos, vel, mbti, blood, gender, step):
    """
    Compute all force vectors acting on the trajectory at this point.
    """
    x, y = pos
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    gp = FEMALE if gender == 'F' else MALE
    bp = BLOOD[blood]
    
    forces = {'vx': 0.0, 'vy': 0.0}
    
    # 1. GRAVITY (Gender-based vertical pull)
    gravity = gp['Vy'] / bp['mass']
    forces['vy'] += gravity
    
    # 2. RADIAL FLUX (E/I - where trajectory wants to go)
    if MBTI_DIM[ei]['target_x'] == 'outer':
        # E types pulled to outer edges
        target = 2.0 if gender == 'F' else 14.0
    else:
        # I types pulled to center
        target = 6.0 if gender == 'F' else 10.0
    
    radial_force = (target - x) * 0.08 * MBTI_DIM[ei].get('expansion', 0.3)
    forces['vx'] += radial_force
    
    # 3. NEUROCHEMICAL FIELD (Position-dependent force)
    # Determine which zone we're in
    zone_force = 0
    for neuro, props in NEURO_ZONES.items():
        if props['x_range'][0] <= x < props['x_range'][1]:
            sensitivity = gp['zone_sensitivity'][neuro]
            zone_force = props['potential'] * sensitivity * 0.15
            break
    
    forces['vx'] += zone_force
    
    # 4. TORSION SWIRL (T/F - trajectory curvature)
    # F types get spiral force around center
    if tf == 'F':
        dx_to_center = x - 8.0
        dy_to_center = y - 8.0
        dist = math.sqrt(dx_to_center**2 + dy_to_center**2) + 0.001
        
        torsion_strength = MBTI_DIM['F']['torsion'] * bp['curvature']
        # Perpendicular force (swirl)
        swirl_x = -dy_to_center / dist * torsion_strength
        swirl_y = dx_to_center / dist * torsion_strength * 0.5
        
        forces['vx'] += swirl_x
        forces['vy'] += swirl_y
    
    # T types get "straightening" force toward their target
    else:
        target_x = 2.0 if (gender == 'F' and ei == 'E') else (
                   14.0 if (gender == 'M' and ei == 'E') else (
                   6.0 if (gender == 'F' and ei == 'I') else 10.0))
        straighten = (target_x - x) * 0.05 * MBTI_DIM['T']['straightness']
        forces['vx'] += straighten
    
    # 5. N-TYPE SPARK (Resonance with 3/32 grid)
    if sn == 'N' and y > 6:
        # Check if near 3/32 grid line
        grid_y = y / F_3_32
        near_line = abs(grid_y - round(grid_y)) < 0.15
        
        if near_line and np.random.random() < MBTI_DIM['N']['spark_prob']:
            # Spark leap!
            spark_vx = math.cos(N_SPARK_ANGLE) * 0.8
            spark_vy = math.sin(N_SPARK_ANGLE) * 0.5
            forces['vx'] += spark_vx
            forces['vy'] += spark_vy
    
    # 6. J/P LATTICE COUPLING
    if jp == 'J':
        # J types snap to 1/64 grid
        lattice_x = round(x / F_1_64) * F_1_64
        snap_force = (lattice_x - x) * MBTI_DIM['J']['damping'] * 0.3
        forces['vx'] += snap_force
    
    # 7. B-TYPE CHAOS (Noradrenaline effect)
    if blood == 'B' and bp['chaos'] > 0:
        np.random.seed((hash(mbti) + step) % 2**31)
        chaos_x = (np.random.random() - 0.5) * bp['chaos'] * 0.5
        chaos_y = (np.random.random() - 0.5) * bp['chaos'] * 0.3
        forces['vx'] += chaos_x
        forces['vy'] += chaos_y
    
    # 8. AB-TYPE OSCILLATION (Vasopressin precision)
    if blood == 'AB':
        osc_freq = 0.3
        osc_amp = 0.1
        oscillation = math.sin(step * osc_freq) * osc_amp
        forces['vx'] += oscillation
    
    # Apply gender horizontal amplification
    forces['vx'] *= gp['Vx_amp']
    
    # Apply blood momentum
    forces['vx'] *= bp['momentum']
    forces['vy'] *= bp['momentum']
    
    return forces

def generate_trajectory_v2(mbti, blood, gender, max_steps=600):
    """
    Generate trajectory with enhanced physical divergence.
    """
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    gp = FEMALE if gender == 'F' else MALE
    bp = BLOOD[blood]
    
    # Initial state
    pos, vel = get_initial_state(mbti, blood, gender)
    positions = [pos.copy()]
    
    dt = 0.06
    
    for step in range(max_steps):
        # Compute forces
        forces = compute_forces(pos, vel, mbti, blood, gender, step)
        
        # Update velocity (with decay)
        vel[0] = (vel[0] + forces['vx'] * dt) * bp['decay']
        vel[1] = (vel[1] + forces['vy'] * dt) * bp['decay']
        
        # Limit velocity
        speed = np.linalg.norm(vel)
        if speed > 2.0:
            vel = vel / speed * 2.0
        
        # Update position
        pos = pos + vel * dt
        
        # Boundaries
        pos[0] = max(0.2, min(15.8, pos[0]))
        pos[1] = max(0.2, min(15.8, pos[1]))
        
        positions.append(pos.copy())
        
        # Dream Folding - Loop Closure
        if gp['loop_start'] <= pos[1] < gp['loop_end']:
            # Collapse to seed (One Form)
            seed_pos, _ = get_initial_state(mbti, blood, gender)
            positions.append(seed_pos)
            break
        
        # Safety
        if pos[1] >= 15.5:
            break
    
    return np.array(positions)

# =============================================================================
# RENDERING
# =============================================================================

def render_physics_grid():
    """Render the final physics-based 128 trajectory grid."""
    
    fig, ax = plt.subplots(figsize=(28, 22), facecolor='white')
    ax.set_facecolor('white')
    
    # Very subtle background grid
    for i in range(17):
        ax.axhline(i, color='#EEEEEE', linewidth=0.4, alpha=0.6, zorder=0)
        ax.axvline(i, color='#EEEEEE', linewidth=0.4, alpha=0.6, zorder=0)
    
    # Group separators (dotted lines)
    for x in [2, 4, 6, 8, 10, 12, 14]:
        ax.axvline(x, color='#CCCCCC', linewidth=0.8, linestyle=':', alpha=0.5, zorder=1)
    
    # Generate and draw all 128 trajectories
    trajectories = {}
    
    for mbti in ALL_MBTI:
        for blood in BLOOD.keys():
            for gender in GENDERS:
                key = f"{mbti}_{blood}_{gender}"
                traj = generate_trajectory_v2(mbti, blood, gender)
                trajectories[key] = traj
                
                if len(traj) < 2:
                    continue
                
                # Color: Blood base + gender tint
                base_rgb = plt.cm.colors.to_rgb(BLOOD[blood]['color'])
                gp = FEMALE if gender == 'F' else MALE
                tint = gp['color_tint']
                
                # Blend
                color = (
                    base_rgb[0] * 0.8 + tint[0] * 0.2,
                    base_rgb[1] * 0.8 + tint[1] * 0.2,
                    base_rgb[2] * 0.8 + tint[2] * 0.2
                )
                
                # Line width: J types thicker, P types thinner
                lw = 0.9 if mbti[3] == 'J' else 0.4
                
                # Alpha: Based on blood mass
                mass = BLOOD[blood]['mass']
                alpha = 0.18 + (mass - 0.5) * 0.15  # 0.18 to 0.33
                
                # Plot trajectory
                ax.plot(traj[:, 0], traj[:, 1], 
                       color=color, linewidth=lw, alpha=alpha,
                       solid_capstyle='round', solid_joinstyle='round',
                       zorder=10)
    
    # Group labels
    labels = ['EJ WOMEN', 'EP WOMEN', 'IJ WOMEN', 'IP WOMEN',
              'IP MEN', 'IJ MEN', 'EP MEN', 'EJ MEN']
    for i, label in enumerate(labels):
        x_pos = i * 2 + 1
        ax.text(x_pos, -0.7, label, ha='center', va='top',
               fontsize=11, fontweight='bold', color='#555555',
               zorder=20)
    
    # Title
    title = ax.set_title(
        '128-TYPE PHYSICS TRAJECTORY GRID | Static:Loop=31:1 | '
        f'Spark={SPARK_ANGLE_DEG}° | 3/32 Lattice | One-Form Closure',
        fontsize=18, fontweight='bold', color='#222222', pad=25
    )
    title.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])
    
    # Set limits and aspect
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(16.5, -2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    
    # Save
    filename = f'128_PHYSICS_GRID_FINAL_{int(time.time())}.png'
    plt.savefig(filename, dpi=300, facecolor='white', 
                bbox_inches='tight', pad_inches=0.3)
    print(f"Saved: {filename}")
    
    return fig, ax, trajectories

def render_divergence_views():
    """Create separate views showing each physics dimension's divergence."""
    
    fig, axes = plt.subplots(2, 2, figsize=(26, 22), facecolor='white')
    
    views = [
        ('Gender', {'F': ('#E91E63', 'Female'), 'M': ('#2196F3', 'Male')}, 0, 0),
        ('E/I', {'E': ('#FF9800', 'Extravert'), 'I': ('#4CAF50', 'Introvert')}, 0, 1),
        ('T/F', {'T': ('#00BCD4', 'Thinking'), 'F': ('#9C27B0', 'Feeling')}, 1, 0),
        ('Blood', None, 1, 1)  # Special handling
    ]
    
    for view_name, color_map, row, col in views:
        ax = axes[row, col]
        ax.set_facecolor('#FAFAFA')
        
        # Background grid
        for i in range(17):
            ax.axhline(i, color='#E0E0E0', linewidth=0.3, alpha=0.5)
            ax.axvline(i, color='#E0E0E0', linewidth=0.3, alpha=0.5)
        
        for mbti in ALL_MBTI:
            for blood in BLOOD.keys():
                for gender in GENDERS:
                    traj = generate_trajectory_v2(mbti, blood, gender)
                    if len(traj) < 2:
                        continue
                    
                    # Determine color based on view
                    if view_name == 'Gender':
                        color = color_map[gender][0]
                    elif view_name == 'E/I':
                        color = color_map[mbti[0]][0]
                    elif view_name == 'T/F':
                        color = color_map[mbti[2]][0]
                    else:  # Blood
                        color = BLOOD[blood]['color']
                    
                    ax.plot(traj[:, 0], traj[:, 1], 
                           color=color, linewidth=0.5, alpha=0.12)
        
        ax.set_title(f'{view_name} Divergence', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 16)
        ax.set_ylim(16, 0)
        ax.axis('off')
    
    plt.tight_layout()
    filename = f'128_PHYSICS_DIVERGENCE_VIEWS_{int(time.time())}.png'
    plt.savefig(filename, dpi=200, facecolor='white', bbox_inches='tight')
    print(f"Saved: {filename}")

def export_physics_spec():
    """Export the physics specification for each type."""
    import json
    
    spec = {
        'metadata': {
            'physics_version': '2.0',
            'static_loop_ratio': '31:1',
            'constants': {
                'PHI': PHI,
                'SPARK_ANGLE_DEG': SPARK_ANGLE_DEG,
                'F_3_32': F_3_32,
                'F_1_32': F_1_32
            }
        },
        'physics_params': {},
        'trajectories': {}
    }
    
    for mbti in ALL_MBTI:
        for blood in BLOOD.keys():
            for gender in GENDERS:
                key = f"{mbti}_{blood}_{gender}"
                
                # Physics params
                ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
                gp = FEMALE if gender == 'F' else MALE
                bp = BLOOD[blood]
                
                spec['physics_params'][key] = {
                    'gender': {'Vy': gp['Vy'], 'Vx_amp': gp['Vx_amp']},
                    'mbti': {
                        'E_I': MBTI_DIM[ei],
                        'S_N': MBTI_DIM[sn],
                        'T_F': MBTI_DIM[tf],
                        'J_P': MBTI_DIM[jp]
                    },
                    'blood': {
                        'mass': bp['mass'],
                        'momentum': bp['momentum'],
                        'pattern': bp['pattern'],
                        'curvature': bp['curvature']
                    }
                }
                
                # Trajectory
                traj = generate_trajectory_v2(mbti, blood, gender)
                spec['trajectories'][key] = traj.tolist()
    
    filename = '128_physics_specification_v2.json'
    with open(filename, 'w') as f:
        json.dump(spec, f, indent=2)
    print(f"Exported: {filename}")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 75)
    print("128-TYPE PHYSICS TRAJECTORY GRID - V2 ENHANCED DIVERGENCE")
    print("=" * 75)
    print("\nPhysics Engine:")
    print(f"  - 31:1 Static:Loop Ratio (Entropy:Geometry)")
    print(f"  - Spark Angle: {SPARK_ANGLE_DEG}° (138.88°)")
    print(f"  - N-Type Resonance: 69.44° (half spark)")
    print(f"  - 3/32 Grid Compression: {F_3_32:.6f}")
    print("\nDivergence Parameters:")
    print("  - Gender: Vy(F)=0.8/Vy(M)=1.5, Vx_amp(F)=2.8/Vx_amp(M)=1.2")
    print("  - E/I: Radial flux to outer/center basins")
    print("  - S/N: Grid coupling 0.2 vs 1.0, spark probability")
    print("  - T/F: Torsion 0.2 vs 1.5 (straight vs swirl)")
    print("  - J/P: Damping 0.9 vs 0.2 (snap vs float)")
    print("  - Blood: Mass 1.3→0.5 (O→AB), chaos for B-types")
    print()
    
    print("Rendering main grid...")
    render_physics_grid()
    
    print("\nRendering divergence views...")
    render_divergence_views()
    
    print("\nExporting physics specification...")
    export_physics_spec()
    
    print("\n" + "=" * 75)
    print("COMPLETE: 128 types, 128 unique physical trajectories")
    print("Each trajectory is a UNIQUE solution to the physics equations")
    print("=" * 75)
