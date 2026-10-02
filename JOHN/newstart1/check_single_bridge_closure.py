import pandas as pd
import json

def main():
    # 1. Load current graph
    edges = []
    # Base Applied
    try:
        df_glue = pd.read_csv("SEAM_GLUE_MAP.csv")
        for _, row in df_glue.iterrows():
            edges.append((str(row.get("patch_a")), str(row.get("patch_b"))))
    except: pass
    
    # Blocked but exist
    try:
        df_fail = pd.read_csv("seam_failure_table.csv")
        for _, row in df_fail.iterrows():
            edges.append((str(row.get("seam_a")), str(row.get("seam_b"))))
    except: pass

    # 2. Add THE BRIDGE (ISLAND -> MAIN)
    # Let's assume mediator:synthetic_alpha -> core_center is found
    edges.append(("mediator:synthetic_alpha", "core_center"))
    
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
        
    graph = {n: set() for n in nodes}
    for u, v in edges:
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
        
    print(f"--- [CLOSURE TEST] ---")
    print(f"Components found: {len(comps)}")
    if len(comps) == 1:
        print("[SUCCESS] Yes. Adding just ONE bridge between ISLAND and MAIN unites the entire geometry.")
    else:
        print(f"[FAILED] No. {len(comps)} components remain. More bridges needed.")

if __name__ == '__main__':
    main()
