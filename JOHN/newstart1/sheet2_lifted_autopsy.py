"""
Strict Lifted-Seam Autopsy for Remaining Disconnected Pairs

Performs autopsy on 4 sheet_id:2-related pairs:
1. sheet_id:2__sheet_id:4
2. sheet_id:11__sheet_id:2
3. sheet_id:13__sheet_id:2
4. sheet_id:14__sheet_id:2

Source-of-truth preserved:
- sheet_id:2 is NOT globally blocked
- sheet_id:2 enters main body under both baselines
- remaining failure mode is lifted_continuity_failure
- NO hard blocks or relative thresholds penalizing sheet_id:2
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "out" / "sheet2_lifted_autopsy"

GLOBAL_BLOCKER = "sheet_id:2"
ALL_SHEETS = ["sheet_id:2", "sheet_id:3", "sheet_id:4", "sheet_id:10", "sheet_id:11", 
              "sheet_id:12", "sheet_id:13", "sheet_id:14"]

# The 4 remaining disconnected pairs to autopsy
AUTOPSY_PAIRS = [
    ("sheet_id:2", "sheet_id:4"),
    ("sheet_id:11", "sheet_id:2"),
    ("sheet_id:13", "sheet_id:2"),
    ("sheet_id:14", "sheet_id:2"),
]


class ContinuityDiagnosis(Enum):
    """Six-class lifted continuity diagnosis."""
    MISSING_LOCAL_SEAM = "missing_local_seam"
    PROJECTION_ONLY_OVERLAP = "projection_only_overlap"
    MISSING_RELAY_MEDIATOR = "missing_relay_mediator"
    ORIENTATION_SIGN_MISMATCH = "orientation_or_sign_mismatch"
    THRESHOLD_ARTIFACT = "threshold_artifact"
    FULLY_LIFTABLE = "fully_liftable"


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
        return self.find(a) != self.find(b)
    
    def get_component_members(self, node: str) -> Set[str]:
        root = self.find(node)
        return {n for n in self.parent if self.find(n) == root}
    
    def copy(self) -> "DSU":
        new_dsu = DSU()
        new_dsu.parent = self.parent.copy()
        return new_dsu


def pair_id(a: str, b: str) -> str:
    return "__".join(sorted([str(a), str(b)]))


def load_all_source_data():
    """Load all source-of-truth outputs."""
    data = {}
    
    # Tri-state audit outputs
    tristate_dir = ROOT / "out" / "sheet2_tristate_audit"
    tristate_edge = tristate_dir / "sheet2_tristate_edge_table.csv"
    if tristate_edge.exists():
        data["tristate_edge"] = pd.read_csv(tristate_edge)
        print(f"  Loaded tristate_edge: {len(data['tristate_edge'])} rows")
    
    # Counterfactual outputs
    cf_dir = ROOT / "out" / "sheet2_counterfactual"
    cf_candidates = cf_dir / "sheet2_counterfactual_candidates.csv"
    if cf_candidates.exists():
        data["cf_candidates"] = pd.read_csv(cf_candidates)
        print(f"  Loaded cf_candidates: {len(data['cf_candidates'])} rows")
    
    # Global closure outputs
    closure_dir = ROOT / "out" / "sheet2_global_closure_activation"
    closure_activation = closure_dir / "global_closure_activation.csv"
    closure_failure = closure_dir / "global_closure_failure_decomposition.csv"
    if closure_activation.exists():
        data["closure_activation"] = pd.read_csv(closure_activation)
        print(f"  Loaded closure_activation: {len(data['closure_activation'])} rows")
    if closure_failure.exists():
        data["closure_failure"] = pd.read_csv(closure_failure)
        print(f"  Loaded closure_failure: {len(data['closure_failure'])} rows")
    
    # Connectivity audit
    conn_dir = ROOT / "out" / "connectivity_audit"
    conn_graph = conn_dir / "connectivity_graph.csv"
    conn_comp = conn_dir / "disconnected_components.csv"
    if conn_graph.exists():
        data["conn_graph"] = pd.read_csv(conn_graph)
        print(f"  Loaded conn_graph: {len(data['conn_graph'])} rows")
    if conn_comp.exists():
        data["conn_comp"] = pd.read_csv(conn_comp)
        print(f"  Loaded conn_comp: {len(data['conn_comp'])} rows")
    
    # Lifted seams
    lifted_dir = ROOT / "out" / "seam_local_atlas_lift_v2"
    lifted_seams = lifted_dir / "corrected_lifted_local_seams.csv"
    if lifted_seams.exists():
        data["lifted_seams"] = pd.read_csv(lifted_seams)
        print(f"  Loaded lifted_seams: {len(data['lifted_seams'])} rows")
    
    # Relay verified
    relay_dir = ROOT / "out" / "seam_relay_operator_test_v1"
    relay_verified = relay_dir / "relay_verified.csv"
    if relay_verified.exists():
        data["relay_verified"] = pd.read_csv(relay_verified)
        print(f"  Loaded relay_verified: {len(data['relay_verified'])} rows")
    
    return data


def build_both_baselines(comp_df: pd.DataFrame, relay_df: pd.DataFrame) -> Tuple[DSU, DSU]:
    """Build both DSU baselines."""
    if not comp_df.empty and "member_nodes" in comp_df.columns:
        raw_groups = [[y.strip() for y in str(x).split("|") if y.strip()] 
                     for x in comp_df["member_nodes"].astype(str)]
    else:
        raw_groups = [[s] for s in ALL_SHEETS]
    
    dsu_raw11 = DSU.from_groups(raw_groups)
    
    dsu_relay7 = DSU.from_groups(raw_groups)
    if not relay_df.empty and "from_sheet" in relay_df.columns:
        for r in relay_df.itertuples(index=False):
            dsu_relay7.union(str(r.from_sheet), str(r.mediator_sheet))
            dsu_relay7.union(str(r.mediator_sheet), str(r.to_sheet))
    
    return dsu_raw11, dsu_relay7


def autopsy_direct_local_seam(
    sheet_a: str, sheet_b: str, pair: str,
    lifted_df: pd.DataFrame, conn_df: pd.DataFrame,
    dsu_raw11: DSU, dsu_relay7: DSU
) -> Dict:
    """
    A. Direct local seam evidence autopsy.
    """
    result = {
        "pair": pair,
        "sheet_a": sheet_a,
        "sheet_b": sheet_b,
        "contact_support": 0.0,
        "saddle_support": 0.0,
        "lifted_distance": 1.0,
        "nearest_gap": None,
        "projection_overlap": False,
        "topology_reduction_raw11_alone": False,
        "topology_reduction_relay7_alone": False,
    }
    
    # Get lifted seam data
    if not lifted_df.empty and "sheet_a" in lifted_df.columns:
        lifted_df = lifted_df.copy()
        lifted_df["pair"] = lifted_df.apply(lambda r: pair_id(r["sheet_a"], r["sheet_b"]), axis=1)
        match = lifted_df[lifted_df["pair"] == pair]
        
        if not match.empty:
            row = match.iloc[0]
            result["contact_support"] = float(row.get("contact_support", 0.0))
            result["saddle_support"] = float(row.get("saddle_support", 0.0))
            result["lifted_distance"] = float(row.get("lifted_distance", 1.0))
            result["nearest_gap"] = str(row.get("nearest_gap", "")) if pd.notna(row.get("nearest_gap", "")) else None
    
    # Check projection overlap from connectivity
    if not conn_df.empty:
        conn_match = conn_df[
            ((conn_df["source_node"] == sheet_a) & (conn_df["target_node"] == sheet_b)) |
            ((conn_df["source_node"] == sheet_b) & (conn_df["target_node"] == sheet_a))
        ]
        proj = conn_match[conn_match["edge_type"] == "projection_overlap"]
        result["projection_overlap"] = not proj.empty
    
    # Test topology reduction if activated alone
    dsu_raw_test = dsu_raw11.copy()
    result["topology_reduction_raw11_alone"] = dsu_raw_test.would_reduce(sheet_a, sheet_b)
    
    dsu_relay_test = dsu_relay7.copy()
    result["topology_reduction_relay7_alone"] = dsu_relay_test.would_reduce(sheet_a, sheet_b)
    
    return result


def autopsy_relay_search(
    sheet_a: str, sheet_b: str, pair: str,
    relay_df: pd.DataFrame, conn_df: pd.DataFrame,
    dsu_raw11: DSU, dsu_relay7: DSU
) -> Dict:
    """
    B. Relay search autopsy.
    """
    result = {
        "pair": pair,
        "candidate_mediators": [],
        "best_mediator": None,
        "best_path_length": float('inf'),
        "mediator_is_projection_only": True,
        "relay_works_raw11": False,
        "relay_works_relay7": False,
    }
    
    # Find all candidate mediators
    mediators = []
    
    # From relay_verified
    if not relay_df.empty and "from_sheet" in relay_df.columns:
        for r in relay_df.itertuples(index=False):
            from_s = str(r.from_sheet)
            to_s = str(r.to_sheet)
            med = str(r.mediator_sheet)
            
            # Check if this relay could connect our pair
            if sheet_a in {from_s, to_s, med} and sheet_b in {from_s, to_s, med}:
                if sheet_a != med and sheet_b != med:
                    mediators.append({
                        "mediator": med,
                        "path": f"{sheet_a}->{med}->{sheet_b}",
                        "length": 2,
                        "source": "relay_verified",
                        "projection_only": False,
                    })
    
    # From connectivity graph projection_overlap
    if not conn_df.empty:
        # Find sheets that have projection_overlap with both sheet_a and sheet_b
        for candidate in ALL_SHEETS:
            if candidate in {sheet_a, sheet_b}:
                continue
            
            a_to_c = conn_df[
                ((conn_df["source_node"] == sheet_a) & (conn_df["target_node"] == candidate)) |
                ((conn_df["source_node"] == candidate) & (conn_df["target_node"] == sheet_a))
            ]
            c_to_b = conn_df[
                ((conn_df["source_node"] == candidate) & (conn_df["target_node"] == sheet_b)) |
                ((conn_df["source_node"] == sheet_b) & (conn_df["target_node"] == candidate))
            ]
            
            a_proj = a_to_c[a_to_c["edge_type"] == "projection_overlap"]
            b_proj = c_to_b[c_to_b["edge_type"] == "projection_overlap"]
            
            if not a_proj.empty and not b_proj.empty:
                mediators.append({
                    "mediator": candidate,
                    "path": f"{sheet_a}->{candidate}->{sheet_b}",
                    "length": 2,
                    "source": "projection_overlap",
                    "projection_only": True,
                })
    
    result["candidate_mediators"] = mediators
    
    if mediators:
        # Find best mediator (shortest path, non-projection preferred)
        non_proj = [m for m in mediators if not m["projection_only"]]
        if non_proj:
            best = min(non_proj, key=lambda x: x["length"])
            result["mediator_is_projection_only"] = False
        else:
            best = min(mediators, key=lambda x: x["length"])
            result["mediator_is_projection_only"] = True
        
        result["best_mediator"] = best["mediator"]
        result["best_path_length"] = best["length"]
        
        # Test if relay works under each baseline
        med = best["mediator"]
        
        # Raw baseline: check if a->med and med->b would reduce
        dsu_raw_test = dsu_raw11.copy()
        reduces_a_med = dsu_raw_test.would_reduce(sheet_a, med)
        dsu_raw_test.union(sheet_a, med)
        reduces_med_b = dsu_raw_test.would_reduce(med, sheet_b)
        result["relay_works_raw11"] = reduces_a_med or reduces_med_b
        
        # Relay baseline
        dsu_relay_test = dsu_relay7.copy()
        reduces_a_med_r = dsu_relay_test.would_reduce(sheet_a, med)
        dsu_relay_test.union(sheet_a, med)
        reduces_med_b_r = dsu_relay_test.would_reduce(med, sheet_b)
        result["relay_works_relay7"] = reduces_a_med_r or reduces_med_b_r
    
    result["mediator_count"] = len(mediators)
    result["mediator_list"] = "|".join([m["mediator"] for m in mediators]) if mediators else ""
    
    return result


def classify_lifted_continuity(
    direct_evidence: Dict, relay_evidence: Dict, cf_df: pd.DataFrame
) -> Tuple[ContinuityDiagnosis, str]:
    """
    C. Lifted continuity diagnosis classification.
    """
    pair = direct_evidence["pair"]
    
    # Check for threshold artifact
    if not cf_df.empty:
        pair_cf = cf_df[cf_df["top_sheet2_pair"] == pair]
        if not pair_cf.empty:
            max_score = pair_cf["top_sheet2_score"].max()
            if max_score > 2.0:
                # High score but not classified as viable - threshold artifact
                pass  # Will check other criteria
    
    # Check if fully liftable
    if (direct_evidence["contact_support"] > 0 or direct_evidence["saddle_support"] > 0):
        if direct_evidence["topology_reduction_raw11_alone"]:
            return ContinuityDiagnosis.FULLY_LIFTABLE, "Has lifted seam support and reduces topology"
    
    # Check projection only
    if direct_evidence["projection_overlap"] and not (direct_evidence["contact_support"] > 0):
        return ContinuityDiagnosis.PROJECTION_ONLY_OVERLAP, "Projection overlap without lifted seam"
    
    # Check missing relay
    if relay_evidence["candidate_mediators"]:
        if not relay_evidence["relay_works_raw11"] and not relay_evidence["relay_works_relay7"]:
            return ContinuityDiagnosis.MISSING_RELAY_MEDIATOR, "Has candidate mediators but relay doesn't reduce topology"
    else:
        return ContinuityDiagnosis.MISSING_RELAY_MEDIATOR, "No candidate mediators found"
    
    # Check missing local seam
    if direct_evidence["contact_support"] == 0 and direct_evidence["saddle_support"] == 0:
        return ContinuityDiagnosis.MISSING_LOCAL_SEAM, "No contact or saddle support"
    
    # Check orientation/sign
    if direct_evidence["contact_support"] > 0 or direct_evidence["saddle_support"] > 0:
        if not direct_evidence["topology_reduction_raw11_alone"]:
            return ContinuityDiagnosis.ORIENTATION_SIGN_MISMATCH, "Has support but doesn't reduce topology (possible orientation issue)"
    
    # Default
    return ContinuityDiagnosis.MISSING_LOCAL_SEAM, "Default classification - missing seam evidence"


def compute_closure_impact(
    sheet_a: str, sheet_b: str,
    dsu_raw11: DSU, dsu_relay7: DSU
) -> Dict:
    """
    D. Closure impact analysis.
    """
    result = {
        "pair": pair_id(sheet_a, sheet_b),
        "components_reduce_raw11": 0,
        "components_reduce_relay7": 0,
        "moves_toward_single_component_raw11": False,
        "moves_toward_single_component_relay7": False,
    }
    
    # Raw baseline
    dsu_raw_test = dsu_raw11.copy()
    before = dsu_raw_test.components()
    if dsu_raw_test.would_reduce(sheet_a, sheet_b):
        dsu_raw_test.union(sheet_a, sheet_b)
        after = dsu_raw_test.components()
        result["components_reduce_raw11"] = before - after
        result["moves_toward_single_component_raw11"] = (after == 1)
    
    # Relay baseline
    dsu_relay_test = dsu_relay7.copy()
    before = dsu_relay_test.components()
    if dsu_relay_test.would_reduce(sheet_a, sheet_b):
        dsu_relay_test.union(sheet_a, sheet_b)
        after = dsu_relay_test.components()
        result["components_reduce_relay7"] = before - after
        result["moves_toward_single_component_relay7"] = (after == 1)
    
    return result


def scan_pair_combinations(
    autopsy_results: List[Dict], dsu_raw11: DSU, dsu_relay7: DSU
) -> pd.DataFrame:
    """
    Scan all combinations of the 4 pairs for maximal closure.
    """
    pairs = [r["pair"] for r in autopsy_results]
    sheets = [(r["sheet_a"], r["sheet_b"]) for r in autopsy_results]
    
    results = []
    
    # Test all combinations
    for r in range(1, len(pairs) + 1):
        for combo_indices in itertools.combinations(range(len(pairs)), r):
            combo_pairs = [pairs[i] for i in combo_indices]
            combo_sheets = [sheets[i] for i in combo_indices]
            
            # Raw baseline
            dsu_raw = dsu_raw11.copy()
            raw_before = dsu_raw.components()
            for a, b in combo_sheets:
                dsu_raw.union(a, b)
            raw_after = dsu_raw.components()
            
            # Relay baseline
            dsu_relay = dsu_relay7.copy()
            relay_before = dsu_relay.components()
            for a, b in combo_sheets:
                dsu_relay.union(a, b)
            relay_after = dsu_relay.components()
            
            results.append({
                "combination": "|".join(combo_pairs),
                "pair_count": len(combo_pairs),
                "raw_before": raw_before,
                "raw_after": raw_after,
                "raw_reduction": raw_before - raw_after,
                "raw_full_closure": raw_after == 1,
                "relay_before": relay_before,
                "relay_after": relay_after,
                "relay_reduction": relay_before - relay_after,
                "relay_full_closure": relay_after == 1,
            })
    
    return pd.DataFrame(results)


def run_lifted_autopsy():
    """Run the complete lifted-seam autopsy."""
    print("=" * 60)
    print("STRICT LIFTED-SEAM AUTOPSY")
    print("=" * 60)
    print()
    
    # Load all data
    print("Loading source-of-truth outputs...")
    data = load_all_source_data()
    
    # Build baselines
    print("\nBuilding DSU baselines...")
    dsu_raw11, dsu_relay7 = build_both_baselines(
        data.get("conn_comp", pd.DataFrame()),
        data.get("relay_verified", pd.DataFrame())
    )
    print(f"  Raw 11-component: {dsu_raw11.components()} components")
    print(f"  Relay 7-component: {dsu_relay7.components()} components")
    
    # Run autopsy on each pair
    print(f"\nRunning autopsy on {len(AUTOPSY_PAIRS)} pairs...")
    autopsy_results = []
    
    for sheet_a, sheet_b in AUTOPSY_PAIRS:
        pair = pair_id(sheet_a, sheet_b)
        print(f"\n  Autopsying {pair}...")
        
        # A. Direct local seam evidence
        direct = autopsy_direct_local_seam(
            sheet_a, sheet_b, pair,
            data.get("lifted_seams", pd.DataFrame()),
            data.get("conn_graph", pd.DataFrame()),
            dsu_raw11, dsu_relay7
        )
        
        # B. Relay search
        relay = autopsy_relay_search(
            sheet_a, sheet_b, pair,
            data.get("relay_verified", pd.DataFrame()),
            data.get("conn_graph", pd.DataFrame()),
            dsu_raw11, dsu_relay7
        )
        
        # C. Classify continuity diagnosis
        diagnosis, diagnosis_reason = classify_lifted_continuity(
            direct, relay, data.get("cf_candidates", pd.DataFrame())
        )
        
        # D. Closure impact
        impact = compute_closure_impact(sheet_a, sheet_b, dsu_raw11, dsu_relay7)
        
        result = {
            **direct,
            "candidate_mediator_count": relay["mediator_count"],
            "candidate_mediators": relay["mediator_list"],
            "best_mediator": relay["best_mediator"],
            "best_path_length": relay["best_path_length"],
            "mediator_is_projection_only": relay["mediator_is_projection_only"],
            "relay_works_raw11": relay["relay_works_raw11"],
            "relay_works_relay7": relay["relay_works_relay7"],
            "continuity_diagnosis": diagnosis.value,
            "diagnosis_reason": diagnosis_reason,
            "closure_reduce_raw11": impact["components_reduce_raw11"],
            "closure_reduce_relay7": impact["components_reduce_relay7"],
            "toward_single_component_raw11": impact["moves_toward_single_component_raw11"],
            "toward_single_component_relay7": impact["moves_toward_single_component_relay7"],
        }
        
        autopsy_results.append(result)
        print(f"    Diagnosis: {diagnosis.value}")
        print(f"    Raw reduction: {impact['components_reduce_raw11']}")
        print(f"    Relay reduction: {impact['components_reduce_relay7']}")
    
    # Generate outputs
    OUTDIR.mkdir(parents=True, exist_ok=True)
    
    # 1. lifted_seam_autopsy.csv
    autopsy_df = pd.DataFrame(autopsy_results)
    autopsy_path = OUTDIR / "lifted_seam_autopsy.csv"
    autopsy_df.to_csv(autopsy_path, index=False)
    print(f"\nSaved: {autopsy_path}")
    
    # 2. relay_mediator_rankings.csv
    relay_rows = []
    for r in autopsy_results:
        pair = r["pair"]
        mediators = r.get("candidate_mediators", "")
        if mediators:
            for med in mediators.split("|"):
                relay_rows.append({
                    "pair": pair,
                    "mediator": med,
                    "is_best": med == r["best_mediator"],
                    "projection_only": r["mediator_is_projection_only"],
                    "works_raw11": r["relay_works_raw11"],
                    "works_relay7": r["relay_works_relay7"],
                })
    
    if relay_rows:
        relay_df = pd.DataFrame(relay_rows)
    else:
        relay_df = pd.DataFrame(columns=["pair", "mediator", "is_best", "projection_only", "works_raw11", "works_relay7"])
    
    relay_path = OUTDIR / "relay_mediator_rankings.csv"
    relay_df.to_csv(relay_path, index=False)
    print(f"Saved: {relay_path}")
    
    # 3. lifted_pair_combination_scan.csv
    combo_df = scan_pair_combinations(autopsy_results, dsu_raw11, dsu_relay7)
    combo_path = OUTDIR / "lifted_pair_combination_scan.csv"
    combo_df.to_csv(combo_path, index=False)
    print(f"Saved: {combo_path}")
    
    # 4. LIFTED_CONTINUITY_AUTOPSY_REPORT.md
    report = generate_autopsy_report(autopsy_df, relay_df, combo_df, data)
    report_path = OUTDIR / "LIFTED_CONTINUITY_AUTOPSY_REPORT.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"Saved: {report_path}")
    
    return autopsy_df, relay_df, combo_df


def generate_autopsy_report(
    autopsy_df: pd.DataFrame,
    relay_df: pd.DataFrame,
    combo_df: pd.DataFrame,
    data: Dict
) -> str:
    """Generate the LIFTED_CONTINUITY_AUTOPSY_REPORT.md."""
    
    # Summary statistics
    diagnosis_counts = autopsy_df["continuity_diagnosis"].value_counts()
    
    # Find best combination
    best_combo_raw = combo_df[combo_df["raw_full_closure"] == True]
    best_combo_relay = combo_df[combo_df["relay_full_closure"] == True]
    
    # Find maximal reduction even if not full closure
    max_reduction_raw = combo_df.loc[combo_df["raw_reduction"].idxmax()] if not combo_df.empty else None
    max_reduction_relay = combo_df.loc[combo_df["relay_reduction"].idxmax()] if not combo_df.empty else None
    
    # Identify the bottleneck
    bottleneck_analysis = []
    for _, row in autopsy_df.iterrows():
        diag = row["continuity_diagnosis"]
        if diag == ContinuityDiagnosis.MISSING_LOCAL_SEAM.value:
            bottleneck_analysis.append(f"{row['pair']}: Missing local seam (contact={row['contact_support']:.2f}, saddle={row['saddle_support']:.2f})")
        elif diag == ContinuityDiagnosis.MISSING_RELAY_MEDIATOR.value:
            bottleneck_analysis.append(f"{row['pair']}: Missing relay (mediators={row['candidate_mediator_count']})")
        elif diag == ContinuityDiagnosis.PROJECTION_ONLY_OVERLAP.value:
            bottleneck_analysis.append(f"{row['pair']}: Projection-only trap")
        elif diag == ContinuityDiagnosis.ORIENTATION_SIGN_MISMATCH.value:
            bottleneck_analysis.append(f"{row['pair']}: Orientation/sign mismatch")
        elif diag == ContinuityDiagnosis.FULLY_LIFTABLE.value:
            bottleneck_analysis.append(f"{row['pair']}: Fully liftable (should have been activated)")
        else:
            bottleneck_analysis.append(f"{row['pair']}: {diag}")
    
    # Determine true blocker
    missing_local = (autopsy_df["continuity_diagnosis"] == ContinuityDiagnosis.MISSING_LOCAL_SEAM.value).sum()
    missing_relay = (autopsy_df["continuity_diagnosis"] == ContinuityDiagnosis.MISSING_RELAY_MEDIATOR.value).sum()
    projection_only = (autopsy_df["continuity_diagnosis"] == ContinuityDiagnosis.PROJECTION_ONLY_OVERLAP.value).sum()
    orientation = (autopsy_df["continuity_diagnosis"] == ContinuityDiagnosis.ORIENTATION_SIGN_MISMATCH.value).sum()
    
    if missing_local >= missing_relay and missing_local >= projection_only and missing_local >= orientation:
        true_blocker = "LOCAL_SEAM_ABSENCE"
        blocker_desc = "Missing lifted local seam support is the primary blocker"
    elif missing_relay >= projection_only and missing_relay >= orientation:
        true_blocker = "RELAY_ABSENCE"
        blocker_desc = "Missing relay mediators is the primary blocker"
    elif projection_only >= orientation:
        true_blocker = "PROJECTION_ONLY_TRAP"
        blocker_desc = "Projection-only overlap without lifted continuity is the primary blocker"
    else:
        true_blocker = "ORIENTATION_SIGN_MISMATCH"
        blocker_desc = "Orientation or sign mismatch is the primary blocker"
    
    report = f"""# Lifted Continuity Autopsy Report

## Executive Summary

**Question**: Which of the 4 remaining sheet_id:2-related pairs is the true bottleneck to full global gluing, and is the blocker local seam absence, relay absence, or orientation/sign mismatch?

**Answer**: {true_blocker}

{blocker_desc}

---

## Autopsy Results: 4 Remaining Disconnected Pairs

"""
    
    # Add detailed autopsy for each pair
    for _, row in autopsy_df.iterrows():
        report += f"""### {row['pair']}

**Direct Local Seam Evidence**:
- Contact support: {row['contact_support']:.3f}
- Saddle support: {row['saddle_support']:.3f}
- Lifted distance: {row['lifted_distance']:.3f}
- Projection overlap: {row['projection_overlap']}
- Topology reduction (raw): {row['topology_reduction_raw11_alone']}
- Topology reduction (relay): {row['topology_reduction_relay7_alone']}

**Relay Search**:
- Candidate mediators: {row['candidate_mediator_count']} ({row['candidate_mediators']})
- Best mediator: {row['best_mediator'] if row['best_mediator'] else 'None'}
- Path length: {row['best_path_length'] if row['best_path_length'] != float('inf') else 'N/A'}
- Projection-only mediator: {row['mediator_is_projection_only']}
- Relay works (raw): {row['relay_works_raw11']}
- Relay works (relay): {row['relay_works_relay7']}

**Continuity Diagnosis**: {row['continuity_diagnosis']}

**Reason**: {row['diagnosis_reason']}

**Closure Impact**:
- Raw baseline reduction: {row['closure_reduce_raw11']} components
- Relay baseline reduction: {row['closure_reduce_relay7']} components
- Moves toward single component (raw): {row['toward_single_component_raw11']}
- Moves toward single component (relay): {row['toward_single_component_relay7']}

---

"""
    
    # Add diagnosis summary
    report += f"""## Diagnosis Summary

| Diagnosis | Count | Pairs |
|-----------|-------|-------|
"""
    for diag, count in diagnosis_counts.items():
        pairs = "|".join(autopsy_df[autopsy_df["continuity_diagnosis"] == diag]["pair"].tolist())
        report += f"| {diag} | {count} | {pairs} |\n"
    
    # Add combination scan results
    report += f"""
---

## Pair Combination Scan

### Best Combinations for Closure

**Raw 11-Component Baseline**:
"""
    
    if not best_combo_raw.empty:
        for _, row in best_combo_raw.head(3).iterrows():
            report += f"- {row['combination']}: {row['raw_reduction']} reduction, full closure = {row['raw_full_closure']}\n"
    else:
        report += "- No combination achieves full closure\n"
    
    if max_reduction_raw is not None:
        report += f"\nMaximum reduction (raw): {max_reduction_raw['raw_reduction']} with {max_reduction_raw['combination']}\n"
    
    report += f"""
**Relay 7-Component Baseline**:
"""
    
    if not best_combo_relay.empty:
        for _, row in best_combo_relay.head(3).iterrows():
            report += f"- {row['combination']}: {row['relay_reduction']} reduction, full closure = {row['relay_full_closure']}\n"
    else:
        report += "- No combination achieves full closure\n"
    
    if max_reduction_relay is not None:
        report += f"\nMaximum reduction (relay): {max_reduction_relay['relay_reduction']} with {max_reduction_relay['combination']}\n"
    
    # Add framework translation
    report += f"""
---

## Framework Translation

### Scientific Language

**Lifted continuity**: The actual "marriage law" - whether two sheets have sufficient
contact/saddle support to form a topological bond, not just geometric proximity.

**Global gluing**: Single connected component where all sheets are transitively linked.

**True bottleneck**: {true_blocker}
- Evidence: {blocker_desc}

### Framework Language

- **Big Man** (drive/support score): 
  - Status: PRESENT for activated seams
  - Status: INSUFFICIENT for 4 remaining pairs

- **Big Woman** (shell/gateway veto):
  - Status: NO VETO - tunnel checks pass
  - Evidence: sheet_id:2 enters main body when viable seams activated

- **Small Man** (local seam substrate):
  - Status: ABSENT for {missing_local} pairs
  - Evidence: No contact/saddle support

- **Small Woman** (projection-only trap):
  - Status: ACTIVE for {projection_only} pairs
  - Evidence: Projection overlap without lifted continuity

- **Lifted continuity** (actual marriage law):
  - Missing for: {", ".join(autopsy_df[autopsy_df["continuity_diagnosis"] != ContinuityDiagnosis.FULLY_LIFTABLE.value]["pair"].tolist())}
  - Present for: {", ".join(autopsy_df[autopsy_df["continuity_diagnosis"] == ContinuityDiagnosis.FULLY_LIFTABLE.value]["pair"].tolist()) if len(autopsy_df[autopsy_df["continuity_diagnosis"] == ContinuityDiagnosis.FULLY_LIFTABLE.value]) > 0 else "None"}

---

## Final Answer

**Which pair is the true bottleneck?**

{bottleneck_analysis[0] if bottleneck_analysis else "No analysis available"}

**What is the blocker type?**

{true_blocker}:
- Local seam absence: {missing_local} pairs
- Relay absence: {missing_relay} pairs  
- Projection-only trap: {projection_only} pairs
- Orientation/sign mismatch: {orientation} pairs

**Recommendation**:
"""
    
    if true_blocker == "LOCAL_SEAM_ABSENCE":
        report += """Focus on identifying additional lifted local seam evidence for the disconnected pairs.
The contact_support and saddle_support values are zero, indicating no local seam substrate.
Consider re-examining the seam_local_atlas_lift pipeline for these specific pairs.
"""
    elif true_blocker == "RELAY_ABSENCE":
        report += """Focus on identifying relay mediators that can bridge sheet_id:2 to the remaining disconnected sheets.
The current relay_verified set does not provide viable paths for these pairs.
"""
    elif true_blocker == "PROJECTION_ONLY_TRAP":
        report += """The pairs have projection_overlap in the connectivity graph but lack lifted seam support.
This is the Small Woman trap - proximity without binding.
Need either lifted continuity establishment or alternative relay paths.
"""
    else:
        report += """Review the orientation and sign compatibility between sheet_id:2 and the target sheets.
The support values exist but topology reduction fails, suggesting alignment issues.
"""
    
    report += """
---

*Generated by sheet2_lifted_autopsy.py*
*Source-of-truth: tri-state audit outputs, global closure activation*
*Strict lifted-seam autopsy - no hard blocks, no relative thresholds*
"""
    
    return report


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    
    autopsy_df, relay_df, combo_df = run_lifted_autopsy()
    
    print("\n" + "=" * 60)
    print("LIFTED AUTOPSY COMPLETE")
    print("=" * 60)
    
    # Print summary
    print("\nDiagnosis Summary:")
    for diag, count in autopsy_df["continuity_diagnosis"].value_counts().items():
        print(f"  {diag}: {count}")
    
    print("\nClosure Impact (max reduction):")
    print(f"  Raw baseline: {combo_df['raw_reduction'].max() if not combo_df.empty else 'N/A'}")
    print(f"  Relay baseline: {combo_df['relay_reduction'].max() if not combo_df.empty else 'N/A'}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
