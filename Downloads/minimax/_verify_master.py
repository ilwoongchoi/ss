import kernel_v1 as k
import math

# Check T_DISCREPANCY closure
print('=== T_DISCREPANCY ===')
print(f'  T formula:  {k.CLOSURE_TENSION_T_FORMULA:.7f}')
print(f'  T prose:    {k.CLOSURE_TENSION_T_PROSE}')
print(f'  Discrepancy: {k.T_DISCREPANCY_PCT:.4f}%')
print(f'  CLOSED:     {k.T_DISCREPANCY_CLOSED}')

# Check master equation closure
print()
print('=== MASTER EQUATION ===')
t = k.compute_psi_static()
for kk, vv in t.items():
    if isinstance(vv, float):
        print(f'  {kk:15s} = {vv:.6f}')
print()
print(f'  Prose Psi_static = 67.77')
print(f'  Computed Psi_static = {t["Psi_static"]:.4f}')
print(f'  Discrepancy: {abs(t["Psi_static"]-67.77)/67.77*100:.3f}%')

# Check BETTI
print()
print('=== BETTI ===')
for kk, vv in k.BETTI.items():
    print(f'  {kk} = {vv}')

# Check MASTER_CONSTANTS Betti
print()
print('=== MASTER_CONSTANTS (Betti) ===')
for kk in ['beta_0', 'beta_5', 'beta_6', 'beta_7', 'beta_11', 'beta_12']:
    print(f'  {kk} = {k.MASTER_CONSTANTS[kk]}')
