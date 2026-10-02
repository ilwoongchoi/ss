# run_detune_sweep_v5_legs.py
# 4-point detune sweep with hysteresis leg split (A/B)
# Leg A (come/day) = switch_state == False
# Leg B (go/night) = switch_state == True

import numpy as np
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry_package.universal_equation import w_gate, kappa_eff, in_sh_band

# ==============================================================================
# CONFIGURATION
# ==============================================================================
OUTPUT_DIR = "out/detune_sweep_v5_legs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

RNG_SEED = 42

# 4 Test Points
POINTS = [
    {"label": "center_in", "r": 0.1117, "q0": 0.9750},
    {"label": "r_out",     "r": 0.1130, "q0": 0.9750},
    {"label": "q0_out",    "r": 0.1117, "q0": 0.9850},
    {"label": "both_out",  "r": 0.1130, "q0": 0.9850}
]

# Physical Constants
N_ROWS, N_COLS = 16, 16
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = np.radians(SPARK_ANGLE_DEG)
SPARK_LEAP_DIST = 2.5
F_1_32 = 1/32.0
COMPRESSION_GAP = 3.0 * F_1_32

# Field Constants
REALITY_TENSION = 1.0
MALE_HORIZONTAL_AMP = 1.2
TORSION_4D = 0.02
GABA_C_V_APEX = 0.14

# Hysteresis
HYST_TAU_SCALE = 0.5
THRESHOLD_ON_FACTOR = 0.2
THRESHOLD_OFF_FACTOR = 0.3
ALPHA_MAX = 0.5
NIGHT_TAU_LAG = SPARK_ANGLE_DEG / 60.0

# PRODUCTION Spark Gate
SPARK_FUNNEL_X_MIN = 6.0
SPARK_FUNNEL_X_MAX = 10.0
SPARK_GATE_Y_MIN = 10.0

# Lambda0 for probabilistic spark
LAMBDA0 = 20.0

# ==============================================================================
# FIELD
# ==============================================================================
def _v_shape(x, y):
    xn, yn = (x - 8.0) / 8.0, (y - 8.0) / 8.0
    return np.exp(-(xn**2 + yn**2) / (2 * (GABA_C_V_APEX ** 2)))

def universal_field(x, y):
    tx, ty = 3.2, 14.0
    d_terminal = np.sqrt((x - tx)**2 + (y - ty)**2)
    terminal = -2.5 * np.exp(-d_terminal**2 / (2 * 1.5**2))
    drift_x = -TORSION_4D * (y - 8.0)
    drift_y = TORSION_4D * (x - 8.0)
    return (terminal + drift_x + 1.35 * drift_y + 1.2 * _v_shape(x, y)) * MALE_HORIZONTAL_AMP * REALITY_TENSION

def spark_refraction(x, y):
    x_c = round((x - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
    return max(0.0, min(float(N_COLS), x_c + SPARK_LEAP_DIST * np.cos(SPARK_ANGLE_RAD))), y + SPARK_LEAP_DIST * np.sin(SPARK_ANGLE_RAD)

# ==============================================================================
# SIMULATION WITH LEG SPLIT
# ==============================================================================
def run_simulation_with_legs(r, q0, kappa, in_band, lambda0, rng_seed=None, debug=False):
    """
    Run simulation with leg-split instrumentation.
    Leg A = switch_state == False (come/day)
    Leg B = switch_state == True (go/night)
    """
    rng = np.random.RandomState(rng_seed)
    
    x, y = 8.0, 0.0
    memory_y = y
    switch_state = False
    renorm = 1.0
    dt = 0.05
    steps = int(300.0 / dt)
    
    # Per-leg instrumentation
    leg_data = {
        'A': {'contact_count': 0, 'spark_count': 0, 'expected_sparks': 0.0, 'spark_ys': []},
        'B': {'contact_count': 0, 'spark_count': 0, 'expected_sparks': 0.0, 'spark_ys': []}
    }
    
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * F_1_32
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    
    if in_band:
        reset_val = 0.380657
        recovery_rate = 0.05
    else:
        dev = abs(kappa - 1/32.0) / (1/32.0)
        reset_val = min(0.9, 0.380657 + dev * 0.4)
        recovery_rate = 0.02
    
    w_gate_val = w_gate(r, q0)
    p_per_dt = np.clip(lambda0 * w_gate_val * dt, 0.0, 1.0)
    
    trajectory = []
    
    for i in range(steps):
        t = i * dt
        vx = universal_field(x, y)
        
        alpha = max(0.0, min(ALPHA_MAX, dt / (hyst_tau + 1e-6)))
        memory_y = (1.0 - alpha) * memory_y + alpha * y
        lag = memory_y - y
        
        if lag < threshold_on and not switch_state:
            switch_state = True
        elif lag > threshold_on * THRESHOLD_OFF_FACTOR and switch_state:
            switch_state = False
        
        # Determine leg
        leg = 'B' if switch_state else 'A'
        
        # Check funnel contact
        in_funnel = (y > SPARK_GATE_Y_MIN and 
                     SPARK_FUNNEL_X_MIN <= x <= SPARK_FUNNEL_X_MAX)
        
        if in_funnel:
            leg_data[leg]['contact_count'] += 1
            leg_data[leg]['expected_sparks'] += p_per_dt
            
            if rng.rand() < p_per_dt:
                leg_data[leg]['spark_count'] += 1
                leg_data[leg]['spark_ys'].append(y)
                x, y = spark_refraction(x, y)
                renorm = reset_val
                switch_state = False
                memory_y = y
        
        x += vx * renorm * dt
        y += 1.5 * dt
        renorm += (1.0 - renorm) * recovery_rate * dt
        x = max(0, min(N_COLS, x))
        
        trajectory.append({"t": t, "x": x, "y": y, "leg": leg, "in_funnel": in_funnel})
        if y > 10 * N_ROWS: break
    
    return trajectory, leg_data, w_gate_val, p_per_dt

# ==============================================================================
# VISUALIZATION
# ==============================================================================
def plot_spark_leg_comparison(tag, leg_data, output_path):
    """Plot spark events by leg as histogram on y-axis."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_A = leg_data['A']['spark_ys']
    y_B = leg_data['B']['spark_ys']
    
    bins = np.linspace(10, 160, 30)
    
    ax.hist(y_A, bins=bins, alpha=0.6, label=f"Leg A (come/day): {len(y_A)} sparks", color='blue')
    ax.hist(y_B, bins=bins, alpha=0.6, label=f"Leg B (go/night): {len(y_B)} sparks", color='red')
    
    ax.set_xlabel("y position")
    ax.set_ylabel("Spark count")
    ax.set_title(f"Spark Distribution by Hysteresis Leg - {tag}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Saved: {output_path}")

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    print("=" * 70)
    print("Detune Sweep V5 - Hysteresis Leg Split (A/B)")
    print("=" * 70)
    print(f"Lambda0 = {LAMBDA0}")
    print(f"Leg A (come/day) = switch_state == False")
    print(f"Leg B (go/night) = switch_state == True")
    print("=" * 70)
    
    summary_rows = []
    
    for i, pt in enumerate(POINTS):
        tag, r, q0 = pt["label"], pt["r"], pt["q0"]
        print(f"\n--- [{i+1}/4] Running {tag}: r={r}, q0={q0} ---")
        
        kappa = kappa_eff(r, q0)
        in_band = in_sh_band(r, q0)
        
        traj, leg_data, w_gate_val, p_per_dt = run_simulation_with_legs(
            r, q0, kappa, in_band, LAMBDA0, rng_seed=RNG_SEED
        )
        
        # Calculate metrics
        contactA = leg_data['A']['contact_count']
        contactB = leg_data['B']['contact_count']
        sparksA = leg_data['A']['spark_count']
        sparksB = leg_data['B']['spark_count']
        expectedA = leg_data['A']['expected_sparks']
        expectedB = leg_data['B']['expected_sparks']
        
        ratioA = sparksA / contactA if contactA > 0 else 0.0
        ratioB = sparksB / contactB if contactB > 0 else 0.0
        
        total_contacts = contactA + contactB
        total_sparks = sparksA + sparksB
        
        print(f"  w_gate = {w_gate_val:.6f}, p_per_dt = {p_per_dt:.6f}")
        print(f"  Contact A: {contactA}, Sparks A: {sparksA}, Ratio: {ratioA:.4f}")
        print(f"  Contact B: {contactB}, Sparks B: {sparksB}, Ratio: {ratioB:.4f}")
        print(f"  Total: contacts={total_contacts}, sparks={total_sparks}")
        
        # Plot
        plot_path = os.path.join(OUTPUT_DIR, f"SPARK_LEG_COMPARISON_{tag}.png")
        plot_spark_leg_comparison(tag, leg_data, plot_path)
        
        summary_rows.append({
            "point": tag,
            "r": r,
            "q0": q0,
            "w_gate": w_gate_val,
            "kappa": kappa,
            "in_band": in_band,
            "lambda0": LAMBDA0,
            "p_per_dt": p_per_dt,
            "contactA": contactA,
            "contactB": contactB,
            "sparksA": sparksA,
            "sparksB": sparksB,
            "expectedA": expectedA,
            "expectedB": expectedB,
            "ratioA": ratioA,
            "ratioB": ratioB
        })
    
    # Save summary
    df_summary = pd.DataFrame(summary_rows)
    summary_path = os.path.join(OUTPUT_DIR, "summary.csv")
    df_summary.to_csv(summary_path, index=False)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(df_summary.to_string(index=False))
    print(f"\nSaved to: {summary_path}")
    
    # Check band selectivity
    in_band_contacts = df_summary[df_summary['in_band'] == True][['contactA', 'contactB']].sum().sum()
    out_band_contacts = df_summary[df_summary['in_band'] == False][['contactA', 'contactB']].sum().sum()
    
    print("\n" + "=" * 70)
    print("BAND SELECTIVITY (by contact count)")
    print("=" * 70)
    print(f"  In-band total contacts:  {in_band_contacts}")
    print(f"  Out-band total contacts: {out_band_contacts}")
    if out_band_contacts > 0:
        print(f"  Ratio (in/out):          {in_band_contacts/out_band_contacts:.2f}x")
    else:
        print(f"  Ratio (in/out):          inf (out-band suppressed)")
    print("=" * 70)

if __name__ == "__main__":
    main()
