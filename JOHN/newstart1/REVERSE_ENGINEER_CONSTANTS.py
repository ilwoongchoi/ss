import numpy as np
from scipy.optimize import minimize

# --- TARGETS (The 5-Sphere) ---
TARGETS = np.array([0.2727, 1.0, 3.8, 5.96])
# We focus on relative ratios because absolute scale is arbitrary until calibrated.
# Ratios relative to Earth(1.0): [0.2727, 1.0, 3.8, 5.96]

# --- THE EQUATION (Parametric) ---
def simulate_equation(params):
    """
    Simulates the Sovereign Equation with tunable parameters.
    Returns the generated shells (peaks).
    """
    impulse_factor, brems_tax = params
    
    # Fixed Axioms
    T_DELAY = 0.2828
    SPARK_ANGLE = 138.88
    LUNAR_CYCLE = 28.0
    
    radii = []
    seeds = [complex(1,1)] # Use one seed for speed in optimization, topology is symmetric
    
    for seed in seeds:
        z = complex(0, 0)
        c = seed * T_DELAY 
        
        for t_step in range(4000): # Sufficient steps
            t = t_step * 0.01
            
            if t >= T_DELAY:
                # Equation
                z = (z**2 + c) * (1.0 - brems_tax)
                
                # Spark & Impulse
                cycle_phase = t % LUNAR_CYCLE
                
                # Apply Spark Twist
                twist = np.deg2rad(SPARK_ANGLE * 0.01)
                z = z * complex(np.cos(twist), np.sin(twist))
                
                # Apply Expansion Impulse
                if cycle_phase < (LUNAR_CYCLE / 2): 
                    z = z * impulse_factor
                
                r = abs(z)
                if r > 0.01: radii.append(r)
                
    # Find Peaks
    if len(radii) == 0: return np.array([0.0])
    
    counts, bin_edges = np.histogram(radii, bins=200, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(counts, height=0.005, distance=10)
    
    if len(peaks) == 0: return np.array([0.0])
    
    return np.sort(bin_centers[peaks])

# --- OBJECTIVE FUNCTION ---
def objective(params):
    """
    Calculates error between generated shells and Target Ratios.
    """
    generated_shells = simulate_equation(params)
    
    # Calibration: Find best fit K to match Earth=1.0
    # We try matching each generated shell to 1.0
    best_error = 1e9
    
    for shell in generated_shells:
        if shell < 0.1: continue
        k = 1.0 / shell # Assume this shell is Earth
        scaled = generated_shells * k
        
        # Calculate distance to nearest targets
        error = 0
        matches = 0
        for t in TARGETS:
            dist = np.min(np.abs(scaled - t))
            error += dist**2 # MSE
            if dist < 0.2 * t: matches += 1
            
        # Penalize if targets are missed
        if matches < 2: error += 100.0
        
        if error < best_error:
            best_error = error
            
    return best_error

# --- MAIN REVERSE ENGINEERING ---
if __name__ == "__main__":
    print("--- REVERSE ENGINEERING SOVEREIGN CONSTANTS ---")
    print("Targets: Moon(0.27), Earth(1.0), Co-mag(3.8), Barnard(5.96)")
    
    # Initial Guess: Impulse ~ 1.002, Tax ~ 0.02
    initial_guess = [1.002, 0.02]
    
    # Bounds: Impulse [1.0, 1.01], Tax [0.001, 0.05]
    bounds = [(1.000, 1.010), (0.001, 0.05)]
    
    print(f"Starting Optimization...")
    result = minimize(objective, initial_guess, bounds=bounds, method='Nelder-Mead')
    
    best_impulse, best_tax = result.x
    print(f"\n[FOUND OPTIMAL CONSTANTS]")
    print(f"  > IMPULSE_FACTOR: {best_impulse:.6f}")
    print(f"  > BREMS_TAX:      {best_tax:.6f}")
    
    # Verification Run
    final_shells = simulate_equation(result.x)
    print(f"\n[FINAL GENERATED SHELLS (Raw)]: {final_shells}")
    
    # Show Alignment
    print("\n[ALIGNMENT CHECK]")
    best_k = 1.0
    best_err = 1e9
    
    for shell in final_shells:
        if shell < 0.1: continue
        k = 1.0 / shell
        scaled = final_shells * k
        err = 0
        for t in TARGETS:
            err += np.min(np.abs(scaled - t))**2
        if err < best_err:
            best_k = k
            best_scaled = scaled
            
    for t in TARGETS:
        nearest = best_scaled[np.argmin(np.abs(best_scaled - t))]
        print(f"  Target {t:5.2f} : Generated {nearest:5.2f} (Diff {abs(t-nearest):.2f})")
