# -*- coding: utf-8 -*-
"""
128-Type Grid V4 — LAW-DRIVEN UNIFIED ENGINE
============================================
Both Python grid and WebGL shader consume IDENTICAL physics from:
  - absolute_constants.py (geometry/physics constants)
  - universal_equation.py (kappa_eff, w_gate dynamics)

Refactored from script-heavy event logic to law-driven trajectory emergence.
Target: >60 FPS on ~3.4GB VRAM, deterministic 3D generative landscape.

PHYSICS STACK (canonical, shared with shader):
  1. Continuous Flow Core: universal_triple_basin_field()
  2. Hysteresis/Lag: State machine with tau_lag derived from SPARK_ANGLE_DEG
  3. Tunnel Transition: w_gate(r, q0) modulates trajectory dynamics
  4. Spark Reset/Refraction: 138.88° angle, 2.5 leap, compression at 3/32
  5. Renorm Update: kappa_eff(r, q0) drives renormalization steps
  6. Gate Weight: w_gate = w_atlas^0.5 * w_kappa^0.5 (alpha=0.5)

Author: Unified Grid/Shader System
Version: 2026.03.07
"""

import json
import math
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

# Import canonical physics laws (shared with shader via GLSL translation)
from geometry_package.absolute_constants import (
    PI, PHI, SQRT2,
    BETTI_7, BETTI_11,
    SPARK_ANGLE_DEG,
    SPARK_LEAP_DIST,
    F_1_32, F_3_32,
    KAPPA_TDA_MID,
    GATE_ALPHA,
    GATE_EPS_KAPPA,
    CALIBRATED_SH_R_STAR,
    CALIBRATED_SH_Q0_STAR,
    CALIBRATED_SIGMA_L,
    CALIBRATED_SIGMA_R,
    TUNNEL_TENSION,
)
from geometry_package.universal_equation import kappa_eff, w_gate

# Optional matplotlib for visualization (shader replaces this in browser)
try:
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
    matplotlib.rcParams['font.family'] = 'Malgun Gothic'
    matplotlib.rcParams['axes.unicode_minus'] = False
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# ===================================================================
# LAW-DRIVEN PHYSICS ENGINE (Shared Core)
# ===================================================================

class PhysicsLaw:
    """
    Canonical physics law container.
    Both Python grid and GLSL shader implement these identical formulas.
    """
    
    # Spark refraction constants (shared with shader)
    SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)
    COMPRESSION_GAP = F_3_32  # 3/32 grid compression
    
    # Hysteresis constants
    HYST_TAU_SCALE = 0.5
    THRESHOLD_ON_FACTOR = 0.2
    THRESHOLD_OFF_FACTOR = 0.3
    ALPHA_MAX = 0.5
    
    # Grid dimensions
    N_ROWS = 16
    N_COLS = 16
    
    # Anisotropy (gender-based trajectory modulation)
    MALE_HORIZONTAL_AMP = 6.0 / 5.0
    FEMALE_HORIZONTAL_AMP = 14.0 / 5.0
    MALE_VERTICAL_SPEED = 3.0 / 2.0
    FEMALE_VERTICAL_SPEED = 4.0 / 5.0
    
    @staticmethod
    def kappa_effective(r: float, q0: float) -> float:
        """
        Effective kappa at position (r, q0).
        Returns 1/32 in SH band, lookup-based otherwise.
        """
        return kappa_eff(r, q0)
    
    @staticmethod
    def gate_weight(r: float, q0: float) -> float:
        """
        Unified gate weight w_gate(r, q0).
        Combines asymmetric ATLAS band with kappa proximity.
        """
        return w_gate(r, q0, alpha=GATE_ALPHA, eps_kappa=GATE_EPS_KAPPA)
    
    @staticmethod
    def spark_refraction(x: float, y: float) -> Tuple[float, float, float]:
        """
        Spark refraction: compression + 138.88° leap.
        
        Returns:
            (x_after, y_after, x_compressed): post-spark position and compression point
        """
        # Compress to 3/32 grid
        x_compressed = round((x - 8.0) / PhysicsLaw.COMPRESSION_GAP) * PhysicsLaw.COMPRESSION_GAP + 8.0
        
        # Apply 138.88° refraction with 2.5 leap
        dx = SPARK_LEAP_DIST * math.cos(PhysicsLaw.SPARK_ANGLE_RAD)
        dy = SPARK_LEAP_DIST * math.sin(PhysicsLaw.SPARK_ANGLE_RAD)
        
        x_after = max(0.0, min(float(PhysicsLaw.N_COLS), x_compressed + dx))
        y_after = y + dy
        
        return x_after, y_after, x_compressed
    
    @staticmethod
    def triple_basin_field(x: float, y: float, gender: str, w_gate_val: float) -> Tuple[float, float]:
        """
        Universal triple basin field with gate-modulated dynamics.
        
        Args:
            x, y: Position
            gender: 'M' or 'F' (anisotropy modulation)
            w_gate_val: Current gate weight [0, 1]
            
        Returns:
            (dx, dy): velocity components
        """
        # Terminal attractor (canopy lift target)
        tx, ty = 3.2 * TUNNEL_TENSION, 14.0 * TUNNEL_TENSION
        d_terminal = math.sqrt((x - tx) ** 2 + (y - ty) ** 2)
        
        # Torsion drift (perpendicular rotation)
        H2_W7 = 1.0 / 9.0
        torsion = H2_W7 * (BETTI_11 / BETTI_7)
        drift_x = -torsion * (y - 8.0)
        drift_y = torsion * (x - 8.0)
        
        # Gender-based anisotropy
        amp = (PhysicsLaw.MALE_HORIZONTAL_AMP if gender == "M" 
               else PhysicsLaw.FEMALE_HORIZONTAL_AMP)
        
        # V-shape potential (GABA apex)
        xn = (x - 8.0) / 8.0
        yn = (y - 8.0) / 8.0
        r_sq = xn * xn + yn * yn
        v_shape = math.exp(-r_sq / (2 * (1.40488 / 10.0) ** 2))
        
        # Gate-modulated dynamics: w_gate -> 1 means "in band, normal flow"
        # w_gate -> 0 means "out of band, bifurcation risk"
        flow_scale = 0.5 + 0.5 * w_gate_val  # Modulate by gate weight
        
        dx = (drift_x + 1.35 * drift_y + 1.2 * v_shape) * amp * flow_scale
        dy = (-2.5 * math.exp(-d_terminal ** 2 / (2 * 1.5 ** 2))) * flow_scale
        
        return dx, dy
    
    @staticmethod
    def renorm_step(renorm: float, w_gate_val: float, kappa: float) -> float:
        """
        Renormalization update step.
        Renorm adjusts based on gate weight and kappa proximity to 1/32.
        
        Args:
            renorm: Current renormalization factor
            w_gate_val: Gate weight
            kappa: Current kappa value
            
        Returns:
            Updated renormalization factor
        """
        kappa_deviation = abs(kappa - KAPPA_TDA_MID) / KAPPA_TDA_MID
        recovery_rate = 0.02 * w_gate_val * (1.0 - kappa_deviation)
        return renorm * (1.0 - recovery_rate) + recovery_rate


# ===================================================================
# GRID LAYOUT (MBTI/Blood/Gender → Start Position)
# ===================================================================

class GridLayout:
    """Maps MBTI/Blood/Gender to starting positions on the 16x16 grid."""
    
    ROW_CENTER_OFFSET = 0.5
    COL_CENTER_OFFSET = 0.5
    
    FEMALE_GROUP_ORDER = ["EJ", "EP", "IJ", "IP"]
    MALE_GROUP_ORDER = ["IP", "IJ", "EP", "EJ"]
    GROUP_MAP_FEMALE = {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6}
    GROUP_MAP_MALE = {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14}
    
    # Offsets from grid fractions
    SN_OFFSET = {"S": -8 * F_1_32, "N": 8 * F_1_32}  # ±0.25
    TF_OFFSET = {"T": -4 * F_1_32, "F": 4 * F_1_32}  # ±0.125
    BLOOD_OFFSET_X = {"O": -2 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": 2 * F_1_32}
    BLOOD_OFFSET_Y = {"O": 4 * F_1_32, "A": 2 * F_1_32, "B": -2 * F_1_32, "AB": -4 * F_1_32}
    
    ALL_MBTI = [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP",
    ]
    BLOODS = ["O", "A", "B", "AB"]
    GENDERS = ["F", "M"]
    
    @classmethod
    def get_start_position(cls, mbti: str, blood: str, gender: str) -> Tuple[float, float]:
        """Calculate start position from MBTI/blood/gender."""
        ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
        group_key = f"{ei}{jp}"
        base_col = (cls.GROUP_MAP_FEMALE if gender == "F" else cls.GROUP_MAP_MALE)[group_key]
        
        x = base_col + cls.COL_CENTER_OFFSET + cls.SN_OFFSET[sn] + cls.TF_OFFSET[tf] + cls.BLOOD_OFFSET_X[blood]
        y = cls.ROW_CENTER_OFFSET + cls.BLOOD_OFFSET_Y[blood]
        
        return x, y
    
    @classmethod
    def generate_all_entities(cls) -> List[Dict[str, Any]]:
        """Generate all 128 entity definitions."""
        entities = []
        for mbti in cls.ALL_MBTI:
            for blood in cls.BLOODS:
                for gender in cls.GENDERS:
                    x0, y0 = cls.get_start_position(mbti, blood, gender)
                    entities.append({
                        "mbti": mbti,
                        "blood": blood,
                        "gender": gender,
                        "x0": x0,
                        "y0": y0,
                    })
        return entities


# ===================================================================
# LAW-DRIVEN TRAJECTORY GENERATOR
# ===================================================================

@dataclass
class TrajectoryState:
    """Mutable trajectory state container."""
    x: float
    y: float
    renorm: float
    is_flash: bool = False
    memory_y: float = field(default=None)
    switch_state: bool = False
    
    def __post_init__(self):
        if self.memory_y is None:
            self.memory_y = self.y


class TrajectoryGenerator:
    """
    Law-driven trajectory generator.
    No hardcoded event scripts—only physics law evaluation.
    """
    
    def __init__(self, dt: float = 0.05, max_steps: int = 500):
        self.dt = dt
        self.max_steps = max_steps
        self.law = PhysicsLaw()
        
        # Twilight bands for hysteresis (from grid fractions)
        self.twilight_1_lo = PhysicsLaw.N_ROWS * (1/16)     # 1.0
        self.twilight_1_hi = PhysicsLaw.N_ROWS * (7/32)     # 3.5
        self.twilight_2_lo = PhysicsLaw.N_ROWS * (17/32)    # 8.5
        self.twilight_2_hi = PhysicsLaw.N_ROWS * (23/32)    # 11.5
        
        # Funnel detection (for spark trigger)
        self.funnel_x_min = 6.0
        self.funnel_x_max = 10.0
        self.funnel_y_min = 8.0
        
        # Hysteresis tau derived from spark angle
        self.tau_lag = SPARK_ANGLE_DEG / 60.0 / PhysicsLaw.HYST_TAU_SCALE * F_1_32
    
    def _compute_gate_params(self, x: float, y: float) -> Tuple[float, float]:
        """
        Convert grid position (x, y) to (r, q0) for gate evaluation.
        Returns (r, q0) normalized for w_gate/kappa_eff.
        """
        # Normalize to calibrated SH parameter space
        xn = (x - 8.0) / 8.0  # [-1, 1]
        yn = (y - 8.0) / 8.0  # [-1, 1]
        
        # Map to r/q0 space (calibrated)
        r = CALIBRATED_SH_R_STAR + xn * 0.01
        q0 = CALIBRATED_SH_Q0_STAR + yn * 0.02
        
        return r, q0
    
    def _in_twilight_band(self, y: float) -> bool:
        """Check if y is in twilight bands (renorm active)."""
        return ((self.twilight_1_lo <= y <= self.twilight_1_hi) or
                (self.twilight_2_lo <= y <= self.twilight_2_hi))
    
    def _in_spark_funnel(self, x: float, y: float) -> bool:
        """Check if in spark funnel region."""
        return (self.funnel_x_min <= x <= self.funnel_x_max and 
                y >= self.funnel_y_min)
    
    def _hysteresis_step(self, state: TrajectoryState, branch_sign: float) -> None:
        """
        Hysteresis lag update.
        switch_state toggles based on memory vs current position.
        """
        # Update memory with lag
        state.memory_y += branch_sign * (state.y - state.memory_y) * self.tau_lag
        
        # Switch thresholds based on gate weight
        r, q0 = self._compute_gate_params(state.x, state.y)
        w = self.law.gate_weight(r, q0)
        
        threshold_on = PhysicsLaw.THRESHOLD_ON_FACTOR * (1.0 - w * 0.5)
        threshold_off = PhysicsLaw.THRESHOLD_OFF_FACTOR * (1.0 - w * 0.3)
        
        if not state.switch_state:
            if abs(state.y - state.memory_y) > threshold_on:
                state.switch_state = True
        else:
            if abs(state.y - state.memory_y) < threshold_off:
                state.switch_state = False
    
    def generate_trajectory(
        self, 
        mbti: str, 
        blood: str, 
        gender: str, 
        branch: str
    ) -> Tuple[List[Tuple[float, float, float, bool]], List[Dict]]:
        """
        Generate trajectory for one entity using only physics laws.
        
        Args:
            mbti: MBTI type
            blood: Blood type
            gender: 'F' or 'M'
            branch: 'sunrise' or 'nightfall'
            
        Returns:
            (pts, flash_events): trajectory points and flash event log
        """
        x0, y0 = GridLayout.get_start_position(mbti, blood, gender)
        state = TrajectoryState(x=x0, y=y0, renorm=1.0)
        
        pts = [(float(state.x), float(state.y), float(state.renorm), False)]
        flash_events = []
        
        branch_sign = +1.0 if branch == "sunrise" else -1.0
        
        for step in range(self.max_steps):
            # 1. Compute gate parameters
            r, q0 = self._compute_gate_params(state.x, state.y)
            w_gate_val = self.law.gate_weight(r, q0)
            kappa = self.law.kappa_effective(r, q0)
            
            # 2. Hysteresis step
            self._hysteresis_step(state, branch_sign)
            
            # 3. Flow step (physics field)
            dx, dy = self.law.triple_basin_field(state.x, state.y, gender, w_gate_val)
            
            # Apply anisotropic speed
            speed_factor = (PhysicsLaw.MALE_VERTICAL_SPEED if gender == "M" 
                           else PhysicsLaw.FEMALE_VERTICAL_SPEED)
            
            state.x += dx * self.dt * w_gate_val
            state.y += dy * self.dt * speed_factor * branch_sign
            
            # 4. Spark detection and refraction
            in_funnel = self._in_spark_funnel(state.x, state.y)
            
            if in_funnel and state.switch_state:
                # TRIGGER SPARK
                x_new, y_new, x_comp = self.law.spark_refraction(state.x, state.y)
                
                flash_events.append({
                    "step": step,
                    "x_before": state.x,
                    "y_before": state.y,
                    "x_after": x_new,
                    "y_after": y_new,
                    "x_compressed": x_comp,
                    "w_gate": w_gate_val,
                    "kappa": kappa,
                })
                
                state.x = x_new
                state.y = y_new
                state.is_flash = True
            else:
                state.is_flash = False
            
            # 5. Renorm update (in twilight bands)
            if self._in_twilight_band(state.y):
                state.renorm = self.law.renorm_step(state.renorm, w_gate_val, kappa)
            
            # 6. Boundary clamp
            state.x = max(0.0, min(float(PhysicsLaw.N_COLS), state.x))
            state.y = max(0.0, min(float(PhysicsLaw.N_ROWS), state.y))
            
            pts.append((float(state.x), float(state.y), float(state.renorm), state.is_flash))
        
        return pts, flash_events
    
    def generate_all_trajectories(self) -> Dict[str, Any]:
        """Generate trajectories for all 128 entities."""
        all_trajectories = {}
        all_flash_events = {}
        
        entities = GridLayout.generate_all_entities()
        
        for entity in entities:
            key = f"{entity['mbti']}_{entity['blood']}_{entity['gender']}"
            
            # Sunrise branch
            pts_sunrise, flashes_sunrise = self.generate_trajectory(
                entity['mbti'], entity['blood'], entity['gender'], 'sunrise'
            )
            
            # Nightfall branch
            pts_nightfall, flashes_nightfall = self.generate_trajectory(
                entity['mbti'], entity['blood'], entity['gender'], 'nightfall'
            )
            
            all_trajectories[key] = {
                "sunrise": pts_sunrise,
                "nightfall": pts_nightfall,
                "entity": entity,
            }
            all_flash_events[key] = {
                "sunrise": flashes_sunrise,
                "nightfall": flashes_nightfall,
            }
        
        return {
            "trajectories": all_trajectories,
            "flash_events": all_flash_events,
            "metadata": {
                "dt": self.dt,
                "max_steps": self.max_steps,
                "law_version": "2026.03.07",
                "physics": {
                    "spark_angle_deg": SPARK_ANGLE_DEG,
                    "spark_leap_dist": SPARK_LEAP_DIST,
                    "compression_gap": F_3_32,
                    "kappa_tda_mid": KAPPA_TDA_MID,
                    "gate_alpha": GATE_ALPHA,
                }
            }
        }


# ===================================================================
# VISUALIZATION (Python side - shader replaces this in browser)
# ===================================================================

def visualize_grid(trajectory_data: Dict, output_path: str = "unified_grid.png"):
    """Visualize the grid using matplotlib (for Python-side verification)."""
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib not available, skipping visualization.")
        return
    
    fig, ax = plt.subplots(figsize=(16, 16))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_aspect('equal')
    ax.set_title(f"Unified 128-Type Grid (Law-Driven)\nSpark: {SPARK_ANGLE_DEG}°, Leap: {SPARK_LEAP_DIST}")
    
    # Draw grid
    for i in range(17):
        ax.axhline(i, color='#333333', linewidth=0.5, alpha=0.3)
        ax.axvline(i, color='#333333', linewidth=0.5, alpha=0.3)
    
    # Color map
    blood_colors = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}
    
    # Draw trajectories
    for key, data in trajectory_data["trajectories"].items():
        entity = data["entity"]
        color = blood_colors[entity["blood"]]
        
        # Sunrise branch
        pts_sunrise = data["sunrise"]
        xs_s = [p[0] for p in pts_sunrise]
        ys_s = [p[1] for p in pts_sunrise]
        ax.plot(xs_s, ys_s, color=color, linewidth=0.8, alpha=0.6)
        
        # Flash points
        for p in pts_sunrise:
            if p[3]:  # is_flash
                ax.scatter(p[0], p[1], c='white', s=20, zorder=5)
    
    # Legend
    legend_patches = [mpatches.Patch(color=c, label=b) for b, c in blood_colors.items()]
    ax.legend(handles=legend_patches, loc='upper right')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor='black')
    print(f"Saved visualization to {output_path}")


# ===================================================================
# MAIN ENTRY
# ===================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("UNIFIED 128-GRID LAW-DRIVEN ENGINE")
    print("=" * 60)
    print(f"Physics Constants:")
    print(f"  SPARK_ANGLE_DEG = {SPARK_ANGLE_DEG}")
    print(f"  SPARK_LEAP_DIST = {SPARK_LEAP_DIST}")
    print(f"  COMPRESSION_GAP = {F_3_32} (3/32)")
    print(f"  KAPPA_TDA_MID = {KAPPA_TDA_MID} (1/32)")
    print(f"  GATE_ALPHA = {GATE_ALPHA}")
    print()
    
    # Generate trajectories
    generator = TrajectoryGenerator(dt=0.05, max_steps=500)
    print("Generating trajectories for all 128 entities...")
    trajectory_data = generator.generate_all_trajectories()
    
    # Count flashes
    total_flashes = sum(
        len(f["sunrise"]) + len(f["nightfall"])
        for f in trajectory_data["flash_events"].values()
    )
    print(f"Total spark events: {total_flashes}")
    
    # Save JSON export (for shader consumption)
    json_path = "unified_trajectories.json"
    with open(json_path, 'w') as f:
        # Convert to serializable format
        json.dump(trajectory_data, f, indent=2, default=str)
    print(f"Saved trajectory data to {json_path}")
    
    # Visualize
    visualize_grid(trajectory_data, "unified_128_grid.png")
    
    print()
    print("Engine ready. Run shader for >60 FPS browser visualization.")
