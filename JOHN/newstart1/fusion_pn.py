import numpy as np
from math import cos, pi

C = np.sqrt(2.0) / 5.0
OMEGA = 7.4
SPARK_ANGLE_RAD = 138.88 * (pi / 180.0)
SPARK_PHASE_LEAK = 1.0 / 128.0

# 24 channels -> (proton_push, neutrino_push, coupling_push)
CHANNEL_PN_BASE = {
    "gdh_gluon": (0.08, 0.00, 0.02),
    "female_gaba_b_latdorsi": (-0.06, -0.10, -0.16),
    "left_acetyl_coa": (0.18, 0.02, 0.04),
    "male_left_5ht": (0.00, 0.10, 0.03),
    "female_left_noradrenaline": (0.14, 0.00, 0.03),
    "left_temporalis_5ht1a": (-0.02, 0.08, -0.03),
    "left_estrogen": (0.10, 0.00, 0.03),
    "right_love": (0.02, 0.08, 0.03),
    "hypoxia": (0.12, 0.00, 0.02),
    "right_dopamine": (0.28, 0.03, 0.06),
    "vasopressin_female": (0.24, 0.42, 0.22),  # dominant PN spark axis
    "male_oxytocin": (0.04, 0.10, 0.04),
    "muscle_a": (0.16, 0.00, 0.05),
    "muscle_b": (0.14, 0.00, 0.05),
    "right_5ht1b_synchrotron": (0.08, 0.00, 0.02),
    "right_androgen": (0.10, 0.00, 0.03),
    "left_endorphin": (0.04, 0.00, -0.02),
    "left_frontalis_d2": (0.15, 0.03, 0.04),
    "right_occipitalis_gaba_a": (-0.06, 0.06, -0.08),
    "right_acetylcholine": (0.16, 0.01, 0.04),
    "left_extraversion": (0.08, 0.00, 0.03),
    "glucocorticoid": (0.12, 0.00, 0.03),
    "right_cortisol": (0.16, 0.00, 0.04),
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
    values = {"p_push": 0.0, "nu_push": 0.0, "coupling_push": 0.0}
    for name, (p_d, nu_d, c_d) in CHANNEL_PN_BASE.items():
        factor = _state_factor(channels.get(name, "no_control"))
        values["p_push"] += p_d * factor
        values["nu_push"] += nu_d * factor
        values["coupling_push"] += c_d * factor

    alpha2_state = channels.get("right_alpha_2", "on")
    if alpha2_state == "off":
        values["coupling_push"] += 0.36
        values["nu_push"] += 0.16
    elif alpha2_state == "on":
        values["coupling_push"] -= 0.22
        values["nu_push"] -= 0.10

    values["vasopressin_on"] = 1.0 if channels.get("vasopressin_female") == "on" else 0.0
    values["dopamine_on"] = 1.0 if channels.get("right_dopamine") == "on" else 0.0
    values["cortisol_on"] = 1.0 if channels.get("right_cortisol") == "on" else 0.0
    values["gaba_b_on"] = 1.0 if channels.get("female_gaba_b_latdorsi") == "on" else 0.0
    values["alpha2_off"] = 1.0 if alpha2_state == "off" else 0.0
    return values


def spark_scalar(channels: dict[str, str], z_atomic: float, window_idx: int) -> float:
    ctrl = extract_controls(channels)
    spark_drive = (
        1.60 * ctrl["vasopressin_on"]
        + 0.95 * ctrl["alpha2_off"]
        + 0.70 * ctrl["cortisol_on"]
        + 0.55 * ctrl["dopamine_on"]
        - 0.90 * ctrl["gaba_b_on"]
    )
    spark_prob = 1.0 / (1.0 + np.exp(-spark_drive))
    phase = cos(float(z_atomic) * SPARK_ANGLE_RAD + SPARK_PHASE_LEAK)
    return float(spark_prob * phase * consciousness_window(window_idx))


def pn_dynamics(
    x: np.ndarray,
    channels: dict[str, str],
    z_atomic: float,
    window_idx: int,
    k_anchor: float = 0.45,
    eps: float = 1e-6,
) -> np.ndarray:
    proton, nu = float(x[0]), float(x[1])
    ctrl = extract_controls(channels)
    spark = spark_scalar(channels, z_atomic, window_idx)

    base_damp = 0.40
    coupling = np.clip(0.24 + ctrl["coupling_push"], 0.02, 1.30)
    p_push = ctrl["p_push"] + 1.15 * spark
    nu_push = ctrl["nu_push"] + 1.00 * spark

    dp = -base_damp * proton + coupling * nu + p_push
    dnu = -base_damp * nu + coupling * proton + nu_push
    dx = np.array([dp, dnu], dtype=float)

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
        dx = pn_dynamics(state, channels, z_atomic, window_idx)
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


def pn_potential(x: np.ndarray, channels: dict[str, str], z_atomic: float, window_idx: int) -> float:
    proton, nu = float(x[0]), float(x[1])
    ctrl = extract_controls(channels)
    spark = spark_scalar(channels, z_atomic, window_idx)
    coupling = np.clip(0.24 + ctrl["coupling_push"], 0.02, 1.30)
    damp = 0.40
    norm_x = np.linalg.norm(x)
    anchor = -0.45 * (norm_x - OMEGA) ** 2
    interaction = coupling * proton * nu
    forcing = ctrl["p_push"] * proton + ctrl["nu_push"] * nu
    spark_term = spark * (1.2 * proton + 1.0 * nu + 1.0)
    dissipation = 0.5 * damp * (proton * proton + nu * nu)
    return float(interaction + forcing + spark_term - dissipation + anchor)

