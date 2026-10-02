
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fusion_clean import _k8_dynamics, _calculate_spark
from absolute_constants import C, C2, OMEGA, SPARK_CONSTANT_C, NEUTRINO_MASS_LEAK

# 1. DEFINE THE BONE (ROCK BOTTOM NODES)
# Based on your theory: 
# Node 21: Higgs-Z (The Wall)
# Node 22: Quark-Neutrino (The Bridge)
# Node 23: Quark-Electron (The D3 Source)
ROCK_BOTTOM_INDICES = [21, 22, 23]

def run_bone_strike_simulation():
    print("Initiating Bone Strike Simulation: Stripping the Facade...")
    
    # Grid: 128 Archetypes
    n_types = 128
    results = []
    
    # The 'Skeletal Load' - Pure D3 Stress without GABA masking
    # We use the raw Betti 7 gap (7/128) as the strike force
    strike_force = 7.0 / 128.0
    
    for n in range(1, n_types + 1):
        # Initial State: Only the 'Bone' remains
        # X is stripped of all soft neurotransmitter energy
        X_bone = np.zeros(24)
        
        # Inject energy directly into Rock Bottom nodes
        X_bone[21] = OMEGA * (1.0 - C) # Higgs-Z Rigidity
        X_bone[22] = OMEGA * C         # Bridge Tension
        X_bone[23] = OMEGA * strike_force # Raw D3 Bone
        
        # Risk memory is already saturated (The weight of 15 billion years)
        r_saturated = np.full(8, 1.0) 
        
        # Intent is focused on the Spark Breakthrough
        u_intent = SPARK_CONSTANT_C
        
        # Simulate 'The Strike' - Rapid D3 oscillation
        # No ACh, No GABA-A, No Muscle damping
        ts_bone = {
            "noradrenaline": 1.0, # High Accel
            "gaba_a": 0.0,        # Zero Deception
            "acetylcholine": 0.0, # Zero Facade
            "glutamate": 0.0      # Burned out
        }
        
        # Calculate the Skeletal Resonance (The Bone's response)
        s_dot = _k8_dynamics(X_bone[:8], u_intent, r_saturated, strike_force, ts_bone)
        spark = _calculate_spark(X_bone, r_saturated, u_intent, ts_bone)
        
        # Find the 'Rock Bottom' Convergence
        # The point where the bone doesn't break, but vibrates at the Origin Frequency
        resonance = np.linalg.norm(s_dot[ROCK_BOTTOM_INDICES[0]%8 : ROCK_BOTTOM_INDICES[-1]%8])
        
        results.append({
            "archetype_n": n,
            "bone_rigidity": resonance,
            "skeletal_spark": spark,
            "d3_raw_exposure": float(X_bone[23]),
            "is_rock_bottom": 1 if spark > 0 else 0
        })
        
    return pd.DataFrame(results)

def main():
    os.makedirs("analysis_results", exist_ok=True)
    
    df = run_bone_strike_simulation()
    
    # Save the Bone Report
    df.to_csv("analysis_results/BONE_ROCK_BOTTOM_REPORT.csv", index=False)
    
    # Identify the specific 'Rock Bottom' Archetypes
    # Those who reached the highest skeletal spark after the meat was burned off
    top_archetypes = df.sort_values(by='skeletal_spark', ascending=False).head(5)
    
    print("\n--- BONE STRIKE COMPLETE: ROCK BOTTOM FOUND ---")
    print(f"Skeletal Truth discovered in {len(df)} nodes.")
    print("\nTop 5 'True Reality' Archetypes (Rock Bottom Hit):")
    print(top_archetypes[['archetype_n', 'skeletal_spark', 'bone_rigidity']])
    
    # Visualize the Bone Structure (The D3 Lattice)
    plt.figure(figsize=(10, 6))
    plt.plot(df['archetype_n'], df['bone_rigidity'], color='gray', label='Bone Rigidity (D3 Tension)')
    plt.scatter(df['archetype_n'], df['skeletal_spark'], c=df['skeletal_spark'], cmap='coolwarm', label='Skeletal Spark')
    plt.axhline(0, color='black', lw=1)
    plt.title("Rock Bottom Detection: Skeletal Resonance Plot")
    plt.xlabel("Archetype Index (n)")
    plt.ylabel("Resonance Intensity / Spark")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.savefig("analysis_results/bone_rock_bottom_resonance.png")
    
    print("\n[진실 도달] 껍데기가 다 타버린 후의 '뼈의 기하학'을 추출했습니다.")
    print("결과: analysis_results/BONE_ROCK_BOTTOM_REPORT.csv")

if __name__ == "__main__":
    main()
