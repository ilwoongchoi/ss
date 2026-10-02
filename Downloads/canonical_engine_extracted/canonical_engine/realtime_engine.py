"""Real-time music parameter engine.

Given user profile (MBTI, blood, gender, RH layer) + current time,
return complete music parameters for that moment.

Usage:
    from canonical_engine.realtime_engine import RealtimeEngine
    engine = RealtimeEngine()
    params = engine.get_now("ENTP", "AB", "M", "A")  # RH layer A/B/C/D
    # or with specific time:
    params = engine.get_at("ENTP", "AB", "M", "A", "14:30")
"""
from __future__ import annotations

import json
import pathlib
from typing import Any

from .slot_query import query_slot, query_all

GEN_DIR = pathlib.Path(__file__).parent / "generated"

# Load all 128 slots
_ALL_SLOTS = query_all()

# Build profile → slots index
_PROFILE_SLOTS: dict[str, list[dict]] = {}
for s in _ALL_SLOTS:
    pk = s["profile_key"]
    _PROFILE_SLOTS.setdefault(pk, []).append(s)

# MBTI opposite mapping for layer B
_MBTI_OPP = {
    "E": "I", "I": "E",
    "N": "S", "S": "N",
    "T": "F", "F": "T",
    "J": "P", "P": "J",
}

# Blood+1 mapping for layer C
_BLOOD_NEXT = {"O": "A", "A": "B", "B": "AB", "AB": "O"}


def _mbti_opposite(mbti: str) -> str:
    return "".join(_MBTI_OPP[c] for c in mbti)


def _profile_for_layer(mbti: str, blood: str, gender: str, layer: str) -> str:
    if layer == "A":
        return f"{mbti}_{gender}_{blood}"
    elif layer == "B":
        return f"{_mbti_opposite(mbti)}_{gender}_{blood}"
    elif layer == "C":
        return f"{mbti}_{gender}_{_BLOOD_NEXT[blood]}"
    elif layer == "D":
        return f"{_mbti_opposite(mbti)}_{gender}_{_BLOOD_NEXT[blood]}"
    raise ValueError(f"Unknown layer {layer}")


def _time_to_minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _find_slot_by_time(time_str: str) -> int | None:
    target = _time_to_minutes(time_str)
    for s in _ALL_SLOTS:
        start = _time_to_minutes(s["time_start"])
        end = _time_to_minutes(s["time_end"])
        # handle midnight wrap (e.g., 21:00-03:00)
        if start <= end:
            if start <= target < end:
                return s["slot"]
        else:
            if target >= start or target < end:
                return s["slot"]
    return None


class RealtimeEngine:
    """Real-time music parameter engine.

    Slot assignment is fixed by the 128-grid timeline (circadian).
    Each slot has a main_type (the profile that 'owns' that time window).
    The user's RH layer (A/B/C/D) determines which energy layer to read.
    """

    def get_at(self, mbti: str, blood: str, gender: str,
               rh_layer: str, time_str: str) -> dict[str, Any]:
        """Get music parameters at a specific time.

        Args:
            mbti: e.g. "ENTP"
            blood: "O", "A", "B", "AB"
            gender: "M" or "F"
            rh_layer: "A", "B", "C", "D"
            time_str: "HH:MM" format

        Returns: complete parameter dict
        """
        slot = _find_slot_by_time(time_str)
        if slot is None:
            return {"error": f"No slot found for time {time_str}"}

        slot_data = query_slot(slot)

        # The user's profile for this RH layer
        user_profile = _profile_for_layer(mbti, blood, gender, rh_layer)

        # Get the 512 layer data for this element
        layer_data = slot_data["layers_512"].get(rh_layer, {})

        # Get the 128 phase data matching this layer's category
        category = layer_data.get("category", "release")
        phase_map = {"release": 0, "stress_growth": 1, "extreme_growth": 2}
        phase_idx = phase_map.get(category, 0)
        phase_data = slot_data["phases_128"][phase_idx]

        # 3AM entropy zone: slots 1-16, layer D only
        is_3am = (slot <= 16 and rh_layer == "D")

        # Circuit node info
        cnode = slot_data["circuit_node_info"]

        result = {
            "time": time_str,
            "slot": slot,
            "slot_time": f"{slot_data['time_start']}-{slot_data['time_end']}",
            "energy_phase": slot_data["energy_phase"],

            # User identity
            "user_profile": user_profile,
            "rh_layer": rh_layer,
            "rh_type": layer_data.get("rh", ""),
            "layer_label": layer_data.get("label", ""),
            "layer_category": category,

            # Circuit
            "circuit_entity": slot_data["circuit_entity"],
            "circuit_node": slot_data["circuit_node"],
            "element": slot_data["element"],
            "particle": cnode.get("particle", ""),
            "color": cnode.get("color", ""),
            "group": cnode.get("group", ""),
            "music_dims": cnode.get("music_dims", []),

            # Body
            "body_location": slot_data["body_location"],
            "canonical_loop_index": slot_data["canonical_loop_index"],

            # Neurochemistry
            "receptor": slot_data["receptor"],
            "neurochem": slot_data["neurochem"],
            "spark_condition": slot_data["spark_condition"],
            "potential": slot_data["potential"],
            "z_index": slot_data["z_index"],

            # Music: 8D vector (from 128 phase)
            "vec8d": phase_data["vec8d"],

            # Music: 5D tension (from 512 layer)
            "tension_5d": layer_data.get("tension_5d", {}),

            # Music: genre + key + tempo
            "genre": layer_data.get("genre", phase_data["genre"]),
            "genre_128_phase": phase_data["genre"],
            "key": layer_data.get("key", ""),
            "tempo_bpm": layer_data.get("tempo_bpm", ""),
            "time_sig": layer_data.get("time_sig", ""),

            # 3AM flag
            "is_3am_entropy_zone": is_3am,
        }

        if is_3am:
            result["3am_note"] = (
                "Layer D extreme in 3AM entropy zone (slots 1-16): "
                "p=random, s=0.5+rand*0.5, nu=0.9+rand*0.1"
            )

        return result

    def get_now(self, mbti: str, blood: str, gender: str,
                rh_layer: str) -> dict[str, Any]:
        """Get music parameters for current time."""
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        return self.get_at(mbti, blood, gender, rh_layer, now)

    def get_full_day(self, mbti: str, blood: str, gender: str,
                     rh_layer: str) -> list[dict[str, Any]]:
        """Get all 128 slots for a user profile + RH layer."""
        results = []
        for s in _ALL_SLOTS:
            t = s["time_start"]
            r = self.get_at(mbti, blood, gender, rh_layer, t)
            results.append(r)
        return results


if __name__ == "__main__":
    import sys

    engine = RealtimeEngine()

    if len(sys.argv) >= 5:
        mbti, blood, gender, rh = sys.argv[1:5]
        time_str = sys.argv[5] if len(sys.argv) > 5 else None
        if time_str:
            result = engine.get_at(mbti, blood, gender, rh, time_str)
        else:
            result = engine.get_now(mbti, blood, gender, rh)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Demo: ENTP AB M layer A at various times
        print("=== ENTP AB M Layer A (RH+ homozygous) ===\n")
        for t in ["00:05", "06:30", "12:00", "18:30", "22:00"]:
            r = engine.get_at("ENTP", "AB", "M", "A", t)
            v = r.get("vec8d", {})
            t5 = r.get("tension_5d", {})
            print(f"{t} | slot {r['slot']:>3} | {r['energy_phase']:<16} | "
                  f"{r['circuit_entity']:<28} | {r['body_location'][:35]:<35} | "
                  f"genre={r['genre']:<25} | "
                  f"P={v.get('P',0):.2f} Z={v.get('Z',0):.2f} Q={v.get('Q',0):.2f} "
                  f"W={v.get('W',0):.2f} H={v.get('H',0):.2f} "
                  f"γ={v.get('Gamma',0):.2f} g={v.get('G',0):.2f} ν={v.get('Nu',0):.2f} | "
                  f"r={t5.get('Rhythm_Density',0):.2f} h={t5.get('Harmonic_Tension',0):.2f} "
                  f"d={t5.get('Dynamic_Curve',0):.2f} p={t5.get('Predictability_Inv',0):.2f} "
                  f"s={t5.get('Spectral_Brightness',0):.2f}")

        # Full day for one profile
        print("\n=== Full day: ENTP AB M Layer A ===\n")
        full = engine.get_full_day("ENTP", "AB", "M", "A")
        out = GEN_DIR / "realtime_demo_full_day.json"
        out.write_text(json.dumps(full, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {len(full)} slots -> {out}")
