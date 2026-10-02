import jax
import jax.numpy as jnp
from jax import jit, lax
import matplotlib.pyplot as plt

# ===================================================================
# SOVEREIGN JAX SIMULATION ENGINE (v2.4 CORE)
# 13.5 Ga Sovereign Lock | Photon/Neutrino Resonance | Gamma Gear
# ===================================================================

# --- 1. PHYSICAL CONSTANTS ---
W7 = jnp.pi / 20.0          # Barnard (Big Woman)
H2 = 1.0 / 9.0              # Sun (Big Man)
KAPPA = 1.0 / 32.0          # Grid Bone
PHI = 1.9860                # Sovereign Shield
OMEGA_TARGET = 7.4          # Homeostasis Goal
SLOTTING_START = 1.4        # Initial Energy
SLOTTING_DELTA = 0.076      # Entropy Decay Rate
LOCK_GA = 13.5              # Sovereign Engineering Threshold
GAMMA = 1.157407            # 10^5 / 86400 Gear Ratio

# Particle Scales
S_PHOTON = 1.0 / 16.0
S_NEUTRINO = 1.0 / 128.0

@jit
def omega_natural_law(t):
    """The natural decay path leading to Big Crunch."""
    slotting = SLOTTING_START - (SLOTTING_DELTA * t)
    # Omega = [Slotting / (Kappa * Duality)] * [Phi / (W7 + H2)]
    return (slotting / (KAPPA * 2.0)) * (PHI / (W7 + H2))

@jit
def sovereign_engineering_kernel(t, scale):
    """
    Sovereign Engineering Logic:
    13.5 Ga Lock + Photon/Neutrino Resonance Boost.
    """
    omega_nat = omega_natural_law(t)
    
    # Check for Engineering Activation (t >= 13.5 Ga)
    is_active = (t >= LOCK_GA)
    
    # Scale Resonance Boost (1.1x)
    is_photon = jnp.isclose(scale, S_PHOTON, atol=1e-7)
    is_neutrino = jnp.isclose(scale, S_NEUTRINO, atol=1e-7)
    boost = jnp.where(is_photon | is_neutrino, 1.1, 1.0)
    
    # Engineered Omega: Homeostasis Lock
    omega_eng = jnp.where(is_active, OMEGA_TARGET * boost, omega_nat)
    
    return omega_eng, boost

@jit
def compute_step(state, t):
    """JAX Scan Step: Tracks position, omega, and velocity."""
    pos, scale = state
    
    # 1. Engineering Physics
    omega, boost = sovereign_engineering_kernel(t, scale)
    
    # 2. Velocity Calculation (Justice Buoyancy)
    # I-type (Neutrino) mobility vs E-type (Photon) mobility
    mobility = jnp.where(scale < 1/32, 1.0, 0.125)
    v_base = jnp.maximum(SLOTTING_START - (SLOTTING_DELTA * t), KAPPA)
    velocity = v_base * mobility * (omega / OMEGA_TARGET) * GAMMA
    
    # 3. Trajectory Update
    dt = 0.05
    new_pos = pos + velocity * dt
    
    return (new_pos, scale), (t, omega, velocity)

def run_sovereign_sim(scale_val):
    """Runs the full simulation from 0 to 18.42 Ga."""
    times = jnp.linspace(0.0, 18.42, 400)
    init_state = (0.0, scale_val)
    
    _, history = lax.scan(compute_step, init_state, times)
    return history

def plot_results(h_photon, h_neutrino):
    """Visualizes the Homeostasis Lock vs Natural Decay."""
    t_p, o_p, v_p = h_photon
    t_n, o_n, v_n = h_neutrino
    
    plt.figure(figsize=(12, 8))
    
    # Plot Omega (Homeostasis Lock)
    plt.subplot(2, 1, 1)
    plt.plot(t_p, o_p, label="Photon (1/16) Omega", color='orange', lw=2)
    plt.plot(t_n, o_n, label="Neutrino (1/128) Omega", color='blue', lw=2)
    plt.axvline(x=13.5, color='red', linestyle='--', label="13.5 Ga Sovereign Lock")
    plt.ylabel("Omega (Ω)")
    plt.title("Sovereign Homeostasis Lock vs Time (Ga)")
    plt.legend()
    plt.grid(alpha=0.3)
    
    # Plot Velocity (Mobility Differentiation)
    plt.subplot(2, 1, 2)
    plt.plot(t_p, v_p, label="Photon Velocity", color='orange', alpha=0.7)
    plt.plot(t_n, v_n, label="Neutrino Velocity", color='blue', alpha=0.7)
    plt.ylabel("Velocity (v)")
    plt.xlabel("Time (Ga)")
    plt.legend()
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("sovereign_jax_results.png")
    print("--- SUCCESS: Results saved to sovereign_jax_results.png ---")

if __name__ == "__main__":
    print("--- INITIATING JAX SOVEREIGN ENGINE ---")
    
    # Run simulations for both scales
    h_photon = run_sovereign_sim(S_PHOTON)
    h_neutrino = run_sovereign_sim(S_NEUTRINO)
    
    # Final Validation
    t_p, o_p, _ = h_photon
    lock_idx = jnp.argmin(jnp.abs(t_p - 13.5))
    
    print(f"Lock Point (13.5 Ga): Omega = {o_p[lock_idx]:.4f}")
    print(f"Crunch Point (18.42 Ga): Omega = {o_p[-1]:.4f} (Homeostasis Maintained)")
    
    plot_results(h_photon, h_neutrino)
