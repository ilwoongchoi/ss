import numpy as np
import matplotlib.pyplot as plt
import math

def render_v12_pure_coulomb_engine():
    # --- 1. AXIOMATIC CONSTANTS ---
    DELTA_T_OBS = 0.2828
    SPARK_ANGLE_DEG = 138.88
    SPARK_RAD = math.radians(SPARK_ANGLE_DEG)
    
    # Coulomb Constants
    K_COULOMB = 1.0  # Normalized
    Q_BASE = 1.0     # Base charge
    
    # 10-Axis Valve States (Active Operators)
    # These modulate the field parameters
    valves = {
        "VASO_EXPANSION": 1.2,   # Volume expansion
        "OXY_BINDING": 0.8,      # EM binding strength
        "GABA_A_SPARK": 1.0,     # Spark trigger sensitivity
        "GABA_B_HEAT": 0.02,     # Thermal damping
        "CORTISOL_RES": 0.5,     # Lensing resistance
        "5HT_VECTOR": 1.0,       # Will vector magnitude
        "5HT1A_SINK": 1.0,       # Sink gravity
        "D2_ENTROPY": 1.0,       # Entropy clearing rate
        "ACETYL_COA": 1.0        # Container integrity
    }

    fig, ax = plt.subplots(figsize=(16, 16), facecolor='black')
    ax.set_facecolor('black')
    
    # Coordinate System: Top-Left PLP Core is (0,0)
    # Face extends to approx (16, 16)
    ax.set_xlim(-2, 18)
    ax.set_ylim(18, -2) # Flip Y: Top is 0
    
    # Draw Anchor (PLP Core)
    ax.scatter([0], [0], color='gold', s=500, marker='*', label='PLP CORE (ZERO POINT)')
    
    # --- 2. PARTICLE INITIALIZATION (Forehead Distribution) ---
    num_particles = 128
    particles = []
    
    # Initialize particles along the forehead line (Y=0.5 approx)
    # Spread via Coulomb repulsion logic (not fixed grid)
    for i in range(num_particles):
        # Initial spread 0 to 16
        x = (i / num_particles) * 16.0 
        y = 0.5 + (np.random.normal(0, 0.1)) # Slight thermal jitter
        
        # Charge polarity (Gender/Phase)
        charge = 1 if i % 2 == 0 else -1 
        
        particles.append({
            "pos": np.array([x, y], dtype=float),
            "vel": np.array([0.0, 0.0], dtype=float),
            "path": [],
            "charge": charge,
            "id": i
        })

    # --- 3. DYNAMICS SIMULATION ---
    steps = 400
    dt = 0.05
    
    print(f"Simulating {num_particles} particles with Pure Coulomb Physics...")
    
    for t_step in range(steps):
        t = t_step * dt
        
        # Phase 1: Observation Delay
        if t < DELTA_T_OBS:
            continue
            
        for p in particles:
            pos = p["pos"]
            vel = p["vel"]
            
            # --- FORCE CALCULATION ---
            forces = np.array([0.0, 0.0])
            
            # 1. Attractor Pull (To PLP Core)
            # Modulated by 5HT1A Valve
            dist_sq = np.sum(pos**2) + 0.1
            dir_to_core = -pos / np.sqrt(dist_sq)
            forces += dir_to_core * (K_COULOMB * valves["5HT1A_SINK"] / dist_sq)
            
            # 2. 10-Axis Flow Field (The "Wind")
            # Downward flow (Gravity/Time) modulated by Cortisol Resistance
            flow_y = valves["5HT_VECTOR"] * (1.0 - valves["CORTISOL_RES"] * 0.1)
            forces += np.array([0.0, flow_y])
            
            # 3. Expansion/Binding (Vaso/Oxy)
            # Vaso pushes out, Oxy pulls in (Lateral forces)
            lateral_stress = (valves["VASO_EXPANSION"] - valves["OXY_BINDING"]) * 0.1
            forces[0] += lateral_stress * p["charge"] # Polarity dependent
            
            # --- INTEGRATION ---
            # Apply Damping (GABA-B Heat)
            vel = vel * (1.0 - valves["GABA_B_HEAT"]) + forces * dt
            pos += vel * dt
            
            # --- 138.88 SPARK CORRECTION ---
            # If velocity vector aligns with critical angle, refract
            speed = np.linalg.norm(vel)
            if speed > 0.01:
                curr_angle = math.atan2(vel[1], vel[0])
                # Check for "Gate Crossing" condition (simplified for sim)
                if t_step % 20 == 0 and valves["GABA_A_SPARK"] > 0.5:
                    new_angle = curr_angle + SPARK_RAD
                    vel[0] = speed * math.cos(new_angle)
                    vel[1] = speed * math.sin(new_angle)
            
            p["pos"] = pos
            p["vel"] = vel
            p["path"].append(pos.copy())

    # --- 4. RENDER ---
    for p in particles:
        path = np.array(p["path"])
        if len(path) > 1:
            # Color by polarity (Charge)
            c = '#00ccff' if p["charge"] > 0 else '#ff3366'
            ax.plot(path[:,0], path[:,1], color=c, alpha=0.4, lw=0.8)
            
    ax.set_axis_off()
    ax.set_title("V12 PURE PHYSICS: COULOMB TRAJECTORIES & 10-VALVE DYNAMICS\n(Anchor: PLP Core | No Grid | Fluid Mechanics)", color='white', fontsize=18)
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
    
    output_fn = "V12_PURE_PHYSICS.png"
    plt.savefig(output_fn, dpi=300, facecolor='black', bbox_inches='tight')
    print(f"--- SUCCESS: {output_fn} rendered ---")

if __name__ == "__main__":
    render_v12_pure_coulomb_engine()
