import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Ellipse, FancyBboxPatch
from matplotlib.collections import LineCollection
import matplotlib.patches as mpatches  # THIS WAS MISSING
import pandas as pd

# ============================================
# 17 GEOMETRY NODES (MASTER_GEOMETRY_NODES.csv)
# ============================================
geometry_nodes = {
    'O': {'name': 'core_center', 'x': 0.0, 'y': 0.0, 'z': -6.0, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 0},
    'A': {'name': 'sheet_id:1', 'x': 2.0, 'y': 0.0, 'z': 0.0, 'sh_r': 0.1126, 'sh_q0': 0.9646, 'layer': 1},
    'B': {'name': 'sheet_id:2', 'x': 0.0, 'y': 2.0, 'z': 0.0, 'sh_r': 0.1121, 'sh_q0': 0.9720, 'layer': 1},
    'C': {'name': 'sheet_id:3', 'x': -2.0, 'y': 0.0, 'z': 0.0, 'sh_r': 0.1126, 'sh_q0': 0.9646, 'layer': 1},
    'D': {'name': 'sheet_id:4', 'x': 0.0, 'y': -2.0, 'z': 0.0, 'sh_r': 0.1121, 'sh_q0': 0.9720, 'layer': 1},
    'E': {'name': 'sheet_id:5', 'x': 4.0, 'y': 0.0, 'z': 1.5, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 2},
    'F': {'name': 'sheet_id:6', 'x': 2.83, 'y': 2.83, 'z': 1.5, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 2},
    'G': {'name': 'sheet_id:7', 'x': 0.0, 'y': 4.0, 'z': 1.5, 'sh_r': 0.1126, 'sh_q0': 0.9646, 'layer': 2},
    'H': {'name': 'sheet_id:8', 'x': -2.83, 'y': 2.83, 'z': 1.5, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 2},
    'I': {'name': 'sheet_id:9', 'x': -4.0, 'y': 0.0, 'z': 1.5, 'sh_r': 0.1126, 'sh_q0': 0.9646, 'layer': 2},
    'J': {'name': 'sheet_id:10', 'x': -2.83, 'y': -2.83, 'z': 1.5, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 2},
    'K': {'name': 'sheet_id:11', 'x': 0.0, 'y': -4.0, 'z': 1.5, 'sh_r': 0.1126, 'sh_q0': 0.9646, 'layer': 2},
    'L': {'name': 'sheet_id:12', 'x': 2.83, 'y': -2.83, 'z': 1.5, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 2},
    'M': {'name': 'sheet_id:13', 'x': 6.0, 'y': 0.0, 'z': 3.0, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 3},
    'N': {'name': 'sheet_id:14', 'x': 0.0, 'y': 6.0, 'z': 3.0, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 3},
    'P': {'name': 'sheet_id:15', 'x': -6.0, 'y': 0.0, 'z': 3.0, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 3},
    'Q': {'name': 'sheet_id:16', 'x': 0.0, 'y': -6.0, 'z': 3.0, 'sh_r': 0.1121, 'sh_q0': 0.9646, 'layer': 3},
}

# 26 UROBOROS ANCHOR POINTS (from FACE_BODY_UROBOROS_MAP.csv)
uroboros_anchors = {
    # Spine (Uroboros) - Vertical central flow
    'CV1': {'x': 0.0, 'y': 8.0, 'z': 4.0, 'face_x': 8.0, 'face_y': 8.0, 'type': 'spine_top'},
    'CV4': {'x': 0.0, 'y': 4.0, 'z': 2.0, 'face_x': 8.0, 'face_y': 8.0, 'type': 'spine_upper'},
    'CV8': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'face_x': 8.0, 'face_y': 8.0, 'type': 'spine_mid'},
    'LV5': {'x': 0.0, 'y': -4.0, 'z': -2.0, 'face_x': 8.0, 'face_y': 8.0, 'type': 'spine_lower'},
    'SV1': {'x': 0.0, 'y': -8.0, 'z': -4.0, 'face_x': 8.0, 'face_y': 8.0, 'type': 'spine_base'},
    
    # Left Side (Choke Pathway - Constricted)
    'LC1': {'x': -3.0, 'y': 6.0, 'z': 3.0, 'face_x': 6.0, 'face_y': 10.0, 'type': 'left_choke'},
    'LC2': {'x': -4.0, 'y': 4.0, 'z': 2.0, 'face_x': 6.0, 'face_y': 10.0, 'type': 'left_choke'},
    'LC3': {'x': -5.0, 'y': 2.0, 'z': 1.0, 'face_x': 6.0, 'face_y': 10.0, 'type': 'left_choke'},
    'LC4': {'x': -6.0, 'y': 0.0, 'z': 0.0, 'face_x': 6.0, 'face_y': 10.0, 'type': 'left_choke'},
    'LC5': {'x': -5.0, 'y': -2.0, 'z': -1.0, 'face_x': 6.0, 'face_y': 10.0, 'type': 'left_choke'},
    'LC6': {'x': -4.0, 'y': -4.0, 'z': -2.0, 'face_x': 6.0, 'face_y': 10.0, 'type': 'left_choke'},
    'LC7': {'x': -3.0, 'y': -6.0, 'z': -3.0, 'face_x': 6.0, 'face_y': 10.0, 'type': 'left_choke'},
    
    # Right Side (Corridor Pathway - Open)
    'RC1': {'x': 3.0, 'y': 6.0, 'z': 3.0, 'face_x': 10.0, 'face_y': 6.0, 'type': 'right_corridor'},
    'RC2': {'x': 4.0, 'y': 4.0, 'z': 2.0, 'face_x': 10.0, 'face_y': 6.0, 'type': 'right_corridor'},
    'RC3': {'x': 5.0, 'y': 2.0, 'z': 1.0, 'face_x': 10.0, 'face_y': 6.0, 'type': 'right_corridor'},
    'RC4': {'x': 6.0, 'y': 0.0, 'z': 0.0, 'face_x': 10.0, 'face_y': 6.0, 'type': 'right_corridor'},
    'RC5': {'x': 5.0, 'y': -2.0, 'z': -1.0, 'face_x': 10.0, 'face_y': 6.0, 'type': 'right_corridor'},
    'RC6': {'x': 4.0, 'y': -4.0, 'z': -2.0, 'face_x': 10.0, 'face_y': 6.0, 'type': 'right_corridor'},
    'RC7': {'x': 3.0, 'y': -6.0, 'z': -3.0, 'face_x': 10.0, 'face_y': 6.0, 'type': 'right_corridor'},
    
    # Cross Points (Mirror Terminals)
    'MT1': {'x': 2.0, 'y': 8.0, 'z': 3.0, 'face_x': 9.0, 'face_y': 7.0, 'type': 'mirror_cross'},
    'MT2': {'x': -2.0, 'y': 8.0, 'z': 3.0, 'face_x': 7.0, 'face_y': 9.0, 'type': 'mirror_cross'},
    'MT3': {'x': 2.0, 'y': -8.0, 'z': -3.0, 'face_x': 9.0, 'face_y': 9.0, 'type': 'mirror_cross'},
    'MT4': {'x': -2.0, 'y': -8.0, 'z': -3.0, 'face_x': 7.0, 'face_y': 7.0, 'type': 'mirror_cross'},
}

# ============================================
# POTENTIAL FIELD GENERATION
# ============================================
def generate_potential_field(X, Y, Z, nodes):
    """Generate spiral potential field based on geometry nodes"""
    potential = np.zeros_like(X)
    
    # Central O-point potential well
    r_center = np.sqrt(X**2 + Y**2 + Z**2)
    potential += -5.0 * np.exp(-r_center**2 / 8.0)  # Deep central well
    
    # Add node contributions
    for node_id, node in nodes.items():
        dx = X - node['x']
        dy = Y - node['y']
        dz = Z - node['z']
        r = np.sqrt(dx**2 + dy**2 + dz**2)
        
        # SH stability determines well depth
        depth = 2.0 * (node['sh_r'] / 0.1121) * (node['sh_q0'] / 0.9646)
        width = 2.5
        
        potential += -depth * np.exp(-r**2 / width**2)
    
    return potential

# ============================================
# ASYMMETRIC CONFINEMENT FIELD
# ============================================
def asymmetric_field_modifier(X, Y, Z):
    """Apply left-choke / right-corridor asymmetry"""
    modifier = np.ones_like(X)
    
    # Left hemisphere constriction
    left_mask = X < 0
    modifier[left_mask] *= 0.6  # Choked flow
    
    # Right hemisphere expansion
    right_mask = X > 0
    modifier[right_mask] *= 1.4  # Open corridor
    
    # Diagonal choke line influence (x+y=16 equivalent in body)
    diagonal_proximity = np.abs(X + Y - 0)
    choke_effect = np.exp(-diagonal_proximity / 3.0)
    modifier *= (1 - 0.3 * choke_effect)
    
    return modifier

# ============================================
# SPIRAL FLOW LINES
# ============================================
def generate_spiral_flow(n_streamlines=64):
    """Generate logarithmic spiral flow lines"""
    t = np.linspace(0, 4*np.pi, 500)
    streamlines = []
    
    for i in range(n_streamlines):
        angle_offset = 2 * np.pi * i / n_streamlines
        
        # Logarithmic spiral: r = a * exp(b*theta)
        a = 0.5
        b = 0.15
        
        r = a * np.exp(b * t)
        theta = t + angle_offset
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = 2.0 * np.sin(t / 2)  # Vertical oscillation
        
        streamlines.append((x, y, z))
    
    return streamlines

# ============================================
# MAIN VISUALIZATION
# ============================================
fig = plt.figure(figsize=(22, 16))

# 3D Universe View
ax1 = fig.add_subplot(2, 2, 1, projection='3d')

# Generate coordinate grid for potential field
x = np.linspace(-10, 10, 80)
y = np.linspace(-10, 10, 80)
z = np.linspace(-6, 6, 40)
X, Y, Z = np.meshgrid(x, y, z)

# Calculate potential field
potential = generate_potential_field(X, Y, Z, geometry_nodes)
modifier = asymmetric_field_modifier(X, Y, Z)
potential *= modifier

# Plot 3D isosurfaces as scatter (simplified representation)
step = 4
x_samp = X[::step, ::step, ::step].flatten()
y_samp = Y[::step, ::step, ::step].flatten()
z_samp = Z[::step, ::step, ::step].flatten()
pot_samp = potential[::step, ::step, ::step].flatten()

# Color by potential value
colors = plt.cm.plasma((pot_samp - pot_samp.min()) / (pot_samp.max() - pot_samp.min()))

# Plot potential field points
scatter = ax1.scatter(x_samp, y_samp, z_samp, c=pot_samp, cmap='plasma', 
                      s=1, alpha=0.3, vmin=pot_samp.min(), vmax=pot_samp.max())

# Plot 17 geometry nodes
for node_id, node in geometry_nodes.items():
    color = 'white' if node_id == 'O' else 'cyan'
    size = 100 if node_id == 'O' else 60
    ax1.scatter([node['x']], [node['y']], [node['z']], 
               c=color, s=size, edgecolors='black', linewidth=1.5, alpha=0.9)
    ax1.text(node['x'], node['y'], node['z']+0.5, f'{node_id}', 
            fontsize=9, color='white', fontweight='bold')

# Plot spiral flow lines
streamlines = generate_spiral_flow(n_streamlines=24)
for xs, ys, zs in streamlines:
    ax1.plot(xs, ys, zs, color='yellow', alpha=0.4, linewidth=0.8)

# Plot uroboros anchors
for anchor_id, anchor in uroboros_anchors.items():
    if 'spine' in anchor['type']:
        color = 'lime'
        size = 40
    elif 'left' in anchor['type']:
        color = 'red'
        size = 35
    elif 'right' in anchor['type']:
        color = 'blue'
        size = 35
    else:
        color = 'magenta'
        size = 30
    
    ax1.scatter([anchor['x']], [anchor['y']], [anchor['z']], 
               c=color, s=size, edgecolors='white', linewidth=1, alpha=0.8)

# Draw asymmetric flow arrows
ax1.quiver([-6]*5, np.linspace(-6, 6, 5), np.zeros(5),
          np.ones(5)*0.5, np.zeros(5), np.zeros(5),
          color='red', alpha=0.6, arrow_length_ratio=0.3)

ax1.quiver([6]*5, np.linspace(-6, 6, 5), np.zeros(5),
          -np.ones(5)*0.5, np.ones(5)*0.3, np.zeros(5),
          color='blue', alpha=0.6, arrow_length_ratio=0.3)

ax1.set_xlabel('X (Left Choke <-> Right Corridor)', fontsize=10)
ax1.set_ylabel('Y (Posterior <-> Anterior)', fontsize=10)
ax1.set_zlabel('Z (Inferior <-> Superior)', fontsize=10)
ax1.set_title('UNIVERSE BODY HEATMAP\n17 Geometry Nodes + Asymmetric Flow', fontsize=12, fontweight='bold')
ax1.set_xlim(-10, 10)
ax1.set_ylim(-10, 10)
ax1.set_zlim(-6, 6)

cbar1 = plt.colorbar(scatter, ax=ax1, shrink=0.5, aspect=10)
cbar1.set_label('Potential Energy', fontsize=9)

# ============================================
# 2D HEATMAP - CORONAL PLANE (X-Z)
# ============================================
ax2 = fig.add_subplot(2, 2, 2)

# Generate 2D slice at Y=0
x_2d = np.linspace(-10, 10, 200)
z_2d = np.linspace(-6, 6, 120)
X_2d, Z_2d = np.meshgrid(x_2d, z_2d)
Y_2d = np.zeros_like(X_2d)

potential_2d = generate_potential_field(X_2d, Y_2d, Z_2d, geometry_nodes)
modifier_2d = asymmetric_field_modifier(X_2d, Y_2d, Z_2d)
potential_2d *= modifier_2d

# Plot heatmap
im = ax2.imshow(potential_2d, extent=[-10, 10, -6, 6], origin='lower',
                cmap='plasma', aspect='auto')
ax2.contour(X_2d, Z_2d, potential_2d, levels=15, colors='white', alpha=0.4, linewidths=0.5)

# Overlay geometry nodes on 2D
for node_id, node in geometry_nodes.items():
    ax2.scatter([node['x']], [node['z']], c='white', s=80, edgecolors='black', linewidth=2)
    ax2.text(node['x']+0.3, node['z']+0.3, node_id, fontsize=10, color='white', fontweight='bold')

# Overlay uroboros anchors
for anchor_id, anchor in uroboros_anchors.items():
    if 'spine' in anchor['type']:
        color = 'lime'
        marker = 's'
    elif 'left' in anchor['type']:
        color = 'red'
        marker = '^'
    elif 'right' in anchor['type']:
        color = 'blue'
        marker = 'v'
    else:
        color = 'magenta'
        marker = 'o'
    
    ax2.scatter([anchor['x']], [anchor['z']], c=color, s=50, marker=marker, 
               edgecolors='white', linewidth=1.5)

# Draw asymmetry indicator
ax2.axvline(x=0, color='yellow', linestyle='--', linewidth=2, alpha=0.5, label='Central Axis')
ax2.fill_betweenx([-6, 6], -10, 0, alpha=0.1, color='red', label='Left Choke')
ax2.fill_betweenx([-6, 6], 0, 10, alpha=0.1, color='blue', label='Right Corridor')

ax2.set_xlabel('X (Left Choke <-> Right Corridor)', fontsize=11)
ax2.set_ylabel('Z (Inferior <-> Superior)', fontsize=11)
ax2.set_title('CORONAL PLANE HEATMAP\nX-Z Slice @ Y=0', fontsize=12, fontweight='bold')
plt.colorbar(im, ax=ax2, label='Potential Energy')

# ============================================
# 2D HEATMAP - SAGITTAL PLANE (Y-Z)
# ============================================
ax3 = fig.add_subplot(2, 2, 3)

# Generate 2D slice at X=0
y_2d = np.linspace(-10, 10, 200)
z_2d = np.linspace(-6, 6, 120)
Y_2d_s, Z_2d_s = np.meshgrid(y_2d, z_2d)
X_2d_s = np.zeros_like(Y_2d_s)

potential_2d_s = generate_potential_field(X_2d_s, Y_2d_s, Z_2d_s, geometry_nodes)

im3 = ax3.imshow(potential_2d_s, extent=[-10, 10, -6, 6], origin='lower',
                 cmap='plasma', aspect='auto')
ax3.contour(Y_2d_s, Z_2d_s, potential_2d_s, levels=15, colors='white', alpha=0.4, linewidths=0.5)

# Overlay spine
spine_x = [u['z'] for u in uroboros_anchors.values() if 'spine' in u['type']]
spine_y = [u['y'] for u in uroboros_anchors.values() if 'spine' in u['type']]
ax3.plot(spine_x, spine_y, 'lime', linewidth=3, marker='s', markersize=8, label='Uroboros Spine')

ax3.set_xlabel('Y (Posterior <-> Anterior)', fontsize=11)
ax3.set_ylabel('Z (Inferior <-> Superior)', fontsize=11)
ax3.set_title('SAGITTAL PLANE HEATMAP\nY-Z Slice @ X=0', fontsize=12, fontweight='bold')
plt.colorbar(im3, ax=ax3, label='Potential Energy')

# ============================================
# FLOW DIAGRAM - ASYMMETRIC CONFINEMENT
# ============================================
ax4 = fig.add_subplot(2, 2, 4)

# Create schematic flow diagram
ax4.set_xlim(0, 16)
ax4.set_ylim(0, 16)

# Face input zone (top)
face_zone = plt.Rectangle((2, 12), 12, 3, fill=True, facecolor='lightgray', 
                          edgecolor='black', linewidth=2, alpha=0.5)
ax4.add_patch(face_zone)
ax4.text(8, 13.5, 'FACE INPUT ZONE', ha='center', fontsize=11, fontweight='bold')

# Left Choke Band (x+y=16, left side)
ax4.plot([2, 6], [14, 10], 'r-', linewidth=4, alpha=0.7, label='Choke Band (x+y=16)')
ax4.fill_between([2, 6], [14, 10], [16, 12], alpha=0.3, color='red')

# Right Corridor (open flow)
corridor_x = [10, 14, 14, 10]
corridor_y = [10, 10, 14, 12]
ax4.fill(corridor_x, corridor_y, alpha=0.3, color='blue', label='Right Corridor')

# Central Processing Nodes (17 geometry nodes representation)
for i, (node_id, node) in enumerate(list(geometry_nodes.items())[:9]):
    x_pos = 4 + (i % 3) * 4
    y_pos = 4 + (i // 3) * 3
    circle = Circle((x_pos, y_pos), 0.8, facecolor='cyan', edgecolor='black', linewidth=2)
    ax4.add_patch(circle)
    ax4.text(x_pos, y_pos, node_id, ha='center', va='center', fontsize=10, fontweight='bold')

# Flow arrows
ax4.annotate('', xy=(6, 8), xytext=(4, 10),
            arrowprops=dict(arrowstyle='->', color='red', lw=3))
ax4.annotate('', xy=(6, 5), xytext=(4, 7),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))

ax4.annotate('', xy=(12, 8), xytext=(12, 10),
            arrowprops=dict(arrowstyle='->', color='blue', lw=4))
ax4.annotate('', xy=(12, 5), xytext=(12, 7),
            arrowprops=dict(arrowstyle='->', color='blue', lw=3))

ax4.annotate('', xy=(8, 1), xytext=(8, 4),
            arrowprops=dict(arrowstyle='->', color='green', lw=5))

# Body output zone (bottom)
body_zone = plt.Rectangle((2, 0), 12, 2, fill=True, facecolor='lightgreen',
                          edgecolor='black', linewidth=2, alpha=0.5)
ax4.add_patch(body_zone)
ax4.text(8, 1, 'BODY OUTPUT (26 Uroboros Anchors)', ha='center', fontsize=11, fontweight='bold')

# 26 anchor representation
for i, anchor_id in enumerate(list(uroboros_anchors.keys())[:13]):
    x_pos = 3 + i
    ax4.scatter([x_pos], [0.5], c='darkgreen', s=50, marker='s')

ax4.set_title('ASYMMETRIC FLOW SCHEMATIC\nLeft Choke → Central → Right Corridor', 
              fontsize=12, fontweight='bold')
ax4.set_aspect('equal')
ax4.axis('off')

# Legend
legend_elements = [
    mpatches.Patch(facecolor='red', alpha=0.5, label='Left Choke (Constricted)'),
    mpatches.Patch(facecolor='blue', alpha=0.5, label='Right Corridor (Open)'),
    mpatches.Patch(facecolor='cyan', label='17 Geometry Nodes'),
    mpatches.Patch(facecolor='lightgreen', label='26 Uroboros Anchors')
]
ax4.legend(handles=legend_elements, loc='upper left', fontsize=9)

plt.tight_layout()
plt.savefig('body_universe_heatmap.png', dpi=300, bbox_inches='tight', 
            facecolor='black', edgecolor='none')
plt.savefig('body_universe_heatmap.pdf', dpi=300, bbox_inches='tight',
            facecolor='black', edgecolor='none')
plt.show()

print("="*60)
print("BODY UNIVERSE HEATMAP GENERATED")
print("="*60)
print(f"17 Geometry Nodes plotted")
print(f"26 Uroboros Anchors plotted")
print(f"Spiral potential field with asymmetric confinement")
print(f"Outputs saved: body_universe_heatmap.png/pdf")
print("="*60)
