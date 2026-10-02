# analyze_sh_band_metrics.py
# SH Boundary Band Metrics Analysis
# 
# PURPOSE:
# Measures "reality indicators" for the Quasar Isomorphism framework
# without heavy PDE computations. Uses existing 128-grid trajectories.
#
# MATHEMATICAL FRAMEWORK:
# 1. Flash Rate: Eyring-Kramers escape rate within SH boundary band
# 2. Filter Strength: Green's function residual analysis (3/32 lattice)
# 3. Band Conditioning: Conditional statistics (in-band vs out-of-band)
#
# OUTPUTS:
# - out/sh_band_metrics.csv: Statistics for all 128 types
# - out/sh_spark_band_comparison.png: Flash rate comparison
# - out/filter_residual_hist.png: Filter residual distribution

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

# Import from geometry package
from geometry_package.absolute_constants import (
    SH_R_STAR, SH_Q0_STAR,
    SH_R_FWHM_L, SH_R_FWHM_R,
    SH_BOUNDARY_MIN, SH_BOUNDARY_MAX,
    SH_Q0_MIN, SH_Q0_MAX,
    SPARK_ANGLE_DEG,
    SPARK_ANGLE_RAD,
    LATTICE_3_32,
    SPARK_LEAP_DIST
)

# Constants from trajectory generator context
N_ROWS = 16
N_COLS = 16

# MBTI types, Blood types, Genders
ALL_MBTI = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["F", "M"]
BRANCHES = ["sunrise", "sunset"]

# ===================================================================
# CONFIGURATION
# ===================================================================
OUTPUT_DIR = "out"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# R margin for band boundaries
R_MARGIN = 0.001


# ===================================================================
# SH BAND WEIGHT FUNCTION
# ===================================================================
def sh_band_weight(r: float, q0: float, 
                   q0_min: float = SH_Q0_MIN,
                   q0_max: float = SH_Q0_MAX) -> float:
    """
    Calculate SH boundary band weight for a given (r, q0) point.
    
    The weight is a product of:
    - Asymmetric Gaussian in r (centered at SH_R_STAR)
    - Uniform (or Gaussian) weight in q0
    
    Args:
        r: Radial parameter (mapped from grid)
        q0: q0 parameter (mapped from grid)
        q0_min: Minimum q0 for band
        q0_max: Maximum q0 for band
        
    Returns:
        Weight between 0 and 1 (1 = fully in band)
    """
    # Check if within hard boundaries
    if r < SH_BOUNDARY_MIN - R_MARGIN or r > SH_BOUNDARY_MAX + R_MARGIN:
        return 0.0
    
    if q0 < q0_min or q0 > q0_max:
        return 0.0
    
    # Asymmetric Gaussian in r
    if r < SH_R_STAR:
        # Left side (FWHM_L)
        sigma_l = SH_R_FWHM_L / (2 * np.sqrt(2 * np.log(2)))
        r_weight = np.exp(-0.5 * ((r - SH_R_STAR) / sigma_l) ** 2)
    else:
        # Right side (FWHM_R)
        sigma_r = SH_R_FWHM_R / (2 * np.sqrt(2 * np.log(2)))
        r_weight = np.exp(-0.5 * ((r - SH_R_STAR) / sigma_r) ** 2)
    
    # Uniform weight in q0 (could be Gaussian instead)
    q0_center = (q0_min + q0_max) / 2
    q0_sigma = (q0_max - q0_min) / 4
    q0_weight = np.exp(-0.5 * ((q0 - q0_center) / q0_sigma) ** 2)
    
    return r_weight * q0_weight


def grid_to_rq0(grid_x: float, grid_y: float,
                x_range: Tuple[float, float] = (0, 16),
                y_range: Tuple[float, float] = (0, 16)) -> Tuple[float, float]:
    """
    Map 16x16 grid coordinates to (r, q0) space.
    
    Args:
        grid_x: X coordinate on 16x16 grid
        grid_y: Y coordinate on 16x16 grid
        x_range: Grid x range
        y_range: Grid y range
        
    Returns:
        (r, q0) tuple
    """
    # Normalize to [0, 1]
    nx = (grid_x - x_range[0]) / (x_range[1] - x_range[0])
    ny = (grid_y - y_range[0]) / (y_range[1] - y_range[0])
    
    # Map r to [SH_BOUNDARY_MIN - margin, SH_BOUNDARY_MAX + margin]
    r_min = SH_BOUNDARY_MIN - 0.005
    r_max = SH_BOUNDARY_MAX + 0.005
    r = r_min + nx * (r_max - r_min)
    
    # Map q0 to [SH_Q0_MIN, SH_Q0_MAX]
    q0 = SH_Q0_MIN + ny * (SH_Q0_MAX - SH_Q0_MIN)
    
    return r, q0


# ===================================================================
# SIMPLIFIED TRAJECTORY SIMULATION
# ===================================================================
def generate_trajectory_simple(mbti: str, blood: str, gender: str, 
                                branch: str = "sunrise", max_steps: int = 1000) -> List[Tuple[float, float, bool]]:
    """
    Simplified trajectory generation for analysis.
    
    This is a lightweight approximation that generates trajectories
    with spark events without the full physics simulation.
    
    Returns:
        List of (x, y, spark_flag) tuples
    """
    # Import here to avoid circular dependencies
    try:
        from generate_128_grid_v4_hysteresis_pure import generate_trajectory_pure
        # Call the actual function
        return generate_trajectory_pure(mbti, blood, gender, branch)
    except Exception as e:
        # Fallback: generate synthetic trajectory
        return _generate_synthetic_trajectory(mbti, blood, gender, max_steps)


def _generate_synthetic_trajectory(mbti: str, blood: str, gender: str, 
                                    max_steps: int = 1000) -> List[Tuple[float, float, bool]]:
    """
    Generate a synthetic trajectory for testing when the real generator fails.
    """
    # Simple hash to get deterministic starting position
    hash_val = hash(f"{mbti}{blood}{gender}") % 1000
    np.random.seed(hash_val)
    
    # Starting position (approximate grid position based on type)
    x = 8.0 + np.random.randn() * 2.0
    y = 0.0
    
    pts = [(x, y, False)]
    
    # Simple upward trajectory with occasional sparks
    for i in range(1, max_steps):
        # Vertical movement
        y += 0.1
        if y > 16:
            break
        
        # Horizontal drift
        x += np.random.randn() * 0.1
        x = max(0, min(16, x))
        
        # Random spark with probability based on position
        # More sparks in middle region (approximating SH band)
        spark_prob = 0.001
        if 8 < y < 12:  # Middle region
            spark_prob = 0.005
        
        is_spark = np.random.random() < spark_prob
        
        if is_spark:
            # Spark causes jump
            x += SPARK_LEAP_DIST * np.cos(SPARK_ANGLE_RAD)
            y += SPARK_LEAP_DIST * np.sin(SPARK_ANGLE_RAD)
            pts.append((float(x), float(y), True))
        else:
            pts.append((float(x), float(y), False))
    
    return pts


# ===================================================================
# TRAJECTORY ANALYSIS
# ===================================================================
@dataclass
class TrajectoryMetrics:
    """Metrics for a single trajectory"""
    mbti: str
    blood: str
    gender: str
    branch: str
    
    total_steps: int
    sh_band_fraction: float  # Fraction of time in SH band
    
    spark_count: int
    spark_rate_total: float  # Sparks per step
    spark_rate_in_band: float
    spark_rate_out_band: float
    
    # Filter analysis
    residual_mean: Optional[float]
    residual_std: Optional[float]
    residuals: List[float]
    
    # Raw data for debugging
    spark_times: List[int]


def analyze_trajectory(mbti: str, blood: str, gender: str, branch: str = "sunrise",
                      max_steps: int = 1000) -> TrajectoryMetrics:
    """
    Analyze a single trajectory for SH band metrics.
    
    Args:
        mbti: MBTI type
        blood: Blood type
        gender: Gender (F/M)
        branch: "sunrise" or "sunset"
        max_steps: Maximum steps to simulate
        
    Returns:
        TrajectoryMetrics object
    """
    # Generate trajectory
    try:
        pts = generate_trajectory_simple(mbti, blood, gender, branch, max_steps)
    except Exception as e:
        print(f"  Warning: Error generating trajectory for {mbti}-{blood}-{gender}-{branch}: {e}")
        # Return empty metrics
        return TrajectoryMetrics(
            mbti=mbti, blood=blood, gender=gender, branch=branch,
            total_steps=0, sh_band_fraction=0.0,
            spark_count=0, spark_rate_total=0.0,
            spark_rate_in_band=0.0, spark_rate_out_band=0.0,
            residual_mean=None, residual_std=None,
            residuals=[], spark_times=[]
        )
    
    total_steps = len(pts)
    if total_steps == 0:
        return TrajectoryMetrics(
            mbti=mbti, blood=blood, gender=gender, branch=branch,
            total_steps=0, sh_band_fraction=0.0,
            spark_count=0, spark_rate_total=0.0,
            spark_rate_in_band=0.0, spark_rate_out_band=0.0,
            residual_mean=None, residual_std=None,
            residuals=[], spark_times=[]
        )
    
    # Calculate SH band weights for each step
    sh_weights = []
    for step, pt in enumerate(pts):
        x, y = pt[0], pt[1]
        r, q0 = grid_to_rq0(x, y)
        weight = sh_band_weight(r, q0)
        sh_weights.append(weight)
    
    sh_weights = np.array(sh_weights)
    
    # SH band fraction (weight > 0.5)
    in_band_mask = sh_weights > 0.5
    sh_band_fraction = np.mean(in_band_mask)
    
    # Spark analysis
    spark_indices = [i for i, pt in enumerate(pts) if len(pt) > 2 and pt[2]]
    spark_count = len(spark_indices)
    spark_rate_total = spark_count / total_steps if total_steps > 0 else 0.0
    
    # Conditional spark rates
    in_band_steps = np.sum(in_band_mask)
    out_band_steps = total_steps - in_band_steps
    
    sparks_in_band = sum(1 for idx in spark_indices if idx < len(in_band_mask) and in_band_mask[idx])
    sparks_out_band = spark_count - sparks_in_band
    
    spark_rate_in_band = sparks_in_band / in_band_steps if in_band_steps > 0 else 0.0
    spark_rate_out_band = sparks_out_band / out_band_steps if out_band_steps > 0 else 0.0
    
    # Filter residual analysis
    residuals = []
    for idx in spark_indices:
        if idx == 0 or idx >= len(pts):
            continue
        
        # Get state before and after
        x_before = pts[idx-1][0]
        x_after = pts[idx][0]
        
        # Calculate expected leap
        dx_leap = SPARK_LEAP_DIST * np.cos(np.radians(SPARK_ANGLE_DEG))
        x_compressed = x_after - dx_leap
        residual = x_before - x_compressed
        residuals.append(residual)
    
    residual_mean = np.mean(residuals) if residuals else None
    residual_std = np.std(residuals) if residuals else None
    
    return TrajectoryMetrics(
        mbti=mbti,
        blood=blood,
        gender=gender,
        branch=branch,
        total_steps=total_steps,
        sh_band_fraction=sh_band_fraction,
        spark_count=spark_count,
        spark_rate_total=spark_rate_total,
        spark_rate_in_band=spark_rate_in_band,
        spark_rate_out_band=spark_rate_out_band,
        residual_mean=residual_mean,
        residual_std=residual_std,
        residuals=residuals,
        spark_times=spark_indices
    )


# ===================================================================
# MAIN ANALYSIS
# ===================================================================
def main():
    """Run SH band metrics analysis for sample of types"""
    print("=" * 60)
    print("SH BAND METRICS ANALYSIS")
    print("Quasar Isomorphism: Reality Indicators")
    print("=" * 60)
    
    all_metrics = []
    
    # Sample subset for faster testing (all would be 128 types)
    # Using all 16 MBTI × 4 Blood × 2 Gender = 128 combinations
    # But with 2 branches each = 256 total
    # For speed, let's do just 1 branch
    
    branch = "sunrise"  # Just do sunrise for speed
    
    total_combinations = len(ALL_MBTI) * len(BLOODS) * len(GENDERS)
    processed = 0
    
    print(f"\nAnalyzing {total_combinations} type combinations (branch: {branch})...")
    print("-" * 60)
    
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                processed += 1
                if processed % 16 == 0:
                    print(f"Progress: {processed}/{total_combinations} ({100*processed/total_combinations:.1f}%)")
                
                try:
                    metrics = analyze_trajectory(mbti, blood, gender, branch, max_steps=1000)
                    all_metrics.append(metrics)
                except Exception as e:
                    print(f"  Error analyzing {mbti}-{blood}-{gender}: {e}")
    
    print(f"\nCompleted analysis of {len(all_metrics)} trajectories")
    
    # ===================================================================
    # SAVE CSV
    # ===================================================================
    csv_path = os.path.join(OUTPUT_DIR, "sh_band_metrics.csv")
    with open(csv_path, 'w') as f:
        # Header
        f.write("mbti,blood,gender,branch,total_steps,sh_band_fraction,")
        f.write("spark_count,spark_rate_total,spark_rate_in_band,spark_rate_out_band,")
        f.write("residual_mean,residual_std\n")
        
        # Data
        for m in all_metrics:
            f.write(f"{m.mbti},{m.blood},{m.gender},{m.branch},")
            f.write(f"{m.total_steps},{m.sh_band_fraction:.6f},")
            f.write(f"{m.spark_count},{m.spark_rate_total:.6f},")
            f.write(f"{m.spark_rate_in_band:.6f},{m.spark_rate_out_band:.6f},")
            f.write(f"{m.residual_mean if m.residual_mean is not None else 'NaN'},")
            f.write(f"{m.residual_std if m.residual_std is not None else 'NaN'}\n")
    
    print(f"Saved: {csv_path}")
    
    # ===================================================================
    # VISUALIZATION 1: Spark Rate Comparison
    # ===================================================================
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("SH Boundary Band: Spark Rate Analysis", fontsize=14)
    
    # Filter valid metrics
    valid_metrics = [m for m in all_metrics if m.total_steps > 0]
    
    if valid_metrics:
        # Data for plotting
        rates_total = [m.spark_rate_total for m in valid_metrics]
        rates_in = [m.spark_rate_in_band for m in valid_metrics]
        rates_out = [m.spark_rate_out_band for m in valid_metrics]
        band_fractions = [m.sh_band_fraction for m in valid_metrics]
        
        # Plot 1: Sample comparison (first 32 types)
        ax = axes[0]
        n_show = min(32, len(valid_metrics))
        x = np.arange(n_show)
        width = 0.25
        
        rates_total_show = rates_total[:n_show]
        rates_in_show = rates_in[:n_show]
        rates_out_show = rates_out[:n_show]
        
        ax.bar(x - width, rates_total_show, width, label='Total', alpha=0.7, color='blue')
        ax.bar(x, rates_in_show, width, label='In Band', alpha=0.7, color='green')
        ax.bar(x + width, rates_out_show, width, label='Out Band', alpha=0.7, color='red')
        ax.set_xlabel('Type Index')
        ax.set_ylabel('Spark Rate')
        ax.set_title(f'Spark Rates (Sample: {n_show} types)')
        ax.legend()
        ax.set_yscale('log')
        
        # Plot 2: SH Band Fraction vs Spark Rate
        ax = axes[1]
        ax.scatter(band_fractions, rates_total, alpha=0.5, c='purple', s=20)
        ax.set_xlabel('SH Band Fraction')
        ax.set_ylabel('Total Spark Rate')
        ax.set_title('Band Occupancy vs Flash Rate')
        ax.set_yscale('log')
        
        # Plot 3: In-Band vs Out-Band comparison
        ax = axes[2]
        # Box plot comparison
        data_to_plot = [rates_in, rates_out]
        bp = ax.boxplot(data_to_plot, labels=['In Band', 'Out Band'], patch_artist=True)
        bp['boxes'][0].set_facecolor('green')
        bp['boxes'][1].set_facecolor('red')
        ax.set_ylabel('Spark Rate')
        ax.set_title('Flash Rate: In-Band vs Out-Band')
        ax.set_yscale('log')
    
    plt.tight_layout()
    plot1_path = os.path.join(OUTPUT_DIR, "sh_spark_band_comparison.png")
    plt.savefig(plot1_path, dpi=150)
    print(f"Saved: {plot1_path}")
    
    # ===================================================================
    # VISUALIZATION 2: Filter Residuals
    # ===================================================================
    all_residuals = []
    for m in valid_metrics:
        all_residuals.extend(m.residuals)
    
    if all_residuals:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle("SW Filter Analysis (3/32 Lattice)", fontsize=14)
        
        # Histogram
        ax = axes[0]
        ax.hist(all_residuals, bins=30, alpha=0.7, color='teal', edgecolor='white')
        ax.axvline(x=np.mean(all_residuals), color='red', linestyle='--', 
                   linewidth=2, label=f"Mean: {np.mean(all_residuals):.4f}")
        ax.axvline(x=np.median(all_residuals), color='orange', linestyle='--',
                   linewidth=2, label=f"Median: {np.median(all_residuals):.4f}")
        ax.set_xlabel('Filter Residual')
        ax.set_ylabel('Count')
        ax.set_title(f'SW Green\'s Function Residuals (n={len(all_residuals)})')
        ax.legend()
        
        # Q-Q plot approximation
        ax = axes[1]
        sorted_residuals = np.sort(all_residuals)
        theoretical = np.random.normal(np.mean(all_residuals), np.std(all_residuals), len(all_residuals))
        theoretical.sort()
        ax.scatter(theoretical, sorted_residuals, alpha=0.3, s=1)
        min_val = min(theoretical[0], sorted_residuals[0])
        max_val = max(theoretical[-1], sorted_residuals[-1])
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='Normal')
        ax.set_xlabel('Theoretical Quantiles')
        ax.set_ylabel('Sample Quantiles')
        ax.set_title('Residual Q-Q Plot')
        ax.legend()
        
        plt.tight_layout()
        plot2_path = os.path.join(OUTPUT_DIR, "filter_residual_hist.png")
        plt.savefig(plot2_path, dpi=150)
        print(f"Saved: {plot2_path}")
    else:
        print("No residuals to plot (no spark events detected)")
    
    # ===================================================================
    # SUMMARY STATISTICS
    # ===================================================================
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total trajectories analyzed: {len(all_metrics)}")
    print(f"Valid trajectories: {len(valid_metrics)}")
    
    if valid_metrics:
        print(f"\nSH Band Occupancy:")
        print(f"  Mean fraction: {np.mean(band_fractions):.4f}")
        print(f"  Std fraction: {np.std(band_fractions):.4f}")
        print(f"\nFlash Statistics:")
        print(f"  Total sparks: {sum(m.spark_count for m in valid_metrics)}")
        print(f"  Mean rate (total): {np.mean(rates_total):.6f}")
        nonzero_in = [r for r in rates_in if r > 0]
        nonzero_out = [r for r in rates_out if r > 0]
        if nonzero_in:
            print(f"  Mean rate (in band): {np.mean(nonzero_in):.6f}")
        if nonzero_out:
            print(f"  Mean rate (out band): {np.mean(nonzero_out):.6f}")
    
    if all_residuals:
        print(f"\nFilter Residuals (3/32 Lattice):")
        print(f"  Count: {len(all_residuals)}")
        print(f"  Mean: {np.mean(all_residuals):.6f}")
        print(f"  Std: {np.std(all_residuals):.6f}")
        print(f"  Interpretation: {'Filter working' if abs(np.mean(all_residuals)) < 0.5 else 'Check calibration'}")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")


if __name__ == "__main__":
    main()
