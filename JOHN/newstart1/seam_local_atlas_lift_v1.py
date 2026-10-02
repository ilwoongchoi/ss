from __future__ import annotations

import json
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "seam_local_atlas_lift_v1"

SPINE = {"sheet_id:3", "sheet_id:4", "sheet_id:10", "sheet_id:12", "sheet_id:13"}


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


def domain_to_sheet(domain: str) -> str:
    d = str(domain)
    if d.startswith("sheet") and ":" in d:
        h = d.split(":", 1)[0]
        if h[5:].isdigit():
            return f"sheet_id:{int(h[5:])}"
    if d.startswith("tile_"):
        return "sheet_id:0"
    return sheet_label(d)


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


def load_contact_domain_map(path: Path) -> pd.DataFrame:
    # matrix -> long
    m = pd.read_csv(path)
    row_col = m.columns[0]
    long_rows = []
    cols = list(m.columns[1:])
    for _, r in m.iterrows():
        a = str(r[row_col])
        for c in cols:
            v = r[c]
            if pd.isna(v):
                continue
            vv = float(v)
            if vv <= 0:
                continue
            long_rows.append({"domain_a": a, "domain_b": str(c), "contact_score": vv})
    return pd.DataFrame(long_rows)


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
                k = pair_key(x, y)
                out[k] = max(out.get(k, 0.0), s)
    return out


def pca_split(df: pd.DataFrame, feature_cols: list[str]) -> np.ndarray:
    x = df[feature_cols].to_numpy(dtype=float)
    if len(x) < 2:
        return np.zeros(len(x), dtype=int)
    x0 = x - x.mean(axis=0, keepdims=True)
    cov = np.cov(x0.T)
    vals, vecs = np.linalg.eigh(cov)
    axis = vecs[:, np.argmax(vals)]
    proj = x0 @ axis
    med = np.median(proj)
    return (proj > med).astype(int)


def add_lift_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["lift_density"] = np.nan
    out["lift_tangent_x"] = np.nan
    out["lift_tangent_y"] = np.nan
    out["lift_radius"] = np.nan
    for sid, g in out.groupby("sheet_id_label"):
        idx = g.index.to_list()
        p = g[["pi_1", "pi_2"]].to_numpy(dtype=float)
        if len(p) == 0:
            continue
        c = p.mean(axis=0)
        for loc, i in enumerate(idx):
            d = np.linalg.norm(p - p[loc], axis=1)
            d_sorted = np.sort(d[d > 0])
            k = min(5, len(d_sorted))
            if k == 0:
                dens = np.nan
                tx, ty = 0.0, 0.0
            else:
                dens = float(np.mean(d_sorted[:k]))
                nidx = np.argsort(d)[1 : k + 1]
                vec = (p[nidx] - p[loc]).mean(axis=0)
                tx, ty = float(vec[0]), float(vec[1])
            out.at[i, "lift_density"] = dens
            out.at[i, "lift_tangent_x"] = tx
            out.at[i, "lift_tangent_y"] = ty
            out.at[i, "lift_radius"] = float(np.linalg.norm(p[loc] - c))
    return out


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
    gap = pd.read_csv(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "geometry_map"
        / "gap_nearest_pairs.csv"
    )
    contact_long = load_contact_domain_map(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "geometry_map"
        / "contact_map_knn_scores.csv"
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
    relay_summary = json.loads(
        (ROOT / "out" / "seam_relay_operator_test_v1" / "component_reduction_summary.json").read_text(encoding="utf-8")
    )
    _ = domain_relays, relay_summary

    cloud["sheet_id_label"] = cloud["sheet_id"].apply(lambda x: f"sheet_id:{int(x)}" if pd.notna(x) else "sheet_id:unknown")
    spine_domains = cloud[cloud["sheet_id_label"].isin(SPINE)].copy()
    spine_domains.to_csv(OUTDIR / "relay_spine_domains.csv", index=False)

    # projection-only bans from gap dist==0
    banned_domain_pairs: set[tuple[str, str]] = set()
    banned_sheet_pairs: set[str] = set()
    for g in gap.itertuples(index=False):
        if float(g.dist_xy) == 0.0:
            a, b = str(g.domain_a), str(g.domain_b)
            banned_domain_pairs.add(tuple(sorted((a, b))))
            banned_sheet_pairs.add(pair_id(domain_to_sheet(a), domain_to_sheet(b)))

    # domain-level subgraph (non-projection evidence only)
    c = contact_long.copy()
    c["sheet_a"] = c["domain_a"].apply(domain_to_sheet)
    c["sheet_b"] = c["domain_b"].apply(domain_to_sheet)
    c = c[c["sheet_a"].isin(SPINE) & c["sheet_b"].isin(SPINE)].copy()
    c = c[c["sheet_a"] != "sheet_id:2"]
    c = c[c["sheet_b"] != "sheet_id:2"]
    c["dom_pair"] = c.apply(lambda r: tuple(sorted((r["domain_a"], r["domain_b"]))), axis=1)
    c = c[~c["dom_pair"].isin(banned_domain_pairs)].copy()
    c["pair"] = c.apply(lambda r: pair_id(r["sheet_a"], r["sheet_b"]), axis=1)
    c = c[~c["pair"].isin(banned_sheet_pairs)].copy()
    c["saddle_support"] = c.apply(lambda r: float(saddle_scores.get(pair_key(r["sheet_a"], r["sheet_b"]), 0.0)), axis=1)
    c["non_projection_support"] = c["contact_score"] + c["saddle_support"]
    domain_subgraph = c[c["non_projection_support"] > 0].copy()
    domain_subgraph.to_csv(OUTDIR / "domain_subgraph.csv", index=False)

    # Local coordinate lift
    lifted = add_lift_features(spine_domains[["domain", "sheet_id_label", "pi_1", "pi_2", "mode_id"]].copy())

    # Micro-chart subdivision for sheet 3 and 4
    lifted["microchart_id"] = "base"
    for sid in ["sheet_id:3", "sheet_id:4"]:
        g = lifted[lifted["sheet_id_label"] == sid].copy()
        if g.empty:
            continue
        labels = pca_split(g, ["pi_1", "pi_2", "lift_tangent_x", "lift_tangent_y", "lift_radius"])
        lifted.loc[g.index, "microchart_id"] = [f"{sid}_m{int(x)}" for x in labels]
    microchart = lifted[["domain", "sheet_id_label", "microchart_id", "pi_1", "pi_2", "lift_density", "lift_tangent_x", "lift_tangent_y", "lift_radius", "mode_id"]].copy()
    microchart.to_csv(OUTDIR / "microchart_assignments.csv", index=False)

    # Build refined seams between microcharts/sheets
    cent = microchart.groupby("microchart_id")[["pi_1", "pi_2", "lift_tangent_x", "lift_tangent_y", "lift_radius"]].mean().reset_index()
    chart_to_sheet = microchart.groupby("microchart_id")["sheet_id_label"].agg(lambda s: s.iloc[0]).to_dict()

    # contact support aggregated by chart pairs
    dom2chart = microchart.set_index("domain")["microchart_id"].to_dict()
    rows = []
    for r in domain_subgraph.itertuples(index=False):
        ca = dom2chart.get(r.domain_a)
        cb = dom2chart.get(r.domain_b)
        if (ca is None) or (cb is None) or (ca == cb):
            continue
        sa = chart_to_sheet.get(ca, "")
        sb = chart_to_sheet.get(cb, "")
        if "sheet_id:2" in (sa, sb):
            continue
        pid = pair_id(sa, sb)
        if pid in banned_sheet_pairs:
            continue
        rows.append(
            {
                "chart_a": ca,
                "chart_b": cb,
                "sheet_a": sa,
                "sheet_b": sb,
                "contact_support": float(r.contact_score),
                "saddle_support": float(r.saddle_support),
            }
        )
    seam_df = pd.DataFrame(rows)
    if seam_df.empty:
        seam_df = pd.DataFrame(
            columns=[
                "chart_a",
                "chart_b",
                "sheet_a",
                "sheet_b",
                "contact_support",
                "saddle_support",
                "lifted_distance",
                "barnard_weight",
                "verified_refined_seam",
                "failure_reason",
            ]
        )
    else:
        agg = (
            seam_df.groupby(["chart_a", "chart_b", "sheet_a", "sheet_b"], as_index=False)
            .agg(contact_support=("contact_support", "max"), saddle_support=("saddle_support", "max"))
        )
        cent_map = cent.set_index("microchart_id")
        dists = []
        for r in agg.itertuples(index=False):
            if (r.chart_a not in cent_map.index) or (r.chart_b not in cent_map.index):
                dists.append(np.nan)
                continue
            va = cent_map.loc[r.chart_a].to_numpy(dtype=float)
            vb = cent_map.loc[r.chart_b].to_numpy(dtype=float)
            dists.append(float(np.linalg.norm(va - vb)))
        agg["lifted_distance"] = dists
        agg["barnard_weight"] = 1.02
        agg["barnard_weight"] = agg["barnard_weight"].clip(lower=0.95, upper=1.05)
        agg["score"] = (0.55 * agg["contact_support"] + 0.45 * agg["saddle_support"]) * agg["barnard_weight"]
        agg["verified_refined_seam"] = (
            (agg["contact_support"] > 0)
            & ((agg["contact_support"] > 0) | (agg["saddle_support"] > 0))
            & (agg["lifted_distance"] < 0.55)
            & (~agg.apply(lambda r: pair_id(r["sheet_a"], r["sheet_b"]) in banned_sheet_pairs, axis=1))
        )
        agg["failure_reason"] = np.where(agg["verified_refined_seam"], "", "fails_nonprojection_or_lift_continuity")
        seam_df = agg
    seam_df.to_csv(OUTDIR / "lifted_local_seams.csv", index=False)

    # Supernode collapse from verified relay motifs
    verified_relay_edges = relay_verified[["from_sheet", "mediator_sheet", "to_sheet"]].copy()
    relay_nodes = set()
    for r in verified_relay_edges.itertuples(index=False):
        relay_nodes.add(str(r.from_sheet))
        relay_nodes.add(str(r.mediator_sheet))
        relay_nodes.add(str(r.to_sheet))
    supernode_name = "relay_spine_supernode"

    # Build supernode connectivity table from verified refined seams
    super_rows = []
    for r in seam_df.itertuples(index=False):
        if not bool(getattr(r, "verified_refined_seam", False)):
            continue
        a, b = str(r.sheet_a), str(r.sheet_b)
        aa = supernode_name if a in relay_nodes else a
        bb = supernode_name if b in relay_nodes else b
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
                "lifted_distance": float(r.lifted_distance),
            }
        )
    super_df = pd.DataFrame(super_rows).drop_duplicates()
    super_df.to_csv(OUTDIR / "supernode_connectivity.csv", index=False)

    # Component reduction after lift + supernode application
    groups = [[y.strip() for y in str(x).split("|") if y.strip()] for x in comps["member_nodes"].astype(str)]
    dsu = DSU.from_groups(groups)
    before = dsu.components()

    # collapse relay nodes to supernode
    if supernode_name not in dsu.parent:
        dsu.parent[supernode_name] = supernode_name
    for n in relay_nodes:
        if n not in dsu.parent:
            dsu.parent[n] = n
        dsu.union(supernode_name, n)

    applied = 0
    for r in super_df.itertuples(index=False):
        if r.node_a not in dsu.parent:
            dsu.parent[r.node_a] = r.node_a
        if r.node_b not in dsu.parent:
            dsu.parent[r.node_b] = r.node_b
        if dsu.union(r.node_a, r.node_b):
            applied += 1
    after = dsu.components()

    # blocked global seams: spine to non-spine with no verified refined seam
    all_sheets = sorted(set(cloud["sheet_id_label"].unique()))
    verified_sheet_pairs = set(
        pair_id(r.sheet_a, r.sheet_b)
        for r in seam_df.itertuples(index=False)
        if bool(getattr(r, "verified_refined_seam", False))
    )
    blocked_rows = []
    for s in sorted(SPINE):
        for t in all_sheets:
            if s == t or t == "sheet_id:2":
                continue
            pid = pair_id(s, t)
            if pid in banned_sheet_pairs:
                reason = "projection_or_contamination_ban"
            elif pid in verified_sheet_pairs:
                continue
            else:
                reason = "no_verified_lifted_local_continuity"
            blocked_rows.append({"seam_a": s, "seam_b": t, "blocked_reason": reason})
    blocked_df = pd.DataFrame(blocked_rows).drop_duplicates()
    blocked_df.to_csv(OUTDIR / "blocked_global_seams.csv", index=False)

    reduction = {
        "components_before_lift": int(before),
        "components_after_lift_and_supernode": int(after),
        "component_reduction_after_lift": int(before - after),
        "relay_components_baseline": 7,
        "improved_beyond_relay_7": bool(after < 7),
        "verified_refined_seams": int((seam_df["verified_refined_seam"] == True).sum()) if "verified_refined_seam" in seam_df.columns else 0,  # noqa: E712
        "applied_supernode_edges": int(applied),
        "sheet2_excluded": True,
        "barnard_selector_only": True,
    }
    (OUTDIR / "component_reduction_after_lift.json").write_text(json.dumps(reduction, indent=2), encoding="utf-8")

    # report
    c3 = int(microchart["microchart_id"].str.startswith("sheet_id:3_m").sum())
    c4 = int(microchart["microchart_id"].str.startswith("sheet_id:4_m").sum())
    report = f"""# SEAM_LOCAL_ATLAS_LIFT_V1_REPORT

## 1) Verified relay spine structure
- Spine focus: sheet_id:3,4,10,12,13
- Relay-mediated baseline from v1: components 11 -> 7

## 2) sheet_id:3/4 microchart split
- sheet_id:3 microchart-assigned domains: {c3}
- sheet_id:4 microchart-assigned domains: {c4}
- Split method: PCA-axis local partition in lifted feature space

## 3) Lifted coordinate continuity
- Lifted seams evaluated: {len(seam_df)}
- Verified refined seams: {reduction["verified_refined_seams"]}
- dist_xy==0 projection overlaps were exclusion-only

## 4) Supernode collapse impact
- Components before lift pipeline: {before}
- Components after lift+supernode: {after}
- Reduction: {before - after}
- Improved beyond relay baseline(7): {reduction["improved_beyond_relay_7"]}

## 5) Remaining globally blocked seams
- See blocked_global_seams.csv

## 6) Final verdict
- wrong sheet granularity: {reduction["verified_refined_seams"] > 0}
- 2D projection loss present: True
- real remaining topological disconnect: {after > 1}

## Interpretation mapping
- Big Man = Barnard selector only
- Big Woman = contamination shell / exclusion law
- Small Man = verified relay spine / refined micro-seam
- Small Woman = projection overlap trap
"""
    (OUTDIR / "SEAM_LOCAL_ATLAS_LIFT_V1_REPORT.md").write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
