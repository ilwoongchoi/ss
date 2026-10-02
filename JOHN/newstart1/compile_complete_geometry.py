import pandas as pd
import json

def main():
    print("=== [COMPILING COMPLETE UNIVERSAL GEOMETRY] ===")
    
    # 1. Load All Nodes (Structures)
    nodes = []
    try:
        patch_df = pd.read_csv("MANIFOLD_PATCH_TABLE.csv")
        for _, row in patch_df.iterrows():
            nodes.append({
                "id": str(row.get("patch_id", "")),
                "name": str(row.get("patch_name", "")),
                "role": str(row.get("component_role", ""))
            })
    except Exception as e:
        print(f"Error loading patches: {e}")

    # Add isolated nodes known from the context
    known_nodes = [n["name"] for n in nodes]
    for n in ["core_center", "right_branch"]:
        if n not in known_nodes:
            nodes.append({"id": "N/A", "name": n, "role": "Isolated Funnel Component"})

    # 2. Load All Applied Bridges
    bridges = []
    try:
        glue_df = pd.read_csv("SEAM_GLUE_MAP.csv")
        for _, row in glue_df.iterrows():
            bridges.append({
                "source": str(row.get("patch_a")),
                "target": str(row.get("patch_b")),
                "type": str(row.get("seam_type")),
                "status": "APPLIED",
                "score": 1.0,
                "gap": 0.0
            })
    except Exception as e:
        pass

    # 3. Load All Blocked/Candidate Bridges
    try:
        fail_df = pd.read_csv("seam_failure_table.csv")
        for _, row in fail_df.iterrows():
            score = float(row.get("contact_score")) if pd.notna(row.get("contact_score")) else "N/A"
            gap = float(row.get("gap_min_dist")) if pd.notna(row.get("gap_min_dist")) else "N/A"
            bridges.append({
                "source": str(row.get("seam_a")),
                "target": str(row.get("seam_b")),
                "type": str(row.get("edge_type", "candidate")),
                "status": "CANDIDATE/BLOCKED",
                "score": score,
                "gap": gap
            })
    except Exception as e:
        pass

    # 4. Load Missing Bridges (Calculated Vectors)
    try:
        calc_df = pd.read_csv("calculated_bridge_results.csv")
        for _, row in calc_df.iterrows():
            bridges.append({
                "source": str(row.get("seam_a")),
                "target": str(row.get("seam_b")),
                "type": "calculated_missing_vector",
                "status": "STRUCTURAL_LINK",
                "score": float(row.get("contact_score", 0)),
                "gap": float(row.get("gap_min_dist", 0)),
                "vector": str(row.get("vector"))
            })
    except Exception as e:
        pass

    geometry = {
        "nodes": nodes,
        "bridges": bridges,
        "total_node_count": len(nodes),
        "total_bridge_count": len(bridges)
    }

    with open("UNIVERSAL_GEOMETRY_COMPLETE_MAP.json", "w") as f:
        json.dump(geometry, f, indent=2)

    print(f"Total Structures (Nodes) Found: {len(nodes)}")
    print(f"Total Bridges (Vectors) Found: {len(bridges)}")
    
    print("\n[CRITICAL STRUCTURAL CONNECTIONS TO FUNNEL]")
    for b in bridges:
        if b["source"] in ["core_center", "right_branch"] or b["target"] in ["core_center", "right_branch"]:
            if b["status"] != "CANDIDATE/BLOCKED": # Print the calculated ones to show the physical links
                print(f" - {b['source']} <-> {b['target']} | Gap: {b['gap']} | Score: {b['score']} | Vector: {b.get('vector', 'N/A')}")

if __name__ == "__main__":
    main()
