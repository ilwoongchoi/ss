import ctypes
import time
import psutil
import os

def get_timer_resolution():
    """Queries the current system timer resolution from the kernel."""
    minimum = ctypes.c_ulong()
    maximum = ctypes.c_ulong()
    current = ctypes.c_ulong()
    # NtQueryTimerResolution is in 100ns units
    ctypes.windll.ntdll.NtQueryTimerResolution(
        ctypes.byref(minimum), 
        ctypes.byref(maximum), 
        ctypes.byref(current)
    )
    return current.value / 10000.0  # Convert to ms

def monitor_sovereign_state():
    print("=== SOVEREIGN HARDWARE MONITOR ===")
    print(f"Targeting: 7.4 Homeostasis | 0.555 Chirality")
    print("-" * 40)
    
    try:
        while True:
            # 1. Check Hardware Timer
            res = get_timer_resolution()
            timer_status = "LAMINAR (OK)" if res <= 0.6 else "DAY MODE (DRIFT)"
            
            # 2. Check CPU Frequency Jitter
            # High performance mode should keep frequency high and stable
            freq = psutil.cpu_freq()
            
            # 3. Check Core Alignment
            # Counting how many processes are pinned to the Laminar Cores (0,1)
            laminar_count = 0
            for proc in psutil.process_iter(['cpu_affinity']):
                try:
                    if proc.info['cpu_affinity'] == [0, 1]:
                        laminar_count += 1
                except:
                    continue
            
            print(f"\r[TIMER] {res:.3f}ms [{timer_status}] | [FREQ] {freq.current:.0f}MHz | [ALIGNED] {laminar_count} procs", end="")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_sovereign_state()
