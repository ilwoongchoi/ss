"""Bridge (v3): integrate state along energy_circulation attractor loops.

Couples absolute_constants into energy_circulation.py's attractor
structure (the properly-built engine) and runs a toroidal
state integration, then measures 8D deviation vs the
canonical constant reference (physics_tile_engine).

Does NOT modify any source file or circuitfile-rewritten.md.
"""
from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter

# run as:  python -m canonical_engine.energy_integrate  (from repo root)
from canonical_engine.energy_circulation import (
    ATTRACTORS, SPHERES, TOROIDAL_ORDER, TOROIDAL_TRANSITIONS,
    STRESS_PAIRS, _find_path,
)
from canonical_engine.absolute_constants import (
    C, OMEGA, SPARK_ANGLE_DEG, SPARK_ANGLE_RAD,
    NEUTRON_TIME_SYNC, SPARK_CONSTANT_C, SPARK_MAGNITUDE,
    LAMBDA_RISK_DECAY, M_RISK_GAIN,
    NOR_DEFAULT, PLP_DEFAULT, BINDING_IMPEDANCE,
)
from canonical_engine.physics_tile_engine import SPHERE_CONSTANTS, get_constant_weights, ALL_DIMS
from canonical_engine.circuit_sim import parse_circuit

GEN = pathlib.Path(__file__).parent / "generated"
GEN.mkdir(exist_ok=True)

DIMS = ALL_DIMS  # ["r","h","d","p","s","gamma","g","nu"]


def phase_from_hour(hour: float) -> str:
    if 0 <= hour < 3:
        return "AB_spark"
    if 3 <= hour < 9:
        return "A_accumulate"
    if 9 <= hour < 15:
        return "O_accumulate"
    if 15 <= hour < 21:
        return "B_accumulate"
    return "AB_integration"


def attractor_loop_path(loop) -> list:
    """Stitch consecutive loop-node pairs into one directed path via _find_path."""
    full = []
    for i in range(len(loop) - 1):
        a, b = loop[i], loop[i + 1]
        p = _find_path(a, b, max_depth=20)
        if p is None:
            continue
        if not full:
            full = list(p)
        else:
            # skip duplicated join node
            full = full + list(p[1:])
    return full


def referenced_8d_for_attractor(attr_name: str) -> dict:
    """Reference 8D = the attractor's sphere constants (physics_tile_engine)."""
    # which sphere owns this attractor
    sphere = None
    for s, info in SPHERES.items():
        if info["attractor"] == attr_name:
            sphere = s
            break
    if sphere is None:
        # fallback: average all sphere constants
        weights = {d: 0.0 for d in DIMS}
        for s in SPHERES:
            prim, sec = SPHERE_CONSTANTS.get(s, ("W7", "OMEGA"))
            wp = get_constant_weights(prim)
            ws = get_constant_weights(sec)
            for d in DIMS:
                weights[d] += 0.5 * wp[d] + 0.5 * ws[d]
        n = len(SPHERES)
        return {d: round(weights[d] / n, 4) for d in DIMS}
    prim, sec = SPHERE_CONSTANTS.get(sphere, ("W7", "OMEGA"))
    wp = get_constant_weights(prim)
    ws = get_constant_weights(sec)
    return {d: round(0.5 * wp[d] + 0.5 * ws[d], 4) for d in DIMS}


def main():
    # node universe (for path existence / energy carrier set)
    nodes = parse_circuit(
        pathlib.Path(__file__).parent.parent / "circuitfile-rewritten.md"
    )
    node_names = set(nodes.keys())

    # build attractor loop paths
    attr_paths = {}
    for name, info in ATTRACTORS.items():
        path = attractor_loop_path(info["loop"])
        attr_paths[name] = path
        missing = [n for n in info["loop"] if n not in node_names]
        info["_missing_nodes"] = missing

    # ---- toroidal state integration ----
    # E[node] in [0,1]; resting baseline = NOR_DEFAULT (absolute_constants)
    E = {n: NOR_DEFAULT for n in node_names}

    # precompute per-phase active sphere + attractor
    def active_sphere_for_phase(phase: str):
        for t in TOROIDAL_TRANSITIONS:
            if t["phase"] == phase:
                return t["to"]  # arrival sphere owns the attractor for that leg
        return "Sun"

    # integration over 24h; collect per-attractor 8D at each hour
    attr_8d_acc = {a: {d: 0.0 for d in DIMS} for a in ATTRACTORS}
    attr_8d_count = {a: 0 for a in ATTRACTORS}

    for h in range(24):
        phase = phase_from_hour(h)
        sphere = active_sphere_for_phase(phase)
        attr_name = SPHERES[sphere]["attractor"]
        info = ATTRACTORS[attr_name]
        path = attr_paths[attr_name]

        is_spark = phase in ("AB_spark", "AB_integration")
        is_reset = phase == "AB_integration"

        # 1. decay everywhere: dE = -lambda * E  (risk-memory decay)
        newE = {n: E[n] * (1.0 - LAMBDA_RISK_DECAY) for n in E}

        # 2. drive along the active attractor loop: dE += M * (incoming energy) * C_coupling
        if path:
            for i in range(len(path) - 1):
                cur, nxt = path[i], path[i + 1]
                drive = E[cur] if cur in E else 0.0
                newE[nxt] = min(1.0, newE.get(nxt, 0.0) + M_RISK_GAIN * drive * C)

        # 3. spark injection at loop start (138.88deg reset)
        if path and is_spark:
            spark = SPARK_MAGNITUDE  # |NEUTRON_TIME_SYNC * e^{i*theta}|
            start = path[0]
            newE[start] = min(1.0, newE.get(start, 0.0) + spark)
            if is_reset:
                # reset closes the manifold: nudge toward OMEGA/10 homeostasis
                target = OMEGA / 10.0  # 0.74
                for n in newE:
                    newE[n] = max(0.0, min(1.0,
                                      newE[n] + 0.10 * (target - newE[n])))

        E = newE

        # 4. record this attractor's instantaneous 8D (energy over its loop -> its dims)
        loop_nodes = [n for n in info["loop"] if n in E]
        if loop_nodes:
            mean_e = sum(E[n] for n in loop_nodes) / len(loop_nodes)
        else:
            mean_e = 0.0
        for d in info["dims"]:
            attr_8d_acc[attr_name][d] += mean_e
        attr_8d_count[attr_name] += 1

    # average attractor 8D
    attr_8d = {}
    for a in ATTRACTORS:
        c = attr_8d_count[a] or 1
        attr_8d[a] = {d: round(attr_8d_acc[a][d] / c, 4) for d in DIMS}

    # ---- deviation vs canonical reference ----
    report = {
        "engine": "energy_circulation attractor-loop integration + absolute_constants",
        "law": "dE/dt = -LAMBDA_RISK_DECAY*E + M_RISK_GAIN*drive*C ; spark=|SPARK_CONSTANT_C| @ 138.88deg ; OMEGA/10 homeostasis",
        "attractors": {},
    }

    attr_dev = {}
    for name, info in ATTRACTORS.items():
        circ = attr_8d[name]
        ref = referenced_8d_for_attractor(name)
        dev = {d: round(abs(circ.get(d, 0.0) - ref[d]), 4) for d in DIMS}
        total = round(sum(dev.values()), 4)
        worst = max(dev, key=dev.get)
        attr_dev[name] = total
        report["attractors"][name] = {
            "dims": info["dims"],
            "sphere": SPHERES and {s: v["attractor"] for s, v in SPHERES.items()}.get(
                [s for s, v in SPHERES.items() if v["attractor"] == name][0]
                if [s for s, v in SPHERES.items() if v["attractor"] == name] else "?",
                "?",
            ),
            "loop": info["loop"],
            "loop_path_len": len(attr_paths[name]),
            "missing_loop_nodes": info.get("_missing_nodes", []),
            "circuit_8d": {d: round(circ.get(d, 0.0), 4) for d in DIMS},
            "reference_8d": ref,
            "deviation": dev,
            "total_deviation": total,
            "worst_dim": worst,
            "worst_dev": dev[worst],
        }

    ranked = sorted(attr_dev.items(), key=lambda kv: kv[1], reverse=True)
    report["attractor_deviation_ranking"] = [
        {"attractor": a, "total_deviation": v} for a, v in ranked
    ]
    overall = round(sum(sum(r["deviation"].values())
                         for r in report["attractors"].values()) / len(ATTRACTORS), 4)
    report["overall_mean_deviation"] = overall
    report["baseline_v1_v2"] = 0.473  # saturated sims, for comparison

    out_json = GEN / "energy_attractor_deviation.json"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = []
    lines.append("=" * 80)
    lines.append("ENERGY CIRCULATION — ATTRACTOR-LOOP INTEGRATION DEVIATION (v3)")
    lines.append("=" * 80)
    lines.append("")
    lines.append("Law: dE/dt = -LAMBDA_RISK_DECAY*E + M_RISK_GAIN*drive*C")
    lines.append(f"     LAMBDA={LAMBDA_RISK_DECAY}  M={M_RISK_GAIN}  C={C:.4f}  "
                 f"spark={SPARK_MAGNITUDE:.4f}@{SPARK_ANGLE_DEG}deg  OMEGA={OMEGA}")
    lines.append("")
    lines.append(f"Overall mean |dev| = {overall:.3f}   (v1/v2 saturated baseline = 0.473)")
    lines.append(f"  -> improvement vs saturated sim: {0.473 - overall:+.3f}")
    lines.append("")
    lines.append("ATTRACTOR RANKING (worst first):")
    for a, v in ranked:
        lines.append(f"  {a:12s} total_dev={v:.3f}")
    lines.append("")
    for name, info in ATTRACTORS.items():
        td = report["attractors"][name]
        lines.append(f"\n■ {name}  (dims={info['dims']})")
        lines.append(f"    loop_path_len={td['loop_path_len']}  missing_nodes={td['missing_loop_nodes']}")
        lines.append(f"    loop: {' -> '.join(info['loop'])}")
        lines.append(f"    circuit : " +
                     ", ".join(f"{d}={td['circuit_8d'][d]:.2f}" for d in DIMS))
        lines.append(f"    ref     : " +
                     ", ".join(f"{d}={td['reference_8d'][d]:.2f}" for d in DIMS))
        lines.append(f"    |dev|   : " +
                     ", ".join(f"{d}={td['deviation'][d]:.2f}" for d in DIMS))
        lines.append(f"    worst dim = {td['worst_dim']} ({td['worst_dev']:.2f}), "
                     f"total = {td['total_deviation']:.3f}")
    text = "\n".join(lines)
    (GEN / "energy_attractor_deviation.txt").write_text(text, encoding="utf-8")

    print(text)
    print(f"\n-> JSON: {out_json}")
    print(f"-> TXT:  {GEN / 'energy_attractor_deviation.txt'}")


if __name__ == "__main__":
    main()
