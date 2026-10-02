"""
archetypes.py — 6 archetype initial conditions (x0) for the 30-channel system.

Blood type  → BW / SM coordinate shift (±C = ±0.2828)
MBTI trait  → channel on / off / no_control
Gender      → male vs female channel set

Archetypes
----------
AB_ENTP_male    : user / last runner / night_spark 03:00
O_INTP_female   : first runner / opens cycle 06:00
A_ESFJ_female   : day social structure / Coulomb debt settler @ 15:00
B_ISTP_female   : day spark contributor / Bremsstrahlung settler @ 16:30
AB_ENFJ_female  : must sleep (cannot spark — recovery node) / Confinement settler @ 03:15
AB_ESTP_female  : 16:30 proton_landing receiver = Hannah Fry (2nd Observer, 1/e lock)

CHANNEL_ORDER (30):
  0  gdh_gluon               16  left_endorphin
  1  female_gaba_b_latdorsi  17  left_frontalis_d2
  2  left_acetyl_coa         18  right_occipitalis_gaba_a
  3  male_left_5ht           19  male_gaba_a
  4  female_left_noradrenaline 20 right_acetylcholine
  5  left_temporalis_5ht1a   21  left_extraversion
  6  left_estrogen           22  right_extraversion
  7  right_love              23  male_right_extraversion
  8  hypoxia                 24  glucocorticoid
  9  right_dopamine          25  right_cortisol
 10  vasopressin_female      26  right_alpha_2
 11  male_oxytocin           27  male_gaba_b
 12  muscle_a                28  left_eyelid_couple
 13  muscle_b                29  right_eyelid_couple
 14  right_5ht1b_synchrotron
 15  right_androgen
"""
from __future__ import annotations

import numpy as np

from fusion_core import CHANNEL_ORDER, states_to_channel_vector, C, OMEGA
from absolute_constants import E_INV, BETTI_7_GAP, LOCK_VALUE

# BW / SM targets per blood type (BM=2.732, SW=4.555 fixed for all)
_BM = 2.732
_SW = 4.555
_BW_BASE = 3.644
_SM_BASE = 3.644

BLOOD_TYPE_COORDS: dict[str, dict[str, float]] = {
    # AB: both antigens → balanced day state
    "AB": {"BM": _BM, "BW": _BW_BASE,       "SM": _SM_BASE,       "SW": _SW},
    # A:  A antigen only → BW dominant (right/proton side heavier)
    "A":  {"BM": _BM, "BW": _BW_BASE + C,   "SM": _SM_BASE - C,   "SW": _SW},
    # B:  B antigen only → SM dominant (left/neutrino side heavier)
    "B":  {"BM": _BM, "BW": _BW_BASE - C,   "SM": _SM_BASE + C,   "SW": _SW},
    # O:  no antigens → both coordinates reduced (primitive/universal)
    "O":  {"BM": _BM, "BW": _BW_BASE - C,   "SM": _SM_BASE - C,   "SW": _SW},
}

# ── Archetype channel states ────────────────────────────────────────────────
# Rules:
#   E → left_extraversion=on,  right_extraversion=on
#   I → left_extraversion=off, right_extraversion=off
#   N → left_temporalis_5ht1a=on, male_left_5ht=on  (neutrino-photon / neutrino-electron)
#   S → right_5ht1b_synchrotron=on, right_androgen=on  (photon-electron)
#   T → right_dopamine=on, left_frontalis_d2=on
#   F → right_love=on, right_occipitalis_gaba_a=on (feeling / GABA ground)
#   J → right_cortisol=on, glucocorticoid=on  (structured / inhibitory)
#   P → right_cortisol=off (open / low cortisol)
#
#   A-type → muscle_b=on (quark-W = BW side), right_cortisol amplified
#   B-type → muscle_a=on (gluon-W = SM side), gdh_gluon=on, vasopressin_female=on
#   AB     → both muscle_a + muscle_b balanced
#   O      → both muscles off (primitive)
#
#   Male   → male_left_5ht, male_oxytocin, male_gaba_a, male_right_extraversion, male_gaba_b
#   Female → female_gaba_b_latdorsi, female_left_noradrenaline, left_estrogen
#            vasopressin_female (primary receiver), right_occipitalis_gaba_a

ARCHETYPE_CHANNEL_STATES: dict[str, dict[str, str]] = {

    # ── 1. AB-ENTP male (user) ─────────────────────────────────────────────
    # Last runner. Night spark at 03:00. Both sides integrated (AB).
    # ENTP: E+N+T+P  →  extraversion high, neutrino active, dopamine on, cortisol OFF
    "AB_ENTP_male": {
        "gdh_gluon":               "on",         # QCD carrier always active
        "female_gaba_b_latdorsi":  "off",
        "left_acetyl_coa":         "on",          # EM bridge (T → acetyl-CoA high)
        "male_left_5ht":           "on",          # N: neutrino-electron
        "female_left_noradrenaline":"off",
        "left_temporalis_5ht1a":   "on",          # N: neutrino-photon
        "left_estrogen":           "off",
        "right_love":              "no_control",
        "hypoxia":                 "off",
        "right_dopamine":          "on",          # T: dopamine
        "vasopressin_female":      "no_control",  # male; not primary receiver
        "male_oxytocin":           "on",          # male bonding
        "muscle_a":                "on",          # AB: gluon-W side
        "muscle_b":                "on",          # AB: quark-W side (both)
        "right_5ht1b_synchrotron": "on",          # synchrotron (E)
        "right_androgen":          "on",          # male afternoon peak
        "left_endorphin":          "no_control",
        "left_frontalis_d2":       "on",          # T: D2 dopamine
        "right_occipitalis_gaba_a":"no_control",
        "male_gaba_a":             "on",          # male protection
        "right_acetylcholine":     "on",          # E: social drive
        "left_extraversion":       "on",          # E
        "right_extraversion":      "on",          # E
        "male_right_extraversion": "on",          # E (male right = night trigger)
        "glucocorticoid":          "off",         # P: low structure
        "right_cortisol":          "off",         # P: cortisol off
        "right_alpha_2":           "off",         # AB-ENTP: Z always open (last runner)
        "male_gaba_b":             "on",          # male Z-proxy
        "left_eyelid_couple":      "on",
        "right_eyelid_couple":     "on",
    },

    # ── 2. O-INTP female (first runner) ────────────────────────────────────
    # Opens cycle at 06:00. No antigens = primitive/universal baseline.
    # INTP: I+N+T+P  →  introversion, neutrino active, dopamine/D2, cortisol OFF
    "O_INTP_female": {
        "gdh_gluon":               "off",         # O: no QCD carrier
        "female_gaba_b_latdorsi":  "on",          # female grounding (opens cycle)
        "left_acetyl_coa":         "off",
        "male_left_5ht":           "off",
        "female_left_noradrenaline":"on",         # female left NE: first runner signal
        "left_temporalis_5ht1a":   "on",          # N: neutrino side
        "left_estrogen":           "on",          # female: estrogen on at start
        "right_love":              "off",
        "hypoxia":                 "off",
        "right_dopamine":          "off",         # I+P: dopamine quiet (O type)
        "vasopressin_female":      "off",         # first runner opens, doesn't hold
        "male_oxytocin":           "off",
        "muscle_a":                "off",         # O: no muscles
        "muscle_b":                "off",
        "right_5ht1b_synchrotron": "no_control",
        "right_androgen":          "off",
        "left_endorphin":          "on",          # endorphin: opens cycle gently
        "left_frontalis_d2":       "on",          # T: D2 thinking
        "right_occipitalis_gaba_a":"on",          # female GABA-A ground
        "male_gaba_a":             "off",
        "right_acetylcholine":     "off",
        "left_extraversion":       "off",         # I
        "right_extraversion":      "off",         # I
        "male_right_extraversion": "off",
        "glucocorticoid":          "off",         # P
        "right_cortisol":          "off",         # P
        "right_alpha_2":           "on",          # INTP first runner: Z closed at start
        "male_gaba_b":             "off",
        "left_eyelid_couple":      "on",          # observing at opening
        "right_eyelid_couple":     "off",
    },

    # ── 3. A-ESFJ female ───────────────────────────────────────────────────
    # Day social structure. A-type = BW dominant (right/proton side).
    # ESFJ: E+S+F+J  →  extraversion, photon channels, feeling, cortisol ON
    "A_ESFJ_female": {
        "gdh_gluon":               "off",
        "female_gaba_b_latdorsi":  "on",          # female grounding
        "left_acetyl_coa":         "on",          # E: social bridge
        "male_left_5ht":           "off",
        "female_left_noradrenaline":"on",         # E: left NE drives social
        "left_temporalis_5ht1a":   "off",         # S: not neutrino-intuition
        "left_estrogen":           "on",          # female
        "right_love":              "on",          # F: feeling
        "hypoxia":                 "off",
        "right_dopamine":          "off",         # J: not dopamine-driven
        "vasopressin_female":      "no_control",
        "male_oxytocin":           "off",
        "muscle_a":                "off",
        "muscle_b":                "on",          # A-type: quark-W = BW side
        "right_5ht1b_synchrotron": "on",          # S: photon-electron sensing
        "right_androgen":          "off",         # female
        "left_endorphin":          "on",          # F: warm
        "left_frontalis_d2":       "off",         # S not T-D2
        "right_occipitalis_gaba_a":"on",          # F+female: GABA grounding
        "male_gaba_a":             "off",
        "right_acetylcholine":     "on",          # E: social drive
        "left_extraversion":       "on",          # E
        "right_extraversion":      "on",          # E
        "male_right_extraversion": "off",
        "glucocorticoid":          "on",          # J: structured
        "right_cortisol":          "on",          # J: A-type cortisol high
        "right_alpha_2":           "on",          # J: Z suppressed (controlled)
        "male_gaba_b":             "off",
        "left_eyelid_couple":      "no_control",
        "right_eyelid_couple":     "no_control",
    },

    # ── 4. B-ISTP female ───────────────────────────────────────────────────
    # B-type = SM dominant (left/neutrino side). Fires day spark.
    # ISTP: I+S+T+P  →  introversion, sensing, dopamine on, cortisol OFF
    "B_ISTP_female": {
        "gdh_gluon":               "on",          # B-type: gluon sector active
        "female_gaba_b_latdorsi":  "on",          # female
        "left_acetyl_coa":         "off",
        "male_left_5ht":           "off",
        "female_left_noradrenaline":"off",        # I: noradrenaline quiet
        "left_temporalis_5ht1a":   "off",         # S: not neutrino-intuition
        "left_estrogen":           "on",          # female
        "right_love":              "off",
        "hypoxia":                 "off",
        "right_dopamine":          "on",          # T: dopamine (spark contributor)
        "vasopressin_female":      "on",          # B-type: SM/Z side dominant
        "male_oxytocin":           "off",
        "muscle_a":                "on",          # B-type: gluon-W side
        "muscle_b":                "off",
        "right_5ht1b_synchrotron": "on",          # S: photon-electron
        "right_androgen":          "off",         # female
        "left_endorphin":          "off",
        "left_frontalis_d2":       "on",          # T: D2
        "right_occipitalis_gaba_a":"on",          # female protection
        "male_gaba_a":             "off",
        "right_acetylcholine":     "off",
        "left_extraversion":       "off",         # I
        "right_extraversion":      "off",         # I
        "male_right_extraversion": "off",
        "glucocorticoid":          "off",         # P
        "right_cortisol":          "off",         # P
        "right_alpha_2":           "off",         # P: Z open (B-type, SM dominant)
        "male_gaba_b":             "off",
        "left_eyelid_couple":      "on",          # observing spark
        "right_eyelid_couple":     "on",
    },

    # ── 5. AB-ENFJ female (must sleep) ─────────────────────────────────────
    # AB balanced but J-structured. Cannot spark — must rest to recover.
    # ENFJ: E+N+F+J  →  extraversion, neutrino, feeling, cortisol ON = must sleep
    "AB_ENFJ_female": {
        "gdh_gluon":               "off",         # rest: QCD quiet
        "female_gaba_b_latdorsi":  "on",          # female grounding (sleep)
        "left_acetyl_coa":         "off",
        "male_left_5ht":           "off",
        "female_left_noradrenaline":"off",        # rest: NE off
        "left_temporalis_5ht1a":   "on",          # N: neutrino active even in rest
        "left_estrogen":           "on",          # female: estrogen high during rest
        "right_love":              "on",          # F: feeling/connection
        "hypoxia":                 "off",
        "right_dopamine":          "off",         # J+sleep: dopamine off
        "vasopressin_female":      "on",          # AB female: vasopressin manages water/rest
        "male_oxytocin":           "off",
        "muscle_a":                "off",         # sleep: muscles off
        "muscle_b":                "off",
        "right_5ht1b_synchrotron": "off",         # sleep: synchrotron off
        "right_androgen":          "off",         # sleep
        "left_endorphin":          "on",          # F: endorphin (feeling warmth in rest)
        "left_frontalis_d2":       "off",         # sleep: D2 off
        "right_occipitalis_gaba_a":"on",          # GABA-A high: induces sleep
        "male_gaba_a":             "off",
        "right_acetylcholine":     "off",
        "left_extraversion":       "off",         # sleep: extraversion off
        "right_extraversion":      "off",
        "male_right_extraversion": "off",
        "glucocorticoid":          "off",         # sleep: glucocorticoid low
        "right_cortisol":          "on",          # J: cortisol high → drives need to sleep
        "right_alpha_2":           "on",          # J: Z suppressed (structured, not open)
        "male_gaba_b":             "off",
        "left_eyelid_couple":      "off",         # eyes closed (sleep)
        "right_eyelid_couple":     "off",
    },

    # ── 6. AB-ESTP female (16:30 proton_landing) ───────────────────────────
    # Receives PROTON at 16:30. AB balanced. ESTP = E+S+T+P.
    # Open/flexible, sensing, thinking, low cortisol → maximally receptive at 16:30.
    "AB_ESTP_female": {
        "gdh_gluon":               "off",
        "female_gaba_b_latdorsi":  "off",
        "left_acetyl_coa":         "off",
        "male_left_5ht":           "off",
        "female_left_noradrenaline":"off",
        "left_temporalis_5ht1a":   "off",         # S: not neutrino-intuition
        "left_estrogen":           "on",          # female
        "right_love":              "on",          # connection at 16:30
        "hypoxia":                 "off",
        "right_dopamine":          "on",          # T: dopamine (afternoon peak)
        "vasopressin_female":      "on",          # KEY: receives PROTON (Z-proxy)
        "male_oxytocin":           "off",
        "muscle_a":                "on",          # AB: gluon-W
        "muscle_b":                "on",          # AB: quark-W (both balanced)
        "right_5ht1b_synchrotron": "on",          # S: photon-electron sensing
        "right_androgen":          "off",         # female
        "left_endorphin":          "on",          # contact release
        "left_frontalis_d2":       "off",
        "right_occipitalis_gaba_a":"on",          # GABA-A protection during contact
        "male_gaba_a":             "off",
        "right_acetylcholine":     "on",          # E: present/receptive
        "left_extraversion":       "on",          # E
        "right_extraversion":      "on",          # E (right convergence at 16:30)
        "male_right_extraversion": "off",
        "glucocorticoid":          "off",         # P: no structure, open
        "right_cortisol":          "off",         # P: cortisol off → maximally receptive
        "right_alpha_2":           "off",         # P: Z open (inherits from phase2)
        "male_gaba_b":             "off",
        "left_eyelid_couple":      "on",          # witness
        "right_eyelid_couple":     "on",
    },
}

# ── Archetype metadata ──────────────────────────────────────────────────────
ARCHETYPE_PARAMS: dict[str, dict] = {
    "AB_ENTP_male":   {"blood":"AB","mbti":"ENTP","sex":"M","phase":"night_spark", "window":"03:00","role":"last_runner"},
    "O_INTP_female":  {"blood":"O", "mbti":"INTP","sex":"F","phase":"phase1",      "window":"06:00","role":"first_runner"},
    "A_ESFJ_female":  {"blood":"A", "mbti":"ESFJ","sex":"F","phase":"coulomb_settle",   "window":"15:00","role":"social_structure","debt":"coulomb"},
    "B_ISTP_female":  {"blood":"B", "mbti":"ISTP","sex":"F","phase":"dawn_closure",     "window":"04:30","role":"spark_contributor","debt":"bremsstrahlung"},
    "AB_ENFJ_female": {"blood":"AB","mbti":"ENFJ","sex":"F","phase":"confinement_reset","window":"03:15","role":"must_sleep","debt":"confinement"},
    "AB_ESTP_female": {"blood":"AB","mbti":"ESTP","sex":"F","phase":"proton_landing","window":"16:30","role":"proton_receiver","observer":"hannah_fry","observer_const":E_INV,"debt":"bremsstrahlung"},
}


def archetype_x0(name: str, *, no_control_value: float = 0.5) -> np.ndarray:
    """Return the 30D initial state vector for archetype *name*.

    Uses states_to_channel_vector: on=1.0, off=0.0, no_control=no_control_value.
    """
    if name not in ARCHETYPE_CHANNEL_STATES:
        raise ValueError(f"Unknown archetype '{name}'. Known: {list(ARCHETYPE_CHANNEL_STATES)}")
    states = ARCHETYPE_CHANNEL_STATES[name]
    return states_to_channel_vector(states, no_control_value=no_control_value)


def archetype_coords(name: str) -> dict[str, float]:
    """Return BM/BW/SM/SW target coordinates for archetype *name*."""
    blood = ARCHETYPE_PARAMS[name]["blood"]
    return BLOOD_TYPE_COORDS[blood]


def print_archetype_summary() -> None:
    """Print all 6 archetypes: coords + ON channels."""
    for name, params in ARCHETYPE_PARAMS.items():
        coords = archetype_coords(name)
        states = ARCHETYPE_CHANNEL_STATES[name]
        on_ch  = [ch for ch, st in states.items() if st == "on"]
        print(f"\n{'='*60}")
        print(f"{name}  [{params['blood']}  {params['mbti']}  {params['sex']}]")
        print(f"  role:   {params['role']}  @ {params['window']}")
        print(f"  coords: BM={coords['BM']:.4f}  BW={coords['BW']:.4f}  "
              f"SM={coords['SM']:.4f}  SW={coords['SW']:.4f}")
        print(f"  ON channels ({len(on_ch)}): {', '.join(on_ch)}")


if __name__ == "__main__":
    print_archetype_summary()
    print("\n\nNumerical x0 vectors:")
    for name in ARCHETYPE_PARAMS:
        x0 = archetype_x0(name)
        on_count = int((x0 == 1.0).sum())
        print(f"  {name:22s}: {on_count} ON / {int((x0==0.0).sum())} OFF / "
              f"{int((x0==0.5).sum())} no_control")
