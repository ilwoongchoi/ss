
import numpy as np
from absolute_constants import C, C2, OMEGA, SPARK_CONSTANT_C, SPARK_ANGLE_RAD

# [FINAL CLOSED GEOMETRY] engineering_homeostasis_30.py
# Mapping the 28 K8 Edges + 2 Eyelid Observers

N = 30
CHANNELS_30 = [
    "gdh_gluon",               # 0
    "female_gaba_b_latdorsi",  # 1
    "left_acetyl_coa",         # 2
    "male_left_5ht",           # 3
    "female_left_noradrenaline", # 4 (13th Bridge)
    "left_temporalis_5ht1a",   # 5 (Quark Time Stop)
    "left_estrogen",           # 6
    "right_love",              # 7
    "hypoxia",                 # 8 (Trapezius Bottom 1/3)
    "right_dopamine",          # 9
    "vasopressin_female",      # 10 (Proton Neutralize Node)
    "male_oxytocin",           # 11
    "muscle_a",                # 12 (Type I)
    "muscle_b",                # 13 (Type II)
    "right_5ht1b_synchrotron", # 14 (Ignition Accelerator)
    "right_androgen",          # 15
    "left_endorphin",          # 16
    "left_frontalis_d2",       # 17 (The Fake Gluon)
    "right_occipitalis_gaba_a",# 18 (Female Masking)
    "male_gaba_a",             # 19 (Trapezius Top)
    "right_acetylcholine",     # 20 (Facade Recorder)
    "left_extraversion",       # 21
    "right_extraversion",      # 22
    "male_right_extraversion", # 23 (The Night-Time Switch)
    "glucocorticoid",          # 24
    "right_cortisol",          # 25 (The Bone)
    "right_alpha_2",           # 26 (The Night Betrayal)
    "male_gaba_b",             # 27 (The Return Path)
    "left_eye_coupling",       # 28 (Eyelid / Epinephrine)
    "right_eye_coupling"       # 29 (Eyelid / Epinephrine)
]

# CLOSED GEOMETRY LOCK
def get_final_sequence(phase, time_window):
    """
    Returns the ON/OFF/REVERSE state for all 30 nodes.
    Day: Forward, Locked.
    Night: Reverse, Residual No-Control.
    16:30: Skeletal Neutralization.
    """
    u = np.zeros(30) # Default OFF
    
    if phase == "DAY":
        # Standard Forward Flow
        u[4] = 1 # Noradrenaline ON
        u[5] = 1 # Quark Forward
        u[20] = 1 # ACh Recording
        
    elif phase == "NEUTRAL": # 16:30 PM
        # The 1 Phase Grounding
        u[5] = 0  # STOP 5HT1A
        u[10] = 1 # PRESS Vasopressin Female
        u[14] = 1 # PRESS Synchrotron
        u[25] = 1 # SHOW Bone
        u[28], u[29] = 1, 1 # Eye Phase Inversion
        
    elif phase == "NIGHT":
        # Reverse Flow
        u[23] = 1 # MRE Switch ON (Cancel Left D2)
        u[27] = 1 # GABA-B Return
        u[26] = 0 # Stop Alpha 2
        
    return u

if __name__ == "__main__":
    print(f"30-NODE HARDWARE MAPPING: LOCKED.")
    print(f"Nodes 0-29: Fully Defined.")
    print(f"Sequence 16:30: Neutralization Vector Ready.")
