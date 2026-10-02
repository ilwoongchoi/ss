import re

with open("geometry_package/absolute_constants.py", "r", encoding="utf-8") as f:
    content = f.read()

gaba_c_constants = """
# ---------------------------------------------------------
# 5. GABA-C CONVERGENCE (V-Shape Crevice)
# ---------------------------------------------------------
# These constants define the nonlinear biological regularizer for cosmological convergence
# derived from retinal expression ratios aligning with the cosmic Ouroboros.
GABA_C_R_CAB = 0.084132  # Tonic inhibition floor (C/(A+B)) -> ~NIGHT_HYSTERESIS / 10
GABA_C_R_CA = 0.092734   # Gate threshold (C/A) -> Near F_3_32 (Darkness Stress)
GABA_C_V_APEX = 0.139965 # Refraction phase shift (Dynamic V-apex)

"""

if "GABA_C_R_CAB" not in content:
    content = content.replace("# 5. CALIBRATION DICTIONARY", gaba_c_constants + "# 6. CALIBRATION DICTIONARY")
    content = content.replace('"TUNNEL_TENSION": TUNNEL_TENSION,', '"TUNNEL_TENSION": TUNNEL_TENSION,\n    "GABA_C_R_CAB": GABA_C_R_CAB,\n    "GABA_C_R_CA": GABA_C_R_CA,\n    "GABA_C_V_APEX": GABA_C_V_APEX,')
    
    with open("geometry_package/absolute_constants.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched absolute_constants.py successfully.")
else:
    print("Already patched.")
