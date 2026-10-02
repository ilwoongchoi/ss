# master_equation_ness_solver.py
# THE FLASH: Quasar Isomorphism Simulation with Kappa TDA Dynamics
# 
# MATHEMATICAL FRAMEWORK:
# - South Pole (BM+SW): Accretion Disk with 3/32 Filter
# - North Pole (SM): Relativistic Jet Output
# - Flash: Eyring-Kramers Escape Rate (kappa_eff-adjusted)
# - Void (BW): Hodge Harmonic Background
# - Kappa TDA: Data-driven geometry gate from dist_all.csv

import numpy as np
import matplotlib.pyplot as plt
import os
import time
import json

from geometry_package import universal_equation as unieq
from geometry_package.universal_equation import DynamicsHooks, kappa_eff, in_sh_band, lookup_p_from_rq0
from geometry_package.absolute_constants import (
    TUNNEL_TENSION, 
    TOTAL_DEBT_AREA,
    RENORMALIZATION_BRIDGE,
    PHI_PB,
    OMEGA_LA,
    LATTICE_3_32,
    BETTI_11,
    BETTI_7,
    SPARK_ANGLE_DEG,
    CHIRALITY_CONSTANT,
    SPARK_LEAP_DIST,
    R_REF,
    Q0_REF,
    SH_R_BAND_MIN,
    SH_R_BAND_MAX,
    SH_Q0_MIN,
    SH_Q0_MAX,
    KAPPA_TDA_MID,
)

# ===================================================================
# SIMULATION SETTINGS
# ===================================================================
dt = 0.01               # Time step
t_max = 800.0           # Total simulation time
steps = int(t_max / dt)
t_arr = np.linspace(0, t_max, steps)

# Stochastic parameter
KAPPA_NOISE = 0.02

# Current (r, q0) position for kappa_eff lookup
# Using reference position - in real usage, this comes from trajectory
CURRENT_R = R_REF       # 0.1117
CURRENT_Q0 = Q0_REF     # 0.975

# ===================================================================
# STATE VECTORS
# ===================================================================
psi_x = np.zeros(steps)         # System State
psi_y = np.zeros(steps)         # System Phase
renorm_gain = np.ones(steps)    # Renormalization Operator Gain

# Initial conditions
psi_x[0] = 0.5
psi_y[0] = 0.0
renorm_gain[0] = 1.0

# Tracking
flash_events = []
flash_residuals = []

# ===================================================================
# KAPPA EFF LOOKUP (once at start)
# ===================================================================
print("=" * 60)
print("QUASAR ISOMORPHISM SIMULATION (Kappa TDA Edition)")
print("=" * 60)

# Get kappa_eff for current position
current_kappa = kappa_eff(CURRENT_R, CURRENT_Q0)
in_band = in_sh_band(CURRENT_R, CURRENT_Q0)

print(f"\n[POSITION]")
print(f"  r = {CURRENT_R:.6f}, q0 = {CURRENT_Q0:.6f}")
print(f"  In SH Band: {in_band}")
print(f"  kappa_eff = {current_kappa:.6f} (1/32 = {KAPPA_TDA_MID:.6f})")

# Get cell info from dist_all
cell_info = lookup_p_from_rq0(CURRENT_R, CURRENT_Q0)
if cell_info:
    print(f"  Nearest cell p = {cell_info['p']:.6f}, distance = {cell_info['distance']:.6f}")

print(f"\n[DYNAMICS HOOKS]")
print(f"  Spark threshold (base): {TUNNEL_TENSION:.6f}")
print(f"  Spark threshold (kappa-adjusted): {DynamicsHooks.spark_threshold(current_kappa):.6f}")
print(f"  Renorm recovery rate (base): 0.05")
print(f"  Renorm recovery rate (kappa-adjusted): {DynamicsHooks.renorm_recovery_rate(current_kappa):.6f}")

# Log hypothesis
print(f"\n[HYPOTHESIS - NOT VALIDATED]")
hypothesis = DynamicsHooks.log_maxwell_flash_hypothesis()

print("-" * 60)

# ===================================================================
# THE FLASH SIMULATION LOOP (with Kappa TDA dynamics)
# ===================================================================

for i in range(1, steps):
    t = t_arr[i-1]
    
    # 1. QUASAR FORCES
    south_pressure = unieq.get_south_pole_pressure(t)
    north_jet = unieq.get_north_pole_jet(t)
    total_force = south_pressure + north_jet
    
    # 2. SW FILTER
    filtered_force = unieq.sw_filter_kernel(total_force, t)
    
    # 3. KAPTA-EFF DYNAMICS CONNECTION (A): Spark Threshold
    # Adjust threshold based on kappa_eff
    spark_threshold = DynamicsHooks.spark_threshold(current_kappa, TUNNEL_TENSION)
    
    # 4. RENORMALIZATION (Kappa TDA Connection B)
    force_after_renorm = filtered_force * renorm_gain[i-1]
    
    # Adjust recovery rate based on kappa_eff
    recovery_rate = DynamicsHooks.renorm_recovery_rate(current_kappa, 0.05)
    renorm_gain[i] = renorm_gain[i-1] + (1.0 - renorm_gain[i-1]) * recovery_rate
    
    # 5. UPDATE STATE (Kappa TDA Connection C: damping)
    # Add damping term calibrated by kappa_eff
    damping = DynamicsHooks.damping_term(psi_x[i-1], current_kappa, use_sw_calibration=False)
    
    dpsi_x = force_after_renorm + damping
    psi_x[i] = psi_x[i-1] + dpsi_x * dt
    
    # Phase rotation
    omega_phase = 2.0 * np.pi / (16.0 * 2.317)
    psi_y[i] = psi_y[i-1] + omega_phase * dt + 0.1 * dpsi_x * dt
    
    # 6. SPARK EVENT (with kappa-adjusted threshold)
    current_tension = abs(psi_x[i])
    flash_rate = unieq.get_flash_probability(current_tension, kappa_noise=KAPPA_NOISE)
    
    if np.random.random() < (flash_rate * dt):
        # FLASH!
        flash_events.append({
            'time': t,
            'tension_before': current_tension,
            'state_before': psi_x[i],
            'renorm_before': renorm_gain[i],
            'kappa_at_flash': current_kappa,
            'in_band': in_band
        })
        
        x_before = psi_x[i]
        
        # Refraction
        psi_x[i] = -psi_x[i] * 0.7
        psi_y[i] += np.pi / 2.0
        
        # Record residual
        dx_leap = SPARK_LEAP_DIST * np.cos(np.radians(SPARK_ANGLE_DEG))
        x_compressed = psi_x[i] - dx_leap
        residual = x_before - x_compressed
        flash_residuals.append(residual)
        
        # Renormalization reset
        renorm_gain[i] = 1.0 / (1.0 + np.log10(RENORMALIZATION_BRIDGE))
        
        flash_events[-1]['state_after'] = psi_x[i]
        flash_events[-1]['renorm_after'] = renorm_gain[i]

# ===================================================================
# STATISTICS
# ===================================================================
print(f"\n[RESULTS]")
print(f"Total Flash Events: {len(flash_events)}")
print(f"Flash Rate: {len(flash_events) / t_max:.4f} per unit time")

if flash_residuals:
    residuals = np.array(flash_residuals)
    print(f"Filter Residual Mean: {np.mean(residuals):.6f}")
    print(f"Filter Residual Std: {np.std(residuals):.6f}")
    
    # Update SW residual stats for future calibration
    DynamicsHooks.SW_RESIDUAL_MEAN = float(np.mean(residuals))
    DynamicsHooks.SW_RESIDUAL_STD = float(np.std(residuals))

print(f"Max State Value: {np.max(np.abs(psi_x)):.6f}")
print(f"Final State: {psi_x[-1]:.6f}")

# ===================================================================
# VISUALIZATION
# ===================================================================
fig = plt.figure(figsize=(18, 12), facecolor="#0a0a14")
fig.suptitle(f"QUASAR ISOMORPHISM: Kappa TDA Dynamics\n"
             f"r={CURRENT_R:.4f}, q0={CURRENT_Q0:.4f}, kappa={current_kappa:.4f}, "
             f"InBand={in_band}",
             color="white", fontsize=14)

gs = plt.GridSpec(3, 2, height_ratios=[2, 1, 1])

# PLOT 1: Main trajectory
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t_arr, psi_x, color="#00ffff", lw=0.8, alpha=0.9, label=r"$\Psi_x$")
ax1.axhline(y=spark_threshold, color="red", ls="--", alpha=0.5, 
            label=f"Threshold ({spark_threshold:.3f})")
ax1.axhline(y=-spark_threshold, color="red", ls="--", alpha=0.5)

for flash in flash_events:
    ax1.axvline(x=flash['time'], color="#ff6600", ls="-", alpha=0.3, lw=0.5)

ax1.set_title("Trajectory (Kappa-Adjusted Threshold)", color="white")
ax1.set_xlabel("Time", color="#cccccc")
ax1.set_ylabel(r"State ($\Psi_x$)", color="#cccccc")
ax1.set_facecolor("#050510")
ax1.tick_params(colors='white')
ax1.legend(loc="upper right", facecolor="#050510", labelcolor="white")
ax1.grid(color='#111122', ls='-', lw=0.5)

# PLOT 2: Phase space
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(psi_x, psi_y, color="#00ff88", lw=0.5, alpha=0.7)
ax2.scatter(psi_x[0], psi_y[0], color="green", s=50, zorder=5, label="Start")
ax2.scatter(psi_x[-1], psi_y[-1], color="red", s=50, zorder=5, label="End")

for flash in flash_events:
    idx = int(flash['time'] / dt)
    if idx < len(psi_x):
        ax2.scatter(psi_x[idx], psi_y[idx], color="#ff6600", s=20, alpha=0.7, zorder=4)

ax2.set_title("Phase Space (The Wormhole)", color="white")
ax2.set_xlabel(r"$\Psi_x$", color="#cccccc")
ax2.set_ylabel(r"$\Psi_y$", color="#cccccc")
ax2.set_facecolor("#050510")
ax2.tick_params(colors='white')
ax2.legend(loc="upper right", facecolor="#050510", labelcolor="white")
ax2.grid(color='#111122', ls='-', lw=0.5)

# PLOT 3: Renormalization Gain
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(t_arr, renorm_gain, color="#ff4444", lw=1.0, label="Gain")
ax3.axhline(y=1.0, color="white", ls="--", alpha=0.3, lw=1)

for flash in flash_events:
    ax3.axvline(x=flash['time'], color="#ff6600", ls="-", alpha=0.3, lw=0.5)

ax3.set_title(f"Renormalization (Recovery Rate: {recovery_rate:.4f})", color="white")
ax3.set_xlabel("Time", color="#cccccc")
ax3.set_ylabel("Gain", color="#cccccc")
ax3.set_facecolor("#050510")
ax3.tick_params(colors='white')
ax3.legend(loc="upper right", facecolor="#050510", labelcolor="white")
ax3.grid(color='#111122', ls='-', lw=0.5)

# PLOT 4: Flash Residuals
ax4 = fig.add_subplot(gs[1, 1])
if flash_residuals:
    ax4.hist(flash_residuals, bins=30, color="#9966ff", alpha=0.7, edgecolor="white")
    ax4.axvline(x=np.mean(flash_residuals), color="red", ls="--", lw=2, 
                label=f"Mean: {np.mean(flash_residuals):.4f}")
    ax4.set_title(f"SW Residuals (n={len(flash_residuals)})", color="white")
else:
    ax4.text(0.5, 0.5, "No Flash Events", ha='center', va='center', 
             transform=ax4.transAxes, color='white', fontsize=12)
    ax4.set_title("SW Filter Residuals", color="white")

ax4.set_xlabel("Residual", color="#cccccc")
ax4.set_ylabel("Count", color="#cccccc")
ax4.set_facecolor("#050510")
ax4.tick_params(colors='white')
if flash_residuals:
    ax4.legend(loc="upper right", facecolor="#050510", labelcolor="white")
ax4.grid(color='#111122', ls='-', lw=0.5)

# PLOT 5: Kappa Info Text
ax5 = fig.add_subplot(gs[2, 0])
ax5.axis('off')
info_text = f"""
[KAPPA TDA PARAMETERS]
Position: r={CURRENT_R:.6f}, q0={CURRENT_Q0:.6f}
In SH Band: {in_band} (r in [{SH_R_BAND_MIN},{SH_R_BAND_MAX}], q0 in [{SH_Q0_MIN},{SH_Q0_MAX}])
kappa_eff: {current_kappa:.6f}

[DYNAMICS HOOKS]
(A) Spark Threshold: {spark_threshold:.6f} (base: {TUNNEL_TENSION:.6f})
(B) Recovery Rate: {recovery_rate:.6f} (base: 0.05)
(C) Damping: kappa-adjusted {'+ SW calibrated' if DynamicsHooks.SW_RESIDUAL_STD > 0 else ''}

[HYPOTHESIS - NOT VALIDATED]
Out-band flash rate (0.0118) × Maxwell Q (11.8) = 0.139
1/BETTI_7 = {1.0/BETTI_7:.4f}
Match: {abs(0.0118 * 11.8 - 1.0/BETTI_7) < 0.05}
"""
ax5.text(0.1, 0.5, info_text, transform=ax5.transAxes, fontsize=10,
         color='white', verticalalignment='center', fontfamily='monospace')

# PLOT 6: Flash Event Table
ax6 = fig.add_subplot(gs[2, 1])
ax6.axis('off')
if flash_events:
    table_data = []
    for i, flash in enumerate(flash_events[:5]):  # First 5 events
        table_data.append([
            f"{flash['time']:.1f}",
            f"{flash['tension_before']:.3f}",
            f"{flash['kappa_at_flash']:.4f}",
            "Yes" if flash['in_band'] else "No"
        ])
    
    table = ax6.table(cellText=table_data,
                      colLabels=['Time', 'Tension', 'Kappa', 'In Band'],
                      cellLoc='center',
                      loc='center',
                      colColours=['#333355']*4)
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    
    for key, cell in table.get_celld().items():
        cell.set_text_props(color='white')
        if key[0] == 0:
            cell.set_facecolor('#444466')
        else:
            cell.set_facecolor('#222233')
    
    ax6.set_title(f"First 5 Flash Events (of {len(flash_events)})", color='white', y=0.95)
else:
    ax6.text(0.5, 0.5, "No Flash Events", ha='center', va='center',
             transform=ax6.transAxes, color='white', fontsize=12)

plt.tight_layout()

# Save
timestamp = time.strftime("%Y%m%d-%H%M%S")
output_path = f"QUASAR_KAPPA_TDA_{timestamp}.png"
plt.savefig(output_path, dpi=300, facecolor="#0a0a14")
print(f"\n[SAVED] {output_path}")

# Save data
if flash_events:
    with open(f"flash_events_kappa_{timestamp}.json", 'w') as f:
        json.dump({
            'flash_events': flash_events,
            'parameters': {
                'r': CURRENT_R,
                'q0': CURRENT_Q0,
                'kappa_eff': current_kappa,
                'in_band': in_band,
                'spark_threshold': spark_threshold,
                'recovery_rate': recovery_rate,
            }
        }, f, indent=2)

plt.show()
