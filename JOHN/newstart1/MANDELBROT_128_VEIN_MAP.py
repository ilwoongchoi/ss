
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# 1. CANONICAL CONSTANTS
try:
    from absolute_constants import C, OMEGA, SPARK_ANGLE_RAD, NEUTRON_TIME_SYNC
except ImportError:
    C = float(np.sqrt(2.0) / 5.0) # 0.2828
    OMEGA = 7.4
    SPARK_ANGLE_RAD = np.deg2rad(138.88)
    NEUTRON_TIME_SYNC = 0.3857

EPSILON0 = (C**2) / 128.0 # Neutrino base leak
UNIT_PHASE = SPARK_ANGLE_RAD / 128.0 # 1/128 precision step

# 2. THE 128 ARCHETYPE VEIN MAPPING
def generate_128_veins():
    """
    Maps 128 integers to complex veins based on the 7+1=8 identity.
    n=1: Neutrino (Leak)
    n=7: Gluon (Source/Confinement)
    n=8: Photon (Spark)
    """
    archetypes = []
    for n in range(1, 129):
        # Number-theoretic phase
        phase = n * UNIT_PHASE
        
        # Magnitude logic: Folded towards C=0.2828
        # External points (OMEGA) folded into pockets
        mag = C + (OMEGA - C) * (1.0 - np.tanh(n / 64.0))
        
        z_n = mag * (np.cos(phase) + 1j * np.sin(phase))
        
        # Identity identification
        label = "generic"
        if n == 1: label = "neutrino"
        elif n == 7: label = "gluon_source"
        elif n == 8: label = "photon_spark"
        elif n == 128: label = "closure_omega"
        
        archetypes.append({
            "n": n,
            "z_real": float(z_n.real),
            "z_imag": float(z_n.imag),
            "phase_deg": float(np.rad2deg(phase)),
            "label": label
        })
    return archetypes

def calculate_tunneling_passwords(archetypes):
    """
    Reverse-calculates the 24-channel 'password' for each archetype's tunneling.
    u24 is derived from the complex residue of the 128-vein mapping.
    """
    passwords = {}
    for arch in archetypes:
        n = arch["n"]
        z = complex(arch["z_real"], arch["z_imag"])
        
        # The 'Password' is a 24-bit representation of the complex coordinates
        # mapped through the 0.2828 metric
        u24 = np.zeros(24)
        
        # Fractal decomposition of the coordinates into 24 bins
        seed = int(abs(z) * 1e6) + n
        np.random.seed(seed)
        u24 = np.random.dirichlet(np.ones(24), size=1)[0] # Normalized energy distribution
        
        # Inject the 7+1=8 constraint into the password
        if n == 8: # Photon Spark
            u24[3] = 0.8  # Force-fire Node 3 (Photon sector)
        elif n == 7: # Gluon Confinement
            u24[4] = 0.8  # Force-fire Node 4 (Gluon sector)
        elif n == 1: # Neutrino Leak
            u24[2] = 0.8  # Force-fire Node 2 (Neutrino sector)
            
        passwords[f"type_{n}"] = {
            "label": arch["label"],
            "u24_vector": u24.tolist(),
            "tunnel_intensity": float(np.tanh(n/128.0))
        }
    return passwords

# 3. VISUALIZATION: THE FOLDED POCKETS
def plot_128_veins(archetypes):
    plt.figure(figsize=(12, 12))
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    
    # Draw Confinement Circle (0.2828)
    circle = plt.Circle((0, 0), C, color='red', fill=False, linestyle='--', label='Confinement (0.2828)')
    plt.gca().add_patch(circle)
    
    # Draw Observer Horizon (1.9860)
    obs_circle = plt.Circle((0, 0), 1.9860, color='blue', fill=False, linestyle=':', label='Observer (1.9860)')
    plt.gca().add_patch(obs_circle)

    # Plot Veins
    x = [a["z_real"] for a in archetypes]
    y = [a["z_imag"] for a in archetypes]
    plt.scatter(x, y, c=range(1, 129), cmap='viridis', s=20, alpha=0.6)
    
    # Highlight Identity Nodes
    for a in archetypes:
        if a["label"] != "generic":
            plt.annotate(a["label"], (a["z_real"], a["z_imag"]), fontsize=9, fontweight='bold')
            plt.scatter([a["z_real"]], [a["z_imag"]], color='red', s=50, edgecolors='black')

    # Draw the Diagonal PLP Tunneling Line (Conceptual)
    plt.plot([0, 1.5], [0, 1.5 * np.tan(SPARK_ANGLE_RAD)], color='orange', lw=2, label='Diagonal PLP Spark Line')

    plt.title("128 Archetype Vein Map: The 정수론의 끝 (End of Number Theory)")
    plt.xlabel("Real (Structure)")
    plt.ylabel("Imaginary (Spark/Phase)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("analysis_results/veins_128_grid.png")
    plt.close()

# 4. MAIN
def main():
    os.makedirs("analysis_results", exist_ok=True)
    
    print("Generating 128 Archetype Vein Mapping...")
    archetypes = generate_128_veins()
    
    print("Calculating 24-Channel Tunneling Passwords...")
    passwords = calculate_tunneling_passwords(archetypes)
    
    # Save Data
    with open("analysis_results/archetype_tunneling_passwords.json", "w") as f:
        json.dump(passwords, f, indent=2)
        
    # Generate Visual
    plot_128_veins(archetypes)
    
    print("\n[정수론의 끝] 128 그리드 유도 완료.")
    print(f" - Neutrino (n=1)  -> Phase: {archetypes[0]['phase_deg']:.4f}°")
    print(f" - Gluon (n=7)     -> Phase: {archetypes[6]['phase_deg']:.4f}°")
    print(f" - Photon (n=8)    -> Phase: {archetypes[7]['phase_deg']:.4f}°")
    print(f" - Total Archetypes: 128")
    print(" - Results saved to 'analysis_results/' directory.")

if __name__ == "__main__":
    main()
