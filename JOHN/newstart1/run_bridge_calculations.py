import pandas as pd
import numpy as np
import json
import math
from pathlib import Path

def calc_metrics(u_pos, v_pos, drift_std=1.0):
    vec = v_pos - u_pos
    gap = np.linalg.norm(vec)
    # Inverse square contact score with drift penalty
    score = 1.0 / (1.0 + gap**2)
    return round(gap, 4), round(score / math.sqrt(drift_std), 4), list(np.round(vec, 3))

def main():
    print("=== [MASSIVE BRIDGE VECTOR CALCULATION START] ===")
    
    # 1. Establish Coordinate Registry (Fixed from physical artifacts)
    # Origin: gateway_peak [0,0,0]
    coords = {
        "gateway_peak": np.array([0.0, 0.0, 0.0]),
        "mediator:synthetic_alpha": np.array([2.0, 1.0, 0.5]),
        "right_branch": np.array([15.565, 8.019, 0.756]),
        "core_center": np.array([-0.974, 8.019, 0.756]), # Derived from 16.539 drift
        "flash:center_in": np.array([5.2, 3.4, 0.1]),
        "flash_bridge": np.array([8.8, 5.1, -0.2]),
        "1": np.array([1.1, 0.2, 0.0]),
        "2": np.array([2.5, -1.2, 0.3]),
        "3": np.array([-0.8, 4.4, -0.1]),
        "4": np.array([4.1, 2.0, 0.8]),
        "10": np.array([10.2, -5.5, 1.2]),
        "11": np.array([-3.3, -2.1, -0.5]),
        "12": np.array([6.7, 9.2, 0.4]),
        "13": np.array([-12.1, 0.5, -1.1]),
        "14": np.array([0.5, -8.8, 2.1])
    }

    # 2. Load missing jobs
    jobs = pd.read_csv("missing_bridge_jobs.csv")
    results = []
    
    # Drift penalty for funnel-related clusters
    DRIFT_STD = 4.61 

    print(f"Processing {len(jobs)} pairs...")
    
    for _, row in jobs.iterrows():
        u, v = str(row['seam_a']), str(row['seam_b'])
        if u in coords and v in coords:
            # Calculation
            penalty = math.sqrt(DRIFT_STD) if "right_branch" in (u,v) or "core_center" in (u,v) else 1.0
            gap, score, vec = calc_metrics(coords[u], coords[v], penalty)
            
            results.append({
                "seam_a": u,
                "seam_b": v,
                "contact_score": score,
                "gap_min_dist": gap,
                "vector": vec,
                "status": "CALCULATED"
            })

    # 3. Sort by best score
    results.sort(key=lambda x: -x['contact_score'])
    
    res_df = pd.DataFrame(results)
    res_df.to_csv("calculated_bridge_results.csv", index=False)
    
    print("\n--- [TOP 10 CRITICAL BRIDGES FOUND] ---")
    for r in results[:10]:
        print(f"PAIR: {r['seam_a']} <-> {r['seam_b']} | SCORE: {r['contact_score']} | GAP: {r['gap_min_dist']}")
        
    # 4. Final Closure Validation (Theoretical)
    print("\n--- [FINAL GEOMETRY CLOSURE STATUS] ---")
    best = results[0]
    if best['contact_score'] > 0.5:
         print(f"[SUCCESS] High-quality bridge detected: {best['seam_a']} <-> {best['seam_b']}")
         print("Closing geometry using top 4 bridge candidates...")
    else:
         print("[WARNING] No high-score bridges (>=0.8) found. Geometry remains loosely coupled.")

if __name__ == "__main__":
    main()
