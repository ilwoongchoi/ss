import numpy as np
import matplotlib.pyplot as plt
import math

def render_v13_observer_will_engine():
    # --- 1. AXIOM: OBSERVER CONSTANTS ---
    DELTA_T_OBS = 0.2828
    SPARK_ANGLE_DEG = 138.88
    SPARK_RAD = math.radians(SPARK_ANGLE_DEG)
    
    # 10-Axis Biological Operators (Transducers)
    # These are not just variables, they are the Observer's HANDS.
    # 0.0 to 1.0 (Normalized Intent)
    ops = {
        "VASO_V1AR": 1.0,    # Container Expansion (Volume)
        "OXY_OTR": 1.0,      # EM Binding (Cohesion)
        "GABA_A": 1.0,       # Spark Trigger (Discharge)
        "GABA_B": 0.5,       # Heat Damping (Cooling)
        "CORTISOL_GR": 0.5,  # Lensing Resistance (Load)
        "5HT_WILL": 1.0,     # Time Vector (Drive)
        "5HT1A_SINK": 1.0,   # Void Access (Drain)
        "D2_LEFT": 1.0,      # Entropy Collection
        "D2_RIGHT": 1.0,     # Sovereign Projection
        "ACETYL_COA": 1.0    # Structural Integrity
    }

    fig, ax = plt.subplots(figsize=(16, 16), facecolor='black')
    ax.set_facecolor('black')
    
    # Coordinate System: Observer's View anchored at PLP Core (Top-Left)
    ax.set_xlim(-2, 18)
    ax.set_ylim(18, -2) # Y-flip: Top is 0
    
    # The Zero Point (The Observer's Eye)
    ax.scatter([0], [0], color='gold', s=600, marker='*', label='PLP CORE (ZERO POINT / OBSERVER EYE)')
    
    # --- 2. TRAJECTORY GENERATION (The Gaze) ---
    # Not particles, but "Rays of Attention"
    num_rays = 128
    rays = []
    
    # Initial Distribution: Forehead Line (The Mental Screen)
    for i in range(num_rays):
        # 128 distinct phase angles of thought
        phase_seed = (i / num_rays) * 2 * np.pi
        
        # Start at Forehead (Mental Plane)
        start_x = (i / num_rays) * 16.0
        start_y = 0.5 + 0.1 * math.sin(phase_seed * 4) # Brainwave jitter
        
        rays.append({
            "pos": np.array([start_x, start_y], dtype=float),
            "vel": np.array([0.0, 0.0], dtype=float),
            "path": [],
            "phase": phase_seed,
            "id": i
        })

    print(f"Projecting {num_rays} Rays of Observer's Will...")
    
    # --- 3. DYNAMICS: THE OBSERVER'S INTERVENTION ---
    steps = 400
    dt = 0.05
    
    for t_step in range(steps):
        t = t_step * dt
        
        # Phase 1: The Gaze (0.2828 Delay)
        # Observer establishes the field before acting
        if t < DELTA_T_OBS:
            continue
            
        for r in rays:
            pos = r["pos"]
            vel = r["vel"]
            
            # --- FORCE OF INTENT ---
            # 1. Will Vector (5HT): Drives time forward (Down)
            drive = np.array([0.0, ops["5HT_WILL"]])
            
            # 2. Lensing Resistance (Cortisol): Curvature of Attention
            # Pulls toward the Left (Past/Anxiety)
            lensing = np.array([-ops["CORTISOL_GR"] * 0.2, 0.0])
            
            # 3. Void Attraction (5HT1A): The Desire for Zero
            dist_sq = np.sum(pos**2) + 0.1
            to_void = -pos / np.sqrt(dist_sq)
            void_pull = to_void * (ops["5HT1A_SINK"] / dist_sq) * 5.0
            
            # 4. Expansion vs Contraction (Vaso/Oxy)
            # Lateral breathing of the field
            breath = math.sin(t + r["phase"])
            expansion = np.array([breath * (ops["VASO_V1AR"] - ops["OXY_OTR"]) * 0.1, 0.0])
            
            # --- THE SPARK (138.88 DEGREE TWIST) ---
            # When tension hits limit, SCM rotates the head (Phase Shift)
            total_force = drive + lensing + void_pull + expansion
            
            # Integrate (Apply Will)
            vel = vel * (1.0 - ops["GABA_B"] * 0.05) + total_force * dt
            
            # Check Spark Condition
            speed = np.linalg.norm(vel)
            if speed > 0.1:
                curr_angle = math.atan2(vel[1], vel[0])
                # Trigger: Periodic reset of the Gaze
                if t_step % 25 == 0 and ops["GABA_A"] > 0.8:
                    # The 138.88 Twist
                    twist = SPARK_RAD * (1 if r["id"] % 2 == 0 else -1)
                    new_angle = curr_angle + twist
                    vel[0] = speed * math.cos(new_angle)
                    vel[1] = speed * math.sin(new_angle)
            
            pos += vel * dt
            
            # Boundary (Facial Limits)
            if pos[0] < -2: pos[0] = -1.9
            if pos[0] > 18: pos[0] = 17.9
            
            r["pos"] = pos
            r["vel"] = vel
            r["path"].append(pos.copy())

    # --- 4. RENDER: THE LIVING FIELD ---
    for r in rays:
        path = np.array(r["path"])
        if len(path) > 1:
            # Color by Phase (Thought Spectrum)
            c = plt.cm.twilight(r["id"] / num_rays)
            ax.plot(path[:,0], path[:,1], color=c, alpha=0.5, lw=0.8)
            
    ax.set_axis_off()
    ax.set_title("V13 THE OBSERVER'S WILL: 128 RAYS OF ATTENTION\n(Anchor: PLP Core | Driver: 10 Bio-Valves | Spark: 138.88°)", color='white', fontsize=18)
    
    output_fn = "V13_OBSERVER_WILL.png"
    plt.savefig(output_fn, dpi=300, facecolor='black', bbox_inches='tight')
    print(f"--- SUCCESS: {output_fn} rendered ---")

if __name__ == "__main__":
    render_v13_observer_will_engine()
