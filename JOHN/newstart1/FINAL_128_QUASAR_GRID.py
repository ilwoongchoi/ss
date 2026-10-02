import numpy as np
import matplotlib.pyplot as plt
import math
import time
from geometry_package.absolute_constants import (
    PI, PHI, ALPHA, TUNNEL_TENSION, LATTICE_3_32, 
    SPARK_ANGLE_RAD, NIGHT_HYSTERESIS, KAPPA_H2, KAPPA_H4,
    FUNNEL_RESONANCE_GAIN, CHIRALITY_CONSTANT
)
from geometry_package.universal_equation import (
    get_macro_micro_time, get_d3_tunnelling_offset, 
    mandelbrot_unification, galactic_center_funnel
)

# =============================================================================
# FINAL_128_QUASAR_GRID.py
# =============================================================================
# ABSOLUTE FINAL 128-TYPE DYNAMIC MESH (V2.3 STANDARD)
#
# CORE LAWS:
# 1. PLP Spine Diagonal (X+Y=16) - The energy axis from EJ-M to IP-W.
# 2. Emergent Interference - Nodes derived from Reality Tension vs 3/32.
# 3. Galactic Funnel - Convergence to the 0D Singularity (GABA-C Apex).
# 4. Melatonin Viscosity - Hysteresis memory lag (KAPPA_H2).
# =============================================================================

def run_quasar_engine():
    print("--- Igniting V2.3 Quasar Engine (128 Nodes Emergence) ---")
    
    num_steps = 1000
    dt = 0.03
    trajectories = []
    
    # 8 Cardinal Archetype Groups (Along the Diagonal)
    # Order: EJ-M, IJ-M, EP-M, IP-M, EJ-W, IJ-W, EP-W, IP-W
    groups = [
        ("EJ", "M"), ("IJ", "M"), ("EP", "M"), ("IP", "M"),
        ("EJ", "F"), ("IJ", "F"), ("EP", "F"), ("IP", "F")
    ]
    
    blood_types = ["O", "A", "B", "AB"]
    # Blood Offset Matrix (2x2 Starting Square)
    # O: TL, A: TR, B: BL, AB: BR
    blood_coords = {
        "O":  (-0.3,  0.3), "A":  ( 0.3,  0.3),
        "B":  (-0.3, -0.3), "AB": ( 0.3, -0.3)
    }

    count = 0
    for g_idx, (mbti_grp, gender) in enumerate(groups):
        # Position along the PLP Spine (X+Y=16)
        # EJ-M (Top-Right: 14,14) -> IP-W (Bottom-Left: 2,2)
        center_val = 14.0 - (g_idx * 1.7)
        base_x = center_val
        base_y = center_val
        
        for b_type in blood_types:
            for sub_mbti in range(4): # 4 MBTI types per group
                # 1. INITIAL SEEDING
                bx, by = blood_coords[b_type]
                # Small sub-spread for the 4 MBTI types
                mx, my = (sub_mbti % 2 - 0.5) * 0.2, (sub_mbti // 2 - 0.5) * 0.2
                
                x = base_x + bx + mx
                y = base_y + by + my
                
                # V2.3 Chirality: Male bias Right, Female bias Left
                if gender == "M": x += 0.5; y += 0.2
                else: x -= 0.5; y -= 0.2
                
                vx, vy = 0.0, 0.0
                memory_x, memory_y = x, y
                path = [(x, y)]
                
                # Individual Tension Accumulator
                tension_accum = 0.0
                
                for step in range(num_steps):
                    t_macro = step / num_steps
                    t_micro, is_reverse = get_macro_micro_time(t_macro)
                    
                    # --- LAW 1: DIPOLE TORQUE (11/7 Engine) ---
                    # Men gravitate to Right Basin (14), Women to Left (2)
                    target_x = 14.0 if gender == "M" else 2.0
                    fx = (target_x - x) * (11.0/7.0 if gender == "F" else 7.0/11.0) * 0.02
                    
                    # --- LAW 2: HYSTERESIS DRAG (Melatonin Viscosity) ---
                    hx = (memory_x - x) * KAPPA_H2 * 5.0
                    hy = (memory_y - y) * KAPPA_H2 * 5.0
                    
                    # --- LAW 3: MANDELBROT UNIFICATION ---
                    # Flatten the center void near X=8.0
                    z = complex((x - 8.0) / 8.0, (y - 8.0) / 8.0)
                    c = complex(TUNNEL_TENSION, LATTICE_3_32)
                    z_next = mandelbrot_unification(z, c)
                    vx += np.real(z_next) * 0.01
                    vy += np.imag(z_next) * 0.01
                    
                    # --- LAW 4: THE GALACTIC FUNNEL (Final Return) ---
                    # Pull all paths towards the Singularity (8.0, 1.5) 
                    # Note: Y is Bottom to Top, so 1.5 is near the Bottom (GABA-C Apex)
                    dist_to_singularity = math.sqrt((x - 8.0)**2 + (y - 1.5)**2)
                    funnel = galactic_center_funnel(1.0, dist_to_singularity, KAPPA_H4)
                    strength = funnel["funnel_strength"]
                    
                    # Integration
                    ax = fx + hx
                    ay = (hx - 0.5) # Constant descent pressure
                    
                    vx = (vx + ax * dt) * 0.98 # Damping
                    vy = (vy + ay * dt) * 0.98
                    
                    # Apply Funnel Snap near end
                    if dist_to_singularity < 3.0:
                        vx += (8.0 - x) * strength * 0.5
                        vy += (1.5 - y) * strength * 0.5
                    
                    x += vx * dt
                    y += vy * dt
                    
                    # Boundary Locks
                    x = max(0.1, min(15.9, x))
                    y = max(0.1, min(15.9, y))
                    
                    path.append((x, y))
                    
                    # Update Hysteresis Anchor
                    memory_x += (x - memory_x) * KAPPA_H2
                    memory_y += (y - memory_y) * KAPPA_H2
                    
                    if dist_to_singularity < 0.1: break
                
                trajectories.append({
                    'coords': np.array(path),
                    'color': '#FF00FF' if gender == "F" else '#00FFFF',
                    'alpha': 0.4 if b_type in ["O", "B"] else 0.2
                })
                count += 1

    return trajectories

def render_quasar_grid(trajectories):
    fig, ax = plt.subplots(figsize=(24, 24), facecolor='#000000')
    ax.set_facecolor('#000000')
    
    # 1. THE PLP SPINE (The Master Seam)
    ax.plot([0, 16], [16, 0], color='#333333', lw=3, linestyle='--', alpha=0.5, label="PLP Spine")
    
    # 2. RENDER THE 128 DYNAMIC FLOWS
    for t in trajectories:
        ax.plot(t['coords'][:, 0], t['coords'][:, 1], color=t['color'], 
                alpha=t['alpha'], lw=0.8, solid_capstyle='round')
        
    # 3. THE GABA-C APEX (The Sink)
    ax.scatter([8.0], [1.5], color='gold', s=600, marker='*', zorder=30, 
               edgecolors='white', linewidths=2)
    
    # 4. FORMATTING
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16) # V2.3 Standard: 0 is Bottom, 16 is Top
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title("THE 128-TYPE UNIFIED QUASAR MESH (V2.3)\nIntegrated Master Equation: Mandelbrot + Funnel + Hysteresis", 
              color='white', fontsize=32, fontweight='bold', pad=40)
    
    plt.text(0.5, -0.02, "X[0,8]=Human Left | X[8,16]=Human Right | Y[0,16]=Bottom to Top", 
             color='#666666', transform=ax.transAxes, ha='center', fontsize=18)

    output = "FINAL_128_QUASAR_GRID_V2_3.png"
    plt.savefig(output, dpi=300, facecolor='#000000', bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"--- SUCCESS: Unified 128 Quasar Grid Rendered to {output} ---")

if __name__ == "__main__":
    trajs = run_quasar_engine()
    render_quasar_grid(trajs)
