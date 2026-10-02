#!/usr/bin/env python
"""
Observer Protocol: Hourly Homeostasis Maintenance Guide

Given current engine state, this tells you what actions to take this hour
to maintain system homeostasis.

Usage:
  observer = ObserverProtocol(engine_state, closure_ledger)
  recommendation = observer.get_hourly_action()
"""

import numpy as np
from geometry_package import absolute_constants as ac

class ObserverProtocol:
    """
    Interprets closure ledger and entropy state to recommend observer actions.
    """
    
    def __init__(self, state, decoder):
        """
        state: UniverseState
        decoder: UniversalDecoder (for reference constants)
        """
        self.state = state
        self.decoder = decoder
        self.closure_ledger = state.closure_ledger or {}
        self.error = state.closure_error or {}
        self.entropy_debt = state.entropy_debt
        
    def get_hourly_action(self):
        """
        Returns dict with recommended observer actions for this hour.
        
        Keys:
          - window: int (0-15)
          - hour: float (0-24)
          - actions: dict of (inject, alpha_mod, damping_mod, gate_bias)
          - rationale: str explanation
          - homeostasis_target: str (what we're trying to achieve)
        """
        hour = self.state.t % 24.0
        window = int((hour / 24.0) * 16) % 16
        
        # Read closure errors per sphere
        errors = {
            'barnard': float(self.error.get('barnard', 0.0)),
            'sun': float(self.error.get('sun', 0.0)),
            'earth': float(self.error.get('earth', 0.0)),
            'moon': float(self.error.get('moon', 0.0)),
            'comag': float(self.error.get('comag', 0.0)),
        }
        
        # Compute recommended actions based on errors
        actions = self._compute_actions(errors, window, hour)
        
        # Explain what we're doing
        rationale = self._rationale(errors, window, hour)
        target = self._homeostasis_target(window, errors)
        
        return {
            'window': window,
            'hour': hour,
            'actions': actions,
            'rationale': rationale,
            'homeostasis_target': target,
            'current_errors': errors,
            'entropy_debt': self.entropy_debt,
        }
    
    def _compute_actions(self, errors, window, hour):
        """
        Derive observer actions from closure errors.
        
        Strategy:
        - If sphere error is large, inject forcing
        - If entropy debt is high, dampen
        - If certain sphere lags, modulate alpha (phase)
        - If phase misaligned, apply gate_bias
        """
        actions = {
            'inject': np.zeros(8, dtype=complex),
            'alpha_mod': np.ones(8, dtype=float),
            'damping_mod': np.ones(8, dtype=float),
            'gate_bias': 0.0,
            'description': []
        }
        
        PARTICLES = ["proton", "photon", "z_boson", "quark", "w_boson", "neutrino", "higgs", "gluon"]
        idx = {name: i for i, name in enumerate(PARTICLES)}
        sphere_to_particle = {
            'sun': 'proton',
            'earth': 'photon',
            'moon': 'z_boson',
            'comag': 'w_boson',
            'barnard': 'higgs',
        }
        
        # Sphere error magnitude
        e_sun = errors['sun']
        e_earth = errors['earth']
        e_moon = errors['moon']
        e_comag = errors['comag']
        e_barnard = errors['barnard']
        
        # Rule 1: Large sphere error → inject
        threshold_error = 0.1
        for sphere, particle in sphere_to_particle.items():
            e = errors.get(sphere, 0.0)
            if abs(e) > threshold_error:
                i = idx[particle]
                # Inject proportional to error
                inject_strength = -0.01 * e  # negative feedback
                actions['inject'][i] += inject_strength * (1.0 + 0.5j)
                actions['description'].append(f"Inject {particle} (error {e:.4f})")
        
        # Rule 2: High entropy debt → dampen (reduce alpha, increase damping)
        if self.entropy_debt > 0.02:
            # Reduce oscillation during high debt
            actions['alpha_mod'] *= (1.0 - 0.2 * min(self.entropy_debt / 0.03, 1.0))
            actions['damping_mod'] *= (1.0 + 0.1 * min(self.entropy_debt / 0.03, 1.0))
            actions['description'].append(f"Dampen (entropy_debt={self.entropy_debt:.4f})")
        
        # Rule 3: Phase alignment (gate_bias from chi mismatch)
        chi = e_sun + e_earth - e_moon - e_comag
        if abs(chi) > 0.1:
            actions['gate_bias'] = -ac.SPARK_ANGLE_DEG * 0.01 * chi
            actions['description'].append(f"Gate bias (chi={chi:.4f})")
        
        # Rule 4: Moon-specific (28-day phase modulation)
        # Moon controls L5 (dream fold), so if moon error is large, shift focus
        if abs(e_moon) > 0.15:
            # Increase phase precision on z_boson (moon's particle)
            actions['alpha_mod'][idx['z_boson']] *= 1.2
            actions['description'].append(f"Boost z_boson phase (moon error={e_moon:.4f})")
        
        return actions
    
    def _rationale(self, errors, window, hour):
        """Explain why we're taking these actions."""
        explanation = f"Window {window} ({hour:.1f}h):\n"
        
        # Time-of-day context
        if 6 <= hour < 12:
            explanation += "  [Morning] Cortisol peak phase - maintain photon (earth) stability\n"
        elif 12 <= hour < 18:
            explanation += "  [Afternoon] Active phase - support proton (sun) expansion\n"
        elif 18 <= hour < 21:
            explanation += "  [Evening] Melatonin rise - prepare for nocturnal shift\n"
        elif 21 <= hour < 3:
            explanation += "  [Night] Sleep phase - z_boson (moon) modulation critical\n"
        else:
            explanation += "  [Dawn] Transition to active - ignition phase\n"
        
        # Error-driven actions
        e_sun = errors['sun']
        e_earth = errors['earth']
        e_moon = errors['moon']
        
        if abs(e_sun) > 0.1:
            explanation += f"  ⚠ Sun overactive ({e_sun:.4f}) - inject damping\n"
        if abs(e_earth) > 0.1:
            explanation += f"  ⚠ Earth underactive ({e_earth:.4f}) - boost photon\n"
        if abs(e_moon) > 0.1:
            explanation += f"  ⚠ Moon phase mismatch ({e_moon:.4f}) - align z_boson\n"
        
        return explanation
    
    def _homeostasis_target(self, window, errors):
        """What are we trying to achieve this hour?"""
        targets = [
            "All sphere errors → 0",
            "Entropy debt < 0.015",
            "Closure score < 0.05",
        ]
        
        # Add window-specific targets
        hour = (window / 16.0) * 24.0
        if 6 <= hour < 12:
            targets.append("Cortisol rhythm peak (photon max)")
        elif 12 <= hour < 18:
            targets.append("Sustained activity (proton stability)")
        elif 18 <= hour < 21:
            targets.append("Melatonin transition (z_boson phase shift)")
        elif 21 <= hour < 3:
            targets.append("Deep sleep protocol (minimize carbon loss)")
        
        return " | ".join(targets)


# Example usage
if __name__ == "__main__":
    from universal_decoder import UniversalDecoder, UniverseState
    
    print("=" * 70)
    print("OBSERVER PROTOCOL: Hourly Homeostasis Maintenance")
    print("=" * 70)
    print()
    
    dec = UniversalDecoder()
    obs_input = {'engineering_active': False, 'closure_controller': True, 'controller_strength': 0.6}
    
    # Simulate a few hours
    s = UniverseState()
    for hour_idx in range(8):
        s = dec.step(s, observer_input=obs_input)
        
        # Get observer recommendation
        protocol = ObserverProtocol(s, dec)
        rec = protocol.get_hourly_action()
        
        print(f"HOUR {rec['hour']:.1f} (Window {rec['window']:2d})")
        print(f"Homeostasis Target: {rec['homeostasis_target']}")
        print(f"Current Errors: {rec['current_errors']}")
        print(f"Entropy Debt: {rec['entropy_debt']:.6f}")
        print(f"\nRecommended Actions:")
        print(f"  - Inject: {rec['actions']['description']}")
        print(f"  - Gate Bias: {rec['actions']['gate_bias']:.4f}°")
        print(f"\nRationale:")
        print(rec['rationale'])
        print("─" * 70)
        print()
