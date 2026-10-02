import numpy as np
from math import cos, pi

OMEGA = 7.4
SPARK_ANGLE_RAD = 138.88 * (pi / 180.0)
SPARK_PHASE_LEAK = 1.0 / 128.0

# 24 channels -> (quark_push, gluon_push, coupling_push)
CHANNEL_QG_BASE = {
    "gdh_gluon": (0.22, 0.32, 0.16),
    "female_gaba_b_latdorsi": (-0.08, -0.08, -0.18),
    "left_acetyl_coa": (0.16, 0.10, 0.08),
    "male_left_5ht": (0.02, 0.06, 0.03),
    "female_left_noradrenaline": (0.14, 0.08, 0.05),
    "left_temporalis_5ht1a": (-0.04, 0.04, -0.03),
    "left_estrogen": (0.08, 0.04, 0.03),
    "right_love": (0.03, 0.05, 0.02),
    "hypoxia": (0.10, 0.06, 0.04),
    "right_dopamine": (0.26, 0.18, 0.09),
    "vasopressin_female": (0.18, 0.22, 0.20),
    "male_oxytocin": (0.04, 0.06, 0.03),
    "muscle_a": (0.16, 0.12, 0.07),
    "muscle_b": (0.18, 0.10, 0.07),
    "right_5ht1b_synchrotron": (0.08, 0.06, 0.03),
    "right_androgen": (0.10, 0.08, 0.04),
    "left_endorphin": (0.02, 0.03, -0.02),
    "left_frontalis_d2": (0.14, 0.10, 0.06),
    "right_occipitalis_gaba_a": (-0.06, -0.04, -0.10),
    "right_acetylcholine": (0.12, 0.10, 0.05),
    "left_extraversion": (0.08, 0.05, 0.03),
    "glucocorticoid": (0.10, 0.08, 0.04),
    "right_cortisol": (0.14, 0.10, 0.05),
    "right_alpha_2": (0.00, 0.00, 0.00),  # special gate
}


def _state_factor(state: str) -> float:
    if state == "on":
        return 1.0
    if state == "off":
        return -0.5
    return 0.0


def consciousness_window(window_idx: int) -> float:
    window_idx = int(window_idx) % 128
    return 0.5 + 0.5 * np.sin(window_idx * np.pi / 64.0)


def extract_controls(channels: dict[str, str]) -> dict[str, float]:
    values = {"q_push": 0.0, "g_push": 0.0, "coupling_push": 0.0}
    for name, (q_d, g_d, c_d) in CHANNEL_QG_BASE.items():
        factor = _state_factor(channels.get(name, "no_control"))
        values["q_push"] += q_d * factor
        values["g_push"] += g_d * factor
        values["coupling_push"] += c_d * factor

    alpha2_state = channels.get("right_alpha_2", "on")
    if alpha2_state == "off":
        values["coupling_push"] += 0.26
    elif alpha2_state == "on":
        values["coupling_push"] -= 0.16

    values["vasopressin_on"] = 1.0 if channels.get("vasopressin_female") == "on" else 0.0
    values["dopamine_on"] = 1.0 if channels.get("right_dopamine") == "on" else 0.0
    values["cortisol_on"] = 1.0 if channels.get("right_cortisol") == "on" else 0.0
    values["gaba_b_on"] = 1.0 if channels.get("female_gaba_b_latdorsi") == "on" else 0.0
    values["alpha2_off"] = 1.0 if alpha2_state == "off" else 0.0
    return values


def spark_scalar(channels: dict[str, str], z_atomic: float, window_idx: int) -> float:
    ctrl = extract_controls(channels)
    spark_drive = (
        1.10 * ctrl["dopamine_on"]
        + 0.85 * ctrl["cortisol_on"]
        + 0.75 * ctrl["alpha2_off"]
        + 0.55 * ctrl["vasopressin_on"]
        - 0.90 * ctrl["gaba_b_on"]
    )
    spark_prob = 1.0 / (1.0 + np.exp(-spark_drive))
    phase = cos(float(z_atomic) * SPARK_ANGLE_RAD + SPARK_PHASE_LEAK)
    return float(spark_prob * phase * consciousness_window(window_idx))


def qg_dynamics(
    x: np.ndarray,
    channels: dict[str, str],
    z_atomic: float,
    window_idx: int,
    k_anchor: float = 0.44,
    eps: float = 1e-6,
) -> np.ndarray:
    quark, gluon = float(x[0]), float(x[1])
    ctrl = extract_controls(channels)
    spark = spark_scalar(channels, z_atomic, window_idx)

    base_damp = 0.42
    coupling = np.clip(0.32 + ctrl["coupling_push"], 0.05, 1.40)
    q_push = ctrl["q_push"] + 0.9 * spark
    g_push = ctrl["g_push"] + 1.0 * spark

    dq = -base_damp * quark + coupling * gluon + q_push
    dg = -base_damp * gluon + coupling * quark + g_push
    dx = np.array([dq, dg], dtype=float)

    norm_x = np.linalg.norm(x)
    anchor = -k_anchor * (norm_x - OMEGA) ** 2 * (x / (norm_x + eps))
    return dx + anchor


def integrate_window(
    x: np.ndarray,
    channels: dict[str, str],
    z_atomic: float,
    window_idx: int,
    substeps: int = 24,
    dt: float = 0.02,
) -> np.ndarray:
    state = np.array(x, dtype=float)
    for _ in range(substeps):
        dx = qg_dynamics(state, channels, z_atomic, window_idx)
        dx_norm = np.linalg.norm(dx)
        if dx_norm > 2.2:
            dx = dx * (2.2 / (dx_norm + 1e-9))
        state = state + dt * dx
        norm_state = np.linalg.norm(state)
        if norm_state > 1e-9:
            target = OMEGA * (state / norm_state)
            lock = 0.11 + 0.18 * np.tanh(max(abs(norm_state - OMEGA) - 0.10, 0.0))
            state = (1.0 - lock) * state + lock * target
        state = np.clip(state, -24.0, 24.0)
    return state


def qg_potential(x: np.ndarray, channels: dict[str, str], z_atomic: float, window_idx: int) -> float:
    quark, gluon = float(x[0]), float(x[1])
    ctrl = extract_controls(channels)
    spark = spark_scalar(channels, z_atomic, window_idx)
    coupling = np.clip(0.32 + ctrl["coupling_push"], 0.05, 1.40)
    damp = 0.42
    norm_x = np.linalg.norm(x)
    anchor = -0.44 * (norm_x - OMEGA) ** 2
    interaction = coupling * quark * gluon
    forcing = ctrl["q_push"] * quark + ctrl["g_push"] * gluon
    spark_term = spark * (1.0 * quark + 1.0 * gluon + 1.0)
    dissipation = 0.5 * damp * (quark * quark + gluon * gluon)
    return float(interaction + forcing + spark_term - dissipation + anchor)

