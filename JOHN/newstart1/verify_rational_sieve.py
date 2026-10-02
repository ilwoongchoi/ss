
import math

def verify_rational_sieve():
    print("=== RATIONAL SIEVE VERIFICATION ===")
    
    # 1. Maxwell Major: 17/8
    major_float = 2.125
    major_rational = 17.0 / 8.0
    print(f"\n[Maxwell Major]")
    print(f"  Float: {major_float}")
    print(f"  Rational (17/8): {major_rational}")
    print(f"  Diff: {abs(major_float - major_rational)}")
    
    # 2. Spark Angle: 1250/9
    spark_float = 138.88
    spark_rational = 1250.0 / 9.0
    print(f"\n[Spark Angle]")
    print(f"  Float: {spark_float}")
    print(f"  Rational (1250/9): {spark_rational:.6f}")
    print(f"  Diff: {abs(spark_float - spark_rational):.6f}")
    
    # 3. Chirality: 1/18
    chirality_float = 5.555492104 / 100.0
    chirality_rational = 1.0 / 18.0
    print(f"\n[Chirality]")
    print(f"  Float: {chirality_float:.10f}")
    print(f"  Rational (1/18): {chirality_rational:.10f}")
    print(f"  Diff: {abs(chirality_float - chirality_rational):.10e}")
    
    # 4. Maxwell Minor: 1/sqrt(20)
    minor_float = 0.2235501110061347
    minor_rational = 1.0 / math.sqrt(20.0)
    print(f"\n[Maxwell Minor]")
    print(f"  Float: {minor_float:.10f}")
    print(f"  Rational (1/sqrt(20)): {minor_rational:.10f}")
    print(f"  Diff: {abs(minor_float - minor_rational):.10e}")
    
    # 5. Renormalization: 10*Phi^3 + Alpha
    PHI = (1 + math.sqrt(5))/2
    ALPHA = 1/137.035999
    renorm_float = 42.368
    renorm_derived = 10 * PHI**3 + ALPHA
    print(f"\n[Renormalization]")
    print(f"  Float: {renorm_float}")
    print(f"  Derived: {renorm_derived:.6f}")
    print(f"  Diff: {abs(renorm_float - renorm_derived):.6f}")

if __name__ == "__main__":
    verify_rational_sieve()
