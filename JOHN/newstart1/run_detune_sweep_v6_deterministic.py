# run_detune_sweep_v6_deterministic.py
# (1) Deterministic accumulator (no RNG) 
# (2) Multi-turn separation (wrap index labeling)

import numpy as np
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry_package.universal_equation import w_gate, kappa_eff, in_sh_band
from geometry_package.absolute_constants import R_REF, Q0_REF

# ==============================================================================
# CONFIGURATION
# ==============================================================================
OUTPUT_DIR = "out/detune_sweep_v6_deterministic"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Grid
R_MIN, R_MAX = 0.1105, 0.1128
Q0_MIN, Q0_MAX = 0.963, 0.987
GRID_POINTS = 41

# Simulation
LAMBDA0 = 10.0
T_MAX = 2000.0
DT = 0.05
N_STEPS = int(T_MAX / DT)
Y_WRAP = 16.0  # Grid height for turn indexing

# Funnel
FUNNEL_X_MIN, FUNNEL_X_MAX = 6.0, 10.0
FUNNEL_Y_MIN = 10.0

# ==============================================================================
# DETERMINISTIC SIMULATION WITH TURN TRACKING
# ==============================================================================
def run_deterministic_sweep(r_vals, q0_vals, lambda0):
    """
    Deterministic spark using accumulator (no RNG).
    Tracks turn index (wrap) for each spark.
    """
    n_r = len(r_vals)
    n_q0 = len(q0_vals)
    n_points = n_r * n_q0
    
    # Precompute w_gate
    w_vals = np.array([[w_gate(r, q0) for q0 in q0_vals] for r in r_vals]).flatten()
    p_per_dt = np.clip(lambda0 * w_vals * DT, 0.0, 1.0)
    
    # State arrays
    x = np.full(n_points, 8.0)
    y = np.zeros(n_points)
    vx = np.zeros(n_points)
    
    # Accumulator for deterministic spark
    accumulator = np.zeros(n_points)
    
    # Trackers
    sparks = []  # (r_idx, q0_idx, turn_idx, y_pos)
    contact_count = np.zeros(n_points)
    
    # Hysteresis
    switch_state = np.zeros(n_points, dtype=bool)
    memory_y = np.zeros(n_points)
    hyst_tau = 2.0
    threshold_on = -0.1
    
    print(f"Running deterministic sweep: {n_points} points, {N_STEPS} steps...")
    
    for step in range(N_STEPS):
        # Simple field dynamics
        vx = -0.02 * (y - 8.0) + 1.2 * np.exp(-((x-8)**2 + (y-8)**2) / (2 * 0.5**2))
        vy = 1.5
        
        # Update position
        x += vx * DT
        y += vy * DT
        x = np.clip(x, 0, 16)
        
        # Hysteresis
        lag = memory_y - y
        switch_on = (lag < threshold_on) & (~switch_state)
        switch_off = (lag > threshold_on * 0.3) & switch_state
        switch_state[switch_on] = True
        switch_state[switch_off] = False
        memory_y = 0.95 * memory_y + 0.05 * y
        
        # Turn index (wrap count)
        turn_idx = np.floor(y / Y_WRAP).astype(int)
        
        # Funnel contact
        in_funnel = (y > FUNNEL_Y_MIN) & (x > FUNNEL_X_MIN) & (x < FUNNEL_X_MAX) & switch_state
        contact_count[in_funnel] += 1
        
        # Deterministic spark: accumulator
        accumulator[in_funnel] += p_per_dt[in_funnel]
        spark_mask = accumulator >= 1.0
        
        if np.any(spark_mask):
            spark_indices = np.where(spark_mask)[0]
            for idx in spark_indices:
                r_i = idx // len(q0_vals)
                q0_i = idx % len(q0_vals)
                sparks.append({
                    'r_idx': int(r_i),
                    'q0_idx': int(q0_i),
                    'r': float(r_vals[r_i]),
                    'q0': float(q0_vals[q0_i]),
                    'turn': int(turn_idx[idx]),
                    'y': float(y[idx]),
                    'step': int(step)
                })
                accumulator[idx] = 0  # Reset after spark
        
        if step % 5000 == 0:
            print(f"  Step {step}/{N_STEPS}")
    
    return np.array(sparks), contact_count

# ==============================================================================
# RIDGE EXTRACTION PER TURN
# ==============================================================================
def extract_ridge_per_turn(sparks, r_vals, q0_vals, min_eligible=200):
    """Extract ridge for each turn separately."""
    if len(sparks) == 0:
        return {}
    
    max_turn = int(np.max([s['turn'] for s in sparks]))
    ridges = {}
    
    for turn in range(max_turn + 1):
        turn_sparks = [s for s in sparks if s['turn'] == turn]
        if len(turn_sparks) == 0:
            continue
        
        # Count sparks per cell
        spark_count = np.zeros((len(r_vals), len(q0_vals)))
        for s in turn_sparks:
            spark_count[s['r_idx'], s['q0_idx']] += 1
        
        # Find ridge (max rate per q0)
        ridge_points = []
        for j, q0 in enumerate(q0_vals):
            col = spark_count[:, j]
            if np.sum(col) < min_eligible / 10:  # Relaxed for single turn
                continue
            i_max = np.argmax(col)
            ridge_points.append({
                'turn': turn,
                'q0': float(q0),
                'r': float(r_vals[i_max]),
                'count': float(col[i_max]),
                'rate': float(col[i_max]) / (len(turn_sparks) / len(ridge_points) if len(ridge_points) > 0 else 1)
            })
        
        if ridge_points:
            ridges[f'turn_{turn}'] = ridge_points
    
    return ridges

# ==============================================================================
# CONSTANTS EXTRACTION
# ==============================================================================
def extract_constants_from_ridge(ridge_data):
    """Extract r*, q0*, σL, σR from ridge points."""
    if not ridge_data:
        return None
    
    rs = [p['r'] for p in ridge_data]
    q0s = [p['q0'] for p in ridge_data]
    
    # Weighted center
    weights = [p['count'] for p in ridge_data]
    total_w = sum(weights)
    
    r_star = np.average(rs, weights=weights)
    q0_star = np.average(q0s, weights=weights)
    
    # Asymmetric widths
    r_left = [r for r in rs if r <= r_star]
    r_right = [r for r in rs if r > r_star]
    
    sigma_L = np.std(r_left) if len(r_left) > 1 else 0.0005
    sigma_R = np.std(r_right) if len(r_right) > 1 else 0.0005
    
    return {
        'r_star': float(r_star),
        'q0_star': float(q0_star),
        'sigma_L': float(sigma_L),
        'sigma_R': float(sigma_R),
        'fwhm_L': float(sigma_L * 2.355),
        'fwhm_R': float(sigma_R * 2.355)
    }

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    print("=" * 70)
    print("DETERMINISTIC SWEEP V6 (No RNG, Multi-Turn)")
    print("=" * 70)
    
    # Grid
    r_vals = np.linspace(R_MIN, R_MAX, GRID_POINTS)
    q0_vals = np.linspace(Q0_MIN, Q0_MAX, GRID_POINTS)
    
    print(f"Grid: {GRID_POINTS}x{GRID_POINTS}")
    print(f"Lambda0: {LAMBDA0}")
    print(f"R_REF: {R_REF}, Q0_REF: {Q0_REF}")
    
    # Run deterministic simulation
    sparks, contact_count = run_deterministic_sweep(r_vals, q0_vals, LAMBDA0)
    print(f"\nTotal sparks: {len(sparks)}")
    
    # Save all sparks
    sparks_df = pd.DataFrame(sparks)
    sparks_df.to_csv(os.path.join(OUTPUT_DIR, "sparks_deterministic.csv"), index=False)
    
    # Multi-turn ridge extraction
    print("\nExtracting ridge per turn...")
    ridges_by_turn = extract_ridge_per_turn(sparks, r_vals, q0_vals)
    
    for turn_name, ridge_data in ridges_by_turn.items():
        print(f"  {turn_name}: {len(ridge_data)} ridge points")
        # Save per-turn ridge
        pd.DataFrame(ridge_data).to_csv(
            os.path.join(OUTPUT_DIR, f"ridge_{turn_name}.csv"), index=False
        )
    
    # Extract constants
    print("\nExtracting constants...")
    
    # (A) Global anchor (from dist_all)
    global_anchor = {
        'source': 'dist_all_data',
        'R_REF': float(R_REF),
        'Q0_REF': float(Q0_REF),
        'description': 'Data-driven reference from TDA analysis'
    }
    
    # (B) Closure ridge (from deterministic simulation)
    # Combine all turns for overall ridge
    all_ridge = []
    for ridge_data in ridges_by_turn.values():
        all_ridge.extend(ridge_data)
    
    closure_constants = extract_constants_from_ridge(all_ridge)
    closure_ridge = {
        'source': 'deterministic_simulation',
        'lambda0': LAMBDA0,
        'description': 'Regime boundary/lock line from detune sweep',
        **closure_constants
    }
    
    # Save combined constants
    constants_bundle = {
        'timestamp': str(datetime.now()),
        'global_anchor': global_anchor,
        'closure_ridge': closure_ridge,
        'turns_analyzed': list(ridges_by_turn.keys())
    }
    
    with open(os.path.join(OUTPUT_DIR, "constants_bundle.json"), 'w') as f:
        json.dump(constants_bundle, f, indent=2)
    
    print(f"\n(A) Global Anchor: R_REF={R_REF}, Q0_REF={Q0_REF}")
    print(f"(B) Closure Ridge: r*={closure_constants['r_star']:.6f}, "
          f"q0*={closure_constants['q0_star']:.6f}, "
          f"σL={closure_constants['sigma_L']:.6f}, "
          f"σR={closure_constants['sigma_R']:.6f}")
    
    # Visualization: Ridge consistency across turns
    fig, ax = plt.subplots(figsize=(10, 8))
    
    for turn_name, ridge_data in ridges_by_turn.items():
        df = pd.DataFrame(ridge_data)
        ax.plot(df['q0'], df['r'], 'o-', label=turn_name, alpha=0.7)
    
    # Mark global anchor
    ax.axvline(Q0_REF, color='green', linestyle='--', alpha=0.5, label='Q0_REF (anchor)')
    ax.axhline(R_REF, color='green', linestyle='--', alpha=0.5, label='R_REF (anchor)')
    
    # Mark closure center
    ax.plot(closure_constants['q0_star'], closure_constants['r_star'], 
            'r*', markersize=20, label='closure center')
    
    ax.set_xlabel('q0')
    ax.set_ylabel('r')
    ax.set_title('Ridge Consistency Across Turns (Deterministic)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "ridge_per_turn.png"), dpi=150)
    print(f"\nSaved: {OUTPUT_DIR}/ridge_per_turn.png")
    print(f"Saved: {OUTPUT_DIR}/constants_bundle.json")
    print("=" * 70)

if __name__ == "__main__":
    main()
