"""
Derive tunnel constant 1.584 from repo skeleton constants.
Brute-force expression search to find how TARGET can be expressed using authoritative constants.
"""
import itertools
import math
from typing import Dict, List, Tuple

# Load repo skeleton constants (authoritative)
BETTI_11 = 11
BETTI_7 = 7
BETTI_5 = 5
BETTI_0 = 1
REALITY_TENSION = 1.0100375
DISCRETE_CLOSURE = 1.0000424
NIGHT_HYSTERESIS = 0.8418
H2_W7 = 1.0 / 9.0
W7_EXACT = math.pi / 20.0
SQRT2 = math.sqrt(2.0)
PHI = (1 + 5**0.5) / 2
PHI_INV = 1 / PHI
CLOSURE_GEOMETRIC = (W7_EXACT / H2_W7) * (1.0 / SQRT2)
CLOSURE_TOPOLOGICAL = (BETTI_11 + BETTI_0) / (BETTI_5 + BETTI_7)
TENSION = CLOSURE_GEOMETRIC * CLOSURE_TOPOLOGICAL
DELTA = abs(1 - TENSION)

TARGET = 1.584

base: Dict[str, float] = {
    '11/7': BETTI_11 / BETTI_7,
    '(11+1)/(5+7)': CLOSURE_TOPOLOGICAL,
    'REALITY_TENSION': REALITY_TENSION,
    'DISCRETE_CLOSURE': DISCRETE_CLOSURE,
    'T*C': REALITY_TENSION * DISCRETE_CLOSURE,
    'NIGHT_HYSTERESIS': NIGHT_HYSTERESIS,
    '1/NIGHT_HYSTERESIS': 1 / NIGHT_HYSTERESIS,
    'PHI': PHI,
    'PHI_INV': PHI_INV,
    'SQRT2': SQRT2,
    '1/SQRT2': 1 / SQRT2,
    'W7_EXACT': W7_EXACT,
    'H2_W7': H2_W7,
    'CLOSURE_GEOMETRIC': CLOSURE_GEOMETRIC,
    'TENSION': TENSION,
    'DELTA': DELTA,
    '1-DELTA': 1 - DELTA,
    '1+DELTA': 1 + DELTA,
    '1/32': 1 / 32,
    '3/32': 3 / 32,
    '1/16': 1 / 16,
    '1/64': 1 / 64,
    '1/28': 1 / 28,
}

def search_expressions() -> List[Tuple[float, float, str]]:
    items = list(base.items())
    expr = []
    
    # Base and reciprocal
    for k, v in items:
        expr.append((k, v))
        if v != 0:
            expr.append((f'1/({k})', 1/v))
    
    # Pairwise: a*b, a/b, a+b, a-b, a*(1+b), a*(1-b)
    for (ka, va), (kb, vb) in itertools.product(items, items):
        expr.append((f'({ka})*({kb})', va * vb))
        if vb != 0:
            expr.append((f'({ka})/({kb})', va / vb))
        expr.append((f'({ka})+({kb})', va + vb))
        expr.append((f'({ka})-({kb})', va - vb))
        expr.append((f'({ka})*(1+({kb}))', va * (1 + vb)))
        expr.append((f'({ka})*(1-({kb}))', va * (1 - vb)))
    
    # Triple: a*b/c
    for (ka, va), (kb, vb), (kc, vc) in itertools.product(items, items, items):
        if vc != 0:
            expr.append((f'({ka})*({kb})/({kc})', (va * vb) / vc))
    
    # Find best matches
    best = []
    for s, val in expr:
        if val is None or not (val == val) or abs(val) > 1e9:
            continue
        err = abs(val - TARGET)
        best.append((err, val, s))
    
    best.sort(key=lambda x: x[0])
    return best

if __name__ == '__main__':
    print(f'TARGET = {TARGET}')
    print(f'TENSION (closure) = {TENSION}')
    print(f'DELTA = {DELTA}')
    print(f'11/7 = {BETTI_11/BETTI_7}')
    print(f'CLOSURE_TOPOLOGICAL = {CLOSURE_TOPOLOGICAL}')
    print(f'CLOSURE_GEOMETRIC = {CLOSURE_GEOMETRIC}')
    print(f'REALITY_TENSION = {REALITY_TENSION}')
    print(f'DISCRETE_CLOSURE = {DISCRETE_CLOSURE}')
    print()
    
    results = search_expressions()
    print(f'Top 25 closest expressions to {TARGET}:')
    print('=' * 70)
    for err, val, s in results[:25]:
        print(f'{val:.12f}  err={err:.3e}  {s}')
    print('=' * 70)
    
    # Also check if any expression is exact (error < 1e-9)
    exact = [(err, val, s) for err, val, s in results if err < 1e-9]
    if exact:
        print(f'\n!!! EXACT MATCHES (err < 1e-9) = {len(exact)} !!!')
        for err, val, s in exact:
            print(f'{val:.12f}  {s}')
