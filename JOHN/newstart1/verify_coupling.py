
import sys
import os

# Add the project root to the path so we can import geometry_package
sys.path.append(os.getcwd())

from geometry_package.universal_equation import current_state, universal_latent, coupling_scale

def verify():
    state = current_state()
    print("=== UNIVERSAL COUPLING VERIFICATION ===")
    print(f"Coupling Scale: {state.coupling_scale:.10f}")
    print(f"Universal Latent: {universal_latent():.10f}")
    print(f"Closure Constraint: {state.closure:.10f}")
    print(f"Raw Tension: {state.raw_tension:.10f}")
    print(f"Mismatch Delta: {state.mismatch_delta:.10f}")
    print("-" * 30)
    print("Components:")
    from geometry_package.absolute_constants import (
        F_1_32, GATE_5_32, RESID_DATA_5_32, TOTAL_DEBT_AREA, NIGHT_HYSTERESIS
    )
    print(f"GATE_5_32: {GATE_5_32}")
    print(f"RESID_DATA_5_32: {RESID_DATA_5_32}")
    print(f"Debt Ratio: {TOTAL_DEBT_AREA/NIGHT_HYSTERESIS}")
    
    # Check if F_1_64 is effectively gone
    # We can't check the local variable in the function easily, but the output speaks for itself.

if __name__ == "__main__":
    verify()
