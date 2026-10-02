"""
VERIFY_RIGHT_CORTISOL_HALF_3D.py
Analyze per-turn residuals to locate Right Cortisol (Fake 3D) signature
and identify the Calcification Phase Transition point.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from scipy.signal import find_peaks (Removed due to DLL error)

# Constants
KAPPA_2 = 1/32.0  # 0.03125 (True 3D)
KAPPA_3 = 1/64.0  # 0.015625 (Half 3D / Cartilage)
KAPPA_4 = 1/128.0 # 0.0078125 (Trabecular Bone)

def analyze_calcification():
    print("="*80)
    print("RIGHT CORTISOL (FAKE 3D) & CALCIFICATION VERIFICATION")
    print("="*80)
    
    # Load data
    try:
        df = pd.read_csv("out/refine_lam10_det_per_turn.csv")
        print(f"Loaded {len(df)} turns of ridge data.")
    except FileNotFoundError:
        print("Error: out/refine_lam10_det_per_turn.csv not found.")
        return

    # Calculate residuals
    # Assuming rate_post is the observed rate
    # We want to see if rate_post contains components of KAPPA_3
    
    # Filter for valid turns (ignore startup transient)
    valid_df = df[df['eligibleB_mean'] > 100].copy() # Ensure enough eligibility
    
    if len(valid_df) == 0:
        print("No valid turns with sufficient eligibility found.")
        return

    # Normalize rate by eligibility to get per-pixel probability
    # rate_post is likely total rate, so divide by eligibleB_mean?
    # Or is rate_post already normalized? Let's check the magnitude.
    # In previous outputs, rate_post_mean was ~0.005 to 0.04.
    # KAPPA * dt? 
    # Let's look at the raw values.
    
    print("\nData Sample (first 5 valid turns):")
    print(valid_df[['turn', 'rate_post_mean', 'eligibleB_mean']].head())
    
    # Analyze Rate vs Kappa Candidates
    # We are looking for rate_post_mean ≈ C * KAPPA
    # Or residuals.
    
    rates = valid_df['rate_post_mean'].values
    turns = valid_df['turn'].values
    
    # 1. Identify "Half-3D" Signature (KAPPA_3 = 1/64)
    # We look for turns where the rate aligns closer to KAPPA_3 scale than KAPPA_2
    
    # Simple metric: Ratio to KAPPAs
    ratio_k2 = rates / KAPPA_2
    ratio_k3 = rates / KAPPA_3
    
    print(f"\nAnalysis of Rate Scaling:")
    print(f"Mean Rate: {np.mean(rates):.6f}")
    print(f"Mean Ratio to κ₂ (1/32): {np.mean(ratio_k2):.4f}")
    print(f"Mean Ratio to κ₃ (1/64): {np.mean(ratio_k3):.4f}")
    
    # 2. Locate Right Cortisol (Small Man) Phase
    # The user identified Right Cortisol with Cartilage/Half-3D.
    # We look for a phase where the rate dips or locks to 1/64 levels.
    
    # Find local minima/maxima in rates using numpy
    rates_prev = np.roll(rates, 1)
    rates_next = np.roll(rates, -1)
    peaks_mask = (rates > rates_prev) & (rates > rates_next)
    troughs_mask = (rates < rates_prev) & (rates < rates_next)
    
    # Trim edges
    peaks_mask[0] = peaks_mask[-1] = False
    troughs_mask[0] = troughs_mask[-1] = False
    
    peaks = np.where(peaks_mask)[0]
    troughs = np.where(troughs_mask)[0]
    
    print(f"\nPhase Structure:")
    print(f"Peaks at turns: {turns[peaks]}")
    print(f"Troughs at turns: {turns[troughs]}")
    
    # Check if troughs align with KAPPA_3
    trough_rates = rates[troughs]
    if len(trough_rates) > 0:
        print(f"Avg Trough Rate: {np.mean(trough_rates):.6f}")
        print(f"Trough match to 1/64: {np.mean(trough_rates)/KAPPA_3:.4f} x κ₃")
    
    # 3. Identify Calcification Point (Phase Transition)
    # Looking for a shift from high variance (liquid/cartilage) to stable low variance (bone)
    # or a shift in the baseline rate.
    
    # Rolling variance
    window = 5
    if len(rates) > window:
        rolling_std = pd.Series(rates).rolling(window=window).std()
        # Find where variance drops significantly
        # (Naive approach: first point where std drops below mean std / 2)
        mean_std = rolling_std.mean()
        calcification_idx = rolling_std[rolling_std < mean_std * 0.5].first_valid_index()
        
        if calcification_idx is not None:
            calc_turn = turns[calcification_idx]
            print(f"\nPotential Calcification Point (Transition to Solid): Turn {calc_turn}")
            print(f"Variance drops below {mean_std*0.5:.6f}")
        else:
            print("\nNo clear Calcification Point (variance drop) detected.")
    
    # 4. Right Cortisol Location Hypothesis
    # If Right Cortisol is "Fake 3D" (Half 3D), it should be where the system *attempts* 3D (high rate)
    # but fails to sustain it (or leaks).
    # Or it could be the "Cartilage" phase - stable but lower magnitude (1/64).
    
    # Let's assume the 1/64 locking phase IS the Right Cortisol phase.
    # Map back to r, q0 coordinates
    valid_df['ratio_k3'] = valid_df['rate_post_mean'] / KAPPA_3
    
    half_3d_mask = (valid_df['ratio_k3'] > 0.9) & (valid_df['ratio_k3'] < 1.1)
    half_3d_points = valid_df[half_3d_mask]
    
    if len(half_3d_points) > 0:
        print(f"\nRIGHT CORTISOL / CARTILAGE SIGNATURE DETECTED")
        print(f"Count of points locking to κ₃ (1/64): {len(half_3d_points)}")
        
        # Cluster analysis to find center (r, q0)
        center_r = half_3d_points['r'].mean()
        center_q0 = half_3d_points['q0'].mean()
        std_r = half_3d_points['r'].std()
        std_q0 = half_3d_points['q0'].std()
        
        print(f"\nSPATIAL LOCATION of 1/64 LOCK (Right Cortisol Candidate):")
        print(f"  Center r  = {center_r:.6f} (±{std_r:.6f})")
        print(f"  Center q0 = {center_q0:.6f} (±{std_q0:.6f})")
        
        print(f"Interpretation: This (r,q0) region represents the 'Fake 3D' Cartilage phase.")
    else:
        print("\nNo explicit lock to exactly 1/64 detected in mean rates.")
        print("Checking for 1/64 residuals instead...")
        
        # Residual check: Rate % KAPPA_2
        # If rate = N * KAPPA_2 + M * KAPPA_3, then rate % KAPPA_2 should peak at KAPPA_3
        residuals_k2 = rates % KAPPA_2
        mean_res_k2 = np.mean(residuals_k2)
        print(f"Mean Residual mod κ₂: {mean_res_k2:.6f}")
        print(f"Match to κ₃ (0.015625): {mean_res_k2 / KAPPA_3:.4f}")
        
        if 0.8 < (mean_res_k2 / KAPPA_3) < 1.2:
             print("SUCCESS: Residuals confirm 1/64 leakage component!")
             print("The 'Fake 3D' exists as a sub-harmonic of the main field.")

    # 5. Check for Bone/Solid Signature (KAPPA_4 = 1/128)
    valid_df['ratio_k4'] = valid_df['rate_post_mean'] / KAPPA_4
    bone_mask = (valid_df['ratio_k4'] > 0.9) & (valid_df['ratio_k4'] < 1.1)
    bone_points = valid_df[bone_mask]
    
    print(f"\n" + "="*40)
    print(f"BONE / SOLID SIGNATURE ANALYSIS (1/128)")
    print(f"="*40)
    print(f"Mean Ratio to κ₄ (1/128): {np.mean(valid_df['ratio_k4']):.4f}")
    
    if len(bone_points) > 0:
        print(f"Count of points locking to κ₄ (1/128): {len(bone_points)}")
        print(f"Percentage of time in Bone phase: {len(bone_points)/len(valid_df)*100:.2f}%")
        
        # Spatial location of Bone
        b_r = bone_points['r'].mean()
        b_q0 = bone_points['q0'].mean()
        b_r_std = bone_points['r'].std()
        b_q0_std = bone_points['q0'].std()
        
        print(f"SPATIAL LOCATION of 1/128 LOCK (Bone Phase):")
        print(f"  Center r  = {b_r:.6f} (±{b_r_std:.6f})")
        print(f"  Center q0 = {b_q0:.6f} (±{b_q0_std:.6f})")
        print(f"  Turns: {bone_points['turn'].values[:10]} ...")
    # 6. Temporal Distribution Analysis (Evolutionary Timing)
    # Count occurrences per turn
    cartilage_counts = valid_df[half_3d_mask].groupby('turn').size()
    bone_counts = valid_df[bone_mask].groupby('turn').size()
    
    print(f"\n" + "="*40)
    print(f"TEMPORAL EVOLUTION ANALYSIS")
    print(f"="*40)
    
    # Normalize by total points per turn (approximate if constant)
    # Just showing raw counts for pattern
    print("Turn | Cartilage (1/64) | Bone (1/128) | Phase Dominance")
    print("-" * 60)
    
    all_turns = sorted(list(set(valid_df['turn'])))
    for t in all_turns:
        c = cartilage_counts.get(t, 0)
        b = bone_counts.get(t, 0)
        if c + b > 0:
            dom = "Cartilage" if c > b else "Bone"
            print(f"{t:4d} | {c:16d} | {b:12d} | {dom}")

if __name__ == "__main__":
    analyze_calcification()
