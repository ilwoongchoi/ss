import numpy as np
from math import cos, pi

OMEGA = 7.4
SPARK_ANGLE_RAD = 138.88 * (pi / 180.0)
SPARK_PHASE_LEAK = 1.0 / 128.0

# 24 channels -> (g_push, e_push, nu_push, ge_push, gn_push, en_push)
CHANNEL_GEN_BASE = {
    "gdh_gluon": (0.28, 0.00, 0.00, 0.08, 0.10, 0.00),
    "female_gaba_b_latdorsi": (-0.04, -0.10, -0.10, -0.04, -0.08, -0.08),
    "left_acetyl_coa": (0.14, 0.04, 0.02, 0.05, 0.04, 0.02),
    "male_left_5ht": (0.00, 0.02, 0.10, 0.00, 0.03, 0.04),
    "female_left_noradrenaline": (0.10, 0.04, 0.00, 0.04, 0.02, 0.02),
    "left_temporalis_5ht1a": (-0.02, 0.04, 0.08, -0.02, -0.02, 0.03),
    "left_estrogen": (0.06, 0.08, 0.00, 0.03, 0.01, 0.03),
    "right_love": (0.00, 0.06, 0.06, 0.02, 0.02, 0.04),
    "hypoxia": (0.08, 0.02, 0.00, 0.03, 0.02, 0.01),
    "right_dopamine": (0.16, 0.12, 0.02, 0.08, 0.04, 0.04),
    "vasopressin_female": (0.10, 0.08, 0.42, 0.05, 0.18, 0.16),
    "male_oxytocin": (0.02, 0.06, 0.10, 0.02, 0.03, 0.05),
    "muscle_a": (0.12, 0.00, 0.00, 0.04, 0.05, 0.00),
    "muscle_b": (0.10, 0.00, 0.00, 0.04, 0.03, 0.00),
    "right_5ht1b_synchrotron": (0.02, 0.10, 0.00, 0.03, 0.00, 0.03),
    "right_androgen": (0.04, 0.10, 0.00, 0.03, 0.00, 0.03),
    "left_endorphin": (0.02, 0.04, 0.00, -0.01, 0.00, 0.00),
    "left_frontalis_d2": (0.10, 0.06, 0.02, 0.04, 0.03, 0.02),
    "right_occipitalis_gaba_a": (-0.04, -0.04, 0.06, -0.04, -0.04, -0.06),
    "right_acetylcholine": (0.10, 0.06, 0.00, 0.04, 0.02, 0.02),
    "left_extraversion": (0.04, 0.08, 0.00, 0.03, 0.01, 0.03),
    "glucocorticoid": (0.08, 0.04, 0.00, 0.03, 0.02, 0.01),
    "right_cortisol": (0.12, 0.06, 0.00, 0.04, 0.03, 0.02),
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
        "g_push": 0.0,
        "e_push": 0.0,
        "nu_push": 0.0,
        "ge_push": 0.0,
        "gn_push": 0.0,
        "en_push": 0.0,
    }
    for name, deltas in CHANNEL_GEN_BASE.items():
        factor = _state_factor(channels.get(name, "no_control"))
        values["g_push"] += deltas[0] * factor
        values["e_push"] += deltas[1] * factor
        values["nu_push"] += deltas[2] * factor
        values["ge_push"] += deltas[3] * factor
        values["gn_push"] += deltas[4] * factor
        values["en_push"] += deltas[5] * factor

    alpha2_state = channels.get("right_alpha_2", "on")
    if alpha2_state == "off":
        values["gn_push"] += 0.22
        values["en_push"] += 0.20
        values["nu_push"] += 0.10
    elif alpha2_state == "on":
        values["gn_push"] -= 0.14
        values["en_push"] -= 0.12
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
        1.35 * ctrl["vasopressin_on"]
        + 0.90 * ctrl["alpha2_off"]
        + 0.70 * ctrl["cortisol_on"]
        + 0.55 * ctrl["dopamine_on"]
        - 0.90 * ctrl["gaba_b_on"]
    )
    spark_prob = 1.0 / (1.0 + np.exp(-spark_drive))
    phase = cos(float(z_atomic) * SPARK_ANGLE_RAD + SPARK_PHASE_LEAK)
    return float(spark_prob * phase * consciousness_window(window_idx))


def gen_dynamics(
    x: np.ndarray,
    channels: dict[str, str],
    z_atomic: float,
    window_idx: int,
    k_anchor: float = 0.44,
    eps: float = 1e-6,
) -> np.ndarray:
    gluon, electron, nu = float(x[0]), float(x[1]), float(x[2])
    ctrl = extract_controls(channels)
    spark = spark_scalar(channels, z_atomic, window_idx)

    damp = 0.40
    ge = np.clip(0.22 + ctrl["ge_push"], 0.02, 1.20)
    gn = np.clip(0.26 + ctrl["gn_push"], 0.02, 1.30)
    en = np.clip(0.24 + ctrl["en_push"], 0.02, 1.30)

    dg = -damp * gluon + ge * electron + gn * nu + ctrl["g_push"] + 0.80 * spark
    de = -damp * electron + ge * gluon + en * nu + ctrl["e_push"] + 0.90 * spark
    dnu = -damp * nu + gn * gluon + en * electron + ctrl["nu_push"] + 1.20 * spark
    dx = np.array([dg, de, dnu], dtype=float)

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
        dx = gen_dynamics(state, channels, z_atomic, window_idx)
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


def gen_potential(x: np.ndarray, channels: dict[str, str], z_atomic: float, window_idx: int) -> float:
    g, e, nu = float(x[0]), float(x[1]), float(x[2])
    ctrl = extract_controls(channels)
    spark = spark_scalar(channels, z_atomic, window_idx)

    ge = np.clip(0.22 + ctrl["ge_push"], 0.02, 1.20)
    gn = np.clip(0.26 + ctrl["gn_push"], 0.02, 1.30)
    en = np.clip(0.24 + ctrl["en_push"], 0.02, 1.30)
    damp = 0.40

    norm_x = np.linalg.norm(x)
    anchor = -0.44 * (norm_x - OMEGA) ** 2
    interaction = ge * g * e + gn * g * nu + en * e * nu
    forcing = ctrl["g_push"] * g + ctrl["e_push"] * e + ctrl["nu_push"] * nu
    spark_term = spark * (0.8 * g + 0.9 * e + 1.2 * nu + 1.0)
    dissipation = 0.5 * damp * (g * g + e * e + nu * nu)
    return float(interaction + forcing + spark_term - dissipation + anchor)

