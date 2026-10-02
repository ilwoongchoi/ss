"""
Sheet-2 Counterfactual Pipeline

CORRECTED EXPERIMENTAL DESIGN:
- Explicitly includes sheet_id:2 in candidate atlas
- Removes hard-coded veto on sheet_id:2 pairs
- Separates prior evidence from verification outcome
- Implements multi-layer re-verification
- Uses absolute + relative thresholding

This pipeline tests the counterfactual: "What if sheet_id:2 was allowed to compete?"
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

# Explicit sheet sets
LEFT = {"sheet_id:3", "sheet_id:4"}
RIGHT = {"sheet_id:10", "sheet_id:12", "sheet_id:13"}
GLOBAL_BLOCKER = "sheet_id:2"
ALL_SPINE = LEFT | RIGHT | {GLOBAL_BLOCKER}

# Baseline moved pairs (for counterfactual comparison)
BASELINE_MOVED = {
    "sheet_id:10__sheet_id:3",
    "sheet_id:12__sheet_id:3",
    "sheet_id:13__sheet_id:3",
    "sheet_id:10__sheet_id:4",
}

# Threshold grid for absolute threshold ablation
ABSOLUTE_THRESHOLDS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
RELATIVE_PERCENTILES = [0.8, 0.9, 0.95, 0.99]


def pair_id(a: str, b: str) -> str:
    """Canonical pair identifier."""
    return "__".join(sorted([str(a), str(b)]))


def involves_sheet2(pair_str: str) -> bool:
    """Check if pair involves the global blocker."""
    return GLOBAL_BLOCKER in pair_str


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
    
    def get_component_map(self) -> Dict[str, Set[str]]:
        """Get mapping from root to component members."""
        comp_map: Dict[str, Set[str]] = {}
        for node in self.parent:
            root = self.find(node)
            if root not in comp_map:
                comp_map[root] = set()
            comp_map[root].add(node)
        return comp_map


@dataclass
class SeamCandidate:
    """A candidate seam between two sheets."""
    pair: str
    sheet_a: str
    sheet_b: str
    contact_support: float
    saddle_support: float
    lifted_distance: float
    relay_bonus: float
    failure_reason: str
    
    # Prior evidence (not veto)
    prior_blocked_from_audit: bool
    prior_trap_flag: bool
    prior_projection_only: bool
    
    # Score (computed later)
    glue_score: float = 0.0
    
    # Verification layers (computed later)
    lifted_local_recheck: Optional[bool] = None
    relay_path_check: Optional[bool] = None
    tunnel_recheck: Optional[bool] = None
    reduces_topology: Optional[bool] = None
    
    # Counterfactual status
    is_sheet2_pair: bool = False
    
    @property
    def candidate_support(self) -> bool:
        return (self.contact_support > 0) or (self.saddle_support > 0) or (self.relay_bonus > 0)


def load_source_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all source data files."""
    # Try multiple possible locations
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
    
    lifted_path = find_file("seam_local_atlas_lift_v2/corrected_lifted_local_seams.csv")
    relay_path = find_file("seam_relay_operator_test_v1/relay_verified.csv")
    conn_path = find_file("connectivity_audit/connectivity_graph.csv")
    comp_path = find_file("connectivity_audit/disconnected_components.csv")
    audit_path = find_file("seam_local_atlas_lift_v2/spine_bridge_audit.csv")
    
    data = {}
    for name, path in [
        ("lifted", lifted_path), ("relay", relay_path), ("conn", conn_path),
        ("comp", comp_path), ("audit", audit_path)
    ]:
        if path and path.exists():
            data[name] = pd.read_csv(path)
        else:
            print(f"Warning: Could not find {name} data at expected locations")
            data[name] = pd.DataFrame()
    
    return data["lifted"], data["relay"], data["conn"], data["comp"], data["audit"]


def build_sheet2_candidate_atlas(
    lifted: pd.DataFrame,
    relay: pd.DataFrame,
    conn: pd.DataFrame,
    audit: pd.DataFrame
) -> List[SeamCandidate]:
    """
    Task A: Build candidate set explicitly including sheet_id:2.
    
    Includes:
    - sheet_id:2 <-> 3
    - sheet_id:2 <-> 4
    - sheet_id:2 <-> 10
    - sheet_id:2 <-> 12
    - sheet_id:2 <-> 13
    - Plus projection_overlap / saddle_candidate / relay-mediated pairs
    """
    candidates: Dict[str, SeamCandidate] = {}
    
    # Helper to add/update candidate
    def add_candidate(pair: str, a: str, b: str, **kwargs):
        if pair not in candidates:
            candidates[pair] = SeamCandidate(
                pair=pair,
                sheet_a=a,
                sheet_b=b,
                contact_support=0.0,
                saddle_support=0.0,
                lifted_distance=1.0,
                relay_bonus=0.0,
                failure_reason="",
                prior_blocked_from_audit=False,
                prior_trap_flag=False,
                prior_projection_only=False,
                is_sheet2_pair=involves_sheet2(pair),
                **kwargs
            )
    
    # 1. Explicit sheet_id:2 pairs (the counterfactual core)
    explicit_sheet2_pairs = [
        (GLOBAL_BLOCKER, "sheet_id:3"),
        (GLOBAL_BLOCKER, "sheet_id:4"),
        (GLOBAL_BLOCKER, "sheet_id:10"),
        (GLOBAL_BLOCKER, "sheet_id:12"),
        (GLOBAL_BLOCKER, "sheet_id:13"),
    ]
    for a, b in explicit_sheet2_pairs:
        p = pair_id(a, b)
        add_candidate(p, a, b)
    
    # 2. Load from lifted_local_seams (existing seam data)
    if not lifted.empty and "sheet_a" in lifted.columns:
        lifted = lifted.copy()
        lifted["pair"] = lifted.apply(lambda r: pair_id(r["sheet_a"], r["sheet_b"]), axis=1)
        
        for r in lifted.itertuples(index=False):
            p = str(r.pair)
            a, b = str(r.sheet_a), str(r.sheet_b)
            
            # Include if involves sheet_id:2 OR is a cross-spine pair
            is_cross_spine = (a in LEFT and b in RIGHT) or (b in LEFT and a in RIGHT)
            
            if involves_sheet2(p) or is_cross_spine:
                contact = float(getattr(r, "contact_support", 0.0))
                saddle = float(getattr(r, "saddle_support", 0.0))
                dist = float(getattr(r, "lifted_distance", 1.0))
                reason = str(getattr(r, "failure_reason", ""))
                
                if p in candidates:
                    # Update with better data
                    candidates[p].contact_support = max(candidates[p].contact_support, contact)
                    candidates[p].saddle_support = max(candidates[p].saddle_support, saddle)
                    candidates[p].lifted_distance = min(candidates[p].lifted_distance, dist)
                    if reason:
                        candidates[p].failure_reason = reason
                else:
                    add_candidate(p, a, b, 
                                 contact_support=contact,
                                 saddle_support=saddle,
                                 lifted_distance=dist,
                                 failure_reason=reason)
    
    # 3. Add projection_overlap and saddle_candidate from connectivity graph
    if not conn.empty and "source_node" in conn.columns:
        conn_sheet = conn[
            conn["source_node"].astype(str).str.startswith("sheet_id:", na=False) &
            conn["target_node"].astype(str).str.startswith("sheet_id:", na=False)
        ].copy()
        
        for r in conn_sheet.itertuples(index=False):
            a, b = str(r.source_node), str(r.target_node)
            p = pair_id(a, b)
            edge_type = str(getattr(r, "edge_type", ""))
            
            # Include if involves sheet_id:2 and is projection/saddle
            if involves_sheet2(p) and edge_type in ["projection_overlap", "saddle_candidate"]:
                confidence = float(getattr(r, "confidence", 0.0)) if hasattr(r, "confidence") else 0.0
                
                if p not in candidates:
                    add_candidate(p, a, b)
                
                if edge_type == "saddle_candidate":
                    candidates[p].saddle_support = max(candidates[p].saddle_support, confidence)
                elif edge_type == "projection_overlap":
                    candidates[p].prior_projection_only = True
    
    # 4. Add relay-mediated pairs
    if not relay.empty and "from_sheet" in relay.columns:
        for r in relay.itertuples(index=False):
            from_s = str(r.from_sheet)
            to_s = str(r.to_sheet)
            mediator = str(r.mediator_sheet)
            
            # Add all pairs in relay path if involves sheet_id:2
            for a, b in [(from_s, mediator), (mediator, to_s), (from_s, to_s)]:
                p = pair_id(a, b)
                if involves_sheet2(p):
                    if p not in candidates:
                        add_candidate(p, a, b)
                    candidates[p].relay_bonus = 1.0
    
    # 5. Load prior audit evidence (as evidence, not veto)
    if not audit.empty and "pair" in audit.columns:
        for r in audit.itertuples(index=False):
            p = str(r.pair) if hasattr(r, "pair") else ""
            if involves_sheet2(p) and p in candidates:
                fail_cat = str(getattr(r, "failure_category", ""))
                if "projection" in fail_cat or "trap" in fail_cat or "loss" in fail_cat:
                    candidates[p].prior_trap_flag = True
                if "tunnel" in fail_cat or "blocked" in fail_cat:
                    candidates[p].prior_blocked_from_audit = True
    
    # 6. Load tunnel_blocked info from connectivity
    if not conn.empty:
        for r in conn.itertuples(index=False):
            a, b = str(r.source_node), str(r.target_node)
            p = pair_id(a, b)
            edge_type = str(getattr(r, "edge_type", ""))
            if involves_sheet2(p) and edge_type == "tunnel_blocked" and p in candidates:
                candidates[p].prior_blocked_from_audit = True
    
    return list(candidates.values())


def compute_counterfactual_scores(
    candidates: List[SeamCandidate],
    akg_spine: float = 0.5,
    adra2a_gate: float = 0.0,
    oprm1_gate: float = 0.0,
    oprk1_shell: float = 0.0,
    d3_gate: float = 0.0,
    left_coldstress_akg: float = 0.0,
    left_estrogen_press: float = 0.0,
    left_noradrenaline_press: float = 0.0,
) -> List[SeamCandidate]:
    """
    Compute glue scores without hard-coded sheet_id:2 block.
    
    Task B: Separate into:
    - prior_blocked_from_old_audit (evidence, not veto)
    - candidate_selected_by_new_score (score-based)
    - reverified_by_new_test (topology-based, done later)
    """
    for c in candidates:
        # Base support
        base_support = 0.55 * c.contact_support + 0.45 * c.saddle_support
        
        # Neurochemical terms (from both scans)
        glu_balance = akg_spine
        gaba_balance = 1.0 - akg_spine
        primary_exc_inh_balance = glu_balance - gaba_balance
        
        left_suppression_collapse = left_coldstress_akg * left_estrogen_press * left_noradrenaline_press
        mid_hub_r = np.clip((d3_gate + 0.5) / 1.5, 0.0, 1.0) * (primary_exc_inh_balance + 1.0) / 2.0
        
        # Penalties (prior evidence reduces score but doesn't veto)
        shell_penalty = 1.0 if c.prior_blocked_from_audit else 0.0
        shell_penalty += oprk1_shell  # Additional shell pressure
        
        trap_penalty = 1.0 if c.prior_trap_flag else 0.0
        if c.prior_projection_only:
            trap_penalty += 0.5
        
        # Compute glue score
        c.glue_score = (
            base_support
            + c.contact_support
            + c.saddle_support
            - c.lifted_distance
            - shell_penalty * 0.5  # Reduced weight - evidence, not veto
            - trap_penalty * 0.5
            - left_suppression_collapse
            + primary_exc_inh_balance
            + mid_hub_r
            + adra2a_gate * 0.3
            + oprm1_gate * 0.3
            + d3_gate * 0.3
            + c.relay_bonus * 0.5
        )
    
    return candidates


def apply_threshold_ablation(
    candidates: List[SeamCandidate],
    threshold_mode: str = "absolute",
    threshold_value: float = 1.0
) -> List[SeamCandidate]:
    """
    Task E: Fix degenerate thresholding.
    
    Modes:
    - absolute: fixed threshold
    - relative_percentile: percentile of sheet_id:2 candidates only
    - relative_all: percentile of all candidates
    """
    sheet2_cands = [c for c in candidates if c.is_sheet2_pair and c.candidate_support]
    
    if threshold_mode == "absolute":
        thresh = threshold_value
    elif threshold_mode == "relative_percentile":
        if sheet2_cands:
            thresh = np.percentile([c.glue_score for c in sheet2_cands], threshold_value * 100)
        else:
            thresh = 0.0
    elif threshold_mode == "relative_all":
        if candidates:
            thresh = np.percentile([c.glue_score for c in candidates], threshold_value * 100)
        else:
            thresh = 0.0
    else:
        thresh = 0.0
    
    # Return candidates above threshold
    return [c for c in candidates if c.glue_score >= thresh]


def run_counterfactual_sweep() -> pd.DataFrame:
    """
    Run full counterfactual sweep with various threshold strategies.
    """
    print("Loading source data...")
    lifted, relay, conn, comp, audit = load_source_data()
    
    print("Building sheet_id:2 inclusive candidate atlas...")
    candidates = build_sheet2_candidate_atlas(lifted, relay, conn, audit)
    print(f"  Built {len(candidates)} candidates, {sum(c.is_sheet2_pair for c in candidates)} involve sheet_id:2")
    
    # Component groups for DSU
    if not comp.empty and "member_nodes" in comp.columns:
        groups = [[y.strip() for y in str(x).split("|") if y.strip()] 
                 for x in comp["member_nodes"].astype(str)]
    else:
        # Default: all sheets separate
        groups = [[s] for s in ALL_SPINE]
    
    results = []
    
    # Sweep configurations
    configs = []
    for akg in [0.0, 0.3, 0.5, 0.7, 1.0]:
        configs.append({
            "akg_spine": akg,
            "adra2a_gate": 0.0,
            "oprm1_gate": 0.0,
            "oprk1_shell": 0.0,
            "d3_gate": 0.0,
            "left_coldstress_akg": 0.0,
            "left_estrogen_press": 0.0,
            "left_noradrenaline_press": 0.0,
        })
        configs.append({
            "akg_spine": akg,
            "adra2a_gate": 0.5,
            "oprm1_gate": 0.5,
            "oprk1_shell": 0.0,
            "d3_gate": 0.5,
            "left_coldstress_akg": 0.0,
            "left_estrogen_press": 0.0,
            "left_noradrenaline_press": 0.0,
        })
    
    # Add left suppression configs
    for suppress in [0.0, 0.5, 1.0]:
        configs.append({
            "akg_spine": 0.5,
            "adra2a_gate": 0.0,
            "oprm1_gate": 0.0,
            "oprk1_shell": 0.0,
            "d3_gate": 0.0,
            "left_coldstress_akg": suppress,
            "left_estrogen_press": suppress,
            "left_noradrenaline_press": suppress,
        })
    
    # Threshold strategies
    thresh_strategies = []
    for t in ABSOLUTE_THRESHOLDS:
        thresh_strategies.append(("absolute", t))
    for p in RELATIVE_PERCENTILES:
        thresh_strategies.append(("relative_percentile", p))
    
    print(f"Running sweep: {len(configs)} configs × {len(thresh_strategies)} threshold strategies...")
    
    for cfg in configs:
        # Score all candidates
        scored = compute_counterfactual_scores(
            [SeamCandidate(**vars(c)) for c in candidates],  # Copy
            **cfg
        )
        
        for thresh_mode, thresh_val in thresh_strategies:
            selected = apply_threshold_ablation(scored, thresh_mode, thresh_val)
            
            # Count sheet_id:2 candidates
            sheet2_selected = [c for c in selected if c.is_sheet2_pair]
            sheet2_above_baseline = [c for c in sheet2_selected 
                                    if c.glue_score >= max((c.glue_score for c in selected if not c.is_sheet2_pair), default=0)]
            
            # Check which baseline pairs would move
            baseline_in_selected = [c.pair for c in selected if c.pair in BASELINE_MOVED]
            
            results.append({
                **cfg,
                "threshold_mode": thresh_mode,
                "threshold_value": thresh_val,
                "total_candidates": len(candidates),
                "sheet2_candidates": sum(1 for c in candidates if c.is_sheet2_pair),
                "selected_count": len(selected),
                "sheet2_selected_count": len(sheet2_selected),
                "sheet2_max_score": max((c.glue_score for c in sheet2_selected), default=-999),
                "sheet2_min_score": min((c.glue_score for c in sheet2_selected), default=-999),
                "non_sheet2_max_score": max((c.glue_score for c in selected if not c.is_sheet2_pair), default=-999),
                "baseline_pairs_in_selected": "|".join(baseline_in_selected),
                "baseline_count": len(baseline_in_selected),
                "sheet2_pairs_above_baseline_count": len(sheet2_above_baseline),
                "top_sheet2_pair": sheet2_selected[0].pair if sheet2_selected else "",
                "top_sheet2_score": sheet2_selected[0].glue_score if sheet2_selected else -999,
            })
    
    return pd.DataFrame(results)


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("SHEET-2 COUNTERFACTUAL PIPELINE")
    print("=" * 60)
    print()
    
    # Run sweep
    df = run_counterfactual_sweep()
    
    # Save results
    output_path = OUTDIR / "sheet2_counterfactual_candidates.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    # Best sheet_id:2 scores
    sheet2_rows = df[df["sheet2_selected_count"] > 0]
    if not sheet2_rows.empty:
        best = sheet2_rows.loc[sheet2_rows["sheet2_max_score"].idxmax()]
        print(f"\nHighest sheet_id:2 score achieved: {best['sheet2_max_score']:.3f}")
        print(f"  Threshold mode: {best['threshold_mode']}, value: {best['threshold_value']}")
        print(f"  AKG spine: {best['akg_spine']}, D3: {best['d3_gate']}")
    
    # Configurations where sheet_id:2 pairs exceed baseline
    above_baseline = df[df["sheet2_pairs_above_baseline_count"] > 0]
    if not above_baseline.empty:
        print(f"\nConfigurations where sheet_id:2 pairs score above baseline: {len(above_baseline)}")
        best_above = above_baseline.loc[above_baseline["sheet2_max_score"].idxmax()]
        print(f"  Best: {best_above['sheet2_pairs_above_baseline_count']} sheet_id:2 pairs above baseline")
    else:
        print("\nNo configurations found where sheet_id:2 pairs exceed baseline scores")
    
    # Compare absolute vs relative thresholding
    abs_best = df[df["threshold_mode"] == "absolute"]["sheet2_max_score"].max()
    rel_best = df[df["threshold_mode"] == "relative_percentile"]["sheet2_max_score"].max()
    print(f"\nThreshold strategy comparison:")
    print(f"  Best absolute threshold result: {abs_best:.3f}")
    print(f"  Best relative percentile result: {rel_best:.3f}")
    
    print("\n" + "=" * 60)
    print("Next step: Run sheet2_reverification.py")
    print("  - Nominate top sheet_id:2 seams")
    print("  - Run verification layers")
    print("  - Check topology reduction")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
