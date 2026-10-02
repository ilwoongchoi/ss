import pandas as pd
import json
import itertools
from collections import defaultdict

def resolve_node(raw_node, patch_map):
    text = str(raw_node).strip()
    if text in patch_map:
        return patch_map[text]
    # Handle sheet_id:X format
    if "sheet_id:" in text:
        return text.split(":")[-1]
    return text

def get_components(nodes, edges):
    graph = {n: set() for n in nodes}
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
    # 1. Map patch_id -> sheet_id
    patch_map = {}
    try:
        df_patch = pd.read_csv("MANIFOLD_PATCH_TABLE.csv")
        # Columns: patch_id, patch_name
        for _, row in df_patch.iterrows():
            pid = str(row.get("patch_id", "")).strip()
            pname = str(row.get("patch_name", "")).strip()
            if "sheet_id:" in pname:
                sid = pname.split(":")[-1]
                patch_map[pid] = sid
            else:
                patch_map[pid] = pname
    except Exception as e:
        print(f"Error loading patch table: {e}")

    # 2. Build edges
    applied_edges = []
    viable_edges = []
    all_nodes = set()

    # Applied from SEAM_GLUE_MAP.csv
    try:
        df_glue = pd.read_csv("SEAM_GLUE_MAP.csv")
        for _, row in df_glue.iterrows():
            u = resolve_node(row.get("patch_a"), patch_map)
            v = resolve_node(row.get("patch_b"), patch_map)
            if u and v and u != v:
                applied_edges.append((u, v))
                all_nodes.update([u, v])
    except Exception as e:
        print(f"Error loading glue map: {e}")

    # Candidates from seam_failure_table.csv
    try:
        df_fail = pd.read_csv("seam_failure_table.csv")
        for _, row in df_fail.iterrows():
            u = resolve_node(row.get("seam_a"), patch_map)
            v = resolve_node(row.get("seam_b"), patch_map)
            if u and v and u != v:
                all_nodes.update([u, v])
                viable = str(row.get("percolation_candidate_flag", "")).lower() == "true"
                if viable:
                    viable_edges.append((u, v))
    except Exception as e:
        print(f"Error loading failure table: {e}")

    nodes_list = sorted(list(all_nodes))
    
    # 3. Components
    baseline_comps = get_components(nodes_list, applied_edges)
    scenario_comps = get_components(nodes_list, applied_edges + viable_edges)

    result = {
        "baseline": [sorted(list(c)) for c in baseline_comps],
        "scenario": [sorted(list(c)) for c in scenario_comps]
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
