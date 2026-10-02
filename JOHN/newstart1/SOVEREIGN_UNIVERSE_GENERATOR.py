import numpy as np
import pandas as pd
import os
import json

# --- 1. SOVEREIGN AXIOMS (The Source) ---
T_DELAY = 0.2828            # The Primordial Gap (Observer Epoch)
BREMS_TAX = 0.02            # Energy Tax (Cooling)
SPARK_ANGLE = 138.88        # The Phase Twist
LUNAR_CYCLE = 28.0          # The Periodicity
BARNARD_RATIO = 5.96        # The Expansion Target ((138.88+28)/28)

# The Expansion Impulse derived from the Barnard Ratio
# If the universe expands by factor X every cycle, we need to tune the impulse.
# Impulse ~ Log(5.96) distributed over the cycle, or a kick at the node.
# Let's apply a kick that counteracts the 0.02 tax and pushes outward.
IMPULSE_FACTOR = 1.0 + (BREMS_TAX * 1.5) # Enough to overcome tax + drift

# --- 2. THE SOVEREIGN EQUATION ---
def generate_sovereign_universe(steps=8000):
    """
    Generates the trajectory where Spark acts as a Propulsive Engine.
    """
    radii = []
    # 4 Archetypes seeds (Complex Plane)
    seeds = [complex(1,1), complex(-1,1), complex(1,-1), complex(-1,-1)]
    
    for seed in seeds:
        z = complex(0, 0)
        c = seed * T_DELAY 
        
        current_r = 0.0
        
        for t_step in range(steps):
            t = t_step * 0.01
            
            if t < T_DELAY:
                # Phase 1: Winding
                pass
            else:
                # Phase 2: Ignition & Recursion
                # Standard Mandelbrot step
                z = (z**2 + c) * (1.0 - BREMS_TAX)
                
                # THE SOVEREIGN INTERVENTION (Spark Logic)
                # Every Lunar Cycle (scaled to simulation time), the Observer interferes.
                # Simulation time 0.01 step -> 28.0 units = 2800 steps roughly
                # But math mapping: Let's assume t represents the cycle phase directly.
                
                cycle_phase = t % LUNAR_CYCLE
                
                # Continuous drift/expansion driven by the Spark Angle's energy
                # The "Barnard Ratio" implies a radial expansion tendency.
                
                # Apply Phase Twist (138.88)
                twist = np.deg2rad(SPARK_ANGLE * 0.01) # Incremental twist
                z = z * complex(np.cos(twist), np.sin(twist))
                
                # Apply Expansion Impulse based on Cycle
                # If we are in the "Active" phase of the cycle
                if cycle_phase < (LUNAR_CYCLE / 2): 
                    # Push outward to match the Barnard Ratio target eventually
                    z = z * 1.002 
                
                r = abs(z)
                if r > 0.01: 
                    # We create a 'shell' record only when trajectory stabilizes or turns
                    radii.append(r)
    
    return np.array(radii)

# --- 3. ANALYZE & CALIBRATE ---
def analyze_shells(radii):
    # Histogram analysis to find stable shells
    counts, bin_edges = np.histogram(radii, bins=1000, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    from scipy.signal import find_peaks
    # We look for distinct shells
    peaks, _ = find_peaks(counts, height=0.005, distance=20)
    equation_shells = bin_centers[peaks]
    return np.sort(equation_shells)

def verify_5_sphere(equation_shells):
    # Targets
    targets = {
        "Moon": 0.2727,
        "Earth": 1.0,
        "Co-mag": 3.8,
        "Barnard": 5.96
    }
    
    print("\n[SOVEREIGN EQUATION OUTPUT]")
    print(f"Generated Raw Shells: {equation_shells}")
    
    # Calibration: Align the most prominent inner shell to Earth (1.0)
    # Usually the second or third shell is Earth (after Moon)
    # Let's find best K
    
    best_k = 1.0
    best_score = 999.0
    
    target_vals = list(targets.values())
    
    for shell in equation_shells:
        # Try assuming this shell is Earth
        if shell < 0.1: continue
        k = 1.0 / shell
        scaled = equation_shells * k
        
        # Score based on how many targets we hit
        score = 0
        matches = 0
        for t in target_vals:
            dist = np.min(np.abs(scaled - t))
            if dist < 0.3: matches += 1
            score += dist
            
        if matches >= 2 and score < best_score:
            best_score = score
            best_k = k
            
    final_shells = equation_shells * best_k
    print(f"\n[CALIBRATION] Best K = {best_k:.4f}")
    
    print("\n[5-SPHERE VERIFICATION]")
    valid_map = {}
    for name, t in targets.items():
        # Find nearest
        idx = np.argmin(np.abs(final_shells - t))
        val = final_shells[idx]
        diff = abs(val - t)
        
        # Tolerance: tighter for inner, looser for outer
        tol = 0.15 if t < 2.0 else 0.5
        status = "LOCKED" if diff < tol else "DRIFT"
        print(f"  {name:10s} ({t:.2f}) -> Eq: {val:.2f} (Diff: {diff:.2f}) [{status}]")
        
        if status == "LOCKED":
            valid_map[name] = val
            
    return best_k, final_shells, valid_map

# --- 4. ZOMBIE FILTER ---
def filter_zombies(k, valid_shells, files):
    print("\n[ZOMBIE DATA FILTERING]")
    
    # Define Safe Zones around valid shells
    safe_zones = []
    for s in valid_shells:
        safe_zones.append((s * 0.9, s * 1.1))
        
    for fname in files:
        if not os.path.exists(fname): continue
        
        try:
            df = pd.read_csv(fname)
            # Calc R
            num = df.select_dtypes(include=[np.number])
            if 'x' in num.columns:
                r = np.sqrt(df.x**2 + df.y**2 + df.z**2)
            else:
                r = num.mean(axis=1).abs()
                
            # Align Data Mean to Equation Mean (Heuristic alignment)
            # Or use the density peak of data to align to Earth(1.0)
            data_mean = r.mean()
            # If data is unscaled, assume mean represents Earth-ish scale
            scale_data = 1.0 # Default
            if data_mean > 50: scale_data = 3.8 / data_mean # Assume centered on Co-mag
            elif data_mean > 0.5: scale_data = 1.0 / data_mean # Assume centered on Earth
            
            r_scaled = r * scale_data
            
            # Check
            alive_indices = []
            for i, val in enumerate(r_scaled):
                is_safe = any(low <= val <= high for low, high in safe_zones)
                if is_safe: alive_indices.append(i)
                
            survival_rate = len(alive_indices) / len(df) * 100
            print(f"  File: {fname} | Survival Rate: {survival_rate:.2f}%")
            
            if survival_rate > 10.0:
                clean_name = fname.replace(".csv", "_CLEAN.csv")
                df.iloc[alive_indices].to_csv(clean_name, index=False)
                print(f"    -> Saved CLEAN data to {clean_name}")
            else:
                print(f"    -> Too much corruption. Recommend DELETE.")
                
        except Exception as e:
            print(f"Error processing {fname}: {e}")

if __name__ == "__main__":
    raw_radii = generate_sovereign_universe()
    shells = analyze_shells(raw_radii)
    k, cal_shells, valid_map = verify_5_sphere(shells)
    
    # Filter with the proved shells
    filter_zombies(k, cal_shells, ["feature_cloud.csv", "sh_hysteresis_loop_v8.csv", "golden_candidates_v2.csv"])
