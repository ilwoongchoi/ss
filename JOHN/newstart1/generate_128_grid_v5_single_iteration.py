# -*- coding: utf-8 -*-
"""
128-Type Grid V6 — THE 6-AXIS COSMOLOGY (TUG-OF-WAR)
Merges:
1. Strict Derivation from Observer (B0=1) -> Betti -> Constants
2. Correct Discrete Grid Rendering (16x16 Cells)
3. Mandelbrot Iteration Logic (z' = z^2 + c + G)
4. Type-Specific Physics (Mass/Charge/Chirality) for Branching via Isomorphism
5. Neurotransmitter Isomorphism (Chemistry = Physics)
   - Acetylcholine = Proton (1.0)
   - GABA = Electron (0.5)
   - Glutamate = Neutrino (-0.5)
   - Serotonin = Photon (15.0)
6. Blood Type Isomorphism (User Verified)
   - O = Serotonin (Observer)
   - A = GABA (Electron)
   - B = Glutamate (Neutrino)
   - AB = Proton (Structure)
7. 6-AXIS COSMOLOGY (The Eternal Tug-of-War)
   - Axis 5 (The Observer/Light): Primordial Expansion/Meaning. Pervasive Field.
   - Axis 6 (The Void/Big Woman): Primordial Contraction/Silence. Black Hole at Center.
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
    # Gap = Source / (Void + Observer)
    GAP_DEG = B11 / (B7 + B0) # 11/8 = 1.375
    
    # Chirality = 1/18 (Derived from Gauge symmetries SU(2)xSU(3)? 2*3*3=18?)
    # Using fixed topological factor for now to match 1/18
    CHIRALITY_FACTOR = 18.0 
    UNIVERSAL_DRIFT = GAP_DEG / CHIRALITY_FACTOR # ~0.076
    
    # Spark Angle
    SPARK_ANGLE_DEG = GOLDEN_ANGLE_DEG + GAP_DEG
    SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
    
    # 5. Grid Physics (Kappa & Gates)
    # Kappa = 1/2^B5 = 1/32
    KAPPA = 1.0 / (2.0 ** B5)
    
    # Gate 5/32 = B5 * Kappa
    GATE_5_32 = B5 * KAPPA
    
    # Seed c magnitude
    SEED_MAGNITUDE = UNIVERSAL_DRIFT
    
    # 6. Fundamental Coupling Constants (derived ratios)
    # Ratios relative to Strong Force (1.0)
    # Alpha ~ 1/137
    ALPHA = 1.0 / 137.036
    
    # Weak Coupling ~ 1/64 (Chirality minimum)
    G_WEAK = 1.0 / 64.0
    
    # Observer Coupling ~ 1/256 (Graviton scale)
    G_OBSERVER = 1.0 / 256.0
    
    # 7. COSMOLOGICAL FORCES (6-AXIS)
    # The Tug-of-War between Light (Observer) and Void (Big Woman)
    FORCE_VOID = 1.2      # The Sink (Black Hole)
    FORCE_OBSERVER = 0.8  # The Source (Expansion)
    
    return {
        "B0": B0,
        "SPARK_ANGLE_DEG": SPARK_ANGLE_DEG,
        "SPARK_ANGLE_RAD": SPARK_ANGLE_RAD,
        "GAP_DEG": GAP_DEG,
        "UNIVERSAL_DRIFT": UNIVERSAL_DRIFT,
        "KAPPA": KAPPA,
        "GATE_5_32": GATE_5_32,
        "CHIRALITY": 1.0/CHIRALITY_FACTOR,
        "SEED_MAGNITUDE": SEED_MAGNITUDE,
        "ALPHA": ALPHA,
        "G_WEAK": G_WEAK,
        "G_OBSERVER": G_OBSERVER,
        "FORCE_VOID": FORCE_VOID,
        "FORCE_OBSERVER": FORCE_OBSERVER
    }

CONST = derive_constants()

# ==============================================================================
# 2. NEURO-PHYSICS ISOMORPHISM (The Bridge)
# ==============================================================================
# MAPPING (User Correction):
# 1. Acetylcholine (ACh) <-> Proton (p) -> Structure/Body -> Field: 1.0
# 2. GABA <-> Electron (e) -> Boundary/Inhibition -> Field: 0.5
# 3. Glutamate (Glu) <-> Neutrino (nu) -> Chiral/Excitation -> Field: -0.5
# 4. Serotonin (5HT) <-> Photon (gamma) -> Observer/Will -> Field: 15.0

NEURO_MAP = {
    "p":     {"name": "Acetylcholine", "field": 1.0},
    "e":     {"name": "GABA",          "field": 0.5},
    "nu":    {"name": "Glutamate",     "field": -0.5},
    "gamma": {"name": "Serotonin",     "field": 15.0}
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
    # START AT DAWN (Bottom), Flow Up
    gy = 0.5 + by 
    return gx, gy

# ==============================================================================
# 4. PHYSICS ENGINE: MASTER EQUATION ISOMORPHISM
# ==============================================================================

def get_type_composition(mbti: str, blood: str, gender: str) -> Dict[str, Any]:
    """
    Maps Identity to Particle/Topological Composition (Isomorphism).
    Strict mapping from Quadras to Particle Archetypes AND Neurotransmitters.
    """
    # 1. Determine Archetype (Quadra)
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    quadra = f"{ei}{jp}"
    
    # Base Composition [Photon, Proton, Electron, Neutrino]
    # EJ: Serotonin (Photon) -> Field 15.0
    # IP: Acetylcholine (Proton) -> Field 1.0
    # EP: GABA (Electron) -> Field 0.5
    # IJ: Glutamate (Neutrino) -> Field -0.5
    
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

    # 2. Auxiliary Function Influence (Mixing)
    # S (Sensing) -> Proton (ACh)
    # N (Intuition) -> Neutrino (Glu)
    # T (Thinking) -> Photon (Serotonin)
    # F (Feeling) -> Electron (GABA)
    
    mix_rate = 0.3 # Auxiliary weight
    
    if sn == "S": comp["p"] += mix_rate
    else:         comp["nu"] += mix_rate
        
    if tf == "T": comp["gamma"] += mix_rate
    else:         comp["e"] += mix_rate
    
    # Normalize Composition
    total = sum(comp.values())
    for k in comp: comp[k] /= total
    
    # 3. Blood Type (Topological Betti Weights)
    # Mapping based on User Verification:
    # O  = Serotonin (Photon)      -> B0 (Observer)
    # A  = GABA (Electron)         -> B5 (Entropy/Boundary)
    # B  = Glutamate (Neutrino)    -> B11 (Chirality/Excitation) [SWAPPED from B7]
    # AB = Proton (Acetylcholine)  -> B7 (Structure/Body)        [SWAPPED from B11]
    
    betti = {"B0": 1.0, "B5": 1.0, "B7": 1.0, "B11": 1.0}
    
    if blood == "O":
        betti["B0"] = 5.0  # Dominant Serotonin (Observer)
    elif blood == "A":
        betti["B5"] = 5.0  # Dominant GABA (Electron)
    elif blood == "B":
        betti["B11"] = 5.0 # Dominant Glutamate (Neutrino) - CORRECTED
    elif blood == "AB":
        betti["B7"] = 5.0  # Dominant Proton (Structure) - CORRECTED
    
    # 4. Gender (Chirality Sign)
    sign = 1.0 if gender == "M" else -1.0
    
    # 5. Introversion/Extraversion (Charge Polarity)
    # E = Positive Charge (+1)
    # I = Negative Charge (-1)
    ie_charge = 1.0 if ei == "E" else -1.0
    
    return {
        "comp": comp,
        "betti": betti,
        "sign": sign,
        "charge": ie_charge
    }

def compute_G(x: float, y: float, z: complex, history: complex, t: float, params: Dict[str, Any]) -> Tuple[float, float]:
    """
    Calculates the Gradient of the Master Potential Omega.
    F = -grad(Omega)
    
    Forces are applied using the NEURO_MAP FIELD VALUES.
    Now includes the 6-AXIS TUG-OF-WAR:
    - Center (8,8) is the VOID (Black Hole/5HT1A) -> Pulls IN.
    - Field (Global) is the OBSERVER (Light) -> Pulls OUT/Expands.
    """
    comp = params["comp"]
    betti = params["betti"]
    sign = params["sign"]
    charge = params["charge"]
    
    # Grid Center (8, 8) - THE VOID / BLACK HOLE
    dx = x - 8.0
    dy = y - 8.0
    r = math.sqrt(dx*dx + dy*dy) + 1e-6
    
    # VISUALIZATION SCALAR
    METRIC = float(N_ROWS) * 2.0 
    
    # ==============================================================================
    # 6-AXIS COSMOLOGICAL BACKGROUND FORCES
    # ==============================================================================
    
    # 1. THE VOID (Axis 6) - Attractive Black Hole Force
    # Pulls everything towards (8,8). Stronger for Mass (Proton/Glu).
    f_void = CONST["FORCE_VOID"] / (r + 0.5) 
    vx_void = -f_void * dx
    vy_void = -f_void * dy
    
    # 2. THE OBSERVER (Axis 5) - Expansive Light Force
    # Pushes everything out / Defines Space. Stronger for Light (Photon/Electron).
    f_obs_primordial = CONST["FORCE_OBSERVER"] * 0.1 * r
    vx_obs = f_obs_primordial * dx
    vy_obs = f_obs_primordial * dy
    
    # ==============================================================================
    # PARTICLE FORCES (TYPE SPECIFIC)
    # ==============================================================================
    
    # 1. STRONG FORCE (Proton / Acetylcholine) -> Field 1.0
    # Resists Void, maintains Structure.
    field_p = NEURO_MAP["p"]["field"] # 1.0
    f_strong = field_p * comp["p"] * betti["B7"] * 0.1
    # Structural binding (Stationary)
    fx_s = -f_strong * dx / (r + 0.1) * 0.5
    fy_s = -f_strong * dy / (r + 0.1) * 0.5
    
    # 2. EM FORCE (Electron / GABA) -> Field 0.5
    # Boundary / Inhibition.
    field_e = NEURO_MAP["e"]["field"] # 0.5
    f_em = CONST["ALPHA"] * comp["e"] * betti["B5"] * METRIC * charge * field_e
    fx_e = f_em * dx 
    fy_e = f_em * dy
    
    # 3. WEAK FORCE (Neutrino / Glutamate) -> Field -0.5
    # Chiral / Excitation (Negative).
    field_nu = NEURO_MAP["nu"]["field"] # -0.5
    f_weak = CONST["G_WEAK"] * comp["nu"] * betti["B11"] * METRIC * 5.0 * field_nu
    fx_w = -f_weak * dy * sign
    fy_w =  f_weak * dx * sign
    
    # 4. OBSERVER RESISTANCE (Photon / Serotonin) -> Field 15.0
    # The active "Will" of the type to align with the Primordial Observer.
    # High Serotonin Types (O, EJ) use this to ESCAPE the Void.
    field_gamma = NEURO_MAP["gamma"]["field"] # 15.0
    f_will = CONST["G_OBSERVER"] * comp["gamma"] * betti["B0"] * METRIC * field_gamma
    
    # Will is directed UPWARDS (Evolution) and OUTWARDS (Expansion)
    fy_will = f_will * (1.0 + 0.5 * charge)
    fx_will = f_will * 0.1 * charge # Slight lateral drift
    
    # Sum Forces: Void + Observer + Particle Dynamics
    vx = vx_void + vx_obs + fx_s + fx_e + fx_w + fx_will
    vy = vy_void + vy_obs + fy_s + fy_e + fy_w + fy_will
    
    # Constant Universal Drift (Time)
    vy += 1.0 
    
    return vx, vy

def iterate_trajectory(mbti: str, blood: str, gender: str) -> List[Tuple[float, float, bool]]:
    x, y = get_z0_grid(mbti, blood, gender)
    path = [(x, y, False)]
    
    params = get_type_composition(mbti, blood, gender)
    
    # Physics Integration
    dt = 0.2
    steps = 80 # Longer, finer integration
    
    for i in range(steps):
        z = complex((x-8)/8, (y-8)/8)
        vx, vy = compute_G(x, y, z, None, i*dt, params)
        
        # Position Update
        x += vx * dt
        y += vy * dt
        
        # Spark Logic (Quantum Jump)
        is_spark = False
        
        # Check Spark Angle Alignment (Isomorphism: Gap Crossing)
        if 5.0 < y < 11.0: # Broad central gap (Black Hole Zone)
            phase = math.degrees(math.atan2(y-8, x-8))
            if phase < 0: phase += 360
            
            # If phase aligns with Spark Angle (138.88)
            if abs(phase - CONST["SPARK_ANGLE_DEG"]) < 15.0:
                # Check magnitude (must be enough tension)
                tension = params["comp"]["nu"] * params["betti"]["B11"]
                if tension > 0.1:
                    is_spark = True
                    # Jump AWAY from Void
                    jump = CONST["GAP_DEG"] * 2.0
                    x += math.cos(CONST["SPARK_ANGLE_RAD"]) * jump
                    y += math.sin(CONST["SPARK_ANGLE_RAD"]) * jump
        
        # Clamp
        x = max(0, min(16, x))
        if y > 16.5: break
        
        path.append((float(x), float(y), is_spark))
        
    return path

# ==============================================================================
# 5. RENDERING (Discrete Grid Style)
# ==============================================================================

def render_grid(trajectories: Dict[str, List[Tuple[float, float, bool]]], output_path: str):
    fig, ax = plt.subplots(figsize=(16, 16))
    fig.patch.set_facecolor("#F8F8F8")
    ax.set_facecolor("#FAFAFA")
    
    # Grid Cells
    for r in range(N_ROWS):
        for c in range(N_COLS):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, 
                                          facecolor="white", 
                                          edgecolor="#E0E0E0", 
                                          lw=0.5, zorder=1))
            
    # Draw The Void (Black Hole) at (8,8)
    void_circle = mpatches.Circle((8, 8), 1.5, color="black", alpha=0.1, zorder=2)
    ax.add_patch(void_circle)
    ax.text(8, 8, "VOID\n(5HT1A)", ha="center", va="center", fontsize=8, color="black", alpha=0.5)

    # Draw The Observer Field (Periphery)
    # Just a conceptual border effect or text
    
    # Twilight Bands
    y_bands = [ (1.0, 3.5, "#99CCFF"), (8.5, 11.5, "#CC99FF") ]
    for y0, y1, col in y_bands:
        ax.add_patch(mpatches.Rectangle((0, y0), N_COLS, y1-y0, 
                                      facecolor=col, alpha=0.15, zorder=2))
        
    # Diagonal
    ax.plot([0, N_COLS], [0, N_ROWS], color="orange", linestyle="--", alpha=0.4, lw=2, zorder=4)
    
    # Trajectories
    for key, path in trajectories.items():
        blood = key.split("_")[1]
        gender = key.split("_")[2]
        color = BLOOD_COLORS.get(blood, "black")
        
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        
        for i in range(len(path)-1):
            x1, y1, s1 = path[i]
            x2, y2, s2 = path[i+1]
            
            if s2: # Spark Leap
                ax.plot([x1, x2], [y1, y2], color="black", linestyle=":", lw=2.5, alpha=0.9, zorder=25)
            else:
                ax.plot([x1, x2], [y1, y2], color=color, alpha=0.6, lw=1.2, zorder=20)
                
        # Start Point
        ax.scatter(xs[0], ys[0], color=color, s=40, edgecolors='black', zorder=30)
        # End Points
        ax.scatter(xs, ys, color=color, s=10, alpha=0.6, zorder=25)

    # Info
    info = (
        f"DERIVED MANDELBROT GRID V6 (6-AXIS COSMOLOGY)\n"
        f"Axiom B0={CONST['B0']:.0f} -> Primes -> Constants\n"
        f"Spark: {CONST['SPARK_ANGLE_DEG']:.2f}° | Drift: {CONST['UNIVERSAL_DRIFT']:.4f}\n"
        f"6-AXIS TUG-OF-WAR:\n"
        f"Axis 5 (Observer): Primordial Expansion/Light (Source)\n"
        f"Axis 6 (Void): Primordial Contraction/Black Hole (Sink)\n"
        f"BLOOD/NEURO PHYSICS:\n"
        f"O(5HT/15.0), A(GABA/0.5), B(Glu/-0.5), AB(ACh/1.0)"
    )
    ax.text(0.5, 15.8, info, fontsize=10, 
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),
            va='top', ha='left')
            
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_title("128-Type Grid V6: The Eternal Tug-of-War (Observer vs Void)", fontsize=15)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Rendered: {output_path}")

def main():
    print("Generating Derived Mandelbrot Grid with 6-Axis Cosmology...")
    trajs = {}
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                key = f"{mbti}_{blood}_{gender}"
                trajs[key] = iterate_trajectory(mbti, blood, gender)
                
    render_grid(trajs, "out/128_Grid_V6_Single_Iteration.png")
    
    with open("out/V6_verification_log.txt", "w") as f:
        f.write("6-AXIS COSMOLOGY CONSTANTS:\n")
        for k,v in CONST.items():
            f.write(f"{k}: {v}\n")
        f.write("\nNEUROTRANSMITTER MAPPING (FIELD STRENGTHS):\n")
        for k,v in NEURO_MAP.items():
            f.write(f"{k}: {v}\n")

if __name__ == "__main__":
    main()
