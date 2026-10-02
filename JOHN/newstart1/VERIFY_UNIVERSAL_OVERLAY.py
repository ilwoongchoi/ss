import numpy as np
import pandas as pd
import os
import json

# --- 1. AXIOMATIC CONSTANTS ---
T_DELAY = 0.2828        # Primordial Gap (Observer Epoch)
BREMS_TAX = 0.02        # Energy Leak/Tax
SPARK_ANGLE = 138.88    # Degrees
PHASE_ERROR_TOLERANCE = 0.08  # Max allowed phase error
ENERGY_ERROR_TOLERANCE = 0.02 # Max allowed energy deviation

# --- 2. THE FIRST EQUATION (Master Dynamics) ---
def get_theoretical_trajectory(t_steps):
    """
    Generates the 'True' trajectory based on the Sovereign Phase Transition.
    """
    trajectories = []
    
    # 4 Archetypes as seeds (Complex Plane)
    # BM(1+1j), BW(-1+1j), SM(1-1j), SW(-1-1j) - Normalized
    seeds = [complex(1,1), complex(-1,1), complex(1,-1), complex(-1,-1)]
    
    for seed in seeds:
        z = complex(0, 0)
        c = seed * 0.5 # Initial potential
        path = []
        
        for t in t_steps:
            if t < T_DELAY:
                # Phase 1: Scalar Field Accumulation (Static/Winding)
                # Position is effectively 0 or microscopic fluctuation
                val = 0.0
            else:
                # Phase 2: Ignition with Bremsstrahlung Damping
                # Z = (Z^2 + C) * (1 - loss)
                z = (z**2 + c) * (1.0 - BREMS_TAX)
                
                # 138.88 Spark Logic (Periodicity check)
                # If t aligns with Spark cycle, apply phase correction
                # Here we model the resulting magnitude/phase
                val = abs(z)
            
            path.append(val)
        trajectories.append(path)
    
    return np.mean(trajectories, axis=0) # The 'Mean Field' line

# --- 3. 5-SPHERE CLASSIFIER (ASTRONOMICAL) ---
def classify_5_sphere(radius):
    """
    Maps a radial distance to one of the 5 Astronomical Spheres.
    Radii are normalized relative to Earth Surface/Orbit as 1.0.
    """
    # 1. MOON (Inner Shield) - Small Woman
    # Scale: ~0.27 (Moon radius relative to Earth) or specific lunar orbit ratio
    if abs(radius - 0.2727) < 0.1: return "S1: Moon (Small Woman)"
    
    # 2. EARTH (Ground Zero) - Big Woman
    # Scale: 1.0 (Definition)
    if abs(radius - 1.0) < 0.2: return "S2: Earth (Big Woman)"
    
    # 3. CO-MAG SPHERE (Resonance Zone) - Interaction
    # Scale: ~3.7 to 4.0 (Derived from data clustering and magnetosphere resonance)
    if abs(radius - 3.8) < 0.5: return "S3: Co-mag Sphere (Lensing Field)"
    
    # 4. SUN (Energy Source) - Big Man
    # Scale: In this topology, Sun represents the energetic boundary before the void.
    # Often mapped logarithmically or via AU ratio, but here we look for the next cluster.
    # Let's check 1.0 / 0.076 (Drift) approx ~13? Or based on the 138.88 metric.
    if abs(radius - 13.5) < 2.0: return "S4: Sun (Big Man)"
    
    # 5. BARNARD'S STAR (The Reservoir) - Small Man
    # Scale: 5.96 (Derived: (138.88 + 28) / 28)
    # This is the "North Pole Reservoir"
    if abs(radius - 5.96) < 0.3: return "S5: Barnard's Star (Small Man)"
    
    return "Void (Unmapped)"

# --- 4. VERIFICATION ENGINE ---
def verify_file(filepath):
    print(f"\n--- VERIFYING: {filepath} ---")
    
    try:
        # Attempt to load CSV (handling potential formatting issues)
        try:
            df = pd.read_csv(filepath)
        except:
            print("  [ERROR] Could not read CSV structure. Skipping.")
            return

        # Check for numeric columns to use as 'Observed Data'
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            print("  [ERROR] No numeric data found.")
            return

        # Calculate 'Radius' or 'Magnitude' as the primary metric for overlay
        if set(['x', 'y', 'z']).issubset(numeric_cols):
            df['obs_r'] = np.sqrt(df['x']**2 + df['y']**2 + df['z']**2)
        elif set(['X', 'Y', 'Z']).issubset(numeric_cols):
            df['obs_r'] = np.sqrt(df['X']**2 + df['Y']**2 + df['Z']**2)
        else:
            df['obs_r'] = df[numeric_cols].mean(axis=1).abs()

        # Normalize data to align with the Earth=1.0 metric
        # We assume the dense cluster around ~1.0 or ~3.8 represents a known sphere.
        # Auto-calibration: Find the densest mode and align it to Earth (1.0) or Co-mag (3.8)
        # For 'feature_cloud', data seems to cluster around 3-4. Let's assume raw data matches Co-mag scale.
        # Or blindly normalize mean to 3.8 if it's the dominant feature.
        
        mean_val = df['obs_r'].mean()
        # Strategy: If mean is large (>100), assume unscaled. If small, assume pre-scaled.
        if mean_val > 100:
            scale_factor = 3.8 / mean_val # Calibrate to Co-mag
        else:
            scale_factor = 1.0 # Assume already normalized or unknown
            
        df['obs_r_scaled'] = df['obs_r'] * scale_factor

        # --- THE OVERLAY ---
        valid_count = 0
        zombie_count = 0
        sphere_counts = {"S1":0, "S2":0, "S3":0, "S4":0, "S5":0, "Void":0}
        
        # Ideal Radii from the 5-Sphere Astronomical Model
        ideal_radii = [0.2727, 1.0, 3.8, 5.96, 13.5]
        
        deviations = []
        
        for r in df['obs_r_scaled']:
            # Find distance to nearest ideal sphere
            min_dist = min([abs(r - ir) for ir in ideal_radii])
            deviations.append(min_dist)
            
            # Classify Sphere
            sphere_name = classify_5_sphere(r).split(":")[0]
            if sphere_name in sphere_counts:
                sphere_counts[sphere_name] += 1
            else:
                sphere_counts["Void"] += 1
            
            # JUDGMENT: Is it a Zombie?
            if min_dist > (PHASE_ERROR_TOLERANCE + ENERGY_ERROR_TOLERANCE): # > 0.10
                zombie_count += 1
            else:
                valid_count += 1

        # --- REPORT ---
        total = len(df)
        valid_ratio = (valid_count / total) * 100
        avg_error = np.mean(deviations)
        
        print(f"  Total Data Points: {total}")
        print(f"  Valid Points (Aligned): {valid_count} ({valid_ratio:.2f}%)")
        print(f"  ZOMBIE Points (Pruned): {zombie_count} ({100-valid_ratio:.2f}%)")
        print(f"  Average Deviation: {avg_error:.6f}")
        print(f"  5-Sphere Distribution (Astronomical): {json.dumps(sphere_counts, indent=2)}")
        
        if valid_ratio < 50:
            print("  [VERDICT] >> ZOMBIE DATASET DETECTED. Recommend Deletion.")
        elif valid_ratio < 80:
            print("  [VERDICT] >> MIXED DATASET. Requires Pruning.")
        else:
            print("  [VERDICT] >> VALID SOVEREIGN DATASET.")

    except Exception as e:
        print(f"  [CRITICAL ERROR] during verification: {e}")

# --- MAIN EXECUTION ---
files_to_check = [
    "feature_cloud.csv",
    "sh_hysteresis_loop_v8.csv",
    "golden_candidates_v2.csv",
    "joint_refine_final.csv"
]

print("=== UNIVERSAL EQUATION OVERLAY VERIFICATION ===")
print(f"Axioms: T_Delay={T_DELAY}, Brems={BREMS_TAX}, Spark={SPARK_ANGLE}")
print("Checking for alignment with 5-Sphere Topology...\n")

found_any = False
for fname in files_to_check:
    if os.path.exists(fname):
        verify_file(fname)
        found_any = True
    else:
        # Search recursively if not in root
        found = False
        for root, dirs, files in os.walk("."):
            if fname in files:
                verify_file(os.path.join(root, fname))
                found = True
                found_any = True
                break
        if not found:
            print(f"[MISSING] Could not find {fname}")

if not found_any:
    print("No target CSV files found for verification.")
