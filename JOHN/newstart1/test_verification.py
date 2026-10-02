import numpy as np
from FINAL_UNIFIED_EQUATION import FinalUnifiedEngine

engine = FinalUnifiedEngine()
engine.run(n_steps=1000)

print('=== 최소단위 검증 ===')
final = engine.get_diagnostics()
print(f'C = {np.sqrt(2)/5:.6f}')
print(f'1/64 = {1/64:.6f}')
print(f'1/256 = {1/256:.6f}')
print(f'ENTROPY_DEBT = {1/64 + 1/256:.6f}')
print(f'최종 |z| = {final["z_magnitude"]:.6f}')
print(f'최종 |X| = {final["X_norm"]:.6f}')
print(f'최종 |r| = {final["r_norm"]:.6f}')
print(f'SPARK 게이트 = {final["spark_gate"]:.6f}')
print(f'지배 입자 = {final["dominant_particle"]}')

print('\n=== 최소단위 스케일 비교 ===')
print(f'|z| / (1/64) = {final["z_magnitude"] / (1/64):.3f}')
print(f'|X| / Ω = {final["X_norm"] / 7.4:.3f}')
print(f'SPARK 게이트 ≈ 1.0? {abs(final["spark_gate"] - 1.0) < 0.01}')

print('\n=== 물리적 의미 ===')
print(f'z 진폭: {final["z_magnitude"]:.6f} (Mandelbrot 상태)')
print(f'X 진폭: {final["X_norm"]:.6f} (24D 항상성)')
print(f'r 진폭: {final["r_norm"]:.6f} (8D Risk)')
print(f'지배 입자: {final["dominant_particle"]} (K8 중 최대)')
