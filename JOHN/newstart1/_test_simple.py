#!/usr/bin/env python
"""Simple convergence test after disabling element forcing."""

from universal_decoder import UniversalDecoder, UniverseState

print("=== Convergence Test (Element Forcing Disabled) ===\n")

dec = UniversalDecoder()
s = UniverseState()

for i in range(16):
    s = dec.step(s, observer_input={'closure_controller': True, 'controller_strength': 0.6})
    led = s.closure_ledger or {}
    score = led.get('closure_score_l2', float('nan'))
    print(f"Step {i+1:2d}: score={score:.6f}")
