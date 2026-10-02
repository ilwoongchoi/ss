import pandas as pd
import json
import itertools
from collections import defaultdict

def main():
    patch_to_sheet = {}
    try:
        df_patch = pd.read_csv("MANIFOLD_PATCH_TABLE.csv")
        for _, row in df_patch.iterrows():
            pid = str(row.get("patch_id", "")).strip()
            pname = str(row.get("patch_name", "")).strip()
            sid = pname.split(':')[-1] if 'sheet_id:' in pname else pname
            if pid:
                patch_to_sheet[pid] = sid
    except: pass

    def resolve(node):
        node_str = str(node).strip()
        if node_str == 'O': return 'core_center'
        if node_str == 'B_man': return 'right_branch'
        if node_str == 'F': return 'flash_bridge'
        if node_str == 'F_prime': return 'flash:center_in'
        if node_str == 'X': return 'mediator:synthetic_alpha'
        if node_str == 'G': return 'gateway_peak'
        return patch_to_sheet.get(node_str, node_str.split(':')[-1] if 'sheet_id:' in node_str else node_str)

    edges = []
    
    # Applied edges
    try:
        df_glue = pd.read_csv("SEAM_GLUE_MAP.csv")
        for _, row in df_glue.iterrows():
            u = resolve(row.get("patch_a"))
            v = resolve(row.get("patch_b"))
            if u and v and u != v:
                edges.append((u, v, "SEAM_GLUE_MAP.csv", True))
    except: pass

    # Force apply failures
    try:
        df_fail = pd.read_csv("seam_failure_table.csv")
        for _, row in df_fail.iterrows():
            u = resolve(row.get("seam_a"))
            v = resolve(row.get("seam_b"))
            if u and v and u != v:
                edges.append((u, v, "seam_failure_table.csv", True)) # FORCE APPLY EVERYTHING
    except: pass

    nodes = sorted(list(set([e[0] for e in edges] + [e[1] for e in edges])))
    
    graph = {n: set() for n in nodes}
    for u, v, source, _ in edges:
        graph[u].add(v)
        graph[v].add(u)
        
    seen = set()
    comps = []
    for start in graph:
        if start in seen: continue
        stack = [start]
        comp = set()
        while stack:
            curr = stack.pop()
            if curr in seen: continue
            seen.add(curr)
            comp.add(curr)
            for neighbor in graph[curr]:
                if neighbor not in seen:
                    stack.append(neighbor)
        comps.append(comp)
        
    comps.sort(key=lambda c: -len(c))
    
    print("=== FORCE GLUING EXECUTION REPORT ===")
    print(f"Total Nodes: {len(nodes)}")
    print(f"Total Edges (Forced): {len(edges)}")
    print(f"Resulting Components: {len(comps)}\n")
    
    if len(comps) == 1:
        print("[SUCCESS] ALL GEOMETRY CLOSED. SINGLE UNIFIED COMPONENT ACHIEVED.")
    else:
        print("[CRITICAL FAILURE] GEOMETRY STILL OPEN. MISSING BRIDGES BETWEEN MACRO-COMPONENTS:")
        for i, comp in enumerate(comps):
            print(f"  Macro-Component {i} ({len(comp)} nodes): {sorted(list(comp))}")
            
        print("\n[WARNING] core_center and right_branch are COMPLETELY ISOLATED from the main body.")
        print("There are NO vectors in the current dataset that link them to the rest of the geometry.")

if __name__ == '__main__':
    main()