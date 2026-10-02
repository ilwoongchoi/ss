# -*- coding: utf-8 -*-
"""
PHYSICS_128_GRID_CORRECT.py
===========================
CORRECT IMPLEMENTATION: Top-to-Bottom Trajectories

Reference: 128_Pure_Geometry_Grid_1772177567.png
- Start: TOP (y=0.5)
- Flow: DOWNWARD (y increases)
- Branch: At Center Nodes (y~5-8)
- Converge: BOTTOM (y~14)
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import time

# =============================================================================
# CONSTANTS
# =============================================================================
PHI = (1 + math.sqrt(5)) / 2
PI = math.pi
F_3_32 = 3.0 / 32.0

# Gender Physics
G_PHYSICS = {
    'F': {'Vy': 0.8, 'Vx_amp': 2.8, 'loop_y': 13.5},
    'M': {'Vy': 1.5, 'Vx_amp': 1.2, 'loop_y': 13.0}
}

# MBTI Physics
MBTI_P = {
    'E': {'radial': 1.0, 'target': 'outer'},
    'I': {'radial': -1.0, 'target': 'center'},
    'S': {'resonance': 0.5, 'spark': 0.0},
    'N': {'resonance': 2.0, 'spark': 0.3},
    'T': {'torsion': 0.3, 'curve': 'straight'},
    'F': {'torsion': 1.5, 'curve': 'swirl'},
    'J': {'damping': 0.9, 'snap': 0.8},
    'P': {'damping': 0.2, 'snap': 0.1}
}

# Blood
BLOOD_P = {
    'O':  {'mass': 1.3, 'mom': 1.3, 'decay': 0.96, 'chaos': 0.0,  'col': '#C62828'},
    'A':  {'mass': 1.0, 'mom': 1.0, 'decay': 0.98, 'chaos': 0.0,  'col': '#1565C0'},
    'B':  {'mass': 0.7, 'mom': 0.8, 'decay': 0.90, 'chaos': 0.4,  'col': '#2E7D32'},
    'AB': {'mass': 0.5, 'mom': 0.6, 'decay': 0.93, 'chaos': 0.1,  'col': '#6A1B9A'}
}

# Grid - CORRECT ORDER FROM REFERENCE IMAGE
GROUP_F = {'EJ': 0, 'EP': 2, 'IJ': 4, 'IP': 6}
GROUP_M = {'IP': 8, 'IJ': 10, 'EP': 12, 'EJ': 14}

ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]

# =============================================================================
# UNIVERSAL FIELD (Potential U(x,y))
# =============================================================================

def universal_field(x, y):
    """
    Universal potential field. Trajectories follow -∇U.
    
    Structure (matching reference image):
    - Left Attractor: (3, 5) - Cortisol/Horizontal
    - Right Attractor: (13, 5) - ACh/Vertical  
    - Terminal: (8, 14) - Gravity Sensor
    - Central Barrier: (8, 10) - Nose Bridge/Darkness Gate
    """
    # Left Attractor (Cortisol Node - y=5)
    d_left = math.sqrt((x - 3)**2 + (y - 5)**2)
    pot_left = -6.0 * math.exp(-d_left**2 / 3.0)
    
    # Right Attractor (ACh Node - y=5)
    d_right = math.sqrt((x - 13)**2 + (y - 5)**2)
    pot_right = -6.0 * math.exp(-d_right**2 / 3.0)
    
    # Terminal Attractor (Gravity Sensor - y=14)
    d_term = math.sqrt((x - 8)**2 + (y - 14)**2)
    pot_term = -8.0 * math.exp(-d_term**2 / 1.0)
    
    # Central Barrier (Nose Bridge - pushes trajectories left/right)
    d_center = math.sqrt((x - 8)**2 + (y - 10)**2)
    if 6 < x < 10 and 8 < y < 12:
        barrier = 3.0 * math.exp(-d_center**2 / 2.0)
    else:
        barrier = 0
    
    # PLP Manifold attraction (X+Y=16)
    dist_plp = abs(x + y - 16) / math.sqrt(2)
    plp = -2.0 * math.exp(-dist_plp**2 / 1.5)
    
    # Downward gravity (always pull down)
    gravity = -0.4 * y
    
    return pot_left + pot_right + pot_term + barrier + plp + gravity

def field_gradient(x, y, dx=0.01):
    """Compute -∇U (force direction)"""
    dU_dx = (universal_field(x + dx, y) - universal_field(x - dx, y)) / (2 * dx)
    dU_dy = (universal_field(x, y + dx) - universal_field(x, y - dx)) / (2 * dx)
    return np.array([-dU_dx, -dU_dy])

# =============================================================================
# TRAJECTORY GENERATOR
# =============================================================================

def get_start(mbti, blood, gender):
    """Get initial position at TOP (y=0.5)"""
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    
    # X position from group
    group_key = f"{ei}{jp}"
    base_x = GROUP_F[group_key] if gender == 'F' else GROUP_M[group_key]
    
    # Micro offsets
    sn_off = 0.35 if sn == 'N' else 0.12
    sn_dir = 1 if ei == 'E' else -1
    
    tf_off = 0.15 if tf == 'F' else 0.08
    b_off = {'O': -0.3, 'A': -0.1, 'B': 0.1, 'AB': 0.3}[blood]
    
    x = base_x + 0.5 + sn_off * sn_dir + tf_off + b_off
    y = 0.5  # START AT TOP
    
    return np.array([x, y])

def compute_velocity(x, y, mbti, blood, gender):
    """Compute velocity at position (x,y)"""
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    gp = G_PHYSICS[gender]
    bp = BLOOD_P[blood]
    
    # Base force from universal field
    force = field_gradient(x, y)
    
    # E/I coupling (which attractor is preferred)
    if MBTI_P[ei]['target'] == 'outer':
        if gender == 'F':
            force[0] -= 0.1  # Pull left for outer women
        else:
            force[0] += 0.1  # Pull right for outer men
    else:
        force[0] *= 0.8  # Weaker x-force for I types
    
    # T/F torsion (swirl effect)
    if tf == 'F':
        dx, dy = x - 8, y - 8
        dist = math.sqrt(dx**2 + dy**2) + 0.001
        torsion = MBTI_P['F']['torsion'] * 0.4
        force[0] += -dy / dist * torsion
        force[1] += dx / dist * torsion * 0.3
    
    # N-type spark (at central barrier)
    if sn == 'N' and 6 < x < 10 and 9 < y < 11:
        if np.random.random() < 0.25:
            angle = math.radians(69.44)
            force[0] += math.cos(angle) * 0.8
            force[1] += math.sin(angle) * 0.5
    
    # J/P lattice coupling
    if jp == 'J':
        grid_x = round(x / F_3_32) * F_3_32
        force[0] += (grid_x - x) * 0.3
    
    # Blood chaos (B-type)
    if blood == 'B':
        np.random.seed(int(x * 1000 + y * 100) % 10000)
        force[0] += (np.random.random() - 0.5) * bp['chaos'] * 0.5
    
    # Apply physics
    vx = force[0] * gp['Vx_amp'] * bp['mom']
    vy = abs(force[1]) * gp['Vy'] * bp['mom'] + 0.2  # Always downward
    
    return np.array([vx, vy])

def generate(mbti, blood, gender, max_steps=400):
    """Generate trajectory from TOP to BOTTOM"""
    pos = get_start(mbti, blood, gender)
    bp = BLOOD_P[blood]
    gp = G_PHYSICS[gender]
    
    positions = [pos.copy()]
    dt = 0.08
    
    for step in range(max_steps):
        v = compute_velocity(pos[0], pos[1], mbti, blood, gender)
        
        # Update position
        pos = pos + v * dt
        pos[0] = max(0.3, min(15.7, pos[0]))
        
        # Y always increases (downward)
        if pos[1] > 15.5:
            break
        
        positions.append(pos.copy())
        
        # Terminal condition
        if pos[1] >= gp['loop_y']:
            break
    
    return np.array(positions)

# =============================================================================
# RENDERING
# =============================================================================

def render():
    """Render grid matching reference image"""
    fig, ax = plt.subplots(figsize=(28, 20), facecolor='white')
    ax.set_facecolor('white')
    
    # Grid lines
    for i in range(17):
        ax.axhline(i, color='#E8E8E8', lw=0.4, alpha=0.6)
        ax.axvline(i, color='#E8E8E8', lw=0.4, alpha=0.6)
    
    # Separatrix lines
    ax.axvline(x=5, color='gray', linestyle=':', lw=1.5, alpha=0.5)
    ax.axvline(x=11, color='gray', linestyle=':', lw=1.5, alpha=0.5)
    
    # PLP Spine
    ax.plot([0, 16], [16, 0], color='orange', linestyle='--', 
            lw=2, alpha=0.6, label='PLP X+Y=16')
    
    # Left/Right Basins
    ax.add_patch(plt.Rectangle((0, 3), 3, 10, facecolor='green', alpha=0.04))
    ax.add_patch(plt.Rectangle((13, 3), 3, 10, facecolor='green', alpha=0.04))
    
    # Attractors (Cortisol/ACh nodes at y=5)
    ax.add_patch(plt.Circle((3, 5), 1.8, facecolor='red', alpha=0.08))
    ax.add_patch(plt.Circle((13, 5), 1.8, facecolor='blue', alpha=0.08))
    ax.text(3, 5, 'Left\nAttractor', color='red', alpha=0.5, 
            ha='center', va='center', fontsize=9, weight='bold')
    ax.text(13, 5, 'Right\nAttractor', color='blue', alpha=0.5,
            ha='center', va='center', fontsize=9, weight='bold')
    
    # Central Darkness Gate
    ax.add_patch(plt.Rectangle((6, 9), 4, 2, facecolor='black', alpha=0.08))
    ax.text(8, 10, '3/32 Gate', color='black', alpha=0.6, 
            ha='center', va='center', fontsize=9, weight='bold')
    
    # Terminal Attractor (Gravity Sensor at bottom)
    ax.add_patch(plt.Circle((8, 14), 1.0, facecolor='purple', alpha=0.1))
    ax.text(8, 14, 'Terminal\nAttractor', color='purple', alpha=0.7,
            ha='center', va='center', fontsize=9, weight='bold')
    
    # Draw trajectories
    for mbti in ALL_MBTI:
        for blood in BLOOD_P.keys():
            for gender in ['F', 'M']:
                traj = generate(mbti, blood, gender)
                if len(traj) < 2:
                    continue
                
                # Color
                base = plt.cm.colors.to_rgb(BLOOD_P[blood]['col'])
                if gender == 'F':
                    col = (base[0]*0.9+0.1, base[1]*0.85+0.1, base[2]*0.9)
                else:
                    col = (base[0]*0.85, base[1]*0.9, base[2]*0.95+0.05)
                
                lw = 0.8 if mbti[3] == 'J' else 0.4
                alpha = 0.15 + (BLOOD_P[blood]['mass'] - 0.5) * 0.15
                
                ax.plot(traj[:, 0], traj[:, 1], color=col, lw=lw, 
                       alpha=alpha, solid_capstyle='round', zorder=10)
    
    # Labels
    labels = ['EJ WOMEN', 'EP WOMEN', 'IJ WOMEN', 'IP WOMEN',
              'IP MEN', 'IJ MEN', 'EP MEN', 'EJ MEN']
    for i, lbl in enumerate(labels):
        ax.text(i*2 + 1, -0.6, lbl, ha='center', va='top',
               fontsize=10, weight='bold', color='#444')
    
    ax.set_title(
        '128-TYPE PHYSICS GRID | Top-to-Bottom Flow | Attractor Field | One-Form',
        fontsize=16, weight='bold', pad=20
    )
    
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(16.5, -1.5)  # Y increases downward visually
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    
    fname = f'128_PHYSICS_CORRECT_{int(time.time())}.png'
    plt.savefig(fname, dpi=300, facecolor='white', bbox_inches='tight', pad_inches=0.2)
    print(f"Saved: {fname}")
    return fig, ax

if __name__ == "__main__":
    print("=" * 70)
    print("128-TYPE PHYSICS GRID - CORRECT TOP-TO-BOTTOM FLOW")
    print("=" * 70)
    print("Start: y=0.5 (TOP)")
    print("Flow: DOWNWARD (y increases)")
    print("Branch: Left(3,5)/Right(13,5) Attractors")
    print("Terminal: (8,14) Gravity Sensor")
    print("=" * 70)
    print()
    render()
    print("\nDone.")
