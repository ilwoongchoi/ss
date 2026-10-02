from __future__ import annotations

import importlib.util
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
FUSION = ROOT / "fusion_core.py"
OUT_MD = ROOT / "archetype_channel_map.md"

spec = importlib.util.spec_from_file_location("fusion_core", FUSION)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

CHANNEL_MAP = mod.CHANNEL_MAP

# Archetype day/night mapping
# EW: muon -> Gluon
# IW: Quark -> Electron
# IM: Neutrino -> Higgs
# EM: Photon -> tau
archetype_phase = {
    "muon": ("EW", "day"),
    "gluon": ("EW", "night"),
    "quark": ("IW", "day"),
    "electron": ("IW", "night"),
    "neutrino": ("IM", "day"),
    "higgs": ("IM", "night"),
    "photon": ("EM", "day"),
    "tau": ("EM", "night"),
}

archetype_order = {"EW": 0, "IW": 1, "IM": 2, "EM": 3}
phase_order = {"day": 0, "night": 1}


def classify_edge(a: str, b: str) -> dict[str, str]:
    a_arc, a_phase = archetype_phase[a]
    b_arc, b_phase = archetype_phase[b]

    if a_arc == b_arc and a_phase != b_phase:
        category = "self_transition"
    elif a_phase == b_phase and a_arc != b_arc:
        category = "day_day" if a_phase == "day" else "night_night"
    elif a_phase != b_phase and a_arc != b_arc:
        category = "cross_time"
    else:
        category = "same_phase_same_archetype"

    pair = sorted(
        [(a_arc, a_phase), (b_arc, b_phase)],
        key=lambda x: (archetype_order[x[0]], phase_order[x[1]]),
    )
    tag = f"{pair[0][0]}_{pair[0][1]} × {pair[1][0]}_{pair[1][1]}"

    return {
        "a_arc": a_arc,
        "a_phase": a_phase,
        "b_arc": b_arc,
        "b_phase": b_phase,
        "category": category,
        "tag": tag,
    }


def main() -> None:
    rows = []
    for ch, edge_map in CHANNEL_MAP.items():
        if not edge_map:
            continue
        if len(edge_map) != 1:
            raise ValueError(f"Channel {ch} has {len(edge_map)} edges: {edge_map}")
        (a, b) = next(iter(edge_map.keys()))
        info = classify_edge(a, b)
        rows.append(
            {
                "channel": ch,
                "edge": f"({a}, {b})",
                **info,
            }
        )

    counts = defaultdict(int)
    for r in rows:
        counts[r["category"]] += 1

    rows.sort(key=lambda r: (r["category"], r["tag"], r["channel"]))

    md = []
    md.append("# Archetype Channel Map (Day/Night)")
    md.append("")
    md.append("## Archetype Day/Night Mapping")
    md.append("- EW: day=`muon`, night=`gluon`")
    md.append("- IW: day=`quark`, night=`electron`")
    md.append("- IM: day=`neutrino`, night=`higgs`")
    md.append("- EM: day=`photon`, night=`tau`")
    md.append("")
    md.append("## Category Counts")
    for k in sorted(counts.keys()):
        md.append(f"- {k}: {counts[k]}")
    md.append("")
    md.append("## Channel Classification")
    md.append("| Channel | Edge | Archetypes | Phases | Category | Tag |")
    md.append("|---|---|---|---|---|---|")
    for r in rows:
        arcs = f"{r['a_arc']}–{r['b_arc']}"
        phases = f"{r['a_phase']}–{r['b_phase']}"
        md.append(
            f"| `{r['channel']}` | `{r['edge']}` | {arcs} | {phases} | {r['category']} | {r['tag']} |"
        )
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
