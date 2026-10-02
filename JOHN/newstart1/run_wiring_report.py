from __future__ import annotations

import json
from pathlib import Path

import fusion_clean as esm
from geometry_package import trilateral_compatibility_15 as tri
from geometry_package import universal_equation as ue


ROOT = Path(__file__).resolve().parent
OUT_MD = ROOT / "analysis_results" / "wiring_report.md"
OUT_JSON = ROOT / "analysis_results" / "wiring_report.json"


EDGE_TO_PAIR = {
    "BM_BW": ("photon", "proton"),
    "BM_SW": ("photon", "electron"),
    "BM_SM": ("photon", "neutrino"),
    "SM_BW": ("neutrino", "proton"),
    "BW_SW": ("proton", "electron"),
    "SM_SW": ("neutrino", "electron"),
}


def _slot_name_by_id() -> dict[int, str]:
    return {d.slot: d.name for d in tri.DOMAIN_SLOTS_15}


def main() -> int:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    slot_name = _slot_name_by_id()
    pair_edges = tri.pair_edges_15()
    pair_to_edge = {frozenset({e.a, e.b}): e for e in pair_edges}

    profiles = {
        "user/outside": esm._channel_control_profile(0, persona="user"),
        "user/hysteresis": esm._channel_control_profile(120, persona="user"),
        "people/outside": esm._channel_control_profile(0, persona="people"),
        "people/hysteresis": esm._channel_control_profile(120, persona="people"),
    }

    # Serialize JSON (raw data)
    OUT_JSON.write_text(
        json.dumps(
            {
                "channel_to_receptor": dict(esm.CHANNEL_TO_RECEPTOR),
                "profiles": profiles,
                "receptor_edge_map": {k: dict(v) for k, v in ue._RECEPTOR_EDGE.items()},
                "pair_edges_15": [e.__dict__ for e in pair_edges],
                "edge_to_pair_4": EDGE_TO_PAIR,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    lines: list[str] = []
    lines.append("# Wiring Report (Channels -> Receptors -> Edges -> 15-Domain Slots)")
    lines.append("")
    lines.append("This is a deterministic map from your named body/channel keys into:")
    lines.append("- receptor family (`universal_equation._RECEPTOR_EDGE`)")
    lines.append("- affected 4-particle edges (BM/BW/SM/SW)")
    lines.append("- corresponding 15-edge particle pairs + domain slots (`trilateral_compatibility_15.py`)")
    lines.append("")

    lines.append("## 15 Edges (Particle Pairs -> Domain Slot)")
    lines.append("")
    lines.append("| idx | pair | domain | slot | slot_name |")
    lines.append("|---|---|---|---:|---|")
    for e in pair_edges:
        lines.append(
            f"| {e.index} | {e.a}-{e.b} | {e.process_domain} | {e.mapped_slot} | {slot_name.get(e.mapped_slot,'')} |"
        )

    lines.append("")
    lines.append("## Channel Controls (user vs people, outside vs hysteresis)")
    lines.append("")
    lines.append("| channel_key | receptor | user/outside | user/hysteresis | people/outside | people/hysteresis |")
    lines.append("|---|---|---:|---:|---:|---:|")

    all_channel_keys = sorted(
        set(esm.CHANNEL_TO_RECEPTOR.keys())
        | set(profiles["user/outside"].keys())
        | set(profiles["user/hysteresis"].keys())
        | set(profiles["people/outside"].keys())
        | set(profiles["people/hysteresis"].keys())
    )
    for k in all_channel_keys:
        receptor = esm.CHANNEL_TO_RECEPTOR.get(k, "")
        lines.append(
            "| "
            + " | ".join(
                [
                    k,
                    receptor,
                    str(profiles["user/outside"].get(k, "")),
                    str(profiles["user/hysteresis"].get(k, "")),
                    str(profiles["people/outside"].get(k, "")),
                    str(profiles["people/hysteresis"].get(k, "")),
                ]
            )
            + " |"
        )

    lines.append("")
    lines.append("## Per-Channel Edge Impact")
    lines.append("")

    for k in sorted(esm.CHANNEL_TO_RECEPTOR.keys()):
        receptor = esm.CHANNEL_TO_RECEPTOR[k]
        edge_map = ue._RECEPTOR_EDGE.get(receptor, {})
        lines.append(f"### {k} -> {receptor}")
        lines.append("")
        if not edge_map:
            lines.append("- (no edges found for this receptor)")
            lines.append("")
            continue
        lines.append("| edge_4 | pair_6 | domain | slot | comp(stress,non_stress,assault,hospitality) |")
        lines.append("|---|---|---|---:|---|")
        for edge4, comp in edge_map.items():
            pair6 = EDGE_TO_PAIR.get(edge4)
            if pair6 is None:
                lines.append(f"| {edge4} |  |  |  | {comp} |")
                continue
            pe = pair_to_edge.get(frozenset(pair6))
            if pe is None:
                lines.append(f"| {edge4} | {pair6[0]}-{pair6[1]} |  |  | {comp} |")
                continue
            lines.append(
                f"| {edge4} | {pair6[0]}-{pair6[1]} | {pe.process_domain} | {pe.mapped_slot} | {comp} |"  # noqa: E501
            )
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(OUT_MD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
