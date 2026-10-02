import json
import sys

def analyze_cv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        with open(file_path, 'r', encoding='cp949') as f:
            data = json.load(f)

    print(f"Project Name: {data.get('name')}")
    
    for scope_idx, scope in enumerate(data.get('scopes', [])):
        scope_name = scope.get('name', f"Scope_{scope_idx}")
        print(f"\n=== {scope_name} (Index: {scope_idx}) ===")
        
        all_nodes = scope.get('allNodes', [])
        adj = {}
        for i, node in enumerate(all_nodes):
            adj[i] = node.get('connections', [])

        node_to_pin = {}
        all_devices = []

        # Find all keys that represent device lists
        for key, value in scope.items():
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                if key in ['allNodes', 'wires']: continue
                for dev in value:
                    obj_type = dev.get('objectType', key)
                    dev_id = dev.get('id', 'N/A')
                    label = dev.get('label', '')
                    
                    dev_info = {
                        'type': obj_type,
                        'label': label,
                        'id': dev_id,
                        'dev': dev
                    }
                    all_devices.append(dev_info)
                    
                    # Try to find node mappings in multiple places
                    n_map = dev.get('nodeList') or dev.get('customData', {}).get('nodes')
                    
                    # Handle SubCircuit separately if needed
                    if obj_type == 'SubCircuit':
                        for i, idx in enumerate(dev.get('inputNodes', [])):
                            node_to_pin[idx] = (dev_info, f"SC_In_{i}")
                        for i, idx in enumerate(dev.get('outputNodes', [])):
                            node_to_pin[idx] = (dev_info, f"SC_Out_{i}")
                    elif n_map:
                        if isinstance(n_map, dict):
                            for p, idx in n_map.items():
                                if isinstance(idx, list):
                                    for i, s_idx in enumerate(idx):
                                        node_to_pin[s_idx] = (dev_info, f"{p}[{i}]")
                                else:
                                    node_to_pin[idx] = (dev_info, p)
                        elif isinstance(n_map, list):
                            for i, idx in enumerate(n_map):
                                node_to_pin[idx] = (dev_info, f"node_{i}")

        def get_all_connected_pins(start_node_idx):
            visited = set()
            queue = [start_node_idx]
            connections = []
            while queue:
                curr = queue.pop(0)
                if curr in visited: continue
                visited.add(curr)
                if curr in node_to_pin:
                    connections.append(node_to_pin[curr])
                for neighbor in adj.get(curr, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
            return connections

        print("\n--- Direct Wire Connections between Labeled Devices ---")
        processed_pairs = set()
        for node_idx, (src_dev, src_pin) in node_to_pin.items():
            if not src_dev['label']: continue
            
            conns = get_all_connected_pins(node_idx)
            for dst_dev, dst_pin in conns:
                if src_dev['id'] == dst_dev['id']: continue
                if not dst_dev['label']: continue
                
                pair = tuple(sorted([(src_dev['id'], src_pin), (dst_dev['id'], dst_pin)]))
                if pair not in processed_pairs:
                    processed_pairs.add(pair)
                    print(f"'{src_dev['label']}' ({src_pin}) <---> '{dst_dev['label']}' ({dst_pin})")

        print("\n--- Logic Paths (Input -> Gates -> Output) ---")
        for dev in all_devices:
            if dev['type'] == 'Input' and dev['label']:
                print(f"Tracing Input: '{dev['label']}'")
                # Look for all pins of this input
                input_nodes = [idx for idx, (d, p) in node_to_pin.items() if d['id'] == dev['id']]
                for start_node in input_nodes:
                    conns = get_all_connected_pins(start_node)
                    for target_dev, target_pin in conns:
                        if target_dev['id'] == dev['id']: continue
                        t_name = target_dev['label'] or f"<{target_dev['type']}>"
                        print(f"  -> {t_name} on pin {target_pin}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_cv(sys.argv[1])
