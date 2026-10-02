from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import time

import numpy as np

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
        import pandas as pd

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


def _ts_from_c30(c30: np.ndarray) -> dict:
    c = np.asarray(c30, dtype=float).ravel()
    if c.size < 30:
        c = np.pad(c, (0, 30 - c.size))
    return {
        "noradrenaline": float(fclean.NOR_5_32) * float(np.clip(c[h24.RAW_CHANNEL_IDX["female_left_noradrenaline"]], 0.0, 1.0)),
        "vasopressin": float(fclean.PLP_3_32) * float(np.clip(c[h24.RAW_CHANNEL_IDX["vasopressin_female"]], 0.0, 1.0)),
        "alpha2": float(np.clip(c[h24.RAW_CHANNEL_IDX["right_alpha_2"]], 0.0, 1.0)),
        "nu_p_coupling": 0.5,
        "nu_e_coupling": 0.5,
    }


def _eval_score(c30: np.ndarray, x8_ref: np.ndarray, hour: float, self_level: float, economy_level: float, universe_level: float) -> dict:
    u_base, d_risk = h24.project_channels(c30)
    d = h24.build_time_condition_vector(
        hour=float(hour),
        self_level=float(self_level),
        economy_level=float(economy_level),
        universe_level=float(universe_level),
    )
    ts = _ts_from_c30(c30)
    z_proxy = float(max(0.0, float(x8_ref[2]) + float(x8_ref[4])))
    phase_lock, gate = fclean.continuous_spark_gate(z_proxy, ts.get("alpha2", 1.0), ts)
    spark_c = SPARK_CONSTANT_C * float(gate)
    actual_d3, confinement, perceived_d3 = h24._d3_core(np.asarray(x8_ref, dtype=float)[:8], np.asarray(c30, dtype=float), float(gate))
    spark_eff = float(phase_lock) * float(gate)
    score = float(spark_eff / (1.0 + float(actual_d3) + float(d_risk)))
    return {
        "score": score,
        "gate": float(gate),
        "phase_lock": float(phase_lock),
        "spark_eff": float(spark_eff),
        "d3_actual": float(actual_d3),
        "d3_confinement": float(confinement),
        "d3_perceived": float(perceived_d3),
        "d_risk": float(d_risk),
        "spark_c_mag": float(abs(spark_c)),
        "u_mag": float(np.linalg.norm(np.asarray(u_base, dtype=float) + float(abs(spark_c)))),
    }


def _tick(*, base_c30: np.ndarray, self_level: float, economy_level: float, universe_level: float, topk: int) -> None:
    now = _dt.datetime.now()
    hour = float(now.hour) + float(now.minute) / 60.0 + float(now.second) / 3600.0
    if _is_hysteresis(hour, hyst_start=float(getattr(_tick, "hyst_start", 1.5)), hyst_end=float(getattr(_tick, "hyst_end", 4.5))):
        phase_name = "hysteresis"
        states = k8.resolve_phase_states("hysteresis", keep_ambiguous_no_control=True, ambiguity_tol=5e-2)
    else:
        phase_name = _phase_for_hour(hour)
        states = k8.day_phase_states() if phase_name == "day" else k8.night_phase_states()
    c30 = _apply_phase_to_base(base_c30, states, no_control_value=0.5)

    x0 = np.linspace(0.85, 1.20, h24.N) * (h24.OMEGA / np.sqrt(h24.N))
    x8_ref = np.asarray(x0, dtype=float)[:8]

    base = _eval_score(c30, x8_ref, hour, self_level, economy_level, universe_level)

    no_control = [ch for ch, st in states.items() if st == "no_control"]
    print("")
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] phase={phase_name} hour={hour:.2f}")
    if no_control:
        print(f"no_control({len(no_control)}): {', '.join(no_control)}")
    print(
        "base:"
        f" gate={base['gate']:.3f} phase_lock={base['phase_lock']:.3f} spark_eff={base['spark_eff']:.3f}"
        f" d3={base['d3_actual']:.3f} d_risk={base['d_risk']:.3f} score={base['score']:.4f}"
    )

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
    moves: list[tuple[float, str, float]] = []
    for ch in candidates:
        if ch not in h24.RAW_CHANNEL_IDX:
            continue
        idx = int(h24.RAW_CHANNEL_IDX[ch])
        current = float(c30[idx])
        best_score = float(base["score"])
        best_val = current
        for val in (0.0, 1.0):
            if abs(val - current) <= 1e-9:
                continue
            c_try = c30.copy()
            c_try[idx] = float(val)
            sc = float(_eval_score(c_try, x8_ref, hour, self_level, economy_level, universe_level)["score"])
            if sc > best_score:
                best_score = sc
                best_val = float(val)
        delta = float(best_score - float(base["score"]))
        if delta > 1e-9:
            moves.append((delta, ch, best_val))
    moves.sort(reverse=True)

    print(f"recommend(top {int(max(1, topk))}):")
    for delta, ch, val in moves[: int(max(1, topk))]:
        print(f"  +{delta:.4f}: set {ch} -> {val:.0f}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Live (or one-shot) spark planner tick based on the 30-node phase map.")
    ap.add_argument("--base-c30", type=str, default="", help="optional base vector for no_control channels (.json or .csv)")
    ap.add_argument("--self", dest="self_level", type=float, default=0.88)
    ap.add_argument("--economy", dest="economy_level", type=float, default=0.72)
    ap.add_argument("--universe", dest="universe_level", type=float, default=0.93)
    ap.add_argument("--topk", type=int, default=6)
    ap.add_argument("--hyst-start", type=float, default=1.5, help="hysteresis window start hour (0..24)")
    ap.add_argument("--hyst-end", type=float, default=4.5, help="hysteresis window end hour (0..24)")
    ap.add_argument("--watch", action="store_true", help="run forever")
    ap.add_argument("--interval-min", type=float, default=90.0, help="watch-only: sleep interval")
    args = ap.parse_args()

    base_c30 = np.full(30, 0.5, dtype=float)
    if str(args.base_c30).strip():
        base_c30 = _load_c30(str(args.base_c30))

    _tick.hyst_start = float(args.hyst_start)  # type: ignore[attr-defined]
    _tick.hyst_end = float(args.hyst_end)      # type: ignore[attr-defined]

    while True:
        _tick(
            base_c30=base_c30,
            self_level=float(args.self_level),
            economy_level=float(args.economy_level),
            universe_level=float(args.universe_level),
            topk=int(args.topk),
        )
        if not bool(args.watch):
            break
        time.sleep(max(1.0, float(args.interval_min)) * 60.0)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
