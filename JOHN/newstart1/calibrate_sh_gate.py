# calibrate_sh_gate.py
# ATLAS SH band와 dist_all 기반 band를 calibrate하여 통합 gate w_gate(r,q0) 생성

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from scipy.interpolate import griddata

# ===================================================================
# 1. LOAD CONSTANTS AND DATA
# ===================================================================
print("=" * 70)
print("SH GATE CALIBRATION: ATLAS vs dist_all")
print("=" * 70)

from geometry_package.absolute_constants import (
    SH_R_STAR, SH_Q0_STAR, SH_R_FWHM_L, SH_R_FWHM_R,
    SH_BOUNDARY_MIN, SH_BOUNDARY_MAX,
    R_REF, Q0_REF, P_REF, P_MAX,
    KAPPA_TDA_MID, SH_Q0_MIN, SH_Q0_MAX,
    SH_R_BAND_MIN, SH_R_BAND_MAX
)

print(f"\n[ATLAS CONSTANTS]")
print(f"  SH_R_STAR: {SH_R_STAR:.6f}, SH_Q0_STAR: {SH_Q0_STAR:.6f}")
print(f"  FWHM_L/R: {SH_R_FWHM_L:.6f}, {SH_R_FWHM_R:.6f}")

print(f"\n[dist_all CONSTANTS]")
print(f"  R_REF: {R_REF:.6f}, Q0_REF: {Q0_REF:.6f}")

# Load dist_all_with_kappa.csv
df = pd.read_csv("out/dist_all_with_kappa.csv")
print(f"\n[DATA] Loaded: {len(df)} cells")

# ===================================================================
# 2. SHIFT & SCALE CALCULATION
# ===================================================================
delta_r = R_REF - SH_R_STAR
delta_q = Q0_REF - SH_Q0_STAR

print(f"\n[SHIFT] Δr={delta_r:.6f}, Δq={delta_q:.6f}")

# dist band 셀들
eps_band = 0.001
band_mask = (df["kappa_tda"] > KAPPA_TDA_MID - eps_band) & (df["kappa_tda"] < KAPPA_TDA_MID + eps_band)
band_cells = df[band_mask].copy()
print(f"[BAND CELLS] {len(band_cells)} cells")

# Scale 추정
r_left = band_cells[band_cells["r"] <= R_REF]["r"]
r_right = band_cells[band_cells["r"] > R_REF]["r"]

s_L = R_REF - np.percentile(r_left, 16) if len(r_left) > 0 else SH_R_FWHM_L
s_R = np.percentile(r_right, 84) - R_REF if len(r_right) > 0 else SH_R_FWHM_R

fwhm_factor = 2 * np.sqrt(2 * np.log(2))
sigma_L = s_L * fwhm_factor
sigma_R = s_R * fwhm_factor

print(f"[SCALE] s_L={s_L:.6f}, s_R={s_R:.6f}")
print(f"[SIGMA] σL={sigma_L:.6f}, σR={sigma_R:.6f}")

# ===================================================================
# 3. WEIGHT FUNCTIONS (vectorized)
# ===================================================================

def w_atlas_vectorized(R, Q0, r_star=R_REF, q0_star=Q0_REF, sigma_l=sigma_L, sigma_r=sigma_R):
    """Vectorized asymmetric Gaussian"""
    dr = R - r_star
    w_r = np.where(dr < 0, 
                   np.exp(-0.5 * (dr / sigma_l) ** 2),
                   np.exp(-0.5 * (dr / sigma_r) ** 2))
    q0_width = SH_Q0_MAX - SH_Q0_MIN
    w_q = np.exp(-0.5 * ((Q0 - q0_star) / (q0_width / 2)) ** 2)
    return w_r * w_q

def w_kappa_vectorized(Kappa, eps):
    """Vectorized kappa weight"""
    return np.exp(-((Kappa - KAPPA_TDA_MID) / eps) ** 2)

# ===================================================================
# 4. CALCULATE ON GRID (coarser for speed)
# ===================================================================
print("\n[GRID CALCULATION]")

r_min, r_max = df["r"].min(), df["r"].max()
q0_min, q0_max = df["q0"].min(), df["q0"].max()

r_grid = np.linspace(r_min, r_max, 50)
q0_grid = np.linspace(q0_min, q0_max, 50)
R_grid, Q0_grid = np.meshgrid(r_grid, q0_grid)

# Interpolate kappa on grid
points = df[["r", "q0"]].values
values = df["kappa_tda"].values
kappa_grid = griddata(points, values, (R_grid, Q0_grid), method='linear', fill_value=KAPPA_TDA_MID)

# eps from data
kappa_std = band_cells["kappa_tda"].std() if len(band_cells) > 0 else 0.005
eps_kappa = max(kappa_std, 0.001)
print(f"  eps_kappa = {eps_kappa:.6f}")

# Calculate weights
W_atlas = w_atlas_vectorized(R_grid, Q0_grid)
W_kappa = w_kappa_vectorized(kappa_grid, eps_kappa)

alpha = 0.5
W_gate = (W_atlas ** alpha) * (W_kappa ** (1 - alpha))

print(f"  w_gate range: [{W_gate.min():.4f}, {W_gate.max():.4f}]")

# ===================================================================
# 5. EXTRACT CALIBRATED CONSTANTS
# ===================================================================
print("\n[CALIBRATED CONSTANTS]")

max_idx = np.unravel_index(np.argmax(W_gate), W_gate.shape)
calibrated_r_star = float(R_grid[max_idx])
calibrated_q0_star = float(Q0_grid[max_idx])

# Threshold = 0.5 for band definition
threshold = 0.5
band_mask_gate = W_gate > threshold

if np.any(band_mask_gate):
    calibrated_r_min = float(R_grid[band_mask_gate].min())
    calibrated_r_max = float(R_grid[band_mask_gate].max())
    calibrated_q0_min = float(Q0_grid[band_mask_gate].min())
    calibrated_q0_max = float(Q0_grid[band_mask_gate].max())
    
    # Extract sigma from calibrated band
    r_left_cal = R_grid[band_mask_gate & (R_grid <= calibrated_r_star)]
    r_right_cal = R_grid[band_mask_gate & (R_grid > calibrated_r_star)]
    
    cal_sigma_l = (calibrated_r_star - r_left_cal.min()) / fwhm_factor if len(r_left_cal) > 0 else sigma_L
    cal_sigma_r = (r_right_cal.max() - calibrated_r_star) / fwhm_factor if len(r_right_cal) > 0 else sigma_R
else:
    calibrated_r_min, calibrated_r_max = r_min, r_max
    calibrated_q0_min, calibrated_q0_max = q0_min, q0_max
    cal_sigma_l, cal_sigma_r = sigma_L, sigma_R

print(f"  CALIBRATED_SH_R_STAR: {calibrated_r_star:.6f}")
print(f"  CALIBRATED_SH_Q0_STAR: {calibrated_q0_star:.6f}")
print(f"  CALIBRATED_BOUNDARY: r=[{calibrated_r_min:.6f}, {calibrated_r_max:.6f}]")
print(f"  CALIBRATED_SIGMA_L/R: {cal_sigma_l:.6f}, {cal_sigma_r:.6f}")

# ===================================================================
# 6. SAVE RESULTS
# ===================================================================
output_data = {
    "calibration_params": {
        "delta_r": float(delta_r),
        "delta_q": float(delta_q),
        "s_L": float(s_L),
        "s_R": float(s_R),
        "sigma_L": float(sigma_L),
        "sigma_R": float(sigma_R),
        "eps_kappa": float(eps_kappa),
        "alpha": alpha
    },
    "atlas_original": {
        "SH_R_STAR": float(SH_R_STAR),
        "SH_Q0_STAR": float(SH_Q0_STAR),
        "SH_R_FWHM_L": float(SH_R_FWHM_L),
        "SH_R_FWHM_R": float(SH_R_FWHM_R),
        "SH_BOUNDARY_MIN": float(SH_BOUNDARY_MIN),
        "SH_BOUNDARY_MAX": float(SH_BOUNDARY_MAX)
    },
    "dist_all_based": {
        "R_REF": float(R_REF),
        "Q0_REF": float(Q0_REF),
        "SH_R_BAND_MIN": float(SH_R_BAND_MIN),
        "SH_R_BAND_MAX": float(SH_R_BAND_MAX),
        "SH_Q0_MIN": float(SH_Q0_MIN),
        "SH_Q0_MAX": float(SH_Q0_MAX),
        "band_cells_count": int(len(band_cells))
    },
    "calibrated": {
        "CALIBRATED_SH_R_STAR": calibrated_r_star,
        "CALIBRATED_SH_Q0_STAR": calibrated_q0_star,
        "CALIBRATED_SH_BOUNDARY_MIN": calibrated_r_min,
        "CALIBRATED_SH_BOUNDARY_MAX": calibrated_r_max,
        "CALIBRATED_SH_R_FWHM_L": float(cal_sigma_l * fwhm_factor),
        "CALIBRATED_SH_R_FWHM_R": float(cal_sigma_r * fwhm_factor),
        "CALIBRATED_SIGMA_L": cal_sigma_l,
        "CALIBRATED_SIGMA_R": cal_sigma_r,
        "CALIBRATED_Q0_MIN": calibrated_q0_min,
        "CALIBRATED_Q0_MAX": calibrated_q0_max,
        "ALPHA": alpha,
        "EPS_KAPPA": float(eps_kappa),
        "WEIGHT_THRESHOLD": threshold
    }
}

with open("out/geometry_constants_from_dist_all.json", "w") as f:
    json.dump(output_data, f, indent=2)

print(f"\n[SAVED] out/geometry_constants_from_dist_all.json")

# ===================================================================
# 7. VISUALIZATION
# ===================================================================
print("\n[VISUALIZATION]")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle("SH Gate Calibration: ATLAS vs dist_all vs Calibrated", fontsize=14)

# Plot 1: w_atlas
ax = axes[0, 0]
im1 = ax.contourf(R_grid, Q0_grid, W_atlas, levels=20, cmap='Blues')
ax.scatter([R_REF], [Q0_REF], color='red', s=100, marker='X')
ax.set_xlabel('r')
ax.set_ylabel('q0')
ax.set_title(f'w_atlas\nσL={sigma_L:.4f}, σR={sigma_R:.4f}')
plt.colorbar(im1, ax=ax)

# Plot 2: w_kappa
ax = axes[0, 1]
im2 = ax.contourf(R_grid, Q0_grid, W_kappa, levels=20, cmap='Greens')
ax.scatter(df["r"], df["q0"], c=df["kappa_tda"], cmap='RdYlGn', s=5, alpha=0.3)
ax.scatter([R_REF], [Q0_REF], color='red', s=100, marker='X')
ax.set_xlabel('r')
ax.set_ylabel('q0')
ax.set_title(f'w_kappa\nε={eps_kappa:.4f}')
plt.colorbar(im2, ax=ax)

# Plot 3: w_gate
ax = axes[0, 2]
im3 = ax.contourf(R_grid, Q0_grid, W_gate, levels=20, cmap='plasma')
ax.contour(R_grid, Q0_grid, W_gate, levels=[threshold], colors='red', linewidths=2)
ax.scatter([calibrated_r_star], [calibrated_q0_star], color='cyan', s=150, marker='*', 
           edgecolors='black', linewidths=2)
ax.scatter([R_REF], [Q0_REF], color='red', s=100, marker='X')
ax.set_xlabel('r')
ax.set_ylabel('q0')
ax.set_title(f'w_gate = w_atlas^0.5 × w_kappa^0.5')
plt.colorbar(im3, ax=ax)

# Plot 4: Band comparison
ax = axes[1, 0]
# ATLAS band (shifted)
r_atlas_shifted_min = SH_BOUNDARY_MIN + delta_r
r_atlas_shifted_max = SH_BOUNDARY_MAX + delta_r
ax.fill_betweenx([q0_min, q0_max], r_atlas_shifted_min, r_atlas_shifted_max, 
                  alpha=0.3, color='blue', label='ATLAS (shifted)')
# dist band
ax.fill_betweenx([q0_min, q0_max], SH_R_BAND_MIN, SH_R_BAND_MAX, 
                  alpha=0.3, color='green', label='dist band')
# Calibrated
ax.fill_betweenx([q0_min, q0_max], calibrated_r_min, calibrated_r_max, 
                  alpha=0.3, color='purple', label='Calibrated')
ax.scatter(df["r"], df["q0"], c='lightgray', s=3, alpha=0.5)
ax.scatter([R_REF], [Q0_REF], color='red', s=100, marker='X', label='Reference')
ax.set_xlabel('r')
ax.set_ylabel('q0')
ax.set_title('Band Comparison')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 5: Cross-section
ax = axes[1, 1]
q0_idx = np.argmin(np.abs(q0_grid - Q0_REF))
ax.plot(r_grid, W_atlas[q0_idx, :], 'b-', label='w_atlas', linewidth=2)
ax.plot(r_grid, W_kappa[q0_idx, :], 'g-', label='w_kappa', linewidth=2)
ax.plot(r_grid, W_gate[q0_idx, :], 'm-', label='w_gate', linewidth=2)
ax.axvline(calibrated_r_star, color='purple', linestyle='--', label='calibrated r*')
ax.axvline(R_REF, color='red', linestyle=':', label='R_REF')
ax.set_xlabel('r')
ax.set_ylabel('weight')
ax.set_title(f'Cross-section at q0={Q0_REF:.3f}')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 6: Summary
ax = axes[1, 2]
ax.axis('off')
summary = f"""
[CALIBRATION RESULTS]

Shift:
  Δr = {delta_r:+.6f}
  Δq = {delta_q:+.6f}

Scale:
  s_L = {s_L:.6f} → σL = {sigma_L:.6f}
  s_R = {s_R:.6f} → σR = {sigma_R:.6f}

Calibrated Constants:
  SH_R_STAR: {calibrated_r_star:.6f}
  SH_Q0_STAR: {calibrated_q0_star:.6f}
  BOUNDARY: [{calibrated_r_min:.6f}, {calibrated_r_max:.6f}]
  SIGMA_L/R: {cal_sigma_l:.6f}, {cal_sigma_r:.6f}

Comparison:
  Original R_REF: {R_REF:.6f}
  Calibrated r*:  {calibrated_r_star:.6f}
  Error: {abs(calibrated_r_star - R_REF):.6f}
"""
ax.text(0.05, 0.95, summary, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig("out/sh_gate_calibration.png", dpi=150, bbox_inches='tight')
print("[SAVED] out/sh_gate_calibration.png")

print("\n" + "=" * 70)
print("CALIBRATION COMPLETE")
print("=" * 70)
