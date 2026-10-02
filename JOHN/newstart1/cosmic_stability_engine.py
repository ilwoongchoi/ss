import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. CORE GEOMETRY & STABILITY CONSTANTS
# ---------------------------------------------------------
REALITY_TENSION = 1.0100375
DISCRETE_CLOSURE = 1.0000424
TOTAL_DEBT_AREA = 1.3228
LOOP_STRENGTH_5 = 5.555492104
LUNAR_CYCLE = 1.0 / 28.0
COMPRESSION_GATE = 3.0 / 32.0   # 0.09375
SPARK_ANGLE = 138.88

# The Void / Self-Sufficiency Constants
# Replacing Oxytocin (Biological Damping) with Pure Void Absorption
OXYTOCIN_DAMPING = 0.0          # Zero emotional friction/exploitation
VOID_CAPACITY = 10.0 * (1.618**3) # Golden ratio capacity for creative bloom

# ---------------------------------------------------------
# 2. COSMIC STABILITY ENGINE
# ---------------------------------------------------------
def run_stability_engine():
    # Time: Days in a year (representing the new daily routine)
    days = np.arange(0, 365.1, 1.0)
    
    # Initial State [BigMan_Conquest, SmallWoman_Stress, Void_Creativity]
    # Starting with high conquest (e.g., Musk/O-Type) and high societal stress
    state = np.array([1.0, 0.8, 0.1])
    
    history = []
    
    for t in days:
        E_BM, E_SW, E_VOID = state
        
        # 1. Systemic Sieve (The 3/32 Filter)
        # Filters out aggressive expansionism into creative potential
        sieve_efficiency = np.sin(t * LUNAR_CYCLE * np.pi) * 0.1 + COMPRESSION_GATE
        
        # 2. Daily Routine Dynamics (Zero Oxytocin Exploitation)
        # O-type conquest desire (E_BM) is redirected. Instead of expanding outward,
        # it is pulled into the Void (E_VOID) via the Pegasus Bridge logic.
        
        dE_BM = - (sieve_efficiency * E_BM) - (OXYTOCIN_DAMPING * E_BM)
        
        # Societal Stress (E_SW) drops as medical/systemic alienation ends.
        # The stress is discharged via 138.88 Spark logic into the Void.
        spark_discharge = 0.0
        if E_SW > (REALITY_TENSION * 0.5):
            spark_discharge = E_SW * (COMPRESSION_GATE * 1.5)
            dE_SW = -spark_discharge - (0.05 * E_SW)
        else:
            dE_SW = -0.01 * E_SW  # Natural gradual calming
            
        # The Void (Creative / Hobby / Self-Sufficient Loop) grows.
        # It absorbs the filtered conquest energy and the discharged societal stress.
        # It is capped by the VOID_CAPACITY to prevent explosive inflation.
        growth_factor = (sieve_efficiency * E_BM) + spark_discharge
        void_saturation = 1.0 - (E_VOID / VOID_CAPACITY)
        
        dE_VOID = growth_factor * void_saturation * DISCRETE_CLOSURE
        
        # Update State
        dt = 1.0
        state = state + np.array([dE_BM, dE_SW, dE_VOID]) * dt
        state = np.maximum(state, 0.0) # Floor at 0
        
        history.append({
            "Day": t,
            "Conquest_Drive_O_Type": round(state[0], 4),
            "Societal_Stress_SW": round(state[1], 4),
            "Creative_Void_Loop": round(state[2], 4)
        })

    df = pd.DataFrame(history)
    df.to_csv("cosmic_stability_daily_routine.csv", index=False)
    
    # ---------------------------------------------------------
    # 3. VISUALIZATION: The Shift to Stability
    # ---------------------------------------------------------
    plt.figure(figsize=(12, 6), facecolor="#0a0a14")
    plt.plot(df['Day'], df['Conquest_Drive_O_Type'], label='Big Man Conquest Drive (e.g., Musk)', color='#ff4444', lw=2)
    plt.plot(df['Day'], df['Societal_Stress_SW'], label='Societal Stress & Alienation (Left Cortisol)', color='#ffaa00', lw=2)
    plt.plot(df['Day'], df['Creative_Void_Loop'], label='Self-Sufficient Creative Void (GABA-B)', color='#00ff88', lw=3)
    
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    
    plt.title("Cosmic Stability Engine: The 1-Year Shift to Zero-Oxytocin Autonomy", color="white", fontsize=16)
    plt.xlabel("Days", color="#cccccc")
    plt.ylabel("Energy / Tension", color="#cccccc")
    
    ax = plt.gca()
    ax.set_facecolor("#050510")
    ax.tick_params(colors='white')
    legend = plt.legend(facecolor="#050510", edgecolor="white")
    for text in legend.get_texts():
        text.set_color("white")
        
    plt.tight_layout()
    output_img = "COSMIC_STABILITY_SHIFT.png"
    plt.savefig(output_img, dpi=300)
    
    print(f"--- Cosmic Stability Engine Executed ---")
    print(f"Initial Conquest Drive: {df.iloc[0]['Conquest_Drive_O_Type']}")
    print(f"Final Conquest Drive: {df.iloc[-1]['Conquest_Drive_O_Type']}")
    print(f"Initial Societal Stress: {df.iloc[0]['Societal_Stress_SW']}")
    print(f"Final Societal Stress: {df.iloc[-1]['Societal_Stress_SW']}")
    print(f"Final Creative Void Energy: {df.iloc[-1]['Creative_Void_Loop']}")
    print(f"\nVisualization saved to {output_img}")
    print("The system has successfully mapped the transition from systemic exploitation to self-sufficient stability.")

if __name__ == "__main__":
    run_stability_engine()
