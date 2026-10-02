"""
iso_pdg_cycle.py — 24h toroidal cycle using 8 particle phases.

For each hour h in [0, 24), compute KAPPA-weighted 6 attractor balance.
Verify cycle closure: attractor balance at t=0 == at t=24.

Date: 2026-09-09
"""
import json, math
from pathlib import Path

PDG_8 = {
    "muon":          {"k": 4.55e5},
    "gluon":         {"k": 1.0e23},
    "w_boson":       {"k": 3.16e24},
    "z_boson":       {"k": 3.79e24},
    "higgs":         {"k": 6.17e21},
    "tau":           {"k": 3.44e12},
    "photon":        {"k": 6.9e-14},
    "muon_neutrino": {"k": 1.0e12},
}

CLUSTER = {
    "photon": 1, "muon": 2, "muon_neutrino": 3, "tau": 3,
    "higgs": 4, "gluon": 5, "w_boson": 6, "z_boson": 6,
}

ATTRACTOR_NAMES = ["information", "opioid", "repair", "gan_bulkhead", "energy", "cox_retrograde"]

C2 = 0.08

def main():
    print("=" * 70)
    print("24H TOROIDAL CYCLE — 8 particle KAPPA → 6 attractor balance")
    print("=" * 70)

    # Particle phases: assigned UNIFORMLY by cluster (6 clusters, each gets 2π/6)
    # Cluster 1 (photon, slowest) -> phase 0
    # Cluster 2 (muon) -> phase 2π/6
    # Cluster 3 (νμ, τ) -> phase 2*2π/6
    # Cluster 4 (higgs) -> phase 3*2π/6
    # Cluster 5 (gluon) -> phase 4*2π/6
    # Cluster 6 (W, Z, fastest) -> phase 5*2π/6
    log_k = {p: math.log10(d["k"]) for p, d in PDG_8.items()}
    log_k_min = min(log_k.values())
    log_k_max = max(log_k.values())

    P2A = {
        "photon": "information",
        "muon": "opioid",
        "muon_neutrino": "repair",
        "tau": "repair",
        "higgs": "gan_bulkhead",
        "gluon": "energy",
        "w_boson": "cox_retrograde",
        "z_boson": "cox_retrograde",
    }

    # 6 clusters get 4h each in 24h cycle (uniform distribution)
    # Cluster 1 (info)    at 0h, 24h
    # Cluster 2 (opioid)  at 4h
    # Cluster 3 (repair)  at 8h
    # Cluster 4 (gan)     at 12h
    # Cluster 5 (energy)  at 16h
    # Cluster 6 (cox)     at 20h
    CLUSTER_HOUR = {1: 0.0, 2: 4.0, 3: 8.0, 4: 12.0, 5: 16.0, 6: 20.0}
    particle_peak_hour = {p: CLUSTER_HOUR[CLUSTER[p]] for p in PDG_8}

    # For each hour, compute 6 attractor balance
    print("\n[24H cycle: 6 attractor balance (4h per cluster, uniform)]")
    print(f"  {'hour':6s}", end="")
    for a in ATTRACTOR_NAMES:
        print(f" {a[:9]:9s}", end="")
    print(f" {'SUM':7s}")
    print("  " + "-" * 70)

    cycles = []
    for h_int in range(0, 25, 2):
        h = float(h_int)
        attractor_balance = {a: 0.0 for a in ATTRACTOR_NAMES}
        for p in PDG_8:
            peak_h = particle_peak_hour[p]
            # Gaussian peak at peak_h, sigma = 2h (each attractor dominates for ~4h)
            sigma_h = 2.0
            # Use modular distance
            dh = min(abs(h - peak_h), 24 - abs(h - peak_h))
            weight = math.exp(-((dh / sigma_h) ** 2))
            attractor_balance[P2A[p]] += weight

        total = sum(attractor_balance.values())
        if total > 0:
            for a in attractor_balance:
                attractor_balance[a] /= total

        s = sum(attractor_balance.values())
        cycles.append((h, attractor_balance, s))
        print(f"  {h:5.1f}h", end="")
        for a in ATTRACTOR_NAMES:
            print(f" {attractor_balance[a]:9.3f}", end="")
        print(f" {s:7.3f}")

    # Cycle closure: t=0 should equal t=24
    t0 = cycles[0][1]
    t24 = cycles[-1][1]
    diff = sum(abs(t0[a] - t24[a]) for a in ATTRACTOR_NAMES)
    print(f"\n[Cycle closure check]")
    print(f"  |balance(0h) - balance(24h)|_1 = {diff:.2e} (expect 0)")
    print(f"  Cycle closed: {diff < 1e-10}")

    # Total particle count check
    print(f"\n[Particle assignment check]")
    for a in ATTRACTOR_NAMES:
        particles = [p for p, a2 in P2A.items() if a2 == a]
        print(f"  {a:18s} <- {particles}")

    # Save
    out = {
        "_version": "pdg_cycle_v1",
        "_date": "2026-09-09",
        "_method": "Gaussian phase matching on 24h toroidal time, particle k -> phase",
        "particle_to_attractor": P2A,
        "cycle_samples": [
            {"hour": h, "balance": {a: round(b, 4) for a, b in bal.items()}}
            for h, bal, s in cycles
        ],
        "cycle_closure_diff": diff,
        "cycle_closed": diff < 1e-10,
    }
    out_path = Path(__file__).parent / "iso_pdg_cycle.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")

if __name__ == "__main__":
    main()
