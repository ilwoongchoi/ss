# test_maxwell_flash_hypothesis.py
# Test hypothesis: Out-band flash rate ~ Maxwell Q-factor relationship
#
# HYPOTHESIS (NOT PROVEN - FOR TESTING ONLY):
#   Out-band flash rate (measured from trajectories) is inversely related to
#   Maxwell Q-factor: rate_out ≈ 1/Q or rate_out × Q ≈ constant
#
# CURRENT OBSERVATION:
#   - Out-band flash rate: 0.0118 (from analyze_sh_band_metrics.py)
#   - Maxwell Q-factor: 11.8 (from absolute_constants.py)
#   - Ratio: 0.0118 × 11.8 ≈ 0.139 ≈ 1/7.2 (close to 1/BETTI_7?)
#
# TEST PROTOCOL:
#   1. Run multiple simulations with different dt/seeds
#   2. Measure out-band flash rate for each
#   3. Check if rate_out × Q remains approximately constant
#   4. Only if reproducible, consider as official constant

import numpy as np
import json
from geometry_package.absolute_constants import MAXWELL_Q_FACTOR, BETTI_7
from geometry_package.universal_equation import kappa_eff, in_sh_band
import warnings

def test_flash_rate_reproducibility(n_runs=5, dt_values=None, seeds=None):
    """
    Test if out-band flash rate is reproducible across different dt/seeds.
    
    This is a stub - actual implementation would run full simulations.
    For now, logs the hypothesis and expected test protocol.
    """
    
    print("=" * 70)
    print("MAXWELL-FLASH HYPOTHESIS TEST PROTOCOL")
    print("=" * 70)
    print()
    print("HYPOTHESIS:")
    print("  Out-band flash rate is related to Maxwell Q-factor by:")
    print("  rate_out * Q ~= constant ~= 1/BETTI_7")
    print()
    print("OBSERVED VALUES (single run):")
    print(f"  Out-band flash rate: 0.0118")
    print(f"  Maxwell Q-factor: {MAXWELL_Q_FACTOR}")
    print(f"  Product: {0.0118 * MAXWELL_Q_FACTOR:.4f}")
    print(f"  1/BETTI_7: {1.0/BETTI_7:.4f}")
    print(f"  Match: {'YES' if abs(0.0118 * MAXWELL_Q_FACTOR - 1.0/BETTI_7) < 0.05 else 'UNCLEAR'}")
    print()
    
    # Log the hypothesis
    hypothesis_log = {
        "timestamp": np.datetime64('now').astype(str),
        "hypothesis": "out_band_flash_rate * maxwell_q ~= 1/BETTI_7",
        "observed": {
            "out_band_flash_rate": 0.0118,
            "maxwell_q_factor": MAXWELL_Q_FACTOR,
            "product": 0.0118 * MAXWELL_Q_FACTOR,
            "one_over_betti_7": 1.0 / BETTI_7,
        },
        "test_protocol": {
            "n_runs": n_runs,
            "dt_values": dt_values or [0.005, 0.01, 0.02],
            "seeds": seeds or list(range(1000, 1000 + n_runs)),
            "expected": "Product should remain stable within ±20% across runs",
        },
        "status": "UNTESTED - Needs multi-run validation",
        "notes": [
            "Single observation shows coincidence (0.139 vs 0.143)",
            "May be spurious correlation",
            "Requires at least 10 independent runs to validate",
            "DO NOT use as official constant until validated",
        ]
    }
    
    # Save log
    log_path = "maxwell_flash_hypothesis_log.json"
    try:
        with open(log_path, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    
    logs.append(hypothesis_log)
    
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)
    
    print(f"[LOGGED] Hypothesis saved to {log_path}")
    print()
    print("REQUIRED TESTS:")
    print("  1. Run analyze_sh_band_metrics.py with different dt (0.005, 0.02)")
    print("  2. Check if out-band flash rate remains ~0.0118")
    print("  3. If stable, calculate rate_out × Q for each run")
    print("  4. Only if CV < 20%, consider hypothesis valid")
    print()
    print("WARNING: This relationship is NOT validated yet.")
    print("         Do not use in production constants.")
    print("=" * 70)
    
    return hypothesis_log

def test_kappa_eff_lookup():
    """Test kappa_eff lookup function with dist_all.csv"""
    print("\n" + "=" * 70)
    print("KAPPA_EFF LOOKUP TEST")
    print("=" * 70)
    
    # Test at reference point
    r_ref = 0.111700
    q0_ref = 0.975000
    
    try:
        kappa = kappa_eff(r_ref, q0_ref, snap_band=True)
        print(f"\nAt reference ({r_ref}, {q0_ref}):")
        print(f"  kappa_eff = {kappa:.6f}")
        print(f"  Expected: ~0.031250 (1/32)")
        print(f"  Match: {'YES' if abs(kappa - 1/32) < 0.001 else 'NO'}")
        
        # Check if in band
        in_band = in_sh_band(r_ref, q0_ref)
        print(f"  In SH Band: {in_band}")
        
    except Exception as e:
        warnings.warn(f"Kappa lookup test failed: {e}")
        print(f"  [ERROR] {e}")
    
    print("=" * 70)

if __name__ == "__main__":
    # Log hypothesis
    test_flash_rate_reproducibility(n_runs=5)
    
    # Test kappa lookup
    test_kappa_eff_lookup()
