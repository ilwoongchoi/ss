"""4 Stress Energy Pairs → 5-Sphere Toroidal Circulation Engine.

The 8D vector decomposes into 4 dualistic stress pairs. Each pair drives one
segment of the 5-sphere toroidal cycle (Sun→Earth→Moon→CoMag→Barnard→Sun).

4 Stress Pairs (from universe-prose.md 8D 감각-스트레스 매핑):
  1. O₂/CO₂   : h (CO₂/osmotic, Earth) ↔ p (oxygen/salt, Moon)
  2. Matter/Non-matter : s (mass/brightness, Sun) ↔ g (binding/무질량, Barnard/CoMag)
  3. Heat/Cold : nu (heat/self-similarity, Moon) ↔ r (cold/rhythm, Sun)
  4. Light/Dark: gamma (light/expansion, Earth/CoMag) ↔ d (dark/dissonance, Barnard)

5 Spheres (toroidal path):
  Sun(H) → Earth(O) → Moon(C) → CoMag(S) → Barnard(Fe) → Sun

Each transition is driven by one stress pair:
  Sun→Earth  (AB spark,      0-3h)  : Light/Dark   (s→gamma)
  Earth→Moon (A accumulate,  3-9h)  : O₂/CO₂       (h→p)
  Moon→CoMag (O accumulate,  9-15h) : Heat/Cold    (nu→g)
  CoMag→Barnard (B accumulate,15-21h): Matter/Non-matter (g→d)
  Barnard→Sun (AB integration,21-3h): Reset/Spark  (d→r, g→s)

3 Attractors:
  Energy      : r, g, gamma  — observer_leftd2→Carbon→SDH→Autophagy→NaCl→Actomyosin→observer_leftd2
  Information : h, nu, s     — MC1R→Glymphatic→Cysteine→MemoryEntropy→PosteriorInsula→Carbon→MC1R
  Repair      : p, d, g      — Carbon→Mycorradicin→Autophagy→Collagen→Methionine→SubstanceP→MC1R→Carbon
"""
from __future__ import annotations

import json
import pathlib
from collections import deque
from typing import Dict, List, Optional, Tuple

from .circuit_loader import NODES

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 4 Stress Pairs
# ---------------------------------------------------------------------------
STRESS_PAIRS: Dict[str, Dict] = {
    "o2_co2": {
        "name": "O₂/CO₂ Stress",
        "name_kr": "산소/이산화탄소 스트레스",
        "dims": ("h", "p"),
        "day_sensor": "h — female GABA-B CO₂ sensor (osmotic stress)",
        "night_stress": "p — hypoxic / low-water oxygen stress",
        "pole_a": {"sphere": "Earth", "dim": "h", "sense": "CO₂/osmotic"},
        "pole_b": {"sphere": "Moon", "dim": "p", "sense": "oxygen/salt"},
        "toroidal_segment": "Earth→Moon",
        "circadian_phase": "A_accumulate",
        "hours": (3, 9),
        "attractors": ("Information", "Repair"),
    },
    "matter_nonmatter": {
        "name": "Matter/Non-matter Stress",
        "name_kr": "물질/비물질 스트레스",
        "dims": ("s", "g"),
        "day_sensor": "s — right sole dopamine C mass / osmotic sense",
        "night_stress": "g — 무질량 sensor (male osmotic) / cold-sense binding",
        "pole_a": {"sphere": "Sun", "dim": "s", "sense": "mass/brightness"},
        "pole_b": {"sphere": "Barnard", "dim": "g", "sense": "binding density/무질량"},
        "bridge": {"sphere": "CoMag", "dim": "g", "sense": "sulfur bridge coupling"},
        "toroidal_segment": "CoMag→Barnard",
        "circadian_phase": "B_accumulate",
        "hours": (15, 21),
        "attractors": ("Energy", "Information"),
    },
    "heat_cold": {
        "name": "Heat/Cold Stress",
        "name_kr": "열/냉기 스트레스",
        "dims": ("nu", "r"),
        "day_sensor": "nu — male GABA-A temperature sensor (heat)",
        "night_stress": "r — 무질량 stress / acid sensor (cold)",
        "pole_a": {"sphere": "Moon", "dim": "nu", "sense": "heat/self-similarity"},
        "pole_b": {"sphere": "Sun", "dim": "r", "sense": "cold/rhythm"},
        "toroidal_segment": "Moon→CoMag",
        "circadian_phase": "O_accumulate",
        "hours": (9, 15),
        "attractors": ("Information", "Energy"),
    },
    "light_dark": {
        "name": "Light/Dark Stress",
        "name_kr": "빛/암흑 스트레스",
        "dims": ("gamma", "d"),
        "day_sensor": "gamma — right D2 UV sensor (light)",
        "night_stress": "d — light stress / photonic load (darkness inversion)",
        "pole_a": {"sphere": "Earth", "dim": "gamma", "sense": "light/spatial expansion"},
        "pole_b": {"sphere": "Barnard", "dim": "d", "sense": "dark/dissonance"},
        "toroidal_segment": "Sun→Earth",
        "circadian_phase": "AB_spark",
        "hours": (0, 3),
        "attractors": ("Energy", "Repair"),
    },
}

# ---------------------------------------------------------------------------
# 5 Spheres
# ---------------------------------------------------------------------------
SPHERES: Dict[str, Dict] = {
    "Sun": {
        "element": "H",
        "particle": "Proton",
        "attractor": "Information",
        "attractor_role": "Information Attractor 점화 — 예측/학습의 스파크",
        "dims": ("r", "s"),
        "nodes": ["cytochrome_c_oxidase", "heme"],
        "body_region": "brain/ETC",
    },
    "Earth": {
        "element": "O",
        "particle": "Photon",
        "attractor": "Repair",
        "attractor_role": "Repair Attractor 엔진 — 산소 기반 항상성",
        "dims": ("gamma", "h"),
        "nodes": ["steel", "water_vapour", "succinate_dehydrogenase"],
        "body_region": "thorax/spine",
    },
    "Moon": {
        "element": "C",
        "particle": "Z-boson",
        "attractor": "Time",
        "attractor_role": "3개 어트랙터의 시간 조정 — 28일 스케줄",
        "dims": ("p", "nu"),
        "nodes": ["co2", "carbon", "memory_entropy"],
        "body_region": "occiput/right brain",
    },
    "CoMag": {
        "element": "S",
        "particle": "W-boson/Gluon",
        "attractor": "Bridge",
        "attractor_role": "어트랙터 간 결합 브릿지 — Maxwell/약력 매개",
        "dims": ("g", "gamma"),
        "nodes": ["sulforaphane", "histosol", "pyrite"],
        "body_region": "pelvis/gut",
    },
    "Barnard": {
        "element": "Fe",
        "particle": "Quark/Higgs",
        "attractor": "Energy",
        "attractor_role": "Energy Attractor 닻 — 질량 저장, 북극점",
        "dims": ("g", "d"),
        "nodes": ["heme", "ferritin", "sulfur_iron_complex"],
        "body_region": "chest/liver",
    },
}

# Toroidal cycle order
TOROIDAL_ORDER: List[str] = ["Sun", "Earth", "Moon", "CoMag", "Barnard"]

# Toroidal transitions: (from_sphere, to_sphere, stress_pair, phase, hours, description)
TOROIDAL_TRANSITIONS: List[Dict] = [
    {
        "from": "Sun",
        "to": "Earth",
        "stress_pair": "light_dark",
        "phase": "AB_spark",
        "hours": (0, 3),
        "desc": "정보 스파크가 수리 엔진을 점화 — s(brightness)→gamma(expansion)",
        "energy_flow": "Light energy: proton spark → oxygen repair ignition",
    },
    {
        "from": "Earth",
        "to": "Moon",
        "stress_pair": "o2_co2",
        "phase": "A_accumulate",
        "hours": (3, 9),
        "desc": "수리가 시간/스케줄에 축적 — h(CO₂)→p(oxygen)",
        "energy_flow": "O₂/CO₂ exchange: oxygen repair → carbon clock accumulation",
    },
    {
        "from": "Moon",
        "to": "CoMag",
        "stress_pair": "heat_cold",
        "phase": "O_accumulate",
        "hours": (9, 15),
        "desc": "시간이 결합 브릿지로 전환 — nu(heat)→g(binding)",
        "energy_flow": "Thermal gradient: carbon clock heat → sulfur bridge coupling",
    },
    {
        "from": "CoMag",
        "to": "Barnard",
        "stress_pair": "matter_nonmatter",
        "phase": "B_accumulate",
        "hours": (15, 21),
        "desc": "결합 에너지가 질량 저장소로 압축 — g(binding)→d(dissonance/mass)",
        "energy_flow": "Matter compression: sulfur binding → iron mass storage",
    },
    {
        "from": "Barnard",
        "to": "Sun",
        "stress_pair": "reset_spark",
        "phase": "AB_integration",
        "hours": (21, 3),
        "desc": "질량 저장이 다음 정보 스파크 충전 — d(dark)→r(cold/rhythm), g→s",
        "energy_flow": "Reset spark (138.88°): iron mass → proton spark recharge",
    },
]

# ---------------------------------------------------------------------------
# 3 Attractors
# ---------------------------------------------------------------------------
ATTRACTORS: Dict[str, Dict] = {
    "Energy": {
        "dims": ("r", "g", "gamma"),
        "loop": [
            "observer_leftd2", "carbon", "succinate_dehydrogenase",
            "autophagy", "nacl", "actomyosin", "observer_leftd2",
        ],
        "sphere": "Barnard",
        "breakdown": "Fatigue, Depression, Hypometabolism",
    },
    "Information": {
        "dims": ("h", "nu", "s"),
        "loop": [
            "mc1r", "glymphatic_system", "cysteine",
            "memory_entropy", "hind_insula", "carbon", "mc1r",
        ],
        "sphere": "Sun",
        "breakdown": "Anxiety, Schizophrenia, OCD",
    },
    "Repair": {
        "dims": ("p", "d", "g"),
        "loop": [
            "carbon", "mycorradicin", "autophagy",
            "collagen", "methionine", "substance_p",
            "mc1r", "carbon",
        ],
        "sphere": "Earth",
        "breakdown": "Chronic inflammation, Long COVID, HSV, Lyme",
    },
}

# ---------------------------------------------------------------------------
# Circuit path tracing between sphere nodes
# ---------------------------------------------------------------------------

def _find_path(src: str, dst: str, max_depth: int = 15) -> Optional[List[str]]:
    """BFS shortest directed path from src to dst through circuit edges."""
    if src not in NODES or dst not in NODES:
        return None
    if src == dst:
        return [src]
    seen = {src}
    parent: Dict[str, str] = {}
    q = deque([(src, 0)])
    while q:
        cur, d = q.popleft()
        if d >= max_depth:
            continue
        for port in NODES[cur].ports:
            if port.kind != "out":
                continue
            nxt = port.link.split(".")[0]
            if nxt not in NODES or nxt in seen:
                continue
            seen.add(nxt)
            parent[nxt] = cur
            if nxt == dst:
                # reconstruct
                path = [nxt]
                while path[-1] != src:
                    path.append(parent[path[-1]])
                return list(reversed(path))
            q.append((nxt, d + 1))
    return None


def _sphere_to_sphere_path(sphere_from: str, sphere_to: str) -> Dict:
    """Trace circuit paths between all node pairs of two spheres."""
    src_nodes = SPHERES[sphere_from]["nodes"]
    dst_nodes = SPHERES[sphere_to]["nodes"]
    paths = []
    for src in src_nodes:
        for dst in dst_nodes:
            if src == dst:
                continue
            p = _find_path(src, dst)
            if p:
                paths.append({
                    "from_node": src,
                    "to_node": dst,
                    "path": p,
                    "length": len(p),
                })
    # pick shortest path
    best = min(paths, key=lambda x: x["length"]) if paths else None
    return {
        "sphere_from": sphere_from,
        "sphere_to": sphere_to,
        "all_paths": paths,
        "best_path": best,
    }


# ---------------------------------------------------------------------------
# Energy circulation computation
# ---------------------------------------------------------------------------

def compute_circulation() -> Dict:
    """Compute the full 4-stress-pair toroidal energy circulation."""
    result = {
        "stress_pairs": {},
        "toroidal_cycle": [],
        "sphere_paths": [],
        "attractor_mapping": {},
    }

    # 1. Stress pair details
    for key, pair in STRESS_PAIRS.items():
        result["stress_pairs"][key] = {
            "name": pair["name"],
            "name_kr": pair["name_kr"],
            "dims": pair["dims"],
            "day_sensor": pair["day_sensor"],
            "night_stress": pair["night_stress"],
            "poles": {
                "a": pair["pole_a"],
                "b": pair["pole_b"],
            },
            "toroidal_segment": pair["toroidal_segment"],
            "circadian_phase": pair["circadian_phase"],
            "hours": pair["hours"],
            "attractors": pair["attractors"],
        }

    # 2. Toroidal transitions with circuit paths
    for trans in TOROIDAL_TRANSITIONS:
        entry = {
            **trans,
            "from_sphere_info": SPHERES[trans["from"]],
            "to_sphere_info": SPHERES[trans["to"]],
        }
        if trans["stress_pair"] != "reset_spark":
            path_info = _sphere_to_sphere_path(trans["from"], trans["to"])
            entry["circuit_paths"] = path_info
        else:
            # Reset spark: Barnard→Sun — the 138.88° diagonal
            path_info = _sphere_to_sphere_path(trans["from"], trans["to"])
            entry["circuit_paths"] = path_info
            entry["spark_angle"] = 138.88
            entry["spark_note"] = "138.88° diagonal reset spark — void 관통 각도"
        result["toroidal_cycle"].append(entry)

    # 3. All sphere-to-sphere circuit paths
    for i in range(len(TOROIDAL_ORDER)):
        s_from = TOROIDAL_ORDER[i]
        s_to = TOROIDAL_ORDER[(i + 1) % len(TOROIDAL_ORDER)]
        result["sphere_paths"].append(_sphere_to_sphere_path(s_from, s_to))

    # 4. Attractor mapping
    for name, attr in ATTRACTORS.items():
        # verify attractor loop paths
        loop_verified = []
        for j in range(len(attr["loop"]) - 1):
            a = attr["loop"][j]
            b = attr["loop"][j + 1]
            p = _find_path(a, b, max_depth=20)
            loop_verified.append({
                "from": a,
                "to": b,
                "path_exists": p is not None,
                "path": p,
            })
        result["attractor_mapping"][name] = {
            "dims": attr["dims"],
            "loop": attr["loop"],
            "sphere": attr["sphere"],
            "breakdown": attr["breakdown"],
            "loop_verified": loop_verified,
        }

    return result


# ---------------------------------------------------------------------------
# Per-hour energy flow
# ---------------------------------------------------------------------------

def _phase_from_hour(hour: float) -> str:
    if 0 <= hour < 3:
        return "AB_spark"
    if 3 <= hour < 9:
        return "A_accumulate"
    if 9 <= hour < 15:
        return "O_accumulate"
    if 15 <= hour < 21:
        return "B_accumulate"
    return "AB_integration"


def hourly_energy_flow() -> List[Dict]:
    """For each hour, report which stress pair is active and its flow direction."""
    hours = []
    for h in range(24):
        phase = _phase_from_hour(h)
        # find the transition for this phase
        trans = None
        for t in TOROIDAL_TRANSITIONS:
            t_phase = t["phase"]
            if t_phase == phase:
                trans = t
                break
        if trans is None:
            # AB_integration maps to the Barnard→Sun transition
            for t in TOROIDAL_TRANSITIONS:
                if t["phase"] == "AB_integration":
                    trans = t
                    break

        stress_key = trans["stress_pair"] if trans else "unknown"
        stress_info = STRESS_PAIRS.get(stress_key, {})
        active_dims = stress_info.get("dims", ())
        sphere_from = trans["from"] if trans else "?"
        sphere_to = trans["to"] if trans else "?"

        hours.append({
            "hour": h,
            "phase": phase,
            "stress_pair": stress_key,
            "stress_name": stress_info.get("name_kr", stress_key),
            "active_dims": active_dims,
            "sphere_from": sphere_from,
            "sphere_to": sphere_to,
            "sphere_from_dims": SPHERES.get(sphere_from, {}).get("dims", ()),
            "sphere_to_dims": SPHERES.get(sphere_to, {}).get("dims", ()),
            "energy_flow": trans["energy_flow"] if trans else "",
            "desc": trans["desc"] if trans else "",
        })
    return hours


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    circulation = compute_circulation()
    hourly = hourly_energy_flow()

    # Write JSON
    out_json = GEN_DIR / "energy_circulation.json"
    out_json.write_text(
        json.dumps({"circulation": circulation, "hourly": hourly}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Write human-readable report
    lines = []
    lines.append("=" * 80)
    lines.append("4 STRESS ENERGY PAIRS → 5-SPHERE TOROIDAL CIRCULATION")
    lines.append("=" * 80)
    lines.append("")

    # Stress pairs
    lines.append("■ 4 Stress Pairs (8D Decomposition)")
    lines.append("-" * 80)
    for key, pair in STRESS_PAIRS.items():
        lines.append(f"  {pair['name_kr']} ({pair['name']})")
        lines.append(f"    dims: {pair['dims']}")
        lines.append(f"    낮: {pair['day_sensor']}")
        lines.append(f"    밤: {pair['night_stress']}")
        lines.append(f"    pole_a: {pair['pole_a']['sphere']}({pair['pole_a']['dim']}) = {pair['pole_a']['sense']}")
        lines.append(f"    pole_b: {pair['pole_b']['sphere']}({pair['pole_b']['dim']}) = {pair['pole_b']['sense']}")
        lines.append(f"    toroidal: {pair['toroidal_segment']}  phase={pair['circadian_phase']}  hours={pair['hours']}")
        lines.append(f"    attractors: {pair['attractors']}")
        lines.append("")

    # Toroidal cycle
    lines.append("■ 5-Sphere Toroidal Cycle")
    lines.append("-" * 80)
    for i, trans in enumerate(TOROIDAL_TRANSITIONS):
        sf = SPHERES[trans["from"]]
        st = SPHERES[trans["to"]]
        stress = STRESS_PAIRS.get(trans["stress_pair"], {})
        lines.append(f"  [{i+1}] {trans['from']}→{trans['to']}  ({trans['phase']}, {trans['hours'][0]}-{trans['hours'][1]}h)")
        lines.append(f"      stress: {stress.get('name_kr', trans['stress_pair'])}")
        lines.append(f"      {sf['element']}({sf['particle']}) dims={sf['dims']} → {st['element']}({st['particle']}) dims={st['dims']}")
        lines.append(f"      flow: {trans['energy_flow']}")
        lines.append(f"      desc: {trans['desc']}")
        # circuit path
        path_info = _sphere_to_sphere_path(trans["from"], trans["to"])
        if path_info["best_path"]:
            bp = path_info["best_path"]
            lines.append(f"      circuit: {bp['from_node']} → {bp['to_node']} ({bp['length']} hops)")
            lines.append(f"        path: {' → '.join(bp['path'])}")
        else:
            lines.append(f"      circuit: NO DIRECT PATH (gap/manual bridge needed)")
        lines.append("")

    # Full toroidal diagram
    lines.append("■ Toroidal Energy Flow Diagram")
    lines.append("-" * 80)
    lines.append("  Sun(H) ──Light/Dark──→ Earth(O) ──O₂/CO₂──→ Moon(C) ──Heat/Cold──→ CoMag(S) ──Matter/Non-matter──→ Barnard(Fe)")
    lines.append("    ↑                                                                                    │")
    lines.append("    │                              ← Reset/Spark (138.88°) ←────────────────────────────│")
    lines.append("    └── r(cold), s(brightness) ←── d(dark), g(binding) ←──────────────────────────────┘")
    lines.append("")

    # 3 Attractors
    lines.append("■ 3 Attractors")
    lines.append("-" * 80)
    for name, attr in ATTRACTORS.items():
        lines.append(f"  {name} Attractor (dims={attr['dims']}, sphere={attr['sphere']})")
        lines.append(f"    loop: {' → '.join(attr['loop'])}")
        lines.append(f"    breakdown: {attr['breakdown']}")
        lines.append("")

    # Hourly
    lines.append("■ Hourly Energy Flow (24h)")
    lines.append("-" * 80)
    for h in hourly:
        lines.append(
            f"  {h['hour']:02d}:00  {h['phase']:16s}  "
            f"{h['stress_name']:20s}  "
            f"{h['sphere_from']:8s}→{h['sphere_to']:8s}  "
            f"dims={h['active_dims']}"
        )
    lines.append("")

    # Attractor ↔ Stress Pair ↔ Sphere cross-map
    lines.append("■ Cross-Map: Stress Pair ↔ Sphere ↔ Attractor")
    lines.append("-" * 80)
    lines.append("  Light/Dark    → Sun→Earth    → Energy + Repair")
    lines.append("  O₂/CO₂        → Earth→Moon   → Information + Repair")
    lines.append("  Heat/Cold     → Moon→CoMag   → Information + Energy")
    lines.append("  Matter/Non-m  → CoMag→Barnard→ Energy + Information")
    lines.append("  Reset/Spark   → Barnard→Sun  → All 3 (closure)")
    lines.append("")
    lines.append("  Each stress pair bridges exactly 2 attractors.")
    lines.append("  The 5th transition (reset) closes all 3 into a single toroidal manifold.")
    lines.append("")

    text = "\n".join(lines)
    print(text)
    (GEN_DIR / "energy_circulation.txt").write_text(text, encoding="utf-8")
    print(f"\n→ JSON: {out_json}")
    print(f"→ TXT:  {GEN_DIR / 'energy_circulation.txt'}")
