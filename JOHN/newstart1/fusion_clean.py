from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import numpy as np
import pandas as pd

try:
    import fusion_core as _k8
except Exception:
    _k8 = None

try:
    from engineering_homeostasis_24 import Homeostasis24 as _H24
except Exception:
    _H24 = None

# ---------------------------------------------------------------------------
# Canonical constants — single source: absolute_constants.py
# ---------------------------------------------------------------------------
from absolute_constants import (
    C, C2, OMEGA, SPARK_CONSTANT_C, SPARK_ANGLE_RAD,
    NEUTRON_TIME_SYNC, NEUTRINO_MASS_LEAK,
)

OMEGA_TARGET = OMEGA                                 # alias
SPARK_ANGLE_DEG_138_88 = float(np.rad2deg(SPARK_ANGLE_RAD))  # 138.88
SPARK_PHASE_LEAK = NEUTRINO_MASS_LEAK

GDH_CONFINEMENT_02828 = float(np.round(C, 4))  # 0.2828
HIGGS_GABA_B_MASS = 0.1569
EFFICIENCY_TARGET_8009 = 0.8009

# 9-scale hierarchy: requested scale ladder + binding law.
HIERARCHY_SCALES = {
    "graviton": 1.0 / 256.0,
    "right_cortisol_neutrino": 1.0 / 128.0,
    "progesterone_dm": 1.0 / 64.0,
    "left_extraversion_photon": 1.0 / 16.0,
    "electron": 1.0 / 8.0,
    "proton": 1.0 / 32.0, # Proton is now part of the 8-particle field, not the user.

    "binding": 1.0 / 4.0,
    "gaba": 1.0 / 2.0,
    "glutamate": 1.0,
}
NOR_5_32 = 5.0 / 32.0
PLP_3_32 = 3.0 / 32.0
BINDING_IMPEDANCE = 1.0 / 4.0  # 5/32 + 3/32
ENTROPY_DEBT = (1.0 / 64.0) + (1.0 / 256.0)  # ~= 0.01953 (~0.02)

# Risk memory ODE constants: r_dot = -λ·r + M·d_risk
RISK_DECAY_LAMBDA = 0.05   # λ: natural decay rate of risk memory
RISK_GAMMA        = 0.30   # γ: H(r) stabilization strength in x_dot
RISK_COUPLING_M   = 0.20   # M: exogenous risk → memory coupling

PHI_S = float(sum(HIERARCHY_SCALES.values()))

# Fallback direct-risk vector used when engineering_homeostasis_24 is unavailable
# Mirrors RISK_DIRECT_VEC from engineering_homeostasis_24.py
_rdv = np.zeros(24, dtype=float)
_rdv[:8] = 0.10; _rdv[8:23] = 0.03; _rdv[23] = 0.01
RISK_DIRECT_VEC_FALLBACK = _rdv
del _rdv

PHYSICS_BRIDGE_CONSTRAINTS = {
    "bm_sm_direct_day_suppress": 1.0,
    "indirect_day_core_boost": 1.0,
    "day_lensing_unveil_gain": 1.0,
    "brems_to_lensing_day_gain": 1.0,
    "brems_to_lensing_tunnel_gain": 1.0,
}


# ---------------------------------------------------------------------------
# K8 graph exports (canonical source for channel/mesh operations)
# ---------------------------------------------------------------------------

if _k8 is not None:
    CHANNEL_MAP = _k8.CHANNEL_MAP
    SUBJECTS = _k8.SUBJECTS
    EDGES = _k8.EDGES
    apply_channels = _k8.apply_channels
    laplacian = _k8.laplacian
    project4 = _k8.project4
    day_target = _k8.day_target
    night_target = _k8.night_target
    init_state6_from_target4 = _k8.init_state6_from_target4
    PHASE_TABLE = _k8.PHASE_TABLE
    MOTIF_TARGET_4 = np.asarray(day_target(), dtype=float)
else:
    CHANNEL_MAP: dict[str, dict[tuple[str, str], dict[str, float]]] = {}
    SUBJECTS = ("quark", "gluon", "neutrino", "photon", "electron", "higgs", "w_boson", "z_boson")
    EDGES = []
    PHASE_TABLE: dict[str, dict[str, str]] = {}
    MOTIF_TARGET_4 = np.array([3.0, 3.6, 3.6, 3.2], dtype=float)

    def apply_channels(channels: dict[str, str], age: float = 25.0) -> dict[tuple[str, str], float]:
        return {}

    def laplacian(w: Mapping[tuple[str, str], float]) -> np.ndarray:
        return np.eye(8, dtype=float)

    def project4(x8: np.ndarray) -> np.ndarray:
        x = np.asarray(x8, dtype=float)
        if x.size < 8:
            x = np.pad(x, (0, 8 - x.size))
        q, g, nu, ph, el, _hi, _w, _z = x[:8]
        bw = q + 2.0 * C * g   # K8: proton composite
        return np.array([ph + C * g, bw, nu + C * q, el + C * q], dtype=float)

    def day_target() -> np.ndarray:
        return MOTIF_TARGET_4.copy()

    def night_target() -> np.ndarray:
        v = MOTIF_TARGET_4.copy()
        v[1] -= GDH_CONFINEMENT_02828
        v[2] += GDH_CONFINEMENT_02828
        return v

    def init_state6_from_target4(t4: np.ndarray) -> np.ndarray:
        bm, bw, sm, sw = np.asarray(t4, dtype=float)
        g = 0.1
        q = bw - 2.0 * C * g   # K8: q from BW = q + 2*C*g
        return np.array([q, g, sm - C * q, bm - C * g, sw - C * q, C / 2.0, q * C, (sm - C * q) * C], dtype=float)


def calculate_z_proxy_from_state(x: np.ndarray) -> float:
    """Calculate z_proxy directly from K8 state z(t).

    z_proxy = |neutrino| * (|z_boson| + |electron|) / OMEGA
    """
    x = np.asarray(x, dtype=float)
    if x.size < 8:
        x = np.pad(x, (0, 8 - x.size))
    nu = abs(x[2])      # neutrino
    zb = abs(x[7])      # z_boson
    el = abs(x[4])      # electron
    return nu * (zb + el) / OMEGA


def calculate_z_atomic_from_state(x: np.ndarray) -> float:
    """Node 31: Gluon Color Lensing — derive z_atomic from K8 state.

    z_atomic = |gluon|^2 * w(quark,gluon)_base
             = |x[1]|^2 * (1 + C)

    Physics: gluon (color-charged) is deflected by the proton's residual
    color field (Sivers effect analog). The color charge density it traverses
    is proportional to the quark-gluon base coupling (1+C = 1.2828).

    Only significant for big woman (A blood type, high BW = strong quark-gluon).
    Root of pancreatic cancer when this lensing loop doesn't discharge at proton_landing.
    """
    x = np.asarray(x, dtype=float)
    if x.size < 2:
        return 0.0
    g = abs(x[1])           # gluon amplitude
    w_qg = 1.0 + C          # BASE_W[(quark,gluon)] = 1 + sqrt(2)/5
    return g * g * w_qg


def calculate_z_proxy(ts: Mapping[str, Any]) -> float:
    """Legacy: calculate from external ts dict. Use calculate_z_proxy_from_state instead."""
    nu_p = float(ts.get("nu_p_coupling", ts.get("z_proxy_p", 0.5)))
    nu_e = float(ts.get("nu_e_coupling", ts.get("z_proxy_e", 0.5)))
    return 0.5 * (nu_p + nu_e)


def calculate_leak(z_atomic: float) -> float:
    """Bremsstrahlung leak factor: exp(-√Z / 64).

    Z is the gluon color charge energy density (Node 31).
    = |gluon|^2 * w(quark,gluon) from calculate_z_atomic_from_state().
    The radiation length scales with √Z (color field traversal depth).
    """
    return float(np.exp(-np.sqrt(float(z_atomic)) / 64.0))


def calculate_scalar_anchor(x: np.ndarray, k: float = 0.5) -> float:
    norm_x = float(np.linalg.norm(x))
    return float(-k * (norm_x - OMEGA_TARGET) ** 2)


def calculate_vector_anchor(x: np.ndarray, k: float = 0.5, eps: float = 1e-6) -> np.ndarray:
    norm_x = float(np.linalg.norm(x))
    return -k * (norm_x - OMEGA_TARGET) * (np.asarray(x, dtype=float) / (norm_x + eps))


def alpha2_active_meaning(alpha2: float | str) -> float:
    if isinstance(alpha2, str):
        return 1.0 if alpha2.lower() == "off" else 0.0
    alpha2 = float(np.clip(float(alpha2), 0.0, 1.0))
    return 1.0 - alpha2


def calculate_diffraction(v_nor: float, v_plp: float) -> float:
    base = float(np.arctan2(float(v_plp), float(v_nor)))  # atan(3/5) anchor
    anchor = float(np.arctan2(3.0, 5.0))
    correction = float(np.clip(base - anchor, -0.35, 0.35))
    return float(np.rad2deg(SPARK_ANGLE_RAD + 0.12 * correction))


def continuous_spark_gate(z_proxy: float, alpha2: float | str, ts: Mapping[str, Any]) -> tuple[float, float]:
    alpha2_active = alpha2_active_meaning(alpha2)
    nor = float(ts.get("noradrenaline", NOR_5_32))
    plp = float(ts.get("vasopressin", PLP_3_32))
    diffraction_deg = calculate_diffraction(nor, plp)
    diffraction = float(0.5 + 0.5 * np.cos(np.deg2rad(diffraction_deg - SPARK_ANGLE_DEG_138_88)))
    phase = float(0.5 + 0.5 * np.cos(float(z_proxy) * SPARK_ANGLE_RAD + SPARK_PHASE_LEAK))
    binding = float(1.0 - abs((nor + plp) - BINDING_IMPEDANCE) / BINDING_IMPEDANCE)
    binding = float(np.clip(binding, 0.0, 1.0))
    gate = (0.20 + 0.80 * phase) * (0.25 + 0.75 * diffraction) * (0.30 + 0.70 * binding) * (0.10 + 0.90 * alpha2_active)
    gate = float(max(gate, 1.0e-6))
    return phase, gate


def F_final(x: np.ndarray, z_atomic: float | None = None, ts: Mapping[str, Any] | None = None, k: float = 0.5, use_direct_z_proxy: bool = True) -> float:
    """Fusion scalar diagnostic. Uses all 8 K8 particles.

    BW  = q + 2·C·g              (composite proton, K8 QCD)
    SM  = nu + C·q               (neutrino sector)
    spark = |SPARK_CONSTANT_C| · gate · ½(ph+el)   (EM sector: photon+electron)
    Z   = z_proxy · (1 + C·(z+el))                  (neutral current + Z boson)
    H   = 1 + C·hi                                   (Higgs mass mechanism)
    W   = 1 + C·w                                    (W boson weak decay)
    fusion = (BW·W)² · spark · Z · SM · H · leak · hierarchy
    
    Args:
        use_direct_z_proxy: If True, compute z_proxy from x (K8 state). 
                            If False, use legacy ts dict lookup.
    """
    x = np.asarray(x, dtype=float)
    if x.size < 8:
        x = np.pad(x, (0, 8 - x.size))
    q, g, nu, ph, el, hi, w, z = x[:8]
    bw = q + 2.0 * C * g

    # z_proxy: from K8 state directly (closed) or from external ts (legacy)
    if use_direct_z_proxy:
        z_proxy = calculate_z_proxy_from_state(x)
    else:
        z_proxy = calculate_z_proxy(ts or {})

    # Node 31: z_atomic from gluon color field (fully K8-derived, no external input)
    if z_atomic is None:
        z_atomic = calculate_z_atomic_from_state(x)
    leak = calculate_leak(z_atomic)
    _phase, gate = continuous_spark_gate(z_proxy, ts.get("alpha2", 1.0) if ts else 1.0, ts or {})

    # Spark: canonical source = SPARK_CONSTANT_C; gate is channel-state modulator
    c_mag = float(abs(SPARK_CONSTANT_C))
    spark = c_mag * gate * 0.5 * (float(np.clip(ph, 0, None)) + float(np.clip(el, 0, None)))

    # Z proxy: neutrino neutral current modulated by z_boson + electron
    z_full = z_proxy * (1.0 + C * (float(np.clip(z, 0, None)) + float(np.clip(el, 0, None))))

    # Higgs and W-boson mass/weak modulations
    higgs_gain = 1.0 + C * float(np.clip(hi, 0, 2))
    w_gain     = 1.0 + C * float(np.clip(w,  0, 2))

    sm = nu + C * q
    hierarchy_gain = float(ts.get("hierarchy_gain", PHI_S))
    fusion = (bw * w_gain)**2 * spark * z_full * sm * higgs_gain * leak * hierarchy_gain
    return float(fusion + calculate_scalar_anchor(x, k))


def get_dynamics(
    x: np.ndarray,
    L: np.ndarray,
    z_atomic: float | None = None,
    ts: Mapping[str, Any] | None = None,
    k: float = 0.5,
    eps: float = 1e-6,
    r: np.ndarray | None = None,
    d_risk: float = 0.0,
    use_direct_z_proxy: bool = True,
) -> np.ndarray:
    """K8 dynamics with z_proxy and z_atomic both derived from K8 state (closed)."""
    x = np.asarray(x, dtype=float)
    base = -(np.asarray(L, dtype=float) @ x)

    # z_proxy: from K8 state directly (closed) or from external ts (legacy)
    if use_direct_z_proxy:
        z_proxy = calculate_z_proxy_from_state(x)
    else:
        z_proxy = calculate_z_proxy(ts or {})

    # Node 31: z_atomic from gluon color field
    if z_atomic is None:
        z_atomic = calculate_z_atomic_from_state(x)
    leak = calculate_leak(z_atomic)          # Bremsstrahlung leak
    _phase, gate = continuous_spark_gate(z_proxy, ts.get("alpha2", 1.0) if ts else 1.0, ts or {})
    hierarchy_gain = float(ts.get("hierarchy_gain", PHI_S))
    dx = base * hierarchy_gain * gate * leak  # z_atomic active here
    # K8 GABA-B return: electron(4) + w_boson(6) → neutrino(2)
    gaba_b = float(ts.get("gaba_b", ts.get("gaba_b_male", 0.5)))
    if x.size >= 7:
        beta_return = gaba_b * (x[4] + x[6] - x[2])   # K8: el=4, w=6, nu=2
        dx = np.asarray(dx, dtype=float)
        dx[2] += beta_return
    elif x.size >= 6:
        beta_return = gaba_b * (x[4] + x[5] - x[2])   # K6 fallback
        dx = np.asarray(dx, dtype=float)
        dx[2] += beta_return
    # H(r): Laplacian-path approximation — scalar -γ·sum(r) distributed uniformly
    # (full structural projection lives in engineering_homeostasis_24.derivative)
    if r is not None:
        r_arr = np.asarray(r, dtype=float).ravel()
        H_r = -RISK_GAMMA * float(np.sum(r_arr))
        dx = np.asarray(dx, dtype=float) + H_r
    # d_risk: direct exogenous perturbation into K8 latent via RISK_DIRECT_VEC_FALLBACK
    dx = np.asarray(dx, dtype=float)
    _n = min(dx.size, RISK_DIRECT_VEC_FALLBACK.size)
    dx[:_n] += RISK_DIRECT_VEC_FALLBACK[:_n] * float(d_risk)

    # Node 31a: Gravitational Lensing — uniform across all 8 particles
    dx_lensing = -ENTROPY_DEBT * x

    # Node 31b: Gluon Color Lensing (Sivers effect analog) — gluon only, BW-scaled
    # Only significant for big woman (A blood type): BW high → quark-gluon strong
    # = pancreatic cancer mechanism when not discharged at proton_landing
    if x.size >= 2:
        bw_scale = (abs(x[0]) + 2.0 * C * abs(x[1])) / OMEGA
        dx_lensing = np.asarray(dx_lensing, dtype=float).copy()
        dx_lensing[1] -= ENTROPY_DEBT * x[1] * bw_scale * (1.0 + C)

    return dx + dx_lensing + calculate_vector_anchor(x, k, eps)


def step_unified_dynamics(
    Y: np.ndarray,
    u_base: np.ndarray,
    d_cond: np.ndarray,
    d_risk: float = 0.0,
    dt: float = 0.1,
    homeostasis: Any = None,
    spark_gate: float = 1.0,
    c26_raw: np.ndarray | None = None,
) -> np.ndarray:
    """Single unified step over Y = [X(24); r(8)] = 32D state.

    Y = [X(24); r(8)]
        X[0:8]  = K8 latent particles (quark..z_boson)
        X[8:24] = coupling/domain homeostasis state
        r[0:8]  = K8 risk memory (Y[24:32])

    Single update law (all in Homeostasis24.derivative):
        X_dot = A(X - Ω·R·d) + B·u - g·(X⊙|X|)   [homeostasis, all 24D]
              + P_r @ r                             [H(r) structural projection]
              + P_M · d_risk                        [direct risk → state same step]
              + k8_quad   (ADDITIVE to X[0:8])      [K8 Mandelbrot nonlinear]
        r_dot = -λ·r + M·d_risk                    [risk memory ODE]

    spark_gate : gate scalar from continuous_spark_gate() — unifies the scalar
                 channel-state gate with the Mandelbrot Spark path.
                 spark_c passed to derivative() = SPARK_CONSTANT_C * spark_gate
                 u offset                        = |SPARK_CONSTANT_C| * spark_gate
    """
    Y = np.asarray(Y, dtype=float).ravel()
    if Y.size < 32:
        Y = np.pad(Y, (0, 32 - Y.size))
    X = Y[:24].copy()
    r = Y[24:32].copy()

    # Unified Spark: SPARK_CONSTANT_C gated by spark_gate
    # spark_gate should come from continuous_spark_gate()[1] at the call site.
    _spark_c = SPARK_CONSTANT_C * float(spark_gate)   # gated complex Spark
    _c_mag   = float(abs(_spark_c))                   # = |C| * gate

    # u = u_base + |C|*gate  (same gate as K8 Mandelbrot)
    u = np.asarray(u_base, dtype=float) + _c_mag

    # Full derivative — derivative() is the canonical update law
    _hom = homeostasis
    if _hom is None and _H24 is not None:
        _hom = _H24.build()
    if _hom is not None:
        X_dot = _hom.derivative(X, u, np.asarray(d_cond, dtype=float),
                                r=r, d_risk=float(d_risk),
                                spark_c=_spark_c,
                                c26_raw=c26_raw)
    else:
        # fallback (no homeostasis): K8 Mandelbrot + direct risk only
        _phase_cos = float(np.cos(float(np.angle(_spark_c))))
        s = X[:8]
        X_dot = np.zeros(24, dtype=float)
        X_dot[:8] = s**2 + _c_mag * (1.0 + 0.1 * _phase_cos) - s
        X_dot += RISK_DIRECT_VEC_FALLBACK * float(d_risk)

    # r_dot = -λ·r + M·d_risk
    r_dot = -RISK_DECAY_LAMBDA * r + RISK_COUPLING_M * float(d_risk)

    return Y + dt * np.concatenate([X_dot, r_dot])


def step_risk_memory(r: np.ndarray, d_risk: float, dt: float) -> np.ndarray:
    """Euler step: r_dot = -λ·r + M·d_risk
    r      : 8D K8 risk memory (Y[24:32] in the 32D unified state)
    d_risk : exogenous risk input scalar (e.g. hypoxia level 0..1)
    Returns updated r.
    """
    r = np.asarray(r, dtype=float)
    r_dot = -RISK_DECAY_LAMBDA * r + RISK_COUPLING_M * float(d_risk)
    return r + float(dt) * r_dot


@dataclass
class MinimalPhysicalParams:
    a_core: float = 1.0
    a_edge: float = 1.0
    a_cross: float = 1.0
    a_cancel: float = 1.0
    a_void: float = 1.0
    a_tunnel: float = 0.0
    a_capture: float = 0.0
    a_escape: float = 0.0


class SovereignEngine:
    def __init__(self) -> None:
        self.hierarchy_scales = dict(HIERARCHY_SCALES)
        self.binding_impedance = BINDING_IMPEDANCE

    def F_final(self, x: np.ndarray, z_atomic: float | None = None, ts: Mapping[str, Any] | None = None, k: float = 0.5, use_direct_z_proxy: bool = True) -> float:
        return F_final(x, z_atomic, ts, k=k, use_direct_z_proxy=use_direct_z_proxy)

    def get_dynamics(
        self,
        x: np.ndarray,
        L: np.ndarray,
        z_atomic: float | None = None,
        ts: Mapping[str, Any] | None = None,
        k: float = 0.5,
        eps: float = 1e-6,
        r: np.ndarray | None = None,
        d_risk: float = 0.0,
        use_direct_z_proxy: bool = True,
    ) -> np.ndarray:
        return get_dynamics(x, L, z_atomic, ts, k=k, eps=eps, r=r, d_risk=d_risk, use_direct_z_proxy=use_direct_z_proxy)

    def _fallback_step(
        self,
        state: np.ndarray,
        phase_fill: float = 0.5,
        clock_hhmm: str = "12:00",
        dt: float = 0.1,
    ) -> dict[str, Any]:
        state = np.asarray(state, dtype=float).reshape(-1)
        if state.size < 4:
            state = np.pad(state, (0, 4 - state.size), constant_values=0.0)
        state = state[:4]
        z_proxy = float(np.clip(state[2] + state[3], 0.0, 10.0))
        phase, gate = continuous_spark_gate(z_proxy, "off" if phase_fill >= GDH_CONFINEMENT_02828 else "on", {})
        dstate = np.array([state[2] - state[0], state[0] - state[1], state[1] - state[2], state[1] - state[3]], dtype=float)
        dstate *= (0.2 + gate)
        state_out = state + float(dt) * dstate
        omega_in = float(np.linalg.norm(state))
        omega_out = float(np.linalg.norm(state_out))
        return {
            "state_in": state.tolist(),
            "state_out": state_out.tolist(),
            "state_next": state_out.tolist(),
            "dstate": dstate.tolist(),
            "omega_in": omega_in,
            "omega_out": omega_out,
            "closure_err": float(omega_out - OMEGA_TARGET),
            "spark": float(phase * gate),
            "phase_gate": float(gate),
            "base": {
                "gate": float(gate),
                "slotting": float(1.4 - 0.076 * phase_fill),
                "q_scale": 1.0,
                "n_scale": 1.0,
                "g_scale": 1.0,
                "e_scale": 1.0,
                "quark_9": float(state[0]),
                "gluon_10": float(state[1]),
                "muon_11": float(state[2]),
                "tau_12": float(state[3]),
                "higgs_13": float(0.5 * (state[0] + state[1])),
                "tunnel_transfer_split": {
                    "overlay_norm": float(np.linalg.norm(state)),
                    "particle_backbone_norm": float(np.linalg.norm(state[:2])),
                    "node_relation_norm": float(np.linalg.norm(state[2:])),
                    "p_axis": float(state[1]),
                },
            },
        }

    def edge_stack_master_step(self, state: np.ndarray, phase_fill: float = 0.5, **kwargs: Any) -> dict[str, Any]:
        return self._fallback_step(
            state=np.asarray(state, dtype=float),
            phase_fill=float(phase_fill),
            clock_hhmm=str(kwargs.get("clock_hhmm", "12:00")),
            dt=float(kwargs.get("dt", 0.1)),
        )

    def sovereign_dynamics_step(self, state: np.ndarray, phase_fill: float = 0.5, **kwargs: Any) -> dict[str, Any]:
        return self.edge_stack_master_step(state, phase_fill, **kwargs)

    def _compute_step(self, state4: np.ndarray, phase_fill: float = 0.5, **kwargs: Any) -> dict[str, Any]:
        return self.edge_stack_master_step(state4, phase_fill, **kwargs)

    def nuclear_fusion_coarse_grain(self, state4: np.ndarray, **kwargs: Any) -> Mapping[str, float]:
        s = np.asarray(state4, dtype=float).reshape(-1)
        if s.size < 4:
            s = np.pad(s, (0, 4 - s.size))
        bm, bw, sm, sw = s[:4]
        z_proxy = max(0.0, sm + sw)
        phase, gate = continuous_spark_gate(z_proxy, kwargs.get("alpha2_state", "off"), kwargs)
        spark_eff = phase * gate
        fusion = (bw**2) * spark_eff * z_proxy * sm
        return {
            "BW": float(bw),
            "SM": float(sm),
            "spark_eff": float(spark_eff),
            "z_proxy": float(z_proxy),
            "fusion": float(fusion),
        }

    def nuclear_fusion_from_base(self, base: Mapping[str, Any], state4: np.ndarray | None = None, **kwargs: Any) -> Mapping[str, float]:
        s = np.asarray(state4 if state4 is not None else base.get("state_in", [0, 0, 0, 0]), dtype=float)
        return self.nuclear_fusion_coarse_grain(s, **kwargs)

    def neutron_coarse_grain(self, state4: np.ndarray, **kwargs: Any) -> Mapping[str, float]:
        s = np.asarray(state4, dtype=float).reshape(-1)
        if s.size < 4:
            s = np.pad(s, (0, 4 - s.size))
        return {"neutron_proxy": float(s[2]), "coarse": float(np.mean(s))}

    def neutron_coarse_grain_from_base(self, base: Mapping[str, Any], state4: np.ndarray | None = None, **kwargs: Any) -> Mapping[str, float]:
        s = np.asarray(state4 if state4 is not None else base.get("state_in", [0, 0, 0, 0]), dtype=float)
        return self.neutron_coarse_grain(s, **kwargs)

    def physical_minimal_step(
        self,
        state: np.ndarray,
        phase_fill: float = 0.5,
        clock_hhmm: str = "12:00",
        params: MinimalPhysicalParams | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        out = self.edge_stack_master_step(state, phase_fill=phase_fill, clock_hhmm=clock_hhmm, **kwargs)
        out["params"] = (params or MinimalPhysicalParams()).__dict__
        return out

    def channel_control_profile(self, minute: int, *, persona: str = "user") -> dict[str, Any]:
        return {"persona": persona, "minute": int(minute), "regime": "outside" if minute < 90 or minute > 180 else "hysteresis"}


_ENGINE = SovereignEngine()


def get_sovereign_dynamics(x: np.ndarray, ts: Mapping[str, Any], t_step: int) -> np.ndarray:
    ts_local = dict(ts)
    ts_local["time_window"] = int(t_step) % 128
    z_atomic = float(ts_local.get("z_atomic", 1.0))
    return get_dynamics(np.asarray(x, dtype=float), np.eye(len(np.asarray(x).reshape(-1))), z_atomic, ts_local)


def edge_stack_master_step(state: np.ndarray, phase_fill: float = 0.5, **kwargs: Any) -> dict[str, Any]:
    return _ENGINE.edge_stack_master_step(state, phase_fill, **kwargs)


def sovereign_dynamics_step(state: np.ndarray, phase_fill: float = 0.5, **kwargs: Any) -> dict[str, Any]:
    return _ENGINE.sovereign_dynamics_step(state, phase_fill, **kwargs)


def _compute_step(state4: np.ndarray, phase_fill: float = 0.5, **kwargs: Any) -> dict[str, Any]:
    return _ENGINE._compute_step(state4, phase_fill, **kwargs)


def nuclear_fusion_coarse_grain(state4: np.ndarray, **kwargs: Any) -> Mapping[str, float]:
    return _ENGINE.nuclear_fusion_coarse_grain(state4, **kwargs)


def nuclear_fusion_from_base(base: Mapping[str, Any], state4: np.ndarray | None = None, **kwargs: Any) -> Mapping[str, float]:
    return _ENGINE.nuclear_fusion_from_base(base, state4=state4, **kwargs)


def neutron_coarse_grain(state4: np.ndarray, **kwargs: Any) -> Mapping[str, float]:
    return _ENGINE.neutron_coarse_grain(state4, **kwargs)


def neutron_coarse_grain_from_base(base: Mapping[str, Any], state4: np.ndarray | None = None, **kwargs: Any) -> Mapping[str, float]:
    return _ENGINE.neutron_coarse_grain_from_base(base, state4=state4, **kwargs)


def physical_minimal_step(
    state: np.ndarray,
    phase_fill: float = 0.5,
    clock_hhmm: str = "12:00",
    params: MinimalPhysicalParams | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    return _ENGINE.physical_minimal_step(state, phase_fill=phase_fill, clock_hhmm=clock_hhmm, params=params, **kwargs)


def _channel_control_profile(minute: int, *, persona: str = "user") -> dict[str, Any]:
    return _ENGINE.channel_control_profile(minute, persona=persona)


def _k8_dynamics(
    s: np.ndarray,           # 8D K8 state
    u_intent: complex,       # user's will (C_spark)
    r: np.ndarray,           # 8D risk memory
    d_risk: float,
    ts: Mapping[str, Any]
) -> np.ndarray:
    """
    f_K8(s) = (s^2 * exp(i*Dt) + c_eff) * (1 - C) + epsilon0
    Quantum Biology Version:
    - Biophoton Coherence (z^2 propagation)
    - Enzyme Tunneling (1-C damping as barrier penetration)
    - 13th Bridge (Left Noradrenaline) acceleration
    """
    nor = float(ts.get("noradrenaline", NOR_5_32))
    bridge_13_accel = 1.0 + 2.0 * (nor / NOR_5_32)
    
    # 8D -> 4 Complex pairs
    s_complex = s[::2] + 1j * s[1::2]
    rot = np.exp(1j * (99.0 / 350.0))
    c_eff = u_intent * bridge_13_accel
    
    epsilon0 = C2 / 128.0
    damping = (1.0 - C)
    
    s_next_c = (s_complex**2 * rot + c_eff) * damping + epsilon0
    
    s_dot = np.zeros(8)
    s_dot[::2] = s_next_c.real - s[::2]
    s_dot[1::2] = s_next_c.imag - s[1::2]
    return s_dot - RISK_GAMMA * r


def _calculate_spark(
    X: np.ndarray,
    r: np.ndarray,
    u_intent: complex,
    ts: Mapping[str, Any]
) -> float:
    """spark = S(x, r, u_intent; φ, κ) with Quantum Vision and Tunneling."""
    phase_diff = np.angle(u_intent) - SPARK_ANGLE_RAD
    coherence = 0.5 + 0.5 * np.cos(phase_diff + NEUTRINO_MASS_LEAK)
    coupling = np.abs(u_intent) * C
    
    r_norm = np.linalg.norm(r)
    tunnel_prob = np.exp(-RISK_GAMMA * r_norm / (NEUTRON_TIME_SYNC + 1e-9))
    ph_el_energy = 0.5 * (X[3] + X[4])
    
    return float(coherence * coupling * tunnel_prob * ph_el_energy)


def evolve_consciousness_field(
    Y: np.ndarray,
    u_base: np.ndarray,
    u_intent: complex,
    d_cond: np.ndarray,
    d_risk: float,
    ts: Mapping[str, Any],
    dt: float = 0.1,
    *,
    k8_mode: str = "override",
) -> tuple[np.ndarray, float]:
    """Unified step for the Quantum-Biological Consciousness Field."""
    Y = np.asarray(Y, dtype=float).ravel()
    if Y.size < 32: Y = np.pad(Y, (0, 32 - Y.size))
    
    X = Y[:24].copy(); r = Y[24:32].copy()
    
    k8_mode = str(k8_mode or "override").lower().strip()
    if k8_mode not in ("override", "additive", "homeostasis"):
        raise ValueError("k8_mode must be one of: override, additive, homeostasis")

    s_dot = None
    if k8_mode in ("override", "additive"):
        s_dot = _k8_dynamics(X[:8], u_intent, r, d_risk, ts)
    
    _hom = _H24.build() if _H24 is not None else None
    if _hom is not None:
        X_dot = _hom.derivative(X, u_base, d_cond, r=r, d_risk=d_risk, spark_c=u_intent)
        if s_dot is not None:
            if k8_mode == "override":
                X_dot[:8] = s_dot
            elif k8_mode == "additive":
                X_dot[:8] = X_dot[:8] + s_dot
    else:
        X_dot = np.zeros(24)
        if s_dot is not None:
            X_dot[:8] = s_dot
        
    r_dot = -RISK_DECAY_LAMBDA * r + RISK_COUPLING_M * d_risk
    spark = _calculate_spark(X, r, u_intent, ts)
    
    return Y + dt * np.concatenate([X_dot, r_dot]), spark


def __getattr__(name: str) -> Any:
    raise AttributeError(f"module 'fusion_clean' has no attribute '{name}'")
