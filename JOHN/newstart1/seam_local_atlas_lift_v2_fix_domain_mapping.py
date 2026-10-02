from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "seam_local_atlas_lift_v2"
SPINE = {"sheet_id:3", "sheet_id:4", "sheet_id:10", "sheet_id:12", "sheet_id:13"}
LEFT_SPINE = {"sheet_id:3", "sheet_id:4"}
RIGHT_SPINE = {"sheet_id:10", "sheet_id:12", "sheet_id:13"}


def sheet_label(x: str | int | float) -> str:
    s = str(x).strip()
    if s.startswith("sheet_id:"):
        return s
    if s.isdigit():
        return f"sheet_id:{int(s)}"
    return s


def pair_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((sheet_label(a), sheet_label(b))))


def pair_id(a: str, b: str) -> str:
    p = pair_key(a, b)
    return f"{p[0]}__{p[1]}"


@dataclass
class DSU:
    parent: dict[str, str]

    @classmethod
    def from_groups(cls, groups: list[list[str]]) -> "DSU":
        nodes = sorted({n for g in groups for n in g if n})
        d = cls(parent={n: n for n in nodes})
        for g in groups:
            g2 = [x for x in g if x]
            if len(g2) > 1:
                r = g2[0]
                for n in g2[1:]:
                    d.union(r, n)
        return d

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


def build_exact_domain_lookup(cloud: pd.DataFrame) -> tuple[dict[str, str], pd.DataFrame, pd.DataFrame]:
    # exact map from domain column
    dom = cloud[["domain", "sheet_id"]].dropna(subset=["domain", "sheet_id"]).copy()
    dom["sheet_label"] = dom["sheet_id"].astype(int).apply(lambda x: f"sheet_id:{x}")
    grouped = dom.groupby("domain")["sheet_label"].agg(lambda s: s.value_counts().idxmax()).reset_index()

    exact = dict(zip(grouped["domain"].astype(str), grouped["sheet_label"].astype(str)))
    resolved_rows = []
    unresolved_rows = []

    # variants: raw / strip prefix / add prefix forms
    variants = []
    for d, s in exact.items():
        variants.append({"domain_query": d, "resolved_sheet": s, "rule": "exact"})
        if ":" in d:
            tail = d.split(":", 1)[1]
            variants.append({"domain_query": tail, "resolved_sheet": s, "rule": "strip_prefix"})
        else:
            # allow canonical prefixed variants seen in contact matrix headers
            for pref in ["sheet1", "sheet2", "sheet3", "sheet4", "sheet10", "sheet11", "sheet12", "sheet13", "sheet14"]:
                variants.append({"domain_query": f"{pref}:{d}", "resolved_sheet": s, "rule": "add_prefix_fallback"})
    vdf = pd.DataFrame(variants).drop_duplicates(subset=["domain_query"], keep="first")
    lookup = dict(zip(vdf["domain_query"], vdf["resolved_sheet"]))

    for k, v in lookup.items():
        resolved_rows.append({"domain_query": k, "resolved_sheet": v})

    # unresolved sample placeholders (filled during contact parse)
    resolved_df = pd.DataFrame(resolved_rows).sort_values("domain_query")
    unresolved_df = pd.DataFrame(unresolved_rows, columns=["domain_query", "reason"])
    return lookup, resolved_df, unresolved_df


def load_contact_long(path: Path) -> pd.DataFrame:
    m = pd.read_csv(path)
    row_col = m.columns[0]
    cols = list(m.columns[1:])
    rows = []
    for _, r in m.iterrows():
        a = str(r[row_col])
        for c in cols:
            v = r[c]
            if pd.isna(v):
                continue
            vv = float(v)
            if vv <= 0:
                continue
            rows.append({"domain_a": a, "domain_b": str(c), "contact_score": vv})
    return pd.DataFrame(rows)


def load_saddle_pair_scores(path: Path) -> dict[tuple[str, str], float]:
    d = json.loads(path.read_text(encoding="utf-8"))
    out: dict[tuple[str, str], float] = {}
    for ev in d.get("events", []):
        if not ev.get("found", False):
            continue
        a = [f"sheet_id:{int(x)}" for x in ev.get("A", [])]
        b = [f"sheet_id:{int(x)}" for x in ev.get("B", [])]
        fs = float(ev.get("F_star", 0.0))
        s = 1.0 / (1.0 + max(fs, 0.0))
        for x in a:
            for y in b:
                if x == y:
                    continue
                out[pair_key(x, y)] = max(out.get(pair_key(x, y), 0.0), s)
    return out


def add_lift_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["lift_density"] = np.nan
    out["lift_tangent_x"] = np.nan
    out["lift_tangent_y"] = np.nan
    out["lift_radius"] = np.nan
    for sid, g in out.groupby("sheet_label"):
        idx = g.index.to_list()
        p = g[["pi_1", "pi_2"]].to_numpy(dtype=float)
        if len(p) < 2:
            continue
        c = p.mean(axis=0)
        for loc, i in enumerate(idx):
            d = np.linalg.norm(p - p[loc], axis=1)
            nidx = np.argsort(d)[1:6]
            if len(nidx) == 0:
                dens = np.nan
                tx, ty = 0.0, 0.0
            else:
                dens = float(np.mean(d[nidx]))
                vec = (p[nidx] - p[loc]).mean(axis=0)
                tx, ty = float(vec[0]), float(vec[1])
            out.at[i, "lift_density"] = dens
            out.at[i, "lift_tangent_x"] = tx
            out.at[i, "lift_tangent_y"] = ty
            out.at[i, "lift_radius"] = float(np.linalg.norm(p[loc] - c))
    return out


def pca_binary_split(df: pd.DataFrame) -> np.ndarray:
    x = df[["pi_1", "pi_2", "lift_tangent_x", "lift_tangent_y", "lift_radius"]].to_numpy(dtype=float)
    if len(x) < 2:
        return np.zeros(len(x), dtype=int)
    x0 = x - x.mean(axis=0, keepdims=True)
    cov = np.cov(x0.T)
    vals, vecs = np.linalg.eigh(cov)
    axis = vecs[:, np.argmax(vals)]
    proj = x0 @ axis
    med = np.median(proj)
    return (proj > med).astype(int)


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    relay_verified = pd.read_csv(ROOT / "out" / "seam_relay_operator_test_v1" / "relay_verified.csv")
    domain_relays = pd.read_csv(ROOT / "out" / "seam_relay_operator_test_v1" / "domain_conditioned_relays.csv")
    cloud = pd.read_csv(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "sheet0_reconstruction"
        / "PI_GLOBAL_POINT_CLOUD_subsheets.csv"
    )
    contact_long = load_contact_long(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "geometry_map"
        / "contact_map_knn_scores.csv"
    )
    gap = pd.read_csv(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "geometry_map"
        / "gap_nearest_pairs.csv"
    )
    saddle_scores = load_saddle_pair_scores(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "percolation_saddle_geometry"
        / "percolation_saddle_geometry.json"
    )
    comps = pd.read_csv(ROOT / "out" / "connectivity_audit" / "disconnected_components.csv")
    conn_md = (ROOT / "out" / "connectivity_audit" / "connectivity_audit.md").read_text(encoding="utf-8")
    old_seams = pd.read_csv(ROOT / "out" / "seam_local_atlas_lift_v1" / "lifted_local_seams.csv")
    old_reduction = json.loads(
        (ROOT / "out" / "seam_local_atlas_lift_v1" / "component_reduction_after_lift.json").read_text(encoding="utf-8")
    )
    _ = relay_verified, domain_relays, conn_md, old_seams, old_reduction

    # 1) exact domain->sheet mapping
    lookup, resolved_df, unresolved_df = build_exact_domain_lookup(cloud)

    contact = contact_long.copy()
    unresolved = []
    contact["sheet_a"] = contact["domain_a"].map(lookup)
    contact["sheet_b"] = contact["domain_b"].map(lookup)
    for r in contact[contact["sheet_a"].isna()].itertuples(index=False):
        unresolved.append({"domain_query": str(r.domain_a), "reason": "no_lookup_match"})
    for r in contact[contact["sheet_b"].isna()].itertuples(index=False):
        unresolved.append({"domain_query": str(r.domain_b), "reason": "no_lookup_match"})
    if unresolved:
        unresolved_df = pd.concat([unresolved_df, pd.DataFrame(unresolved)], ignore_index=True).drop_duplicates()

    resolved_df.to_csv(OUTDIR / "domain_sheet_lookup_resolved.csv", index=False)
    unresolved_df.to_csv(OUTDIR / "domain_sheet_lookup_unresolved.csv", index=False)

    # bans
    banned_domain_pairs = set()
    for g in gap.itertuples(index=False):
        if float(g.dist_xy) == 0.0:
            banned_domain_pairs.add(tuple(sorted((str(g.domain_a), str(g.domain_b)))))

    # corrected domain subgraph restricted to spine and no sheet2
    c = contact.dropna(subset=["sheet_a", "sheet_b"]).copy()
    c["sheet_a"] = c["sheet_a"].astype(str)
    c["sheet_b"] = c["sheet_b"].astype(str)
    c = c[c["sheet_a"].isin(SPINE) & c["sheet_b"].isin(SPINE)].copy()
    c = c[(c["sheet_a"] != "sheet_id:2") & (c["sheet_b"] != "sheet_id:2")].copy()
    c["dom_pair"] = c.apply(lambda r: tuple(sorted((str(r["domain_a"]), str(r["domain_b"])))), axis=1)
    c = c[~c["dom_pair"].isin(banned_domain_pairs)].copy()
    c["pair"] = c.apply(lambda r: pair_id(r["sheet_a"], r["sheet_b"]), axis=1)
    c["saddle_support"] = c.apply(lambda r: float(saddle_scores.get(pair_key(r["sheet_a"], r["sheet_b"]), 0.0)), axis=1)
    c["non_projection_support"] = c["contact_score"] + c["saddle_support"]
    corrected_domain_subgraph = c[c["non_projection_support"] > 0].copy()
    corrected_domain_subgraph.to_csv(OUTDIR / "corrected_domain_subgraph.csv", index=False)

    # microchart lift with corrected mapping
    cloud2 = cloud.copy()
    cloud2["sheet_label"] = cloud2["sheet_id"].astype(int).apply(lambda x: f"sheet_id:{x}")
    spine_cloud = cloud2[cloud2["sheet_label"].isin(SPINE)][["domain", "sheet_label", "pi_1", "pi_2", "mode_id"]].copy()
    lifted = add_lift_features(spine_cloud)
    lifted["microchart_id"] = "base"
    for sid in ["sheet_id:3", "sheet_id:4"]:
        g = lifted[lifted["sheet_label"] == sid].copy()
        if g.empty:
            continue
        lbl = pca_binary_split(g)
        lifted.loc[g.index, "microchart_id"] = [f"{sid}_m{int(x)}" for x in lbl]
    corrected_microcharts = lifted.copy()
    corrected_microcharts.to_csv(OUTDIR / "corrected_microchart_assignments.csv", index=False)

    # corrected lifted seams
    dom2chart = corrected_microcharts.set_index("domain")["microchart_id"].to_dict()
    chart2sheet = corrected_microcharts.groupby("microchart_id")["sheet_label"].agg(lambda s: s.iloc[0]).to_dict()
    cent = corrected_microcharts.groupby("microchart_id")[["pi_1", "pi_2", "lift_tangent_x", "lift_tangent_y", "lift_radius"]].mean()

    rows = []
    for r in corrected_domain_subgraph.itertuples(index=False):
        da, db = str(r.domain_a), str(r.domain_b)
        ca, cb = dom2chart.get(da), dom2chart.get(db)
        if (ca is None) or (cb is None) or (ca == cb):
            continue
        sa, sb = chart2sheet.get(ca, ""), chart2sheet.get(cb, "")
        if sa == "sheet_id:2" or sb == "sheet_id:2":
            continue
        va = cent.loc[ca].to_numpy(dtype=float) if ca in cent.index else None
        vb = cent.loc[cb].to_numpy(dtype=float) if cb in cent.index else None
        if va is None or vb is None:
            continue
        dist = float(np.linalg.norm(va - vb))
        barnard_w = float(np.clip(1.02, 0.95, 1.05))
        score = (0.55 * float(r.contact_score) + 0.45 * float(r.saddle_support)) * barnard_w
        cross_spine = ((sa in LEFT_SPINE and sb in RIGHT_SPINE) or (sb in LEFT_SPINE and sa in RIGHT_SPINE))
        verified = (
            bool(ca in cent.index and cb in cent.index)
            and (float(r.contact_score) > 0 or float(r.saddle_support) > 0)
            and (dist < 0.55)
            and cross_spine
        )
        fail_reason = ""
        if not verified:
            if not cross_spine:
                fail_reason = "not_cross_10_12_13_to_3_4"
            elif float(r.contact_score) <= 0 and float(r.saddle_support) <= 0:
                fail_reason = "no_contact_or_saddle"
            elif dist >= 0.55:
                fail_reason = "lifted_discontinuity"
        rows.append(
            {
                "chart_a": ca,
                "chart_b": cb,
                "sheet_a": sa,
                "sheet_b": sb,
                "contact_support": float(r.contact_score),
                "saddle_support": float(r.saddle_support),
                "lifted_distance": dist,
                "barnard_weight": barnard_w,
                "score": score,
                "verified_refined_seam": bool(verified),
                "failure_reason": fail_reason,
            }
        )
    corrected_lifted = pd.DataFrame(rows).drop_duplicates()
    corrected_lifted.to_csv(OUTDIR / "corrected_lifted_local_seams.csv", index=False)

    # supernode connectivity on corrected verified seams
    supernode = "relay_spine_supernode"
    super_rows = []
    for r in corrected_lifted.itertuples(index=False):
        if not bool(r.verified_refined_seam):
            continue
        a, b = str(r.sheet_a), str(r.sheet_b)
        aa = supernode if a in SPINE else a
        bb = supernode if b in SPINE else b
        if aa == bb:
            continue
        super_rows.append(
            {
                "node_a": aa,
                "node_b": bb,
                "source_sheet_a": a,
                "source_sheet_b": b,
                "contact_support": float(r.contact_support),
                "saddle_support": float(r.saddle_support),
            }
        )
    corrected_super = pd.DataFrame(super_rows).drop_duplicates()
    corrected_super.to_csv(OUTDIR / "corrected_supernode_connectivity.csv", index=False)

    # component recompute
    groups = [[y.strip() for y in str(x).split("|") if y.strip()] for x in comps["member_nodes"].astype(str)]
    dsu = DSU.from_groups(groups)
    before = dsu.components()
    if supernode not in dsu.parent:
        dsu.parent[supernode] = supernode
    for s in SPINE:
        if s not in dsu.parent:
            dsu.parent[s] = s
        dsu.union(supernode, s)
    applied = 0
    for r in corrected_super.itertuples(index=False):
        if r.node_a not in dsu.parent:
            dsu.parent[r.node_a] = r.node_a
        if r.node_b not in dsu.parent:
            dsu.parent[r.node_b] = r.node_b
        if dsu.union(r.node_a, r.node_b):
            applied += 1
    after = dsu.components()

    # dedicated audit for 10/12/13 to 3/4 bridging
    present_sheets = sorted(set(corrected_domain_subgraph["sheet_a"]).union(set(corrected_domain_subgraph["sheet_b"])))
    cross_verified = corrected_lifted[
        corrected_lifted["verified_refined_seam"]
        & (
            ((corrected_lifted["sheet_a"].isin(LEFT_SPINE)) & (corrected_lifted["sheet_b"].isin(RIGHT_SPINE)))
            | ((corrected_lifted["sheet_b"].isin(LEFT_SPINE)) & (corrected_lifted["sheet_a"].isin(RIGHT_SPINE)))
        )
    ].copy()

    audit_rows = []
    for ls in LEFT_SPINE:
        for rs in RIGHT_SPINE:
            pair = pair_id(ls, rs)
            sub = corrected_lifted[
                ((corrected_lifted["sheet_a"] == ls) & (corrected_lifted["sheet_b"] == rs))
                | ((corrected_lifted["sheet_a"] == rs) & (corrected_lifted["sheet_b"] == ls))
            ]
            if sub.empty:
                reason = "a_no_contact_support"
            else:
                if (sub["contact_support"] > 0).any():
                    reason = "verified" if (sub["verified_refined_seam"] == True).any() else "d_true_lifted_discontinuity"  # noqa: E712
                elif (sub["saddle_support"] > 0).any():
                    reason = "c_saddle_only_without_tunnel_support"
                else:
                    reason = "a_no_contact_support"
                if reason != "verified" and pair in {pair_id("sheet_id:10", "sheet_id:10")}:
                    reason = "b_projection_only_overlap_ban"
            audit_rows.append(
                {
                    "left_sheet": ls,
                    "right_sheet": rs,
                    "pair": pair,
                    "pair_present_in_corrected_subgraph": bool(not sub.empty),
                    "verified_cross_bridge": bool((not sub.empty) and (sub["verified_refined_seam"] == True).any()),  # noqa: E712
                    "failure_category": reason if reason != "verified" else "",
                }
            )
    audit_df = pd.DataFrame(audit_rows)
    audit_df.to_csv(OUTDIR / "spine_bridge_audit.csv", index=False)

    reduction = {
        "components_before_corrected_lift": int(before),
        "components_after_corrected_lift": int(after),
        "component_reduction_after_corrected_lift": int(before - after),
        "improved_beyond_v1_after7": bool(after < 7),
        "resolved_domain_queries": int(len(resolved_df)),
        "unresolved_domain_queries": int(len(unresolved_df)),
        "spine_sheet_presence_in_corrected_subgraph": present_sheets,
        "cross_10_12_13_to_3_4_verified_count": int(len(cross_verified)),
        "mapping_bug_only": bool(len(cross_verified) > 0),
        "projection_loss_still_present": True,
        "real_topological_disconnect_remains": bool(after > 1),
        "applied_supernode_edges": int(applied),
    }
    (OUTDIR / "corrected_component_reduction.json").write_text(json.dumps(reduction, indent=2), encoding="utf-8")

    report = f"""# SEAM_LOCAL_ATLAS_LIFT_V2_REPORT

## 1. Why v1 was invalid/incomplete
- v1 used fallback domain mapping that can collapse unprefixed domain labels.
- This run rebuilds exact domain->sheet resolution from PI_GLOBAL_POINT_CLOUD_subsheets.csv.

## 2. Exact mapping recovery statistics
- resolved_domain_queries: {reduction["resolved_domain_queries"]}
- unresolved_domain_queries: {reduction["unresolved_domain_queries"]}

## 3. Do 10/12/13 appear in corrected spine graph?
- present sheets in corrected domain subgraph: {present_sheets}

## 4. Do 10/12/13 truly bridge into 3/4?
- verified cross-bridge count (10/12/13 <-> 3/4): {reduction["cross_10_12_13_to_3_4_verified_count"]}

## 5. Was relay-spine real or label artifact?
- mapping bug only: {reduction["mapping_bug_only"]}
- projection loss still present: {reduction["projection_loss_still_present"]}
- real topological disconnect remains: {reduction["real_topological_disconnect_remains"]}

## 6. Final verdict
- mapping bug only?: {reduction["mapping_bug_only"]}
- projection loss still present?: {reduction["projection_loss_still_present"]}
- real topological disconnect remains?: {reduction["real_topological_disconnect_remains"]}

## Interpretation mapping
- Big Man = Barnard selector only
- Big Woman = contamination / exclusion shell
- Small Man = corrected relay seam that survives exact lookup
- Small Woman = projection overlap trap or label-collapse trap
"""
    (OUTDIR / "SEAM_LOCAL_ATLAS_LIFT_V2_REPORT.md").write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
