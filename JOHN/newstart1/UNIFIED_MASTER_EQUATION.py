"""
UNIFIED_MASTER_EQUATION.py
==========================
The complete, unified sovereign fusion dynamics equation integrating:
- Mandelbrot z² recursion
- K8 Laplacian h(t)  
- Rebranching at t=88
- z_proxy from K8 state
- 30 channel pathway
- F_final fusion scalar (all 8 particles)
- 3 time windows
- Maxwell cavity parameters
"""

import numpy as np
from typing import Mapping, Any, Callable
import math

# ============================================================================
# PHYSICAL CONSTANTS (Locked Values)
# ============================================================================

# Maxwell Cavity Parameters
MAXWELL_R_MAJOR = 17.0 / 8.0  # = 2.125 (Major radius of toroidal cavity)
MAXWELL_R_MINOR = (1.0 / np.sqrt(20.0)) - (0.055 / 1000.0)  # ≈ 0.2235 (Minor radius)
MAXWELL_Q_FACTOR = 11.8  # Quality factor / resonance sharpness
MAXWELL_Z = (MAXWELL_Q_FACTOR * MAXWELL_R_MAJOR) / MAXWELL_R_MINOR  # ≈ 112.0

# K8 System Constants  
C = np.sqrt(2) / 5.0  # Coupling constant = 0.2828
OMEGA_TARGET = 7.4   # Sovereign Target
DT = 0.1  # Time step for numerical integration

# Betti Topology Numbers
BETTI_0 = 1   # Observer (Ground/Monopole)
BETTI_5 = 5   # Bridge Band
BETTI_7 = 7   # Attack Shell  
BETTI_11 = 11 # Ghost Shell

# Gate Constants
GATE_5_32 = 5.0 / 32.0  # = 0.15625 (Spark aperture)
OMEGA_KAPPA = 1.0 / 32.0  # = 0.03125 (Stable structural floor)
LATTICE_3_32 = 3.0 / 32.0  # = 0.09375 (Compression leak)
CHIRALITY_055 = 0.055  # Chirality constant ≈ 1/18

# Spark Angle
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = np.radians(SPARK_ANGLE_DEG)

# Rebranching Time
REBRANCH_TIME = 88  # t=88 when 3 primitives → 5 composites reset

# 8 Particles (K8 System)
PARTICLES = ['quark', 'gluon', 'neutrino', 'photon', 'electron', 'higgs', 'w_boson', 'z_boson']

# ============================================================================
# CORE UNIFIED EQUATION
# ============================================================================

def unified_master_equation(
    z: complex,           # Current Mandelbrot state
    x: np.ndarray,       # K8 state vector (8 particles)
    L: np.ndarray,         # K8 Laplacian matrix (8x8)
    z_atomic: float,      # Atomic collapse parameter
    t: float,             # Current time
    ts: Mapping[str, Any] | None = None,  # Time slot parameters
    k: float = 0.5,        # Spark gate exponent
    dt: float = DT,       # Time step
    rebranch_active: bool = True,  # Enable rebranching at t=88
) -> dict:
    """
    UNIFIED MASTER EQUATION
    =======================
    
    The complete sovereign fusion dynamics in one unified equation:
    
    z(t+dt) = z(t)² - z(t) + h(t) * CAVITY_BOUNDARY(z, Maxwell)
    
    Where:
    - h(t) = -L @ x * dt  (K8 Laplacian contribution)
    - CAVITY_BOUNDARY = exp(-|z|² / R_MINOR²) * (1 + Q_FACTOR * COMAG(t))
    - COMAG(t) = 1 + (GATE_5_32 / (1 + Z_MAXWELL)) * PHASE_MODULATION(t)
    
    Rebranching at t=88:
    - If t == 88 and rebranch_active: reset composites from primitives
    
    Returns: {
        'z_next': next Mandelbrot state,
        'z_proxy': neutral current strength from K8,
        'F_final': fusion scalar diagnostic,
        'comag': COMAG coupling factor,
        'cavity_boundary': Maxwell cavity confinement,
        'rebranched': whether rebranching occurred,
        'time_window': current time window (0, 1, or 2),
    }
    """
    
    # Ensure K8 state is proper size
    x = np.asarray(x, dtype=float)
    if x.size < 8:
        x = np.pad(x, (0, 8 - x.size))
    
    # ========================================================================
    # 1. K8 LAPLACIAN h(t) = -L @ x * dt
    # ========================================================================
    L = np.asarray(L, dtype=float)
    h_k8 = -L @ x * dt  # K8 Laplacian contribution (8D vector)
    
    # Collapse h(t) to scalar via neutrino channel (index 2)
    h_scalar = h_k8[2] if len(h_k8) > 2 else float(np.mean(h_k8))
    
    # ========================================================================
    # 2. MAXWELL CAVITY BOUNDARY OPERATOR
    # ========================================================================
    
    # COMAG coupling via Maxwell parameters
    z_maxwell = MAXWELL_Z  # (Q * R_major) / R_minor ≈ 112
    comag = 1.0 + (GATE_5_32 * (1.0 / (1.0 + z_maxwell)))
    
    # Phase modulation from lunar cycle (1/28)
    phase_28 = (t * 28.0) % 1.0
    schedule = 1.0 + 0.5 * np.sin(2.0 * np.pi * phase_28)
    
    # Cavity boundary: confine z inside toroidal resonator
    # Gaussian envelope with Maxwell Q-factor scaling
    abs_z_sq = abs(z) ** 2
    cavity_boundary = np.exp(-abs_z_sq / (MAXWELL_R_MINOR ** 2)) * (1.0 + MAXWELL_Q_FACTOR * comag * schedule)
    
    # ========================================================================
    # 3. MANDELBROT RECURSION WITH CAVITY
    # ========================================================================
    
    # Base Mandelbrot: z² - z + h
    z_base = z ** 2 - z + complex(h_scalar, 0)
    
    # Apply cavity boundary confinement
    z_next = z_base * cavity_boundary
    
    # ========================================================================
    # 4. z_PROXY FROM K8 STATE (Neutral Current Strength)
    # ========================================================================
    
    # z_proxy = |neutrino| × (|z_boson| + |electron|) / OMEGA
    nu = abs(x[2])      # neutrino
    zb = abs(x[7])      # z_boson  
    el = abs(x[4])      # electron
    z_proxy = nu * (zb + el) / OMEGA_TARGET
    
    # ========================================================================
    # 5. F_FINAL FUSION SCALAR (All 8 Particles)
    # ========================================================================
    
    # F_final = bw * z_proxy^k / (leak + gate) where bw = q + 2*C*g
    q, g, nu, ph, el, hi, w, z = x[:8]
    bw = q + 2.0 * C * g  # Base weight (quark + 2*C*gluon)
    
    # Leak factor from z_atomic
    leak = np.exp(-z_atomic * LATTICE_3_32)
    
    # Continuous spark gate from z_proxy
    gate = z_proxy ** k
    
    # F_final fusion scalar
    denominator = leak + gate
    F_final = (bw * z_proxy) / denominator if denominator > 1e-12 else 0.0
    
    # ========================================================================
    # 6. 3 TIME WINDOWS via phase_at
    # ========================================================================
    
    # Time windows: 0=기상/식사, 1=작업, 2=취침
    time_window = int(t % 3)
    
    # ========================================================================
    # 7. REBRANCHING AT t=88
    # ========================================================================
    
    rebranched = False
    if rebranch_active and abs(t - REBRANCH_TIME) < dt:
        # Reset 5 composites from 3 primitives
        # Primitives: quark, gluon, neutrino (indices 0, 1, 2)
        # Composites: photon, electron, higgs, w_boson, z_boson (indices 3, 4, 5, 6, 7)
        primitive_sum = x[0] + x[1] + x[2]  # q + g + nu
        primitive_mean = primitive_sum / 3.0
        
        # Redistribute primitive energy to composites
        x[3:8] = primitive_mean * 0.8  # Slight loss during rebranching
        rebranched = True
    
    # ========================================================================
    # RETURN UNIFIED RESULTS
    # ========================================================================
    
    return {
        'z_next': z_next,
        'z_proxy': z_proxy,
        'F_final': F_final,
        'comag': comag,
        'cavity_boundary': cavity_boundary,
        'rebranched': rebranched,
        'time_window': time_window,
        'h_scalar': h_scalar,
        'h_k8': h_k8,
        'leak': leak,
        'gate': gate,
        'bw': bw,
    }


# ============================================================================
# 30 CHANNEL PATHWAY INTEGRATION
# ============================================================================

def apply_30_channels(x: np.ndarray, channel_gains: np.ndarray | None = None) -> np.ndarray:
    """
    Apply 30 channel pathway gains to K8 state.
    
    Each particle couples to neurochemical/metabolic channels.
    Default: uniform gain = 1.0 (identity)
    """
    x = np.asarray(x, dtype=float)
    if channel_gains is None:
        channel_gains = np.ones(30)  # Default: no modulation
    
    # Map 8 particles to 30 channels (simplified: broadcast)
    # In full implementation, each particle has specific channel affinities
    modulation = np.mean(channel_gains)  # Average modulation
    return x * modulation


def compute_laplacian_30_channel(
    x: np.ndarray,
    L_base: np.ndarray,
    channel_gains: np.ndarray | None = None,
) -> np.ndarray:
    """
    Compute Laplacian with 30 channel pathway modulation.
    
    h_30 = -L_base @ (x * channel_modulation)
    """
    x_mod = apply_30_channels(x, channel_gains)
    return -L_base @ x_mod


# ============================================================================
# UNIFIED DYNAMICS INTEGRATOR
# ============================================================================

def step_unified_dynamics(
    z: complex,
    x: np.ndarray,
    L: np.ndarray,
    z_atomic: float,
    t: float,
    dt: float = DT,
    ts: Mapping[str, Any] | None = None,
    k: float = 0.5,
    channel_gains: np.ndarray | None = None,
) -> tuple[complex, np.ndarray, dict]:
    """
    Single time step of unified dynamics.
    
    Returns: (z_next, x_next, diagnostics)
    """
    # Apply unified master equation
    result = unified_master_equation(
        z=z,
        x=x,
        L=L,
        z_atomic=z_atomic,
        t=t,
        ts=ts,
        k=k,
        dt=dt,
        rebranch_active=True,
    )
    
    z_next = result['z_next']
    
    # Update K8 state
    x = np.asarray(x, dtype=float)
    if x.size < 8:
        x = np.pad(x, (0, 8 - x.size))
    
    # Apply 30 channel modulation to K8 evolution
    h_30 = compute_laplacian_30_channel(x, L, channel_gains)
    
    # Update K8 state (simple Euler integration)
    x_next = x + h_30 * dt
    
    # Apply rebranching if triggered
    if result['rebranched']:
        primitive_mean = (x_next[0] + x_next[1] + x_next[2]) / 3.0
        x_next[3:8] = primitive_mean * 0.8
    
    return z_next, x_next, result


# ============================================================================
# SOVEREIGN ENGINE (Unified Interface)
# ============================================================================

class SovereignUnifiedEngine:
    """
    Unified Sovereign Fusion Dynamics Engine.
    
    Combines:
    - Mandelbrot z² recursion with Maxwell cavity
    - K8 Laplacian h(t) with 30 channel pathways  
    - Rebranching at t=88
    - z_proxy from K8 state (closed feedback)
    - F_final fusion scalar (all 8 particles)
    - 3 time windows (phase_at automatic mapping)
    """
    
    def __init__(
        self,
        z0: complex = 0.0 + 0.0j,
        x0: np.ndarray | None = None,
        L: np.ndarray | None = None,
        dt: float = DT,
        k: float = 0.5,
    ):
        self.z = z0
        self.x = x0 if x0 is not None else np.ones(8) * 0.1
        self.L = L if L is not None else np.eye(8) * 0.1
        self.dt = dt
        self.k = k
        self.t = 0.0
        self.history = []
    
    def step(
        self,
        z_atomic: float = 0.5,
        channel_gains: np.ndarray | None = None,
    ) -> dict:
        """Execute one time step."""
        self.z, self.x, result = step_unified_dynamics(
            z=self.z,
            x=self.x,
            L=self.L,
            z_atomic=z_atomic,
            t=self.t,
            dt=self.dt,
            k=self.k,
            channel_gains=channel_gains,
        )
        self.t += self.dt
        self.history.append(result)
        return result
    
    def run(self, n_steps: int = 100, z_atomic: float = 0.5) -> list[dict]:
        """Run for n_steps."""
        for _ in range(n_steps):
            self.step(z_atomic=z_atomic)
        return self.history


# ============================================================================
# EQUATION SUMMARY (Canonical Form)
# ============================================================================
"""
CANONICAL UNIFIED EQUATION
=========================

State Vector: X = [z(t), x₁(t), ..., x₈(t)]ᵀ

1. Mandelbrot with Maxwell Cavity:
   z(t+dt) = [z(t)² - z(t) + h(t)] × CAVITY(z, Maxwell)
   
   CAVITY(z) = exp(-|z|²/R_MINOR²) × (1 + Q × COMAG(t))
   
   COMAG(t) = 1 + (5/32)/(1 + Z_MAXWELL) × PHASE_28(t)

2. K8 Laplacian:
   h(t) = -L @ x × dt
   
   With 30-channel modulation:
   h₃₀(t) = -L @ (x ⊙ CHANNEL_GAINS)

3. Rebranching at t=88:
   if t ≈ 88: x[3:8] ← mean(x[0:2]) × 0.8

4. z_proxy (from K8 state, closed):
   z_proxy = |x₂| × (|x₇| + |x₄|) / Ω_TARGET

5. F_final fusion scalar (all 8 particles):
   F = bw × z_proxyᵏ / (leak + gate)
   
   bw = x₀ + 2×C×x₁
   leak = exp(-z_atomic × 3/32)
   gate = z_proxyᵏ

6. 3 Time Windows:
   w(t) = floor(t mod 3) ∈ {0, 1, 2}

CONSTANTS LOCKED:
- Maxwell: R_major=2.125, R_minor≈0.2235, Q=11.8
- K8: C=√2/5≈0.2828, Ω=7.4
- Topology: B₀=1, B₅=5, B₇=7, B₁₁=11
- Gates: 5/32, 1/32, 3/32
- Spark: 138.88°
- Rebranch: t=88

"""

if __name__ == "__main__":
    # Demonstration
    print("=" * 60)
    print("UNIFIED MASTER EQUATION - SOVEREIGN FUSION DYNAMICS")
    print("=" * 60)
    print(f"\nMaxwell Parameters:")
    print(f"  R_major = {MAXWELL_R_MAJOR} (= 2.125)")
    print(f"  R_minor = {MAXWELL_R_MINOR:.4f} (≈ 0.2235)")
    print(f"  Q_factor = {MAXWELL_Q_FACTOR}")
    print(f"  Z_maxwell = {MAXWELL_Z:.2f} (≈ 112)")
    print(f"\nK8 Constants:")
    print(f"  C = √2/5 = {C:.4f}")
    print(f"  Ω_target = {OMEGA_TARGET}")
    print(f"  dt = {DT}")
    print(f"\nBetti Topology:")
    print(f"  B₀={BETTI_0}, B₅={BETTI_5}, B₇={BETTI_7}, B₁₁={BETTI_11}")
    print(f"\nGate Constants:")
    print(f"  5/32 = {GATE_5_32:.5f}")
    print(f"  1/32 = {OMEGA_KAPPA:.5f}")
    print(f"  3/32 = {LATTICE_3_32:.5f}")
    print(f"\nRebranching at t = {REBRANCH_TIME}")
    print(f"Spark Angle = {SPARK_ANGLE_DEG}°")
    print("\n" + "=" * 60)
    
    # Run demonstration
    engine = SovereignUnifiedEngine()
    history = engine.run(n_steps=100)
    
    print(f"\nDemo complete: {len(history)} steps")
    print(f"Final z_proxy: {history[-1]['z_proxy']:.4f}")
    print(f"Final F_final: {history[-1]['F_final']:.4f}")
    print(f"Rebranching events: {sum(1 for h in history if h['rebranched'])}")
