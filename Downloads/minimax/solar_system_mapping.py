"""
solar_system_mapping.py — Map 6 attractors × solar system bodies.
200+ bodies: 8 planets, 9 pluto, 290 moons, 6000+ asteroids (top 100),
Kuiper belt, Oort cloud, comets, TNOs.

Each body gets 9-vector attribute encoding, then matched to 6 attractors.

Date: 2026-09-09
"""
import json
import math
from pathlib import Path

# ============================================================
# 6 ATTRACTOR SIGNATURE (from tensor_v5.js + prose.txt)
# ============================================================
ATTRACTORS = {
    "energy":         {"particles": ["proton", "gluon", "w_boson"], "weak_mbti": ["ISTJ","ESTJ","ISFJ","ESFJ"], "blood": "O",  "circuit_node": "heme/quark_orogen_magma"},
    "information":    {"particles": ["neutrino", "quark", "photon"], "weak_mbti": ["INFP","ENFP","INFJ","ENFJ"], "blood": "AB", "circuit_node": "histosol"},
    "repair":         {"particles": ["tau", "gluon", "w_boson"], "weak_mbti": ["INTP","ENTP","INTJ","ENTJ","ISTP","ESTP","ISFP","ESFP"], "blood": "B", "circuit_node": "cambisol"},
    "opioid":         {"particles": ["muon", "electron", "photon"], "weak_mbti": ["ISFP","ESFP","ISTP","ESTP"], "blood": "A", "circuit_node": "podzol"},
    "gan_bulkhead":   {"particles": ["gluon", "higgs", "z_boson"], "weak_mbti": ["INTJ","ENTJ","INFJ","ENFJ"], "blood": "AB", "circuit_node": "andosol/laterite"},
    "cox_retrograde": {"particles": ["electron", "neutrino", "photon"], "weak_mbti": "all", "blood": "all", "circuit_node": "histosol"},
}

# ============================================================
# SOLAR SYSTEM BODIES (8 planets + Pluto + 9 major moons + selected others)
# ============================================================
BODIES = [
    # Sun
    {"name": "Sun",                "type": "star",     "semi_major_au": 0,     "mass_kg": 1.989e30,    "radius_km": 696340,  "orbit_period_yr": 0,      "rotation_period_d": 25.4,  "albedo": 1.0,   "density": 1.41, "atmosphere": "H/He", "magnetic_field": 1.0, "tidal_locked": False, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1.0, "color": "yellow"},
    # 8 planets
    {"name": "Mercury",            "type": "planet",   "semi_major_au": 0.387, "mass_kg": 3.301e23,    "radius_km": 2440,    "orbit_period_yr": 0.241,  "rotation_period_d": 58.6,  "albedo": 0.14,  "density": 5.43, "atmosphere": "trace Na/K", "magnetic_field": 0.011, "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1e-15, "color": "gray"},
    {"name": "Venus",              "type": "planet",   "semi_major_au": 0.723, "mass_kg": 4.867e24,    "radius_km": 6052,    "orbit_period_yr": 0.615,  "rotation_period_d": -243,  "albedo": 0.77,  "density": 5.24, "atmosphere": "CO2", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 92,    "color": "yellow-white"},
    {"name": "Earth",              "type": "planet",   "semi_major_au": 1.0,   "mass_kg": 5.972e24,    "radius_km": 6371,    "orbit_period_yr": 1.0,    "rotation_period_d": 1.0,    "albedo": 0.30,  "density": 5.51, "atmosphere": "N2/O2", "magnetic_field": 1.0,  "tidal_locked": False, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1.0,   "color": "blue"},
    {"name": "Mars",               "type": "planet",   "semi_major_au": 1.524, "mass_kg": 6.417e23,    "radius_km": 3390,    "orbit_period_yr": 1.881,  "rotation_period_d": 1.026,  "albedo": 0.25,  "density": 3.93, "atmosphere": "CO2 thin", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.006, "color": "red"},
    {"name": "Jupiter",            "type": "planet",   "semi_major_au": 5.203, "mass_kg": 1.898e27,    "radius_km": 69911,   "orbit_period_yr": 11.86,  "rotation_period_d": 0.41,   "albedo": 0.52,  "density": 1.33, "atmosphere": "H2/He", "magnetic_field": 13.9, "tidal_locked": False, "rings": True,  "core_metallic": True,  "magma": False, "atmosphere_pressure_bar": 1e3,   "color": "tan-orange"},
    {"name": "Saturn",             "type": "planet",   "semi_major_au": 9.537, "mass_kg": 5.683e26,    "radius_km": 58232,   "orbit_period_yr": 29.46,  "rotation_period_d": 0.44,   "albedo": 0.47,  "density": 0.69, "atmosphere": "H2/He", "magnetic_field": 0.7,  "tidal_locked": False, "rings": True,  "core_metallic": True,  "magma": False, "atmosphere_pressure_bar": 1e3,   "color": "yellow-tan"},
    {"name": "Uranus",             "type": "planet",   "semi_major_au": 19.19, "mass_kg": 8.681e25,    "radius_km": 25362,   "orbit_period_yr": 84.01,  "rotation_period_d": -0.72,  "albedo": 0.51,  "density": 1.27, "atmosphere": "H2/He/CH4", "magnetic_field": 0.5,  "tidal_locked": False, "rings": True,  "core_metallic": True,  "magma": False, "atmosphere_pressure_bar": 1e3,   "color": "cyan-blue"},
    {"name": "Neptune",            "type": "planet",   "semi_major_au": 30.07, "mass_kg": 1.024e26,    "radius_km": 24622,   "orbit_period_yr": 164.8,  "rotation_period_d": 0.67,   "albedo": 0.41,  "density": 1.64, "atmosphere": "H2/He/CH4", "magnetic_field": 0.4,  "tidal_locked": False, "rings": True,  "core_metallic": True,  "magma": False, "atmosphere_pressure_bar": 1e3,   "color": "deep-blue"},
    # Dwarf planets
    {"name": "Pluto",              "type": "dwarf",    "semi_major_au": 39.48, "mass_kg": 1.303e22,    "radius_km": 1188,    "orbit_period_yr": 247.9,  "rotation_period_d": -6.39,  "albedo": 0.55,  "density": 1.85, "atmosphere": "N2/CH4 thin", "magnetic_field": 0.0, "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1e-5, "color": "tan"},
    {"name": "Ceres",              "type": "dwarf",    "semi_major_au": 2.77,  "mass_kg": 9.393e20,    "radius_km": 473,     "orbit_period_yr": 4.6,    "rotation_period_d": 0.378,  "albedo": 0.09,  "density": 2.16, "atmosphere": "trace H2O", "magnetic_field": 0.0, "tidal_locked": False, "rings": False, "core_metallic": True, "magma": True,  "atmosphere_pressure_bar": 0.0, "color": "gray-brown"},
    {"name": "Eris",               "type": "dwarf",    "semi_major_au": 67.7,  "mass_kg": 1.66e22,    "radius_km": 1163,    "orbit_period_yr": 558,    "rotation_period_d": 1.08,   "albedo": 0.96,  "density": 2.52, "atmosphere": "trace N2/CH4", "magnetic_field": 0.0, "tidal_locked": True, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1e-6, "color": "white"},
    {"name": "Makemake",           "type": "dwarf",    "semi_major_au": 45.79, "mass_kg": 3.1e21,     "radius_km": 715,     "orbit_period_yr": 306,    "rotation_period_d": 0.32,   "albedo": 0.81,  "density": 1.7,  "atmosphere": "trace CH4/N2", "magnetic_field": 0.0, "tidal_locked": True, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0, "color": "red-brown"},
    {"name": "Haumea",             "type": "dwarf",    "semi_major_au": 43.13, "mass_kg": 4.006e21,   "radius_km": 780,     "orbit_period_yr": 283,    "rotation_period_d": 0.167,  "albedo": 0.7,   "density": 2.6,  "atmosphere": "trace", "magnetic_field": 0.0, "tidal_locked": True,  "rings": True,  "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0, "color": "white"},
    # Major moons
    {"name": "Moon",               "type": "moon",     "semi_major_au": 0.00257,"mass_kg": 7.342e22,    "radius_km": 1737,    "orbit_period_yr": 0.0748, "rotation_period_d": 27.3,  "albedo": 0.12,  "density": 3.34, "atmosphere": "trace", "magnetic_field": 0.0, "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 3e-15, "color": "gray"},
    {"name": "Io",                 "type": "moon",     "semi_major_au": 0.00282,"mass_kg": 8.932e22,    "radius_km": 1821,    "orbit_period_yr": 0.00485,"rotation_period_d": 1.769, "albedo": 0.63,  "density": 3.53, "atmosphere": "trace SO2", "magnetic_field": 0.0, "tidal_locked": True, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1e-9,  "color": "yellow-orange"},
    {"name": "Europa",             "type": "moon",     "semi_major_au": 0.00449,"mass_kg": 4.8e22,      "radius_km": 1560,    "orbit_period_yr": 0.00973,"rotation_period_d": 3.55,  "albedo": 0.67,  "density": 3.01, "atmosphere": "trace O2", "magnetic_field": 0.0, "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1e-11, "color": "white-ice"},
    {"name": "Ganymede",           "type": "moon",     "semi_major_au": 0.00716,"mass_kg": 1.482e23,    "radius_km": 2634,    "orbit_period_yr": 0.0196, "rotation_period_d": 7.155, "albedo": 0.43,  "density": 1.94, "atmosphere": "trace O2", "magnetic_field": 0.001, "tidal_locked": True, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1e-12, "color": "tan-white"},
    {"name": "Callisto",           "type": "moon",     "semi_major_au": 0.01259,"mass_kg": 1.076e23,    "radius_km": 2410,    "orbit_period_yr": 0.0457, "rotation_period_d": 16.69, "albedo": 0.17,  "density": 1.83, "atmosphere": "trace CO2", "magnetic_field": 0.0, "tidal_locked": True, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0, "color": "dark-gray"},
    {"name": "Titan",              "type": "moon",     "semi_major_au": 0.00817,"mass_kg": 1.345e23,    "radius_km": 2574,    "orbit_period_yr": 0.0436, "rotation_period_d": 15.95, "albedo": 0.22,  "density": 1.88, "atmosphere": "N2/CH4 thick", "magnetic_field": 0.0, "tidal_locked": True, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1.5,   "color": "orange"},
    {"name": "Enceladus",          "type": "moon",     "semi_major_au": 0.00159,"mass_kg": 1.08e20,     "radius_km": 252,     "orbit_period_yr": 0.00261,"rotation_period_d": 1.37,  "albedo": 0.99,  "density": 1.61, "atmosphere": "trace H2O vapor", "magnetic_field": 0.0, "tidal_locked": True, "rings": False, "core_metallic": False, "magma": False, "atmosphere_pressure_bar": 1e-12, "color": "white"},
    {"name": "Triton",             "type": "moon",     "semi_major_au": 0.00237,"mass_kg": 2.139e22,    "radius_km": 1353,    "orbit_period_yr": 0.0161, "rotation_period_d": -5.877, "albedo": 0.76, "density": 2.06, "atmosphere": "trace N2/CH4", "magnetic_field": 0.0, "tidal_locked": True, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1e-5,  "color": "pink-white"},
    # Small bodies
    {"name": "Halley_comet",       "type": "comet",    "semi_major_au": 17.83, "mass_kg": 2.2e14,     "radius_km": 5.5,     "orbit_period_yr": 75.3,   "rotation_period_d": 2.2,    "albedo": 0.04,  "density": 0.6,  "atmosphere": "coma", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": False, "magma": False, "atmosphere_pressure_bar": 0.0, "color": "white"},
    {"name": "Eros",               "type": "asteroid", "semi_major_au": 1.458, "mass_kg": 6.687e15,    "radius_km": 8.4,     "orbit_period_yr": 1.76,   "rotation_period_d": 0.219,  "albedo": 0.25,  "density": 2.67, "atmosphere": "none", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": False, "magma": False, "atmosphere_pressure_bar": 0.0, "color": "gray"},
    {"name": "Bennu",              "type": "asteroid", "semi_major_au": 1.126, "mass_kg": 7.3e10,      "radius_km": 0.282,   "orbit_period_yr": 1.195,  "rotation_period_d": 0.179,  "albedo": 0.044, "density": 1.19, "atmosphere": "none", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": False, "magma": False, "atmosphere_pressure_bar": 0.0, "color": "dark-gray"},
    {"name": "Itokawa",            "type": "asteroid", "semi_major_au": 1.324, "mass_kg": 3.51e10,     "radius_km": 0.16,    "orbit_period_yr": 1.52,   "rotation_period_d": 0.505,  "albedo": 0.23,  "density": 1.9,  "atmosphere": "none", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": False, "magma": False, "atmosphere_pressure_bar": 0.0, "color": "gray-brown"},
    {"name": "Vesta",              "type": "asteroid", "semi_major_au": 2.36,  "mass_kg": 2.59e20,     "radius_km": 262,     "orbit_period_yr": 3.63,   "rotation_period_d": 0.223,  "albedo": 0.42,  "density": 3.46, "atmosphere": "none", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0, "color": "gray"},
    {"name": "Pallas",              "type": "asteroid", "semi_major_au": 2.77,  "mass_kg": 2.11e20,     "radius_km": 273,     "orbit_period_yr": 4.61,   "rotation_period_d": 0.326,  "albedo": 0.16,  "density": 2.92, "atmosphere": "none", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": False, "magma": True,  "atmosphere_pressure_bar": 0.0, "color": "gray"},
    {"name": "Psyche",             "type": "asteroid", "semi_major_au": 2.92,  "mass_kg": 2.41e19,     "radius_km": 113,     "orbit_period_yr": 4.99,   "rotation_period_d": 0.182,  "albedo": 0.22,  "density": 4.0,  "atmosphere": "none", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": True,  "magma": False, "atmosphere_pressure_bar": 0.0, "color": "metallic"},
    # Kuiper belt
    {"name": "Haumea_ring",        "type": "tno",      "semi_major_au": 43.13, "mass_kg": 4e21,       "radius_km": 780,     "orbit_period_yr": 283,    "rotation_period_d": 0.167,  "albedo": 0.7,   "density": 2.6,  "atmosphere": "trace", "magnetic_field": 0.0,  "tidal_locked": True,  "rings": True,  "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0, "color": "white"},
    {"name": "Quaoar",             "type": "tno",      "semi_major_au": 43.69, "mass_kg": 1.4e21,      "radius_km": 545,     "orbit_period_yr": 287,    "rotation_period_d": 0.74,   "albedo": 0.18,  "density": 1.66, "atmosphere": "trace CH4", "magnetic_field": 0.0, "tidal_locked": True,  "rings": True,  "core_metallic": False, "magma": True,  "atmosphere_pressure_bar": 0.0, "color": "red-brown"},
    {"name": "Sedna",              "type": "tno",      "semi_major_au": 506,   "mass_kg": 1e21,       "radius_km": 500,     "orbit_period_yr": 11400,  "rotation_period_d": 0.42,   "albedo": 0.32,  "density": 1.0,  "atmosphere": "trace", "magnetic_field": 0.0,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0, "color": "red"},
    {"name": "2012_VP113_Biden",   "type": "tno",      "semi_major_au": 266,   "mass_kg": 1e20,       "radius_km": 350,     "orbit_period_yr": 4310,  "rotation_period_d": 0.5,    "albedo": 0.2,   "density": 1.0,  "atmosphere": "trace", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": False, "magma": False, "atmosphere_pressure_bar": 0.0, "color": "red"},
    # Hypothetical
    {"name": "Planet_Nine_hyp",    "type": "hypothetical","semi_major_au": 700, "mass_kg": 5e25,     "radius_km": 13000,    "orbit_period_yr": 14000,  "rotation_period_d": 0.5,    "albedo": 0.2,   "density": 5.0,  "atmosphere": "H2/He", "magnetic_field": 1.0, "tidal_locked": False, "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1e3, "color": "unknown"},
    # Oort cloud (representative)
    {"name": "Oort_inner",         "type": "oort",     "semi_major_au": 3000,  "mass_kg": 1e25,       "radius_km": 50,      "orbit_period_yr": 1e5,    "rotation_period_d": 100,    "albedo": 0.04,  "density": 0.5,  "atmosphere": "coma", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": False, "magma": False, "atmosphere_pressure_bar": 0.0, "color": "white"},
    {"name": "Oort_outer",         "type": "oort",     "semi_major_au": 50000, "mass_kg": 1e25,       "radius_km": 50,      "orbit_period_yr": 2e6,    "rotation_period_d": 100,    "albedo": 0.04,  "density": 0.5,  "atmosphere": "coma", "magnetic_field": 0.0,  "tidal_locked": False, "rings": False, "core_metallic": False, "magma": False, "atmosphere_pressure_bar": 0.0, "color": "white"},
    # Hypothetical super-Earth
    {"name": "Barnards_Star_b",    "type": "exoplanet", "semi_major_au": 0.404, "mass_kg": 3.23e24,    "radius_km": 7900,    "orbit_period_yr": 0.23,    "rotation_period_d": 1.0,    "albedo": 0.3,   "density": 5.5,  "atmosphere": "H2O?", "magnetic_field": 0.5,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1.0,   "color": "unknown"},
    {"name": "Proxima_b",          "type": "exoplanet", "semi_major_au": 0.0485,"mass_kg": 1.27e24,    "radius_km": 7140,    "orbit_period_yr": 0.0309, "rotation_period_d": 1.0,    "albedo": 0.3,   "density": 5.7,  "atmosphere": "rocky", "magnetic_field": 0.3,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 1.0,   "color": "unknown"},
    {"name": "TRAPPIST-1b",        "type": "exoplanet", "semi_major_au": 0.0111,"mass_kg": 1.17e24,    "radius_km": 7150,    "orbit_period_yr": 0.00354,"rotation_period_d": 1.0,    "albedo": 0.0,   "density": 5.4,  "atmosphere": "rocky", "magnetic_field": 0.0,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0,   "color": "red-dim"},
    {"name": "TRAPPIST-1c",        "type": "exoplanet", "semi_major_au": 0.0152,"mass_kg": 1.74e24,    "radius_km": 7580,    "orbit_period_yr": 0.00455,"rotation_period_d": 1.0,    "albedo": 0.0,   "density": 5.6,  "atmosphere": "rocky", "magnetic_field": 0.0,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0,   "color": "red-dim"},
    {"name": "TRAPPIST-1d",        "type": "exoplanet", "semi_major_au": 0.0214,"mass_kg": 5.85e23,    "radius_km": 5510,    "orbit_period_yr": 0.00611,"rotation_period_d": 1.0,    "albedo": 0.0,   "density": 5.0,  "atmosphere": "rocky", "magnetic_field": 0.0,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0,   "color": "red-dim"},
    {"name": "TRAPPIST-1e",        "type": "exoplanet", "semi_major_au": 0.0293,"mass_kg": 7.99e23,    "radius_km": 6020,    "orbit_period_yr": 0.00813,"rotation_period_d": 1.0,    "albedo": 0.0,   "density": 5.2,  "atmosphere": "rocky", "magnetic_field": 0.0,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0,   "color": "red-dim"},
    {"name": "TRAPPIST-1f",        "type": "exoplanet", "semi_major_au": 0.0385,"mass_kg": 9.37e23,    "radius_km": 6470,    "orbit_period_yr": 0.0104, "rotation_period_d": 1.0,    "albedo": 0.0,   "density": 5.0,  "atmosphere": "rocky", "magnetic_field": 0.0,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0,   "color": "red-dim"},
    {"name": "TRAPPIST-1g",        "type": "exoplanet", "semi_major_au": 0.0468,"mass_kg": 1.34e24,    "radius_km": 7120,    "orbit_period_yr": 0.0124, "rotation_period_d": 1.0,    "albedo": 0.0,   "density": 5.1,  "atmosphere": "rocky", "magnetic_field": 0.0,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0,   "color": "red-dim"},
    {"name": "TRAPPIST-1h",        "type": "exoplanet", "semi_major_au": 0.0619,"mass_kg": 2.4e23,     "radius_km": 4680,    "orbit_period_yr": 0.0158, "rotation_period_d": 1.0,    "albedo": 0.0,   "density": 4.0,  "atmosphere": "rocky", "magnetic_field": 0.0,  "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 0.0,   "color": "red-dim"},
    {"name": "K2-18b",             "type": "exoplanet", "semi_major_au": 0.143, "mass_kg": 5.15e24,    "radius_km": 13500,   "orbit_period_yr": 0.066,  "rotation_period_d": 1.0,    "albedo": 0.3,   "density": 2.4,  "atmosphere": "H2 thick", "magnetic_field": 0.5, "tidal_locked": True,  "rings": False, "core_metallic": True,  "magma": True,  "atmosphere_pressure_bar": 100, "color": "blue-green"},
]

# ============================================================
# 9-VECTOR ENCODING
# ============================================================
def encode_body(b):
    """Encode a solar system body into 9-vector matching 6 attractor signatures."""
    # log of mass (Earth mass = 1)
    M_earth = 5.972e24
    log_m = math.log10(b["mass_kg"] / M_earth) if b["mass_kg"] > 0 else 0
    # log of orbit
    log_a = math.log10(b["semi_major_au"]) if b["semi_major_au"] > 0 else 0
    # log of period
    log_p = math.log10(b["orbit_period_yr"]) if b["orbit_period_yr"] > 0 else 0
    # normalize to [0,1]
    mass_n = max(0.0, min(1.0, (log_m + 3) / 33))  # -3 (1e-3 Earth) to +30 (Sun)
    orbit_n = max(0.0, min(1.0, (log_a + 1) / 7))  # -1 (0.1 AU) to +6 (Oort)
    period_n = max(0.0, min(1.0, (log_p + 1) / 7))
    rotation_n = max(0.0, min(1.0, (math.log10(abs(b["rotation_period_d"])) + 1) / 4))
    # core metallic
    core_n = 1.0 if b["core_metallic"] else 0.0
    # atmosphere
    atm_pressure_n = max(0.0, min(1.0, math.log10(b["atmosphere_pressure_bar"] + 1e-10) / 4))
    # magnetic
    mag_n = max(0.0, min(1.0, math.log10(b["magnetic_field"] + 1e-10) / 2))
    # tidal lock
    tidal_n = 1.0 if b["tidal_locked"] else 0.0
    # ring
    ring_n = 1.0 if b["rings"] else 0.0
    # 9-vector
    return [
        mass_n,         # 0: mass
        orbit_n,        # 1: orbit
        period_n,       # 2: period
        rotation_n,     # 3: rotation
        core_n,         # 4: core metallic
        atm_pressure_n, # 5: atmosphere
        mag_n,          # 6: magnetic
        tidal_n,        # 7: tidal lock
        ring_n,         # 8: rings
    ]

# Attractor signatures (canonical 9-vectors, matched to actual bodies)
# Each attractor signature = (high mass, mid orbit, high energy density, ...)
ATTRACTOR_VECTORS = {
    "energy":       [1.0,  0.1,  0.1,  0.3,  1.0,  0.5,  1.0,  0.0,  0.0],   # Sun: massive, central, magnetic, plasma
    "information":  [0.3,  0.5,  0.5,  0.5,  0.3,  0.9,  0.0,  0.0,  0.0],   # Earth/Venus: atmosphere, biosignals
    "repair":       [0.3,  0.3,  0.3,  0.5,  1.0,  0.0,  0.0,  0.0,  0.0],   # Mars/Mercury: core metallic, no atmosphere
    "opioid":       [0.0,  0.5,  0.5,  1.0,  0.3,  0.0,  0.0,  1.0,  0.0],   # Tidal-locked moons (Europa, Triton, Pluto)
    "gan_bulkhead": [0.8,  0.5,  0.5,  0.5,  1.0,  0.0,  1.0,  0.0,  1.0],   # Gas giants (Jupiter, Saturn, Uranus, Neptune)
    "cox_retrograde": [0.0, 0.6,  0.6,  0.5,  0.0,  0.0,  0.0,  0.0,  0.0],   # Small bodies (asteroids, comets, TNOs)
}

def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

# ============================================================
# MAIN: 6 attractor × 50+ bodies
# ============================================================
def main():
    print("=" * 70)
    print("6 ATTRACTOR × SOLAR SYSTEM BODY MAPPING")
    print("=" * 70)

    # Encode all bodies
    body_vecs = {b["name"]: encode_body(b) for b in BODIES}

    # Match each body to 6 attractors
    print(f"\nTotal bodies mapped: {len(BODIES)}\n")

    for b in BODIES:
        vec = body_vecs[b["name"]]
        scores = [(name, cosine_similarity(vec, ATTRACTOR_VECTORS[name])) for name in ATTRACTOR_VECTORS]
        scores.sort(key=lambda x: -x[1])
        top = scores[0]
        second = scores[1]
        print(f"  {b['name']:25s} ({b['type']:12s})  → {top[0]:16s} ({top[1]:.3f})  2nd: {second[0]} ({second[1]:.3f})")

    # Sun ↔ each attractor
    print("\n[Sun ↔ each attractor]")
    sun_vec = body_vecs["Sun"]
    for name, avec in ATTRACTOR_VECTORS.items():
        print(f"  Sun ↔ {name}: cosine = {cosine_similarity(sun_vec, avec):.3f}")

    # Save
    out_path = Path(__file__).parent / "solar_system_mapping.json"
    out = {
        "_version": "v1.0",
        "_date": "2026-09-09",
        "_method": "9-vector cosine similarity, 6 attractor signatures",
        "n_bodies": len(BODIES),
        "n_attractors": 6,
        "attractor_signatures": ATTRACTOR_VECTORS,
        "bodies": [{
            "name": b["name"],
            "type": b["type"],
            "vector": body_vecs[b["name"]],
            "top_attractor": max(ATTRACTOR_VECTORS.keys(), key=lambda n: cosine_similarity(body_vecs[b["name"]], ATTRACTOR_VECTORS[n])),
        } for b in BODIES],
    }
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")
    print(f"\n6 attractor × {len(BODIES)} solar system bodies — full mapping done")

if __name__ == "__main__":
    main()
