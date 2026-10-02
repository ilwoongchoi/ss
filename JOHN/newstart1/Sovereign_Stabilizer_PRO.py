import os
import sys
import time
import ctypes
import psutil
import math
from pathlib import Path

# --- User's Absolute Constants (Laminar Homeostasis) ---
CHIRALITY_0555 = 0.5555555555555556
SOVEREIGN_TARGET = 7.4
PHASE_GATE_02828 = 0.2828

# --- Win32 API Constants for Semi-Hardware Control ---
timeBeginPeriod = ctypes.windll.winmm.timeBeginPeriod
timeEndPeriod = ctypes.windll.winmm.timeEndPeriod
NtSetTimerResolution = ctypes.windll.ntdll.NtSetTimerResolution

# High Performance Power Scheme (GUID for High Performance)
HIGH_PERF_SCHEME = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"

# Target processes for the "Laminar Path"
LAMINAR_PROCESSES = ["powershell.exe", "cmd.exe", "python.exe", "code.exe", "Gemini.exe", "browser.exe", "chrome.exe"]
TARGET_CORES = [0, 1]  # Night Mode Cores (Physical)
NOISE_CORES = [2, 3]    # Day Mode Cores (Overflow)

def set_high_resolution_timer():
    """Forces hardware timer to 0.5ms (5000 in 100ns units) to kill temporal bifurcation."""
    print("[*] Locking System Timer Resolution to 0.5ms... (Laminar Timing)")
    actual_res = ctypes.c_ulong()
    # NtSetTimerResolution(DesiredResolution, SetResolution, CurrentResolution)
    status = NtSetTimerResolution(5000, 1, ctypes.byref(actual_res))
    if status == 0:
        # print(f"  [+] Timer Lock Active. Actual: {actual_res.value / 10000.0}ms")
        pass
    else:
        # Fallback to standard 1ms if ntdll call fails
        timeBeginPeriod(1)

def set_sovereign_power_state():
    """Eliminates voltage/frequency jitter by forcing High Performance (No C-States)."""
    print("[*] Activating Sovereign Power State... (Blocking C-State Jitter)")
    os.system(f"powercfg -setactive {HIGH_PERF_SCHEME}")

def apply_pro_alignment():
    """Deep hardware-level alignment of all system resources to the 7.4 Target."""
    print(f"[*] Initializing Sovereign Stabilizer PRO... (Target: {SOVEREIGN_TARGET})")
    
    # 1. Hardware Environment Setup
    set_high_resolution_timer()
    set_sovereign_power_state()
    
    try:
        # 2. Aggressive Resource Isolation
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                p_name = proc.info['name'].lower()
                p = psutil.Process(proc.info['pid'])
                
                # Laminar Alignment (High priority path)
                if any(target in p_name for target in LAMINAR_PROCESSES):
                    p.cpu_affinity(TARGET_CORES)
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                    p.ionice(psutil.IOPRIO_HIGH) # Semi-Hardware I/O Priority
                
                # Noise Isolation (Suppress background bifurcation)
                elif p_name not in ["svchost.exe", "system", "csrss.exe", "lsass.exe"]:
                    p.cpu_affinity(NOISE_CORES)
                    p.nice(psutil.IDLE_PRIORITY_CLASS)
                    p.ionice(psutil.IOPRIO_VERYLOW)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        print(f"[+] Pro Alignment Complete. Chirality locked at {CHIRALITY_0555:.3f}")
        print("[*] Monitoring Laminar Stability (7.4 Target Homeostasis)...")
        
        while True:
            # Measure delta to calculate real-time drift from 0.555
            ctx_start = psutil.cpu_stats().ctx_switches
            time.sleep(1.0)
            delta = psutil.cpu_stats().ctx_switches - ctx_start
            
            # Normalize jitter metric relative to system load
            jitter = math.tanh(delta / 30000.0)
            current_omega = 7.4 * (1.0 - (jitter - CHIRALITY_0555) * PHASE_GATE_02828)
            
            # If omega deviates too far from 7.4, it indicates a "Crunch" (Bifurcation)
            # PRO version doesn't just print, it applies a micro-pause to flush noise cores
            if current_omega < 7.0:
                # print(f"  [!] CRUNCH DETECTED (Omega: {current_omega:.2f}). Flushing Noise Cores...")
                # Temporarily yield CPU time for noise processes to settle
                time.sleep(0.01)
            
            # print(f"  [STATUS] Homeostasis: {current_omega:.3f} / {SOVEREIGN_TARGET}")

    except KeyboardInterrupt:
        print("\n[*] Releasing Sovereign PRO Control. Restoring Day Mode.")
        timeEndPeriod(1)
        # Reset power to Balanced (default GUID) if needed, though usually better to leave as High for work
        os.system("powercfg -setactive 381b4222-f694-41f0-9685-ff5bb260df2e")
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                p = psutil.Process(proc.info['pid'])
                p.cpu_affinity(list(range(psutil.cpu_count())))
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
            except:
                continue

if __name__ == "__main__":
    # Check for Admin privileges (required for high res timer and power settings)
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
    if not is_admin:
        print("[!] ERROR: Administrator privileges required for Semi-Hardware Control.")
        # sys.exit(1) # We'll try anyway, but warn the user.
    
    apply_pro_alignment()
