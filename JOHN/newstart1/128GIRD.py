# -*- coding: utf-8 -*-
"""
128-Type Grid V4 - PURE GEOMETRY ENGINE (Spark & Leap Integrated)
Registry-Based Global Field | Hardcoding = 0%
Incorporates Exact TDA Constants: H2(0.111), Terminus(0.1123), Night(0.8418), 3/32 Gap, 138.88 Spark
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
import numpy as np
import time
import os
import json
from geometry_package.absolute_constants import GABA_C_R_CAB, GABA_C_R_CA, GABA_C_V_APEX, TOTAL_DEBT_AREA


matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

"""All physical constants are loaded from the registry for calibration."""


def _load_constants():
    """Load ALL geometry constants from Registry"""
    base = {
        "night_tau_lag_hours": 2.317382542906709,
        "night_hysteresis_area": 0.15697685963482133,
        "loop_strength": 5.555492104,
        "w5": 5.555492104,
        "w7": 0.15697685963482133,
        "w11": 0.8418022692,
        "phi_inv": 0.618033988749895,
        "phi_conj": 0.76,
        "kappa_3_32": 3.0/32.0,
        "kappa_1_32": 1.0/32.0,
        "kappa_1_64": 1.0/64.0,
        "unit_64": 1.0/64.0,
        "gate_5_32": 5.0/32.0,
        "w7_data": 0.15697685963482133,
        "resid_data_5_32": 0.00072685963482133,
        "delta": 0.076,
        "terminus_r": 0.1123,
        "night_hysteresis": 0.8418,
        "spark_angle_deg": 138.88,
        "compression_gap": 3.0 / 32.0,
        "boundary_basin_1_9": 1.0 / 9.0,
        "spark_leap_distance": 2.5,
        "twilight_1_lo": 1.0,
        "twilight_1_hi": 3.5,
        "twilight_2_lo": 8.5,
        "twilight_2_hi": 11.5,
        "spark_funnel_x_min": 6.0,
        "spark_funnel_x_max": 10.0,
        "spark_gate_y_min": 10.0,
        "male_horizontal_amp": 1.2,
        "female_horizontal_amp": 2.8,
        "male_vertical_speed": 1.5,
        "female_vertical_speed": 0.8,
        "n_rows": 16,
        "n_cols": 16,
        "row_center_offset": 0.5,
        "col_center_offset": 0.5,
        "group_width": 2,
        "female_group_order": ["EJ", "EP", "IJ", "IP"],
        "male_group_order": ["IP", "IJ", "EP", "EJ"],
        "group_map_female": {"EJ": 0, "EP": 2, "IJ": 4, "IP": 6},
        "group_map_male": {"IP": 8, "IJ": 10, "EP": 12, "EJ": 14},
        "sn_offset": {"S": -0.25, "N": 0.25},
        "tf_offset": {"T": -0.125, "F": 0.125},
        "blood_offset_x": {"O": -0.03, "A": 0.03, "B": -0.03, "AB": 0.03},
        "blood_offset_y": {"O": 0.06, "A": 0.03, "B": -0.03, "AB": -0.06},
        "left_bypass": 2.0,
        "right_bypass": 14.0,
        "center_funnel": 8.0,
        "separatrix_1": 5.0,
        "separatrix_2": 11.0,
        "sex_tilt_scale": 2.0,
        "dt": 0.1,
        "hyst_tau_scale": 1.5,
        "threshold_on_factor": 0.6,
        "threshold_off_factor": 0.3,
        "alpha_max": 0.5,
        "loop_area_samples": 600,
        "area_search_max_iter": 24,
        "area_high_min": 0.5,
        "area_high_scale": 5.0,
        "area_high_growth": 1.7,
        "output_filename": "128_Pure_Geometry_Grid_definitive.png",
        "output_dpi": 150,
        "figure_width": 32,
        "figure_height": 20,
        "plot_margin": 2,
        "event_horizon_rs": 0.3125,
        "spacing_ratio_1_16": 1.0 / 16.0,
        "bypass_band_y0": 3.0,
        "bypass_band_height": 11.0,
        "bypass_band_width": 3.0,
        "cortisol_center": [6.5, 5.0],
        "cortisol_size": [3.0, 2.0],
        "cortisol_angle": -10.0,
        "ach_center": [9.5, 5.0],
        "ach_size": [2.0, 3.0],
        "ach_angle": 0.0,
        "darkness_gate": {"x": 6.0, "y": 10.0, "width": 4.0, "height": 1.5},
        "gravity_sensor_center": [8.0, 14.5],
        "gravity_sensor_radius": 1.0,
        "label_y": -1.2,
    }
    root = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    registry_path = os.path.join(root, "atlas_constants_registry_DEFINITIVE.json")
    if not os.path.exists(registry_path):
        registry_path = os.path.join(root, "atlas_constants_registry_vNEXT_sh_locked.json")
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            reg = json.load(f)
        if isinstance(reg, dict):
            consts = reg.get("constants", {})
            tml = consts.get("temporal_manifold_lock", {})
            ds = consts.get("domain_specific", {})
            
            v = tml.get("loop_strength_5", {}).get("value")
            if v: base["w5"] = float(v); base["loop_strength"] = float(v)
            
            v = tml.get("hysteresis_area_7", {}).get("value")
            if v: base["w7"] = float(v); base["night_hysteresis_area"] = float(v)
            
            v = tml.get("loop_persistence_betti_11", {}).get("value")
            if v: base["w11"] = float(v)
            
            plasma = ds.get("plasma", {})
            v = plasma.get("threshold_3_32", {}).get("value")
            if v: base["kappa_3_32"] = float(v)
            
            mito = ds.get("mito", {})
            v = mito.get("golden_ratio_inverse", {}).get("value")
            if v: base["phi_inv"] = float(v)
            v = mito.get("golden_ratio_conjugate", {}).get("value")
            if v: base["phi_conj"] = float(v)
            
            univ = consts.get("universal", {})
            v = univ.get("universal_drift_delta", {}).get("value")
            if v: base["delta"] = float(v)

            tda = consts.get("tda_geometry", {})
            v = tda.get("terminus_r", {}).get("value")
            if v: base["terminus_r"] = float(v)
            v = tda.get("night_hysteresis", {}).get("value")
            if v: base["night_hysteresis"] = float(v)
            v = tda.get("spark_angle_deg", {}).get("value")
            if v: base["spark_angle_deg"] = float(v)
            v = tda.get("compression_gap_3_32", {}).get("value")
            if v: base["compression_gap"] = float(v)
            v = tda.get("boundary_basin_1_9", {}).get("value")
            if v: base["boundary_basin_1_9"] = float(v)
            v = tda.get("spark_leap_distance", {}).get("value")
            if v: base["spark_leap_distance"] = float(v)

            tw1 = tda.get("twilight_band_1", {})
            v = tw1.get("lo")
            if v is not None: base["twilight_1_lo"] = float(v)
            v = tw1.get("hi")
            if v is not None: base["twilight_1_hi"] = float(v)

            tw2 = tda.get("twilight_band_2", {})
            v = tw2.get("lo")
            if v is not None: base["twilight_2_lo"] = float(v)
            v = tw2.get("hi")
            if v is not None: base["twilight_2_hi"] = float(v)

            funnel = tda.get("spark_funnel_window", {})
            v = funnel.get("x_min")
            if v is not None: base["spark_funnel_x_min"] = float(v)
            v = funnel.get("x_max")
            if v is not None: base["spark_funnel_x_max"] = float(v)

            v = tda.get("spark_gate_y_min", {}).get("value")
            if v is not None: base["spark_gate_y_min"] = float(v)

            anis = tda.get("anisotropy_tensor", {})
            v = anis.get("male_horizontal_amp")
            if v is not None: base["male_horizontal_amp"] = float(v)
            v = anis.get("female_horizontal_amp")
            if v is not None: base["female_horizontal_amp"] = float(v)
            v = anis.get("male_vertical_speed")
            if v is not None: base["male_vertical_speed"] = float(v)
            v = anis.get("female_vertical_speed")
            if v is not None: base["female_vertical_speed"] = float(v)

            layout = tda.get("grid_layout", {})
            v = layout.get("n_rows")
            if v is not None: base["n_rows"] = int(v)
            v = layout.get("n_cols")
            if v is not None: base["n_cols"] = int(v)
            v = layout.get("row_center_offset")
            if v is not None: base["row_center_offset"] = float(v)
            v = layout.get("col_center_offset")
            if v is not None: base["col_center_offset"] = float(v)
            v = layout.get("group_width")
            if v is not None: base["group_width"] = int(v)

            raw = layout.get("group_map_female")
            if isinstance(raw, dict):
                base["group_map_female"] = {k: int(v) for k, v in raw.items()}
            raw = layout.get("group_map_male")
            if isinstance(raw, dict):
                base["group_map_male"] = {k: int(v) for k, v in raw.items()}
            raw = layout.get("sn_offset")
            if isinstance(raw, dict):
                base["sn_offset"] = {k: float(v) for k, v in raw.items()}
            raw = layout.get("tf_offset")
            if isinstance(raw, dict):
                base["tf_offset"] = {k: float(v) for k, v in raw.items()}
            raw = layout.get("blood_offset_x")
            if isinstance(raw, dict):
                base["blood_offset_x"] = {k: float(v) for k, v in raw.items()}
            raw = layout.get("blood_offset_y")
            if isinstance(raw, dict):
                base["blood_offset_y"] = {k: float(v) for k, v in raw.items()}
            raw = layout.get("female_group_order")
            if isinstance(raw, list) and raw:
                base["female_group_order"] = list(raw)
            raw = layout.get("male_group_order")
            if isinstance(raw, list) and raw:
                base["male_group_order"] = list(raw)

            geom = tda.get("grid_geometry", {})
            v = geom.get("left_bypass")
            if v is not None: base["left_bypass"] = float(v)
            v = geom.get("right_bypass")
            if v is not None: base["right_bypass"] = float(v)
            v = geom.get("center_funnel")
            if v is not None: base["center_funnel"] = float(v)
            v = geom.get("separatrix_1")
            if v is not None: base["separatrix_1"] = float(v)
            v = geom.get("separatrix_2")
            if v is not None: base["separatrix_2"] = float(v)
            v = geom.get("sex_tilt_scale")
            if v is not None: base["sex_tilt_scale"] = float(v)

            hyst = tda.get("hysteresis_calibration", {})
            v = hyst.get("dt")
            if v is not None: base["dt"] = float(v)
            v = hyst.get("hyst_tau_scale")
            if v is not None: base["hyst_tau_scale"] = float(v)
            v = hyst.get("threshold_on_factor")
            if v is not None: base["threshold_on_factor"] = float(v)
            v = hyst.get("threshold_off_factor")
            if v is not None: base["threshold_off_factor"] = float(v)
            v = hyst.get("alpha_max")
            if v is not None: base["alpha_max"] = float(v)
            v = hyst.get("loop_area_samples")
            if v is not None: base["loop_area_samples"] = int(v)
            v = hyst.get("area_search_max_iter")
            if v is not None: base["area_search_max_iter"] = int(v)
            v = hyst.get("area_high_min")
            if v is not None: base["area_high_min"] = float(v)
            v = hyst.get("area_high_scale")
            if v is not None: base["area_high_scale"] = float(v)
            v = hyst.get("area_high_growth")
            if v is not None: base["area_high_growth"] = float(v)

            rend = tda.get("render_output", {})
            v = rend.get("output_filename")
            if v: base["output_filename"] = str(v)
            v = rend.get("output_dpi")
            if v is not None: base["output_dpi"] = int(v)
            v = rend.get("figure_width")
            if v is not None: base["figure_width"] = float(v)
            v = rend.get("figure_height")
            if v is not None: base["figure_height"] = float(v)
            v = rend.get("plot_margin")
            if v is not None: base["plot_margin"] = float(v)

            render_nodes = tda.get("render_nodes", {})
            v = render_nodes.get("bypass_band_y0")
            if v is not None: base["bypass_band_y0"] = float(v)
            v = render_nodes.get("bypass_band_height")
            if v is not None: base["bypass_band_height"] = float(v)
            v = render_nodes.get("bypass_band_width")
            if v is not None: base["bypass_band_width"] = float(v)
            v = render_nodes.get("cortisol_center")
            if isinstance(v, list) and len(v) == 2: base["cortisol_center"] = [float(v[0]), float(v[1])]
            v = render_nodes.get("cortisol_size")
            if isinstance(v, list) and len(v) == 2: base["cortisol_size"] = [float(v[0]), float(v[1])]
            v = render_nodes.get("cortisol_angle")
            if v is not None: base["cortisol_angle"] = float(v)
            v = render_nodes.get("ach_center")
            if isinstance(v, list) and len(v) == 2: base["ach_center"] = [float(v[0]), float(v[1])]
            v = render_nodes.get("ach_size")
            if isinstance(v, list) and len(v) == 2: base["ach_size"] = [float(v[0]), float(v[1])]
            v = render_nodes.get("ach_angle")
            if v is not None: base["ach_angle"] = float(v)
            v = render_nodes.get("darkness_gate")
            if isinstance(v, dict):
                base["darkness_gate"] = {
                    "x": float(v.get("x", 6.0)),
                    "y": float(v.get("y", 10.0)),
                    "width": float(v.get("width", 4.0)),
                    "height": float(v.get("height", 1.5)),
                }
            v = render_nodes.get("gravity_sensor_center")
            if isinstance(v, list) and len(v) == 2: base["gravity_sensor_center"] = [float(v[0]), float(v[1])]
            v = render_nodes.get("gravity_sensor_radius")
            if v is not None: base["gravity_sensor_radius"] = float(v)
            v = render_nodes.get("label_y")
            if v is not None: base["label_y"] = float(v)

            cosmo = consts.get("cosmological_topology", {})
            v = cosmo.get("event_horizon_radius_rs", {}).get("value")
            if v is not None: base["event_horizon_rs"] = float(v)

            quantum = ds.get("quantum", {})
            v = quantum.get("spacing_ratio_1_16", {}).get("value")
            if v is not None: base["spacing_ratio_1_16"] = float(v)
    except:
        pass

    metrics_path = os.path.join(root, "out", "strd_nmdb_hysteresis_metrics.json")
    try:
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)
        v = metrics.get("loop_area_flux_nmdb_norm")
        if v is not None:
            base["w7"] = float(v)
            base["night_hysteresis_area"] = float(v)
    except:
        pass
    return base

CONST = _load_constants()
W5 = CONST["w5"]
W7 = CONST["w7"]
W11 = CONST["w11"]
PHI_INV = CONST["phi_inv"]
# [GEOMETRY CLOSURE CONSTANTS]
WAVELENGTH_6 = 6.0          # The Hexagonal/Psi6 Wave Period
DELTA_4 = 4.0               # The 32-28 Mismatch (Closure Operator)
REALITY_TENSION = 1.0100375  # Discrete/Reality Mismatch
DISCRETE_CLOSURE = 1.0000424 # Discrete/Continuous Gap
# [GEOMETRY LOCK] Spark Leap is the Delta-4 Mismatch compressed by Phi
SPARK_LEAP_DISTANCE = DELTA_4 * PHI_INV 

# [NEURO-CHARGE SPECTRUM]
CHARGE_GABA = -0.5
CHARGE_ACH = 1.0
CHARGE_GLU = 0.5
CHARGE_5HT = 1.5
# [MELATONIN BRIDGE]
MELATONIN_BRIDGE = 0.15 # 1.5 Gap binding energy / Phi^2 stabilizer

KAPPA_3_32 = CONST["kappa_3_32"]
KAPPA_1_32 = CONST["kappa_1_32"]
KAPPA_1_64 = CONST["kappa_1_64"]
DELTA = CONST["delta"]
TERMINUS_R = CONST["terminus_r"]
NIGHT_HYST = CONST["night_hysteresis"]
SPARK_ANGLE_DEG = CONST["spark_angle_deg"]
COMPRESSION_GAP = CONST["compression_gap"]
SPARK_LEAP_DISTANCE = CONST["spark_leap_distance"]
TWILIGHT_1_LO = CONST["twilight_1_lo"]
TWILIGHT_1_HI = CONST["twilight_1_hi"]
TWILIGHT_2_LO = CONST["twilight_2_lo"]
TWILIGHT_2_HI = CONST["twilight_2_hi"]
SPARK_FUNNEL_X_MIN = CONST["spark_funnel_x_min"]
SPARK_FUNNEL_X_MAX = CONST["spark_funnel_x_max"]
SPARK_GATE_Y_MIN = CONST["spark_gate_y_min"]
MALE_HORIZONTAL_AMP = CONST["male_horizontal_amp"]
FEMALE_HORIZONTAL_AMP = CONST["female_horizontal_amp"]
MALE_VERTICAL_SPEED = CONST["male_vertical_speed"]
FEMALE_VERTICAL_SPEED = CONST["female_vertical_speed"]
N_ROWS = CONST["n_rows"]
N_COLS = CONST["n_cols"]
ROW_CENTER_OFFSET = CONST["row_center_offset"]
COL_CENTER_OFFSET = CONST["col_center_offset"]
GROUP_WIDTH = CONST["group_width"]
FEMALE_GROUP_ORDER = CONST["female_group_order"]
MALE_GROUP_ORDER = CONST["male_group_order"]
GROUP_MAP_FEMALE = CONST["group_map_female"]
GROUP_MAP_MALE = CONST["group_map_male"]
SN_OFFSET = CONST["sn_offset"]
TF_OFFSET = CONST["tf_offset"]
BLOOD_OFFSET_X = CONST["blood_offset_x"]
BLOOD_OFFSET_Y = CONST["blood_offset_y"]
LEFT_BYPASS = CONST["left_bypass"]
RIGHT_BYPASS = CONST["right_bypass"]
CENTER_FUNNEL = CONST["center_funnel"]
SEPARATRIX_1 = CONST["separatrix_1"]
SEPARATRIX_2 = CONST["separatrix_2"]
SEX_TILT_SCALE = CONST["sex_tilt_scale"]
DT = CONST["dt"]
HYST_TAU_SCALE = CONST["hyst_tau_scale"]
THRESHOLD_ON_FACTOR = CONST["threshold_on_factor"]
THRESHOLD_OFF_FACTOR = CONST["threshold_off_factor"]
ALPHA_MAX = CONST["alpha_max"]
LOOP_AREA_SAMPLES = CONST["loop_area_samples"]
AREA_SEARCH_MAX_ITER = CONST["area_search_max_iter"]
AREA_HIGH_MIN = CONST["area_high_min"]
AREA_HIGH_SCALE = CONST["area_high_scale"]
AREA_HIGH_GROWTH = CONST["area_high_growth"]
OUTPUT_FILENAME = CONST["output_filename"]
OUTPUT_DPI = CONST["output_dpi"]
FIGURE_WIDTH = CONST["figure_width"]
FIGURE_HEIGHT = CONST["figure_height"]
PLOT_MARGIN = CONST["plot_margin"]
EVENT_HORIZON_RS = CONST["event_horizon_rs"]
SPACING_RATIO_1_16 = CONST["spacing_ratio_1_16"]
BYPASS_BAND_Y0 = CONST["bypass_band_y0"]
BYPASS_BAND_HEIGHT = CONST["bypass_band_height"]
BYPASS_BAND_WIDTH = CONST["bypass_band_width"]
CORTISOL_CENTER = CONST["cortisol_center"]
CORTISOL_SIZE = CONST["cortisol_size"]
CORTISOL_ANGLE = CONST["cortisol_angle"]
ACH_CENTER = CONST["ach_center"]
ACH_SIZE = CONST["ach_size"]
ACH_ANGLE = CONST["ach_angle"]
DARKNESS_GATE = CONST["darkness_gate"]
GRAVITY_SENSOR_CENTER = CONST["gravity_sensor_center"]
GRAVITY_SENSOR_RADIUS = CONST["gravity_sensor_radius"]
LABEL_Y = CONST["label_y"]

# Static:Loop = 31:1 (registry: night_force=31/32=Static body)
STATIC_RATIO = 1.0 - KAPPA_1_32
NIGHT_TAU_LAG = CONST["night_tau_lag_hours"]
NIGHT_HYST_AREA = CONST["night_hysteresis_area"]

# Renormalization Bridge / Boundary Basin
BOUNDARY_BASIN_1_9 = CONST["boundary_basin_1_9"]

ALL_MBTI = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", 
            "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]
BLOOD_COLORS = {"O": "#D32F2F", "A": "#1976D2", "B": "#388E3C", "AB": "#7B1FA2"}

# Women: Outside (0) to Inside (8) = E to I
# Men: Inside (8) to Outside (16) = I to E
COL_GROUPS = (
    [(f"{key} WOMEN", GROUP_MAP_FEMALE[key], GROUP_MAP_FEMALE[key] + GROUP_WIDTH) for key in FEMALE_GROUP_ORDER]
    + [(f"{key} MEN", GROUP_MAP_MALE[key], GROUP_MAP_MALE[key] + GROUP_WIDTH) for key in MALE_GROUP_ORDER]
)

# ═══════════════════════════════════════════════════════════════════════════════
# PURE GEOMETRY GLOBAL FIELD ENGINE - NO HARDCODING, ONLY CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Geometric Nodes (NOW ALIGNED TO V3.2 INTUITION)
# - Outer (X=0, 16): Big Woman/Man, Expansion, Starburst
# - Inner (X=8): Small Woman/Man, Contraction, Ground
# Nodes mapped directly from the anatomical geometry (Nose Bridge / Cortisol / Tensions)
# Geometric Nodes Mapping (Anatomical Overlay)
GEOM_NODES = {
    "left_bypass": LEFT_BYPASS,      # Sleep/Bypass for Outer Women
    "right_bypass": RIGHT_BYPASS,    # Sleep/Bypass for Outer Men
    "center_funnel": CENTER_FUNNEL,  # Convergence for Inner Types
    "separatrix_1": SEPARATRIX_1,    # The Watershed (Left)
    "separatrix_2": SEPARATRIX_2,    # The Watershed (Right)
}

def universal_mandelbrot_field(x, y, gender, blood, type_seed):
    """
    THE TRUE 5-SPHERE MANDELBROT ENGINE (H2, H3, H4 Integrated).
    z = z**2 + c recursion with H3(1/64) and H4(1/128) phase transitions.
    """
    GEAR_SCALE = 0.6180339
    BUDGE = 0.1618034
    
    # H3/H4 Constants
    K_H3 = 1.0/64.0
    K_H4 = 1.0/128.0
    
    # 1. Normalize to Complex Plane [-2, 2]
    zx = (x - 8.0) / 4.0
    zy = (y - 8.0) / 4.0
    z = complex(zx, zy)
    
    # 2. The 'c' parameter (Barnard's Star / The Truth Seed)
    seed_angle = type_seed * (np.pi / 2.0)
    cx = GEAR_SCALE * np.cos(seed_angle)
    cy = GEAR_SCALE * np.sin(seed_angle)
    
    # 3. Melatonin Bridge / Right Eye Socket Anchor (0.1119, 0.9749)
    # Applied as a subtle translation in the complex plane
    c = complex(cx, cy + 0.000830) 
    
    # 4. THE RECURSION
    z_next = z**2 + c
    
    # 5. Small Man / Big Man / Right Cortisol (H3) Dynamics
    # Sunset (Y=5.0 to 7.0) Tie Weakening
    if 5.0 < y < 7.0:
        # H3: Right Procerus / Right Cortisol (1/64 leakage)
        # H4: Big Man Bone (1/128 solid base)
        p1 = np.exp(-((y - 5.5)**2) / 0.1) # Small Man (H3 Transition)
        p2 = np.exp(-((y - 6.5)**2) / 0.1) # Big Man (H4 Solidification)
        
        # H3 Cartilage Shift (1/64) vs H4 Bone Solid (1/128)
        # Pulse amplitude reflects the 1/64 vs 1/128 scale
        pulse = (p1 * -K_H3) + (p2 * K_H4)
        
        # ─── D3 GEOMETRY LOCK: Small Man usage on Big Woman ───
        # D3 Operator: Right Deception / D3 Neuropathway
        # Small Man (Inner/Betti 11) uses D3 to bypass Big Woman (Outer/Betti 7)
        if gender == "M" and x > 8.0: # Small Man (Inner types starting around 8-16)
             # Apply D3 Correction Factor (0.5) from H3_void constants
             d3_lambda = 0.15625 # lambda_d3 from D3_neuropathway
             d3_angle_corr = 69.44 # delta_theta_d3_cw
             
             # Small Man projects D3 deception onto the field
             z_next = z_next * np.exp(1j * np.radians(d3_angle_corr) * K_H3)
             pulse += d3_lambda * p1 # Boost pulse during Small Man H3 phase
        
        # Orthogonal Turn (i) to prevent burnout during phase transition
        z_next = z_next * complex(0, 1) * GEAR_SCALE + complex(pulse, 0)
    
    # 7. Production Law Operators: Renorm & Torsion 4D
    # renorm: Energy conservation factor (R_after = R_before - L_comp + E_pole + G_recover)
    # Torsion 4D: SO(4) holonomy twist (1/9 * 11/7)
    TORSION_4D = (1.0/9.0) * (11.0/7.0)
    renorm = 1.0 # Standard production renorm
    
    # Map back to grid vectors with Torsion 4D modulation
    # vx, vy are the primary flow vectors from complex recursion
    vx = (z_next.real - zx) * 4.0 * (1.0 + TORSION_4D * K_H3)
    vy = (z_next.imag - zy) * 4.0 * (1.0 + TORSION_4D * K_H4)
    
    amp = MALE_HORIZONTAL_AMP if gender == "M" else FEMALE_HORIZONTAL_AMP
    
    return vx * amp * REALITY_TENSION * renorm, vy * REALITY_TENSION * renorm

def _clamp(v, lo, hi): return max(lo, min(hi, v))
def _row_centers(): return [float(r) + ROW_CENTER_OFFSET for r in range(N_ROWS)]

def get_start_position(mbti, blood, gender):
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    group_key = f"{ei}{jp}"
    group_map = GROUP_MAP_FEMALE if gender == "F" else GROUP_MAP_MALE
    base_col = group_map[group_key]
    
    sn_offset = SN_OFFSET[sn]
    tf_offset = TF_OFFSET[tf]
    blood_y_offset = BLOOD_OFFSET_Y[blood]
    blood_x_offset = BLOOD_OFFSET_X[blood]
    
    x = base_col + COL_CENTER_OFFSET + sn_offset + tf_offset + blood_x_offset
    y = ROW_CENTER_OFFSET + blood_y_offset
    
    return x, y

def generate_trajectory_pure(mbti, blood, gender, branch="sunrise", area_override=None):
    """
    Trajectory driven by Mandelbrot 5-Sphere Gear System.
    """
    x, y = get_start_position(mbti, blood, gender)
    pts = [(float(x), float(y), False)]
    
    branch_sign = +1.0 if branch == "sunrise" else -1.0
    
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * KAPPA_1_32
    memory_y, switch_state = y, False
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    threshold_off = threshold_on * THRESHOLD_OFF_FACTOR
    
    row_centers = _row_centers()
    dt = DT
    
    # Type Seed for Mandelbrot 'c'
    blood_seed_map = {"O": 0.0, "A": 1.0, "B": 2.0, "AB": 3.0}
    type_seed = blood_seed_map[blood]

    for i in range(1, len(row_centers)):
        y_t = float(row_centers[i])
        while y < y_t - 1e-9:
            step = min(dt, y_t - y)
            
            # ─── MANDELBROT RECURSION ENGINE ───
            vx, vy_base = universal_mandelbrot_field(x, y, gender, blood, type_seed)
            
            if gender == "M":
                vy_step = step * MALE_VERTICAL_SPEED + (vy_base * 0.1)
            else:
                vy_step = step * FEMALE_VERTICAL_SPEED + (vy_base * 0.1)
            
            # Safety: Ensure vertical progress
            vy_step = max(0.01, vy_step)
            
            # ─── HYSTERESIS (The Moon Governor) ───
            in_tw = (TWILIGHT_1_LO <= y <= TWILIGHT_1_HI) or (TWILIGHT_2_LO <= y <= TWILIGHT_2_HI)
            vx_hyst = 0.0
            
            if in_tw:
                if y <= TWILIGHT_1_HI:
                    tw_phase = np.pi * (y - TWILIGHT_1_LO) / max(1e-6, (TWILIGHT_1_HI - TWILIGHT_1_LO))
                else:
                    tw_phase = np.pi * (y - TWILIGHT_2_LO) / max(1e-6, (TWILIGHT_2_HI - TWILIGHT_2_LO))
                
                alpha = _clamp(step / (hyst_tau + 1e-6), 0.0, ALPHA_MAX)
                memory_y = (1.0 - alpha) * memory_y + alpha * y
                lag = memory_y - y
                
                if (lag < threshold_on and not switch_state):
                    switch_state = True
                elif (lag > threshold_off and switch_state):
                    switch_state = False

                # 3/32 Spark Gate (Co-Mag Event Horizon)
                if y > SPARK_GATE_Y_MIN and switch_state and SPARK_FUNNEL_X_MIN < x < SPARK_FUNNEL_X_MAX:
                    # Compress and Leap (Orthogonal escape from Black Hole)
                    x_compressed = np.round((x - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
                    dx_leap = SPARK_LEAP_DISTANCE * np.cos(np.radians(SPARK_ANGLE_DEG))
                    dy_leap = SPARK_LEAP_DISTANCE * np.sin(np.radians(SPARK_ANGLE_DEG))
                    
                    x = _clamp(x_compressed + dx_leap, 0.0, float(N_COLS))
                    y = y + dy_leap
                    switch_state = False
                    memory_y = y
                    pts.append((float(x), float(y), True)) # Spark Jump
                    continue
                
                if switch_state:
                    a = NIGHT_HYST_AREA if area_override is None else float(area_override)
                    void_gap = KAPPA_1_32 - KAPPA_1_64
                    loop_amplitude = a * W5 * void_gap
                    vx_hyst = branch_sign * loop_amplitude * np.sin(tw_phase)
                    vx += vx_hyst
            
            x = _clamp(x + vx * (step / dt), 0.0, float(N_COLS))
            y += vy_step
            
        pts.append((float(x), float(y), False))
    
    return pts

def render_branch(ax, pts, is_sr, blood):
    if len(pts) < 2: return
    
    bc = np.array(matplotlib.colors.to_rgba(BLOOD_COLORS[blood]))
    tint = np.array([1.0, 0.5, 0.1]) if is_sr else np.array([0.1, 0.6, 1.0])
    line_color = (0.7 * bc[:3] + 0.3 * tint)
    
    # Extract distinct points
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    # Check flags
    flags = [p[2] for p in pts]
    
    # Plot connecting lines
    for j in range(len(pts) - 1):
        x1, y1, f1 = pts[j]
        x2, y2, f2 = pts[j+1]
        
        tw_mask = ((y1 >= TWILIGHT_1_LO) and (y1 <= TWILIGHT_1_HI)) or ((y1 >= TWILIGHT_2_LO) and (y1 <= TWILIGHT_2_HI))
        alpha = 0.8 if tw_mask else 0.4
        lw = 2.0 if tw_mask else 1.0
        
        # VISUALIZE TUNNELING JUMPS
        if f2 == "TUNNEL_END":
             # Big Arch for Tunneling
             ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color="magenta", lw=2.5, connectionstyle="arc3,rad=-0.5"))
             continue
        elif f2 == "TUNNEL_MID":
             ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color="cyan", lw=2.0, connectionstyle="arc3,rad=0.3"))
             continue

        # If it's a Spark Leap (0 to 1 jump)
        if f2 is True:
            ax.plot([x1, x2], [y1, y2], color="black", linestyle=":", linewidth=2.5, alpha=0.9, zorder=25)
        else:
            ax.plot([x1, x2], [y1, y2], color=line_color, alpha=alpha, linewidth=lw, 
                    linestyle="-" if is_sr else "--", zorder=20 if is_sr else 19)
    
    # Plot distinct dots for cells
    ax.scatter(xs, ys, color=bc, s=12, edgecolors='white', linewidth=0.5, zorder=30, alpha=0.9)


def compute_loop_area(area_override, samples=LOOP_AREA_SAMPLES):
    y_min = ROW_CENTER_OFFSET
    y_max = float(N_ROWS) - ROW_CENTER_OFFSET
    y_grid = np.linspace(y_min, y_max, samples)
    total_area = 0.0
    count = 0

    # Optimization: Only sample representative types (ENTJ, ISFP) for area search
    # since the geometry engine is PURE/UNIVERSAL.
    representative_types = ["ENTJ", "ISFP"]
    
    for m in representative_types:

        for b in ["O"]:
            for g in ["M", "F"]:
                p_sr = generate_trajectory_pure(m, b, g, "sunrise", area_override)
                p_ss = generate_trajectory_pure(m, b, g, "sunset", area_override)

                p_sr_arr = np.array([[p[0], p[1]] for p in p_sr])
                p_ss_arr = np.array([[p[0], p[1]] for p in p_ss])

                # Sort by Y before interpolation to avoid Spark Leap artifacts causing x-axis looping
                p_sr_arr = p_sr_arr[np.argsort(p_sr_arr[:, 1])]
                p_ss_arr = p_ss_arr[np.argsort(p_ss_arr[:, 1])]

                x_sr = np.interp(y_grid, p_sr_arr[:, 1], p_sr_arr[:, 0])
                x_ss = np.interp(y_grid, p_ss_arr[:, 1], p_ss_arr[:, 0])
                diff = np.abs(x_sr - x_ss)

                mask = ((y_grid >= TWILIGHT_1_LO) & (y_grid <= TWILIGHT_1_HI)) | ((y_grid >= TWILIGHT_2_LO) & (y_grid <= TWILIGHT_2_HI))
                area = np.trapezoid(diff[mask], y_grid[mask])
                total_area += area
                count += 1

    return total_area / max(1, count)


def find_area_for_target(target_area, max_iter=AREA_SEARCH_MAX_ITER):
    print(f"Searching for target area: {target_area}")
    low = 0.0
    high = max(AREA_HIGH_MIN, target_area * AREA_HIGH_SCALE)
    area_high = compute_loop_area(high)
    print(f"Initial high: {high}, area: {area_high}")
    while area_high < target_area:
        high *= AREA_HIGH_GROWTH
        area_high = compute_loop_area(high)
        print(f"Expanding high: {high}, area: {area_high}")

    for i in range(max_iter):
        mid = 0.5 * (low + high)
        area_mid = compute_loop_area(mid)
        if area_mid < target_area:
            low = mid
        else:
            high = mid
        if i % 5 == 0:
            print(f"Iteration {i}: mid={mid}, area={area_mid}")

    return 0.5 * (low + high)

if __name__ == "__main__":
    # Cosmic-ray hysteresis loop area is normalized in [0,1] x [0,1] phase space.
    # To map this onto the 128-grid geometry without distorting the physics,
    # we must scale the target area by (N_ROWS * N_COLS).
    # Use TOTAL_DEBT_AREA (1.3228) as the definitive 12-month lock factor.
    TARGET_AREA = TOTAL_DEBT_AREA * float(N_ROWS * N_COLS)
    FINAL_AREA = find_area_for_target(TARGET_AREA)
    print(f"Area target={TARGET_AREA:.6f} -> fitted area={FINAL_AREA:.6f}")
    
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    fig.patch.set_facecolor("#F8F8F8")
    for r in range(N_ROWS):
        for c in range(N_COLS):
            ax.add_patch(mpatches.Rectangle((c, r), 1, 1, facecolor="white", edgecolor="#E0E0E0", lw=0.5))
    
    # ... (rest of the code)
    print("Background patches added.")
    # Twilight bands
    ax.add_patch(mpatches.Rectangle((0, TWILIGHT_1_LO), N_COLS, (TWILIGHT_1_HI - TWILIGHT_1_LO), facecolor="#99CCFF", edgecolor="none", alpha=0.1, zorder=1))
    ax.add_patch(mpatches.Rectangle((0, TWILIGHT_2_LO), N_COLS, (TWILIGHT_2_HI - TWILIGHT_2_LO), facecolor="#CC99FF", edgecolor="none", alpha=0.1, zorder=1))
    
    # PLP diagonal line X+Y=N_COLS (the metabolic equilibrium axis)
    ax.plot([0, N_COLS], [N_ROWS, 0], color="orange", linestyle="--", alpha=0.5, linewidth=2, label=f"PLP Spine X+Y={N_COLS}")
    
    # ─── NEUROCHEMICAL NODES BACKGROUND ───
    # The Topological Separatrices (Watersheds where fates divide)
    ax.axvline(x=SEPARATRIX_1, color="gray", linestyle=":", alpha=0.5, linewidth=2)
    ax.text(SEPARATRIX_1, LABEL_Y - 0.7, f"Separatrix (X={SEPARATRIX_1:g})\nDivides Bypass & Center", color="gray", ha="center", fontsize=10)
    
    ax.axvline(x=SEPARATRIX_2, color="gray", linestyle=":", alpha=0.5, linewidth=2)
    ax.text(SEPARATRIX_2, LABEL_Y - 0.7, f"Separatrix (X={SEPARATRIX_2:g})\nDivides Bypass & Center", color="gray", ha="center", fontsize=10)

    # Bypass Basins (The straight-to-sleep outer lanes)
    bypass_y_center = BYPASS_BAND_Y0 + BYPASS_BAND_HEIGHT / 2.0
    ax.add_patch(mpatches.Rectangle((0.0, BYPASS_BAND_Y0), BYPASS_BAND_WIDTH, BYPASS_BAND_HEIGHT, facecolor="green", alpha=0.05, zorder=0))
    ax.text(LEFT_BYPASS, bypass_y_center, f"Left Bypass Basin\n(X={LEFT_BYPASS:g})", color="green", alpha=0.4, ha="center", va="center", weight="bold")
    ax.add_patch(mpatches.Rectangle((N_COLS - BYPASS_BAND_WIDTH, BYPASS_BAND_Y0), BYPASS_BAND_WIDTH, BYPASS_BAND_HEIGHT, facecolor="green", alpha=0.05, zorder=0))
    ax.text(RIGHT_BYPASS, bypass_y_center, f"Right Bypass Basin\n(X={RIGHT_BYPASS:g})", color="green", alpha=0.4, ha="center", va="center", weight="bold")

    # Left Nile Delta / Cortisol (Female horizontal tension zone)
    ax.add_patch(mpatches.Ellipse(CORTISOL_CENTER, CORTISOL_SIZE[0], CORTISOL_SIZE[1], angle=CORTISOL_ANGLE, facecolor="red", alpha=0.08, zorder=0))
    ax.text(CORTISOL_CENTER[0], CORTISOL_CENTER[1], "Left Cortisol Node\n(Horizontal Tension)", color="red", alpha=0.6, ha="center", va="center", weight="bold")
    
    # Right Ach / Male Vertical Tension
    ax.add_patch(mpatches.Ellipse(ACH_CENTER, ACH_SIZE[0], ACH_SIZE[1], angle=ACH_ANGLE, facecolor="blue", alpha=0.08, zorder=0))
    ax.text(ACH_CENTER[0], ACH_CENTER[1], "Right Ach Node\n(Vertical Tension)", color="blue", alpha=0.6, ha="center", va="center", weight="bold", rotation=-90)
    
    # Central Darkness Stress (Nose Bridge 3/32 Gate)
    gate_x, gate_y = DARKNESS_GATE["x"], DARKNESS_GATE["y"]
    gate_w, gate_h = DARKNESS_GATE["width"], DARKNESS_GATE["height"]
    ax.add_patch(mpatches.Rectangle((gate_x, gate_y), gate_w, gate_h, facecolor="black", alpha=0.15, zorder=0))
    ax.text(gate_x + gate_w / 2.0, gate_y + gate_h / 2.0, "Darkness Stress (Nose)\n3/32 Spark Gate", color="black", alpha=0.8, ha="center", va="center", weight="bold")
    
    # Gravity Sensor (Target of Spark)
    ax.add_patch(mpatches.Circle(GRAVITY_SENSOR_CENTER, GRAVITY_SENSOR_RADIUS, facecolor="purple", alpha=0.15, zorder=0))
    ax.text(GRAVITY_SENSOR_CENTER[0], GRAVITY_SENSOR_CENTER[1], "Gravity Sensor\n(0-Phase Reset)", color="purple", alpha=0.8, ha="center", va="center", weight="bold")

    for label, xs, xe in COL_GROUPS:
        ax.text((xs + xe) / 2, LABEL_Y, label, ha="center", weight="bold", size=14)

    total_trajs = len(ALL_MBTI) * len(BLOODS) * len(GENDERS)
    curr_traj = 0
    for m in ALL_MBTI:
        for b in BLOODS:
            for g in GENDERS:
                curr_traj += 1
                if curr_traj % 20 == 0:
                    print(f"Rendering trajectory {curr_traj}/{total_trajs}")
                p_sr = generate_trajectory_pure(m, b, g, "sunrise", FINAL_AREA)
                p_ss = generate_trajectory_pure(m, b, g, "sunset", FINAL_AREA)
                render_branch(ax, p_sr, True, b)
                render_branch(ax, p_ss, False, b)

    ax.set_title(f"128-TYPE PURE GEOMETRY GRID | Static:Loop=31:1 | W5={W5:.2f} W7={W7:.3f} W11={W11:.3f}",
                 fontsize=20, pad=30, weight="bold")
    ax.set_xlim(-PLOT_MARGIN, N_COLS + PLOT_MARGIN)
    ax.set_ylim(N_ROWS + PLOT_MARGIN, LABEL_Y - PLOT_MARGIN)
    ax.axis("off")
    ax.legend(loc="upper right", fontsize=12)
    plt.tight_layout()
    
    filename = OUTPUT_FILENAME
    plt.savefig(filename, dpi=OUTPUT_DPI)
    print(f"Saved: {filename}")
