import numpy as np
import h5py
import time
import os
import math

# ==============================================================================
# THE REWIND CLOCK CONSTANTS (The 443 Ma Transition)
# ==============================================================================
# Hardware Constants from the v6_conduit logs
TUNNEL_CONSTANT = 49.58841846
KAPPA_START = 710.328125         # The "Runaway" interference state (Now)
KAPPA_TARGET = 0.03125           # 1/32 Resonance (The Goal)

# Dimensional Branches
DIM_INDEX_SMALL_MAN = 1.618      # Phi (The 1D Fractal Branch)
DIM_INDEX_BIG_WOMAN = 1.5        # (The Volume/Metabolism Branch)
DIM_INDEX_BALANCE = 1.559        # The "Both D2" Midpoint (443 Ma)

# Unified Equation Constants
W_7 = math.pi / 20.0             # Barnard Reservoir
H_2 = 1.0 / 9.0                  # Sun Engine
SOVEREIGN_MARGIN = 1.9860        # The Justice Shield (hc)
SUBTRACTIVE_TENSION = 0.076      # The Slotting Operator

# ==============================================================================
# REWIND ENGINE LOGIC
# ==============================================================================

class RewindClockEngine:
    def __init__(self, n_particles=100000, total_steps=5000):
        self.n_particles = n_particles
        self.total_steps = total_steps
        self.dt = 0.01
        
        # Initial State: The "Runaway" Universe
        # Particles are dispersed and have high kappa-stress
        self.pos = np.random.normal(0, 10.0, (n_particles, 4))
        self.kappa = np.full((n_particles,), KAPPA_START)
        
        # Initial Velocities: Chaotic and Interference-prone
        v_raw = np.random.normal(0, 1, (n_particles, 4))
        v_norms = np.linalg.norm(v_raw, axis=1, keepdims=True)
        self.vel = (v_raw / v_norms) * 0.1 # Slow, heavy drift
        
        # Ledger
        self.history_kappa = np.zeros(total_steps)
        self.history_sovereignty = np.zeros(total_steps)

    def step(self, step_idx):
        """
        Rewinds the universal clock by collapsing the runaway kappa back to the 1.9860 margin.
        """
        progress = step_idx / self.total_steps
        
        # 1. The Dimensional Collapse (1.618 -> 1.559)
        # As we rewind, the Small Man branch realigns with the Big Woman branch.
        current_dim_idx = DIM_INDEX_SMALL_MAN - (DIM_INDEX_SMALL_MAN - DIM_INDEX_BALANCE) * progress
        
        # 2. The Kappa Decompression (710.3 -> 1/32)
        # We use the Tunnel Constant and Subtractive Tension to bleed off the interference.
        # Logic: Kappa decays exponentially as the "interference" is removed.
        self.kappa = self.kappa * np.exp(-0.002 * (TUNNEL_CONSTANT / SOVEREIGN_MARGIN))
        
        # Ensure we don't drop below the 1/32 Floor
        self.kappa = np.maximum(self.kappa, KAPPA_TARGET)
        
        # 3. Calculate the "Justice Score" (The Sovereign Check)
        # Omega = [Phi / (W7 + H2)] * (Kappa_Target / Kappa_Current)
        # In the rewind, the score starts very low (interference) and must reach 1.0.
        justice_score = (SOVEREIGN_MARGIN / (W_7 + H_2)) * (KAPPA_TARGET / np.mean(self.kappa))
        
        # 4. Position Contraction (The Inverse Expansion)
        # The universe "shrinks" back to the 443 Ma Jawed Fish state.
        contraction_factor = 1.0 - (progress * 0.9)
        self.pos *= contraction_factor
        
        # 5. Record
        self.history_kappa[step_idx] = np.mean(self.kappa)
        self.history_sovereignty[step_idx] = justice_score

    def run(self):
        print(f"--- INITIATING UNIVERSAL CLOCK REWIND (100,000 Nodes) ---")
        print(f"Current Kappa: {KAPPA_START:.4f} | Target: {KAPPA_TARGET:.4f}")
        print(f"Tunnel Constant: {TUNNEL_CONSTANT:.4f} | Margin: {SOVEREIGN_MARGIN:.4f}")
        
        start_time = time.time()
        for i in range(self.total_steps):
            self.step(i)
            if i % 500 == 0:
                k_val = self.history_kappa[i]
                j_score = self.history_sovereignty[i]
                status = "RESONATING" if j_score > 0.9 else "INTERFERENCE"
                print(f"Step {i:4d}/{self.total_steps} | Kappa: {k_val:8.4f} | Justice: {j_score:.6f} [{status}]")
        
        end_time = time.time()
        print(f"\n--- REWIND COMPLETE in {end_time - start_time:.2f} seconds ---")
        print(f"Final Kappa: {self.history_kappa[-1]:.6f}")
        print(f"Final Justice Score: {self.history_sovereignty[-1]:.6f}")

    def save_rewind_ledger(self, filename="out/REWIND_BOTH_D2_LEDGER.h5"):
        os.makedirs("out", exist_ok=True)
        print(f"Saving rewind data to {filename}...")
        with h5py.File(filename, 'w') as f:
            f.create_dataset("kappa_history", data=self.history_kappa)
            f.create_dataset("sovereignty_history", data=self.history_sovereignty)
            f.attrs["theory"] = "443 Ma Both D2 Rewind"
            f.attrs["kappa_start"] = KAPPA_START
            f.attrs["kappa_target"] = KAPPA_TARGET
            f.attrs["sovereign_margin"] = SOVEREIGN_MARGIN
        print("Rewind Ledger sealed.")

if __name__ == "__main__":
    engine = RewindClockEngine()
    engine.run()
    engine.save_rewind_ledger()
