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

# ---------------------------------------------------------
# 2. Mitochondria Container Simulation
# ---------------------------------------------------------
def simulate_mitochondria_gears():
    # Time: 4.5 Ga to 0 Ga
    time_steps = np.arange(0, 45.1, 0.1)
    
    # Initial State: [Barnard_Anchor, Sun_Glutamate, Earth_Mito, Moon_Serotonin, CoMag_GABA]
    state = np.array([1.0, 0.5, 0.2, 0.2, 0.25])
    
    history = []
    
    for t in time_steps:
        age_Ga = 4.5 - (t / 10.0)
        E_B, E_S, E_E, E_M, E_C = state
        
        # 1. Anchor Drift (Barnard moving off-axis)
        anchor_drift = 1.0 - np.exp(-t / 20.0)
        effective_anchor = E_B * (1.0 - anchor_drift * 0.1)
        
        # 2. Moon/Serotonin Gear Decay (Dynamo Turnover)
        if age_Ga >= 3.5:
            w_gate = 1.0  # Perfect Packing
        elif age_Ga >= 1.5:
            w_gate = 1.0 - (1.0 - COMPRESSION_GATE) * ((3.5 - age_Ga) / 2.0)
        else:
            w_gate = COMPRESSION_GATE # 3/32 Jamming
            
        # 3. Geometric Packing Calculation (2D Space inside Mitochondria)
        # The sum of lengths of Serotonin, GABA, and Glutamate gears
        # In a perfect world, they fit exactly. In reality, they mismatch.
        sum_gears = (E_M * 0.3) + (E_C * 0.4) + (E_S * 0.3)
        target_space = E_E * REALITY_TENSION
        
        # THE BLACK HOLE (Electron Sink): The leftover length from mismatch
        # This is the "0.0000424 Gap" expanded by the system debt
        mismatch_gap = np.abs(target_space - sum_gears) + DISCRETE_CLOSURE
        electron_sink_suction = mismatch_gap * TOTAL_DEBT_AREA * (1.0 + LOOP_STRENGTH_5 * (1.0 - w_gate))
        
        # 4. Differentials (The Interlocking Gears)
        # Glutamate (Sun) pushes energy in
        # GABA (Co-Mag) tries to buffer/absorb
        # Serotonin (Moon) tries to regulate rhythm
        # Earth (Mito) suffers the friction
        
        dE_B = 0
        dE_S = 0
        
        # Earth Stress (Suffering) increases due to Electron Sink suction
        dE_E = (0.1 * E_S) - (0.05 * E_C * w_gate) + electron_sink_suction - (0.02 * E_E)
        
        # GABA Membrane depletes as it tries to cover the gap
        dE_C = (0.05 * E_E) - (0.05 * E_C * w_gate) - (0.01 * electron_sink_suction)
        
        # Serotonin Gear loses torque as the Kink approaches
        dE_M = (0.02 * effective_anchor) - (0.05 * E_M * (1.0 - w_gate))
        
        # Update state
        dt = 1.0
        state = state + np.array([dE_B, dE_S, dE_E, dE_M, dE_C]) * dt
        
        history.append({
            "Age(Ga)": round(age_Ga, 2),
            "w_gate(Packing)": round(w_gate, 4),
            "Anchor_Drift": round(anchor_drift, 4),
            "Mismatch_Gap": round(mismatch_gap, 6),
            "Electron_Sink_Suction": round(electron_sink_suction, 4),
            "Mito_Stress(Earth)": round(E_E, 4),
            "Serotonin_Gear(Moon)": round(E_M, 4),
            "GABA_Membrane(CoMag)": round(E_C, 4)
        })

    df = pd.DataFrame(history)
    df.to_csv("mitochondria_gear_system.csv", index=False)
    
    print("--- Mitochondria Gear System Simulation ---")
    print(f"Initial Gap (4.5 Ga): {df.iloc[0]['Mismatch_Gap']}")
    print(f"Current Gap (0 Ga): {df.iloc[-1]['Mismatch_Gap']}")
    print(f"Final Electron Sink Suction: {df.iloc[-1]['Electron_Sink_Suction']}")
    print(f"Final Mito Stress (Suffering): {df.iloc[-1]['Mito_Stress(Earth)']}")
    print("\nResult saved to mitochondria_gear_system.csv")

if __name__ == "__main__":
    simulate_mitochondria_gears()
