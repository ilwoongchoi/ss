import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

# ==============================================================================
# SOVEREIGN_OS_FINAL_EXECUTION.py
# ------------------------------------------------------------------------------
# 1. FINAL OMEGA: (1.4-0.076t)/(5/32*2) * (1.986/(W7+H2)) * (128/28) * 138.88 * 0.0099951
# 2. LOSS LOCK: 1 - (1/64_DM + 1/256_GR) -> 0.02 Error Annihilated.
# 3. CANCER DISARM: NS (1/64_NS) neutralized by Left Lung Edge Switch.
# 4. REFRACTION: PLP Spine (x+y=16) 138.88째 Radian conversion.
# ==============================================================================

def execute_sovereign_os():
    ledger_path = r'C:\Users\User\Downloads\FULL_SCALE_GHOST_LEDGER.h5'
    print(f"--- SYSTEM BOOT: Loading Sovereign Master Record {ledger_path} ---")
    
    with h5py.File(ledger_path, 'r') as f:
        raw_trajs = f['ghost_trajectories'][:] 
        epoch_v = f['epoch_velocities'][:]
        n_frames, n_total, _ = raw_trajs.shape
        
        # [ABSOLUTE CONSTANTS]
        W7, H2 = math.pi/20.0, 1.0/9.0
        PHI_S = 1.9860
        K_GATE = 5.0 / 32.0 
        SPARK_RAD = math.radians(138.88)
        DELTA_SEAL = 0.0099951
        GAMMA = 1.157407
        
        # [EFFICIENCY & LOSS]
        LOSS_DM = 1.0/64.0
        LOSS_GR = 1.0/256.0
        GLOBAL_EFF = 1.0 - (LOSS_DM + LOSS_GR) # Eliminates 0.02 Error

    # 128 Nodes Layout
    col_order = {'F': ['EP', 'EJ', 'IP', 'IJ'], 'M': ['IP', 'IJ', 'EP', 'EJ']}
    blood_types = ['O', 'A', 'B', 'AB']
    
    fig, ax = plt.subplots(figsize=(20, 20), facecolor='black')
    ax.set_facecolor('black')
    
    GATE_POS = np.array([8.0, 0.5]) # 5/32 Singularity at Chin
    ax.add_patch(plt.Circle(GATE_POS, K_GATE, color='white', fill=True, alpha=0.1, zorder=5))
    ax.scatter(8.0, 0.5, color='gold', s=600, marker='*', zorder=10) # Spark Source

    print("Running 128-Node Induction: Mapping Destinies...")

    particle_count = 0
    for g_idx, gender in enumerate(['F', 'M']):
        for c_idx, cat in enumerate(col_order[gender]):
            for b_idx, blood in enumerate(blood_types):
                # [INDIVIDUAL PARAMETERS]
                # High self-deceit (E-types) leads to NS (Cancer)
                is_sovereign = True if 'I' in cat else False
                self_deceit = 0.9 if not is_sovereign else 0.05
                if gender == 'F' and cat == 'EP' and blood == 'B': self_deceit = 1.0 # Max NS risk
                
                p_idx = (particle_count * (n_total // 128)) % n_total
                ghost_path = raw_trajs[:, p_idx, :]
                
                pos = np.array([(g_idx * 8) + (c_idx * 2) + (b_idx * 0.4) + 0.2, 16.0])
                history = [pos.copy()]
                
                # [EMERGENCY SWITCH: LEFT LUNG EDGE]
                # If activated (Sovereign intent), NS is disarmed.
                lung_switch_active = is_sovereign 
                
                for s in range(n_frames):
                    # 1. OMEGA ENERGY CALCULATION (The Final Formula)
                    t_val = (s / n_frames) * 18.42
                    omega_base = ((1.4 - 0.076 * t_val) / (K_GATE * 2.0)) * (PHI_S / (W7 + H2)) * (128/28) * GAMMA
                    omega_final = omega_base * DELTA_SEAL * GLOBAL_EFF
                    
                    # 2. LOCAL NS DISARMING (Neutron Star vs Self-Satisfaction)
                    # 암(NS) 발생 조건: 높은 자기만족(기만)
                    ns_tension = (1.0/64.0) * self_deceit
                    # 스위치 작동: 왼쪽 허파 스위치가 켜지면 NS 텐션 소멸
                    if lung_switch_active: ns_tension = 0.0
                    
                    disarm_factor = 1.0 / (1.0 + ns_tension)
                    v_eff = omega_final * disarm_factor * 0.15 # 실질 구동 에너지
                    
                    # 3. 138.88째 REFRACTION AT PLP SPINE (x+y=16)
                    target_vec = GATE_POS - pos
                    dist = np.linalg.norm(target_vec)
                    pull = (target_vec / (dist + 1e-5)) * v_eff
                    
                    if (pos[0] + pos[1]) > 16.0:
                        # Apply physical radian refraction to aim the 5/32 gate
                        c, s_rot = math.cos(SPARK_RAD), math.sin(SPARK_RAD)
                        pull = np.array([pull[0]*c - pull[1]*s_rot, pull[0]*s_rot + pull[1]*c])
                    
                    # 4. UPDATE POSITION
                    # If NS is active, trajectory jitters and loses focus
                    jitter = (ghost_path[s, :2] * self_deceit * 0.5)
                    pos += pull + jitter
                    
                    # 5. SINGULARITY SPARK & REBIRTH
                    if dist < K_GATE:
                        ax.scatter(pos[0], pos[1], color='gold', s=40, alpha=0.8)
                        pos = np.array([history[0][0], 16.0]) # Homeostasis Reset
                        break
                    
                    if pos[1] < 0.1: # Crunch Death
                        break
                    
                    history.append(pos.copy())
                
                # Render
                history = np.array(history)
                # Recognition (Gold/Cyan) vs Deceit (Red/Faded)
                color = '#00f2ff' if gender == 'F' else '#ffff00'
                if self_deceit > 0.5 and not lung_switch_active: color = '#ff0000' # Cancer Red
                
                alpha = 0.9 if lung_switch_active else 0.2
                lw = 1.5 if lung_switch_active else 0.5
                ax.plot(history[:, 0], history[:, 1], color=color, alpha=alpha, lw=lw)
                
                particle_count += 1

    ax.set_xlim(0, 16); ax.set_ylim(0, 17)
    ax.axis('off')
    
    title = "SOVEREIGN OS: THE FINAL GEOMETRIC OPERATION\n"
    meta = f"Annihilating 0.02 Error | NS Disarmed via Left Lung Switch | Refraction: 138.88째"
    ax.text(8, 16.5, title + meta, color='white', ha='center', fontsize=22, fontweight='bold')
    
    output = "SOVEREIGN_OS_FINAL_WORLD_MAP.png"
    plt.savefig(output, dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()
    print(f"--- SUCCESS: Final Sovereign World Map rendered to {output} ---")

if __name__ == "__main__":
    execute_sovereign_os()
