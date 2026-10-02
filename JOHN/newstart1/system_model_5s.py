import numpy as np
import pandas as pd
import os

# ---------------------------------------------------------
# 1. Absolute Constants (Framework Locked)
# ---------------------------------------------------------
REALITY_TENSION = 1.0100375
DISCRETE_CLOSURE = 1.0000424
LOOP_STRENGTH_5 = 5.555492104
LUNAR_CYCLE = 1.0 / 28.0
COMPRESSION_GATE = 3.0 / 32.0   # 0.09375 (Möbius Kink Threshold)
TOTAL_DEBT_AREA = 1.3228
SPARK_ANGLE = 138.88

# ---------------------------------------------------------
# 2. ODE System Definition
# ---------------------------------------------------------
def simulate_5_sphere_system():
    # Time parameters: 0 to 45 (representing 4.5 Ga to 0 Ga, 0.1 steps)
    time_steps = np.arange(0, 45.1, 0.1)
    
    # Initial State [E_B, E_S, E_E, E_M, E_C]
    # Barnard(1D Truth), Sun(Left UV), Earth(332 Rectifier), Moon(Dynamo/SM), Co-Mag(Big Woman)
    state = np.array([1.0, 0.5, 0.2, 0.2, 0.25])
    
    history = []
    
    for t in time_steps:
        age_Ga = 4.5 - (t / 10.0)
        E_B, E_S, E_E, E_M, E_C = state
        
        # ---------------------------------------------------------
        # Epoch scaling & Dynamo Gate (w_gate)
        # ---------------------------------------------------------
        # Barnard influence drops over time as it moves off the North Pole axis
        barnard_scale = np.exp(-t / 15.0) 
        
        # Moon dynamo logic (w_gate)
        if age_Ga >= 3.5:
            w_gate = 1.0  # Epoch 1: Strong Brother Moon
            kink_state = "Brother (SM)"
        elif age_Ga >= 1.5:
            # Epoch 2: Mid Eukaryote Merger (Dynamo fading)
            # Linear decay to COMPRESSION_GATE
            w_gate = 1.0 - (1.0 - COMPRESSION_GATE) * ((3.5 - age_Ga) / 2.0)
            kink_state = "Turning Over"
        else:
            # Epoch 3: Bilaterian Loop (Upturned Small Woman)
            w_gate = COMPRESSION_GATE
            kink_state = "Upturned (SW)"
            
        # Möbius Kink triggers when w_gate hits the 3/32 threshold
        is_mobius_kink = 1 if w_gate <= COMPRESSION_GATE else 0

        # ---------------------------------------------------------
        # Flow Coefficients (The geometry of the 5 nodes)
        # ---------------------------------------------------------
        k_BE = 0.05 * barnard_scale * REALITY_TENSION  # Barnard 1D strike to Earth
        k_BM = 0.02 * barnard_scale                    # Barnard seed to Moon
        k_SE = 0.1                                     # Sun UV/Heat to Earth
        
        # Earth to Co-Mag mapping:
        # When w_gate is high, Earth easily dumps energy to the Co-Mag shield.
        # When w_gate is low (3/32), Earth is trapped, forced to process debt internally.
        k_EC = 0.15 * w_gate * DISCRETE_CLOSURE
        k_CM = 0.1 * w_gate                            # Co-Mag to Moon
        k_leak = 0.05                                  # Big Woman void leak
        
        # Metabolic Burn (Earth processing 1.3228 Debt via 1/28 loop)
        # Increases drastically when Moon's protection drops.
        metabolic_stress = (TOTAL_DEBT_AREA / 10.0) * E_E * (1.0 + LOOP_STRENGTH_5 * LUNAR_CYCLE * (1.0 - w_gate))

        # ---------------------------------------------------------
        # Differentials
        # ---------------------------------------------------------
        dE_B = 0  # External source
        dE_S = 0  # External source
        
        dE_E = (k_BE * E_B) + (k_SE * E_S) - (k_EC * E_E) - metabolic_stress
        dE_C = (k_EC * E_E) - (k_CM * E_C) - (k_leak * E_C)
        dE_M = (k_BM * E_B) + (k_CM * E_C) - (0.05 * E_M)
        
        # Spark Reset Condition (138.88 Beam)
        spark_fired = 0
        if E_E > (REALITY_TENSION * 0.4): # Arbitrary stress threshold for the model
            # Earth discharges stress via the Spark Angle geometry
            dE_E -= (COMPRESSION_GATE * E_E)
            spark_fired = 1
            
        # Update state (Euler integration step dt=1.0 for simplicity of coefficients)
        dt = 1.0
        state = state + np.array([dE_B, dE_S, dE_E, dE_M, dE_C]) * dt
        
        history.append({
            "Time(Ga_ago)": round(age_Ga, 2),
            "Barnard_Scale": round(barnard_scale, 4),
            "Moon_w_gate": round(w_gate, 4),
            "Kink_State": kink_state,
            "Is_Mobius_Kink": is_mobius_kink,
            "Spark_Fired": spark_fired,
            "E_B (Barnard)": round(E_B, 4),
            "E_S (Sun)": round(E_S, 4),
            "E_E (Earth/Stress)": round(E_E, 4),
            "E_M (Moon)": round(E_M, 4),
            "E_C (Co-Mag)": round(E_C, 4),
            "Metabolic_Burn": round(metabolic_stress, 4)
        })

    df = pd.DataFrame(history)
    output_path = "system_model_5s_output.csv"
    df.to_csv(output_path, index=False)
    
    # Generate a brief summary
    print(f"--- 5-Sphere System Simulation Complete ---")
    print(f"Epoch 1 (Strong Moon, 4.0 Ga): E_E = {df[df['Time(Ga_ago)'] == 4.0]['E_E (Earth/Stress)'].values[0]}")
    print(f"Epoch 2 (Eukaryote Merger, 2.0 Ga): E_E = {df[df['Time(Ga_ago)'] == 2.0]['E_E (Earth/Stress)'].values[0]}")
    print(f"Epoch 3 (Bilaterian Loop, 0.5 Ga): E_E = {df[df['Time(Ga_ago)'] == 0.5]['E_E (Earth/Stress)'].values[0]}")
    print(f"\nUpturning (Möbius Kink) reached 3/32 gate at: {df[df['Is_Mobius_Kink'] == 1]['Time(Ga_ago)'].max()} Ga")
    print(f"Total Sparks fired (138.88 reset events): {df['Spark_Fired'].sum()}")
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    simulate_5_sphere_system()
