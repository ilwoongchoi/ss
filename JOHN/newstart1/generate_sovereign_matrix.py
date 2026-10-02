
import pandas as pd
import numpy as np

# Constants from Sovereign Theory
C = 0.2828
C2 = 0.08
STEPS = 128
NODES = 24

# Phase timings (mapped to 128 steps)
# 00:00 = Step 0, 24:00 = Step 128
# Step = (HH * 60 + MM) / 11.25
P2_0945 = 52
SOV_1030 = 56
P1_1545 = 84
HYST_0215 = 12
TRANS_NIGHT = 0

node_names = [
    "1_GDH", "2_GABA_B", "3_Acetyl_CoA_L", "4_Serotonin_L", "5_Noradrenaline_L", 
    "6_5HT1A_L", "7_Estrogen_L", "8_Right_Love", "9_Hypoxia", "10_Dopamine_R", 
    "11_Vasopressin", "12_Oxytocin_M", "13_Muscle_A", "14_Muscle_B", "15_5HT1B_R", 
    "16_Androgen_R", "17_Endorphin_L", "18_Frontalis_D2", "19_Occipitalis_GABA_A", 
    "20_Acetylcholine_R", "21_Extraversion_L", "22_Glucocorticoid", "23_Cortisol_R", 
    "24_Alpha2_Adrenaline_R"
]

# Initialize matrix
matrix = np.zeros((STEPS, NODES))

# Helper to set states based on FUSION_V8_MASTER_MAP logic
def set_phase_state(step, phase_name):
    # Logic based on the user-approved 5-phase table
    if phase_name == "P1":
        on_nodes = [1, 3, 5, 11, 13, 14, 18, 19, 21, 23]
    elif phase_name == "P2":
        on_nodes = [10, 11, 16, 18, 19, 21] # Alpha-2 is OFF=ACTIVE
    elif phase_name == "HYST":
        on_nodes = [2, 3, 4, 7, 17, 18, 19]
    elif phase_name == "SOV":
        on_nodes = [1, 2, 3, 5, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 21]
    elif phase_name == "TRANS":
        on_nodes = [4, 6, 9, 15, 18, 19]
    else:
        on_nodes = []
    
    for n in on_nodes:
        matrix[step % STEPS, n-1] = 1.0

# Define key points
phases = [
    (TRANS_NIGHT, "TRANS"),
    (HYST_0215, "HYST"),
    (P2_0945, "P2"),
    (SOV_1030, "SOV"),
    (P1_1545, "P1"),
    (127, "TRANS")
]

# Interpolate between phases
for i in range(len(phases) - 1):
    start_step, start_name = phases[i]
    end_step, end_name = phases[i+1]
    
    set_phase_state(start_step, start_name)
    set_phase_state(end_step, end_name)
    
    # Simple linear interpolation for intermediate steps
    for s in range(start_step + 1, end_step):
        for n in range(NODES):
            matrix[s, n] = matrix[start_step, n] + (matrix[end_step, n] - matrix[start_step, n]) * (s - start_step) / (end_step - start_step)

# Add 0.3125 spark context to specific nodes
matrix[:, 9] *= 1.0125  # Dopamine (R) scale
matrix[:, 22] *= 1.2828 # Cortisol (R) scale

# Create DataFrame
df = pd.DataFrame(matrix, columns=node_names)
df.index.name = "Step"
df['Time'] = [f"{int(s*11.25 // 60):02d}:{int(s*11.25 % 60):02d}" for s in range(STEPS)]

# Save to CSV
df.to_csv("SOVEREIGN_MASTER_128_24_MATRIX.csv")
print("File generated: SOVEREIGN_MASTER_128_24_MATRIX.csv")
