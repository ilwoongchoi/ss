import numpy as np
import h5py
import time
import os
import math

# ==============================================================================
# THE PRIMORDIAL DUST REWIND CONSTANTS (4.0 Billion Years Ago)
# ==============================================================================
# The Archetypal Epoch Limits
EPOCH_START = "PRESENT (The 1/32 Hardware Lock)"
EPOCH_END = "4.0 Ga ARCHAEAN (The 3/32 GABA-A Rebirth / Lunar Dynamo)"

# The Particle States
CURRENT_KAPPA = 0.03125            # 1/32 (The Modern Hardware Sieve)
PRIMORDIAL_SYMMETRY = 0.09375      # 3/32 (The 10-11 o'clock Origin / CO-MAG Sphere)

# The Dissolution Metric
# As we rewind, the 1.9860 Sovereign Margin "melts" because there is no D3 yet.
# The 1/8 (Small Woman) and 1/128 (Small Man) dissolve into the 0D Dust.
W_7 = math.pi / 20.0             
H_2 = 1.0 / 9.0                  
CO_MAG_PULL = 1.414              # Lunar Dynamo Electromagnetic Dominance

# ==============================================================================
# GHOST DUST REWIND ENGINE LOGIC
# ==============================================================================

class GhostDustRewindEngine:
    def __init__(self, n_particles=50000, total_steps=5000):
        self.n_particles = n_particles
        self.total_steps = total_steps
        self.dt = 0.01
        
        # Initial State: The Modern Discrete Universe
        # Particles are highly structured, locked into the 1/32 Grid
        self.pos = np.random.normal(0, 1.0, (n_particles, 4))
        
        # In the modern era, velocity is tightly constrained by the 1/32 resonance
        v_raw = np.random.normal(0, 1, (n_particles, 4))
        v_norms = np.linalg.norm(v_raw, axis=1, keepdims=True)
        self.vel = (v_raw / v_norms) * CURRENT_KAPPA
        
        # The "Discrete Bond" (Starts at 1.0, melts to 0.0)
        self.structural_bond = np.ones(n_particles)
        
        # Ledger
        self.history_kappa = np.zeros(total_steps)
        self.history_bonds = np.zeros(total_steps)

    def step(self, step_idx):
        """
        Rewinds the universal clock to the 4.0 Ga Amino Acid Dust State.
        The discrete 1/8 and 1/128 particles dissolve into continuous 3/32 symmetry.
        """
        progress = step_idx / self.total_steps
        
        # 1. Rewinding the Kappa (1/32 -> 3/32)
        # We are moving backwards from the rigid 1/32 hardware to the fluid 3/32 origin.
        current_kappa = CURRENT_KAPPA + (PRIMORDIAL_SYMMETRY - CURRENT_KAPPA) * progress
        
        # 2. Melting the Structural Bonds (1.0 -> 0.0)
        # The 1.9860 Sovereign margin is relaxed. The PACT is dissolved.
        # The Small Woman and Small Man lose their discrete boundaries.
        melt_factor = math.exp(-5.0 * progress) # Rapid dissolution of the grid
        self.structural_bond = np.ones(self.n_particles) * melt_factor
        
        # 3. The Lunar Dynamo Override (CO-MAG)
        # As the modern grid melts, the Moon's primordial magnetic field takes over.
        # The trajectories lose their 4D Torsion and become spherical "Dust" floating.
        lunar_pull = CO_MAG_PULL * progress
        
        # 4. Trajectory Update (From Straight Line to Dust Cloud)
        # Velocity magnitude shifts to the 3/32 state, but direction becomes randomized (dust)
        v_norms = np.linalg.norm(self.vel, axis=1, keepdims=True)
        
        # Introduce "Dust Noise" proportional to the melting of the bonds
        dust_noise = np.random.normal(0, 0.05 * (1.0 - melt_factor), (self.n_particles, 4))
        self.vel = (self.vel / v_norms) * current_kappa + dust_noise
        
        # 5. Position Update (Floating in Midair)
        # The strict geometric expansion is reversed; particles "hover" in the CO-MAG womb
        self.pos += (self.vel * self.dt) * (1.0 - lunar_pull)
        
        # 6. Record
        self.history_kappa[step_idx] = current_kappa
        self.history_bonds[step_idx] = np.mean(self.structural_bond)

    def run(self):
        print(f"\n--- INITIATING PRIMORDIAL DUST REWIND ({self.n_particles} Nodes) ---")
        print(f"Target Era: {EPOCH_END}")
        print(f"Objective: Dissolve the 1/8 (Small Woman) & 1/128 (Small Man) into 3/32 Symmetry.")
        print(f"Hardware Lock: Disengaging...")
        
        start_time = time.time()
        for i in range(self.total_steps):
            self.step(i)
            if i % 500 == 0:
                k_val = self.history_kappa[i]
                bond_val = self.history_bonds[i]
                status = "GRID MELTING" if bond_val > 0.1 else "FLOATING DUST"
                print(f"Step {i:4d}/{self.total_steps} | Kappa State: {k_val:8.4f} | Grid Cohesion: {bond_val:.4f} [{status}]")
        
        end_time = time.time()
        print(f"\n--- REWIND COMPLETE in {end_time - start_time:.2f} seconds ---")
        print(f"Final Kappa State: {self.history_kappa[-1]:.6f} (The 3/32 Origin)")
        print(f"Final Grid Cohesion: {self.history_bonds[-1]:.6f} (The 0D Ghost State)")
        print("The two branches have successfully melted into the CO-MAG Sphere.")

    def save_dust_ledger(self, filename="out/PRIMORDIAL_DUST_LEDGER.h5"):
        os.makedirs("out", exist_ok=True)
        print(f"Saving Dust Ledger to {filename}...")
        with h5py.File(filename, 'w') as f:
            f.create_dataset("kappa_history", data=self.history_kappa)
            f.create_dataset("bond_history", data=self.history_bonds)
            f.attrs["theory"] = "4.0 Ga Amino Acid Dust Dissolution"
            f.attrs["kappa_start"] = CURRENT_KAPPA
            f.attrs["kappa_target"] = PRIMORDIAL_SYMMETRY
            f.attrs["co_mag_pull"] = CO_MAG_PULL
        print("Dust Ledger sealed. The Ghost is now floating in midair.")

if __name__ == "__main__":
    engine = GhostDustRewindEngine()
    engine.run()
    engine.save_dust_ledger()
