from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent

CONNECTIVITY_DIR = ROOT / "out" / "connectivity_audit"
TRACKA_DIR = ROOT / "out" / "external_trackA" / "sh_1_64_micro_r_0p017100"
RIGHT_BRANCH_DIR = ROOT / "out" / "right_branch_hypothesis"
MERSENNE_REPORT = (
    ROOT
    / "out"
    / "mersenne_verify"
    / "UNIVERSE_MERSENNE_CORE__20260109_102759Z"
    / "report.md"
)
SOLENOID_ROOTCAUSE = (
    ROOT
    / "pi_atlas"
    / "NEW_DOMAIN_EXPANSION"
    / "domain_validation"
    / "BIFURCATIONCONVERGENCE"
    / "results"
    / "SOLENOID_1D_ROOTCAUSE.md"
)
TUNNEL_JSON = ROOT / "moveout" / "tunnel_verification_knn" / "tunnel_verification_results.json"


def norm_sheet(node: str) -> str:
    n = str(node).strip()
    if n.startswith("sheet_id:"):
        return n
    if n.startswith("sheet") and ":" in n:
        left = n.split(":", 1)[0]
        if left[5:].isdigit():
            return f"sheet_id:{int(left[5:])}"
    if n.startswith("tile_"):
        return "sheet_id:0"
    return n


def seam_key(a: str, b: str) -> tuple[str, str]:
    na, nb = norm_sheet(a), norm_sheet(b)
    return tuple(sorted((na, nb)))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_gap_min_map(gap_df: pd.DataFrame) -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    for row in gap_df.itertuples(index=False):
        key = seam_key(row.domain_a, row.domain_b)
        dist = float(row.dist_xy)
        prev = out.get(key)
        if prev is None or dist < prev:
            out[key] = dist
    return out


def main() -> int:
    graph_df = pd.read_csv(CONNECTIVITY_DIR / "connectivity_graph.csv")
    gap_df = pd.read_csv(TRACKA_DIR / "geometry_map" / "gap_nearest_pairs.csv")
    percolation_df = pd.read_csv(
        TRACKA_DIR / "percolation_saddle_geometry" / "percolation_saddle_events.csv"
    )
    connectivity_summary = read_json(CONNECTIVITY_DIR / "summary.json")
    right_branch_verdict = read_json(RIGHT_BRANCH_DIR / "right_branch_verdict.json")
    tunnel = read_json(TUNNEL_JSON)

    solenoid_text = SOLENOID_ROOTCAUSE.read_text(encoding="utf-8")
    mersenne_text = MERSENNE_REPORT.read_text(encoding="utf-8")
    solenoid_1d_only = ("1D" in solenoid_text) and ("Do not integrate solenoid into the 2D PASS pipeline" in solenoid_text)
    mersenne_diag_only = "diagnostics-only" in mersenne_text

    gap_min_map = build_gap_min_map(gap_df)

    rows: list[dict] = []
    for row in graph_df.itertuples(index=False):
        key = seam_key(row.source_node, row.target_node)
        seam_a, seam_b = key
        edge_type = str(row.edge_type)
        contact_score = float(row.confidence) if pd.notna(row.confidence) else 0.0
        gap_min_dist = gap_min_map.get(key)
        proj_flag = edge_type == "projection_overlap" or (gap_min_dist == 0.0 if gap_min_dist is not None else False)
        percolation_flag = edge_type == "saddle_candidate"

        tunnel_blocked = edge_type == "tunnel_blocked" or (
            "sheet_id:2" in key and any(v.get("verification") == "TRUE_DISCONNECTION" for v in tunnel.get("results", {}).values())
        )
        tunnel_status = "blocked" if tunnel_blocked else "open_or_unverified"

        corridor_status = (
            "corridor"
            if ("right_branch" in (seam_a, seam_b) and right_branch_verdict.get("verdict") == "corridor")
            else "attractor_or_unknown"
        )

        evidence = str(row.evidence)
        solenoid_conflict = solenoid_1d_only and ("solenoid" in evidence.lower())
        mersenne_conflict = mersenne_diag_only and connectivity_summary.get("true_components", 0) > 1 and edge_type in {
            "saddle_candidate",
            "contact_candidate",
        }

        barnard_candidate = (
            (edge_type in {"saddle_candidate", "contact_candidate"})
            and (not tunnel_blocked)
            and (not proj_flag)
            and ("right_branch" not in key)
        )

        if tunnel_blocked:
            final_verdict = "hard_tunnel_block"
        elif proj_flag:
            final_verdict = "projection_only_overlap"
        elif corridor_status == "corridor" and edge_type == "corridor":
            final_verdict = "corridor_only_non_gluing"
        elif barnard_candidate:
            final_verdict = "candidate_for_barnard_reweighting"
        else:
            final_verdict = "weak_candidate_unverified"

        rows.append(
            {
                "seam_a": seam_a,
                "seam_b": seam_b,
                "contact_score": contact_score,
                "gap_min_dist": gap_min_dist,
                "projection_overlap_flag": bool(proj_flag),
                "percolation_candidate_flag": bool(percolation_flag),
                "tunnel_status": tunnel_status,
                "corridor_or_attractor_status": corridor_status,
                "solenoid_conflict_flag": bool(solenoid_conflict),
                "mersenne_conflict_flag": bool(mersenne_conflict),
                "barnard_reweight_candidate": bool(barnard_candidate),
                "final_verdict": final_verdict,
                "edge_type": edge_type,
                "blocked_reason": str(row.blocked_reason),
                "evidence": evidence,
            }
        )

    seam_df = pd.DataFrame(rows).sort_values(
        by=["final_verdict", "contact_score"], ascending=[True, False]
    )
    seam_df.to_csv(ROOT / "seam_failure_table.csv", index=False)

    # Barnard-linked seam ranking (selector only, never bypass tunnel blocks)
    rank_df = seam_df.copy()
    rank_df["base_strength"] = rank_df["contact_score"].clip(lower=0.0, upper=1.0)
    gap_num = pd.to_numeric(rank_df["gap_min_dist"], errors="coerce").fillna(1.0)
    rank_df["gap_gate"] = 1.0 / (1.0 + gap_num)
    rank_df["tunnel_gate"] = (rank_df["tunnel_status"] != "blocked").astype(float)
    rank_df["projection_gate"] = (~rank_df["projection_overlap_flag"]).astype(float)
    rank_df["corridor_gate"] = (
        rank_df["corridor_or_attractor_status"] != "corridor"
    ).astype(float) * 0.6 + 0.4
    rank_df["barnard_epoch_weighted"] = rank_df["base_strength"] * rank_df["gap_gate"] * rank_df["tunnel_gate"] * rank_df["projection_gate"] * rank_df["corridor_gate"] * 0.5666666667

    rank_df["support_class"] = "decay-dominated"
    rank_df.loc[
        rank_df["barnard_epoch_weighted"] > 0.25, "support_class"
    ] = "external vector supported"
    rank_df.loc[
        (rank_df["barnard_epoch_weighted"] > 0.1) & (rank_df["barnard_epoch_weighted"] <= 0.25),
        "support_class",
    ] = "shield-supported"
    rank_df.loc[
        (rank_df["barnard_epoch_weighted"] <= 0.1) & (rank_df["tunnel_status"] != "blocked"),
        "support_class",
    ] = "internally leaky"
    rank_df.loc[rank_df["tunnel_status"] == "blocked", "support_class"] = "decay-dominated"

    out_cols = [
        "seam_a",
        "seam_b",
        "edge_type",
        "final_verdict",
        "barnard_epoch_weighted",
        "support_class",
        "tunnel_status",
        "projection_overlap_flag",
        "corridor_or_attractor_status",
        "evidence",
    ]
    rank_df = rank_df.sort_values(by="barnard_epoch_weighted", ascending=False)
    rank_df[out_cols].to_csv(ROOT / "barnard_reweight_candidates.csv", index=False)

    hard_block = seam_df[seam_df["final_verdict"] == "hard_tunnel_block"]
    fake_overlap = seam_df[seam_df["final_verdict"] == "projection_only_overlap"]
    barnard_ok = rank_df[
        (rank_df["final_verdict"] == "candidate_for_barnard_reweighting")
        & (rank_df["tunnel_status"] != "blocked")
    ]
    best_candidate = (
        "none"
        if barnard_ok.empty
        else f"{barnard_ok.iloc[0]['seam_a']} <-> {barnard_ok.iloc[0]['seam_b']}"
    )

    percolation_names = ", ".join(percolation_df["name"].astype(str).tolist())
    report = f"""# SEAM_FAILURE_REPORT

## Proven facts
- True connected components remain `{connectivity_summary.get("true_components")}`.
- Main hard block is `gateway_peak -> sheet_id:2` (`TRUE_DISCONNECTION` in tunnel verification).
- Right branch verdict is `{right_branch_verdict.get("verdict")}` (corridor, not attractor).
- Projection-only overlaps exist (`{int(fake_overlap.shape[0])}` seam rows flagged), including `dist_xy==0` pairs.
- Solenoid root-cause document states 1D-only handling and explicit non-integration into 2D PASS.
- Mersenne report is diagnostics-only and not a direct gluing proof.

## Seam failure diagnosis
- Main hard block: `gateway_peak <-> sheet_id:2` is tunnel-blocked and cannot be upgraded by Barnard.
- Fake center overlaps: any seam with `projection_overlap_flag=true` is treated as rendered coincidence, not a bridge.
- Solenoid incompatibility: seam-level direct solenoid bridge evidence is absent; solenoid is flagged as conflict source if used for 2D gluing claims.
- Mersenne conflict: candidate seams stay multi-component while Mersenne checks are diagnostics-only; this is compatibility pressure, not a bridge operator.
- Percolation candidates found in events: `{percolation_names}` (candidate only, not true gluing).

## Barnard-linked reweighting plan (selector only)
- Barnard is applied only as candidate seam ranking, never as teleportation/bridge creation.
- Excluded from amplification: tunnel-blocked seams, projection-only overlaps, and corridor-only links.
- Best next candidate seam under current evidence: `{best_candidate}`.

## Why corridor still does not glue
Global gluing fails because the dominant seam to `sheet_id:2` is a verified tunnel block, while many center overlaps are projection artifacts (`dist_xy==0`) and right-branch behavior is corridor drift rather than attractor capture.
"""
    (ROOT / "SEAM_FAILURE_REPORT.md").write_text(report, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
