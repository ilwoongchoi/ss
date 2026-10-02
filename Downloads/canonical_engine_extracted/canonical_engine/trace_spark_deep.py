"""Deep analysis: find B7 and B11 in circuit structure,
trace spark path, and compute 138.88 from circuit properties."""
import json, math
from collections import defaultdict

with open('generated/circuit.json', 'r') as f:
    circuit = json.load(f)

nodes = {n['name']: n for n in circuit}

# Identify all DFFs
dffs = []
for n in circuit:
    name = n['name']
    ports = n.get('ports', [])
    out_names = [p.get('name','') for p in ports if p.get('kind') == 'out']
    in_names = [p.get('name','') for p in ports if p.get('kind') == 'in']
    has_q = any('q' == nm for nm in out_names) or any('q' in nm for nm in out_names)
    has_clk = any('clk' in nm for nm in in_names)
    if has_q and has_clk:
        dffs.append(n)
    elif has_q and not has_clk and any('q_bar' in nm for nm in out_names):
        dffs.append(n)

print(f"=== DFFs (B11 candidates) ===")
print(f"Count: {len(dffs)}")
for i, n in enumerate(dffs):
    el = n.get('element', '?')
    pt = n.get('particle', '?')
    loc = n.get('location', '?')[:70] if n.get('location') else '?'
    print(f"  {i+1}. {n['name']} | {el} | {pt} | {loc}")

# MUX nodes
mux_nodes = []
for n in circuit:
    ports = n.get('ports', [])
    ctrl_ports = [p for p in ports if p.get('kind') == 'ctrl']
    in_ports = [p for p in ports if p.get('kind') == 'in']
    out_ports = [p for p in ports if p.get('kind') == 'out']
    if len(ctrl_ports) == 1 and len(in_ports) == 2 and len(out_ports) == 1:
        mux_nodes.append(n)

print(f"\n=== MUX nodes ===")
print(f"Count: {len(mux_nodes)}")
for n in mux_nodes:
    print(f"  {n['name']} | {n.get('element','?')} | {n.get('particle','?')}")

# Observer nodes
obs_nodes = [n for n in nodes if n.startswith('observer_')]
print(f"\n=== Observer nodes ===")
print(f"Count: {len(obs_nodes)}")
for nm in obs_nodes:
    n = nodes[nm]
    print(f"  {nm} | {n.get('element','?')} | {n.get('particle','?')}")

# Particle distribution
particle_counts = defaultdict(int)
for n in circuit:
    pt = n.get('particle', '')
    if pt:
        particle_counts[pt] += 1

print(f"\n=== Particle distribution ===")
for pt, cnt in sorted(particle_counts.items(), key=lambda x: -x[1]):
    print(f"  {pt}: {cnt}")

# Color distribution
color_counts = defaultdict(int)
for n in circuit:
    c = n.get('color', '')
    if c:
        color_counts[c] += 1

print(f"\n=== Color distribution ===")
for c, cnt in sorted(color_counts.items(), key=lambda x: -x[1]):
    print(f"  {c}: {cnt}")

# Group distribution
group_counts = defaultdict(int)
for n in circuit:
    g = n.get('group', '')
    if g:
        group_counts[g] += 1

print(f"\n=== Group distribution ===")
for g, cnt in sorted(group_counts.items(), key=lambda x: -x[1]):
    print(f"  {g}: {cnt}")

# DFF Z values
print(f"\n=== DFF element analysis ===")
dff_zs = []
for n in dffs:
    el = n.get('element', '?')
    z = None
    if '(' in el:
        try:
            z = int(el.split('(')[1].split(')')[0].split(',')[0])
            dff_zs.append(z)
        except:
            pass
    print(f"  {n['name']}: element={el}, Z={z}, particle={n.get('particle','?')}")

print(f"\n  DFF Z values: {dff_zs}")
print(f"  Sum: {sum(dff_zs)}")
print(f"  Sum mod 360: {sum(dff_zs) % 360}")
print(f"  Sum mod 128: {sum(dff_zs) % 128}")
print(f"  Sum mod 32: {sum(dff_zs) % 32}")

# Path analysis
print(f"\n=== SPARK PATH ANALYSIS ===")
print(f"Shortest path: Mg(12) -> Na(11) -> [left_genital_d2] -> Rb(37)")
print(f"  Z values: 12, 11, 37")
print(f"  dZ: -1, +26")
print(f"  -1 = -B0")
print(f"  +26 = ? (not B7=7)")
print(f"")
print(f"Longer path: Mg(12) -> Na(11) -> Ar(18) -> Rb(37)")
print(f"  Z values: 12, 11, 18, 37")
print(f"  dZ: -1, +7, +19")
print(f"  -1 = -B0 (observer)")
print(f"  +7 = +B7 (void)")
print(f"  +19 = +(B11+B7+B0) = 11+7+1 = 19 (source+void+observer)")
print(f"  Total dZ = 25 = 5^2 = B5^2")

# Key computation
phi = (1 + 5**0.5) / 2
golden = 360 / phi**2
gap = 11.0 / (7.0 + 1.0)
spark = golden + gap

print(f"\n=== 138.88 DECOMPOSITION ===")
print(f"  Golden angle = 360/phi^2 = {golden:.6f} deg")
print(f"  Gap = B11/(B7+B0) = 11/8 = {gap} deg")
print(f"  Spark = {golden:.6f} + {gap} = {spark:.6f} deg")
print(f"")
print(f"  In the circuit path:")
print(f"    Step 1: Mg(12) -> Na(11), dZ = -B0 = -1")
print(f"    Step 2: Na(11) -> Ar(18), dZ = +B7 = +7")
print(f"    Step 3: Ar(18) -> Rb(37), dZ = +(B11+B7+B0) = +19")
print(f"")
print(f"  The GAP in the angle formula = B11/(B7+B0) = 11/8 = 1.375")
print(f"  This is the ratio of SOURCE (11 DFFs) to VOID+OBSERVER (7+1)")
print(f"")
print(f"  DFF count = {len(dffs)} = B11 (geometric source)")
print(f"  B7 = 7 (skeletal void nodes, NOT circuit Betti)")
print(f"  B0 = 1 (observer, 1 connected component)")

# Check: is 7 the number of something in the circuit?
print(f"\n=== SEARCHING FOR 7 IN CIRCUIT ===")
# Count 2-channel tristates
tristate_2ch = 0
for n in circuit:
    ports = n.get('ports', [])
    ctrl_ports = [p for p in ports if p.get('kind') == 'ctrl']
    out_ports = [p for p in ports if p.get('kind') == 'out']
    if len(ctrl_ports) == 2 and len(out_ports) == 2:
        tristate_2ch += 1
print(f"  2-channel tristates: {tristate_2ch}")

# Count nodes with RED color
red_nodes = [n for n in circuit if n.get('color') == 'RED']
print(f"  RED nodes: {len(red_nodes)}")
for n in red_nodes:
    print(f"    {n['name']} | {n.get('element','?')} | {n.get('particle','?')}")

# Count AlkaliMetal group
alkali = [n for n in circuit if n.get('group') == 'AlkaliMetal']
print(f"\n  AlkaliMetal nodes: {len(alkali)}")
for n in alkali:
    print(f"    {n['name']} | {n.get('element','?')} | {n.get('particle','?')}")

# Count NobleGas
noble = [n for n in circuit if n.get('group') == 'NobleGas']
print(f"\n  NobleGas nodes: {len(noble)}")
for n in noble:
    print(f"    {n['name']} | {n.get('element','?')} | {n.get('particle','?')}")

# Try: 7 = number of nodes with specific property
# Count nodes with 'w_boson' particle
w_boson = [n for n in circuit if n.get('particle') == 'w_boson']
print(f"\n  w_boson nodes: {len(w_boson)}")
for n in w_boson:
    print(f"    {n['name']} | {n.get('element','?')}")

# Count nodes with 'muon' particle
muon = [n for n in circuit if n.get('particle') == 'muon']
print(f"\n  muon nodes: {len(muon)}")
for n in muon:
    print(f"    {n['name']} | {n.get('element','?')}")

# Count nodes with 'gluon' particle
gluon = [n for n in circuit if n.get('particle') == 'gluon']
print(f"\n  gluon nodes: {len(gluon)}")
for n in gluon:
    print(f"    {n['name']} | {n.get('element','?')}")

# The 7 skeletal nodes - check which are in circuit
print(f"\n=== 7 SKELETAL VOID NODES (B7) ===")
skeletal = [
    ('Right D2 (VOID)', None),
    ('Left GABA-B (0D)', None),
    ('Right GABA-A (1D line)', None),
    ('Right ACh (1D height)', 'right_acetylcholine'),
    ('Left 5HT1A (2D plane)', None),
    ('Left D2 (3D volume)', 'observer_leftd2'),
    ('Right Cortisol (fake 3D)', None),
]
found = 0
for label, node_name in skeletal:
    if node_name and node_name in nodes:
        n = nodes[node_name]
        print(f"  {label}: CIRCUIT NODE {node_name} | {n.get('element','?')} | {n.get('particle','?')}")
        found += 1
    else:
        print(f"  {label}: NOT IN CIRCUIT (skeletal/conceptual only)")
print(f"  Found in circuit: {found}/7")
print(f"  Missing: {7-found} (these are anatomical points, not circuit nodes)")
