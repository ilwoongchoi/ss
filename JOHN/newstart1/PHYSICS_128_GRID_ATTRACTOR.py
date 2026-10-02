# -*- coding: utf-8 -*-
"""
PHYSICS_128_GRID_ATTRACTOR.py
=============================
UNIVERSAL ATTRACTOR FIELD - Space itself determines the trajectories

PHYSICAL REALITY (No hardcoded labels, only forces):
- Space has Potential Field U(x,y) - trajectories follow -∇U
- Attractor Points: Local minima in potential landscape  
- Separatrix: Basin boundaries where trajectories bifurcate
- PLP Constraint: Diagonal manifold X+Y=16 acts as equilibrium axis
- Refraction: Trajectories bend when crossing critical boundaries
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import time

# =============================================================================
# UNIVERSAL CONSTANTS (Physics Laws)
# =============================================================================
PHI = (1 + math.sqrt(5)) / 2
PI = math.pi
F_3_32 = 3.0 / 32.0  # Grid compression

# =============================================================================
# POTENTIAL FIELD GENERATOR
# =============================================================================

def potential_field(x, y):
    """
    Define the universal potential field U(x,y).
    Trajectories follow steepest descent: v = -∇U
    
    Critical features (emergent from physics, not hardcoded):
    1. Left Sink: Around (3, 5) - basin for left-side types
    2. Right Sink: Around (13, 5) - basin for right-side types  
    3. Central Barrier: Around (8, 10) - nose bridge region
    4. Terminal Sink: Around (8, 14) - final convergence
    5. PLP Manifold: X+Y=16 diagonal equilibrium
    """
    # Distance to PLP diagonal (X+Y=16)
    dist_plp = abs((x + y - 16) / math.sqrt(2))
    
    # Left Attractor (basin at lower left)
    d_left = math.sqrt((x - 3)**2 + (y - 5)**2)
    potential_left = -8.0 * math.exp(-d_left**2 / (2 * 2.0**2))  # Deep well
    
    # Right Attractor (basin at lower right)
    d_right = math.sqrt((x - 13)**2 + (y - 5)**2)
    potential_right = -8.0 * math.exp(-d_right**2 / (2 * 2.0**2))  # Deep well
    
    # Terminal Attractor (bottom center - gravity well)
    d_terminal = math.sqrt((x - 8)**2 + (y - 14)**2)
    potential_terminal = -6.0 * math.exp(-d_terminal**2 / (2 * 0.8**2))  # Sharp, deep terminal well
    
    # Central Barrier (nose bridge - potential hill to push trajectories sideways)
    d_center = math.sqrt((x - 8)**2 + (y - 8)**2)
    if 5 < x < 11 and 6 < y < 11:
        barrier = 4.0 * math.exp(-d_center**2 / (2 * 1.5**2))  # Stronger barrier
    else:
        barrier = 0
    
    # PLP Manifold attraction (diagonal X+Y=16)
    # Types are attracted to different "heights" on this diagonal
    plp_attraction = -1.5 * math.exp(-dist_plp**2 / (2 * 1.0**2))
    
    # Vertical gravity (global downward drift - Y increases downward in our coord)
    # Potential DECREASES as Y increases (so gradient points downward)
    gravity = -0.5 * y  # At Y=0: 0, at Y=16: -8 (decreasing)
    
    return potential_left + potential_right + potential_terminal + barrier + plp_attraction + gravity

def gradient_potential(x, y, dx=0.01):
    """Compute -∇U (steepest descent direction)"""
    dU_dx = (potential_field(x + dx, y) - potential_field(x - dx, y)) / (2 * dx)
    dU_dy = (potential_field(x, y + dx) - potential_field(x, y - dx)) / (2 * dx)
    return np.array([-dU_dx, -dU_dy])  # Negative gradient = force

# =============================================================================
# TYPE-SPECIFIC PHYSICAL PARAMETERS
# =============================================================================

# Each type has unique coupling constants to the universal field
TYPE_PHYSICS = {}

# MBTI determines how strongly each type couples to field features
MBTI_COEFF = {
    # E/I: Determines left/right basin preference
    'E': {'left_coupling': 0.3, 'right_coupling': 1.0, 'center_coupling': 0.2},
    'I': {'left_coupling': 0.8, 'right_coupling': 0.3, 'center_coupling': 1.0},
    
    # S/N: Determines resonance with grid/compression
    'S': {'grid_coupling': 0.2, 'barrier_transparency': 0.1, 'refraction': 0.0},
    'N': {'grid_coupling': 1.0, 'barrier_transparency': 0.8, 'refraction': 69.44},
    
    # T/F: Determines path curvature (straight vs spiral)
    'T': {'torsion': 0.2, 'inertia': 1.2, 'damping': 0.9},
    'F': {'torsion': 1.8, 'inertia': 0.8, 'damping': 0.4},
    
    # J/P: Determines discrete vs continuous flow
    'J': {'snap_to_grid': 0.8, 'quantization': 1.0, 'entropy': 0.2},
    'P': {'snap_to_grid': 0.1, 'quantization': 0.0, 'entropy': 0.8}
}

# Blood type determines mass/momentum (how type responds to forces)
BLOOD_PHYSICS = {
    'O':  {'mass': 1.4, 'momentum': 1.3, 'decay': 0.96, 'chaos': 0.0},
    'A':  {'mass': 1.0, 'momentum': 1.0, 'decay': 0.98, 'chaos': 0.0},
    'B':  {'mass': 0.7, 'momentum': 0.8, 'decay': 0.92, 'chaos': 0.4},
    'AB': {'mass': 0.5, 'momentum': 0.6, 'decay': 0.94, 'chaos': 0.1}
}

# Gender determines anisotropy (horizontal vs vertical coupling)
GENDER_PHYSICS = {
    'F': {'Vx_amp': 2.8, 'Vy_base': 0.8, 'asymmetry': -0.3},  # Left-biased
    'M': {'Vx_amp': 1.2, 'Vy_base': 1.5, 'asymmetry': 0.3}    # Right-biased
}

# Grid groups
GROUP_F = {'EJ': 0, 'EP': 2, 'IJ': 4, 'IP': 6}
GROUP_M = {'IP': 8, 'IJ': 10, 'EP': 12, 'EJ': 14}

ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]

# =============================================================================
# TRAJECTORY GENERATOR
# =============================================================================

def get_initial_position(mbti, blood, gender):
    """
    Initial position is determined by EJ/EP/IJ/IP group + micro-offsets
    This is the ONLY place type identity enters (initial conditions)
    After this, pure physics takes over
    """
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Base group position
    group_key = f"{ei}{jp}"
    base_x = GROUP_F[group_key] if gender == 'F' else GROUP_M[group_key]
    
    # Micro-offsets (deterministic, not random)
    # S/N determines initial "spread"
    sn_off = 0.4 if sn == 'N' else 0.15
    sn_dir = 1 if ei == 'E' else -1
    
    # T/F determines initial angle
    tf_off = 0.2 if tf == 'F' else 0.08
    
    # Blood determines vertical offset (mass affects starting height)
    b_mass = BLOOD_PHYSICS[blood]['mass']
    y_offset = (1.5 - b_mass) * 0.4  # Heavier = lower start
    
    b_offsets = {'O': -0.3, 'A': -0.1, 'B': 0.1, 'AB': 0.3}
    
    x = base_x + 0.5 + sn_off * sn_dir + tf_off + b_offsets[blood]
    y = 0.5 + y_offset
    
    return np.array([x, y])

def compute_velocity_field(x, y, mbti, blood, gender):
    """
    Compute velocity at point (x,y) for given type.
    This is where the UNIVERSAL PHYSICS applies.
    """
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # Get base force from potential field
    force = gradient_potential(x, y)
    
    # Apply type-specific coupling to field components
    coeff_ei = MBTI_COEFF[ei]
    coeff_sn = MBTI_COEFF[sn]
    coeff_tf = MBTI_COEFF[tf]
    coeff_jp = MBTI_COEFF[jp]
    
    blood_p = BLOOD_PHYSICS[blood]
    gender_p = GENDER_PHYSICS[gender]
    
    # Modulate force based on E/I (which basin is preferred)
    if x < 8:  # Left side
        force[0] *= coeff_ei['left_coupling'] * (1 + gender_p['asymmetry'])
    else:  # Right side
        force[0] *= coeff_ei['right_coupling'] * (1 - gender_p['asymmetry'])
    
    # N-type: Can penetrate central barrier (transparency)
    if 6 < x < 10 and y > 8:
        force[1] *= (1 + coeff_sn['barrier_transparency'])
    
    # F-type: Add torsion (swirl around attractors)
    if coeff_tf['torsion'] > 0.5:
        dx = x - 8
        dy = y - 8
        dist = math.sqrt(dx**2 + dy**2) + 0.001
        torsion_strength = coeff_tf['torsion'] * 0.3
        force[0] += -dy / dist * torsion_strength
        force[1] += dx / dist * torsion_strength * 0.5
    
    # T-type: Straighten path toward nearest attractor
    else:
        # Find nearest basin
        if x < 8:
            target_x = 3
        else:
            target_x = 13
        force[0] += (target_x - x) * 0.05 * coeff_tf['inertia']
    
    # J-type: Snap to 3/32 grid when close
    if coeff_jp['snap_to_grid'] > 0.5:
        grid_x = round((x - 8) / F_3_32) * F_3_32 + 8
        grid_y = round(y / F_3_32) * F_3_32
        if abs(x - grid_x) < 0.15:
            force[0] += (grid_x - x) * coeff_jp['snap_to_grid']
    
    # P-type: Add entropy (Brownian motion)
    if coeff_jp['entropy'] > 0.5:
        seed = int(x * 1000 + y * 100) + hash(mbti) % 10000
        np.random.seed(seed)
        force[0] += (np.random.random() - 0.5) * coeff_jp['entropy'] * 0.3
        force[1] += (np.random.random() - 0.5) * coeff_jp['entropy'] * 0.2
    
    # N-type spark: Refraction at critical angle when hitting barrier
    if sn == 'N' and 6 < x < 10 and y > 9 and y < 11:
        if np.random.random() < 0.3:  # Spark event
            angle_rad = math.radians(69.44)
            force[0] += math.cos(angle_rad) * 1.5
            force[1] += math.sin(angle_rad) * 1.0
    
    # Apply blood physics (mass/momentum/decay)
    vx = force[0] * gender_p['Vx_amp'] * blood_p['momentum'] / blood_p['mass']
    vy = force[1] * gender_p['Vy_base'] * blood_p['momentum'] / blood_p['mass']
    
    # B-type chaos (noradrenaline jitter)
    if blood == 'B':
        np.random.seed(int(time.time() * 1000) % 10000)
        vx += (np.random.random() - 0.5) * blood_p['chaos'] * 0.5
        vy += (np.random.random() - 0.5) * blood_p['chaos'] * 0.3
    
    return np.array([vx, vy])

def generate_trajectory(mbti, blood, gender, max_steps=600):
    """Generate trajectory following physics field"""
    pos = get_initial_position(mbti, blood, gender)
    bp = BLOOD_PHYSICS[blood]
    
    positions = [pos.copy()]
    dt = 0.05
    velocity = np.array([0.0, 0.0])
    
    for step in range(max_steps):
        # Get instantaneous velocity from field
        field_v = compute_velocity_field(pos[0], pos[1], mbti, blood, gender)
        
        # Smooth velocity update (inertia)
        velocity = velocity * bp['decay'] + field_v * (1 - bp['decay'])
        
        # Speed limit
        speed = np.linalg.norm(velocity)
        if speed > 1.2:
            velocity = velocity / speed * 1.2
        
        # Update position (Y increases downward)
        pos[1] += velocity[1] * dt  # Y goes down
        pos[0] += velocity[0] * dt
        
        # Boundaries
        pos[0] = max(0.3, min(15.7, pos[0]))
        pos[1] = max(0.3, min(15.7, pos[1]))
        
        positions.append(pos.copy())
        
        # Terminal condition: reached gravity well (very close)
        dist_terminal = math.sqrt((pos[0] - 8)**2 + (pos[1] - 14)**2)
        if dist_terminal < 0.6:
            # Dream folding - collapse to start
            start = get_initial_position(mbti, blood, gender)
            positions.append(start)
            break
        
        if pos[1] >= 15.5:
            break
    
    return np.array(positions)

# =============================================================================
# RENDERING
# =============================================================================

def render_universal_grid():
    """Render the final physics grid with all features"""
    fig, ax = plt.subplots(figsize=(28, 22), facecolor='white')
    ax.set_facecolor('white')
    
    # Background grid
    for i in range(17):
        ax.axhline(i, color='#EEEEEE', linewidth=0.4, alpha=0.6)
        ax.axvline(i, color='#EEEEEE', linewidth=0.4, alpha=0.6)
    
    # PLP Spine (X+Y=16) - Diagonal equilibrium manifold
    ax.plot([0, 16], [16, 0], color='orange', linestyle='--', 
            linewidth=2, alpha=0.6, label='PLP Manifold X+Y=16', zorder=5)
    
    # Separatrix boundaries (basin dividers)
    ax.axvline(x=5, color='gray', linestyle=':', linewidth=1.5, alpha=0.5, zorder=5)
    ax.axvline(x=11, color='gray', linestyle=':', linewidth=1.5, alpha=0.5, zorder=5)
    
    # Left/Right Bypass Basins (implicitly defined by attractor positions)
    # Visual indicators only - actual physics is in the potential field
    ax.add_patch(plt.Rectangle((0, 3), 3, 10, facecolor='green', 
                                alpha=0.03, zorder=0))
    ax.add_patch(plt.Rectangle((13, 3), 3, 10, facecolor='green', 
                                alpha=0.03, zorder=0))
    ax.text(1.5, 8, 'Left Basin', color='green', alpha=0.4, 
            ha='center', fontsize=9, weight='bold')
    ax.text(14.5, 8, 'Right Basin', color='green', alpha=0.4, 
            ha='center', fontsize=9, weight='bold')
    
    # Attractor regions (potential wells)
    # These emerge from physics, not hardcoded
    ax.add_patch(plt.Circle((3, 5), 1.5, facecolor='red', alpha=0.05, zorder=0))
    ax.add_patch(plt.Circle((13, 5), 1.5, facecolor='blue', alpha=0.05, zorder=0))
    ax.add_patch(plt.Circle((8, 14), 1.0, facecolor='purple', alpha=0.08, zorder=0))
    
    # Central barrier region (potential hill)
    ax.add_patch(plt.Rectangle((6, 10), 4, 1.5, facecolor='black', 
                                alpha=0.06, zorder=0))
    ax.text(8, 10.75, '3/32 Compression', color='black', alpha=0.5,
            ha='center', va='center', fontsize=9, weight='bold')
    
    # Generate and draw trajectories
    for mbti in ALL_MBTI:
        for blood in ['O', 'A', 'B', 'AB']:
            for gender in ['F', 'M']:
                traj = generate_trajectory(mbti, blood, gender)
                if len(traj) < 2:
                    continue
                
                # Color by blood type
                colors = {'O': '#C62828', 'A': '#1565C0', 'B': '#2E7D32', 'AB': '#6A1B9A'}
                base_col = colors[blood]
                
                # Gender tint
                rgb = plt.cm.colors.to_rgb(base_col)
                if gender == 'F':
                    rgb = (rgb[0]*0.9+0.1, rgb[1]*0.85+0.1, rgb[2]*0.9)
                else:
                    rgb = (rgb[0]*0.85, rgb[1]*0.9, rgb[2]*0.95+0.05)
                
                # Line width by J/P
                lw = 0.9 if mbti[3] == 'J' else 0.4
                
                # Alpha by mass
                mass = BLOOD_PHYSICS[blood]['mass']
                alpha = 0.2 + (mass - 0.5) * 0.15
                
                ax.plot(traj[:, 0], traj[:, 1], color=rgb, 
                       linewidth=lw, alpha=alpha, solid_capstyle='round', zorder=10)
    
    # Group labels
    labels = ['EJ WOMEN', 'EP WOMEN', 'IJ WOMEN', 'IP WOMEN',
              'IP MEN', 'IJ MEN', 'EP MEN', 'EJ MEN']
    for i, lbl in enumerate(labels):
        ax.text(i*2 + 1, -0.6, lbl, ha='center', va='top',
               fontsize=10, weight='bold', color='#444444')
    
    ax.text(3, 5, '← Left Attractor', color='red', alpha=0.5, 
            fontsize=8, style='italic')
    ax.text(13, 5, 'Right Attractor →', color='blue', alpha=0.5, 
            fontsize=8, style='italic', ha='right')
    ax.text(8, 14, 'Terminal\nAttractor', color='purple', alpha=0.6,
            fontsize=8, ha='center', va='center', weight='bold')
    
    ax.text(5, -1.2, 'Separatrix', color='gray', fontsize=8, ha='center')
    ax.text(11, -1.2, 'Separatrix', color='gray', fontsize=8, ha='center')
    
    # Title
    ax.set_title(
        '128-TYPE UNIVERSAL ATTRACTOR GRID | Potential Field U(x,y) | '
        '∇U Physics | One-Form Closure',
        fontsize=16, weight='bold', pad=20
    )
    
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(-2, 16.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    
    fname = f'128_ATTRACTOR_GRID_{int(time.time())}.png'
    plt.savefig(fname, dpi=300, facecolor='white', bbox_inches='tight', pad_inches=0.3)
    print(f"Saved: {fname}")
    return fig, ax

if __name__ == "__main__":
    print("=" * 70)
    print("128-TYPE UNIVERSAL ATTRACTOR GRID")
    print("=" * 70)
    print("\nPhysics: Potential Field U(x,y) with emergent attractors")
    print("Left Attractor: (3, 5) | Right Attractor: (13, 5) | Terminal: (8, 14)")
    print("PLP Manifold: X+Y=16 | Separatrix: X=5, X=11")
    print("\nTypes follow -∇U (steepest descent) with type-specific coupling")
    print("=" * 70)
    print()
    
    render_universal_grid()
    
    print("\nDone. Attractor field defines trajectories, not hardcoded paths.")
