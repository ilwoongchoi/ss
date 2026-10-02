"""
generate_unified_128_grid.py
============================
K8 Mandelbrot Universe:  z_new = z² - z + h(t)

h(t) = -L(phase, channels) @ z * DT   (K8 Laplacian dynamics)

3 primitives:  quark(1), gluon(i), higgs(C)
Composites rebranch from primitives at t=88 (proton_landing / Right Love reset)
After t=88:  vasopressin_female ON  →  continuous equilibrium maintenance

128 archetypes × 128 time windows
6 named archetypes marked on grid
"""

import numpy as np
import matplotlib.pyplot as plt
import os

from fusion_core import (
    SUBJECTS, IDX, laplacian, apply_channels,
    PHASE_TABLE, C, OMEGA,
)
from universe_sim import primordial_z
from archetypes import (
    ARCHETYPE_CHANNEL_STATES, ARCHETYPE_PARAMS, BLOOD_TYPE_COORDS,
)

# ── Constants ─────────────────────────────────────────────────────────────────
E_INV        = 1.0 / np.e          # Hannah Fry observer constant
ENTROPY_DEBT = 1/64 + 1/256        # Gravitational lensing (recirculation)
DT           = 0.03

NAMED = list(ARCHETYPE_CHANNEL_STATES.keys())   # 6 archetypes


# ── Phase mapper: 128 steps = one circadian day ───────────────────────────────
def phase_at(t: int) -> str:
    """Map grid column t (0..127) to K8 phase name via circadian clock."""
    hour = t * 24.0 / 128          # 0.0 .. 24.0
    if 2.25 <= hour < 4.50:
        if 3.00 <= hour < 3.25:
            return "night_spark"
        return "hysteresis"
    if 9.75 <= hour < 15.75:
        return "phase2"
    if 15.75 <= hour < 16.50:
        return "phase1"
    if 16.50 <= hour < 16.75:     # t=88  proton_landing / Right Love
        return "proton_landing"
    return "phase1"


# ── Rebranching: reset composites from 3 primitives ──────────────────────────
def rebranch(z: np.ndarray) -> np.ndarray:
    """
    At Right Love (t=88) reset:
      photon   = quark × gluon
      electron = gluon²
      neutrino = gluon × higgs²
      w_boson  = quark × higgs    ← BW axis
      z_boson  = gluon × higgs    ← SM axis
    """
    q = z[IDX["quark"]]
    g = z[IDX["gluon"]]
    h = z[IDX["higgs"]]
    z[IDX["photon"]]   = q * g
    z[IDX["electron"]] = g ** 2
    z[IDX["neutrino"]] = g * h ** 2
    z[IDX["w_boson"]]  = q * h
    z[IDX["z_boson"]]  = g * h
    return z


# ── Initial state from blood type ─────────────────────────────────────────────
def make_z0(arch_name: str) -> np.ndarray:
    """
    Start from primordial_z(C), then scale quark/gluon amplitudes
    so that BW/SM ratio matches blood type coordinates.
    All composites rebranch from these primitives.
    """
    params = ARCHETYPE_PARAMS[arch_name]
    blood  = params.get("blood", params.get("blood_type", "AB"))
    coords = BLOOD_TYPE_COORDS.get(blood, {"BW": OMEGA/2, "SM": OMEGA/2})
    bw_t   = coords["BW"]
    sm_t   = coords["SM"]

    z = primordial_z(C).copy()

    # Scale primitives so composite amplitudes approach blood-type targets
    scale = 0.08          # start damped — Mandelbrot unfolds from here

# Maxwell Cavity Constants (Synchrotron Boundary)
MAXWELL_R_MAJOR = 2.125      # Torus major radius
MAXWELL_R_MINOR = 0.2235     # Torus minor radius (~2.125/9.5)
MAXWELL_Q = 11.8             # Quality factor
MAXWELL_BETA = MAXWELL_R_MINOR / MAXWELL_R_MAJOR  # Aspect ratio

# Cavity boundary operator: projects z onto torus surface
def maxwell_boundary(z: np.ndarray) -> np.ndarray:
    """Apply Maxwell cavity boundary condition - toroidal constraint."""
    norms = np.abs(z)
    # Torus radial constraint: particles orbit at R_major ± R_minor
    r_eff = np.mean(norms) if norms.size > 0 else 0.0
    if r_eff > MAXWELL_R_MAJOR + MAXWELL_R_MINOR:
        # Outside outer wall: pull back to boundary
        scale = (MAXWELL_R_MAJOR + MAXWELL_R_MINOR) / (r_eff + 1e-15)
        return z * scale
    elif r_eff < MAXWELL_R_MAJOR - MAXWELL_R_MINOR and r_eff > 0:
        # Inside inner wall (hollow core): push out
        scale = (MAXWELL_R_MAJOR - MAXWELL_R_MINOR) / (r_eff + 1e-15)
        return z * scale
    return z

    q_amp = bw_t / (OMEGA + 1e-9)
    g_amp = sm_t / (OMEGA + 1e-9)

    z[IDX["quark"]]  = q_amp * scale * (1.0 + 0j)
    z[IDX["gluon"]]  = g_amp * scale * 1j
    z[IDX["higgs"]]  = C + 0j

    z = rebranch(z)
    return z


# ── SPARK observable ──────────────────────────────────────────────────────────
def spark_intensity(z: np.ndarray) -> float:
    """BW: proton-side capture strength, normalised to OMEGA."""
    wb = abs(z[IDX["w_boson"]])
    zb = abs(z[IDX["z_boson"]])
    s  = wb + zb + 1e-15
    return float(wb / s * OMEGA)


# ── Archetype class ───────────────────────────────────────────────────────────
class Archetype:
    def __init__(self, grid_idx: int):
        name_idx  = grid_idx * len(NAMED) // 128
        self.name = NAMED[name_idx % len(NAMED)]
        self.z    = make_z0(self.name)
        self.base_ch   = dict(ARCHETYPE_CHANNEL_STATES[self.name])
        self.post_reset = False

    def step(self, t: int) -> float:
        phase = phase_at(t)

        # Channel states: start from archetype base, then apply phase-specific states
        ch = dict(self.base_ch)
        
        # Merge phase-specific channel states from PHASE_TABLE (all 30 channels)
        phase_states = PHASE_TABLE.get(phase, {})
        for channel, state in phase_states.items():
            if state != "no_control":  # Phase state overrides archetype base
                ch[channel] = state
        
        # Post-reset: vasopressin maintenance after rebranching
        if self.post_reset:
            ch["vasopressin_female"] = "on"
            ch["right_love"] = "no_control"

        # h(t) = K8 Laplacian contribution
        w = apply_channels(ch)
        L = laplacian(w)
        h = -L @ self.z * DT

        # Mandelbrot recursion: z = z² - z + h
        self.z = self.z ** 2 - self.z + h

        # Escape radius: clip before NaN propagates
        # |z| > 10 = escaped (chaotic) → pull back to boundary
        norms = np.abs(self.z)
        escaped = norms > 10.0
        if escaped.any():
            self.z[escaped] = 10.0 * self.z[escaped] / (norms[escaped] + 1e-15)

        # Right Love reset at t=88  (proton_landing)
        if t == 88:
            self.z = rebranch(self.z)
            self.post_reset = True

        # Maxwell cavity boundary: toroidal constraint on particle orbits
        self.z = maxwell_boundary(self.z)

        # Entropy lensing: gravitational recirculation (not energy loss)
        self.z -= ENTROPY_DEBT * self.z

        return spark_intensity(self.z)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("K8 MANDELBROT UNIVERSE  z = z^2 - z + h(t)")
    print(f"C={C:.6f}  OMEGA={OMEGA}  E_INV={E_INV:.4f}")
    print(f"Rebranch at t=88 (Right Love)  →  Vasopressin maintenance after")
    print()

    grid      = np.zeros((128, 128))
    universes = [Archetype(i) for i in range(128)]

    for t in range(128):
        if t % 16 == 0:
            print(f"  t={t:3d}  phase={phase_at(t)}")
        for y in range(128):
            val = universes[y].step(t)
            grid[y, t] = min(val, OMEGA * 4)   # clip outliers

    # ── Emergence report ──────────────────────────────────────────────────────
    print()
    print("=== EMERGENCE ===")
    valid = grid[grid > 1e-6]
    if len(valid):
        print(f"  mean SPARK : {np.mean(valid):.4f}   (OMEGA={OMEGA})")
        print(f"  std  SPARK : {np.std(valid):.4f}")
        print(f"  net flow   : {np.mean(valid) - ENTROPY_DEBT:.4f}")
    else:
        print("  (all zero — check imports)")

    print()
    print("6 Named Archetypes:")
    for i, name in enumerate(NAMED):
        y    = i * 128 // len(NAMED)
        traj = grid[y, :]
        print(f"  {name:25s}  row={y:3d}  "
              f"t=0:{traj[0]:.3f}  t=88:{traj[88]:.3f}  t=127:{traj[-1]:.3f}")

    # ── Plot ──────────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(
        2, 1, figsize=(14, 12), facecolor="black",
        gridspec_kw={"height_ratios": [4, 1]},
    )

    ax = axes[0]
    ax.set_facecolor("black")
    vmax = float(np.percentile(valid, 95)) if len(valid) else OMEGA
    im   = ax.imshow(grid, aspect="auto", cmap="magma", origin="lower",
                     vmin=0, vmax=vmax)
    plt.colorbar(im, ax=ax, label="SPARK (BW)", shrink=0.8)

    # Mark 6 named archetypes
    for i, name in enumerate(NAMED):
        y     = i * 128 // len(NAMED)
        label = name.replace("_female", "").replace("_male", "")
        ax.axhline(y=y, color="cyan", alpha=0.35, lw=0.8)
        ax.text(2, y + 0.5, label, color="cyan", fontsize=7, va="bottom")

    # Mark key time windows
    for t_mark, label, col in [
        (17,  "night_spark",   "yellow"),
        (72,  "coulomb",       "lime"),
        (88,  "rebranch",      "white"),
    ]:
        ax.axvline(x=t_mark, color=col, alpha=0.55, lw=1)
        ax.text(t_mark + 0.5, 122, label, color=col, fontsize=7,
                rotation=90, va="top")

    ax.set_title(
        f"K8 MANDELBROT UNIVERSE   z = z² - z + h(t)\n"
        f"primitives: quark · gluon · higgs  |  rebranch t=88  |  OMEGA={OMEGA}",
        color="white", fontsize=11,
    )
    ax.set_xlabel("t (128 windows)", color="white")
    ax.set_ylabel("Archetype (128)", color="white")
    ax.tick_params(colors="white")

    # Bottom panel: mean SPARK over time
    ax2 = axes[1]
    ax2.set_facecolor("black")
    mean_t = np.mean(grid, axis=0)
    ax2.plot(mean_t, color="orange", lw=1.5, label="mean SPARK")
    ax2.axhline(y=OMEGA,        color="cyan",  ls="--", lw=1, alpha=0.7,
                label=f"OMEGA={OMEGA}")
    ax2.axhline(y=ENTROPY_DEBT, color="gray",  ls=":",  lw=0.8, alpha=0.6,
                label=f"entropy debt={ENTROPY_DEBT:.4f}")
    ax2.axvline(x=88, color="white", ls="--", lw=0.8, alpha=0.5)
    ax2.set_ylabel("mean SPARK", color="white")
    ax2.tick_params(colors="white")
    ax2.legend(facecolor="#111", labelcolor="white", fontsize=8)

    os.makedirs("analysis_results", exist_ok=True)
    outpath = "analysis_results/UNIFIED_128_GRID.png"
    plt.tight_layout()
    plt.savefig(outpath, dpi=200, bbox_inches="tight", facecolor="black")
    plt.close()
    print(f"\n[DONE] {outpath}")


if __name__ == "__main__":
    main()
