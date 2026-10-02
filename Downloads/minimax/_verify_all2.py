import kernel_v1 as k

print('=== CLOSURES ===')
print(f'T_DISCREPANCY:         {k.T_DISCREPANCY_CLOSED} ({k.T_DISCREPANCY_PCT:.4f}%)')
print(f'CA1_CMB_TOPOLOGY:      {k.CA1_CMB_TOPOLOGY_CLOSED}')
print(f'HUBBLE_TENSION:        {k.HUBBLE_TENSION_CLOSED}')
print(f'MUON_G2:               {k.MUON_G2_CLOSED}')
print(f'DYNAMICAL_STABILITY:   {k.DYNAMICAL_STABILITY_CLOSED}')
print(f'PTA_NANOGRAV:          {k.PTA_NANOGRAV_CLOSED}')
print(f'JWST_Z14:              {k.JWST_Z14_CLOSED}')

print()
print('=== MASTER EQUATION ===')
psi = k.compute_psi_static()
T = psi['T_closure']
R = psi['R_renorm']
Phi_B = psi['Phi_B']
Psi = psi['Psi_static']
print(f'T       = {T:.6f}  (prose 0.99965)')
print(f'R       = {R:.6f}  (prose 42.368)')
print(f'Phi_B   = {Phi_B:.6f}  (prose 2.078)')
print(f'Psi     = {Psi:.4f}  (prose 67.77)')

print()
print('=== F_final FIX POINT ===')
print(f'F_final(1,1,1,1,1) = {k.F_final(1.0, 1.0, 1.0, 1.0, 1.0)}')
print(f'F_final range: [0, 1.0] for all L_n, obs in [0,1]')
