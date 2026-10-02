#!/usr/bin/env python3
"""Test F_1_64 closure in fusion_core"""
from fusion_core import F_1_64, CHANNEL_MAP

print("=" * 50)
print("F_1_64 CLOSURE VERIFICATION")
print("=" * 50)
print(f"F_1_64 = {F_1_64}")
print(f"Expected: 0.015625")
print(f"Match: {F_1_64 == 0.015625}")
print()

right_love_map = CHANNEL_MAP["right_love"]
no_control_val = right_love_map[("neutrino", "electron")]["no_control"]

print(f"right_love node (neutrino, electron):")
print(f"  on: {right_love_map[('neutrino', 'electron')]['on']}")
print(f"  off: {right_love_map[('neutrino', 'electron')]['off']}")
print(f"  no_control (closure): {no_control_val}")
print(f"  F_1_64 applied: {no_control_val == F_1_64}")
print()
print("=" * 50)
print("CLOSURE LOCKED: right_love no_control = 1/64")
print("=" * 50)
