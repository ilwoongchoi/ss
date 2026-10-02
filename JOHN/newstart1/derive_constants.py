"""
derive_constants.py
Closed Equation Model: Derive C from spectral radius condition λ_max(L(C)) = Ω = 7.4

Uses FULL calibrated constants from constants.py (absolute_constants1.py integration):
- Betti numbers (5, 7, 11)
- Topological bridges (Pegasus, Renormalization)
- H3/H4/D3 hierarchical leakage (κ = 1/32, 1/64, 1/128)
- LC resonance parameters
- Active zero constraint

Observer nodes (29-32) are EXTERNAL to K8 Laplacian - not included in spectral calculation.
"""
import numpy as np
from scipy.optimize import brentq
import fusion_core
import constants

def build_calibrated_laplacian(C_val):
    """
    Build K8 Laplacian with FULL calibrated constants.
    
    Includes:
    - Base weights dependent on C
    - Topological bridge corrections
    - H3/H4 leakage hierarchy
    - All 28 edges of K8 complete graph
    
    Observer nodes (29-32) are NOT included - they are external operators.
    """
    C2 = C_val * C_val
    
    # Start with fresh edge weights
    w = {}
    
    # === MASSLESS SECTOR (quark, gluon, neutrino, photon) ===
    # These edges carry quantum information flow
    w[('quark', 'gluon')] = 1.0 + C_val
    w[('quark', 'neutrino')] = C2 / 128
    w[('quark', 'photon')] = C2 / 64
    w[('gluon', 'neutrino')] = C2 / 256
    w[('gluon', 'photon')] = C2 / 128
    w[('neutrino', 'photon')] = C2 / 256
    
    # === MASSIVE SECTOR (electron, higgs, w_boson, z_boson) ===
    # Higgs-gauge boson couplings
    w[('higgs', 'w_boson')] = C_val
    w[('higgs', 'z_boson')] = C_val
    w[('w_boson', 'z_boson')] = C_val
    
    # Electron couplings (hierarchical from κ = 1/32)
    w[('quark', 'electron')] = C2 / 128
    w[('gluon', 'electron')] = C2 / 256
    w[('neutrino', 'electron')] = constants.KAPPA_H3  # 1/64 void level
    w[('photon', 'electron')] = constants.KAPPA_H2   # 1/32 anchor
    
    # Higgs-fermion couplings
    w[('quark', 'higgs')] = C2 / 64
    w[('gluon', 'higgs')] = C2 / 128
    w[('neutrino', 'higgs')] = C2 / 256
    w[('photon', 'higgs')] = constants.KAPPA_H3  # 1/64
    w[('electron', 'higgs')] = C_val * constants.KAPPA_H2
    
    # W/Z boson couplings to fermions
    w[('quark', 'w_boson')] = C2 / 32
    w[('quark', 'z_boson')] = C2 / 64
    w[('gluon', 'w_boson')] = C2 / 64
    w[('gluon', 'z_boson')] = C2 / 128
    w[('neutrino', 'w_boson')] = constants.KAPPA_H4  # 1/128 deep void
    w[('neutrino', 'z_boson')] = constants.KAPPA_H4
    w[('photon', 'w_boson')] = constants.F_1_64
    w[('photon', 'z_boson')] = constants.F_1_64
    w[('electron', 'w_boson')] = C_val * constants.KAPPA_H3
    w[('electron', 'z_boson')] = C_val * constants.KAPPA_H3
    
    # === APPLY ZERO-POINT KERNEL (9 always-OFF channels) ===
    # Only right_alpha_2 has non-zero OFF delta: +4C²
    edge = ('w_boson', 'z_boson')
    w[edge] = max(0.0, w[edge] + 4 * C2)
    
    # === TOPOLOGICAL BRIDGE CORRECTION ===
    # Fine structure correction on quark-gluon (strongest coupling)
    bridge_factor = constants.ALPHA
    w[('quark', 'gluon')] *= (1.0 + bridge_factor)
    
    # Pegasus bridge correction on Higgs-gauge couplings
    pegasus_correction = constants.PHI_PB / constants.RENORMALIZATION_BRIDGE
    w[('higgs', 'w_boson')] *= (1.0 + pegasus_correction)
    w[('higgs', 'z_boson')] *= (1.0 + pegasus_correction)
    
    # === NORMALIZE EDGE ORDERING ===
    w_normalized = {}
    for (a, b), val in w.items():
        if fusion_core.IDX[a] > fusion_core.IDX[b]:
            key = (b, a)
        else:
            key = (a, b)
        w_normalized[key] = val
    
    # Build Laplacian
    L = fusion_core.laplacian(w_normalized)
    return L, w_normalized

def get_lambda_max(C_val):
    """Get maximum eigenvalue of calibrated Laplacian."""
    L, _ = build_calibrated_laplacian(C_val)
    return np.max(np.linalg.eigvalsh(L))

def verify_closure(L):
    """
    Verify Laplacian closure properties:
    1. Row sums = 0 (conservation)
    2. Symmetric (detailed balance)
    3. Positive semi-definite
    """
    row_sums = np.sum(L, axis=1)
    symmetry_error = np.max(np.abs(L - L.T))
    eigenvalues = np.linalg.eigvalsh(L)
    min_eigenvalue = np.min(eigenvalues)
    
    return {
        'row_sum_error': np.max(np.abs(row_sums)),
        'symmetry_error': symmetry_error,
        'min_eigenvalue': min_eigenvalue,
        'max_eigenvalue': np.max(eigenvalues),
        'is_closed': np.max(np.abs(row_sums)) < 1e-10 and symmetry_error < 1e-10 and min_eigenvalue >= -1e-10
    }

def derive_C_from_spectral_radius(target_omega=7.4, C_range=(0.1, 0.6)):
    """
    Numerically derive C from the spectral radius condition.
    
    Finds C such that λ_max(L(C)) = Ω = 7.4
    """
    try:
        C_solution = brentq(lambda c: get_lambda_max(c) - target_omega, C_range[0], C_range[1])
        return C_solution
    except ValueError:
        return None

if __name__ == '__main__':
    TARGET_OMEGA = constants.OMEGA  # 5.287234 (derived)
    C_EXPECTED = constants.C        # √2/5
    
    print('=' * 60)
    print('CLOSED EQUATION MODEL - Spectral Radius Derivation')
    print('=' * 60)
    print(f'\nTarget: λ_max(L(C)) = Ω = {TARGET_OMEGA}')
    print(f'Expected C = √2/5 = {C_EXPECTED:.8f}')
    
    # Build Laplacian with expected C and verify closure
    print('\n--- Verifying Laplacian Closure with Expected C ---')
    L_expected, w_expected = build_calibrated_laplacian(C_EXPECTED)
    closure = verify_closure(L_expected)
    
    print(f'  Row sum error: {closure["row_sum_error"]:.2e}')
    print(f'  Symmetry error: {closure["symmetry_error"]:.2e}')
    print(f'  Min eigenvalue: {closure["min_eigenvalue"]:.6f}')
    print(f'  Max eigenvalue: {closure["max_eigenvalue"]:.6f}')
    print(f'  Is closed: {closure["is_closed"]}')
    
    # Derive C from spectral radius
    print('\n--- Deriving C from Spectral Radius Condition ---')
    C_derived = derive_C_from_spectral_radius(TARGET_OMEGA)
    
    if C_derived is not None:
        print(f'  Derived C: {C_derived:.8f}')
        print(f'  Expected C: {C_EXPECTED:.8f}')
        error = abs(C_derived - C_EXPECTED)
        print(f'  Absolute error: {error:.2e}')
        relative_error = error / C_EXPECTED * 100
        print(f'  Relative error: {relative_error:.4f}%')
        
        # Verify the derived C
        lambda_max_derived = get_lambda_max(C_derived)
        print(f'\n  λ_max(L(C_derived)) = {lambda_max_derived:.6f}')
        print(f'  Target Ω = {TARGET_OMEGA}')
        
        if error < 0.01:  # 1% tolerance
            print('\n[SUCCESS] Model is self-consistent.')
            print('C is derivable from K8 graph topology + calibrated constants.')
        else:
            print('\n[PARTIAL] Derived C differs from expected.')
            print('Calibration constants may need adjustment.')
    else:
        print('\n[ERROR] Could not find solution in range [0.1, 0.6].')
        
        # Diagnostic: scan λ_max over C range
        print('\nDiagnostic scan:')
        for c in np.linspace(0.1, 0.5, 9):
            lam = get_lambda_max(c)
            print(f'  C = {c:.2f}: λ_max = {lam:.4f}')
    
    # Show calibrated constants used
    print('\n--- Calibrated Constants Used ---')
    print(f'  κ_H2 (anchor): {constants.KAPPA_H2}')
    print(f'  κ_H3 (void): {constants.KAPPA_H3}')
    print(f'  κ_H4 (deep): {constants.KAPPA_H4}')
    print(f'  α (fine structure): {constants.ALPHA:.10f}')
    print(f'  φ_PB (Pegasus): {constants.PHI_PB:.6f}')
    print(f'  Renorm bridge: {constants.RENORMALIZATION_BRIDGE:.6f}')
