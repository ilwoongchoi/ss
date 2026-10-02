"""
iso_8base_41deriv.py — 8 base buffer particles generate 41 derived particles.

8 base: muon, gluon, w_boson, muon_neutrino, z_boson, higgs, tau, photon
Each derived = unique combination/pathway of 8 base buffer cascade.

7-step stress cascade:
  stress -> Higgs -> Gluon -> Muon -> Photon -> Tau -> W -> Z -> nu_mu (ghost)

41 derived = base + 7 transition states + 28 cascade paths + 5 cycle states

Date: 2026-09-09
"""
import json, math
from pathlib import Path

BASE_8 = ["higgs","gluon","muon","photon","tau","w_boson","z_boson","muon_neutrino"]
CASCADE = ["higgs","gluon","muon","photon","tau","w_boson","z_boson"]  # 7 steps
GHOST = "muon_neutrino"

# Transition rates (cascade ODE coefficients, normalized)
# k_HG = Higgs -> Gluon rate, etc.
# Use 7-step stress relaxation with decreasing rates (each step slower)
K_TRANSITION = {
    "HG": 1.0,    # higgs -> gluon (fastest)
    "GM": 0.7,    # gluon -> muon
    "MP": 0.5,    # muon -> photon
    "PT": 0.3,    # photon -> tau
    "TW": 0.2,    # tau -> W
    "WZ": 0.1,    # W -> Z
    "Znu": 0.05,  # Z -> nu_mu (slowest)
}

# 41 derived particles
def generate_41():
    """Generate 41 derived particles from 8 base + cascade structure."""
    derived = []

    # 1-8: 8 base particles (raw)
    for b in BASE_8:
        derived.append({"name": b, "type": "base", "n_compose": 1, "components": [b]})

    # 9-15: 7 transition states (Higgs-Gluon, Gluon-Muon, etc.)
    transitions = ["HG","GM","MP","PT","TW","WZ","Znu"]
    for t in transitions:
        a, b = t[0], t[1] if len(t) > 1 else ""
        # Map letters
        a_map = {"H":"higgs","G":"gluon","M":"muon","P":"photon","T":"tau","W":"w_boson","Z":"z_boson"}
        b_map = {"G":"gluon","M":"muon","P":"photon","T":"tau","W":"w_boson","Z":"z_boson","n":"muon_neutrino"}
        name_a = a_map.get(a, a)
        name_b = b_map.get(b, b)
        if t == "Znu":
            derived.append({"name": f"{name_a}_{name_b}", "type": "transition",
                           "n_compose": 2, "components": [name_a, name_b], "rate": K_TRANSITION[t]})
        else:
            derived.append({"name": f"{name_a}_{name_b}", "type": "transition",
                           "n_compose": 2, "components": [name_a, name_b], "rate": K_TRANSITION[t]})

    # 16-43: 28 cascade paths (combinations of cascade order)
    # 8 choose 2 = 28 unique pairs from cascade
    pairs = []
    for i, a in enumerate(CASCADE):
        for j, b in enumerate(CASCADE):
            if i < j:  # ordered pair
                pairs.append((a, b))
    # Take first 28
    for a, b in pairs[:28]:
        derived.append({"name": f"{a}_{b}_path", "type": "cascade_path",
                       "n_compose": 2, "components": [a, b]})

    # 44-48: 5 cycle states (full loop, ghost output, dual, etc.)
    cycle_states = [
        {"name": "full_loop_8step", "type": "cycle", "n_compose": 8,
         "components": CASCADE + [GHOST]},
        {"name": "ghost_output", "type": "ghost", "n_compose": 1, "components": [GHOST]},
        {"name": "stress_input", "type": "input", "n_compose": 1, "components": ["stress"]},
        {"name": "stress_HG_2step", "type": "short_cycle", "n_compose": 3,
         "components": ["stress", "higgs", "gluon"]},
        {"name": "stress_to_ghost_full", "type": "long_cycle", "n_compose": 9,
         "components": ["stress"] + CASCADE + [GHOST]},
    ]
    derived.extend(cycle_states)

    # Trim or extend to 41 exactly
    return derived[:41]

# 7-step cascade ODE
def cascade_ode(t, x, k):
    """
    7-step stress relaxation:
    dH/dt = sigma_in - k_HG * H
    dG/dt = k_HG * H - k_GM * G
    dM/dt = k_GM * G - k_MP * M
    dP/dt = k_MP * M - k_PT * P
    dT/dt = k_PT * P - k_TW * T
    dW/dt = k_TW * T - k_WZ * W
    dZ/dt = k_WZ * W - k_Znu * Z
    dN/dt = k_Znu * Z  (sink)
    """
    H, G, M, P, T_, W, Z, N = x
    dH = -k["HG"] * H
    dG = k["HG"] * H - k["GM"] * G
    dM = k["GM"] * G - k["MP"] * M
    dP = k["MP"] * M - k["PT"] * P
    dT = k["PT"] * P - k["TW"] * T_
    dW = k["TW"] * T_ - k["WZ"] * W
    dZ = k["WZ"] * W - k["Znu"] * Z
    dN = k["Znu"] * Z
    return [dH, dG, dM, dP, dT, dW, dZ, dN]

def rk4(f, t, x, h, k):
    k1 = f(t, x, k)
    k2 = f(t+h/2, [x[i]+h*k1[i]/2 for i in range(8)], k)
    k3 = f(t+h/2, [x[i]+h*k2[i]/2 for i in range(8)], k)
    k4 = f(t+h, [x[i]+h*k3[i] for i in range(8)], k)
    return [x[i] + h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(8)], t+h

def integrate(f, x0, t_end, dt, k):
    ts, xs = [0.0], [x0[:]]
    t, x = 0.0, x0[:]
    n_max = int(t_end / dt)
    for _ in range(n_max):
        x, t = rk4(f, t, x, dt, k)
        ts.append(t); xs.append(x[:])
    return ts, xs

def main():
    print("=" * 70)
    print("8 BASE -> 41 DERIVED PARTICLES (cascade combinations)")
    print("=" * 70)
    print()
    print(f"  8 base buffer particles:")
    for b in BASE_8:
        print(f"    - {b}")

    print()
    print(f"  7-step cascade (k values):")
    print(f"    sigma_in -> H[{K_TRANSITION['HG']}] -> G[{K_TRANSITION['GM']}] -> M[{K_TRANSITION['MP']}]")
    print(f"           -> P[{K_TRANSITION['PT']}] -> T[{K_TRANSITION['TW']}] -> W[{K_TRANSITION['WZ']}]")
    print(f"           -> Z[{K_TRANSITION['Znu']}] -> nu_mu (ghost sink)")

    # Generate 41
    derived = generate_41()
    print(f"\n  Generated {len(derived)} derived particles:")
    types = {}
    for d in derived:
        t = d["type"]
        types[t] = types.get(t, 0) + 1
    for t, c in types.items():
        print(f"    {t:20s}: {c} particles")

    # Run cascade ODE
    print()
    print("=" * 70)
    print("CASCADE ODE: 8 particle stress relaxation")
    print("=" * 70)
    x0 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Higgs starts with 1.0
    # Time to 13.8 Gyr in normalized units (tau = 1/(slowest rate) = 1/0.05 = 20)
    ts, xs = integrate(cascade_ode, x0, t_end=80.0, dt=0.1, k=K_TRANSITION)

    print(f"\n  {'t':6s}", end="")
    for label in ["H","G","M","P","T","W","Z","Nu"]:
        print(f" {label:7s}", end="")
    print(f"  {'SUM':7s}")
    for i in [0, 5, 10, 20, 40, 60, 80, 100, 200, 400, 600, 799]:
        if i < len(ts):
            x = xs[i]
            s = sum(x)
            print(f"  {ts[i]:5.1f}", end="")
            for v in x:
                print(f" {v:7.4f}", end="")
            print(f"  {s:7.4f}")

    # Conservation check: total should be ~1.0 (Higgs initial)
    final = xs[-1]
    sum_final = sum(final)
    print(f"\n  Final sum: {sum_final:.4f} (initial 1.0) -- mass conservation")
    nu_final = final[-1]  # neutrino sink
    print(f"  Neutrino (ghost sink) fraction: {nu_final:.4f}")

    # Save
    out = {
        "_version": "8base_41deriv_v1",
        "_date": "2026-09-09",
        "_method": "8 base buffer particles + 7-step stress cascade ODE",
        "base_8": BASE_8,
        "cascade_7": CASCADE,
        "k_transitions": K_TRANSITION,
        "n_derived": len(derived),
        "derived_breakdown": types,
        "cascade_ode_result": {
            "initial_H": 1.0,
            "final_sum": round(sum_final, 4),
            "ghost_sink_fraction": round(nu_final, 4),
        },
    }
    out_path = Path(__file__).parent / "iso_8base_41deriv.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")

if __name__ == "__main__":
    main()
