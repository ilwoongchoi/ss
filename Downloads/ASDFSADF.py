
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_potential(mbti, blood, gender):
    # 1. MBTI Potential (NT > NF > ST > SF)
    mbti_pot = {
        "ENTP": 0.95, "INTP": 0.90, "ENTJ": 0.85, "INTJ": 0.80,
        "ENFP": 0.75, "INFP": 0.70, "ENFJ": 0.65, "INFJ": 0.60,
        "ESTP": 0.55, "ISTP": 0.50, "ESTJ": 0.45, "ISTJ": 0.40,
        "ESFP": 0.35, "ISFP": 0.30, "ESFJ": 0.25, "ISFJ": 0.20
    }
    
    # 2. Blood Type Potential (AB > B > A > O) - Voltage/Density gradient
    blood_pot = {"AB": 1.0, "B": 0.75, "A": 0.5, "O": 0.25}
    
    # 3. Gender Potential (M: Ascent/Spark, F: Descent/Desire)
    gender_pot = {"M": 1.1, "F": 0.9}
    
    return mbti_pot[mbti] * blood_pot[blood] * gender_pot[gender]

def generate_potential_baton_grid():
    mbti_16 = [
        "ESTP", "ISTP", "ESFP", "ISFP", "ESTJ", "ISTJ", "ESFJ", "ISFJ",
        "ENTP", "INTP", "ENFP", "INFP", "ENTJ", "INTJ", "ENFJ", "INFJ"
    ]
    blood_types = ["O", "A", "B", "AB"]
    genders = ["M", "F"]

    all_types = []
    for m in mbti_16:
        for b in blood_types:
            for g in genders:
                pot = get_potential(m, b, g)
                all_types.append({
                    "type": f"{m}_{b}_{g}",
                    "potential": pot,
                    "mbti": m,
                    "blood": b,
                    "gender": g
                })
    
    # Sort by potential (High to Low) for Linear Baton-Touch Flow
    # Energy flows from Source (ENTP AB M) to Sink (ISFJ O F)
    all_types.sort(key=lambda x: x['potential'], reverse=True)

    window_duration = 1440 / 128
    start_time = datetime.strptime("00:00:00", "%H:%M:%S")
    
    grid_data = []
    for i, t in enumerate(all_types):
        w_start = start_time + timedelta(minutes=i * window_duration)
        w_end = w_start + timedelta(minutes=window_duration)
        
        # Mapping to Atomic/Brain Chemistry Logic
        z_index = 128 - i
        neuro = "Dopamine (D2)" if "NT" in t['mbti'] else "Serotonin" if "NF" in t['mbti'] else "GABA" if "ST" in t['mbti'] else "Acetylcholine"
        
        grid_data.append({
            "Window": i,
            "Start": w_start.strftime("%H:%M:%S"),
            "End": w_end.strftime("%H:%M:%S"),
            "Type": t['type'],
            "Potential": round(t['potential'], 4),
            "Z_Index": z_index,
            "Neurochem": neuro,
            "Spark_Condition": "138.88V_Ready" if t['potential'] > 0.8 else "Stability_Focus"
        })

    df = pd.DataFrame(grid_data)
    df.to_csv("d:/Users/user/Documents/newstart/128_POTENTIAL_BATON_GRID.csv", index=False)
    print("Potential-driven Baton Grid saved to 128_POTENTIAL_BATON_GRID.csv")
    return df

if __name__ == "__main__":
    generate_potential_baton_grid()
