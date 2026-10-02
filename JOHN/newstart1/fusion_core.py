"""
fusion_core.py - K8 graph engine.
Provides: apply_channels, laplacian, project4,
          day_target, night_target, init_state8_from_target4,
          CHANNEL_MAP, SUBJECTS, EDGES, OMEGA, C, C2, PHASE_TABLE

K8 nodes: quark, gluon, neutrino, photon, electron, higgs, muon, tau
Proton is DERIVED (composite): p = quark + C*gluon
BW = p + C*g = quark + 2*C*gluon
"""
from __future__ import annotations

import numpy as np
from itertools import combinations

# ── Constants ──────────────────────────────────────────────────────────────
C  = 2*(2**0.5)/10   # sqrt(2)/5 = 0.2828
C2 = C * C           # 0.08
F_1_64 = 1/64        # 0.015625 - 평형점 닫힘 값 (final closure parameter)
OMEGA = 7.4

TURNING_POINT_AGE = 10.0
BRIDGE_13_SCALE   = 4.0
EFFICIENCY_TARGET = 0.8009

SUBJECTS = ("quark", "gluon", "neutrino", "photon", "electron",
            "higgs", "muon", "tau")
IDX  = {s: i for i, s in enumerate(SUBJECTS)}
EDGES = [(a, b) for a, b in combinations(SUBJECTS, 2)]  # 28 edges

# ── Base edge weights (K8) ─────────────────────────────────────────────────
BASE_W: dict[tuple, float] = {e: 0.0 for e in EDGES}

# QCD sector
BASE_W[("quark",   "gluon")]    = 1.0 + C

# Strong → weak bridge (quark/gluon couple to W boson, not proton directly)
BASE_W[("quark",   "muon")]     = 1.0
BASE_W[("gluon",   "muon")]     = 1.0

# EM sector
BASE_W[("neutrino","photon")]   = 1/16
BASE_W[("photon",  "muon")]     = 2/16
BASE_W[("photon",  "electron")] = 3/16

# Neutral current / Z proxy (was neutrino-proton)
BASE_W[("neutrino","tau")]      = 3/16

# Weak decay (was proton-electron)
BASE_W[("muon",    "electron")] = 3/16

# Lepton sector
BASE_W[("neutrino","electron")] = 4/16

# Sub-leading couplings (unchanged from K6)
BASE_W[("quark",   "neutrino")] = C2/128
BASE_W[("gluon",   "neutrino")] = C2/256
BASE_W[("gluon",   "photon")]   = C2/128
BASE_W[("quark",   "photon")]   = C2/64
BASE_W[("quark",   "electron")] = C2/128
BASE_W[("gluon",   "electron")] = C2/256

# Higgs mechanism: W and Z get mass through Higgs coupling
BASE_W[("higgs",   "muon")]     = C
BASE_W[("higgs",   "tau")]      = C
BASE_W[("muon",    "tau")]      = C

# ── Channel map (28 K8 edge channels only) ──────────────────
# Each of the 28 edges of K8 maps to EXACTLY ONE biological channel.
# Edge tuple order follows SUBJECTS index order (combinations order).
# SUBJECTS = (quark=0, gluon=1, neutrino=2, photon=3, electron=4,
#              higgs=5, muon=6, tau=7)
#
# NEUTRINO HEPTAGON (7 edges: neutrino ↔ each other particle)
#   (quark,neutrino)  = right_dopamine  — time truth / pure flow
#   (gluon,neutrino)  = female_left_noradrenaline — gluon truth / deception cancel
#   (neutrino,photon) = male_gaba_b           — light truth / inner spark
#   (neutrino,electron)= left_endorphin          — charge truth / naked bond
#   (neutrino,higgs)  = b_type_muscle      — mass truth / invariant anchor
#   (neutrino,muon)   = right_epinephrine          — change truth / seeking drive
#   (neutrino,tau)    = right_cortisol— neutral truth / concealment
#
# MUON HEXAGON (6 edges: muon ↔ each non-neutrino particle)
#   (photon,muon)     = left_epinephrine — EM ignition accelerator
#   (quark,muon)      = female_gaba_b               — kinetic time / BW constraint
#   (higgs,muon)      = male_left_noradrenaline     — proton neutralize / 4:30 PM
#   (electron,muon)   = a_type_muscle — charge transform block
#   (gluon,muon)      = right_extraversion               — structural tension
#   (muon,tau)        = left_d2          — spark clamp / night betrayal
#
# REMAINING 15 edges (all pairs among quark/gluon/photon/electron/higgs/tau)
CHANNEL_MAP: dict[str, dict[tuple, dict[str, float]]] = {
    # ── 28 channels = exact K8 edge-channel core ────────────────────────────
    # 28 edges (complete K8) — 1:1 mapping to body control nodes
    "receptor_5ht1a":               {("quark",   "gluon"):      {"on": +2 * C2, "off": -C2, "no_control": 0}},
    "right_alpha_2":  {("gluon",   "tau"):        {"on": +C2,     "off": 0,   "no_control": 0}},
    "glucocorticoid":         {("quark",   "electron"):   {"on": +2*C2, "off": 0,    "no_control": 0}},
    "male_gaba_b":           {("neutrino","photon"):     {"on": +C2,     "off": 0,   "no_control": 0}},
    "left_epinephrine":  {("photon",  "muon"):       {"on": +C2,     "off": 0,   "no_control": 0}},
    "right_dopamine":   {("electron","higgs"):      {"on": +C2,     "off": 0,   "no_control": 0}},
    "acetyl_coa":           {("quark",   "neutrino"):   {"on": +2 * C2, "off": 0,   "no_control": 0}},
    "b_type_muscle":      {("neutrino", "higgs"):     {"on": +C2,   "off": 0,    "no_control": F_1_64}},
    "female_vasopressin":                 {("gluon",   "higgs"):      {"on": +C2,     "off": 0,   "no_control": 0}},
    "right_epinephrine":          {("neutrino","muon"):       {"on": +4 * C2, "off": 0,   "no_control": 0}},
    "male_left_noradrenaline":      {("higgs",   "muon"):       {"on": +3 * C2, "off": 0,   "no_control": 0}},
    "left_endorphin":           {("neutrino","electron"):   {"on": +2 * C2, "off": 0,   "no_control": 0}},
    "right_extraversion":                {("gluon",   "muon"):       {"on": +2 * C2, "off": -C2, "no_control": 0}},
    "female_gaba_b":                {("quark",   "muon"):       {"on": +2 * C2, "off": -C2, "no_control": 0}},
    "right_acetylcholine": {("photon",  "electron"):   {"on": +2 * C2, "off": 0,   "no_control": 0}},
    "female_right_self_satisfaction":          {("quark",   "higgs"):      {"on": +2 * C2, "off": 0,   "no_control": 0}},
    "female_gaba_a":          {("electron","tau"):        {"on": +C2,     "off": -C2, "no_control": 0}},
    "left_self_satisfaction":       {("gluon",   "electron"):   {"on": +C2,     "off": 0,   "no_control": 0}},
    "right_cortisol":{("neutrino","tau"):        {"on": +2 * C2, "off": 0,   "no_control": 0}},
    "a_type_muscle": {("muon",    "electron"):   {"on": +C2,     "off": 0,   "no_control": 0}},
    "left_extraversion":     {("photon",  "tau"):        {"on": +C2,     "off": 0,   "no_control": 0}},
    "right_5ht1b_synchrotron":       {("quark",   "photon"):     {"on": +2 * C2, "off": 0,   "no_control": 0}},
    "hypoxia":      {("gluon",   "photon"):     {"on": +2 * C2, "off": 0,   "no_control": 0}},
    "female_left_noradrenaline": {("gluon",   "neutrino"):   {"on": +2 * C2, "off": 0,   "no_control": 0}},
    "male_gaba_a":          {("quark",   "tau"):        {"on": +C2,     "off": -C2, "no_control": 0}},
    "right_androgen":          {("higgs",   "tau"):        {"on": +2 * C2, "off": -C2, "no_control": 0}},
    "left_d2":           {("muon",    "tau"):        {"on": -C2,     "off": +4 * C2, "no_control": 0}},
    "male_right_noradrenaline":             {("photon",  "higgs"):      {"on": +C2,     "off": 0,   "no_control": 0}},
}


CHANNEL_ORDER = tuple(CHANNEL_MAP.keys())

OBSERVER_BRIDGE_MAP = {
    "cck": "quark",
    "right_d2": "gluon",
    "male_oxytocin": "neutrino",
    "right_love": "photon",
    "left_serotonin": "electron",
    "gdh": "higgs",
    "my_left_epinephrine": "muon",
    "my_right_self_satisfaction": "tau",
}

# ── Channel particle tiers ─────────────────────────────────────────────────
# Tier = K8 edge type of the channel's PRIMARY coupling.
# Lower tier fires FIRST inside a phase (stronger/slower coupling = carrier).
#
#   1  QCD            quark-gluon, gluon-muon, quark-muon
#   2  EM photon-muon photon-muon  (spark bridge / BW line)
#   3  EM photon-e    photon-electron (synchrotron / extraversion)
#   4  EM nu-photon   neutrino-photon (GABA-A, 5HT1A neutral bridge)
#   5  Weak lepton    muon-electron, neutrino-electron
#   6  Tau neutral    neutrino-tau  (vasopressin, alpha-2, GABA-B)
#   7  Exogenous      environmental input (female_vasopressin — no K8 coupling)

CHANNEL_TIER: dict[str, int] = {
    # Tier 1 — QCD / strong↔weak backbone
    "receptor_5ht1a":               1,   # quark-gluon
    "right_extraversion":                1,   # gluon-muon
    "female_gaba_b":                1,   # quark-muon
    # Tier 2 — photon↔W spark bridge
    "left_epinephrine": 2,   # photon-muon
    "glucocorticoid":      2,   # quark-electron (metabolic drive into charge)
    "left_self_satisfaction":       2,    # gluon-electron
    "left_extraversion":     2,    # photon-tau (recording/gating)
    "male_gaba_a":          2,    # quark-tau
    "right_androgen":          2,    # higgs-tau
    # Tier 3 — photon↔electron / social drive
    "right_acetylcholine": 3,
    "right_5ht1b_synchrotron":       3,
    "hypoxia":      3,
    "male_right_noradrenaline":             3,
    # Tier 4 — neutrino↔(quark/photon/z) neutral bridges
    "right_dopamine":   5,    # electron-higgs
    "male_gaba_b":           4,    # neutrino-photon
    "right_cortisol": 4,   # neutrino-tau
    "female_left_noradrenaline": 4,    # gluon-neutrino (night cancel switch)
    # Tier 5 — weak lepton / mass coupling
    "b_type_muscle":      5,   # neutrino-higgs (LC resonator, mass anchor)
    "left_endorphin":           5,    # neutrino-electron
    "acetyl_coa":           4,    # quark-neutrino
    "a_type_muscle": 5,   # muon-electron (charged coupling, male contribution)
    "right_epinephrine":          5,    # neutrino-muon
    "female_right_self_satisfaction":          5,    # quark-higgs
    "female_gaba_a":          5,    # electron-tau
    # Tier 6 — electroweak / Z clamp
    "right_alpha_2":  6,    # gluon-tau
    "male_left_noradrenaline":      6,    # higgs-muon
    "left_d2":           6,    # muon-tau
    # Tier 7 — exogenous / environmental
    "female_vasopressin":                 7,    # gluon-higgs (risk/exogenous)
    # Tier 8 — observers
    }

# Phase-specific tier firing order.
# Tuple = (tier_first, tier_second, ...) — controls which particle sector leads.
#
#   phase1          QCD-first  : BW (quark-gluon) fills as carrier
#   phase2          EM-first   : photon-muon spark ignites, QCD follows
#   proton_landing  Z-first    : male_left_noradrenaline (T6) receives PROTON; T3 right converges
#   night_spark     T3→T6      : female_left_noradrenaline triggers, Z disinhibits
#   hysteresis      Z-first    : left_d2 OFF opens Z, then lepton sector settles
_PHASE_TIER_ORDER: dict[str, tuple[int, ...]] = {
    "phase1":         (1, 2, 3, 4, 5, 6, 7),
    "phase2":         (2, 3, 4, 5, 1, 6, 7),
    "proton_landing": (6, 3, 4, 5, 2, 1, 7),
    "night_spark":    (3, 6, 2, 5, 4, 1, 7),
    "hysteresis":     (6, 5, 4, 2, 3, 1, 7),
}

_STATE_RANK = {"on": 0, "off": 1, "no_control": 2}


def phase_node_sequence(phase: str) -> list[str]:
    """Return all 28 K8 edge channels in temporal activation order for *phase*.

    Ordering rules (three-key sort):
      1. Tier priority for this phase  (which particle sector leads)
      2. State rank within tier        (on → off → no_control)
      3. CHANNEL_ORDER index           (insertion-order tiebreak)

    Example — night_spark fires: female_left_noradrenaline (T3,on) first,
    then left_d2 (T6,off = Z opens), then right_epinephrine (T2,on), …
    """
    if phase not in _PHASE_TIER_ORDER:
        raise ValueError(f"Unknown phase '{phase}'. Known: {list(_PHASE_TIER_ORDER)}")
    tier_rank = {tier: i for i, tier in enumerate(_PHASE_TIER_ORDER[phase])}
    states    = PHASE_TABLE.get(phase, {})

    def _key(ch: str) -> tuple[int, int, int]:
        t  = CHANNEL_TIER.get(ch, 99)
        pr = tier_rank.get(t, 99)
        sr = _STATE_RANK.get(states.get(ch, "no_control"), 2)
        return (pr, sr, CHANNEL_ORDER.index(ch))

    return sorted(CHANNEL_ORDER, key=_key)


def states_to_channel_vector(states: dict[str, str], *, no_control_value: float = 0.5) -> np.ndarray:
    """Convert {channel: on/off/no_control} → numeric vector in CHANNEL_ORDER."""
    v = np.zeros(len(CHANNEL_ORDER), dtype=float)
    for i, name in enumerate(CHANNEL_ORDER):
        st = str(states.get(name, "no_control"))
        if st == "on":
            v[i] = 1.0
        elif st == "off":
            v[i] = 0.0
        else:
            v[i] = float(no_control_value)
    return v

# ── PHASE_TABLE ────────────────────────────────────────────────────────────
PHASE_TABLE = {
    "phase1": {
        "receptor_5ht1a":"on","right_alpha_2":"off",
        "glucocorticoid":"on","male_gaba_b":"off",
        "left_epinephrine":"on","right_dopamine":"off",
        "acetyl_coa":"off","b_type_muscle":"off",
        "female_vasopressin":"no_control",
        "right_epinephrine":"off","male_left_noradrenaline":"on",
        "left_endorphin":"off",
        "right_extraversion":"on","female_gaba_b":"off",
        "right_acetylcholine":"no_control","female_right_self_satisfaction":"no_control",
        "female_gaba_a":"no_control","left_self_satisfaction":"on",
        "right_cortisol":"off","left_extraversion":"off",
        "right_5ht1b_synchrotron":"on","hypoxia":"off",
        "female_left_noradrenaline":"no_control",
        "male_gaba_a":"off","right_androgen":"on",
        "left_d2":"on","male_right_noradrenaline":"off",
        "a_type_muscle":"no_control",
    },
    "phase2": {
        "receptor_5ht1a":"no_control","right_alpha_2":"off",
        "glucocorticoid":"no_control","male_gaba_b":"no_control",
        "left_epinephrine":"off","right_dopamine":"off",
        "acetyl_coa":"no_control","b_type_muscle":"no_control",
        "female_vasopressin":"no_control",
        "right_epinephrine":"on","male_left_noradrenaline":"off",
        "left_endorphin":"no_control",
        "right_extraversion":"off","female_gaba_b":"on",
        "right_acetylcholine":"no_control","female_right_self_satisfaction":"on",
        "female_gaba_a":"off","left_self_satisfaction":"on",
        "right_cortisol":"off","left_extraversion":"no_control",
        "right_5ht1b_synchrotron":"on","hypoxia":"on",
        "female_left_noradrenaline":"no_control",
        "male_gaba_a":"off","right_androgen":"no_control",
        "left_d2":"off","male_right_noradrenaline":"off",
        "a_type_muscle":"no_control",
    },
    "hysteresis": {
        "receptor_5ht1a":"off","right_alpha_2":"on",
        "glucocorticoid":"off","male_gaba_b":"on",
        "left_epinephrine":"no_control","right_dopamine":"no_control",
        "acetyl_coa":"on","b_type_muscle":"on",
        "female_vasopressin":"no_control",
        "right_epinephrine":"off","male_left_noradrenaline":"on",
        "left_endorphin":"no_control",
        "right_extraversion":"on","female_gaba_b":"no_control",
        "right_acetylcholine":"no_control","female_right_self_satisfaction":"on",
        "female_gaba_a":"off","left_self_satisfaction":"on",
        "right_cortisol":"on","left_extraversion":"no_control",
        "right_5ht1b_synchrotron":"off","hypoxia":"off",
        "female_left_noradrenaline":"no_control",
        "male_gaba_a":"off","right_androgen":"off",
        "left_d2":"off","male_right_noradrenaline":"on",
        "a_type_muscle":"no_control",
    },
    "proton_landing": {
        # 16:30 | epi_L off (QCD released), sat_L off, epi_R no_control
        # male_left_noradrenaline ON: PROTON absorbed. left_d2 OFF: Z open.
        "receptor_5ht1a":"off","right_alpha_2":"off",
        "glucocorticoid":"off","male_gaba_b":"off",
        "left_epinephrine":"off","right_dopamine":"no_control",
        "acetyl_coa":"no_control","b_type_muscle":"no_control",
        "female_vasopressin":"on",
        "right_epinephrine":"off",
        "male_left_noradrenaline":"on",
        "left_endorphin":"on",
        "right_extraversion":"off","female_gaba_b":"off",
        "right_acetylcholine":"on",
        "female_right_self_satisfaction":"on",
        "female_gaba_a":"on",
        "left_self_satisfaction":"off",
        "right_cortisol":"on",
        "left_extraversion":"no_control",
        "right_5ht1b_synchrotron":"off",
        "hypoxia":"on",
        "female_left_noradrenaline":"on",
        "male_gaba_a":"off","right_androgen":"off",
        "left_d2":"off",
        "male_right_noradrenaline":"off",
        "a_type_muscle":"on",
    },
    "night_spark": {
        # 03:00–03:15 | 318.88° — sat_L OFF → epi_R FREE → cancels QCD.
        # right_epinephrine ON: Parkinson's critical window.
        # left_d2 OFF: Z disinhibition.
        "receptor_5ht1a":"off",
        "right_alpha_2":"on",
        "glucocorticoid":"off",
        "male_gaba_b":"on",
        "left_epinephrine":"off",
        "right_dopamine":"no_control",
        "acetyl_coa":"on","b_type_muscle":"on",
        "female_vasopressin":"on",
        "right_epinephrine":"on",
        "male_left_noradrenaline":"on",
        "left_endorphin":"no_control","right_extraversion":"on","female_gaba_b":"no_control",
        "right_acetylcholine":"on",
        "female_right_self_satisfaction":"no_control",
        "female_gaba_a":"on","left_self_satisfaction":"on",
        "right_cortisol":"on","left_extraversion":"on",
        "right_5ht1b_synchrotron":"off","hypoxia":"on",
        "female_left_noradrenaline":"on",
        "male_gaba_a":"off","right_androgen":"off",
        "left_d2":"off",
        "male_right_noradrenaline":"on",
        "a_type_muscle":"on",
    },
}

# ── Phase time windows (24-h clock, origin = 06:00, 16 windows × 1.5h) ────────
PHASE_TIME_WINDOWS = {
    "phase1":            {"start": "15:45", "end": "15:45", "description": "BW capture (spark charge)"},
    "phase2":            {"start": "09:45", "end": "09:45", "description": "spark ignition (138.88°)"},
    "proton_landing":    {"start": "16:30", "end": "16:30", "description": "PROTON neutralization (157.5°, 75min post-spark)"},
    "hysteresis":        {"start": "02:15", "end": "04:30", "description": "Z boson / neutrino (left_d2 OFF)"},
    "night_spark":       {"start": "03:00", "end": "03:15", "description": "night discharge (318.88° = SPARK+180°)"},
    # ── Debt settlement windows ────────────────────────────────────────────
    "coulomb_settle":    {"start": "15:00", "end": "15:00", "description": "Coulomb debt settlement (A_ESFJ_female / -z linear anchor)", "archetype": "A_ESFJ_female",  "debt": "coulomb"},
    "confinement_reset": {"start": "03:15", "end": "03:15", "description": "Confinement debt + time-reversal / 역회귀 (AB_ENFJ_female)", "archetype": "AB_ENFJ_female", "debt": "confinement"},
    "dawn_closure":      {"start": "04:30", "end": "04:30", "description": "Bremsstrahlung final seal — b_type_muscle=1/64, exp(-√Z/64) (B_ISTP_female)", "archetype": "B_ISTP_female",  "debt": "bremsstrahlung"},
}

# ── Functions ──────────────────────────────────────────────────────────────

def age_scaling(age: float) -> float:
    if age < 10: return age / 10.0
    if age < 25: return 1.0
    return max(0.1, 1.0 - (age - 25) / 100.0)


def apply_channels(channels: dict[str, str], age: float = 25.0) -> dict[tuple, float]:
    w = {e: float(v) for e, v in BASE_W.items()}
    scale = age_scaling(age)
    for ch, state in channels.items():
        if ch not in CHANNEL_MAP or state == "no_control":
            continue
        for edge, deltas in CHANNEL_MAP[ch].items():
            # Normalize edge tuple to match the order in BASE_W (lexicographical by index)
            a, b = edge
            if IDX[a] > IDX[b]:
                edge = (b, a)

            delta = float(deltas.get(state, 0.0))
            w[edge] = max(0.0, w[edge] + delta * scale)
    return w


def laplacian(w: dict[tuple, float]) -> np.ndarray:
    L = np.zeros((8, 8), dtype=float)
    for (a, b), wv in w.items():
        ia, ib = IDX[a], IDX[b]
        val = np.exp(wv) - 1.0
        L[ia, ia] += val;  L[ib, ib] += val
        L[ia, ib] -= val;  L[ib, ia] -= val
    return L


# ---------------------------------------------------------------------------
# 4D motif / target projection (BM, BW, SM, SW) and initialization
# ---------------------------------------------------------------------------

MOTIF_DEGREES_4 = np.array([6.0, 8.0, 8.0, 10.0], dtype=float)  # BM, BW, SM, SW


def project4(x8: np.ndarray) -> np.ndarray:
    """Project an 8D K8 state into the canonical 4D motif space.

    Returns a vector [BM, BW, SM, SW] where:
      - BW = quark + 2*C*gluon                    (proton-composite line)
      - BM = photon + C*gluon                     (photon dressed by gluon)
      - SM = neutrino + C*quark                   (neutrino dressed by quark)
      - SW = electron + C*quark                   (electron dressed by quark)
    """
    x = np.asarray(x8, dtype=float).ravel()
    if x.size < 8:
        x = np.pad(x, (0, 8 - x.size))
    q, g, nu, ph, el = (float(v) for v in x[:5])
    bw = q + 2.0 * C * g
    bm = ph + C * g
    sm = nu + C * q
    sw = el + C * q
    return np.array([bm, bw, sm, sw], dtype=float)


def day_target() -> np.ndarray:
    """Canonical day target in 4D motif space (normalized to OMEGA)."""
    v = np.asarray(MOTIF_DEGREES_4, dtype=float)
    return OMEGA * (v / float(np.linalg.norm(v)))


def night_target() -> np.ndarray:
    """Canonical night target in 4D motif space.

    Matches the repo's standard night shift:
      BW -= C,  SM += C
    """
    t = np.asarray(day_target(), dtype=float).copy()
    t[1] -= float(C)  # BW
    t[2] += float(C)  # SM
    return t


def init_state8_from_target4(t4: np.ndarray, *, g: float = 0.1) -> np.ndarray:
    """Construct an 8D K8 state consistent with a desired 4D motif target.

    This is not unique; we pick a deterministic, stable initialization used
    across the repo (see archive/fusion_clean.py fallbacks).
    """
    bm, bw, sm, sw = (float(v) for v in np.asarray(t4, dtype=float).ravel()[:4])
    g = float(g)
    q = bw - 2.0 * C * g
    nu = sm - C * q
    ph = bm - C * g
    el = sw - C * q
    hi = float(C) / 2.0
    w = q * float(C)
    z = nu * float(C)
    return np.array([q, g, nu, ph, el, hi, w, z], dtype=float)


def init_state6_from_target4(t4: np.ndarray) -> np.ndarray:
    """Backward-compat alias: older code calls this '6' but uses an 8D K8 state."""
    return init_state8_from_target4(t4)


# ---------------------------------------------------------------------------
# Massless-sector utilities
# ---------------------------------------------------------------------------
MASSLESS_SUBJECTS = ("gluon", "neutrino", "photon")
MASSLESS_IDX = tuple(IDX[s] for s in MASSLESS_SUBJECTS)


def massless_submatrix(L: np.ndarray) -> np.ndarray:
    """Return the Laplacian restricted to the (gluon, neutrino, photon) subspace.

    Note: this is a *closed-subspace approximation*. In the full K8 dynamics,
    these nodes also couple to quark/electron/W/Z/Higgs; this helper is meant
    for explicit mixing diagnostics and time-only reinterpretations.
    """
    idx = MASSLESS_IDX
    return np.asarray(L, dtype=float)[np.ix_(idx, idx)].copy()


def massless_mix_matrix(L: np.ndarray, dt: float) -> np.ndarray:
    """Compute the massless mixing operator exp(-dt * L_massless)."""
    Lm = massless_submatrix(L)
    evals, evecs = np.linalg.eigh(Lm)  # symmetric PSD in ideal arithmetic
    evals = np.clip(evals, 0.0, None)
    return evecs @ np.diag(np.exp(-float(dt) * evals)) @ evecs.T


def step_massless(x8: np.ndarray, L: np.ndarray, dt: float) -> np.ndarray:
    """Apply only the massless-sector mixing step to x8 (others unchanged)."""
    x = np.asarray(x8, dtype=float).copy()
    idx = np.array(MASSLESS_IDX, dtype=int)
    U = massless_mix_matrix(L, dt=float(dt))
    x[idx] = U @ x[idx]
    return x




# backward-compat alias (sovereign_128 imports this name)


def _objective_baseline(w: dict[tuple, float]) -> float:
    """Objective: how close the effective weights are to BASE_W (cancellation)."""
    return float(sum((float(w[e]) - float(BASE_W[e])) ** 2 for e in BASE_W))


def _best_objective_with_forced(
    base_states: dict[str, str],
    unknown: list[str],
    *,
    force: dict[str, str],
    age: float,
) -> tuple[float, dict[str, str]]:
    forced = dict(base_states)
    forced.update({k: v for k, v in force.items() if k in forced})

    remaining = [ch for ch in unknown if forced.get(ch, "no_control") == "no_control"]
    best_obj: float | None = None
    best_states: dict[str, str] = forced

    # brute-force is fine here: typical unknown count is small (≤ 11 in current PHASE_TABLE)
    from itertools import product

    for assign in product(("on", "off"), repeat=len(remaining)):
        cand = dict(forced)
        for ch, st in zip(remaining, assign):
            cand[ch] = st
        w = apply_channels(cand, age=age)
        obj = _objective_baseline(w)
        if best_obj is None or obj < best_obj:
            best_obj = obj
            best_states = cand

    return float(best_obj if best_obj is not None else _objective_baseline(apply_channels(best_states, age=age))), best_states


def resolve_phase_states(
    phase: str,
    *,
    age: float = 25.0,
    keep_ambiguous_no_control: bool = True,
    ambiguity_tol: float = 1e-9,
    overrides: dict[str, str] | None = None,
) -> dict[str, str]:
    """Resolve PHASE_TABLE states using the particle-edge map.

    - Start from PHASE_TABLE[phase] (strings: on/off/no_control).
    - Optionally apply `overrides`.
    - Fill any `no_control` entries with on/off by minimizing deviation from BASE_W.
    - If `keep_ambiguous_no_control=True`, channels whose best-on vs best-off objective
      differ by ≤ ambiguity_tol are kept as "no_control".
    """
    phase_key = str(phase).strip()
    if phase_key not in PHASE_TABLE:
        raise KeyError(f"Unknown phase: {phase_key!r} (have: {sorted(PHASE_TABLE)})")

    states = dict(PHASE_TABLE[phase_key])
    if overrides:
        states.update({k: str(v) for k, v in overrides.items() if k in states})

    unknown = [ch for ch, st in states.items() if st == "no_control" and ch in CHANNEL_MAP]
    if not unknown:
        return states

    best_obj, best_states = _best_objective_with_forced(states, unknown, force={}, age=float(age))

    if not keep_ambiguous_no_control:
        return best_states

    ambiguous: set[str] = set()
    for ch in unknown:
        obj_on, _ = _best_objective_with_forced(states, unknown, force={ch: "on"}, age=float(age))
        obj_off, _ = _best_objective_with_forced(states, unknown, force={ch: "off"}, age=float(age))
        if abs(obj_on - obj_off) <= float(ambiguity_tol) * max(1.0, float(best_obj)):
            ambiguous.add(ch)

    resolved = dict(states)
    for ch in unknown:
        resolved[ch] = "no_control" if ch in ambiguous else best_states.get(ch, "no_control")
    return resolved


def day_phase_states(*, age: float = 25.0) -> dict[str, str]:
    """Day = phase1 with left-noradrenaline active inhibiting female_left_noradrenaline."""
    base = dict(PHASE_TABLE["phase1"])
    overrides: dict[str, str] = {}
    if base.get("left_epinephrine") == "on":
        overrides["female_left_noradrenaline"] = "off"
    return resolve_phase_states(
        "phase1",
        age=float(age),
        keep_ambiguous_no_control=False,  # day: fully resolved ON/OFF
        overrides=overrides,
    )


def night_phase_states(*, age: float = 25.0) -> dict[str, str]:
    """Night = phase2 with female_left_noradrenaline default ON (no left-noradrenaline inhibition)."""
    overrides = {"female_left_noradrenaline": "on"}
    return resolve_phase_states(
        "phase2",
        age=float(age),
        keep_ambiguous_no_control=True,   # night: allow residual "no_control"
        # Keep "3rd-state" nodes when the best ON/OFF objectives are close.
        # Tuned so night keeps a small set of residual no_control under the current map.
        ambiguity_tol=5e-2,
        overrides=overrides,
    )


def night_spark_states(*, age: float = 25.0) -> dict[str, str]:
    """Night spark = 03:00-03:15 (318.88° from 6:00).

    15-min discharge window within hysteresis.
    - left_epinephrine OFF  → female_left_noradrenaline FREE (ON)
    - female_left_noradrenaline ON     → cancels gluon / left_d2 (photon-wboson: -C²)
    - right_epinephrine ON              → Parkinson's critical window
    - left_d2 OFF              → Z boson disinhibition
    All states are fully resolved (no no_control residuals).
    """
    return resolve_phase_states(
        "night_spark",
        age=float(age),
        keep_ambiguous_no_control=False,  # spark: sharp discharge, all resolved
    )


def compose_core_operator10d(states: dict[str, str]) -> np.ndarray:
    """Lift the 28 core edge-channel states into a 10x10 operator."""
    from geometry_package.channel_operator_10d import compose_operator

    core_states = {k: v for k, v in states.items() if k in CHANNEL_MAP}
    return compose_operator(core_states)


def compose_full_operator10d(
    core_states: dict[str, str],
    bridge_states: dict[str, str] | None = None,
) -> np.ndarray:
    """Lift the full 36-node state (28 core + 8 observer bridges) into 10x10."""
    from geometry_package.channel_operator_10d import compose_operator

    states = {k: v for k, v in core_states.items() if k in CHANNEL_MAP}
    if bridge_states:
        for k, v in bridge_states.items():
            if k in OBSERVER_BRIDGE_MAP:
                states[k] = v
    return compose_operator(states)


def spark_bridge_states(
    overrides: dict[str, str] | None = None,
) -> dict[str, str]:
    """Default observer-bridge activation state for spark discharge algebra.

    This is not a primitive sequence axiom. It is the current bridge-loading
    snapshot used when composing the full 36-node operator.
    """
    states = {
        "cck": "on",
        "right_d2": "on",
        "male_oxytocin": "off",
        "right_love": "on",
        "left_serotonin": "off",
        "gdh": "on",
        "my_left_epinephrine": "on",
        "my_right_self_satisfaction": "on",
    }
    if overrides:
        for key, value in overrides.items():
            if key in OBSERVER_BRIDGE_MAP:
                states[key] = str(value)
    return states


def full_spark_operator10d(*, age: float = 25.0) -> np.ndarray:
    """Compose the current spark-window 36-node operator on the 10-subject space."""
    core = night_spark_states(age=float(age))
    bridges = spark_bridge_states()
    return compose_full_operator10d(core, bridges)
