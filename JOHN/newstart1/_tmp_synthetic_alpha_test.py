
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Set

@dataclass
class DSU:
    """Disjoint Set Union."""
    parent: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def from_nodes(cls, nodes: List[str]) -> "DSU":
        return cls(parent={n: n for n in nodes})
    
    def find(self, x: str) -> str:
        if x not in self.parent:
            self.parent[x] = x
            return x
        p = self.parent[x]
        if p != x:
            self.parent[x] = self.find(p)
        return self.parent[x]
    
    def union(self, a: str, b: str) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[rb] = ra
        return True
    
    def components(self) -> int:
        return len({self.find(x) for x in self.parent})

def run_test():
    # 0. Initial State
    main_nodes = [
        "sheet_id:1", "sheet_id:2", "sheet_id:3", "sheet_id:4",
        "sheet_id:10", "sheet_id:11", "sheet_id:12", "sheet_id:13", "sheet_id:14",
        "flash_bridge", "flash:center_in"
    ]
    isolated_nodes = ["gateway_peak"]
    
    all_initial_nodes = main_nodes + isolated_nodes
    dsu = DSU.from_nodes(all_initial_nodes)
    
    # Form the main component
    for i in range(len(main_nodes) - 1):
        dsu.union(main_nodes[0], main_nodes[i+1])
        
    trace = []
    
    # Step 0: Initial
    trace.append({
        "step": 0,
        "action": "initial_locked_state",
        "nodes": len(dsu.parent),
        "components": dsu.components()
    })
    
    # 1. Add mediator:synthetic_alpha to the universe
    mediator = "mediator:synthetic_alpha"
    dsu.find(mediator) # Ensures it's in the DSU
    trace.append({
        "step": 1,
        "action": "add_synthetic_alpha",
        "nodes": len(dsu.parent),
        "components": dsu.components()
    })
    
    # 2. Activate gateway_peak <-> mediator:synthetic_alpha seam
    dsu.union("gateway_peak", mediator)
    trace.append({
        "step": 2,
        "action": "activate_gateway_peak_seam",
        "nodes": len(dsu.parent),
        "components": dsu.components()
    })
    
    # 3. Activate mediator:synthetic_alpha <-> sheet_id:4 relay
    dsu.union(mediator, "sheet_id:4")
    trace.append({
        "step": 3,
        "action": "activate_sheet_id_4_relay",
        "nodes": len(dsu.parent),
        "components": dsu.components()
    })
    
    df_trace = pd.DataFrame(trace)
    df_trace.to_csv("SYNTHETIC_ALPHA_COMPONENT_TRACE.csv", index=False)
    
    final_components = dsu.components()
    verdict = "SUCCESS" if final_components == 1 else "FAILURE"
    
    with open("FINAL_2TO1_VERDICT.md", "w") as f:
        f.write(f"# Final 2→1 Verdict\n\n")
        f.write(f"**Target**: 2→1 component reduction via mediator:synthetic_alpha\n")
        f.write(f"**Final Components**: {final_components}\n")
        f.write(f"**Status**: {verdict}\n\n")
        if final_components == 1:
            f.write(f"The mediator:synthetic_alpha successfully bridges the gateway_peak to the main component.\n")
        else:
            f.write(f"The mediator:synthetic_alpha failed to reduce the state to 1 component.\n")

    # Generate Report
    report = f"""# Synthetic Alpha Activation Report

## Test Parameters
- **Base State**: 2 components (Main + gateway_peak)
- **Mediator**: mediator:synthetic_alpha
- **Activation Path**: gateway_peak <-> mediator:synthetic_alpha <-> sheet_id:4

## Step-by-Step Trace

| Step | Action | Nodes | Components |
|------|--------|-------|------------|
"""
    for _, row in df_trace.iterrows():
        report += f"| {row['step']} | {row['action']} | {row['nodes']} | {row['components']} |\n"
        
    report += f"""
## Verification
- Initial components: {trace[0]['components']}
- Final components: {final_components}
- Reduction: {trace[0]['components'] - final_components}

## Conclusion
The activation arithmetic confirms that adding a mediator with seams to both the isolated node and the main component's sheet_id:4 results in a single connected component.
"""
    with open("SYNTHETIC_ALPHA_ACTIVATION_REPORT.md", "w") as f:
        f.write(report)

    print("Test complete. Outputs generated.")

if __name__ == "__main__":
    run_test()
