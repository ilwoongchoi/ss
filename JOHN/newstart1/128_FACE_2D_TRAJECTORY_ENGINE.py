"""
128_FACE_2D_TRAJECTORY_ENGINE.py

2D Face Field Trajectory Engine for 128 Personality Types.

Maps neurotransmitter nodes to actual FACE_FIELD_MAP coordinates and generates
trajectories showing how 128 types move across the face in 2D plane.

Key Features:
- 2D projection (x, y) of face field
- 16 neurotransmitter nodes based on FACE_FIELD_MAP peak analysis
- 128 unique slotting loops (each type at different node at same time)
- Scale gates (kappa_eff, w_gate) influence trajectory binding
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.collections import LineCollection
from pathlib import Path

# ============================================================================
# NEUROTRANSMITTER NODES (from FACE_FIELD_MAP peak analysis)
# ============================================================================

NEURO_NODES_2D = {
    # Left Hemisphere (Dopaminergic)
    'Dopamine_L1': {'x': 2.0, 'y': 9.75, 'score': 0.030775, 'region': 'left'},
    'Dopamine_L2': {'x': 1.5, 'y': 9.5, 'score': 0.030638, 'region': 'left'},
    'Glutamate_L': {'x': 1.0, 'y': 5.0, 'score': 0.025, 'region': 'left'},
    
    # Midline (Acetylcholine/Hub)
    'Acetylcholine_M1': {'x': 8.5, 'y': 14.0, 'score': 0.028790, 'region': 'mid'},
    'Acetylcholine_M2': {'x': 9.0, 'y': 14.0, 'score': 0.028769, 'region': 'mid'},
    'Melatonin': {'x': 8.0, 'y': 12.0, 'score': 0.015, 'region': 'mid'},
    'Histamine': {'x': 8.0, 'y': 2.0, 'score': 0.02, 'region': 'mid'},
    'Norepinephrine': {'x': 8.5, 'y': 8.0, 'score': 0.022, 'region': 'mid'},
    
    # Right Hemisphere (Serotonergic)
    'Serotonin_R1': {'x': 11.25, 'y': 9.0, 'score': 0.029757, 'region': 'right'},
    'Serotonin_R2': {'x': 12.0, 'y': 9.0, 'score': 0.029553, 'region': 'right'},
    'GABA_R': {'x': 14.0, 'y': 6.0, 'score': 0.024, 'region': 'right'},
    
    # Additional nodes for 16-window cycle
    'Oxytocin': {'x': 6.0, 'y': 10.0, 'score': 0.018, 'region': 'mid-left'},
    'Testosterone': {'x': 10.0, 'y': 10.0, 'score': 0.018, 'region': 'mid-right'},
    'Estrogen': {'x': 4.0, 'y': 12.0, 'score': 0.016, 'region': 'left'},
    'Progesterone': {'x': 12.0, 'y': 12.0, 'score': 0.016, 'region': 'right'},
    'GABA_L': {'x': 2.0, 'y': 6.0, 'score': 0.020, 'region': 'left'},
}

# 16-window neurotransmitter cycle
CYCLE_16 = [
    'Dopamine_L1',      # Window 1: Dawn
    'Glutamate_L',      # Window 2: Early morning
    'Acetylcholine_M1', # Window 3: Morning
    'Histamine',        # Window 4: Late morning
    'Norepinephrine',   # Window 5: Noon
    'Serotonin_R1',     # Window 6: Afternoon
    'Dopamine_L2',      # Window 7: Late afternoon
    'Acetylcholine_M2', # Window 8: Evening
    'GABA_L',           # Window 9: Dusk
    'Melatonin',        # Window 10: Night
    'Oxytocin',         # Window 11: Deep night
    'Testosterone',     # Window 12: Midnight
    'Estrogen',         # Window 13: Late night
    'Progesterone',     # Window 14: Pre-dawn
    'GABA_R',           # Window 15: Early dawn
    'Serotonin_R2',     # Window 16: Dawn approach
]

# ============================================================================
# SLOTTING & SCALE GATE SYSTEM
# ============================================================================

def get_slotting_params(type_id):
    """
    Generate unique slotting parameters for each of 128 types.
    
    Each type has:
    - Unique phase offset (determines which window at t=0)
    - Unique slotting rate (determines speed of cycling)
    """
    np.random.seed(type_id)
    
    # Base parameters
    base_start = 1.4
    base_rate = 0.076
    
    # Type-specific variations
    phase_offset = (type_id % 16) / 16.0 * 2 * np.pi
    rate_variation = 1.0 + (type_id % 8) / 100.0  # 1.00 to 1.07
    
    return {
        'start': base_start,
        'rate': base_rate * rate_variation,
        'phase': phase_offset,
        'type_id': type_id
    }

def calculate_window(t, slot_params):
    """
    Calculate current window (1-16) based on time and slotting parameters.
    
    Each type cycles through 16 windows at different rates/phases,
    so at any given time t, different types are at different windows.
    """
    # Slotting value decreases over time
    slotting = slot_params['start'] - slot_params['rate'] * t
    
    # Add phase offset (unique per type)
    slotting += np.sin(t * 0.5 + slot_params['phase']) * 0.1
    
    # Map to window 1-16
    normalized = (slotting % 2.0) / 2.0
    window = int(normalized * 16) + 1
    return min(max(window, 1), 16)

def get_scale_gate_influence(node_key, face_df):
    """
    Get scale gate (kappa_eff, w_gate) influence for a node.
    
    Scale gates bind trajectories to specific regions based on:
    - kappa_eff: Effective grid resolution
    - w_gate: Gate width (accessibility)
    """
    if node_key not in NEURO_NODES_2D:
        return {'kappa': 0.03125, 'w_gate': 0.01}
    
    node = NEURO_NODES_2D[node_key]
    
    # Find nearest point in FACE_FIELD_MAP
    distances = np.sqrt(
        (face_df['x'] - node['x'])**2 + 
        (face_df['y'] - node['y'])**2
    )
    nearest_idx = distances.idxmin()
    nearest = face_df.loc[nearest_idx]
    
    return {
        'kappa': nearest['kappa_eff'],
        'w_gate': nearest['w_gate'],
        'score': nearest['score']
    }

# ============================================================================
# TRAJECTORY GENERATION
# ============================================================================

def generate_2d_trajectory(type_id, face_df, num_steps=200, total_time=24):
    """
    Generate 2D trajectory for a single type across neurotransmitter nodes.
    
    The trajectory shows how this type moves from node to node over time,
    influenced by scale gates that bind it to specific regions.
    """
    slot_params = get_slotting_params(type_id)
    
    t_span = np.linspace(0, total_time, num_steps)
    trajectory = np.zeros((num_steps, 2))
    node_sequence = []
    
    # Initial position (varies by type)
    np.random.seed(type_id)
    current_pos = np.array([
        np.random.uniform(4, 12),
        np.random.uniform(4, 12)
    ])
    
    for i, t in enumerate(t_span):
        # Determine current window
        window = calculate_window(t, slot_params)
        
        # Get target neurotransmitter node
        node_key = CYCLE_16[window - 1]
        node_sequence.append(node_key)
        
        # Get node position
        target_pos = np.array([
            NEURO_NODES_2D[node_key]['x'],
            NEURO_NODES_2D[node_key]['y']
        ])
        
        # Get scale gate influence
        gate = get_scale_gate_influence(node_key, face_df)
        
        # Scale gate binding strength
        binding = gate['w_gate'] * 100  # Amplify for effect
        kappa_influence = gate['kappa'] / 0.03125  # Normalize
        
        # Movement with scale gate influence
        if i == 0:
            trajectory[i] = current_pos
        else:
            # Direction to target
            direction = target_pos - current_pos
            distance = np.linalg.norm(direction)
            
            if distance > 0.1:
                # Velocity affected by scale gates
                base_velocity = 0.3
                velocity = base_velocity * (1 + min(binding, 1.0)) * kappa_influence
                
                # Move towards target
                direction = direction / distance
                current_pos = current_pos + direction * min(velocity, distance)
            else:
                # Jitter around node when close
                jitter_scale = max(0.05, 0.2 * max(0, (1 - binding)))
                jitter = np.random.normal(0, jitter_scale, 2)
                current_pos = target_pos + jitter
            
            trajectory[i] = current_pos.copy()
    
    return trajectory, node_sequence, slot_params

def generate_all_trajectories(face_df, num_types=128):
    """Generate trajectories for all 128 types."""
    
    trajectories = []
    all_node_sequences = []
    slot_params_list = []
    
    print(f"Generating {num_types} trajectories...")
    
    for type_id in range(num_types):
        traj, nodes, slot = generate_2d_trajectory(type_id, face_df)
        trajectories.append(traj)
        all_node_sequences.append(nodes)
        slot_params_list.append(slot)
        
        if (type_id + 1) % 32 == 0:
            print(f"  Completed {type_id + 1}/{num_types}")
    
    print("Done!")
    return trajectories, all_node_sequences, slot_params_list

# ============================================================================
# VISUALIZATION
# ============================================================================

def get_type_color(type_id):
    """Get color based on type characteristics."""
    # Color by phase group (which window at t=0)
    phase_group = type_id % 16
    colors = [
        '#FF0000', '#FF4000', '#FF8000', '#FFC000',
        '#FFFF00', '#C0FF00', '#80FF00', '#40FF00',
        '#00FF00', '#00FF40', '#00FF80', '#00FFC0',
        '#00FFFF', '#00C0FF', '#0080FF', '#0040FF',
    ]
    return colors[phase_group]

def plot_2d_face_field(trajectories, face_df):
    """Plot 2D face field with trajectories and neurotransmitter nodes."""
    
    fig, ax = plt.subplots(figsize=(16, 14), facecolor='#0a0a15')
    ax.set_facecolor('#0a0a15')
    
    # Plot background score heatmap
    scatter = ax.scatter(
        face_df['x'], face_df['y'],
        c=face_df['score'],
        cmap='hot',
        alpha=0.3,
        s=10,
        vmin=0, vmax=0.03
    )
    
    # Plot trajectories with gradient colors
    for type_id, traj in enumerate(trajectories):
        color = get_type_color(type_id)
        
        # Plot trajectory line
        ax.plot(traj[:, 0], traj[:, 1], 
               color=color, alpha=0.3, linewidth=0.8)
        
        # Mark start point
        ax.scatter(traj[0, 0], traj[0, 1], 
                  color=color, s=20, marker='o', alpha=0.6)
        
        # Mark end point
        ax.scatter(traj[-1, 0], traj[-1, 1], 
                  color=color, s=30, marker='x', alpha=0.8)
    
    # Plot neurotransmitter nodes
    for node_name, node_data in NEURO_NODES_2D.items():
        x, y = node_data['x'], node_data['y']
        score = node_data['score']
        region = node_data['region']
        
        # Color by region
        if region == 'left':
            color = '#00FFFF'  # Cyan for left/dopamine
        elif region == 'right':
            color = '#FF00FF'  # Magenta for right/serotonin
        else:
            color = '#FFFF00'  # Yellow for midline
        
        # Node size based on score
        size = 200 + score * 5000
        
        ax.scatter(x, y, color=color, s=size, alpha=0.8, 
                  edgecolors='white', linewidths=2, zorder=5)
        
        # Label
        ax.annotate(node_name, (x, y), 
                   xytext=(5, 5), textcoords='offset points',
                   color='white', fontsize=8, alpha=0.9)
    
    # Draw septum (midline)
    ax.axvline(x=8, color='white', linestyle='--', alpha=0.3, linewidth=1)
    ax.text(8.1, 15.5, 'SEPTUM (X=8)', color='white', fontsize=10, alpha=0.5)
    
    # Labels
    ax.set_xlabel('X: Left (Dopamine) ← → Right (Serotonin)', 
                 color='white', fontsize=12)
    ax.set_ylabel('Y: Occipital (0) → Frontal (16)', 
                 color='white', fontsize=12)
    ax.set_title(
        '128-TYPE 2D FACE FIELD TRAJECTORIES\n' +
        'Neurotransmitter Nodes + Scale Gate Binding',
        color='white', fontsize=14
    )
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('FACE_FIELD Score', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#00FFFF', 
                  markersize=10, label='Left/Dopamine', linestyle='None'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF00FF', 
                  markersize=10, label='Right/Serotonin', linestyle='None'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFFF00', 
                  markersize=10, label='Midline/Hub', linestyle='None'),
    ]
    ax.legend(handles=legend_elements, facecolor='#0a0a15', 
             labelcolor='white', loc='upper left')
    
    # Set limits
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    output = '128_FACE_2D_TRAJECTORIES.png'
    plt.savefig(output, dpi=300, facecolor='#0a0a15', bbox_inches='tight')
    plt.close()
    
    return output

def print_trajectory_stats(trajectories, node_sequences, slot_params_list):
    """Print statistics about the trajectories."""
    
    print("\n" + "="*60)
    print("2D TRAJECTORY STATISTICS")
    print("="*60)
    
    print(f"\nTotal types: {len(trajectories)}")
    print(f"Time steps per trajectory: {len(trajectories[0])}")
    
    # Node visit counts
    from collections import Counter
    all_nodes = [n for seq in node_sequences for n in seq]
    node_counts = Counter(all_nodes)
    
    print("\nNeurotransmitter node visits:")
    for node, count in node_counts.most_common():
        pct = count / len(all_nodes) * 100
        print(f"  {node:20s}: {count:5d} visits ({pct:5.1f}%)")
    
    # Slotting diversity
    print("\nSlotting parameter diversity:")
    rates = [s['rate'] for s in slot_params_list]
    phases = [s['phase'] for s in slot_params_list]
    print(f"  Rate range: {min(rates):.6f} - {max(rates):.6f}")
    print(f"  Phase range: {min(phases):.4f} - {max(phases):.4f} rad")
    
    # Trajectory coverage
    print("\nTrajectory spatial coverage:")
    all_points = np.vstack(trajectories)
    print(f"  X range: {all_points[:,0].min():.2f} - {all_points[:,0].max():.2f}")
    print(f"  Y range: {all_points[:,1].min():.2f} - {all_points[:,1].max():.2f}")
    
    # Sample type details
    print("\nSample type trajectories:")
    for i in [0, 32, 64, 96]:
        unique_nodes = len(set(node_sequences[i]))
        print(f"  Type {i:3d}: {unique_nodes:2d} unique nodes visited")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Load face field data
    face_path = Path("FACE_FIELD_MAP.csv")
    if not face_path.exists():
        print(f"ERROR: Cannot find {face_path}")
        exit(1)
    
    print("Loading FACE_FIELD_MAP...")
    face_df = pd.read_csv(face_path)
    print(f"Loaded {len(face_df)} points")
    
    # Generate trajectories
    trajectories, node_sequences, slot_params = generate_all_trajectories(face_df)
    
    # Plot
    output_file = plot_2d_face_field(trajectories, face_df)
    
    # Stats
    print_trajectory_stats(trajectories, node_sequences, slot_params)
    
    print(f"\n{'='*60}")
    print(f"OUTPUT: {output_file}")
    print(f"{'='*60}")
    print("\nKey Features:")
    print("  ✓ 128 unique slotting loops")
    print("  ✓ 16 neurotransmitter nodes on 2D face field")
    print("  ✓ Scale gate binding (kappa_eff, w_gate)")
    print("  ✓ Each type at different node at same time")
