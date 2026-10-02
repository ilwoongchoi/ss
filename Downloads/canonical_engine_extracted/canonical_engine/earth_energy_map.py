"""Earth Coordinate Mapping + Energy Circulation for All Universe Subjects.

Maps every subject in the universe model onto Earth coordinates:
  - 20 Y-DNA haplogroups → population centers
  - 10 mtDNA haplogroups → maternal line centers
  - 33 ethnic archetypes → blended coordinates
  - ~25 geological circuit nodes → geological features
  - 5 cosmic spheres → projection latitudes
  - 3 attractors → Earth energy centers

Then computes energy circulation paths between all subjects using:
  - Toroidal sphere transitions (24h circadian)
  - Circuit topology (feedback loops, attractor cycles)
  - Haplogroup 8D vector resonance
  - Geological node stress pair coupling

Outputs:
  generated/earth_energy_map.png        — world map with all subjects + flow
  generated/earth_energy_paths.json     — computed energy paths
  generated/earth_subjects_coords.json  — all subject coordinates
  generated/earth_energy_report.txt     — human-readable report
"""
from __future__ import annotations

import json
import math
import pathlib
from typing import Dict, List, Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)

import sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from haplogroup_vector_mapping import Y_DNA, MTDNA, ETHNIC_ARCHETYPES

# ===========================================================================
# 1. Y-DNA HAPLOGROUP EARTH COORDINATES
# ===========================================================================

Y_DNA_COORDS: Dict[str, Dict] = {
    "R1a": {"lat": 50.45, "lon": 30.52, "label": "Balto-Slavic / Indo-Iranian", "region": "E.Europe/C.Asia"},
    "R1b": {"lat": 53.35, "lon": -6.26, "label": "Celtic / Italic / Germanic", "region": "W.Europe/Atlantic"},
    "I1":  {"lat": 59.33, "lon": 18.07, "label": "Nordic / Germanic", "region": "Scandinavia"},
    "I2":  {"lat": 44.79, "lon": 20.46, "label": "Dinaric / Balkan / Sardinian", "region": "Balkans"},
    "J1":  {"lat": 24.71, "lon": 46.68, "label": "Semitic / Arabian / Cohanim", "region": "Arabian Peninsula"},
    "J2":  {"lat": 41.01, "lon": 28.98, "label": "Mesopotamian / Minoan / Anatolian", "region": "Anatolia/Mesopotamia"},
    "E1b1b": {"lat": 9.03, "lon": 38.74, "label": "NE Africa / Berber / E-V13", "region": "Horn of Africa/Maghreb"},
    "E1b1a": {"lat": 6.52, "lon": 3.38, "label": "Sub-Saharan / Bantu / W.African", "region": "W.Africa"},
    "N1c":  {"lat": 60.17, "lon": 24.94, "label": "Uralo-Finnic / Baltic / Siberian", "region": "Finland/Siberia"},
    "G2a":  {"lat": 41.69, "lon": 44.80, "label": "Caucasian / Neolithic Farmer", "region": "Caucasus/Anatolia"},
    "O1":   {"lat": 23.13, "lon": 113.26, "label": "Austronesian / Tai-Kadai", "region": "S.China/SE.Asia/Polynesia"},
    "O2":   {"lat": 39.90, "lon": 116.40, "label": "Sino-Tibetan / Han / Korean / Japanese", "region": "E.Asia"},
    "C":    {"lat": 47.92, "lon": 106.92, "label": "Mongolic / Turkic / Na-Dene", "region": "Mongolia/Siberia"},
    "Q":    {"lat": 65.00, "lon": -170.00, "label": "Native American / Paleo-Siberian", "region": "Beringia/Americas"},
    "T":    {"lat": 30.04, "lon": 31.24, "label": "Near Eastern / Egyptian / Ethiopian", "region": "Nile/Near East"},
    "D":    {"lat": 29.65, "lon": 91.11, "label": "Tibetan / Ainu / Andamanese", "region": "Tibet/Japan/Andaman"},
    "L":    {"lat": 19.08, "lon": 72.88, "label": "S.Asian / Dravidian / Indian", "region": "India/S.Asia"},
    "H":    {"lat": 28.61, "lon": 77.21, "label": "Indian tribal / Romani / Dravidian", "region": "India/Romani diaspora"},
}

# ===========================================================================
# 2. mtDNA HAPLOGROUP EARTH COORDINATES
# ===========================================================================

MTDNA_COORDS: Dict[str, Dict] = {
    "H":  {"lat": 48.86, "lon": 2.35, "label": "W.European dominant (45%)", "region": "W.Europe"},
    "U":  {"lat": 52.52, "lon": 13.40, "label": "Ancient European hunter-gatherer", "region": "Europe (ancient)"},
    "J":  {"lat": 33.51, "lon": 36.29, "label": "Near Eastern (9%)", "region": "Near East"},
    "T":  {"lat": 33.89, "lon": 35.50, "label": "Near Eastern (8%)", "region": "Near East"},
    "K":  {"lat": 31.78, "lon": 35.22, "label": "Neolithic farmer / Ashkenazi (32%)", "region": "Levant/Europe"},
    "V":  {"lat": 43.26, "lon": -2.93, "label": "Iberian / Scandinavian (4%)", "region": "Basque/Iberia"},
    "X":  {"lat": 33.50, "lon": 35.50, "label": "Native American / Druze / Berber", "region": "Druze/Americas"},
    "M":  {"lat": 22.57, "lon": 88.36, "label": "Pan-Asian macro-haplogroup", "region": "All Asia"},
    "L2": {"lat": 5.60, "lon": -0.19, "label": "W.African / Sub-Saharan", "region": "W.Africa"},
    "L3": {"lat": -1.29, "lon": 36.82, "label": "E.African / Out-of-Africa root", "region": "E.Africa"},
}

# ===========================================================================
# 3. ETHNIC ARCHETYPE COORDINATES (blended from Y-DNA + mtDNA)
# ===========================================================================

ETHNIC_COORDS: Dict[str, Dict] = {
    "Han_Chinese":       {"lat": 34.00, "lon": 113.00, "label": "Han Chinese"},
    "Korean":            {"lat": 37.55, "lon": 126.97, "label": "Korean"},
    "Japanese":          {"lat": 35.68, "lon": 139.69, "label": "Japanese"},
    "Tibetan":           {"lat": 29.65, "lon": 91.11, "label": "Tibetan"},
    "Scandinavian":      {"lat": 59.33, "lon": 18.07, "label": "Scandinavian"},
    "Basque":            {"lat": 43.26, "lon": -2.93, "label": "Basque"},
    "Irish_Celtic":      {"lat": 53.35, "lon": -6.26, "label": "Irish Celtic"},
    "Slavic_Eastern":    {"lat": 50.45, "lon": 30.52, "label": "Slavic Eastern"},
    "Serbian_Dinaric":   {"lat": 44.79, "lon": 20.46, "label": "Serbian Dinaric"},
    "Sardinian":         {"lat": 40.12, "lon": 9.41, "label": "Sardinian"},
    "Arabian_Gulf":      {"lat": 24.71, "lon": 46.68, "label": "Arabian Gulf"},
    "Ashkenazi_Jewish":  {"lat": 31.78, "lon": 35.22, "label": "Ashkenazi Jewish"},
    "Levantine_Arab":    {"lat": 33.51, "lon": 36.29, "label": "Levantine Arab"},
    "Anatolian_Turk":    {"lat": 41.01, "lon": 28.98, "label": "Anatolian Turk"},
    "Ethiopian":         {"lat": 9.03, "lon": 38.74, "label": "Ethiopian"},
    "Berber_Moroccan":   {"lat": 31.63, "lon": -8.01, "label": "Berber Moroccan"},
    "Greek_Balkan":      {"lat": 37.98, "lon": 23.73, "label": "Greek Balkan"},
    "W_African_Yoruba":  {"lat": 6.52, "lon": 3.38, "label": "W.African Yoruba"},
    "Bantu_Central":     {"lat": -4.04, "lon": 21.76, "label": "Bantu Central"},
    "Finnish":           {"lat": 60.17, "lon": 24.94, "label": "Finnish"},
    "Estonian_Baltic":   {"lat": 59.44, "lon": 24.75, "label": "Estonian Baltic"},
    "Georgian_Caucasian": {"lat": 41.69, "lon": 44.80, "label": "Georgian Caucasian"},
    "Mongol":            {"lat": 47.92, "lon": 106.92, "label": "Mongol"},
    "Manchu":            {"lat": 45.75, "lon": 126.63, "label": "Manchu"},
    "Native_American":   {"lat": 40.00, "lon": -100.00, "label": "Native American"},
    "Inca_Andean":       {"lat": -13.53, "lon": -71.97, "label": "Inca Andean"},
    "S_Indian_Dravidian": {"lat": 11.02, "lon": 76.95, "label": "S.Indian Dravidian"},
    "N_Indian_Brahmin":  {"lat": 25.31, "lon": 83.01, "label": "N.Indian Brahmin"},
    "Malay_Austronesian": {"lat": 3.14, "lon": 101.69, "label": "Malay Austronesian"},
    "Polynesian":        {"lat": -17.74, "lon": -149.33, "label": "Polynesian"},
    "Egyptian":          {"lat": 30.04, "lon": 31.24, "label": "Egyptian"},
    "Ainu_Japan":        {"lat": 43.06, "lon": 141.35, "label": "Ainu Japan"},
    "Romani":            {"lat": 44.43, "lon": 26.10, "label": "Romani"},
}

# ===========================================================================
# 4. CIRCUIT GEOLOGICAL NODE EARTH COORDINATES
# ===========================================================================

GEO_NODE_COORDS: Dict[str, Dict] = {
    "steel": {
        "lat": 65.50, "lon": 20.50, "label": "Banded Iron Formation (Kiruna, Sweden)",
        "geo_type": "iron_formation", "stress_pair": "matter_nonmatter",
    },
    "clay_gouge": {
        "lat": 36.00, "lon": -120.00, "label": "San Andreas Fault gouge zone",
        "geo_type": "fault_gouge", "stress_pair": "heat_cold",
    },
    "craton": {
        "lat": -26.00, "lon": 24.00, "label": "Kaapvaal Craton (S.Africa, oldest ~3.7Ga)",
        "geo_type": "craton", "stress_pair": "matter_nonmatter",
    },
    "laterite": {
        "lat": -1.00, "lon": 23.00, "label": "Congo Basin tropical laterite",
        "geo_type": "tropical_weathering", "stress_pair": "o2_co2",
    },
    "podzol": {
        "lat": 64.00, "lon": 26.00, "label": "Finnish boreal podzol",
        "geo_type": "boreal_soil", "stress_pair": "heat_cold",
    },
    "andosol": {
        "lat": 35.36, "lon": 138.73, "label": "Fuji volcanic andosol (Japan)",
        "geo_type": "volcanic_soil", "stress_pair": "o2_co2",
    },
    "cambisol": {
        "lat": 48.00, "lon": 8.00, "label": "European temperate cambisol (Black Forest)",
        "geo_type": "temperate_soil", "stress_pair": "o2_co2",
    },
    "histosol": {
        "lat": 60.00, "lon": 90.00, "label": "Siberian peatland histosol",
        "geo_type": "peatland", "stress_pair": "heat_cold",
    },
    "pyrite": {
        "lat": -27.00, "lon": -70.00, "label": "Atacama hydrothermal pyrite (Chile)",
        "geo_type": "hydrothermal_sulfide", "stress_pair": "matter_nonmatter",
    },
    "fold_belt": {
        "lat": 28.00, "lon": 87.00, "label": "Himalayan fold belt",
        "geo_type": "orogenic_belt", "stress_pair": "heat_cold",
    },
    "subduction_zone": {
        "lat": 15.00, "lon": 145.00, "label": "Mariana subduction zone",
        "geo_type": "subduction", "stress_pair": "light_dark",
    },
    "basin": {
        "lat": 32.00, "lon": 44.00, "label": "Mesopotamian sedimentary basin",
        "geo_type": "sedimentary_basin", "stress_pair": "o2_co2",
    },
    "monazite": {
        "lat": -22.00, "lon": 46.00, "label": "Madagascar monazite rare earth deposit",
        "geo_type": "rare_earth", "stress_pair": "light_dark",
    },
    "plume": {
        "lat": 64.96, "lon": -19.02, "label": "Iceland mantle plume hotspot",
        "geo_type": "mantle_plume", "stress_pair": "heat_cold",
    },
    "large_igneous_province": {
        "lat": 66.00, "lon": 95.00, "label": "Siberian Traps LIP",
        "geo_type": "LIP", "stress_pair": "matter_nonmatter",
    },
    "manganese_nodule": {
        "lat": 15.00, "lon": -150.00, "label": "Pacific deep-sea manganese nodules (Clarion-Clipperton)",
        "geo_type": "deep_sea_nodule", "stress_pair": "matter_nonmatter",
    },
    "gluon_orogen": {
        "lat": 30.00, "lon": 81.00, "label": "Himalayan orogen (gluon coupling)",
        "geo_type": "orogenic_core", "stress_pair": "matter_nonmatter",
    },
    "outer_core_convection": {
        "lat": 0.00, "lon": 0.00, "label": "Core-mantle boundary (global, equatorial)",
        "geo_type": "deep_earth", "stress_pair": "heat_cold",
    },
    "lower_mantle": {
        "lat": -10.00, "lon": 160.00, "label": "Pacific LLSVP (large low-shear-velocity province)",
        "geo_type": "deep_mantle", "stress_pair": "matter_nonmatter",
    },
    "oxidised_manganese": {
        "lat": -23.00, "lon": 30.00, "label": "Kalahari manganese field (S.Africa)",
        "geo_type": "manganese_oxide", "stress_pair": "o2_co2",
    },
    "magnetite": {
        "lat": -32.00, "lon": 116.00, "label": "Western Australia magnetite deposit",
        "geo_type": "iron_oxide", "stress_pair": "light_dark",
    },
    "thorium": {
        "lat": 25.00, "lon": 73.00, "label": "Rajasthan thorium deposit (India)",
        "geo_type": "radioactive", "stress_pair": "light_dark",
    },
    "quark_orogen_magma": {
        "lat": -6.00, "lon": 105.00, "label": "Sunda arc partial melt (Indonesia)",
        "geo_type": "arc_magma", "stress_pair": "heat_cold",
    },
    "succinate_dehydrogenase": {
        "lat": 42.00, "lon": 14.00, "label": "Mediterranean metabolic hub (Italy)",
        "geo_type": "metabolic_reference", "stress_pair": "heat_cold",
    },
    "ferritin": {
        "lat": 51.50, "lon": -0.13, "label": "Iron storage reference (London)",
        "geo_type": "iron_storage", "stress_pair": "matter_nonmatter",
    },
}

# ===========================================================================
# 5. COSMIC SPHERE EARTH PROJECTIONS
# ===========================================================================

SPHERE_PROJECTIONS: Dict[str, Dict] = {
    "Sun": {
        "lat": 23.50, "lon": 0.00, "label": "Tropic of Cancer (solar zenith)",
        "dims": ("r", "s"), "attractor": "Information",
        "body_region": "brain/ETC",
    },
    "Earth": {
        "lat": 0.00, "lon": 0.00, "label": "Equator (Earth center)",
        "dims": ("gamma", "h"), "attractor": "Repair",
        "body_region": "thorax/spine",
    },
    "Moon": {
        "lat": -23.50, "lon": 180.00, "label": "Tropic of Capricorn (lunar antipode)",
        "dims": ("p", "nu"), "attractor": "Time",
        "body_region": "occiput/right brain",
    },
    "CoMag": {
        "lat": 45.00, "lon": 90.00, "label": "Coma Berenices projection (N.Asia)",
        "dims": ("g", "gamma"), "attractor": "Bridge",
        "body_region": "pelvis/gut",
    },
    "Barnard": {
        "lat": -45.00, "lon": -90.00, "label": "Barnard's Star projection (S.Pacific)",
        "dims": ("g", "d"), "attractor": "Energy",
        "body_region": "chest/liver",
    },
}

# ===========================================================================
# 6. ATTRACTOR EARTH CENTERS
# ===========================================================================

ATTRACTOR_CENTERS: Dict[str, Dict] = {
    "Energy": {
        "lat": -45.00, "lon": -90.00, "label": "Barnard projection (S.Pacific)",
        "dims": ("r", "g", "gamma"),
        "sphere": "Barnard",
    },
    "Information": {
        "lat": 23.50, "lon": 0.00, "label": "Sun projection (Tropic of Cancer)",
        "dims": ("h", "nu", "s"),
        "sphere": "Sun",
    },
    "Repair": {
        "lat": 0.00, "lon": 0.00, "label": "Earth center (Equator)",
        "dims": ("p", "d", "g"),
        "sphere": "Earth",
    },
}

# ===========================================================================
# 7. STRESS PAIR DEFINITIONS (from energy_circulation.py)
# ===========================================================================

STRESS_PAIRS = {
    "o2_co2": {"dims": ("h", "p"), "poles": ("Earth", "Moon"), "hours": (3, 9)},
    "heat_cold": {"dims": ("nu", "r"), "poles": ("Moon", "Sun"), "hours": (9, 15)},
    "matter_nonmatter": {"dims": ("s", "g"), "poles": ("Sun", "Barnard"), "hours": (15, 21)},
    "light_dark": {"dims": ("gamma", "d"), "poles": ("Earth", "Barnard"), "hours": (0, 3)},
}

# ===========================================================================
# 8. GREAT CIRCLE DISTANCE + ENERGY FLOW
# ===========================================================================

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great circle distance in km."""
    R = 6371.0
    rlat1, rlat2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))


def bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Initial bearing in degrees."""
    rlat1, rlat2 = math.radians(lat1), math.radians(lat2)
    dlon = math.radians(lon2 - lon1)
    x = math.sin(dlon) * math.cos(rlat2)
    y = math.cos(rlat1) * math.sin(rlat2) - math.sin(rlat1) * math.cos(rlat2) * math.cos(dlon)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def interpolate_great_circle(
    lat1: float, lon1: float, lat2: float, lon2: float, n: int = 50
) -> List[Tuple[float, float]]:
    """Interpolate points along great circle path."""
    rlat1, rlat2 = math.radians(lat1), math.radians(lat2)
    rlon1, rlon2 = math.radians(lon1), math.radians(lon2)
    cos_d = math.sin(rlat1) * math.sin(rlat2) + \
        math.cos(rlat1) * math.cos(rlat2) * math.cos(rlon2 - rlon1)
    cos_d = max(-1.0, min(1.0, cos_d))
    d = math.acos(cos_d)
    if d < 1e-10:
        return [(lat1, lon1)] * n

    points = []
    for i in range(n):
        f = i / (n - 1)
        A = math.sin((1 - f) * d) / math.sin(d)
        B = math.sin(f * d) / math.sin(d)
        x = A * math.cos(rlat1) * math.cos(rlon1) + B * math.cos(rlat2) * math.cos(rlon2)
        y = A * math.cos(rlat1) * math.sin(rlon1) + B * math.cos(rlat2) * math.sin(rlon2)
        z = A * math.sin(rlat1) + B * math.sin(rlat2)
        lat = math.degrees(math.atan2(z, math.sqrt(x*x + y*y)))
        lon = math.degrees(math.atan2(y, x))
        points.append((lat, lon))
    return points


# ===========================================================================
# 9. COMPUTE ENERGY FLOW BETWEEN ALL SUBJECTS
# ===========================================================================

def compute_energy_flows() -> List[Dict]:
    """Compute energy flow paths between all subjects on Earth.

    Flow types:
    1. Sphere → Sphere (toroidal transitions, 24h cycle)
    2. Sphere → Geological node (sphere projects to matching stress pair)
    3. Haplogroup → Geological node (soil/geology resonance)
    4. Haplogroup → Haplogroup (8D vector resonance, shared vectors)
    5. Attractor → All (energy/information/repair distribution)
    """

    flows: List[Dict] = []

    # --- 1. Sphere → Sphere toroidal transitions ---
    sphere_order = ["Sun", "Earth", "Moon", "CoMag", "Barnard"]
    toroidal_seq = [
        ("Barnard", "Sun", "reset_spark", "AB_integration", (21, 3), "138.88° spark: iron mass → proton spark"),
        ("Sun", "Earth", "light_dark", "AB_spark", (0, 3), "light → dark inversion"),
        ("Earth", "Moon", "o2_co2", "A_accumulate", (3, 9), "CO₂/osmotic → oxygen/salt"),
        ("Moon", "CoMag", "heat_cold", "O_accumulate", (9, 15), "heat/self-similarity → cold/rhythm"),
        ("CoMag", "Barnard", "matter_nonmatter", "B_accumulate", (15, 21), "mass/brightness → binding/무질량"),
    ]

    for src, dst, sp, phase, hours, desc in toroidal_seq:
        s = SPHERE_PROJECTIONS[src]
        d = SPHERE_PROJECTIONS[dst]
        dist = haversine(s["lat"], s["lon"], d["lat"], d["lon"])
        flows.append({
            "type": "sphere_to_sphere",
            "stress_pair": sp,
            "circadian_phase": phase,
            "hours": hours,
            "description": desc,
            "src": src, "dst": dst,
            "src_lat": s["lat"], "src_lon": s["lon"],
            "dst_lat": d["lat"], "dst_lon": d["lon"],
            "distance_km": round(dist, 1),
            "path": interpolate_great_circle(s["lat"], s["lon"], d["lat"], d["lon"]),
        })

    # --- 2. Sphere → Geological node (stress pair matching) ---
    for sphere_name, sphere in SPHERE_PROJECTIONS.items():
        sphere_dims = set(sphere["dims"])
        for geo_name, geo in GEO_NODE_COORDS.items():
            geo_sp = geo["stress_pair"]
            sp_info = STRESS_PAIRS.get(geo_sp, {})
            sp_dims = set(sp_info.get("dims", ()))
            # Check if sphere dims overlap with stress pair dims
            if sphere_dims & sp_dims:
                dist = haversine(sphere["lat"], sphere["lon"], geo["lat"], geo["lon"])
                if dist < 15000:  # within reasonable range
                    flows.append({
                        "type": "sphere_to_geo",
                        "stress_pair": geo_sp,
                        "src": sphere_name, "dst": geo_name,
                        "src_lat": sphere["lat"], "src_lon": sphere["lon"],
                        "dst_lat": geo["lat"], "dst_lon": geo["lon"],
                        "distance_km": round(dist, 1),
                        "path": interpolate_great_circle(
                            sphere["lat"], sphere["lon"], geo["lat"], geo["lon"], n=30
                        ),
                    })

    # --- 3. Haplogroup → Geological node (soil/geology resonance) ---
    # Map soil types to geological nodes
    soil_to_geo = {
        "chernozem": "craton", "mollisol": "craton",
        "calcisol": "steel", "limestone": "steel",
        "regosol": "cambisol",
        "podzol": "podzol", "spodosol": "podzol",
        "leptosol": "fold_belt", "mountain": "fold_belt",
        "arenosol": "basin", "desert": "basin",
        "solonchak": "oxidised_manganese", "saline": "oxidised_manganese",
        "fluvisol": "basin", "alluvial": "basin",
        "vertisol": "laterite", "clay": "laterite",
        "nitisol": "laterite", "iron-rich": "laterite",
        "ferralsol": "laterite", "plinthosol": "laterite",
        "andosol": "andosol", "volcanic": "andosol",
        "anthrosol": "cambisol", "rice": "cambisol",
        "acrisol": "laterite", "tropical": "laterite",
        "kastanozem": "craton", "steppe": "craton",
        "cryosol": "histosol", "permafrost": "histosol",
        "gelisol": "histosol",
        "gleysol": "histosol", "waterlogged": "histosol",
    }

    for hg_key, hg_data in Y_DNA.items():
        if hg_key not in Y_DNA_COORDS:
            continue
        hg_coord = Y_DNA_COORDS[hg_key]
        soil = hg_data.get("soil", "").lower()
        geology = hg_data.get("geology", "").lower()

        # Find matching geological node
        matched_geo = None
        for soil_key, geo_node in soil_to_geo.items():
            if soil_key in soil and geo_node in GEO_NODE_COORDS:
                matched_geo = geo_node
                break

        if not matched_geo:
            # Try geology keywords
            for geo_name, geo_data in GEO_NODE_COORDS.items():
                if any(kw in geology for kw in geo_data.get("geo_type", "").split("_")):
                    matched_geo = geo_name
                    break

        if matched_geo and matched_geo in GEO_NODE_COORDS:
            geo = GEO_NODE_COORDS[matched_geo]
            dist = haversine(hg_coord["lat"], hg_coord["lon"], geo["lat"], geo["lon"])
            flows.append({
                "type": "haplogroup_to_geo",
                "src": f"Y-DNA:{hg_key}", "dst": f"geo:{matched_geo}",
                "soil": hg_data.get("soil", ""),
                "src_lat": hg_coord["lat"], "src_lon": hg_coord["lon"],
                "dst_lat": geo["lat"], "dst_lon": geo["lon"],
                "distance_km": round(dist, 1),
                "path": interpolate_great_circle(
                    hg_coord["lat"], hg_coord["lon"], geo["lat"], geo["lon"], n=20
                ),
            })

    # --- 4. Haplogroup → Haplogroup (8D vector resonance) ---
    # Compute 8D similarity between all Y-DNA pairs
    hg_keys = list(Y_DNA_COORDS.keys())
    for i in range(len(hg_keys)):
        for j in range(i + 1, len(hg_keys)):
            k1, k2 = hg_keys[i], hg_keys[j]
            if k1 not in Y_DNA or k2 not in Y_DNA:
                continue
            v1 = Y_DNA[k1]["v"]
            v2 = Y_DNA[k2]["v"]
            # Cosine similarity
            dims = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]
            dot = sum(v1[d] * v2[d] for d in dims)
            mag1 = math.sqrt(sum(v1[d]**2 for d in dims))
            mag2 = math.sqrt(sum(v2[d]**2 for d in dims))
            if mag1 > 0 and mag2 > 0:
                sim = dot / (mag1 * mag2)
            else:
                sim = 0

            # Only draw flows for high similarity (> 0.95)
            if sim > 0.95:
                c1 = Y_DNA_COORDS[k1]
                c2 = Y_DNA_COORDS[k2]
                dist = haversine(c1["lat"], c1["lon"], c2["lat"], c2["lon"])
                flows.append({
                    "type": "haplogroup_resonance",
                    "similarity": round(sim, 4),
                    "src": f"Y-DNA:{k1}", "dst": f"Y-DNA:{k2}",
                    "src_lat": c1["lat"], "src_lon": c1["lon"],
                    "dst_lat": c2["lat"], "dst_lon": c2["lon"],
                    "distance_km": round(dist, 1),
                    "path": interpolate_great_circle(
                        c1["lat"], c1["lon"], c2["lat"], c2["lon"], n=20
                    ),
                })

    # --- 5. Attractor → All (distribution centers) ---
    for attr_name, attr in ATTRACTOR_CENTERS.items():
        # Connect to nearest 3 geological nodes
        geo_dists = []
        for geo_name, geo in GEO_NODE_COORDS.items():
            d = haversine(attr["lat"], attr["lon"], geo["lat"], geo["lon"])
            geo_dists.append((geo_name, geo, d))
        geo_dists.sort(key=lambda x: x[2])
        for geo_name, geo, dist in geo_dists[:3]:
            flows.append({
                "type": "attractor_to_geo",
                "attractor": attr_name,
                "src": f"attractor:{attr_name}", "dst": f"geo:{geo_name}",
                "src_lat": attr["lat"], "src_lon": attr["lon"],
                "dst_lat": geo["lat"], "dst_lon": geo["lon"],
                "distance_km": round(dist, 1),
                "path": interpolate_great_circle(
                    attr["lat"], attr["lon"], geo["lat"], geo["lon"], n=20
                ),
            })

    return flows


# ===========================================================================
# 10. PLOT WORLD MAP
# ===========================================================================

def plot_world_map(flows: List[Dict]):
    """Plot all subjects and energy flows on a world map."""

    fig, ax = plt.subplots(figsize=(28, 16), facecolor="#0a0a12")
    ax.set_facecolor("#0a0a12")

    # Simple world outline (coastline approximation using lat/lon grid)
    # Draw a basic grid as background
    for lat in range(-90, 91, 30):
        ax.axhline(lat, color="#1a1a2e", linewidth=0.5, alpha=0.5)
    for lon in range(-180, 181, 30):
        ax.axvline(lon, color="#1a1a2e", linewidth=0.5, alpha=0.5)

    # Draw equator and tropics
    ax.axhline(0, color="#333355", linewidth=1, alpha=0.6, linestyle="-")
    ax.axhline(23.5, color="#333355", linewidth=0.8, alpha=0.4, linestyle="--")
    ax.axhline(-23.5, color="#333355", linewidth=0.8, alpha=0.4, linestyle="--")

    text_color = "#E0E0E0"

    # Color scheme by type
    type_colors = {
        "sphere_to_sphere": "#FFD700",
        "sphere_to_geo": "#FF6B6B",
        "haplogroup_to_geo": "#4ECDC4",
        "haplogroup_resonance": "#95E1D3",
        "attractor_to_geo": "#C77DFF",
    }
    type_labels = {
        "sphere_to_sphere": "Sphere → Sphere (toroidal)",
        "sphere_to_geo": "Sphere → Geological",
        "haplogroup_to_geo": "Haplogroup → Geological (soil)",
        "haplogroup_resonance": "Haplogroup ↔ Haplogroup (8D resonance)",
        "attractor_to_geo": "Attractor → Geological",
    }

    # Draw flows
    for flow in flows:
        ftype = flow["type"]
        color = type_colors.get(ftype, "#666666")
        path = flow.get("path", [])
        if len(path) < 2:
            continue

        lats = [p[0] for p in path]
        lons = [p[1] for p in path]

        alpha = 0.7 if ftype == "sphere_to_sphere" else 0.3
        lw = 2.5 if ftype == "sphere_to_sphere" else 1.0

        ax.plot(lons, lats, color=color, linewidth=lw, alpha=alpha, zorder=2)

    # Plot Y-DNA haplogroups
    for hg_key, coord in Y_DNA_COORDS.items():
        ax.scatter(coord["lon"], coord["lat"], c="#4ECDC4", s=80, zorder=5,
                   edgecolors="#0a0a12", linewidth=0.5)
        ax.annotate(hg_key, (coord["lon"], coord["lat"]),
                    textcoords="offset points", xytext=(5, 5),
                    fontsize=7, color="#4ECDC4", fontweight="bold")

    # Plot mtDNA haplogroups
    for mt_key, coord in MTDNA_COORDS.items():
        ax.scatter(coord["lon"], coord["lat"], c="#A8E6CF", s=50, zorder=5,
                   marker="s", edgecolors="#0a0a12", linewidth=0.5)
        ax.annotate(f"mt:{mt_key}", (coord["lon"], coord["lat"]),
                    textcoords="offset points", xytext=(5, -8),
                    fontsize=6, color="#A8E6CF")

    # Plot geological nodes
    for geo_name, coord in GEO_NODE_COORDS.items():
        ax.scatter(coord["lon"], coord["lat"], c="#FF6B6B", s=60, zorder=5,
                   marker="^", edgecolors="#0a0a12", linewidth=0.5)
        ax.annotate(geo_name, (coord["lon"], coord["lat"]),
                    textcoords="offset points", xytext=(5, 5),
                    fontsize=6, color="#FF6B6B")

    # Plot spheres (large stars)
    sphere_markers = {"Sun": "*", "Earth": "o", "Moon": "D", "CoMag": "P", "Barnard": "X"}
    sphere_colors = {"Sun": "#FFD700", "Earth": "#4CAF50", "Moon": "#9E9E9E", "CoMag": "#E91E63", "Barnard": "#FF5722"}
    for sp_name, coord in SPHERE_PROJECTIONS.items():
        marker = sphere_markers.get(sp_name, "o")
        color = sphere_colors.get(sp_name, "#FFFFFF")
        ax.scatter(coord["lon"], coord["lat"], c=color, s=300, zorder=6,
                   marker=marker, edgecolors="#FFFFFF", linewidth=1)
        ax.annotate(sp_name, (coord["lon"], coord["lat"]),
                    textcoords="offset points", xytext=(8, 8),
                    fontsize=10, color=color, fontweight="bold")

    # Plot attractors
    for attr_name, coord in ATTRACTOR_CENTERS.items():
        ax.scatter(coord["lon"], coord["lat"], c="#C77DFF", s=200, zorder=6,
                   marker="*", edgecolors="#FFFFFF", linewidth=1, alpha=0.7)

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#4ECDC4", markersize=8, label="Y-DNA haplogroup"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="#A8E6CF", markersize=8, label="mtDNA haplogroup"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="#FF6B6B", markersize=8, label="Geological node"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor="#FFD700", markersize=12, label="Cosmic sphere"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor="#C77DFF", markersize=12, label="Attractor"),
    ]
    for ftype, color in type_colors.items():
        legend_elements.append(
            Line2D([0], [0], color=color, linewidth=2, label=type_labels.get(ftype, ftype))
        )

    ax.legend(handles=legend_elements, loc="lower left", fontsize=9,
              facecolor="#0a0a12", edgecolor="#333355", labelcolor=text_color)

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("Longitude", color=text_color, fontsize=12)
    ax.set_ylabel("Latitude", color=text_color, fontsize=12)
    ax.set_title(
        "Universe Energy Circulation Map — All Subjects on Earth\n"
        "Haplogroups + Geological Nodes + Cosmic Spheres + Toroidal Flow",
        color=text_color, fontsize=16, fontweight="bold"
    )
    ax.tick_params(colors=text_color)
    for spine in ax.spines.values():
        spine.set_color("#333355")

    plt.tight_layout()
    out_path = GEN_DIR / "earth_energy_map.png"
    fig.savefig(out_path, dpi=150, facecolor="#0a0a12", bbox_inches="tight")
    plt.close(fig)
    print(f"-> {out_path}")
    return out_path


# ===========================================================================
# 11. EXPORT COORDINATES + FLOWS
# ===========================================================================

def export_data(flows: List[Dict]):
    """Export all coordinates and flows as JSON."""

    all_subjects = {
        "Y_DNA": {k: {**v, **Y_DNA_COORDS[k]} for k, v in Y_DNA.items() if k in Y_DNA_COORDS},
        "mtDNA": {k: {**v, **MTDNA_COORDS[k]} for k, v in MTDNA.items() if k in MTDNA_COORDS},
        "ethnic_archetypes": {},
        "geological_nodes": GEO_NODE_COORDS,
        "spheres": SPHERE_PROJECTIONS,
        "attractors": ATTRACTOR_CENTERS,
    }

    # Add ethnic archetype coords
    for ek, ev in ETHNIC_ARCHETYPES.items():
        if ek in ETHNIC_COORDS:
            all_subjects["ethnic_archetypes"][ek] = {
                **ETHNIC_COORDS[ek],
                "vector8": ev.get("vector8", {}),
                "ydna": ev.get("ydna", ""),
                "mtdna": ev.get("mtdna", ""),
                "blood_type": ev.get("blood_type", ""),
            }

    # Export subjects
    subjects_path = GEN_DIR / "earth_subjects_coords.json"
    subjects_path.write_text(
        json.dumps(all_subjects, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    print(f"-> {subjects_path}")

    # Export flows (without path arrays for readability)
    flows_export = []
    for f in flows:
        f_copy = {k: v for k, v in f.items() if k != "path"}
        f_copy["has_path"] = True
        flows_export.append(f_copy)

    flows_path = GEN_DIR / "earth_energy_paths.json"
    flows_path.write_text(
        json.dumps({
            "total_flows": len(flows),
            "flows_by_type": {},
            "flows": flows_export,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"-> {flows_path}")

    return all_subjects


# ===========================================================================
# 12. PRINT REPORT
# ===========================================================================

def print_report(flows: List[Dict], subjects: Dict):
    """Print human-readable energy circulation report."""
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("UNIVERSE ENERGY CIRCULATION — EARTH COORDINATE MAP")
    lines.append("=" * 80)
    lines.append("")

    # Subject counts
    lines.append("■ Subjects on Earth")
    lines.append("-" * 80)
    lines.append(f"  Y-DNA haplogroups:     {len(subjects.get('Y_DNA', {}))}")
    lines.append(f"  mtDNA haplogroups:     {len(subjects.get('mtDNA', {}))}")
    lines.append(f"  Ethnic archetypes:     {len(subjects.get('ethnic_archetypes', {}))}")
    lines.append(f"  Geological nodes:      {len(subjects.get('geological_nodes', {}))}")
    lines.append(f"  Cosmic spheres:        {len(subjects.get('spheres', {}))}")
    lines.append(f"  Attractors:            {len(subjects.get('attractors', {}))}")
    total = sum(len(subjects.get(k, {})) for k in ["Y_DNA", "mtDNA", "ethnic_archetypes", "geological_nodes", "spheres", "attractors"])
    lines.append(f"  TOTAL:                 {total}")
    lines.append("")

    # Flow counts by type
    by_type: Dict[str, int] = {}
    for f in flows:
        by_type[f["type"]] = by_type.get(f["type"], 0) + 1

    lines.append("■ Energy Flow Paths")
    lines.append("-" * 80)
    for ftype, count in sorted(by_type.items(), key=lambda x: -x[1]):
        lines.append(f"  {ftype:30s}  {count:4d} flows")
    lines.append(f"  {'TOTAL':30s}  {len(flows):4d} flows")
    lines.append("")

    # Toroidal sphere transitions
    lines.append("■ Toroidal Sphere Transitions (24h Circadian)")
    lines.append("-" * 80)
    for f in flows:
        if f["type"] == "sphere_to_sphere":
            lines.append(f"  {f['src']:10s} → {f['dst']:10s}  "
                         f"stress={f['stress_pair']:20s}  "
                         f"hours={f['hours']}  "
                         f"dist={f['distance_km']:7.0f}km")
            lines.append(f"    {f['description']}")
    lines.append("")

    # Sphere → Geological node
    lines.append("■ Sphere → Geological Node Projections")
    lines.append("-" * 80)
    for f in flows:
        if f["type"] == "sphere_to_geo":
            lines.append(f"  {f['src']:10s} → {f['dst']:25s}  "
                         f"stress={f['stress_pair']:20s}  "
                         f"dist={f['distance_km']:7.0f}km")
    lines.append("")

    # Haplogroup → Geological node
    lines.append("■ Haplogroup → Geological Node (Soil Resonance)")
    lines.append("-" * 80)
    for f in flows:
        if f["type"] == "haplogroup_to_geo":
            lines.append(f"  {f['src']:15s} → {f['dst']:25s}  "
                         f"soil={f.get('soil', '?')[:30]:30s}  "
                         f"dist={f['distance_km']:7.0f}km")
    lines.append("")

    # Haplogroup resonance
    lines.append("■ Haplogroup ↔ Haplogroup (8D Vector Resonance > 0.95)")
    lines.append("-" * 80)
    for f in flows:
        if f["type"] == "haplogroup_resonance":
            lines.append(f"  {f['src']:15s} ↔ {f['dst']:15s}  "
                         f"sim={f['similarity']:.4f}  "
                         f"dist={f['distance_km']:7.0f}km")
    lines.append("")

    # Attractor → Geological
    lines.append("■ Attractor → Geological Node (Distribution)")
    lines.append("-" * 80)
    for f in flows:
        if f["type"] == "attractor_to_geo":
            lines.append(f"  {f['src']:20s} → {f['dst']:25s}  "
                         f"dist={f['distance_km']:7.0f}km")
    lines.append("")

    # Key insight: energy circulation pattern
    lines.append("■ Energy Circulation Pattern")
    lines.append("-" * 80)
    lines.append("  1. Barnard(S.Pacific) → Sun(Tropic of Cancer)  [21-3h: 138.88° spark reset]")
    lines.append("  2. Sun → Earth(Equator)                        [0-3h: light→dark]")
    lines.append("  3. Earth → Moon(Tropic of Capricorn)            [3-9h: CO₂→O₂]")
    lines.append("  4. Moon → CoMag(N.Asia)                        [9-15h: heat→cold]")
    lines.append("  5. CoMag → Barnard(S.Pacific)                  [15-21h: matter→non-matter]")
    lines.append("")
    lines.append("  Each sphere projects to geological nodes with matching stress pair.")
    lines.append("  Haplogroups bind to geological nodes via soil type resonance.")
    lines.append("  8D vector similarity creates inter-haplogroup resonance channels.")
    lines.append("")

    text = "\n".join(lines)
    (GEN_DIR / "earth_energy_report.txt").write_text(text, encoding="utf-8")
    print(text[:3000])
    print(f"\n... full report -> {GEN_DIR / 'earth_energy_report.txt'}")


# ===========================================================================
# MAIN
# ===========================================================================

if __name__ == "__main__":
    print("Computing energy flows between all universe subjects...")
    flows = compute_energy_flows()
    print(f"  {len(flows)} energy flow paths computed")

    subjects = export_data(flows)
    plot_world_map(flows)
    print_report(flows, subjects)
