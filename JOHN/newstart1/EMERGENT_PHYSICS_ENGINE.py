import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# PURE PHYSICS ENGINE (NO BIOLOGICAL HARDCODING)
# ---------------------------------------------------------
# Constants derived strictly from framework physics
TUNNEL_TENSION = 1.0100375
DISCRETE_CLOSURE = 1.0000424
LATTICE_3_32 = 3.0 / 32.0
SMOOTHING_RESID = 0.00083
SPARK_LEAP = 2.5
TORSION = 0.1746

def run_pure_physics():
    # 1. 128 Unlabeled Particles (Pure mathematical seeds, no MBTI/Blood)
    num_particles = 128
    states = np.zeros((num_particles, 2)) # X, Y positions
    
    # Distribute initial points evenly across the top boundary (Y=0)
    for i in range(num_particles):
        states[i, 0] = (i / num_particles) * 16.0
        states[i, 1] = 0.0
        
    all_paths = [[] for _ in range(num_particles)]
    
    # Simulation settings
    steps = 400
    dt = 0.05
    
    # Global continuous field parameters
    center_x = 8.0
    
    for s in range(steps):
        # Time reversal based on lunar twist (1/28)
        # Using pure mathematical phase, no "sun/night" labels
        phase = (s / steps) * 28.0 * np.pi
        time_direction = -1.0 if np.cos(phase) < 0 else 1.0
        
        for i in range(num_particles):
            x, y = states[i]
            all_paths[i].append((x, y))
            
            # A. The Core Tension Field (Continuous)
            # Tension pulls outward from center based on Reality Tension
            dist_x = x - center_x
            force_x = dist_x * (TUNNEL_TENSION - 1.0)
            
            # B. The Torsion Field (Chiral Twist)
            # Creates the curving/wrapping geometry
            drift_x = -TORSION * (y - 8.0) * time_direction
            drift_y = TORSION * (x - center_x) * time_direction
            
            # C. The Flattening Operator (Melatonin Pivot)
            # Smooths the center to prevent singularity
            smoothing = np.exp(-(dist_x**2) / (SMOOTHING_RESID * 100))
            
            # D. The Sieve (3/32 Lattice Friction)
            # Downward progression is resisted by the discrete lattice
            friction_y = LATTICE_3_32 * y
            
            # Combine physics vectors
            vx = (force_x + drift_x) * (1.0 - smoothing)
            vy = 1.0 + drift_y - friction_y # Base descent + drift - friction
            
            # E. The Discharge Event (Spark)
            # If pressure exceeds discrete closure at the boundaries
            if abs(vx) > DISCRETE_CLOSURE and y > 8.0:
                angle = np.radians(138.88)
                states[i, 0] += SPARK_LEAP * np.cos(angle)
                states[i, 1] += SPARK_LEAP * np.sin(angle)
            else:
                states[i, 0] += vx * dt
                states[i, 1] += vy * dt
                
            # Boundary conditions (16x16 space)
            states[i, 0] = np.clip(states[i, 0], 0, 16)
            if states[i, 1] > 16: states[i, 1] = 16

    # ---------------------------------------------------------
    # VISUALIZATION
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 16), facecolor="#050510")
    
    # Plot using a continuous color map based on starting X position (no biological colors)
    colors = plt.cm.viridis(np.linspace(0, 1, num_particles))
    
    for i in range(num_particles):
        path = np.array(all_paths[i])
        ax.plot(path[:, 0], path[:, 1], color=colors[i], lw=1.0, alpha=0.5)
        
    ax.axvline(x=center_x, color="white", ls="--", alpha=0.2)
    ax.set_xlim(0, 16); ax.set_ylim(16, 0)
    ax.set_facecolor("#050510")
    ax.axis("off")
    
    plt.title("PURE PHYSICS MANIFOLD: Emergent Geometry (No Hardcoding)", color="white", fontsize=20)
    output_fn = "EMERGENT_PHYSICS_GRID.png"
    plt.savefig(output_fn, dpi=150, facecolor="#050510")
    print(f"Generated pure physics geometry: {output_fn}")

if __name__ == "__main__":
    run_pure_physics()
