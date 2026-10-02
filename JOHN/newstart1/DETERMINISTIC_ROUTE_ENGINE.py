
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def run_deterministic_engine():
    print("--- INITIATING DETERMINISTIC ROUTE ENGINE ---")
    
    # 1. HARDWARE NODE COORDINATES (Relative to Center 8,8)
    # Mapping from user's absolute coordinates to 16x16 grid
    nodes = {
        "ALPHA2_R": {"pos": [8 + 2.1, 1.3], "color": "#00FFFF", "label": "Alpha2 (R) Impedance"},
        "ALPHA2_L": {"pos": [8 - 2.1, 1.3], "color": "#00FFFF", "label": "Alpha2 (L) Impedance"},
        "FRONTALIS_R_EDGE": {"pos": [8 + 4.8, 2.9], "color": "#FF0000", "label": "Frontalis (R) Edge"},
        "FRONTALIS_L_EDGE": {"pos": [8 - 4.8, 2.9], "color": "#FF0000", "label": "Frontalis (L) Edge"},
        "TEMPORALIS_L": {"pos": [8 - 2.5, 6.5], "color": "#FF00FF", "label": "Left Temporalis (5HT1A)"},
        "OCCIPITALIS_R_EDGE": {"pos": [8 + 4.0, 5.7], "color": "#00FF00", "label": "Occipitalis (R) Edge"},
        "OCCIPITALIS_L_EDGE": {"pos": [8 - 1.9, 5.7], "color": "#00FF00", "label": "Occipitalis (L) Edge"}
    }
    
    # 2. DETERMINISTIC ROUTE (The Fixed Path)
    # The charge must flow through these points in a specific order
    route = [
        "ALPHA2_L", "FRONTALIS_L_EDGE", "TEMPORALIS_L", "OCCIPITALIS_L_EDGE",
        "OCCIPITALIS_R_EDGE", "FRONTALIS_R_EDGE", "ALPHA2_R"
    ]
    
    # 3. VISUALIZATION
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='#050510')
    ax.set_facecolor('#050510')
    
    # Draw Background Grid
    for i in range(17):
        ax.axhline(i, color='#111122', lw=0.5)
        ax.axvline(i, color='#111122', lw=0.5)
    
    # Draw The Route
    path_coords = np.array([nodes[node]["pos"] for node in route])
    ax.plot(path_coords[:, 0], path_coords[:, 1], color='#FFFFFF', lw=3, alpha=0.3, ls='--')
    
    # Draw Nodes and "Shiver" Resonance
    for name, data in nodes.items():
        pos = data["pos"]
        # Core node
        ax.scatter(pos[0], pos[1], color=data["color"], s=200, zorder=5, edgecolors='white', lw=2)
        
        # Resonance Halo (The lost 'shiver' simulation)
        for r in [0.3, 0.6, 0.9]:
            circle = plt.Circle((pos[0], pos[1]), r, color=data["color"], fill=False, alpha=0.2 / r, lw=1)
            ax.add_patch(circle)
            
        ax.text(pos[0] + 0.3, pos[1], data["label"], color='white', fontsize=9, alpha=0.8)

    # Calculate Charge Flow (Vector Field)
    # The deterministic route acts as a magnetic rail
    Y, X = np.mgrid[0:16:20j, 0:16:20j]
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    
    for i in range(len(path_coords)-1):
        p1 = path_coords[i]
        p2 = path_coords[i+1]
        mid = (p1 + p2) / 2
        direction = p2 - p1
        dist = np.linalg.norm(direction)
        if dist > 0:
            direction /= dist
            # Add influence to nearby points
            mask = np.sqrt((X-mid[0])**2 + (Y-mid[1])**2) < 3.0
            U[mask] += direction[0]
            V[mask] += direction[1]

    ax.streamplot(X, Y, U, V, color='#444466', alpha=0.4, density=1.5)

    ax.set_xlim(0, 16)
    ax.set_ylim(16, 0) # Top to Bottom
    ax.set_aspect('equal')
    
    plt.title("DETERMINISTIC BODY ROUTE\nHardware Skeleton: Alpha2 | Temporalis | Frontalis | Occipitalis", 
              color='white', fontsize=16, fontweight='bold', pad=20)
    
    plt.xlabel("X-Axis (Internal Impedance Map)", color='white')
    plt.ylabel("Y-Axis (Temporal Flow: Top to Bottom)", color='white')
    
    output_fn = "DETERMINISTIC_BODY_ROUTE.png"
    plt.savefig(output_fn, dpi=300, bbox_inches='tight', facecolor='#050510')
    print(f"--- SUCCESS: Deterministic Route rendered to {output_fn} ---")

if __name__ == "__main__":
    run_deterministic_engine()
