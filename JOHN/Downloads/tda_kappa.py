from __future__ import annotations

from dataclasses import dataclass

from geometry_package.absolute_constants import F_1_16, F_1_32, F_1_64


@dataclass(frozen=True)
class KappaGateWeights:
    """
    Barycentric weights over the three discrete leakage anchors:
    1/64 (rigid), 1/32 (baseline), 1/16 (chaos).
    """

    w_1_64: float
    w_1_32: float
    w_1_16: float


def _clamp(value: float, lo: float, hi: float) -> float:
    return float(max(lo, min(hi, value)))


def kappa_tda_from_p_h1(
    p_h1: float,
    p_ref: float,
    p_max: float,
    *,
    kappa_min: float = F_1_64,
    kappa_mid: float = F_1_32,
    kappa_max: float = F_1_16,
) -> float:
    """
    Continuous→discrete bridge from H1 persistence to κ_TDA.

    This implements the piecewise mapping described in
    `geometry_package/GEOMETRY_EQUATIONS.md` (Appendix A).
    """
    p_h1_f = float(p_h1)
    p_ref_f = float(p_ref)
    p_max_f = float(p_max)

    if p_h1_f <= 0.0:
        return float(kappa_min)

    if p_ref_f <= 0.0:
        # Degenerate: if ref is zero, treat any positive persistence as baseline.
        return float(kappa_mid)

    if p_h1_f <= p_ref_f:
        kappa = kappa_min + (kappa_mid - kappa_min) * (p_h1_f / p_ref_f)
        return _clamp(kappa, float(kappa_min), float(kappa_mid))

    if p_max_f <= p_ref_f:
        # Degenerate: no upper range exists; clamp at max.
        return float(kappa_max)

    kappa = kappa_mid + (kappa_max - kappa_mid) * ((p_h1_f - p_ref_f) / (p_max_f - p_ref_f))
    return _clamp(kappa, float(kappa_mid), float(kappa_max))


def gate_weights_from_kappa(
    kappa: float,
    *,
    kappa_min: float = F_1_64,
    kappa_mid: float = F_1_32,
    kappa_max: float = F_1_16,
) -> KappaGateWeights:
    """
    Convert a continuous κ into weights over the discrete anchors.

    - κ in [1/64, 1/32] interpolates between (1/64, 1/32)
    - κ in [1/32, 1/16] interpolates between (1/32, 1/16)
    """
    k = float(kappa)
    k_min = float(kappa_min)
    k_mid = float(kappa_mid)
    k_max = float(kappa_max)

    if k <= k_min:
        return KappaGateWeights(1.0, 0.0, 0.0)
    if k >= k_max:
        return KappaGateWeights(0.0, 0.0, 1.0)

    if k <= k_mid:
        denom = max(k_mid - k_min, 1e-12)
        t = (k - k_min) / denom
        return KappaGateWeights(1.0 - t, t, 0.0)

    denom = max(k_max - k_mid, 1e-12)
    t = (k - k_mid) / denom
    return KappaGateWeights(0.0, 1.0 - t, t)


def effective_kappa_from_weights(
    weights: KappaGateWeights,
    *,
    kappa_min: float = F_1_64,
    kappa_mid: float = F_1_32,
    kappa_max: float = F_1_16,
) -> float:
    return float(
        weights.w_1_64 * float(kappa_min)
        + weights.w_1_32 * float(kappa_mid)
        + weights.w_1_16 * float(kappa_max)
    )

