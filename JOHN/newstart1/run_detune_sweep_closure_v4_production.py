# run_detune_sweep_closure_v4_production.py
import numpy as np
import pandas as pd
import json
import os
import argparse
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
from geometry_package.universal_equation import w_gate
from geometry_package.absolute_constants import (
    SH_R_BAND_MIN,
    SH_R_BAND_MAX,
    SH_Q0_MIN,
    SH_Q0_MAX,
    CALIBRATED_SH_R_STAR,
    CALIBRATED_SH_Q0_STAR,
    CALIBRATED_SIGMA_L,
    CALIBRATED_SIGMA_R,
)

# ==============================================================================
# CONFIGURATION
# ==============================================================================
CONSTANTS_PATH = "out/geometry_constants_from_dist_all.json"
DIST_DATA_PATH = "out/dist_all_with_kappa.csv"

OUTPUT_DIR = "out/detune_closure_sweep_v4_production"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sweep grid
R0 = 0.1117
Q00 = 0.9750
R_SPAN = 0.0012
Q0_SPAN = 0.012
GRID_POINTS = 41  # 41x41 grid (override with --grid)
SEEDS_PER_CELL = 5

# ==============================================================================
# "SKELETON / PRODUCTION" CONSTANTS
# ==============================================================================
N_ROWS = 16
N_COLS = 16

SPARK_ANGLE_DEG = 138.88
SPARK_ANGLE_RAD = np.radians(SPARK_ANGLE_DEG)

# match skeleton
SPARK_LEAP_DIST = 2.5

F_1_32 = 1.0 / 32.0
COMPRESSION_GAP = 3.0 * F_1_32  # 3/32 lattice step

# Dynamics constants (keep as-is from v3 unless you already tuned them elsewhere)
REALITY_TENSION = 1.0
MALE_HORIZONTAL_AMP = 1.2
TORSION_4D = 0.02
GABA_C_V_APEX = 0.14

# Hysteresis
HYST_TAU_SCALE = 0.5
THRESHOLD_ON_FACTOR = 0.15
THRESHOLD_OFF_FACTOR = 0.3
ALPHA_MAX = 0.5
NIGHT_TAU_LAG = SPARK_ANGLE_DEG / 60.0  # kept from v3

# PRODUCTION spark gate
SPARK_FUNNEL_X_MIN = 6.0
SPARK_FUNNEL_X_MAX = 10.0
SPARK_GATE_Y_MIN   = 10.0

# allow multi-cycle observation (via wrap)
Y_WRAP = 32.0
T_MAX = 2000.0  # seconds (override with --t_max)
LAMBDA0 = 10.0

# ==============================================================================
# IO helpers
# ==============================================================================
def load_data():
    if not os.path.exists(CONSTANTS_PATH):
        # fallback band, if calibration json missing
        constants = {
            "calibrated": {
                "CALIBRATED_SH_BOUNDARY_MIN": 0.1116,
                "CALIBRATED_SH_BOUNDARY_MAX": 0.1126,
                "CALIBRATED_Q0_MIN": 0.961,
                "CALIBRATED_Q0_MAX": 0.983,
            }
        }
    else:
        with open(CONSTANTS_PATH, "r") as f:
            constants = json.load(f)

    if not os.path.exists(DIST_DATA_PATH):
        df = pd.DataFrame()
    else:
        df = pd.read_csv(DIST_DATA_PATH)

    return constants, df

def get_kappa_eff(r, q0, df: pd.DataFrame) -> float:
    if df.empty:
        return 1.0 / 32.0
    dists = np.sqrt((df["r"] - r) ** 2 + (df["q0"] - q0) ** 2)
    row = df.iloc[dists.idxmin()]
    if "kappa_tda" in row:
        return float(row["kappa_tda"])
    return 1.0 / 32.0

def check_in_band(r, q0, constants) -> bool:
    band = constants.get("calibrated", {})
    r_min = band.get("CALIBRATED_SH_BOUNDARY_MIN", 0.1116)
    r_max = band.get("CALIBRATED_SH_BOUNDARY_MAX", 0.1126)
    q0_min = band.get("CALIBRATED_Q0_MIN", 0.961)
    q0_max = band.get("CALIBRATED_Q0_MAX", 0.983)
    return (r_min <= r <= r_max) and (q0_min <= q0 <= q0_max)

# ==============================================================================
# Core field / operators
# ==============================================================================
def _v_shape(x, y):
    xn, yn = (x - 8.0) / 8.0, (y - 8.0) / 8.0
    return np.exp(-(xn**2 + yn**2) / (2 * (GABA_C_V_APEX ** 2)))

def universal_field(x, y):
    tx, ty = 3.2, 14.0
    d_terminal = np.sqrt((x - tx) ** 2 + (y - ty) ** 2)
    terminal = -2.5 * np.exp(-d_terminal**2 / (2 * 1.5**2))
    
    # Clamp y for drift to prevent explosion at large Y
    y_drift = min(float(y), 16.0)
    drift_x = -TORSION_4D * (y_drift - 8.0)
    drift_y = TORSION_4D * (x - 8.0)
    
    # Centering force in funnel
    centering = 0.0
    if y > 10.0:
        centering = -0.5 * (x - 8.0)

    return (terminal + drift_x + 1.35 * drift_y + 1.2 * _v_shape(x, y) + centering) * MALE_HORIZONTAL_AMP * REALITY_TENSION

def quantize_to_lattice(x: float) -> float:
    """3/32 lattice quantization around x=8."""
    return round((x - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0

def spark_refraction(x, y):
    # lattice snap at spark
    x_c = quantize_to_lattice(x)
    x_new = x_c + SPARK_LEAP_DIST * np.cos(SPARK_ANGLE_RAD)
    y_new = y   + SPARK_LEAP_DIST * np.sin(SPARK_ANGLE_RAD)
    # clamp
    x_new = max(0.0, min(float(N_COLS), float(x_new)))
    return x_new, float(y_new)

def analyze_cycles(trajectory, flashes):
    """Compute cycle statistics from switch_state and lag traces and spark intervals."""
    if not trajectory:
        return {}

    ts = np.array([p["t"] for p in trajectory])
    switch_seq = np.array([p["switch_state"] for p in trajectory], dtype=bool)
    lag_seq = np.array([p["lag"] for p in trajectory], dtype=float)

    # Switch-based transitions
    ft_indices = np.where((~switch_seq[:-1]) & (switch_seq[1:]))[0] + 1  # False->True
    tf_indices = np.where((switch_seq[:-1]) & (~switch_seq[1:]))[0] + 1  # True->False
    ft_times = ts[ft_indices] if ft_indices.size else np.array([])
    tf_times = ts[tf_indices] if tf_indices.size else np.array([])
    cycle_count_switch = min(len(ft_times), len(tf_times))

    durations_switch = []
    peak_lag_switch = []
    if cycle_count_switch > 0:
        for i in range(cycle_count_switch):
            start_idx = ft_indices[i]
            end_idx = tf_indices[i]
            if end_idx <= start_idx:
                continue
            durations_switch.append(ts[end_idx] - ts[start_idx])
            peak_lag_switch.append(np.max(np.abs(lag_seq[start_idx:end_idx+1])))

    # Lag sign based transitions (+ -> - -> +)
    lag_sign = np.sign(lag_seq)
    lag_sign[lag_sign == 0] = 1  # treat zero as positive to avoid stalling
    pos_to_neg = np.where((lag_sign[:-1] > 0) & (lag_sign[1:] < 0))[0] + 1
    neg_to_pos = np.where((lag_sign[:-1] < 0) & (lag_sign[1:] > 0))[0] + 1
    pt_times = ts[pos_to_neg] if pos_to_neg.size else np.array([])
    np_times = ts[neg_to_pos] if neg_to_pos.size else np.array([])
    cycle_count_lag = min(len(pos_to_neg), len(neg_to_pos))

    durations_lag = []
    peak_lag_lag = []
    if cycle_count_lag > 0:
        for i in range(cycle_count_lag):
            start_idx = pos_to_neg[i]
            end_idx = neg_to_pos[i]
            if end_idx <= start_idx:
                continue
            durations_lag.append(ts[end_idx] - ts[start_idx])
            peak_lag_lag.append(np.max(np.abs(lag_seq[start_idx:end_idx+1])))

    # Spark interval based estimate
    spark_ts = np.array([f["time"] for f in flashes]) if flashes else np.array([])
    spark_mode = np.nan
    cycle_est_spark = np.nan
    if spark_ts.size >= 2:
        intervals = np.diff(spark_ts)
        if intervals.size:
            hist, bin_edges = np.histogram(intervals, bins=min(10, max(2, intervals.size)))
            idx = int(np.argmax(hist))
            spark_mode = float(0.5 * (bin_edges[idx] + bin_edges[idx+1]))
            if spark_mode > 0:
                total_time = ts[-1] - ts[0]
                cycle_est_spark = float(total_time / spark_mode)

    def safe_stats(arr):
        if not arr:
            return (np.nan, np.nan)
        a = np.array(arr, dtype=float)
        return float(np.mean(a)), float(np.std(a))

    mean_dur_sw, std_dur_sw = safe_stats(durations_switch)
    mean_dur_lg, std_dur_lg = safe_stats(durations_lag)

    return {
        "cycles_switch": cycle_count_switch,
        "mean_dur_switch": mean_dur_sw,
        "std_dur_switch": std_dur_sw,
        "peak_lag_switch": peak_lag_switch,
        "cycles_lag": cycle_count_lag,
        "mean_dur_lag": mean_dur_lg,
        "std_dur_lag": std_dur_lg,
        "peak_lag_lag": peak_lag_lag,
        "spark_mode": spark_mode,
        "cycle_est_spark": cycle_est_spark,
    }

def _v_shape_vec(x, y, apex):
    """Vectorized gaussian bump used in universal_field_vec."""
    xn = (x - 8.0) / 8.0
    yn = (y - 8.0) / 8.0
    return np.exp(-(xn * xn + yn * yn) / (2.0 * (apex ** 2)))

def universal_field_vec(x, y,
                        male_horizontal_amp,
                        reality_tension,
                        torsion_4d,
                        gaba_c_v_apex):
    """Vectorized field matching scalar universal_field logic."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    tx, ty = 3.2, 14.0
    d2 = (x - tx) ** 2 + (y - ty) ** 2
    terminal = -2.5 * np.exp(-d2 / (2.0 * (1.5 ** 2)))

    # match scalar: clamp y for drift
    y_drift = np.minimum(y, 16.0)
    drift_x = -torsion_4d * (y_drift - 8.0)
    drift_y = torsion_4d * (x - 8.0)

    vshape = _v_shape_vec(x, y, gaba_c_v_apex)

    # match scalar: centering force in funnel
    centering = np.where(y > 10.0, -0.5 * (x - 8.0), 0.0)

    return (terminal + drift_x + 1.35 * drift_y + 1.2 * vshape + centering) * male_horizontal_amp * reality_tension

def run_sweep_vectorized(r_vals, q0_vals, seeds, lambda0, t_max, wg_mode="normal", deterministic=False, collect_turns=False):
    # Construct grid
    rr, qq = np.meshgrid(r_vals, q0_vals, indexing='ij')
    r_flat = np.repeat(rr.ravel(), seeds)
    q0_flat = np.repeat(qq.ravel(), seeds)
    
    n_particles = len(r_flat)
    print(f"Vectorized simulation: {n_particles} particles...")

    # Precompute w_gate
    print("Precomputing w_gate...")
    unique_coords, inverse = np.unique(np.column_stack((r_flat, q0_flat)), axis=0, return_inverse=True)
    w_unique = np.array([float(w_gate(row[0], row[1])) for row in unique_coords])
    if wg_mode == "ones":
        w_unique = np.ones_like(w_unique)
    elif wg_mode == "shuffle":
        rng_shuffle = np.random.default_rng(123)
        rng_shuffle.shuffle(w_unique)
    w_vals = w_unique[inverse]
    
    # State init
    x = np.full(n_particles, 8.0)
    y = np.full(n_particles, 0.0)
    memory_y = np.copy(y)
    switch_state = np.zeros(n_particles, dtype=bool)
    renorm = np.full(n_particles, 1.0)
    turn_idx = np.zeros(n_particles, dtype=int)
    acc = np.zeros(n_particles, dtype=float)  # for deterministic accumulator
    
    # Stats
    eligibleB_count = np.zeros(n_particles, dtype=int)
    sparks_B = np.zeros(n_particles, dtype=float)
    sum_p = np.zeros(n_particles, dtype=float)
    if collect_turns:
        turn_eligible = defaultdict(lambda: np.zeros(n_particles, dtype=int))
        turn_sparks = defaultdict(lambda: np.zeros(n_particles, dtype=float))
        turn_expected = defaultdict(lambda: np.zeros(n_particles, dtype=float))
    
    # Constants
    dt = 0.05
    steps = int(t_max / dt)
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * F_1_32
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    reset_val = 0.380657
    recovery_rate = 0.05
    
    for step in range(steps):
        if step % 5000 == 0:
            print(f"Step {step}/{steps}")
            
        # Hysteresis
        alpha_h = max(0.0, min(ALPHA_MAX, dt / (hyst_tau + 1e-6)))
        memory_y = (1.0 - alpha_h) * memory_y + alpha_h * y
        lag = memory_y - y
        
        # Switch
        to_on = (lag < threshold_on) & (~switch_state)
        switch_state[to_on] = True
        to_off = (lag > threshold_on * THRESHOLD_OFF_FACTOR) & (switch_state)
        switch_state[to_off] = False
        
        # Spark Check
        in_funnel = (y > SPARK_GATE_Y_MIN) & (x > SPARK_FUNNEL_X_MIN) & (x < SPARK_FUNNEL_X_MAX)
        eligible_mask = in_funnel & switch_state
        
        if np.any(eligible_mask):
            eligibleB_count[eligible_mask] += 1
            p = np.clip(lambda0 * w_vals[eligible_mask] * dt, 0.0, 1.0)
            sum_p[eligible_mask] += p
            if collect_turns:
                ti_all = turn_idx[eligible_mask]
                full_indices_all = np.where(eligible_mask)[0]
                for t in np.unique(ti_all):
                    m_t = eligible_mask & (turn_idx == t)
                    turn_eligible[t][m_t] += 1
                    turn_expected[t][m_t] += np.clip(lambda0 * w_vals[m_t] * dt, 0.0, 1.0)
            full_indices = np.where(eligible_mask)[0]

            if deterministic:
                acc[full_indices] += p
                trigger_count = np.floor(acc[full_indices]).astype(int)
                acc[full_indices] -= trigger_count
                spark_indices = full_indices[trigger_count > 0]
                trigger_weights = trigger_count[trigger_count > 0]
            else:
                rand_vals = np.random.random(np.count_nonzero(eligible_mask))
                triggered = rand_vals < p
                spark_indices = full_indices[triggered]
                trigger_weights = np.ones_like(spark_indices, dtype=float)
            
            if spark_indices.size > 0:
                sparks_B[spark_indices] += trigger_weights
                if collect_turns:
                    ti_s = turn_idx[spark_indices]
                    for t in np.unique(ti_s):
                        m_t = spark_indices[ti_s == t]
                        turn_sparks[t][m_t] += trigger_weights[ti_s == t]
                x_old = x[spark_indices]
                x_c = np.round((x_old - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
                x_new = x_c + SPARK_LEAP_DIST * np.cos(SPARK_ANGLE_RAD)
                y_new = y[spark_indices] + SPARK_LEAP_DIST * np.sin(SPARK_ANGLE_RAD)
                x[spark_indices] = np.clip(x_new, 0.0, float(N_COLS))
                y[spark_indices] = y_new
                renorm[spark_indices] = reset_val
                switch_state[spark_indices] = False
                memory_y[spark_indices] = y_new

        # Evolve
        vx = universal_field_vec(
            x,
            y,
            male_horizontal_amp=MALE_HORIZONTAL_AMP,
            reality_tension=REALITY_TENSION,
            torsion_4d=TORSION_4D,
            gaba_c_v_apex=GABA_C_V_APEX,
        )
        x += vx * renorm * dt
        y += 0.3 * dt
        renorm += (1.0 - renorm) * recovery_rate * dt
        x = np.clip(x, 0.0, float(N_COLS))
        
        wrap_mask = y > Y_WRAP
        if np.any(wrap_mask):
            y[wrap_mask] -= Y_WRAP
            memory_y[wrap_mask] = y[wrap_mask]
            switch_state[wrap_mask] = ~switch_state[wrap_mask]
            turn_idx[wrap_mask] += 1
            
    def summarize(r_arr, q_arr, elig_arr, sparks_arr, expected_arr):
        df_res = pd.DataFrame({
            "r": r_arr,
            "q0": q_arr,
            "eligibleB": elig_arr,
            "sparksB": sparks_arr,
            "expectedB": expected_arr
        })
        df_res["rate"] = df_res["sparksB"] / df_res["eligibleB"].replace(0, 1)
        df_res.loc[df_res["eligibleB"] == 0, "rate"] = 0.0
        df_res["rate_post"] = (df_res["sparksB"] + 1) / (df_res["eligibleB"] + 2)
        grp = df_res.groupby(["r", "q0"])
        summary_local = grp.agg({
            "eligibleB": ["mean", "std"],
            "sparksB": ["mean", "std"],
            "expectedB": "mean",
            "rate": ["mean", "std"],
            "rate_post": ["mean", "std"],
        }).reset_index()
        summary_local.columns = ['_'.join(col).strip() if col[1] else col[0] for col in summary_local.columns.values]
        w_df_local = pd.DataFrame({"r": unique_coords[:,0], "q0": unique_coords[:,1], "w_gate_sim": w_unique})
        summary_local = pd.merge(summary_local, w_df_local, on=["r", "q0"])
        summary_local = summary_local.rename(columns={
            "expectedB_mean": "expectedB_mean",
            "rate_mean": "rateB_eligible_mean",
            "rate_std": "rateB_eligible_std",
            "rate_post_mean": "rate_post_mean",
            "rate_post_std": "rate_post_std",
        })
        summary_local["mean_pB_mean"] = summary_local["expectedB_mean"] / summary_local["eligibleB_mean"].replace(0, 1)
        return summary_local

    summary = summarize(r_flat, q0_flat, eligibleB_count, sparks_B, sum_p)

    per_turn_summary = None
    if collect_turns:
        per_turn_rows = []
        for t, elig_arr in turn_eligible.items():
            sparks_arr = turn_sparks.get(t, np.zeros(n_particles, dtype=float))
            expected_arr = turn_expected.get(t, np.zeros(n_particles, dtype=float))
            sum_df = summarize(r_flat, q0_flat, elig_arr, sparks_arr, expected_arr)
            sum_df["turn"] = t
            per_turn_rows.append(sum_df)
        if per_turn_rows:
            per_turn_summary = pd.concat(per_turn_rows, ignore_index=True)

    return summary, per_turn_summary

# ==============================================================================
def _anchor_from_dist(df: pd.DataFrame):
    if df.empty:
        return None, None
    if "wasserstein_H1" in df:
        idx = df["wasserstein_H1"].idxmin()
    else:
        idx = 0
    row = df.loc[idx]
    return float(row["r"]), float(row["q0"])

def _compute_ridge(q_values, r_values, rate_grid, eligible_grid, min_eligible, alpha, ridge_window):
    mask_grid = eligible_grid >= min_eligible
    rate_masked = np.ma.array(rate_grid, mask=~mask_grid)
    R, Q = rate_grid.shape
    rate_eff = np.where(mask_grid, rate_grid, 0.0)
    EPS = 1e-6
    cost = np.full((R, Q), np.inf)
    back = np.full((R, Q), -1, dtype=int)
    cost[:, 0] = -np.log(rate_eff[:, 0] + EPS)
    for j in range(1, Q):
        for i in range(R):
            i0 = max(0, i - ridge_window)
            i1 = min(R, i + ridge_window + 1)
            prev = cost[i0:i1, j-1] + alpha * np.abs(np.arange(i0, i1) - i)
            k_rel = int(np.argmin(prev))
            k = i0 + k_rel
            cost[i, j] = prev[k_rel] - np.log(rate_eff[i, j] + EPS)
            back[i, j] = k
    end_idx = int(np.argmin(cost[:, -1]))
    ridge_indices = [end_idx]
    for j in range(Q-1, 0, -1):
        end_idx = back[end_idx, j]
        if end_idx < 0:
            end_idx = ridge_indices[-1]
        ridge_indices.append(end_idx)
    ridge_indices = ridge_indices[::-1]
    ridge_q = q_values
    ridge_r = r_values[ridge_indices]
    ridge_rate = rate_eff[ridge_indices, np.arange(Q)]
    ridge_elig = eligible_grid[ridge_indices, np.arange(Q)]
    return ridge_q, ridge_r, ridge_rate, ridge_elig, rate_masked, mask_grid

# ==============================================================================
def main():

    parser = argparse.ArgumentParser(description="2D detune mapping sweep with probabilistic LegB spark gate")
    parser.add_argument("--lambda0", type=float, default=LAMBDA0, help="Spark rate multiplier")
    parser.add_argument("--seeds", type=int, default=SEEDS_PER_CELL, help="Seeds per grid cell")
    parser.add_argument("--grid", type=int, default=GRID_POINTS, help="Grid points per axis (e.g., 21 or 41)")
    parser.add_argument("--t_max", type=float, default=T_MAX, help="Simulation duration (seconds)")
    parser.add_argument("--min_eligible", type=int, default=100, help="Mask cells with eligibleB_mean below this for ridge/plot")
    parser.add_argument("--wg_mode", type=str, default="normal", choices=["normal", "ones", "shuffle"], help="w_gate mode: normal, all-ones, or shuffled")
    parser.add_argument("--r_min", type=float, default=None, help="Override r min for sweep")
    parser.add_argument("--r_max", type=float, default=None, help="Override r max for sweep")
    parser.add_argument("--q0_min", type=float, default=None, help="Override q0 min for sweep")
    parser.add_argument("--q0_max", type=float, default=None, help="Override q0 max for sweep")
    parser.add_argument("--nr", type=int, default=None, help="Override r grid points (rows)")
    parser.add_argument("--nq0", type=int, default=None, help="Override q0 grid points (cols)")
    parser.add_argument("--alpha", type=float, default=0.15, help="Ridge DP jump penalty")
    parser.add_argument("--ridge_window", type=int, default=6, help="Ridge DP neighbor half-window in r-index")
    parser.add_argument("--out_csv", type=str, default=None, help="Override output CSV path")
    parser.add_argument("--out_png", type=str, default=None, help="Override output heatmap path")
    parser.add_argument("--deterministic", action="store_true", help="Use deterministic accumulator (RNG-free) for sparks")
    parser.add_argument("--per_turn", action="store_true", help="Collect per-turn (Y_WRAP) stats and ridge")
    parser.add_argument("--constants_out", type=str, default=os.path.join(OUTPUT_DIR, "constants_bundle.json"), help="Path to save anchor + closure constants bundle")
    args = parser.parse_args()

    lambda0 = args.lambda0
    seeds = args.seeds
    grid_points = args.grid
    t_max = args.t_max
    min_eligible = args.min_eligible
    wg_mode = args.wg_mode
    r_min = args.r_min
    r_max = args.r_max
    q0_min = args.q0_min
    q0_max = args.q0_max
    nr = args.nr
    nq0 = args.nq0
    alpha = args.alpha
    ridge_window = args.ridge_window
    deterministic = args.deterministic
    per_turn = args.per_turn
    constants_out = args.constants_out

    constants, df = load_data()

    r_lo = r_min if r_min is not None else (R0 - R_SPAN)
    r_hi = r_max if r_max is not None else (R0 + R_SPAN)
    q_lo = q0_min if q0_min is not None else (Q00 - Q0_SPAN)
    q_hi = q0_max if q0_max is not None else (Q00 + Q0_SPAN)

    r_points = nr if nr is not None else grid_points
    q_points = nq0 if nq0 is not None else grid_points

    r_values = np.linspace(r_lo, r_hi, r_points)
    q_values = np.linspace(q_lo, q_hi, q_points)

    rows = []
    rate_grid = np.zeros((grid_points, grid_points))
    w_grid = np.zeros((grid_points, grid_points))

    print(f"Running 2D sweep {r_points}x{q_points}, seeds={seeds}, lambda0={lambda0}, t_max={t_max}, wg_mode={wg_mode}")

    # Run Vectorized Sweep
    summary_df, per_turn_df = run_sweep_vectorized(
        r_values,
        q_values,
        seeds,
        lambda0,
        t_max,
        wg_mode=wg_mode,
        deterministic=deterministic,
        collect_turns=per_turn,
    )
    
    # Add auxiliary columns
    summary_df["lambda0"] = lambda0
    summary_df["seeds"] = seeds
    summary_df["kappa_eff"] = summary_df.apply(lambda row: get_kappa_eff(row["r"], row["q0"], df), axis=1)
    summary_df["in_band"] = summary_df.apply(lambda row: check_in_band(row["r"], row["q0"], constants), axis=1)
    
    # Prepare for plotting
    # Reshape metrics to grid. Assumes groupby sorted by r then q0.
    sorted_df = summary_df.sort_values(["r", "q0"])
    rate_grid = sorted_df["rate_post_mean"].values.reshape(len(r_values), len(q_values))
    w_grid = sorted_df["w_gate_sim"].values.reshape(len(r_values), len(q_values))
    eligible_grid = sorted_df["eligibleB_mean"].values.reshape(len(r_values), len(q_values))

    ridge_q, ridge_r, ridge_rate, ridge_elig, rate_masked, mask_grid = _compute_ridge(
        q_values, r_values, rate_grid, eligible_grid, min_eligible, alpha, ridge_window
    )

    out_csv = args.out_csv or os.path.join(OUTPUT_DIR, f"map2d_lambda{lambda0:.3f}.csv")
    summary_df.to_csv(out_csv, index=False)

    out_png = args.out_png or os.path.join(OUTPUT_DIR, f"map2d_lambda{lambda0:.3f}.png")
    plt.figure(figsize=(9, 7))
    extent = [q_values.min(), q_values.max(), r_values.min(), r_values.max()]
    plt.imshow(rate_masked, origin='lower', aspect='auto', extent=extent, cmap='magma')

    plt.colorbar(label='rateB_eligible')

    # SH band overlay
    plt.axhspan(SH_R_BAND_MIN, SH_R_BAND_MAX, color='cyan', alpha=0.15, label='SH r-band')
    plt.axvspan(SH_Q0_MIN, SH_Q0_MAX, color='lime', alpha=0.12, label='SH q0-band')

    # w_gate contour at 0.5
    cs = plt.contour(q_values, r_values, w_grid, levels=[0.5], colors='white', linewidths=1.2)
    plt.clabel(cs, fmt='w_gate=0.5', inline=True, fontsize=8)

    plt.plot(ridge_q, ridge_r, color='deepskyblue', lw=1.6, label='rate ridge (DP)')

    plt.xlabel('q0')
    plt.ylabel('r')
    plt.title(f'LegB spark rate (lambda0={lambda0}, min_eligible={min_eligible})')

    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

    ridge_out = out_csv.replace('.csv', '_ridge.csv')
    ridge_df = pd.DataFrame({
        "q0": ridge_q,
        "r": ridge_r,
        "rate_post": ridge_rate,
        "eligible": ridge_elig,
    })
    ridge_df.to_csv(ridge_out, index=False)

    print(f"Saved CSV: {out_csv}")
    print(f"Saved ridge CSV: {ridge_out}")
    print(f"Saved heatmap: {out_png}")

    # Per-turn ridge export
    if per_turn and per_turn_df is not None:
        per_turn_sorted = per_turn_df.sort_values(["turn", "r", "q0"])
        per_turn_csv = out_csv.replace('.csv', '_per_turn.csv')
        per_turn_sorted.to_csv(per_turn_csv, index=False)
        print(f"Saved per-turn CSV: {per_turn_csv}")
        for t in sorted(per_turn_sorted["turn"].unique()):
            df_t = per_turn_sorted[per_turn_sorted["turn"] == t]
            rate_t = df_t["rate_post_mean"].values.reshape(len(r_values), len(q_values))
            elig_t = df_t["eligibleB_mean"].values.reshape(len(r_values), len(q_values))
            rq, rr, rrates, relig, _, _ = _compute_ridge(q_values, r_values, rate_t, elig_t, min_eligible, alpha, ridge_window)
            ridge_t_out = out_csv.replace('.csv', f'_turn{t}_ridge.csv')
            pd.DataFrame({
                "q0": rq,
                "r": rr,
                "rate_post": rrates,
                "eligible": relig,
                "turn": t,
            }).to_csv(ridge_t_out, index=False)
            print(f"Saved turn ridge CSV: {ridge_t_out}")

    # Constants bundle export
    R_REF, Q0_REF = _anchor_from_dist(df)
    constants_bundle = {
        "anchor_from_dist_all": {
            "R_REF": R_REF,
            "Q0_REF": Q0_REF,
        },
        "closure_ridge": {
            "r_star": CALIBRATED_SH_R_STAR,
            "q0_star": CALIBRATED_SH_Q0_STAR,
            "sigma_L": CALIBRATED_SIGMA_L,
            "sigma_R": CALIBRATED_SIGMA_R,
        },
    }
    with open(constants_out, "w") as f:
        json.dump(constants_bundle, f, indent=2)
    print(f"Saved constants bundle: {constants_out}")

    print("Done.")

if __name__ == "__main__":
    main()