"""
Final Connected Manifold 3D Renderer
Renders the 13-patch, 11-seam closure manifold with intrinsic/extended distinction.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.patches as mpatches

def render_final_manifold(output_path="FINAL_CONNECTED_MANIFOLD_3D.png"):
    """
    Render the final connected manifold with:
    - 13 patches (12 intrinsic + 1 extended mediator)
    - 11 seams (9 intrinsic + 2 extended)
    - Visual distinction of barrier and bypass
    """
    
    fig = plt.figure(figsize=(20, 16), facecolor="#0a0a15")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0a0a15")
    
    # ============================================================
    # PATCH COORDINATES (3D embedding of manifold structure)
    # ============================================================
    
    # Main cluster patches arranged in connected geometry
    patches = {
        # Intrinsic patches - Main component (arranged in structural relation)
        'A': {'pos': (2, 0, 0), 'name': 'sheet_id:1', 'type': 'intrinsic_main'},
        'B': {'pos': (0, 2, 0), 'name': 'sheet_id:2', 'type': 'intrinsic_main'},
        'C': {'pos': (0, 0, 2), 'name': 'sheet_id:3', 'type': 'intrinsic_main'},
        'D': {'pos': (-2, 0, 0), 'name': 'sheet_id:4', 'type': 'intrinsic_main'},
        '10': {'pos': (1, 1, 1), 'name': 'sheet_id:10', 'type': 'intrinsic_main'},
        '11': {'pos': (1, 3, 0), 'name': 'sheet_id:11', 'type': 'intrinsic_main'},
        '12': {'pos': (-1, 2, 1), 'name': 'sheet_id:12', 'type': 'intrinsic_main'},
        '13': {'pos': (0, -1, 2), 'name': 'sheet_id:13', 'type': 'intrinsic_main'},
        '14': {'pos': (-1, 3, 0), 'name': 'sheet_id:14', 'type': 'intrinsic_main'},
        "F'": {'pos': (0, 0, 3), 'name': 'flash:center_in', 'type': 'intrinsic_main'},
        'F': {'pos': (1, 0, 2), 'name': 'flash_bridge', 'type': 'intrinsic_main'},
        
        # Intrinsic patch - Isolated component (barrier-separated)
        'G': {'pos': (0, 5, 0), 'name': 'gateway_peak', 'type': 'intrinsic_isolated'},
        
        # Extended patch - External mediator
        'X': {'pos': (-1, 3, -1), 'name': 'mediator:synthetic_alpha', 'type': 'extended_mediator'},
    }
    
    # ============================================================
    # SEAMS (Connections between patches)
    # ============================================================
    
    intrinsic_seams = [
        ('B', 'D', 'Lane A'),      # step 1
        ('11', 'B', 'Lane B'),     # step 2
        ('14', 'B', 'Lane B'),     # step 3
        ('13', 'C', 'Lane C'),     # step 4 (relay via C to B)
        ('C', 'B', 'Lane C cont'), # step 4 continuation
        ('10', 'B', 'Stage 2'),    # step 5
        ('12', 'B', 'Stage 2'),    # step 6
        ('10', 'A', 'A-D'),        # step 7
        ('F', 'C', 'Flash'),       # step 8
        ("F'", 'C', 'Flash comp'), # step 9
    ]
    
    extended_seams = [
        ('G', 'X', 'Expansion'),   # step 10
        ('X', 'D', 'Relay'),       # step 11
    ]
    
    # Barrier annotation (uncrossable in intrinsic, bypassed in extended)
    barrier = ('G', 'B')
    
    # ============================================================
    # RENDER PATCHES
    # ============================================================
    
    colors = {
        'intrinsic_main': '#00ff88',      # Green - connected intrinsic
        'intrinsic_isolated': '#ff4444',  # Red - isolated by barrier
        'extended_mediator': '#ffaa00',   # Orange - external mediator
    }
    
    sizes = {
        'intrinsic_main': 400,
        'intrinsic_isolated': 600,
        'extended_mediator': 500,
    }
    
    # Plot each patch
    for patch_id, patch_data in patches.items():
        pos = patch_data['pos']
        patch_type = patch_data['type']
        name = patch_data['name']
        
        ax.scatter(*pos, 
                  c=colors[patch_type], 
                  s=sizes[patch_type],
                  alpha=0.9,
                  edgecolors='white',
                  linewidths=2,
                  zorder=5)
        
        # Label
        ax.text(pos[0], pos[1], pos[2] + 0.3, 
               f"{patch_id}\n({name})",
               color='white', fontsize=8, ha='center',
               fontweight='bold' if patch_type == 'intrinsic_isolated' else 'normal')
    
    # ============================================================
    # RENDER INTRINSIC SEAMS (Gold/White)
    # ============================================================
    
    for p1, p2, label in intrinsic_seams:
        pos1 = patches[p1]['pos']
        pos2 = patches[p2]['pos']
        
        # Draw seam line
        ax.plot([pos1[0], pos2[0]], 
               [pos1[1], pos2[1]], 
               [pos1[2], pos2[2]],
               color='#ffd700', alpha=0.7, linewidth=2, zorder=3)
        
        # Midpoint label
        mid = ((pos1[0] + pos2[0])/2, (pos1[1] + pos2[1])/2, (pos1[2] + pos2[2])/2)
        ax.text(mid[0], mid[1], mid[2], label, color='#aaaaaa', fontsize=6, alpha=0.8)
    
    # ============================================================
    # RENDER EXTENDED SEAMS (Bright Cyan - mediator bridges)
    # ============================================================
    
    for p1, p2, label in extended_seams:
        pos1 = patches[p1]['pos']
        pos2 = patches[p2]['pos']
        
        # Draw extended seam (thicker, brighter)
        ax.plot([pos1[0], pos2[0]], 
               [pos1[1], pos2[1]], 
               [pos1[2], pos2[2]],
               color='#00ffff', alpha=0.9, linewidth=4, zorder=4)
        
        # Label
        mid = ((pos1[0] + pos2[0])/2, (pos1[1] + pos2[1])/2, (pos1[2] + pos2[2])/2)
        ax.text(mid[0], mid[1], mid[2], label, color='#00ffff', fontsize=7, fontweight='bold')
    
    # ============================================================
    # RENDER BARRIER (Dashed Red - uncrossable)
    # ============================================================
    
    barrier_pos1 = patches[barrier[0]]['pos']
    barrier_pos2 = patches[barrier[1]]['pos']
    
    # Draw barrier indicator (dashed line, NOT a seam)
    ax.plot([barrier_pos1[0], barrier_pos2[0]], 
           [barrier_pos1[1], barrier_pos2[1]], 
           [barrier_pos1[2], barrier_pos2[2]],
           color='#ff0000', linestyle='--', alpha=0.5, linewidth=3, zorder=2)
    
    # Barrier label
    barrier_mid = ((barrier_pos1[0] + barrier_pos2[0])/2,
                   (barrier_pos1[1] + barrier_pos2[1])/2 + 0.5,
                   (barrier_pos1[2] + barrier_pos2[2])/2)
    ax.text(barrier_mid[0], barrier_mid[1], barrier_mid[2], 
           'β: TRUE BARRIER\n(uncrossable, bypassed via X)',
           color='#ff6666', fontsize=9, ha='center', fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#220000', alpha=0.7))
    
    # ============================================================
    # RENDER BYPASS PATH (Green arrow showing G→X→D→...→B)
    # ============================================================
    
    # Annotate the bypass (3D text)
    ax.text(barrier_pos1[0] - 1.5, barrier_pos1[1] - 1, barrier_pos1[2] + 1,
           'BYPASS:\nG→X→D→...→B',
           color='#00ff00', fontsize=9, ha='center',
           bbox=dict(boxstyle='round', facecolor='#003300', alpha=0.8))
    
    # ============================================================
    # STYLING AND LEGEND
    # ============================================================
    
    ax.set_axis_off()
    ax.set_box_aspect([1.0, 1.0, 0.8])
    
    # Set limits
    ax.set_xlim(-4, 4)
    ax.set_ylim(-2, 6)
    ax.set_zlim(-2, 5)
    
    # Title
    ax.text2D(0.5, 0.98, "FINAL CONNECTED MANIFOLD", 
             transform=ax.transAxes, color='white', fontsize=18, 
             ha='center', fontweight='bold')
    ax.text2D(0.5, 0.94, "13 Patches | 11 Seams | 2-Phase Closure | π₀ = 1 (Unified)", 
             transform=ax.transAxes, color='#aaaaaa', fontsize=12, ha='center')
    
    # Legend
    legend_elements = [
        mpatches.Patch(color='#00ff88', label='Intrinsic - Main Component (11 patches)'),
        mpatches.Patch(color='#ff4444', label='Intrinsic - Isolated (gateway_peak)'),
        mpatches.Patch(color='#ffaa00', label='Extended - Mediator (synthetic_alpha)'),
        mpatches.Patch(color='#ffd700', label='Intrinsic Seams (9)'),
        mpatches.Patch(color='#00ffff', label='Extended Seams (2)'),
        mpatches.Patch(color='#ff0000', label='True Barrier β (bypassed, not erased)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', 
             facecolor='#1a1a2e', edgecolor='white', labelcolor='white',
             fontsize=10)
    
    # Component summary text
    summary_text = """CLOSURE SEQUENCE:
Phase 1 (Intrinsic): 12 patches, 9 seams → 2 components
  Component 1: 11 patches (green)
  Component 2: 1 patch isolated (red) by barrier β

Phase 2 (Extended): +1 mediator patch, +2 seams → 1 component
  Bypass: G→X→D route around barrier β
  Result: Full unified connectedness"""
    
    ax.text2D(0.02, 0.45, summary_text,
             transform=ax.transAxes, color='#cccccc', fontsize=9,
             family='monospace',
             bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor="#0a0a15")
    plt.close(fig)
    print(f"Rendered FINAL CONNECTED MANIFOLD to {output_path}")
    return output_path

if __name__ == "__main__":
    render_final_manifold()
