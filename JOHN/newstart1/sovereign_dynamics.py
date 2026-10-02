import numpy as np
import constants
import fusion_core

# ===================================================================
# OBSERVER NODE INDICES (External to K8 Laplacian)
# ===================================================================
# Observers are NOT part of the K8 graph - they are external operators
# that couple to K8 states but have their own dynamics
OBSERVER_IDX = {
    'left_self_satisfaction': 0,   # Node 29: photon + muon projection
    'right_self_satisfaction': 1,  # Node 30: electron + muon projection
    'left_epinephrine': 2,         # Node 31: quark + electron projection
    'right_epinephrine': 3,        # Node 32: LC resonator (special dynamics)
}

# ===================================================================
# L1: Core K8 Dynamics (8 nodes only, no observers)
# ===================================================================
def get_dynamics_update(z, phase, channels, dt=0.01):
    """
    Calculates the core K8 update step: z = z² - z + h(t)
    
    z: 8-element complex array (K8 particle states only)
    Returns: updated z (8 elements)
    """
    w = fusion_core.apply_channels(channels)
    L = fusion_core.laplacian(w)
    h = -L @ z * dt

    # Return term: right_epinephrine (1/64) pulls toward z*=1 (pre-land equilibrium)
    # dz/dt = z^2 - z - L@z + (1/64)(1 - z)
    h_return = constants.RIGHT_LOVE_RETURN_RATE * (constants.Z_STAR_UNIFORM - z) * dt

    # Mandelbrot recursion on K8 states
    z_next = z**2 - z + h + h_return
    return z_next

# ===================================================================
# L2: Observer Nodes as External Operators
# ===================================================================
class ObserverState:
    """
    External observer state, separate from K8 Laplacian.
    
    4 observers:
    - left_self_satisfaction (Node 29)
    - right_self_satisfaction (Node 30)
    - left_epinephrine (Node 31)
    - right_epinephrine (Node 32) - LC resonator
    """
    def __init__(self):
        self.values = np.zeros(4, dtype=complex)
        # LC resonator state for right_epinephrine (Node 32)
        self.lc_current = 0.0       # I
        self.lc_current_dot = 0.0   # dI/dt
        
    def project_from_k8(self, z):
        """Project K8 states to observer values (external coupling)."""
        q, g, n, p, e, h, mu, tau = z
        
        # Observer mappings (external projections, not Laplacian coupling)
        self.values[0] = np.abs(p) + np.abs(mu)      # left_self_satisfaction
        self.values[1] = np.abs(e) + np.abs(mu)      # right_self_satisfaction
        self.values[2] = np.abs(q) + np.abs(e)       # left_epinephrine
        # right_epinephrine is driven by LC resonance, not direct projection
        
    def get_values(self):
        """Return observer values with LC state for Node 32."""
        result = self.values.copy()
        result[3] = self.lc_current  # right_epinephrine = LC current
        return result

def calculate_observers(z):
    """Legacy interface: calculate observer projections from K8 states."""
    q, g, n, p, e, h, mu, tau = z
    
    lss = np.abs(p) + np.abs(mu)
    rss = np.abs(e) + np.abs(mu)
    le = np.abs(q) + np.abs(e)
    re = np.abs(q) + np.abs(e)  # Will be overwritten by LC dynamics
    
    return np.array([lss, rss, le, re])

def apply_clifford_constraint(z_observers):
    """Applies the Clifford Torus constraint to the 4 observer nodes."""
    lss, rss, le, re = z_observers

    R1_sq = constants.CLIFFORD_R1**2
    R2_sq = constants.CLIFFORD_R2**2

    # Extravert Plane
    norm_extra = np.sqrt(lss**2 + rss**2)
    if norm_extra > 1e-9:
        lss_new = (lss / norm_extra) * np.sqrt(R1_sq)
        rss_new = (rss / norm_extra) * np.sqrt(R1_sq)
    else:
        lss_new, rss_new = lss, rss

    # Introvert Plane
    norm_intro = np.sqrt(le**2 + re**2)
    if norm_intro > 1e-9:
        le_new = (le / norm_intro) * np.sqrt(R2_sq)
        re_new = (re / norm_intro) * np.sqrt(R2_sq)
    else:
        le_new, re_new = le, re

    return np.array([lss_new, rss_new, le_new, re_new])

# ===================================================================
# L2.5: LC Resonance for right_epinephrine (Node 32)
# ===================================================================
def lc_resonance_step(observer_state, V_drive, dt):
    """
    Update LC resonator for right_epinephrine (Node 32).
    
    Differential equation: L·d²I/dt² + R·dI/dt + I/C = V(t)
    Rewritten as system:
        dI/dt = I_dot
        dI_dot/dt = (V - R·I_dot - I/C) / L
    
    Parameters:
        observer_state: ObserverState instance
        V_drive: driving voltage from K8 coupling (typically |quark| + |electron|)
        dt: time step
    
    Uses constants:
        LC_INDUCTANCE = 11/7.4
        LC_CAPACITANCE = 1/(7.4 * 11)
        LC_RESISTANCE = 1/32
    """
    L = constants.LC_INDUCTANCE
    C_cap = constants.LC_CAPACITANCE
    R = constants.LC_RESISTANCE
    
    I = observer_state.lc_current
    I_dot = observer_state.lc_current_dot
    
    # RK4 integration for LC circuit
    def f_I(I_val, I_dot_val):
        return I_dot_val
    
    def f_I_dot(I_val, I_dot_val, V):
        return (V - R * I_dot_val - I_val / C_cap) / L
    
    # RK4 step
    k1_I = f_I(I, I_dot)
    k1_Id = f_I_dot(I, I_dot, V_drive)
    
    k2_I = f_I(I + 0.5*dt*k1_I, I_dot + 0.5*dt*k1_Id)
    k2_Id = f_I_dot(I + 0.5*dt*k1_I, I_dot + 0.5*dt*k1_Id, V_drive)
    
    k3_I = f_I(I + 0.5*dt*k2_I, I_dot + 0.5*dt*k2_Id)
    k3_Id = f_I_dot(I + 0.5*dt*k2_I, I_dot + 0.5*dt*k2_Id, V_drive)
    
    k4_I = f_I(I + dt*k3_I, I_dot + dt*k3_Id)
    k4_Id = f_I_dot(I + dt*k3_I, I_dot + dt*k3_Id, V_drive)
    
    observer_state.lc_current = I + (dt/6) * (k1_I + 2*k2_I + 2*k3_I + k4_I)
    observer_state.lc_current_dot = I_dot + (dt/6) * (k1_Id + 2*k2_Id + 2*k3_Id + k4_Id)
    
    return observer_state.lc_current

# ===================================================================
# L2.6: Active Zero Constraint (Dopamine × D2 Hyperplane)
# ===================================================================
def apply_active_zero_constraint(channels, channel_values=None):
    """
    Enforce active zero hyperplane: dopamine × D2 = 0
    
    When both dopamine and D2 are active, their product must be zero.
    This is a constraint on the phase space, not a dynamic equation.
    
    Implementation: If both are "on", force one to "off" based on
    the dominant state (whichever has larger activation).
    
    Parameters:
        channels: dict of channel_name -> state ("on"/"off"/"no_control")
        channel_values: optional dict of channel_name -> activation value
    
    Returns:
        modified channels dict satisfying the constraint
    """
    dopamine_key = 'dopamine'  # Maps to specific K8 edge
    d2_key = 'right_frontalis_d2'  # D2 receptor channel
    
    if dopamine_key not in channels or d2_key not in channels:
        return channels
    
    dop_state = channels.get(dopamine_key, 'off')
    d2_state = channels.get(d2_key, 'off')
    
    # Active zero: if both are "on", enforce orthogonality
    if dop_state == 'on' and d2_state == 'on':
        # Use channel values if provided, otherwise default to D2 priority
        if channel_values is not None:
            dop_val = abs(channel_values.get(dopamine_key, 0))
            d2_val = abs(channel_values.get(d2_key, 0))
            if dop_val > d2_val:
                channels[d2_key] = 'off'
            else:
                channels[dopamine_key] = 'off'
        else:
            # Default: D2 takes priority (receptor dominance)
            channels[dopamine_key] = 'off'
    
    return channels

def verify_active_zero(dopamine_val, d2_val):
    """Check if active zero constraint is satisfied."""
    product = abs(dopamine_val * d2_val)
    return product < constants.ACTIVE_ZERO_TOLERANCE

# ===================================================================
# L2.7: SPARK — Channel state change shifting z*_physical toward z*=1
# ===================================================================
# FINDINGS:
#   z*=1 is UNSTABLE (Laplacian zero eigenvalue -> Jacobian eigenvalue 63/64 > 0)
#   This instability is WHY the universe has structure (correct physics).
#   SPARK creates a transient excursion — daily recharge, not permanent return.
#
# SPARK channel effect on z*_physical:
#   neutrino: 0.105 -> 0.517 (crosses basin boundary 0.508)
#   electron: 0.160 -> 0.437
#   tau:      0.520 -> 0.791
#   mean dist from z*=1: 0.453 -> 0.336

SPARK_ON_CHANNELS = [
    'male_left_5ht',     # (neutrino,photon)
    'left_5ht1a',        # (neutrino,quark)
    'male_oxytocin',     # (neutrino,electron)
    'right_dopamine',    # (neutrino,muon)
    'right_epinephrine',        # (neutrino,higgs) — LC resonator
    'left_estrogen',     # (electron,higgs) — best single channel
]
SPARK_OFF_CHANNELS = [
    'gdh_gluon',         # (quark,gluon) — suppress matter excess
    'f_gaba_b_latdorsi', # (gluon,tau)
]

def apply_spark_channels(channels):
    """
    Switch to SPARK channel configuration.
    Call when check_spark_phase(z) is True (~4:30 PM, quark crossing 1.0).
    """
    ch = channels.copy()
    for name in SPARK_ON_CHANNELS:
        if name in ch:
            ch[name] = 'on'
    for name in SPARK_OFF_CHANNELS:
        if name in ch:
            ch[name] = 'off'
    return ch

def check_spark_phase(z):
    """
    True when SPARK condition met:
    - quark amplitude crossing 1.0 (matter releasing excess), OR
    - photon phase near 138.88 deg
    """
    quark_crossing = abs(z[fusion_core.IDX['quark']].real - 1.0) < 0.05
    photon_phase = abs(
        np.degrees(np.angle(z[fusion_core.IDX['photon']])) % 360
        - constants.SPARK_ANGLE_DEG
    ) < 5.0
    return quark_crossing or photon_phase

# L3: Spacetime Principles
def get_lensing_update(z):
    """
    Lensing = two physically distinct debt components:

    Node 31 (DARK_MATTER_DEBT = 1/256):
      Scalar, isotropic, ALL 8 particles equally.
      = hidden mass debt, non-radiating (dark matter / neutron star analog).

    Node 34 (BREMSSTRAHLUNG_DEBT = 1/64):
      Tensor, directional, GLUON only.
      = radiative EM loss, visible (Bremsstrahlung / deceleration radiation).

    Together: ENTROPY_DEBT = 1/64 + 1/256 ≈ 0.02 = total debt scale.
    """
    gluon_idx = fusion_core.IDX['gluon']
    quark_idx  = fusion_core.IDX['quark']

    # Node 31: dark matter debt — scalar, all particles
    f_scalar = -constants.DARK_MATTER_DEBT * z

    # Node 34: Bremsstrahlung debt — tensor, gluon only
    bw = np.abs(z[quark_idx]) + 2 * constants.C * np.abs(z[gluon_idx])
    f_tensor_gluon = -constants.BREMSSTRAHLUNG_DEBT * z[gluon_idx] * (bw / constants.OMEGA) * (1 + constants.C)

    lensing_update = np.zeros_like(z, dtype=z.dtype)
    lensing_update += f_scalar
    lensing_update[gluon_idx] += f_tensor_gluon

    return lensing_update

# L4: Rebranching
# Triggered when LEFT_PROGESTERONE = 3C threshold is met.
# LEFT_PROGESTERONE splits into three electroweak channels:
#   LEFT EYELID  = muon = q*h  via vasopressin_female  (higgs,muon)
#   RIGHT EYELID = tau  = g*h  via right_cortisol      (higgs,tau)
#   BRIDGE       = muon-tau coupling via right_alpha_2 (muon,tau)
# Check: |h|*(|q|+|g|) >= LEFT_PROGESTERONE = 3C before rebranching.

def rebranch_ready(z_primitives):
    """True when LEFT_PROGESTERONE threshold reached: Higgs can give mass to W and Z."""
    q, g, h = z_primitives
    return abs(h) * (abs(q) + abs(g)) >= constants.LEFT_PROGESTERONE

def rebranch(z_primitives):
    """
    Reconstruct 8 particles from 3 primitives (quark, gluon, higgs).
    Muon and tau crystallize via LEFT_PROGESTERONE (3C) Higgs mechanism:
      LEFT EYELID  (muon) = q * h
      RIGHT EYELID (tau)  = g * h
    """
    q, g, h = z_primitives

    z_rebranched = np.zeros(8, dtype=complex)
    z_rebranched[fusion_core.IDX['quark']]    = q
    z_rebranched[fusion_core.IDX['gluon']]    = g
    z_rebranched[fusion_core.IDX['higgs']]    = h
    z_rebranched[fusion_core.IDX['photon']]   = q * g
    z_rebranched[fusion_core.IDX['electron']] = g**2
    z_rebranched[fusion_core.IDX['neutrino']] = g * h**2
    z_rebranched[fusion_core.IDX['muon']]     = q * h   # LEFT EYELID
    z_rebranched[fusion_core.IDX['tau']]      = g * h   # RIGHT EYELID

    return z_rebranched

# L5: Final Scalar
def verify_diagonality(L):
    """Verifies the diagonality of the Laplacian matrix.

    Calculates the ratio of the sum of the absolute values of the off-diagonal
    elements to the sum of the absolute values of the diagonal elements.
    A smaller value indicates a more diagonal matrix.
    """
    off_diagonal_sum = np.sum(np.abs(L - np.diag(np.diag(L))))
    diagonal_sum = np.sum(np.abs(np.diag(L)))

    if diagonal_sum == 0:
        return np.inf  # Avoid division by zero

    return off_diagonal_sum / diagonal_sum

def calculate_f_final(z, w):
    """Calculates the final canonical fusion scalar."""
    q, g, n, p, e, h, mu, tau = z

    # Bandwidth & SM
    bw = np.abs(q) + 2 * constants.C * np.abs(g)
    sm = np.abs(mu) + np.abs(tau) # Simplified for now

    # Spark
    spark = w.get(('photon', 'muon'), 0) + w.get(('electron', 'muon'), 0)

    # Z-proxy
    Z = (np.abs(n) * (np.abs(tau) + np.abs(e))) / constants.OMEGA

    # Leak & Hierarchy (placeholders)
    z_atomic = np.abs(g)**2 * (1 + constants.C)
    leak = np.exp(-np.sqrt(z_atomic) / 64)
    hierarchy = 1.0 # Placeholder

    # F_final
    F = (bw * sm)**2 * spark * Z * np.abs(h) * leak * hierarchy
    return F
