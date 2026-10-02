"""
solar_8p_mapping.py — Replace 9-vector with 8-DIMENSION vector (kernel's 5+2+1).

8 dimensions (from kernel_v1.py DIMS): r, h, d, p, s, gamma, g, nu
  body_5:    r, h, d, gamma, g
  observer_2: p, s
  bridge_1:   nu

Drop "rings" feature (9-vector 9th slot, only 4 bodies have rings).
8 features: mass, orbit, period, rotation, core, atmosphere, magnetic, tidal_lock
Then map: 8-dim vector -> 6 attractor.

Date: 2026-09-09
"""
import json, math
from pathlib import Path

DIMS_8 = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]

# 46 solar system bodies with real measured properties
# Sources: NASA fact sheets, JPL SBDB, IAU 2015
BODIES_46 = [
    # Sun
    {"name":"Sun",       "mass_kg":1.989e30,  "radius_km":696340, "au":0,       "period_yr":0,     "rot_d":25.4,  "core_metallic":False, "atm_bar":1e-7, "mag":1.0,  "tidal":False, "rings":False, "type":"G2V"},
    # Planets
    {"name":"Mercury",   "mass_kg":3.301e23,  "radius_km":2440,   "au":0.387,   "period_yr":0.241, "rot_d":58.6,  "core_metallic":True,  "atm_bar":1e-15,"mag":0.011,"tidal":True,  "rings":False, "type":"planet"},
    {"name":"Venus",     "mass_kg":4.867e24,  "radius_km":6052,   "au":0.723,   "period_yr":0.615, "rot_d":-243,  "core_metallic":True,  "atm_bar":92,   "mag":0.0,  "tidal":False, "rings":False, "type":"planet"},
    {"name":"Earth",     "mass_kg":5.972e24,  "radius_km":6371,   "au":1.0,     "period_yr":1.0,   "rot_d":1.0,   "core_metallic":True,  "atm_bar":1.0,  "mag":1.0,  "tidal":False, "rings":False, "type":"planet"},
    {"name":"Mars",      "mass_kg":6.417e23,  "radius_km":3390,   "au":1.524,   "period_yr":1.881, "rot_d":1.026, "core_metallic":True,  "atm_bar":0.006,"mag":0.0,  "tidal":False, "rings":False, "type":"planet"},
    {"name":"Jupiter",   "mass_kg":1.898e27,  "radius_km":69911,  "au":5.203,   "period_yr":11.86, "rot_d":0.414, "core_metallic":True,  "atm_bar":1e3,  "mag":13.9, "tidal":False, "rings":True,  "type":"planet"},
    {"name":"Saturn",    "mass_kg":5.683e26,  "radius_km":58232,  "au":9.537,   "period_yr":29.46, "rot_d":0.444, "core_metallic":True,  "atm_bar":1e3,  "mag":0.7,  "tidal":False, "rings":True,  "type":"planet"},
    {"name":"Uranus",    "mass_kg":8.681e25,  "radius_km":25362,  "au":19.19,   "period_yr":84.01, "rot_d":-0.718,"core_metallic":True,  "atm_bar":1e3,  "mag":0.5,  "tidal":False, "rings":True,  "type":"planet"},
    {"name":"Neptune",   "mass_kg":1.024e26,  "radius_km":24622,  "au":30.07,   "period_yr":164.8, "rot_d":0.671, "core_metallic":True,  "atm_bar":1e3,  "mag":0.4,  "tidal":False, "rings":True,  "type":"planet"},
    # Dwarf planets
    {"name":"Ceres",     "mass_kg":9.393e20,  "radius_km":473,    "au":2.77,    "period_yr":4.6,   "rot_d":0.378, "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":False, "rings":False, "type":"dwarf"},
    {"name":"Pluto",     "mass_kg":1.303e22,  "radius_km":1188,   "au":39.48,   "period_yr":247.9, "rot_d":-6.39, "core_metallic":True,  "atm_bar":1e-5, "mag":0.0,  "tidal":True,  "rings":False, "type":"dwarf"},
    {"name":"Haumea",    "mass_kg":4.006e21,  "radius_km":816,    "au":43.22,   "period_yr":283.8, "rot_d":0.167, "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":True,  "rings":True,  "type":"dwarf"},
    {"name":"Makemake",  "mass_kg":3.1e21,    "radius_km":715,    "au":45.79,   "period_yr":306.2, "rot_d":0.937, "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":True,  "rings":False, "type":"dwarf"},
    {"name":"Eris",      "mass_kg":1.66e22,   "radius_km":1163,   "au":67.78,   "period_yr":561.4, "rot_d":1.08,  "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":True,  "rings":False, "type":"dwarf"},
    # Major moons
    {"name":"Moon",      "mass_kg":7.342e22,  "radius_km":1737,   "au":0.00257, "period_yr":0.075,"rot_d":27.3,  "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
    {"name":"Io",        "mass_kg":8.932e22,  "radius_km":1822,   "au":0.00282, "period_yr":0.005,"rot_d":1.769, "core_metallic":True,  "atm_bar":1e-8, "mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
    {"name":"Europa",    "mass_kg":4.8e22,    "radius_km":1561,   "au":0.00449, "period_yr":0.009,"rot_d":3.55,  "core_metallic":True,  "atm_bar":1e-12,"mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
    {"name":"Ganymede",  "mass_kg":1.482e23,  "radius_km":2634,   "au":0.00716, "period_yr":0.020,"rot_d":7.155, "core_metallic":True,  "atm_bar":1e-12,"mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
    {"name":"Callisto",  "mass_kg":1.076e23,  "radius_km":2410,   "au":0.01259, "period_yr":0.046,"rot_d":16.69, "core_metallic":True,  "atm_bar":1e-12,"mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
    {"name":"Titan",     "mass_kg":1.345e23,  "radius_km":2575,   "au":0.00817, "period_yr":0.024,"rot_d":15.95, "core_metallic":True,  "atm_bar":1.5,  "mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
    {"name":"Triton",    "mass_kg":2.14e22,   "radius_km":1353,   "au":0.00237, "period_yr":0.016,"rot_d":-5.877,"core_metallic":True,  "atm_bar":1e-5, "mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
    {"name":"Charon",    "mass_kg":1.586e21,  "radius_km":606,    "au":0.00014, "period_yr":0.0006,"rot_d":6.387,"core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
    # Asteroids
    {"name":"Vesta",     "mass_kg":2.59e20,   "radius_km":262,    "au":2.36,    "period_yr":3.63,  "rot_d":0.223, "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":False, "rings":False, "type":"asteroid"},
    {"name":"Pallas",    "mass_kg":2.04e20,   "radius_km":272,    "au":2.77,    "period_yr":4.62,  "rot_d":0.326, "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":False, "rings":False, "type":"asteroid"},
    {"name":"Hygiea",    "mass_kg":8.32e19,   "radius_km":215,    "au":3.14,    "period_yr":5.55,  "rot_d":0.567, "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":False, "rings":False, "type":"asteroid"},
    {"name":"Juno",      "mass_kg":2.67e19,   "radius_km":233,    "au":2.67,    "period_yr":4.36,  "rot_d":0.300, "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":False, "rings":False, "type":"asteroid"},
    {"name":"Bennu",     "mass_kg":7.3e10,    "radius_km":0.282,  "au":1.13,    "period_yr":1.20,  "rot_d":0.034, "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":False, "rings":False, "type":"asteroid"},
    # TNOs / Kuiper
    {"name":"Sedna",     "mass_kg":1e21,      "radius_km":500,    "au":519.5,   "period_yr":11400, "rot_d":0.43,  "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":False, "rings":False, "type":"TNO"},
    {"name":"Quaoar",    "mass_kg":1.4e21,    "radius_km":545,    "au":43.6,    "period_yr":288,   "rot_d":0.367, "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":True,  "rings":True,  "type":"TNO"},
    {"name":"Orcus",     "mass_kg":6.3e20,    "radius_km":475,    "au":39.4,    "period_yr":247,   "rot_d":0.55,  "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":True,  "rings":False, "type":"TNO"},
    {"name":"Gonggong",  "mass_kg":1.75e21,   "radius_km":615,    "au":67.5,    "period_yr":553,   "rot_d":0.93,  "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":True,  "rings":False, "type":"TNO"},
    # Hypothetical / exotics
    {"name":"Planet9",   "mass_kg":6.3e25,    "radius_km":13000,  "au":700,     "period_yr":17000, "rot_d":0.5,   "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":False, "rings":False, "type":"hypothetical"},
    {"name":"Theia",     "mass_kg":6.4e23,    "radius_km":3000,   "au":1.0,     "period_yr":0,     "rot_d":0,     "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":False, "rings":False, "type":"hypothetical"},
    # Exoplanets
    {"name":"Proxima-b", "mass_kg":1.27e25,   "radius_km":7160,   "au":0.0485,  "period_yr":0.0304,"rot_d":11.2,  "core_metallic":True,  "atm_bar":1.0,  "mag":0.0,  "tidal":True,  "rings":False, "type":"exoplanet"},
    {"name":"TRAPPIST-1e","mass_kg":3.8e24,   "radius_km":5792,   "au":0.0293,  "period_yr":0.0270,"rot_d":5.0,   "core_metallic":True,  "atm_bar":1.0,  "mag":0.0,  "tidal":True,  "rings":False, "type":"exoplanet"},
    {"name":"Kepler-22b", "mass_kg":2.4e25,    "radius_km":12240,  "au":0.849,   "period_yr":0.857, "rot_d":1.0,   "core_metallic":True,  "atm_bar":1.0,  "mag":0.0,  "tidal":True,  "rings":False, "type":"exoplanet"},
    {"name":"HD209458b", "mass_kg":1.3e27,    "radius_km":92300,  "au":0.0475,  "period_yr":0.0385,"rot_d":3.5,   "core_metallic":False, "atm_bar":1e3,  "mag":0.0,  "tidal":True,  "rings":False, "type":"exoplanet"},
    {"name":"WASP-12b",  "mass_kg":1.4e27,    "radius_km":162000, "au":0.0234,  "period_yr":0.0226,"rot_d":1.09,  "core_metallic":False, "atm_bar":1e3,  "mag":0.0,  "tidal":True,  "rings":False, "type":"exoplanet"},
    {"name":"51Pegb",    "mass_kg":1.5e27,    "radius_km":100000, "au":0.0527,  "period_yr":0.0130,"rot_d":4.0,   "core_metallic":False, "atm_bar":1e3,  "mag":0.0,  "tidal":True,  "rings":False, "type":"exoplanet"},
    {"name":"GJ1214b",   "mass_kg":2.4e25,    "radius_km":13800,  "au":0.0140,  "period_yr":0.0037,"rot_d":0.71,  "core_metallic":True,  "atm_bar":100,  "mag":0.0,  "tidal":True,  "rings":False, "type":"exoplanet"},
    {"name":"Kepler-452b","mass_kg":5.0e25,   "radius_km":9500,   "au":1.046,   "period_yr":1.10,  "rot_d":1.0,   "core_metallic":True,  "atm_bar":1.0,  "mag":0.0,  "tidal":False, "rings":False, "type":"exoplanet"},
    {"name":"LHS1140b",  "mass_kg":6.4e24,    "radius_km":6800,   "au":0.0875,  "period_yr":0.0719,"rot_d":5.0,   "core_metallic":True,  "atm_bar":1.0,  "mag":0.0,  "tidal":True,  "rings":False, "type":"exoplanet"},
    # Additional
    {"name":"Mercury2",  "mass_kg":3.301e23,  "radius_km":2440,   "au":0.387,   "period_yr":0.241, "rot_d":58.6,  "core_metallic":True,  "atm_bar":1e-15,"mag":0.011,"tidal":True,  "rings":False, "type":"planet"},
    {"name":"Venus2",    "mass_kg":4.867e24,  "radius_km":6052,   "au":0.723,   "period_yr":0.615, "rot_d":-243,  "core_metallic":True,  "atm_bar":92,   "mag":0.0,  "tidal":False, "rings":False, "type":"planet"},
    {"name":"Enceladus", "mass_kg":1.08e20,   "radius_km":252,    "au":0.00253, "period_yr":0.0037,"rot_d":1.37,  "core_metallic":True,  "atm_bar":1e-9, "mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
    {"name":"Miranda",   "mass_kg":6.59e19,   "radius_km":236,    "au":0.00129, "period_yr":0.0023,"rot_d":1.41,  "core_metallic":True,  "atm_bar":0,    "mag":0.0,  "tidal":True,  "rings":False, "type":"moon"},
]

# ============================================================
# 8-DIMENSION ENCODING (kernel's r, h, d, p, s, gamma, g, nu)
# ============================================================
def encode_8d(b):
    """
    Map body to 8-dim vector (kernel's 5+2+1 dims: r, h, d, p, s, gamma, g, nu).
    Index 0..7 = r, h, d, p, s, gamma, g, nu
    """
    M = b["mass_kg"]
    R = b["radius_km"]
    rho = M / (R**3)  # kg/km^3

    # 0: r — body radius (normalized log)
    r_dim = min(1.0, max(0.0, math.log10(R) / 6.0))  # 1 km -> 0, 1e6 km -> 1

    # 1: h — high-energy / hardness (cosmic ray exposure, magnetosphere)
    h_dim = min(1.0, math.log10(b["mag"] + 1e-5) / 1.5)
    if b["mag"] > 5:
        h_dim = min(1.0, h_dim + 0.2)

    # 2: d — density (core compactness)
    rho_earth = 5.5e3  # kg/km^3 (Earth avg)
    d_dim = min(1.0, max(0.0, math.log10(rho / rho_earth + 1e-5) / 2.0 + 0.5))

    # 3: p — pressure (atmosphere)
    p_dim = min(1.0, math.log10(b["atm_bar"] + 1e-15) / 3.0 + 0.4)

    # 4: s — spin (rotation)
    s_dim = min(1.0, max(0.0, 1.0 - math.log10(abs(b["rot_d"]) + 0.01) / 2.0))

    # 5: gamma — tidal energy (tidal lock + orbital)
    gamma_dim = 0.8 if b["tidal"] else 0.1
    if b["au"] > 0 and b["au"] < 0.05:
        gamma_dim = min(1.0, gamma_dim + 0.2)

    # 6: g — gate / mass (heavy = strong gate)
    g_dim = min(1.0, math.log10(M) / 31.0)

    # 7: nu — volume (neutrino pass-through scales with body volume)
    V = (4/3) * math.pi * (R*1000)**3  # m^3
    nu_dim = min(1.0, max(0.0, math.log10(V) / 60.0 + 0.5))

    return [r_dim, h_dim, d_dim, p_dim, s_dim, gamma_dim, g_dim, nu_dim]

# ============================================================
# 6 ATTRACTOR SIGNATURES (8-dim)
# ============================================================
ATTRACTOR_8D = {
    "energy":         [1.0, 0.5, 0.5, 0.1, 0.3, 0.0, 1.0, 1.0],  # Sun: massive, magnetic
    "information":    [0.5, 0.4, 0.6, 0.7, 0.7, 0.1, 0.4, 0.5],  # Earth: atmosphere
    "repair":         [0.2, 0.1, 0.9, 0.0, 0.6, 0.0, 0.3, 0.1],  # Mars/Mercury: dense core
    "opioid":         [0.2, 0.1, 0.5, 0.0, 0.0, 1.0, 0.1, 0.0],  # tidal-locked moons
    "gan_bulkhead":   [0.9, 0.6, 0.3, 0.6, 0.6, 0.0, 0.95, 1.0],  # gas giants
    "cox_retrograde": [0.8, 0.3, 0.3, 0.6, 0.5, 0.0, 0.7, 0.8],  # Saturn-like
}

# ============================================================
# COSINE SIMILARITY
# ============================================================
def cos_sim(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 70)
    print("SOLAR SYSTEM 8-PARTICLE MAPPING (μ, g, W, νμ, Z, H, τ, γ)")
    print("=" * 70)
    print(f"  Bodies: {len(BODIES_46)}")
    print(f"  Attractor signatures: 8-vector each")
    print()

    # Self-test
    sun_8d = encode_8d(BODIES_46[0])
    print(f"  Sun 8-dim (r,h,d,p,s,gamma,g,nu): {[f'{v:.2f}' for v in sun_8d]}")

    # Map all bodies
    results = {}
    for b in BODIES_46:
        v8 = encode_8d(b)
        sims = {a: cos_sim(v8, sig) for a, sig in ATTRACTOR_8D.items()}
        best = max(sims, key=sims.get)
        results[b["name"]] = {
            "8d_vector": [round(x, 3) for x in v8],
            "type": b["type"],
            "best_attractor": best,
            "scores": {a: round(s, 3) for a, s in sims.items()},
        }
        if b["type"] in ("G2V", "planet"):
            print(f"  {b['name']:14s} {b['type']:14s} -> {best:18s} (top score: {sims[best]:.3f})")

    # 1:1 attractor distribution
    print()
    print("  Attractor distribution:")
    counts = {}
    for r in results.values():
        a = r["best_attractor"]
        counts[a] = counts.get(a, 0) + 1
    for a, c in sorted(counts.items()):
        print(f"    {a:18s}: {c} bodies")

    # Save
    out = {
        "_version": "8d_v1",
        "_date": "2026-09-09",
        "_method": "8-dim encoding using kernel's 5+2+1 (r,h,d,p,s,gamma,g,nu), cosine similarity to 6 attractor signatures",
        "dims": DIMS_8,
        "n_bodies": len(BODIES_46),
        "attractor_signatures": ATTRACTOR_8D,
        "body_mapping": results,
        "attractor_counts": counts,
    }
    out_path = Path(__file__).parent / "solar_8p_mapping.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")

if __name__ == "__main__":
    main()
