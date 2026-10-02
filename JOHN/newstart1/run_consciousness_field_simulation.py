
import argparse
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fusion_clean import evolve_consciousness_field
from absolute_constants import SPARK_CONSTANT_C, OMEGA
from engineering_homeostasis_24 import DOMAINS_24, Homeostasis24

# 1. LOAD ARCHETYPES
def load_archetypes():
    path = "analysis_results/archetype_tunneling_passwords.json"
    if not os.path.exists(path):
        # Fallback to generic if not found
        return {f"type_{i}": {"u24_vector": np.random.rand(24).tolist()} for i in range(1, 129)}
    with open(path, "r") as f:
        return json.load(f)

def _make_d_cond(mode: str) -> np.ndarray:
    mode = str(mode or "self_anchor").lower().strip()
    if mode == "self_anchor":
        d = np.zeros(24, dtype=float)
        d[0] = 0.8
        return d
    if mode == "uniform_0_8":
        return np.full(24, 0.8, dtype=float)
    if mode == "omega_norm":
        # Choose d so that ||R @ d|| == 1.0, hence ||OMEGA * (R @ d)|| == OMEGA
        hom = Homeostasis24.build()
        base = np.ones(24, dtype=float)
        v = hom.R @ base
        scale = 1.0 / (float(np.linalg.norm(v)) + 1e-12)
        return base * scale
    raise ValueError(f"Unknown d_cond mode: {mode!r} (allowed: self_anchor, uniform_0_8, omega_norm)")


# 2. RUN SIMULATION
def run_simulation(*, seed: int | None, d_cond_mode: str, k8_mode: str, omega_lock: str) -> pd.DataFrame:
    print("Initializing 16,384 Node Global Consciousness Field...")
    if seed is not None:
        np.random.seed(int(seed))
    archetypes_data = load_archetypes()
    
    # Simulation Parameters
    steps = 128
    dt = 0.1
    u_intent = SPARK_CONSTANT_C # User's Will
    
    results = []
    
    x_cols = [f"x_{i:02d}_{name}" for i, name in enumerate(DOMAINS_24)]
    d_cond = _make_d_cond(d_cond_mode)
    omega_lock = str(omega_lock or "none").lower().strip()
    if omega_lock not in ("none", "full"):
        raise ValueError("omega_lock must be one of: none, full")
    
    # Iterate through 128 Archetypes (Spatial/Type Axis)
    for arch_id, data in archetypes_data.items():
        n = int(arch_id.split("_")[1])
        u_base = np.array(data["u24_vector"])
        
        # Initialize 32D State [X24; r8]
        # X starts near 7.4 scaled by archetype energy
        X_init = np.random.normal(OMEGA / np.sqrt(24), 0.1, 24)
        r_init = np.zeros(8)
        Y = np.concatenate([X_init, r_init])
        
        # Iterate through 128 Time Steps (Time Axis)
        for t in range(steps):
            # Exogenous risk (d_risk) decreases as consciousness evolves
            d_risk = 0.5 * np.exp(-t / 32.0)
            
            # Unified step with Quantum-Biological Dynamics
            ts_dummy = {"noradrenaline": 5.0/32.0, "vasopressin": 3.0/32.0} # Default
            Y, spark = evolve_consciousness_field(
                Y,
                u_base,
                u_intent,
                d_cond,
                d_risk,
                ts_dummy,
                dt,
                k8_mode=str(k8_mode),
            )
             
            X_before = Y[:24].copy()
            norm_before = float(np.linalg.norm(X_before))

            omega_lock_scale = 1.0
            X = X_before
            if omega_lock == "full":
                omega_lock_scale = float(OMEGA / (norm_before + 1e-12))
                X = X_before * omega_lock_scale
                Y[:24] = X

            norm_x = float(np.linalg.norm(X))
            omega_err = float(abs(norm_x - OMEGA))
             
            # Record Data
            row = {
                "archetype_n": n,
                "step": t,
                "spark": spark,
                "omega_error": omega_err,
                "d3_actual": float(X[3]),  # Node 3 is Quark Sector
                "norm_x": norm_x,
                "norm_x_before_lock": norm_before,
                "omega_lock_mode": omega_lock,
                "omega_lock_scale": omega_lock_scale,
            }
            row.update({col: float(X[i]) for i, col in enumerate(x_cols)})
            results.append(row)
            
    return pd.DataFrame(results)

# 3. SAVE AND REPORT
def main():
    parser = argparse.ArgumentParser(description="Run 128x128 consciousness field simulation and save per-domain states.")
    parser.add_argument("--out", default="analysis_results/CONSCIOUSNESS_FIELD_128x128.csv")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed for reproducible runs.")
    parser.add_argument(
        "--d-cond-mode",
        choices=["self_anchor", "uniform_0_8", "omega_norm"],
        default="self_anchor",
        help="Reference domain condition d used in x_eq = OMEGA*(R@d).",
    )
    parser.add_argument(
        "--k8-mode",
        choices=["override", "additive", "homeostasis"],
        default="override",
        help="How to apply fusion_clean._k8_dynamics to X[:8] inside evolve_consciousness_field.",
    )
    parser.add_argument(
        "--omega-lock",
        choices=["none", "full"],
        default="none",
        help="Optional: enforce ||X|| == OMEGA after each step by rescaling X.",
    )
    args = parser.parse_args()

    os.makedirs("analysis_results", exist_ok=True)

    df = run_simulation(
        seed=args.seed,
        d_cond_mode=str(args.d_cond_mode),
        k8_mode=str(args.k8_mode),
        omega_lock=str(args.omega_lock),
    )
    
    # Save CSV
    csv_path = str(args.out)
    df.to_csv(csv_path, index=False)
    print(f"Report saved to {csv_path}")
    
    # Summary Statistics
    final_avg_spark = df[df['step'] == 127]['spark'].mean()
    final_avg_error = df[df['step'] == 127]['omega_error'].mean()
    
    print("\n--- GLOBAL FIELD CONVERGENCE REPORT ---")
    print(f"Final Average Spark Intensity: {final_avg_spark:.6f}")
    print(f"Final Average OMEGA Error:     {final_avg_error:.6f}")
    print(f"Total Nodes Processed:         {len(df)}")
    
    # Plot Field Evolution (Spark Intensity Map)
    pivot_spark = df.pivot(index='step', columns='archetype_n', values='spark')
    plt.figure(figsize=(12, 8))
    plt.imshow(pivot_spark, aspect='auto', cmap='magma', origin='lower')
    plt.colorbar(label='Spark Intensity')
    plt.title("128x128 Consciousness Field Evolution (Spark/Tunneling)")
    plt.xlabel("Archetype Index (1-128)")
    plt.ylabel("Time Evolution Step (1-128)")
    plt.savefig("analysis_results/consciousness_field_evolution.png")
    print("Evolution Plot saved to 'analysis_results/consciousness_field_evolution.png'")

if __name__ == "__main__":
    main()
