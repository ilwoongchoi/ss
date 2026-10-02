from __future__ import annotations

"""
run_operator_facial_128_grid.py

Generate 128-type trajectories using the CURRENT operator:
  geometry_package.edge_stack_master_equation.sovereign_dynamics_step

Output is PNG (not just CSV) so "128-grid" is visible as trajectories on a 16x16 face lattice.

128 types = 16 MBTI x 4 blood x 2 gender.
We do not regress or fit. Types differ only by deterministic initial condition + phase offsets.
"""

import math
import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from geometry_package import absolute_constants as ac
from fusion_clean import sovereign_dynamics_step


ROOT = Path(r"d:\Users\user\Documents\newstart")
OUT_DIR = ROOT / "analysis_results"

OUT_FACE_PNG_PEOPLE = OUT_DIR / "operator_face_128_people.png"
OUT_STATE3D_PNG_PEOPLE = OUT_DIR / "operator_state3d_128_people.png"
OUT_FACE_PNG_USER = OUT_DIR / "operator_face_128_user.png"
OUT_STATE3D_PNG_USER = OUT_DIR / "operator_state3d_128_user.png"


MBTIS = [
    "ESTJ",
    "ENTJ",
    "ESFJ",
    "ENFJ",
    "ESTP",
    "ENTP",
    "ESFP",
    "ENFP",
    "ISTJ",
    "INTJ",
    "ISFJ",
    "INFJ",
    "ISTP",
    "INTP",
    "ISFP",
    "INFP",
]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]


@dataclass(frozen=True)
class Type128:
    idx: int
    mbti: str
    blood: str
    gender: str

    @property
    def key(self) -> str:
        return f"{self.mbti}_{self.blood}_{self.gender}"


def minute_to_clock(minute: int) -> str:
    minute = int(minute) % (24 * 60)
    return f"{minute // 60:02d}:{minute % 60:02d}"


def motif_target_state4() -> np.ndarray:
    # Degrees from SM motif scaffold: BM=6, BW=8, SM=8, SW=10.
    deg = np.array([6.0, 8.0, 8.0, 10.0], dtype=float)
    return (deg / float(np.linalg.norm(deg))) * float(ac.OMEGA_TARGET)


def type_initial_state4(t: Type128) -> np.ndarray:
    """
    Deterministic (no fitting) initial conditions:
    - start near motif_target
    - apply small structured offsets from MBTI/blood/gender so the 128 types separate
    - normalize back to ||x||=OMEGA_TARGET
    """
    base = motif_target_state4()

    # MBTI bits: E/I, S/N, T/F, J/P
    ei = 1.0 if t.mbti[0] == "E" else -1.0
    sn = 1.0 if t.mbti[1] == "N" else -1.0
    tf = 1.0 if t.mbti[2] == "T" else -1.0
    jp = 1.0 if t.mbti[3] == "J" else -1.0

    # Blood as small signed bias (keep magnitudes small; this is just separation).
    blood_bias = {"O": -1.0, "A": 1.0, "B": -0.5, "AB": 0.5}.get(t.blood, 0.0)

    # Gender chirality: M pushes "male" components (BM/SM), F pushes "female" components (BW/SW).
    g = 1.0 if t.gender == "M" else -1.0

    # Structured delta (kept intentionally small).
    delta = np.array(
        [
            0.28 * g + 0.12 * ei + 0.06 * tf,         # BM
            -0.22 * g + 0.08 * jp + 0.04 * blood_bias, # BW
            0.14 * sn + 0.06 * jp - 0.04 * g,          # SM
            0.10 * ei - 0.10 * sn + 0.05 * blood_bias, # SW
        ],
        dtype=float,
    )

    x0 = base + delta
    n = float(np.linalg.norm(x0))
    if n > 1.0e-9:
        x0 = x0 * (float(ac.OMEGA_TARGET) / n)
    return x0


def state4_to_face_xy(state4: np.ndarray) -> tuple[float, float]:
    """
    4D -> 2D face projection.

    x: male-vs-female axis  (right/left on face lattice)
    y: big-vs-small axis    (vertical metabolic depth)
    """
    bm, bw, sm, sw = [float(v) for v in np.asarray(state4, dtype=float).reshape(4)]
    male = bm + sm
    female = bw + sw
    big = bm + bw
    small = sm + sw

    # Smoothly map to [0,16] using tanh (avoid outliers blowing up the picture).
    x = 8.0 + 7.5 * math.tanh((male - female) / float(ac.OMEGA_TARGET))
    y = 8.0 + 7.5 * math.tanh((big - small) / float(ac.OMEGA_TARGET))
    x = float(np.clip(x, 0.0, 16.0))
    y = float(np.clip(y, 0.0, 16.0))
    return x, y


def iter_type_trajectory(
    t: Type128,
    *,
    persona: str,
    n_steps: int = 96,  # 15-min steps over 24h
    dt: float = 0.1,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns:
      states4: (n_steps, 4)
      face_xy: (n_steps, 2)
    """
    x = type_initial_state4(t)

    states = []
    xy = []

    # Deterministic phase offsets (slotting without random search).
    minute_offset = int(round(1440.0 * (t.idx / 128.0))) % (24 * 60)
    pf_offset = float(t.idx / 128.0)

    for i in range(n_steps):
        minute = (i * 15 + minute_offset) % (24 * 60)
        clock = minute_to_clock(minute)
        pf = float((i / max(n_steps - 1, 1) + pf_offset) % 1.0)

        out = sovereign_dynamics_step(
            x,
            phase_fill=pf,
            clock_hhmm=clock,
            dt=dt,
            control_override={"__persona__": str(persona)},
        )
        x = np.asarray(out["state_next"], dtype=float).reshape(4)

        states.append(x.copy())
        xy.append(state4_to_face_xy(x))

    return np.asarray(states, dtype=float), np.asarray(xy, dtype=float)


def all_types_128() -> list[Type128]:
    out: list[Type128] = []
    idx = 0
    for mbti in MBTIS:
        for blood in BLOODS:
            for gender in GENDERS:
                out.append(Type128(idx=idx, mbti=mbti, blood=blood, gender=gender))
                idx += 1
    return out


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    ap = argparse.ArgumentParser()
    ap.add_argument("--persona", choices=["people", "user", "both"], default="people")
    args = ap.parse_args()

    types = all_types_128()
    blood_colors = {"O": "#d32f2f", "A": "#1976d2", "B": "#388e3c", "AB": "#7b1fa2"}

    def render(persona: str, out_face: Path, out_3d: Path) -> None:
        # --- 2D FACE GRID ---
        fig, ax = plt.subplots(figsize=(16, 16), facecolor="white")
        ax.set_facecolor("#fcfcfc")
        for i in range(17):
            ax.axhline(i, color="#dddddd", lw=0.6, zorder=0)
            ax.axvline(i, color="#dddddd", lw=0.6, zorder=0)
        # Spine / seam: x+y=16
        ax.plot([0, 16], [16, 0], color="#ff9900", lw=4, alpha=0.8)
        # Ridges (visual refs; not a bifurcation engine).
        ax.axvline(5, color="#00cc99", ls="--", lw=2, alpha=0.5)
        ax.axvline(11, color="#00cc99", ls="--", lw=2, alpha=0.5)

        for t in types:
            _, xy = iter_type_trajectory(t, persona=persona)
            c = blood_colors.get(t.blood, "#444444")
            alpha = 0.85 if t.gender == "M" else 0.45
            ax.plot(xy[:, 0], xy[:, 1], color=c, alpha=alpha, lw=1.0)
            ax.scatter([xy[0, 0]], [xy[0, 1]], color=c, alpha=alpha, s=12, marker="o" if t.gender == "M" else "s")

        ax.set_xlim(0, 16)
        ax.set_ylim(0, 16)
        ax.set_aspect("equal")
        ax.set_title(f"OPERATOR 128-GRID ({persona})\nFace lattice projection from state4 dynamics", fontsize=16)
        fig.savefig(out_face, dpi=300, bbox_inches="tight")
        plt.close(fig)

        # --- 3D STATE TRAJECTORIES (BM,BW,SM) ---
        fig = plt.figure(figsize=(12, 10))
        ax3 = fig.add_subplot(111, projection="3d")
        for t in types:
            states, _ = iter_type_trajectory(t, persona=persona)
            c = blood_colors.get(t.blood, "#444444")
            alpha = 0.85 if t.gender == "M" else 0.45
            ax3.plot(states[:, 0], states[:, 1], states[:, 2], color=c, alpha=alpha, lw=0.8)

        ax3.set_xlabel("BM")
        ax3.set_ylabel("BW")
        ax3.set_zlabel("SM")
        ax3.set_title(f"OPERATOR 128 Trajectories in (BM,BW,SM) ({persona})")
        fig.savefig(out_3d, dpi=220, bbox_inches="tight")
        plt.close(fig)

    todo: list[tuple[str, Path, Path]] = []
    if args.persona in ("people", "both"):
        todo.append(("people", OUT_FACE_PNG_PEOPLE, OUT_STATE3D_PNG_PEOPLE))
    if args.persona in ("user", "both"):
        todo.append(("user", OUT_FACE_PNG_USER, OUT_STATE3D_PNG_USER))

    for persona, out_face, out_3d in todo:
        render(persona, out_face, out_3d)
        print(str(out_face))
        print(str(out_3d))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
