# -*- coding: utf-8 -*-
"""
PHYSICS_128_GRID_DIPOLE.py
==========================
DIPOLE VORTEX: Male-Female Trajectory Exchange

Morning: Female (Left) → Male (Right) [Electron toss]
Evening: Male (Right) → Female (Left) [Energy return]

Coupling pairs meet at specific spacetime points for "evening convergence"
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

# Coupling: Which male types meet which female types
# Based on EJ/EP/IJ/IP complementarity
COUPLING_PAIRS = {
    # Female Group -> Male Group (evening meeting)
    ('EJ', 'F'): 'IP',  # EJ women meet IP men
    ('EP', 'F'): 'IJ',  # EP women meet IJ men
    ('IJ', 'F'): 'EP',  # IJ women meet EP men
    ('IP', 'F'): 'EJ',  # IP women meet EJ men
    # Male -> Female (reverse for male perspective)
    ('IP', 'M'): 'EJ',
    ('IJ', 'M'): 'EP',
    ('EP', 'M'): 'IJ',
    ('EJ', 'M'): 'IP',
}

GROUP_F = {'EJ': 0, 'EP': 2, 'IJ': 4, 'IP': 6}
GROUP_M = {'IP': 8, 'IJ': 10, 'EP': 12, 'EJ': 14}

ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]

BLOOD_P = {
    'O':  {'mass': 1.3, 'mom': 1.3, 'col': '#C62828'},
    'A':  {'mass': 1.0, 'mom': 1.0, 'col': '#1565C0'},
    'B':  {'mass': 0.7, 'mom': 0.8, 'col': '#2E7D32'},
    'AB': {'mass': 0.5, 'mom': 0.6, 'col': '#6A1B9A'}
}

# =============================================================================
# UNIVERSAL FIELD WITH DIPOLE
# =============================================================================

def universal_field_dipole(x, y, gender, phase='evening'):
    """
    Potential field with dipole coupling.
    
    phase='morning': Female → Male (left to right)
    phase='evening': Male → Female (right to left)
    """
    # Standard attractors
    d_left = math.sqrt((x - 3)**2 + (y - 5)**2)
    pot_left = -5.0 * math.exp(-d_left**2 / 3.0)
    
    d_right = math.sqrt((x - 13)**2 + (y - 5)**2)
    pot_right = -5.0 * math.exp(-d_right**2 / 3.0)
    
    # Terminal
    d_term = math.sqrt((x - 8)**2 + (y - 14)**2)
    pot_term = -6.0 * math.exp(-d_term**2 / 1.0)
    
    # Central barrier
    d_center = math.sqrt((x - 8)**2 + (y - 10)**2)
    if 6 < x < 10 and 8 < y < 12:
        barrier = 2.5 * math.exp(-d_center**2 / 2.0)
    else:
        barrier = 0
    
    # Evening meeting point (dipole exchange zone at y=8)
    d_meet = math.sqrt((x - 8)**2 + (y - 8)**2)
    if phase == 'evening':
        meeting = -3.0 * math.exp(-d_meet**2 / 4.0)  # Attract to center
    else:
        meeting = 0
    
    # Crossover field (dipole bridge)
    if phase == 'evening' and 6 < y < 10:
        if gender == 'M':
            # Men pushed left toward women
            dipole = -2.0 * (x - 5) / 5.0 if x > 5 else 0
        else:
            # Women pushed right toward men  
            dipole = 2.0 * (11 - x) / 5.0 if x < 11 else 0
    else:
        dipole = 0
    
    gravity = -0.35 * y
    
    return pot_left + pot_right + pot_term + barrier + meeting + gravity + dipole * 0.5

def field_grad(x, y, gender, phase='evening', dx=0.01):
    """Compute gradient"""
    dU_dx = (universal_field_dipole(x + dx, y, gender, phase) - 
             universal_field_dipole(x - dx, y, gender, phase)) / (2 * dx)
    dU_dy = (universal_field_dipole(x, y + dx, gender, phase) - 
             universal_field_dipole(x, y - dx, gender, phase)) / (2 * dx)
    return np.array([-dU_dx, -dU_dy])

# =============================================================================
# TRAJECTORY WITH DIPOLE EXCHANGE
# =============================================================================

def get_start(mbti, blood, gender):
    """Initial position"""
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_key = f"{ei}{jp}"
    
    if gender == 'F':
        base_x = GROUP_F[group_key]
    else:
        base_x = GROUP_M[group_key]
    
    sn_off = 0.35 if sn == 'N' else 0.12
    sn_dir = 1 if ei == 'E' else -1
    tf_off = 0.15 if tf == 'F' else 0.08
    b_off = {'O': -0.3, 'A': -0.1, 'B': 0.1, 'AB': 0.3}[blood]
    
    x = base_x + 0.5 + sn_off * sn_dir + tf_off + b_off
    y = 0.5
    
    return np.array([x, y])

def compute_velocity_dipole(x, y, mbti, blood, gender, step, max_steps):
    """Velocity with dipole coupling"""
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    bp = BLOOD_P[blood]
    
    # Determine phase based on vertical position
    progress = step / max_steps
    phase = 'evening' if progress > 0.4 else 'morning'
    
    # Base force
    force = field_grad(x, y, gender, phase)
    
    # E/I radial preference
    if ei == 'E':
        force[0] *= 1.2 if gender == 'F' else 0.8  # E women expand left, E men contract
    else:
        force[0] *= 0.8 if gender == 'F' else 1.2  # I women contract, I men expand right
    
    # Evening crossover (dipole exchange at y=6-10)
    if 6 < y < 11 and phase == 'evening':
        if gender == 'M' and x > 8:
            # Men cross left toward women
            force[0] -= 0.4 * (x - 8) / 4.0
        elif gender == 'F' and x < 8:
            # Women cross right toward men
            force[0] += 0.4 * (8 - x) / 4.0
    
    # T/F curvature
    if tf == 'F':
        dx, dy = x - 8, y - 8
        dist = math.sqrt(dx**2 + dy**2) + 0.001
        force[0] += -dy / dist * 0.5
        force[1] += dx / dist * 0.2
    
    # Spark at center for N-types
    if sn == 'N' and 7 < x < 9 and 9 < y < 11:
        if np.random.random() < 0.2:
            angle = math.radians(69.44)
            force[0] += math.cos(angle) * 0.6
            force[1] += math.sin(angle) * 0.4
    
    # J/P lattice
    if jp == 'J':
        grid_x = round(x / F_3_32) * F_3_32
        force[0] += (grid_x - x) * 0.2
    
    # Blood chaos
    if blood == 'B':
        np.random.seed(int(x * 1000 + y * 100) % 10000)
        force[0] += (np.random.random() - 0.5) * 0.3
    
    # Apply physics
    if gender == 'F':
        vx = force[0] * 2.8 * bp['mom']
    else:
        vx = force[0] * 1.2 * bp['mom']
    
    vy = abs(force[1]) * 0.8 + 0.15
    
    return np.array([vx, vy])

def generate_dipole(mbti, blood, gender, max_steps=500):
    """Generate trajectory with dipole exchange"""
    pos = get_start(mbti, blood, gender)
    bp = BLOOD_P[blood]
    
    positions = [pos.copy()]
    dt = 0.07
    
    for step in range(max_steps):
        v = compute_velocity_dipole(pos[0], pos[1], mbti, blood, gender, step, max_steps)
        
        pos = pos + v * dt
        pos[0] = max(0.3, min(15.7, pos[0]))
        
        if pos[1] > 15:
            break
        
        positions.append(pos.copy())
        
        if pos[1] >= 13.5:
            break
    
    return np.array(positions)

# =============================================================================
# RENDERING
# =============================================================================

def render_dipole():
    """Render with dipole coupling visible"""
    fig, ax = plt.subplots(figsize=(30, 22), facecolor='white')
    ax.set_facecolor('white')
    
    # Grid
    for i in range(17):
        ax.axhline(i, color='#E8E8E8', lw=0.4, alpha=0.6)
        ax.axvline(i, color='#E8E8E8', lw=0.4, alpha=0.6)
    
    # Separatrix
    ax.axvline(x=5, color='gray', linestyle=':', lw=1.5, alpha=0.5)
    ax.axvline(x=11, color='gray', linestyle=':', lw=1.5, alpha=0.5)
    
    # PLP
    ax.plot([0, 16], [16, 0], color='orange', linestyle='--', lw=2, alpha=0.6)
    
    # Dipole meeting zone (evening)
    ax.add_patch(plt.Rectangle((4, 6), 8, 4, facecolor='purple', alpha=0.05))
    ax.text(8, 8, 'DIPOLE EXCHANGE ZONE\n(Evening Meeting)', color='purple', 
            alpha=0.6, ha='center', va='center', fontsize=10, weight='bold')
    
    # Basins
    ax.add_patch(plt.Rectangle((0, 3), 3, 10, facecolor='green', alpha=0.04))
    ax.add_patch(plt.Rectangle((13, 3), 3, 10, facecolor='green', alpha=0.04))
    
    # Attractors
    ax.add_patch(plt.Circle((3, 5), 1.8, facecolor='red', alpha=0.08))
    ax.add_patch(plt.Circle((13, 5), 1.8, facecolor='blue', alpha=0.08))
    ax.text(3, 5, 'LEFT\nSINK', color='red', alpha=0.5, ha='center', va='center', fontsize=9)
    ax.text(13, 5, 'RIGHT\nSINK', color='blue', alpha=0.5, ha='center', va='center', fontsize=9)
    
    # Terminal
    ax.add_patch(plt.Circle((8, 14), 1.0, facecolor='purple', alpha=0.1))
    ax.text(8, 14, 'TERMINAL\nCONVERGENCE', color='purple', alpha=0.7, 
            ha='center', va='center', fontsize=9, weight='bold')
    
    # Draw all trajectories
    for mbti in ALL_MBTI:
        for blood in BLOOD_P.keys():
            for gender in ['F', 'M']:
                traj = generate_dipole(mbti, blood, gender)
                if len(traj) < 2:
                    continue
                
                # Color: Blood + Gender tint
                base = plt.cm.colors.to_rgb(BLOOD_P[blood]['col'])
                if gender == 'F':
                    col = (base[0]*0.9+0.15, base[1]*0.85+0.1, base[2]*0.9)
                else:
                    col = (base[0]*0.8, base[1]*0.9, base[2]*0.95+0.1)
                
                lw = 0.9 if mbti[3] == 'J' else 0.45
                alpha = 0.18 + (BLOOD_P[blood]['mass'] - 0.5) * 0.12
                
                ax.plot(traj[:, 0], traj[:, 1], color=col, lw=lw, 
                       alpha=alpha, solid_capstyle='round', zorder=10)
    
    # Labels
    labels = ['EJ WOMEN', 'EP WOMEN', 'IJ WOMEN', 'IP WOMEN',
              'IP MEN', 'IJ MEN', 'EP MEN', 'EJ MEN']
    for i, lbl in enumerate(labels):
        ax.text(i*2 + 1, -0.6, lbl, ha='center', va='top',
               fontsize=11, weight='bold', color='#333')
    
    # Arrows showing dipole flow
    ax.annotate('', xy=(6, 8), xytext=(10, 8),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2, alpha=0.5))
    ax.annotate('', xy=(10, 8), xytext=(6, 8),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2, alpha=0.5))
    
    ax.set_title(
        '128-TYPE DIPOLE GRID | Morning: F→M | Evening: M→F | One-Form Closure',
        fontsize=18, weight='bold', pad=20
    )
    
    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(16.5, -1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    
    fname = f'128_DIPOLE_GRID_{int(time.time())}.png'
    plt.savefig(fname, dpi=300, facecolor='white', bbox_inches='tight', pad_inches=0.3)
    print(f"Saved: {fname}")
    return fig, ax

if __name__ == "__main__":
    print("=" * 75)
    print("128-TYPE DIPOLE GRID - Male-Female Exchange")
    print("=" * 75)
    print("Morning: Female → Male (Left to Right, electron toss)")
    print("Evening: Male → Female (Right to Left, energy return)")
    print("Meeting: Dipole Exchange Zone (y=6-10, center)")
    print("=" * 75)
    print()
    render_dipole()
    print("\nComplete: Specific I-men cross to meet E-women at evening.")
