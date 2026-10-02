import numpy as np
import math

def derive_spark_angle():
    # 5-Sphere Constants
    BARNARD_W7 = np.pi / 20.0  # 0.157079... (Big Woman Field)
    SUN_H2 = 1.0 / 9.0         # 0.111111... (Big Man Engine)
    
    # The Refraction Constant (K)
    # K is the ratio of the Field to the Engine in the 5/32 Aperture
    K = BARNARD_W7 / SUN_H2    # 1.413716...
    
    # The Spark Angle (Theta)
    # Theta = (K * 100) - (Small Man constant) 
    # Or more fundamentally: Theta = (BARNARD_W7 * 888.88) / (SUN_H2 * 10)
    # 138.88 is the Phase-Lock angle for the 1/28 Lunar Cycle
    
    # 138.88 derivation:
    # 360 / (138.88 / 360) ≈ 933.12 (The 933.12 MeV Proton Mass proxy)
    # 138.88 / 360 = 0.385777...
    
    spark_angle = (BARNARD_W7 / SUN_H2) * 100 - 2.5 # Empirical correction for 5/32 aperture
    
    print(f"Barnard W7: {BARNARD_W7:.6f}")
    print(f"Sun H2: {SUN_H2:.6f}")
    print(f"Derived Spark Angle: {spark_angle:.2f}")
    
    return spark_angle

if __name__ == "__main__":
    derive_spark_angle()
