from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
import pandas as pd

from absolute_constants import SPARK_CONSTANT_C
import engineering_homeostasis_24 as h24
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
            pass
    return np.clip(c, 0.0, 1.0)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run a 24h day/night cycle using the 30-node phase map.")
    ap.add_argument("--steps", type=int, default=128, help="steps per day (unless --steps-per-day is provided)")
    ap.add_argument("--days", type=int, default=1)
    ap.add_argument("--steps-per-day", type=int, default=0, help="override steps/day; 0 means use --steps")
    ap.add_argument("--dt", type=float, default=0.20)
    ap.add_argument("--x-clip", type=float, default=8.0, help="clip X after each step to [-x_clip, x_clip]")
    ap.add_argument("--self", dest="self_level", type=float, default=0.88)
    ap.add_argument("--economy", dest="economy_level", type=float, default=0.72)
    ap.add_argument("--universe", dest="universe_level", type=float, default=0.93)
    ap.add_argument("--out", type=str, default="analysis_results/phase30_day_night_cycle.csv")
    ap.add_argument("--base-c30", type=str, default="", help="optional base vector for no_control channels (.json or .csv)")
    ap.add_argument("--hyst-start", type=float, default=1.5, help="hysteresis window start hour (0..24)")
    ap.add_argument("--hyst-end", type=float, default=4.5, help="hysteresis window end hour (0..24)")
    args = ap.parse_args()

    day_states = k8.day_phase_states()
    night_states = k8.night_phase_states()
    hyst_states = k8.resolve_phase_states("hysteresis", keep_ambiguous_no_control=True, ambiguity_tol=5e-2)

    base_c30 = np.full(30, 0.5, dtype=float)
    if str(args.base_c30).strip():
        base_c30 = _load_c30(str(args.base_c30))

    model = h24.Homeostasis24.build()
    x = np.linspace(0.85, 1.20, h24.N) * (h24.OMEGA / np.sqrt(h24.N))
    r = np.zeros(8, dtype=float)

    steps_per_day = int(args.steps_per_day) if int(args.steps_per_day) > 0 else int(args.steps)
    days = int(max(1, args.days))
    total_steps = int(days * steps_per_day)

    rows: list[dict] = []
    for step in range(total_steps):
        day = int(step // steps_per_day)
        step_in_day = int(step % steps_per_day)
        hour = 24.0 * float(step_in_day) / max(1.0, float(steps_per_day))
        hour_abs = 24.0 * float(day) + float(hour)
        if _is_hysteresis(hour, hyst_start=float(args.hyst_start), hyst_end=float(args.hyst_end)):
            phase = "hysteresis"
            states = hyst_states
        else:
            phase = _phase_for_hour(hour)
            states = day_states if phase == "day" else night_states
        c30 = _apply_phase_to_base(base_c30, states, no_control_value=0.5)
        u24, d_risk = h24.project_channels(c30)
        d = h24.build_time_condition_vector(
            hour=hour,
            self_level=float(args.self_level),
            economy_level=float(args.economy_level),
            universe_level=float(args.universe_level),
        )

        dx = model.derivative(x, u24, d, r=r, d_risk=d_risk, spark_c=SPARK_CONSTANT_C, c26_raw=c30)
        rows.append(
            {
                "step": step,
                "day": int(day),
                "hour": hour,
                "hour_abs": float(hour_abs),
                "phase": phase,
                "x_norm": float(np.linalg.norm(x)),
                "dx_norm": float(np.linalg.norm(dx)),
                "d_risk": float(d_risk),
            }
        )

        x = model.rk4_step(
            x,
            u24,
            d,
            dt=float(args.dt),
            r=r,
            d_risk=d_risk,
            spark_c=SPARK_CONSTANT_C,
            c26_raw=c30,
        )
        x = np.clip(x, -float(args.x_clip), float(args.x_clip))
        r = h24.step_risk_memory(r, d_risk, dt=float(args.dt))

    df = pd.DataFrame(rows)
    df.to_csv(str(args.out), index=False)
    print(f"Wrote {args.out}")
    print(f"day_no_control={sum(v=='no_control' for v in day_states.values())}")
    print(f"night_no_control={sum(v=='no_control' for v in night_states.values())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
