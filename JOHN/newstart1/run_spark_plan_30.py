from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
import pandas as pd

from absolute_constants import SPARK_CONSTANT_C
import engineering_homeostasis_24 as h24
import fusion_clean as fclean
import fusion_core as k8


def _phase_for_hour(hour: float) -> str:
    hh = float(hour) % 24.0
    return "day" if 6.0 <= hh < 18.0 else "night"


def _is_hysteresis(hour: float, *, hyst_start: float, hyst_end: float) -> bool:
    hh = float(hour) % 24.0
    return float(hyst_start) <= hh < float(hyst_end)


def _load_c30(path: str) -> np.ndarray:
    p = pathlib.Path(str(path))
    if not p.exists():
        raise FileNotFoundError(str(p))

    if p.suffix.lower() == ".json":
        payload = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return np.asarray(payload, dtype=float)
        if isinstance(payload, dict):
            c = np.full(30, 0.5, dtype=float)
            for key, val in payload.items():
                if key not in h24.RAW_CHANNEL_IDX:
                    continue
                c[int(h24.RAW_CHANNEL_IDX[key])] = float(val)
            return c
        raise TypeError("base-c30 json must be a list[float] or {channel: value}")

    if p.suffix.lower() == ".csv":
        df = pd.read_csv(str(p))
        if {"channel", "value"} <= set(df.columns):
            c = np.full(30, 0.5, dtype=float)
            for _, row in df.iterrows():
                ch = str(row["channel"])
                if ch not in h24.RAW_CHANNEL_IDX:
                    continue
                c[int(h24.RAW_CHANNEL_IDX[ch])] = float(row["value"])
            return c

        if len(df.index) >= 1:
            return np.asarray(df.iloc[0].to_numpy(dtype=float), dtype=float)
        raise ValueError("base-c30 csv is empty")

    raise ValueError(f"Unsupported base-c30 format: {p.suffix} (use .json or .csv)")


def _apply_phase_to_base(c30_base: np.ndarray, states: dict[str, str], *, no_control_value: float = 0.5) -> np.ndarray:
    c = np.asarray(c30_base, dtype=float).ravel()
    if c.size < 30:
        c = np.pad(c, (0, 30 - c.size), constant_values=float(no_control_value))
    c = c[:30].copy()
    for ch, st in states.items():
        if ch not in h24.RAW_CHANNEL_IDX:
            continue
        idx = int(h24.RAW_CHANNEL_IDX[ch])
        if st == "on":
            c[idx] = 1.0
        elif st == "off":
            c[idx] = 0.0
        elif st == "no_control":
            # keep base value
            pass
    return np.clip(c, 0.0, 1.0)


def _ts_from_c30(c30: np.ndarray) -> dict:
    c = np.asarray(c30, dtype=float).ravel()
    if c.size < 30:
        c = np.pad(c, (0, 30 - c.size))
    return {
        # gate inputs (scaled to canonical magnitudes)
        "noradrenaline": float(fclean.NOR_5_32) * float(np.clip(c[h24.RAW_CHANNEL_IDX["female_left_noradrenaline"]], 0.0, 1.0)),
        "vasopressin": float(fclean.PLP_3_32) * float(np.clip(c[h24.RAW_CHANNEL_IDX["vasopressin_female"]], 0.0, 1.0)),
        "alpha2": float(np.clip(c[h24.RAW_CHANNEL_IDX["right_alpha_2"]], 0.0, 1.0)),  # numeric: alpha2_active = 1-alpha2
        # z_proxy components (minimal; can be overridden per-person)
        "nu_p_coupling": 0.5,
        "nu_e_coupling": 0.5,
    }


def _score(gate: float, phase: float, actual_d3: float, d_risk: float) -> float:
    spark_eff = float(phase) * float(gate)
    return float(spark_eff / (1.0 + float(actual_d3) + float(d_risk)))


def main() -> int:
    ap = argparse.ArgumentParser(description="Spark planner from 30-node day/night phase maps.")
    ap.add_argument("--steps", type=int, default=128, help="steps per day (unless --steps-per-day is provided)")
    ap.add_argument("--days", type=int, default=1)
    ap.add_argument("--steps-per-day", type=int, default=0, help="override steps/day; 0 means use --steps")
    ap.add_argument("--dt", type=float, default=0.20)
    ap.add_argument("--self", dest="self_level", type=float, default=0.88)
    ap.add_argument("--economy", dest="economy_level", type=float, default=0.72)
    ap.add_argument("--universe", dest="universe_level", type=float, default=0.93)
    ap.add_argument("--out", type=str, default="analysis_results/spark_plan_30.csv")
    ap.add_argument("--topk", type=int, default=8)
    ap.add_argument("--base-c30", type=str, default="", help="optional base vector for no_control channels (.json or .csv)")
    ap.add_argument("--d3-burn-gain", type=float, default=8.0, help="Debt model: burn = d3_burn_gain * spark_eff")
    ap.add_argument("--hyst-start", type=float, default=1.5, help="Debt model: hysteresis window start hour (0..24)")
    ap.add_argument("--hyst-end", type=float, default=4.5, help="Debt model: hysteresis window end hour (0..24)")
    ap.add_argument(
        "--mode",
        type=str,
        default="static",
        choices=("static", "dynamic"),
        help="static: evaluate gate/D3 on a fixed reference state; dynamic: integrate full 24D+8D system (can overflow).",
    )
    ap.add_argument("--x-clip", type=float, default=8.0, help="dynamic-only: clip X after each step to [-x_clip, x_clip].")
    ap.add_argument("--recommend", action="store_true", help="Print channel recommendations for top windows.")
    args = ap.parse_args()

    day_states = k8.day_phase_states()
    night_states = k8.night_phase_states()
    hyst_states = k8.resolve_phase_states("hysteresis", keep_ambiguous_no_control=True, ambiguity_tol=5e-2)

    base_c30 = np.full(30, 0.5, dtype=float)
    if str(args.base_c30).strip():
        base_c30 = _load_c30(str(args.base_c30))

    model = h24.Homeostasis24.build()
    x0 = np.linspace(0.85, 1.20, h24.N) * (h24.OMEGA / np.sqrt(h24.N))
    x = x0.copy()
    r = np.zeros(8, dtype=float)

    steps_per_day = int(args.steps_per_day) if int(args.steps_per_day) > 0 else int(args.steps)
    days = int(max(1, args.days))
    total_steps = int(days * steps_per_day)
    dt_hours = 24.0 / float(max(1, steps_per_day))

    debt_cum = 0.0
    debt_cum_hyst = 0.0

    rows: list[dict] = []
    for step in range(total_steps):
        day = int(step // steps_per_day)
        step_in_day = int(step % steps_per_day)
        hour = 24.0 * float(step_in_day) / max(1.0, float(steps_per_day))
        hour_abs = 24.0 * float(day) + float(hour)
        if _is_hysteresis(hour, hyst_start=float(args.hyst_start), hyst_end=float(args.hyst_end)):
            phase_name = "hysteresis"
            states = hyst_states
        else:
            phase_name = _phase_for_hour(hour)
            states = day_states if phase_name == "day" else night_states
        c30 = _apply_phase_to_base(base_c30, states, no_control_value=0.5)

        u_base, d_risk = h24.project_channels(c30)
        d = h24.build_time_condition_vector(
            hour=hour,
            self_level=float(args.self_level),
            economy_level=float(args.economy_level),
            universe_level=float(args.universe_level),
        )

        ts = _ts_from_c30(c30)
        x_ref = x0 if str(args.mode) == "static" else x
        z_proxy = float(max(0.0, float(x_ref[2]) + float(x_ref[4])))  # minimal SM+SW proxy
        phase, gate = fclean.continuous_spark_gate(z_proxy, ts.get("alpha2", 1.0), ts)
        spark_c = SPARK_CONSTANT_C * float(gate)

        # align with fusion_clean.step_unified_dynamics: u = u_base + |spark_c|
        u = np.asarray(u_base, dtype=float) + float(abs(spark_c))

        actual_d3, confinement, perceived_d3 = h24._d3_core(np.asarray(x_ref, dtype=float)[:8], np.asarray(c30, dtype=float), float(gate))
        score = _score(float(gate), float(phase), float(actual_d3), float(d_risk))

        # Debt/accumulation model (purely internal to this repo model)
        spark_eff = float(phase) * float(gate)
        burn = float(args.d3_burn_gain) * float(spark_eff)
        debt_step = float(max(0.0, float(actual_d3) - burn)) * float(dt_hours)
        debt_cum += float(debt_step)
        in_hyst = _is_hysteresis(hour, hyst_start=float(args.hyst_start), hyst_end=float(args.hyst_end))
        if bool(in_hyst):
            debt_cum_hyst += float(debt_step)

        dx = model.derivative(x_ref, u, d, r=r, d_risk=d_risk, spark_c=spark_c, c26_raw=c30)
        q, g, nu, ph, el, hi, w, z = (float(v) for v in np.asarray(x_ref, dtype=float)[:8])
        rows.append(
            {
                "step": step,
                "day": int(day),
                "hour": float(hour),
                "hour_abs": float(hour_abs),
                "phase": phase_name,
                "gate": float(gate),
                "phase_lock": float(phase),
                "spark_eff": float(phase) * float(gate),
                "d_risk": float(d_risk),
                "d3_actual": float(actual_d3),
                "d3_confinement": float(confinement),
                "d3_perceived": float(perceived_d3),
                "burn": float(burn),
                "debt_step": float(debt_step),
                "debt_cum": float(debt_cum),
                "debt_cum_hyst": float(debt_cum_hyst),
                "in_hyst": int(bool(in_hyst)),
                "score": float(score),
                "x_norm": float(np.linalg.norm(x)),
                "dx_norm": float(np.linalg.norm(dx)),
                "q": q,
                "g": g,
                "nu": nu,
                "ph": ph,
                "el": el,
                "hi": hi,
                "w": w,
                "z": z,
            }
        )

        if str(args.mode) == "dynamic":
            x = model.rk4_step(
                x,
                u,
                d,
                dt=float(args.dt),
                r=r,
                d_risk=float(d_risk),
                spark_c=spark_c,
                c26_raw=c30,
            )
            x = np.clip(x, -float(args.x_clip), float(args.x_clip))
            r = h24.step_risk_memory(r, float(d_risk), dt=float(args.dt))

    df = pd.DataFrame(rows)
    df.to_csv(str(args.out), index=False)

    topk = int(max(1, args.topk))
    top = df.sort_values("score", ascending=False).head(topk)
    print(f"Wrote {args.out}")
    print(f"day_no_control={sum(v=='no_control' for v in day_states.values())}")
    print(f"night_no_control={sum(v=='no_control' for v in night_states.values())}")
    print("Top windows by score:")
    for _, row in top.iterrows():
        print(
            f"  day={int(row['day'])} hour={row['hour']:.2f} phase={row['phase']} gate={row['gate']:.3f} "
            f"spark_eff={row['spark_eff']:.3f} d3={row['d3_actual']:.3f} "
            f"d_risk={row['d_risk']:.3f} score={row['score']:.4f}"
        )

    # Debt-focused report
    top_debt = df.sort_values("debt_step", ascending=False).head(topk)
    print("Top windows by debt_step:")
    for _, row in top_debt.iterrows():
        print(
            f"  day={int(row['day'])} hour={row['hour']:.2f} phase={row['phase']} "
            f"debt_step={row['debt_step']:.4f} burn={row['burn']:.3f} d3={row['d3_actual']:.3f} "
            f"in_hyst={int(row['in_hyst'])}"
        )

    if bool(args.recommend):
        candidates = [
            "right_alpha_2",
            "female_left_noradrenaline",
            "vasopressin_female",
            "male_right_extraversion",
            "gdh_gluon",
            "right_acetylcholine",
            "male_gaba_a",
            "left_eyelid_couple",
            "right_eyelid_couple",
            "hypoxia",
        ]
        print("Recommendations (single-channel set to 0/1, evaluated on that window's state):")
        for _, row in top.iterrows():
            phase_name = str(row["phase"])
            if phase_name == "hysteresis":
                states = hyst_states
            else:
                states = day_states if phase_name == "day" else night_states
            c30_base = _apply_phase_to_base(base_c30, states, no_control_value=0.5)
            x_ref = np.array([row[k] for k in ("q", "g", "nu", "ph", "el", "hi", "w", "z")], dtype=float)
            z_proxy = float(max(0.0, float(x_ref[2]) + float(x_ref[4])))

            def eval_score(c30: np.ndarray) -> float:
                _u_base, _d_risk = h24.project_channels(c30)
                _ts = _ts_from_c30(c30)
                _phase, _gate = fclean.continuous_spark_gate(z_proxy, _ts.get("alpha2", 1.0), _ts)
                _spark_c = SPARK_CONSTANT_C * float(_gate)
                _u = np.asarray(_u_base, dtype=float) + float(abs(_spark_c))
                _actual_d3, *_ = h24._d3_core(x_ref, np.asarray(c30, dtype=float), float(_gate))
                return _score(float(_gate), float(_phase), float(_actual_d3), float(_d_risk))

            base_score = eval_score(c30_base)
            best_moves: list[tuple[float, str, float]] = []
            for ch in candidates:
                if ch not in h24.RAW_CHANNEL_IDX:
                    continue
                idx = int(h24.RAW_CHANNEL_IDX[ch])
                best_val = float(c30_base[idx])
                best_score = base_score
                for val in (0.0, 1.0):
                    if abs(val - float(c30_base[idx])) <= 1e-9:
                        continue
                    c30 = c30_base.copy()
                    c30[idx] = val
                    sc = eval_score(c30)
                    if sc > best_score:
                        best_score = sc
                        best_val = float(val)
                delta = float(best_score - base_score)
                if delta > 1e-9:
                    best_moves.append((delta, ch, best_val))
            best_moves.sort(reverse=True)
            print(f"  day={int(row['day'])} hour={row['hour']:.2f} phase={phase_name} base_score={base_score:.4f}")
            for delta, ch, val in best_moves[:6]:
                print(f"    +{delta:.4f}: set {ch} -> {val:.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
