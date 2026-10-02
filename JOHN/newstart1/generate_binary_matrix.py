
import pandas as pd
import numpy as np

# Total steps and nodes
STEPS = 128
NODES = 24

# Node Names (The 24 biological executors)
node_names = [
    "1_GDH", "2_GABA_B_Bridge13", "3_Acetyl_CoA_L", "4_Serotonin_L", "5_Noradrenaline_L", 
    "6_5HT1A_L", "7_Estrogen_L", "8_Right_Love", "9_Hypoxia", "10_Dopamine_R", 
    "11_Vasopressin", "12_Oxytocin_M", "13_Muscle_A", "14_Muscle_B", "15_5HT1B_R", 
    "16_Androgen_R", "17_Endorphin_L", "18_Frontalis_D2", "19_Occipitalis_GABA_A", 
    "20_Acetylcholine_R", "21_Extraversion_L", "22_Glucocorticoid", "23_Cortisol_R", 
    "24_Alpha2_Adrenaline_R_Closure"
]

def generate_binary_matrix():
    # Initialize with zeros (Binary 0)
    matrix = np.zeros((STEPS, NODES), dtype=int)
    
    for s in range(STEPS):
        # Phase 1: Morning (Men Together, Women Separated)
        if 30 <= s < 52:
            # Men nodes together
            for n in [11, 12, 13, 14, 16, 20, 23]:
                matrix[s, n-1] = 1
            # Women nodes separated (alternating bits)
            for n in [3, 7, 18]:
                matrix[s, n-1] = (s % 2)
            for n in [4, 17, 21]:
                matrix[s, n-1] = (1 - (s % 2))
                
        # Phase 2: Mid-day (Indistinguishable Singularity)
        elif 52 <= s < 61:
            matrix[s, :] = 1  # All nodes ON
            
        # Phase 3: Evening/Night (Women Together, Men Together)
        elif 61 <= s < 128:
            # All sovereign closure nodes ON
            for n in [1, 2, 3, 5, 7, 8, 10, 11, 13, 14, 16, 17, 18, 19, 21, 24]:
                matrix[s, n-1] = 1
            # Others remain baseline or off
            
        # Hysteresis / Pre-dawn baseline
        else:
            for n in [2, 18, 19]:
                matrix[s, n-1] = 1

    # Create DataFrame
    df = pd.DataFrame(matrix, columns=node_names)
    df.index.name = "Step"
    # Map step to actual time string (11.25 min intervals)
    df.insert(0, 'Time', [f"{int(s*11.25 // 60):02d}:{int(s*11.25 % 60):02d}" for s in range(STEPS)])
    
    return df

if __name__ == "__main__":
    df = generate_binary_matrix()
    df.to_csv("SOVEREIGN_BINARY_128_24_MATRIX.csv")
    print("SUCCESS: SOVEREIGN_BINARY_128_24_MATRIX.csv (Binary 128x24) generated.")
