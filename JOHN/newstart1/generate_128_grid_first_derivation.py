from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt

MBTI = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISTP","ESTJ","ESTP",
    "ISFJ","ISFP","ESFJ","ESFP",
]
BLOODS = ["A", "B", "O", "AB"]
GENDERS = ["F", "M"]

SEED_ANGLE_DEG = 138.88
C = np.exp(1j * np.deg2rad(SEED_ANGLE_DEG))
GATE_RADIUS = 5.0 / 32.0

PROTON_POLE = 0.85 + 0.35j
ELECTRON_POLE = -0.85 - 0.35j
NEUTRINO_POLE = -0.15 + 0.90j
PHOTON_POLE = 0.15 - 0.90j


def bits_from_mbti(mbti: str) -> np.ndarray:
    return np.array([
        0 if mbti[0] == "I" else 1,
        0 if mbti[1] == "N" else 1,
        0 if mbti[2] == "T" else 1,
        0 if mbti[3] == "J" else 1,
    ], dtype=float)


def z0_from_type(mbti: str, blood: str, gender: str) -> complex:
    b = bits_from_mbti(mbti)
    blood_idx = BLOODS.index(blood)
    gender_idx = GENDERS.index(gender)
    x = (b[0] * 2 - 1) * 0.70 + (b[2] * 2 - 1) * 0.32 + (blood_idx - 1.5) * 0.20
    y = (b[1] * 2 - 1) * 0.70 + (b[3] * 2 - 1) * 0.32 + (gender_idx - 0.5) * 0.26
    return complex(x, y)


def hysteresis_state(t: float, prev_h: float) -> float:
    day_drive = 1.0 if 6.0 <= t < 18.0 else 0.0
    alpha = 0.08
    return (1 - alpha) * prev_h + alpha * day_drive


def G(z: complex, t: float, h: float, trait: np.ndarray) -> complex:
    eps = 1e-5
    q_p, q_e, q_nu, q_g = 1.0, -1.0, 0.25, 0.45
    f_p = q_p * (z - PROTON_POLE) / (abs(z - PROTON_POLE) ** 3 + eps)
    f_e = q_e * (z - ELECTRON_POLE) / (abs(z - ELECTRON_POLE) ** 3 + eps)
    f_n = q_nu * (z - NEUTRINO_POLE) / (abs(z - NEUTRINO_POLE) ** 3 + eps)
    f_g = q_g * (z - PHOTON_POLE) / (abs(z - PHOTON_POLE) ** 3 + eps)
    coulomb = -0.010 * (f_p + f_e + 0.8 * f_n + 0.55 * f_g)

    weak = 0.006 * (1.0 if 0.0 <= t < 6.0 else 0.35) * np.exp(1j * (0.6 + 0.3 * trait[1])) * z

    gate_center = 0.10 + 0.05j
    gate_local = math.exp(-((abs(z - gate_center) / GATE_RADIUS) ** 2))
    gate_force = -0.014 * gate_local * (z - gate_center)

    route = (0.008 * h - 0.005 * (1 - h)) * z
    return coulomb + weak + gate_force + route


def simulate_one(mbti: str, blood: str, gender: str, steps: int = 260):
    z = z0_from_type(mbti, blood, gender)
    trait = bits_from_mbti(mbti)
    h = 0.5
    dt = 0.10
    traj = [z]
    for k in range(steps):
        t = (24.0 * k) / steps
        h = hysteresis_state(t, h)
        # differential recurrence to avoid cardioid bulb collapse
        z = z + dt * (z * z + C + G(z, t, h, trait))
        r = abs(z)
        if r > 4.0:
            z = (z / r) * 3.2
        traj.append(z)
    return np.array(traj, dtype=np.complex128)


def main():
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)

    all_traj = []
    labels = []
    for mbti in MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                all_traj.append(simulate_one(mbti, blood, gender))
                labels.append(f"{mbti}-{blood}-{gender}")

    colors = {
        "INT": "#2f4bff", "ENT": "#ff4136", "INF": "#7e57c2", "ENF": "#28a745",
        "IST": "#17a2b8", "EST": "#ff8c00", "ISF": "#6c757d", "ESF": "#e83e8c",
    }

    plt.figure(figsize=(11, 11), dpi=140)
    for tr, lb in zip(all_traj, labels):
        c = colors.get(lb[:3], "#444")
        plt.plot(tr.real, tr.imag, color=c, alpha=0.35, linewidth=0.7)

    theta = np.linspace(0, 2 * np.pi, 300)
    gc = 0.10 + 0.05j
    plt.plot(gc.real + GATE_RADIUS * np.cos(theta), gc.imag + GATE_RADIUS * np.sin(theta), "k--", lw=0.7, alpha=0.4)
    plt.title("128 First-Derivation Grid (corrected differential recurrence)")
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.axis("equal")
    plt.grid(alpha=0.18)
    plt.tight_layout()

    out = out_dir / "FIRST_DERIVATION_128_GRID_v2.png"
    plt.savefig(out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
