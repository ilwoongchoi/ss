# analyze_dist_all_geometry.py
# dist_all.csv로부터 동역학 → geometry 상수 추출
#
# PURPOSE:
# - Reference cell (r_ref, q0_ref) 찾기
# - kappa_TDA(r,q0) 맵 정의
# - SH boundary band 데이터 기반 재정의
# - 128-grid 파라미터로 낼 요약 상수 계산

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

# ===================================================================
# 1. LOAD DATA
# ===================================================================
input_path = "analysis_results/iter3_tda_v2/dist_all.csv"
df = pd.read_csv(input_path)

print("=" * 60)
print("DIST_ALL.CSV GEOMETRY EXTRACTION")
print("=" * 60)
print(f"Input: {input_path}")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print("-" * 60)

# ===================================================================
# 2. REFERENCE CELL (wasserstein_H1 ≈ 0)
# ===================================================================
# wasserstein_H1이 최소인 지점이 reference (자기 자신과의 거리 = 0)
ref_idx = df["wasserstein_H1"].idxmin()
ref_row = df.loc[ref_idx]

r_ref = float(ref_row["r"])
q0_ref = float(ref_row["q0"])
p_ref = float(ref_row["max_persistence"])

print(f"\n[REFERENCE CELL]")
print(f"  Index: {ref_idx}")
print(f"  r_ref:  {r_ref:.6f}")
print(f"  q0_ref: {q0_ref:.6f}")
print(f"  p_ref (max_persistence): {p_ref:.6f}")
print(f"  wasserstein_H1 at ref: {ref_row['wasserstein_H1']:.6f}")

# ===================================================================
# 3. KAPPA_TDA MAP 정의
# ===================================================================
p_max = float(df["max_persistence"].max())
p_min = float(df["max_persistence"].min())

# 게이트 상수 (1/64 → 1/32 → 1/16)
kmin, kmid, kmax = 1/64, 1/32, 1/16

def kappa_tda(p):
    """
    Piecewise-linear kappa map:
    - p ≤ p_ref: kmin → kmid (1/64 → 1/32)
    - p > p_ref: kmid → kmax (1/32 → 1/16)
    """
    if p <= p_ref:
        # 선형 보간: kmin + (kmid-kmin) * (p / p_ref)
        ratio = (p - p_min) / (p_ref - p_min + 1e-12)
        return kmin + (kmid - kmin) * ratio
    else:
        # 선형 보간: kmid + (kmax-kmid) * ((p-p_ref) / (p_max-p_ref))
        ratio = (p - p_ref) / (p_max - p_ref + 1e-12)
        return kmid + (kmax - kmid) * ratio

# Apply to all rows
df["kappa_tda"] = df["max_persistence"].map(kappa_tda)

print(f"\n[KAPPA_TDA MAP]")
print(f"  p_min: {p_min:.6f}")
print(f"  p_ref: {p_ref:.6f}")
print(f"  p_max: {p_max:.6f}")
print(f"  kappa range: [{df['kappa_tda'].min():.6f}, {df['kappa_tda'].max():.6f}]")
print(f"  Target kmid (1/32): {kmid:.6f}")

# ===================================================================
# 4. SH BOUNDARY BAND 재정의
# ===================================================================
# Band = kappa_tda가 1/32 주변에 모이는 띠
eps = 0.001  # 1/32 주변 허용 오차

band_mask = (df["kappa_tda"] > kmid - eps) & (df["kappa_tda"] < kmid + eps)
band = df[band_mask].copy()

print(f"\n[SH BOUNDARY BAND]")
print(f"  Definition: |kappa - 1/32| < {eps}")
print(f"  Band size: {len(band)} / {len(df)} ({100*len(band)/len(df):.1f}%)")

if len(band) > 0:
    band_stats = {
        "r_min": float(band["r"].min()),
        "r_max": float(band["r"].max()),
        "r_mean": float(band["r"].mean()),
        "r_std": float(band["r"].std()),
        "q0_min": float(band["q0"].min()),
        "q0_max": float(band["q0"].max()),
        "q0_mean": float(band["q0"].mean()),
        "q0_std": float(band["q0"].std()),
        "persistence_mean": float(band["max_persistence"].mean()),
        "persistence_std": float(band["max_persistence"].std()),
        "wasserstein_mean": float(band["wasserstein_H1"].mean()),
        "bottleneck_mean": float(band["bottleneck_H1"].mean()),
    }
    
    print(f"  r range: [{band_stats['r_min']:.6f}, {band_stats['r_max']:.6f}]")
    print(f"  q0 range: [{band_stats['q0_min']:.6f}, {band_stats['q0_max']:.6f}]")
    print(f"  FWHM (r): {band_stats['r_max'] - band_stats['r_min']:.6f}")
else:
    band_stats = {}
    print("  WARNING: No band cells found with current epsilon!")

# ===================================================================
# 5. SUMMARY CONSTANTS (128-grid 상위 규칙)
# ===================================================================
summary = {
    "ref_cell": {
        "r_ref": r_ref,
        "q0_ref": q0_ref,
        "p_ref": p_ref,
    },
    "p_range": {
        "p_min": p_min,
        "p_max": p_max,
    },
    "kappa_constants": {
        "kmin_1_64": kmin,
        "kmid_1_32": kmid,
        "kmax_1_16": kmax,
    },
    "kappa_tda_stats": {
        "mean": float(df["kappa_tda"].mean()),
        "std": float(df["kappa_tda"].std()),
        "min": float(df["kappa_tda"].min()),
        "max": float(df["kappa_tda"].max()),
    },
    "sh_boundary_band": band_stats,
    "data_stats": {
        "total_cells": len(df),
        "band_cells": len(band),
        "r_range": [float(df["r"].min()), float(df["r"].max())],
        "q0_range": [float(df["q0"].min()), float(df["q0"].max())],
    }
}

# ===================================================================
# 6. SAVE OUTPUTS
# ===================================================================
output_dir = Path("out")
output_dir.mkdir(exist_ok=True)

# Save enriched CSV
df.to_csv(output_dir / "dist_all_with_kappa.csv", index=False)
print(f"\n[SAVED] {output_dir / 'dist_all_with_kappa.csv'}")

# Save band-only CSV
if len(band) > 0:
    band.to_csv(output_dir / "sh_band_from_kappa.csv", index=False)
    print(f"[SAVED] {output_dir / 'sh_band_from_kappa.csv'}")

# Save JSON summary
with open(output_dir / "geometry_constants_from_dist_all.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"[SAVED] {output_dir / 'geometry_constants_from_dist_all.json'}")

# ===================================================================
# 7. VISUALIZATION
# ===================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("Geometry from dist_all.csv: κ_TDA & SH Boundary Band", fontsize=14)

# Plot 1: kappa_tda vs max_persistence
ax = axes[0, 0]
scatter = ax.scatter(df["max_persistence"], df["kappa_tda"], 
                     c=df["wasserstein_H1"], cmap="viridis", alpha=0.6, s=20)
ax.axvline(p_ref, color="red", linestyle="--", label=f"p_ref = {p_ref:.4f}")
ax.axhline(kmid, color="orange", linestyle="--", label=f"1/32 = {kmid:.4f}")
ax.set_xlabel("max_persistence (p)")
ax.set_ylabel("kappa_tda (κ)")
ax.set_title("κ_TDA Map: Persistence → Geometry Gate")
ax.legend()
plt.colorbar(scatter, ax=ax, label="wasserstein_H1")

# Plot 2: r-q0 plane colored by kappa
ax = axes[0, 1]
scatter = ax.scatter(df["r"], df["q0"], c=df["kappa_tda"], 
                     cmap="RdYlGn", vmin=kmin, vmax=kmax, alpha=0.6, s=20)
ax.scatter(r_ref, q0_ref, color="red", s=100, marker="X", 
           edgecolors="black", linewidths=2, label="Reference Cell", zorder=5)
if len(band) > 0:
    ax.scatter(band["r"], band["q0"], color="cyan", s=10, 
               alpha=0.3, label=f"SH Band (n={len(band)})", zorder=4)
ax.set_xlabel("r")
ax.set_ylabel("q0")
ax.set_title("r-q0 Plane: κ_TDA Distribution")
plt.colorbar(scatter, ax=ax, label="kappa_tda")
ax.legend()

# Plot 3: Histogram of kappa values
ax = axes[1, 0]
ax.hist(df["kappa_tda"], bins=50, alpha=0.7, color="steelblue", edgecolor="white")
ax.axvline(kmid, color="orange", linestyle="--", linewidth=2, label=f"1/32 = {kmid:.4f}")
ax.axvline(kmin, color="blue", linestyle=":", alpha=0.5, label=f"1/64 = {kmin:.4f}")
ax.axvline(kmax, color="green", linestyle=":", alpha=0.5, label=f"1/16 = {kmax:.4f}")
ax.set_xlabel("kappa_tda")
ax.set_ylabel("Count")
ax.set_title("κ_TDA Distribution (Should peak near 1/32)")
ax.legend()

# Plot 4: Band statistics
ax = axes[1, 1]
if len(band) > 0:
    # Show band region
    ax.scatter(df["r"], df["max_persistence"], c="lightgray", alpha=0.3, s=10, label="All cells")
    ax.scatter(band["r"], band["max_persistence"], c="red", s=30, 
               alpha=0.7, label=f"SH Band cells (n={len(band)})")
    ax.axhline(p_ref, color="blue", linestyle="--", alpha=0.5, label=f"p_ref = {p_ref:.4f}")
    ax.set_xlabel("r")
    ax.set_ylabel("max_persistence")
    ax.set_title("SH Boundary Band: Persistence vs r")
    ax.legend()
else:
    ax.text(0.5, 0.5, "No band cells found", ha="center", va="center", 
            transform=ax.transAxes, fontsize=12)
    ax.set_title("SH Boundary Band")

plt.tight_layout()
plt.savefig(output_dir / "dist_all_geometry_analysis.png", dpi=150)
print(f"[SAVED] {output_dir / 'dist_all_geometry_analysis.png'}")

# ===================================================================
# 8. PRINT FINAL SUMMARY
# ===================================================================
print("\n" + "=" * 60)
print("FINAL GEOMETRY CONSTANTS (for 128-grid)")
print("=" * 60)
print(f"""
# Reference Cell (The Anchor)
R_REF = {r_ref:.6f}
Q0_REF = {q0_ref:.6f}
P_REF = {p_ref:.6f}

# Persistence Range
P_MIN = {p_min:.6f}
P_MAX = {p_max:.6f}

# Gate Constants (from kappa map)
K_MIN = 1/64 = {kmin:.6f}
K_MID = 1/32 = {kmid:.6f}  ← THE ANCHOR
K_MAX = 1/16 = {kmax:.6f}

# SH Boundary Band (|κ - 1/32| < {eps})
""")
if len(band) > 0:
    print(f"""BAND_R_MIN = {band_stats['r_min']:.6f}
BAND_R_MAX = {band_stats['r_max']:.6f}
BAND_Q0_MIN = {band_stats['q0_min']:.6f}
BAND_Q0_MAX = {band_stats['q0_max']:.6f}
BAND_R_FWHM = {band_stats['r_max'] - band_stats['r_min']:.6f}
""")

print("=" * 60)
print("Analysis complete!")
