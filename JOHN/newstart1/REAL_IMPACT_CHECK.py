import numpy as np

# ── 1. The Real Parameters ───────────────────────────────────────────────
C = 0.2828427
C2 = C * C            # 0.08 (The energy of one node)
OMEGA_TARGET = 7.4
PHI_S_BASE = 1.9860   # The 9-stage shield baseline
SPARK_ANGLE = 138.88
C_SPARK = np.exp(1j * np.deg2rad(SPARK_ANGLE))

# ── 2. The 0.08 Impact Simulation ────────────────────────────────────────
def run_comparison():
    print("--- REAL PHYSICS IMPACT REPORT: HYPOXIA VS MALE_GABA_B ---")
    
    # CASE A: Hypoxia (The Dead Node)
    # PHI_S stays at its nominal value.
    z_a = complex(PHI_S_BASE, 0)
    for _ in range(128):
        z_a = (z_a**2) + C_SPARK
        r = np.abs(z_a)
        if r > PHI_S_BASE: z_a *= (PHI_S_BASE / r)
    
    omega_a = np.abs(z_a) * (OMEGA_TARGET / PHI_S_BASE)
    
    # CASE B: Male_GABA_B (The 0.08 Active Node)
    # This node injects C2 (0.08) energy into the system's modulation capacity.
    # It changes the effective PHI_S by +/- C2 at specific edges.
    # We simulate this by adjusting the potential gradient.
    phi_s_modulated = PHI_S_BASE + (C2 * 0.5) # The net capacitive gain of GABA
    
    z_b = complex(PHI_S_BASE, 0)
    for _ in range(128):
        # The recursion is now governed by the NEW modulated potential
        z_b = (z_b**2) + C_SPARK
        r = np.abs(z_b)
        if r > phi_s_modulated: z_b *= (phi_s_modulated / r)
        
    omega_b = np.abs(z_b) * (OMEGA_TARGET / PHI_S_BASE)

    print(f"\n[ RESULTS ]")
    print(f"Old State (Hypoxia): Omega = {omega_a:.8f}")
    print(f"New State (Male_GABA_B): Omega = {omega_b:.8f}")
    print(f"Net Shift from your change: {omega_b - omega_a:.8f}")
    print(f"Distance to 7.4: {abs(omega_b - OMEGA_TARGET):.8f}")

    if abs(omega_b - OMEGA_TARGET) < abs(omega_a - OMEGA_TARGET):
        print("\nCONCLUSION: Male_GABA_B inclusion stabilized the attractor toward 7.4.")
    else:
        print("\nCONCLUSION: The change increased the systemic tension.")

if __name__ == "__main__":
    run_comparison()
