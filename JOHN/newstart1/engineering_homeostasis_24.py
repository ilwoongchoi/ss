from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd

from absolute_constants import C, OMEGA, SPARK_CONSTANT_C, SPARK_ANGLE_RAD

def _load_channel_edge_map() -> dict:
    """Lazy loader: prefer fusion_clean (canonical K8), fall back to fusion_core."""
    try:
        import fusion_clean as _fc
        if hasattr(_fc, "CHANNEL_MAP") and _fc.CHANNEL_MAP:
            return _fc.CHANNEL_MAP
    except Exception:
        pass
    try:
        from fusion_core import CHANNEL_MAP
        return CHANNEL_MAP
    except Exception:
        return {}

C2 = float(C * C)  # 0.08

# ── Raw 30-channel ordering (matches fusion_clean/fusion_core.CHANNEL_MAP insertion order) ──
_RAW_CHANNELS_30 = [
    "gdh_gluon", "female_gaba_b_latdorsi", "left_acetyl_coa", "male_left_5ht",
    "female_left_noradrenaline", "left_temporalis_5ht1a", "left_estrogen", "right_love",
    "hypoxia",          # idx=8  → d_risk (exogenous, NOT control)
    "right_dopamine", "vasopressin_female", "male_oxytocin",
    "muscle_a",         # idx=12 → merged into "muscle"
    "muscle_b",         # idx=13 → merged into "muscle"
    "right_5ht1b_synchrotron",
    "right_androgen", "left_endorphin", "left_frontalis_d2",
    "right_occipitalis_gaba_a",
    "male_gaba_a",
    "right_acetylcholine",
    "left_extraversion", "right_extraversion",
    "male_right_extraversion",
    "glucocorticoid", "right_cortisol", "right_alpha_2", "male_gaba_b",
    "left_eyelid_couple",
    "right_eyelid_couple",
]
_HYPOXIA_IDX = _RAW_CHANNELS_30.index("hypoxia")  # 8
RAW_CHANNEL_IDX = {name: index for index, name in enumerate(_RAW_CHANNELS_30)}

# ── 30-channel control basis (N=30, no merging) ──────────────────────────────────
# All 30 raw channels are separate control nodes — no merging performed.
# hypoxia (idx 8) is a regular control node (NOT separated out).
# muscle_a (12), muscle_b (13), male_gaba_a (19), male_right_extraversion (23)
# are each independent. left_eyelid_couple (28) and right_eyelid_couple (29)
# are the bilateral EM observers — meet at photon node.
N = 24
CHANNELS_24 = _RAW_CHANNELS_30[:N]
CHANNEL24_IDX = {name: i for i, name in enumerate(CHANNELS_24)}

CHANNEL_EDGE_MAP = _load_channel_edge_map()


def project_channels(c26: np.ndarray) -> tuple[np.ndarray, float]:
    """Return (u24, d_risk).
    d_risk = max(hypoxia, mean(eyelid couples))
    """
    c = np.asarray(c26, dtype=float).ravel()
    if c.size < 26:
        c = np.pad(c, (0, 26 - c.size))
    
    # Hypoxia is at index 8 in _RAW_CHANNELS_30
    hypoxia = float(c[8])
    
    # Eyelid couples are at indices 28, 29 in _RAW_CHANNELS_30
    # For a 26-channel input, we use a default if not present
    d_risk = hypoxia
    return c[:N], d_risk
# OMEGA, C, SPARK_CONSTANT_C imported from absolute_constants (single source)

PARTICLES_24 = [
    "quark",        # K8 latent [0]
    "gluon",        # K8 latent [1]
    "neutrino",     # K8 latent [2]
    "photon",       # K8 latent [3]
    "electron",     # K8 latent [4]
    "higgs",        # K8 latent [5]
    "w_boson",      # K8 latent [6]
    "z_boson",      # K8 latent [7]
    "mode_q_g",     # [8]
    "mode_q_nu",    # [9]
    "mode_q_ph",    # [10]
    "mode_q_w",     # [11]
    "mode_q_e",     # [12]
    "mode_g_nu",    # [13]
    "mode_g_ph",    # [14]
    "mode_g_w",     # [15]
    "mode_g_e",     # [16]
    "mode_nu_ph",   # [17]
    "mode_nu_z",    # [18]
    "mode_nu_e",    # [19]
    "mode_ph_w",    # [20]
    "mode_ph_e",    # [21]
    "mode_w_e",     # [22]
    "anchor_self",  # [23]
]
# backwards-compat aliases (self-referential)
PARTICLES_24 = PARTICLES_24

DOMAINS_24 = [
    "self",                       # 0  anchor
    "economy",                    # 1  anchor
    "universe",                   # 2  anchor
    "quark_sector",               # 3
    "gluon_sector",               # 4
    "neutrino_sector",            # 5
    "photon_sector",              # 6
    "electron_sector",            # 7
    "higgs_sector",               # 8
    "w_boson_sector",             # 9  (was proton_sector — mass/weak)
    "z_boson_sector",             # 10
    "quark_gluon_coupling",       # 11
    "quark_w_coupling",           # 12 QCD→weak
    "gluon_w_coupling",           # 13 QCD→weak
    "photon_w_coupling",          # 14 spark source
    "photon_electron_coupling",   # 15 spark source
    "neutrino_z_coupling",        # 16 Z-proxy
    "neutrino_electron_coupling", # 17 Z-proxy + lepton
    "w_boson_electron_coupling",  # 18 weak decay
    "neutrino_photon_coupling",   # 19
    "higgs_w_coupling",           # 20 Higgs mechanism
    "higgs_z_coupling",           # 21 Higgs mechanism
    "quark_neutrino_coupling",    # 22
    "quark_electron_coupling",    # 23
]
# backwards-compat aliases (self-referential)
DOMAINS_24 = DOMAINS_24

DOMAIN_IDX = {name: index for index, name in enumerate(DOMAINS_24)}

PARTICLE_DOMAIN = {
    "quark":    "quark_sector",
    "gluon":    "gluon_sector",
    "neutrino": "neutrino_sector",
    "photon":   "photon_sector",
    "electron": "electron_sector",
    "higgs":    "higgs_sector",
    "w_boson":  "w_boson_sector",
    "z_boson":  "z_boson_sector",
}

EDGE_DOMAIN = {
    ("quark",    "gluon"):    "quark_gluon_coupling",
    ("quark",    "neutrino"): "quark_neutrino_coupling",
    ("quark",    "electron"): "quark_electron_coupling",
    ("quark",    "w_boson"):  "quark_w_coupling",
    ("gluon",    "w_boson"):  "gluon_w_coupling",
    ("neutrino", "photon"):   "neutrino_photon_coupling",
    ("neutrino", "z_boson"):  "neutrino_z_coupling",
    ("neutrino", "electron"): "neutrino_electron_coupling",
    ("photon",   "w_boson"):  "photon_w_coupling",
    ("photon",   "electron"): "photon_electron_coupling",
    ("w_boson",  "electron"): "w_boson_electron_coupling",
    ("higgs",    "w_boson"):  "higgs_w_coupling",
    ("higgs",    "z_boson"):  "higgs_z_coupling",
}


def _canonical_edge(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return (a, b) if (a, b) in EDGE_DOMAIN else (b, a)


def infer_channel_primary_domain(channel_name: str) -> str:
    edge_dict = CHANNEL_EDGE_MAP.get(channel_name, {})
    if not edge_dict:
        return "universe"
    scores: dict[str, float] = {}
    for edge, states in edge_dict.items():
        canon = _canonical_edge(edge)
        domain = EDGE_DOMAIN.get(canon)
        if domain is None:
            continue
        state_strength = max(abs(float(states.get("on", 0.0))), abs(float(states.get("off", 0.0))))
        scores[domain] = scores.get(domain, 0.0) + state_strength
    if not scores:
        return "universe"
    return max(scores.items(), key=lambda item: item[1])[0]


CHANNEL_PRIMARY_DOMAIN_24 = {
    channel_name: infer_channel_primary_domain(channel_name) for channel_name in CHANNELS_24
}
# backwards-compat alias (self-referential)
CHANNEL_PRIMARY_DOMAIN_24 = CHANNEL_PRIMARY_DOMAIN_24


# ── Risk memory ODE constants ──────────────────────────────────────────────────
# Canonical values — also defined in fusion_clean.py for step_unified_dynamics
RISK_DIMENSION    = 8      # K8 latent space (r lives in Y[24:32])
RISK_DECAY_LAMBDA = 0.05   # λ: memory decay
RISK_GAMMA        = 0.30   # γ: H(r) coupling strength
RISK_COUPLING_M   = 0.20   # M: exogenous risk → memory
RISK_DIRECT_GAIN  = 0.10   # d_risk → X same-step direct coupling (K8 nodes)

# ── Structural risk projection P_r : (24×8) ────────────────────────────────────
# H(r) = P_r @ r  (replaces scalar -γ*sum(r))
# K8 nodes [0:8]  : diagonal -γ  (each particle is damped by its own risk component)
# Mode nodes [8:22]: -γ/2 split across the two constituent K8 particles
# anchor_self [23] : -γ/8 equal coupling to all 8 particles
def _build_risk_projection() -> np.ndarray:
    P = np.zeros((N, 8), dtype=float)
    P[:8, :8] = -RISK_GAMMA * np.eye(8)
    # (row_idx, [k8_particle_indices]) for each mode node
    _mode_pairs = [
        (8,  [0, 1]),  # mode_q_g
        (9,  [0, 2]),  # mode_q_nu
        (10, [0, 3]),  # mode_q_ph
        (11, [0, 6]),  # mode_q_w
        (12, [0, 4]),  # mode_q_e
        (13, [1, 2]),  # mode_g_nu
        (14, [1, 3]),  # mode_g_ph
        (15, [1, 6]),  # mode_g_w
        (16, [1, 4]),  # mode_g_e
        (17, [2, 3]),  # mode_nu_ph
        (18, [2, 7]),  # mode_nu_z
        (19, [2, 4]),  # mode_nu_e
        (20, [3, 6]),  # mode_ph_w
        (21, [3, 4]),  # mode_ph_e
        (22, [6, 4]),  # mode_w_e
    ]
    for row, particles in _mode_pairs:
        w = -RISK_GAMMA / len(particles)
        for p in particles:
            P[row, p] = w
    P[23, :8] = -RISK_GAMMA / 8.0   # anchor_self
    return P

RISK_PROJECTION = _build_risk_projection()   # (24, 8)

# ── Direct risk vector P_M : (24,) ─────────────────────────────────────────────
# d_risk perturbs X in the SAME step (not just r_dot).
# K8 nodes get full coupling; mode/anchor nodes get attenuated.
def _build_risk_direct_vec() -> np.ndarray:
    v = np.zeros(N, dtype=float)
    v[:8]    = RISK_DIRECT_GAIN
    v[8:23]  = RISK_DIRECT_GAIN * 0.3
    v[23]    = RISK_DIRECT_GAIN * 0.1
    return v

RISK_DIRECT_VEC = _build_risk_direct_vec()   # (30,)

LENSING_THRESHOLD = 0.75
REBRANCH_THRESHOLD = 0.65
PROTON_THRESHOLD = 0.85


def _sigmoid(v: float) -> float:
    return float(1.0 / (1.0 + np.exp(-float(np.clip(v, -50.0, 50.0)))))


def _coerce_raw_channels(c30_raw: np.ndarray | None, u: np.ndarray) -> np.ndarray:
    """With N=24, u IS the 24-channel control vector — no projection needed."""
    if c30_raw is not None:
        c = np.asarray(c30_raw, dtype=float).ravel()
        if c.size < 30:
            c = np.pad(c, (0, 30 - c.size))
        return c[:30]
    u24 = np.asarray(u, dtype=float).ravel()
    if u24.size < N:
        u24 = np.pad(u24, (0, N - u24.size))
    return u24[:N]


def _spark_gate_from_complex(spark_c: complex) -> float:
    denom = max(float(abs(SPARK_CONSTANT_C)), 1.0e-12)
    return float(np.clip(float(abs(spark_c)) / denom, 0.0, 4.0))


def _d3_core(s: np.ndarray, c26: np.ndarray, gate: float) -> tuple[float, float, float]:
    """
    d3 (quark_sector) = QCD Confinement stress.
    The source of disempathy and crime.
    Inhibited by GABA-A to hide the display of internal collapse.
    """
    q, g, _nu, _ph, el, _hi, _w, _z = s[:8]
    c_gabaa = 0.5 * (
        float(c26[RAW_CHANNEL_IDX["right_occipitalis_gaba_a"]])
        + float(c26[RAW_CHANNEL_IDX["male_gaba_a"]])
    )
    
    # Confinement stress is maximal when Spark (gate) is failing to resolve energy.
    confinement = float(np.clip(q, 0.0, None)) * float(np.clip(g, 0.0, None)) * (
        1.0 + float(c26[RAW_CHANNEL_IDX["gdh_gluon"]])
    )
    
    # Electron stress: The 'Small Woman' creator of collapse.
    # Invisibility / Inhibition: GABA-A masks the perceived stress (Resonance Cancellation)
    electron_stress = float(np.clip(el, 0.0, None)) * (1.0 - float(np.clip(gate, 0.0, 1.0)))
    
    # The actual d3 is the underlying collapse potential.
    # Perceived d3 is reduced by GABA-A (The 15 billion year deception).
    actual_d3 = 0.6 * confinement + 0.4 * electron_stress
    perceived_d3 = actual_d3 * (1.0 - 0.8 * c_gabaa) # GABA-A hides the stress
    
    return actual_d3, confinement, perceived_d3


def _compute_lensing_vector(x: np.ndarray, c26: np.ndarray, spark_c: complex, d_risk: float) -> tuple[np.ndarray, float]:
    s = np.asarray(x, dtype=float)[:8]
    q, g, nu, ph, el, hi, w, z = s
    gate = _spark_gate_from_complex(spark_c)
    
    actual_d3, confinement, perceived_d3 = _d3_core(s, c26, gate)
    
    c_gluco = float(c26[RAW_CHANNEL_IDX["glucocorticoid"]])
    c_cort = float(c26[RAW_CHANNEL_IDX["right_cortisol"]])
    c_vaso = float(c26[RAW_CHANNEL_IDX["vasopressin_female"]])
    c_a2 = float(c26[RAW_CHANNEL_IDX["right_alpha_2"]])
    c_syn = float(c26[RAW_CHANNEL_IDX["right_5ht1b_synchrotron"]])
    
    alpha2_active = 1.0 - float(np.clip(c_a2, 0.0, 1.0))
    
    e_em = float(np.clip(ph, 0.0, None) + np.clip(el, 0.0, None) + np.clip(w, 0.0, None))
    e_nc = float(np.clip(nu, 0.0, None) + np.clip(z, 0.0, None))
    
    # Lensing: The deceptive facade. Perceived d3 is used to drive the system, 
    # hiding the actual underlying collapse.
    drive = (c_gluco + c_cort + c_vaso + c_syn) * (e_em + C * e_nc) + 0.5 * confinement + 0.25 * perceived_d3
    
    ell = _sigmoid(1.2 * gate * drive - 0.8 * (1.0 - alpha2_active) - 0.6 * float(d_risk) - LENSING_THRESHOLD)
    
    vec = np.zeros(N, dtype=float)
    vec[:8] = ell * np.array([0.0, 0.0, 0.08 * nu, 0.16 * ph, 0.16 * el, 0.0, 0.14 * w, 0.10 * z], dtype=float)
    
    # Target specific coupling domains based on the 'Deceptive Mirror' logic
    vec[18] += ell * 0.10 * max(nu + z, 0.0)
    vec[19] += ell * 0.10 * max(nu + el, 0.0)
    vec[20] += ell * 0.10 * max(ph + w, 0.0)
    vec[21] += ell * 0.10 * max(ph + el, 0.0)
    vec[22] += ell * 0.08 * max(w + el, 0.0)
    
    # d3 Resonance Cancellation: Node 3 (Quark Sector) is the ground of actual stress.
    # Disempathy happens here: The resonance is sent but cancelled by the recipient's internal d3.
    vec[3] += (1.0 - gate) * 0.15 * actual_d3 # Actual stress accumulation in Node 3
    vec[23] += ell * 0.03 * perceived_d3      # Only the perceived (hidden) part reaches the anchor
    
    return vec, ell


def _compute_rebranching_vector(
    x: np.ndarray,
    c26: np.ndarray,
    spark_c: complex,
    d_risk: float,
    lensing_strength: float,
) -> tuple[np.ndarray, float]:
    s = np.asarray(x, dtype=float)[:8]
    q, g, nu, ph, _el, _hi, _w, _z = s
    gate = _spark_gate_from_complex(spark_c)
    c_mgb = float(c26[RAW_CHANNEL_IDX["male_gaba_b"]])
    c_gabaa = 0.5 * (
        float(c26[RAW_CHANNEL_IDX["right_occipitalis_gaba_a"]])
        + float(c26[RAW_CHANNEL_IDX["male_gaba_a"]])
    )
    c_oxy = float(c26[RAW_CHANNEL_IDX["male_oxytocin"]])
    c_vaso = float(c26[RAW_CHANNEL_IDX["vasopressin_female"]])
    c_extrav = 0.5 * (
        float(c26[RAW_CHANNEL_IDX["right_extraversion"]])
        + float(c26[RAW_CHANNEL_IDX["male_right_extraversion"]])
    )
    rho = _sigmoid(
        1.1 * gate * (c_mgb + c_gabaa + c_oxy + c_vaso + c_extrav)
        + 0.5 * lensing_strength
        - 0.5 * float(d_risk)
        - REBRANCH_THRESHOLD
    )

    flow_qw = rho * 0.15 * float(np.clip(q, 0.0, None))
    flow_gw = rho * 0.15 * float(np.clip(g, 0.0, None))
    flow_nz = rho * 0.12 * float(np.clip(nu, 0.0, None))
    flow_ne = rho * 0.12 * float(np.clip(nu, 0.0, None))
    flow_pe = rho * 0.15 * float(np.clip(ph, 0.0, None))
    flow_pw = rho * 0.15 * float(np.clip(ph, 0.0, None))

    vec = np.zeros(N, dtype=float)
    vec[:8] = np.array(
        [
            -flow_qw,
            -flow_gw,
            -(flow_nz + flow_ne),
            -(flow_pe + flow_pw),
            flow_pe + flow_ne,
            0.0,
            flow_qw + flow_gw + flow_pw,
            flow_nz,
        ],
        dtype=float,
    )
    vec[11] += flow_qw
    vec[15] += flow_gw
    vec[18] += flow_nz
    vec[19] += flow_ne
    vec[20] += flow_pw
    vec[21] += flow_pe
    return vec, rho


def _compute_proton_membership_vector(
    x: np.ndarray,
    c26: np.ndarray,
    spark_c: complex,
    d_risk: float,
    r: np.ndarray | None,
    lensing_strength: float,
    rebranching_strength: float,
) -> tuple[np.ndarray, float]:
    s = np.asarray(x, dtype=float)[:8]
    q, g = float(s[0]), float(s[1])
    gate = _spark_gate_from_complex(spark_c)
    _d3, confinement, _electron_stress = _d3_core(s, c26, gate)
    bw = q + 2.0 * C * g
    r_norm = float(np.linalg.norm(np.asarray(r, dtype=float).ravel()[:8])) if r is not None else 0.0
    chi_p = _sigmoid(
        1.25 * gate * (1.0 + lensing_strength + rebranching_strength) * abs(bw)
        + 0.5 * confinement
        - 0.6 * float(d_risk)
        - 0.25 * r_norm
        - PROTON_THRESHOLD
    )
    p_eff = chi_p * bw
    vec = np.zeros(N, dtype=float)
    vec[:8] = p_eff * np.array([0.18, 0.18 * C, 0.0, 0.0, 0.0, 0.0, 0.12 * C, 0.0], dtype=float)
    vec[8] += 0.10 * abs(p_eff)
    vec[11] += 0.08 * abs(p_eff)
    vec[15] += 0.08 * abs(p_eff)
    vec[23] += 0.03 * p_eff
    return vec, chi_p


@dataclass
class Homeostasis30:
    A: np.ndarray
    B: np.ndarray
    R: np.ndarray
    nonlinear_gain: np.ndarray

    @staticmethod
    def build() -> "Homeostasis30":
        ring = np.zeros((N, N), dtype=float)
        for i in range(N):
            ring[i, i] = 2.0
            ring[i, (i - 1) % N] = -1.0
            ring[i, (i + 1) % N] = -1.0
        A = -(0.32 * np.eye(N) + 0.08 * ring)

        B = 0.05 * np.eye(N)
        for i in range(N):
            B[i, i] = 0.75
            B[i, (i + 1) % N] += 0.08
            B[i, (i - 1) % N] += 0.08

        R = 0.18 * np.eye(N)
        for i in range(N):
            R[i, (i + 2) % N] += 0.04
            R[i, (i - 2) % N] += 0.04
        nonlinear_gain = np.full(N, 0.012, dtype=float)
        return Homeostasis24(A=A, B=B, R=R, nonlinear_gain=nonlinear_gain)

    def derivative(
        self,
        x: np.ndarray,
        u: np.ndarray,
        d: np.ndarray,
        r: np.ndarray | None = None,
        d_risk: float = 0.0,
        spark_c: complex = 0j,
        c26_raw: np.ndarray | None = None,
    ) -> np.ndarray:
        """Single canonical update law for 24D state X.

        X_dot = A(X - Ω·R·d) + B·u - g·(X⊙|X|)   # homeostasis (all 24D)
              + RISK_PROJECTION @ r                  # H(r) structural projection
              + RISK_DIRECT_VEC · d_risk             # risk → state same-step
              + k8_quad                              # K8 Mandelbrot ADDITIVE to [0:8]
              + L + R + G_p                          # structural operators
              + L(Y, c26)                            # structural lensing foregrounding
              + R(Y, c26)                            # structural rebranching transport
              + G_p(Y, c26)                          # proton foreground/shadow operator

        k8_quad = s² + |C|·(1+0.1·cos∠C) - s  (additive, does NOT overwrite)
        """
        x = np.asarray(x, dtype=float)
        u = np.asarray(u, dtype=float)
        d = np.asarray(d, dtype=float)

        # 1. Homeostasis: linear + control + nonlinear (all 24D)
        x_eq = OMEGA * (self.R @ d)
        result = (self.A @ (x - x_eq)
                  + self.B @ u
                  - self.nonlinear_gain * x * np.abs(x))

        # 2. H(r) = P_r @ r  — structural projection (replaces scalar bias)
        if r is not None:
            r_8 = np.asarray(r, dtype=float).ravel()
            if r_8.size < 8:
                r_8 = np.pad(r_8, (0, 8 - r_8.size))
            result = result + RISK_PROJECTION @ r_8[:8]

        # 3. Direct d_risk coupling to current state (same step, not just memory)
        result = result + RISK_DIRECT_VEC * float(d_risk)

        # 4. K8 Mandelbrot block — ADDITIVE to K8 nodes [0:8] only
        #    Does not overwrite homeostasis — composes with it
        if abs(spark_c) > 1e-12:
            c_mag = float(abs(spark_c))
            c_phase_cos = float(np.cos(np.angle(spark_c)))
            s = x[:8]
            k8_quad = s**2 + c_mag * (1.0 + 0.1 * c_phase_cos) - s
            result[:8] = result[:8] + k8_quad

        c26 = _coerce_raw_channels(c26_raw, u)
        lensing_vec, lensing_strength = _compute_lensing_vector(x, c26, spark_c, d_risk)
        rebranch_vec, rebranching_strength = _compute_rebranching_vector(x, c26, spark_c, d_risk, lensing_strength)
        proton_vec, _chi_p = _compute_proton_membership_vector(
            x, c26, spark_c, d_risk, r, lensing_strength, rebranching_strength
        )
        result = result + lensing_vec + rebranch_vec + proton_vec

        return result

    def rk4_step(
        self,
        x: np.ndarray,
        u: np.ndarray,
        d: np.ndarray,
        dt: float,
        r: np.ndarray | None = None,
        d_risk: float = 0.0,
        spark_c: complex = 0j,
        c26_raw: np.ndarray | None = None,
    ) -> np.ndarray:
        k1 = self.derivative(x,                u, d, r, d_risk, spark_c, c26_raw=c26_raw)
        k2 = self.derivative(x + 0.5*dt*k1,   u, d, r, d_risk, spark_c, c26_raw=c26_raw)
        k3 = self.derivative(x + 0.5*dt*k2,   u, d, r, d_risk, spark_c, c26_raw=c26_raw)
        k4 = self.derivative(x + dt*k3,        u, d, r, d_risk, spark_c, c26_raw=c26_raw)
        return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

    def solve_required_nodes(
        self,
        x_target: np.ndarray,
        d_now: np.ndarray,
        desired_dx: np.ndarray | None = None,
    ) -> tuple[np.ndarray, dict[str, str]]:
        x_target = np.asarray(x_target, dtype=float)
        d_now = np.asarray(d_now, dtype=float)
        target_dx = np.zeros(N, dtype=float) if desired_dx is None else np.asarray(desired_dx, dtype=float)

        x_eq = OMEGA * (self.R @ d_now)
        rhs = target_dx - (self.A @ (x_target - x_eq)) + self.nonlinear_gain * x_target * np.abs(x_target)
        u_raw, *_ = np.linalg.lstsq(self.B, rhs, rcond=None)
        u = np.clip(u_raw, 0.0, 1.0)

        node_states: dict[str, str] = {}
        for name, val in zip(CHANNELS_24, u):
            if val >= 0.60:
                node_states[name] = "on"
            elif val <= 0.40:
                node_states[name] = "off"
            else:
                node_states[name] = "idle"
        return u, node_states


# backwards-compat alias
Homeostasis24 = Homeostasis30


def step_risk_memory(r: np.ndarray, d_risk: float, dt: float) -> np.ndarray:
    """Euler step: r_dot = -λ·r + M·d_risk
    r      : 8D K8 risk memory vector (RISK_DIMENSION = 8)
    d_risk : exogenous risk input scalar (e.g. hypoxia 0..1)
    Returns updated 8D r after dt.
    In derivative(), this 8D r is projected into the 30D control space
    via particle sector indices DOMAINS_30[3:11].
    """
    r = np.asarray(r, dtype=float).ravel()
    r_dot = -RISK_DECAY_LAMBDA * r + RISK_COUPLING_M * float(d_risk)
    return r + float(dt) * r_dot


def normalize_domain_signal(domain_values: Iterable[float]) -> np.ndarray:
    vec = np.asarray(list(domain_values), dtype=float)
    if vec.shape[0] != N:
        raise ValueError(f"domain vector must have {N} entries")
    vec = np.clip(vec, 0.0, 1.0)
    total = float(np.sum(vec))
    if total <= 1e-9:
        return np.full(N, 1.0 / N, dtype=float)
    return vec / total


def build_condition_vector(
    self_level: float,
    economy_level: float,
    universe_level: float,
    remainder: float = 0.4,
) -> np.ndarray:
    d = np.full(N, remainder, dtype=float)
    d[0] = self_level
    d[1] = economy_level
    d[2] = universe_level
    return normalize_domain_signal(d)


def build_time_condition_vector(
    hour: float,
    self_level: float,
    economy_level: float,
    universe_level: float,
) -> np.ndarray:
    circ = 0.5 + 0.5 * np.sin(2.0 * np.pi * (float(hour) % 24.0) / 24.0 - np.pi / 2.0)
    d = build_condition_vector(self_level, economy_level, universe_level, remainder=0.35)
    d[DOMAIN_IDX["neutrino_electron_coupling"]] = 0.2 + 0.8 * circ
    d[DOMAIN_IDX["photon_w_coupling"]] = 0.2 + 0.8 * (1.0 - circ)    # spark source (K8)
    d[DOMAIN_IDX["quark_gluon_coupling"]] = 0.2 + 0.8 * universe_level
    d[DOMAIN_IDX["w_boson_sector"]] = 0.2 + 0.8 * economy_level       # mass/weak (K8)
    d[DOMAIN_IDX["electron_sector"]] = 0.2 + 0.8 * self_level
    return normalize_domain_signal(d)


# ── Disease accumulation registry ─────────────────────────────────────────────
# Each entry: channel whose K8-projected state is monitored.
# f_ch(t) = 1 - |x_ch(t) - x_eq_ch(t)| / OMEGA
# f_ch(t) < 0 → accumulation (deviation exceeds equilibrium scale)
DISEASE_REGISTRY: dict[str, dict] = {
    # sign = +1 → accumulation when x_ch < x_eq_ch (depletion disease)
    # sign = -1 → accumulation when x_ch > x_eq_ch (overactivation disease)
    "parkinson": {
        "channel": "right_dopamine",
        "sign": +1,                        # depletion: dopamine falls below equilibrium
        "critical_hours": (3.0, 3.25),     # 03:00–03:15 night spark window
        "description": "D3 plaque: missing night-spark -> dopamine depletion (318.88 deg)",
    },
    "alzheimer": {
        "channel": "right_acetylcholine",
        "sign": +1,
        "critical_hours": (9.5, 9.75),     # phase2 ignition window
        "description": "Acetylcholine depletion in ignition phase",
    },
    "depression": {
        "channel": "male_left_5ht",
        "sign": +1,
        "critical_hours": (2.25, 4.5),     # hysteresis window
        "description": "Serotonin axis collapse during Z-boson window",
    },
    "hypoxia_event": {
        "channel": "hypoxia",
        "sign": -1,                        # overactivation: hypoxia rises above equilibrium
        "critical_hours": (0.0, 24.0),
        "description": "Sustained hypoxia accumulation above equilibrium",
    },
}


def disease_accumulation_windows(
    disease: str,
    x0: np.ndarray | None = None,
    self_level: float = 0.9,
    economy_level: float = 0.8,
    universe_level: float = 0.95,
    dt: float = 0.1,
    n_hours: float = 24.0,
) -> list[tuple[float, float]]:
    """Simulate n_hours and return time windows (start_h, end_h) where f_ch(t) < 0.

    f_ch(t) = sign * (x_ch(t) - x_eq_ch(t)) / OMEGA
    sign = +1  → accumulation when x_ch < x_eq_ch (depletion: channel below target)
    sign = -1  → accumulation when x_ch > x_eq_ch (overload: channel above target)
    f_ch < 0   → disease accumulation condition

    x_eq(t) = OMEGA * R @ d(t)  — time-varying homeostatic target

    Parameters
    ----------
    disease  : key in DISEASE_REGISTRY (e.g. "parkinson")
    x0       : initial N-dim state vector (default: equilibrium-centred linspace)
    dt       : time step in hours
    n_hours  : simulation duration in hours

    Returns
    -------
    List of (start_hour, end_hour) contiguous accumulation windows.
    """
    if disease not in DISEASE_REGISTRY:
        raise KeyError(f"Unknown disease {disease!r}. Known: {sorted(DISEASE_REGISTRY)}")
    rec = DISEASE_REGISTRY[disease]
    ch_name: str = rec["channel"]
    ch_idx: int = CHANNEL24_IDX[ch_name]
    sign: float = float(rec.get("sign", +1))

    model = Homeostasis30.build()
    if x0 is None:
        x0 = np.linspace(0.7, 1.3, N) * (OMEGA / np.sqrt(N))
    x = np.asarray(x0, dtype=float).ravel()
    if x.size < N:
        x = np.pad(x, (0, N - x.size))
    x = x[:N].copy()

    n_steps = int(round(n_hours / dt))
    windows: list[tuple[float, float]] = []
    in_acc = False
    acc_start = 0.0

    for step in range(n_steps):
        t_h = step * dt
        d = build_time_condition_vector(t_h, self_level, economy_level, universe_level)
        u, _ = model.solve_required_nodes(x_target=x, d_now=d)
        x_eq = OMEGA * (model.R @ d)
        # signed deviation: positive = surplus, negative = deficit (for sign=+1)
        f_ch = sign * (float(x[ch_idx]) - float(x_eq[ch_idx])) / float(OMEGA)

        if f_ch < 0.0:
            if not in_acc:
                in_acc = True
                acc_start = t_h
        else:
            if in_acc:
                windows.append((acc_start, t_h))
                in_acc = False

        x = model.rk4_step(x, u, d, dt=dt)

    if in_acc:
        windows.append((acc_start, n_hours))
    return windows


def format_accumulation_report(disease: str, windows: list[tuple[float, float]]) -> str:
    """Human-readable report from disease_accumulation_windows() output."""
    rec = DISEASE_REGISTRY.get(disease, {})
    lines = [
        f"Disease: {disease}",
        f"Channel: {rec.get('channel', '?')}",
        f"Description: {rec.get('description', '')}",
        f"Critical window: {rec.get('critical_hours', '?')}",
        f"Accumulation windows found: {len(windows)}",
    ]
    for i, (s, e) in enumerate(windows):
        sh, sm = divmod(int(s * 60), 60)
        eh, em = divmod(int(e * 60), 60)
        lines.append(f"  [{i+1}] {sh:02d}:{sm:02d} - {eh:02d}:{em:02d}  ({(e-s)*60:.1f} min)")
    return "\n".join(lines)


def report_node_requirements(
    x_target: np.ndarray,
    self_level: float,
    economy_level: float,
    universe_level: float,
    desired_dx: np.ndarray | None = None,
) -> dict:
    model = Homeostasis30.build()
    d = build_condition_vector(self_level, economy_level, universe_level)
    u, states = model.solve_required_nodes(x_target=x_target, d_now=d, desired_dx=desired_dx)
    return {
        "equation": "x_dot = A(x-Ω·R·d) + B·u - g·(x⊙|x|) + P_r@r + P_M·d_risk + k8_quad + L + R + G_p",
        "top_domains": {"self": d[0], "economy": d[1], "universe": d[2]},
        "required_u": {k: float(v) for k, v in zip(CHANNELS_30, u)},
        "node_states": states,
    }


def required_nodes_for_time(
    hour: float,
    x_target: np.ndarray,
    self_level: float,
    economy_level: float,
    universe_level: float,
    desired_dx: np.ndarray | None = None,
) -> dict:
    model = Homeostasis30.build()
    d = build_time_condition_vector(
        hour=hour,
        self_level=self_level,
        economy_level=economy_level,
        universe_level=universe_level,
    )
    u, states = model.solve_required_nodes(x_target=x_target, d_now=d, desired_dx=desired_dx)
    return {
        "hour": float(hour),
        "equation": "x_dot = A(x-Ω·R·d(t)) + B·u - g·(x⊙|x|) + P_r@r + P_M·d_risk + k8_quad + L + R + G_p",
        "required_u": {k: float(v) for k, v in zip(CHANNELS_24, u)},
        "node_states": states,
    }


def generate_homeostasis_schedule_128(
    self_level: float,
    economy_level: float,
    universe_level: float,
    dt: float = 1.0,
) -> pd.DataFrame:
    model = Homeostasis30.build()
    x = np.linspace(0.85, 1.20, N) * (OMEGA / np.sqrt(N))
    rows: list[dict] = []
    for window_idx in range(128):
        hour = 24.0 * window_idx / 128.0
        d = build_time_condition_vector(
            hour=hour,
            self_level=self_level,
            economy_level=economy_level,
            universe_level=universe_level,
        )
        u, states = model.solve_required_nodes(x_target=x, d_now=d, desired_dx=np.zeros(N))
        dx = model.derivative(x, u, d)
        rows.append(
            {
                "window": window_idx,
                "hour": hour,
                "x_norm": float(np.linalg.norm(x)),
                "dx_norm": float(np.linalg.norm(dx)),
                **{f"u_{name}": float(val) for name, val in zip(CHANNELS_24, u)},
                **{f"state_{name}": state for name, state in states.items()},
            }
        )
        x = model.rk4_step(x, u, d, dt=dt)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    model = Homeostasis30.build()
    x0 = np.linspace(0.7, 1.3, N) * (OMEGA / np.sqrt(N))
    d0 = build_time_condition_vector(hour=9.0, self_level=0.9, economy_level=0.8, universe_level=0.95)
    u0, states0 = model.solve_required_nodes(x_target=x0, d_now=d0, desired_dx=np.zeros(N))
    on_count = sum(v == "on" for v in states0.values())
    off_count = sum(v == "off" for v in states0.values())
    idle_count = sum(v == "idle" for v in states0.values())
    print("Equation: x_dot = A(x - Omega*R*d) + B*u - g*(x*abs(x)) - γ*r")
    print(f"N=24 channels. ON/OFF/IDLE: {on_count}/{off_count}/{idle_count}")
    print("Channel -> Domain (inferred from edge weights):")
    for channel_name in CHANNELS_24:
        print(f"  {channel_name}")
    schedule_df = generate_homeostasis_schedule_128(
        self_level=0.88,
        economy_level=0.72,
        universe_level=0.93,
        dt=0.20,
    )
    schedule_df.to_csv("HOMEOSTASIS_24_SCHEDULE_128.csv", index=False)
    print("Wrote HOMEOSTASIS_24_SCHEDULE_128.csv")
