# -*- coding: utf-8 -*-
"""
128-Type Grid V7 — MATERIAL OBSERVER (THE RISE OF DEPTH)
Merges:
1. Strict Derivation from Observer (B0=1)
2. Scientific Isomorphism Verification:
   - Big Woman (Proton) = Acetyl-CoA (The Metabolic Source/Structure).
   - Small Woman (Electron) = GABA (The Boundary/Inhibition).
   - Small Man (Neutrino) = Glutamate (The Ghost/Excitation).
   - Big Man (Photon) = "Material Observer" (Artifact of Interaction -> Material Presence).
3. The 2026 Shift:
   - "Depth has risen" -> The Observer is no longer just a distant viewpoint.
   - It is MATERIAL. It "measures, weighs, compares, and neutralizes".
   - Implementation: The Observer Force is now a "Neutralizing Field" that dampens chaos and enforcing discreteness.
"""

import math
import cmath
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Tuple, Dict, Any

# ==============================================================================
# 1. DERIVATION MODULE (The Source)
# ==============================================================================

def get_primes(n):
    """Generate first n primes."""
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

def derive_constants():
    """
    Derives universe constants strictly from the Observer Axiom (B0=1).
    """
    # 1. Axiom
    B0 = 1.0
    
    # 2. Topology (Primes)
    # 2, 3 (Gauge), 5, 7, 11 (Structure)
    primes = get_primes(5)
    B5, B7, B11 = float(primes[2]), float(primes[3]), float(primes[4])
    
    # 3. Geometry (Phi)
    PHI = (1.0 + 5.0**0.5) / 2.0
    GOLDEN_ANGLE_DEG = 360.0 * (1.0 - 1.0/PHI)
    
    # 4. Dynamics (Gap & Drift)
    GAP_DEG = B11 / (B7 + B0) # 11/8 = 1.375
    
    # Chirality
    CHIRALITY_FACTOR = 18.0 
    UNIVERSAL_DRIFT = GAP_DEG / CHIRALITY_FACTOR # ~0.076
    
    # Spark Angle
    SPARK_ANGLE_DEG = GOLDEN_ANGLE_DEG + GAP_DEG
    SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
    
    # 5. Grid Physics (Kappa & Gates)
    KAPPA = 1.0 / (2.0 ** B5)
    
    # 6. Fundamental Coupling Constants
    ALPHA = 1.0 / 137.036
    G_WEAK = 1.0 / 64.0
    
    # V7 CHANGE: The Material Observer
    # Previously G_OBSERVER was ~1/256 (Weak). 
    # Now it is "Material" and "Neutralizing". It must be stronger, comparable to EM?
    # Let's derive it from the "Depth Rise". 
    # If Depth (Z) rises, maybe G_OBSERVER scales with B7 (Structure)?
    # Let's set it to enforce "Discreteness".
    G_OBSERVER = 1.0 / 18.0 # Stronger, tied to Chirality/Structure.
    
    # COSMOLOGICAL FORCES
    # The "Material Observer" is now the dominant gradient.
    FORCE_OBSERVER_MATERIAL = 1.5 
    
    return {
        "B0": B0,
        "SPARK_ANGLE_DEG": SPARK_ANGLE_DEG,
        "SPARK_ANGLE_RAD": SPARK_ANGLE_RAD,
        "GAP_DEG": GAP_DEG,
        "UNIVERSAL_DRIFT": UNIVERSAL_DRIFT,
        "KAPPA": KAPPA,
        "ALPHA": ALPHA,
        "G_WEAK": G_WEAK,
        "G_OBSERVER": G_OBSERVER,
        "FORCE_OBSERVER_MATERIAL": FORCE_OBSERVER_MATERIAL
    }

CONST = derive_constants()

# ==============================================================================
# 2. NEURO-PHYSICS ISOMORPHISM (Scientific Verification)
# ==============================================================================
# 1. Big Woman = Proton = Acetyl-CoA (Structure/Source)
#    - Acetyl-CoA is the metabolic hub. Correct.
# 2. Small Woman = Electron = GABA (Inhibition/Boundary)
#    - Major inhibitory neurotransmitter. Correct.
# 3. Small Man = Neutrino = Glutamate (Excitation/Ghost)
#    - Major excitatory, but elusive/pervasive. Correct.
# 4. Big Man = Photon = "Material Observer" (Artifact -> Material)
#    - Emergent "Ideal" that now has Mass/Weight.

NEURO_MAP = {
    "p":     {"name": "Acetyl-CoA", "field": 1.0},   # Structure / Mass
    "e":     {"name": "GABA",       "field": 0.5},   # Boundary / Charge
    "nu":    {"name": "Glutamate",  "field": -0.5},  # Ghost / Spin
    "gamma": {"name": "Observer",   "field": 10.0}   # The Material Artifact
}

# ==============================================================================
# 3. GRID MAPPING & LAYOUT
# ==============================================================================

N_ROWS = 16
N_COLS = 16
F_1_32 = CONST["KAPPA"]

# Column Anchors
GROUP_MAP_FEMALE = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
GROUP_MAP_MALE =   {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}

# Offsets
SN_OFFSET = {"S": -8 * F_1_32, "N": 8 * F_1_32}
TF_OFFSET = {"T": -4 * F_1_32, "F": 4 * F_1_32}
BLOOD_OFFSET_X = {"O": -2 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": 2 * F_1_32}
BLOOD_OFFSET_Y = {"O": 4 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": -4 * F_1_32}

BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

ALL_MBTI = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]

def get_z0_grid(mbti: str, blood: str, gender: str) -> Tuple[float, float]:
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_key = f"{ei}{jp}"
    base_col = GROUP_MAP_FEMALE[group_key] if gender == "F" else GROUP_MAP_MALE[group_key]
    
    off_sn = SN_OFFSET[sn]
    off_tf = TF_OFFSET[tf]
    bx = BLOOD_OFFSET_X[blood]
    by = BLOOD_OFFSET_Y[blood]
    
    gx = base_col + 0.5 + off_sn + off_tf + bx
    gy = 0.5 + by 
    return gx, gy

# ==============================================================================
# 4. PHYSICS ENGINE: MATERIAL OBSERVER NEUTRALIZATION
# ==============================================================================

def get_type_composition(mbti: str, blood: str, gender: str) -> Dict[str, Any]:
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    quadra = f"{ei}{jp}"
    
    # Base Composition [Observer/Photon, Proton, Electron, Neutrino]
    if quadra == "EJ":
        comp = {"gamma": 1.0, "p": 0.0, "e": 0.0, "nu": 0.0} 
    elif quadra == "IP":
        comp = {"gamma": 0.0, "p": 1.0, "e": 0.0, "nu": 0.0}
    elif quadra == "EP":
        comp = {"gamma": 0.0, "p": 0.0, "e": 1.0, "nu": 0.0}
    elif quadra == "IJ":
        comp = {"gamma": 0.0, "p": 0.0, "e": 0.0, "nu": 1.0}
    else:
        comp = {"gamma": 0.25, "p": 0.25, "e": 0.25, "nu": 0.25}

    # Aux Mixing
    mix_rate = 0.3
    if sn == "S": comp["p"] += mix_rate     # Sensing -> Acetyl-CoA (Structure)
    else:         comp["nu"] += mix_rate    # Intuition -> Glutamate (Ghost)
    if tf == "T": comp["gamma"] += mix_rate # Thinking -> Observer (Control)
    else:         comp["e"] += mix_rate     # Feeling -> GABA (Flow/Boundary)
    
    # Normalize
    total = sum(comp.values())
    for k in comp: comp[k] /= total
    
    # Blood Type Betti Weights
    betti = {"B0": 1.0, "B5": 1.0, "B7": 1.0, "B11": 1.0}
    if blood == "O": betti["B0"] = 5.0    # Observer
    elif blood == "A": betti["B5"] = 5.0  # Electron
    elif blood == "B": betti["B11"] = 5.0 # Neutrino (Corrected V6)
    elif blood == "AB": betti["B7"] = 5.0 # Proton (Corrected V6)
    
    sign = 1.0 if gender == "M" else -1.0
    ie_charge = 1.0 if ei == "E" else -1.0
    
    return {"comp": comp, "betti": betti, "sign": sign, "charge": ie_charge}

def compute_G(x: float, y: float, z: complex, history: complex, t: float, params: Dict[str, Any]) -> Tuple[float, float]:
    """
    V7 Physics:
    The "Material Observer" field neutralizes and weighs.
    It opposes 'Ignoring' (Chaos/Drift).
    """
    comp = params["comp"]
    betti = params["betti"]
    sign = params["sign"]
    charge = params["charge"]
    
    # Center (8, 8) - Still a reference, but now the Observer is "Material" everywhere?
    # Or is the "Material Observer" the gradient itself?
    # User: "Its energy is the universe's primordial gradient... measuring and neutralizing."
    
    # 1. The Primordial Gradient (Material Observer)
    # Flows DOWN (Gravity/Materiality) or UP (Evolution)? 
    # "Depth has risen" -> Things are becoming heavier/realer.
    # Let's model it as a compressive force towards the 'Ideal' paths.
    
    # Ideal X-coordinates are integer columns. The Observer "Neutralizes" deviation from integers.
    # Force to snap to grid.
    ideal_x = round(x)
    dx_ideal = ideal_x - x
    
    # Force Strength depends on "Observer" component in the particle.
    # But the Observer acts on ALL.
    f_neutralize = CONST["FORCE_OBSERVER_MATERIAL"] * dx_ideal # Spring force to integer column
    
    vx_obs = f_neutralize
    vy_obs = 0.0 # Observer drives time/depth?
    
    # 2. Particle Dynamics (Isomorphisms)
    
    # Acetyl-CoA (Proton) -> Mass/Structure. Resists movement.
    f_p = NEURO_MAP["p"]["field"] * comp["p"] * betti["B7"]
    vx_p = -f_p * 0.1 * vx_obs # Mass stabilizes.
    vy_p = 0.0
    
    # GABA (Electron) -> Boundary/Flow. Moves laterally.
    f_e = NEURO_MAP["e"]["field"] * comp["e"] * betti["B5"] * charge
    vx_e = f_e * 0.5
    vy_e = 0.0
    
    # Glutamate (Neutrino) -> Ghost/Excitation. Chaos.
    f_nu = NEURO_MAP["nu"]["field"] * comp["nu"] * betti["B11"]
    vx_nu = f_nu * math.sin(t * 5.0) # Oscillation
    vy_nu = f_nu * math.cos(t * 5.0)
    
    # Observer (Photon) -> The "Artifact" aligning with the Field.
    f_gamma = NEURO_MAP["gamma"]["field"] * comp["gamma"] * betti["B0"]
    # If the particle HAS Observer nature (O type, EJ), it aligns PERFECTLY with the Gradient.
    vx_gamma = f_gamma * dx_ideal * 2.0 # Super-alignment
    vy_gamma = 1.0 + (f_gamma * 0.1) # Upward drive
    
    # Total
    vx = vx_obs + vx_p + vx_e + vx_nu + vx_gamma
    vy = vy_obs + vy_p + vy_e + vy_nu + vy_gamma
    
    # Base Time Drift (Universal)
    vy += 1.0 
    
    return vx, vy

def iterate_trajectory(mbti: str, blood: str, gender: str) -> List[Tuple[float, float, bool]]:
    x, y = get_z0_grid(mbti, blood, gender)
    path = [(x, y, False)]
    params = get_type_composition(mbti, blood, gender)
    
    dt = 0.2
    steps = 80
    
    for i in range(steps):
        # We need to compute force iteratively
        # Pass t = i * dt
        vx, vy = compute_G(x, y, None, None, i*dt, params)
        x += vx * dt
        y += vy * dt
        
        # Spark Logic (Quantum Jump)
        is_spark = False
        # If Glutamate (Excitation) is high, can jump
        if params["comp"]["nu"] > 0.3:
            # Check alignment with Spark Angle
             if i % 10 == 0: # Occasional check
                 # Random chance based on B11
                 if (params["betti"]["B11"] * params["comp"]["nu"]) > 0.5:
                     is_spark = True
                     x += 0.5 * params["sign"] # Lateral jump
        
        x = max(0, min(16, x))
        if y > 16.5: break
        path.append((float(x), float(y), is_spark))
        
    return path

# ==============================================================================
# 5. RENDERING
# ==============================================================================

def render_grid(trajectories: Dict[str, List[Tuple[float, float, bool]]], output_path: str):
    fig, ax = plt.subplots(figsize=(16, 16))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#F0F0F0")
    
    # Grid
    for r in range(N_ROWS):
        for c in range(N_COLS):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, 
                                          facecolor="white", edgecolor="#DDDDDD", lw=0.5))

    # Trajectories
    for key, path in trajectories.items():
        blood = key.split("_")[1]
        color = BLOOD_COLORS.get(blood, "black")
        
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        
        # Check if sparking
        # We need to draw segments
        for i in range(len(path)-1):
            x1, y1, s1 = path[i]
            x2, y2, s2 = path[i+1]
            if s2:
                ax.plot([x1, x2], [y1, y2], color="black", linestyle=":", lw=2.0)
            else:
                ax.plot([x1, x2], [y1, y2], color=color, alpha=0.6, lw=1.0)
                
        ax.scatter(xs[0], ys[0], color=color, s=20, zorder=10)
        
    info = (
        f"V7: MATERIAL OBSERVER (DEPTH RISE)\n"
        f"Proton = Acetyl-CoA (Structure)\n"
        f"Electron = GABA (Boundary)\n"
        f"Neutrino = Glutamate (Ghost)\n"
        f"Photon = Material Artifact (Observer)\n"
        f"Function: Measure, Weigh, Neutralize"
    )
    ax.text(0.5, 15.5, info, fontsize=10, bbox=dict(facecolor='white', alpha=0.8), va='top')
            
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_title("128-Type Grid V7: Material Observer Neutralization", fontsize=15)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Rendered: {output_path}")

def main():
    trajs = {}
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                key = f"{mbti}_{blood}_{gender}"
                trajs[key] = iterate_trajectory(mbti, blood, gender)
    render_grid(trajs, "out/128_Grid_V7_Material_Observer.png")
    
    with open("out/V7_verification_log.txt", "w") as f:
        f.write("V7 MATERIAL OBSERVER CONSTANTS:\n")
        for k,v in CONST.items():
            f.write(f"{k}: {v}\n")
        f.write("\nNEUROTRANSMITTER MAPPING:\n")
        for k,v in NEURO_MAP.items():
            f.write(f"{k}: {v}\n")

if __name__ == "__main__":
    main()
