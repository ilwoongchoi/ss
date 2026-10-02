"""Deep analysis: find B7 and B11 in circuit structure,
trace spark path, and compute 138.88 from circuit properties."""
import json, math
from collections import defaultdict, deque

with open('generated/circuit.json', 'r') as f:
    circuit = json.load(f)

nodes = {n['name']: n for n in circuit}
print(f"Total circuit nodes: {len(nodes)}")

# Build directed adjacency
adj = defaultdict(set)
for n in circuit:
    name = n['name']
    for p in n.get('ports', []):
        link = p.get('link', '')
        if link and '.' in link:
            target = link.split('.')[0]
            if target in nodes and target != name:
                adj[name].add(target)

# BFS shortest path
def bfs(start, end):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        if path[-1] == end:
            return path
        for nb in adj.get(path[-1], []):
            if nb not in visited:
                visited.add(nb)
                queue.append(path + [nb])
    return None

# Key nodes
philtrum = 'observer_left_endorphin_electron_antineutrino'
leftd2 = 'observer_leftd2'
aurora = 'aurora'
right_sole = 'right_sole_dopamine'
sulforaphane = 'sulforaphane'
sodium = 'sodium'

print(f"\n=== KEY NODES ===")
for name in [philtrum, leftd2, right_sole, sulforaphane, sodium, aurora]:
    n = nodes.get(name, {})
    print(f"  {name}: element={n.get('element','?')}, particle={n.get('particle','?')}, location={n.get('location','?')[:80]}")

# Trace all paths from philtrum to aurora (up to 10 hops)
def bfs_all_paths(start, end, max_hops=10):
    """Find all paths up to max_hops length"""
    results = []
    queue = deque([(start, [start])])
    while queue:
        node, path = queue.popleft()
        if len(path) > max_hops:
            continue
        if node == end and len(path) > 1:
            results.append(path)
            continue
        for nb in adj.get(node, []):
            if nb not in path:
                queue.append((nb, path + [nb]))
    return results

print(f"\n=== PATHS: philtrum -> aurora ===")
paths = bfs_all_paths(philtrum, aurora, max_hops=8)
paths.sort(key=len)
for i, p in enumerate(paths[:15]):
    elements = []
    for node in p:
        el = nodes[node].get('element', '?')
        # Extract atomic number from element string like "Mg(12)"
        if '(' in el:
            z = el.split('(')[1].split(')')[0]
            elements.append(f"{el.split('(')[0]}({z})")
        else:
            elements.append(el)
    print(f"  Path {i} ({len(p)-1} hops): {' -> '.join(p)}")
    print(f"    Elements: {' -> '.join(elements)}")

# Extract atomic numbers along shortest path
def get_z(name):
    el = nodes[name].get('element', '?')
    if '(' in el:
        try:
            return int(el.split('(')[1].split(')')[0].split(',')[0])
        except:
            return None
    return None

def get_element_symbol(name):
    el = nodes[name].get('element', '?')
    if '(' in el:
        return el.split('(')[0]
    return el

print(f"\n=== SHORTEST PATH ANALYSIS ===")
if paths:
    shortest = min(paths, key=len)
    print(f"Shortest path: {' -> '.join(shortest)}")
    print(f"\nNode details:")
    z_values = []
    for node in shortest:
        z = get_z(node)
        pt = nodes[node].get('particle', '?')
        loc = nodes[node].get('location', '?')
        if z:
            z_values.append(z)
        print(f"  {node}: Z={z}, particle={pt}, location={loc[:70] if loc else '?'}")
    
    print(f"\nZ values along path: {z_values}")
    print(f"Z differences: {[z_values[i+1]-z_values[i] for i in range(len(z_values)-1)]}")
    
    # Try various computations
    if z_values:
        print(f"\n=== COMPUTATION ATTEMPTS ===")
        print(f"  Sum of Z: {sum(z_values)}")
        print(f"  Sum of Z mod 360: {sum(z_values) % 360}")
        print(f"  Sum of |dZ|: {sum(abs(z_values[i+1]-z_values[i]) for i in range(len(z_values)-1))}")
        
        # Spark phase for each Z
        SPARK = 138.88
        print(f"\n  Spark phases (Z * 138.88 mod 360):")
        for z in z_values:
            phase = (z * SPARK) % 360
            print(f"    Z={z}: phase={phase:.2f} deg, cos={math.cos(math.radians(phase)):.4f}")
        
        # Phase differences
        phases = [(z * SPARK) % 360 for z in z_values]
        print(f"\n  Phase differences:")
        for i in range(len(phases)-1):
            diff = phases[i+1] - phases[i]
            print(f"    {z_values[i]}->{z_values[i+1]}: {diff:.2f} deg")

# Also check: what is the cycle structure of the circuit graph?
print(f"\n=== CIRCUIT GRAPH TOPOLOGY ===")
# Count nodes with self-loops, cycles, etc.
# Build undirected graph for cycle detection
undirected = defaultdict(set)
for a in adj:
    for b in adj[a]:
        undirected[a].add(b)
        undirected[b].add(a)

# Count edges
edge_count = sum(len(v) for v in undirected.values()) // 2
print(f"  Nodes: {len(nodes)}")
print(f"  Undirected edges: {edge_count}")

# For a connected graph: cycle_rank = E - V + components
# Find connected components
visited = set()
components = 0
for node in nodes:
    if node not in visited:
        components += 1
        stack = [node]
        while stack:
            n = stack.pop()
            if n in visited:
                continue
            visited.add(n)
            for nb in undirected.get(n, []):
                if nb not in visited:
                    stack.append(nb)

print(f"  Connected components: {components}")
cycle_rank = edge_count - len(nodes) + components
print(f"  Cycle rank (Betti 1): {cycle_rank}")

# Check if 7, 11 appear anywhere
print(f"\n  Cycle rank = {cycle_rank}")
print(f"  Is cycle_rank related to 7 or 11? {cycle_rank} vs 7={cycle_rank==7}, 11={cycle_rank==11}")

# Count node types
gate_types = defaultdict(int)
for n in circuit:
    name = n['name']
    # Infer gate type from node structure
    ports = n.get('ports', [])
    out_ports = [p for p in ports if p.get('kind') == 'out']
    in_ports = [p for p in ports if p.get('kind') == 'in']
    ctrl_ports = [p for p in ports if p.get('kind') == 'ctrl']
    
    if any('q' in p.get('name','') for p in out_ports):
        if any('clk' in p.get('name','') for p in in_ports):
            gate_types['DFF'] += 1
        else:
            gate_types['latch'] += 1
    elif len(ctrl_ports) > 0:
        gate_types['tristate'] += 1
    elif len(out_ports) == 1 and len(in_ports) >= 2:
        gate_types['logic'] += 1
    else:
        gate_types['other'] += 1

print(f"\n  Gate type counts: {dict(gate_types)}")
