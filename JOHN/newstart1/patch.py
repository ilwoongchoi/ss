import re

with open("scripts/cosmo_obs/validate_universal_equation_boss.py", "r") as f:
    content = f.read()

# Replace gaba_factor_for_mode to apply_gaba_mode
content = content.replace(
"""def gaba_factor_for_mode(mode: str) -> float:
    if mode == "none":
        return 1.0
    if mode == "cab_scale":
        return float(GABA_C_R_CAB)
    if mode == "ca_scale":
        return float(GABA_C_R_CA)
    if mode == "apex_scale":
        return float(GABA_C_V_APEX)
    raise ValueError(f"Unknown gaba_mode: {mode}")""",
"""import math
def apply_gaba_mode(base_val: float, mode: str) -> float:
    if mode == "none":
        return base_val
    if mode == "cab_scale":
        return float(base_val * GABA_C_R_CAB)
    if mode == "ca_scale":
        return float(base_val * GABA_C_R_CA)
    if mode == "apex_scale":
        return float(base_val * GABA_C_V_APEX)
    if mode == "nonlinear_v_shape":
        # Nonlinear V-Shape Convergence (Refraction + Offset Damping)
        # Phase shift from V_APEX, Gate threshold from R_CA, Floor from R_CAB
        phase_shift = math.cos(GABA_C_V_APEX)
        return float((base_val * phase_shift) + (GABA_C_R_CA - GABA_C_R_CAB))
    raise ValueError(f"Unknown gaba_mode: {mode}")"""
)

# Update run_bao_test
content = content.replace(
    "gaba_factor = gaba_factor_for_mode(gaba_mode)\n    slope_fixed = float(slope_base * gaba_factor)",
    "slope_fixed = apply_gaba_mode(slope_base, gaba_mode)\n    gaba_factor = slope_fixed / slope_base if slope_base != 0 else 0"
)

# Update run_monopole_test
content = content.replace(
    "gaba_factor = gaba_factor_for_mode(gaba_mode)\n    gamma_fixed = float(gamma_base * gaba_factor)",
    "gamma_fixed = apply_gaba_mode(gamma_base, gaba_mode)\n    gaba_factor = gamma_fixed / gamma_base if gamma_base != 0 else 0"
)

# Update choices in argparse
content = content.replace(
    'choices=["none", "cab_scale", "ca_scale", "apex_scale"],',
    'choices=["none", "cab_scale", "ca_scale", "apex_scale", "nonlinear_v_shape"],'
)

# Update the payload json output where gaba_factor_for_mode is used
content = content.replace(
    '"factor": gaba_factor_for_mode(args.gaba_mode),',
    '"factor": bao["gaba_factor"],'
)

with open("scripts/cosmo_obs/validate_universal_equation_boss.py", "w") as f:
    f.write(content)
print("Patched successfully.")
