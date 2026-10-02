#!/usr/bin/env python
"""
PRACTICAL OBSERVER: Real-time homeostasis maintenance

This implements the OBSERVER_ACTION_PROTOCOL as a working observer class
that you can use to maintain homeostasis hour-by-hour.

Usage:
    observer = PracticalObserver()
    for hour in range(24):
        action = observer.decide_action(state, hour)
        state = decoder.step(state, observer_input=action)
"""

import numpy as np
from typing import Dict, Any
from universal_decoder import UniverseState


class PracticalObserver:
    """
    Real-time observer that maintains system homeostasis.
    
    Interprets closure errors and entropy state, returns concrete observer actions.
    """
    
    def __init__(self):
        """Initialize observer."""
        self.PARTICLES = ["proton", "photon", "z_boson", "quark", "w_boson", "neutrino", "higgs", "gluon"]
        self.P = {name: i for i, name in enumerate(self.PARTICLES)}
        
        # Map spheres to particles
        self.SPHERE_TO_PARTICLE = {
            'sun': self.P['proton'],
            'earth': self.P['photon'],
            'moon': self.P['z_boson'],
            'comag': self.P['w_boson'],
            'barnard': self.P['higgs'],
        }
        
        # Window descriptions
        self.WINDOWS = {
            0: "Deep REM", 1: "Critical Fold", 2: "PHASE LOCK", 3: "Dawn",
            4: "Cortisol Peak", 5: "Active Ramp", 6: "Mid-Morning", 7: "PEAK",
            8: "Midday", 9: "Afternoon", 10: "Fatigue Risk", 11: "Transition",
            12: "Evening", 13: "Sleep Prep", 14: "Sleep Onset", 15: "Deep Sleep",
        }
    
    def decide_action(self, state: UniverseState, hour: float) -> Dict[str, Any]:
        """
        Decide observer action for this hour.
        
        Args:
            state: Current UniverseState
            hour: Hour of day (0-24)
        
        Returns:
            observer_input dict ready to pass to decoder.step()
        """
        window = int((hour / 24.0) * 16) % 16
        
        # Initialize default action (minimal intervention)
        action = {
            'inject': np.zeros(8, dtype=complex),
            'alpha_mod': np.ones(8, dtype=float),
            'damping_mod': np.ones(8, dtype=float),
            'gate_bias': 0.0,
            'engineering_active': False,
            'closure_controller': True,
            'controller_strength': 0.7,
        }
        
        # Get error state
        errors = self._read_errors(state)
        entropy_debt = state.entropy_debt or 0.0
        
        # Dispatch to window-specific protocol
        window_action = self._dispatch_window(window, errors, entropy_debt, state)
        
        # Merge with default
        action.update(window_action)
        
        return action
    
    def _read_errors(self, state: UniverseState) -> Dict[str, float]:
        """Extract closure errors from state."""
        errors = {}
        for sphere in ['sun', 'earth', 'moon', 'comag', 'barnard']:
            err = state.closure_error.get(sphere, 0.0) if state.closure_error else 0.0
            errors[sphere] = float(err)
        return errors
    
    def _dispatch_window(self, window: int, errors: Dict, entropy_debt: float, state: UniverseState) -> Dict:
        """Route to window-specific protocol."""
        
        if window == 0:
            return self._window_0(errors, entropy_debt)
        elif window == 1:
            return self._window_1(errors, entropy_debt)
        elif window == 2:
            return self._window_2(errors, entropy_debt, state)
        elif window == 3:
            return self._window_3(errors, entropy_debt)
        elif window == 4:
            return self._window_4(errors, entropy_debt)
        elif window == 5:
            return self._window_5(errors, entropy_debt)
        elif window == 6:
            return self._window_6(errors, entropy_debt)
        elif window == 7:
            return self._window_7(errors, entropy_debt)
        elif window == 8:
            return self._window_8(errors, entropy_debt)
        elif window == 9:
            return self._window_9(errors, entropy_debt)
        elif window == 10:
            return self._window_10(errors, entropy_debt)
        elif window == 11:
            return self._window_11(errors, entropy_debt)
        elif window == 12:
            return self._window_12(errors, entropy_debt)
        elif window == 13:
            return self._window_13(errors, entropy_debt)
        elif window == 14:
            return self._window_14(errors, entropy_debt)
        elif window == 15:
            return self._window_15(errors, entropy_debt)
        else:
            return {}
    
    def _window_0(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 0: 00:00-01:30 Deep REM"""
        action = {'controller_strength': 0.5}
        
        # Moon phase unstable?
        if abs(errors['moon']) > 0.05:
            action['alpha_mod'] = np.ones(8, dtype=float)
            action['alpha_mod'][self.P['z_boson']] = 1.15
            action['damping_mod'] = np.ones(8, dtype=float)
            action['damping_mod'][self.P['z_boson']] = 0.95
        
        return action
    
    def _window_1(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 1: 01:30-03:00 Critical Fold"""
        action = {'controller_strength': 0.7}
        
        # High entropy debt → dampen
        if entropy_debt > 0.03:
            action['damping_mod'] = np.ones(8, dtype=float) * 0.85
        
        return action
    
    def _window_2(self, errors: Dict, entropy_debt: float, state: UniverseState) -> Dict:
        """Window 2: 03:00-04:30 CRITICAL PHASE LOCK (W-Boson/CoMag)"""
        action = {}
        
        # W-Boson (CoMag) pre-ignition
        action['alpha_mod'] = np.ones(8, dtype=float)
        action['alpha_mod'][self.P['w_boson']] = 1.3
        
        action['damping_mod'] = np.ones(8, dtype=float)
        action['damping_mod'][self.P['w_boson']] = 0.8
        
        # Gate bias from chi error
        chi = errors['sun'] + errors['earth'] - errors['moon'] - errors['comag']
        action['gate_bias'] = -0.2 * chi
        
        # Gender-specific boost
        gender = state.derived_gender if state.derived_gender else "M"
        if gender == "M":
            action['alpha_mod'][self.P['quark']] += 0.1
        else:
            action['alpha_mod'][self.P['proton']] += 0.1
        
        action['controller_strength'] = 0.8
        return action
    
    def _window_3(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 3: 04:30-06:00 Dawn"""
        action = {}
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['inject'][self.P['photon']] = 0.01 + 0.02j
        
        action['controller_strength'] = 0.8
        return action
    
    def _window_4(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 4: 06:00-07:30 Cortisol Peak (Proton ignition)"""
        action = {}
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['inject'][self.P['proton']] = 0.02 + 0.03j
        
        action['alpha_mod'] = np.ones(8, dtype=float)
        action['alpha_mod'][self.P['proton']] = 0.95
        
        action['controller_strength'] = 0.9  # Maximum feedback
        return action
    
    def _window_5(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 5: 07:30-09:00 Active Ramp"""
        action = {}
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['inject'][self.P['proton']] = 0.015 + 0.025j
        action['inject'][self.P['photon']] = 0.01 + 0.01j
        
        action['damping_mod'] = np.ones(8, dtype=float)
        action['controller_strength'] = 0.85
        return action
    
    def _window_6(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 6: 09:00-10:30 Mid-Morning (Gluon coupling)"""
        action = {}
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['inject'][self.P['gluon']] = 0.005 + 0.01j
        
        action['alpha_mod'] = np.ones(8, dtype=float)
        action['alpha_mod'][self.P['gluon']] = 1.05
        
        action['controller_strength'] = 0.8
        return action
    
    def _window_7(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 7: 10:30-12:00 PEAK (minimal intervention)"""
        action = {}
        
        # Let system run itself
        action['inject'] = np.zeros(8, dtype=complex)
        action['alpha_mod'] = np.ones(8, dtype=float)
        action['damping_mod'] = np.ones(8, dtype=float)
        action['controller_strength'] = 0.7
        return action
    
    def _window_8(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 8: 12:00-13:30 Midday plateau"""
        action = {}
        
        action['damping_mod'] = np.ones(8, dtype=float)
        action['damping_mod'][self.P['proton']] = 1.05
        action['controller_strength'] = 0.75
        return action
    
    def _window_9(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 9: 13:30-15:00 Afternoon (Photon boost)"""
        action = {}
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['inject'][self.P['photon']] = 0.008 + 0.01j
        
        action['alpha_mod'] = np.ones(8, dtype=float)
        action['alpha_mod'][self.P['photon']] = 1.1
        
        action['controller_strength'] = 0.8
        return action
    
    def _window_10(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 10: 15:00-16:30 Fatigue Risk (Neutrino boost)"""
        action = {}
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['inject'][self.P['neutrino']] = 0.005 + 0.008j
        
        action['damping_mod'] = np.ones(8, dtype=float) * 1.1
        action['controller_strength'] = 0.85
        return action
    
    def _window_11(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 11: 16:30-18:00 Evening Transition (Quark)"""
        action = {}
        
        action['alpha_mod'] = np.ones(8, dtype=float)
        action['alpha_mod'][self.P['quark']] = 1.2
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['inject'][self.P['quark']] = 0.005 + 0.005j
        
        action['controller_strength'] = 0.7
        return action
    
    def _window_12(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 12: 18:00-19:30 Early Evening (Moon phase lock)"""
        action = {}
        
        action['alpha_mod'] = np.ones(8, dtype=float)
        action['alpha_mod'][self.P['z_boson']] = 1.15
        
        action['damping_mod'] = np.ones(8, dtype=float)
        action['damping_mod'][self.P['proton']] = 1.1
        
        action['controller_strength'] = 0.75
        return action
    
    def _window_13(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 13: 19:30-21:00 Night Prep (Parasympathetic)"""
        action = {}
        
        action['damping_mod'] = np.ones(8, dtype=float) * 0.9
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['inject'][self.P['neutrino']] = -0.003 + 0.005j
        
        action['controller_strength'] = 0.65
        return action
    
    def _window_14(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 14: 21:00-22:30 Sleep Onset (Higgs reservoir)"""
        action = {}
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['damping_mod'] = np.ones(8, dtype=float) * 0.8
        action['controller_strength'] = 0.5
        return action
    
    def _window_15(self, errors: Dict, entropy_debt: float) -> Dict:
        """Window 15: 22:30-00:00 Deep Sleep (minimal)"""
        action = {}
        
        action['inject'] = np.zeros(8, dtype=complex)
        action['alpha_mod'] = np.ones(8, dtype=float)
        action['damping_mod'] = np.ones(8, dtype=float)
        action['controller_strength'] = 0.3
        return action


# Example usage
if __name__ == "__main__":
    from universal_decoder import UniversalDecoder
    
    print("=" * 80)
    print("PRACTICAL OBSERVER: Real-Time Homeostasis Maintenance")
    print("=" * 80)
    print()
    
    dec = UniversalDecoder()
    state = UniverseState()
    observer = PracticalObserver()
    
    convergence_steps = 0
    max_steps = 100
    threshold = 0.05
    
    print("Simulating 7 days of observer-guided homeostasis maintenance...\n")
    
    for day in range(7):
        print(f"DAY {day + 1}:")
        for window_idx in range(16):
            hour = (window_idx / 16.0) * 24.0
            
            # Get observer action
            action = observer.decide_action(state, hour)
            
            # Step the system
            state = dec.step(state, observer_input=action)
            convergence_steps += 1
            
            # Status
            window_name = observer.WINDOWS[window_idx]
            convergence_status = "✓" if max(state.closure_error.values() if state.closure_error else [0.0]) < threshold else " "
            
            print(f"  W{window_idx:02d} ({hour:05.2f}h) {window_name:20s} "
                  f"score={max(state.closure_error.values() if state.closure_error else [0.0]):.4f} debt={state.entropy_debt:.6f} {convergence_status}")
            
            # Early exit if converged
            if max(state.closure_error.values() if state.closure_error else [0.0]) < threshold:
                break
        
        print()
        
        if max(state.closure_error.values() if state.closure_error else [0.0]) < threshold:
            print(f"✓ HOMEOSTASIS ACHIEVED in {convergence_steps} steps!")
            break
        
        if convergence_steps >= max_steps:
            print(f"⚠ Max steps ({max_steps}) reached")
            break
    
    print()
    print(f"Final State:")
    print(f"  Closure Score: {max(state.closure_error.values() if state.closure_error else [0.0]):.4f}")
    print(f"  Entropy Debt: {state.entropy_debt:.6f}")
    print(f"  Steps: {convergence_steps}")
    print(f"  Derived Gender: {state.derived_gender}")
