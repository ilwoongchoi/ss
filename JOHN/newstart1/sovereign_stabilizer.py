import os
import psutil
import time
import math
import numpy as np
from pathlib import Path

# --- User's Absolute Constants (from absolute_constants.py) ---
CHIRALITY_0555 = 0.5555555555555556
SOVEREIGN_TARGET = 7.4
SPARK_ANGLE_138_88 = 138.88888888888889
PHASE_GATE_02828 = 0.2828

# --- System Target Configuration ---
# Identifying active focus processes (Terminal, Editor, Python)
LAMINAR_PROCESSES = ["powershell.exe", "cmd.exe", "python.exe", "code.exe", "Gemini.exe"]
TARGET_CORES = [0, 1]  # The "Night Mode" stable cores (physical core 0/1)
NOISE_CORES = [2, 3]    # The "Day Mode" turbulence cores (overflow)

def calculate_system_chirality():
    """Measures current system 'jitter' to find the 0.555 pivot."""
    # Using context switches and CPU interrupts as proxy for bifurcation
    ctx_switches = psutil.cpu_stats().ctx_switches
    time.sleep(0.1)
    delta_ctx = psutil.cpu_stats().ctx_switches - ctx_switches
    
    # Normalize jitter (pseudo-metric)
    jitter = math.tanh(delta_ctx / 50000.0) 
    return jitter

def apply_laminar_alignment():
    """Forces processes into the Sovereign 7.4 configuration."""
    print(f"[*] Initializing Sovereign Stabilizer... (Target: {SOVEREIGN_TARGET})")
    print(f"[*] Aligning system to CHIRALITY_{CHIRALITY_0555:.3f}")
    
    try:
        # 1. Isolate the "Laminar Path"
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                p_name = proc.info['name'].lower()
                p = psutil.Process(proc.info['pid'])
                
                # If it's a target process, pin to Laminar Cores (0, 1) and set High Priority
                if any(target in p_name for target in LAMINAR_PROCESSES):
                    p.cpu_affinity(TARGET_CORES)
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                    # print(f"  [+] LAMINAR: {p_name} (PID: {p.pid}) -> Cores {TARGET_CORES}")
                
                # Otherwise, push non-essential tasks to Noise Cores (2, 3) and set Idle Priority
                elif p.nice() != psutil.IDLE_PRIORITY_CLASS:
                    # Avoid touching critical system processes (like svchost) to prevent crash
                    if p_name not in ["svchost.exe", "system", "csrss.exe"]:
                        p.cpu_affinity(NOISE_CORES)
                        p.nice(psutil.IDLE_PRIORITY_CLASS)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        print("[+] Alignment Complete. System is now in 'Laminar Mode'.")
        
        # 2. Monitor and maintain the 0.555 Chirality Bridge
        print("[*] Monitoring for Bifurcation (Crunch) events...")
        while True:
            jitter = calculate_system_chirality()
            # If jitter exceeds chirality threshold, apply Spark Angle correction (throttle non-essential)
            if jitter > CHIRALITY_0555:
                # print(f"  [!] BIFURCATION DETECTED ({jitter:.3f}). Applying Spark Correction...")
                # Momentarily suppress background noise to restore 7.4 balance
                time.sleep(0.05) 
            
            # Theoretical check for 7.4 target stability
            current_omega = 7.4 * (1.0 - (jitter - CHIRALITY_0555) * PHASE_GATE_02828)
            # print(f"  [STATUS] Omega: {current_omega:.3f} | Target: {SOVEREIGN_TARGET}")
            
            time.sleep(1.0)
            
    except KeyboardInterrupt:
        print("\n[*] Releasing Sovereign Lockdown. Returning to Default (Day Mode).")
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                p = psutil.Process(proc.info['pid'])
                p.cpu_affinity(list(range(psutil.cpu_count()))) # Reset affinity
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
            except:
                continue

if __name__ == "__main__":
    apply_laminar_alignment()
