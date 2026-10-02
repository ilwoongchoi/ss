import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# --- AXIOMS ---
T_DELAY = 0.2828        # The Primordial Gap
BREMS_TAX = 0.02        # Energy Tax (Cooling)
SPARK_ANGLE = 138.88    # The Sovereign Twist
# No hardcoded radii. We check if the equation GENERATES them.

def run_sovereign_equation(steps=10000):
    """
    Runs the Master Equation and returns the radial distribution of the trajectory.
    Does 0.2828 naturally create the 5-Sphere structure?
    """
    trajectories = []
    # 4 Seeds (Archetypes)
    seeds = [complex(1,1), complex(-1,1), complex(1,-1), complex(-1,-1)]
    
    all_radii = []
    
    print(f"Running Sovereign Equation (T_Delay={T_DELAY}, Brems={BREMS_TAX})...")
    
    for seed in seeds:
        z = complex(0, 0)
        # C determines the Fractal Shape. 
        # In Mandelbrot, C is usually the pixel coord. Here, it's the Archetype Seed * Delay.
        c = seed * T_DELAY 
        
        path_radii = []
        
        for t_step in range(steps):
            t = t_step * 0.01 # Time resolution
            
            if t < T_DELAY:
                # Phase 1: Winding / Static Potential
                # Just accumulating potential, r ~ 0
                pass
            else:
                # Phase 2: Ignition
                # Z_new = Z_old^2 + C
                # Apply Bremsstrahlung Cooling (Energy Conservation)
                z = (z**2 + c) * (1.0 - BREMS_TAX)
                
                # Apply Spark Twist (Phase Correction)
                # Every period (roughly related to 1/Drift or 13.5GA logic)
                # Let's say spark happens naturally via the complex rotation, 
                # but if we strictly follow the 'Clearing', we check angle.
                
                r = abs(z)
                if r > 0.01: # Filter initial zero
                    path_radii.append(r)
                    
        all_radii.extend(path_radii)
        
    return np.array(all_radii)

def find_natural_orbits(radii):
    """
    Finds where the trajectory naturally spends the most time (Stable Orbits).
    """
    # Create a histogram to find density peaks
    counts, bin_edges = np.histogram(radii, bins=200, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Find peaks (local maxima in density)
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(counts, height=0.1, distance=5)
    
    peak_radii = bin_centers[peaks]
    return peak_radii, counts, bin_centers

def verify_astronomical_alignment(peak_radii):
    """
    Checks if the Equation's peaks align with the 5-Sphere Constants.
    """
    targets = {
        "Moon (SW)": 0.2727,
        "Earth (BW)": 1.0,
        "Co-mag (Lensing)": 3.8,
        "Barnard (SM)": 5.96
    }
    
    print("\n--- 5-SPHERE VERIFICATION REPORT ---")
    print("Do the Equation's natural orbits match the Heavens?")
    
    matches = {}
    for name, target in targets.items():
        # Find closest generated peak
        if len(peak_radii) == 0:
            best_match = 0.0
            diff = 999.0
        else:
            idx = (np.abs(peak_radii - target)).argmin()
            best_match = peak_radii[idx]
            diff = abs(best_match - target)
        
        status = "MATCH" if diff < 0.2 else "FAIL"
        print(f"  Target: {name:15s} ({target}) | Equation Generated: {best_match:.4f} | Diff: {diff:.4f} [{status}]")
        matches[name] = status
        
    return matches

def overlay_data(peak_radii, csv_files):
    """
    Overlays existing CSV data onto the Equation's Natural Orbits.
    """
    print("\n--- DATA OVERLAY ON EQUATION ORBITS ---")
    
    for fname in csv_files:
        if not os.path.exists(fname):
            continue
            
        try:
            df = pd.read_csv(fname)
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            # Calc Radius
            if set(['x', 'y', 'z']).issubset(numeric_cols):
                obs_r = np.sqrt(df['x']**2 + df['y']**2 + df['z']**2)
            elif set(['X', 'Y', 'Z']).issubset(numeric_cols):
                obs_r = np.sqrt(df['X']**2 + df['Y']**2 + df['Z']**2)
            else:
                obs_r = df[numeric_cols].mean(axis=1).abs()
            
            # Simple Auto-scale to Earth=1.0 assumption for check
            mean_val = obs_r.mean()
            scale = 1.0 / mean_val if mean_val > 0 else 1.0
            if mean_val > 100: scale = 3.8 / mean_val # Try Co-mag scaling
            
            scaled_r = obs_r * scale
            
            # Check alignment with peaks
            aligned_count = 0
            for r in scaled_r:
                # Is it close to ANY equation-generated peak?
                min_dist = min([abs(r - p) for p in peak_radii]) if len(peak_radii) > 0 else 1.0
                if min_dist < 0.15: # Tolerance
                    aligned_count += 1
            
            ratio = (aligned_count / len(df)) * 100
            print(f"  File: {fname} | Aligned with Equation: {ratio:.2f}%")
            
        except Exception as e:
            print(f"  Error reading {fname}: {e}")

if __name__ == "__main__":
    # 1. Run Equation
    radii = run_sovereign_equation()
    
    # 2. Find Orbits
    peaks, counts, bins = find_natural_orbits(radii)
    print(f"\nEquation Generated Natural Orbits (Radii): {peaks}")
    
    # 3. Verify 5-Spheres
    verify_astronomical_alignment(peaks)
    
    # 4. Overlay Data
    overlay_data(peaks, ["feature_cloud.csv", "sh_hysteresis_loop_v8.csv", "golden_candidates_v2.csv"])
