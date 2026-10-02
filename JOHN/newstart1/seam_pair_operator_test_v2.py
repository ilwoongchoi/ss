from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "seam_pair_operator_test_v2"


def norm_node(x: str) -> str:
    s = str(x).strip()
    if s.startswith("sheet_id:"):
        return s
    if s.startswith("sheet") and ":" in s:
        head = s.split(":", 1)[0]
        if head[5:].isdigit():
            return f"sheet_id:{int(head[5:])}"
    if s.startswith("tile_"):
        return "sheet_id:0"
    return s


def pair_key(a: str, b: str) -> tuple[str, str]:
    na, nb = norm_node(a), norm_node(b)
    return tuple(sorted((na, nb)))


def pair_id(a: str, b: str) -> str:
    p = pair_key(a, b)
    return f"{p[0]}__{p[1]}"


def domain_to_sheet(domain: str) -> str:
    d = str(domain)
    if d.startswith("sheet") and ":" in d:
        left = d.split(":", 1)[0]
        if left[5:].isdigit():
            return f"sheet_id:{int(left[5:])}"
    if d.startswith("tile_"):
        return "sheet_id:0"
    return norm_node(d)


@dataclass
class DSU:
    parent: dict[str, str]

    @classmethod
    def from_nodes(cls, nodes: list[str]) -> "DSU":
        return cls(parent={n: n for n in nodes})

    def find(self, x: str) -> str:
        p = self.parent.get(x, x)
        if p != x:
            self.parent[x] = self.find(p)
        return self.parent.get(x, x)

    def union(self, a: str, b: str) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[rb] = ra
        return True

    def components(self) -> int:
        return len({self.find(x) for x in self.parent})


def load_contact_pair_scores(path: Path) -> dict[tuple[str, str], float]:
    # Matrix-style CSV: first column is row domain, remaining are domain columns
    df = pd.read_csv(path)
    if df.empty:
        return {}

    row_col = df.columns[0]
    col_domains = list(df.columns[1:])
    out: dict[tuple[str, str], float] = {}
    for _, row in df.iterrows():
        ra = row[row_col]
        sa = domain_to_sheet(ra)
        for cb in col_domains:
            v = row[cb]
            if pd.isna(v):
                continue
            val = float(v)
            if val <= 0.0:
                continue
            sb = domain_to_sheet(cb)
            if sa == sb:
                continue
            k = pair_key(sa, sb)
            prev = out.get(k, 0.0)
            if val > prev:
                out[k] = val
    return out


def load_percolation_pair_support(path: Path) -> dict[tuple[str, str], float]:
    d = json.loads(path.read_text(encoding="utf-8"))
    out: dict[tuple[str, str], float] = {}
    for ev in d.get("events", []):
        if not ev.get("found", False):
            continue
        a_list = [f"sheet_id:{int(x)}" for x in ev.get("A", [])]
        b_list = [f"sheet_id:{int(x)}" for x in ev.get("B", [])]
        f_star = float(ev.get("F_star", 0.0))
        strength = 1.0 / (1.0 + max(f_star, 0.0))
        for a in a_list:
            for b in b_list:
                if a == b:
                    continue
                k = pair_key(a, b)
                out[k] = max(out.get(k, 0.0), strength)
    return out


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    seam = pd.read_csv(ROOT / "seam_failure_table.csv")
    comps = pd.read_csv(ROOT / "out" / "connectivity_audit" / "disconnected_components.csv")
    gap = pd.read_csv(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "geometry_map"
        / "gap_nearest_pairs.csv"
    )
    contact_scores = load_contact_pair_scores(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "geometry_map"
        / "contact_map_knn_scores.csv"
    )
    percolation_support = load_percolation_pair_support(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "percolation_saddle_geometry"
        / "percolation_saddle_geometry.json"
    )

    seam["pair"] = seam.apply(lambda r: pair_id(r["seam_a"], r["seam_b"]), axis=1)
    seam["pa"] = seam.apply(lambda r: pair_key(r["seam_a"], r["seam_b"])[0], axis=1)
    seam["pb"] = seam.apply(lambda r: pair_key(r["seam_a"], r["seam_b"])[1], axis=1)

    # Additional projection exclusion from gap dist==0 (exclusion only)
    gap_proj_pairs: set[str] = set()
    for g in gap.itertuples(index=False):
        if float(g.dist_xy) == 0.0:
            gap_proj_pairs.add(pair_id(domain_to_sheet(g.domain_a), domain_to_sheet(g.domain_b)))

    # Pair-level contamination bans
    banned_rows = []
    pair_groups = seam.groupby("pair", sort=False)
    for pid, g in pair_groups:
        any_proj = bool(
            (g["projection_overlap_flag"] == True).any()  # noqa: E712
            or (g["final_verdict"] == "projection_only_overlap").any()
            or (pid in gap_proj_pairs)
        )
        any_blocked = bool((g["tunnel_status"] == "blocked").any())
        has_sheet2 = bool((g["pa"] == "sheet_id:2").any() or (g["pb"] == "sheet_id:2").any())
        if any_proj or any_blocked or has_sheet2:
            reason = []
            if any_proj:
                reason.append("projection_contaminated")
            if any_blocked:
                reason.append("tunnel_blocked")
            if has_sheet2:
                reason.append("sheet_id:2_ban")
            banned_rows.append(
                {
                    "pair": pid,
                    "seam_a": g["pa"].iloc[0],
                    "seam_b": g["pb"].iloc[0],
                    "ban_reason": "|".join(reason),
                }
            )

    banned_df = pd.DataFrame(banned_rows).drop_duplicates(subset=["pair"])
    banned_pairs = set(banned_df["pair"].tolist())
    banned_df.to_csv(OUTDIR / "contaminated_pairs_removed.csv", index=False)

    clean = seam[
        (~seam["pair"].isin(banned_pairs))
        & (seam["final_verdict"] == "candidate_for_barnard_reweighting")
        & (seam["tunnel_status"] != "blocked")
        & (seam["projection_overlap_flag"] == False)  # noqa: E712
    ].copy()

    # Pair-level aggregation and ranking with evidence priority
    agg = (
        clean.groupby(["pair", "pa", "pb"], as_index=False)
        .agg(
            contact_score=("contact_score", "max"),
            percolation_candidate_flag=("percolation_candidate_flag", "max"),
            barnard_reweight_candidate=("barnard_reweight_candidate", "max"),
            mersenne_conflict_flag=("mersenne_conflict_flag", "max"),
            has_saddle=("edge_type", lambda s: bool((s == "saddle_candidate").any())),
            has_contact=("edge_type", lambda s: bool((s == "contact_candidate").any())),
        )
    )
    if agg.empty:
        raise RuntimeError("No clean candidate pairs after strict pair-level banning.")

    c = pd.to_numeric(agg["contact_score"], errors="coerce").fillna(0.0)
    if c.max() > c.min():
        c_norm = (c - c.min()) / (c.max() - c.min())
    else:
        c_norm = pd.Series(np.ones(len(c)), index=c.index)
    agg["rank_score"] = (
        0.45 * c_norm
        + 0.35 * agg["percolation_candidate_flag"].astype(float)
        + 0.20 * agg["barnard_reweight_candidate"].astype(float)
        - 0.50 * agg["mersenne_conflict_flag"].astype(float)
    )
    # evidence order: saddle > contact > else
    agg["evidence_priority"] = np.where(agg["has_saddle"], 2, np.where(agg["has_contact"], 1, 0))
    agg = agg.sort_values(["evidence_priority", "rank_score"], ascending=[False, False]).head(10).copy()

    # Local-path verification (no DSU-only shortcut)
    # Positive evidence: contact_map + percolation
    # Exclusion evidence: gap dist==0 only
    verified = []
    failed = []
    for r in agg.itertuples(index=False):
        k = pair_key(r.pa, r.pb)
        local_contact = float(contact_scores.get(k, 0.0))
        local_saddle = float(percolation_support.get(k, 0.0))

        # Barnard is selector-only bounded [0.9,1.1]
        barnard_weight = 1.05 if bool(r.barnard_reweight_candidate) else 1.0
        barnard_weight = float(np.clip(barnard_weight, 0.9, 1.1))

        effective_score = (0.6 * local_contact + 0.4 * local_saddle) * barnard_weight

        is_verified = (local_contact > 0.0) and (local_saddle > 0.0) and (effective_score > 0.05)
        rec = {
            "pair": r.pair,
            "seam_a": r.pa,
            "seam_b": r.pb,
            "rank_score": float(r.rank_score),
            "local_contact_score": local_contact,
            "local_saddle_score": local_saddle,
            "barnard_weight": barnard_weight,
            "effective_local_path_score": effective_score,
            "verified": bool(is_verified),
            "failure_reason": "" if is_verified else "missing_non_projection_local_path",
        }
        if is_verified:
            verified.append(rec)
        else:
            failed.append(rec)

    verified_df = pd.DataFrame(verified)
    failed_df = pd.DataFrame(failed)

    # Component reduction from truly verified local-path seams
    groups = [str(x).split("|") for x in comps["member_nodes"].astype(str)]
    nodes = sorted({n.strip() for g in groups for n in g if n.strip()})
    dsu = DSU.from_nodes(nodes)
    for g in groups:
        g = [x.strip() for x in g if x.strip()]
        if len(g) > 1:
            root = g[0]
            for n in g[1:]:
                dsu.union(root, n)
    before = dsu.components()
    applied = 0
    for r in verified:
        a, b = r["seam_a"], r["seam_b"]
        if a not in dsu.parent:
            dsu.parent[a] = a
        if b not in dsu.parent:
            dsu.parent[b] = b
        if dsu.union(a, b):
            applied += 1
    after = dsu.components()

    # Invalidate previously verified (v1) by pair-level contamination
    v1_path = ROOT / "out" / "seam_pair_operator_test" / "verified_gluing_edges.csv"
    invalidated: list[str] = []
    if v1_path.exists():
        v1 = pd.read_csv(v1_path)
        for x in v1.itertuples(index=False):
            pid = pair_id(x.seam_a, x.seam_b)
            if pid in banned_pairs:
                invalidated.append(f"{pair_key(x.seam_a, x.seam_b)[0]} <-> {pair_key(x.seam_a, x.seam_b)[1]}")
    invalidated = sorted(set(invalidated))

    # cleanest hub / sheet10 vs sheet1 verdict
    clean_hub = "none"
    sheet10_count = 0
    sheet1_count = 0
    if not verified_df.empty:
        cnt: dict[str, int] = {}
        for x in verified_df.itertuples(index=False):
            cnt[x.seam_a] = cnt.get(x.seam_a, 0) + 1
            cnt[x.seam_b] = cnt.get(x.seam_b, 0) + 1
        clean_hub = max(cnt, key=cnt.get)
        sheet10_count = cnt.get("sheet_id:10", 0)
        sheet1_count = cnt.get("sheet_id:1", 0)

    agg.to_csv(OUTDIR / "clean_pair_candidates.csv", index=False)
    verified_df.to_csv(OUTDIR / "local_path_verified_edges.csv", index=False)
    failed_df.to_csv(OUTDIR / "local_path_failed_edges.csv", index=False)

    summary = {
        "true_components_before": int(before),
        "true_components_after_local_path_verification": int(after),
        "component_reduction": int(before - after),
        "applied_verified_edges": int(applied),
        "clean_candidate_pairs": int(len(agg)),
        "contaminated_pairs_removed": int(len(banned_df)),
        "invalidated_prev_verified_count": int(len(invalidated)),
        "cleanest_surviving_hub_sheet": clean_hub,
        "sheet_id_10_is_real_local_glue_hub": bool(sheet10_count >= sheet1_count and sheet10_count > 0),
        "sheet_id_1_false_hub_due_to_projection_contamination": bool(sheet1_count == 0 and len(invalidated) > 0),
        "barnard_role": {
            "selector_only": True,
            "bridge_creator": False,
            "weight_bounds": [0.9, 1.1],
        },
    }
    (OUTDIR / "component_reduction_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    inv_txt = "\n".join([f"- {s}" for s in invalidated]) if invalidated else "- none"
    report = f"""# SEAM_PAIR_OPERATOR_V2_REPORT

## Pair-level contamination enforcement
- Projection/tunnel/sheet_id:2 bans were applied at pair level before ranking.
- Contaminated pairs removed: {len(banned_df)}.
- Clean candidate pairs kept (top-10 max): {len(agg)}.

## Invalidated previously verified seams (v1 -> invalid under pair-level rules)
{inv_txt}

## Local-path verification result
- Components before: {before}
- Components after: {after}
- Reduction: {before - after}
- Verified local-path edges: {len(verified_df)}
- Failed local-path edges: {len(failed_df)}

## Hub diagnosis
- Cleanest surviving hub sheet: {clean_hub}
- sheet_id:10 real local glue hub: {summary["sheet_id_10_is_real_local_glue_hub"]}
- sheet_id:1 false hub from projection contamination: {summary["sheet_id_1_false_hub_due_to_projection_contamination"]}

## Interpretation mapping
- Big Man: Barnard selector only.
- Big Woman: shell constraints / contamination rules.
- Small Man: local seam that may genuinely glue.
- Small Woman: projection overlap trap / fake center coincidence.
"""
    (OUTDIR / "SEAM_PAIR_OPERATOR_V2_REPORT.md").write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
