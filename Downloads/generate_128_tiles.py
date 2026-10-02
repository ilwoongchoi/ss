#!/usr/bin/env python3
"""
generate_128_tiles.py — 128 profiles × 5 tiles × 8D params + arpeggiator config
Output: 128_tiles_arpeggiator.csv

5 tiles per profile:
  1. RELEASE       — Layer A (base blood type, aa rh+)
  2. STRESS_GROWTH — Layer B (heterozygous ao rh+, blood+1 shift)
  3. EXTREME_GROWTH— Layer C (aa rh-, base blood type)
  4. PRESENT_MOMENT— Layer D (ao rh-, blood+1 shift)
  5. OBSERVER_3AM  — 3AM hysteresis random + jitter

Arpeggiator config derived from 8D:
  r    → tempo (BPM)
  h    → chord complexity (intervals)
  d    → scale darkness (root + scale type)
  p    → pattern predictability (step pattern)
  s    → brightness/filter cutoff
  gamma→ reverb/space
  g    → time signature / grouping
  nu   → loop recursion depth
"""

import csv
import math
import os
import sys

# Import from particle_to_8d
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from particle_to_8d import (
    DIM_ORDER, MBTI_TYPES, BLOOD_TYPES, GENDERS,
    particles_to_dims, compute_4layers, clamp,
    apply_16window_shift, mulberry32, hash_code,
    TOROIDAL_SLOTS, get_toroidal_slot,
)

# ============================================================
# ARPEGGIATOR CONFIGURATION FROM 8D
# ============================================================

def dims_to_arpeggiator(dims, layer_name, profile_label, tile_idx):
    """Convert 8D params to arpeggiator configuration."""
    r = dims.get("r", 0.5)
    h = dims.get("h", 0.5)
    d = dims.get("d", 0.5)
    p = dims.get("p", 0.5)
    s = dims.get("s", 0.5)
    gamma = dims.get("gamma", 0.5)
    g = dims.get("g", 0.5)
    nu = dims.get("nu", 0.5)

    # r → tempo: 60-180 BPM
    bpm = int(60 + r * 120)

    # h → chord complexity
    if h < 0.3:
        chord = "power_chord"
        intervals = [0, 7]
    elif h < 0.5:
        chord = "triad"
        intervals = [0, 4, 7]
    elif h < 0.7:
        chord = "seventh"
        intervals = [0, 4, 7, 11]
    elif h < 0.85:
        chord = "extended"
        intervals = [0, 4, 7, 11, 14]
    else:
        chord = "microtonal_cluster"
        intervals = [0, 1, 4, 7, 8, 11]

    # d → scale darkness
    if d < 0.2:
        scale = "major"
        scale_notes = [0, 2, 4, 5, 7, 9, 11]
    elif d < 0.4:
        scale = "mixolydian"
        scale_notes = [0, 2, 4, 5, 7, 9, 10]
    elif d < 0.6:
        scale = "minor"
        scale_notes = [0, 2, 3, 5, 7, 8, 10]
    elif d < 0.8:
        scale = "phrygian"
        scale_notes = [0, 1, 3, 5, 7, 8, 10]
    else:
        scale = "atonal"
        scale_notes = [0, 1, 3, 4, 6, 7, 9, 11]

    # p → pattern predictability
    if p < 0.3:
        pattern = "random_walk"
        steps = [0, 3, 1, 5, 2, 6, 4, 7]
    elif p < 0.5:
        pattern = "wandering"
        steps = [0, 2, 4, 3, 5, 7, 6, 4]
    elif p < 0.7:
        pattern = "up_down"
        steps = [0, 2, 4, 7, 4, 2, 0, 2]
    else:
        pattern = "straight_up"
        steps = [0, 2, 4, 7, 9, 11, 12, 14]

    # s → brightness / filter cutoff
    cutoff_hz = int(200 + s * 7800)  # 200Hz - 8000Hz

    # gamma → reverb / space
    reverb_ms = int(10 + gamma * 990)  # 10ms - 1000ms
    if gamma < 0.3:
        space = "dry"
    elif gamma < 0.6:
        space = "room"
    elif gamma < 0.8:
        space = "hall"
    else:
        space = "cathedral"

    # g → time signature / grouping
    if g < 0.25:
        time_sig = "4/4"
        grouping = 4
    elif g < 0.5:
        time_sig = "3/4"
        grouping = 3
    elif g < 0.75:
        time_sig = "7/8"
        grouping = 7
    else:
        time_sig = "5/4"
        grouping = 5

    # nu → loop recursion depth
    if nu < 0.3:
        loop_depth = 1
        loop_mode = "single_pass"
    elif nu < 0.5:
        loop_depth = 2
        loop_mode = "short_loop"
    elif nu < 0.7:
        loop_depth = 4
        loop_mode = "nested_loop"
    elif nu < 0.9:
        loop_depth = 8
        loop_mode = "fractal_recursive"
    else:
        loop_depth = 16
        loop_mode = "deep_recursive"

    return {
        "bpm": bpm,
        "chord_type": chord,
        "intervals": "-".join(str(i) for i in intervals),
        "scale": scale,
        "scale_notes": "-".join(str(n) for n in scale_notes),
        "pattern": pattern,
        "steps": "-".join(str(s) for s in steps),
        "filter_cutoff_hz": cutoff_hz,
        "reverb_ms": reverb_ms,
        "space": space,
        "time_signature": time_sig,
        "grouping": grouping,
        "loop_depth": loop_depth,
        "loop_mode": loop_mode,
    }


# ============================================================
# 5 TILES PER PROFILE
# ============================================================

TILE_NAMES = ["RELEASE", "STRESS_GROWTH", "EXTREME_GROWTH", "PRESENT_MOMENT", "OBSERVER_3AM"]

def compute_5_tiles(profile_label, time_phase="day"):
    """Compute 5 tiles for a profile."""
    parts = profile_label.split("_")
    mbti, gender, blood = parts[0], parts[1], parts[2]

    # Base 8D from particles_to_dims
    base_result = particles_to_dims(profile_label, time_phase)
    base_dims = base_result["dims"]

    # Blood type shift for stress/extreme
    blood_shift = {"O": "A", "A": "B", "B": "AB", "AB": "O"}
    shifted_blood = blood_shift.get(blood, blood)
    shifted_label = f"{mbti}_{gender}_{shifted_blood}"

    tiles = []

    # Tile 1: RELEASE — base blood type, Layer A
    seed_val = abs(hash_code(profile_label)) % 100000
    release_dims = apply_16window_shift(dict(base_dims), 0, 0.20, seed_val)
    tiles.append({
        "tile": "RELEASE",
        "layer": "A",
        "genotype": "aa_rh+",
        "blood": blood,
        "dims": release_dims,
        "arpeggiator": dims_to_arpeggiator(release_dims, "body", profile_label, 0),
    })

    # Tile 2: STRESS_GROWTH — shifted blood type, Layer B
    stress_result = particles_to_dims(shifted_label, time_phase)
    stress_dims = stress_result["dims"]
    stress_dims = apply_16window_shift(dict(stress_dims), 4, 0.25, seed_val + 1)
    tiles.append({
        "tile": "STRESS_GROWTH",
        "layer": "B",
        "genotype": "ao_rh+",
        "blood": shifted_blood,
        "dims": stress_dims,
        "arpeggiator": dims_to_arpeggiator(stress_dims, "observer", shifted_label, 1),
    })

    # Tile 3: EXTREME_GROWTH — base blood type, Layer C (rh-)
    extreme_dims = apply_16window_shift(dict(base_dims), 8, 0.30, seed_val + 2)
    # Extreme growth: amplify d and nu
    extreme_dims["d"] = clamp(extreme_dims["d"] + 0.15)
    extreme_dims["nu"] = clamp(extreme_dims["nu"] + 0.10)
    tiles.append({
        "tile": "EXTREME_GROWTH",
        "layer": "C",
        "genotype": "aa_rh-",
        "blood": blood,
        "dims": extreme_dims,
        "arpeggiator": dims_to_arpeggiator(extreme_dims, "bridge", profile_label, 2),
    })

    # Tile 4: PRESENT_MOMENT — shifted blood, Layer D (rh-)
    present_dims = apply_16window_shift(dict(stress_dims), 12, 0.20, seed_val + 3)
    tiles.append({
        "tile": "PRESENT_MOMENT",
        "layer": "D",
        "genotype": "ao_rh-",
        "blood": shifted_blood,
        "dims": present_dims,
        "arpeggiator": dims_to_arpeggiator(present_dims, "dark", shifted_label, 3),
    })

    # Tile 5: OBSERVER_3AM — 3AM hysteresis random + max jitter
    rng = mulberry32(seed_val + 999)
    observer_dims = {}
    for dim_name in DIM_ORDER:
        base_val = base_dims[dim_name]
        jitter = 1.0 + (rng() * 2 - 1) * 0.30  # ±30% jitter
        observer_dims[dim_name] = clamp(base_val * jitter)
    # 3AM: nu spikes, s drops
    observer_dims["nu"] = clamp(observer_dims["nu"] + 0.20)
    observer_dims["s"] = clamp(observer_dims["s"] - 0.15)
    tiles.append({
        "tile": "OBSERVER_3AM",
        "layer": "3AM",
        "genotype": "hysteresis_random",
        "blood": blood,
        "dims": observer_dims,
        "arpeggiator": dims_to_arpeggiator(observer_dims, "3am", profile_label, 4),
    })

    return tiles


# ============================================================
# MAIN — Generate CSV
# ============================================================

def main():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "128_tiles_arpeggiator.csv")

    # Build all 128 profiles
    all_profiles = []
    for mbti in MBTI_TYPES:
        for gender in GENDERS:
            for blood in BLOOD_TYPES:
                all_profiles.append(f"{mbti}_{gender}_{blood}")

    # CSV header
    fieldnames = [
        "profile_id", "tile", "layer", "genotype", "blood",
        "r", "h", "d", "p", "s", "gamma", "g", "nu",
        "bpm", "chord_type", "intervals", "scale", "scale_notes",
        "pattern", "steps", "filter_cutoff_hz", "reverb_ms", "space",
        "time_signature", "grouping", "loop_depth", "loop_mode",
    ]

    rows = []
    for profile in all_profiles:
        tiles = compute_5_tiles(profile, time_phase="day")
        for tile in tiles:
            d = tile["dims"]
            arp = tile["arpeggiator"]
            row = {
                "profile_id": profile,
                "tile": tile["tile"],
                "layer": tile["layer"],
                "genotype": tile["genotype"],
                "blood": tile["blood"],
                "r": round(d["r"], 4),
                "h": round(d["h"], 4),
                "d": round(d["d"], 4),
                "p": round(d["p"], 4),
                "s": round(d["s"], 4),
                "gamma": round(d["gamma"], 4),
                "g": round(d["g"], 4),
                "nu": round(d["nu"], 4),
                "bpm": arp["bpm"],
                "chord_type": arp["chord_type"],
                "intervals": arp["intervals"],
                "scale": arp["scale"],
                "scale_notes": arp["scale_notes"],
                "pattern": arp["pattern"],
                "steps": arp["steps"],
                "filter_cutoff_hz": arp["filter_cutoff_hz"],
                "reverb_ms": arp["reverb_ms"],
                "space": arp["space"],
                "time_signature": arp["time_signature"],
                "grouping": arp["grouping"],
                "loop_depth": arp["loop_depth"],
                "loop_mode": arp["loop_mode"],
            }
            rows.append(row)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows ({len(all_profiles)} profiles × 5 tiles)")
    print(f"Output: {output_path}")

    # Print sample
    print(f"\n=== SAMPLE: ENTP_M_O ===")
    entp_tiles = compute_5_tiles("ENTP_M_O", "day")
    for t in entp_tiles:
        d = t["dims"]
        a = t["arpeggiator"]
        print(f"\n  Tile: {t['tile']} (Layer {t['layer']}, {t['genotype']}, blood={t['blood']})")
        print(f"    8D: r={d['r']:.3f} h={d['h']:.3f} d={d['d']:.3f} p={d['p']:.3f} s={d['s']:.3f} γ={d['gamma']:.3f} g={d['g']:.3f} ν={d['nu']:.3f}")
        print(f"    ARP: {a['bpm']}BPM {a['chord_type']} {a['scale']} {a['pattern']} cutoff={a['filter_cutoff_hz']}Hz reverb={a['reverb_ms']}ms {a['space']} {a['time_signature']} loop={a['loop_mode']}({a['loop_depth']})")


if __name__ == "__main__":
    main()
