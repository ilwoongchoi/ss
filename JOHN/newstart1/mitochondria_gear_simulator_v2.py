import numpy as np
import pandas as pd

# ---------------------------------------------------------
# 1. Gear & Neurochemical Constants (The Packing Logic)
# ---------------------------------------------------------
REALITY_TENSION = 1.0100375    # Barnard's Anchor
DISCRETE_CLOSURE = 1.0000424   # The "Unclosable Gap"
TOTAL_DEBT_AREA = 1.3228       # The Black Hole (Electron Sink) capacity
LOOP_STRENGTH_5 = 5.555492104
LUNAR_CYCLE = 1.0 / 28.0       # Serotonin Rhythm
COMPRESSION_GATE = 3.0 / 32.0   # 0.09375 (Möbius Kink Threshold)
SPARK_ANGLE = 138.88           # Discharge Vector

# ---------------------------------------------------------
# 2. Mitochondria Container Simulation with Spark Reset
# ---------------------------------------------------------
def simulate_mitochondria_gears_stable():
    # Time: 4.5 Ga to 0 Ga (450 steps)
    time_steps = np.arange(0, 45.1, 0.1)
    
    # Initial State: [Barnard_Anchor, Sun_Glutamate, Earth_Mito, Moon_Serotonin, CoMag_GABA]
    # E_E = Earth (Mito Stress), E_M = Moon (Serotonin), E_C = CoMag (GABA)
    state = np.array([1.0, 0.5, 0.2, 0.2, 0.25])
    
    history = []
    spark_events = 0
    
    for t in time_steps:
        age_Ga = 4.5 - (t / 10.0)
        E_B, E_S, E_E, E_M, E_C = state
        
        # 1. Anchor Drift (Barnard influence moving off-axis)
        anchor_drift = 1.0 - np.exp(-t / 25.0)
        effective_anchor = E_B * (1.0 - anchor_drift * 0.15)
        
        # 2. Moon/Serotonin Gear Decay (Dynamo Turnover Mapping)
        if age_Ga >= 3.5:
            w_gate = 1.0  # Perfect Alignment
        elif age_Ga >= 1.5:
            # Linear transition to the 3/32 gate
            w_gate = 1.0 - (1.0 - COMPRESSION_GATE) * ((3.5 - age_Ga) / 2.0)
        else:
            w_gate = COMPRESSION_GATE # Locked in the Möbius Kink
            
        # 3. Geometric Packing & The Black Hole (Electron Sink)
        # Sum of gear lengths: Serotonin(0.3), GABA(0.4), Glutamate(0.3)
        sum_gears = (E_M * 0.3) + (E_C * 0.4) + (E_S * 0.3)
        target_space = E_E * REALITY_TENSION
        
        # The Mismatch Gap creates the Suction (The Black Hole)
        # We add a damping factor to prevent instant explosion while keeping the tension
        mismatch_gap = np.abs(target_space - sum_gears) + (DISCRETE_CLOSURE * 0.1)
        
        # Suction increases as w_gate drops (Serotonin protection lost)
        electron_sink_suction = mismatch_gap * TOTAL_DEBT_AREA * (1.0 + (LOOP_STRENGTH_5 * LUNAR_CYCLE * (1.0 - w_gate)))
        
        # 4. SPARK RESET (The 138.88 Discharge)
        # If Stress (E_E) exceeds the Reality Tension threshold, fire a Spark
        spark_fired = 0
        if E_E > (REALITY_TENSION * 0.35): # Critical Stress Threshold
            # Discharge the stress through the Spark Angle vector
            E_E -= (E_E * COMPRESSION_GATE * 1.5) # Forceful reset
            spark_fired = 1
            spark_events += 1
            
        # 5. Differentials (Interlocking Gear Logic)
        dE_B = 0
        dE_S = 0
        
        # Earth Stress (Mito) gets pushed by Glutamate and sucked by the Sink
        # Damped by GABA (E_C) and intrinsic relaxation
        dE_E = (0.05 * E_S) - (0.03 * E_C * w_gate) + (0.02 * electron_sink_suction) - (0.04 * E_E)
        
        # GABA Membrane (CoMag) gets consumed by trying to shield the Sink
        dE_C = (0.02 * E_E) - (0.05 * E_C * w_gate) - (0.01 * electron_sink_suction)
        
        # Serotonin Gear (Moon) torque depends on Barnard Anchor and w_gate
        dE_M = (0.01 * effective_anchor) - (0.02 * E_M * (1.0 - w_gate))
        
        # Euler Step (dt=0.5 for stability)
        dt = 0.5
        # Update E_E immediately if spark fired to prevent next-step explosion
        state[2] = E_E 
        state = state + np.array([dE_B, dE_S, dE_E, dE_M, dE_C]) * dt
        
        # Floor values at zero
        state = np.maximum(state, 0.0)
        
        history.append({
            "Age(Ga)": round(age_Ga, 2),
            "w_gate": round(w_gate, 4),
            "Gap": round(mismatch_gap, 6),
            "Sink_Suction": round(electron_sink_suction, 4),
            "Mito_Stress": round(state[2], 4),
            "Serotonin": round(state[3], 4),
            "GABA": round(state[4], 4),
            "Spark": spark_fired
        })

    df = pd.DataFrame(history)
    df.to_csv("mitochondria_gear_stable.csv", index=False)
    
    print("--- Stable Mitochondria Gear Simulation ---")
    print(f"Total Spark Reset Events (138.88 Discharge): {spark_events}")
    print(f"Final Mito Stress (0 Ga): {df.iloc[-1]['Mito_Stress']}")
    print(f"Final Serotonin Torque: {df.iloc[-1]['Serotonin']}")
    print(f"Final GABA Membrane: {df.iloc[-1]['GABA']}")
    print(f"Data saved to mitochondria_gear_stable.csv")

if __name__ == "__main__":
    simulate_mitochondria_gears_stable()
