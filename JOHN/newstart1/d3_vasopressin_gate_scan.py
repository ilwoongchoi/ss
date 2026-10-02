from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "d3_vasopressin_gate_scan"
LEFT = {"sheet_id:3", "sheet_id:4"}
RIGHT = {"sheet_id:10", "sheet_id:12", "sheet_id:13"}


def pair_id(a: str, b: str) -> str:
    a = str(a)
    b = str(b)
    return "__".join(sorted([a, b]))


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


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    seams = pd.read_csv(ROOT / "out" / "seam_local_atlas_lift_v2" / "corrected_lifted_local_seams.csv")
    reduction = json.loads(
        (ROOT / "out" / "seam_local_atlas_lift_v2" / "corrected_component_reduction.json").read_text(encoding="utf-8")
    )
    audit = pd.read_csv(ROOT / "out" / "seam_local_atlas_lift_v2" / "spine_bridge_audit.csv")
    comps = pd.read_csv(ROOT / "out" / "connectivity_audit" / "disconnected_components.csv")

    d3_values = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]

    # Cross-spine candidates only
    cross = seams[
        ((seams["sheet_a"].isin(LEFT) & seams["sheet_b"].isin(RIGHT)) |
         (seams["sheet_b"].isin(LEFT) & seams["sheet_a"].isin(RIGHT)))
    ].copy()

    # Banned/trap info from audit + failure_reason
    trap_pairs = set(
        audit[audit["failure_category"].str.contains("projection|trap|loss", na=False)]["pair"].tolist()
    )

    if "barnard_weight" not in cross.columns:
        cross["barnard_weight"] = 1.0

    cross["pair"] = cross.apply(lambda r: pair_id(r["sheet_a"], r["sheet_b"]), axis=1)
    cross["trap_penalty"] = (~cross["pair"].isin(trap_pairs)).astype(float)
    cross["base_support"] = 0.55 * cross["contact_support"] + 0.45 * cross["saddle_support"]
    cross["distance_penalty"] = 1.0 / (1.0 + cross["lifted_distance"])

    # Threshold from top decile of existing cross-spine glue scores at d3=1.0
    if cross.empty:
        raw_scores = pd.Series(dtype=float)
    else:
        raw_scores = (
            cross["base_support"] * cross["distance_penalty"] * cross["barnard_weight"] * cross["trap_penalty"]
        )
    if len(raw_scores) == 0:
        threshold = 0.0
    else:
        threshold = float(np.quantile(raw_scores, 0.9))

    score_rows = []
    component_rows = []

    groups = [[y.strip() for y in str(x).split("|") if y.strip()] for x in comps["member_nodes"].astype(str)]
    for d3 in d3_values:
        vasopressin_gate = d3
        cross["glue_score"] = (
            cross["base_support"]
            * cross["distance_penalty"]
            * vasopressin_gate
            * cross["barnard_weight"]
            * cross["trap_penalty"]
        )

        cross["verified_d3_bridge"] = (cross["glue_score"] > threshold) & (cross["trap_penalty"] > 0)

        # component recompute with verified edges only
        dsu = DSU.from_groups(groups)
        before = dsu.components()
        applied = 0
        for r in cross[cross["verified_d3_bridge"]].itertuples(index=False):
            a = str(r.sheet_a)
            b = str(r.sheet_b)
            if a not in dsu.parent:
                dsu.parent[a] = a
            if b not in dsu.parent:
                dsu.parent[b] = b
            if dsu.union(a, b):
                applied += 1
        after = dsu.components()

        for r in cross.itertuples(index=False):
            if r.trap_penalty <= 0:
                rej = "small_woman_trap"
            elif r.glue_score <= threshold:
                rej = "below_threshold"
            else:
                rej = ""
            score_rows.append(
                {
                    "left_sheet": r.sheet_a if r.sheet_a in LEFT else r.sheet_b,
                    "right_sheet": r.sheet_b if r.sheet_b in RIGHT else r.sheet_a,
                    "d3_gate": d3,
                    "contact_support": float(r.contact_support),
                    "saddle_support": float(r.saddle_support),
                    "lifted_distance": float(r.lifted_distance),
                    "base_support": float(r.base_support),
                    "glue_score": float(r.glue_score),
                    "verified_d3_bridge": bool(r.verified_d3_bridge),
                    "rejection_reason": rej,
                }
            )

        component_rows.append(
            {
                "d3_gate": d3,
                "components_before": int(before),
                "components_after": int(after),
                "reduction": int(before - after),
                "verified_cross_spine_edges": int(applied),
            }
        )

    score_df = pd.DataFrame(score_rows)
    comp_df = pd.DataFrame(component_rows)

    if score_df.empty:
        score_df = pd.DataFrame(
            columns=[
                "left_sheet",
                "right_sheet",
                "d3_gate",
                "contact_support",
                "saddle_support",
                "lifted_distance",
                "base_support",
                "glue_score",
                "verified_d3_bridge",
                "rejection_reason",
            ]
        )
    score_df.to_csv(OUTDIR / "d3_gate_scan_scores.csv", index=False)
    comp_df.to_csv(OUTDIR / "d3_gate_component_scan.csv", index=False)

    # Report
    if "d3_gate" not in score_df.columns or score_df.empty:
        any_bridge_high = False
    else:
        any_bridge_high = bool(
            (score_df[(score_df["d3_gate"] == 1.0) & (score_df["verified_d3_bridge"])]).any().any()
        )
    monotonic = comp_df["reduction"].is_monotonic_decreasing
    if not any_bridge_high:
        verdict = "D3-gate is not sufficient; obstruction remains elsewhere"
    else:
        verdict = "D3-gate is sufficient to explain corridor gluing failure"

    report = f"""# D3_VASOPRESSIN_GLUE_REPORT

Threshold (top decile cross-spine at d3=1.0): {threshold:.6f}
Cross-spine candidate seams: {int(len(cross))}

A. Any 10/12/13 -> 3/4 bridge at high d3_gate? {any_bridge_high}
B. Bridge collapses monotonically as d3_gate goes down? {monotonic}
C. If none at d3=1.0: D3 deactivation alone is insufficient.
D. Interpretations:
- scientific: upstream neuromodulatory gate failure
- framework: Big Man weak / Big Woman shell / Small Man seam / Small Woman trap

Verdict: {verdict}
"""
    (OUTDIR / "D3_VASOPRESSIN_GLUE_REPORT.md").write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
