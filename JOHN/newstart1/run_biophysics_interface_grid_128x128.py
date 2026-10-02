import argparse
import json
import math
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mandelbrot_vein_mapper import EPSILON0, SPARK_ANGLE_RAD, _epsilon_extra_value, _leak_value, iterate_kernel


@dataclass(frozen=True)
class WindowParams:
    window: int
    u_male_gaba_b: float
    u_right_occipitalis_gaba_a: float
    u_female_left_noradrenaline: float
    collapse_proxy_source: str
    collapse_proxy_value: float
    leak_return: float
    epsilon_extra_total: float
    c_gain: float


def _probe_points(grid: int = 4, span: float = 1.2) -> list[complex]:
    xs = np.linspace(-span, span, grid)
    pts: list[complex] = []
    for x in xs:
        for y in xs:
            pts.append(complex(float(x), float(y)))
    return pts


def _safe_float(val: object, default: float = 0.0) -> float:
    try:
        if val is None:
            return float(default)
        x = float(val)
        if not math.isfinite(x):
            return float(default)
        return x
    except Exception:
        return float(default)


def _window_params(
    row: pd.Series,
    base_leak: float,
    base_epsilon_extra: float,
    leak_return_scale: float,
    epsilon_mask_scale: float,
    c_gain_scale: float,
    collapse_col: str | None,
) -> WindowParams:
    window = int(row["window"])
    u_mgb = _safe_float(row.get("u_male_gaba_b", 0.0))
    u_gabaa = _safe_float(row.get("u_right_occipitalis_gaba_a", 0.0))
    u_nor = _safe_float(row.get("u_female_left_noradrenaline", 0.0))

    collapse_proxy_source = "stress_proxy(glucocorticoid,cortisol)"
    collapse_proxy_value = 0.5 * (
        _safe_float(row.get("u_glucocorticoid", 0.0)) + _safe_float(row.get("u_right_cortisol", 0.0))
    )
    if collapse_col:
        if collapse_col in row.index:
            collapse_proxy_source = collapse_col
            collapse_proxy_value = _safe_float(row.get(collapse_col, 0.0))

    leak_return = leak_return_scale * u_mgb * (1.0 / 128.0)

    epsilon_mask = epsilon_mask_scale * u_gabaa * float(EPSILON0)
    epsilon_extra_total = base_epsilon_extra + epsilon_mask

    c_gain = 1.0 + c_gain_scale * u_nor

    return WindowParams(
        window=window,
        u_male_gaba_b=u_mgb,
        u_right_occipitalis_gaba_a=u_gabaa,
        u_female_left_noradrenaline=u_nor,
        collapse_proxy_source=collapse_proxy_source,
        collapse_proxy_value=float(collapse_proxy_value),
        leak_return=float(leak_return),
        epsilon_extra_total=float(epsilon_extra_total),
        c_gain=float(c_gain),
    )


def _load_sim_d3_grid(
    path: str,
    *,
    window_col: str,
    n_col: str,
    d3_col: str,
) -> np.ndarray | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None

    df = pd.read_csv(p)
    for col in (window_col, n_col, d3_col):
        if col not in df.columns:
            raise ValueError(f"Simulation results missing required column: {col!r} (path={str(p)!r})")

    w = df[window_col].astype(int).to_numpy()
    n = df[n_col].astype(int).to_numpy()
    d3 = df[d3_col].astype(float).to_numpy()

    grid = np.full((128, 128), np.nan, dtype=float)
    ok = (w >= 0) & (w < 128) & (n >= 1) & (n <= 128) & np.isfinite(d3)
    grid[w[ok], n[ok] - 1] = d3[ok]
    return grid


def _probe_metrics(
    probes: Iterable[complex],
    c_eff: complex,
    leak: float,
    epsilon_extra: float,
    max_iter: int,
    escape_r: float,
) -> tuple[float, float]:
    pots = []
    escaped = 0
    for z0 in probes:
        pot = float(
            iterate_kernel(
                z0,
                None,
                plane="julia",
                mode="mandelbrot",
                julia_c_override=c_eff,
                max_iter=int(max_iter),
                escape_r=float(escape_r),
                leak=float(leak),
                epsilon_extra=float(epsilon_extra),
            )
        )
        pots.append(pot)
        if pot < float(max_iter):
            escaped += 1
    mean_pot = float(np.mean(pots)) if pots else float("nan")
    escape_frac = float(escaped / max(1, len(pots)))
    return mean_pot, escape_frac


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a 128x128 bio/physics interface grid by modulating the canonical kernel with bio channels."
    )
    parser.add_argument("--bio-schedule", default="HOMEOSTASIS_24_SCHEDULE_128.csv")
    parser.add_argument(
        "--sim-results",
        default="analysis_results/CONSCIOUSNESS_FIELD_128x128.csv",
        help="Optional: simulation results CSV that provides per-cell d3_actual (step x archetype_n).",
    )
    parser.add_argument("--sim-window-col", default="step", help="Simulation results window column (default: step)")
    parser.add_argument("--sim-n-col", default="archetype_n", help="Simulation results n column (default: archetype_n)")
    parser.add_argument("--sim-d3-col", default="d3_actual", help="Simulation results d3 column (default: d3_actual)")
    parser.add_argument("--out", default="analysis_results/veins_pocket_tunnel/interface_128/grid_128x128")
    parser.add_argument("--base-leak", choices=["none", "locked", "derived"], default="locked")
    parser.add_argument("--base-epsilon", choices=["none", "resid_5_32", "pi_over_20_minus_5_32"], default="resid_5_32")
    parser.add_argument("--leak-return-scale", type=float, default=1.0)
    parser.add_argument("--epsilon-mask-scale", type=float, default=1.0)
    parser.add_argument("--c-gain-scale", type=float, default=1.0)
    parser.add_argument("--collapse-scale", type=float, default=0.02)
    parser.add_argument(
        "--collapse-col",
        default="",
        help=(
            "Optional: use this bio schedule column as collapse proxy driver (used only when sim d3 is missing); "
            "defaults to stress proxy based on glucocorticoid+cortisol."
        ),
    )
    parser.add_argument("--probes-grid", type=int, default=4, help="Probe grid per axis (total = grid^2)")
    parser.add_argument("--probes-span", type=float, default=1.2, help="Probe span in Julia plane")
    parser.add_argument("--max-iter", type=int, default=80)
    parser.add_argument("--escape-r", type=float, default=10.0)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    df_bio = pd.read_csv(args.bio_schedule)
    if "window" not in df_bio.columns:
        raise ValueError("bio schedule must include 'window' column (0..127).")
    df_bio = df_bio.copy()
    df_bio["window"] = df_bio["window"].astype(int)
    df_bio = df_bio.sort_values("window").reset_index(drop=True)
    if df_bio["window"].tolist() != list(range(128)):
        raise ValueError("bio schedule must cover window=0..127 exactly.")

    base_leak = float(_leak_value(args.base_leak))
    base_epsilon_extra = float(_epsilon_extra_value(args.base_epsilon))
    collapse_col = str(args.collapse_col).strip() or None
    sim_d3_grid = _load_sim_d3_grid(
        str(args.sim_results).strip(),
        window_col=str(args.sim_window_col),
        n_col=str(args.sim_n_col),
        d3_col=str(args.sim_d3_col),
    )
    sim_available = sim_d3_grid is not None and int(np.isfinite(sim_d3_grid).sum()) > 0

    probes = _probe_points(grid=int(args.probes_grid), span=float(args.probes_span))

    windows = [
        _window_params(
            row=row,
            base_leak=base_leak,
            base_epsilon_extra=base_epsilon_extra,
            leak_return_scale=float(args.leak_return_scale),
            epsilon_mask_scale=float(args.epsilon_mask_scale),
            c_gain_scale=float(args.c_gain_scale),
            collapse_col=collapse_col,
        )
        for _, row in df_bio.iterrows()
    ]

    rows = []
    mean_pot_real = np.zeros((128, 128), dtype=float)
    mean_pot_ray = np.zeros((128, 128), dtype=float)
    escape_real = np.zeros((128, 128), dtype=float)
    escape_ray = np.zeros((128, 128), dtype=float)

    spark_ray_unit = complex(math.cos(SPARK_ANGLE_RAD), math.sin(SPARK_ANGLE_RAD))

    t0 = time.perf_counter()
    sim_used_cells = 0
    for w in windows:
        for n in range(1, 129):
            collapse_source = str(w.collapse_proxy_source)
            collapse_value = float(w.collapse_proxy_value)
            if sim_available:
                d3 = float(sim_d3_grid[w.window, n - 1])
                if math.isfinite(d3):
                    collapse_source = f"sim:{str(args.sim_d3_col)}"
                    collapse_value = d3
                    sim_used_cells += 1

            leak_total = base_leak + float(w.leak_return) + float(args.collapse_scale) * float(collapse_value)

            c_base = float(n) / 128.0
            c_gain = float(w.c_gain)

            c_eff_real = complex(c_gain * c_base, 0.0)
            c_eff_ray = (c_gain * c_base) * spark_ray_unit

            mp_real, ef_real = _probe_metrics(
                probes=probes,
                c_eff=c_eff_real,
                leak=leak_total,
                epsilon_extra=w.epsilon_extra_total,
                max_iter=int(args.max_iter),
                escape_r=float(args.escape_r),
            )
            mp_ray, ef_ray = _probe_metrics(
                probes=probes,
                c_eff=c_eff_ray,
                leak=leak_total,
                epsilon_extra=w.epsilon_extra_total,
                max_iter=int(args.max_iter),
                escape_r=float(args.escape_r),
            )

            mean_pot_real[w.window, n - 1] = mp_real
            mean_pot_ray[w.window, n - 1] = mp_ray
            escape_real[w.window, n - 1] = ef_real
            escape_ray[w.window, n - 1] = ef_ray

            rows.append(
                {
                    "window": int(w.window),
                    "n": int(n),
                    "c_base": float(c_base),
                    "c_gain": float(c_gain),
                    "u_male_gaba_b": float(w.u_male_gaba_b),
                    "u_right_occipitalis_gaba_a": float(w.u_right_occipitalis_gaba_a),
                    "u_female_left_noradrenaline": float(w.u_female_left_noradrenaline),
                    "collapse_source": str(collapse_source),
                    "collapse_value": float(collapse_value),
                    "collapse_proxy_source": str(w.collapse_proxy_source),
                    "collapse_proxy_value": float(w.collapse_proxy_value),
                    "leak_total": float(leak_total),
                    "epsilon_extra_total": float(w.epsilon_extra_total),
                    "mean_potential_real": float(mp_real),
                    "escape_frac_real": float(ef_real),
                    "mean_potential_spark_ray": float(mp_ray),
                    "escape_frac_spark_ray": float(ef_ray),
                    "delta_mean_potential": float(mp_ray - mp_real),
                    "delta_escape_frac": float(ef_ray - ef_real),
                }
            )

        # progress line
        print(
            f"window={w.window:3d} leak_base={base_leak + w.leak_return:.6f} eps_extra={w.epsilon_extra_total:.6f} "
            f"c_gain={w.c_gain:.4f} collapse_proxy={w.collapse_proxy_value:.6f}"
        )

    seconds = float(time.perf_counter() - t0)

    out_csv = out_dir / "biophysics_interface_grid_128x128.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)

    def _save_heatmap(arr: np.ndarray, title: str, fname: str, vmin=None, vmax=None) -> None:
        plt.figure(figsize=(12, 7))
        plt.imshow(arr, aspect="auto", origin="lower", cmap="magma", vmin=vmin, vmax=vmax)
        plt.colorbar()
        plt.title(title)
        plt.xlabel("particle n (1..128)")
        plt.ylabel("bio window (0..127)")
        plt.tight_layout()
        plt.savefig(out_dir / fname, dpi=160)
        plt.close()

    _save_heatmap(mean_pot_real, "Mean escape potential (real c=n/128)", "mean_potential_real.png")
    _save_heatmap(mean_pot_ray, "Mean escape potential (spark_ray c=(n/128)e^{i·138.88°})", "mean_potential_spark_ray.png")
    _save_heatmap(escape_real, "Escape fraction (real c=n/128)", "escape_frac_real.png", vmin=0.0, vmax=1.0)
    _save_heatmap(escape_ray, "Escape fraction (spark_ray)", "escape_frac_spark_ray.png", vmin=0.0, vmax=1.0)
    _save_heatmap(
        mean_pot_ray - mean_pot_real,
        "Δ mean potential (spark_ray - real)",
        "delta_mean_potential.png",
    )

    meta = {
        "bio_schedule": str(args.bio_schedule),
        "sim_results": str(args.sim_results),
        "sim_columns": {"window": str(args.sim_window_col), "n": str(args.sim_n_col), "d3": str(args.sim_d3_col)},
        "sim_used_cells": int(sim_used_cells),
        "out": str(out_dir),
        "base_leak_mode": args.base_leak,
        "base_leak_value": float(base_leak),
        "base_epsilon_mode": args.base_epsilon,
        "base_epsilon_extra": float(base_epsilon_extra),
        "epsilon0": float(EPSILON0),
        "spark_angle_rad": float(SPARK_ANGLE_RAD),
        "probe_points": {"grid": int(args.probes_grid), "span": float(args.probes_span), "count": int(len(probes))},
        "kernel": {"max_iter": int(args.max_iter), "escape_r": float(args.escape_r)},
        "mapping_scales": {
            "leak_return_scale": float(args.leak_return_scale),
            "epsilon_mask_scale": float(args.epsilon_mask_scale),
            "c_gain_scale": float(args.c_gain_scale),
            "collapse_scale": float(args.collapse_scale),
            "collapse_col": collapse_col,
        },
        "runtime_seconds": seconds,
        "outputs": {
            "grid_csv": str(out_csv),
            "mean_potential_real_png": str(out_dir / "mean_potential_real.png"),
            "mean_potential_spark_ray_png": str(out_dir / "mean_potential_spark_ray.png"),
            "escape_frac_real_png": str(out_dir / "escape_frac_real.png"),
            "escape_frac_spark_ray_png": str(out_dir / "escape_frac_spark_ray.png"),
            "delta_mean_potential_png": str(out_dir / "delta_mean_potential.png"),
        },
    }
    (out_dir / "biophysics_interface_grid_128x128_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\nWrote: {out_csv}")
    print(f"Wrote: {out_dir / 'biophysics_interface_grid_128x128_meta.json'}")
    print(f"Runtime: {seconds:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
