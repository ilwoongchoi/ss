from __future__ import annotations

"""
Executable closure maps that were previously listed as "missing" in UNRESOLVED_FINAL_GAPS.md.

Design goal:
- Make the S5 master-law runnable with *file-backed, deterministic* sub-maps.
- Use only constants already locked in-repo (e.g., TOTAL_CONSTANT_TABLE.csv, S5_STATE_VARIABLES.md).

This is not a claim of physical truth. It is the canonical implementation needed to remove
"missing map" placeholders from the current workspace file set.
"""

import dataclasses
import math
from typing import Iterable

import numpy as np


# Locked discrete anchors (from S5_STATE_VARIABLES.md / TOTAL_CONSTANT_TABLE.csv)
W7_EXACT = math.pi / 20.0
KAPPA_1_32 = 1.0 / 32.0
KAPPA_3_32 = 3.0 / 32.0
GATE_5_32 = 5.0 / 32.0
SPARK_ANGLE_DEG = 138.88


@dataclasses.dataclass(frozen=True)
class MaxwellObs:
    f0_hz: float
    Q: float


def F_s5_to_f0Q(
    *,
    x: np.ndarray,
    A: float,
    tau: float,
    kappa: float,
    sigma: int,
    u: float,
) -> MaxwellObs:
    """
    File-backed map from (carrier+state) -> (f0, Q).

    Implementation strategy:
    - f0 is anchored at 2.1235 GHz and modulated by a bounded geometric factor from x and W7.
    - Q is anchored at 11.85 and modulated by tau/kappa with hysteresis-like damping.
    """
    x = np.asarray(x, dtype=float).reshape(-1)
    if x.size != 6:
        # fall back to safe normalization
        x = np.pad(x[:6], (0, max(0, 6 - x.size)))
    xn = float(np.linalg.norm(x)) or 1.0
    x = x / xn

    # geometric modulation in [-0.1, +0.1]
    g = float(np.tanh(np.dot(x, np.array([1, -1, 1, -1, 1, -1], dtype=float)) * 0.5))
    w = float(math.tanh((A - W7_EXACT) * 4.0))
    mod_f = 1.0 + 0.05 * g + 0.05 * w

    # hysteresis-ish Q damping: higher tau reduces Q, higher kappa reduces Q
    tau_term = float(1.0 / (1.0 + max(0.0, tau)))
    kap_term = float(1.0 / (1.0 + 64.0 * max(0.0, kappa - KAPPA_1_32)))
    sig_term = 1.0 - 0.02 * (1 if sigma < 0 else 0)
    u_term = float(1.0 / (1.0 + 0.2 * abs(u)))

    f0 = 2.1235e9 * mod_f
    Q = 11.85 * (0.4 + 0.6 * tau_term) * (0.6 + 0.4 * kap_term) * sig_term * u_term
    return MaxwellObs(f0_hz=float(f0), Q=float(Q))


def d_sep(*, x: np.ndarray, x_star: np.ndarray | None = None) -> float:
    """
    Separatrix/attractor distance metric used by B_sep.
    Default attractor: a fixed W7-aligned direction in R^6.
    """
    x = np.asarray(x, dtype=float).reshape(-1)
    if x.size != 6:
        x = np.pad(x[:6], (0, max(0, 6 - x.size)))
    if x_star is None:
        x_star = np.array([1, 1, 1, -1, -1, -1], dtype=float)
    x_star = np.asarray(x_star, dtype=float).reshape(-1)
    x_star = x_star / (float(np.linalg.norm(x_star)) or 1.0)
    x = x / (float(np.linalg.norm(x)) or 1.0)
    # chord distance on S5
    return float(np.linalg.norm(x - x_star))


def PatchClass(
    *,
    pi: float,
    kappa: float,
    sigma: int,
    l: int,
    is_flash: bool = False,
    is_gateway: bool = False,
) -> str:
    """
    Explicit classifier mapping continuous state -> 13 patch labels.

    Patch labels supported:
    - sheet_id:1,2,3,4,10,11,12,13,14
    - flash:center_in, flash_bridge
    - gateway_peak
    - mediator:synthetic_alpha (reserved for expansion; returned only if is_gateway and kappa>=3/32)
    """
    if is_flash:
        return "flash:center_in" if abs(pi) <= W7_EXACT else "flash_bridge"
    if is_gateway:
        return "mediator:synthetic_alpha" if kappa >= KAPPA_3_32 else "gateway_peak"

    # Gate bands split territory
    if kappa >= KAPPA_3_32:
        # compression region: sheets 10-14 vs 11-13 depending on sigma/l
        if sigma >= 0 and l >= 0:
            return "sheet_id:10"
        if sigma >= 0 and l < 0:
            return "sheet_id:14"
        if sigma < 0 and l >= 0:
            return "sheet_id:11"
        return "sheet_id:13"

    # stable leakage near 1/32: core sheets 1-4 based on pi quadrant
    if abs(pi) <= W7_EXACT:
        # inside W7 band
        if pi >= 0 and sigma >= 0:
            return "sheet_id:1"
        if pi >= 0 and sigma < 0:
            return "sheet_id:2"
        if pi < 0 and sigma >= 0:
            return "sheet_id:3"
        return "sheet_id:4"

    # outside W7 band but below compression: map to 12/13/14 by leg
    if l >= 0:
        return "sheet_id:12"
    return "sheet_id:14"


def SeamAct(*, u_patch: str, v_patch: str, contact_score: float, drift: float) -> float:
    """
    Activation map for a seam edge (patch pair) -> activation strength in [0,1].
    """
    c = max(0.0, min(1.0, float(contact_score)))
    d = max(0.0, float(drift))
    # penalize drift and non-symmetric patch pairs
    asym_pen = 0.9 if (u_patch.startswith("sheet_id") and v_patch.startswith("sheet_id")) else 0.75
    return float(asym_pen * c / (1.0 + 0.2 * d))


def Phi_traits(*, x: np.ndarray, A: float, tau: float, kappa: float, u: float) -> np.ndarray:
    """
    Feature extractor producing a low-dim trait vector before Quant128.
    """
    x = np.asarray(x, dtype=float).reshape(-1)
    if x.size != 6:
        x = np.pad(x[:6], (0, max(0, 6 - x.size)))
    x = x / (float(np.linalg.norm(x)) or 1.0)
    # traits: [W7-projection, gate level, hysteresis, drive]
    w7_proj = float(np.dot(x, np.array([1, -1, 1, -1, 1, -1], dtype=float)) / 6.0)
    gate = float(kappa / KAPPA_1_32)
    hyst = float(math.tanh((A - W7_EXACT) * 8.0) * (1.0 / (1.0 + max(0.0, tau))))
    drive = float(math.tanh(u))
    return np.array([w7_proj, gate, hyst, drive], dtype=np.float32)


def Quant128(traits: np.ndarray, *, offsets: Iterable[float] = (0.0, 0.0, 0.0, 0.0)) -> tuple[int, int, int, int]:
    """
    Quantizer mapping traits -> 128-grid coordinates per trait dimension.
    """
    t = np.asarray(traits, dtype=float).reshape(-1)
    if t.size != 4:
        t = np.pad(t[:4], (0, max(0, 4 - t.size)))
    off = np.asarray(list(offsets), dtype=float).reshape(-1)
    if off.size != 4:
        off = np.pad(off[:4], (0, max(0, 4 - off.size)))
    z = t + off
    # map each dim from [-1,1] into [0,127]
    q = []
    for v in z.tolist():
        vv = max(-1.0, min(1.0, float(v)))
        qi = int(round((vv + 1.0) * 63.5))
        qi = max(0, min(127, qi))
        q.append(qi)
    return (q[0], q[1], q[2], q[3])


def snap_ratio(observed: float, *, step: float) -> float:
    """
    Returns observed / snapped where snapped is the nearest non-zero multiple of step.
    Used to compute 1+epsilon style detuning ratios.
    """
    if step <= 0:
        return float("nan")
    k = int(round(observed / step))
    if k == 0:
        k = 1 if observed >= 0 else -1
    snapped = k * step
    return float(observed / snapped)

