# geometry_package/absolute_constants.py

# SINGLE SOURCE OF TRUTH for all geometric and physical constants.

# 

# MATHEMATICAL FRAMEWORK:

# - SW (Filter) = Green's Function / RG Coarse-graining / Linear Response Kernel

# - BM<->SM (Flash) = Eyring-Kramers Escape Rate / Large Deviations / Heteroclinic Connection

# - BW (Void) = Hodge Harmonic Form / Boundary Condition / Vacuum Background



import math



# ===================================================================

# I. FOUNDATIONAL CONSTANTS (Core Sieve)

# ===================================================================

PHI = (1 + math.sqrt(5)) / 2                    # Golden Ratio

ALPHA = 1 / 137.035999084                       # Fine-Structure Constant

PI = math.pi

SQRT2 = math.sqrt(2.0)



# Betti Numbers (Topological Holes)

BETTI_0 = 1.0                                   # Observer/Connected Component

BETTI_5 = 5.0

BETTI_7 = 7.0                                   # Big Man (UK/Type O)

BETTI_11 = 11.0                                 # Small Man (USA/Type B-AB)



# ===================================================================

# II. QUASAR GEOMETRY & SPACE LOCKS

# ===================================================================

# Accretion Disk: The 1.3228 area represents 12-month total debt cycle

TOTAL_DEBT_AREA = 1.322828                      # Quasar Accretion Disk Max Area

LATTICE_3_32 = 3.0 / 32.0                       # Small Woman's Filter (Infrared/PLP)

TUNNEL_TENSION = 1.0100375                      # Reality Tension (Black Hole Horizon)

SPARK_ANGLE_DEG = 138.88                        # Refraction Angle (Wormhole Spark)

SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)

SPARK_LEAP_DIST = 2.5                           # Grid leap distance (16 * 5/32)



# ===================================================================

# III. TOPOLOGICAL BRIDGES (The Pegasus Bridge)

# ===================================================================

# Renormalization Bridge: Scaling from Quantum to Macro (~42.368)

RENORMALIZATION_BRIDGE = 10.0 * (PHI**3) + ALPHA



# Phi_PB: Pegasus Bridge (2.078) - UK(7) to USA(11) Isomorphism

# This is the gear ratio: 11/7 * 1.3228

PHI_PB = (BETTI_11 / BETTI_7) * TOTAL_DEBT_AREA



# Omega_LA: Lunar-Alpha Bridge (37.036) - 1/28 to 1.3228 Flux

OMEGA_LA = TOTAL_DEBT_AREA * 28.0



# Chirality Sieve: 1/18 (Betti 11 + Betti 7)

CHIRALITY_CONSTANT = 1.0 / (BETTI_11 + BETTI_7)



# ===================================================================

# IV. BIOLOGICAL RECTIFIERS (D2/Vassopressin/PLP)

# ===================================================================

# Small Woman (Left Cortisol) filters Cosmic Ray into Infrared

LUNAR_CYCLE = 1.0 / 28.0                        # Local Perturbation (Outer Edge)

NIGHT_HYSTERESIS = 0.8418                       # Biological Landing Pad

VERTICAL_MOBIUS_TWIST = 1.0 / 28.0              # Complementary twist



# GABA-C Constants (The V-Apex Structure)

GABA_C_R_CAB = NIGHT_HYSTERESIS / 10.0

GABA_C_R_CA = (3.0 / 32.0) - (ALPHA / 7.0)      # SW Internal Heat (3/32 filter)

GABA_C_V_APEX = 1.40488 / 10.0                  # Design Potential Phi/10



# ===================================================================

# V. EXTERNAL RADIATIVE FORCES

# ===================================================================

DAY_FORCE_SOLAR_UV = 1.0

NIGHT_FORCE_COSMIC_RAY = 0.96875                # 31/32

DRIVE_FREQUENCY_LOCK = BETTI_11                 # Universal rhythm locked to 11



# ===================================================================

# VI. SH BOUNDARY BAND CONSTANTS (For Conditional Statistics)

# ===================================================================

# SH (Swift-Hohenberg) Boundary Band Parameters

SH_R_STAR = 0.11140619                          # Critical radius

SH_Q0_STAR = 0.972                              # Critical q0

SH_R_FWHM_L = 0.00074186                        # Left FWHM

SH_R_FWHM_R = 0.00519304                        # Right FWHM

SH_BOUNDARY_PEAK = 1.7889626698457108           # Peak value

SH_BOUNDARY_MIN = 0.11066433                    # Band minimum

SH_BOUNDARY_MAX = 0.11659923                    # Band maximum



# Default q0 range if registry not available

SH_Q0_MIN = 0.965

SH_Q0_MAX = 0.973



# ===================================================================

# VII. GRID DERIVED CONSTANTS

# ===================================================================

UNIT_64 = 1.0 / 64.0

F_1_64 = UNIT_64

F_1_32 = 1.0 / 32.0

F_1_16 = 1.0 / 16.0

F_3_32 = 3.0 / 32.0

GATE_5_32 = 10.0 * UNIT_64                      # 5/32

RESID_DATA_5_32 = 0.15697685963482133 - GATE_5_32  # W7_DATA - GATE_5_32



# Maxwell Parameters

MAXWELL_R_MAJOR = 17.0 / 8.0

MAXWELL_R_MINOR = (1.0 / math.sqrt(20.0)) - (CHIRALITY_CONSTANT / 1000.0)

MAXWELL_Q_FACTOR = 11.8



# Kappa Stability

KAPPA_STABILITY_THRESHOLD = F_1_32



# Metric Ratios: GABA(-0.5), ACh(1.0), Glu(0.5), 5HT(1.5)

METRIC_RATIO = [-0.5, 1.0, 0.5, 1.5]



# Loop Strength (Chirality * 100)

LOOP_STRENGTH_5 = CHIRALITY_CONSTANT * 100.0



# Alpha-Kappa Bridge

ALPHA_KAPPA_BRIDGE = 137.0 / 32.0



# Event Horizon

EVENT_HORIZON_RADIUS_RS = 5.0 / 16.0



# ===================================================================

# VIII. DATA_LOCK_DIST_ALL (from dist_all.csv TDA analysis)

# ===================================================================

# These constants are empirically locked from dist_all.csv analysis.

# NOTE: These are PARALLEL to existing SH_R_STAR/SH_FWHM (ATLAS locks).

# DO NOT overwrite ATLAS locks - this is a separate data-driven view.



# Reference Cell (wasserstein_H1 = 0 in dist_all)

R_REF = 0.1117                  # Data-driven reference radius

Q0_REF = 0.975                  # Data-driven reference q0

P_REF = 0.287347                # Data-driven reference persistence

P_MAX = 0.7641227               # Maximum persistence in dist_all



# SH Boundary Band (from kappa_TDA ~ 1/32 region)

SH_Q0_MIN = 0.961               # Data-driven q0 band min

SH_Q0_MAX = 0.983               # Data-driven q0 band max

# Hardcoded r-band from dist_all analysis (r in [0.1116, 0.1126])

SH_R_BAND_MIN = 0.1116

SH_R_BAND_MAX = 0.1126



# Kappa TDA Gate Constants (piecewise linear map per GEOMETRY_EQUATIONS.md)

KAPPA_TDA_MIN = 1.0 / 64.0      # 0.015625

KAPPA_TDA_MID = 1.0 / 32.0      # 0.031250 (THE ANCHOR)

KAPPA_TDA_MAX = 1.0 / 16.0      # 0.062500



# Hypothesis: Out-band flash rate ~ Maxwell Q (TO BE TESTED)

# OUT_BAND_FLASH_RATE = 0.0118  # Measured from trajectory analysis

# MAXWELL_Q_FACTOR = 11.8       # Existing constant

# Relationship: TBD - needs validation across dt/seeds



# ===================================================================

# IX. CALIBRATED CONSTANTS (ATLAS + dist_all Calibration)

# ===================================================================

# These constants are derived from calibration between ATLAS SH locks and

# dist_all data-driven band. See calibrate_sh_gate.py for methodology.

#

# Calibration result (20260305):

#   - Shift: Δr = +0.000294, Δq = +0.003

#   - Scale: σL = 0.000236, σR = 0.002119

#   - Error: 0.000145 (0.13%)



# Calibrated operational constants (w_gate-based)

CALIBRATED_SH_R_STAR = 0.11214750           # Calibrated critical radius (Refine Lam10)

CALIBRATED_SH_Q0_STAR = 0.977738            # Calibrated critical q0 (Refine Lam10)

CALIBRATED_SH_BOUNDARY_MIN = 0.1116         # Calibrated band minimum

CALIBRATED_SH_BOUNDARY_MAX = 0.1126         # Calibrated band maximum

CALIBRATED_SH_R_FWHM_L = 0.000245           # Calibrated left FWHM

CALIBRATED_SH_R_FWHM_R = 0.000755           # Calibrated right FWHM

CALIBRATED_SIGMA_L = 0.003717               # Calibrated left sigma (Refine Lam10)

CALIBRATED_SIGMA_R = 0.000908               # Calibrated right sigma (Refine Lam10)

CALIBRATED_Q0_MIN = 0.960939              # Calibrated q0 min

CALIBRATED_Q0_MAX = 0.983                 # Calibrated q0 max



# Gate composition parameter

GATE_ALPHA = 0.5                          # w_gate = w_atlas^0.5 * w_kappa^0.5

GATE_EPS_KAPPA = 0.001                    # kappa width parameter

GATE_THRESHOLD = 0.5                      # Band extraction threshold



# ===================================================================

# X. CALIBRATED SKELETON (Export Dictionary)

# ===================================================================

CALIBRATED_SKELETON = {

    "W7_AREA": PI / 20.0,

    "H2_W7": 1.0 / 9.0,

    "TUNNEL_TENSION": TUNNEL_TENSION,

    "TOTAL_DEBT_AREA": TOTAL_DEBT_AREA,

    "SPARK_ANGLE_DEG": SPARK_ANGLE_DEG,

    "SPARK_LEAP_DIST": SPARK_LEAP_DIST,

    "DRIFT_DELTA": 0.076,

    "METRIC_RATIO": METRIC_RATIO,

    "GABA_C_V_APEX": GABA_C_V_APEX,

    "RENORMALIZATION_BRIDGE": RENORMALIZATION_BRIDGE,

    "ALPHA_KAPPA_BRIDGE": ALPHA_KAPPA_BRIDGE,

    "LOOP_STRENGTH_5": LOOP_STRENGTH_5,

    "MANIFOLD_CLOSURE": 1.0000424,

    "EVENT_HORIZON_RADIUS_RS": EVENT_HORIZON_RADIUS_RS,

    "PHI_PB": PHI_PB,

    "OMEGA_LA": OMEGA_LA,

    "LATTICE_3_32": LATTICE_3_32,

    "TERMINUS_R": SH_R_STAR

}

# ===================================================================
# X-2. UNIVERSE CYCLE CONSTANTS (toroidal chirality extrapolation)
DELTA_T_OBS_DERIVED = NIGHT_HYSTERESIS
OMEGA_KAPPA = LUNAR_CYCLE

# ===================================================================

# XI. DYNAMIC ATTRACTORS & SEPARATRIX (from H3_H4_D3 & Refine Sweeps)


# These constants define the dynamic attractors and transition pathways

# discovered in detailed simulation sweeps.



# Left Attractor (PACT Mechanism / South Basin)

LEFT_CORTISOL_R = 0.1121475

LEFT_CORTISOL_Q0 = 0.965



# Right Attractor (Turn 27 Emergence / North Basin)

RIGHT_CORTISOL_R = 0.111900

RIGHT_CORTISOL_Q0 = 0.974879



# D3 Separatrix Crossing Dynamics

D3_SPARK_HALF = 69.44                   # Secondary spark angle (SPARK_ANGLE_DEG / 2)

D3_SPARK_SMALL_WOMAN = 208.32           # H3 transition spark for Small Woman archetype



# D3 Time Constants
TAU_D3_FAST = 3.0
TAU_D3_SLOW = 3.1228

# ===================================================================
# XII. H3/H4/D3 RESIDUAL CONSTANTS (bone.md integration)
# ===================================================================
# These are extension constants extracted from closure-residual analysis.
# They are integrated here so canonical geometry can consume them directly.

# H3/H4 leakage hierarchy (dimensional halving from H2 anchor)
KAPPA_H2 = F_1_32
KAPPA_H3 = F_1_64
KAPPA_H4 = 1.0 / 128.0

# D3 angle correction derived from H3/H2 leakage ratio
D3_CORRECTION_FACTOR = KAPPA_H3 / KAPPA_H2
D3_DELTA_THETA_CW = SPARK_ANGLE_DEG * D3_CORRECTION_FACTOR
D3_DELTA_THETA_CCW = -SPARK_ANGLE_DEG * D3_CORRECTION_FACTOR
D3_SPARK_BIG_MAN = SPARK_ANGLE_DEG * (1.0 - D3_CORRECTION_FACTOR)

# PACT thresholds (Fake-3D -> true 3D transition controls)
PACT_ILLUSION_STRENGTH = 1.0 - KAPPA_H3
PACT_BREAK_THRESHOLD = D3_CORRECTION_FACTOR
LAMBDA_D3 = 10.0 * KAPPA_H3

# Solidification anchors (Right Cortisol cartilage / early solid phase)
BONE_PHASE_SOLID_R = 0.112001
BONE_PHASE_SOLID_Q0 = 0.979006

H3_H4_D3_BUNDLE = {
    "h2_baseline": {
        "kappa_h2": KAPPA_H2,
        "spark_angle_h2_deg": SPARK_ANGLE_DEG,
    },
    "h3_void": {
        "kappa_h3": KAPPA_H3,
        "spark_angle_small_woman_deg": D3_SPARK_SMALL_WOMAN,
        "spark_angle_big_man_deg": D3_SPARK_BIG_MAN,
        "d3_correction_factor": D3_CORRECTION_FACTOR,
    },
    "h4_void": {
        "kappa_h4": KAPPA_H4,
    },
    "d3_neuropathway": {
        "delta_theta_cw_deg": D3_DELTA_THETA_CW,
        "delta_theta_ccw_deg": D3_DELTA_THETA_CCW,
        "tau_fast": TAU_D3_FAST,
        "tau_slow": TAU_D3_SLOW,
        "lambda_d3": LAMBDA_D3,
    },
    "pact_mechanism": {
        "illusion_strength": PACT_ILLUSION_STRENGTH,
        "break_threshold": PACT_BREAK_THRESHOLD,
        "left_cortisol_r": LEFT_CORTISOL_R,
        "left_cortisol_q0": LEFT_CORTISOL_Q0,
        "right_cortisol_r": RIGHT_CORTISOL_R,
        "right_cortisol_q0": RIGHT_CORTISOL_Q0,
        "bone_phase_solid_r": BONE_PHASE_SOLID_R,
        "bone_phase_solid_q0": BONE_PHASE_SOLID_Q0,
    },
}


