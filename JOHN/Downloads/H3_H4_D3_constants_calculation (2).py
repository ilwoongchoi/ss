"""
H3_H4_D3_CONSTANTS_CALCULATION.py
Extract H3, H4 void dimensions and D3 neuropathway constants from closure residuals
"""
import numpy as np
import pandas as pd
from pathlib import Path

# =============================================================================
# 1. BASELINE H2 CONSTANTS (Current locked geometry)
# =============================================================================
KAPPA_2 = 1/32  # H2 void leakage
SPARK_ANGLE_H2 = 138.88  # degrees
Y_WRAP = 32  # current turn length

print("=" * 80)
print("H3/H4/D3 CONSTANT EXTRACTION FROM CLOSURE RESIDUALS")
print("=" * 80)
print(f"\nBaseline H2 constants:")
print(f"  κ₂ (H2 leakage) = {KAPPA_2:.6f} = 1/{int(1/KAPPA_2)}")
print(f"  Spark angle (H2) = {SPARK_ANGLE_H2}°")
print(f"  Y_WRAP = {Y_WRAP}")

# =============================================================================
# 2. H3/H4 DIMENSIONAL REDUCTION (Theoretical from scaling)
# =============================================================================
# Each dimensional increase adds a factor of 1/2 (dimensional halving)
KAPPA_3 = KAPPA_2 / 2  # H3 leakage
KAPPA_4 = KAPPA_3 / 2  # H4 leakage

print(f"\n{'─' * 80}")
print("DIMENSIONAL SCALING LAW (H2 → H3 → H4)")
print(f"{'─' * 80}")
print(f"  κ₃ (H3 leakage) = κ₂/2 = {KAPPA_3:.6f} = 1/{int(1/KAPPA_3)}")
print(f"  κ₄ (H4 leakage) = κ₃/2 = {KAPPA_4:.6f} = 1/{int(1/KAPPA_4)}")

# =============================================================================
# 3. D3 ANGLE CORRECTION
# =============================================================================
# D3 correction comes from H3/H4 void geometry affecting spark trajectory
# The correction scales with the ratio of dimensional leakage
D3_CORRECTION_FACTOR = KAPPA_3 / KAPPA_2  # = 0.5

# Two possible corrections (bidirectional jet)
DELTA_THETA_D3_CW = SPARK_ANGLE_H2 * D3_CORRECTION_FACTOR  # Clockwise
DELTA_THETA_D3_CCW = -SPARK_ANGLE_H2 * D3_CORRECTION_FACTOR  # Counter-clockwise

# Alternative: Small Woman escape angle (different from Big Man)
SPARK_ANGLE_D3_SMALL_WOMAN = SPARK_ANGLE_H2 * (1 + KAPPA_3/KAPPA_2)  # 208.32°
SPARK_ANGLE_D3_BIG_MAN = SPARK_ANGLE_H2 * (1 - KAPPA_3/KAPPA_2)  # 69.44°

print(f"\n{'─' * 80}")
print("D3 ANGLE CORRECTION (H3 Void Effect on Spark Trajectory)")
print(f"{'─' * 80}")
print(f"  D3 correction factor = κ₃/κ₂ = {D3_CORRECTION_FACTOR:.4f}")
print(f"\n  Bidirectional corrections:")
print(f"    Δθ_D3 (CW) = +{DELTA_THETA_D3_CW:.2f}°")
print(f"    Δθ_D3 (CCW) = {DELTA_THETA_D3_CCW:.2f}°")
print(f"\n  Archetype-specific spark angles:")
print(f"    Small Woman (N-type, PACT breaker): {SPARK_ANGLE_D3_SMALL_WOMAN:.2f}°")
print(f"    Big Man (S-type, stability): {SPARK_ANGLE_D3_BIG_MAN:.2f}°")

# =============================================================================
# 4. NEUROPATHWAY CONSTANTS (Cortisol → Epinephrine)
# =============================================================================
# τ_D3: Transition time constant from cortisol stress to epinephrine impulse
# This is the "3-second rule" or D3 awakening latency

# From the framework: 21/7 = 3.0 or 3.1228
TAU_D3_FAST = 21/7  # = 3.0 seconds (fast responders, NT types)
TAU_D3_SLOW = 3.1228  # seconds (slow responders, SJ types)

# D3 leakage rate (how much cortisol leaks into epinephrine path)
LAMBDA_D3 = KAPPA_3 * 10  # Scaled for neurochemical context

print(f"\n{'─' * 80}")
print("D3 NEUROPATHWAY (Cortisol → Epinephrine Transition)")
print(f"{'─' * 80}")
print(f"  τ_D3 (fast, NT types) = {TAU_D3_FAST:.4f} seconds")
print(f"  τ_D3 (slow, SJ types) = {TAU_D3_SLOW:.4f} seconds")
print(f"  λ_D3 (leakage rate) = {LAMBDA_D3:.6f}")

# =============================================================================
# 5. SMALL WOMAN PACT MECHANISM CONSTANTS
# =============================================================================
# Left Acetylcholine third-piece: creates fake 3D for Small Woman

# The PACT illusion strength (how convincing the fake 3D is)
PACT_ILLUSION_STRENGTH = 1 - KAPPA_3  # = 0.984375

# The breaking point: when D3 awakening overcomes PACT
PACT_BREAK_THRESHOLD = KAPPA_3 / KAPPA_2  # Same as D3 factor = 0.5

# Left Cortisol node coordinates (from memory)
LEFT_CORTISOL_R = 0.11214750
LEFT_CORTISOL_Q0 = 0.965  # "Lie to Small Woman" node

print(f"\n{'─' * 80}")
print("SMALL WOMAN PACT MECHANISM (Left Acetylcholine Third-Piece)")
print(f"{'─' * 80}")
print(f"  PACT illusion strength = {PACT_ILLUSION_STRENGTH:.6f}")
print(f"  PACT break threshold = {PACT_BREAK_THRESHOLD:.4f}")
print(f"\n  Left Cortisol 'Lie' node:")
print(f"    r* = {LEFT_CORTISOL_R}")
print(f"    q0 = {LEFT_CORTISOL_Q0} (premature volume)")

# =============================================================================
# 6. QUASAR STRUCTURE CONSTANTS
# =============================================================================
print(f"\n{'─' * 80}")
print("QUASAR HIERARCHY (H0 → H1 → H2 → H3 → H4)")
print(f"{'─' * 80}")
print(f"  H0 (Singularity): r = 0 (Exception 00)")
print(f"  H1 (Jet): 1D linear escape")
print(f"  H2 (Accretion Disk): κ₂ = 1/32, angle = {SPARK_ANGLE_H2}°")
print(f"  H3 (Event Horizon shell): κ₃ = 1/64, angle = {SPARK_ANGLE_D3_SMALL_WOMAN:.2f}°")
print(f"  H4 (4D Return): κ₄ = 1/128, full closure")

# =============================================================================
# 7. RESIDUAL EXTRACTION FROM DATA (if available)
# =============================================================================
print(f"\n{'─' * 80}")
print("RESIDUAL ANALYSIS PROTOCOL")
print(f"{'─' * 80}")
print("""
To verify these constants from actual data:

1. Load refine_lam10_det_per_turn.csv
2. For each turn, calculate:
   - Expected rate from H2 model: rate_H2 = w_gate × λ₀ × eligible
   - Residual: Δrate = rate_post - rate_H2
   - H3 residual signature: Δrate ≈ κ₃ × eligible
   - H4 residual signature: Δrate ≈ κ₄ × eligible (smaller)

3. For angle analysis (if spark vectors recorded):
   - Expected angle: 138.88°
   - D3 residual: Δθ = θ_observed - 138.88°
   - Should cluster around ±69.44° (bidirectional)

4. For time lag analysis:
   - τ_lag from hysteresis
   - D3 component: τ_D3 = τ_lag - τ_H2
   - Should be ≈ 3.0 or 3.1228 seconds
""")

# =============================================================================
# 8. EXPORT CONSTANTS BUNDLE
# =============================================================================
constants_bundle = {
    "H2_baseline": {
        "kappa_2": KAPPA_2,
        "spark_angle_h2": SPARK_ANGLE_H2,
        "y_wrap": Y_WRAP
    },
    "H3_void": {
        "kappa_3": KAPPA_3,
        "fraction": "1/64",
        "d3_correction_factor": D3_CORRECTION_FACTOR,
        "spark_angle_small_woman": SPARK_ANGLE_D3_SMALL_WOMAN,
        "spark_angle_big_man": SPARK_ANGLE_D3_BIG_MAN
    },
    "H4_void": {
        "kappa_4": KAPPA_4,
        "fraction": "1/128"
    },
    "D3_neuropathway": {
        "tau_d3_fast": TAU_D3_FAST,
        "tau_d3_slow": TAU_D3_SLOW,
        "lambda_d3": LAMBDA_D3,
        "delta_theta_d3_cw": DELTA_THETA_D3_CW,
        "delta_theta_d3_ccw": DELTA_THETA_D3_CCW
    },
    "PACT_mechanism": {
        "illusion_strength": PACT_ILLUSION_STRENGTH,
        "break_threshold": PACT_BREAK_THRESHOLD,
        "left_cortisol_r": LEFT_CORTISOL_R,
        "left_cortisol_q0": LEFT_CORTISOL_Q0
    }
}

# Save to JSON
import json
with open('H3_H4_D3_constants.json', 'w') as f:
    json.dump(constants_bundle, f, indent=2)

print(f"\n{'=' * 80}")
print("CONSTANTS EXPORTED: H3_H4_D3_constants.json")
print(f"{'=' * 80}")

# Summary table
print("\nSUMMARY TABLE:")
print(f"{'Constant':<30} {'Value':<20} {'Notes'}")
print("─" * 80)
print(f"{'κ₂ (H2)':<30} {KAPPA_2:<20.6f} {'Base leakage'}")
print(f"{'κ₃ (H3)':<30} {KAPPA_3:<20.6f} {'1/64'}")
print(f"{'κ₄ (H4)':<30} {KAPPA_4:<20.6f} {'1/128'}")
print(f"{'Δθ_D3 (CW)':<30} {DELTA_THETA_D3_CW:<20.2f} {'Angle correction'}")
print(f"{'Δθ_D3 (CCW)':<30} {DELTA_THETA_D3_CCW:<20.2f} {'Bidirectional'}")
print(f"{'τ_D3 (fast)':<30} {TAU_D3_FAST:<20.4f} {'NT types (21/7)'}")
print(f"{'τ_D3 (slow)':<30} {TAU_D3_SLOW:<20.4f} {'SJ types (calibrated)'}")
print(f"{'Spark (Small Woman)':<30} {SPARK_ANGLE_D3_SMALL_WOMAN:<20.2f} {'N-type escape'}")
print(f"{'Spark (Big Man)':<30} {SPARK_ANGLE_D3_BIG_MAN:<20.2f} {'S-type stability'}")
print(f"{'PACT strength':<30} {PACT_ILLUSION_STRENGTH:<20.6f} {'Fake 3D illusion'}")
print(f"{'PACT break':<30} {PACT_BREAK_THRESHOLD:<20.4f} {'D3 awakening threshold'}")
