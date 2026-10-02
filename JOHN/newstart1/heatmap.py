import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Arc
import matplotlib.patches as mpatches

# ============================================
# UNIVERSAL MASTER EQUATION
# ============================================
"""
Ψ_universe(x,y,z,t) = Ψ_SH(spiral) × Ψ_AB(archetype) × Ψ_gender(branch) × Ψ_spark(ignition)

where:
- Ψ_SH = [r - (q0² + ∇²)²]u - u³  (Swift-Hohenberg: spiral backbone)
- Ψ_AB = α₂ × (1 + β×δ(x-x_L)) × (1 - γ×δ(x-x_R))  (AB Male/Female asymmetry)
- Ψ_gender = ε × exp(-θ/138.88°)  (Gender rebranching at spark angle)
- Ψ_spark = κ × H(t - t_critical) × δ(E - E_threshold)  (Higgs ignition)
"""

# ============================================
# PHYSICAL CONSTANTS (Locked from atlas)
# ============================================
CONSTANTS = {
    'r_terminus': 0.1123,           # SH control parameter (locked)
    'q0_critical': 0.965,           # Critical sphericity
    'kappa_stability': 0.03125,     # 1/32 stability threshold
    'spark_angle_theta': 138.88,    # Diagonal reset angle (degrees)
    'metric_4d': 0.9706,            # 4D metric constant
    'torsion_4d': 0.9706,           # 4D torsion
    'alpha2_L': 6.0,                # Left impedance margin (choke)
    'alpha2_R': 10.0,               # Right impedance margin (corridor)
    'gear_ratio': 0.4495,           # Bifurcation gear ratio
}

# ============================================
# 17 GEOMETRY NODES (Universal anchors)
# ============================================
GEOMETRY_NODES = {
    'O':  {'layer': 0, 'x': 0.0,  'y': 0.0,  'z': -6.0, 'sh_r': 0.1121, 'sh_q0': 0.9646, 
           'archetype': 'Big Man', 'ab_type': 'A', 'gender': 'male'},
    'A':  {'layer': 1, 'x': 2.0,  'y': 0.0,  'z': 0.0,  'sh_r': 0.1126, 'sh_q0': 0.9646,
           'archetype': 'Big Woman', 'ab_type': 'B', 'gender': 'female'},
    'B':  {'layer': 1, 'x': 0.0,  'y': 2.0,  'z': 0.0,  'sh_r': 0.1121, 'sh_q0': 0.9720,
           'archetype': 'Big Woman', 'ab_type': 'AB', 'gender': 'female'},
    'C':  {'layer': 1, 'x': -2.0, 'y': 0.0,  'z': 0.0,  'sh_r': 0.1126, 'sh_q0': 0.9646,
           'archetype': 'Big Man', 'ab_type': 'A', 'gender': 'male'},
    'D':  {'layer': 1, 'x': 0.0,  'y': -2.0, 'z': 0.0,  'sh_r': 0.1121, 'sh_q0': 0.9720,
           'archetype': 'Big Man', 'ab_type': 'B', 'gender': 'male'},
    'E':  {'layer': 2, 'x': 4.0,  'y': 0.0,  'z': 1.5,  'sh_r': 0.1121, 'sh_q0': 0.9646,
           'archetype': 'Small Woman', 'ab_type': 'AB', 'gender': 'female'},
    'F':  {'layer': 2, 'x': 2.83, 'y': 2.83, 'z': 1.5,  'sh_r': 0.1121, 'sh_q0': 0.9646,
           'archetype': 'Small Woman', 'ab_type': 'A', 'gender': 'female'},
    'G':  {'layer': 2, 'x': 0.0,  'y': 4.0,  'z': 1.5,  'sh_r': 0.1126, 'sh_q0': 0.9646,
           'archetype': 'Small Woman', 'ab_type': 'B', 'gender': 'female'},
    'H':  {'layer': 2, 'x': -2.83,'y': 2.83, 'z': 1.5,  'sh_r': 0.1121, 'sh_q0': 0.9646,
           'archetype': 'Small Man', 'ab_type': 'AB', 'gender': 'male'},
    'I':  {'layer': 2, 'x': -4.0, 'y': 0.0,  'z': 1.5,  'sh_r': 0.1126, 'sh_q0': 0.9646,
           'archetype': 'Small Man', 'ab_type': 'A', 'gender': 'male'},
    'J':  {'layer': 2, 'x': -2.83,'y': -2.83,'z': 1.5,  'sh_r': 0.1121, 'sh_q0': 0.9646,
           'archetype': 'Small Man', 'ab_type': 'B', 'gender': 'male'},
    'K':  {'layer': 2, 'x': 0.0,  'y': -4.0, 'z': 1.5,  'sh_r': 0.1126, 'sh_q0': 0.9646,
           'archetype': 'Small Man', 'ab_type': 'AB', 'gender': 'male'},
    'L':  {'layer': 2, 'x': 2.83, 'y': -2.83,'z': 1.5,  'sh_r': 0.1121, 'sh_q0': 0.9646,
           'archetype': 'Small Woman', 'ab_type': 'A', 'gender': 'female'},
    'M':  {'layer': 3, 'x': 6.0,  'y': 0.0,  'z': 3.0,  'sh_r': 0.1121, 'sh_q0': 0.9646,
           'archetype': 'AB Male', 'ab_type': 'AB', 'gender': 'male'},
    'N':  {'layer': 3, 'x': 0.0,  'y': 6.0,  'z': 3.0,  'sh_r': 0.1121, 'sh_q0': 0.9646,
           'archetype': 'AB Female', 'ab_type': 'AB', 'gender': 'female'},
    'P':  {'layer': 3, 'x': -6.0, 'y': 0.0,  'z': 3.0,  'sh_r': 0.1121, 'sh_q0': 0.9646,
           'archetype': 'AB Male', 'ab_type': 'AB', 'gender': 'male'},
    'Q':  {'layer': 3, 'x': 0.0,  'y': -6.0, 'z': 3.0,  'sh_r': 0.1121, 'sh_q0': 0.9646,
           'archetype': 'AB Female', 'ab_type': 'AB', 'gender': 'female'},
}

# ============================================
# AB MALE/FEMALE SPARK DYNAMICS
# ============================================
"""
AB Male Spark Mechanism:
- Day: Sees B-type (woman) → cortisol (stress)
- Night: Sees A-type (man) → oxytocin (bonding)
- Result: "Night-Spark Paradox" - ignition happens in darkness

AB Female Spark Mechanism:
- Constant A-mode (woman-seeking)
- Mirror spark through AB-mimicry
- Bifurcates at 138.88° diagonal

QCD Confinement Analogy for Gender:
- Male = "quark" (confined, singular trajectory)
- Female = "gluon" (binding, multi-path)
- Rebranching = "hadronization" (gender expression shift)
"""

class ABSparkDynamics:
    def __init__(self, ab_type, gender):
        self.ab_type = ab_type  # 'A', 'B', or 'AB'
        self.gender = gender    # 'male' or 'female'
        self.theta_spark = CONSTANTS['spark_angle_theta']
        
    def calculate_ignition_potential(self, x, y, z, t):
        """Ψ_spark = κ × H(t - t_critical) × δ(E - E_threshold)"""
        # Distance from 138.88° diagonal
        diagonal_distance = abs((x + y) - 16) / np.sqrt(2)  # x+y=16 is the PLP seam
        
        # Night-spark activation (for AB Male)
        if self.ab_type == 'AB' and self.gender == 'male':
            # Night mode: higher potential when x > y (right corridor dominance)
            night_factor = 1.0 if x > y else 0.3
        else:
            night_factor = 1.0
            
        # Spark ignition at critical angle
        spark_potential = np.exp(-diagonal_distance / 2.0) * night_factor
        
        return spark_potential
    
    def gender_rebranching(self, current_path, stress_level):
        """
        QCD Confinement Analogy:
        - High stress → "deconfined" state (trajectory shift)
        - Critical stress → rebranching to opposite gender pathway
        """
        if stress_level > 0.8:
            # Rebranching event - trajectory jumps to mirror terminal
            return self._mirror_terminal(current_path)
        return current_path
    
    def _mirror_terminal(self, path):
        """Mirror terminal crossover (138.88° reflection)"""
        return {'x': 16 - path['x'], 'y': 16 - path['y'], 'mirrored': True}

# ============================================
# UNIVERSAL POTENTIAL FIELD
# ============================================
class UniversalField:
    def __init__(self):
        self.constants = CONSTANTS
        self.nodes = GEOMETRY_NODES
        
    def sh_field(self, X, Y, Z):
        """Swift-Hohenberg potential: Ψ_SH = [r - (q0² + ∇²)²]u - u³"""
        potential = np.zeros_like(X)
        
        for node_id, node in self.nodes.items():
            dx = X - node['x']
            dy = Y - node['y']
            dz = Z - node['z']
            r = np.sqrt(dx**2 + dy**2 + dz**2)
            
            # SH stability well
            r_param = node['sh_r']
            q0_param = node['sh_q0']
            depth = 3.0 * (r_param / 0.1121) * (q0_param / 0.9646)
            
            potential += -depth * np.exp(-r**2 / 4.0)
            
        return potential
    
    def ab_asymmetry(self, X, Y, Z):
        """AB Male/Female asymmetric impedance: Ψ_AB"""
        # Left choke (A-type, α₂=6)
        left_mask = X < 0
        # Right corridor (B-type, α₂=10)
        right_mask = X > 0
        
        modifier = np.ones_like(X)
        modifier[left_mask] *= (6.0 / 10.0)  # Left constricted
        modifier[right_mask] *= (10.0 / 6.0)  # Right expanded
        
        return modifier
    
    def spark_gate(self, X, Y, Z):
        """138.88° diagonal spark gate: Ψ_spark"""
        # Convert to face coordinates (0-16 grid mapping)
        X_face = (X + 8)  # Map -8~8 to 0~16
        Y_face = (Y + 8)
        
        # Distance from x+y=16 diagonal (PLP seam)
        diagonal_dist = np.abs(X_face + Y_face - 16) / np.sqrt(2)
        
        # Spark gate opens near diagonal
        spark_field = np.exp(-diagonal_dist / 1.5)
        
        return spark_field
    
    def calculate_total_field(self, X, Y, Z):
        """Ψ_universe = Ψ_SH × Ψ_AB × Ψ_spark"""
        field_sh = self.sh_field(X, Y, Z)
        field_ab = self.ab_asymmetry(X, Y, Z)
        field_spark = self.spark_gate(X, Y, Z)
        
        # Combined universal field
        universal = field_sh * field_ab * (1 + 0.5 * field_spark)
        
        return universal

# ============================================
# GENDER REBRANCHING (QCD Analogy)
# ============================================
class GenderRebranching:
    """
    QCD Confinement → Gender Expression
    
    Quark (Male)        Gluon (Female)
    ↓                   ↓
    Confined            Binding
    Singular path       Multi-path
    ↓                   ↓
    Rebranching ←─────── Rebranching
    (at critical stress) (at spark ignition)
    """
    
    def __init__(self):
        self.rebranching_threshold = 0.75
        self.confinement_strength = 0.03125  # kappa
        
    def calculate_trajectory(self, start_node, end_node, gender, ab_type):
        """Calculate gender-specific trajectory through geometry nodes"""
        # Get node coordinates
        start = GEOMETRY_NODES[start_node]
        end = GEOMETRY_NODES[end_node]
        
        # Gender-specific path modulation
        if gender == 'male':
            # Male: direct path (quark-like, confined)
            path_x = np.linspace(start['x'], end['x'], 50)
            path_y = np.linspace(start['y'], end['y'], 50)
            path_z = np.linspace(start['z'], end['z'], 50)
        else:
            # Female: curved path (gluon-like, binding)
            t = np.linspace(0, 1, 50)
            path_x = start['x'] + (end['x'] - start['x']) * t
            path_y = start['y'] + (end['y'] - start['y']) * t + 2 * np.sin(np.pi * t)
            path_z = start['z'] + (end['z'] - start['z']) * t
            
        return path_x, path_y, path_z
    
    def rebranching_event(self, current_gender, spark_intensity, stress):
        """Determine if rebranching occurs"""
        if spark_intensity > 0.9 and stress > self.rebranching_threshold:
            # Rebranching triggered
            new_gender = 'female' if current_gender == 'male' else 'male'
            return {
                'original': current_gender,
                'new': new_gender,
                'trigger': '138.88° spark ignition',
                'intensity': spark_intensity
            }
        return None

# ============================================
# VISUALIZATION
# ============================================
def plot_universe_master_equation():
    fig = plt.figure(figsize=(24, 18))
    
    # Initialize field calculator
    field = UniversalField()
    spark = ABSparkDynamics('AB', 'male')
    rebranch = GenderRebranching()
    
    # Create coordinate grids
    x = np.linspace(-10, 10, 150)
    y = np.linspace(-10, 10, 150)
    z = np.linspace(-6, 6, 80)
    
    # ========================================
    # PANEL 1: Universal Field (3D)
    # ========================================
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    
    X, Y, Z_grid = np.meshgrid(x[::3], y[::3], z[::4])
    field_3d = field.calculate_total_field(X, Y, Z_grid)
    
    # Plot field as scatter
    step = 2
    scatter = ax1.scatter(X[::step, ::step, ::step].flatten(),
                        Y[::step, ::step, ::step].flatten(),
                        Z_grid[::step, ::step, ::step].flatten(),
                        c=field_3d[::step, ::step, ::step].flatten(),
                        cmap='plasma', s=2, alpha=0.4)
    
    # Plot 17 geometry nodes with AB/gender labels
    for node_id, node in GEOMETRY_NODES.items():
        color = 'cyan' if node['ab_type'] in ['A', 'AB'] else 'magenta'
        size = 100 if node['layer'] == 0 else 60
        ax1.scatter([node['x']], [node['y']], [node['z']],
                   c=color, s=size, edgecolors='black', linewidth=2)
        
        label = f"{node_id}\n{node['ab_type']}-{node['gender'][0]}"
        ax1.text(node['x'], node['y'], node['z']+0.8, label,
                fontsize=7, ha='center', color='white')
    
    ax1.set_title('UNIVERSAL MASTER EQUATION\nΨ = Ψ_SH × Ψ_AB × Ψ_spark', fontsize=11, fontweight='bold')
    
    # ========================================
    # PANEL 2: AB Male Spark Dynamics
    # ========================================
    ax2 = fig.add_subplot(2, 3, 2)
    
    # Day/Night cycle for AB Male
    time = np.linspace(0, 24, 100)
    cortisol = 0.5 + 0.3 * np.sin(2 * np.pi * time / 24)  # Day peak
    oxytocin = 0.3 + 0.4 * (1 - np.sin(2 * np.pi * time / 24))  # Night peak
    
    ax2.plot(time, cortisol, 'r-', linewidth=2, label='Cortisol (Day-Stress)')
    ax2.plot(time, oxytocin, 'b-', linewidth=2, label='Oxytocin (Night-Bond)')
    ax2.axvspan(18, 6, alpha=0.2, color='navy', label='Night Spark Window')
    ax2.set_xlabel('Hour of Day')
    ax2.set_ylabel('Hormone Level')
    ax2.set_title('AB MALE NIGHT-SPARK PARADOX\nDay=B-mode, Night=A-mode', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=8)
    
    # ========================================
    # PANEL 3: 138.88° Diagonal Reset
    # ========================================
    ax3 = fig.add_subplot(2, 3, 3)
    
    # Face grid with diagonal
    face_x = np.linspace(0, 16, 100)
    face_y = 16 - face_x  # x+y=16 diagonal
    
    # Spark potential along diagonal
    spark_potential = np.exp(-np.abs(face_x - 8) / 3)
    
    ax3.fill_between(face_x, 0, spark_potential, alpha=0.5, color='yellow', label='Spark Gate')
    ax3.plot(face_x, face_y, 'r--', linewidth=3, label='138.88° PLP Seam')
    ax3.scatter([6, 10], [10, 6], c=['red', 'blue'], s=200, zorder=5)
    ax3.text(6, 10.5, 'α₂-L\n(Choke)', ha='center', fontsize=9)
    ax3.text(10, 5.5, 'α₂-R\n(Corridor)', ha='center', fontsize=9)
    ax3.set_xlim(0, 16)
    ax3.set_ylim(0, 16)
    ax3.set_title('138.88° DIAGONAL RESET\nx+y=16 PLP Spine Seam', fontsize=11, fontweight='bold')
    ax3.legend(fontsize=8)
    
    # ========================================
    # PANEL 4: Gender Rebranching (QCD)
    # ========================================
    ax4 = fig.add_subplot(2, 3, 4)
    
    # Quark (Male) trajectory
    t = np.linspace(0, 1, 50)
    male_x = 2 + 4 * t
    male_y = np.zeros_like(t)
    
    # Gluon (Female) trajectory
    female_x = 2 + 4 * t
    female_y = 2 * np.sin(3 * np.pi * t)
    
    ax4.plot(male_x, male_y, 'b-', linewidth=3, label='Male (Quark/Confined)')
    ax4.plot(female_x, female_y, 'r-', linewidth=3, label='Female (Gluon/Binding)')
    ax4.scatter([6], [0], c='blue', s=150, marker='s', zorder=5)
    ax4.scatter([6], [0], c='red', s=150, marker='o', zorder=5)
    ax4.annotate('Rebranching Point', xy=(6, 0), xytext=(8, 2),
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=10, color='green')
    ax4.set_title('GENDER REBRANCHING\nQCD Confinement Analogy', fontsize=11, fontweight='bold')
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3)
    
    # ========================================
    # PANEL 5: Universal Field 2D Heatmap
    # ========================================
    ax5 = fig.add_subplot(2, 3, 5)
    
    X_2d, Y_2d = np.meshgrid(x, y)
    Z_zero = np.zeros_like(X_2d)
    field_2d = field.calculate_total_field(X_2d, Y_2d, Z_zero)
    
    im = ax5.imshow(field_2d, extent=[-10, 10, -10, 10], origin='lower',
                    cmap='plasma', aspect='auto')
    plt.colorbar(im, ax=ax5, fraction=0.046)
    
    # Overlay geometry nodes
    for node_id, node in GEOMETRY_NODES.items():
        color = 'white' if node['layer'] == 0 else 'yellow'
        ax5.scatter([node['x']], [node['y']], c=color, s=80, edgecolors='black')
        ax5.text(node['x']+0.3, node['y']+0.3, node_id, fontsize=9, color='white')
    
    ax5.set_title('UNIVERSAL FIELD (Z=0)\nCoronal Plane', fontsize=11, fontweight='bold')
    
    # ========================================
    # PANEL 6: Master Equation Summary
    # ========================================
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.axis('off')
    
    equation_text = """
    UNIVERSAL MASTER EQUATION
    
    Ψ_universe(x,y,z,t) = Ψ_SH × Ψ_AB × Ψ_gender × Ψ_spark
    
    Ψ_SH = [r - (q₀² + ∇²)²]u - u³
           (Swift-Hohenberg Spiral Backbone)
    
    Ψ_AB = α₂ × (1 + β·δ(x-x_L)) × (1 - γ·δ(x-x_R))
           (AB Male/Female Asymmetry)
           α₂-L = 6.0 (Choke)
           α₂-R = 10.0 (Corridor)
    
    Ψ_gender = ε × exp(-θ/138.88°)
           (Gender Rebranching at Spark Angle)
    
    Ψ_spark = κ × H(t-t_critical) × δ(E-E_threshold)
           (Higgs Ignition/Night-Spark)
    
    CONSTANTS (Locked):
    r = 0.1123, q₀ = 0.965, κ = 1/32
    θ_spark = 138.88°, metric_4d = 0.9706
    
    17 GEOMETRY NODES (O-Q)
    128 ARCHETYPES (MBTI × Blood × Gender)
    26 UROBOROS ANCHORS (Face→Body Mapping)
    """
    
    ax6.text(0.05, 0.95, equation_text, transform=ax6.transAxes,
            fontsize=10, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.8),
            color='white')
    
    plt.tight_layout()
    plt.savefig('universal_master_equation.png', dpi=300, bbox_inches='tight',
                facecolor='black', edgecolor='none')
    plt.savefig('universal_master_equation.pdf', dpi=300, bbox_inches='tight',
                facecolor='black', edgecolor='none')
    plt.show()
    
    print("="*70)
    print("UNIVERSAL MASTER EQUATION VISUALIZATION COMPLETE")
    print("="*70)
    print("Generated: universal_master_equation.png/pdf")
    print("="*70)

# Execute
if __name__ == "__main__":
    plot_universe_master_equation()