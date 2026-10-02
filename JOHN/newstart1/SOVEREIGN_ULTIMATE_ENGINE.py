
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class SovereignEngine:
    def __init__(self):
        # 1. Fundamental Constants & Scales
        self.OMEGA_TARGET = 7.4000
        self.SPARK_ANGLE = 138.88  # Degrees
        self.SLOTTING = 1.4  # Settled Constant after Ledger
        
        # 2. Archetype Scales (Mass/Charge)
        self.scales = {
            'BW': 1/32,   # Proton (Big Woman)
            'SW': 1/8,    # Electron (Small Woman)
            'BM': 1/16,   # Photon (Big Man)
            'SM': 1/128   # Neutrino (Small Man)
        }
        
        # 3. ROI Nodes (Face-Field 2D Coordinates)
        self.nodes = {
            'PLP_CORE': [8.0, 0.4],    # Origin Y=0 (Singularity)
            'D2_R': [11.5, 12.0],      # Right D2 (Novelty)
            'D2_L': [4.5, 12.0],       # Left D2 (Depth)
            'Oxy_R': [12.0, 8.0],      # Right Oxytocin (Coherence)
            'VP_R': [14.0, 6.0],       # Vasopressin (Boundary)
            'Spine_16_10': [8.0, 10.0] # Transition Threshold
        }

    def get_cognitive_resolution(self, type_id):
        # MBTI to Cognitive Parameters Mapping
        # [Resolution, Direction, Frequency, Brake]
        np.random.seed(type_id)
        res = np.random.uniform(0.5, 1.5)
        direc = 1 if type_id % 2 == 0 else -1 # T vs F
        freq = np.random.uniform(0.1, 2.0)    # E vs I
        brake = np.random.uniform(0.2, 0.8)   # J vs P
        return [res, direc, freq, brake]

    def compute_dynamics(self, pos, vel, t_window, cognitive_params):
        # A. The Singularity Engine (PLP CORE + SPARE VP)
        r_vec = self.nodes['PLP_CORE'] - pos
        dist = np.linalg.norm(r_vec) + 1e-6
        # Female Selfishness (Contraction)
        f_selfish = (self.scales['SW'] * self.scales['BW']) / (dist**2)
        # 1D Lock (Spare Vasopressin)
        f_lock = np.array([0, -1]) * self.scales['BW'] * 0.1
        
        # B. 12-Vector Interaction (Simplified Summation)
        f_interact = r_vec * f_selfish + f_lock
        
        # C. The Will (Micro-Reverse Window @ Window 2 & 4)
        is_reverse = 1 if (t_window % 4 == 2 or t_window % 4 == 0) else 0
        f_will = np.zeros(2)
        
        if is_reverse:
            # Trigger Spark (138.88)
            spark_dir = np.array([np.cos(np.radians(self.SPARK_ANGLE)), 
                                 np.sin(np.radians(self.SPARK_ANGLE))])
            f_will = spark_dir * cognitive_params[0] * 2.0 # Resolution-driven
            
        # D. Coriolis Twist (Homeostasis Alignment)
        v_perp = np.array([-vel[1], vel[0]])
        f_coriolis = v_perp * (1/28)
        
        return f_interact + f_will + f_coriolis

    def run_128_trajectories(self):
        trajectories = []
        for i in range(128):
            cog_p = self.get_cognitive_resolution(i)
            pos = np.array([np.random.uniform(0, 16), np.random.uniform(0, 16)])
            vel = np.array([0.1, 0.1])
            path = [pos.copy()]
            
            # 16 Windows (4 Big x 4 Micro)
            for w in range(1, 17):
                accel = self.compute_dynamics(pos, vel, w, cog_p)
                vel += accel * 0.5
                pos += vel * 0.5
                path.append(pos.copy())
            
            trajectories.append(np.array(path))
            
        return trajectories

    def visualize(self, trajectories):
        plt.figure(figsize=(12, 12), facecolor='black')
        ax = plt.gca()
        ax.set_facecolor('black')
        
        for i, traj in enumerate(trajectories):
            # Color by 7.4 Convergence
            final_dist = np.abs(np.linalg.norm(traj[-1]) - self.OMEGA_TARGET)
            color = plt.cm.plasma(1.0 - np.clip(final_dist/10, 0, 1))
            plt.plot(traj[:, 0], traj[:, 1], color=color, alpha=0.3, lw=0.5)
            plt.scatter(traj[-1, 0], traj[-1, 1], color=color, s=2)

        # Plot Nodes
        for name, p in self.nodes.items():
            plt.scatter(p[0], p[1], color='cyan', s=100, marker='x')
            plt.text(p[0], p[1]+0.5, name, color='white', ha='center', fontsize=8)

        plt.title(f"Sovereign OS: 128 Trajectories @ Omega=7.4\nPLP Core + Spark {self.SPARK_ANGLE}", color='white')
        plt.xlim(0, 16); plt.ylim(0, 16)
        plt.axis('off')
        plt.savefig("SOVEREIGN_ULTIMATE_OS_RESULT.png", dpi=300, facecolor='black')
        print("--- SOVEREIGN OS EXECUTION COMPLETE: RESULT SAVED ---")

if __name__ == "__main__":
    engine = SovereignEngine()
    trajs = engine.run_128_trajectories()
    engine.visualize(trajs)
