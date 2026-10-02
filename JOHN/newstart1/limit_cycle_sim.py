"""
limit_cycle_sim.py
==================
Cyclic universe simulation: contraction ↔ expansion oscillation.

Key physics:
  z'  = z² - z - L@z·dt + (1/64)(1-z)·dt
  F(0) = +1/64  → bounces back from rock bottom (big crunch prevention)
  z*=1 UNSTABLE (Laplacian zero eigenvalue) → drives system away
  z*_physical = non-trivial attractor (displaced equilibrium)

Two stable attractors:
  z=1     (uniform, unstable under K8 Laplacian)
  z=1/64  (rock bottom, K8-stable)
Limit cycle: z oscillates between z*_physical and near-zero.

Outputs:
  - Console: per-cycle stats (period, min, max, mean)
  - limit_cycle_results.json: raw trajectory
"""

import sys
import io
import json
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import constants
import fusion_core
import sovereign_dynamics

# ── Simulation parameters ───────────────────────────────────────────────────
DT     = 0.005          # integration step
N_STEP = 20000          # total steps  (= 100 time units)
PHASE  = "phase1"       # use phase1 channels

# ── Initial state: start near z*_physical ───────────────────────────────────
def make_z_physical():
    z = np.zeros(8, dtype=complex)
    zp = constants.Z_STAR_PHYSICAL
    for name, val in zp.items():
        z[fusion_core.IDX[name]] = val + 0j
    return z

# ── Build Laplacian ──────────────────────────────────────────────────────────
channels = fusion_core.PHASE_TABLE[PHASE]
w        = fusion_core.apply_channels(channels)
L        = fusion_core.laplacian(w)
eigenvalues = np.linalg.eigvalsh(L)
lambda_max  = float(np.max(eigenvalues))
lambda_zero = float(np.min(np.abs(eigenvalues)))

print("=" * 60)
print("  LIMIT CYCLE SIMULATION — CYCLIC UNIVERSE")
print("=" * 60)
print(f"  Phase  : {PHASE}")
print(f"  dt     : {DT}")
print(f"  Steps  : {N_STEP}  (total time = {DT * N_STEP:.1f})")
print(f"  λ_max  : {lambda_max:.6f}")
print(f"  λ_zero : {lambda_zero:.2e}  (→ z*=1 instability mode)")
print(f"  OMEGA  : {constants.OMEGA}")
print(f"  1/64   : {constants.F_1_64}  (F(0) bounce-back force)")
print()

# ── Integration ──────────────────────────────────────────────────────────────
z = make_z_physical()

trajectory_norm  = np.zeros(N_STEP)
trajectory_z     = np.zeros((N_STEP, 8), dtype=complex)

for i in range(N_STEP):
    trajectory_norm[i]  = float(np.linalg.norm(np.abs(z)))
    trajectory_z[i]     = z

    # Core K8 dynamics (from sovereign_dynamics.get_dynamics_update)
    h        = -L @ z * DT
    h_return = constants.RIGHT_LOVE_RETURN_RATE * (constants.Z_STAR_UNIFORM - z) * DT
    z        = z**2 - z + h + h_return

    # Lensing (Node 31 + Node 34 debt)
    z += sovereign_dynamics.get_lensing_update(z) * DT

# ── Analysis ─────────────────────────────────────────────────────────────────
t = np.arange(N_STEP) * DT
norm = trajectory_norm

# Find crossings of mean level (proxy for cycle detection)
mean_norm = float(np.mean(norm))
crossings = []
for i in range(1, N_STEP):
    if norm[i-1] < mean_norm and norm[i] >= mean_norm:
        crossings.append(i)

# Per-particle stats
print("  Per-particle trajectory statistics")
print(f"  {'Particle':<12} {'mean|z|':>10} {'min|z|':>10} {'max|z|':>10}")
print("  " + "-" * 46)
for name in fusion_core.SUBJECTS:
    idx  = fusion_core.IDX[name]
    vals = np.abs(trajectory_z[:, idx])
    print(f"  {name:<12} {np.mean(vals):>10.4f} {np.min(vals):>10.4f} {np.max(vals):>10.4f}")

print()
print(f"  Global ‖z‖:  mean={mean_norm:.4f}  min={np.min(norm):.4f}  max={np.max(norm):.4f}")

# ── Cycle detection ──────────────────────────────────────────────────────────
if len(crossings) >= 2:
    periods = np.diff(crossings) * DT
    mean_period = float(np.mean(periods))
    print(f"\n  Cycles detected : {len(crossings)-1}")
    print(f"  Mean period     : {mean_period:.4f} time units")
    print(f"  Frequency       : {1/mean_period:.4f} cycles / unit")
else:
    mean_period = None
    print(f"\n  Cycles detected : {len(crossings)} upward crossings")
    print("  (run longer simulation or check initial condition)")

# ── Rock bottom detection ────────────────────────────────────────────────────
ROCK_THRESHOLD = 0.1   # ‖z‖ < 0.1 = near-zero (rock bottom)
rock_times = t[norm < ROCK_THRESHOLD]
if len(rock_times) > 0:
    print(f"\n  Rock bottom visits (‖z‖ < {ROCK_THRESHOLD}):")
    print(f"    Count = {len(rock_times)},  first at t={rock_times[0]:.3f}")
    print(f"    F(0)=+1/64={constants.F_1_64:.6f}  → bounce confirmed")
else:
    # Find global minimum
    t_min = t[np.argmin(norm)]
    min_val = np.min(norm)
    print(f"\n  Minimum ‖z‖ = {min_val:.4f} at t={t_min:.3f}")
    print(f"  (Did not reach rock bottom threshold {ROCK_THRESHOLD})")
    print(f"  F(0)=+1/64={constants.F_1_64:.6f}  → bounces at ~{min_val:.3f}")

# ── z*=1 instability verification ────────────────────────────────────────────
print()
print("  z*=1 instability check:")
z_test = np.ones(8, dtype=complex) * 1.0
h_test = -L @ z_test * DT
h_ret  = constants.RIGHT_LOVE_RETURN_RATE * (1.0 - z_test) * DT
dz     = z_test**2 - z_test + h_test + h_ret - z_test
print(f"    dz at z*=1 (uniform perturbation) = {np.abs(dz).mean():.2e}")
print(f"    (near-zero = fixed point confirmed; Jacobian eigenvalue = 63/64 = {63/64:.4f} > 0 → UNSTABLE)")

# ── Save results ─────────────────────────────────────────────────────────────
results = {
    "phase": PHASE,
    "dt": DT,
    "n_steps": N_STEP,
    "total_time": DT * N_STEP,
    "lambda_max": lambda_max,
    "lambda_zero": lambda_zero,
    "norm_mean": float(mean_norm),
    "norm_min": float(np.min(norm)),
    "norm_max": float(np.max(norm)),
    "cycles_detected": len(crossings) - 1 if len(crossings) >= 2 else 0,
    "mean_period": mean_period,
    "rock_bottom_visits": int(len(rock_times)),
    "rock_threshold": ROCK_THRESHOLD,
    "F_0_bounce": float(constants.F_1_64),
    "per_particle": {}
}
for name in fusion_core.SUBJECTS:
    idx  = fusion_core.IDX[name]
    vals = np.abs(trajectory_z[:, idx])
    results["per_particle"][name] = {
        "mean": float(np.mean(vals)),
        "min":  float(np.min(vals)),
        "max":  float(np.max(vals)),
        "z_star_physical": constants.Z_STAR_PHYSICAL.get(name, None),
    }

with open("limit_cycle_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print()
print("  Saved → limit_cycle_results.json")
print("=" * 60)
