import numpy as np
import pandas as pd
import argparse
from geometry_package.universal_equation import w_gate
from run_detune_sweep_closure_v4_production import universal_field_vec, SPARK_GATE_Y_MIN, SPARK_FUNNEL_X_MIN, SPARK_FUNNEL_X_MAX, COMPRESSION_GAP, SPARK_LEAP_DIST, SPARK_ANGLE_RAD, N_COLS, Y_WRAP, ALPHA_MAX, NIGHT_TAU_LAG, HYST_TAU_SCALE, F_1_32, THRESHOLD_ON_FACTOR, THRESHOLD_OFF_FACTOR

def run_trace(r, q0, lambda0, t_max, seed):
    # Setup
    seeds = 200
    n_particles = seeds
    
    # Precompute w_gate
    w_val = float(w_gate(r, q0))
    w_vals = np.full(n_particles, w_val)
    
    x = np.full(n_particles, 8.0)
    y = np.full(n_particles, 0.0)
    memory_y = np.copy(y)
    switch_state = np.zeros(n_particles, dtype=bool)
    renorm = np.full(n_particles, 1.0)
    
    events = []
    
    dt = 0.05
    steps = int(t_max / dt)
    
    hyst_tau = (NIGHT_TAU_LAG / HYST_TAU_SCALE) * F_1_32
    threshold_on = -hyst_tau * THRESHOLD_ON_FACTOR
    reset_val = 0.380657
    recovery_rate = 0.05
    
    print(f"Running trace r={r}, q0={q0}, particles={n_particles}")
    
    for step in range(steps):
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
            p = np.clip(lambda0 * w_vals[eligible_mask] * dt, 0.0, 1.0)
            
            rand_vals = np.random.random(np.count_nonzero(eligible_mask))
            triggered = rand_vals < p
            full_indices = np.where(eligible_mask)[0]
            spark_indices = full_indices[triggered]
            
            if spark_indices.size > 0:
                x_old = x[spark_indices]
                x_c = np.round((x_old - 8.0) / COMPRESSION_GAP) * COMPRESSION_GAP + 8.0
                x_new = x_c + SPARK_LEAP_DIST * np.cos(SPARK_ANGLE_RAD)
                y_new = y[spark_indices] + SPARK_LEAP_DIST * np.sin(SPARK_ANGLE_RAD)
                
                # Log events
                current_time = step * dt
                x_new_clipped = np.clip(x_new, 0.0, float(N_COLS))
                for i in range(len(spark_indices)):
                    events.append({
                        "t": float(current_time),
                        "x_before": float(x_old[i]),
                        "y_before": float(y[spark_indices][i]),
                        "x_after": float(x_new_clipped[i]),
                        "y_after": float(y_new[i]),
                    })

                x[spark_indices] = x_new_clipped
                y[spark_indices] = y_new
                renorm[spark_indices] = reset_val
                switch_state[spark_indices] = False
                memory_y[spark_indices] = y_new

        # Evolve
        vx = universal_field_vec(
            x, y,
            male_horizontal_amp=1.2,
            reality_tension=1.0,
            torsion_4d=0.02,
            gaba_c_v_apex=0.14
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
            
    return events

def main():
    # Center of the ridge from calibration
    r_star = 0.11214750
    q0_star = 0.977738
    
    events = run_trace(r_star, q0_star, lambda0=10.0, t_max=2000.0, seed=42)
    
    print(f"Collected {len(events)} spark events.")
    
    # Analyze Alignment
    U = []
    for e in events:
        dx = e["x_after"] - e["x_before"]
        dy = e["y_after"] - e["y_before"]
        v = np.array([dx, dy], float)
        n = np.linalg.norm(v)
        if n > 0:
            U.append(v/n)
            
    if U:
        U = np.vstack(U)
        m = U.mean(axis=0)
        score = float(np.linalg.norm(m))
        print(f"BEAM ALIGNMENT SCORE: {score:.6f}")
        print(f"Mean Vector: {m}")
    else:
        print("No events.")

if __name__ == "__main__":
    main()
