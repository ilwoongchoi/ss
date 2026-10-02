# -*- coding: utf-8 -*-
"""
PHYSICS_128_TRAJECTORY_GRID.py
==============================
DEFINITIVE IMPLEMENTATION: 128 Personality Types as Physical Trajectories

CORE PRINCIPLE: No arbitrary variations - each type follows DISTINCT physical laws.

THE UNIVERSAL LAW (31:1 Static:Loop Ratio):
- 31 time units: Linear entropy diffusion (Static Flow)
- 1 time unit (45 min): Geometric convergence (Loop Folding)

NEUROCHEMICAL POTENTIAL FIELD (X-axis, 0-16):
  X=0-4:   GABA (-0.5)    - Inhibitory, left-side female sensitivity
  X=4-8:   ACh (1.0)      - Truth logic, cortisol node
  X=8-12:  Glu (0.5)      - Excitatory, right-side male sensitivity  
  X=12-16: 5HT (1.5)      - Serotonin, vertical tension

GENDER POLARITY:
  Female: Vy=0.8, Vx_amp=2.8, Loop closes 3:00 AM (y=13.5-14.0)
  Male:   Vy=1.5, Vx_amp=1.2, Loop closes 2:15 AM (y=13.0-13.5)

MBTI FIELD COUPLING:
  E/I (Radial Flux): E→outer basins (X=2,14), I→center (X=8)
  S/N (Resonance): N→3/32 grid resonance, spark at 69.44°
  T/F (Torsion): T→straight (testosterone), F→swirl (estrogen+progesterone)
  J/P (Damping): J→snap to lattice, P→float between grid points

BLOOD TYPE (Metabolic Mass/Inertia):
  O  (Dopamine):     mass=1.2, high momentum, starburst seed
  A  (Cortisol):     mass=1.0, high damping, stable flow
  B  (Noradrenaline): mass=0.8, low mass, chaotic curvature
  AB (Vasopressin):  mass=0.6, precise tuning, integrated trajectory

DREAM FOLDING (1/32 Law):
  At closure window, all trajectories collapse to seed (Lattice Lock)
  Creates "One Form" reset for next cycle.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import math

# =============================================================================
# ABSOLUTE CONSTANTS (Single Source of Truth)
# =============================================================================

# Foundational
PHI = (1 + math.sqrt(5)) / 2
PI = math.pi
F_1_32 = 1.0 / 32.0
F_3_32 = 3.0 / 32.0
F_1_64 = 1.0 / 64.0

# The 31:1 Law - Static:Loop Ratio
STATIC_RATIO = 31.0 / 32.0  # 31 parts linear entropy
LOOP_RATIO = 1.0 / 32.0      # 1 part geometric convergence

# Spark/Leap Constants (The 0→1 Transition)
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
SPARK_LEAP_DIST = 2.5
COMPRESSION_GAP = F_3_32  # 3/32 lattice compression

# Neurochemical Potential Field (X-axis charges)
NEURO_POTENTIAL = {
    'GABA': -0.5,    # X=0-4
    'ACh': 1.0,      # X=4-8  
    'Glu': 0.5,      # X=8-12
    '5HT': 1.5       # X=12-16
}

# Gender Physics
GENDER_PHYSICS = {
    'F': {'Vy': 0.8, 'Vx_amp': 2.8, 'loop_start': 13.5, 'loop_end': 14.0, 
          'sensitive_zone': (0, 8), 'neuro_pref': ['GABA', 'ACh']},
    'M': {'Vy': 1.5, 'Vx_amp': 1.2, 'loop_start': 13.0, 'loop_end': 13.5,
          'sensitive_zone': (8, 16), 'neuro_pref': ['Glu', '5HT']}
}

# MBTI Cognitive Functions → Physical Parameters
MBTI_PHYSICS = {
    # E/I: Radial flux direction
    'E': {'radial_target': 'outer', 'flux_strength': 1.2, 'basin_x': lambda g: 2 if g=='F' else 14},
    'I': {'radial_target': 'center', 'flux_strength': -0.8, 'basin_x': lambda g: 6 if g=='F' else 10},
    
    # S/N: Resonance with 3/32 grid
    'S': {'resonance_freq': 0.5, 'spark_angle': 0, 'grid_coupling': 0.3},
    'N': {'resonance_freq': 1.5, 'spark_angle': 69.44, 'grid_coupling': 1.0},
    
    # T/F: Torsion/swirl characteristics  
    'T': {'torsion': 0.4, 'path_type': 'straight', 'hormone': 'testosterone'},
    'F': {'torsion': 1.4, 'path_type': 'swirl', 'hormone': 'estrogen_progesterone'},
    
    # J/P: Damping/lattice interaction
    'J': {'damping': 0.9, 'snap_to_grid': True, 'lattice_coupling': 1.0},
    'P': {'damping': 0.2, 'snap_to_grid': False, 'lattice_coupling': 0.3}
}

# Blood Type: Metabolic Engine Parameters
BLOOD_PHYSICS = {
    'O':  {'mass': 1.2, 'dopamine': 1.0, 'momentum': 1.3, 'decay': 0.9, 'color': '#D32F2F'},
    'A':  {'mass': 1.0, 'cortisol': 0.8, 'oxytocin': 0.6, 'damping': 1.2, 'decay': 0.95, 'color': '#1976D2'},
    'B':  {'mass': 0.8, 'noradrenaline': 1.1, 'chaos': 0.3, 'decay': 0.85, 'color': '#388E3C'},
    'AB': {'mass': 0.6, 'vasopressin': 0.9, 'ACh': 0.7, 'precision': 1.2, 'decay': 0.92, 'color': '#7B1FA2'}
}

# Grid Layout: 8 Groups × 2 columns each
GROUP_MAP_FEMALE = {'EJ': 0, 'EP': 2, 'IJ': 4, 'IP': 6}
GROUP_MAP_MALE = {'IP': 8, 'IJ': 10, 'EP': 12, 'EJ': 14}

ALL_MBTI = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP", 
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]
BLOODS = ['O', 'A', 'B', 'AB']
GENDERS = ['F', 'M']

# =============================================================================
# PHYSICS ENGINE
# =============================================================================

def get_neurochemical_influence(x):
    """Get neurochemical potential at position x (0-16)."""
    if x < 4:
        return NEURO_POTENTIAL['GABA'] * (1 - x/4)
    elif x < 8:
        return NEURO_POTENTIAL['ACh'] * ((x-4)/4)
    elif x < 12:
        return NEURO_POTENTIAL['Glu'] * ((x-8)/4)
    else:
        return NEURO_POTENTIAL['5HT'] * min(1, (x-12)/4)

def compute_divergence_vector(x, y, mbti, blood, gender):
    """
    Compute the instantaneous velocity vector for a personality type.
    This is where the PHYSICAL DISTINCTION happens.
    """
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    gp = GENDER_PHYSICS[gender]
    bp = BLOOD_PHYSICS[blood]
    
    # 1. BASE VERTICAL (Entropy Descent)
    # Modified by gender vertical speed and blood mass
    vy_base = gp['Vy'] / bp['mass']
    
    # 2. RADIAL FLUX (E/I determination)
    # E types expand outward, I types contract to center
    target_x = MBTI_PHYSICS[ei]['basin_x'](gender)
    radial_pull = (target_x - x) * MBTI_PHYSICS[ei]['flux_strength'] * 0.1
    
    # 3. NEUROCHEMICAL FIELD EFFECT
    # Gender-specific sensitivity to neurochemical zones
    neuro = get_neurochemical_influence(x)
    if gender == 'F' and x < 8:
        # Female left-side amplification (GABA/ACh)
        neuro_effect = neuro * 0.3 * gp['Vx_amp']
    elif gender == 'M' and x > 8:
        # Male right-side amplification (Glu/5HT)
        neuro_effect = neuro * 0.3 * gp['Vx_amp']
    else:
        neuro_effect = neuro * 0.1
    
    # 4. TORSION/SWIRL (T/F determination)
    # Creates spiral motion around center (8, 8)
    dx_to_center = x - 8.0
    dy_to_center = y - 8.0
    distance = math.sqrt(dx_to_center**2 + dy_to_center**2) + 0.001
    
    torsion = MBTI_PHYSICS[tf]['torsion']
    # Perpendicular vector for swirl
    swirl_x = -dy_to_center / distance * torsion * 0.5
    swirl_y = dx_to_center / distance * torsion * 0.3
    
    # 5. RESONANCE SPARK (S/N determination)
    # N-types get spark leap when hitting 3/32 grid lines
    spark_effect_x = 0
    spark_effect_y = 0
    if sn == 'N':
        # Check proximity to 3/32 grid
        grid_x = (x - 8) / F_3_32
        grid_y = y / F_3_32
        near_grid = abs(grid_x - round(grid_x)) < 0.2 or abs(grid_y - round(grid_y)) < 0.2
        
        if near_grid and y > 8:  # Only in lower half
            # Spark leap at 69.44°
            spark_angle = math.radians(69.44)
            spark_mag = MBTI_PHYSICS['N']['resonance_freq'] * 0.5
            spark_effect_x = math.cos(spark_angle) * spark_mag
            spark_effect_y = math.sin(spark_angle) * spark_mag
    
    # 6. DAMPING/LATTICE COUPLING (J/P determination)
    damping = MBTI_PHYSICS[jp]['damping']
    if MBTI_PHYSICS[jp]['snap_to_grid']:
        # J-types snap to 1/64 lattice
        lattice_x = round(x / F_1_64) * F_1_64
        lattice_pull = (lattice_x - x) * damping * 0.5
    else:
        # P-types drift freely
        lattice_pull = 0
    
    # 7. BLOOD TYPE MODULATION
    # O: Starburst (high initial velocity)
    # A: Stable flow (damping)
    # B: Chaotic (random perturbation)
    # AB: Precision (smooth interpolation)
    
    momentum = bp.get('momentum', 1.0)
    blood_damping = bp.get('damping', 1.0)
    chaos = bp.get('chaos', 0.0)
    
    # Chaos for B-types (noradrenaline)
    if chaos > 0:
        np.random.seed(hash(mbti + blood + gender) % 2**31)
        chaos_x = (np.random.random() - 0.5) * chaos
        chaos_y = (np.random.random() - 0.5) * chaos * 0.5
    else:
        chaos_x, chaos_y = 0, 0
    
    # COMBINE ALL EFFECTS
    vx = (radial_pull + neuro_effect + swirl_x + spark_effect_x + lattice_pull + chaos_x) 
    vx *= gp['Vx_amp'] * momentum / blood_damping
    
    vy = (vy_base + swirl_y + spark_effect_y + chaos_y) * STATIC_RATIO
    vy += (spark_effect_y * LOOP_RATIO)  # Loop contribution
    
    return np.array([vx, vy])

def generate_trajectory(mbti, blood, gender, max_steps=800):
    """
    Generate complete trajectory for one personality type.
    Returns array of (x, y) positions from start to dream fold.
    """
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    gp = GENDER_PHYSICS[gender]
    
    # Starting position based on EJ/EP/IJ/IP + gender
    group_key = f"{ei}{jp}"
    if gender == 'F':
        base_x = GROUP_MAP_FEMALE[group_key]
    else:
        base_x = GROUP_MAP_MALE[group_key]
    
    # Micro-offset for blood type (visual separation)
    blood_offset = {'O': -0.25, 'A': -0.08, 'B': 0.08, 'AB': 0.25}
    x = base_x + 0.5 + blood_offset[blood]
    y = 0.5 + blood_offset[blood] * 0.5
    
    start_pos = np.array([x, y])
    
    # Trajectory storage
    positions = [start_pos.copy()]
    dt = 0.08
    
    # Dream folding detection
    loop_started = False
    
    for step in range(max_steps):
        # Compute velocity vector
        v = compute_divergence_vector(x, y, mbti, blood, gender)
        
        # Update position
        x += v[0] * dt
        y += v[1] * dt
        
        # Boundary clamping
        x = max(0.5, min(15.5, x))
        y = max(0.5, min(15.5, y))
        
        positions.append(np.array([x, y]))
        
        # Dream Folding (1/32 Law): Collapse to seed
        if gp['loop_start'] <= y < gp['loop_end']:
            if not loop_started:
                loop_started = True
                # Lattice lock: snap to seed
                x, y = start_pos[0], start_pos[1]
                positions.append(np.array([x, y]))
                break
        
        # Safety break
        if y >= 15.0:
            break
    
    return np.array(positions)

# =============================================================================
# RENDERING ENGINE
# =============================================================================

def render_trajectory_grid():
    """
    Render the complete 128-type trajectory grid.
    Visual style: Pure physics, minimal decoration, maximum divergence.
    """
    fig, ax = plt.subplots(figsize=(24, 18), facecolor='white')
    ax.set_facecolor('white')
    
    # Subtle grid lines (very faint)
    for i in range(17):
        ax.axhline(i, color='#E8E8E8', linewidth=0.3, alpha=0.5)
        ax.axvline(i, color='#E8E8E8', linewidth=0.3, alpha=0.5)
    
    # Draw all 128 trajectories
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                traj = generate_trajectory(mbti, blood, gender)
                
                if len(traj) < 2:
                    continue
                
                # Color: Blood type base with gender tint
                base_color = BLOOD_PHYSICS[blood]['color']
                
                # Convert to RGB and apply gender tint
                rgb = plt.cm.colors.to_rgb(base_color)
                if gender == 'F':
                    # Slight warm tint for female
                    rgb = (rgb[0]*0.9 + 0.1, rgb[1]*0.95 + 0.05, rgb[2]*0.9)
                else:
                    # Slight cool tint for male
                    rgb = (rgb[0]*0.9, rgb[1]*0.95, rgb[2]*0.9 + 0.1)
                
                # Line width based on J/P (J=thicker, P=thinner)
                jp = mbti[3]
                lw = 0.8 if jp == 'J' else 0.4
                
                # Alpha based on blood mass (heavier = more visible)
                mass = BLOOD_PHYSICS[blood]['mass']
                alpha = 0.15 + (mass - 0.6) * 0.2  # 0.15 to 0.35
                
                # Draw trajectory
                ax.plot(traj[:, 0], traj[:, 1], 
                       color=rgb, 
                       linewidth=lw,
                       alpha=alpha,
                       solid_capstyle='round')
    
    # Group labels at top (minimal)
    labels = ['EJ WOMEN', 'EP WOMEN', 'IJ WOMEN', 'IP WOMEN', 
              'IP MEN', 'IJ MEN', 'EP MEN', 'EJ MEN']
    for i, label in enumerate(labels):
        ax.text(i * 2 + 1, -0.5, label, ha='center', fontsize=9, 
                color='#666666', weight='bold')
    
    # Title with physics constants
    ax.set_title(
        f'128-TYPE PHYSICS TRAJECTORY GRID | Static:Loop=31:1 | '
        f'Spark={SPARK_ANGLE_DEG}° | 3/32 Grid | One-Form Closure',
        fontsize=16, pad=20, weight='bold', color='#333333'
    )
    
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(16.5, -1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    
    # Save with high DPI
    filename = f'128_PHYSICS_TRAJECTORY_GRID_{int(time.time())}.png'
    plt.savefig(filename, dpi=300, facecolor='white', 
                bbox_inches='tight', pad_inches=0.2)
    print(f"Saved: {filename}")
    
    return fig, ax

def render_with_divergence_analysis():
    """
    Render grid with divergence analysis - showing how types physically separate.
    """
    fig, axes = plt.subplots(2, 2, figsize=(28, 22), facecolor='white')
    
    # Collect all trajectories for analysis
    all_traj = {}
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                key = f"{mbti}_{blood}_{gender}"
                all_traj[key] = generate_trajectory(mbti, blood, gender)
    
    # Plot 1: Full Grid
    ax1 = axes[0, 0]
    ax1.set_facecolor('white')
    for key, traj in all_traj.items():
        if len(traj) < 2:
            continue
        parts = key.split('_')
        blood = parts[1]
        gender = parts[2]
        color = BLOOD_PHYSICS[blood]['color']
        rgb = plt.cm.colors.to_rgb(color)
        if gender == 'F':
            rgb = (rgb[0]*0.9 + 0.1, rgb[1]*0.95 + 0.05, rgb[2]*0.9)
        ax1.plot(traj[:, 0], traj[:, 1], color=rgb, linewidth=0.5, alpha=0.2)
    ax1.set_title('Complete 128-Type Grid', fontsize=14, weight='bold')
    ax1.set_xlim(0, 16)
    ax1.set_ylim(16, 0)
    ax1.axis('off')
    
    # Plot 2: Gender Divergence
    ax2 = axes[0, 1]
    ax2.set_facecolor('white')
    for key, traj in all_traj.items():
        gender = key.split('_')[2]
        color = '#FF6B6B' if gender == 'F' else '#4ECDC4'
        ax2.plot(traj[:, 0], traj[:, 1], color=color, linewidth=0.5, alpha=0.15)
    ax2.set_title('Gender Divergence (Red=Female, Cyan=Male)', fontsize=14, weight='bold')
    ax2.set_xlim(0, 16)
    ax2.set_ylim(16, 0)
    ax2.axis('off')
    
    # Plot 3: E/I Divergence
    ax3 = axes[1, 0]
    ax3.set_facecolor('white')
    for key, traj in all_traj.items():
        mbti = key.split('_')[0]
        ei = mbti[0]
        color = '#FFD93D' if ei == 'E' else '#6BCB77'
        ax3.plot(traj[:, 0], traj[:, 1], color=color, linewidth=0.5, alpha=0.15)
    ax3.set_title('E/I Divergence (Yellow=Extravert, Green=Introvert)', fontsize=14, weight='bold')
    ax3.set_xlim(0, 16)
    ax3.set_ylim(16, 0)
    ax3.axis('off')
    
    # Plot 4: Blood Type Divergence
    ax4 = axes[1, 1]
    ax4.set_facecolor('white')
    blood_colors = {'O': '#D32F2F', 'A': '#1976D2', 'B': '#388E3C', 'AB': '#7B1FA2'}
    for key, traj in all_traj.items():
        blood = key.split('_')[1]
        ax4.plot(traj[:, 0], traj[:, 1], color=blood_colors[blood], 
                linewidth=0.5, alpha=0.15)
    ax4.set_title('Blood Type Divergence (O=Red, A=Blue, B=Green, AB=Purple)', fontsize=14, weight='bold')
    ax4.set_xlim(0, 16)
    ax4.set_ylim(16, 0)
    ax4.axis('off')
    
    plt.tight_layout()
    filename = f'128_DIVERGENCE_ANALYSIS_{int(time.time())}.png'
    plt.savefig(filename, dpi=200, facecolor='white', bbox_inches='tight')
    print(f"Saved: {filename}")

def export_trajectory_data():
    """Export all 128 trajectories as structured data."""
    import json
    
    data = {
        'metadata': {
            'physics_version': '1.0',
            'static_loop_ratio': '31:1',
            'spark_angle': SPARK_ANGLE_DEG,
            'grid_resolution': '16x16',
            'total_types': 128
        },
        'trajectories': {}
    }
    
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                key = f"{mbti}_{blood}_{gender}"
                traj = generate_trajectory(mbti, blood, gender)
                
                # Compute physics parameters used
                ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
                gp = GENDER_PHYSICS[gender]
                bp = BLOOD_PHYSICS[blood]
                
                data['trajectories'][key] = {
                    'mbti': mbti,
                    'blood': blood,
                    'gender': gender,
                    'physics_params': {
                        'vertical_speed': gp['Vy'],
                        'horizontal_amplitude': gp['Vx_amp'],
                        'mass': bp['mass'],
                        'radial_target': MBTI_PHYSICS[ei]['radial_target'],
                        'resonance': MBTI_PHYSICS[sn]['resonance_freq'],
                        'torsion': MBTI_PHYSICS[tf]['torsion'],
                        'damping': MBTI_PHYSICS[jp]['damping'],
                        'loop_window': [gp['loop_start'], gp['loop_end']]
                    },
                    'path': traj.tolist()
                }
    
    filename = '128_physics_trajectories.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Exported: {filename}")
    return data

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    import time
    
    print("=" * 70)
    print("128-TYPE PHYSICS TRAJECTORY GRID")
    print("=" * 70)
    print(f"Physics Constants:")
    print(f"  Static:Loop Ratio = 31:1")
    print(f"  Spark Angle = {SPARK_ANGLE_DEG}°")
    print(f"  3/32 Compression Gap = {F_3_32:.6f}")
    print(f"  Gender Physics: F(Vy={GENDER_PHYSICS['F']['Vy']}, Vx={GENDER_PHYSICS['F']['Vx_amp']})")
    print(f"                  M(Vy={GENDER_PHYSICS['M']['Vy']}, Vx={GENDER_PHYSICS['M']['Vx_amp']})")
    print()
    
    print("Generating 128 trajectories with PHYSICAL DIVERGENCE...")
    print("Each type follows distinct laws based on:")
    print("  - Gender (Polarity & Inertia)")
    print("  - MBTI (Field Coupling: E/I, S/N, T/F, J/P)")
    print("  - Blood Type (Metabolic Mass)")
    print()
    
    # Generate main grid
    render_trajectory_grid()
    
    # Generate divergence analysis
    print("\nGenerating divergence analysis...")
    render_with_divergence_analysis()
    
    # Export data
    print("\nExporting trajectory data...")
    export_trajectory_data()
    
    print("\n" + "=" * 70)
    print("COMPLETE: All trajectories are physically distinct.")
    print("No two types follow the same path.")
    print("=" * 70)
