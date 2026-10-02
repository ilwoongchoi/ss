import pandas as pd
import numpy as np

def analyze_ridge(csv_path):
    df = pd.read_csv(csv_path)
    
    # Filter out zero rates if any (though ridge usually tracks max)
    df = df[df['rate_post'] > 0]
    
    if df.empty:
        print("Ridge is empty or all zeros.")
        return

    # 1. Find the Center (Peak of the ridge)
    max_idx = df['rate_post'].idxmax()
    center_row = df.loc[max_idx]
    
    q0_star = center_row['q0']
    r_star = center_row['r']
    max_rate = center_row['rate_post']
    
    print(f"Ridge Peak (Center):")
    print(f"  q0* = {q0_star:.6f}")
    print(f"  r*  = {r_star:.8f}")
    print(f"  max_rate = {max_rate:.6f}")

    # 2. Estimate Widths (Sigma L/R) along q0
    half_max = max_rate / 2.0
    
    df_sorted = df.sort_values('q0')
    qs = df_sorted['q0'].values
    rates = df_sorted['rate_post'].values
    
    # Find peak index in sorted array (may differ from max_idx due to sorting/noise)
    peak_idx = np.argmax(rates)
    q_peak = qs[peak_idx]
    
    # Left side (descending from peak to left)
    q_left = np.nan
    for i in range(peak_idx, 0, -1):
        if rates[i-1] < half_max:
            # Linear interpolation between i and i-1
            y1, y0 = rates[i], rates[i-1]
            x1, x0 = qs[i], qs[i-1]
            fraction = (half_max - y0) / (y1 - y0)
            q_left = x0 + fraction * (x1 - x0)
            break
            
    # Right side (ascending from peak to right)
    q_right = np.nan
    for i in range(peak_idx, len(rates) - 1):
        if rates[i+1] < half_max:
            # Linear interpolation between i and i+1
            y1, y0 = rates[i], rates[i+1]
            x1, x0 = qs[i], qs[i+1]
            # y0 is lower, y1 is higher (at i)
            # wait, y1 is at i (high), y0 is at i+1 (low)
            # fraction = (half_max - y0) / (y1 - y0) -> (half - low) / (high - low)
            fraction = (half_max - y0) / (y1 - y0)
            q_right = x0 + fraction * (x1 - x0) # wait, x0 is i+1, x1 is i
            # Actually easier: slope = (y0 - y1) / (x0 - x1) -> (low - high) / (right - left)
            # q_target = x1 + (half - y1) / slope
            slope = (rates[i+1] - rates[i]) / (qs[i+1] - qs[i])
            q_right = qs[i] + (half_max - rates[i]) / slope
            break
    
    sigma_L = 0.0
    sigma_R = 0.0
    
    if not np.isnan(q_left):
        sigma_L = q_peak - q_left
    else:
        # Fallback if we don't cross half-max (e.g. at boundary)
        sigma_L = q_peak - qs[0]

    if not np.isnan(q_right):
        sigma_R = q_right - q_peak
    else:
        sigma_R = qs[-1] - q_peak
        
    print(f"Widths (along q0):")
    print(f"  sigma_L = {sigma_L:.6f}")
    print(f"  sigma_R = {sigma_R:.6f}")
    print(f"  FWHM    = {sigma_L + sigma_R:.6f}")
    
    # Generate Python code snippet
    print("\n# Update for absolute_constants.py")
    print(f"CALIBRATED_SH_Q0_STAR = {q0_star:.6f}")
    print(f"CALIBRATED_SH_R_STAR = {r_star:.8f}")
    print(f"CALIBRATED_SIGMA_L = {sigma_L:.6f}")
    print(f"CALIBRATED_SIGMA_R = {sigma_R:.6f}")

if __name__ == "__main__":
    csv_path = "out/detune_closure_sweep_v4_production/refine_lam10_ridge.csv"
    analyze_ridge(csv_path)
