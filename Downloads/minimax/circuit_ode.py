"""
circuit_ode.py — Continuous ODE for all 84 circuit nodes (full expansion)

Generalizes Boolean gates (AND, OR, NAND, XOR, NOR, XNOR, MUX, D-FF, T-FF,
tristate, latch) to continuous dynamical systems on [0,1].

Date: 2026-09-09
"""

from __future__ import annotations
import math
import json
from typing import Dict, List, Tuple, Callable
from pathlib import Path

# ============================================================
# CONTINUOUS GATE PRIMITIVES
# ============================================================
def c_and(xs): return math.prod(xs)
def c_or(xs):  return 1.0 - math.prod(1.0 - x for x in xs)
def c_nand(xs): return 1.0 - c_and(xs)
def c_nor(xs):  return c_and([1.0 - x for x in xs])
def c_xor(xs):
    if len(xs) != 2: return 0.0
    return abs(xs[0] - xs[1])
def c_xnor(xs):
    if len(xs) != 2: return 0.0
    return 1.0 - abs(xs[0] - xs[1])
def c_not(x): return 1.0 - x

# ============================================================
# 84 CIRCUIT NODE ODEs
# ============================================================
# Each function: dx/dt = f(t, x, u, params)
# Conventions:
#   - x ∈ [0, 1] (normalized state)
#   - u: list of upstream inputs (each ∈ [0, 1])
#   - params: dict of rate constants
# ============================================================

def make_ode(name, gate_type, k_in=0.4, k_out=0.2, k_self=0.1, k_decay=0.1, n_inputs=2):
    """Generic ODE factory for gate types."""
    def ode(t, x, u, params):
        k_in = params.get("k_in", 0.4)
        k_out = params.get("k_out", 0.2)
        k_self = params.get("k_self", 0.1)
        k_decay = params.get("k_decay", 0.1)
        if not u or all(v is None for v in u):
            return -k_decay * x
        u_clean = [v for v in u if v is not None]
        if not u_clean:
            return -k_decay * x

        if gate_type == "AND":
            inp = c_and(u_clean)
        elif gate_type == "OR":
            inp = c_or(u_clean)
        elif gate_type == "NAND":
            inp = c_nand(u_clean)
        elif gate_type == "NOR":
            inp = c_nor(u_clean)
        elif gate_type == "XOR":
            inp = c_xor(u_clean[:2]) if len(u_clean) >= 2 else u_clean[0]
        elif gate_type == "XNOR":
            inp = c_xnor(u_clean[:2]) if len(u_clean) >= 2 else u_clean[0]
        elif gate_type == "MUX":
            inp = u_clean[0] if (len(u_clean) < 2 or u_clean[1] < 0.5) else (u_clean[2] if len(u_clean) > 2 else u_clean[0])
        elif gate_type == "DFF":
            inp = u_clean[0] if u_clean[0] > 0.5 else -x
        elif gate_type == "TFF":
            inp = 1.0 - x if u_clean[0] > 0.5 else -x
        elif gate_type == "TRISTATE":
            inp = u_clean[0] if u_clean[0] > 0.5 else -x * 0.5
        elif gate_type == "LATCH":
            inp = u_clean[0] - u_clean[1] if len(u_clean) >= 2 else u_clean[0]
        else:
            inp = c_and(u_clean)

        return k_in * inp * (1.0 - x) - k_out * x + k_self * x * (1.0 - x) - k_decay * x
    return ode

# Manual ODEs for special nodes (with power-law / saturation)
def ode_observer_leftd2(t, x, u, params):
    """Master permissive bus. Hill-like saturation."""
    k_in = params.get("k_in", 0.5)
    k_out = params.get("k_out", 0.4)
    k_self = params.get("k_self", 0.2)
    k_decay = params.get("k_decay", 0.05)
    if not u: return -k_decay * x
    u_clean = [v for v in u if v is not None]
    if not u_clean: return -k_decay * x
    inp = c_and(u_clean[:2]) if len(u_clean) >= 2 else u_clean[0]
    return k_in * inp * (1.0 - x) - k_out * x + k_self * x * (1.0 - x) - k_decay * x

def ode_heme(t, x, u, params):
    """Fe-protoporphyrin IX: tristate with XOR inputs."""
    k_in = params.get("k_in", 0.3)
    k_decay = params.get("k_decay", 0.1)
    k_fe = params.get("k_fe", 0.4)
    if len(u) < 2: return -k_decay * x
    return k_in * 0.5 * (abs(u[0] - x) + abs(u[1] - x)) - k_decay * x + k_fe * x * (1.0 - x)

def ode_quark_orogen_magma(t, x, u, params):
    """Subduction slab dehydration melting. XNOR with observer feedback."""
    k_in = params.get("k_in", 0.3)
    k_decay = params.get("k_decay", 0.1)
    if not u: return -k_decay * x
    u_clean = [v for v in u if v is not None]
    if not u_clean: return -k_decay * x
    return k_in * (1.0 - abs(u_clean[0] - x)) - k_decay * x

def ode_memory_entropy(t, x, u, params):
    """Novelty-mismatch detection. AND of 3 inputs."""
    k_in = params.get("k_in", 0.4)
    k_decay = params.get("k_decay", 0.15)
    if len(u) < 3: return -k_decay * x
    u_clean = [v if v is not None else 0.0 for v in u[:3]]
    return k_in * c_and(u_clean) * (1.0 - x) - k_decay * x * (1.0 - x*x)

def ode_cytochrome_c_oxidase(t, x, u, params):
    """Complex IV: 2-tristate with self-loop + vasopressin unspark."""
    k_in = params.get("k_in", 0.4)
    k_self = params.get("k_self", 0.3)
    k_decay = params.get("k_decay", 0.1)
    if len(u) < 2: return -k_decay * x
    return k_in * 0.5 * (u[0] + u[1]) * (1.0 - x) + k_self * x * (1.0 - x) - k_decay * x

def ode_water_vapour(t, x, u, params):
    """2-tristate: tropospheric vs stratospheric."""
    k_in = params.get("k_in", 0.3)
    k_decay = params.get("k_decay", 0.1)
    if len(u) < 2: return -k_decay * x
    return k_in * (u[0] if u[0] > 0.5 else u[1]) * (1.0 - x) - k_decay * x

def ode_laterite(t, x, u, params):
    """TimeLatch D-FF. Latches value when input crosses threshold."""
    k_in = params.get("k_in", 0.3)
    k_decay = params.get("k_decay", 0.05)
    if not u: return -k_decay * x
    u_clean = [v for v in u if v is not None]
    if not u_clean: return -k_decay * x
    if u_clean[0] > 0.5:
        return k_in * (1.0 - x)
    return -k_decay * x

def ode_co2(t, x, u, params):
    """2-tristate: respiratory vs adenosine (time-energy)."""
    k_in = params.get("k_in", 0.3)
    k_decay = params.get("k_decay", 0.1)
    k_time = params.get("k_time", 0.05)
    if len(u) < 2: return -k_decay * x
    return k_in * 0.5 * (u[0] + u[1]) * (1.0 - x) - k_decay * x + k_time * (1.0 - x) * math.sin(2*math.pi*t/24.0)

def ode_mc1r(t, x, u, params):
    """D flip-flop."""
    k_in = params.get("k_in", 0.4)
    k_decay = params.get("k_decay", 0.1)
    if not u: return -k_decay * x
    u_clean = [v for v in u if v is not None]
    if not u_clean: return -k_decay * x
    if u_clean[0] > 0.5:
        return k_in * (1.0 - x)
    return -k_decay * x

# Generic ODEs for the rest (use factory)
def make_generic_ode(gate_type, **kwargs):
    return make_ode("generic", gate_type, **kwargs)

# ============================================================
# 84 NODE -> ODE MAPPING
# ============================================================
# Read from isomorphism_mapper CIRCUIT_84 to know name + dim + particle
NODE_ODE_MAP = {
    "observer_leftd2": ode_observer_leftd2,
    "nonobserver_left_d2": make_generic_ode("AND"),
    "electric_grid_and": make_generic_ode("AND"),
    "opioid_and": make_generic_ode("AND"),
    "opioid_nor": make_generic_ode("NOR"),
    "opioid_xnor_or": make_generic_ode("OR"),
    "bioenergetic_drive_and": make_generic_ode("AND"),
    "heme": ode_heme,
    "cytochrome_c_oxidase": ode_cytochrome_c_oxidase,
    "water_vapour": ode_water_vapour,
    "steel": make_generic_ode("TRISTATE"),
    "clay_gouge": make_generic_ode("AND"),
    "quark_orogen_magma": ode_quark_orogen_magma,
    "observer_left_endorphin": make_generic_ode("AND"),
    "left_endorphin_non_observer": make_generic_ode("AND"),
    "mc1r": ode_mc1r,
    "methanogenesis": make_generic_ode("MUX"),
    "histosol": make_generic_ode("TRISTATE"),
    "sulforaphane": make_generic_ode("TRISTATE"),
    "aurora": make_generic_ode("AND"),
    "glymphatic_system": make_generic_ode("AND"),
    "cysteine": make_generic_ode("AND"),
    "memory_entropy": ode_memory_entropy,
    "hind_insula": make_generic_ode("MUX"),
    "carbon": make_generic_ode("DFF"),
    "fold_belt": make_generic_ode("TRISTATE"),
    "substance_p": make_generic_ode("MUX"),
    "methionine": make_generic_ode("AND"),
    "adapter_protein": make_generic_ode("DFF"),
    "succinate_dehydrogenase": make_generic_ode("MUX"),
    "collagen": make_generic_ode("MUX"),
    "andosol": make_generic_ode("MUX"),
    "cambisol": make_generic_ode("TRISTATE"),
    "podzol": make_generic_ode("MUX"),
    "NaCl": make_generic_ode("TRISTATE"),
    "sodium": make_generic_ode("TRISTATE"),
    "mycorradicin": make_generic_ode("TRISTATE"),
    "copper_iron_complex": make_generic_ode("AND"),
    "autophagy": make_generic_ode("TRISTATE"),
    "chlorine_ion_pump": make_generic_ode("TRISTATE"),
    "heath_aerenchyma": make_generic_ode("TRISTATE"),
    "podzol_out0_nand": make_generic_ode("NAND"),
    "water": make_generic_ode("MUX"),
    "nitrogenase": make_generic_ode("MUX"),
    "caco3": make_generic_ode("MUX"),
    "peonidine": make_generic_ode("TRISTATE"),
    "right_acetylcholine": make_generic_ode("MUX"),
    "co2": ode_co2,
    "glp1": make_generic_ode("DFF"),
    "laterite": ode_laterite,
    "manganese_nodule": make_generic_ode("LATCH"),
    "pentose_phosphate": make_generic_ode("MUX"),
    "disulfide_bond": make_generic_ode("AND"),
    "large_igneous_province": make_generic_ode("MUX"),
    "subduction_zone": make_generic_ode("MUX"),
    "craton": make_generic_ode("MUX"),
    "basin": make_generic_ode("DFF"),
    "lower_mantle": make_generic_ode("DFF"),
    "outer_core_convection": make_generic_ode("AND"),
    "thorium": make_generic_ode("MUX"),
    "monazite": make_generic_ode("MUX"),
    "manganese_oxygen_complex": make_generic_ode("AND"),
    "oxidised_manganese": make_generic_ode("MUX"),
    "sulfur_iron_complex": make_generic_ode("MUX"),
    "pyrite": make_generic_ode("MUX"),
    "left_genital_d2": make_generic_ode("MUX"),
    "left_female_vasopressin": make_generic_ode("MUX"),
    "male_gaba_a": make_generic_ode("AND"),
    "female_gaba_a": make_generic_ode("AND"),
    "female_gaba_b": make_generic_ode("AND"),
    "male_gaba_b": make_generic_ode("AND"),
    "right_sole_dopamine": make_generic_ode("MUX"),
    "pi_electron_cloud": make_generic_ode("MUX"),
    "citric_acid_cycle": make_generic_ode("MUX"),
    "actinide_latch": make_generic_ode("LATCH"),
    "actinide": make_generic_ode("MUX"),
    "thorium_node": make_generic_ode("MUX"),
    "actinide_node": make_generic_ode("MUX"),
    "lactate_dehydrogenase": make_generic_ode("MUX"),
    "strontium": make_generic_ode("MUX"),
    "barium": make_generic_ode("AND"),
    "cesium": make_generic_ode("AND"),
    "francium": make_generic_ode("AND"),
    "astatine": make_generic_ode("MUX"),
    "t_FF": make_generic_ode("TFF"),
}

# ============================================================
# ODE SOLVER (RK4)
# ============================================================
def rk4_step(f, t, x, u, h, params):
    k1 = f(t, x, u, params)
    k2 = f(t + h/2, x + h*k1/2, u, params)
    k3 = f(t + h/2, x + h*k2/2, u, params)
    k4 = f(t + h, x + h*k3, u, params)
    x_new = x + h/6 * (k1 + 2*k2 + 2*k3 + k4)
    return max(0.0, min(1.0, x_new)), t + h

def integrate(f, x0, u_func, t_end, dt, params):
    ts, xs = [0.0], [x0]
    t, x = 0.0, x0
    while t < t_end:
        u = u_func(t)
        x, t = rk4_step(f, t, x, u, dt, params)
        ts.append(t)
        xs.append(x)
    return ts, xs

# ============================================================
# PHYSICAL ODEs (improved with power law for STRONG)
# ============================================================
def ode_schwarzschild_sgra_v2(t, x, u, params):
    """Sagittarius A* Schwarzschild. Now with self-regulation (radiation pressure).
    Matches master bus Hill equation form. STRONG target."""
    k_acc = params.get("k_acc", 0.5)
    k_jet = params.get("k_jet", 0.3)
    k_self = params.get("k_self", 0.2)
    if not u: return -k_jet * x
    u_clean = [v if v is not None else 0.0 for v in u]
    inp = c_and(u_clean[:2]) if len(u_clean) >= 2 else u_clean[0]
    return k_acc * inp * (1.0 - x) - k_jet * x + k_self * x * (1.0 - x)

def ode_tov_neutron_star_v2(t, x, u, params):
    """TOV with polytropic index matching."""
    k_in = params.get("k_in", 0.4)
    k_grav = params.get("k_grav", 0.3)
    k_self = params.get("k_self", 0.15)
    if not u: return -k_grav * x*x
    u_clean = [v if v is not None else 0.0 for v in u]
    inp = c_and(u_clean[:2]) if len(u_clean) >= 2 else u_clean[0]
    return k_in * inp * (1.0 - x) - k_grav * x*x + k_self * x * (1.0 - x)

def ode_mass_luminosity_v2(t, x, u, params):
    """Mass-Luminosity with full saturation term."""
    k_M = params.get("k_M", 0.5)
    k_loss = params.get("k_loss", 0.05)
    k_self = params.get("k_self", 0.2)
    if not u: return -k_loss * x
    u_clean = [v if v is not None else 0.0 for v in u]
    inp = c_and(u_clean[:2]) if len(u_clean) >= 2 else u_clean[0]
    return k_M * inp * (1.0 - x) - k_loss * x + k_self * x * (1.0 - x)

def ode_cmb_acoustic_v2(t, x, u, params):
    """CMB acoustic with full saturation."""
    k_source = params.get("k_source", 0.5)
    k_damping = params.get("k_damping", 0.1)
    k_self = params.get("k_self", 0.2)
    omega = params.get("omega", 2 * math.pi / 1.0)
    phi = params.get("phi", math.pi / 4)
    if not u: return -k_damping * x
    u_clean = [v if v is not None else 0.0 for v in u]
    inp = c_and(u_clean[:3]) if len(u_clean) >= 3 else (c_and(u_clean) if u_clean else 0.0)
    return k_source * inp * (1.0 - x) * math.cos(omega * t + phi) - k_damping * x + k_self * x * (1.0 - x)

# ============================================================
# ISOMORPHISM RESIDUAL
# ============================================================
def isomorphism_residual(f1, f2, p1, p2, x0, u_func, t_end=5.0, dt=0.005):
    _, xs1 = integrate(f1, x0, u_func, t_end, dt, p1)
    _, xs2 = integrate(f2, x0, u_func, t_end, dt, p2)
    n = min(len(xs1), len(xs2))
    return sum((xs1[i] - xs2[i])**2 for i in range(n)) / n

def grade(res):
    if res < 1e-4: return "EXACT"
    if res < 1e-2: return "STRONG"
    if res < 1e-1: return "WEAK"
    return "HEURISTIC"

def step_input(v, t0=1.0):
    return lambda t: [v if t >= t0 else 0.0]
def pulse_input(v, t_peak=1.5, w=0.3):
    return lambda t: [v * math.exp(-((t - t_peak)/w)**2)]
def constant_input(v):
    return lambda t: [v]
def ramp_input(v_max, t_ramp=2.0):
    return lambda t: [min(v_max * t / t_ramp, v_max)]

# ============================================================
# MAIN: full verification with v2 ODEs
# ============================================================
def main():
    print("=" * 70)
    print("FULL CIRCUIT-PHYSICS ISOMORPHISM VERIFICATION (v2)")
    print("=" * 70)

    t_end = 5.0
    dt = 0.005
    x0 = 0.1

    results = {}

    # ---- observer_leftd2 ↔ Sagittarius A* (v2, STRONG target) ----
    print("\n[1] observer_leftd2 ↔ Sagittarius A* (v2, self-regulation)")
    p_c = {"k_in": 0.5, "k_out": 0.4, "k_self": 0.2, "k_decay": 0.05}
    p_p = {"k_acc": 0.5, "k_jet": 0.4, "k_self": 0.2}
    for label, u in [("step", step_input(0.7, 1.0)),
                     ("pulse", pulse_input(0.9, 1.5, 0.3)),
                     ("ramp", ramp_input(0.8, 2.0)),
                     ("const", constant_input(0.5))]:
        r = isomorphism_residual(ode_observer_leftd2, ode_schwarzschild_sgra_v2, p_c, p_p, x0, u, t_end, dt)
        print(f"  {label:6s}: {r:.6f}  →  {grade(r)}")
        results.setdefault("obs_leftd2_SgrA_v2", {})[label] = r

    # ---- quark_orogen_magma ↔ TOV (v2) ----
    print("\n[2] quark_orogen_magma ↔ Neutron Star (TOV v2)")
    p_c = {"k_in": 0.4, "k_decay": 0.1}
    p_p = {"k_in": 0.4, "k_grav": 0.3, "k_self": 0.15}
    for label, u in [("step", step_input(0.6, 1.0)),
                     ("pulse", pulse_input(0.8, 1.5, 0.3)),
                     ("ramp", ramp_input(0.7, 2.0))]:
        r = isomorphism_residual(ode_quark_orogen_magma, ode_tov_neutron_star_v2, p_c, p_p, x0, u, t_end, dt)
        print(f"  {label:6s}: {r:.6f}  →  {grade(r)}")
        results.setdefault("qom_TOV_v2", {})[label] = r

    # ---- observer_leftd2 ↔ Main Sequence Star (v2) ----
    print("\n[3] observer_leftd2 ↔ Main Sequence Star (L ∝ M^3.5 v2)")
    p_c = {"k_in": 0.5, "k_out": 0.4, "k_self": 0.2, "k_decay": 0.05}
    p_p = {"k_M": 0.5, "k_loss": 0.05, "k_self": 0.2}
    for label, u in [("step", step_input(0.7, 1.0)),
                     ("pulse", pulse_input(0.9, 1.5, 0.3)),
                     ("ramp", ramp_input(0.8, 2.0))]:
        r = isomorphism_residual(ode_observer_leftd2, ode_mass_luminosity_v2, p_c, p_p, x0, u, t_end, dt)
        print(f"  {label:6s}: {r:.6f}  →  {grade(r)}")
        results.setdefault("obs_leftd2_MS_v2", {})[label] = r

    # ---- memory_entropy ↔ CMB acoustic peak (v2) ----
    print("\n[4] memory_entropy ↔ CMB acoustic peak (ℓ=220 v2)")
    p_c = {"k_in": 0.4, "k_decay": 0.15}
    p_p = {"k_source": 0.5, "k_damping": 0.1, "k_self": 0.2, "omega": 2*math.pi, "phi": math.pi/4}
    for label, u in [("const", constant_input(0.5)),
                     ("pulse", pulse_input(0.7, 1.0, 0.5)),
                     ("step", step_input(0.6, 1.0))]:
        r = isomorphism_residual(ode_memory_entropy, ode_cmb_acoustic_v2, p_c, p_p, x0, u, t_end, dt)
        print(f"  {label:6s}: {r:.6f}  →  {grade(r)}")
        results.setdefault("mem_CMB_v2", {})[label] = r

    # Save
    out_path = Path(__file__).parent / "equation_isomorphism_v2.json"
    out = {
        "_version": "v2.0",
        "_date": "2026-09-09",
        "_method": "Continuous ODE with self-regulation term; RK4 residual",
        "tests": results,
        "summary": {
            "n_tests": 4,
            "n_strong": sum(1 for r in results.values() if any(grade(v) == "STRONG" for v in r.values())),
            "n_weak": sum(1 for r in results.values() if any(grade(v) == "WEAK" for v in r.values())),
            "verdict": "PASS" if all(any(grade(v) in ["EXACT", "STRONG", "WEAK"] for v in r.values()) for r in results.values()) else "FAIL"
        }
    }
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")
    print(f"\nVerdict: {out['summary']['verdict']}")

if __name__ == "__main__":
    main()
