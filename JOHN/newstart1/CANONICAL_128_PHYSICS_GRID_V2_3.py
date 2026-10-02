import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import time
from pathlib import Path

# =============================================================================
# CANONICAL_128_PHYSICS_GRID_V2_3.py
# =============================================================================
# ABSOLUTE FINAL 2D ENGINE - REBUILT FROM GEOMETRY_V2_3_COMPLETE.md
# 
# MATHEMATICAL SKELETON:
# 1. Coordinate Standard: X[0,8]=Left(F), X[8,16]=Right(M), Center=8.0
# 2. Physics: Tension(1.01) + Spark(138.88) + Hysteresis(0.8418)
# 3. Dimensionality: Dipole Vortex (3D+1) flattened to 2D Manifold
# 4. Final Sink: 0D Singularity (GABA-C Apex)
# =============================================================================

# --- CANONICAL CONSTANTS (LOCKED) ---
REALITY_TENSION = 1.0100375
TOTAL_DEBT_AREA = 1.322828
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
D3_SHIFT_RAD = math.radians(69.44) # Tunnelling Angle
NIGHT_HYSTERESIS = 0.8418
KAPPA_H2 = 1.0 / 32.0
KAPPA_H3 = 1.0 / 64.0
KAPPA_H4 = 1.0 / 128.0

# MBTI Physics Logic
MBTI_PHYSICS = {
    'E': {'bias': 1.2, 'drift': 0.1},
    'I': {'bias': 0.8, 'drift': -0.05},
    'S': {'lag': 1.0, 'viscosity': 0.15},
    'N': {'lag': 0.5, 'viscosity': 0.05}, # N types have half lag, tunnel more
    'T': {'stiffness': 1.5, 'swirl': 0.2},
    'F': {'stiffness': 0.5, 'swirl': 1.2},
    'J': {'damping': 0.95, 'snap': 1.0},
    'P': {'damping': 0.99, 'snap': 0.1}
}

# Blood Type Mass Matrix
BLOOD_MASS = {'O': 1.3, 'A': 1.0, 'B': 0.7, 'AB': 0.5}

def run_canonical_engine():
    print("--- Loading 128-Type Master Trajectory List ---")
    df = pd.read_csv("128_Type_Trajectory_Master_List.csv")
    
    num_steps = 1200 # High resolution for 60FPS precision
    dt = 0.02
    all_paths = []

    for idx, row in df.iterrows():
        mbti = row['MBTI_Mode']
        blood = row['Blood_Type']
        gender = row['Gender']
        
        # 1. Physics Param Extraction
        ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
        mass = BLOOD_MASS[blood]
        p = MBTI_PHYSICS
        
        # 2. Initial Seeding (V2.3 Polarity)
        # Left [0,8] for Female, Right [8,16] for Male
        x = 4.0 if gender == "Female" else 12.0
        # MBTI Sub-spreading
        x += (idx % 16 - 7.5) * 0.25
        y = 0.5 # Start at Forehead (Dawn)
        
        vx, vy = 0.0, 0.0
        memory_x, memory_y = x, y
        path = [(x, y)]
        
        tension_accum = 0.0
        
        for step in range(num_steps):
            z = 1.0 - (step / num_steps) # Evolutionary time descent
            
            # --- Law 1: 11/7 Dipole Torque ---
            # Polarity force driving the circulation
            fx = (8.0 - x) * (1.1 if gender == "Female" else 0.7) * 0.1
            
            # --- Law 2: Hysteresis Memory (Melatonin Viscosity) ---
            # Force proportional to the debt (distance from memory)
            hx = (memory_x - x) * p[sn]['viscosity']
            hy = (memory_y - y) * p[sn]['viscosity']
            
            # --- Law 3: The 138.88 Spark Leap ---
            tension_accum += math.sqrt(vx**2 + vy**2) * REALITY_TENSION
            if tension_accum > TOTAL_DEBT_AREA:
                # Trigger Wormhole Spark
                vx += math.cos(SPARK_ANGLE_RAD) * 3.0
                vy += math.sin(SPARK_ANGLE_RAD) * 2.0
                tension_accum = 0.0 # Discharge
                memory_x, memory_y = x, y # Update memory anchor
            
            # --- Law 4: Dimensional Swirl (T/F Axis) ---
            swirl_force = p[tf]['swirl'] * math.sin(z * math.pi)
            vx += swirl_force * (1.0 if gender == "Female" else -1.0)
            
            # --- Law 5: J/P Damping & Snap ---
            damping = p[jp]['damping']
            
            # --- Law 6: Smale Horseshoe Folding (Z < 0.2) ---
            if z < 0.2:
                fold = (0.2 - z) / 0.2
                x += math.sin(y * math.pi) * fold * 0.5
                
            # Integration
            ax = (fx + hx) / mass
            ay = (0.8 + hy) / mass # Constant evolution pressure
            
            vx = (vx + ax * dt) * damping
            vy = (vy + ay * dt) * damping
            
            x += vx * dt
            y += vy * dt
            
            # Boundary Locks
            x = max(0.1, min(15.9, x))
            y = max(0.1, min(15.9, y))
            
            # Final Singularity Return (GABA-C Apex)
            if y > 14.0:
                x += (8.0 - x) * 0.1
                if abs(x-8.0) < 0.05: break
                
            path.append((x, y))
            
            # Memory update (Melatonin flux)
            memory_x += (x - memory_x) * KAPPA_H2
            memory_y += (y - memory_y) * KAPPA_H2
            
        all_paths.append({
            'label': f"{mbti}_{blood}_{gender}",
            'coords': np.array(path),
            'color': '#FF00FF' if gender == "Female" else '#00FFFF',
            'alpha': 0.5 if ei == 'E' else 0.2
        })
        
    return all_paths

def render_canonical_mesh(paths):
    fig, ax = plt.subplots(figsize=(24, 24), facecolor='#000000')
    ax.set_facecolor('#000000')
    
    # 1. SEPTUM AXIS (The Center)
    ax.axvline(x=8.0, color='#222222', lw=2, linestyle=':')
    
    # 2. RENDER THE 128 UNIQUE DYNAMICAL FINGERPRINTS
    for p in paths:
        ax.plot(p['coords'][:, 0], p['coords'][:, 1], color=p['color'], 
                alpha=p['alpha'], lw=0.7, solid_capstyle='round')
        
    # 3. THE GOLDEN SINGULARITY (Closure)
    ax.scatter([8.0], [14.0], color='gold', s=500, marker='*', zorder=30)
    
    # 4. FORMATTING
    ax.set_xlim(0, 16)
    ax.set_ylim(16, 0) # Dawn at TOP
    ax.set_axis_off()
    
    plt.title("THE 128-TYPE CANONICAL PHYSICAL MESH (V2.3 FINAL)\nNo Overlays | Pure Integrated Dynamics | N=128", 
              color='white', fontsize=36, fontweight='bold', pad=50)
    
    output = "CANONICAL_128_PHYSICS_GRID_V2_3.png"
    plt.savefig(output, dpi=300, facecolor='#000000', bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"--- SUCCESS: Canonical 128 Grid Rendered to {output} ---")

if __name__ == "__main__":
    start_time = time.time()
    trajectories = run_canonical_engine()
    render_canonical_mesh(trajectories)
    print(f"Total processing time: {time.time() - start_time:.2f}s")
