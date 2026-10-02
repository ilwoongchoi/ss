# synchronize_geometry.py
import os
import re

# Path to the geometry package.
# Assumes the script is run from the project root 'newstart'.
GEOMETRY_PACKAGE_PATH = "geometry_package"

# --- 1. Define the single source of truth for constants ---
ABSOLUTE_CONSTANTS_CONTENT = """# geometry_package/absolute_constants.py
# SINGLE SOURCE OF TRUTH for all geometric and physical constants.
import math

# --- Primary Sieve & Potential ---
PHI = (1 + math.sqrt(5)) / 2
ALPHA = 1 / 137.035999084
DESIGN_POTENTIAL_PHI = 1.40488

# --- Betti Numbers & Topology ---
BETTI_0 = 1.0
BETTI_5 = 5.0
BETTI_7 = 7.0
BETTI_11 = 11.0

# --- Gates & Thresholds ---
GATE_1_9 = 1.0 / 9.0
GATE_5_32 = 5.0 / 32.0
TUNNEL_TENSION = 1.0100375 # Reality Tension
H_GATE_RESOLUTION_DISCRETE = 1.0 / 64.0

# --- Renormalization / Sieve Bridges ---
RENORMALIZATION_BRIDGE = 10.0 * (PHI**3) + ALPHA # 42.368
ALPHA_KAPPA_BRIDGE = 137.0 / 32.0
CHIRALITY_CONSTANT = 1.0 / (BETTI_11 + BETTI_7) # 1/18
LOOP_STRENGTH_5 = CHIRALITY_CONSTANT * 100.0

# --- Derived Cosmological & Physical Constants ---
KAPPA_STABILITY_THRESHOLD = 0.03125
UNIVERSAL_DRIFT_DELTA = 0.076
EVENT_HORIZON_RADIUS_RS = 0.3125

# --- Biological / Junction Constants ---
NIGHT_HYSTERESIS = 0.8418
GABA_C_R_CAB = NIGHT_HYSTERESIS / 10.0
GABA_C_R_CA = (3.0 / 32.0) - (ALPHA / 7.0)
GABA_C_V_APEX = DESIGN_POTENTIAL_PHI / 10.0

# --- External Forces ---
LUNAR_CYCLE = 1.0 / 28.0
VERTICAL_MOBIUS_TWIST = 1.0 / 28.0
DAY_FORCE_SOLAR_UV = 1.0
NIGHT_FORCE_COSMIC_RAY = 0.96875

# --- Spark Geometry ---
SPARK_ANGLE_DEG = 138.88

# This print statement confirms the file is loaded.
# print("ABSOLUTE_CONSTANTS loaded: Single source of truth.")
"""

# --- 2. The main script logic ---
def synchronize_geometry():
    print("--- Starting Geometry Synchronization ---")

    # Create package directory if it doesn't exist
    if not os.path.exists(GEOMETRY_PACKAGE_PATH):
        os.makedirs(GEOMETRY_PACKAGE_PATH)
        print(f"Created directory: {GEOMETRY_PACKAGE_PATH}")
        # Create an empty __init__.py to make it a package
        with open(os.path.join(GEOMETRY_PACKAGE_PATH, "__init__.py"), "w") as f:
            f.write("# This file makes the 'geometry_package' directory a Python package.\n")

    # Write the canonical constants file
    constants_path = os.path.join(GEOMETRY_PACKAGE_PATH, "absolute_constants.py")
    with open(constants_path, "w", encoding="utf-8") as f:
        f.write(ABSOLUTE_CONSTANTS_CONTENT)
    print(f"Wrote canonical constants to: {constants_path}")

    # Patch the main solver to use the new constants
    solver_path = "master_equation_ness_solver.py"
    if os.path.exists(solver_path):
        with open(solver_path, "r", encoding="utf-8") as f:
            solver_content = f.read()

        # Replace old, long import with a simple wildcard import
        # This regex handles variations in whitespace and line breaks.
        pattern = r"from\s+geometry_package\.absolute_constants\s+import[\s\(]+[A-Z0-9_,\s]+[\)]?"
        replacement = "from geometry_package.absolute_constants import *"

        # Check if the replacement is needed
        if re.search(pattern, solver_content):
            solver_content = re.sub(pattern, replacement, solver_content, count=1)
            with open(solver_path, "w", encoding="utf-8") as f:
                f.write(solver_content)
            print(f"Patched imports in: {solver_path}")
        else:
            print(f"Imports in {solver_path} seem correct already. No patch needed.")

    else:
        print(f"WARNING: {solver_path} not found. Skipping patch.")


    # Clean up old/duplicate files
    files_to_delete = [
        os.path.join(GEOMETRY_PACKAGE_PATH, "아씨발.py"),
        os.path.join(GEOMETRY_PACKAGE_PATH, "geometry_3d_renderer_v5_uroboros_backup.py"),
        os.path.join(GEOMETRY_PACKAGE_PATH, "absolute_constants_v5_uroboros_backup.py"),
    ]
    for f_path in files_to_delete:
        if os.path.exists(f_path):
            try:
                os.remove(f_path)
                print(f"Deleted duplicate/old file: {f_path}")
            except OSError as e:
                print(f"Error deleting file {f_path}: {e}")

    print("\n--- Geometry Synchronization Complete ---")
    print("All core files have been standardized to use 'geometry_package/absolute_constants.py'.")
