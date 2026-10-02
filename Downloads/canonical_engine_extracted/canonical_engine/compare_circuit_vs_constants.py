"""Bridge (v2): circuit 8D vs canonical-constant 8D, constant-driven.

Uses circuit_sim_constants.ConstantDrivenSim (copies circuit_sim.py,
adds absolute_constants coupling + sphere-cycle sweep) instead of the
un-physical pure min/max simulator.

Reads circuitfile-rewritten.md UNMODIFIED. Does not touch it.
"""
from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from circuit_sim_constants import (
    parse_circuit, CircuitSimulator as ConstantDrivenSim, compute_8d, NODE_MUSIC_MAP,
)
from physics_tile_engine import (
    TILES, SPHERE_PHASES, compute_tile_parameters_physics, ALL_DIMS,
)

GEN = pathlib.Path(__file__).parent / "generated"
GEN.mkdir(exist_ok=True)

MD = pathlib.Path(__file__).parent.parent / "circuitfile-rewritten.md"


def tile_8d(sim, tile_nodes):
    vec = {d: 0.0 for d in ALL_DIMS}
    for n in tile_nodes:
        if n not in sim.values:
            continue
        chans = NODE_MUSIC_MAP.get(n, {}).get("channels", {})
        for ch, dim in chans.items():
            v = sim.values[n].get(ch, 0.0)
            if v > vec[dim]:
                vec[dim] = v
    return vec


def reference_8d_mean(tile_name):
    refs = {
        sph: compute_tile_parameters_physics(
            tile_name, sph,
            (SPHERE_PHASES[sph][2][0] + SPHERE_PHASES[sph][2][1]) / 2.0,
        )
        for sph in SPHERE_PHASES
    }
    return {
        d: sum(r[d] for r in refs.values()) / len(refs)
        for d in ALL_DIMS
    }


def main():
    print("Parsing + constant-driven simulating (24h toroidal sweep)...")
    nodes = parse_circuit(MD)
    sim = ConstantDrivenSim(nodes)
    print(f"  parsed {len(sim.nodes)} nodes")

    # accumulate per-tile 8D across the 24h sphere cycle
    tile_acc = {t: {d: 0.0 for d in ALL_DIMS} for t in TILES}
    hourly_full = []
    for hour in range(24):
        sim.step(hour=hour)
        for t, info in TILES.items():
            v = tile_8d(sim, info["nodes"])
            for d in ALL_DIMS:
                tile_acc[t][d] += v[d]
        hourly_full.append(compute_8d(sim))
    n = 24.0
    for t in tile_acc:
        for d in ALL_DIMS:
            tile_acc[t][d] /= n
    full_mean = {d: sum(h[d] for h in hourly_full) / n for d in ALL_DIMS}

    report = {
        "dims": ALL_DIMS,
        "engine": "ConstantDrivenSim (couples absolute_constants + sphere cycle)",
        "full_circuit_8d_mean": {d: round(full_mean[d], 4) for d in ALL_DIMS},
        "tiles": {},
    }

    tile_dev = {}
    for tile_name, info in TILES.items():
        circ = tile_acc[tile_name]
        ref = reference_8d_mean(tile_name)
        dev = {d: round(abs(circ[d] - ref[d]), 4) for d in ALL_DIMS}
        total = round(sum(dev.values()), 4)
        worst = max(dev, key=dev.get)
        tile_dev[tile_name] = total
        report["tiles"][tile_name] = {
            "nodes": info["nodes"],
            "primary_constant": info["primary_constant"],
            "secondary_constant": info["secondary_constant"],
            "circuit_8d_mean": {d: round(circ[d], 4) for d in ALL_DIMS},
            "reference_8d_mean": {d: round(ref[d], 4) for d in ALL_DIMS},
            "deviation": dev,
            "total_deviation": total,
            "worst_dim": worst,
            "worst_dev": dev[worst],
        }

    ranked = sorted(tile_dev.items(), key=lambda kv: kv[1], reverse=True)
    report["tile_deviation_ranking"] = [{"tile": t, "total_deviation": v} for t, v in ranked]

    dim_mean = {
        d: round(sum(report["tiles"][t]["deviation"][d] for t in TILES) / len(TILES), 4)
        for d in ALL_DIMS
    }
    report["mean_deviation_per_dim"] = dim_mean
    report["overall_mean_deviation"] = round(sum(dim_mean.values()) / len(ALL_DIMS), 4)

    out_json = GEN / "circuit_vs_constants_deviation_v2.json"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = []
    lines.append("=" * 80)
    lines.append("CIRCUIT 8D  vs  CANONICAL CONSTANT 8D  — DEVIATION REPORT (v2, constant-driven)")
    lines.append("=" * 80)
    lines.append("")
    lines.append("Engine: ConstantDrivenSim (absolute_constants + 24h sphere sweep)")
    lines.append(f"Full-circuit 8D mean: " +
                 ", ".join(f"{d}={full_mean[d]:.2f}" for d in ALL_DIMS))
    lines.append("")
    lines.append(f"Overall mean |dev| = {report['overall_mean_deviation']:.3f} "
                 f"(0.0 = perfect, {0.473:.3f} = previous un-physical sim)")
    lines.append(f"  -> improvement vs v1: {0.473 - report['overall_mean_deviation']:+.3f}")
    lines.append("")
    lines.append("TILE RANKING (worst first):")
    for t, v in ranked:
        lines.append(f"  {t:12s} total_dev={v:.3f}")
    lines.append("")
    lines.append("PER-TILE BREAKDOWN:")
    for tile_name, info in TILES.items():
        td = report["tiles"][tile_name]
        lines.append(f"\n  {tile_name}  ({info['nodes']})")
        lines.append(f"    const: {info['primary_constant']} / {info['secondary_constant']}")
        lines.append(f"    circuit : " +
                     ", ".join(f"{d}={td['circuit_8d_mean'][d]:.2f}" for d in ALL_DIMS))
        lines.append(f"    ref_mean: " +
                     ", ".join(f"{d}={td['reference_8d_mean'][d]:.2f}" for d in ALL_DIMS))
        lines.append(f"    |dev|   : " +
                     ", ".join(f"{d}={td['deviation'][d]:.2f}" for d in ALL_DIMS))
        lines.append(f"    worst dim = {td['worst_dim']} ({td['worst_dev']:.2f}), "
                     f"total = {td['total_deviation']:.3f}")
    text = "\n".join(lines)
    (GEN / "circuit_vs_constants_deviation_v2.txt").write_text(text, encoding="utf-8")

    print(text)
    print(f"\n-> JSON: {out_json}")
    print(f"-> TXT:  {GEN / 'circuit_vs_constants_deviation_v2.txt'}")


if __name__ == "__main__":
    main()
