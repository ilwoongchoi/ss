
import numpy as np
import pandas as pd
import math
import sys

def verify_sh_structures():
    print("=== SH Structure Verification (Band Extent Analysis) ===")
    
    # Load Data
    csv_path = r"d:\Users\user\Documents\newstart\ATLAS_V2.2_RELEASE\sh_boundary_scores.csv"
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: CSV not found at {csv_path}")
        sys.exit(1)
        
    print(f"Loaded {len(df)} rows from sh_boundary_scores.csv")
    
    # 1. Find Peak (Global Maximum)
    peak_idx = df['boundary_score'].argmax()
    peak_row = df.iloc[peak_idx]
    peak_r = peak_row['r']
    peak_score = peak_row['boundary_score']
    peak_q0 = peak_row['q0']
    
    print(f"\n[Discrete Peak]")
    print(f"  r*: {peak_r:.8f}")
    print(f"  q0*: {peak_q0}")
    print(f"  Score: {peak_score:.10f}")
    
    # 2. Check Peak Quantization (sqrt(16/5))
    target_peak = math.sqrt(16.0/5.0)
    peak_diff = abs(peak_score - target_peak)
    
    print(f"\n[Peak Quantization Check]")
    print(f"  Target sqrt(16/5): {target_peak:.10f}")
    print(f"  Difference: {peak_diff:.10e}")
    if peak_diff < 1e-3:
        print("  -> MATCHES sqrt(16/5) within 1e-3 (Candidate Locked)")
    else:
        print("  -> DOES NOT MATCH (Check scaling or definition)")

    # 3. FWHM Analysis (Band Extent)
    # The document implies the FWHM band is the range of r where score > half_max
    # across the relevant q0 slice (or global).
    half_max = peak_score / 2.0
    print(f"\n[FWHM Analysis - Band Extent]")
    print(f"  Half-Max Threshold: {half_max:.10f}")
    
    # Filter points above half-max
    high_score_df = df[df['boundary_score'] >= half_max]
    
    if len(high_score_df) == 0:
        print("  No points found above half-max (excluding peak).")
        return

    # Find min and max r in this set
    r_L = high_score_df['r'].min()
    r_R = high_score_df['r'].max()
    
    print(f"  Range of r with Score >= Half-Max:")
    print(f"  r_min (Left Edge): {r_L:.8f}")
    print(f"  r_max (Right Edge): {r_R:.8f}")
    
    w_L = peak_r - r_L
    w_R = r_R - peak_r
    
    print(f"  w_L (peak - r_min): {w_L:.8f}")
    print(f"  w_R (r_max - peak): {w_R:.8f}")
        
    # 4. Skew Ratio
    if w_L > 0 and w_R > 0:
        skew_ratio = w_R / w_L
        print(f"\n[Skew Ratio]")
        print(f"  w_R / w_L = {skew_ratio:.10f}")
        
        target_skew = 7.0
        skew_diff = abs(skew_ratio - target_skew)
        print(f"  Difference from 7.0: {skew_diff:.10e}")
        
        if skew_diff < 0.1:
            print("  -> MATCHES 1:7 Skew (Candidate Locked)")
        else:
            print("  -> DOES NOT MATCH 7.0 (Check data density)")
            
        # 5. Generate Constants Block
        print("\n=== GENERATED CONSTANTS BLOCK (for absolute_constants.py) ===")
        print(f"# --- SH transition derived (from ATLAS V2.2 sh_boundary_scores.csv) ---")
        print(f"SH_R_STAR = {peak_r:.8f}")
        print(f"SH_Q0_STAR = {peak_q0}")
        print(f"SH_BOUNDARY_PEAK = {peak_score:.16f}")
        print(f"")
        print(f"SH_R_FWHM_L = {w_L:.10f}")
        print(f"SH_R_FWHM_R = {w_R:.10f}")
        print(f"SH_SKEW_RATIO_OBSERVED = {skew_ratio:.10f}  # SH_R_FWHM_R / SH_R_FWHM_L")
        print(f"SH_SKEW_RATIO_NEAREST_INT = {round(skew_ratio)}")
        print(f"SH_SKEW_RATIO_LOCK_ERR = {abs(skew_ratio - round(skew_ratio)):.10e}")
        print(f"")
        print(f"# peak quantization candidate")
        print(f"import math")
        print(f"SH_PEAK_QUANT_CANDIDATE = math.sqrt(16/5)")
        print(f"SH_PEAK_QUANT_ERR = abs(SH_BOUNDARY_PEAK - SH_PEAK_QUANT_CANDIDATE)")
        print(f"SH_SKEW_DRIVER_CANDIDATE = SH_SKEW_RATIO_NEAREST_INT - 1  # 6 (interpretation)")
    else:
        print("  Invalid widths (zero or negative). Data not surrounding peak?")

if __name__ == "__main__":
    verify_sh_structures()
