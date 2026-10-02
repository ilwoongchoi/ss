#!/usr/bin/env python3
import pandas as pd
import re
import json
import itertools
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Iterable

def extract_sheet_id(text: object) -> Optional[str]:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None
    s = str(text).strip()
    if not s:
        return None
    # Look for "sheet_id:X" or just "X"
    m = re.search(r"sheet[\s_\-]*id[\s:=_\-]*([0-9]+)", s, re.IGNORECASE)
    if m:
        return str(int(m.group(1)))
    if re.match(r"^[0-9]+$", s):
        return str(int(s))
    return s # Return as is if it's not a simple number but still a node name

@dataclass
class Edge:
    u: str
    v: str
    source_table: str
    applied: bool
    viable: bool
    contact_score: Optional[float]
    gap_min_dist: Optional[float]
    raw: Dict[str, object]

def get_components(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> List[Set[str]]:
    graph: Dict[str, Set[str]] = {n: set() for n in nodes}
    for u, v in edges:
        if u in graph and v in graph:
            graph[u].add(v)
            graph[v].add(u)
    
    seen = set()
    comps = []
    for start in graph:
        if start in seen:
            continue
        stack = [start]
        comp = set()
        while stack:
            curr = stack.pop()
            if curr in seen:
                continue
            seen.add(curr)
            comp.add(curr)
            for neighbor in graph[curr]:
                if neighbor not in seen:
                    stack.append(neighbor)
        comps.append(comp)
    comps.sort(key=lambda c: (-len(c), sorted(list(c))))
    return comps

def main():
    # 1. Load mapping
    patch_to_sheet = {}
    if pd.io.common.file_exists("MANIFOLD_PATCH_TABLE.csv"):
        df_patch = pd.read_csv("MANIFOLD_PATCH_TABLE.csv")
        for _, row in df_patch.iterrows():
            pid = str(row.get("patch_id", "")).strip()
            pname = str(row.get("patch_name", "")).strip()
            sid = extract_sheet_id(pname) or pname
            if pid:
                patch_to_sheet[pid] = sid

    def resolve(node):
        node_str = str(node).strip()
        if node_str in patch_to_sheet:
            return patch_to_sheet[node_str]
        return extract_sheet_id(node_str) or node_str

    # 2. Load edges
    all_edges: List[Edge] = []
    
    # Applied/Planned edges from SEAM_GLUE_MAP.csv
    if pd.io.common.file_exists("SEAM_GLUE_MAP.csv"):
        df_glue = pd.read_csv("SEAM_GLUE_MAP.csv")
        for _, row in df_glue.iterrows():
            u = resolve(row.get("patch_a"))
            v = resolve(row.get("patch_b"))
            if u and v and u != v:
                all_edges.append(Edge(
                    u=u, v=v, source_table="SEAM_GLUE_MAP.csv",
                    applied=True, viable=True,
                    contact_score=None, gap_min_dist=None,
                    raw=row.to_dict()
                ))
    
    # Candidate/Failure edges from seam_failure_table.csv
    if pd.io.common.file_exists("seam_failure_table.csv"):
        df_fail = pd.read_csv("seam_failure_table.csv")
        for _, row in df_fail.iterrows():
            u = resolve(row.get("seam_a"))
            v = resolve(row.get("seam_b"))
            if u and v and u != v:
                viable = str(row.get("percolation_candidate_flag", "")).lower() == "true"
                try:
                    score = float(row.get("contact_score")) if pd.notna(row.get("contact_score")) else None
                except: score = None
                try:
                    gap = float(row.get("gap_min_dist")) if pd.notna(row.get("gap_min_dist")) else None
                except: gap = None
                
                all_edges.append(Edge(
                    u=u, v=v, source_table="seam_failure_table.csv",
                    applied=False, viable=viable,
                    contact_score=score, gap_min_dist=gap,
                    raw=row.to_dict()
                ))

    nodes = sorted(list(set([e.u for e in all_edges] + [e.v for e in all_edges])))
    
    # 3. Baseline components (only applied edges)
    applied_edges = [(e.u, e.v) for e in all_edges if e.applied]
    baseline_comps = get_components(nodes, applied_edges)
    
    # 4. Scenario: what if we apply all viable candidates?
    scenario_edges = [(e.u, e.v) for e in all_edges if e.applied or e.viable]
    scenario_comps = get_components(nodes, scenario_edges)
    
    # Map nodes to scenario component index
    node_to_comp = {}
    for i, comp in enumerate(scenario_comps):
        for n in comp:
            node_to_comp[n] = i
            
    # 5. Find bridges between scenario components
    bridges = []
    for e in all_edges:
        if e.applied or e.viable:
            continue
        idx_u = node_to_comp.get(e.u)
        idx_v = node_to_comp.get(e.v)
        if idx_u is not None and idx_v is not None and idx_u != idx_v:
            bridges.append(e)
            
    # Sort bridges by gap distance (ascending) then contact score (descending)
    def bridge_sort_key(e: Edge):
        gap = e.gap_min_dist if e.gap_min_dist is not None else 999999.0
        score = e.contact_score if e.contact_score is not None else -1.0
        return (gap, -score)
    
    bridges.sort(key=bridge_sort_key)
    
    # 6. Report
    print(f"Audit Results:")
    print(f"Total Nodes: {len(nodes)}")
    print(f"Baseline Components (Applied): {len(baseline_comps)}")
    print(f"Scenario Components (Applied + Viable): {len(scenario_comps)}")
    
    if len(scenario_comps) > 1:
        print(f"\nRemaining disconnected component pairs:")
        for i, comp in enumerate(scenario_comps):
            print(f"  Comp {i}: {sorted(list(comp))}")
            
        print(f"\nALL Candidate Bridging Edges (to close geometry):")
        if not bridges:
            print("  No bridging edges found in the data.")
        for b in bridges:
            print(f"  {b.u} <--> {b.v} | Gap: {b.gap_min_dist} | Score: {b.contact_score} | Source: {b.source_table} | Reason: {b.raw.get('blocked_reason')}")
    else:
        print("\nGeometry is fully closed in the Scenario (Applied + Viable).")

    # Save to JSON as requested
    report = {
        "summary": {
            "nodes": len(nodes),
            "baseline_components": len(baseline_comps),
            "scenario_components": len(scenario_comps)
        },
        "components": [sorted(list(c)) for c in scenario_comps],
        "bridges": [
            {
                "u": b.u, "v": b.v, 
                "gap": b.gap_min_dist, 
                "score": b.contact_score, 
                "table": b.source_table,
                "blocked_reason": b.raw.get("blocked_reason")
            } for b in bridges
        ]
    }
    with open("geometry_audit_report.json", "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()
