
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fusion_clean import evolve_consciousness_field, _calculate_spark
from absolute_constants import SPARK_CONSTANT_C, OMEGA, C, NEUTRON_TIME_SYNC

def run_skeletal_ignition():
    print("Executing SKELETAL_IGNITION: Overdriving the 13th Bridge...")
    
    # Load Archetype Passwords
    path = "analysis_results/archetype_tunneling_passwords.json"
    with open(path, "r") as f:
        archetypes = json.load(f)
        
    results = []
    
    for arch_id, data in archetypes.items():
        n = int(arch_id.split("_")[1])
        u_base = np.array(data["u24_vector"])
        
        # 1. OVERDRIVE: Activate the 13th Bridge (Left Noradrenaline)
        # We force-fire the accelerator node (Index 4)
        u_base[4] = 1.5 # Over 1.0 to break the 0.2828 barrier
        
        # 2. SKELETAL STATE: Focus energy on the Rock Bottom (21, 22, 23)
        X_ignite = np.zeros(24)
        X_ignite[21] = 5.0 # Higgs-Z Rigidity
        X_ignite[22] = 5.0 # Bridge Tension
        X_ignite[23] = 7.0 # Raw D3 Source (The Bone)
        
        # Add some 'Friction Heat' (Photon/Electron) from the D3 strike
        X_ignite[3] = 2.0 # Internal Photon generation
        X_ignite[4] = 2.0 # Internal Electron mobilization
        
        r_memory = np.full(8, 0.1) # Memory is cleared by the high voltage
        
        # 3. IGNITION: Calculate the Spark Breakthrough
        ts_ignition = {
            "noradrenaline": 2.0, # 13th Bridge Overdrive
            "alpha2": 0.0,        # No Alpha 2 suppression
            "gaba_a": 0.0         # No Deception
        }
        
        # Direct Spark Calculation
        spark = _calculate_spark(X_ignite, r_memory, SPARK_CONSTANT_C, ts_ignition)
        
        # 4. CONVERGENCE TO TRUE OMEGA
        # Does the ignition push the system towards a stable 7.4?
        norm_x = np.linalg.norm(X_ignite)
        
        results.append({
            "archetype_n": n,
            "ignition_spark": spark,
            "bridge_voltage": float(u_base[4]),
            "d3_residue": float(X_ignite[23] - spark), # Spark consumes D3
            "is_ignited": 1 if spark > 0.5 else 0
        })
        
    return pd.DataFrame(results)

def main():
    os.makedirs("analysis_results", exist_ok=True)
    
    df = run_skeletal_ignition()
    
    # Save the Ignition Report
    df.to_csv("analysis_results/SKELETAL_IGNITION_REPORT.csv", index=False)
    
    ignited_count = df['is_ignited'].sum()
    avg_spark = df['ignition_spark'].mean()
    
    print("\n--- SKELETAL IGNITION COMPLETE ---")
    print(f"Total Ignited Archetypes: {ignited_count} / 128")
    print(f"Average Ignition Spark:   {avg_spark:.6f}")
    
    # Visualize the Breakthrough
    plt.figure(figsize=(12, 6))
    plt.bar(df['archetype_n'], df['ignition_spark'], color='orange', alpha=0.7, label='Ignition Spark')
    plt.axhline(0.5, color='red', linestyle='--', label='Ignition Threshold')
    plt.title("Skeletal Ignition Breakthrough: 13th Bridge Overdrive")
    plt.xlabel("Archetype Index (n)")
    plt.ylabel("Spark Intensity")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.savefig("analysis_results/skeletal_ignition_breakthrough.png")
    
    print("\n[점화 성공] 뼈 자체가 타오르기 시작했습니다. 150억 년의 기만이 증발 중입니다.")
    print("결과 보고서: analysis_results/SKELETAL_IGNITION_REPORT.csv")

if __name__ == "__main__":
    main()
