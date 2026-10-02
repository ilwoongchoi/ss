import numpy as np
from math import cos, pi

OMEGA = 7.4
SPARK_ANGLE_RAD = 138.88 * (pi / 180.0)
SPARK_PHASE_LEAK = 1.0 / 128.0

# 24 channels -> (proton_push, quark_push, nu_push, pq_push, pn_push, qn_push)
CHANNEL_PQN_BASE = {
    "gdh_gluon": (0.00, 0.24, 0.00, 0.04, 0.00, 0.06),
    "female_gaba_b_latdorsi": (-0.08, -0.04, -0.10, -0.05, -0.10, -0.08),
    "left_acetyl_coa": (0.12, 0.10, 0.02, 0.05, 0.03, 0.03),
    "male_left_5ht": (0.02, 0.00, 0.10, 0.01, 0.03, 0.03),
    "female_left_noradrenaline": (0.12, 0.06, 0.00, 0.04, 0.02, 0.02),
    "left_temporalis_5ht1a": (-0.02, 0.00, 0.08, -0.01, 0.02, 0.03),
    "left_estrogen": (0.10, 0.04, 0.00, 0.03, 0.01, 0.01),
    "right_love": (0.04, 0.00, 0.06, 0.01, 0.03, 0.02),
    "hypoxia": (0.10, 0.04, 0.00, 0.03, 0.01, 0.02),
    "right_dopamine": (0.22, 0.10, 0.02, 0.08, 0.04, 0.04),
    "vasopressin_female": (0.30, 0.08, 0.42, 0.06, 0.20, 0.10),
    "male_oxytocin": (0.05, 0.02, 0.10, 0.02, 0.04, 0.03),
    "muscle_a": (0.14, 0.08, 0.00, 0.05, 0.02, 0.03),
    "muscle_b": (0.16, 0.12, 0.00, 0.05, 0.02, 0.03),
    "right_5ht1b_synchrotron": (0.08, 0.04, 0.00, 0.03, 0.01, 0.01),
    "right_androgen": (0.10, 0.06, 0.00, 0.03, 0.01, 0.01),
    "left_endorphin": (0.04, 0.02, 0.00, -0.01, 0.00, 0.00),
    "left_frontalis_d2": (0.12, 0.08, 0.02, 0.04, 0.02, 0.03),
    "right_occipitalis_gaba_a": (-0.06, -0.02, 0.06, -0.03, -0.05, -0.04),
    "right_acetylcholine": (0.12, 0.06, 0.00, 0.04, 0.02, 0.02),
    "left_extraversion": (0.08, 0.04, 0.00, 0.03, 0.01, 0.01),
    "glucocorticoid": (0.10, 0.04, 0.00, 0.03, 0.02, 0.01),
    "right_cortisol": (0.14, 0.06, 0.00, 0.04, 0.03, 0.02),
    "right_alpha_2": (0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
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
    values = {
        "p_push": 0.0,
        "q_push": 0.0,
        "nu_push": 0.0,
        "pq_push": 0.0,
        "pn_push": 0.0,
        "qn_push": 0.0,
    }
    for name, deltas in CHANNEL_PQN_BASE.items():
        factor = _state_factor(channels.get(name, "no_control"))
        values["p_push"] += deltas[0] * factor
        values["q_push"] += deltas[1] * factor
        values["nu_push"] += deltas[2] * factor
        values["pq_push"] += deltas[3] * factor
        values["pn_push"] += deltas[4] * factor
        values["qn_push"] += deltas[5] * factor

    alpha2_state = channels.get("right_alpha_2", "on")
    if alpha2_state == "off":
        values["pn_push"] += 0.24
        values["qn_push"] += 0.14
        values["nu_push"] += 0.10
    elif alpha2_state == "on":
        values["pn_push"] -= 0.15
        values["qn_push"] -= 0.10
        values["nu_push"] -= 0.06

    values["vasopressin_on"] = 1.0 if channels.get("vasopressin_female") == "on" else 0.0
    values["dopamine_on"] = 1.0 if channels.get("right_dopamine") == "on" else 0.0
    values["cortisol_on"] = 1.0 if channels.get("right_cortisol") == "on" else 0.0
    values["gaba_b_on"] = 1.0 if channels.get("female_gaba_b_latdorsi") == "on" else 0.0
    values["alpha2_off"] = 1.0 if alpha2_state == "off" else 0.0
    return values


def spark_scalar(channels: dict[str, str], z_atomic: float, window_idx: int) -> float:
    ctrl = extract_controls(channels)
    spark_drive = (
        1.45 * ctrl["vasopressin_on"]
        + 0.90 * ctrl["alpha2_off"]
        + 0.75 * ctrl["cortisol_on"]
        + 0.55 * ctrl["dopamine_on"]
        - 0.90 * ctrl["gaba_b_on"]
    )
    spark_prob = 1.0 / (1.0 + np.exp(-spark_drive))
    phase = cos(float(z_atomic) * SPARK_ANGLE_RAD + SPARK_PHASE_LEAK)
    return float(spark_prob * phase * consciousness_window(window_idx))


def pqn_dynamics(
    x: np.ndarray,
    channels: dict[str, str],
    z_atomic: float,
    window_idx: int,
    k_anchor: float = 0.45,
    eps: float = 1e-6,
) -> np.ndarray:
    proton, quark, nu = float(x[0]), float(x[1]), float(x[2])
    ctrl = extract_controls(channels)
    spark = spark_scalar(channels, z_atomic, window_idx)

    damp = 0.40
    pq = np.clip(0.24 + ctrl["pq_push"], 0.02, 1.20)
    pn = np.clip(0.28 + ctrl["pn_push"], 0.02, 1.30)
    qn = np.clip(0.22 + ctrl["qn_push"], 0.02, 1.20)

    dp = -damp * proton + pq * quark + pn * nu + ctrl["p_push"] + 1.05 * spark
    dq = -damp * quark + pq * proton + qn * nu + ctrl["q_push"] + 0.85 * spark
    dnu = -damp * nu + pn * proton + qn * quark + ctrl["nu_push"] + 1.20 * spark
    dx = np.array([dp, dq, dnu], dtype=float)

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
        dx = pqn_dynamics(state, channels, z_atomic, window_idx)
        dx_norm = np.linalg.norm(dx)
        if dx_norm > 2.4:
            dx = dx * (2.4 / (dx_norm + 1e-9))
        state = state + dt * dx
        norm_state = np.linalg.norm(state)
        if norm_state > 1e-9:
            target = OMEGA * (state / norm_state)
            lock = 0.11 + 0.18 * np.tanh(max(abs(norm_state - OMEGA) - 0.10, 0.0))
            state = (1.0 - lock) * state + lock * target
        state = np.clip(state, -24.0, 24.0)
    return state


def pqn_potential(x: np.ndarray, channels: dict[str, str], z_atomic: float, window_idx: int) -> float:
    p, q, nu = float(x[0]), float(x[1]), float(x[2])
    ctrl = extract_controls(channels)
    spark = spark_scalar(channels, z_atomic, window_idx)

    pq = np.clip(0.24 + ctrl["pq_push"], 0.02, 1.20)
    pn = np.clip(0.28 + ctrl["pn_push"], 0.02, 1.30)
    qn = np.clip(0.22 + ctrl["qn_push"], 0.02, 1.20)
    damp = 0.40

    norm_x = np.linalg.norm(x)
    anchor = -0.45 * (norm_x - OMEGA) ** 2
    interaction = pq * p * q + pn * p * nu + qn * q * nu
    forcing = ctrl["p_push"] * p + ctrl["q_push"] * q + ctrl["nu_push"] * nu
    spark_term = spark * (1.05 * p + 0.85 * q + 1.20 * nu + 1.0)
    dissipation = 0.5 * damp * (p * p + q * q + nu * nu)
    return float(interaction + forcing + spark_term - dissipation + anchor)

