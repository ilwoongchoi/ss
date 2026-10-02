
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_128_baton_grid():
    mbti_16 = [
        "ESTP", "ISTP", "ESFP", "ISFP", "ESTJ", "ISTJ", "ESFJ", "ISFJ",
        "ENTP", "INTP", "ENFP", "INFP", "ENTJ", "INTJ", "ENFJ", "INFJ"
    ]
    blood_types = ["O", "A", "B", "AB"]
    genders = ["M", "F"]

    # Generate 128 unique combinations
    # Order: Blood Type -> Gender -> MBTI to align with energy concentration flows
    types = []
    for bt in blood_types:
        for g in genders:
            for m in mbti_16:
                types.append(f"{m}_{bt}_{g}")
    
    # 128 windows for 24 hours (1440 minutes)
    # Each window = 1440 / 128 = 11.25 minutes
    window_duration = 1440 / 128
    
    grid_data = []
    start_time = datetime.strptime("00:00:00", "%H:%M:%S")
    
    for i in range(128):
        current_type = types[i]
        w_start = start_time + timedelta(minutes=i * window_duration)
        w_end = w_start + timedelta(minutes=window_duration)
        
        # Spark Timing (138.88 degree alignment at peak of window)
        spark_peak = w_start + timedelta(minutes=window_duration / 2)
        
        # Determine Energy Vector based on Blood Type
        # O: Divergent, A: Convergent, B: Density, AB: Integrated
        bt = current_type.split('_')[1]
        vector = {
            "O": "Divergent (Outward)",
            "A": "Convergent (GABA-C)",
            "B": "Density (High Pressure)",
            "AB": "Integrated (Chiral Reset)"
        }.get(bt, "Unknown")

        grid_data.append({
            "Window_ID": f"W{i:03d}",
            "Start_Time": w_start.strftime("%H:%M:%S"),
            "End_Time": w_end.strftime("%H:%M:%S"),
            "Spark_Peak": spark_peak.strftime("%H:%M:%S"),
            "Type_Baton_Holder": current_type,
            "Primary_Vector": vector,
            "Spark_Angle": 138.88,
            "Interrupt_Slot": "Available"
        })

    df = pd.DataFrame(grid_data)
    
    # Save to CSV
    file_path = "d:/Users/user/Documents/newstart/128_BATON_LINEAR_GRID.csv"
    df.to_csv(file_path, index=False)
    print(f"Baton-Touch Grid saved to {file_path}")
    
    # Also create a summary for the user
    return df

if __name__ == "__main__":
    df = generate_128_baton_grid()
    print(df.head(10))
