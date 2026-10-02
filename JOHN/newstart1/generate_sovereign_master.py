
import pandas as pd
import numpy as np

# Invariant Constants
C = 0.2828
C2 = 0.08
STEPS = 128
NODES = 24
ROTATION_TOTAL = 138.88  # Total convergence angle

# 24 Node Names
node_names = [
    "1_GDH_q", "2_GABA_B_Bridge13", "3_Acetyl_CoA_L", "4_Serotonin_L", "5_Noradrenaline_L", 
    "6_5HT1A_L", "7_Estrogen_L", "8_Right_Love_Field", "9_Hypoxia", "10_Dopamine_R_Spark", 
    "11_Vasopressin_Anchor", "12_Oxytocin_M", "13_Muscle_A_BW", "14_Muscle_B_BW", "15_5HT1B_R", 
    "16_Androgen_R_Spark", "17_Endorphin_L_Omega", "18_Frontalis_D2", "19_Occipitalis_GABA_A", 
    "20_Acetylcholine_R", "21_Extraversion_L", "22_Glucocorticoid", "23_Cortisol_R_VEV", 
    "24_Alpha2_Adrenaline_R_Closure"
]

def generate_sovereign_dynamics():
    matrix = np.zeros((STEPS, NODES))
    
    for s in range(STEPS):
        # Current phase angle in radians
        theta = np.radians(s * (ROTATION_TOTAL / STEPS))
        
        # Base oscillation for physical nodes (1-21)
        for n in range(21):
            # Phase shift by node index to create the 'wave' through the 6x4 matrix
            phase_shift = (n % 6) * (np.pi / 3)
            val = np.sin(theta + phase_shift)
            
            # Quantize by C
            matrix[s, n] = np.round(val / C) * C
            
        # Sovereign Closure Nodes (2, 23, 24 - override or specialized logic)
        
        # Node 2 (GABA-B): Active during Hysteresis (night) to return energy
        if 0 <= s <= 20 or 110 <= s < 128:
            matrix[s, 1] = 1.0  # Return Bridge ON
            
        # Node 23 (Cortisol): VEV Scale, high during day (Step 30-90)
        if 30 <= s <= 90:
            matrix[s, 22] = 1.2828  # High VEV
        else:
            matrix[s, 22] = 0.2828  # Baseline C
            
        # Node 24 (Alpha-2): Closure Gate
        # Must be OFF (0 or low) during P2 and SOV to allow Z-current
        if 50 <= s <= 60:
            matrix[s, 23] = 0.0  # GATE OPEN (Medial Pressure / Closure)
        else:
            matrix[s, 23] = 1.0  # GATE CLOSED
            
        # Spark Nodes (10, 16): Peak at P2 (Step 52)
        dist_to_p2 = abs(s - 52)
        spark_val = 1.0125 * np.exp(-dist_to_p2 / 10)
        matrix[s, 9] = np.round(spark_val / C2) * C2
        matrix[s, 15] = np.round(spark_val / C2) * C2

    # Create DataFrame
    df = pd.DataFrame(matrix, columns=node_names)
    df.index.name = "Step"
    # Map step to actual time string
    df.insert(0, 'Time', [f"{int(s*11.25 // 60):02d}:{int(s*11.25 % 60):02d}" for s in range(STEPS)])
    
    return df

if __name__ == "__main__":
    df = generate_sovereign_dynamics()
    df.to_csv("SOVEREIGN_MASTER_128_24_MATRIX.csv")
    print("SUCCESS: SOVEREIGN_MASTER_128_24_MATRIX.csv generated with 128x24 resolution.")
