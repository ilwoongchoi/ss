"""Circuit Wiring Validation Engine.

Validates all forward/reverse connections in the circuit:
- Port/node existence
- Port type compatibility (out/ctrl → in/ctrl)
- Bidirectional consistency
- Cycle detection
- Isolated node detection

Generates detailed error report highlighting incorrect wiring.
"""
from __future__ import annotations

import json
import pathlib
from collections import defaultdict
from typing import Dict, List, Set, Tuple

from .circuit_loader import NODES

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Validation Results
# ---------------------------------------------------------------------------
class ValidationResult:
    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        self.stats: Dict[str, int] = defaultdict(int)

    def add_error(self, error_type: str, node: str, port: str, message: str, target: str = ""):
        self.errors.append({
            "type": error_type,
            "node": node,
            "port": port,
            "message": message,
            "target": target,
        })
        self.stats["total_errors"] += 1
        self.stats[f"error_{error_type}"] += 1

    def add_warning(self, warning_type: str, node: str, message: str):
        self.warnings.append({
            "type": warning_type,
            "node": node,
            "message": message,
        })
        self.stats["total_warnings"] += 1
        self.stats[f"warning_{warning_type}"] += 1

# ---------------------------------------------------------------------------
# Validation Functions
# ---------------------------------------------------------------------------
def parse_link(link: str) -> Tuple[str, str]:
    """Parse link string 'node.port' into (node, port)."""
    if "." not in link:
        return link, ""
    parts = link.split(".", 1)
    return parts[0], parts[1]

def validate_node_existence(result: ValidationResult):
    """Check that all linked nodes exist in NODES."""
    for node_name, node in NODES.items():
        for port in node.ports:
            if not port.link:
                continue
            
            target_node, target_port = parse_link(port.link)
            
            if target_node not in NODES:
                result.add_error(
                    "missing_target_node",
                    node_name,
                    port.name,
                    f"Target node '{target_node}' does not exist in circuit",
                    target_node,
                )

def validate_port_existence(result: ValidationResult):
    """Check that all linked ports exist on target nodes."""
    for node_name, node in NODES.items():
        for port in node.ports:
            if not port.link:
                continue
            
            target_node, target_port = parse_link(port.link)
            
            if target_node not in NODES:
                continue  # Already caught by node existence check
            
            target_node_obj = NODES[target_node]
            target_ports = {p.name: p for p in target_node_obj.ports}
            
            if target_port not in target_ports:
                result.add_error(
                    "missing_target_port",
                    node_name,
                    port.name,
                    f"Target port '{target_port}' does not exist on node '{target_node}'",
                    f"{target_node}.{target_port}",
                )

def validate_port_type_compatibility(result: ValidationResult):
    """Check that port types are compatible (out/ctrl → in/ctrl)."""
    valid_transitions = {
        "out": ["in", "ctrl"],
        "ctrl": ["in", "ctrl"],
        "in": [],  # in ports should not have outgoing links
    }
    
    for node_name, node in NODES.items():
        for port in node.ports:
            if not port.link:
                continue
            
            target_node, target_port = parse_link(port.link)
            
            if target_node not in NODES:
                continue
            if target_port == "":
                continue
            
            target_node_obj = NODES[target_node]
            target_ports = {p.name: p for p in target_node_obj.ports}
            
            if target_port not in target_ports:
                continue  # Already caught by port existence check
            
            target_port_obj = target_ports[target_port]
            
            # Check if this transition is valid
            if port.kind not in valid_transitions:
                result.add_error(
                    "invalid_source_port_type",
                    node_name,
                    port.name,
                    f"Source port kind '{port.kind}' cannot have outgoing links",
                    f"{target_node}.{target_port}",
                )
            elif target_port_obj.kind not in valid_transitions[port.kind]:
                result.add_error(
                    "port_type_mismatch",
                    node_name,
                    port.name,
                    f"Port type '{port.kind}' → '{target_port_obj.kind}' is invalid",
                    f"{target_node}.{target_port}",
                )

def validate_bidirectional_consistency(result: ValidationResult):
    """Check that reverse links exist and are consistent."""
    for node_name, node in NODES.items():
        for port in node.ports:
            if not port.link:
                continue
            
            target_node, target_port = parse_link(port.link)
            
            if target_node not in NODES:
                continue
            if target_port == "":
                continue
            
            target_node_obj = NODES[target_node]
            target_ports = {p.name: p for p in target_node_obj.ports}
            
            if target_port not in target_ports:
                continue
            
            target_port_obj = target_ports[target_port]
            
            # Check if target port links back to this node
            if not target_port_obj.link:
                result.add_warning(
                    "missing_reverse_link",
                    f"{target_node}.{target_port}",
                    f"Port does not have a reverse link to '{node_name}.{port.name}'",
                )
                continue
            
            reverse_node, reverse_port = parse_link(target_port_obj.link)
            
            if reverse_node != node_name or reverse_port != port.name:
                result.add_error(
                    "reverse_link_mismatch",
                    node_name,
                    port.name,
                    f"Reverse link points to '{reverse_node}.{reverse_port}', expected '{node_name}.{port.name}'",
                    f"{target_node}.{target_port}",
                )

def detect_cycles(result: ValidationResult):
    """Detect cycles in the circuit graph."""
    # Build adjacency list
    adj = defaultdict(list)
    for node_name, node in NODES.items():
        for port in node.ports:
            if port.kind in ["out", "ctrl"] and port.link:
                target_node, _ = parse_link(port.link)
                if target_node in NODES:
                    adj[node_name].append(target_node)
    
    # Detect cycles using DFS
    visited = set()
    rec_stack = set()
    cycles = []
    
    def dfs(node: str, path: List[str]):
        if node in rec_stack:
            cycle_start = path.index(node)
            cycle = path[cycle_start:] + [node]
            cycles.append(cycle)
            return
        if node in visited:
            return
        
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in adj[node]:
            dfs(neighbor, path)
        
        path.pop()
        rec_stack.remove(node)
    
    for node_name in NODES:
        if node_name not in visited:
            dfs(node_name, [])
    
    # Report cycles
    for cycle in cycles:
        cycle_str = " → ".join(cycle)
        result.add_error(
            "cycle_detected",
            cycle[0],
            "",
            f"Cycle detected: {cycle_str}",
            "",
        )

def detect_isolated_nodes(result: ValidationResult):
    """Detect nodes with no connections."""
    for node_name, node in NODES.items():
        has_incoming = False
        has_outgoing = False
        
        for port in node.ports:
            if port.kind == "in" and port.link:
                has_incoming = True
            if port.kind in ["out", "ctrl"] and port.link:
                has_outgoing = True
        
        if not has_incoming and not has_outgoing:
            result.add_warning(
                "isolated_node",
                node_name,
                f"Node has no incoming or outgoing connections",
            )
        elif not has_incoming:
            result.add_warning(
                "no_incoming_connections",
                node_name,
                f"Node has no incoming connections",
            )
        elif not has_outgoing:
            result.add_warning(
                "no_outgoing_connections",
                node_name,
                f"Node has no outgoing connections",
            )

def validate_self_loops(result: ValidationResult):
    """Check for ports that link to the same node."""
    for node_name, node in NODES.items():
        for port in node.ports:
            if not port.link:
                continue
            
            target_node, _ = parse_link(port.link)
            
            if target_node == node_name:
                result.add_error(
                    "self_loop",
                    node_name,
                    port.name,
                    f"Port links to the same node (self-loop)",
                    f"{target_node}",
                )

# ---------------------------------------------------------------------------
# Main Validation
# ---------------------------------------------------------------------------
def validate_circuit() -> ValidationResult:
    """Run all validation checks."""
    result = ValidationResult()
    
    print("Validating circuit wiring...")
    print(f"Total nodes: {len(NODES)}")
    
    # Count total ports
    total_ports = sum(len(node.ports) for node in NODES.values())
    print(f"Total ports: {total_ports}")
    
    # Run validations
    print("\n1. Checking node existence...")
    validate_node_existence(result)
    
    print("2. Checking port existence...")
    validate_port_existence(result)
    
    print("3. Checking port type compatibility...")
    validate_port_type_compatibility(result)
    
    print("4. Checking bidirectional consistency...")
    validate_bidirectional_consistency(result)
    
    print("5. Detecting cycles...")
    detect_cycles(result)
    
    print("6. Detecting isolated nodes...")
    detect_isolated_nodes(result)
    
    print("7. Checking for self-loops...")
    validate_self_loops(result)
    
    return result

# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------
def generate_report(result: ValidationResult, output_path: pathlib.Path):
    """Generate detailed validation report."""
    lines = []
    lines.append("=" * 80)
    lines.append("CIRCUIT WIRING VALIDATION REPORT")
    lines.append("=" * 80)
    lines.append("")
    
    # Summary
    lines.append("SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Total nodes: {len(NODES)}")
    lines.append(f"Total ports: {sum(len(node.ports) for node in NODES.values())}")
    lines.append(f"Total errors: {result.stats['total_errors']}")
    lines.append(f"Total warnings: {result.stats['total_warnings']}")
    lines.append("")
    
    # Error breakdown
    lines.append("ERROR BREAKDOWN")
    lines.append("-" * 80)
    for key, count in result.stats.items():
        if key.startswith("error_"):
            error_type = key.replace("error_", "")
            lines.append(f"  {error_type}: {count}")
    lines.append("")
    
    # Warning breakdown
    lines.append("WARNING BREAKDOWN")
    lines.append("-" * 80)
    for key, count in result.stats.items():
        if key.startswith("warning_"):
            warning_type = key.replace("warning_", "")
            lines.append(f"  {warning_type}: {count}")
    lines.append("")
    
    # Detailed errors
    if result.errors:
        lines.append("DETAILED ERRORS")
        lines.append("-" * 80)
        for i, error in enumerate(result.errors, 1):
            lines.append(f"{i}. [{error['type']}]")
            lines.append(f"   Node: {error['node']}")
            lines.append(f"   Port: {error['port']}")
            lines.append(f"   Target: {error['target']}")
            lines.append(f"   Message: {error['message']}")
            lines.append("")
    
    # Detailed warnings
    if result.warnings:
        lines.append("DETAILED WARNINGS")
        lines.append("-" * 80)
        for i, warning in enumerate(result.warnings, 1):
            lines.append(f"{i}. [{warning['type']}]")
            lines.append(f"   Node: {warning['node']}")
            lines.append(f"   Message: {warning['message']}")
            lines.append("")
    
    text = "\n".join(lines)
    print(text)
    output_path.write_text(text, encoding="utf-8")
    
    # Also write JSON
    json_path = output_path.with_suffix(".json")
    json_data = {
        "summary": dict(result.stats),
        "errors": result.errors,
        "warnings": result.warnings,
    }
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"\n→ TXT: {output_path}")
    print(f"→ JSON: {json_path}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result = validate_circuit()
    report_path = GEN_DIR / "circuit_validation_report.txt"
    generate_report(result, report_path)
