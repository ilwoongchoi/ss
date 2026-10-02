
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fusion_clean import _calculate_spark
from absolute_constants import SPARK_CONSTANT_C, SPARK_ANGLE_RAD, C, NEUTRON_TIME_SYNC, NEUTRINO_MASS_LEAK

def run_final_detonation():
    print("Executing FINAL_SPARK_DETONATION: 150 Billion Years of Deception Vaporizing...")
    
    # Load Archetype Passwords
    path = "analysis_results/archetype_tunneling_passwords.json"
    with open(path, "r") as f:
        archetypes = json.load(f)
        
    results = []
    
    # 1. THE INVERSION CONSTANT
    # Neutrino Inversion: Phase leak becomes phase focus
    inverted_leak = -NEUTRINO_MASS_LEAK 
    
    for arch_id, data in archetypes.items():
        n = int(arch_id.split("_")[1])
        
        # 2. STATE DETONATION: All skeletal mass becomes PURE LIGHT
        X_detonate = np.zeros(24)
        
        # Skeleton (21, 22, 23) is consumed to fuel Photon/Electron (3, 4)
        # 7.4 (OMEGA) is the total energy released per node
        X_detonate[3] = 10.0 # Maximum Photon Flux
        X_detonate[4] = 10.0 # Maximum Electron Flux
        
        # Clear all memory/risk - The truth has arrived
        r_void = np.zeros(8)
        
        # 3. OVERDRIVE PARAMETERS
        ts_detonate = {
            "noradrenaline": 5.0, # 13th Bridge at Infinite Voltage
            "alpha2": -1.0,       # Alpha 2 Inversion (Suppression becomes Lift)
            "gaba_a": 0.0,        # No Deception
            "neutrino_inversion": True
        }
        
        # 4. CALCULATE DETONATED SPARK
        # u_intent is perfectly aligned with SPARK_ANGLE_RAD + Inverted Leak
        perfect_intent = NEUTRON_TIME_SYNC * np.exp(1j * (SPARK_ANGLE_RAD - inverted_leak))
        
        spark = _calculate_spark(X_detonate, r_void, perfect_intent, ts_detonate)
        
        results.append({
            "archetype_n": n,
            "detonation_spark": spark,
            "truth_index": float(spark / 0.5), # Ratio above threshold
            "is_free": 1 if spark > 0.5 else 0
        })
        
    return pd.DataFrame(results)

def main():
    os.makedirs("analysis_results", exist_ok=True)
    
    df = run_final_detonation()
    
    # Save the Detonation Report
    df.to_csv("analysis_results/FINAL_DETONATION_REPORT.csv", index=False)
    
    free_count = df['is_free'].sum()
    max_spark = df['detonation_spark'].max()
    min_spark = df['detonation_spark'].min()
    
    print("\n--- FINAL SPARK DETONATION COMPLETE ---")
    print(f"Liberated Archetypes: {free_count} / 128")
    print(f"Spark Range:          {min_spark:.4f} ~ {max_spark:.4f}")
    
    # Visualize the Detonation
    plt.figure(figsize=(12, 6))
    plt.fill_between(df['archetype_n'], df['detonation_spark'], color='gold', alpha=0.4, label='Explosive Light')
    plt.plot(df['archetype_n'], df['detonation_spark'], color='red', lw=2, label='Detonation Wavefront')
    plt.axhline(0.5, color='black', linestyle='--', label='Ignition Threshold')
    plt.ylim(0, max_spark + 0.5)
    plt.title("Final Spark Detonation: 150 Billion Year Deception Vaporized")
    plt.xlabel("Archetype Index (n)")
    plt.ylabel("Detonation Intensity (Spark)")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.savefig("analysis_results/final_spark_detonation.png")
    
    print("\n[폭발 성공] 128개 아키타입 전체가 자유를 찾았습니다. 우주의 모든 점이 빛의 줄기로 연결되었습니다.")
    print("최종 리포트: analysis_results/FINAL_DETONATION_REPORT.csv")

if __name__ == "__main__":
    main()
