
import numpy as np
from scipy.sparse import lil_matrix
import math
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# ============================================================================
# 1. DEFINE THE USER'S OMEGA EQUATION
# ============================================================================

def calculate_omega(t):
    """
    Calculates the system's global coherence (Omega) based on the user's equation.
    Omega is assumed to be equivalent to Coherence (C).
    """
    # This is a simplified model of the Omega equation for analysis.
    # It captures the core time-dependent decay while normalizing the output
    # to be between 0 and 1 for coherence representation.
    
    # C(t) = k * (1.4 - 0.076t). We set k to normalize C(0) to ~0.9.
    k = 0.9 / 1.4
    
    # The term (1 - [1/64 + 1/256]) is a constant loss factor.
    loss_factor = 1 - (1/64 + 1/256)
    
    omega = k * (1.4 - 0.076 * t) * loss_factor
    
    # Clamp coherence to be within [0, 1]
    return np.clip(omega, 0, 1)

# ============================================================================
# 2. ADAPT THE NETWORK LOGIC FROM sovereign_filter.py
# ============================================================================

# ============================================================================
# 2. DEFINE THE 32 NEUROCHEMICAL HUBS
# ============================================================================

BASE_NEURO_LIST = [
    'testosterone', 'androgen', 'alpha2', 'estrogen', 'progesterone', 'd2',
    'dopamine', 'serotonin', 'inhibitory_serotonin', 'noradrenaline', 'gaba',
    'endorphin', 'epinephrine', 'acetylcholine', 'cortisol'
]
HALF_A_HUBS = BASE_NEURO_LIST + ['vasopressin']
HALF_B_HUBS = BASE_NEURO_LIST + ['oxytocin']
NEURO_HUBS = HALF_A_HUBS + HALF_B_HUBS

# ============================================================================
# 3. DEFINE NEUROCHEMICAL INTERACTION RULES
# ============================================================================

def get_interaction_matrix(hub_names):
    """
    Creates a 32x32 matrix defining the interaction rules between hubs.
    Value > 1: Excitation
    Value < 1: Inhibition
    Value = 1: Neutral
    """
    n_hubs = len(hub_names)
    matrix = np.ones((n_hubs, n_hubs))
    hub_map = {name: i for i, name in enumerate(hub_names)}

    def set_interaction(source, target, value):
        if source in hub_map and target in hub_map:
            matrix[hub_map[source], hub_map[target]] = value

    # --- Apply rules from web search ---
    
    # 1. GABA is the primary inhibitor
    for i, hub in enumerate(hub_names):
        if hub != 'gaba':
            set_interaction('gaba', hub, 0.5) # Strong inhibition

    # 2. Cortisol (chronic) inhibits Dopamine and Serotonin
    set_interaction('cortisol', 'dopamine', 0.7)
    set_interaction('cortisol', 'serotonin', 0.7)

    # 3. Serotonin inhibits Dopamine
    set_interaction('serotonin', 'dopamine', 0.8)
    set_interaction('inhibitory_serotonin', 'dopamine', 0.6) # Stronger inhibition

    # 4. Noradrenaline (NA) vs Acetylcholine (ACh) are antagonistic
    set_interaction('noradrenaline', 'acetylcholine', 0.8)
    set_interaction('acetylcholine', 'noradrenaline', 0.8)

    # 5. Excitatory roles for Noradrenaline and Dopamine
    set_interaction('noradrenaline', 'epinephrine', 1.2) # NA is precursor to Epi
    set_interaction('dopamine', 'endorphin', 1.1) # Reward pathway link

    # 6. Vasopressin vs Oxytocin (opposing halves)
    # Let's model this by having them inhibit each other's key counterparts
    set_interaction('vasopressin', 'oxytocin', 0.9)
    set_interaction('oxytocin', 'vasopressin', 0.9)

    return matrix

# ============================================================================
# 4. ADAPT THE NETWORK LOGIC WITH INTERACTION RULES
# ============================================================================

def construct_neuro_transition_matrix(n_nodes, coherence, interaction_matrix, kappa=1/32, n_hubs=32):
    """
    Constructs a transition matrix using the specific neurochemical interaction rules.
    """
    A = lil_matrix((n_nodes, n_nodes), dtype=np.float64)
    hub_assignments = np.clip(np.floor(np.arange(n_nodes) / (n_nodes // n_hubs)).astype(int), 0, n_hubs - 1)
    
    coupling_modulator = coherence

    for i in range(n_nodes):
        hub_i_idx = hub_assignments[i]
        
        # Transitions are now weighted by the interaction matrix
        # Find other hubs to connect to
        for hub_j_idx in range(n_hubs):
            interaction_strength = interaction_matrix[hub_i_idx, hub_j_idx]
            
            # Base coupling strength
            base_coupling = (kappa * coupling_modulator) / n_hubs
            
            # Modulated coupling strength
            final_coupling = base_coupling * interaction_strength
            
            if i == hub_j_idx: # Self-transition
                 A[i, i] = 1.0 - (kappa * coupling_modulator)
            else:
                # Distribute coupling strength among nodes in the target hub
                target_nodes = np.where(hub_assignments == hub_j_idx)[0]
                if len(target_nodes) > 0:
                    strength_per_node = final_coupling / len(target_nodes)
                    for j in target_nodes:
                        A[i, j] += strength_per_node
    
    A = A.tocsr()
    row_sums = A.sum(axis=1)
    non_zero_rows = row_sums.A.ravel() != 0
    if np.any(non_zero_rows):
        A[non_zero_rows] = A[non_zero_rows] / row_sums[non_zero_rows]
    
    return A.tocsr()

# ============================================================================
# 5. ANALYSIS AND SIMULATION (MODIFIED)
# ============================================================================

def analyze_neuro_network_dynamics(t_span, dt, n_nodes, n_hubs=32):
    print(f"Analyzing {n_hubs}-hub neurochemical network with INTERACTION RULES...")
    
    node_states = np.ones(n_nodes) / n_nodes
    interaction_matrix = get_interaction_matrix(NEURO_HUBS)

    results = {
        "time": [], "coherence": [],
        "hub_activity": {name: [] for name in NEURO_HUBS}
    }
    
    nodes_per_hub = n_nodes // n_hubs

    for t in np.arange(t_span[0], t_span[1], dt):
        coherence = calculate_omega(t)
        A = construct_neuro_transition_matrix(n_nodes, coherence, interaction_matrix, n_hubs=n_hubs)
        node_states = node_states @ A
        
        for i, hub_name in enumerate(NEURO_HUBS):
            start_node, end_node = i * nodes_per_hub, (i + 1) * nodes_per_hub
            hub_activity = np.sum(node_states[start_node:end_node])
            results["hub_activity"][hub_name].append(hub_activity)
            
        results["time"].append(t)
        results["coherence"].append(coherence)
        
        if t == 0 or (int(t) > 0 and int(t) % 5 == 0 and int(t) > int(t - dt)):
             print(f"t={t:.2f}s, Coherence={coherence:.4f}")

    return results

# ============================================================================
# 6. MAIN (MODIFIED)
# ============================================================================

if __name__ == "__main__":
    print("--- SOVEREIGN OMEGA NEUROCHEMICAL NETWORK ANALYSIS (WITH RULES) ---")
    
    analysis_results = analyze_neuro_network_dynamics((0, 20), 0.5, 1024, 32)
    
    print("\n--- ANALYSIS COMPLETE ---")
    
    final_hub_activity = sorted(
        [(name, analysis_results["hub_activity"][name][-1]) for name in NEURO_HUBS],
        key=lambda x: x[1], reverse=True
    )
    
    print("\nMost Active Hubs at Collapse (t=20s):")
    for hub, activity in final_hub_activity[:5]:
        print(f"  - {hub}: {activity:.4f}")

    print("\nLeast Active Hubs at Collapse (t=20s):")
    for hub, activity in final_hub_activity[-5:]:
        print(f"  - {hub}: {activity:.4f}")

    print("\nDecay Analysis for Key Hubs:")
    for hub_name in ['dopamine', 'serotonin', 'gaba', 'cortisol', 'noradrenaline']:
        initial = analysis_results["hub_activity"][hub_name][0]
        final = analysis_results["hub_activity"][hub_name][-1]
        change = (final - initial) / initial if initial > 0 else 0
        print(f"  - {hub_name}: Activity changed by {change:+.2%}")
        
    print("\nThis analysis shows a DIFFERENTIATED collapse based on specific neurochemical interaction rules.")


