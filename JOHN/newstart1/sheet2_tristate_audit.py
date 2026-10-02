"""
Sheet-2 Tri-State Edge Audit

Strict edge model with 5 classes:
1. direct_gateway_blocked - tunnel/shell blocks direct connection
2. local_pairwise_viable - direct seam viable without relay
3. projection_only - projection overlap but no lifted seam
4. relay_mediated - requires indirect path via mediator
5. fully_lifted_glue - has lifted local seam support

Distinguishes raw 11-component baseline from relay-collapsed 7-component baseline.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "sheet2_tristate_audit"

GLOBAL_BLOCKER = "sheet_id:2"
ALL_SHEETS = ["sheet_id:2", "sheet_id:3", "sheet_id:4", "sheet_id:10", "sheet_id:11", 
              "sheet_id:12", "sheet_id:13", "sheet_id:14"]


class EdgeState(Enum):
    """Five-class edge state model."""
    DIRECT_GATEWAY_BLOCKED = "direct_gateway_blocked"
    LOCAL_PAIRWISE_VIABLE = "local_pairwise_viable"
    PROJECTION_ONLY = "projection_only"
    RELAY_MEDIATED = "relay_mediated"
    FULLY_LIFTED_GLUE = "fully_lifted_glue"


@dataclass
class DSU:
    """Disjoint Set Union for component tracking."""
    parent: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def from_groups(cls, groups: List[List[str]]) -> "DSU":
        nodes = sorted({n for g in groups for n in g if n})
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
    
    def would_reduce(self, a: str, b: str) -> bool:
        """Check if adding edge would reduce component count."""
        return self.find(a) != self.find(b)
    
    def get_component_members(self, node: str) -> Set[str]:
        """Get all members of the component containing node."""
        root = self.find(node)
        return {n for n in self.parent if self.find(n) == root}


@dataclass
class TriStateEdge:
    """Edge with tri-state classification."""
    pair: str
    sheet_a: str
    sheet_b: str
    
    # Scores
    glue_score: float
    
    # Verification layers
    lifted_pass: bool
    relay_exists: bool
    relay_mediator: Optional[str]
    tunnel_pass: bool
    
    # Topology under both baselines
    topology_reduction_raw11: bool
    topology_reduction_relay7: bool
    
    # Classification
    final_edge_state: EdgeState
    
    # Metadata
    config_key: str = ""  # For deduplication
    prior_blocked: bool = False


def pair_id(a: str, b: str) -> str:
    return "__".join(sorted([str(a), str(b)]))


def load_source_data():
    """Load all source data."""
    possible_roots = [
        ROOT / "out",
        ROOT / "left_akg_extract" / "out",
        ROOT / "akg_spine_extract" / "out",
        ROOT / ".." / "out",
        ROOT / "out" / "sheet2_counterfactual",
    ]
    
    def find_file(subpath: str) -> Optional[Path]:
        for pr in possible_roots:
            p = pr / subpath
            if p.exists():
                return p
        return None
    
    paths = {
        "lifted": find_file("seam_local_atlas_lift_v2/corrected_lifted_local_seams.csv"),
        "relay": find_file("seam_relay_operator_test_v1/relay_verified.csv"),
        "conn": find_file("connectivity_audit/connectivity_graph.csv"),
        "comp": find_file("connectivity_audit/disconnected_components.csv"),
        "audit": find_file("seam_local_atlas_lift_v2/spine_bridge_audit.csv"),
        "counterfactual": find_file("sheet2_counterfactual/sheet2_counterfactual_candidates.csv"),
    }
    
    data = {}
    for name, path in paths.items():
        if path and path.exists():
            data[name] = pd.read_csv(path)
            print(f"  Loaded {name}: {len(data[name])} rows")
        else:
            print(f"  Warning: {name} not found at {path}")
            data[name] = pd.DataFrame()
    
    return data


def build_baselines(comp_df: pd.DataFrame, relay_df: pd.DataFrame) -> Tuple[DSU, DSU]:
    """
    Build two DSU baselines:
    1. Raw 11-component baseline (from disconnected_components)
    2. Relay-collapsed 7-component baseline (after applying verified relays)
    """
    # Raw 11-component baseline
    if not comp_df.empty and "member_nodes" in comp_df.columns:
        raw_groups = [[y.strip() for y in str(x).split("|") if y.strip()] 
                     for x in comp_df["member_nodes"].astype(str)]
    else:
        raw_groups = [[s] for s in ALL_SHEETS]
    
    dsu_raw11 = DSU.from_groups(raw_groups)
    print(f"  Raw baseline: {dsu_raw11.components()} components")
    
    # Relay-collapsed 7-component baseline
    dsu_relay7 = DSU.from_groups(raw_groups)
    
    if not relay_df.empty and "from_sheet" in relay_df.columns:
        for r in relay_df.itertuples(index=False):
            from_s = str(r.from_sheet)
            to_s = str(r.to_sheet)
            mediator = str(r.mediator_sheet)
            
            # Union all three in relay path
            dsu_relay7.union(from_s, mediator)
            dsu_relay7.union(mediator, to_s)
    
    print(f"  Relay-collapsed baseline: {dsu_relay7.components()} components")
    
    return dsu_raw11, dsu_relay7


def get_sheet2_pairs_from_counterfactual(counter_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract unique sheet_id:2 pairs from counterfactual results.
    Deduplicate by pair + config.
    """
    if counter_df.empty:
        return pd.DataFrame()
    
    # Filter to rows with sheet_id:2 candidates
    sheet2_rows = counter_df[counter_df["sheet2_selected_count"] > 0].copy()
    
    if sheet2_rows.empty:
        return pd.DataFrame()
    
    # Get best score per pair
    # First, reconstruct pair from top_sheet2_pair column
    results = []
    
    for _, row in sheet2_rows.iterrows():
        pair = row.get("top_sheet2_pair", "")
        if not pair or pd.isna(pair):
            continue
        
        # Parse sheets from pair
        sheets = pair.split("__")
        if len(sheets) != 2:
            continue
        
        sheet_a, sheet_b = sheets
        
        # Build config key for deduplication
        config_key = f"akg={row.get('akg_spine', 0)}_d3={row.get('d3_gate', 0)}"
        
        results.append({
            "pair": pair,
            "sheet_a": sheet_a,
            "sheet_b": sheet_b,
            "glue_score": row.get("top_sheet2_score", 0),
            "config_key": config_key,
            "threshold_mode": row.get("threshold_mode", ""),
            "threshold_value": row.get("threshold_value", 0),
        })
    
    df = pd.DataFrame(results)
    if df.empty:
        return df
    
    # Deduplicate by pair + config_key, keep highest score
    df = df.sort_values("glue_score", ascending=False)
    df = df.drop_duplicates(subset=["pair", "config_key"], keep="first")
    
    print(f"  Extracted {len(df)} unique sheet_id:2 pair configs")
    return df


def run_verification_layers(
    pair: str, sheet_a: str, sheet_b: str,
    lifted_df: pd.DataFrame, relay_df: pd.DataFrame, 
    conn_df: pd.DataFrame, audit_df: pd.DataFrame
) -> Tuple[bool, bool, Optional[str], bool]:
    """
    Run 4 verification layers, return (lifted_pass, relay_exists, relay_mediator, tunnel_pass).
    """
    # Layer 1: Lifted local seam check
    lifted_pass = False
    if not lifted_df.empty and "sheet_a" in lifted_df.columns:
        lifted_df = lifted_df.copy()
        lifted_df["pair"] = lifted_df.apply(lambda r: pair_id(r["sheet_a"], r["sheet_b"]), axis=1)
        match = lifted_df[lifted_df["pair"] == pair]
        if not match.empty:
            row = match.iloc[0]
            contact = float(row.get("contact_support", 0.0))
            saddle = float(row.get("saddle_support", 0.0))
            lifted_pass = (contact > 0) or (saddle > 0)
    
    # Layer 2: Relay path check
    relay_exists = False
    relay_mediator = None
    
    if not relay_df.empty and "from_sheet" in relay_df.columns:
        for r in relay_df.itertuples(index=False):
            from_s = str(r.from_sheet)
            to_s = str(r.to_sheet)
            med = str(r.mediator_sheet)
            
            # Check if this relay connects our sheets
            if {sheet_a, sheet_b} <= {from_s, to_s, med}:
                relay_exists = True
                relay_mediator = med
                break
    
    if not relay_exists and not conn_df.empty:
        # Check for projection_overlap as indirect path
        conn_match = conn_df[
            ((conn_df["source_node"] == sheet_a) & (conn_df["target_node"] == sheet_b)) |
            ((conn_df["source_node"] == sheet_b) & (conn_df["target_node"] == sheet_a))
        ]
        proj = conn_match[conn_match["edge_type"] == "projection_overlap"]
        if not proj.empty:
            relay_exists = True
            relay_mediator = "projection_overlap"
    
    # Layer 3: Tunnel check
    tunnel_pass = True
    
    if not conn_df.empty:
        conn_match = conn_df[
            ((conn_df["source_node"] == sheet_a) & (conn_df["target_node"] == sheet_b)) |
            ((conn_df["source_node"] == sheet_b) & (conn_df["target_node"] == sheet_a))
        ]
        tunnel_blocked = conn_match[conn_match["edge_type"] == "tunnel_blocked"]
        if not tunnel_blocked.empty:
            tunnel_pass = False
    
    if not audit_df.empty and "pair" in audit_df.columns:
        audit_match = audit_df[audit_df["pair"] == pair]
        if not audit_match.empty:
            fail_cat = str(audit_match.iloc[0].get("failure_category", ""))
            if "tunnel" in fail_cat.lower() or "blocked" in fail_cat.lower():
                tunnel_pass = False
    
    return lifted_pass, relay_exists, relay_mediator, tunnel_pass


def classify_edge_state(
    lifted_pass: bool,
    relay_exists: bool,
    tunnel_pass: bool,
    reduces_raw11: bool,
    reduces_relay7: bool
) -> EdgeState:
    """
    Classify edge into one of 5 states:
    1. direct_gateway_blocked - tunnel fails
    2. fully_lifted_glue - lifted_pass + reduces topology
    3. local_pairwise_viable - no lifted but tunnel passes and reduces
    4. relay_mediated - needs relay to reduce
    5. projection_only - has projection but doesn't reduce
    """
    if not tunnel_pass:
        return EdgeState.DIRECT_GATEWAY_BLOCKED
    
    if lifted_pass and reduces_raw11:
        return EdgeState.FULLY_LIFTED_GLUE
    
    if reduces_raw11:
        # Reduces without lifted seam = local pairwise viable
        return EdgeState.LOCAL_PAIRWISE_VIABLE
    
    if relay_exists and reduces_relay7:
        # Needs relay to reduce
        return EdgeState.RELAY_MEDIATED
    
    if relay_exists and not reduces_relay7:
        # Has projection/relay but still doesn't reduce
        return EdgeState.PROJECTION_ONLY
    
    # Default: projection_only (has some overlap but not viable)
    return EdgeState.PROJECTION_ONLY


def run_tristate_audit() -> pd.DataFrame:
    """Run full tri-state audit."""
    print("=" * 60)
    print("SHEET-2 TRI-STATE EDGE AUDIT")
    print("=" * 60)
    print()
    
    # Load data
    print("Loading source data...")
    data = load_source_data()
    
    # Build baselines
    print("\nBuilding DSU baselines...")
    dsu_raw11, dsu_relay7 = build_baselines(data["comp"], data["relay"])
    
    # Get sheet_id:2 pairs from counterfactual
    print("\nExtracting sheet_id:2 pairs...")
    pairs_df = get_sheet2_pairs_from_counterfactual(data["counterfactual"])
    
    if pairs_df.empty:
        print("No sheet_id:2 pairs found")
        return pd.DataFrame()
    
    # Run verification and classification
    print(f"\nRunning verification on {len(pairs_df)} pair configs...")
    edges = []
    
    for _, row in pairs_df.iterrows():
        pair = row["pair"]
        sheet_a = row["sheet_a"]
        sheet_b = row["sheet_b"]
        
        # Run verification layers
        lifted_pass, relay_exists, relay_mediator, tunnel_pass = run_verification_layers(
            pair, sheet_a, sheet_b,
            data["lifted"], data["relay"], data["conn"], data["audit"]
        )
        
        # Compute topology reduction under both baselines
        dsu_raw_test = DSU.from_groups([[n for n in ALL_SHEETS]])
        dsu_raw_test.parent = dsu_raw11.parent.copy()
        reduces_raw11 = dsu_raw_test.would_reduce(sheet_a, sheet_b)
        
        dsu_relay_test = DSU.from_groups([[n for n in ALL_SHEETS]])
        dsu_relay_test.parent = dsu_relay7.parent.copy()
        reduces_relay7 = dsu_relay_test.would_reduce(sheet_a, sheet_b)
        
        # Classify edge state
        edge_state = classify_edge_state(
            lifted_pass, relay_exists, tunnel_pass,
            reduces_raw11, reduces_relay7
        )
        
        edge = TriStateEdge(
            pair=pair,
            sheet_a=sheet_a,
            sheet_b=sheet_b,
            glue_score=row["glue_score"],
            lifted_pass=lifted_pass,
            relay_exists=relay_exists,
            relay_mediator=relay_mediator,
            tunnel_pass=tunnel_pass,
            topology_reduction_raw11=reduces_raw11,
            topology_reduction_relay7=reduces_relay7,
            final_edge_state=edge_state,
            config_key=row["config_key"],
        )
        edges.append(edge)
    
    # Convert to DataFrame
    results = []
    for e in edges:
        results.append({
            "pair": e.pair,
            "glue_score": e.glue_score,
            "lifted_pass": e.lifted_pass,
            "relay_exists": e.relay_exists,
            "relay_mediator": e.relay_mediator or "",
            "tunnel_pass": e.tunnel_pass,
            "topology_reduction_raw11": e.topology_reduction_raw11,
            "topology_reduction_relay7": e.topology_reduction_relay7,
            "final_edge_state": e.final_edge_state.value,
            "config_key": e.config_key,
        })
    
    return pd.DataFrame(results)


def generate_state_summary(df: pd.DataFrame) -> str:
    """Generate summary of edge state distribution."""
    if df.empty:
        return "No data available"
    
    state_counts = df["final_edge_state"].value_counts()
    total = len(df)
    
    summary = []
    for state in EdgeState:
        count = state_counts.get(state.value, 0)
        pct = 100 * count / total if total > 0 else 0
        summary.append(f"  {state.value}: {count} ({pct:.1f}%)")
    
    return "\n".join(summary)


def generate_summary_report(df: pd.DataFrame) -> str:
    """Generate final summary report answering: 'Is sheet_id:2 globally blocked, locally viable, or lift-missing?'"""
    
    if df.empty:
        return "# Sheet-2 Tri-State Audit Report\n\nNo data available."
    
    # Aggregate by pair (best score per pair)
    pair_best = df.loc[df.groupby("pair")["glue_score"].idxmax()]
    
    # Count by state
    state_counts = pair_best["final_edge_state"].value_counts()
    total_pairs = len(pair_best)
    
    # Determine overall status
    blocked_count = state_counts.get(EdgeState.DIRECT_GATEWAY_BLOCKED.value, 0)
    viable_count = state_counts.get(EdgeState.LOCAL_PAIRWISE_VIABLE.value, 0) + \
                   state_counts.get(EdgeState.FULLY_LIFTED_GLUE.value, 0)
    lift_missing_count = state_counts.get(EdgeState.PROJECTION_ONLY.value, 0) + \
                        state_counts.get(EdgeState.RELAY_MEDIATED.value, 0)
    
    # Determine primary status
    if blocked_count == total_pairs:
        primary_status = "GLOBALLY BLOCKED"
        status_desc = "All sheet_id:2 pairs are direct_gateway_blocked (tunnel/shell obstruction)"
    elif viable_count > 0:
        primary_status = "LOCALLY VIABLE"
        status_desc = f"{viable_count}/{total_pairs} sheet_id:2 pairs can bridge directly"
    elif lift_missing_count > 0:
        primary_status = "LIFT-MISSING"
        status_desc = f"{lift_missing_count}/{total_pairs} pairs lack lifted continuity but have projection/relay potential"
    else:
        primary_status = "UNDETERMINED"
        status_desc = "Mixed or unclear status"
    
    report = f"""# Sheet-2 Tri-State Audit Report

## Executive Summary

**Question**: Is sheet_id:2 globally blocked, locally viable, or lift-missing?

**Answer**: {primary_status}

{status_desc}

---

## Edge State Distribution (by unique pair, best config)

| State | Count | Percentage | Description |
|-------|-------|------------|-------------|
| direct_gateway_blocked | {state_counts.get(EdgeState.DIRECT_GATEWAY_BLOCKED.value, 0)} | {100*state_counts.get(EdgeState.DIRECT_GATEWAY_BLOCKED.value, 0)/total_pairs:.1f}% | Tunnel/shell blocks direct connection |
| local_pairwise_viable | {state_counts.get(EdgeState.LOCAL_PAIRWISE_VIABLE.value, 0)} | {100*state_counts.get(EdgeState.LOCAL_PAIRWISE_VIABLE.value, 0)/total_pairs:.1f}% | Direct seam viable without relay |
| fully_lifted_glue | {state_counts.get(EdgeState.FULLY_LIFTED_GLUE.value, 0)} | {100*state_counts.get(EdgeState.FULLY_LIFTED_GLUE.value, 0)/total_pairs:.1f}% | Has lifted local seam support |
| relay_mediated | {state_counts.get(EdgeState.RELAY_MEDIATED.value, 0)} | {100*state_counts.get(EdgeState.RELAY_MEDIATED.value, 0)/total_pairs:.1f}% | Requires indirect path via mediator |
| projection_only | {state_counts.get(EdgeState.PROJECTION_ONLY.value, 0)} | {100*state_counts.get(EdgeState.PROJECTION_ONLY.value, 0)/total_pairs:.1f}% | Projection overlap but no lifted seam |

**Total unique pairs**: {total_pairs}

---

## Topology Reduction Analysis

### Raw 11-Component Baseline
Edges reducing topology: {pair_best["topology_reduction_raw11"].sum()}/{total_pairs}

### Relay-Collapsed 7-Component Baseline
Edges reducing topology: {pair_best["topology_reduction_relay7"].sum()}/{total_pairs}

---

## Detailed Pair Analysis

| Pair | Score | Lifted | Relay | Tunnel | Reduces (11) | Reduces (7) | State |
|------|-------|--------|-------|--------|--------------|-------------|-------|
"""
    
    for _, row in pair_best.sort_values("glue_score", ascending=False).iterrows():
        report += f"| {row['pair']} | {row['glue_score']:.3f} | {row['lifted_pass']} | {row['relay_exists']} | {row['tunnel_pass']} | {row['topology_reduction_raw11']} | {row['topology_reduction_relay7']} | {row['final_edge_state']} |\n"
    
    report += """
---

## Framework Translation

### Scientific Frame

**Global Blocker Hypothesis**: sheet_id:2 prevents full topology closure
- Evidence: """ + ("Strong - all pairs blocked" if blocked_count == total_pairs else 
              "Weak - some pairs viable" if viable_count > 0 else 
              "Mixed - projection-only gaps") + """

**Local Viability**: Direct sheet_id:2 seams exist
- Evidence: """ + (f"{viable_count} pairs reduce topology under raw 11-comp baseline" if viable_count > 0 else "No direct seams verified") + """

**Lifted Continuity Gap**: Missing high-quality local seams
- Evidence: """ + (f"{lift_missing_count} pairs have projection but no lifted support" if lift_missing_count > 0 else "All pairs have lifted support or are blocked") + """

### Framework Language

- **Big Man** (excitatory/AKG-aligned bridge drive): """ + ("Active - drives viable seam formation" if viable_count > 0 else "Blocked by shell") + """
- **Big Woman** (shell/gateway veto): """ + ("Dominant - blocks all sheet_id:2 access" if blocked_count == total_pairs else "Partial - some gates open") + """
- **Small Man** (local seam substrate): """ + ("Present - viable local seams exist" if viable_count > 0 else "Absent - no direct substrate") + """
- **Small Woman** (projection-only trap): """ + (f"Active - {lift_missing_count} pairs trapped in projection-only state" if lift_missing_count > 0 else "Inactive - no projection traps") + """

---

## Conclusions

1. **No hard-coded blocks used**: All classifications based on actual verification layers
2. **Topology tested under both baselines**: Raw 11-comp and relay-collapsed 7-comp
3. **Five-class model**: Distinguishes true blocks from missing data from relay needs

"""
    
    # Add final interpretation
    if primary_status == "LOCALLY VIABLE":
        report += """
**Final Interpretation**: sheet_id:2 is NOT globally blocked. Local pairwise viable seams exist 
that can reduce topology. The "global blocker" status is an artifact of prior experimental designs 
that hard-coded sheet_id:2 as blocked or excluded it from candidate sets.

**Recommendation**: Enable the locally viable seams to test actual global closure.
"""
    elif primary_status == "LIFT-MISSING":
        report += """
**Final Interpretation**: sheet_id:2 is not globally blocked (tunnel checks pass), but lacks 
lifted local seam support. The viable paths are relay-mediated or projection-only.

**Recommendation**: Focus on relay mediator identification to bridge sheet_id:2 indirectly.
"""
    elif primary_status == "GLOBALLY BLOCKED":
        report += """
**Final Interpretation**: sheet_id:2 is genuinely blocked by tunnel/shell constraints.
No viable direct or indirect paths exist under current data.

**Recommendation**: Accept sheet_id:2 as true global blocker; focus on other closure strategies.
"""
    
    report += """
---

*Generated by sheet2_tristate_audit.py*
*Tri-state edge model: direct_gateway_blocked / local_pairwise_viable / projection_only / relay_mediated / fully_lifted_glue*
"""
    
    return report


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    
    # Run audit
    df = run_tristate_audit()
    
    if df.empty:
        print("\nNo results generated")
        return 1
    
    # Save detailed results
    output_path = OUTDIR / "sheet2_tristate_edge_table.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")
    
    # Print state summary
    print("\n" + "=" * 60)
    print("EDGE STATE DISTRIBUTION")
    print("=" * 60)
    print(generate_state_summary(df))
    
    # Generate and save summary report
    report = generate_summary_report(df)
    report_path = OUTDIR / "sheet2_tristate_summary_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nSaved: {report_path}")
    
    print("\n" + "=" * 60)
    print("TRI-STATE AUDIT COMPLETE")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
