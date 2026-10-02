"""
iso_pdg_kappa.py — KAPPA matrix for 8 particles using PDG widths.

1. Compute phases: φ_i = 2π * log10(k_i) / log10(k_max)
2. KAPPA_ij = C² * sin(φ_i - φ_j) * w_pair (antisymmetric)
3. Cluster 8 particles into 6 timescale families
4. Match 6 clusters to 6 attractors

Date: 2026-09-09
"""
import json, math
from pathlib import Path

PDG_8 = {
    "muon":          {"k": 4.55e5,   "Gamma_GeV": 2.996e-10, "tau_s": 2.197e-6},
    "gluon":         {"k": 1.0e23,   "Gamma_GeV": 0.0,       "tau_s": 1.0e-23},
    "w_boson":       {"k": 3.16e24,  "Gamma_GeV": 2.085,     "tau_s": 3.16e-25},
    "z_boson":       {"k": 3.79e24,  "Gamma_GeV": 2.495,     "tau_s": 2.64e-25},
    "higgs":         {"k": 6.17e21,  "Gamma_GeV": 4.07e-3,   "tau_s": 1.62e-22},
    "tau":           {"k": 3.44e12,  "Gamma_GeV": 2.27e-10,  "tau_s": 2.91e-13},
    "photon":        {"k": 6.9e-14,  "Gamma_GeV": 0.0,       "tau_s": 1.45e13},
    "muon_neutrino": {"k": 1.0e12,   "Gamma_GeV": 0.0,       "tau_s": 1.0e-12},
}

# 6 attractors
ATTRACTORS_6 = ["energy", "information", "repair", "opioid", "gan_bulkhead", "cox_retrograde"]

# Cluster assignment (by timescale, log10(k))
# 1: photon, 2: muon, 3: muon_neutrino + tau, 4: higgs, 5: gluon, 6: w_boson + z_boson
CLUSTER = {
    "photon":        1,  # slowest (k=6.9e-14)
    "muon":          2,
    "muon_neutrino": 3,
    "tau":           3,
    "higgs":         4,
    "gluon":         5,
    "w_boson":       6,  # fastest (k=3.16e24)
    "z_boson":       6,
}

# 6 attractor cluster assignment (by physical meaning)
CLUSTER_ATTRACTOR = {
    1: "information",     # photon = EM = information carrier
    2: "opioid",          # muon = opioid analog (2.2μs lifetime, μSR physics)
    3: "repair",          # tau + νμ = heavy lepton + ghost = repair/damage
    4: "gan_bulkhead",    # higgs = mass gate = bulkhead
    5: "energy",          # gluon = strong force = energy storage
    6: "cox_retrograde",  # W + Z = electroweak = retroaction
}

C2 = 0.08  # coupling quantum from kernel

def main():
    print("=" * 70)
    print("KAPPA MATRIX for 8 particles (PDG widths as k)")
    print("=" * 70)

    # Compute phases
    log_k = {p: math.log10(d["k"]) for p, d in PDG_8.items()}
    log_k_min = min(log_k.values())
    log_k_max = max(log_k.values())
    phases = {p: 2 * math.pi * (log_k[p] - log_k_min) / (log_k_max - log_k_min)
              for p in PDG_8}

    print("\n[Phases (normalized to 2π, slowest=0, fastest=2π)]")
    for p, phi in sorted(phases.items(), key=lambda x: x[1]):
        print(f"  {p:15s} phi = {phi:.3f} rad ({math.degrees(phi):6.1f}°)")

    # KAPPA matrix
    particles = list(PDG_8.keys())
    n = len(particles)
    K = [[0.0]*n for _ in range(n)]
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles):
            K[i][j] = C2 * math.sin(phases[p1] - phases[p2])

    # Antisymmetry check
    print("\n[KAPPA antisymmetry check]")
    max_asym = 0.0
    for i in range(n):
        for j in range(n):
            asym = abs(K[i][j] + K[j][i])
            max_asym = max(max_asym, asym)
    print(f"  max |K_ij + K_ji| = {max_asym:.2e} (expect 0)")
    print(f"  Antisymmetric: {max_asym < 1e-10}")

    # Print KAPPA matrix
    print("\n[KAPPA matrix (8x8, antisymmetric)]")
    print(f"  {'':15s}", end="")
    for p in particles:
        print(f" {p[:6]:7s}", end="")
    print()
    for i, p1 in enumerate(particles):
        print(f"  {p1:15s}", end="")
        for j in range(n):
            print(f" {K[i][j]:+7.4f}", end="")
        print()

    # 6 cluster → 6 attractor mapping
    print("\n[6 CLUSTER → 6 ATTRACTOR MAPPING]")
    print(f"  Cluster 1 (photon)        → {CLUSTER_ATTRACTOR[1]}")
    print(f"  Cluster 2 (muon)          → {CLUSTER_ATTRACTOR[2]}")
    print(f"  Cluster 3 (νμ + τ)        → {CLUSTER_ATTRACTOR[3]}")
    print(f"  Cluster 4 (higgs)         → {CLUSTER_ATTRACTOR[4]}")
    print(f"  Cluster 5 (gluon)         → {CLUSTER_ATTRACTOR[5]}")
    print(f"  Cluster 6 (W + Z)         → {CLUSTER_ATTRACTOR[6]}")

    # Cluster KAPPA (6x6 reduced)
    print("\n[CLUSTER KAPPA (6x6, reduce by cluster mean)]")
    cluster_ids = [1, 2, 3, 4, 5, 6]
    K_cluster = [[0.0]*6 for _ in range(6)]
    for ci in cluster_ids:
        for cj in cluster_ids:
            s = 0.0
            cnt = 0
            for i, p1 in enumerate(particles):
                if CLUSTER[p1] != ci: continue
                for j, p2 in enumerate(particles):
                    if CLUSTER[p2] != cj: continue
                    s += K[i][j]
                    cnt += 1
            if cnt > 0:
                K_cluster[ci-1][cj-1] = s / cnt
    print(f"  {'':12s}", end="")
    for c in cluster_ids:
        print(f" C{c}      ", end="")
    print()
    cluster_names = ["info", "opioid", "repair", "gan", "energy", "cox"]
    for ci in cluster_ids:
        print(f"  C{ci} ({cluster_names[ci-1]:6s})", end="")
        for cj in cluster_ids:
            print(f" {K_cluster[ci-1][cj-1]:+7.4f}", end="")
        print()

    # Check cluster antisymmetry
    cluster_asym = max(abs(K_cluster[i][j] + K_cluster[j][i])
                       for i in range(6) for j in range(6))
    print(f"\n  Cluster max |K_ij + K_ji| = {cluster_asym:.2e} (expect 0)")

    # Toroidal sum: should be ~0 (closed)
    diag_sum = sum(K_cluster[i][i] for i in range(6))
    print(f"  Diagonal sum (should be 0): {diag_sum:.2e}")

    # Save
    out = {
        "_version": "pdg_kappa_v1",
        "_date": "2026-09-09",
        "_method": "Phases from log10(k) normalized 0..2π, KAPPA = C² sin(φ_i - φ_j)",
        "phases": {p: round(phi, 4) for p, phi in phases.items()},
        "kappa_matrix": [[round(K[i][j], 6) for j in range(n)] for i in range(n)],
        "antisymmetric": max_asym < 1e-10,
        "cluster_to_attractor": CLUSTER_ATTRACTOR,
        "cluster_kappa": [[round(K_cluster[i][j], 6) for j in range(6)] for i in range(6)],
        "cluster_antisymmetric": cluster_asym < 1e-10,
        "cluster_diag_sum": round(diag_sum, 6),
    }
    out_path = Path(__file__).parent / "iso_pdg_kappa.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")

if __name__ == "__main__":
    main()
