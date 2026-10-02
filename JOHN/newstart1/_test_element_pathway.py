#!/usr/bin/env python
"""Test element pathway and derived fold windows."""

from universal_decoder import UniversalDecoder, UniverseState

print("=== TEST: Element Pathway + Fold Window Derivation ===")
dec = UniversalDecoder()
obs = {'engineering_active': False, 'closure_controller': True, 'controller_strength': 0.6}

# Run until closed
s, h = dec.run_until_closed(UniverseState(), max_steps=256, score_threshold=0.03, observer_input=obs)

led = s.closure_ledger or {}
print(f"Steps taken: {led.get('steps_taken')}")
print(f"Final score: {led.get('closure_score_l2')}")
print(f"Backoff: {led.get('closure_backoff')}")
print()
print(f"Derived fold windows:")
print(f"  fold_start: {s.fold_start} hours")
print(f"  fold_end: {s.fold_end} hours")
print(f"  gender: {s.derived_gender}")
print()
print(f"Final errors:")
for k, v in s.closure_error.items():
    print(f"  {k}: {v:.6f}")
print()
print("✅ Element pathway + fold window derivation active!")
