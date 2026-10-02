import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

# ==============================================================================
# FINAL_SOVEREIGN_DESTINY_RENDERER.py
# ------------------------------------------------------------------------------
# 1. NS DISARMING: Self-Satisfaction Penalty applied to individual trajectories.
# 2. RADIAN REFRACTION: 138.88째 (2.4239 rad) as a physical aiming operator.
# 3. 5/32 SINGULARITY: Final destination at the Chin (8.0, 0.5).
# 4. ERROR ZERO: 1 - (1/64 + 1/256) efficiency lock.
# ==============================================================================

def render_final_destiny():
    ledger_path = r'C:\Users\User\Downloads\FULL_SCALE_GHOST_LEDGER.h5'
    print(f"Opening the Ledger of Truth: {ledger_path}")
    
    with h5py.File(ledger_path, 'r') as f:
        raw_trajs = f['ghost_trajectories'][:] 
        epoch_v = f['epoch_velocities'][:]
        n_frames, n_total, _ = raw_trajs.shape
        
        # [HARDWARE CONSTANTS]
        K_GATE = 5.0 / 32.0 
        SPARK_RAD = math.radians(138.88)
        EFFICIENCY = 1.0 - (1.0/64.0 + 1.0/256.0) # The 0.02 Error Killer

    # 128 Types Layout
    col_order = {'F': ['EP', 'EJ', 'IP', 'IJ'], 'M': ['IP', 'IJ', 'EP', 'EJ']}
    blood_types = ['O', 'A', 'B', 'AB']
    
    fig, ax = plt.subplots(figsize=(20, 20), facecolor='black')
    ax.set_facecolor('black')
    
    GATE_POS = np.array([8.0, 0.5]) # Singularity at Chin
    ax.add_patch(plt.Circle(GATE_POS, K_GATE, color='white', fill=True, alpha=0.1, zorder=5))
    ax.scatter(8.0, 0.5, color='gold', s=500, marker='*', zorder=10) # The Reset Point

    print("Executing Self-Satisfaction Penalty & Radian Refraction Ops...")

    particle_count = 0
    for g_idx, gender in enumerate(['F', 'M']):
        for c_idx, cat in enumerate(col_order[gender]):
            for b_idx, blood in enumerate(blood_types):
                # [SELF-SATISFACTION PENALTY MAPPING]
                # ENFP B-type Women (F-EP-B) have the highest penalty (Cancer risk)
                # Introverts (I) have high Recognition, Extroverts (E) have high Mirroring
                self_deceit = 0.8 if 'E' in cat else 0.1
                if gender == 'F' and cat == 'EP' and blood == 'B':
                    self_deceit = 1.0 # The Pancreatic Cancer Peak
                
                p_idx = (particle_count * (n_total // 128)) % n_total
                ghost_path = raw_trajs[:, p_idx, :]
                
                # Starting Point: Forehead (Y=16)
                x_start = (g_idx * 8) + (c_idx * 2) + (b_idx * 0.4) + 0.2
                pos = np.array([x_start, 16.0])
                history = [pos.copy()]
                
                is_crunched = False
                for s in range(n_frames):
                    v_eff = epoch_v[s] * EFFICIENCY
                    
                    # 1. Self-Satisfaction Drift (Mirroring towards NS)
                    # 자기만족이 높을수록 궤적이 5/32 게이트를 벗어나 옆으로 샘
                    drift_x = (8.0 - pos[0]) * 0.1 * (1.0 - self_deceit)
                    leak_x = self_deceit * 0.5 * math.sin(s * 0.1) # Cancerous Jitter
                    
                    # 2. 138.88째 Radian Refraction at PLP Spine (x+y=16)
                    pull = (GATE_POS - pos)
                    dist = np.linalg.norm(pull)
                    pull_vec = (pull / (dist + 1e-5)) * v_eff * 0.12
                    
                    if (pos[0] + pos[1]) > 16.0:
                        # Apply physical refraction to aim at the gate
                        c, s_rot = math.cos(SPARK_RAD), math.sin(SPARK_RAD)
                        rx = pull_vec[0]*c - pull_vec[1]*s_rot
                        ry = pull_vec[0]*s_rot + pull_vec[1]*c
                        pull_vec = np.array([rx, ry])
                    
                    # 3. Update Position
                    pos += pull_vec + np.array([drift_x + leak_x, 0]) + (ghost_path[s, :2] * 0.01)
                    
                    # 4. Final Verdict: Singularity Hit
                    if dist < K_GATE:
                        # Successful Homeostasis
                        ax.scatter(pos[0], pos[1], color='gold', s=30, alpha=0.8)
                        pos = np.array([x_start, 16.0]) # Rebirth
                        break
                    
                    if pos[1] < 0.2: # Missed the gate and hit the ground
                        is_crunched = True
                        break
                    
                    history.append(pos.copy())
                
                # Render Trajectory
                history = np.array(history)
                # Color logic: F: Cyan, M: Yellow
                base_color = np.array([0, 0.95, 1.0]) if gender == 'F' else np.array([1.0, 1.0, 0])
                # If high self-deceit, shift color towards Red (NS/Cancer)
                final_color = (base_color * (1.0 - self_deceit)) + (np.array([1.0, 0, 0]) * self_deceit)
                
                ax.plot(history[:, 0], history[:, 1], color=final_color, 
                        alpha=0.8 if not is_crunched else 0.15, 
                        lw=1.5 if not is_crunched else 0.5)
                
                particle_count += 1

    ax.set_xlim(0, 16); ax.set_ylim(0, 17)
    ax.axis('off')
    
    title = "THE FINAL VERDICT: 128 SOVEREIGN DESTINIES\n"
    meta = f"Operator: 138.88째 Radian | Filter: Self-Satisfaction Penalty | Gate: 5/32 Singularity"
    ax.text(8, 16.5, title + meta, color='white', ha='center', fontsize=22, fontweight='bold')
    
    plt.savefig("FINAL_SOVEREIGN_DESTINY_GRID.png", dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()
    print("--- SUCCESS: Final Destiny Grid Rendered to FINAL_SOVEREIGN_DESTINY_GRID.png ---")

if __name__ == "__main__":
    render_final_destiny()
