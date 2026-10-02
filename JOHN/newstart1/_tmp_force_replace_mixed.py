from pathlib import Path
import re

p = Path('universal_decoder.py')
t = p.read_text(encoding='utf-8-sig')

pattern = r"def _mixed_logic_circuit\(state: UniverseState, latent: dict, hour: float\) -> dict:\n(?:    .*\n)+?(?=\ndef _observe_theory_state\()"
replacement = '''def _mixed_logic_circuit(state: UniverseState, latent: dict, hour: float) -> dict:
    m = state.metabolites if isinstance(state.metabolites, dict) else {}
    f = state.pathway_flux if isinstance(state.pathway_flux, dict) else {}

    atp_hi = 1 if float(m.get("atp", 0.0)) > 0.55 else 0
    redox_hi = 1 if float(f.get("redox_pressure", 0.0)) > 0.45 else 0
    oxphos_hi = 1 if float(f.get("oxphos", 0.0)) > 0.35 else 0
    gly_hi = 1 if float(f.get("glycolysis", 0.0)) > 0.40 else 0
    conf_hi = 1 if float(latent.get("confinement_index", 0.0)) > 0.0 else 0
    par_hi = 1 if float(latent.get("parallelity_index", 0.0)) > 0.0 else 0
    day_on = 1 if (6.0 <= float(hour) <= 18.0) else 0

    repo_sig = _repo_biochemical_signal(state, latent, hour=float(hour))
    repo_stress_hi = 1 if float(repo_sig.get("stress_signal", 0.0)) > 0.35 else 0
    repo_mob_hi = 1 if float(repo_sig.get("mobility_signal", 0.0)) > 0.30 else 0
    repo_anchor_hi = 1 if float(repo_sig.get("anchor_signal", 0.0)) > 0.30 else 0

    supply_gate = and_gate(atp_hi, oxphos_hi)
    stress_gate = and_gate(redox_hi, conf_hi)
    mobility_gate = and_gate(gly_hi, par_hi)
    day_stress_gate = and_gate(day_on, stress_gate)
    repo_stress_gate = and_gate(repo_stress_hi, conf_hi)
    repo_mobility_gate = and_gate(repo_mob_hi, par_hi)

    alpha_mix = 1.0 + 0.08 * float(supply_gate) - 0.06 * float(day_stress_gate) + 0.04 * float(mobility_gate) + 0.05 * float(repo_mobility_gate) - 0.03 * float(repo_anchor_hi)
    damping_mix = 1.0 + 0.10 * float(stress_gate) - 0.05 * float(supply_gate) + 0.06 * float(repo_stress_gate) + 0.04 * float(repo_anchor_hi)
    debt_mix = 1.0 + 0.08 * float(stress_gate) - 0.06 * float(mobility_gate) + 0.05 * float(repo_stress_gate)
    gate_bias_deg = 0.75 * float(mobility_gate) - 1.00 * float(day_stress_gate) + 0.50 * float(repo_mobility_gate) - 0.50 * float(repo_stress_gate)

    redox = float(np.nan_to_num(float(f.get("redox_pressure", 0.0)), nan=0.0, posinf=1.0, neginf=0.0))
    oxph = float(np.nan_to_num(float(f.get("oxphos", 0.0)), nan=0.0, posinf=1.0, neginf=0.0))
    gly = float(np.nan_to_num(float(f.get("glycolysis", 0.0)), nan=0.0, posinf=1.0, neginf=0.0))
    par = float(np.nan_to_num(float(latent.get("parallelity_index", 0.0)), nan=0.0, posinf=1.0, neginf=-1.0))
    repo_stress = float(np.nan_to_num(float(repo_sig.get("stress_signal", 0.0)), nan=0.0, posinf=1.0, neginf=0.0))
    repo_mob = float(np.nan_to_num(float(repo_sig.get("mobility_signal", 0.0)), nan=0.0, posinf=1.0, neginf=0.0))
    repo_anchor = float(np.nan_to_num(float(repo_sig.get("anchor_signal", 0.0)), nan=0.0, posinf=1.0, neginf=0.0))

    eq_alpha = 1.0 + 0.08 * oxph - 0.06 * redox + 0.04 * gly + 0.05 * repo_mob - 0.03 * repo_anchor
    eq_damping = 1.0 + 0.10 * redox - 0.05 * oxph + 0.06 * repo_stress + 0.04 * repo_anchor
    eq_debt = 1.0 + 0.08 * redox - 0.06 * gly + 0.05 * repo_stress
    eq_gate_bias_deg = 0.75 * par - 1.00 * (float(day_on) * redox) + 0.50 * repo_mob - 0.50 * repo_stress

    return {
        "alpha_mix": float(max(0.7, min(1.3, alpha_mix))),
        "damping_mix": float(max(0.7, min(1.4, damping_mix))),
        "debt_mix": float(max(0.8, min(1.3, debt_mix))),
        "gate_bias_deg": float(gate_bias_deg),
        "switch_bits": {
            "supply_gate": int(supply_gate),
            "stress_gate": int(stress_gate),
            "mobility_gate": int(mobility_gate),
            "repo_stress_gate": int(repo_stress_gate),
            "repo_mobility_gate": int(repo_mobility_gate),
        },
        "expression_state": {
            "alpha_mix": float(alpha_mix),
            "damping_mix": float(damping_mix),
            "debt_mix": float(debt_mix),
            "gate_bias_deg": float(gate_bias_deg),
        },
        "equation_state": {
            "alpha_eq": float(eq_alpha),
            "damping_eq": float(eq_damping),
            "debt_eq": float(eq_debt),
            "gate_bias_eq_deg": float(eq_gate_bias_deg),
        },
        "comparison": {
            "alpha_error": float(alpha_mix - eq_alpha),
            "damping_error": float(damping_mix - eq_damping),
            "debt_error": float(debt_mix - eq_debt),
            "gate_bias_error_deg": float(gate_bias_deg - eq_gate_bias_deg),
        },
        "repo_signal": repo_sig,
    }
'''

new_t, n = re.subn(pattern, replacement, t, flags=re.M)
if n != 1:
    raise SystemExit(f'replace failed: {n}')
p.write_text(new_t, encoding='utf-8-sig')
print('mixed_logic replaced', n)
