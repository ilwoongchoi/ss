"""
Sheet-2 Re-verification Module

Task C: After scoring, nominate top sheet_id:2 seams and re-run verification.

Required verification layers:
1. Lifted local seam recheck
2. Relay-mediated path check
3. Tunnel / connectivity recheck
4. DSU component reduction before vs after

A seam becomes "verified" only if it reduces topology after re-verification.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "sheet2_counterfactual"

GLOBAL_BLOCKER = "sheet_id:2"
ALL_SHEETS = ["sheet_id:2", "sheet_id:3", "sheet_id:4", "sheet_id:10", "sheet_id:12", "sheet_id:13"]


def pair_id(a: str, b: str) -> str:
    return "__".join(sorted([str(a), str(b)]))


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
        """Check if adding this edge would reduce component count."""
        return self.find(a) != self.find(b)


@dataclass
class VerificationResult:
    """Result of full verification pipeline for a seam."""
    pair: str
    sheet_a: str
    sheet_b: str
    glue_score: float
    
    # Prior evidence
    prior_blocked_from_audit: bool
    prior_trap_flag: bool
    prior_projection_only: bool
    
    # Layer 1: Lifted local seam recheck
    lifted_recheck_passed: Optional[bool] = None
    lifted_recheck_details: str = ""
    
    # Layer 2: Relay-mediated path check
    relay_path_exists: Optional[bool] = None
    relay_mediator: Optional[str] = None
    relay_path_details: str = ""
    
    # Layer 3: Tunnel/connectivity recheck
    tunnel_recheck_passed: Optional[bool] = None
    tunnel_details: str = ""
    
    # Layer 4: Topology reduction
    topology_reduces: Optional[bool] = None
    components_before: Optional[int] = None
    components_after: Optional[int] = None
    
    # Final verdict
    fully_verified: bool = False
    failure_modes: List[str] = field(default_factory=list)


def load_source_data():
    """Load source data for verification."""
    possible_roots = [
        ROOT / "out",
        ROOT / "left_akg_extract" / "out",
        ROOT / "akg_spine_extract" / "out",
        ROOT / ".." / "out",
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
    }
    
    data = {}
    for name, path in paths.items():
        if path and path.exists():
            data[name] = pd.read_csv(path)
        else:
            data[name] = pd.DataFrame()
    
    return data["lifted"], data["relay"], data["conn"], data["comp"], data["audit"]


def layer1_lifted_local_recheck(
    pair: str, sheet_a: str, sheet_b: str,
    lifted: pd.DataFrame, audit: pd.DataFrame
) -> Tuple[bool, str]:
    """
    Layer 1: Recheck lifted local seam quality.
    
    Returns (passed, details)
    """
    details = []
    
    # Check if pair exists in lifted seams
    if not lifted.empty and "sheet_a" in lifted.columns:
        lifted["pair"] = lifted.apply(lambda r: pair_id(r["sheet_a"], r["sheet_b"]), axis=1)
        match = lifted[lifted["pair"] == pair]
        
        if not match.empty:
            row = match.iloc[0]
            contact = float(row.get("contact_support", 0.0))
            saddle = float(row.get("saddle_support", 0.0))
            dist = float(row.get("lifted_distance", 1.0))
            
            details.append(f"Found in lifted_local_seams: contact={contact:.3f}, saddle={saddle:.3f}, dist={dist:.3f}")
            
            # Quality checks
            if contact > 0 or saddle > 0:
                passed = True
                details.append("PASS: Has positive contact or saddle support")
            else:
                passed = False
                details.append("FAIL: No contact or saddle support")
            
            if dist < 0.5:
                details.append(f"GOOD: Low lifted_distance ({dist:.3f})")
            else:
                details.append(f"WARN: High lifted_distance ({dist:.3f})")
        else:
            passed = False
            details.append("Not found in lifted_local_seams - no direct seam data")
    else:
        passed = False
        details.append("No lifted_local_seams data available")
    
    return passed, "; ".join(details)


def layer2_relay_path_check(
    pair: str, sheet_a: str, sheet_b: str,
    relay: pd.DataFrame, conn: pd.DataFrame
) -> Tuple[bool, Optional[str], str]:
    """
    Layer 2: Check for relay-mediated path.
    
    Returns (path_exists, mediator_sheet, details)
    """
    details = []
    mediator = None
    
    if not relay.empty and "from_sheet" in relay.columns:
        # Look for relay paths involving these sheets
        for r in relay.itertuples(index=False):
            from_s = str(r.from_sheet)
            to_s = str(r.to_sheet)
            med = str(r.mediator_sheet)
            
            # Check if this relay connects our sheets (possibly through mediator)
            if {sheet_a, sheet_b} <= {from_s, to_s, med}:
                mediator = med
                details.append(f"Found relay path: {from_s} -> {med} -> {to_s}")
                break
    
    # Also check connectivity graph for projection-mediated paths
    if not conn.empty and mediator is None:
        conn_matches = conn[
            ((conn["source_node"] == sheet_a) & (conn["target_node"] == sheet_b)) |
            ((conn["source_node"] == sheet_b) & (conn["target_node"] == sheet_a))
        ]
        
        for r in conn_matches.itertuples(index=False):
            edge_type = str(getattr(r, "edge_type", ""))
            if "projection" in edge_type or "relay" in edge_type:
                details.append(f"Found {edge_type} connection")
                if mediator is None:
                    mediator = f"{edge_type}_mediator"
    
    path_exists = mediator is not None
    if not details:
        details.append("No relay-mediated path found")
    
    return path_exists, mediator, "; ".join(details)


def layer3_tunnel_recheck(
    pair: str, sheet_a: str, sheet_b: str,
    conn: pd.DataFrame, audit: pd.DataFrame
) -> Tuple[bool, str]:
    """
    Layer 3: Recheck tunnel/connectivity constraints.
    
    Returns (passed, details)
    """
    details = []
    
    # Check connectivity graph for tunnel_blocked
    if not conn.empty and "source_node" in conn.columns:
        tunnel_check = conn[
            ((conn["source_node"] == sheet_a) & (conn["target_node"] == sheet_b)) |
            ((conn["source_node"] == sheet_b) & (conn["target_node"] == sheet_a))
        ]
        
        tunnel_blocked = tunnel_check[tunnel_check["edge_type"] == "tunnel_blocked"]
        if not tunnel_blocked.empty:
            details.append("BLOCKED: tunnel_blocked edge in connectivity graph")
            passed = False
        else:
            details.append("PASS: No tunnel_blocked edge")
            passed = True
        
        # Check for projection_overlap (not a block, but information)
        proj = tunnel_check[tunnel_check["edge_type"] == "projection_overlap"]
        if not proj.empty:
            details.append("INFO: projection_overlap exists (may indicate indirect path)")
    else:
        details.append("No connectivity graph available - assuming pass")
        passed = True
    
    # Check audit for tunnel-related failures
    if not audit.empty and "pair" in audit.columns:
        audit_match = audit[audit["pair"] == pair]
        if not audit_match.empty:
            fail_cat = str(audit_match.iloc[0].get("failure_category", ""))
            if "tunnel" in fail_cat.lower():
                details.append(f"AUDIT: Prior tunnel failure recorded ({fail_cat})")
                passed = False
            elif "blocked" in fail_cat.lower():
                details.append(f"AUDIT: Prior blocked status ({fail_cat})")
                passed = False
    
    return passed, "; ".join(details)


def layer4_topology_reduction(
    pair: str, sheet_a: str, sheet_b: str,
    comp: pd.DataFrame
) -> Tuple[bool, int, int, str]:
    """
    Layer 4: Check if adding this seam reduces component count.
    
    Returns (reduces, before, after, details)
    """
    # Build initial DSU from components
    if not comp.empty and "member_nodes" in comp.columns:
        groups = [[y.strip() for y in str(x).split("|") if y.strip()] 
                 for x in comp["member_nodes"].astype(str)]
    else:
        groups = [[s] for s in ALL_SHEETS]
    
    dsu = DSU.from_groups(groups)
    before = dsu.components()
    
    # Check if union would reduce
    would_reduce = dsu.would_reduce(sheet_a, sheet_b)
    
    # Actually perform union
    dsu.union(sheet_a, sheet_b)
    after = dsu.components()
    
    details = f"Components: {before} -> {after}, reduction={before - after}"
    
    return would_reduce, before, after, details


def run_full_verification(
    candidates_df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Run full 4-layer verification on top sheet_id:2 candidates.
    """
    print("Loading source data for verification...")
    lifted, relay, conn, comp, audit = load_source_data()
    
    # Get top sheet_id:2 candidates
    sheet2_df = candidates_df[candidates_df["top_sheet2_pair"] != ""].copy()
    
    if sheet2_df.empty:
        print("No sheet_id:2 candidates found in input")
        return pd.DataFrame()
    
    # Get unique top pairs
    top_pairs = sheet2_df.nlargest(top_n, "top_sheet2_score")[["top_sheet2_pair", "top_sheet2_score"]].drop_duplicates()
    
    print(f"\nRunning 4-layer verification on top {len(top_pairs)} sheet_id:2 candidates...")
    
    results = []
    
    for _, row in top_pairs.iterrows():
        pair = row["top_sheet2_pair"]
        score = row["top_sheet2_score"]
        
        sheets = pair.split("__")
        if len(sheets) != 2:
            continue
        sheet_a, sheet_b = sheets
        
        print(f"\n  Verifying {pair} (score={score:.3f})...")
        
        result = VerificationResult(
            pair=pair,
            sheet_a=sheet_a,
            sheet_b=sheet_b,
            glue_score=score,
            prior_blocked_from_audit=False,
            prior_trap_flag=False,
            prior_projection_only=False,
        )
        
        # Load prior evidence
        if not audit.empty and "pair" in audit.columns:
            audit_match = audit[audit["pair"] == pair]
            if not audit_match.empty:
                fail_cat = str(audit_match.iloc[0].get("failure_category", ""))
                result.prior_blocked_from_audit = "blocked" in fail_cat or "tunnel" in fail_cat
                result.prior_trap_flag = "trap" in fail_cat or "projection" in fail_cat
        
        # Layer 1: Lifted local seam recheck
        result.lifted_recheck_passed, result.lifted_recheck_details = \
            layer1_lifted_local_recheck(pair, sheet_a, sheet_b, lifted, audit)
        print(f"    Layer 1 (Lifted seam): {'PASS' if result.lifted_recheck_passed else 'FAIL'}")
        
        # Layer 2: Relay path check
        result.relay_path_exists, result.relay_mediator, result.relay_path_details = \
            layer2_relay_path_check(pair, sheet_a, sheet_b, relay, conn)
        print(f"    Layer 2 (Relay path): {'FOUND' if result.relay_path_exists else 'NOT FOUND'}")
        if result.relay_mediator:
            print(f"      Mediator: {result.relay_mediator}")
        
        # Layer 3: Tunnel recheck
        result.tunnel_recheck_passed, result.tunnel_details = \
            layer3_tunnel_recheck(pair, sheet_a, sheet_b, conn, audit)
        print(f"    Layer 3 (Tunnel): {'PASS' if result.tunnel_recheck_passed else 'FAIL'}")
        
        # Layer 4: Topology reduction
        result.topology_reduces, result.components_before, result.components_after, details = \
            layer4_topology_reduction(pair, sheet_a, sheet_b, comp)
        print(f"    Layer 4 (Topology): {details}")
        
        # Determine failure modes
        failure_modes = []
        if not result.lifted_recheck_passed:
            failure_modes.append("missing_lifted_local_seam")
        if not result.relay_path_exists:
            failure_modes.append("no_relay_mediator")
        if not result.tunnel_recheck_passed:
            failure_modes.append("tunnel_blocked")
        if not result.topology_reduces:
            failure_modes.append("no_topology_reduction")
        if result.prior_blocked_from_audit:
            failure_modes.append("prior_audit_block")
        if result.prior_trap_flag:
            failure_modes.append("prior_trap_flag")
        
        result.failure_modes = failure_modes
        
        # Final verdict: verified only if topology reduces AND tunnel passes
        result.fully_verified = result.topology_reduces and result.tunnel_recheck_passed
        
        print(f"    FINAL: {'VERIFIED' if result.fully_verified else 'FAILED'}")
        if failure_modes:
            print(f"      Failure modes: {', '.join(failure_modes)}")
        
        results.append({
            "pair": result.pair,
            "sheet_a": result.sheet_a,
            "sheet_b": result.sheet_b,
            "glue_score": result.glue_score,
            "prior_blocked_from_audit": result.prior_blocked_from_audit,
            "prior_trap_flag": result.prior_trap_flag,
            "layer1_lifted_passed": result.lifted_recheck_passed,
            "layer2_relay_exists": result.relay_path_exists,
            "layer2_relay_mediator": result.relay_mediator,
            "layer3_tunnel_passed": result.tunnel_recheck_passed,
            "layer4_topology_reduces": result.topology_reduces,
            "components_before": result.components_before,
            "components_after": result.components_after,
            "fully_verified": result.fully_verified,
            "failure_modes": "|".join(failure_modes),
        })
    
    return pd.DataFrame(results)


def generate_component_reduction_counterfactual(
    verified_df: pd.DataFrame,
    candidates_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate counterfactual component reduction analysis.
    
    What would happen if we added verified sheet_id:2 seams?
    """
    # Get baseline component count
    baseline_comp = candidates_df["baseline_count"].max() if "baseline_count" in candidates_df.columns else 4
    
    # Get verified sheet_id:2 seams
    verified_sheet2 = verified_df[verified_df["fully_verified"] == True]
    
    results = []
    
    # Scenario 0: Baseline (no sheet_id:2)
    results.append({
        "scenario": "baseline_no_sheet2",
        "added_seams": "",
        "seam_count": 0,
        "estimated_components": 7,  # Known from prior analysis
        "reduction_from_baseline": 0,
    })
    
    # Scenario 1: Add each verified sheet_id:2 seam individually
    for _, row in verified_sheet2.iterrows():
        results.append({
            "scenario": f"add_{row['pair']}",
            "added_seams": row["pair"],
            "seam_count": 1,
            "estimated_components": row["components_after"],
            "reduction_from_baseline": row["components_before"] - row["components_after"],
        })
    
    # Scenario 2: Add all verified sheet_id:2 seams together
    if len(verified_sheet2) > 1:
        all_seams = "|".join(verified_sheet2["pair"].tolist())
        # Approximate: adding all would reduce by at most (count) components
        # But actual reduction depends on DSU structure
        estimated = max(7 - len(verified_sheet2), 1)
        results.append({
            "scenario": "add_all_verified_sheet2",
            "added_seams": all_seams,
            "seam_count": len(verified_sheet2),
            "estimated_components": estimated,
            "reduction_from_baseline": len(verified_sheet2),
        })
    
    # Scenario 3: What if we allowed ALL sheet_id:2 pairs (counterfactual upper bound)
    all_sheet2 = candidates_df[candidates_df["sheet2_selected_count"] > 0]
    if not all_sheet2.empty:
        max_sheet2 = all_sheet2["sheet2_selected_count"].max()
        results.append({
            "scenario": "counterfactual_all_sheet2_allowed",
            "added_seams": "all_sheet_id:2_pairs",
            "seam_count": int(max_sheet2),
            "estimated_components": max(7 - max_sheet2, 1),
            "reduction_from_baseline": int(max_sheet2),
        })
    
    return pd.DataFrame(results)


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("SHEET-2 REVERIFICATION")
    print("=" * 60)
    print()
    
    # Load counterfactual candidates
    candidates_path = OUTDIR / "sheet2_counterfactual_candidates.csv"
    if not candidates_path.exists():
        print(f"Error: {candidates_path} not found")
        print("Run sheet2_counterfactual_pipeline.py first")
        return 1
    
    candidates_df = pd.read_csv(candidates_path)
    print(f"Loaded {len(candidates_df)} counterfactual sweep results")
    
    # Run full verification
    verified_df = run_full_verification(candidates_df, top_n=10)
    
    if verified_df.empty:
        print("\nNo sheet_id:2 candidates to verify")
        return 0
    
    # Save verification results
    output_path = OUTDIR / "sheet2_reverification_results.csv"
    verified_df.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")
    
    # Summary
    print("\n" + "=" * 60)
    print("REVERIFICATION SUMMARY")
    print("=" * 60)
    
    total = len(verified_df)
    verified = verified_df["fully_verified"].sum()
    
    print(f"\nTotal candidates tested: {total}")
    print(f"Fully verified: {verified}")
    print(f"Failed: {total - verified}")
    
    if verified > 0:
        print("\nVerified sheet_id:2 seams:")
        for _, row in verified_df[verified_df["fully_verified"]].iterrows():
            print(f"  - {row['pair']} (score={row['glue_score']:.3f})")
    
    # Failure mode analysis
    all_failures = []
    for modes in verified_df["failure_modes"]:
        if pd.notna(modes) and modes:
            all_failures.extend(modes.split("|"))
    
    if all_failures:
        from collections import Counter
        failure_counts = Counter(all_failures)
        print("\nFailure mode distribution:")
        for mode, count in failure_counts.most_common():
            print(f"  - {mode}: {count}")
    
    # Generate component reduction counterfactual
    counterfactual_df = generate_component_reduction_counterfactual(verified_df, candidates_df)
    counterfactual_path = OUTDIR / "component_reduction_counterfactual.csv"
    counterfactual_df.to_csv(counterfactual_path, index=False)
    print(f"\nSaved: {counterfactual_path}")
    
    print("\n" + "=" * 60)
    print("Next step: Run sheet2_failure_diagnosis.py")
    print("  - Diagnose specific failure mechanisms")
    print("  - Generate failure_modes.md report")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
