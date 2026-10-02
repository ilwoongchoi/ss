# -*- coding: utf-8 -*-
"""
absolute_constants.py
=====================
Zero-Error Mathematical Skeleton for the Geometry Manifold.
All physical/empirical data must snap to these exact mathematical limits.
"""

import math

# ---------------------------------------------------------
# 0. FUNDAMENTAL CONSTANTS (The Sieve Roots)
# ---------------------------------------------------------
PHI = (1.0 + math.sqrt(5.0)) / 2.0  # The Golden Ratio
ALPHA = 1.0 / 137.035999084         # Fine Structure Constant

# ---------------------------------------------------------
# 1. THE TOPOLOGICAL CLOSURE (Continuous vs Discrete Tension)
# ---------------------------------------------------------
# H2 computational proof locked to exactly 1/9 (Discrete Topological Gap)
H2_W7 = 1.0 / 9.0

# The Continuous Void Area is purely geometric: pi / 20
W7_EXACT = math.pi / 20.0  # ~0.15707963267948966

# [DEFINITIVE TENSION CONSTANTS]
REALITY_TENSION = 1.0100375  # Discrete/Reality Mismatch
DISCRETE_CLOSURE = 1.0000424 # Discrete/Continuous Gap (Topological Closure)

# Betti Numbers
BETTI_11 = 11
BETTI_21_HARMONIC = 3.0 # The 21:7 Universal Biological/Cosmological Stability Ratio.
BETTI_5 = 5
BETTI_7 = 7
BETTI_0 = 1.0 # The Observer / Ground State

# Closure Equation
CLOSURE_GEOMETRIC = (W7_EXACT / H2_W7) * (1.0 / math.sqrt(2.0))
CLOSURE_TOPOLOGICAL = (BETTI_11 + BETTI_0) / (BETTI_5 + BETTI_7)
MANIFOLD_CLOSURE = DISCRETE_CLOSURE  # ~1.0000424

# ---------------------------------------------------------
# 2. THE DISCRETE HARMONICS (Fractions)
# ---------------------------------------------------------
F_1_32 = 1.0 / 32.0   # 0.03125
F_3_32 = 3.0 / 32.0   # 0.09375
F_1_16 = 1.0 / 16.0   # 0.0625
F_1_64 = 1.0 / 64.0   # 0.015625

# [NEW CLOSURE CONSTANTS - MARCH 2026]
UNIT_64 = 1.0 / 64.0
GATE_5_32 = 10.0 * UNIT_64  # 0.15625
W7_DATA = 0.15697685963482133
RESID_DATA_5_32 = W7_DATA - GATE_5_32  # ~0.0007268
BIAS_EXACT_MINUS_DATA = W7_EXACT - W7_DATA  # ~0.0001027

# [SH PHASE TRANSITION CLOSURE]
# From ATLAS_V2.2_RELEASE/sh_boundary_scores.csv
SH_R_STAR = 0.11140619
SH_Q0_STAR = 0.972
SH_BOUNDARY_PEAK = 1.7889626698457108

# FWHM Band Extents
SH_R_FWHM_MIN = 0.11066433
SH_R_FWHM_MAX = 0.11659923
SH_Q0_FWHM_MIN = 0.965
SH_Q0_FWHM_MAX = 0.973

# Asymmetry & Skew (Verified 1:7 Ratio)
SH_R_FWHM_L = 0.00074186
SH_R_FWHM_R = 0.00519304
SH_SKEW_RATIO_OBSERVED = 7.0000269593  # SH_R_FWHM_R / SH_R_FWHM_L
SH_SKEW_RATIO_NEAREST_INT = 7
SH_SKEW_RATIO_LOCK_ERR = 2.6959264575e-05

# Peak Quantization Candidate (Sqrt(16/5))
SH_PEAK_QUANT_CANDIDATE = 1.7888543819998317 # math.sqrt(16/5)
SH_PEAK_QUANT_ERR = 0.0001082878 # abs(SH_BOUNDARY_PEAK - SH_PEAK_QUANT_CANDIDATE)
SH_SKEW_DRIVER_CANDIDATE = 6 # SH_SKEW_RATIO_NEAREST_INT - 1 (Hexagonal Driver)

# ---------------------------------------------------------
# 3. SPARK AND VECTORS
# ---------------------------------------------------------
# SPARK_ANGLE_DEG: The Time/Gravity Bridge
# Formerly 138.88. Sieve reveals it is the rational 1250/9 (138.888...)
# This is exactly 1000 / 7.2 (The 72-fold harmonic).
SPARK_ANGLE_DEG = 1250.0 / 9.0 
SPARK_LEAP_DIST = 2.5

NIGHT_HYSTERESIS = 0.8418
TERMINUS_R = 0.1123

# ---------------------------------------------------------
# 4. UNIVERSAL SIEVE DERIVATIONS
# ---------------------------------------------------------
LUNAR_CYCLE = 1.0 / 28.0
VERTICAL_MOBIUS_TWIST = LUNAR_CYCLE
TIDAL_TORQUE_ANGLE = 360.0 / 28.0

# [THE RENORMALIZATION SIEVE]
# Unifies Geometric Expansion (Phi) with QED (Alpha)
# 10 * Phi^3 + Alpha = 42.36797... (Target 42.368, Err 2e-5)
RENORMALIZATION_BRIDGE = 10.0 * (PHI**3) + ALPHA

# [THE CHIRALITY SIEVE]
# Unifies Biological Chirality with Topological Betti Sum
# 1 / (Betti_11 + Betti_7) = 1/18 = 0.0555...
# Old value: 5.555492104 / 100 = 0.0555549...
CHIRALITY_CONSTANT = 1.0 / (BETTI_11 + BETTI_7)
LOOP_STRENGTH_5 = CHIRALITY_CONSTANT * 100.0  # Preserved for backward compat

# Tunnel Tension
TUNNEL_TENSION = (BETTI_11 / BETTI_7) * REALITY_TENSION

# ---------------------------------------------------------
# 5. GABA-C CONVERGENCE (The Shadow Sieve)
# ---------------------------------------------------------
# Biology is the Cosmos decimated (1/10 scale).

# GABA_CAB (0.0841...) is exactly Night Hysteresis / 10
GABA_C_R_CAB = NIGHT_HYSTERESIS / 10.0

# GABA_V_APEX (0.1399...) is exactly Design Potential / 10
DESIGN_POTENTIAL_PHI = 1.4 # Master Design Potential
GABA_C_V_APEX = DESIGN_POTENTIAL_PHI / 10.0

# GABA_CA (0.0927...) is the "Darkness Leak"
# F_3_32 (0.09375) - Alpha/7 (0.00104) ~ 0.09271
# Represents light (Alpha) penetrating the Darkness (3/32)
GABA_C_R_CA = F_3_32 - (ALPHA / 7.0)

# ---------------------------------------------------------
# 6. MAXWELL CAVITY (The Rational Sieve)
# ---------------------------------------------------------
# The physical "box" is defined by exact rationals and geometric roots.

# Maxwell Major: EXACTLY 17/8 (2.125)
MAXWELL_R_MAJOR = 17.0 / 8.0

# Maxwell Minor: 1/sqrt(20) corrected by Chirality/1000
# Base geometric width is related to W7_EXACT (pi/20) -> sqrt(1/20).
# The correction is the "Twist" (Chirality).
# 0.223606... - 0.000055... = 0.223551... (Matches old 0.2235501... to 1e-6)
MAXWELL_R_MINOR = (1.0 / math.sqrt(20.0)) - (CHIRALITY_CONSTANT / 1000.0)

MAXWELL_Q_FACTOR = 11.8

# 7. INTEGRATED DEBT
TOTAL_DEBT_AREA = (11.0 / 7.0) * NIGHT_HYSTERESIS

# 8. CALIBRATION DICTIONARY
CALIBRATED_SKELETON = {
    "W7_AREA": W7_EXACT,
    "H2_W7": H2_W7,
    "KAPPA_1_32": F_1_32,
    "COMPRESSION_GAP_3_32": F_3_32,
    "SPACING_1_16": F_1_16,
    "KAPPA_1_64": F_1_64,
    "SPARK_ANGLE_DEG": SPARK_ANGLE_DEG,
    "SPARK_LEAP_DIST": SPARK_LEAP_DIST,
    "NIGHT_HYSTERESIS": NIGHT_HYSTERESIS,
    "TERMINUS_R": TERMINUS_R,
    "BETTI_11": BETTI_11,
    "BETTI_5": BETTI_5,
    "BETTI_7": BETTI_7,
    "BETTI_0": BETTI_0,
    "MANIFOLD_CLOSURE": MANIFOLD_CLOSURE,
    "LUNAR_CYCLE": LUNAR_CYCLE,
    "VERTICAL_MOBIUS_TWIST": VERTICAL_MOBIUS_TWIST,
    "TIDAL_TORQUE_ANGLE": TIDAL_TORQUE_ANGLE,
    "TUNNEL_TENSION": TUNNEL_TENSION,
    "LOOP_STRENGTH_5": LOOP_STRENGTH_5,
    "CHIRALITY_CONSTANT": CHIRALITY_CONSTANT,
    "GABA_C_R_CAB": GABA_C_R_CAB,
    "GABA_C_R_CA": GABA_C_R_CA,
    "GABA_C_V_APEX": GABA_C_V_APEX,
    "MAXWELL_R_MAJOR": MAXWELL_R_MAJOR,
    "MAXWELL_R_MINOR": MAXWELL_R_MINOR,
    "MAXWELL_Q_FACTOR": MAXWELL_Q_FACTOR,
    "TOTAL_DEBT_AREA": TOTAL_DEBT_AREA,
    "UNIT_64": UNIT_64,
    "GATE_5_32": GATE_5_32,
    "W7_DATA": W7_DATA,
    "RESID_DATA_5_32": RESID_DATA_5_32,
    "SH_R_STAR": SH_R_STAR,
    "SH_Q0_STAR": SH_Q0_STAR,
    "RENORMALIZATION_BRIDGE": RENORMALIZATION_BRIDGE,
}

# ---------------------------------------------------------
# 9. UROBOROS WORMHOLE (The 4D Scale Sieve)
# ---------------------------------------------------------
# The winding number is the ratio of the Source (11) to the Void Structure (7).
# It defines how many times the 4D spiral wraps for every surface orbit.
UROBOROS_WINDING = float(BETTI_11) / float(BETTI_7)  # 11/7 approx 1.5714...

# The torsion is the H2 (1/9) gap applied to the winding.
# This defines the "Twist" required to tunnel through the center.
UROBOROS_TORSION = H2_W7 * UROBOROS_WINDING  # (1/9) * (11/7) approx 0.1746...

