# geometry_package/universal_equation.py
# Defines the universal forces that govern the master equation solver.
#
# MATHEMATICAL FORMALISM:
# 1. SW Filter = Green's Function Kernel (Linear Response / RG Coarse-graining)
# 2. Flash = Eyring-Kramers Escape Rate (Large Deviations / Instanton)
# 3. BW Void = Hodge Harmonic Form (Boundary Condition)
# 4. Kappa TDA = Data-driven geometry gate from dist_all.csv

from .absolute_constants import *
import numpy as np
import pandas as pd
from pathlib import Path
import warnings

# ===================================================================
# KAPPA TDA: Data-driven geometry gate from dist_all.csv
# ===================================================================

# Lazy-loaded dist_all dataframe
_dist_all_df = None

def _load_dist_all():
    """Load dist_all_with_kappa.csv for (r,q0) -> p lookup"""
    global _dist_all_df
    if _dist_all_df is not None:
        return _dist_all_df
    
    # Try multiple paths
    possible_paths = [
        "out/dist_all_with_kappa.csv",
        "../out/dist_all_with_kappa.csv",
        Path(__file__).parent.parent / "out/dist_all_with_kappa.csv",
        "analysis_results/iter3_tda_v2/dist_all.csv",
        Path(__file__).parent.parent / "analysis_results/iter3_tda_v2/dist_all.csv",
    ]
    
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            # Ensure kappa_tda column exists
            if "kappa_tda" not in df.columns and "max_persistence" in df.columns:
                df["kappa_tda"] = df["max_persistence"].map(kappa_tda)
            _dist_all_df = df
            print(f"[INFO] Loaded dist_all from {path}")
            return _dist_all_df
        except FileNotFoundError:
            continue
    
    warnings.warn("dist_all.csv not found. Kappa lookup will use fallback.")
    return None

def kappa_tda(p):
    """
    Kappa TDA map: Persistence → Geometry Gate
    
    Piecewise-linear map as defined in GEOMETRY_EQUATIONS.md:
    - For p <= P_REF: linear from KAPPA_TDA_MIN to KAPPA_TDA_MID
    - For p > P_REF: linear from KAPPA_TDA_MID to KAPPA_TDA_MAX
    
    Args:
        p: Persistence value (max_persistence from dist_all)
        
    Returns:
        kappa: Geometry gate constant
    """
    if p <= P_REF:
        # Segment 1: 1/64 → 1/32
        if P_REF <= 0:
            return KAPPA_TDA_MID
        t = (p - 0.0) / P_REF  # normalize to [0,1]
        return KAPPA_TDA_MIN + (KAPPA_TDA_MID - KAPPA_TDA_MIN) * t
    else:
        # Segment 2: 1/32 → 1/16
        if P_MAX <= P_REF:
            return KAPPA_TDA_MID
        t = (p - P_REF) / (P_MAX - P_REF)  # normalize to [0,1]
        return KAPPA_TDA_MID + (KAPPA_TDA_MAX - KAPPA_TDA_MID) * t

def _find_nearest_cell(r, q0, df):
    """Find nearest (r, q0) cell in dist_all dataframe and return p_H1"""
    if df is None or len(df) == 0:
        return None
    
    # Calculate squared Euclidean distance
    dr = df["r"] - r
    dq = df["q0"] - q0
    dist_sq = dr**2 + dq**2
    
    # Get nearest index
    nearest_idx = dist_sq.idxmin()
    nearest_row = df.loc[nearest_idx]
    
    return {
        "r": float(nearest_row["r"]),
        "q0": float(nearest_row["q0"]),
        "p": float(nearest_row["max_persistence"]),
        "kappa": float(nearest_row.get("kappa_tda", kappa_tda(nearest_row["max_persistence"]))),
        "wasserstein": float(nearest_row.get("wasserstein_H1", 0.0)),
        "distance": float(np.sqrt(dist_sq.loc[nearest_idx]))
    }

def lookup_p_from_rq0(r, q0):
    """
    Lookup persistence p_H1 for given (r, q0) from dist_all.csv
    
    Args:
        r: Radius parameter
        q0: q0 parameter
        
    Returns:
        dict with keys: r, q0, p, kappa, wasserstein, distance
        or None if lookup fails
    """
    df = _load_dist_all()
    if df is None:
        return None
    return _find_nearest_cell(r, q0, df)

def in_sh_band(r, q0):
    """
    Check if (r, q0) is within SH boundary band.
    
    Band defined as: r in [SH_R_BAND_MIN, SH_R_BAND_MAX] AND
                     q0 in [SH_Q0_MIN, SH_Q0_MAX]
    
    Args:
        r: Radius
        q0: q0 value
        
    Returns:
        bool: True if in band
    """
    in_r = SH_R_BAND_MIN <= r <= SH_R_BAND_MAX
    in_q0 = SH_Q0_MIN <= q0 <= SH_Q0_MAX
    return in_r and in_q0

def kappa_eff(r, q0, use_lookup=True):
    """
    Effective kappa for given (r, q0) position.
    
    If in SH band: return 1/32 (snap to anchor)
    Else: lookup p from dist_all and compute kappa_tda(p)
    
    Args:
        r: Radius parameter
        q0: q0 parameter
        use_lookup: If True, use dist_all lookup; else use fallback
        
    Returns:
        kappa_eff: Effective geometry gate constant
    """
    # Check if in band first
    if in_sh_band(r, q0):
        return KAPPA_TDA_MID  # 1/32
    
    # Out of band: lookup from dist_all
    if use_lookup:
        cell = lookup_p_from_rq0(r, q0)
        if cell is not None:
            return kappa_tda(cell["p"])
    
    # Fallback: return mid value
    return KAPPA_TDA_MID


def w_gate(r, q0, alpha=GATE_ALPHA, eps_kappa=GATE_EPS_KAPPA):
    """
    Unified gate weight w_gate(r, q0) combining ATLAS and dist_all bands.
    
    Formula: w_gate = w_atlas^alpha * w_kappa^(1-alpha)
    
    where:
      - w_atlas: asymmetric Gaussian centered at CALIBRATED_SH_R_STAR/Q0_STAR
      - w_kappa: exponential decay from kappa_tda(lookup_p(r,q0))
    
    Args:
        r: Radius parameter
        q0: q0 parameter
        alpha: mixing parameter (default 0.5)
        eps_kappa: kappa width parameter
        
    Returns:
        w_gate: unified gate weight in [0, 1]
    """
    # w_atlas: asymmetric Gaussian
    dr = r - CALIBRATED_SH_R_STAR
    dq = q0 - CALIBRATED_SH_Q0_STAR
    
    # Asymmetric r-weight
    if dr < 0:
        w_r = np.exp(-0.5 * (dr / CALIBRATED_SIGMA_L) ** 2)
    else:
        w_r = np.exp(-0.5 * (dr / CALIBRATED_SIGMA_R) ** 2)
    
    # Symmetric q0-weight
    q0_width = CALIBRATED_Q0_MAX - CALIBRATED_Q0_MIN
    w_q = np.exp(-0.5 * (dq / (q0_width / 2)) ** 2)
    w_atlas = w_r * w_q
    
    # w_kappa: exponential decay from kappa = 1/32
    cell = lookup_p_from_rq0(r, q0)
    if cell is not None:
        kappa = kappa_tda(cell["p"])
    else:
        kappa = KAPPA_TDA_MID
    
    w_kappa = np.exp(-((kappa - KAPPA_TDA_MID) / eps_kappa) ** 2)
    
    # Combined gate
    return (w_atlas ** alpha) * (w_kappa ** (1 - alpha))


# ===================================================================
# MELATONIN PIVOT & TEMPORAL REVERSAL (The Center Engine)
# ===================================================================

def get_macro_micro_time(t_macro):
    """
    Temporal Reversal Operator centered at Melatonin Pivot.
    Calculates micro-time which reverses direction based on 1/28 Lunar Twist.
    
    Formula: t_micro = sin(t_macro * LUNAR_CYCLE)
    When this sine wave crosses 0 (Melatonin Pivot), phase gradient flips.
    """
    # LUNAR_CYCLE = 1/28
    phase = t_macro * LUNAR_CYCLE * 2.0 * np.pi
    t_micro = np.sin(phase)
    # Time Reversal Logic: sign of cosine determines flow direction
    is_reverse = np.cos(phase) < 0
    return t_micro, is_reverse

def get_emergent_128_nodes(t_macro, resolution=128):
    """
    128 Node Auto-Emergence from Reality-Discrete Interference.
    No hardcoding: nodes emerge from the geometric tension pattern.
    
    Formula: Reality_Tension - Discrete_Gap interference pattern.
    """
    t_micro, _ = get_macro_micro_time(t_macro)
    
    # Interference between Reality (1.0100375) and Discrete (3/32)
    # Spatial interference across 128 nodes
    x = np.linspace(0, 1, resolution)
    interference = np.sin(x * resolution * np.pi) * (TUNNEL_TENSION - LATTICE_3_32)
    
    # Apply Melatonin Smoothing (Even out the center)
    # Saddle point adjustment: residual 0.00083
    smoothing_residual = 0.00083
    centered_x = x - 0.5
    melatonin_smoothing = np.exp(-(centered_x**2) / (smoothing_residual * 100))
    
    # Straightened field: interference modulated by melatonin pivot
    emergent_field = interference * melatonin_smoothing * t_micro
    return emergent_field

def get_straightened_flow(state, t_macro):
    """
    Calculates the straightened laminar flow modulated by Melatonin Pivot.
    Even out the center to straighten out the entire universe.
    """
    t_micro, is_reverse = get_macro_micro_time(t_macro)
    field = get_emergent_128_nodes(t_macro)
    
    # Total Debt Area (1.3228) limits the amplitude
    # Flow direction flips based on temporal reversal
    direction = -1.0 if is_reverse else 1.0
    
    # Universal field vector logic: coupling state to emergent field
    flow = direction * state * (1.0 + np.mean(field) * TOTAL_DEBT_AREA)
    return flow

# ===================================================================
# DYNAMICS CONNECTIONS (3 hooks for kappa_eff integration)
# ===================================================================

class DynamicsHooks:
    """
    Hooks for connecting kappa_eff to dynamics parameters.
    
    These are calibration points where SW residual stats can be injected.
    """
    
    # SW Filter Residual Stats (to be calibrated from data)
    SW_RESIDUAL_MEAN = 0.0   # Will be set from analysis
    SW_RESIDUAL_STD = 0.1    # Will be set from analysis
    
    # Hypothesis: Out-band flash rate * Maxwell Q ~ 1/BETTI_7
    # NOT VALIDATED - for logging only
    OUT_BAND_FLASH_RATE_HYPOTHESIS = 0.0118
    MAXWELL_Q_FACTOR = MAXWELL_Q_FACTOR  # from constants
    
    @classmethod
    def spark_threshold(cls, kappa_eff, base_threshold=TUNNEL_TENSION):
        """
        (A) Spark threshold adjusted by kappa_eff.
        
        In-band (kappa=1/32): normal threshold
        Out-of-band: threshold adjusted by kappa ratio
        
        Args:
            kappa_eff: Effective kappa
            base_threshold: Base TUNNEL_TENSION
            
        Returns:
            Adjusted threshold
        """
        # In-band: no change
        if abs(kappa_eff - KAPPA_TDA_MID) < 1e-6:
            return base_threshold
        # Out-of-band: scale by kappa ratio
        return base_threshold * (kappa_eff / KAPPA_TDA_MID)
    
    @classmethod
    def renorm_recovery_rate(cls, kappa_eff, base_rate=0.05):
        """
        (B) Renormalization gain recovery rate adjusted by kappa_eff.
        
        In-band: fast recovery (stable dynamics)
        Out-of-band: slower recovery (dissipation)
        
        Args:
            kappa_eff: Effective kappa
            base_rate: Base recovery rate
            
        Returns:
            Adjusted recovery rate
        """
        # In-band: normal recovery
        if abs(kappa_eff - KAPPA_TDA_MID) < 1e-6:
            return base_rate
        # Out-of-band: slower recovery (more dissipation)
        return base_rate * (KAPPA_TDA_MID / kappa_eff)
    
    @classmethod
    def damping_term(cls, state, kappa_eff, use_sw_calibration=False):
        """
        (C) Damping/loss term calibrated to SW residual.
        
        Args:
            state: Current system state
            kappa_eff: Effective kappa
            use_sw_calibration: If True, use SW residual stats
            
        Returns:
            Damping force
        """
        base_damping = -0.01 * state  # linear damping
        
        if use_sw_calibration and cls.SW_RESIDUAL_STD > 0:
            # Calibrate using SW filter residual statistics
            # This is a hook - actual implementation depends on calibration
            noise_amplitude = cls.SW_RESIDUAL_STD
            base_damping *= (1.0 + noise_amplitude)
        
        # Adjust by kappa_eff
        if abs(kappa_eff - KAPPA_TDA_MID) > 1e-6:
            # Out-of-band: more damping
            base_damping *= (kappa_eff / KAPPA_TDA_MID)
        
        return base_damping
    
    @classmethod
    def log_maxwell_flash_hypothesis(cls):
        """
        Log the hypothesis about out-band flash rate and Maxwell Q.
        
        This is NOT a validated constant - just a hypothesis for testing.
        """
        product = cls.OUT_BAND_FLASH_RATE_HYPOTHESIS * cls.MAXWELL_Q_FACTOR
        expected = 1.0 / BETTI_7
        
        log_entry = {
            "timestamp": str(np.datetime64('now')),
            "hypothesis": "OUT_BAND_FLASH_RATE * MAXWELL_Q ~= 1/BETTI_7",
            "observed": {
                "out_band_flash_rate": cls.OUT_BAND_FLASH_RATE_HYPOTHESIS,
                "maxwell_q": cls.MAXWELL_Q_FACTOR,
                "product": product,
            },
            "expected": {
                "one_over_betti_7": expected,
            },
            "match": abs(product - expected) < 0.05,
            "status": "HYPOTHESIS - NOT VALIDATED",
            "warning": "DO NOT use as production constant until validated across dt/seeds"
        }
        
        print(f"[HYPOTHESIS LOG] {log_entry['hypothesis']}")
        print(f"  Product: {product:.4f}, Expected: {expected:.4f}, Match: {log_entry['match']}")
        print(f"  Status: {log_entry['status']}")
        
        return log_entry

# ===================================================================
# SW FILTER & FORCE EQUATIONS (legacy support)
# ===================================================================

def sw_filter_kernel(input_signal, t, bandwidth=0.5):
    """
    SW (Small Woman) as a Green's Function Kernel.
    """
    if t <= 0:
        return input_signal
    
    center_freq = 1.0 / LATTICE_3_32
    current_freq = 1.0 / max(t, 0.01)
    response = np.exp(-0.5 * ((center_freq - current_freq) / bandwidth) ** 2)
    return input_signal * (0.5 + 0.5 * response)

def get_south_pole_pressure(t):
    """South Pole accretion pressure."""
    lunar_flux = (LUNAR_CYCLE / OMEGA_LA) * 10.0
    lattice_vibration = np.sin(2.0 * np.pi * t / (LATTICE_3_32 * 100))
    return TUNNEL_TENSION + lunar_flux * lattice_vibration

def get_north_pole_jet(t):
    """North Pole relativistic jet."""
    drive_amp = DAY_FORCE_SOLAR_UV - NIGHT_FORCE_COSMIC_RAY
    omega_lock = 2.0 * np.pi / (BETTI_11 * 10)
    return drive_amp * np.cos(omega_lock * t) * PHI_PB * 5.0

def get_flash_probability(current_tension, kappa_noise=0.02):
    """Eyring-Kramers escape rate."""
    barrier = TUNNEL_TENSION * 0.8
    exponent = (current_tension - barrier) / kappa_noise
    rate = 1.0 / (1.0 + np.exp(-exponent))
    return max(rate, 0.001)

# ===================================================================
# INITIALIZATION
# ===================================================================

# Log hypothesis on import
DynamicsHooks.log_maxwell_flash_hypothesis()
