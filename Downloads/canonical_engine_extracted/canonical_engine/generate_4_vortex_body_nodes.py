"""4-Vortex Spiral Body Node Generator.

When the full circuit energy circulates, the log spiral resolves into 4
whirlpool (vortex) centers. Each vortex is anchored by a TCA-cycle
intermediate mapped to a specific body location:

  V1 — alpha-Ketoglutarate  : left inner eye / brain    (sulforaphane region)
  V2 — Oxaloacetate         : left waist / iliac crest  (mc1r region)
  V3 — Succinate (SDH)      : right chest / pectoralis  (succinate_dehydrogenase)
  V4 — Succinyl-CoA         : pelvis / lower abdomen    (left_genital_d2 / gluon_orogen)

Each vortex generates a local log-spiral r = a * e^(b*theta) whose points
are assigned to the nearest circuit node within that vortex. The 64
circuit nodes (from body_locations.json) are distributed across the 4
vortices by anatomical region, and their properties (element, particle,
music dims, 8D vector, TCA stage, stress pair) are propagated to the
generated spiral points.

Total output: ~1000 body nodes with full attribute set.
"""
from __future__ import annotations

import csv
import json
import math
import pathlib
from typing import Dict, List, Optional, Tuple

from .circuit_loader import NODES
from .energy_circulation import STRESS_PAIRS, SPHERES, ATTRACTORS
from .absolute_constants import SPARK_ANGLE_DEG, SPARK_ANGLE_RAD

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)

BODY_LOC_FILE = GEN_DIR / "body_locations.json"
BODY_NORM_FILE = GEN_DIR / "body_locations_normalized.json"

body_locs: Dict[str, Dict[str, str]] = json.loads(
    BODY_LOC_FILE.read_text(encoding="utf-8")
)
body_norm: Dict[str, Dict[str, str]] = json.loads(
    BODY_NORM_FILE.read_text(encoding="utf-8")
)

# ---------------------------------------------------------------------------
# Log spiral parameters (from ROI_SPIRAL_FIT.py: a=3.58, b=0.0216)
# ---------------------------------------------------------------------------
B_GLOBAL = 0.0216  # shared growth rate

# ---------------------------------------------------------------------------
# 4 Vortex Centers
# ---------------------------------------------------------------------------
# Face-grid coordinates (0-16) and body-grid coordinates (y: 0-170).
# Each vortex has its own spiral seed radius `a` and angular extent.

VORTEX_CENTERS: Dict[str, Dict] = {
    "V1_brain": {
        "label": "alpha-Ketoglutarate",
        "tca_stage": "alpha-ketoglutarate",
        "tca_enzyme": "alpha-ketoglutarate dehydrogenase",
        "stress_pair": "light_dark",
        "sphere": "Sun",
        "attractor": "Information",
        "body_region": "brain/head/face",
        "face_center": (6.5, 11.0),
        "body_center": (8.0, 30.0),
        "a": 2.5,
        "b": B_GLOBAL,
        "n_points": 250,
        "r_max_face": 8.0,
        "r_max_body": 60.0,
        "body_y_range": (10, 55),
        "keywords": [
            "frontalis", "brain", "scalp", "occiput", "philtrum", "lip",
            "eye", "temporalis", "hippocampus", "canthus", "endorphin",
            "sulforaphane", "cysteine", "memory_entropy", "hind_insula",
            "aurora", "co2", "peonidine", "disulfide", "pentose",
            "right_acetylcholine", "male_right_oxytocin", "sodium",
            "water", "pi_electron_cloud", "nonobserver", "observer_left",
            "left_endorphin",
        ],
    },
    "V2_waist": {
        "label": "Oxaloacetate",
        "tca_stage": "oxaloacetate",
        "tca_enzyme": "malate dehydrogenase / citrate synthase",
        "stress_pair": "o2_co2",
        "sphere": "Earth",
        "attractor": "Repair",
        "body_region": "waist/abdomen/pancreas",
        "face_center": (5.5, 8.0),
        "body_center": (8.0, 85.0),
        "a": 3.0,
        "b": B_GLOBAL,
        "n_points": 200,
        "r_max_face": 7.0,
        "r_max_body": 40.0,
        "body_y_range": (55, 105),
        "keywords": [
            "waist", "ilium", "iliac", "abdomen", "epigastric", "pancreas",
            "mc1r", "methionine", "basin", "podzol", "glp1", "cck",
            "outer_core_convection", "methylation", "lower_mantle",
            "large_igneous", "craton", "plume", "cytochrome_c_oxidase",
        ],
    },
    "V3_chest": {
        "label": "Succinate (SDH)",
        "tca_stage": "succinate",
        "tca_enzyme": "succinate dehydrogenase",
        "stress_pair": "heat_cold",
        "sphere": "Moon",
        "attractor": "Energy",
        "body_region": "chest/thorax/ribs",
        "face_center": (10.0, 9.0),
        "body_center": (8.0, 50.0),
        "a": 3.58,
        "b": B_GLOBAL,
        "n_points": 250,
        "r_max_face": 8.0,
        "r_max_body": 35.0,
        "body_y_range": (25, 60),
        "keywords": [
            "chest", "nipple", "pectoralis", "rib", "armpit", "sternum",
            "heme", "succinate_dehydrogenase", "lactate_dehydrogenase",
            "ferritin", "substance_p", "heath_aerenchyma",
            "mangrove_aerenchyma", "manganese_oxygen", "sulfur_iron",
            "chlorine_ion_pump", "adapter_protein", "fold_belt",
            "subduction_zone", "water_vapour", "carbon",
        ],
    },
    "V4_pelvis": {
        "label": "Succinyl-CoA",
        "tca_stage": "succinyl-coa",
        "tca_enzyme": "succinyl-coa synthetase",
        "stress_pair": "matter_nonmatter",
        "sphere": "CoMag",
        "attractor": "Energy",
        "body_region": "pelvis/glute/legs/feet",
        "face_center": (8.0, 6.0),
        "body_center": (8.0, 125.0),
        "a": 4.0,
        "b": B_GLOBAL,
        "n_points": 300,
        "r_max_face": 9.0,
        "r_max_body": 55.0,
        "body_y_range": (95, 175),
        "keywords": [
            "pelvis", "anus", "rectum", "glute", "bum", "foot", "toe",
            "sole", "calf", "knee", "Achilles", "thigh", "genital",
            "left_genital_d2", "gluon_orogen", "quark_orogen_magma",
            "steel", "clay_gouge", "thorium", "laterite", "magnetite",
            "oxidised_manganese", "right_sole_dopamine", "actomyosin",
            "collagen", "copper_iron_complex", "cambisol", "andosol",
            "histosol", "pyrite", "caco3", "NaCl", "autophagy",
            "mycorradicin", "methanogenesis", "fumarate",
        ],
    },
}

# TCA cycle ordering (clockwise through the cycle)
TCA_ORDER = [
    "oxaloacetate", "citrate", "isocitrate", "alpha-ketoglutarate",
    "succinyl-coa", "succinate", "fumarate", "malate", "oxaloacetate",
]

# Additional TCA intermediate body locations (from My Activity.html mapping)
TCA_BODY_MAP = {
    "citrate": {"body": "upper abdomen / liver", "vortex": "V2_waist"},
    "isocitrate": {"body": "right subclavicular", "vortex": "V3_chest"},
    "alpha-ketoglutarate": {"body": "left inner eye / left hippocampus", "vortex": "V1_brain"},
    "succinyl-coa": {"body": "lower abdomen / pelvis (dantian)", "vortex": "V4_pelvis"},
    "succinate": {"body": "right pectoralis major", "vortex": "V3_chest"},
    "fumarate": {"body": "bilateral medial malleoli (ankles)", "vortex": "V4_pelvis"},
    "malate": {"body": "right lateral femur", "vortex": "V4_pelvis"},
    "oxaloacetate": {"body": "glabella / left waist", "vortex": "V2_waist"},
}


# ---------------------------------------------------------------------------
# 1. Assign circuit nodes to vortices
# ---------------------------------------------------------------------------

def assign_nodes_to_vortices() -> Dict[str, List[str]]:
    """Assign each of the 64 circuit nodes to the best-matching vortex."""
    assignment: Dict[str, List[str]] = {k: [] for k in VORTEX_CENTERS}
    unassigned: List[str] = []

    for node_name in body_locs:
        raw = body_locs[node_name]["raw"].lower()
        norm = body_norm.get(node_name, {})
        region = norm.get("region", "")
        side = norm.get("side", "")

        best_vortex = None
        best_score = 0

        for vid, vc in VORTEX_CENTERS.items():
            score = 0
            for kw in vc["keywords"]:
                if kw in raw or kw in node_name.lower():
                    score += 2
            if region in vc["body_region"] or region in vc["body_region"].split("/"):
                score += 1
            if score > best_score:
                best_score = score
                best_vortex = vid

        if best_vortex and best_score > 0:
            assignment[best_vortex].append(node_name)
        else:
            unassigned.append(node_name)

    # Distribute unassigned by region heuristic
    region_fallback = {
        "head": "V1_brain", "face": "V1_brain", "brain": "V1_brain",
        "waist": "V2_waist", "abdomen": "V2_waist", "back": "V2_waist",
        "chest": "V3_chest", "arm": "V3_chest",
        "hip": "V4_pelvis", "foot": "V4_pelvis", "knee": "V4_pelvis",
        "other": "V4_pelvis",
    }
    for node_name in unassigned:
        norm = body_norm.get(node_name, {})
        region = norm.get("region", "other")
        vid = region_fallback.get(region, "V4_pelvis")
        assignment[vid].append(node_name)

    return assignment


# ---------------------------------------------------------------------------
# 2. Estimate body coordinates for circuit nodes
# ---------------------------------------------------------------------------

def estimate_node_body_coords(node_name: str) -> Tuple[float, float]:
    """Estimate (x, y) body coordinates for a circuit node from its location text."""
    raw = body_locs.get(node_name, {}).get("raw", "").lower()
    norm = body_norm.get(node_name, {})
    side = norm.get("side", "center")
    region = norm.get("region", "other")

    # Base x by side
    if side == "left":
        x = 6.0
    elif side == "right":
        x = 10.0
    elif side == "bilateral":
        x = 8.0
    else:
        x = 8.0

    # Base y by region (body height, 0=head, 170=feet)
    region_y = {
        "head": 15, "face": 12, "brain": 20,
        "neck": 25, "chest": 45, "back": 55,
        "waist": 85, "abdomen": 80, "hip": 100,
        "knee": 140, "calf": 155, "ankle": 165,
        "foot": 170, "hand": 90, "wrist": 95, "arm": 70,
        "other": 60,
    }
    y = region_y.get(region, 60)

    # Fine-tune from keywords
    if "scalp" in raw or "vertex" in raw:
        y = 5
    elif "brain" in raw:
        y = 18
    elif "occiput" in raw or "occipital" in raw:
        y = 10
    elif "philtrum" in raw or "lip" in raw:
        y = 12
    elif "throat" in raw or "cervical" in raw:
        y = 25
    elif "nipple" in raw or "pectoralis" in raw:
        y = 45
    elif "rib" in raw:
        y = 42
    elif "armpit" in raw or "axillary" in raw:
        y = 48
    elif "sternum" in raw or "mediastinum" in raw:
        y = 50
    elif "abdomen" in raw or "epigastric" in raw:
        y = 78
    elif "pancreas" in raw:
        y = 75
    elif "waist" in raw or "iliac" in raw:
        y = 85
    elif "hip" in raw:
        y = 100
    elif "pelvis" in raw or "glute" in raw or "bum" in raw:
        y = 110
    elif "anus" in raw or "rectum" in raw or "perineal" in raw:
        y = 115
    elif "genital" in raw:
        y = 112
    elif "thigh" in raw or "femoral" in raw:
        y = 125
    elif "knee" in raw:
        y = 140
    elif "calf" in raw or "gastrocnemius" in raw:
        y = 155
    elif "Achilles" in raw or "calcaneal" in raw or "ankle" in raw:
        y = 165
    elif "sole" in raw or "plantar" in raw:
        y = 170
    elif "toe" in raw or "digit" in raw or "hallux" in raw:
        y = 172
    elif "finger" in raw or "hand" in raw:
        y = 90
        x = 10.0 if "right" in raw else 6.0
    elif "wrist" in raw:
        y = 92
        x = 10.0 if "right" in raw else 6.0

    # Fine-tune x from specific left/right mentions
    if "left" in raw and "right" not in raw:
        x = min(x, 6.5)
    elif "right" in raw and "left" not in raw:
        x = max(x, 9.5)
    elif "bilateral" in raw or "both" in raw:
        x = 8.0

    return (x, y)


# ---------------------------------------------------------------------------
# 3. Spiral point generation
# ---------------------------------------------------------------------------

def generate_vortex_points(vid: str, vc: Dict) -> List[Dict]:
    """Generate spiral points for one vortex in both face and body coordinates."""
    a = vc["a"]
    b = vc["b"]
    n = vc["n_points"]
    fc = vc["face_center"]
    bc = vc["body_center"]
    r_max_f = vc["r_max_face"]
    r_max_b = vc["r_max_body"]
    y_lo, y_hi = vc["body_y_range"]

    theta_max = math.log(r_max_f / a) / b if r_max_f > a else 50.0

    points = []
    for i in range(n):
        t = i / max(n - 1, 1)
        theta = t * theta_max
        r_face = a * math.exp(b * theta)
        r_body = a * math.exp(b * theta) * (r_max_b / r_max_f)

        # Face-grid coordinates
        fx = fc[0] + r_face * math.cos(theta)
        fy = fc[1] + r_face * math.sin(theta)

        # Body-grid coordinates — spiral wraps around body center
        # Map theta to body y progression (spiral descends body)
        body_progress = t  # 0=top, 1=bottom
        by = y_lo + (y_hi - y_lo) * body_progress
        # Body x oscillates around center with decreasing amplitude
        bx = bc[0] + r_body * math.cos(theta + math.pi) * 0.3

        # Clamp body x to reasonable range
        bx = max(2.0, min(14.0, bx))
        by = max(0.0, min(180.0, by))

        points.append({
            "node_id": f"{vid}_{i:04d}",
            "vortex_id": vid,
            "vortex_label": vc["label"],
            "tca_stage": vc["tca_stage"],
            "tca_enzyme": vc["tca_enzyme"],
            "stress_pair": vc["stress_pair"],
            "sphere": vc["sphere"],
            "attractor": vc["attractor"],
            "spiral_idx": i,
            "spiral_theta": theta,
            "spiral_r_face": r_face,
            "spiral_r_body": r_body,
            "spiral_revolutions": theta / (2 * math.pi),
            "face_x": round(fx, 4),
            "face_y": round(fy, 4),
            "body_x": round(bx, 4),
            "body_y": round(by, 4),
            "body_region": vc["body_region"],
        })
    return points


# ---------------------------------------------------------------------------
# 4. Propagate circuit node properties to spiral points
# ---------------------------------------------------------------------------

def propagate_node_properties(
    points: List[Dict],
    assigned_nodes: Dict[str, List[str]],
) -> List[Dict]:
    """For each spiral point, find the nearest circuit node in the same vortex
    and propagate its properties."""

    # Build per-vortex node coordinate lists
    vortex_node_coords: Dict[str, List[Tuple[str, float, float]]] = {}
    for vid, node_list in assigned_nodes.items():
        coords = []
        for nname in node_list:
            if nname in NODES:
                bx, by = estimate_node_body_coords(nname)
                coords.append((nname, bx, by))
        vortex_node_coords[vid] = coords

    for pt in points:
        vid = pt["vortex_id"]
        bx, by = pt["body_x"], pt["body_y"]
        candidates = vortex_node_coords.get(vid, [])

        best_node = None
        best_dist = float("inf")
        for nname, nx, ny in candidates:
            dist = math.sqrt((bx - nx) ** 2 + (by - ny) ** 2)
            if dist < best_dist:
                best_dist = dist
                best_node = nname

        if best_node and best_node in NODES:
            cn = NODES[best_node]
            pt["nearest_circuit_node"] = best_node
            pt["circuit_element"] = cn.element
            pt["circuit_particle"] = cn.particle
            pt["circuit_group"] = cn.group
            pt["circuit_color"] = cn.color
            pt["circuit_music_dims"] = list(cn.music_dims)
            pt["circuit_location"] = cn.location or body_locs.get(best_node, {}).get("raw", "")
            pt["binding_strength"] = round(math.exp(-best_dist * 0.05), 4)
            pt["body_distance"] = round(best_dist, 2)
        else:
            pt["nearest_circuit_node"] = None
            pt["binding_strength"] = 0.0
            pt["body_distance"] = 999.0

    return points


# ---------------------------------------------------------------------------
# 5. Add 8D music dimension vectors
# ---------------------------------------------------------------------------

def add_8d_vectors(points: List[Dict]) -> List[Dict]:
    """Compute 8D music dimension values for each point from spiral phase,
    stress pair mapping, cross-vortex toroidal coupling, and circadian phase.

    Key physics:
    - Each stress pair has two poles (dims) that are anti-correlated (π phase shift)
    - The native stress pair of a vortex dominates; other pairs couple weakly
    - Toroidal circulation creates cross-vortex interference
    - Spark angle (138.88°) creates discontinuous leaps at specific phases
    """

    # 8D dims: r, h, d, p, s, gamma, g, nu
    # Each stress pair: (pole_a_dim, pole_b_dim) — anti-correlated
    dim_map = {
        "light_dark": ("gamma", "d"),       # light vs dark
        "o2_co2": ("h", "p"),               # CO2 vs O2
        "heat_cold": ("nu", "r"),           # heat vs cold
        "matter_nonmatter": ("s", "g"),     # matter vs non-matter
    }

    # Toroidal coupling: which stress pairs influence which vortices
    # Native pair gets weight 1.0, adjacent pairs get 0.3, opposite gets 0.1
    vortex_coupling = {
        "V1_brain": {"light_dark": 1.0, "o2_co2": 0.4, "heat_cold": 0.3, "matter_nonmatter": 0.15},
        "V2_waist": {"o2_co2": 1.0, "heat_cold": 0.3, "light_dark": 0.2, "matter_nonmatter": 0.15},
        "V3_chest": {"heat_cold": 1.0, "matter_nonmatter": 0.4, "o2_co2": 0.25, "light_dark": 0.2},
        "V4_pelvis": {"matter_nonmatter": 1.0, "light_dark": 0.35, "heat_cold": 0.25, "o2_co2": 0.2},
    }

    # Circadian phase offsets (radians) for each stress pair
    # o2_co2: 3-9h, heat_cold: 9-15h, matter_nonmatter: 15-21h, light_dark: 0-3h+21-3h
    circadian_phase = {
        "o2_co2": 0.0,
        "heat_cold": math.pi * 0.5,
        "matter_nonmatter": math.pi,
        "light_dark": math.pi * 1.5,
    }

    for pt in points:
        vid = pt["vortex_id"]
        native_sp = pt["stress_pair"]
        theta = pt["spiral_theta"]
        revs = pt["spiral_revolutions"]

        vec = {d: 0.5 for d in ["r", "h", "d", "p", "s", "gamma", "g", "nu"]}

        coupling = vortex_coupling.get(vid, {native_sp: 1.0})

        for sp, (dim_a, dim_b) in dim_map.items():
            w = coupling.get(sp, 0.1)
            phase = circadian_phase.get(sp, 0.0)

            # Pole A: cos wave, Pole B: anti-correlated (π shift)
            osc = math.cos(theta * 0.5 + phase)
            val_a = 0.5 + 0.35 * w * osc
            val_b = 0.5 - 0.35 * w * osc

            # Accumulate (multiple stress pairs can influence same dim)
            vec[dim_a] = max(vec[dim_a], min(1.0, val_a)) if w > 0.2 else vec[dim_a]
            vec[dim_b] = max(vec[dim_b], min(1.0, val_b)) if w > 0.2 else vec[dim_b]

            # For weak coupling, blend instead of max
            if w <= 0.2 and w > 0.05:
                vec[dim_a] = 0.7 * vec[dim_a] + 0.3 * val_a
                vec[dim_b] = 0.7 * vec[dim_b] + 0.3 * val_b

        # Spark angle influence — 138.88° phase creates discontinuous leap
        spark_phase_frac = SPARK_ANGLE_DEG / 360.0
        local_phase = (theta / (2 * math.pi)) % 1.0
        spark_dist = abs(local_phase - spark_phase_frac)
        spark_dist = min(spark_dist, 1.0 - spark_dist)  # wrap-around

        if spark_dist < 0.03:
            # Spark leap: boost native pair's pole_a, suppress pole_b
            native_dims = dim_map.get(native_sp, ("r", "s"))
            spark_boost = 0.2 * (1.0 - spark_dist / 0.03)
            vec[native_dims[0]] = min(1.0, vec[native_dims[0]] + spark_boost)
            vec[native_dims[1]] = max(0.0, vec[native_dims[1]] - spark_boost * 0.5)
            pt["spark_active"] = True
        else:
            pt["spark_active"] = False

        pt["vec_8d"] = {k: round(v, 4) for k, v in vec.items()}

        # Primary genre from music dims
        music_dims = pt.get("circuit_music_dims", list(dim_map.get(native_sp, ("r", "s"))))
        pt["primary_dims"] = music_dims

    return points


# ---------------------------------------------------------------------------
# 6. Add TCA cycle position
# ---------------------------------------------------------------------------

def add_tca_position(points: List[Dict]) -> List[Dict]:
    """Add TCA cycle position (0-7) based on vortex and spiral phase."""
    tca_vortex_order = ["V1_brain", "V2_waist", "V3_chest", "V4_pelvis"]
    # Map: V1=alpha-KG(3), V2=oxaloacetate(0), V3=succinate(5), V4=succinyl-CoA(4)

    vortex_tca_index = {
        "V1_brain": 3,    # alpha-ketoglutarate
        "V2_waist": 0,    # oxaloacetate (also citrate=1)
        "V3_chest": 5,    # succinate
        "V4_pelvis": 4,   # succinyl-coa (also fumarate=6, malate=7)
    }

    for pt in points:
        vid = pt["vortex_id"]
        base_idx = vortex_tca_index.get(vid, 0)
        # Spiral phase advances TCA position within the vortex
        revs = pt["spiral_revolutions"]
        tca_offset = int(revs * 2) % 2  # 0 or 1 step forward
        tca_idx = (base_idx + tca_offset) % 8
        pt["tca_index"] = tca_idx
        pt["tca_name"] = TCA_ORDER[tca_idx]

    return points


# ---------------------------------------------------------------------------
# 7. Main generation
# ---------------------------------------------------------------------------

def generate_all_nodes() -> List[Dict]:
    """Generate all ~1000 body nodes across 4 vortices."""
    assigned = assign_nodes_to_vortices()

    all_points: List[Dict] = []
    for vid, vc in VORTEX_CENTERS.items():
        pts = generate_vortex_points(vid, vc)
        all_points.extend(pts)

    # Propagate properties
    all_points = propagate_node_properties(all_points, assigned)
    all_points = add_8d_vectors(all_points)
    all_points = add_tca_position(all_points)

    # Add vortex assignment summary
    summary = {vid: len(nodes) for vid, nodes in assigned.items()}
    return all_points, assigned, summary


def write_outputs(
    points: List[Dict],
    assigned: Dict[str, List[str]],
    summary: Dict[str, int],
):
    """Write JSON, CSV, and human-readable report."""

    # JSON
    out_json = GEN_DIR / "vortex_body_nodes.json"
    out_json.write_text(
        json.dumps({
            "total_nodes": len(points),
            "vortex_summary": summary,
            "vortex_centers": {
                vid: {
                    "label": vc["label"],
                    "tca_stage": vc["tca_stage"],
                    "face_center": vc["face_center"],
                    "body_center": vc["body_center"],
                    "a": vc["a"],
                    "b": vc["b"],
                    "n_points": vc["n_points"],
                    "assigned_circuit_nodes": assigned[vid],
                }
                for vid, vc in VORTEX_CENTERS.items()
            },
            "nodes": points,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # CSV
    out_csv = GEN_DIR / "vortex_body_nodes.csv"
    fieldnames = [
        "node_id", "vortex_id", "vortex_label", "tca_stage", "tca_name",
        "tca_index", "stress_pair", "sphere", "attractor",
        "spiral_idx", "spiral_theta", "spiral_r_face", "spiral_revolutions",
        "face_x", "face_y", "body_x", "body_y", "body_region",
        "nearest_circuit_node", "circuit_element", "circuit_particle",
        "circuit_group", "circuit_color", "circuit_music_dims",
        "binding_strength", "body_distance",
        "r", "h", "d", "p", "s", "gamma", "g", "nu",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for pt in points:
            row = {k: pt.get(k, "") for k in fieldnames}
            # Flatten 8D vector
            vec = pt.get("vec_8d", {})
            for d in ["r", "h", "d", "p", "s", "gamma", "g", "nu"]:
                row[d] = vec.get(d, "")
            # Flatten music dims list
            md = pt.get("circuit_music_dims", [])
            row["circuit_music_dims"] = "|".join(md) if isinstance(md, list) else str(md)
            w.writerow(row)

    # Human-readable report
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("4-VORTEX SPIRAL BODY NODE GENERATOR")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Total nodes generated: {len(points)}")
    lines.append("")

    lines.append("■ Vortex Centers")
    lines.append("-" * 80)
    for vid, vc in VORTEX_CENTERS.items():
        lines.append(f"  {vid} — {vc['label']} ({vc['tca_stage']})")
        lines.append(f"    face_center: {vc['face_center']}  body_center: {vc['body_center']}")
        lines.append(f"    spiral: a={vc['a']}, b={vc['b']}, points={vc['n_points']}")
        lines.append(f"    stress_pair: {vc['stress_pair']}  sphere: {vc['sphere']}  attractor: {vc['attractor']}")
        lines.append(f"    assigned circuit nodes ({summary[vid]}): {', '.join(assigned[vid][:8])}{'...' if len(assigned[vid]) > 8 else ''}")
        lines.append("")

    lines.append("■ Node Distribution by Vortex")
    lines.append("-" * 80)
    for vid in VORTEX_CENTERS:
        count = sum(1 for p in points if p["vortex_id"] == vid)
        lines.append(f"  {vid}: {count} nodes")
    lines.append(f"  TOTAL: {len(points)} nodes")
    lines.append("")

    lines.append("■ Sample Nodes (first 5 per vortex)")
    lines.append("-" * 80)
    for vid in VORTEX_CENTERS:
        lines.append(f"  [{vid}]")
        vortex_pts = [p for p in points if p["vortex_id"] == vid]
        for pt in vortex_pts[:5]:
            node = pt.get("nearest_circuit_node", "—")
            elem = pt.get("circuit_element", "—")
            tca = pt.get("tca_name", "—")
            bx, by = pt["body_x"], pt["body_y"]
            lines.append(
                f"    {pt['node_id']:12s}  body=({bx:5.1f},{by:5.1f})  "
                f"node={node:30s}  elem={elem:10s}  tca={tca}"
            )
        lines.append("")

    lines.append("■ TCA Cycle Flow Through Vortices")
    lines.append("-" * 80)
    lines.append("  V2(oxaloacetate) → V1(alpha-KG) → V4(succinyl-CoA) → V3(succinate) → V2")
    lines.append("  TCA: OAA → citrate → isocitrate → αKG → succinyl-CoA → succinate → fumarate → malate → OAA")
    lines.append("")

    lines.append("■ 8D Vector Sample (V1 first 3)")
    lines.append("-" * 80)
    for pt in [p for p in points if p["vortex_id"] == "V1_brain"][:3]:
        vec = pt.get("vec_8d", {})
        lines.append(
            f"  {pt['node_id']:12s}  "
            f"r={vec.get('r',0):.2f} h={vec.get('h',0):.2f} d={vec.get('d',0):.2f} "
            f"p={vec.get('p',0):.2f} s={vec.get('s',0):.2f} γ={vec.get('gamma',0):.2f} "
            f"g={vec.get('g',0):.2f} ν={vec.get('nu',0):.2f}"
        )
    lines.append("")

    text = "\n".join(lines)
    (GEN_DIR / "vortex_body_nodes_report.txt").write_text(text, encoding="utf-8")

    print(text[:2000])
    print(f"\n... full report → {GEN_DIR / 'vortex_body_nodes_report.txt'}")
    print(f"→ JSON: {out_json}")
    print(f"→ CSV:  {out_csv}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    points, assigned, summary = generate_all_nodes()
    write_outputs(points, assigned, summary)
