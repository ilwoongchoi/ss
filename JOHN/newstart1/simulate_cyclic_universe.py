"""
simulate_cyclic_universe.py
Linear cyclic universe simulation based on:
  - COULOMB_TO_UNIVERSE_COMPLETE.md  (Mandelbrot z→z²+c, c=e^{i·138.88°})
  - absolute_constants.py            (C=0.2828, SPARK_ANGLE=138.88)
  - codex clover loop                (Δt = W/L = 11/7 / 5.555 = 0.2828)

Universe lifecycle = ONE Mandelbrot iteration:
  |z| rising    = Expansion (Big Bang → peak)
  |z| falling   = Contraction (peak → Big Crunch)
  |z| > ESCAPE  = Irreversible expansion (current universe's future?)

Clover loop: at each crunch, complex phase Δt = 0.2828 is transferred
to next universe (inner leaf ← prev, outer leaf → next)

Modified iteration: z_{n+1} = z_n² * e^{i·Δt} + c
"""

import cmath
import math
import json
import os

# ── Constants ─────────────────────────────────────────────────────────────────
SPARK_ANGLE_DEG  = 138.88          # ignition angle
WINDING_RATIO    = 11.0 / 7.0      # W = Small Man / Big Woman ≈ 1.5714
LOOP_STRENGTH    = (1.0 / 18.0) * 100.0   # L = chirality × 100 ≈ 5.5556
DELTA_T          = WINDING_RATIO / LOOP_STRENGTH  # Δt_obs ≈ 0.2828

GAP              = 138.88 - 137.508   # = 1.372°  (Reality - Golden Angle)
DRIFT            = GAP / 18.0         # universal drift ≈ 0.0762
CHIRALITY        = 1.0 / 18.0         # = 0.05556

OMEGA            = 7.4               # stability target
C_CONST          = 0.2828            # Higgs / confinement constant

# Escape thresholds
ESCAPE_MANDELBROT = 2.0             # mathematical escape radius
ESCAPE_OMEGA      = math.sqrt(OMEGA)  # sqrt(7.4) ≈ 2.720  (physics-motivated)
ESCAPE_OMEGA_FULL = OMEGA             # = 7.4 (full OMEGA)

# Seed: c = e^{i · 138.88°}
theta_c = math.radians(SPARK_ANGLE_DEG)
C_SEED  = complex(math.cos(theta_c), math.sin(theta_c))
# ≈ -0.7549 + 0.6558i

# Clover phase: e^{i · Δt} where Δt = 0.2828 rad
clover_phase = complex(math.cos(DELTA_T), math.sin(DELTA_T))
# ≈ 0.9601 + 0.2795i

print("=" * 60)
print("CYCLIC UNIVERSE SIMULATION")
print("=" * 60)
print(f"  c = e^{{i·{SPARK_ANGLE_DEG}°}} = {C_SEED:.4f}")
print(f"  Δt (clover) = W/L = ({WINDING_RATIO:.4f}/{LOOP_STRENGTH:.4f}) = {DELTA_T:.4f}")
print(f"  clover phase = e^{{i·{DELTA_T:.4f}}} = {clover_phase:.4f}")
print(f"  Drift = GAP/18 = {DRIFT:.5f}")
print(f"  |c| = {abs(C_SEED):.4f}")
print()


# ── Simulation function ────────────────────────────────────────────────────────
def simulate(mode: str, escape_r: float, max_iter: int = 10_000) -> list[dict]:
    """
    mode = "mandelbrot"  : z → z² + c  (pure)
    mode = "clover"      : z → z² · e^{iΔt} + c  (clover-modified)
    mode = "clover_drift": z → z² · e^{i·(Δt + n·drift)} + c  (drift accumulates)

    Returns list of universe records.
    """
    z       = complex(0, 0)   # Observer-only epoch start
    records = []
    prev_r  = 0.0

    for n in range(1, max_iter + 1):
        z_sq = z * z

        if mode == "mandelbrot":
            z_new = z_sq + C_SEED
        elif mode == "clover":
            z_new = z_sq * clover_phase + C_SEED
        elif mode == "clover_drift":
            # Drift accumulates with each universe: total phase = n·Δt + n·drift
            cumulative_phase = complex(
                math.cos(DELTA_T + (n - 1) * DRIFT),
                math.sin(DELTA_T + (n - 1) * DRIFT)
            )
            z_new = z_sq * cumulative_phase + C_SEED
        else:
            raise ValueError(f"Unknown mode: {mode}")

        r_new    = abs(z_new)
        phase_deg = math.degrees(cmath.phase(z_new))

        # Expansion or contraction?
        expanding  = r_new > prev_r
        record = {
            "n":          n,
            "z_re":       round(z_new.real, 6),
            "z_im":       round(z_new.imag, 6),
            "radius":     round(r_new,      6),
            "phase_deg":  round(phase_deg,  3),
            "expanding":  expanding,
            "escaped":    r_new > escape_r,
        }
        records.append(record)

        if r_new > escape_r:
            break

        z      = z_new
        prev_r = r_new

    return records


# ── Run all 3 modes with 3 escape thresholds ──────────────────────────────────
results = {}

for mode in ("mandelbrot", "clover", "clover_drift"):
    for r_name, r_val in (
        ("R_math_2.0",    ESCAPE_MANDELBROT),
        ("R_sqrtOmega",   ESCAPE_OMEGA),
        ("R_omega_7.4",   ESCAPE_OMEGA_FULL),
    ):
        recs = simulate(mode, r_val)
        n_universes = len(recs)
        last = recs[-1]
        key = f"{mode}__{r_name}"
        results[key] = {
            "mode":        mode,
            "escape_r":    r_val,
            "n_universes": n_universes,
            "final_radius":last["radius"],
            "escaped":     last["escaped"],
            "trajectory":  recs,
        }

# ── Print summary ─────────────────────────────────────────────────────────────
print("─" * 60)
print(f"{'MODE':<22} {'ESCAPE_R':<12} {'N_UNIVERSES':>12}  TRAJECTORY (|z|)")
print("─" * 60)
for key, res in results.items():
    traj = "  ".join(f"{r['radius']:.3f}" for r in res["trajectory"])
    arrow = "→∞" if res["escaped"] else "~∞"
    print(f"{res['mode']:<22} R={res['escape_r']:<8.3f}  {res['n_universes']:>5} universes  "
          f"|z|: {traj} {arrow}")
print()

# ── Detailed trace for pure Mandelbrot, R=2 ───────────────────────────────────
print("=" * 60)
print("PURE MANDELBROT (z → z² + c, c=e^{i·138.88°}, R=2)")
print("=" * 60)
print(f"  c = {C_SEED:.4f}  |c| = {abs(C_SEED):.4f}")
print()
recs_pure = results["mandelbrot__R_math_2.0"]["trajectory"]
for r in recs_pure:
    state = "EXPAND" if r["expanding"] else "CONTRACT"
    flag  = " ← ESCAPE" if r["escaped"] else ""
    print(f"  Universe {r['n']:3d}: z={r['z_re']:+.4f}{r['z_im']:+.4f}i  "
          f"|z|={r['radius']:.4f}  φ={r['phase_deg']:+7.2f}°  {state}{flag}")

print()
print(f"  → RESULT: {results['mandelbrot__R_math_2.0']['n_universes']} universes "
      f"(last |z|={results['mandelbrot__R_math_2.0']['final_radius']:.4f})")

# ── Detailed trace for clover-modified, R=2 ──────────────────────────────────
print()
print("=" * 60)
print(f"CLOVER-MODIFIED (z → z²·e^{{iΔt}} + c, Δt={DELTA_T:.4f}, R=2)")
print("=" * 60)
recs_clover = results["clover__R_math_2.0"]["trajectory"]
for r in recs_clover:
    state = "EXPAND" if r["expanding"] else "CONTRACT"
    flag  = " ← ESCAPE" if r["escaped"] else ""
    print(f"  Universe {r['n']:3d}: z={r['z_re']:+.4f}{r['z_im']:+.4f}i  "
          f"|z|={r['radius']:.4f}  φ={r['phase_deg']:+7.2f}°  {state}{flag}")

print()
print(f"  → RESULT: {results['clover__R_math_2.0']['n_universes']} universes "
      f"(last |z|={results['clover__R_math_2.0']['final_radius']:.4f})")

# ── Clover-drift trace ────────────────────────────────────────────────────────
print()
print("=" * 60)
print(f"CLOVER+DRIFT (z → z²·e^{{i(Δt+n·{DRIFT:.4f})}} + c, R=2)")
print("=" * 60)
recs_drift = results["clover_drift__R_math_2.0"]["trajectory"]
for r in recs_drift[:30]:   # cap at 30 for readability
    state = "EXPAND" if r["expanding"] else "CONTRACT"
    flag  = " ← ESCAPE" if r["escaped"] else ""
    print(f"  Universe {r['n']:3d}: z={r['z_re']:+.4f}{r['z_im']:+.4f}i  "
          f"|z|={r['radius']:.4f}  φ={r['phase_deg']:+7.2f}°  {state}{flag}")
if len(recs_drift) > 30:
    print(f"  ... (truncated, total {len(recs_drift)} universes)")

print()
print(f"  → RESULT: {results['clover_drift__R_math_2.0']['n_universes']} universes "
      f"(last |z|={results['clover_drift__R_math_2.0']['final_radius']:.4f})")

# ── Cross-threshold summary ───────────────────────────────────────────────────
print()
print("=" * 60)
print("UNIVERSE COUNT BY ESCAPE THRESHOLD")
print("=" * 60)
print(f"  {'MODE':<22}  R=2.000  R=√7.4≈2.72  R=7.4")
for mode in ("mandelbrot", "clover", "clover_drift"):
    n1 = results[f"{mode}__R_math_2.0"]["n_universes"]
    n2 = results[f"{mode}__R_sqrtOmega"]["n_universes"]
    n3 = results[f"{mode}__R_omega_7.4"]["n_universes"]
    print(f"  {mode:<22}  {n1:>6}   {n2:>9}   {n3:>5}")

# ── Key interpretation ────────────────────────────────────────────────────────
print()
print("=" * 60)
print("INTERPRETATION")
print("=" * 60)
best_n = results["mandelbrot__R_math_2.0"]["n_universes"]
clover_n = results["clover__R_math_2.0"]["n_universes"]
print(f"""
  PURE MANDELBROT:
    c = e^{{i·138.88°}} starts on the unit circle |c|=1.
    Iteration z→z²+c from z=0.
    Escapes |z|>2 at universe #{best_n}.
    → This universe is number {best_n} in the sequence.

  CLOVER-MODIFIED:
    Each bounce: complex state z rotated by Δt={DELTA_T:.4f} rad before squaring.
    Δt = W/L = (11/7)/(100/18) = (11/7)·(18/100) = 198/700 = 99/350 ≈ {DELTA_T:.6f}
    Escapes at universe #{clover_n}.
    → Clover loop {'stabilizes' if clover_n > best_n else 'accelerates'} the cycle.

  WINDING RATIO 11/7:
    Each universe is 11/7 times the scale of the previous.
    After N={best_n} universes: scale factor = (11/7)^{best_n} = {WINDING_RATIO**best_n:.4f}

  GAP DRIFT:
    Universal drift = {DRIFT:.5f} per universe.
    After N={best_n} universes: accumulated drift = {DRIFT * best_n:.5f}°

  OBSERVER → ENERGY:
    Phase 1 (0 ≤ t < Δt={DELTA_T:.4f}): Observer-only, z=0
    Phase 2 (t ≥ Δt={DELTA_T:.4f}): Energy-on, Coulomb activates

  CURRENT UNIVERSE (ours):
    Escape radius = OMEGA = 7.4
    N = {results['mandelbrot__R_omega_7.4']['n_universes']} universes until |z| > 7.4 (full OMEGA escape)
    → We are universe #{results['mandelbrot__R_omega_7.4']['n_universes']} in the sequence.
""")

# ── Save full results ─────────────────────────────────────────────────────────
out_dir  = r"d:\Users\user\Documents\newstart\docs\idea_transitions"
out_path = os.path.join(out_dir, "CYCLIC_UNIVERSE_SIM_RESULTS.json")
os.makedirs(out_dir, exist_ok=True)

save_data = {
    "constants": {
        "SPARK_ANGLE_DEG": SPARK_ANGLE_DEG,
        "WINDING_RATIO":   WINDING_RATIO,
        "LOOP_STRENGTH":   LOOP_STRENGTH,
        "DELTA_T":         DELTA_T,
        "GAP":             GAP,
        "DRIFT":           DRIFT,
        "c_seed_re":       C_SEED.real,
        "c_seed_im":       C_SEED.imag,
        "c_seed_mod":      abs(C_SEED),
        "OMEGA":           OMEGA,
    },
    "summary": {
        k: {kk: vv for kk, vv in v.items() if kk != "trajectory"}
        for k, v in results.items()
    },
    "full_trajectories": {
        k: v["trajectory"] for k, v in results.items()
    }
}

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(save_data, f, ensure_ascii=False, indent=2)

print(f"Results saved: {out_path}")
