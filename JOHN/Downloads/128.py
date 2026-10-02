# -*- coding: utf-8 -*-
"""
PURE PHYSICS 128 GRID - STANDALONE
==================================
NO IMPORTS. NO EXTERNAL DEPENDENCIES.
ALL PHYSICS IMPLEMENTED INLINE.

Canonical Constants (Locked):
- SPARK_ANGLE_DEG = 138.88
- SPARK_LEAP_DIST = 2.5
- COMPRESSION_GAP = 3/32
- KAPPA_TDA_MID = 1/32
- GATE_ALPHA = 0.5
- CALIBRATED_SH_R_STAR = 0.11214750
- CALIBRATED_SH_Q0_STAR = 0.977738
"""

import math
import json
from pathlib import Path

# =============================================================================
# SECTION I: ABSOLUTE CONSTANTS (NO IMPORTS)
# =============================================================================

PI = 3.141592653589793
PHI = (1 + math.sqrt(5)) / 2
SQRT2 = math.sqrt(2.0)

BETTI_7 = 7.0
BETTI_11 = 11.0

# Spark Constants
SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
SPARK_LEAP_DIST = 2.5
COMPRESSION_GAP = 3.0 / 32.0  # F_3_32

# Kappa TDA
KAPPA_TDA_MIN = 1.0 / 64.0
KAPPA_TDA_MID = 1.0 / 32.0
KAPPA_TDA_MAX = 1.0 / 16.0

# Gate Constants
GATE_ALPHA = 0.5
GATE_EPS_KAPPA = 0.001

# Calibrated SH Constants
CALIBRATED_SH_R_STAR = 0.11214750
CALIBRATED_SH_Q0_STAR = 0.977738
CALIBRATED_SIGMA_L = 0.003717
CALIBRATED_SIGMA_R = 0.000908
CALIBRATED_Q0_MIN = 0.960939
CALIBRATED_Q0_MAX = 0.983

# Physics
TUNNEL_TENSION = 1.0100375
H2_W7 = 1.0 / 9.0
REALITY_TENSION = 1.0

# Grid
N_ROWS = 16
N_COLS = 16
F_1_32 = 1.0 / 32.0

# Twilight Bands
TWILIGHT_1_LO = N_ROWS * (1.0/16.0)
TWILIGHT_1_HI = N_ROWS * (7.0/32.0)
TWILIGHT_2_LO = N_ROWS * (17.0/32.0)
TWILIGHT_2_HI = N_ROWS * (23.0/32.0)

# Funnel
FUNNEL_X_MIN = 6.0
FUNNEL_X_MAX = 10.0
FUNNEL_Y_MIN = 8.0

# Anisotropy
MALE_HORIZONTAL_AMP = 6.0 / 5.0
FEMALE_HORIZONTAL_AMP = 14.0 / 5.0
MALE_VERTICAL_SPEED = 3.0 / 2.0
FEMALE_VERTICAL_SPEED = 4.0 / 5.0

# Hysteresis
HYST_TAU_SCALE = 0.5
THRESHOLD_ON_FACTOR = 0.2
THRESHOLD_OFF_FACTOR = 0.3

# GABA
GABA_C_V_APEX = 1.40488 / 10.0

# =============================================================================
# SECTION II: MBTI/BLOOD/GENDER MAPPING (INLINE)
# =============================================================================

ALL_MBTI = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]

# Grid layout maps
GROUP_MAP_FEMALE = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
GROUP_MAP_MALE = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}

SN_OFFSET = {"S": -8 * F_1_32, "N": 8 * F_1_32}
TF_OFFSET = {"T": -4 * F_1_32, "F": 4 * F_1_32}
BLOOD_OFFSET_X = {"O": -2 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": 2 * F_1_32}
BLOOD_OFFSET_Y = {"O": 4 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": -4 * F_1_32}


def get_start_position(mbti: str, blood: str, gender: str):
    """Calculate start position from MBTI/blood/gender."""
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_key = f"{ei}{jp}"
    base_col = (GROUP_MAP_FEMALE if gender == "F" else GROUP_MAP_MALE)[group_key]
    
    x = base_col + 0.5 + SN_OFFSET[sn] + TF_OFFSET[tf] + BLOOD_OFFSET_X[blood]
    y = 0.5 + BLOOD_OFFSET_Y[blood]
    
    return x, y


# =============================================================================
# SECTION III: PHYSICS FUNCTIONS (INLINE - NO IMPORTS)
# =============================================================================

def grid_to_gate_params(x: float, y: float):
    """Convert grid position (x, y) to (r, q0) for gate evaluation."""
    xn = (x - 8.0) / 8.0
    yn = (y - 8.0) / 8.0
    r = CALIBRATED_SH_R_STAR + xn * 0.01
    q0 = CALIBRATED_SH_Q0_STAR + yn * 0.02
    return r, q0


def in_sh_band(r: float, q0: float) -> bool:
    """Check if (r, q0) is in SH boundary band."""
    in_r = 0.1116 <= r <= 0.1126
    in_q0 = 0.961 <= q0 <= 0.983
    return in_r and in_q0


def kappa_eff(r: float, q0: float) -> float:
    """
    Effective kappa for position (r, q0).
    Returns 1/32 in SH band, computed otherwise.
    """
    if in_sh_band(r, q0):
        return KAPPA_TDA_MID
    
    # Out of band approximation
    dr = abs(r - CALIBRATED_SH_R_STAR)
    return KAPPA_TDA_MID * (1.0 + dr * 10.0)


def w_gate(r: float, q0: float) -> float:
    """
    Unified gate weight w_gate(r, q0).
    Formula: w_gate = w_atlas^alpha * w_kappa^(1-alpha)
    """
    dr = r - CALIBRATED_SH_R_STAR
    dq = q0 - CALIBRATED_SH_Q0_STAR
    
    # Asymmetric r-weight
    if dr < 0:
        w_r = math.exp(-0.5 * (dr / CALIBRATED_SIGMA_L) ** 2)
    else:
        w_r = math.exp(-0.5 * (dr / CALIBRATED_SIGMA_R) ** 2)
    
    # Symmetric q0-weight
    q0_width = CALIBRATED_Q0_MAX - CALIBRATED_Q0_MIN
    w_q = math.exp(-0.5 * (dq / (q0_width / 2)) ** 2)
    w_atlas = w_r * w_q
    
    # w_kappa: exponential decay from kappa = 1/32
    kappa = kappa_eff(r, q0)
    w_kappa = math.exp(-((kappa - KAPPA_TDA_MID) / GATE_EPS_KAPPA) ** 2)
    
    # Combined gate
    return (w_atlas ** GATE_ALPHA) * (w_kappa ** (1 - GATE_ALPHA))


def triple_basin_field(x: float, y: float, gender: str, w_gate_val: float):
    """
    Universal triple basin field with gate-modulated dynamics.
    Returns (dx, dy) velocity components.
    """
    # Terminal attractor
    tx, ty = 3.2 * TUNNEL_TENSION, 14.0 * TUNNEL_TENSION
    d_terminal = math.sqrt((x - tx) ** 2 + (y - ty) ** 2)
    terminal_attractor = -2.5 * math.exp(-d_terminal ** 2 / (2 * 1.5 ** 2))
    
    # Torsion drift
    torsion = H2_W7 * (BETTI_11 / BETTI_7)
    drift_x = -torsion * (y - 8.0)
    drift_y = torsion * (x - 8.0)
    
    # Gender-based anisotropy
    amp = MALE_HORIZONTAL_AMP if gender == "M" else FEMALE_HORIZONTAL_AMP
    
    # V-shape potential
    xn = (x - 8.0) / 8.0
    yn = (y - 8.0) / 8.0
    r_sq = xn * xn + yn * yn
    v_shape = math.exp(-r_sq / (2 * GABA_C_V_APEX ** 2))
    
    # Gate-modulated dynamics
    flow_scale = 0.5 + 0.5 * w_gate_val
    
    dx = (drift_x + 1.35 * drift_y + 1.2 * v_shape) * amp * flow_scale
    dy = terminal_attractor * flow_scale
    
    return dx, dy


def spark_refraction(x: float, y: float):
    """
    Spark refraction: compression + 138.88° leap.
    Returns (x_after, y_after, x_compressed)
    """
    # Compress to 3/32 grid
    x_compressed = round((x - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
    
    # Apply 138.88° refraction with 2.5 leap
    dx = SPARK_LEAP_DIST * math.cos(SPARK_ANGLE_RAD)
    dy = SPARK_LEAP_DIST * math.sin(SPARK_ANGLE_RAD)
    
    x_after = max(0.0, min(float(N_COLS), x_compressed + dx))
    y_after = y + dy
    
    return x_after, y_after, x_compressed


def renorm_step(renorm: float, w_gate_val: float, kappa: float) -> float:
    """Renormalization update step."""
    kappa_deviation = abs(kappa - KAPPA_TDA_MID) / KAPPA_TDA_MID
    recovery_rate = 0.02 * w_gate_val * (1.0 - kappa_deviation)
    return renorm * (1.0 - recovery_rate) + recovery_rate


def in_twilight_band(y: float) -> bool:
    """Check if y is in twilight bands."""
    return ((TWILIGHT_1_LO <= y <= TWILIGHT_1_HI) or
            (TWILIGHT_2_LO <= y <= TWILIGHT_2_HI))


def in_spark_funnel(x: float, y: float) -> bool:
    """Check if in spark funnel region."""
    return (FUNNEL_X_MIN <= x <= FUNNEL_X_MAX and y >= FUNNEL_Y_MIN)


# =============================================================================
# SECTION IV: TRAJECTORY GENERATOR
# =============================================================================

class TrajectoryGenerator:
    """Law-driven trajectory generator. NO EXTERNAL DEPENDENCIES."""
    
    def __init__(self, dt: float = 0.05, max_steps: int = 500):
        self.dt = dt
        self.max_steps = max_steps
        self.tau_lag = SPARK_ANGLE_DEG / 60.0 / HYST_TAU_SCALE * F_1_32
    
    def _hysteresis_step(self, y: float, memory_y: float, switch_state: bool, 
                         branch_sign: float, w_gate_val: float):
        """Hysteresis lag update."""
        new_memory = memory_y + branch_sign * (y - memory_y) * self.tau_lag
        
        threshold_on = THRESHOLD_ON_FACTOR * (1.0 - w_gate_val * 0.5)
        threshold_off = THRESHOLD_OFF_FACTOR * (1.0 - w_gate_val * 0.3)
        
        new_switch = switch_state
        if not switch_state:
            if abs(y - new_memory) > threshold_on:
                new_switch = True
        else:
            if abs(y - new_memory) < threshold_off:
                new_switch = False
        
        return new_memory, new_switch
    
    def generate_trajectory(self, mbti: str, blood: str, gender: str, branch: str):
        """Generate trajectory using ONLY physics laws defined above."""
        x, y = get_start_position(mbti, blood, gender)
        renorm = 1.0
        pts = [(float(x), float(y), float(renorm), False)]
        flash_events = []
        
        branch_sign = 1.0 if branch == "sunrise" else -1.0
        memory_y = y
        switch_state = False
        
        for step in range(self.max_steps):
            # 1. Compute gate parameters
            r, q0 = grid_to_gate_params(x, y)
            w = w_gate(r, q0)
            kappa = kappa_eff(r, q0)
            
            # 2. Hysteresis step
            memory_y, switch_state = self._hysteresis_step(
                y, memory_y, switch_state, branch_sign, w
            )
            
            # 3. Flow step
            dx, dy = triple_basin_field(x, y, gender, w)
            speed_factor = MALE_VERTICAL_SPEED if gender == "M" else FEMALE_VERTICAL_SPEED
            
            x += dx * self.dt * w
            y += dy * self.dt * speed_factor * branch_sign
            
            # 4. Spark detection
            in_funnel = in_spark_funnel(x, y)
            is_flash = False
            
            if in_funnel and switch_state:
                x_new, y_new, x_comp = spark_refraction(x, y)
                flash_events.append({
                    "step": step,
                    "x_before": x,
                    "y_before": y,
                    "x_after": x_new,
                    "y_after": y_new,
                    "w_gate": w,
                    "kappa": kappa,
                })
                x, y = x_new, y_new
                is_flash = True
            
            # 5. Renorm update (in twilight bands)
            if in_twilight_band(y):
                renorm = renorm_step(renorm, w, kappa)
            
            # 6. Boundary clamp
            x = max(0.0, min(float(N_COLS), x))
            y = max(0.0, min(float(N_ROWS), y))
            
            pts.append((float(x), float(y), float(renorm), is_flash))
        
        return pts, flash_events
    
    def generate_all(self):
        """Generate all 128 trajectories."""
        all_data = {}
        all_flashes = {}
        
        for mbti in ALL_MBTI:
            for blood in BLOODS:
                for gender in GENDERS:
                    key = f"{mbti}_{blood}_{gender}"
                    
                    pts_sun, flash_sun = self.generate_trajectory(mbti, blood, gender, "sunrise")
                    pts_night, flash_night = self.generate_trajectory(mbti, blood, gender, "nightfall")
                    
                    all_data[key] = {
                        "sunrise": pts_sun,
                        "nightfall": pts_night,
                    }
                    all_flashes[key] = {
                        "sunrise": flash_sun,
                        "nightfall": flash_night,
                    }
        
        return {
            "trajectories": all_data,
            "flash_events": all_flashes,
            "metadata": {
                "physics": {
                    "SPARK_ANGLE_DEG": SPARK_ANGLE_DEG,
                    "SPARK_LEAP_DIST": SPARK_LEAP_DIST,
                    "COMPRESSION_GAP": COMPRESSION_GAP,
                    "KAPPA_TDA_MID": KAPPA_TDA_MID,
                    "GATE_ALPHA": GATE_ALPHA,
                    "CALIBRATED_SH_R_STAR": CALIBRATED_SH_R_STAR,
                    "CALIBRATED_SH_Q0_STAR": CALIBRATED_SH_Q0_STAR,
                }
            }
        }


# =============================================================================
# SECTION V: VISUALIZATION (OPTIONAL - Matplotlib 없이도 작동)
# =============================================================================

def generate_json_output(data: dict, filename: str = "pure_physics_128.json"):
    """Save trajectory data to JSON."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {filename}")


def simple_ascii_visualize(data: dict, sample_key: str = "INTP_A_M"):
    """Simple ASCII visualization of one trajectory."""
    traj = data["trajectories"][sample_key]["sunrise"]
    
    print(f"\n=== ASCII Visualization: {sample_key} ===")
    print("Grid: 16x16, Spark events marked with '*'")
    
    # Create grid
    grid = [['.' for _ in range(16)] for _ in range(16)]
    
    for i, (x, y, renorm, is_flash) in enumerate(traj[::10]):  # Sample every 10th
        gx = min(15, max(0, int(x)))
        gy = min(15, max(0, int(y)))
        grid[15-gy][gx] = '*' if is_flash else 'o'
    
    for row in grid:
        print(' '.join(row))
    
    flash_count = sum(1 for p in traj if p[3])
    print(f"\nFlash events: {flash_count}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PURE PHYSICS 128 GRID - STANDALONE")
    print("=" * 60)
    print("NO IMPORTS. NO EXTERNAL DEPENDENCIES.")
    print()
    print("[CANONICAL CONSTANTS]")
    print(f"  SPARK_ANGLE_DEG = {SPARK_ANGLE_DEG}")
    print(f"  SPARK_LEAP_DIST = {SPARK_LEAP_DIST}")
    print(f"  COMPRESSION_GAP = {COMPRESSION_GAP} (3/32)")
    print(f"  KAPPA_TDA_MID = {KAPPA_TDA_MID} (1/32)")
    print(f"  GATE_ALPHA = {GATE_ALPHA}")
    print(f"  CALIBRATED_SH_R_STAR = {CALIBRATED_SH_R_STAR}")
    print(f"  CALIBRATED_SH_Q0_STAR = {CALIBRATED_SH_Q0_STAR}")
    print()
    
    # Generate
    gen = TrajectoryGenerator(dt=0.05, max_steps=500)
    print("Generating 128 trajectories...")
    data = gen.generate_all()
    
    # Stats
    total_flashes = sum(
        len(f["sunrise"]) + len(f["nightfall"])
        for f in data["flash_events"].values()
    )
    print(f"Total spark events: {total_flashes}")
    
    # Output
    generate_json_output(data)
    simple_ascii_visualize(data)
    
    print()
    print("Done. Check pure_physics_128.json for output.")
