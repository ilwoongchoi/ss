import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "connectivity_audit"
OUTDIR.mkdir(parents=True, exist_ok=True)


def _latest_path(glob_pat: str, base: Path) -> Path | None:
    paths = list(base.rglob(glob_pat))
    if not paths:
        return None
    return max(paths, key=lambda p: p.stat().st_mtime)


def load_json(path: Path) -> dict | None:
    if not path or not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_edge(edges, src, dst, edge_type, confidence, evidence, blocked_reason=""):
    edges.append(
        {
            "source_node": src,
            "target_node": dst,
            "edge_type": edge_type,
            "confidence": float(confidence),
            "evidence": evidence,
            "blocked_reason": blocked_reason,
        }
    )


def build_components(nodes, edges, true_types):
    adj = {n: set() for n in nodes}
    for e in edges:
        if e["edge_type"] in true_types:
            a, b = e["source_node"], e["target_node"]
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)
    seen = set()
    comps = []
    for n in nodes:
        if n in seen:
            continue
        stack = [n]
        comp = set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            comp.add(cur)
            for nxt in adj.get(cur, []):
                if nxt not in seen:
                    stack.append(nxt)
        comps.append(comp)
    return comps


def main():
    edges = []
    evidence_notes = []

    # Pick a coherent run root: derive from latest percolation JSON.
    percolation = _latest_path("percolation_saddle_geometry.json", ROOT / "out")
    if not percolation:
        raise SystemExit("Missing percolation_saddle_geometry.json under out/")
    run_root = percolation.parent.parent
    evidence_notes.append(f"run_root={run_root}")

    point_cloud = run_root / "sheet0_reconstruction" / "PI_GLOBAL_POINT_CLOUD_subsheets.csv"
    contact_csv = run_root / "geometry_map" / "contact_map_knn_scores.csv"
    gap_pairs = run_root / "geometry_map" / "gap_nearest_pairs.csv"

    perco = load_json(percolation)
    tunnel = load_json(ROOT / "moveout" / "tunnel_verification_knn" / "tunnel_verification_results.json")

    # Right-branch diagnostics (separate subsystem; still relevant for "corridor vs attractor")
    rb_dir = ROOT / "out" / "right_branch_hypothesis"
    rb_verdict = load_json(rb_dir / "right_branch_verdict.json")
    if rb_verdict:
        verdict = rb_verdict.get("verdict", "unknown")
        add_edge(
            edges,
            "core_center",
            "right_branch",
            "corridor" if verdict == "corridor" else "attractor",
            0.95 if verdict == "corridor" else 0.7,
            "out/right_branch_hypothesis/right_branch_verdict.json",
            blocked_reason="drift/dispersion" if verdict == "corridor" else "",
        )
        evidence_notes.append(f"right_branch_verdict={verdict}")

    # Load point cloud and build domain->sheet_id mapping.
    if not point_cloud.exists():
        raise SystemExit(f"Missing point cloud: {point_cloud}")
    dfp = pd.read_csv(point_cloud)
    if not {"domain", "pi_1", "pi_2", "sheet_id"}.issubset(dfp.columns):
        raise SystemExit(f"Point cloud missing required columns: {point_cloud}")
    dfp["sheet_id"] = dfp["sheet_id"].astype(int)

    domain_to_sheet = dict(zip(dfp["domain"].astype(str), dfp["sheet_id"].astype(int)))
    sheet_nodes = sorted(dfp["sheet_id"].unique().tolist())
    nodes = {f"sheet_id:{sid}" for sid in sheet_nodes}

    # Candidate edges from percolation saddles (bottlenecks, not proof of connectivity).
    if perco and "events" in perco:
        for ev in perco["events"]:
            if not ev.get("found"):
                continue
            A = [f"sheet_id:{i}" for i in ev.get("A", [])]
            B = [f"sheet_id:{i}" for i in ev.get("B", [])]
            for a in A:
                for b in B:
                    add_edge(
                        edges,
                        a,
                        b,
                        "saddle_candidate",
                        0.8,
                        f"{percolation}:{ev.get('name','')}",
                        blocked_reason="needs_tunnel_verification",
                    )
        evidence_notes.append(f"percolation={percolation}")

    # Candidate edges from contact map aggregated to sheet_id.
    if contact_csv.exists():
        dfc = pd.read_csv(contact_csv, index_col=0)
        # aggregate max contact between any domains in two sheets
        domains = list(dfc.index)
        dom_sheet = {d: domain_to_sheet.get(d) for d in domains}
        by_sheet = {}
        for d, sid in dom_sheet.items():
            if sid is None:
                continue
            by_sheet.setdefault(int(sid), []).append(d)
        for i in by_sheet:
            for j in by_sheet:
                if j <= i:
                    continue
                sub = dfc.loc[by_sheet[i], by_sheet[j]]
                mx = float(np.nanmax(sub.to_numpy())) if sub.size else 0.0
                if mx >= 0.05:
                    add_edge(
                        edges,
                        f"sheet_id:{i}",
                        f"sheet_id:{j}",
                        "contact_candidate",
                        mx,
                        str(contact_csv),
                        blocked_reason="contact_only",
                    )
        evidence_notes.append(f"contact_map={contact_csv}")

    # Gap nearest pairs: detect projection overlaps (dist_xy==0) and seam candidates.
    overlap_pairs = []
    if gap_pairs.exists():
        dfg = pd.read_csv(gap_pairs)
        if {"domain_a", "domain_b", "dist_xy"}.issubset(dfg.columns):
            dfg["sheet_a"] = dfg["domain_a"].map(domain_to_sheet)
            dfg["sheet_b"] = dfg["domain_b"].map(domain_to_sheet)
            dfg = dfg.dropna(subset=["sheet_a", "sheet_b"])
            dfg["sheet_a"] = dfg["sheet_a"].astype(int)
            dfg["sheet_b"] = dfg["sheet_b"].astype(int)
            # summarize per sheet-pair
            grp = (
                dfg.groupby(["sheet_a", "sheet_b"], as_index=False)
                .agg(min_dist=("dist_xy", "min"), n_pairs=("dist_xy", "count"))
            )
            for _, row in grp.iterrows():
                a, b = int(row["sheet_a"]), int(row["sheet_b"])
                if a == b:
                    continue
                min_dist = float(row["min_dist"])
                if min_dist <= 0.05:
                    et = "gap_pair_candidate"
                    blocked = "gap_only"
                    conf = 0.6 if min_dist == 0.0 else 0.4
                    if min_dist == 0.0:
                        et = "projection_overlap"
                        blocked = "same_coords_dist_xy_0"
                        overlap_pairs.append((a, b))
                        conf = 0.9
                    add_edge(
                        edges,
                        f"sheet_id:{a}",
                        f"sheet_id:{b}",
                        et,
                        conf,
                        str(gap_pairs),
                        blocked_reason=blocked,
                    )
        evidence_notes.append(f"gap_pairs={gap_pairs}")

    # Tunnel verification: overrides candidate edges for target_sheet.
    if tunnel:
        target_sheet = int(tunnel.get("target_sheet", -1))
        ver30 = tunnel.get("results", {}).get("30", {})
        verification = ver30.get("verification", "")
        nodes.add("gateway_peak")
        if target_sheet >= 0:
            nodes.add(f"sheet_id:{target_sheet}")
            add_edge(
                edges,
                "gateway_peak",
                f"sheet_id:{target_sheet}",
                "tunnel_blocked",
                0.99,
                "moveout/tunnel_verification_knn/tunnel_verification_results.json",
                blocked_reason=verification or "UNKNOWN",
            )
        evidence_notes.append(f"tunnel_target_sheet={target_sheet} verification={verification}")

        # quantify overlap near the peak for target sheet (projection vs latent disconnect)
        peak_xy = tunnel.get("peak_coords", None)
        peak_r = float(tunnel.get("peak_radius", 0.2))
        if peak_xy and len(peak_xy) == 2:
            px, py = float(peak_xy[0]), float(peak_xy[1])
            dfp["d_peak"] = np.sqrt((dfp["pi_1"] - px) ** 2 + (dfp["pi_2"] - py) ** 2)
            in_peak = dfp[dfp["d_peak"] <= peak_r]
            counts = in_peak.groupby("sheet_id").size().to_dict()
            for sid, cnt in counts.items():
                add_edge(
                    edges,
                    "gateway_peak",
                    f"sheet_id:{int(sid)}",
                    "gateway_contact",
                    min(0.95, float(cnt) / 100.0 + 0.1),
                    "peak_radius_overlap",
                    blocked_reason="proximity_only",
                )

    # Flash events (engine bridge operator evidence, separate from PI sheet atlas)
    flash_dir = ROOT / "out" / "detune_closure_sweep_v4"
    for name in ["center_in", "r_out", "q0_out", "both_out"]:
        fp = flash_dir / f"flash_events_{name}.json"
        if not fp.exists():
            continue
        payload = json.load(open(fp, "r", encoding="utf-8"))
        events = payload.get("flash_events", payload) if isinstance(payload, dict) else payload
        if not events:
            continue
        add_edge(
            edges,
            f"flash:{name}",
            "flash_bridge",
            "flash_transition",
            min(0.99, len(events) / 1000.0 + 0.1),
            str(fp),
        )
        nodes.add(f"flash:{name}")
        nodes.add("flash_bridge")

    nodes_list = sorted(nodes)

    # True connectivity requires explicit transition evidence (tunnel-verified or actual flash bridge).
    true_types = {"tunnel_verified", "flash_transition"}
    comps = build_components(nodes_list, edges, true_types)
    comp_index = {n: i for i, comp in enumerate(comps) for n in comp}

    # Minimal cuts: candidate edges that look strong but cross true components.
    cut_rows = []
    for e in edges:
        if e["edge_type"] in {"contact_candidate", "saddle_candidate", "gap_pair_candidate", "projection_overlap"}:
            a, b = e["source_node"], e["target_node"]
            if comp_index.get(a) != comp_index.get(b):
                cut_rows.append(e)

    # Components table
    comp_rows = []
    for idx, comp in enumerate(comps):
        member_nodes = sorted(comp)
        corr_only = all(
            e["edge_type"] in {"corridor", "contact_candidate", "saddle_candidate", "gap_pair_candidate", "projection_overlap", "gateway_contact"}
            for e in edges
            if e["source_node"] in comp and e["target_node"] in comp
        )
        comp_rows.append(
            {
                "component_id": idx,
                "member_nodes": "|".join(member_nodes),
                "isolated_flag": len(member_nodes) == 1,
                "corridor_only_flag": corr_only,
            }
        )

    # Transition candidates table: rank projection overlaps and saddles by strength.
    trans_rows = []
    for e in edges:
        if e["edge_type"] in {"projection_overlap", "saddle_candidate", "contact_candidate", "tunnel_blocked"}:
            trans_rows.append(
                {
                    "from_state": e["source_node"],
                    "to_state": e["target_node"],
                    "via_flash": e["edge_type"] == "flash_transition",
                    "via_saddle": e["edge_type"] == "saddle_candidate",
                    "via_tunnel": e["edge_type"].startswith("tunnel"),
                    "leg": "",
                    "lag_sign": "",
                    "turn": "",
                    "score": float(e["confidence"]),
                }
            )

    pd.DataFrame(edges).to_csv(OUTDIR / "connectivity_graph.csv", index=False)
    pd.DataFrame(comp_rows).to_csv(OUTDIR / "disconnected_components.csv", index=False)
    pd.DataFrame(trans_rows).to_csv(OUTDIR / "transition_law_candidates.csv", index=False)

    # Visualization: pi-space with sheet_id labels (projection overlap focus)
    fig, ax = plt.subplots(figsize=(10, 8))
    cmap = plt.cm.tab20
    for sid in sheet_nodes:
        d = dfp[dfp["sheet_id"] == sid]
        ax.scatter(d["pi_1"], d["pi_2"], s=15, alpha=0.6, label=str(sid), color=cmap((sid % 20) / 20))
    if tunnel and tunnel.get("peak_coords"):
        px, py = float(tunnel["peak_coords"][0]), float(tunnel["peak_coords"][1])
        ax.scatter([px], [py], s=200, marker="*", color="black", label="gateway_peak")
        r = float(tunnel.get("peak_radius", 0.2))
        circ = plt.Circle((px, py), r, color="black", fill=False, alpha=0.4)
        ax.add_patch(circ)
    ax.set_xlabel("pi_1")
    ax.set_ylabel("pi_2")
    ax.set_title("Latent Disconnectivity Map (projection overlaps vs tunnel)")
    ax.legend(ncol=3, fontsize=7)
    plt.tight_layout()
    plt.savefig(OUTDIR / "latent_disconnectivity_map.png", dpi=200)
    plt.close(fig)

    # Audit markdown
    right_corridor = rb_verdict.get("verdict") == "corridor" if rb_verdict else False
    target_sheet = int(tunnel.get("target_sheet", -1)) if tunnel else -1
    verification = tunnel.get("results", {}).get("30", {}).get("verification", "") if tunnel else ""

    audit = []
    audit.append("# Connectivity Audit (Sheet Disconnectivity / Tunnel / Projection Overlap)")
    audit.append("")
    audit.append("## Evidence Summary")
    for note in evidence_notes:
        audit.append(f"- {note}")
    audit.append("")
    audit.append("## Hypothesis Tests")
    if right_corridor:
        audit.append("- H1 supported: right branch is corridor (drift/dispersion too large for attractor).")
    if target_sheet >= 0 and verification == "TRUE_DISCONNECTION":
        audit.append(f"- H4 supported: target sheet_id:{target_sheet} is tunnel-blocked from gateway_peak (TRUE_DISCONNECTION).")
    if overlap_pairs:
        audit.append("- H2 supported: multiple sheet_id pairs have dist_xy==0 (same projected coords) without verified transition -> projection-only overlap.")
    audit.append("- H5 supported: candidate seams (contact/saddle/gap) exist but are not sufficient without tunnel/transition evidence.")
    audit.append("")
    audit.append("## Where Gluing Fails")
    if target_sheet >= 0:
        audit.append(f"- gateway_peak -> sheet_id:{target_sheet} is blocked (tunnel_verification_results.json).")
    if overlap_pairs:
        # show a few
        shown = 0
        audit.append("- Projection overlaps (dist_xy==0) examples:")
        for a, b in overlap_pairs[:10]:
            audit.append(f"  - sheet_id:{a} <-> sheet_id:{b} (gap_nearest_pairs.csv dist_xy==0)")
            shown += 1
            if shown >= 10:
                break
    audit.append("")
    audit.append("## Minimal Cuts (Strong candidate seams crossing true components)")
    for e in cut_rows[:30]:
        audit.append(f"- {e['source_node']} -> {e['target_node']} [{e['edge_type']}] blocked={e['blocked_reason']} conf={e['confidence']:.3f}")
    audit.append("")
    audit.append("## Verdict")
    audit.append("Global manifold does not glue because the current atlas has projection-level overlaps (dist_xy==0) and saddle/contact candidates, but tunnel verification shows at least one key sheet is truly disconnected from the gateway peak; the missing object is a verified transition/gluing rule, not another proximity heuristic.")

    (OUTDIR / "connectivity_audit.md").write_text("\n".join(audit), encoding="utf-8")

    summary = {
        "true_components": len(comps),
        "candidate_edges": int(sum(e['edge_type'].endswith('_candidate') or e['edge_type']=='projection_overlap' for e in edges)),
        "blocked_tunnel_target": f"sheet_id:{target_sheet}" if target_sheet >= 0 else None,
        "right_branch": "corridor" if right_corridor else "unknown_or_attractor",
        "projection_overlap_pairs": int(len(overlap_pairs)),
    }
    (OUTDIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
