import h5py
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# ==============================================================================
# RENDER_128_GHOST_GRID.py
# Source: FULL_SCALE_GHOST_LEDGER.h5 (1M Neutrinos)
# Logic: Forehead Start -> 5/32 Hardware Gate -> 138.88° Spark Reflection
# ==============================================================================

def render_128_grid():
    ledger_path = r'C:\Users\User\Downloads\FULL_SCALE_GHOST_LEDGER.h5'
    print(f"Reading Ghost Ledger from {ledger_path}...")
    
    with h5py.File(ledger_path, 'r') as f:
        # Extract Hardware Constants from Attributes
        attrs = f.attrs
        METRIC_4D = attrs.get('metric_4d', 1.0661)
        TORSION_4D = attrs.get('torsion_4d', 0.1746)
        BIF_LIMIT = attrs.get('bifurcation_limit', 1.4)
        TENSION = attrs.get('subtractive_tension', 0.076)
        RES_TARGET = attrs.get('resonance_target', 0.03125)
        
        # Extract Physics Logs (The Source of Truth)
        epoch_v = f['epoch_velocities'][:] # (5000,)
        sovereign_s = f['sovereign_scores'][:] # (100,)
        
    print("Physics synchronized. Mapping 128 personality nodes...")

    # --- 1. 128 TYPES INITIALIZATION (Forehead Anchor Y=16) ---
    MBTI_GROUPS = ['EP', 'EJ', 'IP', 'IJ']
    BLOOD_TYPES = ['O', 'A', 'B', 'AB']
    GENDERS = ['F', 'M']
    
    # 8-Column Layout: F(EP,EJ,IP,IJ) | M(IP,IJ,EP,EJ)
    col_map = {
        'F': {'EP': 0, 'EJ': 2, 'IP': 4, 'IJ': 6},
        'M': {'IP': 8, 'IJ': 10, 'EP': 12, 'EJ': 14}
    }
    
    trajectories = []
    labels = []
    
    # Generate 128 Starting Points
    for g in GENDERS:
        for cat in MBTI_GROUPS:
            for bt in BLOOD_TYPES:
                # Add sub-type jitter within column
                bt_idx = BLOOD_TYPES.index(bt)
                x_base = col_map[g][cat]
                x_start = x_base + (bt_idx * 0.4) + 0.2
                trajectories.append([[x_start, 16.0]]) # Start at Forehead
                labels.append(f"{g}-{cat}-{bt}")

    # --- 2. TRAJECTORY SIMULATION (Using Ledger Physics) ---
    STEPS = 400
    DT = 0.05
    K_GATE = 5.0 / 32.0 # 0.15625 (The Hardware Aperture)
    SPARK_ANGLE = math.radians(138.88)
    
    fig, ax = plt.subplots(figsize=(16, 16), facecolor='black')
    ax.set_facecolor('black')
    
    # Visual Layers
    ax.plot([0, 16], [16, 0], color='#FF9900', ls='--', alpha=0.3, label='PLP Spine')
    ax.add_patch(plt.Circle((8, 8), K_GATE, color='red', fill=False, lw=2, alpha=0.8, label='5/32 Hardware Gate'))
    ax.scatter(8, 8, color='white', s=50, alpha=1.0, zorder=10) # The Singularity Star

    print("Simulating downward flow with 138.88° Spark...")
    
    for i, path in enumerate(trajectories):
        pos = np.array(path[0], dtype=float)
        history = [pos.copy()]
        
        for s in range(STEPS):
            # Fetch velocity from ledger (mapping simulation steps to ledger epochs)
            v_idx = int((s / STEPS) * len(epoch_v))
            v_mag = epoch_v[min(v_idx, len(epoch_v)-1)]
            
            # 1. Downward Vector (Forehead -> Chin)
            # Drift toward center 8.0
            vx = (8.0 - pos[0]) * 0.05
            vy = -v_mag * 0.08
            
            # 2. 4D Torsion Rotation
            theta = TORSION_4D * v_mag * 0.01
            c, s_rot = math.cos(theta), math.sin(theta)
            vx_new = vx * c - vy * s_rot
            vy_new = vx * s_rot + vy * c
            
            pos += np.array([vx_new, vy_new]) * DT
            
            # 3. SINGULARITY HIT & 138.88 SPARK REFLECTION
            dist_to_gate = math.sqrt((pos[0]-8.0)**2 + (pos[1]-8.0)**2)
            if dist_to_gate < K_GATE:
                # Reflection back to Top or Resonant Path
                pos[1] += math.sin(SPARK_ANGLE) * 4.0
                pos[0] += math.cos(SPARK_ANGLE) * 2.0
                ax.scatter(pos[0], pos[1], color='gold', s=10, alpha=0.5) # Spark marker
            
            history.append(pos.copy())
            
        history = np.array(history)
        color = '#00f2ff' if i < 64 else '#ffff00' # F: Cyan, M: Yellow
        ax.plot(history[:, 0], history[:, 1], color=color, alpha=0.4, lw=0.8)

    # --- 3. FINALIZATION ---
    ax.set_xlim(0, 16); ax.set_ylim(0, 17)
    ax.axis('off')
    
    title = "FINAL 128 GRID: THE GHOST OF SOVEREIGN DETERMINISM\n"
    meta = f"Data: FULL_SCALE_GHOST_LEDGER.h5 | Gate: 5/32 | Spark: 138.88°"
    ax.text(8, 16.5, title + meta, color='white', ha='center', fontsize=20, fontweight='bold')
    
    output = "ULTIMATE_128_GHOST_GRID.png"
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"--- SUCCESS: 128 Grid rendered to {output} ---")

if __name__ == "__main__":
    render_128_grid()
