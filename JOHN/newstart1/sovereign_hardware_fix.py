
import numpy as np
import time
import psutil
import math
from absolute_constants import *

class SovereignHardwareFix:
    """
    V12 Pure Coulomb Hardware Fix Engine.
    Aligns hardware electronic flow (represented by CPU metrics) 
    to the 7.4 Homeostasis target using 10-axis valve logic.
    """
    def __init__(self):
        print("--- DEPLOYING SOVEREIGN HARDWARE FIX ENGINE (V12-FINAL) ---")
        self.target = SOVEREIGN_TARGET # 7.4
        self.spark_rad = math.radians(SPARK_ANGLE_DEG) # 138.88°
        
        # 10-Axis Valve States (Physical Control Parameters)
        self.valves = {
            "5HT1A_SINK": 1.0,   # Target Gravity
            "5HT_VECTOR": 1.0,   # Forward Momentum
            "GABA_A_SPARK": 1.0, # Alignment Trigger
            "CORTISOL_RES": 0.5, # Lensing Resistance
            "VASO_EXPANSION": 1.2, # Hardware Capacity
            "OXY_BINDING": 0.8    # Inter-core Coherence
        }
        
        self.last_cpu_state = np.array([0.0, 0.0]) # [Load, Temperature]

    def get_hardware_trajectory(self):
        """
        Maps real-time hardware physics to the Coulomb engine coordinate system.
        """
        cpu_load = psutil.cpu_percent(interval=0.1) / 100.0
        # 온도 정보 (가능한 경우) 혹은 부하 변화량을 가상 속도로 사용
        temp_factor = 0.5 # Default
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                temp_factor = temps[next(iter(temps))][0].current / 100.0
        except:
            pass
            
        return np.array([cpu_load * 16.0, temp_factor * 16.0])

    def apply_coulomb_correction(self, pos, vel):
        """
        Applies the V12 Pure Coulomb force to align the hardware flow.
        """
        forces = np.array([0.0, 0.0])
        
        # 1. Attractor Pull to PLP CORE (0,0) - The Sovereign Target
        dist_sq = np.sum(pos**2) + 0.1
        dir_to_core = -pos / np.sqrt(dist_sq)
        forces += dir_to_core * (1.0 * self.valves["5HT1A_SINK"] / dist_sq)
        
        # 2. Linear Flow 정렬 (Night Mode)
        flow_y = self.valves["5HT_VECTOR"] * (1.0 - self.valves["CORTISOL_RES"] * 0.1)
        forces += np.array([0.0, flow_y])
        
        # 3. Expansion/Binding Balance (Vaso/Oxy)
        lateral_stress = (self.valves["VASO_EXPANSION"] - self.valves["OXY_BINDING"]) * 0.1
        forces[0] += lateral_stress
        
        # Integration
        dt = 0.05
        new_vel = vel * 0.95 + forces * dt
        new_pos = pos + new_vel * dt
        
        # --- THE 138.88° SPARK CORRECTION (Bifurcation Break) ---
        speed = np.linalg.norm(new_vel)
        if speed > 0.5: # 과도한 난류 발생 시
            curr_angle = math.atan2(new_vel[1], new_vel[0])
            new_angle = curr_angle + self.spark_rad
            new_vel[0] = speed * math.cos(new_angle)
            new_vel[1] = speed * math.sin(new_angle)
            print(f"\n[SPARK] Bifurcation Refracted at 138.88°. Laminar Flow Restored.")
            
        return new_pos, new_vel

    def run(self):
        print(f"Aligning Hardware to Homeostasis Lockdown: {self.target}")
        pos = self.get_hardware_trajectory()
        vel = np.array([0.0, 0.0])
        
        try:
            while True:
                # 1. 실제 하드웨어 데이터 샘플링
                real_pos = self.get_hardware_trajectory()
                
                # 2. 물리 모델을 통한 정렬 궤적 계산
                pos, vel = self.apply_coulomb_correction(real_pos, vel)
                
                # 3. 현재 정렬 상태(Lockdown) 계산
                # 7.4 근접도 측정
                lockdown_val = (1.0 / (np.linalg.norm(pos) + 0.1)) * 74.0
                coherence = 1.0 - (abs(lockdown_val - self.target) / self.target)
                
                status = "LAMINAR (NIGHT)" if coherence > 0.555 else "TURBULENT (DAY)"
                
                print(f"\rHardware Vector: [{pos[0]:.2f}, {pos[1]:.2f}] | Lockdown: {lockdown_val:.4f} | Status: {status}", end="")
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nSovereign Hardware Fix Engine Offline.")

if __name__ == "__main__":
    fix_engine = SovereignHardwareFix()
    fix_engine.run()
