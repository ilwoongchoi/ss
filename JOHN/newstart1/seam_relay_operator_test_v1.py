from __future__ import annotations

import json
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "seam_relay_operator_test_v1"


def sheet_label(x: str | int | float) -> str:
    s = str(x).strip()
    if s.startswith("sheet_id:"):
        return s
    if s.startswith("sheet") and ":" in s:
        h = s.split(":", 1)[0]
        if h[5:].isdigit():
            return f"sheet_id:{int(h[5:])}"
    if s.isdigit():
        return f"sheet_id:{int(s)}"
    return s


def pair_key(a: str, b: str) -> tuple[str, str]:
    x, y = sheet_label(a), sheet_label(b)
    return tuple(sorted((x, y)))


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
    return sheet_label(d)


@dataclass
class DSU:
    parent: dict[str, str]

    @classmethod
    def from_groups(cls, groups: list[list[str]]) -> "DSU":
        nodes = sorted({n for g in groups for n in g})
        d = cls(parent={n: n for n in nodes})
        for g in groups:
            g2 = [x for x in g if x]
            if len(g2) > 1:
                root = g2[0]
                for n in g2[1:]:
                    d.union(root, n)
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


def load_contact_pair_scores(path: Path) -> dict[tuple[str, str], float]:
    df = pd.read_csv(path)
    if df.empty:
        return {}
    row_col = df.columns[0]
    col_domains = list(df.columns[1:])
    out: dict[tuple[str, str], float] = {}
    for _, row in df.iterrows():
        sa = domain_to_sheet(row[row_col])
        for c in col_domains:
            v = row[c]
            if pd.isna(v):
                continue
            vv = float(v)
            if vv <= 0:
                continue
            sb = domain_to_sheet(c)
            if sa == sb:
                continue
            k = pair_key(sa, sb)
            out[k] = max(out.get(k, 0.0), vv)
    return out


def load_saddle_pair_scores(path: Path) -> dict[tuple[str, str], float]:
    d = json.loads(path.read_text(encoding="utf-8"))
    out: dict[tuple[str, str], float] = {}
    for ev in d.get("events", []):
        if not ev.get("found", False):
            continue
        a = [f"sheet_id:{int(x)}" for x in ev.get("A", [])]
        b = [f"sheet_id:{int(x)}" for x in ev.get("B", [])]
        f_star = float(ev.get("F_star", 0.0))
        s = 1.0 / (1.0 + max(f_star, 0.0))
        for x in a:
            for y in b:
                if x == y:
                    continue
                k = pair_key(x, y)
                out[k] = max(out.get(k, 0.0), s)
    return out


def local_sheet_coherence(cloud: pd.DataFrame, a: str, b: str, c: str) -> tuple[bool, float]:
    subset = cloud[cloud["sheet_id_label"].isin([a, b, c])][["sheet_id_label", "pi_1", "pi_2"]].dropna()
    if len(subset) < 30:
        return False, np.nan
    cent = subset.groupby("sheet_id_label")[["pi_1", "pi_2"]].mean()
    if any(x not in cent.index for x in [a, b, c]):
        return False, np.nan
    ab = float(np.linalg.norm((cent.loc[a] - cent.loc[b]).to_numpy()))
    bc = float(np.linalg.norm((cent.loc[b] - cent.loc[c]).to_numpy()))
    ac = float(np.linalg.norm((cent.loc[a] - cent.loc[c]).to_numpy()))
    median_edge = np.median([ab, bc, ac])
    coherent = (ab <= 1.5 * median_edge) and (bc <= 1.5 * median_edge)
    return bool(coherent), float((ab + bc) / 2.0)


def mode_coherence(cloud: pd.DataFrame, a: str, b: str, c: str) -> list[dict]:
    out = []
    if "mode_id" not in cloud.columns:
        return out
    mdf = cloud.dropna(subset=["mode_id"]).copy()
    if mdf.empty:
        return out
    mdf["mode_id"] = mdf["mode_id"].astype(str)
    for mode, g in mdf.groupby("mode_id"):
        gg = g[g["sheet_id_label"].isin([a, b, c])]
        counts = gg["sheet_id_label"].value_counts()
        if any(counts.get(x, 0) < 3 for x in [a, b, c]):
            continue
        ok, metric = local_sheet_coherence(gg, a, b, c)
        out.append(
            {
                "mode_id": mode,
                "coherent": ok,
                "coherence_metric": metric,
            }
        )
    return out


def domain_coherence(cloud: pd.DataFrame, a: str, b: str, c: str) -> dict:
    ddf = cloud[cloud["sheet_id_label"].isin([a, b, c])].dropna(subset=["domain", "pi_1", "pi_2"]).copy()
    if ddf.empty:
        return {"domain_continuity": False, "domain_pairs_ok": 0, "domain_pairs_total": 0}
    dom_cent = ddf.groupby(["sheet_id_label", "domain"])[["pi_1", "pi_2"]].mean().reset_index()
    if dom_cent.empty:
        return {"domain_continuity": False, "domain_pairs_ok": 0, "domain_pairs_total": 0}
    ok = 0
    total = 0
    for x, y in [(a, b), (b, c)]:
        xa = dom_cent[dom_cent["sheet_id_label"] == x][["pi_1", "pi_2"]]
        ya = dom_cent[dom_cent["sheet_id_label"] == y][["pi_1", "pi_2"]]
        if xa.empty or ya.empty:
            continue
        total += 1
        dmin = np.inf
        xvals = xa.to_numpy()
        yvals = ya.to_numpy()
        for xv in xvals:
            dist = np.linalg.norm(yvals - xv, axis=1).min()
            dmin = min(dmin, dist)
        if np.isfinite(dmin) and dmin < 0.35:
            ok += 1
    return {"domain_continuity": ok > 0, "domain_pairs_ok": ok, "domain_pairs_total": total}


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    clean_pairs = pd.read_csv(ROOT / "out" / "seam_pair_operator_test_v2" / "clean_pair_candidates.csv")
    contaminated = pd.read_csv(ROOT / "out" / "seam_pair_operator_test_v2" / "contaminated_pairs_removed.csv")
    cloud = pd.read_csv(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "sheet0_reconstruction"
        / "PI_GLOBAL_POINT_CLOUD_subsheets.csv"
    )
    comps = pd.read_csv(ROOT / "out" / "connectivity_audit" / "disconnected_components.csv")

    contact_scores = load_contact_pair_scores(
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
    gap = pd.read_csv(
        ROOT
        / "out"
        / "external_trackA"
        / "sh_1_64_micro_r_0p017100"
        / "geometry_map"
        / "gap_nearest_pairs.csv"
    )

    cloud["sheet_id_label"] = cloud["sheet_id"].apply(lambda x: f"sheet_id:{int(x)}" if pd.notna(x) else "sheet_id:unknown")
    banned_pairs = set(contaminated["pair"].astype(str).tolist())

    # exclusion-only from gap: dist_xy==0
    for g in gap.itertuples(index=False):
        if float(g.dist_xy) == 0.0:
            banned_pairs.add(pair_id(domain_to_sheet(g.domain_a), domain_to_sheet(g.domain_b)))

    # edge set from clean pairs with rules
    edge_records = []
    for r in clean_pairs.itertuples(index=False):
        a, b = str(r.pa), str(r.pb)
        pid = pair_id(a, b)
        if pid in banned_pairs:
            continue
        if "sheet_id:2" in (a, b):
            continue
        edge_records.append(
            {
                "pair": pid,
                "a": pair_key(a, b)[0],
                "b": pair_key(a, b)[1],
                "rank_score": float(r.rank_score),
                "mersenne_conflict_flag": bool(r.mersenne_conflict_flag),
            }
        )
    edges = pd.DataFrame(edge_records).drop_duplicates(subset=["pair"])
    if edges.empty:
        raise RuntimeError("No clean edges for relay search after exclusions.")

    # adjacency
    nbr: dict[str, set[str]] = {}
    for e in edges.itertuples(index=False):
        nbr.setdefault(e.a, set()).add(e.b)
        nbr.setdefault(e.b, set()).add(e.a)

    # 2-hop candidates A-B-C
    relays = []
    for b, ns in nbr.items():
        ns_sorted = sorted(ns)
        for a, c in combinations(ns_sorted, 2):
            if a == c:
                continue
            p1 = pair_key(a, b)
            p2 = pair_key(b, c)
            pid1 = pair_id(*p1)
            pid2 = pair_id(*p2)
            if pid1 in banned_pairs or pid2 in banned_pairs:
                continue

            c1 = float(contact_scores.get(p1, 0.0))
            c2 = float(contact_scores.get(p2, 0.0))
            s1 = float(saddle_scores.get(p1, 0.0))
            s2 = float(saddle_scores.get(p2, 0.0))

            has_nonproj_each_hop = ((c1 > 0 or s1 > 0) and (c2 > 0 or s2 > 0))
            has_contact_any = (c1 > 0) or (c2 > 0)
            coherent, coh_metric = local_sheet_coherence(cloud, a, b, c)

            barnard_weight = 1.02  # weak bounded selector effect
            barnard_weight = float(np.clip(barnard_weight, 0.95, 1.05))
            edge1 = edges[edges["pair"] == pid1]
            edge2 = edges[edges["pair"] == pid2]
            m_conflict = bool((edge1["mersenne_conflict_flag"].any()) or (edge2["mersenne_conflict_flag"].any()))

            base = (0.35 * (c1 + c2) + 0.35 * (s1 + s2) + 0.20 * float(coherent) + 0.10 * float(has_contact_any))
            penalty = 0.15 * float(m_conflict) + 0.10  # chain-length penalty for 2-hop
            score = (base - penalty) * barnard_weight
            score -= 0.20 if (c1 <= 0 and c2 <= 0) else 0.0

            motif = "triangle" if pair_id(a, c) in set(edges["pair"]) else "hinge"
            verified = has_nonproj_each_hop and has_contact_any and coherent
            relays.append(
                {
                    "from_sheet": a,
                    "mediator_sheet": b,
                    "to_sheet": c,
                    "hop1_pair": pid1,
                    "hop2_pair": pid2,
                    "motif": motif,
                    "hop1_contact": c1,
                    "hop2_contact": c2,
                    "hop1_saddle": s1,
                    "hop2_saddle": s2,
                    "has_nonproj_each_hop": bool(has_nonproj_each_hop),
                    "has_contact_any_hop": bool(has_contact_any),
                    "local_coherent": bool(coherent),
                    "coherence_metric": coh_metric,
                    "mersenne_conflict_flag": bool(m_conflict),
                    "barnard_weight": barnard_weight,
                    "relay_score": float(score),
                    "verified": bool(verified),
                    "failure_reason": "" if verified else "relay_requirements_not_met",
                }
            )

    relay_df = pd.DataFrame(relays)
    if relay_df.empty:
        relay_df = pd.DataFrame(
            columns=[
                "from_sheet",
                "mediator_sheet",
                "to_sheet",
                "hop1_pair",
                "hop2_pair",
                "motif",
                "relay_score",
                "verified",
                "failure_reason",
            ]
        )

    relay_df = relay_df.sort_values("relay_score", ascending=False)
    verified_df = relay_df[relay_df["verified"] == True].copy()  # noqa: E712
    failed_df = relay_df[relay_df["verified"] == False].copy()  # noqa: E712

    # mode-conditioned
    mode_rows = []
    for r in relay_df.itertuples(index=False):
        modes = mode_coherence(cloud, r.from_sheet, r.mediator_sheet, r.to_sheet)
        if not modes:
            mode_rows.append(
                {
                    "from_sheet": r.from_sheet,
                    "mediator_sheet": r.mediator_sheet,
                    "to_sheet": r.to_sheet,
                    "mode_id": "none",
                    "mode_relay_coherent": False,
                    "coherence_metric": np.nan,
                }
            )
        else:
            for m in modes:
                mode_rows.append(
                    {
                        "from_sheet": r.from_sheet,
                        "mediator_sheet": r.mediator_sheet,
                        "to_sheet": r.to_sheet,
                        "mode_id": m["mode_id"],
                        "mode_relay_coherent": bool(m["coherent"]),
                        "coherence_metric": m["coherence_metric"],
                    }
                )
    mode_df = pd.DataFrame(mode_rows)

    # domain-conditioned
    dom_rows = []
    for r in relay_df.itertuples(index=False):
        d = domain_coherence(cloud, r.from_sheet, r.mediator_sheet, r.to_sheet)
        dom_rows.append(
            {
                "from_sheet": r.from_sheet,
                "mediator_sheet": r.mediator_sheet,
                "to_sheet": r.to_sheet,
                "domain_continuity": bool(d["domain_continuity"]),
                "domain_pairs_ok": int(d["domain_pairs_ok"]),
                "domain_pairs_total": int(d["domain_pairs_total"]),
            }
        )
    dom_df = pd.DataFrame(dom_rows)

    # component reduction from verified relays
    groups = [[y.strip() for y in str(x).split("|") if y.strip()] for x in comps["member_nodes"].astype(str)]
    dsu = DSU.from_groups(groups)
    before = dsu.components()
    applied = 0
    for r in verified_df.itertuples(index=False):
        a, c = r.from_sheet, r.to_sheet
        if a not in dsu.parent:
            dsu.parent[a] = a
        if c not in dsu.parent:
            dsu.parent[c] = c
        if dsu.union(a, c):
            applied += 1
    after = dsu.components()

    # best mediator
    best_mediator = "none"
    if not verified_df.empty:
        cts = verified_df["mediator_sheet"].value_counts()
        best_mediator = str(cts.index[0])

    mode_exists = bool((mode_df["mode_relay_coherent"] == True).any()) if not mode_df.empty else False  # noqa: E712
    dom_exists = bool((dom_df["domain_continuity"] == True).any()) if not dom_df.empty else False  # noqa: E712

    relay_df.to_csv(OUTDIR / "relay_candidates.csv", index=False)
    verified_df.to_csv(OUTDIR / "relay_verified.csv", index=False)
    failed_df.to_csv(OUTDIR / "relay_failed.csv", index=False)
    mode_df.to_csv(OUTDIR / "mode_conditioned_relays.csv", index=False)
    dom_df.to_csv(OUTDIR / "domain_conditioned_relays.csv", index=False)

    summary = {
        "true_components_before": int(before),
        "true_components_after_relay_verification": int(after),
        "component_reduction": int(before - after),
        "relay_candidates": int(len(relay_df)),
        "relay_verified": int(len(verified_df)),
        "relay_failed": int(len(failed_df)),
        "best_relay_mediator_sheet": best_mediator,
        "mode_conditioned_relay_exists": mode_exists,
        "domain_conditioned_relay_exists": dom_exists,
        "direct_pairwise_glue_absent": True,
        "mediated_glue_present": bool(len(verified_df) > 0 and (before - after) > 0),
        "barnard_selector_only": True,
    }
    (OUTDIR / "component_reduction_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    report = f"""# SEAM_RELAY_OPERATOR_V1_REPORT

## 1) Why direct pairwise gluing failed
- Pairwise local-path verification in v2 yielded zero verified edges after pair-level contamination bans.

## 2) Whether any mediated relay exists
- Relay candidates tested: {len(relay_df)}
- Relay verified: {len(verified_df)}
- Component reduction from relay application: {before - after}

## 3) Best relay mediator
- Best mediator sheet: {best_mediator}

## 4) Mode-conditioned relay
- Mode-conditioned coherent relay exists: {mode_exists}

## 5) Domain-conditioned relay
- Domain-conditioned continuity exists: {dom_exists}

## 6) Explicit conclusion
- direct glue absent: True
- mediated glue present: {summary["mediated_glue_present"]}
- if absent, next step coordinate-lift / atlas refinement: {not summary["mediated_glue_present"]}

## Interpretation mapping
- Big Man = Barnard selector only
- Big Woman = contamination shell / exclusion laws
- Small Man = real relay seam if found
- Small Woman = projection overlap trap / fake center coincidence
"""
    (OUTDIR / "SEAM_RELAY_OPERATOR_V1_REPORT.md").write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
