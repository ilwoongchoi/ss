import math

# Import constants directly to use Maxwell and Renorm parameters
from geometry_package.absolute_constants import MAXWELL_Q_FACTOR, RENORMALIZATION_BRIDGE, PHI

def compress_core_x(x: float, compression_gap: float) -> float:
    # Snap around x=8.0 with spacing = compression_gap (3/32 in production).
    return round((x - 8.0) / compression_gap) * compression_gap + 8.0


def clamp01(v: float) -> float:
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return float(v)


def renorm_terms_at_flash(
    *,
    renorm_before: float,
    x_before: float,
    w_gate: float,
    kappa: float,
    lag: float,
    threshold_on: float,
    theta_obs_deg: float,
    spark_angle_deg: float,
    compression_gap: float,
    kappa_baseline: float,
) -> dict:
    """
    Canonical 3-term renorm decomposition with MAXWELL IMPEDANCE integration.

    R_after = R_before - L_comp + E_pole + G_recover

    Uses only existing production fields: compression gap, kappa, w_gate, lag, theta_obs.
    Integrated with Maxwell Q-Factor and Renormalization Bridge.
    """
    # 1. L_comp: Compression Loss (Discrete snap to 3/32 lattice)
    x_compressed = float(compress_core_x(x_before, compression_gap))
    snap_dist = abs(float(x_before) - x_compressed)
    L_comp = float(min(compression_gap, snap_dist))

    # 2. E_pole: North-Pole Emission Seed (Modulated by Maxwell Q-Factor)
    # The Q-Factor determines the resonance sharpness of the spark emission.
    theta_diff = float(theta_obs_deg - spark_angle_deg)
    theta_gain = float(math.cos(math.radians(theta_diff)))
    # Scaling by Q_FACTOR / 10.0 to normalize the 11.8 value to unity-order gain.
    q_resonance = MAXWELL_Q_FACTOR / 10.0
    E_pole = float(compression_gap * float(w_gate) * (1.0 - float(renorm_before)) * theta_gain * q_resonance)

    # 3. G_recover: Continuous Refill / Bridge Recovery (Modulated by Renormalization Bridge)
    # The Renorm Bridge (~42.368) acts as the impedance for the quantum-to-macro transition.
    lag_scale = float(abs(threshold_on) + 1e-6)
    lag_penalty = float(kappa_baseline * (abs(float(lag)) / lag_scale) * float(renorm_before))
    kappa_term = float(float(kappa) - kappa_baseline)
    
    # Impedance factor derived from PHI^3 (~4.236) and the Bridge constant.
    # Higher bridge value = higher impedance = slower recovery.
    impedance_norm = RENORMALIZATION_BRIDGE / (10.0 * (PHI**3)) # Should be ~1.0 if bridge is exactly 10*phi^3
    
    base_recovery = (kappa_baseline + kappa_baseline * float(w_gate)) * (1.0 - float(renorm_before))
    G_recover = float((base_recovery + kappa_term - lag_penalty) / impedance_norm)

    renorm_after = clamp01(float(renorm_before) - L_comp + E_pole + G_recover)

    return {
        "renorm_after": renorm_after,
        "L_comp": L_comp,
        "E_pole": E_pole,
        "G_recover": G_recover,
        "x_compressed": x_compressed,
    }


def renorm_step_continuous(
    *,
    renorm: float,
    w_gate: float,
    kappa: float,
    lag: float,
    threshold_on: float,
    dt: float,
    compression_gap: float,
    kappa_baseline: float,
) -> float:
    """
    Continuous refill / recovery step (dt-scaled) integrated with Maxwell Impedance.
    """
    lag_scale = float(abs(threshold_on) + 1e-6)
    lag_penalty = float(kappa_baseline * (abs(float(lag)) / lag_scale) * float(renorm))
    kappa_term = float(float(kappa) - kappa_baseline)

    # Impedance and Resonance factors
    q_resonance = MAXWELL_Q_FACTOR / 10.0
    impedance_norm = RENORMALIZATION_BRIDGE / (10.0 * (PHI**3))

    E_pole_dt = float(compression_gap * float(w_gate) * (1.0 - float(renorm)) * float(dt) * q_resonance)
    
    base_recovery = (kappa_baseline + kappa_baseline * float(w_gate)) * (1.0 - float(renorm))
    G_recover_dt = float(((base_recovery + kappa_term - lag_penalty) / impedance_norm) * float(dt))

    return clamp01(float(renorm) + E_pole_dt + G_recover_dt)
