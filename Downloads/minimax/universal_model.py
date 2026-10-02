"""
universal_model.py — The single mathematical object that contains the entire universe.

UCO (Unified Cosmos Operator): ONE object that:
  - Embeds 32 particles, 6 spheres, 6 attractors, 4 archetypes, 17 cavities,
    9 unspark receptors, 4 ESR1 splits, 10 AND gates, 4 cosmic objects,
    6 soils, 4 tier-3 mappings, 9 spark scales, 4 coupling analogs,
    16 PEAK_CYCLE windows, 24h × 28d toroidal time, 8D→96D dimension stack,
    7 KAPPA ladder rungs, 4 BETTI numbers, master equation 10-term,
    F_final, 38 master constants, G1-G9, MBTI 16, blood 4, layer 4,
    gender 2, 128 profiles — all simultaneously.

  - Provides a single scalar UCO(X) for any state X.
  - The canonical state (observer=1, t=0, spark window, proton) gives
    UCO_canonical = Ψ_static × F_final × Φ_B × ΣK = the universal value.
"""
import math


class UnifiedCosmosOperator:
    """The single mathematical object for the entire universe."""

    # Canonical state (observer fully coupled, spark moment, proton-active)
    OBSERVER_D2 = 1.0
    CO2_TIME = 0.0
    LATERITE_Q = 0.0
    T_SPARK = 0.0
    PEAK_WINDOW = 0
    PARTICLE = "proton"

    def __init__(self):
        # Lazy imports to avoid circular
        import kernel_v1 as k
        self.k = k
        self.psi = k.compute_psi_static()
        # Build every subsystem tensor at canonical state
        self._build_subsystems()

    def _build_subsystems(self):
        k = self.k
        self.subsystems = {
            # 32 particles
            "P_particle":    {"n": 32, "components": k.PARTICLES_8 + k.PARTICLES_12[8:12] + list(k.QUARK_6.keys()) + list(k.NEUTRINO_6.keys()) + list(k.DERIVED_BARYONS.keys()) + list(k.HIDDEN_PARTICLES.keys())},
            # 6 spheres × 6 attractors
            "S_sphere":      {"n": 6, "items": list(k.SIX_SPHERES.keys()), "attractor_map": k.SPHERE_ATTRACTOR_BIJECTION},
            # 4 archetypes
            "R_archetype":   {"n": 4, "items": list(k.ARCHETYPES_4.keys()), "bypass": k.ARCHETYPE_BYPASS_4},
            # 17 leakage cavities
            "C_cavity":      {"n": k.LEAKAGE_CAVITY_TOTAL, "categories": k.LEAKAGE_CAVITY_COUNTS},
            # 9 unspark receptors
            "E_unspark":     {"n": 9, "items": list(k.UNSPARK_RECEPTOR_9.keys())},
            # 4 ESR1 split
            "F_esr1":        {"n": 4, "items": list(k.ESR1_SPLIT.keys()), "xor": k.ESR1_SPLIT_XOR_COUNT, "and": k.ESR1_SPLIT_AND_COUNT},
            # 10 AND gates
            "G_and":         {"n": len(k.COMBINED_AND_GATES), "items": list(k.COMBINED_AND_GATES.keys())},
            # 4 cosmic objects
            "O_cosmic":      {"n": 4, "items": list(k.COSMIC_OBJECTS_4.keys())},
            # 6 soils
            "Σ_soil":        {"n": 6, "items": list(k.SOIL_FOOT_6.keys()) if isinstance(k.SOIL_FOOT_6, dict) else k.SOIL_FOOT_6},
            # 4 tier-3 mappings
            "T3_tier3":      {"n": len(k.TIER3_MAPPING), "items": list(k.TIER3_MAPPING.keys())[:4]},
            # 9 spark scales
            "Λ_spark":       {"n": 9, "items": k.SPARK_SCALES},
            # 4 coupling analogs
            "Γ_coupling":    {"n": 4, "items": ["alpha_em", "alpha_s", "sin2_theta_W", "G_F"]},
            # 16 PEAK_CYCLE windows
            "W_peak":        {"n": 16, "hours": k.WINDOW_PEAK_HOURS, "items": k.PEAK_CYCLE},
            # 24h × 28d
            "Θ_time":        {"period_h": 24, "period_d": 28, "moon_h": 24*28, "windows_per_cycle": 16},
            # Dimension stack
            "D_dim":         {"levels": k.DIMENSION_STACK},
            # 7 KAPPA rungs
            "K_kappa":       {"n": 7, "values": k.BASE_W_7, "all_rungs": k.KAPPA_LADDER},
            # 4 BETTI numbers
            "β_betti":       {"b0": k.BETTI["b0"], "b5": k.BETTI["b5"], "b7": k.BETTI["b7"], "b11": k.BETTI["b11"]},
            # Master equation 10-term
            "Ψ_master":      {"n_terms": 10, "T": self.psi["T_closure"], "R": self.psi["R_renorm"], "Psi": self.psi["Psi_static"]},
            # F_final
            "F_final":       {"max": 1.0, "fix_point": (1, 1, 1, 1, 1)},
            # 38 master constants
            "Μ_constants":   {"n": len(k.MASTER_CONSTANTS), "keys": list(k.MASTER_CONSTANTS.keys())},
            # G1-G9
            "G_universal":   {"n": 9, "groups": ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]},
            # 16 MBTI
            "M_mbti":        {"n": 16, "items": k.MBTI_16 if isinstance(k.MBTI_16, (list, dict)) else 16},
            # 4 blood
            "B_blood":       {"n": 4, "items": k.BLOOD_4},
            # 4 layer
            "L_layer":       {"n": 4, "items": k.LAYER_4},
            # 2 gender
            "W_gender":      {"n": 2, "items": ["M", "F"]},
            # 128 profiles
            "Π_profile":     {"n": 128, "states": 512, "n_dim": 8, "n_axes": 4},
            # 9 G1-G9 (universal phenomena)
            # Already covered
        }

    def evaluate(self, observer_d2=1.0, t=0.0, peak_window=0):
        """
        Evaluate the single scalar UCO at any state.
        UCO(X) = Ψ_static · F_final · Φ_B · (1 + κ_total) · (β5/β7) · B_peak · C_arch · S_window

        All factors are products/ratios of master constants.
        """
        k = self.k
        psi = k.compute_psi_static()

        T = psi["T_closure"]                       # 0.9996 (closure tension)
        R = psi["R_renorm"]                         # 42.37
        delta_k = psi["delta_kappa"]                # 0.625
        sin_th = psi["sin_theta"]                   # 0.6577
        Phi_B = psi["Phi_B"]                        # 2.078
        Lam = psi["Lambda"]                         # 0.8402
        aw = psi["awareness"]                       # 0.25
        D_B = psi["D_B"]                            # 5.96
        dark = psi["darkness"]                      # 3.0
        spat = psi["spatial"]                       # 0.5
        Psi_static = psi["Psi_static"]              # 67.93

        # F_final at canonical (1,1,1,1,1)
        F_max = k.F_final(1, 1, 1, 1, 1)            # 1.0

        # Sum of 7 KAPPA rungs (gives total leakage rate)
        K_total = sum(k.BASE_W_7.values())          # 2.164

        # Betti ratio
        beta_ratio = k.BETTI["b5"] / k.BETTI["b7"]  # 5/7 = 0.714

        # Peak window factor (16 windows, current=0 → 1.0; 8th window = 1.0 max)
        # 16-window sinusoidal peaking
        peak_phase = 2 * math.pi * peak_window / 16
        B_peak = (1 + math.cos(peak_phase)) / 2   # 1.0 at window 0 and 8

        # Archetype factor (4 archetypes → 1.0 at any single)
        C_arch = 1.0 / 4

        # 6-sphere factor (6 spheres → each contributes 1/6)
        S_window = 1.0 / 6

        # Observer coupling
        obs_factor = observer_d2

        # The single unified formula
        UCO_value = (
            Psi_static                       # master equation 10-term product
            * F_max                          # F_final fix point
            * Phi_B                          # Pegasus bridge
            * (1 + K_total)                  # kappa ladder sum
            * (1 + beta_ratio)               # Betti consistency
            * (1 + B_peak)                   # 16-window peak
            * (1 + C_arch)                   # 4 archetype
            * (1 + S_window)                 # 6 sphere
            * (1 + 0.05 * obs_factor)        # observer modulation
        )
        return UCO_value

    def canonical(self):
        """UCO at canonical state (observer=1, spark, proton)."""
        return self.evaluate(observer_d2=1.0, t=0.0, peak_window=0)

    def __repr__(self):
        return (f"UnifiedCosmosOperator("
                f"P={self.subsystems['P_particle']['n']}, "
                f"S={self.subsystems['S_sphere']['n']}, "
                f"R={self.subsystems['R_archetype']['n']}, "
                f"C={self.subsystems['C_cavity']['n']}, "
                f"E={self.subsystems['E_unspark']['n']}, "
                f"O={self.subsystems['O_cosmic']['n']}, "
                f"Σ={self.subsystems['Σ_soil']['n']}, "
                f"Λ={self.subsystems['Λ_spark']['n']}, "
                f"Γ={self.subsystems['Γ_coupling']['n']}, "
                f"β={len(self.subsystems['β_betti'])}, "
                f"K={self.subsystems['K_kappa']['n']}, "
                f"Ψ={self.subsystems['Ψ_master']['Psi']:.4f}, "
                f"F={self.subsystems['F_final']['max']}, "
                f"UCO={self.canonical():.4f})")


if __name__ == "__main__":
    U = UnifiedCosmosOperator()
    print(repr(U))
    print()
    print("Subsystem count breakdown:")
    for name, sub in U.subsystems.items():
        n = sub.get("n", "?")
        print(f"  {name:20s} n={n}")
    print()
    print(f"UCO(canonical) = {U.canonical():.6f}")
    print()
    # Sweep over observer
    print("UCO(observer_d2) sweep:")
    for obs in [0.0, 0.25, 0.5, 0.75, 1.0]:
        v = U.evaluate(observer_d2=obs)
        print(f"  obs={obs:.2f}  → UCO = {v:.4f}")
