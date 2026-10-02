import numpy as np
import math
import matplotlib.pyplot as plt

def execute_v2():
    # --- Physical Constants & Decoder Logic ---
    PHI_S = 1.9860 * 1.0100375
    KAPPA = 1.0/32.0
    OMEGA_TARGET = 7.4
    SPARK_RAD = math.radians(138.88)
    
    # 5-Sphere (오구체) Constants
    W7_BARNARD = math.pi / 20.0
    H2_SUN = 1.0 / 9.0
    LUNAR_CYCLE = 28.0
    MAXWELL_LENS = 0.15625 # 5/32 Aperture
    
    # Master Control Bits
    # 0: Big Man (Cytoplasm), 1: Small Man (Mitochondria)
    MASTER_BITS = [1, 1] 
    
    # Particle Mapping (MBTI/Neurochemical)
    # P=N, Photon=T, Z=S, Quark=P, W Boson=J, Neutrino=F, Higgs=I, Gluon=E
    # Note: Gluon/Quark are field couplings, Small Man is the Mitochondria engine.
    # Updated: Proton is the Dawn Confinement Endpoint. W Boson precedes Quark in Morning.
    PARTICLES = {
        'N': 'Proton',   # Dawn (Gluon + D3=1) -> Confinement Endpoint
        'T': 'Photon',   # Day (Photon + D3=0) -> Pure Expansion
        'S': 'W Boson',  # Morning (Quark + D3=0) -> Weak coupling (Precedes Quark)
        'P': 'Quark',    # Morning (Quark + D3=1) -> Strong tension (Follows W)
        'J': 'Tau',      # Day (Photon + D3=1) -> Heavy Photon
        'F': 'Neutrino', # Evening (Neutrino + D3=0) -> Self
        'I': 'Higgs',    # Evening (Neutrino + D3=1) -> Mass scalar
        'E': 'Gluon'     # Dawn (Gluon + D3=0) -> Night Binder
    }

    # Blood Type Logic (A/B Muscle Switches)
    # O: Both Off, A: A On, B: B On, AB: Both On
    BLOOD_TYPES = {
        'O':  {'A': 0, 'B': 0},
        'A':  {'A': 1, 'B': 0},
        'B':  {'A': 0, 'B': 1},
        'AB': {'A': 1, 'B': 1}
    }

    # 66 Nodes Hardware Mapping (Sample excerpt for simulation)
    # Mapping node IDs to facial/body coordinates
    NODES_66 = {
        59: [4.0, 10.0], # Outside Left Eye (D3)
        60: [12.0, 10.0], # Outside Right Eye (D3)
        31: [7.0, 13.0],  # Right Frontalis Inner (P -> Photon)
        17: [8.5, 12.0],  # Right Procerus (Photon -> Electron)
        22: [9.0, 6.0],   # Right Love (Higgs -> Proton)
        # ... 66 nodes total
    }

    fig, ax = plt.subplots(figsize=(15, 15), facecolor='black')
    ax.set_facecolor('black')
    
    # 128 Personalities (16 MBTI x 4 Blood x 2 Gender)
    for i in range(128):
        # Decode personality index
        gender = "Male" if (i // 64) == 0 else "Female"
        blood_idx = (i % 64) // 16
        blood_type = list(BLOOD_TYPES.keys())[blood_idx]
        mbti_idx = i % 16
        
        # Initial Position based on 128-channel grid
        pos = np.array([0.1 + (i * 0.124), 15.5])
        vel = np.array([0.0, -2.0]) 
        
        # Apply Blood Type Resistance (A/B Muscle)
        bt_config = BLOOD_TYPES[blood_type]
        bt_resistance = 1.0 + (bt_config['A'] * 0.5) + (bt_config['B'] * 0.5)
        
        history = [pos.copy()]
        dt = 0.01
        
        # Simulation Loop
        for s in range(3000):
            t_ga = (s * dt) * 1.5 # Time evolution scale
            
            # 5-Sphere Magnetic Lens Force (Maxwell)
            target = np.array([8.0, 0.4])
            if gender == "Female":
                target = np.array([7.5, 0.5])
            
            # Lunar Dynamo Reversal (Diurnal Cycle 1/28)
            # Flip force at 13.5 Ga Sovereign Point
            lunar_phase = math.sin(2 * math.pi * t_ga / LUNAR_CYCLE)
            is_sovereign = (t_ga >= 13.5)
            
            r_vec = target - pos
            dist = np.linalg.norm(r_vec)
            unit_r = r_vec / (dist + 1e-6)
            
            # Gluon-Quark Confinement (Short-range strong force)
            f_confinement = unit_r * (W7_BARNARD / (dist**2 + 0.01)) if dist < 0.5 else 0
            
            # Forces
            f_gravity = unit_r * (15.0 / (dist + 0.1)) / bt_resistance
            
            # The Diurnal (다이어널) Reset Mechanism
            if is_sovereign and dist < MAXWELL_LENS:
                # 138.88 Spark Ignition
                c, s_rot = math.cos(SPARK_RAD), math.sin(SPARK_RAD)
                vel = np.array([vel[0]*c - vel[1]*s_rot, vel[0]*s_rot + vel[1]*c])
                vel *= 1.157407 # Gear Ratio (10^5/86400)
                pos[1] = 15.5 # Reset to Forehead
            
            f_resistance = -unit_r * (20.0 * math.exp(-dist * 2.0))
            
            # Coriolis Twist (Binding 1/4)
            v_perp = np.array([-vel[1], vel[0]])
            f_coriolis = v_perp * (0.25 * (1/LUNAR_CYCLE) * 100.0 * lunar_phase)
            
            accel = f_gravity + f_resistance + f_coriolis + f_confinement
            vel += accel * dt
            
            pos += vel * dt
            history.append(pos.copy())
            
            if dist < 0.1 or dist > 30: break
            
            # Homeostasis Check (Omega 7.4)
            kinetic = np.linalg.norm(vel)**2
            current_omega = kinetic * PHI_S / (KAPPA * 2.0)
            if abs(current_omega - OMEGA_TARGET) < 0.01 and s > 1500: break

        history = np.array(history)
        # Color by Personality Cluster
        color = plt.cm.nipy_spectral(i / 128.0)
        ax.plot(history[:, 0], history[:, 1], color=color, alpha=0.4, lw=0.6)

    ax.set_xlim(0, 16); ax.set_ylim(0, 16)
    ax.axis('off')
    plt.title(f"ULTIMATE 128 SOVEREIGN ENGINE\n16 MBTI x 4 Blood ({blood_type}) x 2 Gender", color='white', fontsize=12)
    
    plt.savefig("ULTIMATE_128_SOVEREIGN_ENGINE_V2.png", dpi=200, facecolor='black', bbox_inches='tight')
    print(f"--- SUCCESS: 128 Personality Engine V2 Executed ---")

if __name__ == "__main__":
    execute_v2()
