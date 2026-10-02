from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from geometry_package.absolute_constants import GABA_C_V_APEX, TUNNEL_TENSION


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "seam_pair_operator_test"


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

    def count_components(self) -> int:
        roots = {self.find(x) for x in self.parent}
        return len(roots)


def parse_nodes(member_nodes: str) -> list[str]:
    return [m.strip() for m in str(member_nodes).split("|") if m.strip()]


def normalize_series(x: pd.Series) -> pd.Series:
    v = pd.to_numeric(x, errors="coerce").fillna(0.0)
    lo, hi = v.min(), v.max()
    if hi <= lo:
        return pd.Series(np.ones(len(v)), index=v.index)
    return (v - lo) / (hi - lo)


def barnard_weight_from_row(row: pd.Series) -> float:
    # Selector-only modulation, clamped to [0.9, 1.1]
    base = 1.0
    if bool(row.get("barnard_reweight_candidate", False)):
        base += 0.05
    if bool(row.get("mersenne_conflict_flag", False)):
        base -= 0.05
    return float(np.clip(base, 0.9, 1.1))


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    seam_df = pd.read_csv(ROOT / "seam_failure_table.csv")
    conn_df = pd.read_csv(ROOT / "out" / "connectivity_audit" / "connectivity_graph.csv")
    comps_df = pd.read_csv(ROOT / "out" / "connectivity_audit" / "disconnected_components.csv")
    barnard_df = pd.read_csv(ROOT / "barnard_reweight_candidates.csv")
    tunnel_json = json.loads(
        (ROOT / "moveout" / "tunnel_verification_knn" / "tunnel_verification_results.json").read_text(
            encoding="utf-8"
        )
    )
    _ = conn_df, barnard_df, tunnel_json  # explicit load per requirement

    # A) strict row filter
    work = seam_df[
        (seam_df["final_verdict"] == "candidate_for_barnard_reweighting")
        & (seam_df["tunnel_status"] != "blocked")
        & (seam_df["projection_overlap_flag"] == False)  # noqa: E712
    ].copy()
    work = work[
        (~work["seam_a"].astype(str).str.contains("sheet_id:2"))
        & (~work["seam_b"].astype(str).str.contains("sheet_id:2"))
    ].copy()

    if work.empty:
        raise RuntimeError("No valid candidate seams after hard constraints.")

    # B) ranking score
    contact_norm = normalize_series(work["contact_score"])
    work["rank_score"] = (
        0.45 * contact_norm
        + 0.35 * work["percolation_candidate_flag"].astype(float)
        + 0.20 * work["barnard_reweight_candidate"].astype(float)
        - 0.50 * work["mersenne_conflict_flag"].astype(float)
    )
    work = work.sort_values("rank_score", ascending=False).head(10).copy()  # C) top 10

    # Build baseline components from disconnected_components.csv
    component_groups = [parse_nodes(mn) for mn in comps_df["member_nodes"].astype(str)]
    baseline_nodes = sorted({n for g in component_groups for n in g})
    dsu = DSU.from_nodes(baseline_nodes)
    for g in component_groups:
        if len(g) > 1:
            root = g[0]
            for n in g[1:]:
                dsu.union(root, n)
    before = dsu.count_components()

    # D) local seam operator from threshold logic
    # base_gain inferred from existing threshold relation
    base_gain = float(np.clip(GABA_C_V_APEX / TUNNEL_TENSION, 0.01, 1.0))
    verify_threshold = float(np.clip(GABA_C_V_APEX * 0.5, 0.05, 0.2))

    results = []
    verified = []
    failed = []

    for _, row in work.iterrows():
        a = str(row["seam_a"])
        b = str(row["seam_b"])

        if a not in dsu.parent:
            dsu.parent[a] = a
        if b not in dsu.parent:
            dsu.parent[b] = b

        bw = barnard_weight_from_row(row)
        contact_weight = float(np.clip(float(row["contact_score"]), 0.0, 1.0))
        saddle_weight = 1.0 + 0.1 * float(bool(row["percolation_candidate_flag"]))
        seam_gain = base_gain * bw * contact_weight * saddle_weight

        comp_before = dsu.count_components()
        can_union = seam_gain >= verify_threshold
        reduced = False
        reason = ""
        if can_union:
            reduced = dsu.union(a, b)
            if not reduced:
                reason = "already_same_component"
        else:
            reason = f"gain_below_threshold:{seam_gain:.6f}<{verify_threshold:.6f}"

        comp_after = dsu.count_components()
        rec = {
            "seam_a": a,
            "seam_b": b,
            "rank_score": float(row["rank_score"]),
            "base_gain": base_gain,
            "barnard_weight": bw,
            "contact_weight": contact_weight,
            "saddle_weight": saddle_weight,
            "seam_gain": seam_gain,
            "verify_threshold": verify_threshold,
            "component_count_before": comp_before,
            "component_count_after": comp_after,
            "component_reduced": bool(comp_after < comp_before),
            "verification_status": "verified" if comp_after < comp_before else "failed",
            "failure_reason": reason,
        }
        results.append(rec)
        if rec["verification_status"] == "verified":
            verified.append(rec)
        else:
            failed.append(rec)

    results_df = pd.DataFrame(results)
    verified_df = pd.DataFrame(verified)
    failed_df = pd.DataFrame(failed)

    results_df.to_csv(OUTDIR / "seam_pair_results.csv", index=False)
    verified_df.to_csv(OUTDIR / "verified_gluing_edges.csv", index=False)
    failed_df.to_csv(OUTDIR / "failed_gluing_edges.csv", index=False)

    after = dsu.count_components()
    summary = {
        "true_components_before": int(before),
        "true_components_after_candidate_reweighting": int(after),
        "component_reduction": int(before - after),
        "top10_candidates_evaluated": int(len(results_df)),
        "verified_edges_count": int(len(verified_df)),
        "failed_edges_count": int(len(failed_df)),
        "blocked_sheet_enforced": "sheet_id:2",
        "selector_rules": {
            "barnard_role": "selector_and_gain_modulator_only",
            "bridge_creator": False,
            "projection_overlap_promoted": False,
        },
    }
    (OUTDIR / "component_reduction_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    best = (
        "none"
        if results_df.empty
        else f"{results_df.iloc[0]['seam_a']}<->{results_df.iloc[0]['seam_b']}"
    )
    best_failed = (
        "none"
        if failed_df.empty
        else f"{failed_df.iloc[0]['seam_a']}<->{failed_df.iloc[0]['seam_b']} ({failed_df.iloc[0]['failure_reason']})"
    )
    report = f"""# SEAM_PAIR_OPERATOR_REPORT

## Scientific verdict
- Components before: {before}
- Components after: {after}
- Reduction: {before - after}
- Barnard role: selector and bounded gain modulator only (`barnard_weight in [0.9,1.1]`)
- Barnard bridge creation: disabled
- Hard block preserved: `gateway_peak -> sheet_id:2` excluded by rule
- Projection overlaps: excluded by rule

## Best seam outcomes
- Top ranked seam: {best}
- Best failed seam: {best_failed}

## Interpretation mapping
- Big Man: external seam selector/gain modulator (Barnard), not bridge law.
- Big Woman: shell-level constraints and conflicts (including 1D-only solenoid evidence).
- Small Man: local seam recipient where pairwise operator is tested.
- Small Woman: projection-overlap trap excluded from gluing promotion.
"""
    (OUTDIR / "SEAM_PAIR_OPERATOR_REPORT.md").write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
